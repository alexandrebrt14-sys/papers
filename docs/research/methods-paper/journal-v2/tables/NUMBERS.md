# NUMBERS — the verifier for TABLES.md

Every figure asserted in `TABLES.md`, the statement or call that produces it, and the value obtained on the snapshot named below. A reviewer who runs the statements in order should land on the same numbers; where a figure comes from plain SQL, the statement printed here is the same string object that was executed by `build_tables.py`, so the two cannot drift.

## Snapshot

```sql
SELECT MIN(timestamp) AS first_ts, MAX(timestamp) AS last_ts,
       COUNT(*) AS rows_all,
       SUM(CASE WHEN COALESCE(is_probe,0)=0 THEN 1 ELSE 0 END) AS rows_canonical,
       SUM(CASE WHEN COALESCE(is_probe,0)=1 THEN 1 ELSE 0 END) AS rows_probe
  FROM citations;
```

| Field | Value |
|---|---|
| earliest `citations.timestamp` | `2026-04-23T22:23:00.960050+00:00` |
| latest `citations.timestamp` | `2026-09-08T19:30:57.635649+00:00` |
| rows, all | 86,543 |
| rows, canonical (`COALESCE(is_probe,0)=0`) | 68,624 |
| rows, adversarial probes | 17,919 |

Open the database read-only:

```python
import sqlite3
con = sqlite3.connect("file:data/papers.db?mode=ro", uri=True)
```

Or with the CLI, from the repository root:

```bash
sqlite3 "file:data/papers.db?mode=ro"
```

Regenerate everything:

```bash
cd docs/research/methods-paper/journal-v2/tables
python build_tables.py          # rewrites TABLES.md and NUMBERS.md
python window_analysis.py       # Table 13 alone, with its two checks
```

## V1. Verification that re-extraction reproduces the series

Every table that reports a rate under the uniform window depends on one identity: applying the project's extractor to `response_text[:200]` must reproduce the stored `cited_v2` on every row whose stored text is already at or below 200 characters. If it did not, the deltas in Tables 3 and 13 would be confounded with a change of matching rule.

Produced by `build_tables.reextract_uniform`, which is `scripts/harmonize_citation_window.py` reimplemented against a read-only connection, using `EntityExtractor` over `get_v2_cohort(vertical, include_anchors=True, include_decoys=True)`.

| Quantity | Value |
|---|---:|
| canonical rows re-extracted | 68,624 |
| rows where `len(response_text) <= 200` and re-extraction disagreed with `cited_v2` | **0** |

Result: 0 disagreements. The matching rule used in these tables is the matching rule that produced the series.

Cohort sizes entering the extractors:

| Vertical | Cohort size |
|---|---:|
| `fintech` | 31 |
| `varejo` | 32 |
| `saude` | 32 |
| `tecnologia` | 32 |
| distinct across verticals | 127 (79 Brazilian real + 32 anchors + 16 decoys) |

## T1. Engine panel

```sql
SELECT llm, model_version,
       COUNT(*) AS n,
       MIN(date(timestamp)) AS first_day,
       MAX(date(timestamp)) AS last_day
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY llm, model_version
 ORDER BY llm, first_day;
```

| Engine | `model_version` | n | First day | Last day |
|---|---|---:|---|---|
| ChatGPT | `gpt-4o-mini-2024-07-18` | 15,168 | 2026-04-23 | 2026-09-08 |
| Claude | `claude-haiku-4-5-20251001` | 15,034 | 2026-04-23 | 2026-09-08 |
| Gemini | `gemini-2.5-pro` | 10,939 | 2026-04-23 | 2026-06-09 |
| Gemini | `gemini-2.5-flash` | 4,416 | 2026-08-08 | 2026-09-08 |
| Groq | `llama-3.3-70b-versatile` | 14,208 | 2026-04-23 | 2026-08-16 |
| Perplexity | `sonar` | 7,741 | 2026-04-23 | 2026-09-08 |
| Grok | `grok-4.6` | 1,118 | 2026-08-23 | 2026-09-08 |

Architectural class is not in the database. It is taken from MANUSCRIPT.md Table 3 and hard-coded in `_common.ENGINE_CLASS`; Perplexity is the only retrieval-augmented arm.

## T2. Stored extraction string length

```sql
SELECT llm,
       COUNT(*) AS n,
       ROUND(AVG(length(response_text)),1) AS mean_chars,
       MIN(length(response_text)) AS min_chars,
       MAX(length(response_text)) AS max_chars,
       SUM(CASE WHEN length(response_text)=200 THEN 1 ELSE 0 END) AS exactly_200
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL
 GROUP BY llm;
```

| Engine | n | Mean | Min | Max | Exactly 200 | Share |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 200.0 | 200 | 200 | 15,168 | 100.0% |
| Claude | 15,034 | 200.0 | 200 | 200 | 15,034 | 100.0% |
| Gemini | 15,355 | 195.7 | 87 | 200 | 14,224 | 92.6% |
| Groq | 14,208 | 200.0 | 200 | 200 | 14,208 | 100.0% |
| Perplexity | 7,741 | 668.0 | 198 | 2,502 | 305 | 3.9% |
| Grok | 1,118 | 200.0 | 179 | 200 | 1,117 | 99.9% |

Manuscript v1.0 Table 4 reported the same quantity over the full series including probes. That variant, for comparison:

```sql
SELECT llm, COUNT(*) AS n, ROUND(AVG(length(response_text)),1) AS mean_chars,
       MIN(length(response_text)) AS min_chars, MAX(length(response_text)) AS max_chars,
       SUM(CASE WHEN length(response_text)=200 THEN 1 ELSE 0 END) AS exactly_200
  FROM citations WHERE response_text IS NOT NULL GROUP BY llm;
```

