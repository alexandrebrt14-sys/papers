"""citation_match.py — does an answer cite a given site? A URL match, no judgment.

Learned from the treg ``ai-visibility`` recipe: whether an engine *cited* a
brand's site needs no language model. It is a comparison between the brand's
domain and the hosts of the sources the engine exposed. The hard part is only
normalization, because answer engines rarely hand back a clean URL:

- ``https://WWW.Nubank.com.br:443/conta/?utm_source=chatgpt.com`` (case, www,
  port, tracking parameters);
- ``https://www.google.com/url?q=https://nubank.com.br/&sa=U`` (redirector);
- ``https://blog.nubank.com.br/...`` (subdomain of the brand's domain);
- ``https://notnubank.com.br`` (must NOT match ``nubank.com.br``).

This module is stricter than ``failure_classifier._entity_in_sources``, which
matches an entity *slug* as a substring of the URL (useful as a proxy when no
domain is known). Here the brand's domain is known and the host must be equal to
it or be one of its subdomains.

Pure functions, no network: an encrypted redirect (Google ``/goto``, Vertex AI
grounding links) that cannot be resolved offline is reported as unresolved,
never guessed.
"""
from __future__ import annotations

import base64
import binascii
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

# Query parameters that only track the click and never change the page.
TRACKING_PARAMS: frozenset[str] = frozenset({
    "gclid", "gclsrc", "dclid", "gbraid", "wbraid", "fbclid", "msclkid",
    "yclid", "mc_cid", "mc_eid", "igshid", "srsltid", "_hsenc", "_hsmi",
    "mkt_tok", "ref_src", "spm",
})
TRACKING_PREFIXES: tuple[str, ...] = ("utm_",)

# Host prefixes that are the same site as the bare domain.
_SAME_SITE_PREFIXES: tuple[str, ...] = ("www.", "www2.", "www3.", "m.", "amp.")

# Redirectors whose target sits in a query parameter.
_REDIRECT_PARAMS: dict[str, tuple[str, ...]] = {
    "google.": ("q", "url", "u"),          # google.com/url, google.com.br/url
    "l.facebook.com": ("u",),
    "lm.facebook.com": ("u",),
    "l.instagram.com": ("u",),
    "out.reddit.com": ("url",),
    "duckduckgo.com": ("uddg",),
    "r.search.yahoo.com": ("RU",),
    "href.li": (),
}

# Redirectors whose target is encrypted and cannot be read offline.
_OPAQUE_REDIRECT_HOSTS: tuple[str, ...] = (
    "vertexaisearch.cloud.google.com",     # Gemini grounding-api-redirect
    "t.co",
    "lnkd.in",
)

_MAX_UNWRAP_DEPTH = 4
# google.com, www.google.com.br, google.co.uk; not notgoogle.com.
_GOOGLE_HOST = re.compile(r"^(?:[a-z0-9-]+\.)*google\.(?:com|co|[a-z]{2})(?:\.[a-z]{2})?$")


def _ensure_scheme(url: str) -> str:
    url = url.strip()
    if url.startswith("//"):
        return "https:" + url
    if "://" not in url:
        return "https://" + url
    return url


def normalize_host(url_or_host: str) -> str:
    """Return the comparable host of a URL or bare host.

    Lowercases, drops credentials, port, trailing dot and same-site prefixes
    (``www.``, ``m.``, ``amp.``). Internationalized hosts are converted to their
    Unicode form so ``xn--`` and accented spellings compare equal.
    Returns ``""`` when there is no host.
    """
    if not url_or_host:
        return ""
    try:
        netloc = urlsplit(_ensure_scheme(str(url_or_host))).netloc
    except ValueError:
        return ""
    host = netloc.rsplit("@", 1)[-1]
    if host.startswith("["):  # IPv6 literal
        host = host.split("]", 1)[0] + "]"
    else:
        host = host.split(":", 1)[0]
    host = host.strip().rstrip(".").lower()
    if "xn--" in host:
        try:
            host = host.encode("ascii").decode("idna")
        except (UnicodeError, ValueError):
            pass
    changed = True
    while changed:
        changed = False
        for prefix in _SAME_SITE_PREFIXES:
            if host.startswith(prefix) and host.count(".") >= 2:
                host = host[len(prefix):]
                changed = True
    return host


