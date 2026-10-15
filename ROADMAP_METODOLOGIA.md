# Roadmap científico e metodologia preservada

O ciclo inicial do `papers` encerrou a coleta em 11 de setembro de 2026. Este registro organiza a metodologia, os recortes e as limitações do estudo concluído. O projeto [PesquisaGeo2027](https://github.com/alexandrebrt14-sys/PesquisaGeo2027) continua ativo, com protocolo próprio e infraestrutura ativa, incluindo recursos compartilhados preservados.

A referência para as conclusões é o preprint corrigido [BRGEO-1: A longitudinal audit of entity-mention measurement in generative engines](https://doi.org/10.5281/zenodo.22711743), registrado em 11/09/2026. A [versão anterior no SSRN](https://doi.org/10.2139/ssrn.7446519) e o manuscrito do [PR #64](https://github.com/alexandrebrt14-sys/papers/pull/64) preservam estágios anteriores. Esses depósitos são preprints, sem revisão por periódico.

## Etapas realizadas

| Etapa | Procedimento e limite |
|---|---|
| Definição do instrumento | Especificação da janela observada, coorte de entidades, consultas, serviço e versão, configuração de geração e correspondência textual |
| Coleta, de abril a setembro de 2026 | Persistência de respostas de APIs, com participação e versões de modelos variáveis ao longo do período |
| Mensuração | Identificação lexical de entidades no texto disponível, com sondas adversariais separadas das consultas canônicas |
| Auditoria retrospectiva | Comparação de janelas nas mesmas respostas; revisão de aliases, faltantes, conjuntos vazios e elegibilidade dos numeradores e denominadores |
| Comparação entre serviços | Uso de populações e células de consulta/data comparáveis, com limites explícitos de interpretação |
| Encerramento em 11/09/2026 | Congelamento da coleta e publicação do preprint corrigido |
| Higienização em 15/10/2026 | Preservação do banco final e dos textos, desativação de Actions e exclusão autorizada dos artefatos temporários |

A coorte documentada reúne 127 entradas: 79 brasileiras reais, 32 internacionais e 16 fictícias. A bateria possui 192 consultas canônicas em quatro verticais e 64 sondas adversariais. Esses números descrevem o instrumento; as linhas coletadas não são observações independentes.

O banco final contém 92.064 respostas. O artigo corrigido utiliza 91.392, enquanto o manuscrito do PR #64 declara um corte anterior de 86.543. [DADOS_FINAIS.md](DADOS_FINAIS.md) explica a reconciliação temporal e oferece a consulta de reprodução.

## Resultados e limites de interpretação

A auditoria demonstra a sensibilidade dos indicadores às decisões de mensuração. A janela de texto, a resolução de aliases, o tratamento de conjuntos vazios e a elegibilidade da população alteram os resultados. Uma menção lexical pode ocorrer em recusa, repetição da pergunta ou contexto sem recomendação. Os resultados não demonstram efeito causal de GEO, impacto comercial ou superioridade geral de um provedor.

O texto integral dedicado está ausente nas 83.486 respostas anteriores a setembro. Reanálises desse período ficam limitadas ao texto preservado. Datas sem respostas não equivalem a taxas zero; registros administrativos retrospectivos não equivalem a tentativas observadas. Mudanças de versão e repetição de consultas limitam a independência das linhas.

Fontes expostas pela API não revelam toda a recuperação interna do serviço. Campos existentes no esquema também não comprovam mensuração implementada: `absorption_status` não constituía uma medida independente de apoio semântico. As tabelas sem registros não sustentam resultados de intervenções ou sobreposição entre fontes.

## Textos e referências preservados

O acervo inclui protocolos, propostas prospectivas históricas, registro de encerramento, base conceitual GEO, governança, regras editoriais, manuscritos e materiais de análise. O README anterior permanece em [README_HISTORICO.md](README_HISTORICO.md); seus comandos e cronogramas descrevem a operação passada.

Foram preservados pacotes textuais do commit `82c28e750e6f242007a0ad8fe9df77845d6a8edd` e do PR #64 no commit `60f652e462ac116db31a85ea8a4087185120a74d`. O segundo conserva seções autorais, decisões, revisões, tabelas, scripts e análises em `docs/research/methods-paper/journal-v2/`. É um estágio anterior, sem comprovação de publicação em periódico.

## Estado operacional

O GitHub Actions deste repositório está desabilitado. Foram removidos 183 artefatos temporários, totalizando 3.890.874.784 bytes, após preservação dos dados e relatórios finais e autorização expressa do proprietário. A consulta final retornou zero artefatos. O histórico Git permanece disponível, sem reescrita.

O Supabase `drzqkrqebvhcjotwhups`, seu schema `pesquisageo2027`, o bucket `pesquisageo2027-publico`, os pipelines ativos e o Worker compartilhado `brasilgeo-db-backup` foram mantidos. As pequenas tabelas `papers_dashboard_data`, `papers_finops` e `papers_research_sessions` também permanecem: existem consumidores de leitura no site. Chaves compartilhadas não foram revogadas.

A consulta deste acervo não exige novas chamadas a modelos, retomada de coleta ou servidor local. Qualquer novo experimento requer uma decisão específica do proprietário.
