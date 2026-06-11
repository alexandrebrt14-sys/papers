# Trabalhos relacionados — Vantagem de citação da vertical fintech em LLMs

> Documento de apoio para a seção de *related work* do artigo sobre viés setorial de
> citação espontânea em motores generativos. Base empírica nossa: 62.820 observações
> (5 LLMs × 4 verticais brasileiras, abr–jun/2026), fintech com 28,15% de citação
> espontânea vs. 24,94% (varejo), 14,50% (tecnologia), 13,35% (saúde), ~50% das menções
> fintech concentradas no Nubank e forte interação vertical×LLM (Perplexity-RAG cita
> muito mais que modelos paramétricos).
>
> Todas as referências abaixo foram verificadas por busca direta na web e/ou no arXiv
> entre 10 e 11 de junho de 2026. As que não pôde-se confirmar estão marcadas como
> **[A VERIFICAR]**. Os dois identificadores fornecidos no briefing (2605.25517 e
> 2605.12887) foram confirmados individualmente — ver correntes 1 e 2.

---

## (a) Mapa da literatura em 8 correntes

### Corrente 1 — GEO (Generative Engine Optimization): fundação e medição

O eixo central. A literatura nasce com Princeton (2024) e amadurece rápido em 2025–2026,
saindo da otimização de página única para a medição empírica de o que é citado.

- **Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande (2024).** "GEO:
  Generative Engine Optimization." *KDD 2024* (arXiv:2311.09735). Primeiro paradigma
  peer-reviewed de GEO; introduz o GEO-bench e mostra ganhos de visibilidade de até
  ~40% via técnicas como *Cite Sources*, *Quotation Addition* e *Statistics Addition*.
  É a fundação metodológica de "visibilidade em resposta generativa" — nós medimos
  exatamente essa visibilidade, mas como **fenômeno observacional por setor**, não como
  alavanca de otimização.

- **Zhong et al. — AutoGEO (2026).** "What Generative Search Engines Like and How to
  Optimize Web Content Cooperatively." *ICLR 2026* (arXiv:2510.11438; código em
  github.com/cxcscmu/AutoGEO). Aprende automaticamente as preferências do motor
  generativo extraindo regras de LLMs de fronteira e reescreve conteúdo (AutoGEO-API +
  AutoGEO-Mini treinado por RL). Relevante porque formaliza que existem **preferências
  sistemáticas e aprendíveis** do motor — coerente com nosso achado de que o viés é
  estruturado, não ruído.

- **Vishwakarma, Kumar, Jamidar (2026).** "What Gets Cited: Competitive GEO in AI Answer
  Engines." (arXiv:2605.25517) **[ID confirmado]**. 252 mil *trials* controlados em seis
  LLMs comparando pares de documentos; relevância tópica e posição na lista são os
  maiores motores de "ser citado primeiro", com ganho de preço e *timestamps*. É o
  trabalho mais próximo do nosso no nível de *causa da citação* — porém pareando
  documentos, não medindo viés agregado entre setores de mercado real.

- **Chen, Wang, Chen, Koudas (2025).** "Generative Engine Optimization: How to Dominate
  AI Search." (arXiv:2509.08919). Experimentos controlados de grande escala "across
  multiple verticals, languages, and query paraphrases"; achado central de que a AI
  Search tem **viés sistemático e esmagador por *earned media*** (fontes terceiras
  autoritativas) sobre conteúdo próprio/social. Confirma a relevância de testar
  múltiplas verticais e idiomas — exatamente o desenho que estendemos longitudinalmente
  para o Brasil.

- **Ye, Mao, Guan, Tian (2026).** "EcoGEO: Trajectory-Aware Evidence Ecosystems for
  Web-Enabled LLM Search Agents." (arXiv:2605.12887) **[ID confirmado]**. Desloca GEO de
  página única para o ecossistema de evidências (método TRACE: página de navegação +
  páginas de suporte heterogêneas com termos compartilhados). Relevante para o
  argumento de que a citação depende do **ambiente de evidências da entidade**, não só
  do documento isolado — possível explicação de por que Nubank/fintech, com ecossistema
  de cobertura denso, dominam.