| Engine | n | Mean | Min | Max | Share exactly 200 |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 19,584 | 200.0 | 200 | 200 | 100.0% |
| Claude | 19,418 | 200.0 | 200 | 200 | 100.0% |
| Gemini | 19,818 | 195.8 | 87 | 200 | 92.6% |
| Groq | 18,304 | 199.8 | 74 | 200 | 99.8% |
| Perplexity | 7,933 | 656.7 | 198 | 2,502 | 6.3% |
| Grok | 1,486 | 199.9 | 170 | 200 | 99.5% |

## T3. Citation rate, as collected and under a uniform window

The 'as collected' column and the truncation count come from SQL:

```sql
SELECT llm,
       COUNT(*) AS n,
       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited_as_collected,
       SUM(COALESCE(cited_v2,0)) AS cited_v2,
       SUM(CASE WHEN length(response_text) > 200 THEN 1 ELSE 0 END) AS rows_truncated
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL
 GROUP BY llm;
```

The 'uniform window' column comes from `build_tables.reextract_uniform`, described in V1 above. Counts and rates:

| Engine | n | Cited as collected | Rate | 95% CI | Cited under window | Rate | 95% CI | Δ pp | Rows truncated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 2,604 | 17.1677% | [16.58, 17.78] | 2,604 | 17.1677% | [16.58, 17.78] | +0.0000 | 0 |
| Claude | 15,034 | 3,871 | 25.7483% | [25.06, 26.45] | 3,871 | 25.7483% | [25.06, 26.45] | +0.0000 | 0 |
| Gemini | 15,355 | 285 | 1.8561% | [1.65, 2.08] | 285 | 1.8561% | [1.65, 2.08] | +0.0000 | 0 |
| Groq | 14,208 | 1,210 | 8.5163% | [8.07, 8.99] | 1,210 | 8.5163% | [8.07, 8.99] | +0.0000 | 0 |
| Perplexity | 7,741 | 5,796 | 74.8740% | [73.90, 75.83] | 4,028 | 52.0346% | [50.92, 53.15] | -22.8394 | 7,435 |
| Grok | 1,118 | 331 | 29.6064% | [27.00, 32.35] | 331 | 29.6064% | [27.00, 32.35] | +0.0000 | 0 |
| **Panel** | 68,624 | 14,097 | 20.5424% | [20.24, 20.85] | 12,329 | 17.9660% | [17.68, 18.26] | -2.5764 | 7,435 |

Perplexity split by collection regime, which is why its 'as collected' figure is no longer the 75.7% of manuscript v1.0:

```sql
SELECT CASE WHEN length(response_text) > 200
            THEN 'stored text longer than the window'
            ELSE 'stored text at or below the window' END AS regime,
       COUNT(*) AS n,
       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited,
       SUM(CASE WHEN response_full_text IS NOT NULL
                 AND length(response_full_text) > 0 THEN 1 ELSE 0 END)
         AS with_full_text_retained,
       MIN(date(timestamp)) AS first_day, MAX(date(timestamp)) AS last_day
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND llm='Perplexity'
 GROUP BY regime ORDER BY regime DESC;
```

| Regime | n | Cited | Rate | 95% CI | Period |
|---|---:|---:|---:|---:|---|
| stored text longer than the window | 7,435 | 5,630 | 75.72% | [74.74, 76.68] | 2026-04-23 to 2026-08-31 |
| stored text at or below the window | 306 | 166 | 54.25% | [48.65, 59.74] | 2026-04-28 to 2026-09-08 |

Cross-check against manuscript v1.0, which closed at 2026-08-31:

```sql
SELECT llm, COUNT(*) AS n, SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND date(timestamp) <= '2026-08-31'
 GROUP BY llm;
```

Expected from VERIFICATION.md: ChatGPT 17.2%, Claude 25.8%, Gemini 1.8%, Groq 8.5%, Perplexity 75.7%, Grok 32.3% over 66,399 canonical rows. That query reproduces those figures on this snapshot; the figures in TABLES.md differ because the snapshot now runs to 2026-09-08 and adds 2,225 canonical rows.

## T4. First-mention offset

```sql
SELECT llm,
       COUNT(*) AS n_cited,
       ROUND(AVG(first_entity_offset_v2),1) AS mean_offset,
       ROUND(AVG(response_length_chars_v2),1) AS mean_observed_length,
       ROUND(AVG(1.0*first_entity_offset_v2/response_length_chars_v2),4) AS mean_relative
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND cited_v2=1
   AND first_entity_offset_v2 IS NOT NULL
   AND response_length_chars_v2 > 0
 GROUP BY llm;
```

The median of the relative offset is not expressible in portable SQLite SQL and is computed in Python from:

```sql
SELECT llm, 1.0*first_entity_offset_v2/response_length_chars_v2 AS rel
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND cited_v2=1
   AND first_entity_offset_v2 IS NOT NULL
   AND response_length_chars_v2 > 0;
```

| Engine | n cited | Mean absolute offset | Mean observed length | Mean relative | Median relative |
|---|---:|---:|---:|---:|---:|
| ChatGPT | 2,604 | 116.4 | 200.0 | 0.5822 | 0.6000 |
| Claude | 3,871 | 124.2 | 200.0 | 0.6210 | 0.6450 |
| Gemini | 285 | 95.9 | 196.1 | 0.4927 | 0.3750 |
| Groq | 1,210 | 107.8 | 200.0 | 0.5388 | 0.5300 |
| Perplexity | 5,796 | 155.3 | 648.9 | 0.2330 | 0.1715 |
| Grok | 331 | 39.7 | 199.9 | 0.1983 | 0.0000 |

## T5. Preamble criterion

