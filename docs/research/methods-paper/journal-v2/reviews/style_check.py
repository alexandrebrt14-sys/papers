#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
style_check.py — medidor da PARTE C de research/R4-standards.md.

Conta, nao opina. Toda regra com limiar vira um numero medido contra o limiar.
Escopo: prosa corrida dos blocos A a D. Ficam fora do denominador de prosa:
tabelas, blocos de codigo, titulos, listas de referencia, legendas de tabela e
figura, especificacoes de figura, a secao "Reference keys used" e a secao
"Anti-tic pass" (que e declaracao do redator, auditada a parte).

Uso:  python style_check.py [--json]
"""

import re
import sys
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = os.path.join(os.path.dirname(HERE), "sections")

FILES = [
    ("A", "A-front-intro-related.md"),
    ("B", "B-specification-instantiation-adoption.md"),
    ("C", "C-field-record-missingness.md"),
    ("D", "D-window-decoys.md"),
    ("E", "E-findings-index-plan.md"),
    ("F", "F-governance-threats-discussion.md"),
]

# ---------------------------------------------------------------- lexicos

FILLER_OPENERS = [  # C.1.3 — FALHA ao abrir paragrafo
    "Moreover", "Furthermore", "Additionally", "It is worth noting that",
    "It is important to note that", "In this context", "In this regard",
    "That said", "Notably", "Importantly",
]

TRANSITION_OPENERS = [  # C.2 — AVISO ao abrir paragrafo
    "However", "In contrast", "On the other hand", "In summary",
    "Finally", "Overall", "Thus", "Consequently",
]

EMPTY_ADJ = [  # C.1.10
    "robust", "crucial", "strategic", "transformative", "disruptive",
    "powerful", "innovative", "essential", "pivotal", "seamless",
    "comprehensive", "cutting-edge", "state-of-the-art", "significant",
]

INTENSIFIERS = ["extremely", "highly", "entirely", "truly", "basically"]  # C.2

WORDY = {  # C.2
    "due to the fact that": "because",
    "in order to": "to",
    "with regard to": "about",
    "in the realm of": "in",
    "a number of": "de o numero",
    "it should be emphasized that": "cortar",
}

COPULA_EVASION = ["serves as", "acts as", "functions as",
                  "positions itself as", "plays the role of"]  # C.2

VAGUE_GERUND = ["contributing to", "paving the way for", "facilitating",
                "fostering", "enabling"]  # C.2

NOMINALIZATION = ["the implementation of the", "the utilization of",
                  "the operationalization of"]  # C.2

SOURCE_INTRODUCERS = ["according to", "as shown by"]  # C.2 (>1 / 120 palavras)

C6 = [  # C.6 — 40 entradas
    "delve into", "it is worth noting that", "it is important to note that",
    "in today's rapidly evolving landscape", "this study aims to shed light on",
    "sheds light on", "sheds new light on", "plays a crucial role in",
    "a testament to", "navigating the complexities of", "rich tapestry",
    "tapestry of", "underscores the importance of", "showcases", "showcasing",
    "intricate", "meticulous", "meticulously", "pivotal", "crucial", "vital",
    "robust", "comprehensive overview", "state-of-the-art", "cutting-edge",
    "paradigm shift", "leverage", "utilize", "seamless", "seamlessly",
    "holistic", "multifaceted", "myriad", "a plethora of", "foster",
    "fostering", "has garnered significant attention", "ever-growing",
    "ever-increasing", "bridge the gap", "not only", "as previously mentioned",
    "in the realm of", "embark on", "unlock the potential of", "game-changer",
    "to the best of our knowledge", "in conclusion", "ultimately, this underscores",
]

# C.1.1 — formas fechadas de antitese
ANTITHESIS = [
    (r"\bnot merely\b[^.]{0,80}\bbut\b", "not merely X but Y"),
    (r"\bit is not about\b[^.]{0,80}\bit is about\b", "it is not about X, it is about Y"),
    (r"\b(?:this|that|it) is not\b[^.;:]{0,80}[;:]\s*it is\b", "this is not X; it is Y"),
    (r"\bis not the problem\b", "X is not the problem, Y is the problem"),
    (r"\bless about\b[^.]{0,60}\band more about\b", "less about X and more about Y"),
    (r"\bfar from being\b", "far from being X"),
    (r"\bnot only\b[^.]{0,80}\bbut also\b", "not only X but also Y"),
    (r"\bthe question is not whether\b[^.]{0,40}\bbut\b", "the question is not whether, but when"),
    (r"\bmore than\b[^.,]{0,40},\s*this is\b", "more than X, this is Y"),
]

# C.1.1 — forma graduada: "is not X: it is Y" / "is not X, it is Y"
ANTITHESIS_GRAD = [
    (r"\bis not\b[^.;:]{1,90}[:;]\s*(?:it|they|this|that)\s+(?:is|are)\b",
     "is not X: it is Y"),
    (r"\bis not\b[^.;:]{1,90},\s*(?:it|they|this|that)\s+(?:is|are)\b",
     "is not X, it is Y"),
    (r"\bis not\s+\w[^.;:]{0,60};\s*it\s+is\b", "is not X; it is Y"),
    # variante com adverbio intercalado: "is therefore not X; it is Y"
    (r"\b(?:is|are)\s+(?:therefore|thus|not merely|simply|just|only|also|\w+ly)\s+not\b"
     r"[^.;:]{1,90}[:;,]\s*(?:it|they|this|that)\s+(?:is|are)\b",
     "is <adv> not X; it is Y"),
]

PSEUDO_CLOSERS = [  # C.1.2
    "the future is already here", "this changes everything",
    "the best is yet to come", "one thing is certain", "this is only the beginning",
    "the writing is on the wall", "at the end of the day",
]

SELF_NARRATION = [  # C.1.5
    "this paper presents", "this study aims to", "the present article seeks to",
    "in this work, we will explore", "this paper proposes", "this article presents",
    "the contribution of this paper", "this paper makes", "this section will discuss",
    "in this paper we", "we present", "this paper argues",
]

VERIFICATION_META = [  # C.1.6
    "we verified that", "after extensive research", "sources consulted",
    "our methodology suggests", "as calculated using our approach",
    "data were checked", "we checked", "we confirmed",
]

PREAMBLE = [  # C.1.4
    "before we begin", "in this document", "it is important to contextualize",
    "first of all", "in what follows we present", "this section will discuss",
]

ALERT_LABELS = ["Note:", "Important:", "Caveat:", "Disclaimer:", "Warning:"]  # C.1.12

VAGUE_ATTRIBUTION = [  # C.1.8
    "studies show", "research suggests", "experts agree", "it is widely believed",
    "the literature indicates", "recent work has shown",
]

ERRATA = [  # C.1.14
    "an earlier version of this paper", "corrected figures", "updated on",
    "manuscript v1.0", "the v1.0", "published v1.0", "v1.0 reported",
    "v1.0 avoided", "v1.0 described", "v1.0 carried", "v1.0 event table",
    "declared in v1.0", "in v1.0",
]

# --------------------------------------------------------------- extracao


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def split_prose(raw):
    """Devolve (paragrafos_de_prosa, linhas_aparato, secoes)."""
    lines = raw.split("\n")
    prose_lines, apparatus = [], []
    sections = []          # (heading, indice do paragrafo em que comeca)
    in_code = False
    stop = False
    display_items = 0
    for ln in lines:
        s = ln.strip()
        if s.startswith("```"):
            in_code = not in_code
            apparatus.append(ln)
            continue
        if in_code:
            apparatus.append(ln)
            continue
        if re.match(r"^#{1,6}\s", s):
            title = re.sub(r"^#{1,6}\s+", "", s)
            if re.match(r"(?i)^(anti-tic pass|reference keys used|"
                        r"provenance note|keys referenced|"
                        r"open marks and number provenance|"
                        r"notes for the integrator)", title):
                stop = True
                continue
            stop = False
            sections.append((title, len(prose_lines)))
            prose_lines.append("")          # quebra de paragrafo
            prose_lines.append("@@HEAD@@" + title)
            prose_lines.append("")
            continue
        if stop:
            continue
        if s.startswith("|") or s.startswith("---") or s == "":
            if s.startswith("|"):
                apparatus.append(ln)
            prose_lines.append("")
            continue
        if re.match(r"^\*\*(Table|Figure)\s", s) or re.match(r"^\*Panel\s", s):
            display_items += 1
            apparatus.append(ln)
            prose_lines.append("")
            continue
        if re.match(r"^[-*+]\s", s) or re.match(r"^\[\w+\d{4}", s) or \
           re.match(r"^\*\*\[\w+", s):
            apparatus.append(ln)
            prose_lines.append("")
            continue
        if re.match(r"^\*This subsection is (normative|informative)", s) or \
           re.match(r"^\*\*Keywords", s) or re.match(r"^\*\*JEL", s) or \
           re.match(r"^\*\*Alexandre", s) or s.startswith("Brasil GEO,") or \
           s.startswith("Custodian of the specification"):
            apparatus.append(ln)
            prose_lines.append("")
            continue
        prose_lines.append(ln)

    blob = "\n".join(prose_lines)
    chunks = [c.strip() for c in re.split(r"\n\s*\n", blob) if c.strip()]
    paras, heads = [], []
    cur_head = "(front matter)"
    for c in chunks:
        if c.startswith("@@HEAD@@"):
            cur_head = c[len("@@HEAD@@"):]
            continue
        paras.append((cur_head, re.sub(r"\s+", " ", c)))
    return paras, apparatus, sections, display_items


def strip_markup(t):
    t = re.sub(r"`[^`]*`", " CODE ", t)
    t = re.sub(r"\[[^\]\[]{2,60}\]", " ", t)          # chaves de citacao
    t = re.sub(r"\*\*|\*|_", "", t)
    return t


def words(t):
    return re.findall(r"[A-Za-z][A-Za-z'À-ſ-]*", t)


def sentences(t):
    t = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", t)
    t = re.sub(r"\b(§|no|No|vs|e\.g|i\.e|cf|pp|Fig|Eq|Dr|St)\.", r"\1<DOT>", t)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ſ§])", t)
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


def count_ci(hay, needle):
    return len(re.findall(r"(?<![A-Za-z])" + re.escape(needle) + r"(?![A-Za-z])",
                          hay, re.I))


# ------------------------------------------------------------------ medir

def analyse(tag, path):
    raw = load(path)
    paras, apparatus, sections, display_items = split_prose(raw)
    clean = [(h, strip_markup(p)) for h, p in paras]
    full = " ".join(p for _, p in clean)
    full_raw = " ".join(p for _, p in paras)
    W = words(full)
    nw = len(W)
    nchars = sum(len(p) for _, p in clean)
    sents = []
    for _, p in clean:
        sents.extend(sentences(p))
    slen = [len(words(s)) for s in sents]
    mean = sum(slen) / len(slen) if slen else 0
    sd = (sum((x - mean) ** 2 for x in slen) / len(slen)) ** 0.5 if slen else 0

    r = {"bloco": tag, "arquivo": os.path.basename(path)}
    r["palavras_prosa"] = nw
    r["caracteres_prosa"] = nchars
    r["paragrafos"] = len(clean)
    r["frases"] = len(sents)
    r["itens_visuais"] = display_items

    # C.1.9 — tamanho de paragrafo
    lens = sorted(((len(p), h, p[:70]) for h, p in clean), reverse=True)
    r["paragrafo_maior_chars"] = lens[0][0] if lens else 0
    r["paragrafo_maior_local"] = lens[0][1] if lens else ""
    r["paragrafos_acima_1500"] = sum(1 for L, _, _ in lens if L > 1500)
    r["paragrafos_acima_2200"] = sum(1 for L, _, _ in lens if L > 2200)
    r["top5_paragrafos"] = [(L, h) for L, h, _ in lens[:5]]

    # C.3 — comprimento de frase
    r["frase_media_palavras"] = round(mean, 1)
    r["frase_desvio_padrao"] = round(sd, 1)
    r["frase_min"] = min(slen) if slen else 0
    r["frase_max"] = max(slen) if slen else 0
    r["frases_acima_60"] = sum(1 for x in slen if x > 60)

    # C.1.3 — conectivo de enchimento
    op_filler, op_trans = [], []
    for h, p in clean:
        for c in FILLER_OPENERS:
            if re.match(r"(?i)^" + re.escape(c) + r"\b", p):
                op_filler.append((h, c, p[:60]))
        for c in TRANSITION_OPENERS:
            if re.match(r"(?i)^" + re.escape(c) + r"\b", p):
                op_trans.append((h, c, p[:60]))
    r["C13_abertura_paragrafo"] = op_filler
    r["C2_transicao_abertura_paragrafo"] = op_trans
    filler_any = {c: count_ci(full, c) for c in FILLER_OPENERS if count_ci(full, c)}
    trans_any = {c: count_ci(full, c) for c in TRANSITION_OPENERS if count_ci(full, c)}
    r["C13_lista_em_qualquer_posicao"] = filler_any
    r["C2_transicao_em_qualquer_posicao"] = trans_any
    gastos = sum(filler_any.values()) + sum(trans_any.values())
    r["conectivos_gastos_total"] = gastos
    r["conectivos_por_250_palavras"] = round(gastos / (nw / 250.0), 2) if nw else 0
    r["conectivos_limiar"] = "falha se >1,00 por 250 palavras E total >=4"
    r["conectivos_veredito"] = ("FALHA" if (gastos >= 4 and gastos / (nw / 250.0) > 1.0)
                                else "ok")

    # C.2 — aposicao contrastiva "X, not Y"
    app = re.findall(r",\s+not\s+(?:only\s+)?[a-z][^.,;:]{0,60}", full)
    app = [a for a in app if not re.match(r",\s+not\s+only", a)]
    coord = re.findall(r",\s+and\s+not\b", full)
    r["C2_aposicao_contrastiva"] = len(app)
    r["C2_aposicao_exemplos"] = app[:12]
    r["C2_aposicao_coordenada_nao_conta"] = len(coord)
    dens = len(app) / (nw / 1000.0) if nw else 0
    r["C2_aposicao_por_1000"] = round(dens, 2)
    r["C2_aposicao_veredito"] = ("FALHA" if (dens >= 5 and len(app) >= 5)
                                 else "AVISO" if (dens >= 3 and len(app) >= 3)
                                 else "ok")

    # C.1.1 — antitese
    hits = []
    for pat, name in ANTITHESIS:
        for m in re.finditer(pat, full, re.I):
            hits.append((name, full[max(0, m.start() - 40):m.end() + 40]))
    grad = []
    for pat, name in ANTITHESIS_GRAD:
        for m in re.finditer(pat, full, re.I):
            grad.append((name, full[max(0, m.start() - 60):m.end() + 40]))
    # dedup por posicao aproximada
    seen, g2 = set(), []
    for n, t in grad:
        k = t[40:90]
        if k in seen:
            continue
        seen.add(k)
        g2.append((n, t))
    r["C11_antitese_formula_fechada"] = hits
    r["C11_antitese_graduada"] = g2
    r["C11_veredito"] = ("FALHA" if hits or len(g2) >= 2
                         else "AVISO" if len(g2) == 1 else "ok")

    # C.1.7 — travessao em prosa
    em = [full_raw[max(0, m.start() - 55):m.end() + 55]
          for m in re.finditer(r"[—–]", full_raw)]
    r["C17_travessao_em_prosa"] = len(em)
    r["C17_exemplos"] = em[:8]

    # C.1.10 — adjetivo vazio
    adj = {}
    for a in EMPTY_ADJ:
        n = count_ci(full, a)
        if n:
            adj[a] = n
    r["C110_adjetivos_vazios"] = adj
    r["C110_total"] = sum(adj.values())
    r["C110_raiz_acima_de_2"] = {k: v for k, v in adj.items() if v > 2}
    r["C110_veredito"] = ("FALHA" if (sum(adj.values()) >= 5 or
                                      any(v > 2 for v in adj.values())) else "ok")

    # C.1.2 / C.1.4 / C.1.5 / C.1.6 / C.1.8 / C.1.12 / C.1.14
    def scan(lst, label):
        out = {}
        for x in lst:
            n = len(re.findall(re.escape(x), full, re.I))
            if n:
                out[x] = n
        return out
    r["C12_fechos_pseudo"] = scan(PSEUDO_CLOSERS, "C12")
    r["C14_preambulo"] = scan(PREAMBLE, "C14")
    r["C15_autonarracao"] = scan(SELF_NARRATION, "C15")
    r["C16_meta_verificacao"] = scan(VERIFICATION_META, "C16")
    r["C18_atribuicao_vaga"] = scan(VAGUE_ATTRIBUTION, "C18")
    r["C112_alerta_rotulado"] = {x: len(re.findall(re.escape(x), full))
                                 for x in ALERT_LABELS
                                 if re.findall(re.escape(x), full)}
    r["C114_errata_versao"] = scan(ERRATA, "C114")

    # C.1.13 — porcentagem (lista com contexto, decisao manual)
    pct = []
    for m in re.finditer(r"(\d[\d.,]*)\s?%", full):
        pct.append(full[max(0, m.start() - 110):m.end() + 70])
    r["percentagens_total"] = len(pct)
    r["percentagens_contexto"] = pct

    # C.2 — abertura de paragrafo repetida
    op3 = Counter()
    op3_where = defaultdict(list)
    for h, p in clean:
        k = " ".join(words(p)[:3]).lower()
        if k:
            op3[k] += 1
            op3_where[k].append(h)
    rep = {k: v for k, v in op3.items() if v >= 3}
    r["C2_abertura_repetida_3x"] = {k: (v, op3_where[k]) for k, v in rep.items()}
    r["C2_abertura_repetida_2x"] = {k: v for k, v in op3.items() if v == 2}

    # C.2 — adverbios intensificadores e -ly concentrados
    inten = {a: count_ci(full, a) for a in INTENSIFIERS if count_ci(full, a)}
    r["C2_intensificadores"] = inten
    r["C2_intensificadores_total"] = sum(inten.values())
    ly_max, ly_where = 0, ""
    for h, p in clean:
        n = len([w for w in words(p) if w.lower().endswith("ly") and
                 w.lower() not in ("only", "family", "supply", "apply", "reply",
                                   "early", "likely", "italy", "july")])
        if n > ly_max:
            ly_max, ly_where = n, h
    r["C2_adverbios_ly_max_por_paragrafo"] = ly_max
    r["C2_adverbios_ly_local"] = ly_where

    # C.2 — perguntas retoricas
    q = [s for s in sents if s.rstrip().endswith("?")]
    r["C2_perguntas"] = len(q)
    r["C2_perguntas_exemplos"] = q[:5]
    r["C2_perguntas_por_300"] = round(len(q) / (nw / 300.0), 2) if nw else 0

    # C.2 — locucoes, copula, gerundio, nominalizacao, introdutores de fonte
    r["C2_locucoes"] = {k: count_ci(full, k) for k in WORDY if count_ci(full, k)}
    r["C2_copula"] = {k: count_ci(full, k) for k in COPULA_EVASION
                      if count_ci(full, k)}
    r["C2_gerundio_vago"] = {k: count_ci(full, k) for k in VAGUE_GERUND
                             if count_ci(full, k)}
    r["C2_nominalizacao"] = {k: count_ci(full, k) for k in NOMINALIZATION
                             if count_ci(full, k)}
    si = sum(count_ci(full, k) for k in SOURCE_INTRODUCERS)
    r["C2_introdutores_fonte"] = si
    r["C2_introdutores_por_120"] = round(si / (nw / 120.0), 2) if nw else 0

    # C.2 — apoio visual
    r["C2_chars_por_item_visual"] = (round(nchars / display_items)
                                     if display_items else None)
    r["C2_apoio_visual_veredito"] = ("ok" if display_items and
                                     nchars / display_items <= 5000 else "AVISO")

    # C.3 — simetria de paragrafo e inversao
    sc = [len(sentences(p)) for _, p in clean]
    sym = sum(1 for i in range(len(sc) - 2)
              if sc[i] == sc[i + 1] == sc[i + 2])
    r["C3_simetria_3_paragrafos_iguais"] = sym
    inv = 0
    subord = ("when", "while", "although", "because", "since", "if", "as",
              "after", "before", "given", "across", "within", "under",
              "between", "for", "in", "on", "by", "with", "at", "from",
              "measured", "applied", "restricted", "sorted", "confronting",
              "holding", "read", "until", "two", "three", "four", "five")
    for s in sents:
        w0 = (words(s)[:1] or [""])[0].lower()
        if w0 in subord:
            inv += 1
    r["C3_abertura_por_adjunto_pct"] = (round(100 * inv / len(sents), 1)
                                        if sents else 0)

    # C.6 — lexico
    c6 = {}
    for x in C6:
        n = count_ci(full, x) if " " not in x else len(
            re.findall(re.escape(x), full, re.I))
        if n:
            c6[x] = n
    r["C6_lexico"] = c6

    # rather than / instead of (fora da regua, medido por ritmo)
    r["ritmo_rather_than"] = len(re.findall(r"\brather than\b", full, re.I))
    r["ritmo_instead_of"] = len(re.findall(r"\binstead of\b", full, re.I))

    # C.4.4 — primeira frase de cada secao
    firsts = []
    cur = None
    for h, p in clean:
        if h != cur:
            cur = h
            s0 = sentences(p)[0] if sentences(p) else ""
            firsts.append((h, len(words(s0)), s0[:190]))
    r["C44_primeira_frase_por_secao"] = firsts
    r["C14_primeira_frase_acima_45"] = [(h, n) for h, n, _ in firsts if n > 45]

    # C.4.4 — primeiras 120 palavras de cada secao (julgamento manual)
    bysec = defaultdict(list)
    order = []
    for h, p in clean:
        if h not in bysec:
            order.append(h)
        bysec[h].append(p)
    r["C44_primeiras_120_palavras"] = [
        (h, " ".join(words(" ".join(bysec[h]))[:120])) for h in order]

    # C.4.6 — ultima frase de cada secao, e se carrega numero
    closers = []
    for h in order:
        ss = sentences(" ".join(bysec[h]))
        last = ss[-1] if ss else ""
        closers.append((h, bool(re.search(r"\d", last)), last[:220]))
    r["C46_fecho_por_secao"] = closers
    # fechos de paragrafo sem numero
    nonum = 0
    for _, p in clean:
        ss = sentences(p)
        if ss and not re.search(r"\d", ss[-1]):
            nonum += 1
    r["C46_fechos_paragrafo_sem_numero_pct"] = (
        round(100 * nonum / len(clean), 1) if clean else 0)

    # texto limpo guardado para as medidas entre blocos
    r["_full"] = full
    r["_paras"] = clean
    return r


# ------------------------------------------------- medidas entre blocos

STOP = set("""a an the and or but of in on at to for from by with as is are was
were be been being it its this that these those there here their his her not
no than then so such which who whom what when where while if because since
into over under about against between among through during before after above
below up down out off again further once all any both each few more most other
some only own same too very can will just should now do does did have has had
having i we you they he she them us our your my me one two three four five six
seven eight nine ten per also across within without upon toward towards""".split())


def content_words(t):
    return [w.lower() for w in words(t)
            if len(w) > 2 and w.lower() not in STOP]


def mirror_overlap(concl, abstract):
    """C.2 conclusao-espelho: sobreposicao de palavras de conteudo."""
    a = set(content_words(concl))
    b = set(content_words(abstract))
    if not a:
        return None
    inter = a & b
    return {
        "palavras_conteudo_conclusao": len(a),
        "palavras_conteudo_resumo": len(b),
        "compartilhadas": len(inter),
        "sobreposicao_pct_sobre_conclusao": round(100 * len(inter) / len(a), 1),
        "sobreposicao_pct_sobre_resumo": (round(100 * len(inter) / len(b), 1)
                                          if b else 0),
        "jaccard_pct": round(100 * len(inter) / len(a | b), 1),
        "lista": sorted(inter),
    }


def shingles(text, n=7):
    cw = content_words(text)
    return {tuple(cw[i:i + n]): i for i in range(len(cw) - n + 1)}


def cross_redundancy(rs, alvo, contra, n=7):
    """Trechos do bloco alvo cujo n-grama de palavras de conteudo reaparece
    em outro bloco. Devolve os casamentos agrupados por paragrafo."""
    idx = {}
    for r in rs:
        if r["bloco"] not in contra:
            continue
        for h, p in r["_paras"]:
            for sh in shingles(p, n):
                idx.setdefault(sh, []).append((r["bloco"], h))
    out = []
    for r in rs:
        if r["bloco"] != alvo:
            continue
        for h, p in r["_paras"]:
            hits = defaultdict(int)
            for sh in shingles(p, n):
                for loc in idx.get(sh, []):
                    hits[loc] += 1
            if hits:
                out.append((h, p[:120], dict(sorted(
                    hits.items(), key=lambda kv: -kv[1]))))
    return out


def report(rs):
    out = []
    P = out.append
    P("=" * 78)
    P("MEDICAO PARTE C — blocos " + ", ".join(r["bloco"] for r in rs))
    P("=" * 78)
    hdr = tuple(["regra"] + [r["bloco"] for r in rs])
    rows = [
        ("palavras de prosa", "palavras_prosa"),
        ("caracteres de prosa", "caracteres_prosa"),
        ("paragrafos", "paragrafos"),
        ("frases", "frases"),
        ("C.1.9 maior paragrafo (chars)", "paragrafo_maior_chars"),
        ("C.1.9 paragrafos > 1500 (AVISO)", "paragrafos_acima_1500"),
        ("C.1.9 paragrafos > 2200 (FALHA)", "paragrafos_acima_2200"),
        ("C.1.3 conectivos gastos (total)", "conectivos_gastos_total"),
        ("C.1.3 por 250 palavras (lim 1,0)", "conectivos_por_250_palavras"),
        ("C.1.3 veredito", "conectivos_veredito"),
        ("C.2 aposicao 'X, not Y'", "C2_aposicao_contrastiva"),
        ("C.2 aposicao por 1.000 (3/5)", "C2_aposicao_por_1000"),
        ("C.2 aposicao veredito", "C2_aposicao_veredito"),
        ("C.1.1 antitese formula fechada", None),
        ("C.1.1 antitese graduada", None),
        ("C.1.1 veredito", "C11_veredito"),
        ("C.1.7 travessao em prosa", "C17_travessao_em_prosa"),
        ("C.1.10 adjetivos vazios (total)", "C110_total"),
        ("C.1.10 veredito", "C110_veredito"),
        ("C.2 perguntas retoricas", "C2_perguntas"),
        ("C.2 intensificadores (lim 3)", "C2_intensificadores_total"),
        ("C.2 -ly max por paragrafo (lim 4)", "C2_adverbios_ly_max_por_paragrafo"),
        ("C.2 introdutores por 120 (lim 1)", "C2_introdutores_por_120"),
        ("C.2 chars por item visual (5000)", "C2_chars_por_item_visual"),
        ("C.3 frase media (palavras)", "frase_media_palavras"),
        ("C.3 desvio padrao da frase", "frase_desvio_padrao"),
        ("C.3 frase min / max", None),
        ("C.3 frases > 60 palavras", "frases_acima_60"),
        ("C.3 simetria 3 paragrafos", "C3_simetria_3_paragrafos_iguais"),
        ("C.3 abertura por adjunto (%)", "C3_abertura_por_adjunto_pct"),
        ("percentagens no bloco", "percentagens_total"),
        ("'rather than'", "ritmo_rather_than"),
        ("'instead of'", "ritmo_instead_of"),
    ]
    w = 36
    P(f"{hdr[0]:<{w}}" + "".join(f"{h:>11}" for h in hdr[1:]))
    P("-" * 78)
    for label, key in rows:
        if key is None:
            if "formula fechada" in label:
                vals = [len(r["C11_antitese_formula_fechada"]) for r in rs]
            elif "graduada" in label:
                vals = [len(r["C11_antitese_graduada"]) for r in rs]
            else:
                vals = [f"{r['frase_min']}/{r['frase_max']}" for r in rs]
        else:
            vals = [r.get(key, "") for r in rs]
        P(f"{label:<{w}}" + "".join(f"{str(v):>11}" for v in vals))
    P("")
    for r in rs:
        P("=" * 78)
        P(f"BLOCO {r['bloco']} — {r['arquivo']}")
        P("=" * 78)
        for k in ("C11_antitese_formula_fechada", "C11_antitese_graduada",
                  "C13_abertura_paragrafo", "C2_transicao_abertura_paragrafo",
                  "C13_lista_em_qualquer_posicao",
                  "C2_transicao_em_qualquer_posicao",
                  "C2_aposicao_exemplos", "C17_exemplos",
                  "C110_adjetivos_vazios", "C12_fechos_pseudo", "C14_preambulo",
                  "C15_autonarracao", "C16_meta_verificacao",
                  "C18_atribuicao_vaga", "C112_alerta_rotulado",
                  "C114_errata_versao", "C2_abertura_repetida_3x",
                  "C2_abertura_repetida_2x", "C2_intensificadores",
                  "C2_locucoes", "C2_copula", "C2_gerundio_vago",
                  "C2_nominalizacao", "C6_lexico", "top5_paragrafos",
                  "C2_perguntas_exemplos", "C14_primeira_frase_acima_45"):
            v = r.get(k)
            if v:
                P(f"\n[{k}]")
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        P(f"  {kk}: {vv}")
                else:
                    for item in v:
                        P(f"  {item}")
        P("\n[C44_primeira_frase_por_secao]")
        for h, n, s in r["C44_primeira_frase_por_secao"]:
            P(f"  ({n:>2} pal) {h}")
            P(f"        {s}")
        P("\n[percentagens_contexto]")
        for c in r["percentagens_contexto"]:
            P("  ... " + c.replace("\n", " "))
    return "\n".join(out)


def section_text(rs, bloco, prefixo):
    """Prosa de uma secao, pelo prefixo do titulo."""
    for r in rs:
        if r["bloco"] != bloco:
            continue
        return " ".join(p for h, p in r["_paras"]
                        if h.lower().startswith(prefixo.lower()))
    return ""


def raw_block(path, start, end):
    raw = load(path)
    i = raw.find(start)
    j = raw.find(end, i + 1) if i >= 0 else -1
    return raw[i + len(start):j] if i >= 0 and j > i else ""


def extra_report(rs):
    out = []
    P = out.append
    P("=" * 78)
    P("MEDIDAS ENTRE BLOCOS E EXIGENCIAS POSITIVAS")
    P("=" * 78)

    abstract = raw_block(os.path.join(SECTIONS, FILES[0][1]),
                         "## Abstract", "**Keywords:**")
    concl = section_text(rs, "F", "16.")
    mo = mirror_overlap(strip_markup(concl), strip_markup(abstract))
    P("\n[C.2 conclusao-espelho: F secao 16 contra o resumo do bloco A]")
    if mo:
        for k, v in mo.items():
            if k != "lista":
                P(f"  {k}: {v}")
        P("  compartilhadas: " + ", ".join(mo["lista"]))

    for alvo, contra in (("E", "ABCD"), ("F", "ABCDE"), ("E", "F")):
        P(f"\n[redundancia: bloco {alvo} contra {contra}, 7-grama de conteudo]")
        for h, snip, hits in cross_redundancy(rs, alvo, contra):
            P(f"  {h}")
            P(f"    {snip}")
            for (b, hh), n in hits.items():
                P(f"      -> {n} n-gramas em {b} / {hh}")

    for r in rs:
        if r["bloco"] not in ("E", "F"):
            continue
        P(f"\n[C.4.4 primeiras 120 palavras por secao — bloco {r['bloco']}]")
        for h, t in r["C44_primeiras_120_palavras"]:
            P(f"  --- {h}")
            P(f"      {t}")
        P(f"\n[C.4.6 fecho de secao — bloco {r['bloco']}]")
        for h, num, s in r["C46_fecho_por_secao"]:
            P(f"  [{'num' if num else 'SEM NUMERO'}] {h}")
            P(f"      {s}")
        P(f"  fechos de paragrafo sem numero: "
          f"{r['C46_fechos_paragrafo_sem_numero_pct']}%")
    return "\n".join(out)


def main():
    rs = [analyse(tag, os.path.join(SECTIONS, fn)) for tag, fn in FILES]
    sel = None
    for i, a in enumerate(sys.argv):
        if a == "--blocks" and i + 1 < len(sys.argv):
            sel = sys.argv[i + 1].upper()
    shown = [r for r in rs if sel is None or r["bloco"] in sel]
    if "--json" in sys.argv:
        for r in rs:
            r.pop("_full", None)
            r.pop("_paras", None)
        print(json.dumps(shown, ensure_ascii=False, indent=2))
    elif "--extra" in sys.argv:
        print(extra_report(rs))
    else:
        print(report(shown))


if __name__ == "__main__":
    main()
