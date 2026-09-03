"""Wave Setembro 2026 - pesquisa GEO/SEO em 5 provedores (consolidacao mai-set + delta 27-ago -> 03-set-2026)."""
import asyncio, pathlib, json, os, time
import httpx

OUT = pathlib.Path(__file__).parent / "raw"
OUT.mkdir(parents=True, exist_ok=True)
K = os.environ.get

SYSTEM = ("Você é pesquisador sênior de GEO (Generative Engine Optimization) e SEO. Responda em português do Brasil "
 "com acentuação completa. Hoje é 03 de setembro de 2026. Janela principal: 27 de agosto a 03 de setembro de 2026; "
 "para papers e frameworks, aceite tudo publicado de maio de 2026 em diante. Para CADA fato: data, fonte nomeada e URL. "
 "Distinga fonte primária (paper, doc oficial, press release, blog do vendor, changelog) de secundária (imprensa). "
 "Se não achar, diga 'não localizado' em vez de inventar. Nunca fabrique arXiv IDs, DOIs ou URLs; se não tiver certeza do ID, escreva 'ID não verificado'. "
 "Estruture com títulos e tabelas. Seja denso e acionável para uma consultoria de GEO no Brasil (alexandrecaramaschi.com / brasilgeo.ai). "
 "Nunca use travessão; use vírgula, dois-pontos ou parênteses.")