- **(2026).** "AgenticGEO: A Self-Evolving Agentic System for Generative Engine
  Optimization." (arXiv:2603.20213). Formula GEO como aprendizado de política de
  controle condicionada ao conteúdo, melhorando qualidade intrínseca para adaptação a
  motores *black-box*. Marcador da maturação do campo; uso como contexto de "estado da
  arte de intervenção", contrastando com nossa lente puramente observacional.

### Corrente 2 — Comportamento de citação de motores de busca de IA (Perplexity/SearchGPT/AIO)

Estudos empíricos de larga escala sobre **quais fontes** os motores citam — o vizinho
mais direto da nossa metodologia de coleta.

- **Yang, Kai-Cheng (2025).** "News Source Citing Patterns in AI Search Systems."
  (arXiv:2507.05301). 24 mil conversas, 65 mil respostas, 366.087 citações ligando a
  83.533 domínios únicos em OpenAI, Perplexity e Google. Achados: 9% citam notícias;
  forte concentração em poucos veículos; viés liberal pronunciado; fontes de baixa
  credibilidade raramente citadas. **Referência metodológica-âncora** (escala e desenho
  multi-motor); a diferença é que mapeamos **entidades de mercado por setor**, não
  domínios de notícia, e o fazemos longitudinalmente em mercado não-anglófono.

- **Schockaert et al. (2026).** "AI Answer Engine Citation Behavior: An Empirical
  Analysis of the GEO-16 Framework." (arXiv:2509.10762) **[ID confirmado]**. Framework de
  16 pilares → *GEO score* G∈[0,1]; 1.702 citações em 70 *prompts* de intenção de
  produto, três motores (Brave, Google AIO, Perplexity), 1.100 URLs auditadas.
  Metadados/frescor, HTML semântico e dados estruturados são os mais associados à
  citação. Mostra que **a qualidade de página prediz citação por motor** — usamos como
  *confounder* a controlar quando atribuímos a vantagem ao setor e não ao conteúdo.

- **Vishwakarma, Kumar, Jamidar (2026).** "What Gets Cited" (arXiv:2605.25517) — também
  pertence a esta corrente (ver Corrente 1).

- **Profound / Seer / qwairy (2025–2026), relatórios de indústria.** Achados recorrentes:
  Perplexity ~21,9 citações por pergunta vs. ChatGPT ~7,9; ~11% de sobreposição de
  domínios entre ChatGPT e Perplexity; ~87% das citações do SearchGPT batem com top-10
  do Bing. **[Fontes de indústria — usar só como contexto, não como evidência peer-reviewed.]**
  Sustentam quantitativamente nosso achado de **forte interação vertical×LLM** (Perplexity
  cita muito mais que modelos paramétricos).

### Corrente 3 — RAG vs. conhecimento paramétrico e seleção de fontes

Explica *por que* o eixo motor (Perplexity-RAG vs. modelos paramétricos) é o efeito mais
forte da nossa matriz.

- **Sun et al. (2024).** "Quantifying reliance on external information over parametric
  knowledge during RAG using mechanistic analysis." (arXiv:2410.00857). LLMs mostram
  forte efeito de "atalho", apoiando-se quase exclusivamente no contexto recuperado e
  minimamente no *prior* do modelo. Mecanismo direto por trás de Perplexity citar muito
  mais: quando há recuperação, a entidade com cobertura web densa (Nubank) entra na
  resposta; sem recuperação (paramétrico), domina o que o pré-treino consolidou.

- **(2024).** "A Survey on Large Language Models for Critical Societal Domains: Finance,
  Healthcare, and Law." (arXiv:2405.01769). Survey que organiza diferenças de
  comportamento de LLM por domínio crítico (inclui finanças e saúde) — útil para
  enquadrar por que esperar **heterogeneidade setorial** de cobertura e citação.

- **(2026).** "Position: LLMs Must Use Functor-Based and RAG-Driven Bias Mitigation for
  Fairness." (arXiv:2603.07368) **[A VERIFICAR — apenas listagem de busca; abstract não
  inspecionado individualmente]**. Posiciona RAG como vetor de mitigação ou amplificação
  de viés conforme o corpus recuperado — pertinente à discussão de que a vantagem
  fintech pode ser herdada do corpus, não criada pelo modelo.

### Corrente 4 — Viés de popularidade e saliência de entidade em LLMs

