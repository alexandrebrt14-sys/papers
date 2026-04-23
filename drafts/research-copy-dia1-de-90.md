# Copy /research — Dia 1 de 90 (pronto para JSX)

## 1. Badge/banner topo

- Versão A (neutra): `Dia 1 de 90 · Janela confirmatória v2 · Próxima coleta 06:00 BRT`
- Versão B (urgência científica): `Coleta ao vivo · Dia 1/90 · Dataset bloqueado até 21/07/2026`
- Versão C (convidando acompanhamento): `Acompanhe em tempo real · Dia 1 de 90 · Atualização diária 06:00 BRT`

## 2. Hero subtitle

Esta página expõe, em tempo real, o dataset da janela confirmatória v2 em construção. A cada dia acumulamos novas observações das 5 LLMs sobre empresas brasileiras, conforme protocolo pré-registrado antes da coleta começar.

## 3. Estado atual da coleta

Estamos no **dia {day} de 90** da janela confirmatória v2, iniciada em 23/04/2026 e programada para fechar em 21/07/2026. O dataset acumula **{total} observações** coletadas até o momento, distribuídas conforme o desenho fatorial pré-registrado.

**Distribuição por vertical:** {byVertical}
**Distribuição por LLM:** {byLLM}

Todas as observações seguem a bateria balanceada de 192 queries sobre a cohort de 127 entidades (79 brasileiras, 32 âncoras internacionais, 16 decoys). A taxonomia, os prompts e os parâmetros de temperatura foram congelados antes da primeira coleta e permanecem imutáveis até o dia 90.

**Última atualização:** {lastUpdate}

## 4. Como o dataset cresce

Duas coletas automatizadas rodam por dia, às **06:00 e 18:00 BRT**, via GitHub Actions. Cada execução percorre 4 verticais × 48 queries × 5 LLMs, gerando aproximadamente **960 observações diárias**. Ao final de cada run, o pipeline faz commit direto no repositório `papers`, com manifest SHA-256 para garantir reprodutibilidade bit-a-bit. O dataset é público desde o primeiro registro — sem embargo, sem versão privada, sem curadoria posterior.

## 5. Próximos marcos

- **Dia 3 (25/04/2026):** potência estatística de H1 atingida (detecção do efeito-âncora)
- **Dia 38 (30/05/2026):** potência estatística de H2 atingida (assimetria de instrumentação)
- **Dia 90 (21/07/2026):** fechamento da janela confirmatória e congelamento do dataset
- **Outubro/2026:** submissão do Paper 5 à Elsevier

## 6. Disclaimer de transparência

A metodologia foi **pré-registrada no OSF** (protocolo em {osfUrl}) antes da primeira coleta, incluindo hipóteses, critérios de decisão e regras de correção por FDR (Benjamini-Hochberg). Não há resultado buscado: o Paper 4 ("Null-Triad", Zenodo DOI 10.5281/zenodo.19712217) já documentou publicamente três falhas metodológicas da v1. Comprometemo-nos a reportar, no Paper 5, tanto achados positivos quanto null findings.
