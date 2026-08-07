
================================================================
ESCALONAMENTO CLOUD SUGERIDO (precisa da sua permissão)
----------------------------------------------------------------
  Motivos     : --provider explicito
  Modelo cloud: Google · Gemini 2.5 Flash
  Por que     : provider forcado pelo usuario (--provider google)
  Custo est.  : ~$0.0048 USD (estimativa)
  Via         : API direta
================================================================
Permissão: auto-aprovada (--yes)
Como revisor crítico sênior e segunda opinião, analisei o documento `GEO_WAVE_JULHO_22_2026_CANONICAL.md` com foco em problemas graves que justificariam um commit de correção imediato. Foram identificados os seguintes pontos:

1.  **Contradição interna no número de IDs verificados**
    *   **§0. Sumário executivo / §1. O corpus científico 2026 / §8.1. `papers` (pesquisa acadêmica) / Apêndice · método desta wave:** O documento inicia afirmando que existem "32 papers únicos relevantes no arXiv" (§0) e que "os 32 IDs abaixo foram retornados pela API do arXiv" (§1). No entanto, nas seções de aplicação e método, afirma-se que "os 33 IDs deste doc foram verificados via API em 22-jul-2026" (§8.1 e Apêndice). Esta é uma contradição numérica direta e factual sobre o tamanho do corpus central do documento.

2.  **Inconsistência na categorização temporal dos IDs de papers**
    *   **§0. Sumário executivo:** A descrição do corpus afirma "32 papers únicos relevantes no arXiv (31 com ID de 2026; 1 submetido em 30-dez-2025 e anunciado em jan/2026)". O paper `arXiv:2601.00869` é explicitamente mencionado como o "1 submetido em 30-dez-2025". No entanto, seu ID (`2601.00869`) indica que ele foi anunciado em janeiro de 2026, o que o qualifica como um "ID de 2026" (pois começa com `26`). A categorização `(31 com ID de 2026; 1 submetido em 30-dez-2025...)` sugere categorias mutuamente exclusivas que somam 32, mas o `2601.00869` pertence a ambas as descrições, tornando a contagem e a categorização semanticamente confusas e, portanto, um erro factual na descrição do corpus.

3.  **Instrução que induz agente a erro (ponteiro obsoleto)**
    *   **§8.3. `curso-factory` (fábrica de cursos):** A instrução "Corrigir ponteiro obsoleto no CLAUDE.md: a linha que referencia `docs/knowledge/geo-aeo/` aponta para pasta inexistente; substituir pela trilha de waves" descreve um erro funcional em um documento associado. Embora o erro não esteja no corpo principal do `GEO_WAVE_JULHO_22_2026_CANONICAL.md`, a instrução contida nele induz um agente ou usuário a um caminho inexistente, falhando na sua execução e caracterizando um problema grave que merece correção.

Esses são os problemas graves remanescentes que justificam um commit de correção.