Núcleo teórico da explicação: ~50% das menções fintech no Nubank é um padrão de
*winner-take-most* compatível com viés de popularidade e atalho de saliência.

- **Lehmann, Lee, Schockaert, Wermter (2025/EACL 2026).** "Knowing the Facts but Choosing
  the Shortcut: Understanding How Large Language Models Compare Entities."
  (arXiv:2510.16815). Mesmo possuindo o fato, LLMs favorecem heurísticas superficiais —
  **popularidade da entidade, ordem de menção e coocorrência semântica** —, mais nos
  modelos menores. Explicação teórica direta da concentração no Nubank e do gradiente
  entre LLMs.

- **Lichtenberg, Buchholz, Schwöbel (2024).** "Large Language Models as Recommender
  Systems: A Study of Popularity Bias." *Gen-IR@SIGIR 2024* (arXiv:2406.01285).
  Contraintuitivamente, o recomendador baseado em LLM exibe **menos** viés de
  popularidade que sistemas tradicionais, mesmo sem mitigação explícita. Contraponto
  importante: o viés que medimos pode vir do *corpus de citação/recuperação*, não de uma
  tendência intrínseca do recomendador — nuance a discutir.

- **Bashardoust et al. (2024).** "Global is Good, Local is Bad?: Understanding Brand Bias
  in LLMs." Atribuição correta: **Kamruzzaman, Nguyen, Kim (2024).** *EMNLP 2024*
  (arXiv:2406.13997). Viés consistente associando marcas globais a atributos positivos e
  marcas locais a negativos, com efeito *country-of-origin* (favorece a marca local
  quando o país é especificado). Relevante porque nosso *prompt* é local (Brasil) e em
  pt-BR — o efeito país-de-origem pode estar **inflando** a citação de campeões locais
  como Nubank.

- **(2025).** "Bias Beware: The Impact of Cognitive Biases on LLM-Driven Product
  Recommendations." (arXiv:2502.01349). Vieses cognitivos (ancoragem, etc.) deslocam
  recomendação de produto — reforça que a ordem/saliência move o resultado.

### Corrente 5 — Auditoria de preferência de marca/cultura e viés setorial comercial

Trabalhos que constroem *pipelines* de auditoria de viés por marca, setor e cultura — o
gênero metodológico em que nosso artigo se inscreve.

- **(2026).** "Auditing Preferences for Brands and Cultures in LLMs."
  (arXiv:2603.18300). Quantifica preferência por marca e cultura com métricas
  comparáveis entre tópicos e personas; *pipeline* de auditoria escalável para
  pesquisadores, plataformas e reguladores. Vizinho metodológico próximo — porém sem
  desenho longitudinal nem foco em mercado emergente único.

- **(2026).** "A Scalable Entity-Based Framework for Auditing Bias in LLMs."
  (arXiv:2601.12374) **[A VERIFICAR — apenas listagem de busca]**. Framework de auditoria
  baseada em entidades; potencialmente comparável ao nosso NER-por-entidade. Confirmar
  antes de citar.

- **(2025).** "Exposing Product Bias in LLM Investment Recommendation."
  (arXiv:2503.08750). Viés sistemático de produto/marca em recomendação de investimento,
  com concentração de capital em poucas firmas. Análogo financeiro do nosso *winner-take-most*.

- **(2026).** "Pro-AI Bias in Large Language Models." (arXiv:2601.13749) **[A VERIFICAR]**.
  Contexto sobre vieses sistemáticos de preferência; checar pertinência específica.

### Corrente 6 — Viés setorial em finanças e mercado financeiro em IA generativa

A intersecção mais específica: por que **finanças/fintech** seria um setor à parte.

- **(2025).** "Your AI, Not Your View: The Bias of LLMs in Investment Analysis."
  (arXiv:2507.20957). LLMs preferem **ações de tecnologia, *large-cap* e estratégias
  contrárias**, sobrepondo a intenção do usuário; finanças é dos setores com viés mais
  severo. Sustenta que finanças não é um setor neutro para o modelo — coerente com a
  fintech destacar-se na citação.

