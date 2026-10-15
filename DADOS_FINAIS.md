# Dados finais e proveniência

O banco final preservado contém 92.064 respostas, coletadas entre 23/04 e 11/09/2026, em 56 datas UTC distintas. A inspeção de 15/10/2026 utilizou SQLite em `mode=ro&immutable=1`, sem executar código experimental ou alterar o banco. `PRAGMA integrity_check` retornou `ok` e `PRAGMA foreign_key_check` não encontrou violações. Essas verificações confirmam integridade estrutural; a validade das medidas depende dos limites descritos no [roadmap metodológico](ROADMAP_METODOLOGIA.md).

## Origem e integridade

O banco veio do artefato `papers-db-349`, ID `10285736318`, da [execução 34647968968](https://github.com/alexandrebrt14-sys/papers/actions/runs/34647968968), vinculada ao commit `f4d4534b296b173a0051364fe7055b4bd0197c90`. O artefato foi excluído do GitHub Actions após preservação e conferência de hash. Seu ID é uma referência de proveniência, e não um endereço de download atual.

Na custódia local do autor, os caminhos abaixo são relativos a `overseer-output/encerramento/papers/`.

| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| `dados-finais/papers.db` | 175.427.584 | `3448cb84d4fb6b30bf60ab5544f46ad13d771cf4a5cb3786b5fe24410f7149de` |
| `dados-finais/papers-db-349.zip` | 42.606.895 | `aa474982d008e72764c1d0535de576bd0ca797320a9cfadfc63d6f15d233c80a` |

O ZIP contém o banco original e permite recuperá-lo sem depender do artefato removido. O manifesto de integridade acompanha o acervo privado. Os dados brutos permanecem fora do Git.

## Reconciliação com o artigo

As contagens foram medidas em `citations`. Consultas canônicas usam `COALESCE(is_probe, 0) = 0`; sondas usam `is_probe = 1`.

| Recorte | Respostas | Canônicas | Sondas | Datas UTC |
|---|---:|---:|---:|---:|
| Banco completo | 92.064 | 72.625 | 19.439 | 56 |
| Anterior a 11/09/2026 às 21h UTC | 91.392 | 72.145 | 19.247 | 56 |
| Rodada posterior ao corte | 672 | 480 | 192 | 1 |
| Até 08/09/2026 às 19h30min57,635649s UTC, corte declarado no PR #64 | 86.543 | 68.624 | 17.919 | 53 |

O corte de 11/09 reproduz os totais publicados no artigo corrigido. A última resposta incluída é de `2026-09-11T11:07:23.385313+00:00`. As 672 linhas adicionais vão de `2026-09-11T21:11:04.453866+00:00` a `2026-09-11T22:56:51.929692+00:00`.

Essa reconciliação identifica a diferença temporal no banco preservado. Não comprova identidade linha a linha com o arquivo original usado no artigo, que não foi fornecido separadamente. As respostas adicionais não integram automaticamente os resultados publicados.

```sql
SELECT COUNT(*) AS respostas,
       SUM(COALESCE(is_probe, 0) = 0) AS canonicas,
       SUM(COALESCE(is_probe, 0) = 1) AS sondas,
       COUNT(DISTINCT date(timestamp)) AS datas_utc,
       MIN(timestamp) AS primeira,
       MAX(timestamp) AS ultima
FROM citations
WHERE timestamp < '2026-09-11T21:00:00+00:00';
```

## Conteúdo do banco

| Tabela com registros | Linhas |
|---|---:|
| `citations` | 92.064 |
| `citation_context` | 36.976 |
| `collection_runs` | 696 |
| `daily_snapshots` | 211 |
| `finops_usage` | 92.064 |
| `finops_daily_rollup` | 274 |
| `finops_alerts` | 166 |
| `finops_budgets` | 7 |
| `finops_key_fingerprints` | 4 |
| `model_versions` | 7 |
| `verticals` | 4 |

As dez tabelas vazias são `competitor_citations`, `dual_responses`, `hypotheses`, `intervention_measurements`, `interventions`, `prompt_variants`, `scaling_observations`, `score_calibration_inputs`, `serp_ai_overlap` e `url_verifications`.

Todas as 19.439 sondas também estão marcadas como calibração. São a mesma população de linhas, e não dois conjuntos a somar. `response_full_text` está preenchido em 8.578 respostas: 6.226 canônicas e 2.352 sondas. As 83.486 respostas anteriores a setembro não têm esse campo preenchido.

`response_hash` é um identificador abreviado do texto usado pelo extrator; não substitui o SHA-256 do arquivo nem demonstra identidade entre respostas integrais. `collection_runs` contém 352 registros `success` e 344 `aborted`; parte dos abortos são anotações administrativas retrospectivas, portanto essa tabela não mede diretamente chamadas tentadas.

## Agregados e textos

O agregado `data/dashboard_data.json`, gerado em 11/09/2026 às `22:57:21.354750+00:00`, registra as mesmas 92.064 consultas e 33.439 marcações do detector legado. Sua origem é o commit `a8810bee6896202dbd3aaa345f8cc6d16db0d065`, com SHA-256 `ea9f7926c873b82192849734b3c84c7be2117b6d44dc2c67eb8677890eff3bb4`. Projeções de calendário desse JSON são históricas.

| Pacote textual privado | Arquivos | Bytes | SHA-256 |
|---|---:|---:|---|
| `main-82c28e750e6f-textos.zip` | 399 | 2.762.418 | `3d740ba93363b14edce173107cdb0653ff02497e35531f6afea64a3bcc559306` |
| `pr64-60f652e462ac-textos.zip` | 470 | 3.601.236 | `849fef1008ac2fae8db5d167caf9b49491e541d8263fa0b26893cb520f9d19a9` |

O pacote do PR #64 conserva seu próprio recorte e análises. O benchmark final e o relatório semanal final também foram preservados. Os snapshots intermediários e relatórios temporários de execução foram removidos.

## Acesso

O banco em nível de resposta permanece sob custódia privada do autor. A licença CC BY 4.0 do manuscrito não se estende automaticamente ao banco. Uma reanálise deve usar cópia do original imutável e declarar filtros, versão do código e denominadores. Não aplicar migrações ao snapshot arquivado.

Este snapshot SQLite não substitui nem autoriza pausar a infraestrutura ativa de [PesquisaGeo2027](https://github.com/alexandrebrt14-sys/PesquisaGeo2027).
