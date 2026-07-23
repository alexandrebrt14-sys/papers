
================================================================
ESCALONAMENTO CLOUD SUGERIDO (precisa da sua permissão)
----------------------------------------------------------------
  Motivos     : --provider explicito
  Modelo cloud: OpenAI · GPT-5.5
  Por que     : provider forcado pelo usuario (--provider openai)
  Custo est.  : ~$0.0314 USD (estimativa)
  Via         : API direta
================================================================
Permissão: auto-aprovada (--yes)
1. **§0/§1 — UCP/AI Mode no Brasil está superafirmado.** “Checkout do Universal Commerce Protocol no AI Mode brasileiro desde 19-mai-2026” é claim central, mas em §9 a fonte é imprensa/associação, não Google. Para premissa canônica, exige fonte primária do Google ou rebaixar para “reportado por imprensa; pendente de confirmação primária”.

2. **§0/§8.2 — Contradição sobre checkout agêntico.** O TL;DR diz que UCP/checkout já está ativo no AI Mode brasileiro desde mai/2026; §2/§8.2 recomenda copy “checkout agêntico é 2027/amanhã”. Harmonizar: ou já é superfície operacional em 2026, ou é piloto/rollout limitado.

3. **§1 — “Sem esperar o ACP da OpenAI” mistura protocolos sem definição.** ACP/UCP/AP2/Stripe aparecem como se fossem comparáveis e consolidados. Precisa definir nomes oficiais, mantenedores e status; do contrário há risco de confundir protocolo de pagamento, checkout em app e integração comercial.

4. **§2 — “CONFIRMADO” está mal rotulado para OpenAI via imprensa.** “Relatório da OpenAI via Fast Company/Softex” não é fonte primária acessada diretamente. Rótulo correto: `vendor_sobre_si via secundária`; confiança menor, com URL do relatório original ou remoção do “CONFIRMADO”.

5. **§2 — 93% “uso de ferramenta com IA” não sustenta “adoção massiva de topo de funil” para GEO/genAI.** Se a pesquisa inclui IA embutida, recomendadores, filtros, autocorreção etc., não equivale a uso consciente de ChatGPT/Gemini nem busca por IA. A inferência comercial está inflada.

6. **§2 — Dados heterogêneos estão agregados como se fossem comparáveis.** Vendor, Datafolha, Opinion Box, Canaltech e relatório de agência têm bases, perguntas e universos diferentes. A leitura consolidada precisa explicitar amostra/metodologia ou evitar porcentagens lado a lado como premissa operacional.

7. **§3 — “Conteúdo licenciado tende a ganhar presença estrutural” é hipótese, não implicação factual.** Licenciamento pode afetar treinamento, grounding, exibição, atribuição ou nada disso publicamente. Rebaixar para “hipótese testável”; não afirmar “valor GEO direto e mensurável” sem série temporal.

8. **§3/§9 c3 — “Encerra a ação judicial da Folha” exige prova processual.** Acordo comercial não necessariamente extingue ação. Precisa de número do processo, decisão homologatória/desistência, ou frase mais segura: “foi reportado como associado ao encerramento/à resolução da disputa”.

9. **§3 — CADE: “processo administrativo” pode estar juridicamente impreciso.** No CADE há procedimento preparatório, inquérito administrativo, processo administrativo sancionador, estudo de mercado etc. Especificar classe, órgão responsável e número; “processo administrativo sobre Google e jornalismo” é vago e pode ser errado.

10. **§4 — PL 2338: “mesmo aprovado, volta ao Senado” está errado ou incompleto.** Só volta ao Senado se a Câmara alterar o texto aprovado pelo Senado. Se aprovado sem alterações, segue à sanção/veto. Corrigir.

11. **§4 — PL 2338: multas e “modelo AI Act” precisam de qualificação de versão.** “Multas até R$ 50M” depende do substitutivo vigente; pode haver teto alternativo por faturamento/infração. Citar artigo/versão/data e marcar como projeto, não regime vigente.

12. **§4 — “Enquanto isso valem LGPD + ANPD + CONAR + ECA Digital” mistura naturezas normativas.** LGPD é lei; atos da ANPD podem ser regulatórios/orientativos; CONAR é autorregulação publicitária; ECA Digital tem escopo específico. Não tratar tudo como “marco legal” equivalente.

13. **§4 — CONAR não “cria responsabilidade solidária” em sentido legal amplo.** Guia do CONAR pode atribuir corresponsabilidade ética/publicitária entre anunciante, agência e influenciador, mas não cria por si só responsabilidade civil solidária como lei. Redigir como “corresponsabilidade no âmbito autorregulatório, sem prejuízo de responsabilidades legais”.

14. **§4 — LGPD está simplificada demais.** “Coleta/uso de dados pessoais em prompts e pipelines segue regida pela LGPD” é correto, mas insuficiente: incluir base legal, finalidade, minimização, transparência, operador/controlador, transferência internacional, dados sensíveis, crianças/adolescentes, retenção, segurança e art. 20 para decisões automatizadas.

15. **§4 — Sandbox da ANPD não é salvo-conduto.** Se citar participantes e “ativo”, deixar claro que sandbox não autoriza descumprimento da LGPD nem valida produto/cliente. Evitar que agentes leiam como chancela regulatória.

16. **§5 — Claims de mercado são frágeis e autorreferidos.** “<5% das agências”, “1,2% das empresas”, preços de concorrentes, “barato de liderar” e “mais lastro técnico que qualquer player” são claims comerciais comparativos sem base independente. Risco de publicidade enganosa/denigração; rotular como opinião interna ou remover.

17. **§6.1 — “Em estado selvagem” precisa separar exploração real de PoC.** Comet/Atlas/CometJacking parecem demonstrações de pesquisa; Unit 42/Google seriam observações reais. Não misturar “demonstrado”, “observado in the wild” e “risco teórico” no mesmo nível de evidência.

18. **§6.2 — “Sanitizar TODO conteúdo” é recomendação vaga e tecnicamente insuficiente.** Escapar HTML/remove script não impede prompt injection por texto visível. Incluir isolamento de conteúdo não confiável, delimitação, política de não execução de instruções vindas de página, least privilege, allowlists de ações, confirmação humana e testes red-team.

19. **§6.3 — Web Bot Auth/Signed Agents está tratado como padrão mais maduro do que parece.** Verificar se há WG formal, draft, RFC, header `Signature-Agent`, algoritmos obrigatórios e participantes. RFC 9421 existe, mas uso específico para bots/agentes pode ainda ser draft/vendor. Não recomendar como “padrão” para controle crítico sem fallback.

20. **§9 — Machine-readable claims têm confiança e tipo de fonte inconsistentes.** c1 usa imprensa/consultoria/DIAP parcial mas `confianca: alta`; c4 chama CONAR de `doc_oficial` e embute “responsabilidade solidária” juridicamente perigosa; c5 usa imprensa para claim global Google; c7 mistura blog de vendor, OpenAI e Unit 42. Rebaixar confiança, separar claims e exigir URLs primárias com data de acesso.
