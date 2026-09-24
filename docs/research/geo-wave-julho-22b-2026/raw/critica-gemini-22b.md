
================================================================
ESCALONAMENTO CLOUD SUGERIDO (precisa da sua permissão)
----------------------------------------------------------------
  Motivos     : --provider explicito
  Modelo cloud: Google · Gemini 2.5 Flash
  Por que     : provider forcado pelo usuario (--provider google)
  Custo est.  : ~$0.0033 USD (estimativa)
  Via         : API direta
================================================================
Permissão: auto-aprovada (--yes)
A revisão crítica identificou um problema grave remanescente que justifica um commit de correção:

*   **§2.2 - Contradição interna / Instrução que induz a erro:**
    *   **Problema:** A seção é intitulada "Postura canônica Brasil GEO ('citável sem ceder treino')". No entanto, o snippet de `robots.txt` fornecido na "OPÇÃO RESTRITIVA" (para clientes com conteúdo proprietário sensível) inclui a diretiva `User-agent: Google-Extended` `Allow: /`. A própria documentação, logo abaixo na condição (c), afirma que o Google-Extended "controla uso em treino de futuras gerações Gemini e em grounding". Permitir o Google-Extended significa *ceder o conteúdo para treino* no ecossistema Gemini, o que contradiz diretamente o objetivo declarado de "ficar citável **sem ceder treino**". A instrução atual levaria o agente a crer que está implementando uma postura de "sem ceder treino" para o Google-Extended, quando, na verdade, está fazendo o oposto.
    *   **Correção sugerida:** Para a "OPÇÃO RESTRITIVA" sob o título "citável sem ceder treino", a diretiva para Google-Extended deveria ser `Disallow: /`. Caso a intenção seja, de fato, permitir o treino para Google-Extended mesmo na opção restritiva, o título da seção ou a descrição da opção devem ser ajustados para refletir essa nuance e evitar a contradição.
