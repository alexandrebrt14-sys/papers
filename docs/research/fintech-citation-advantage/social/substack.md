SUBJECT: Tirei uma marca da conta e o setor inteiro mudou de lugar
PREHEADER: 62.820 perguntas a cinco IAs, quatro setores, uma descoberta incômoda sobre quem os modelos realmente citam.

---

Oi,

Esta semana publiquei um working paper que começou com uma pergunta simples e terminou desmontando uma das crenças mais repetidas no mercado de IA.

A pergunta era: por que a fintech é a vertical mais citada espontaneamente pelos modelos de linguagem? Reuni 62.820 observações entre 23 de abril e 9 de junho, em cinco motores — ChatGPT, Claude, Gemini, Perplexity e Groq — sobre quatro setores brasileiros: fintech, varejo, tecnologia e saúde. E os dados confirmaram o folclore: a fintech lidera, com 28,15% das menções, contra 24,94% do varejo, 14,50% da tecnologia e 13,35% da saúde.

Aí eu puxei um fio. E o ranking inteiro desabou.

## O número da semana

> **49,7%** — a fatia de TODAS as menções de fintech que vão para uma única marca: o Nubank.

Quando removi da contagem as respostas que citam só o Nubank, a taxa da fintech caiu de 28,15% para **11,46%**. A vertical que liderava foi para o último lugar. A razão de chances de ser citada, comparada à da saúde, inverteu: de 4,13 para 0,77.

Ou seja: a "vantagem do setor" não era do setor. Era de uma empresa. O resto da fintech, sem o Nubank, é o pior colocado da amostra.

## Por que isso importa para você

Não é uma curiosidade sobre o Nubank. É um padrão que se repete em todo lugar:

- No **varejo**, tirar só o Mercado Livre derruba o setor 5,67 pontos; tirar Mercado Livre **e** Magazine Luiza juntos derruba 14,35 pontos. O varejo tem duas âncoras em vez de uma.
- Em **tecnologia** e **saúde**, a mesma lógica, com âncoras mais fracas (Totvs e Hypera).

A diferença entre os setores não é "ter ou não ter concentração". É quantas marcas-âncora cada um tem. Todo setor é dirigido pelas suas duas ou três marcas do topo. O que parece preferência do modelo por uma vertical é, na real, gravidade de marca.

E tem um detalhe que me deixou de queixo caído: o share do Nubank **cresceu durante o próprio experimento**, de 41% para 57% em menos de dois meses. O rico ficou mais rico enquanto eu media. A taxa agregada da fintech parecia estável — mas só porque a cauda (PicPay, Inter, C6) encolhia na mesma medida em que a âncora crescia. Calmaria na superfície, concentração disparando por baixo.

Mais um achado que joga água na ideia de "vantagem sistemática": só **2 dos 5 motores** colocam a fintech acima do varejo. Os outros três mostram o contrário. Quase todo o excedente vem de um único modelo (o Claude, com um gap de 40 pontos entre fintech e tecnologia). Dominar um LLM não é dominar os outros.

## A lição que mudou como eu penso GEO

Eu passei a olhar para isso de um jeito diferente, e acho que vale para qualquer um que se importe em ser lembrado pela IA.

A intuição diz: "esteja na vertical certa". Os dados dizem: **a vertical é epifenômeno, a âncora é o ativo**. Não adianta ser mais uma marca num setor citado. O que vale é ser **a** marca que o modelo cospe por padrão quando a categoria aparece. O Nubank não é "uma opção de banco digital" para os modelos — ele ocupa o lugar de "banco digital brasileiro".

Três coisas que eu tiraria disso, na prática:

1. A meta de GEO não é aparecer. É virar o nome canônico da categoria.
2. Meça motor por motor. Visibilidade em IA não é um número só.
3. A chance está nos setores fragmentados, onde nenhuma marca virou âncora ainda — tecnologia B2B é o terreno mais aberto.

Uma ressalva honesta, que está no paper: os números absolutos são lidos como limite superior (o texto coletado foi truncado nos primeiros 200 caracteres em quatro dos cinco motores, e os modelos são de tier econômico). Isso pede cautela com cada ponto percentual — mas não muda a direção do achado. A inversão sob remoção da âncora aguenta todos os testes de robustez que eu rodei.

## Leia o estudo completo

A metodologia, as cinco predições falsificáveis e a decomposição por motor estão no paper: **[alexandrecaramaschi.com/publicacoes/anchor-entity-effect](https://alexandrecaramaschi.com/publicacoes/anchor-entity-effect)** (espelho em [brasilgeo.ai/pesquisa/anchor-entity-effect](https://brasilgeo.ai/pesquisa/anchor-entity-effect)). O PDF e o dataset bruto, com os scripts de análise, estão abertos em **[github.com/alexandrebrt14-sys/papers](https://github.com/alexandrebrt14-sys/papers)**.

Se essa edição te fez pensar em alguma marca — a sua ou a do seu cliente —, encaminha para quem precisa ver. É o tipo de coisa que muda uma estratégia de conteúdo inteira quando cai na mesa certa.

Até a próxima,
Alexandre

*Alexandre Caramaschi — CEO da Brasil GEO, ex-CMO da Semantix (Nasdaq), cofundador da AI Brasil.*