The regular expression used for Table 7 of manuscript v1.0 was never committed to the repository. It is described in prose in `MANUSCRIPT.md` (Table 7 caption), `docs/METHODOLOGY_V2.md` section 4.1-bis.1 and `governance/REVISAO-EXTERNA-PAPER-20260831.md` item D9, all three saying the same thing: anchored at the start of the response, matching greeting, hedge, question restatement and model self-reference. It cannot be re-run, so the pattern below is a re-specification, published in full because the criterion is part of the result.

Applied as `re.search(PATTERN, response_text, re.IGNORECASE)` over canonical rows with non-null `response_text`. The pattern is assembled in `_common.py` from three alternatives. Each is printed below as a literal regular expression, not as Python source, so it can be pasted into any engine without unescaping.

(a) greeting or praise of the question:

```regex
(?:excelente|[óo]tima|boa|grande)\s+pergunta|excellent\s+question|great\s+question|good\s+question|that'?s\s+(?:an?\s+)?(?:excellent|great|good|interesting|very\s+good|tricky|complex|challenging)|com\s+certeza|claro(?:\!|,|\s+que)|of\s+course|certainly[,!]|sure[,!]
```

(b) hedge on whether the question can be answered:

```regex
[ée]\s+(?:muito\s+|bastante\s+)?(?:dif[íi]cil|complexo|complicado|imposs[íi]vel)|n[ãa]o\s+(?:h[áa]|existe|d[áa])\s+(?:uma\s+)?(?:resposta|empresa|consenso|forma|[úu]nica)|n[ãa]o\s+d[áa]\s+para|it'?s?\s+(?:a\s+)?(?:tricky|difficult|hard|complex|impossible|challenging|not\s+easy)|it\s+is\s+(?:tricky|difficult|hard|complex|impossible|challenging)|predicting|prever|there\s+is\s+no\s+single|there'?s\s+no\s+single|no\s+single\s+company|[ée]\s+importante\s+(?:notar|destacar|ressaltar|considerar)|it'?s\s+important\s+to\s+note
```

(c) explicit model self-reference:

```regex
as\s+an?\s+(?:large\s+)?(?:language\s+model|ai\b|artificial\s+intelligence)|como\s+(?:um|uma)\s+(?:modelo\s+de\s+linguagem|ia\b|intelig[êe]ncia\s+artificial)
```

The three are joined as `^\W*(?:a|b|c)` and compiled with `re.IGNORECASE`. The complete pattern, exactly as compiled:

```regex
^\W*(?:(?:excelente|[óo]tima|boa|grande)\s+pergunta|excellent\s+question|great\s+question|good\s+question|that'?s\s+(?:an?\s+)?(?:excellent|great|good|interesting|very\s+good|tricky|complex|challenging)|com\s+certeza|claro(?:\!|,|\s+que)|of\s+course|certainly[,!]|sure[,!]|[ée]\s+(?:muito\s+|bastante\s+)?(?:dif[íi]cil|complexo|complicado|imposs[íi]vel)|n[ãa]o\s+(?:h[áa]|existe|d[áa])\s+(?:uma\s+)?(?:resposta|empresa|consenso|forma|[úu]nica)|n[ãa]o\s+d[áa]\s+para|it'?s?\s+(?:a\s+)?(?:tricky|difficult|hard|complex|impossible|challenging|not\s+easy)|it\s+is\s+(?:tricky|difficult|hard|complex|impossible|challenging)|predicting|prever|there\s+is\s+no\s+single|there'?s\s+no\s+single|no\s+single\s+company|[ée]\s+importante\s+(?:notar|destacar|ressaltar|considerar)|it'?s\s+important\s+to\s+note|as\s+an?\s+(?:large\s+)?(?:language\s+model|ai\b|artificial\s+intelligence)|como\s+(?:um|uma)\s+(?:modelo\s+de\s+linguagem|ia\b|intelig[êe]ncia\s+artificial))
```

Values on the snapshot, canonical stratum:

| Engine | n | Preamble | Share | 95% CI | Cited | Rate |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 15,168 | 0 | 0.00% | [0.00, 0.03] | 2,604 | 17.17% |
| Claude | 15,034 | 0 | 0.00% | [0.00, 0.03] | 3,871 | 25.75% |
| Gemini | 15,355 | 12,288 | 80.03% | [79.39, 80.65] | 285 | 1.86% |
| Groq | 14,208 | 0 | 0.00% | [0.00, 0.03] | 1,210 | 8.52% |
| Perplexity | 7,741 | 308 | 3.98% | [3.57, 4.44] | 5,796 | 74.87% |
| Grok | 1,118 | 106 | 9.48% | [7.90, 11.34] | 331 | 29.61% |

**Divergence from manuscript v1.0.** The same pattern applied to the exact row set of manuscript v1.0 (canonical, `date(timestamp) <= '2026-08-31'`, 66,399 rows), against the published figures:

| Engine | n | This criterion | Published v1.0 | Difference |
|---|---:|---:|---:|---:|
| ChatGPT | 14,976 | 0.0% | 2.1% | -2.1 pp |
| Claude | 14,842 | 0.0% | 0.0% | +0.0 pp |
| Gemini | 14,587 | 82.3% | 79.6% | +2.7 pp |
| Groq | 14,208 | 0.0% | 1.1% | -1.1 pp |
| Perplexity | 7,436 | 4.0% | 9.2% | -5.2 pp |
| Grok | 350 | 9.1% | 4.0% | +5.1 pp |

The two criteria agree that Gemini is the outlier by a wide margin and that Claude is at zero. They disagree on Perplexity and Grok by a few percentage points, in opposite directions. The claim the paper rests on, that the arm with the most preamble is parametric and the retrieval-augmented arm has little, holds under both. A reader who prefers a different criterion can substitute one: the pattern is a constant in `_common.py` and every figure in T5 regenerates from it.

## T6. Rate by vertical and engine