PPLX = {
 "p1_papers_maio_set": "Papers acadêmicos (arXiv, SIGIR, KDD, ACL, EMNLP, CIKM, RecSys, WWW, WSDM) publicados ou atualizados entre maio e setembro de 2026 sobre Generative Engine Optimization, AEO, citação por LLMs, visibilidade de marca em motores de resposta, RAG e recuperação para AI search, detecção de conteúdo otimizado para IA, embeddings e rerankers. Para cada paper: arXiv ID real, autores, data, achado central com número, método, e o que muda na prática para quem opera GEO. Priorize os de 20 de agosto a 03 de setembro de 2026, mas liste também os fundadores de maio a agosto. Separe 'ID verificado na web' de 'ID não verificado'.",
 "p2_vendors_colunas": "Lançamentos, estudos, dados, preços e colunas publicados entre 27-ago-2026 e 03-set-2026 por Profound, Ahrefs (Brand Radar, estudos de AI Overviews), Semrush/Adobe (AI Visibility Toolkit, Brand Visibility), Conductor, Peec AI, Otterly, Scrunch/Sitecore, AthenaHQ, Similarweb, SparkToro, Moz, seoClarity, BrightEdge, Search Engine Land, Search Engine Journal, Search Engine Roundtable, Kevin Indig, Aleyda Solis, Lily Ray, Rand Fishkin, Mike King (iPullRank), Andrea Volpini (WordLift), Dan Petrovic, Tim Soulo, Glenn Gabe, Barry Schwartz. Números de estudo (citation share, referral, CTR, overlap), features novas, aquisições, rodadas, e o que cada coluna defende ou refuta. Inclua posições críticas e céticas.",
 "p3_motores_seo": "O que mudou em busca e motores de resposta entre 27-ago-2026 e 03-set-2026: Google (core update ou spam update, AI Overviews, AI Mode, Search Console relatório de IA, Preferred Sources, Gemini na busca, agentic checkout, Merchant Center, Discover), Bing/Copilot, ChatGPT search/shopping/ads (GPT-5.6, site: operator, ChatGPT Ads no Brasil), Perplexity (Comet, ads, Agent API), Claude, Grok, Apple, Meta AI. Comportamento de citação de cada motor. Dados de tráfego de referência de IA, cliques em AIO, zero-click. Como SEO clássico e GEO se sobrepõem ou divergem segundo evidência do período.",
 "p4_semantica_vetorial": "Estado da arte prático (maio a setembro de 2026) de nuvem semântica, espaço vetorial, embeddings, chunking, rerankers, grafos de conhecimento, entidades e knowledge graph aplicados a GEO: como motores de resposta recuperam, reordenam e selecionam passagens; o que a evidência diz sobre tamanho de chunk, headings-pergunta, densidade de entidade, dados estruturados, frescor, diversidade de evidência. Novos modelos de embedding e rerank lançados no período (OpenAI, Google Gemini Embedding, Cohere, Voyage, Jina, Qwen, open-source) com números de benchmark (MTEB, BEIR). Datas, fontes primárias e URLs.",
 "p5_frameworks_kpis_reports": "Consolidação de maio a setembro de 2026: frameworks de EXECUÇÃO de trabalhos de GEO (workflow, etapas, cadência, papéis, entregáveis) propostos por vendors, agências e papers; frameworks de MEDIÇÃO (KPIs: citation rate, mention rate, share of voice, share of answer, AI referral, AI-assisted conversion, prompt coverage; definição operacional e fórmula de cada um, e quem publicou); modelos de RELATÓRIO mensal de GEO+SEO para cliente (estrutura, periodicidade, como apresentar incerteza). Quais KPIs viraram consenso, quais foram desmentidos, e quais vendors mudaram a metodologia no período. Para cada item, nome, data, URL.",
 "s1_brasil": "Notícias, estudos, lançamentos e colunas sobre GEO, SEO, AI Overviews e Modo IA, ChatGPT (incluindo ChatGPT Ads no Brasil) e mercado de busca no BRASIL entre 20-ago-2026 e 03-set-2026: Google Brasil, imprensa (Folha, Estadão, UOL, Valor, Meio & Mensagem, Mobile Time, Adnews, iMasters), agências brasileiras (Conversion, Rock Content, RD Station, Agência Mestre, Hedgehog), eventos (RD Summit, Web Summit Rio, SEO Summit), CADE, PL 2338, ANPD, Marco Legal da IA. Números com data, fonte e URL.",
 "s2_modelos_lancamentos": "Lançamentos de modelos e produtos de LLM entre 20-ago-2026 e 03-set-2026 (OpenAI GPT-5.x, Google Gemini 3.x, Anthropic Claude 5 / Fable / Mythos, xAI Grok, Meta Llama, Mistral, DeepSeek, Qwen, Kimi) e o que cada um mudou em busca web, citação de fontes, browsing agêntico, memória e comércio. Também novos modelos de embedding e rerank, e mudanças de API relevantes para medição (Perplexity Agent API, OpenAI Responses, xAI Agent Tools). Datas, fontes primárias e URLs.",
}
GEM = {
 "g1_kpis_reports": "Pesquise na web (agosto e setembro de 2026) frameworks de KPI, medição e relatório de GEO e AI visibility publicados por vendors e agências (Profound, Ahrefs, Semrush, Conductor, Peec, Otterly, Similarweb, seoClarity, BrightEdge, agências). Quero: nome do KPI, definição operacional, fórmula, fonte primária com URL e data, e exemplos de dashboards e relatórios mensais. Sinalize KPIs sem fonte primária. Destaque o que mudou depois de 27 de agosto de 2026.",
 "g2_papers_arxiv": "Pesquise no arxiv.org e no Google Scholar papers de maio a setembro de 2026 sobre generative engine optimization, LLM citation, answer engine optimization, brand visibility in AI search, RAG retrieval for AI search, AI overviews impact, GEO detection. Liste apenas IDs arXiv REAIS que você encontrou na web, com título, autores, data e achado com número. Se não tiver certeza do ID, escreva 'ID não verificado'. Priorize os de 20 de agosto a 03 de setembro de 2026.",
}
OAI = {
 "o1_executivo": "Usando busca na web, produza um briefing executivo de GEO+SEO para 27-ago-2026 a 03-set-2026, com consolidação do que se firmou desde maio de 2026: (1) 10 fatos com maior impacto operacional (data, fonte, URL); (2) o que Profound, Ahrefs, Semrush/Adobe, Conductor, Similarweb, Peec e Otterly publicaram no período; (3) framework de execução de um trabalho de GEO em setembro de 2026 (etapas, entregáveis, cadência, KPIs por etapa, template de report mensal); (4) o que foi desmentido ou perdeu força desde maio; (5) 5 apostas para out-dez/2026; (6) 5 papers arXiv de maio a setembro de 2026 que todo consultor de GEO deveria ler, com ID real ou 'ID não verificado'.",
}
XAI = {
 "x1_pulso_x": "Com busca no X/Twitter e na web, resuma o pulso da última semana e meia (24-ago a 03-set-2026) da comunidade de SEO/GEO: threads mais discutidas, polêmicas (ceticismo sobre GEO, dados de referral de IA, llms.txt, Google AI Mode, ChatGPT Ads, Cloudflare 15-set), anúncios de vendors, e o que os principais nomes (Rand Fishkin, Lily Ray, Kevin Indig, Aleyda Solis, Mike King, Glenn Gabe, Barry Schwartz, Tim Soulo, Profound, Ahrefs, Semrush, Similarweb) disseram. Cite handle, data e link.",
}