def strip_tracking(url: str) -> str:
    """Remove click-tracking query parameters (``utm_*``, ``gclid``...) and the fragment."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url
    kept = [
        (k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if k.lower() not in TRACKING_PARAMS and not k.lower().startswith(TRACKING_PREFIXES)
    ]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), ""))


def _bing_target(query: Mapping[str, str]) -> str | None:
    """bing.com/ck/a?u=a1<base64url> carries the target base64-encoded after ``a1``."""
    raw = query.get("u", "")
    if not raw.startswith("a1"):
        return None
    payload = raw[2:]
    payload += "=" * (-len(payload) % 4)
    try:
        return base64.urlsafe_b64decode(payload).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None


def unwrap_redirect(url: str) -> tuple[str, bool]:
    """Follow known redirectors offline.

    Returns ``(target_url, resolved)``. ``resolved`` is False only when the URL
    is an encrypted redirect whose destination cannot be known without a
    network call; the input is then returned unchanged.
    """
    current = _ensure_scheme(url)
    for _ in range(_MAX_UNWRAP_DEPTH):
        try:
            parts = urlsplit(current)
        except ValueError:
            return current, True
        host = parts.netloc.lower().split(":", 1)[0]
        query = dict(parse_qsl(parts.query, keep_blank_values=True))

        if any(host == h or host.endswith("." + h) for h in _OPAQUE_REDIRECT_HOSTS):
            return current, False
        is_google = bool(_GOOGLE_HOST.match(host))
        if is_google and parts.path.startswith("/goto"):
            return current, False  # encrypted Google redirect (AI Mode, SERP)

        target: str | None = None
        if "bing.com" in host and parts.path.startswith("/ck/"):
            target = _bing_target(query)
        else:
            for marker, params in _REDIRECT_PARAMS.items():
                if marker == "google.":
                    applies = is_google and parts.path in ("/url", "/imgres")
                else:
                    applies = host == marker or host.endswith("." + marker)
                if applies:
                    for p in params:
                        value = query.get(p, "")
                        if value.lower().startswith(("http%3a", "https%3a")):
                            value = unquote(value)  # double-encoded target
                        if value.startswith(("http://", "https://", "//")):
                            target = value
                            break
                if target:
                    break
        if not target:
            return current, True
        current = _ensure_scheme(target)
    return current, True


def canonical_url(url: str) -> str:
    """Unwrap redirectors, drop tracking and normalize the host. Empty input -> ``""``."""
    if not url or not str(url).strip():
        return ""
    target, _ = unwrap_redirect(str(url))
    clean = strip_tracking(target)
    try:
        parts = urlsplit(clean)
    except ValueError:
        return clean
    path = parts.path.rstrip("/") or ""
    return urlunsplit(("https", normalize_host(clean), path, parts.query, ""))


def host_matches_domain(host: str, domain: str, include_subdomains: bool = True) -> bool:
    """True when ``host`` is ``domain`` or (optionally) one of its subdomains.

    Label-aware: ``notnubank.com.br`` does not match ``nubank.com.br``.
    """
    h = normalize_host(host)
    d = normalize_host(domain)
    if not h or not d:
        return False
    if h == d:
        return True
    return include_subdomains and h.endswith("." + d)


def source_urls(sources: Iterable[Any] | None) -> list[str]:
    """Extract URL strings from the shapes engines return.

    Accepts plain strings or dicts carrying ``url``, ``link``, ``uri`` or
    ``href`` (Cloro ``sources`` / ``citationPills``, Perplexity ``citations``,
    Gemini grounding chunks as ``{"web": {"uri": ...}}``).
    """
    urls: list[str] = []
    for s in sources or ():
        if isinstance(s, str):
            if s.strip():
                urls.append(s.strip())
        elif isinstance(s, Mapping):
            for key in ("url", "link", "uri", "href"):
                value = s.get(key)
                if isinstance(value, str) and value.strip():
                    urls.append(value.strip())
                    break
            else:
                web = s.get("web")
                if isinstance(web, Mapping) and isinstance(web.get("uri"), str):
                    urls.append(web["uri"].strip())
    return urls


@dataclass(frozen=True)
class CitationMatch:
    """Result of checking one domain against one answer's sources."""
    domain: str
    cited: bool
    matched_urls: tuple[str, ...] = field(default_factory=tuple)
    unresolved_redirects: int = 0

    @property
    def undetermined(self) -> bool:
        """No match, but some sources could not be resolved offline."""
        return not self.cited and self.unresolved_redirects > 0


def find_citation(
    sources: Iterable[Any] | None,
    domain: str,
    include_subdomains: bool = True,
) -> CitationMatch:
    """Check whether any source of an answer points at ``domain``.

    ``cited`` is a plain URL fact. When it is False but some sources were
    encrypted redirects, ``undetermined`` is True: the correct reading is "not
    known", and a caller that needs certainty can resolve those links with a
    separate (paid or network) step.
    """
    matched: list[str] = []
    unresolved = 0
    seen: set[str] = set()
    for raw in source_urls(sources):
        target, resolved = unwrap_redirect(raw)
        if not resolved:
            unresolved += 1
            continue
        canon = canonical_url(target)
        if canon in seen:
            continue
        seen.add(canon)
        if host_matches_domain(target, domain, include_subdomains):
            matched.append(canon)
    return CitationMatch(
        domain=normalize_host(domain),
        cited=bool(matched),
        matched_urls=tuple(matched),
        unresolved_redirects=unresolved,
    )