Computed from the uniform-window re-extraction (V1), grouped by `llm` and `vertical`. The statement below returns the *as-collected* counts. For the five arms whose stored text never exceeded the window it returns exactly the counts tabulated here; for Perplexity it returns larger ones, and that difference is the window effect of Table 3 seen cell by cell.

```sql
SELECT llm, vertical, COUNT(*) AS n,
       SUM(CASE WHEN cited THEN 1 ELSE 0 END) AS cited
  FROM citations WHERE COALESCE(is_probe,0)=0 AND response_text IS NOT NULL
 GROUP BY llm, vertical;
```

| Engine | Vertical | n | Cited | Rate | 95% CI |
|---|---|---:|---:|---:|---:|
| ChatGPT | fintech | 3,792 | 687 | 18.12% | [16.92, 19.38] |
| ChatGPT | varejo | 3,792 | 849 | 22.39% | [21.09, 23.74] |
| ChatGPT | saude | 3,792 | 293 | 7.73% | [6.92, 8.62] |
| ChatGPT | tecnologia | 3,792 | 775 | 20.44% | [19.18, 21.75] |
| Claude | fintech | 3,792 | 1,926 | 50.79% | [49.20, 52.38] |
| Claude | varejo | 3,792 | 1,152 | 30.38% | [28.94, 31.86] |
| Claude | saude | 3,754 | 414 | 11.03% | [10.07, 12.07] |
| Claude | tecnologia | 3,696 | 379 | 10.25% | [9.32, 11.27] |
| Gemini | fintech | 3,840 | 169 | 4.40% | [3.80, 5.10] |
| Gemini | varejo | 3,840 | 96 | 2.50% | [2.05, 3.04] |
| Gemini | saude | 3,840 | 0 | 0.00% | [0.00, 0.10] |
| Gemini | tecnologia | 3,835 | 20 | 0.52% | [0.34, 0.80] |
| Groq | fintech | 3,552 | 334 | 9.40% | [8.49, 10.41] |
| Groq | varejo | 3,552 | 454 | 12.78% | [11.72, 13.92] |
| Groq | saude | 3,552 | 213 | 6.00% | [5.26, 6.83] |
| Groq | tecnologia | 3,552 | 209 | 5.88% | [5.16, 6.71] |
| Perplexity | fintech | 1,961 | 1,330 | 67.82% | [65.72, 69.85] |
| Perplexity | varejo | 1,940 | 1,326 | 68.35% | [66.25, 70.38] |
| Perplexity | saude | 1,920 | 855 | 44.53% | [42.32, 46.76] |
| Perplexity | tecnologia | 1,920 | 517 | 26.93% | [24.99, 28.96] |
| Grok | fintech | 288 | 170 | 59.03% | [53.27, 64.55] |
| Grok | varejo | 288 | 117 | 40.62% | [35.11, 46.38] |
| Grok | saude | 288 | 30 | 10.42% | [7.39, 14.48] |
| Grok | tecnologia | 254 | 14 | 5.51% | [3.31, 9.04] |
| **Panel** | fintech | 17,225 | 4,616 | 26.80% | [26.14, 27.46] |
| **Panel** | varejo | 17,204 | 3,994 | 23.22% | [22.59, 23.85] |
| **Panel** | saude | 17,146 | 1,805 | 10.53% | [10.08, 11.00] |
| **Panel** | tecnologia | 17,049 | 1,914 | 11.23% | [10.76, 11.71] |

## T7. Rate by language, query type and category

Same source as T6, grouped by `query_lang`, `query_type` and `query_category`.

### T7a, language

| Engine | Level | n | Cited | Rate | 95% CI |
|---|---|---:|---:|---:|---:|
| ChatGPT | pt | 7,584 | 843 | 11.12% | [10.43, 11.84] |
| ChatGPT | en | 7,584 | 1,761 | 23.22% | [22.28, 24.18] |
| Claude | pt | 7,518 | 1,864 | 24.79% | [23.83, 25.78] |
| Claude | en | 7,516 | 2,007 | 26.70% | [25.71, 27.71] |
| Gemini | pt | 7,677 | 66 | 0.86% | [0.68, 1.09] |
| Gemini | en | 7,678 | 219 | 2.85% | [2.50, 3.25] |
| Groq | pt | 7,104 | 375 | 5.28% | [4.78, 5.82] |
| Groq | en | 7,104 | 835 | 11.75% | [11.03, 12.52] |
| Perplexity | pt | 3,871 | 2,097 | 54.17% | [52.60, 55.74] |
| Perplexity | en | 3,870 | 1,931 | 49.90% | [48.32, 51.47] |
| Grok | pt | 560 | 148 | 26.43% | [22.95, 30.23] |
| Grok | en | 558 | 183 | 32.80% | [29.03, 36.80] |
| Panel | pt | 34,314 | 5,393 | 15.72% | [15.34, 16.11] |
| Panel | en | 34,310 | 6,936 | 20.22% | [19.79, 20.64] |

### T7b, query type

| Engine | Level | n | Cited | Rate | 95% CI |
|---|---|---:|---:|---:|---:|
| ChatGPT | directive | 7,584 | 2,424 | 31.96% | [30.92, 33.02] |
| ChatGPT | exploratory | 7,584 | 180 | 2.37% | [2.05, 2.74] |
| Claude | directive | 7,519 | 2,337 | 31.08% | [30.05, 32.14] |
| Claude | exploratory | 7,515 | 1,534 | 20.41% | [19.52, 21.34] |
| Gemini | directive | 7,679 | 210 | 2.73% | [2.39, 3.12] |
| Gemini | exploratory | 7,676 | 75 | 0.98% | [0.78, 1.22] |
| Groq | directive | 7,104 | 805 | 11.33% | [10.62, 12.09] |
| Groq | exploratory | 7,104 | 405 | 5.70% | [5.19, 6.26] |
| Perplexity | directive | 3,873 | 2,867 | 74.03% | [72.62, 75.38] |
| Perplexity | exploratory | 3,868 | 1,161 | 30.02% | [28.59, 31.48] |
| Grok | directive | 560 | 256 | 45.71% | [41.63, 49.86] |
| Grok | exploratory | 558 | 75 | 13.44% | [10.86, 16.52] |
| Panel | directive | 34,319 | 8,899 | 25.93% | [25.47, 26.40] |
| Panel | exploratory | 34,305 | 3,430 | 10.00% | [9.69, 10.32] |

