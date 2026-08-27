"""Wave Agosto 2026 — pesquisa GEO/SEO em 5 provedores (delta 22-jul -> 27-ago-2026)."""
import asyncio, pathlib, json
import httpx

ROOT = pathlib.Path(r"D:\GENESIS_GITHUB\alexandrebrt14-sys\geo-orchestrator")
OUT = pathlib.Path(__file__).parent / "raw"
OUT.mkdir(parents=True, exist_ok=True)
env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, _, v = line.partition("="); env[k.strip()] = v.strip().strip('"').strip("'")
K = env.get

SYSTEM = ("Você é pesquisador sênior de GEO (Generative Engine Optimization) e SEO. Responda em português do Brasil "
 "com acentuação completa. Janela de interesse: 22 de julho de 2026 a 27 de agosto de 2026 (hoje é 27-ago-2026); "
 "aceite fatos anteriores só se forem fundadores. Para CADA fato: data, fonte nomeada e URL. Distinga sempre "
 "fonte primária (paper, doc oficial, press release, blog do vendor) de secundária (imprensa). Se não achar, diga "
 "'não localizado' em vez de inventar. Nunca fabrique arXiv IDs ou URLs. Estruture com títulos e tabelas. Seja denso "
 "e acionável para uma consultoria de GEO no Brasil (alexandrecaramaschi.com / brasilgeo.ai).")