- **(2026).** "Fin-Bias: Comprehensive Evaluation for LLM Decision-Making under human
  bias in Finance Domain." (arXiv:2605.09106) **[A VERIFICAR — apenas listagem de
  busca]**. Avaliação de vieses humanos replicados por LLM em finanças. Checar abstract.

- **(2026).** "Who Invests, Who Gets Funded: Gender and Racial Bias in LLM-Generated
  Investment Advice." *Journal of Business Ethics* (DOI 10.1007/s10551-026-06251-6).
  Viés demográfico em conselho de investimento; evidência de que o domínio financeiro
  carrega vieses fortes e socialmente relevantes — enquadra a importância normativa de
  medir a vantagem fintech.

### Corrente 7 — Avaliação de LLM em mercado não-anglófono (foco pt-BR/Brasil)

Sustenta o argumento de **mercado emergente não-anglófono** como lacuna.

- **(2026).** "Beyond English benchmarks: clinical LLM evaluation in Brazilian
  Portuguese." (arXiv:2606.07853). *Benchmark* clínico bilíngue (ClinicalBr, 2.892 casos
  de 28 periódicos SciELO). Evidência de que avaliação em pt-BR exige *benchmark*
  próprio — reforça que nosso estudo preenche um vazio de mercado.

- **(2026).** "ALBA: A European Portuguese Benchmark for Evaluating Language and
  Linguistic Dimensions in Generative LLMs." (arXiv:2603.26516). Documenta que dados e
  *benchmarks* são dominados por pt-BR, levando a viés sistemático — útil para discutir
  por que estudos pt-BR de *mercado* (e não só de língua) ainda inexistem.

- **(2026).** "CLARIN-PT-LDB: An Open LLM Leaderboard for Portuguese." (arXiv:2603.12872)
  **[A VERIFICAR — apenas listagem de busca]**. *Leaderboard* aberto de português;
  contexto de infraestrutura de avaliação.

- **(2025).** "BRoverbs — Measuring how much LLMs understand Portuguese proverbs."
  (arXiv:2509.08960) **[A VERIFICAR]**. Avaliação cultural pt-BR; contexto periférico.

### Corrente 8 — Deriva longitudinal e estabilidade temporal de LLMs

Sustenta a dimensão **longitudinal** (abr–jun/2026) do nosso desenho.

- **(2026).** "BeliefShift: Benchmarking Temporal Belief Consistency and Opinion Drift in
  LLM Agents." (arXiv:2603.23848) **[A VERIFICAR — apenas listagem de busca]**. Primeiro
  *benchmark* longitudinal de deriva de crença/opinião em agentes. Análogo metodológico
  da nossa janela temporal.

- **(2026).** "The Geometry of Forgetting: Temporal Knowledge Drift as an Independent
  Axis in LLM Representations." (arXiv:2605.09195) **[A VERIFICAR]**. Deriva de
  conhecimento temporal como direção no *residual stream*; relevante para discutir por
  que medir ao longo do tempo, não em um ponto.

- **(2025).** "Longitudinal Monitoring of LLM Content Moderation of Social Issues."
  (arXiv:2510.01255) **[A VERIFICAR]**. Monitoramento longitudinal de comportamento de
  LLM; precedente de desenho longitudinal de auditoria. O conceito de *service drift*
  (mudanças não anunciadas do provedor) motiva nossa coleta repetida.

---

## (b) A lacuna exata que nosso artigo preenche

A literatura cobre, separadamente:

1. **o que é citado** e por quê, no nível do documento (GEO, AutoGEO, *What Gets Cited*,
   GEO-16, Yang 2025);
2. **viés de marca/popularidade/setor** em recomendação e comparação de entidades
   (*Global is Good*, popularity bias, *shortcut*, viés financeiro);
3. **avaliação em pt-BR**, mas de **língua/cultura/clínica**, não de **mercado**
   (ClinicalBr, ALBA, CLARIN-PT);
4. **deriva longitudinal**, mas de crença/moderação, não de citação setorial.

