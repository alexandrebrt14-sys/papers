"""Roda os 7 prompts do Perplexity (definidos em research_script.py) no Perplexity WEB via navegador logado."""
import importlib.util
import pathlib
import subprocess  # nosec B404: chamada controlada ao driver local pplx_web.cjs

AQUI = pathlib.Path(__file__).parent
SCRIPT = AQUI / ("research_script.py" if (AQUI / "research_script.py").exists() else "research.py")
spec = importlib.util.spec_from_file_location("research_script", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
PRE = ("Hoje é 03 de setembro de 2026. Responda em português do Brasil com acentuação completa. Para cada fato: data, fonte nomeada e URL. "
       "Distinga fonte primária de secundária. Se não achar, diga 'não localizado'. Nunca invente arXiv IDs ou URLs. ")
for n, p in mod.PPLX.items():
    r = subprocess.run(["node", str(AQUI / "pplx_web.cjs"), "web_" + n, PRE + p],  # nosec B603
                       capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    print(r.stdout.strip(), r.stderr.strip()[-300:], flush=True)
print("=== done ===")