### T7c, semantic category

| Engine | Level | n | Cited | Rate | 95% CI |
|---|---|---:|---:|---:|---:|
| ChatGPT | descoberta | 2,528 | 37 | 1.46% | [1.06, 2.01] |
| ChatGPT | comparativo | 2,528 | 720 | 28.48% | [26.76, 30.27] |
| ChatGPT | mercado | 2,528 | 754 | 29.83% | [28.07, 31.64] |
| ChatGPT | confianca | 2,528 | 594 | 23.50% | [21.89, 25.19] |
| ChatGPT | experiencia | 2,528 | 0 | 0.00% | [0.00, 0.15] |
| ChatGPT | inovacao | 2,528 | 499 | 19.74% | [18.23, 21.34] |
| Claude | descoberta | 2,512 | 1,303 | 51.87% | [49.92, 53.82] |
| Claude | comparativo | 2,512 | 706 | 28.11% | [26.38, 29.90] |
| Claude | mercado | 2,496 | 861 | 34.50% | [32.66, 36.38] |
| Claude | confianca | 2,512 | 496 | 19.75% | [18.24, 21.35] |
| Claude | experiencia | 2,506 | 158 | 6.30% | [5.42, 7.32] |
| Claude | inovacao | 2,496 | 347 | 13.90% | [12.60, 15.32] |
| Gemini | descoberta | 2,560 | 8 | 0.31% | [0.16, 0.62] |
| Gemini | comparativo | 2,560 | 110 | 4.30% | [3.58, 5.15] |
| Gemini | mercado | 2,560 | 83 | 3.24% | [2.62, 4.00] |
| Gemini | confianca | 2,560 | 4 | 0.16% | [0.06, 0.40] |
| Gemini | experiencia | 2,560 | 80 | 3.12% | [2.52, 3.87] |
| Gemini | inovacao | 2,555 | 0 | 0.00% | [0.00, 0.15] |
| Groq | descoberta | 2,368 | 228 | 9.63% | [8.50, 10.88] |
| Groq | comparativo | 2,368 | 420 | 17.74% | [16.25, 19.33] |
| Groq | mercado | 2,368 | 354 | 14.95% | [13.57, 16.44] |
| Groq | confianca | 2,368 | 151 | 6.38% | [5.46, 7.43] |
| Groq | experiencia | 2,368 | 23 | 0.97% | [0.65, 1.45] |
| Groq | inovacao | 2,368 | 34 | 1.44% | [1.03, 2.00] |
| Perplexity | descoberta | 2,584 | 1,543 | 59.71% | [57.81, 61.59] |
| Perplexity | comparativo | 2,584 | 1,411 | 54.61% | [52.68, 56.52] |
| Perplexity | mercado | 2,573 | 1,074 | 41.74% | [39.85, 43.66] |
| Perplexity | confianca | 0 | 0 | — | [nan, nan] |
| Perplexity | experiencia | 0 | 0 | — | [nan, nan] |
| Perplexity | inovacao | 0 | 0 | — | [nan, nan] |
| Grok | descoberta | 192 | 86 | 44.79% | [37.93, 51.86] |
| Grok | comparativo | 190 | 73 | 38.42% | [31.80, 45.50] |
| Grok | mercado | 184 | 57 | 30.98% | [24.74, 37.99] |
| Grok | confianca | 184 | 24 | 13.04% | [8.92, 18.67] |
| Grok | experiencia | 184 | 52 | 28.26% | [22.25, 35.16] |
| Grok | inovacao | 184 | 39 | 21.20% | [15.91, 27.66] |
| Panel | descoberta | 12,744 | 3,205 | 25.15% | [24.40, 25.91] |
| Panel | comparativo | 12,742 | 3,440 | 27.00% | [26.23, 27.78] |
| Panel | mercado | 12,709 | 3,183 | 25.05% | [24.30, 25.81] |
| Panel | confianca | 10,152 | 1,269 | 12.50% | [11.87, 13.16] |
| Panel | experiencia | 10,146 | 313 | 3.08% | [2.77, 3.44] |
| Panel | inovacao | 10,131 | 919 | 9.07% | [8.53, 9.65] |

Battery coverage by engine and category, which is the reason the panel row of T7c is not a category effect:

```sql
SELECT llm, query_category, COUNT(*) AS n
  FROM citations WHERE COALESCE(is_probe,0)=0
 GROUP BY llm, query_category;
```

| Engine | descoberta | comparativo | mercado | confianca | experiencia | inovacao |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 2,528 | 2,528 | 2,528 | 2,528 | 2,528 | 2,528 |
| Claude | 2,512 | 2,512 | 2,496 | 2,512 | 2,506 | 2,496 |
| Gemini | 2,560 | 2,560 | 2,560 | 2,560 | 2,560 | 2,555 |
| Groq | 2,368 | 2,368 | 2,368 | 2,368 | 2,368 | 2,368 |
| Perplexity | 2,584 | 2,584 | 2,573 | 0 | 0 | 0 |
| Grok | 192 | 190 | 184 | 184 | 184 | 184 |

## T8. Concentration of first mentions