**Nenhum trabalho combina as quatro dimensões.** Especificamente, não há — até onde a
busca confirmou — estudo que seja simultaneamente: (i) **longitudinal** (janela de
~10 semanas, abr–jun/2026, capturando *service drift*); (ii) **multi-LLM** (5 motores,
incluindo um RAG-nativo e quatro paramétricos); (iii) **multi-setor** com comparação
estatística formal entre verticais (qui-quadrado, IC95 Wilson); (iv) em **mercado
emergente não-anglófono** (Brasil, pt-BR), medindo **entidades comerciais reais** e não
domínios de notícia ou marcas hipotéticas; (v) com **calibração/decoys** e controle de
*confounders* (mix de `query_category`); (vi) sobre **dataset que pode ser tornado
público** (62.820 observações com NER por entidade).

Em uma frase: **é, ao que tudo indica, o primeiro estudo longitudinal multi-LLM de viés
setorial de citação espontânea de entidades comerciais em um mercado não-anglófono,
isolando o efeito de setor do efeito de motor (RAG vs. paramétrico) e do efeito de
conteúdo.** As verticais GEO (Aggarwal, Chen-Koudas) tratam "vertical" como variável de
teste de *prompt*, não como objeto de viés de mercado; Yang (2025) é multi-motor e de
larga escala, mas anglófono e centrado em notícias; *What Gets Cited* é multi-LLM e
causal, mas em laboratório pareando documentos, sem dimensão de mercado nem longitudinal.

---

## (c) Tabela de posicionamento — nosso trabalho vs. os 5 mais próximos

| Trabalho | Longitudinal | Multi-LLM | Multi-setor (teste formal) | Mercado emergente / não-anglófono | Decoys / calibração | Dataset público |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Nosso (Fintech Citation Advantage, 2026)** | **Sim** (~10 sem.) | **Sim** (5, RAG+paramétrico) | **Sim** (χ², IC95 Wilson, 4 verticais) | **Sim** (Brasil, pt-BR) | **Sim** (probes/calibração) | **Sim** (62.820 obs, NER) |
| GEO — Aggarwal et al., KDD 2024 (2311.09735) | Não | Parcial (motores generativos) | Parcial (vertical = teste de prompt) | Não (anglófono) | Não | Sim (GEO-bench) |
| What Gets Cited — Vishwakarma et al., 2026 (2605.25517) | Não | **Sim** (6 LLMs) | Não (pares de documentos) | Não | Parcial (controle pareado) | Parcial |
| News Source Citing — Yang, 2025 (2507.05301) | Parcial (uma coleta ampla) | **Sim** (3 sistemas) | Não (domínios de notícia) | Não (anglófono) | Não | Parcial (citações) |
| GEO-16 — 2509.10762 | Não | **Sim** (3 motores) | Parcial (intenção de produto) | Não | Não | Parcial (1.100 URLs) |
| Global is Good, Local is Bad — Kamruzzaman et al., EMNLP 2024 (2406.13997) | Não | **Sim** (GPT-4, Llama-3) | Não (marca global vs. local) | Parcial (efeito país-de-origem) | Parcial (pares contrastivos) | Parcial |

Leitura: cada vizinho cobre 1–3 colunas; **só o nosso preenche as seis simultaneamente**,
e é o único com desenho **longitudinal × multi-setor × mercado emergente** ao mesmo tempo.

---

## (d) Referências (formato BibTeX-like)

> Entradas marcadas `% [A VERIFICAR]` vieram apenas de listagem de busca e exigem
> confirmação de abstract/autoria antes da submissão final.