def save(name, tag, text, srcs):
    (OUT / f"{name}.md").write_text(f"# {name} ({tag})\n\n{text}\n\n## Fontes\n" + "\n".join(f"- {s}" for s in srcs), encoding="utf-8")
    print(f"[OK] {name}: {len(text)} chars, {len(srcs)} fontes", flush=True)


def fail(name, e):
    print(f"[FAIL] {name}: {type(e).__name__}: {str(e)[:300]}", flush=True)
    body = getattr(getattr(e, "response", None), "text", "")
    (OUT / f"{name}.ERROR.txt").write_text(repr(e) + "\n" + (body or "")[:2000], encoding="utf-8")


async def pplx(c, name, prompt, model="sonar-pro", max_tokens=8000):
    t0 = time.time()
    try:
        b = {"model": model, "max_tokens": max_tokens,
             "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
             "return_citations": True, "search_recency_filter": "month"}
        r = await c.post("https://api.perplexity.ai/chat/completions", headers={"Authorization": f"Bearer {K('PERPLEXITY_API_KEY')}"}, json=b)
        r.raise_for_status(); d = r.json()
        text = d["choices"][0]["message"]["content"]
        if not text.strip(): raise RuntimeError(f"resposta vazia: {json.dumps(d)[:300]}")
        cits = [x if isinstance(x, str) else (x.get("url") or str(x)) for x in (d.get("citations") or [])]
        (OUT / f"{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        save(name, f"Perplexity {model}, {int(time.time()-t0)} s", text, cits)
    except Exception as e: fail(name, e)


async def pplx_seq(c):
    for n, p in PPLX.items():
        await pplx(c, n, p)


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
        if not text.strip(): raise RuntimeError(json.dumps(d)[:400])
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
        b = {"model": "grok-4.6", "instructions": SYSTEM, "input": prompt,
             "tools": [{"type": "x_search"}, {"type": "web_search"}], "max_output_tokens": 8000}
        r = await c.post("https://api.x.ai/v1/responses", headers={"Authorization": f"Bearer {K('XAI_API_KEY')}"}, json=b)
        r.raise_for_status(); d = r.json()
        (OUT / f"{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        text, srcs = "", []
        for item in d.get("output", []):
            for ct in item.get("content", []) or []:
                if ct.get("type") == "output_text":
                    text += ct.get("text", "")
                    for a in ct.get("annotations", []) or []:
                        if a.get("url"): srcs.append(a["url"])
        if not text.strip(): raise RuntimeError(json.dumps(d)[:400])
        save(name, "xAI grok-4.6 responses+x_search", text, sorted(set(srcs)))
    except Exception as e: fail(name, e)


async def main():
    async with httpx.AsyncClient(timeout=900.0) as c:
        await asyncio.gather(
            pplx_seq(c),
            *[gem(c, n, p) for n, p in GEM.items()],
            *[oai(c, n, p) for n, p in OAI.items()],
            *[xai(c, n, p) for n, p in XAI.items()],
        )
    print("=== done ===", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
