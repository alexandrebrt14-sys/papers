# Estado final do projeto papers

O ciclo de coleta foi encerrado em **11 de setembro de 2026**, no fuso de São Paulo, por decisão do autor após a publicação do preprint. O projeto preserva o acervo para consulta e reanálise. Novas pesquisas exigem escopo e autorização próprios.

| Superfície | Estado de encerramento |
|---|---|
| Coleta diária | Desativada no GitHub; cron removido e execução de coleta bloqueada no código |
| Benchmark semanal | Desativado no GitHub; nenhuma consulta experimental nova |
| Calibração semanal | Desativada no GitHub; nenhum novo controle fictício coletado |
| CLI, API e adaptadores de coleta | Bloqueio explícito antes de rede e persistência; sem variável de retomada |
| Consulta e reanálise | Preservadas para o acervo histórico |
| FinOps e segurança | Manutenção separada da coleta; chaves compartilhadas preservadas |

## Publicações

O [Zenodo](https://zenodo.org/records/22711743), DOI 10.5281/zenodo.22711743, publica a revisão empírica corrigida de 41 páginas. O [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7446519) preserva a versão anterior de 183 páginas da mesma pesquisa. Os depósitos são preprints, sem revisão por periódico. O pacote em nível de resposta não foi publicado junto com o manuscrito corrigido.

## Recortes preservados

| Fonte | Quantidade | Definição |
|---|---|---|
| Artigo corrigido, 23/04 a 11/09/2026 | 91.392 respostas | 72.145 canônicas e 19.247 sondas; 56 datas UTC observadas |
| Análises históricas do artigo, antes de 01/09 UTC | 83.486 respostas | 66.399 canônicas e 17.087 sondas; 50 datas observadas |
| Dashboard final, gerado em 11/09 às 22h57 UTC | 92.064 consultas | Agregado operacional legado; 33.439 marcadas pelo detector; não equivale ao snapshot do artigo |

O [manifesto](../data/project_status.json) fixa origem, hash, publicações e recortes. A projeção anterior de completar 90 dias não está mais vigente. Nenhum resultado deste encerramento demonstra efeito causal de GEO ou qualidade relativa dos provedores.

Leia o [registro de conclusões, falhas, aprendizados e propostas](ENCERRAMENTO_2026-09-11.md). Este estado substitui a indicação automática anterior de coleta ativa e não é regenerado pelo monitoramento.