```bibtex
@inproceedings{aggarwal2024geo,
  title     = {GEO: Generative Engine Optimization},
  author    = {Aggarwal, Pranjal and Murahari, Vishvak and Rajpurohit, Tanmay and
               Kalyan, Ashwin and Narasimhan, Karthik and Deshpande, Ameet},
  booktitle = {Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery
               and Data Mining (KDD)},
  pages     = {5--16},
  year      = {2024},
  doi       = {10.1145/3637528.3671900},
  note      = {arXiv:2311.09735}
}

@inproceedings{autogeo2026,
  title     = {What Generative Search Engines Like and How to Optimize Web Content
               Cooperatively (AutoGEO)},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2026},
  note      = {arXiv:2510.11438; code: github.com/cxcscmu/AutoGEO}
}

@misc{vishwakarma2026whatgetscited,
  title  = {What Gets Cited: Competitive GEO in AI Answer Engines},
  author = {Vishwakarma, Rahul and Kumar, Shushant and Jamidar, Ratnesh},
  year   = {2026},
  eprint = {2605.25517},
  archivePrefix = {arXiv}
}

@misc{chen2025geodominate,
  title  = {Generative Engine Optimization: How to Dominate AI Search},
  author = {Chen, Mahe and Wang, Xiaoxuan and Chen, Kaiwen and Koudas, Nick},
  year   = {2025},
  eprint = {2509.08919},
  archivePrefix = {arXiv}
}

@misc{ye2026ecogeo,
  title  = {EcoGEO: Trajectory-Aware Evidence Ecosystems for Web-Enabled LLM Search Agents},
  author = {Ye, Hengwei and Mao, Jiasheng and Guan, Zhenhan and Tian, Zheng},
  year   = {2026},
  eprint = {2605.12887},
  archivePrefix = {arXiv}
}

@misc{agenticgeo2026,
  title  = {AgenticGEO: A Self-Evolving Agentic System for Generative Engine Optimization},
  year   = {2026},
  eprint = {2603.20213},
  archivePrefix = {arXiv}
}

@misc{yang2025newssource,
  title  = {News Source Citing Patterns in AI Search Systems},
  author = {Yang, Kai-Cheng},
  year   = {2025},
  eprint = {2507.05301},
  archivePrefix = {arXiv}
}

@misc{geo16_2025,
  title  = {AI Answer Engine Citation Behavior: An Empirical Analysis of the
            GEO-16 Framework},
  year   = {2025},
  eprint = {2509.10762},
  archivePrefix = {arXiv}
}

@misc{sun2024ragreliance,
  title  = {Quantifying Reliance on External Information over Parametric Knowledge
            during Retrieval Augmented Generation (RAG) using Mechanistic Analysis},
  year   = {2024},
  eprint = {2410.00857},
  archivePrefix = {arXiv}
}

@misc{survey2024criticaldomains,
  title  = {A Survey on Large Language Models for Critical Societal Domains:
            Finance, Healthcare, and Law},
  year   = {2024},
  eprint = {2405.01769},
  archivePrefix = {arXiv}
}

@misc{lehmann2025shortcut,
  title  = {Knowing the Facts but Choosing the Shortcut: Understanding How Large
            Language Models Compare Entities},
  author = {Lehmann, Hans Hergen and Lee, Jae Hee and Schockaert, Steven and
            Wermter, Stefan},
  year   = {2025},
  eprint = {2510.16815},
  archivePrefix = {arXiv},
  note   = {Accepted at EACL 2026}
}

@inproceedings{lichtenberg2024popularitybias,
  title     = {Large Language Models as Recommender Systems: A Study of Popularity Bias},
  author    = {Lichtenberg, Jan Malte and Buchholz, Alexander and Schw{\"o}bel, Pola},
  booktitle = {Gen-IR Workshop at SIGIR},
  year      = {2024},
  note      = {arXiv:2406.01285}
}

@inproceedings{kamruzzaman2024brandbias,
  title     = {``Global is Good, Local is Bad?'': Understanding Brand Bias in LLMs},
  author    = {Kamruzzaman, Mahammed and Nguyen, Hieu Minh and Kim, Gene Louis},
  booktitle = {Proceedings of EMNLP 2024},
  year      = {2024},
  note      = {arXiv:2406.13997}
}

@misc{cognitivebias2025products,
  title  = {Bias Beware: The Impact of Cognitive Biases on LLM-Driven Product
            Recommendations},
  year   = {2025},
  eprint = {2502.01349},
  archivePrefix = {arXiv}
}

@misc{auditbrands2026,
  title  = {Auditing Preferences for Brands and Cultures in LLMs},
  year   = {2026},
  eprint = {2603.18300},
  archivePrefix = {arXiv}
}

@misc{investmentbias2025,
  title  = {Your AI, Not Your View: The Bias of LLMs in Investment Analysis},
  year   = {2025},
  eprint = {2507.20957},
  archivePrefix = {arXiv}
}

@misc{productbias2025investment,
  title  = {Exposing Product Bias in LLM Investment Recommendation},
  year   = {2025},
  eprint = {2503.08750},
  archivePrefix = {arXiv}
}

@article{whoinvests2026,
  title   = {Who Invests, Who Gets Funded: Gender and Racial Bias in
             LLM-Generated Investment Advice},
  journal = {Journal of Business Ethics},
  year    = {2026},
  doi     = {10.1007/s10551-026-06251-6}
}

@misc{clinicalbr2026,
  title  = {Beyond English Benchmarks: Clinical LLM Evaluation in Brazilian Portuguese},
  year   = {2026},
  eprint = {2606.07853},
  archivePrefix = {arXiv}
}

@misc{alba2026,
  title  = {ALBA: A European Portuguese Benchmark for Evaluating Language and
            Linguistic Dimensions in Generative LLMs},
  year   = {2026},
  eprint = {2603.26516},
  archivePrefix = {arXiv}
}

% ===== [A VERIFICAR] — confirmar abstract/autoria antes da submissão =====

@misc{ragfairness2026,                 % [A VERIFICAR]
  title  = {Position: LLMs Must Use Functor-Based and RAG-Driven Bias Mitigation
            for Fairness},
  year   = {2026},
  eprint = {2603.07368},
  archivePrefix = {arXiv}
}

@misc{entityauditframework2026,        % [A VERIFICAR]
  title  = {A Scalable Entity-Based Framework for Auditing Bias in LLMs},
  year   = {2026},
  eprint = {2601.12374},
  archivePrefix = {arXiv}
}

@misc{proaibias2026,                   % [A VERIFICAR]
  title  = {Pro-AI Bias in Large Language Models},
  year   = {2026},
  eprint = {2601.13749},
  archivePrefix = {arXiv}
}

@misc{finbias2026,                     % [A VERIFICAR]
  title  = {Fin-Bias: Comprehensive Evaluation for LLM Decision-Making under
            Human Bias in Finance Domain},
  year   = {2026},
  eprint = {2605.09106},
  archivePrefix = {arXiv}
}

@misc{clarinptldb2026,                 % [A VERIFICAR]
  title  = {CLARIN-PT-LDB: An Open LLM Leaderboard for Portuguese to Assess
            Language, Culture and Civility},
  year   = {2026},
  eprint = {2603.12872},
  archivePrefix = {arXiv}
}

@misc{broverbs2025,                    % [A VERIFICAR]
  title  = {BRoverbs -- Measuring How Much LLMs Understand Portuguese Proverbs},
  year   = {2025},
  eprint = {2509.08960},
  archivePrefix = {arXiv}
}

@misc{beliefshift2026,                 % [A VERIFICAR]
  title  = {BeliefShift: Benchmarking Temporal Belief Consistency and Opinion
            Drift in LLM Agents},
  year   = {2026},
  eprint = {2603.23848},
  archivePrefix = {arXiv}
}

@misc{geometryforgetting2026,          % [A VERIFICAR]
  title  = {The Geometry of Forgetting: Temporal Knowledge Drift as an Independent
            Axis in LLM Representations},
  year   = {2026},
  eprint = {2605.09195},
  archivePrefix = {arXiv}
}

@misc{longmonitoring2025,              % [A VERIFICAR]
  title  = {Longitudinal Monitoring of LLM Content Moderation of Social Issues},
  year   = {2025},
  eprint = {2510.01255},
  archivePrefix = {arXiv}
}
```

---

### Nota de verificação

- **Confirmados individualmente por WebFetch/busca direta:** Aggarwal/GEO (2311.09735),
  What Gets Cited (2605.25517), EcoGEO (2605.12887), GEO-16 (2509.10762), AutoGEO
  (2510.11438), Chen-Koudas (2509.08919), AgenticGEO (2603.20213), Yang News Source
  (2507.05301), RAG reliance (2410.00857), shortcut/entity comparison (2510.16815),
  popularity bias recommender (2406.01285), Global is Good (2406.13997), brand/culture
  audit (2603.18300), investment bias (2507.20957), ClinicalBr pt-BR (2606.07853), ALBA
  (2603.26516).
- **Marcados [A VERIFICAR]:** apareceram apenas em listagens de resultado de busca; o
  abstract/autoria não foi inspecionado um a um. Confirmar antes da submissão.
- O briefing citou *What Gets Cited* com ID 2605.25517 e *EcoGEO* com 2605.12887 — **ambos
  conferem** com o conteúdo correto.
