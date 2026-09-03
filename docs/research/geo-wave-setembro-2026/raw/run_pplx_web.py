import subprocess, pathlib, sys
src = pathlib.Path("research.py").read_text(encoding="utf-8").replace("asyncio.run(main())", "")
ns = {"__file__": str(pathlib.Path("research.py").resolve())}
exec(compile(src, "research.py", "exec"), ns)
PRE = ("Hoje é 03 de setembro de 2026. Responda em português do Brasil com acentuação completa. Para cada fato: data, fonte nomeada e URL. "
       "Distinga fonte primária de secundária. Se não achar, diga 'não localizado'. Nunca invente arXiv IDs ou URLs. ")
for n, p in ns["PPLX"].items():
    r = subprocess.run(["node", "pplx_web.cjs", "web_" + n, PRE + p], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout.strip(), r.stderr.strip()[-300:], flush=True)
print("=== done ===")