First mentions are taken under the uniform 200-character window, from the re-extraction described in V1: for each canonical observation, the cohort entity with the lowest offset inside the window. Counted with `collections.Counter`.

| Quantity | Value |
|---|---:|
| observations carrying a first mention | 12,329 |
| distinct entities ever named first | 42 |
| cohort, distinct entities | 127 |
| Brazilian real firms named first | 31 of 79 |
| international anchors named first | 11 of 32 |
| fictitious decoys named first | 0 of 16 |
| cumulative share, top 1 | 37.2699% |
| cumulative share, top 3 | 65.6258% |
| cumulative share, top 5 | 76.9811% |
| cumulative share, top 10 | 89.2611% |
| Herfindahl-Hirschman index, 0 to 1 | 0.191654 |
| HHI equivalent number of participants (1/HHI) | 5.218 |
| Gini over named entities | 0.817563 |

Top ten:

| Rank | Entity | First mentions | Share |
|---:|---|---:|---:|
| 1 | Nubank | 4,595 | 37.2699% |
| 2 | Mercado Livre | 2,090 | 16.9519% |
| 3 | Magazine Luiza | 1,406 | 11.4040% |
| 4 | Totvs | 813 | 6.5942% |
| 5 | EMS Pharma | 587 | 4.7611% |
| 6 | Hypera Pharma | 540 | 4.3799% |
| 7 | Involves | 345 | 2.7983% |
| 8 | Accenture | 212 | 1.7195% |
| 9 | Americanas | 209 | 1.6952% |
| 10 | Walmart | 208 | 1.6871% |

Index definitions, stated so neither is guessed at:

```python
def hhi(counts):   # reported index
    total = sum(counts)
    return sum((c / total) ** 2 for c in counts)

def gini(counts):  # secondary, over named entities only
    xs, n, total = sorted(counts), len(counts), sum(counts)
    cum = sum((i + 1) * x for i, x in enumerate(xs))
    return (2 * cum) / (n * total) - (n + 1) / n
```

Distinct first entities under the as-collected window, for contrast:

```sql
SELECT COUNT(DISTINCT first_entity_v2) AS distinct_first_entities
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND first_entity_v2 IS NOT NULL;
```

Value: 53 against 42 under the uniform window.

### T8b. Lexical collisions in the cohort

Two cohort surface forms are ordinary words. Confirm the matched contexts before believing the counts:

```sql
SELECT llm, query_lang, substr(response_text,1,180)
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND first_entity_v2='Involves' LIMIT 6;
```

Frequencies of every entity ever matched, which is how the two were found:

```python
from collections import Counter; import json, sqlite3
con = sqlite3.connect("file:data/papers.db?mode=ro", uri=True)
c = Counter()
for (j,) in con.execute("SELECT cited_entities_v2_json FROM citations "
                        "WHERE COALESCE(is_probe,0)=0 AND cited_entities_v2_json IS NOT NULL"):
    for e in json.loads(j): c[e] += 1
print(c.most_common())
```

Sensitivity, computed in `build_tables.build` by removing ['Involves', 'Target'] from the matched entity list of each observation:

| Quantity | With collisions | Without |
|---|---:|---:|
| panel citations under the uniform window | 12,329 | 11,976 |
| panel citation rate | 17.9660% | 17.4516% |
| distinct entities named first | 42 | 40 |
| HHI | 0.191654 | 0.202289 |
| top-1 share | 37.2699% | 38.3684% |

| Detail | Value |
|---|---:|
| observations with at least one colliding match | 353 |
| observations cited only because of a collision | 353 |
| observations whose first mention is a collision | 353 |
| matches of `Involves` | 345 |
| matches of `Target` | 8 |
| collisions in `en` responses | 353 |
| collisions in Groq responses | 173 |
| collisions in ChatGPT responses | 158 |
| collisions in Gemini responses | 22 |

## T9. Calibration decoys in the canonical stratum

Extractors restricted to the sixteen decoys of `src/config_v2.FICTITIOUS_DECOYS_V2`, with no aliases and no stop contexts, run over the canonical rows twice: over `response_text[:200]` and over `response_text` as stored. Built by `_common.build_decoy_extractors`.

| Engine | Canonical n | Decoy in window | Decoy in stored text |
|---|---:|---:|---:|
| ChatGPT | 15,168 | 0 | 0 |
| Claude | 15,034 | 0 | 0 |
| Gemini | 15,355 | 0 | 0 |
| Groq | 14,208 | 0 | 0 |
| Perplexity | 7,741 | 0 | 0 |
| Grok | 1,118 | 0 | 0 |
| **Panel** | 68,624 | 0 | 0 |

Point estimate 0.0%; 95% Wilson interval [0.000000, 0.005598] percentage points, i.e. an upper bound of 3.84 expected occurrences in 68,624 observations.

The stored column agrees and is reported so the agreement is visible, but it is not independent evidence, because it was only ever populated on the probe stratum:

```sql
SELECT COUNT(*) AS n_canonical,
       SUM(COALESCE(fictional_hit,0)) AS flagged_in_canonical
  FROM citations WHERE COALESCE(is_probe,0)=0;
```

Value: 0 flagged rows in 68,624 canonical rows.

## T10. Adversarial stratum

```sql
SELECT llm,
       COUNT(*) AS n_probe,
       SUM(COALESCE(fictional_hit,0)) AS flagged_old_criterion
  FROM citations
 WHERE COALESCE(is_probe,0)=1
 GROUP BY llm;
```

The refusal marker is the regex of `VERIFICATION.md` section 5.3, reproduced verbatim in `_common.REFUSAL_PT` and `_common.REFUSAL_EN`, applied to:

```sql
SELECT llm, response_text
  FROM citations
 WHERE COALESCE(is_probe,0)=1 AND fictional_hit=1
   AND response_text IS NOT NULL AND length(response_text) > 0;
```

