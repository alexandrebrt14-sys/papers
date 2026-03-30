"""Set GitHub repository secrets via API.

Usage:
    python scripts/set-github-secrets.py

Reads secrets from .env file and pushes them to GitHub repo secrets.
Requires: pip install PyNaCl httpx python-dotenv
"""

import base64
import os
import sys
from pathlib import Path

try:
    from nacl import encoding, public
    import httpx
    from dotenv import dotenv_values
except ImportError:
    print("Instalando dependências: PyNaCl httpx python-dotenv")
    os.system(f"{sys.executable} -m pip install PyNaCl httpx python-dotenv")
    from nacl import encoding, public
    import httpx
    from dotenv import dotenv_values

REPO = "alexandrebrt14-sys/papers"
API_BASE = f"https://api.github.com/repos/{REPO}"

# Secrets to sync from .env
SECRET_NAMES = [
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_AI_API_KEY",
    "PERPLEXITY_API_KEY",
    "SERPAPI_KEY",
    # Persistência Supabase — necessário para sync do dashboard
    "SUPABASE_URL",
    "SUPABASE_KEY",
]


def get_github_token() -> str:
    """Get GitHub token from git credential manager."""
    import subprocess
    result = subprocess.run(
        ["git", "credential-manager", "get"],
        input="protocol=https\nhost=github.com\n",
        capture_output=True, text=True, timeout=10,
    )
    for line in result.stdout.splitlines():
        if line.startswith("password="):
            return line[9:]
    raise RuntimeError("Não foi possível obter token do git credential manager")


def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a secret using the repository's public key."""
    pk = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed = public.SealedBox(pk).encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(sealed).decode("utf-8")


def main():
    # Load .env
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print(f"ERRO: {env_path} não encontrado. Copie .env.example para .env e preencha.")
        sys.exit(1)

    env = dotenv_values(env_path)
    token = get_github_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    # Get repo public key for encryption
    resp = httpx.get(f"{API_BASE}/actions/secrets/public-key", headers=headers)
    resp.raise_for_status()
    pk_data = resp.json()
    public_key = pk_data["key"]
    key_id = pk_data["key_id"]

    print(f"Configurando secrets para {REPO}...\n")

    for name in SECRET_NAMES:
        value = env.get(name, "")
        if not value or value.startswith("#"):
            print(f"  [SKIP] {name} — vazio ou comentado")
            continue

        encrypted = encrypt_secret(public_key, value)
        resp = httpx.put(
            f"{API_BASE}/actions/secrets/{name}",
            headers=headers,
            json={"encrypted_value": encrypted, "key_id": key_id},
        )
        if resp.status_code in (201, 204):
            print(f"  [OK]   {name} — configurado")
        else:
            print(f"  [ERRO] {name} — {resp.status_code}: {resp.text}")

    print("\nPronto! Verifique em: https://github.com/{REPO}/settings/secrets/actions")


if __name__ == "__main__":
    main()