DEEP = {
 "p1_papers_frameworks": "Papers acadêmicos (arXiv, SIGIR, KDD, ACL, EMNLP, CIKM, RecSys, WWW) publicados ou atualizados entre julho e agosto de 2026 sobre Generative Engine Optimization, AEO, citação por LLMs, RAG e recuperação para motores de resposta. Para cada paper: arXiv ID real, autores, data, achado central com número, método, e o que muda na prática. Depois: frameworks de EXECUÇÃO de trabalhos de GEO (workflow, etapas, cadência, papéis) propostos por papers ou vendors nesse período, e frameworks de MEDIÇÃO e REPORT (KPIs, dashboards, relatório mensal para cliente, atribuição). Quais KPIs viraram consenso e quais foram desmentidos.",
 "p2_vendors_colunas": "Lançamentos, estudos, dados e colunas publicados entre 22-jul-2026 e 27-ago-2026 por Profound, Ahrefs (Brand Radar, AI Overviews studies), Semrush/Adobe (AI Visibility Toolkit, AI Visibility Index), Conductor, Peec AI, Otterly, Scrunch/Sitecore, AthenaHQ, Similarweb, SparkToro, Moz, Search Engine Land, Search Engine Journal, Kevin Indig, Aleyda Solis, Lily Ray, Rand Fishkin, Mike King (iPullRank), Andrea Volpini (WordLift), Dan Petrovic. Números de estudo (citation share, referral, CTR, overlap), preços e features novas, aquisições e rodadas de investimento, e o que cada coluna defende ou refuta. Incluir posições críticas/céticas.",
 "p3_seo_google_engines": "O que mudou em busca e motores de resposta entre 22-jul-2026 e 27-ago-2026: Google (core updates, spam updates, AI Overviews, AI Mode, Search Console relatórios de IA, Gemini na busca, agentic checkout/UCP, Merchant Center), Bing/Copilot, ChatGPT search e shopping, Perplexity (Comet, ads, publisher program), Claude, Grok, Apple. Comportamento de citação de cada motor (quantas fontes, tipo de fonte, links). Dados de tráfego de referência de IA, cliques em AIO, zero-click. Como SEO clássico e GEO se sobrepõem ou divergem segundo evidência desse período.",
 "p4_semantica_vetorial_reports": "Estado da arte prático (julho-agosto de 2026) de nuvem semântica, espaço vetorial, embeddings, chunking, rerankers, grafos de conhecimento e entidades aplicados a GEO: como motores de resposta recuperam e selecionam passagens, o que a evidência diz sobre tamanho de chunk, headings-pergunta, densidade de entidade, dados estruturados, llms.txt, frescor. Novos modelos de embedding e rerank lançados no período (OpenAI, Google, Cohere, Voyage, Jina, open-source) com números. Depois: modelos de RELATÓRIO e dashboard de GEO+SEO usados por agências e vendors (estrutura, métricas, periodicidade, como apresentar incerteza ao cliente), com exemplos e URLs.",
}
PRO = {
 "s1_brasil": "Notícias, estudos, lançamentos e colunas sobre GEO, SEO, AI Overviews/Modo IA, ChatGPT e mercado de busca no BRASIL entre 22-jul-2026 e 27-ago-2026: Google Brasil, imprensa (Folha, Estadão, UOL, Meio & Mensagem, Mobile Time, Adnews), agências brasileiras, Resultados Digitais, Rock Content, Conversion, eventos (RD Summit, Web Summit Rio), CADE, PL 2338, ANPD. Números com data, fonte e URL.",
 "s2_modelos_lancamentos": "Lançamentos de modelos e produtos de LLM entre 22-jul-2026 e 27-ago-2026 (OpenAI GPT-5.x, Google Gemini 3.x, Anthropic Claude 5/Fable/Mythos, xAI Grok, Meta Llama, Mistral, DeepSeek, Qwen) e o que cada um mudou em busca web, citação de fontes, browsing agêntico, memória e comércio. Também novos modelos de embedding e rerank. Datas, fontes primárias e URLs.",
}
GEM = {
 "g1_kpis_reports": "Pesquise na web (julho-agosto de 2026) frameworks de KPI, medição e relatório de GEO/AI visibility publicados por vendors e agências (Profound, Ahrefs, Semrush, Conductor, Peec, Otterly, Similarweb, agências). Quero: nome do KPI, definição operacional, fórmula, fonte primária com URL e data, e exemplos de dashboards/relatórios mensais. Sinalize KPIs sem fonte primária.",
 "g2_papers_arxiv": "Pesquise no arxiv.org e no Google Scholar papers de julho e agosto de 2026 sobre generative engine optimization, LLM citation, answer engine, RAG retrieval for AI search, AI overviews impact. Liste apenas IDs arXiv REAIS que você encontrou na web, com título, autores, data e achado com número. Se não tiver certeza do ID, escreva 'ID não verificado'.",
}
OAI = {
 "o1_executivo": "Usando busca na web, produza um briefing executivo de GEO+SEO para o período 22-jul-2026 a 27-ago-2026: (1) 10 fatos com maior impacto operacional (data, fonte, URL); (2) o que Profound, Ahrefs, Semrush/Adobe, Conductor e Similarweb publicaram nesse período; (3) framework de execução de um trabalho de GEO em 2026 (etapas, entregáveis, cadência, KPIs por etapa, template de report mensal); (4) o que foi desmentido ou perdeu força; (5) 5 apostas para set-out/2026.",
}
XAI = {
 "x1_pulso_x": "Com busca no X/Twitter e na web, resuma o pulso das últimas 5 semanas (22-jul a 27-ago-2026) da comunidade de SEO/GEO: threads mais discutidas, polêmicas (ex.: ceticismo sobre GEO, dados de referral de IA, llms.txt, Google AI Mode), anúncios de vendors, e o que os principais nomes (Rand Fishkin, Lily Ray, Kevin Indig, Aleyda Solis, Mike King, Glenn Gabe, Barry Schwartz, Profound, Ahrefs, Semrush) disseram. Cite handle, data e link.",
}

def save(name, tag, text, srcs):
    (OUT / f"{name}.md").write_text(f"# {name} ({tag})\n\n{text}\n\n## Fontes\n" + "\n".join(f"- {s}" for s in srcs), encoding="utf-8")
    print(f"[OK] {name}: {len(text)} chars, {len(srcs)} fontes", flush=True)

def fail(name, e):
    print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:300]}", flush=True)
    body = getattr(getattr(e, "response", None), "text", "")
    (OUT / f"{name}.ERROR.txt").write_text(repr(e) + "\n" + (body or "")[:2000], encoding="utf-8")