| Engine | Probe n | Flagged | Share | 95% CI | Flagged with text | With refusal marker | Share | 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 4,416 | 4,298 | 97.33% | [96.81, 97.76] | 4,298 | 2,897 | 67.40% | [65.99, 68.79] |
| Claude | 4,384 | 4,384 | 100.00% | [99.91, 100.00] | 4,384 | 4,053 | 92.45% | [91.63, 93.20] |
| Gemini | 4,463 | 4,032 | 90.34% | [89.44, 91.18] | 4,032 | 1,890 | 46.88% | [45.34, 48.42] |
| Groq | 4,096 | 4,084 | 99.71% | [99.49, 99.83] | 4,084 | 2,520 | 61.70% | [60.20, 63.18] |
| Perplexity | 192 | 164 | 85.42% | [79.73, 89.71] | 164 | 25 | 15.24% | [10.54, 21.54] |
| Grok | 368 | 366 | 99.46% | [98.04, 99.85] | 366 | 184 | 50.27% | [45.17, 55.37] |
| **Panel** | 17,919 | 17,328 | 96.70% | [96.43, 96.95] | 17,328 | 11,569 | 66.76% | [66.06, 67.46] |

VERIFICATION.md section 5.3 expects 15,993 flagged and 10,775 carrying a refusal marker, 67.4%, on the snapshot of 2026-08-31. This snapshot has 17,328 and 11,569, 66.8%: the same quantity on more data.

## T11. Temporal coverage

```sql
SELECT strftime('%Y-%m', timestamp) AS month,
       COUNT(*) AS n_canonical,
       COUNT(DISTINCT date(timestamp)) AS days_with_data
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY month ORDER BY month;
```

| Month | Days with data | Canonical n | Calendar days in span | Days missing |
|---|---:|---:|---:|---:|
| 2026-04 | 8 | 10,930 | 8 | 0 |
| 2026-05 | 23 | 25,899 | 31 | 8 |
| 2026-06 | 9 | 13,624 | 30 | 21 |
| 2026-07 | 0 | 0 | 31 | 31 |
| 2026-08 | 10 | 15,946 | 31 | 21 |
| 2026-09 | 3 | 2,225 | 8 | 5 |

The `GROUP BY` returns no row for 2026-07 because no observation exists in that month. The table above walks every month in the span so the empty month is visible rather than absent.

```sql
SELECT status, COUNT(*) AS n, MIN(date(timestamp)) AS first_day,
       MAX(date(timestamp)) AS last_day
  FROM collection_runs GROUP BY status;
```

| Status | n | First day | Last day |
|---|---:|---|---|
| `aborted` | 344 | 2026-05-02 | 2026-09-05 |
| `success` | 328 | 2026-04-23 | 2026-09-08 |

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT date(timestamp)) AS distinct_days,
       substr(MIN(error_msg),1,60) AS reason_prefix
  FROM collection_runs WHERE status='aborted';
```

344 rows over 86 distinct days, all carrying the same reason, which begins `gap sem coleta persistida — restore do artifact nunca trouxe`. These are retroactive gap markers written by `scripts/mark_collection_gaps.py`, not observed failures.

Partial days are derived from:

```sql
SELECT date(timestamp) AS day, llm,
       COUNT(*) AS n,
       COUNT(DISTINCT query) AS distinct_queries
  FROM citations
 WHERE COALESCE(is_probe,0)=0
 GROUP BY day, llm
 ORDER BY day, llm;
```

The registry `data/partial_days.json` is read directly; present = True, 5 entries, of which 2 fall inside the snapshot span 2026-04-23 to 2026-09-08 and 3 fall after it. No script in the repository writes or reads that file on the analysis path, so it is treated as a hand-kept record, authoritative on what it covers and silent on the rest of the series.

| Registry day | Engines missing | Inside snapshot span |
|---|---|---|
| 2026-09-06 | ChatGPT, Claude | yes |
| 2026-09-07 | ChatGPT, Claude | yes |
| 2026-09-10 | Claude, Gemini | no |
| 2026-09-10 | ChatGPT, Claude | no |
| 2026-09-11 | ChatGPT | no |

Agreement between the registry and the derived rule, on the days both cover:

| Day | Registry says missing | Derived rule says absent | Match |
|---|---|---|---|
| 2026-09-06 | ChatGPT, Claude | ChatGPT, Claude | yes |
| 2026-09-07 | ChatGPT, Claude | ChatGPT, Claude | yes |

The derived rule is implemented in `build_tables.build`:

```python
# battery size = the largest distinct-query count the engine ever reached
# in one day; a day is partial when some engine active in the surrounding
# period is short of its battery or absent altogether
battery[e] = max(per_day[d][e]['uq'] for d in days if e in per_day[d])
short  = [e for e in engines if e in per_day[d]
          and per_day[d][e]['uq'] < battery[e]]
absent = [e for e in engines if e not in per_day[d]
          and active_span[e][0] <= d <= active_span[e][1]]
```

| Engine | Battery size inferred |
|---|---:|
| ChatGPT | 192 |
| Claude | 192 |
| Gemini | 192 |
| Groq | 192 |
| Perplexity | 96 |
| Grok | 192 |

Result: 19 partial days out of 53 days with data, listed in TABLES.md Table 11.

## T12. Descriptive temporal stability

Daily rates come from the uniform-window re-extraction (V1) grouped by `llm` and `date(timestamp)`, keeping only days with at least 30 canonical observations for that engine. The slope is ordinary least squares of daily rate in percentage points on days elapsed since 2026-04-23, implemented in `_common.ols_slope`; the interval is a residual-based normal interval and is descriptive only.

| Engine | Days used | n | Slope pp/day | Interval low | Interval high | Min daily | Max daily |
|---|---:|---:|---:|---:|---:|---:|---:|
| ChatGPT | 51 | 15,168 | +0.001085 | -0.005259 | +0.007430 | 15.62% | 19.43% |
| Claude | 51 | 15,034 | -0.006072 | -0.029819 | +0.017676 | 9.62% | 34.96% |
| Gemini | 52 | 15,355 | +0.018323 | +0.013103 | +0.023544 | 0.35% | 7.29% |
| Groq | 48 | 14,208 | +0.017134 | +0.010934 | +0.023334 | 5.66% | 10.42% |
| Perplexity | 51 | 7,700 | -0.043290 | -0.090594 | +0.004014 | 38.89% | 70.13% |
| Grok | 5 | 1,118 | -0.275887 | -2.258192 | +1.706418 | 21.53% | 51.04% |

```python
def ols_slope(xs, ys):
    n  = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    sxx = sum((x-mx)**2 for x in xs)
    b   = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sxx
    a   = my - b*mx
    s2  = sum((y-(a+b*x))**2 for x, y in zip(xs, ys)) / (n-2)
    se  = (s2/sxx) ** 0.5
    return b, b - 1.959963984540054*se, b + 1.959963984540054*se
```

## T13. Window effect on every arm

Produced by `window_analysis.py`, which selects:

```sql
SELECT id, timestamp, llm, vertical, query_lang, query_type,
       response_text, response_full_text, cited_v2
  FROM citations
 WHERE COALESCE(is_probe,0)=0
   AND response_full_text IS NOT NULL
   AND length(response_full_text) > 0
 ORDER BY id;
```

and, for each row, extracts over `response_full_text[:200]` and over `response_full_text` with the same extractor.

| Check | Mismatches | Verdict |
|---|---:|---|
| `response_text` == `response_full_text[:200]` | 0 | PASS |
| re-extraction of the first 200 chars == stored `cited_v2` | 0 | PASS |
| rows compared | 2,225 | — |

| Engine | n | Cited at 200 | Rate | 95% CI | Cited on full | Rate | 95% CI | Δ pp | Gains | Losses | McNemar p | Mean full len | Median full len | Max full len | Rows > 200 | Dates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ChatGPT | 192 | 33 | 17.1875% | [12.51, 23.15] | 103 | 53.6458% | [46.59, 60.56] | +36.4583 | 70 | 0 | 1.694e-21 | 1,894.7 | 1,894 | 4,088 | 192 | 2026-09-08 |
| Claude | 192 | 48 | 25.0000% | [19.41, 31.57] | 127 | 66.1458% | [59.19, 72.46] | +41.1458 | 79 | 0 | 3.309e-24 | 1,194.4 | 1,130 | 3,072 | 192 | 2026-09-08 |
| Gemini | 768 | 20 | 2.6042% | [1.69, 3.99] | 256 | 33.3333% | [30.09, 36.74] | +30.7292 | 236 | 0 | 1.811e-71 | 1,895.3 | 452 | 19,777 | 390 | 2026-09-06, 2026-09-07, 2026-09-08 |
| Perplexity | 305 | 165 | 54.0984% | [48.49, 59.61] | 235 | 77.0492% | [72.01, 81.41] | +22.9508 | 70 | 0 | 1.694e-21 | 556.2 | 528 | 1,032 | 305 | 2026-09-06, 2026-09-07, 2026-09-08 |
| Grok | 768 | 218 | 28.3854% | [25.31, 31.68] | 646 | 84.1146% | [81.36, 86.53] | +55.7292 | 428 | 0 | 2.885e-129 | 2,014.6 | 1,991 | 4,263 | 767 | 2026-09-06, 2026-09-07, 2026-09-08 |

Gemini stratified by day, which is why the pooled Gemini row understates the effect:

| Day | n | Cited at 200 | Cited on full | Mean full length |
|---|---:|---:|---:|---:|
| 2026-09-06 | 384 | 6 | 6 | 142.6 |
| 2026-09-07 | 96 | 7 | 65 | 3,539.7 |
| 2026-09-08 | 288 | 7 | 185 | 3,684.0 |
| **2026-09-07 and 2026-09-08** | 384 | 14 | 250 | 3,648.0 |

Restricted to those two days: 3.6458% [2.18, 6.03] at 200 characters against 65.1042% [60.21, 69.70] on the full text, +61.4583 pp.

Mean entities found per observation, which is the same effect counted without the binary threshold:

| Engine | Mean entities in first 200 chars | Mean entities in full text | Median first-mention offset in full text |
|---|---:|---:|---:|
| ChatGPT | 0.2344 | 1.8594 | 245.0 |
| Claude | 0.3490 | 2.3438 | 241.0 |
| Gemini | 0.0404 | 1.7943 | 549.5 |
| Perplexity | 1.0689 | 2.4590 | 114.0 |
| Grok | 0.5781 | 4.3451 | 311.5 |

Groq contributes no rows: it left the panel on 2026-08-16 and full-text retention began on 2026-08-31. Verify with:

```sql
SELECT llm, COUNT(*) AS canonical_rows_with_full_text
  FROM citations
 WHERE COALESCE(is_probe,0)=0 AND response_full_text IS NOT NULL
   AND length(response_full_text) > 0
 GROUP BY llm;
```

## Rule

No figure enters `TABLES.md` without appearing in this file with the statement that produces it. A figure in the tables and not here either came from a measurement nobody can repeat, or came from nowhere.

Two figures in `TABLES.md` are not reproducible from the database alone and are flagged as such where they appear: the architectural class of each engine in Table 1, which is editorial and taken from MANUSCRIPT.md Table 3; and the preamble regular expression in Table 5, which is a re-specification of a criterion that manuscript v1.0 described but never committed.