async def pplx(c, name, prompt, model, max_tokens):
    try:
        b = {"model": model, "max_tokens": max_tokens,
             "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
             "return_citations": True, "search_recency_filter": "month" if model == "sonar-pro" else "year"}
        r = await c.post("https://api.perplexity.ai/chat/completions", headers={"Authorization": f"Bearer {K('PERPLEXITY_API_KEY')}"}, json=b)
        r.raise_for_status(); d = r.json()
        text = d["choices"][0]["message"]["content"]
        if not text.strip(): raise RuntimeError(f"resposta vazia: {json.dumps(d)[:300]}")
        cits = [x if isinstance(x, str) else (x.get("url") or str(x)) for x in (d.get("citations") or [])]
        (OUT / f"{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        save(name, f"Perplexity {model}", text, cits)
    except Exception as e: fail(name, e)

async def gem(c, name, prompt):
    try:
        b = {"contents": [{"role": "user", "parts": [{"text": SYSTEM + "\n\n" + prompt}]}],
             "tools": [{"google_search": {}}],
             "generationConfig": {"maxOutputTokens": 8000, "thinkingConfig": {"thinkingBudget": 2048}}}
        r = await c.post("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent",
                         headers={"x-goog-api-key": K("GOOGLE_AI_API_KEY")}, json=b)
        r.raise_for_status(); d = r.json()
        cand = (d.get("candidates") or [{}])[0]
        text = "\n".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts") or [] if p.get("text"))
        srcs = [f"{(ch.get('web') or {}).get('title','')} — {(ch.get('web') or {}).get('uri')}" for ch in ((cand.get("groundingMetadata") or {}).get("groundingChunks") or []) if (ch.get('web') or {}).get('uri')]
        save(name, "Gemini 3.1 Pro grounded", text, srcs)
    except Exception as e: fail(name, e)

async def oai(c, name, prompt):
    try:
        b = {"model": "gpt-5.5", "tools": [{"type": "web_search"}], "instructions": SYSTEM, "input": prompt, "max_output_tokens": 12000}
        r = await c.post("https://api.openai.com/v1/responses", headers={"Authorization": f"Bearer {K('OPENAI_API_KEY')}"}, json=b)
        r.raise_for_status(); d = r.json()
        text, srcs = "", []
        for item in d.get("output", []):
            for ct in item.get("content", []) or []:
                if ct.get("type") == "output_text":
                    text += ct.get("text", "")
                    for a in ct.get("annotations", []) or []:
                        if a.get("url"): srcs.append(f"{a.get('title','')} — {a['url']}")
        if not text.strip(): raise RuntimeError(json.dumps(d)[:400])
        save(name, "OpenAI gpt-5.5 web_search", text, sorted(set(srcs)))
    except Exception as e: fail(name, e)

async def xai(c, name, prompt):
    try:
        b = {"model": "grok-4.6", "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
             "search_parameters": {"mode": "on", "return_citations": True, "sources": [{"type": "x"}, {"type": "web"}]}, "max_tokens": 8000}
        r = await c.post("https://api.x.ai/v1/chat/completions", headers={"Authorization": f"Bearer {K('XAI_API_KEY')}"}, json=b)
        r.raise_for_status(); d = r.json()
        text = d["choices"][0]["message"]["content"]
        save(name, "xAI grok-4.6 live search", text, d.get("citations") or [])
    except Exception as e: fail(name, e)

async def main():
    async with httpx.AsyncClient(timeout=1500.0) as c:
        await asyncio.gather(
            *[pplx(c, n, p, "sonar-deep-research", 32000) for n, p in DEEP.items()],
            *[pplx(c, n, p, "sonar-pro", 8000) for n, p in PRO.items()],
            *[gem(c, n, p) for n, p in GEM.items()],
            *[oai(c, n, p) for n, p in OAI.items()],
            *[xai(c, n, p) for n, p in XAI.items()],
        )
    print("=== done ===", flush=True)
asyncio.run(main())
