---
name: produto
description: >
  Transforma o que uma pessoa já sabe, já faz e já resolve num produto digital rápido de consumir
  e desenhado pra execução: o aluno termina com um artefato pronto na mão, não com aulas assistidas.
  Faz a extração do repertório, escolhe o problema com base em dado real de demanda, define o
  artefato final, decompõe a linha de execução passo a passo, escreve o roteiro aula a aula,
  monta preço/página/validação (vender antes de produzir) e a porta pro próximo produto.
  Use quando o usuário disser "/produto", "criar um infoproduto", "transformar meu conhecimento
  em produto", "montar um curso", "quero vender o que eu sei", "criar um produto digital",
  "estruturar minha mentoria/workshop", ou pedir pra desenhar uma oferta de conhecimento do zero.
---

# /produto — Produto que é comprado rápido, consumido de verdade e puxa o próximo

A maioria dos produtos de conhecimento falha por desenho, não por conteúdo. Curso longo compete
com feed, streaming e a vida do comprador, perde a disputa, e a culpa cai no produto ("era ruim")
quando o que aconteceu foi que ninguém chegou ao fim nem executou nada.

Esta skill constrói o oposto: **um produto curto, com uma linha lógica única, que leva a pessoa
a executar enquanto consome.** Ela sai com conhecimento novo, sim, e com a base conceitual pra
não improvisar. Mas o peso está na execução.

## As três taxas

Todo produto de conhecimento é julgado por três números. Cada decisão desta skill serve a um deles.

| Taxa | O que mede | O que a resolve |
|---|---|---|
| **Compra** | quanta gente decide entrar | problema ardente e específico + promessa que se distingue |
| **Consumo** | quanta gente chega ao fim e executa | escopo curto + linha única + artefato como destino |
| **Recompra** | quanta gente volta pro próximo | o produto termina nomeando o problema seguinte |

Produto que vende e ninguém consome não se sustenta: sem resultado não há boca a boca, e sem boca
a boca a venda depende só de tráfego pago pra sempre.

## Não confundir com

| Skill | O que faz |
|---|---|
| **esta** | desenha e escreve o **produto** (o que se entrega) do zero |
| `/diagnostico` | extrai Tese, Mecanismo e Oferta do **posicionamento** da pessoa/negócio |
| `/copy-lp` | escreve a **copy da página de vendas** de uma oferta já definida |
| `/content-hacking` | disseca conteúdo de terceiro pra virar pauta — entrada, não saída |

Se o posicionamento ainda não existe, rodar `/diagnostico` antes: a Tese alimenta a Etapa 3 daqui.
Se o produto já está desenhado e falta a página, é `/copy-lp`.

## Dependências

- **Contexto:** `_contexto/empresa.md` (o que a pessoa faz), `_contexto/preferencias.md` (tom e
  proibições de linguagem), `_contexto/posicionamento.md` (Tese e Mecanismo, se existirem),
  `_contexto/estrategia.md` (foco atual) — quando existirem.
- **Pesquisa de demanda:** `WebSearch` + `WebFetch` (nativas).
- **Tokens da marca:** `marca/design.json` — só na Etapa 6, se houver peça visual (capa, checklist,
  PDF). Não improvisar cor ou fonte.
- **Saída:** `produtos/<slug-do-produto>/` — ou o que o `CLAUDE.md` da raiz definir.
  **Se a raiz definir esteira própria de produtos, ela manda.**

## Arquivos de apoio

Ler sob demanda, na etapa em que entram:

| Arquivo | Quando |
|---|---|
| `references/demanda.md` | Etapa 1 — onde o dado de demanda mora e como ler |
| `references/linha.md` | Etapa 2 — artefato, decomposição, exclusão deliberada |
| `references/ancora.md` | Etapa 3 — a frase-âncora, o teste de honestidade, as 6 rotas de nome |
| `references/roteiro.md` | Etapa 5 — estrutura de aula, vitória rápida, títulos |
| `references/venda.md` | Etapa 6 — preço, checkout como página, validação antes de produzir |
| `references/esteira.md` | Etapa 7 — pós-venda e a porta do próximo produto |

---

## O princípio que rege tudo: o artefato

> **O produto não é o que você ensina. É o que a pessoa termina com na mão.**
> Desenha do artefato pra trás.

Artefato é uma coisa concreta que passa a existir por causa do produto: uma planilha preenchida,
um perfil reconstruído, uma proposta pronta pra enviar, uma campanha no ar, um plano de 90 dias
escrito, um site publicado. É o que o comprador aponta e diz "isso aqui não existia antes".

Um único ponto de partida resolve as três taxas:

- **Compra** — artefato concreto é promessa verificável. "Você sai com X pronto" vende mais fácil
  que "você vai entender Y", porque o comprador consegue imaginar a posse.
- **Consumo** — quando o destino é uma coisa, cada aula vira um passo obrigatório e curto, e o
  aluno mede progresso em peça pronta, não em vídeo assistido. Ele não precisa de disciplina, ele
  precisa da próxima peça.
- **Recompra** — quem termina com o artefato funcionando bate no **próximo gargalo**, e passa a ter
  um problema novo, mais caro e mais específico. Aí nasce o próximo produto.

**A régua de corte que vem daí, e que decide quase tudo:**

> Se a aula não move uma peça do artefato, ela sai.

Não importa quão boa ela é, quão interessante o tema é, quanto você sabe daquilo. Sai. É o critério
que impede o produto de inchar, e é a diferença entre um curso e uma linha de execução.

### As três falhas e onde elas nascem

| Falha | Causa real | Onde a skill trata |
|---|---|---|
| **Ninguém compra** | problema criado pelo autor, não pedido pelo mercado | Etapa 1 |
| **Compra e não consome** | escopo largo, caminho com bifurcações, sem artefato | Etapas 2 e 4 |
| **Consome e não volta** | o produto acaba em lugar nenhum | Etapa 7 |

### O erro que mais mata produto antes de nascer

Quem se dispõe a ensinar estuda mais que a média. Isso puxa o interesse pra temas avançados, que
a audiência **ainda não sabe que existem** — e o produto nasce sobre algo que ninguém pediu.

O sintoma é reconhecível: a ideia é intelectualmente empolgante, o autor não tem case nem bagagem
naquilo, e ninguém nunca perguntou sobre aquele assunto. A saída não é adivinhar: é olhar dado
(Etapa 1). Se a skill perceber esse padrão na conversa, **nomear em voz alta** e voltar pro dado.

> A pergunta que destrava: *"se esse conteúdo (ou esse pedido que te fazem sempre) fosse um produto,
> o que ele estaria prometendo?"*

---

## Fluxo

Sete etapas. **Três têm checkpoint** (problema, linha e roteiro) — são as decisões que, se erradas,
invalidam tudo que vem depois. O resto roda direto.

### Etapa 1 — Extração e escolha do problema

**1a. Inventário.** Perguntar, em bloco único (não uma pergunta por vez):

1. O que você já fez muitas vezes, pra você ou pros outros, e deu certo?
2. O que te perguntam sem parar — em DM, em conversa, no trabalho?
3. O que você resolve pra alguém em menos de uma semana?
4. Que material você já tem pronto e usa de verdade (planilha, checklist, roteiro, processo)?
5. Onde você já viu alguém travar num problema que pra você é banal?

A pergunta 4 é a mais subestimada: material que já existe e já é usado costuma ser o esqueleto do
produto inteiro, e encurta a produção pela metade.

**1b. Dado.** Levantar sinal real de demanda seguindo `references/demanda.md`. Nunca decidir por
intuição. Se a pessoa tem audiência, o dado dela vale mais que qualquer pesquisa externa.

**1c. Gate.** Cada candidato passa por cinco perguntas. Reprova em uma, reprova no gate:

| # | Pergunta | Reprova quando |
|---|---|---|
| 1 | A demanda está comprovada por gente já pagando ou já pedindo? | só existe na cabeça do autor |
| 2 | O assunto **não** está em tendência de queda? | está caindo (flat serve, não precisa subir) |
| 3 | O problema é específico e resolvível rápido? | é um tema grande, não um problema |
| 4 | Quem vai ensinar consegue resolver isso de fato? | nem por bagagem nem por estudo declarado |
| 5 | Quem vai ensinar aguenta se dedicar a isso por anos? | o interesse é passageiro |

Sobre a 4: **dá pra criar produto a partir dos próprios estudos**, desde que isso seja dito com
todas as letras. O que não se faz é posar de quem já viveu o que não viveu. Se o `CLAUDE.md` da
raiz tiver regra sobre isso, ela manda.

**CHECKPOINT:** apresentar **3 problemas candidatos**, cada um em uma linha, com o dado que sustenta
e o resultado do gate. O usuário escolhe 1 ou pede outros três.

Salvar em `problema.md`.

### Etapa 2 — O artefato e a linha de execução

O núcleo da skill. Detalhe em `references/linha.md`.

1. **Nomear o artefato.** Uma coisa, concreta, que existe no fim. Se não dá pra fotografar ou
   abrir num arquivo, ainda não é artefato.
2. **Escrever o objetivo específico.** Com número e prazo quando couber. "Atrair mais clientes" não
   é objetivo; "um funil de captação no ar em 14 dias" é.
3. **Decompor em passos sequenciais.** Cada passo produz **uma peça** do artefato. Passo que não
   produz peça é teoria disfarçada de etapa.
4. **Escrever as exclusões.** O que o produto deliberadamente **não** cobre, listado. É o que mantém
   a linha curta e o que faz a promessa ser crível.

> **Um caminho, não um cardápio.** Toda bifurcação que você deixa aberta vira variabilidade de
> resultado: metade dos alunos escolhe errado e não chega. Se existem três jeitos de fazer, escolha
> um e diga que escolheu.

**CHECKPOINT:** mostrar artefato + objetivo + os passos numerados + as exclusões. Esperar aprovação.

Salvar em `linha.md`.

### Etapa 3 — A frase-âncora e o nome

Uma frase que o comprador precisa acreditar. Se ele acredita, a compra é consequência.

> **[A virada] é o que destrava [o desejo], e só acontece por [o mecanismo].**

- **Desejo** — é **comum a todo o mercado**. Todo concorrente promete o mesmo, e tudo bem. Não
  gaste energia tentando ter um desejo próprio.
- **Virada** — o "o quê". A leitura nova sobre o problema. É o que toca a emoção e faz parar.
- **Mecanismo** — o "como". O passo a passo da Etapa 2, agora **nomeado**. É o que justifica a
  decisão pela razão, e é mensagem de esperança pra quem já tentou e não conseguiu.

Virada e mecanismo têm que ser seus. O desejo, não.

**O teste de honestidade, obrigatório antes de fechar a frase:** traduzir a virada pra linguagem
literal. Se a tradução literal continua sendo exatamente o que o produto entrega, a virada é
reenquadramento e pode ficar. Se a tradução literal entrega **menos** do que a virada promete, é
embalagem e cai. Detalhe e exemplos em `references/ancora.md`.

Depois: **nomear o mecanismo** e **nomear o produto** por uma das seis rotas (ação, identidade,
método, resultado, tempo, simplicidade). As seis estão em `references/ancora.md`.

Se `_contexto/posicionamento.md` existir, a virada tem que conversar com a Tese, não brigar com ela.

Salvar em `ancora.md`.

### Etapa 4 — Escopo e formato

**A régua é tempo até o artefato, não horas de aula.** O mesmo resultado em menos tempo vale mais,
sempre. Produto caro não precisa ser produto longo.

Escolher **o formato mais curto que entrega o artefato**:

| Formato | Quando | Ordem de grandeza |
|---|---|---|
| **Aula única / masterclass** | o artefato sai em uma sessão guiada | 60–120 min |
| **Workshop** | o artefato precisa de prática acompanhada | 2–4 encontros |
| **Curso curto** | são 4–6 peças que dependem uma da outra | 4–6 módulos, aulas de 5–15 min |
| **Ferramenta + aula** | o material já existe e a aula só ensina a usar | 1 entregável + 20 min |

Meta de desenho: **a primeira peça do artefato fica pronta na primeira sessão.** Se o aluno precisa
passar de duas aulas antes de produzir qualquer coisa, o começo está inchado.

Rodar a régua de corte em cada aula planejada, e listar o que foi cortado (o corte documentado
evita que ele volte na próxima revisão).

### Etapa 5 — O roteiro, aula a aula

Cada aula responde quatro perguntas antes de ser escrita:

1. O que o aluno ganha com isso?
2. O que ele **terá em mãos** no fim?
3. Qual exercício ele faz?
4. O que aqui está em excesso e pode sair?

**A proporção:** 10% o quê · 10% por quê · 80% como. O "o quê" e o "por quê" existem pro aluno não
improvisar e quebrar a linha, não pra ensinar teoria. O "como" é mostrado fazendo — tela
compartilhada, mão na ferramenta —, não explicado em slide.

**A estrutura de cada aula** (seis beats) e a **vitória rápida** estão em `references/roteiro.md`.
A vitória rápida é a peça mais importante do desenho de consumo: valor entregue cedo que **não
exige esforço do aluno** (planilha, calculadora, checklist, curadoria). Ela não é o artefato — o
artefato exige trabalho. Ela é o que compra a atenção que leva à primeira execução.

**CHECKPOINT:** mostrar o roteiro completo, aula a aula, com título, os quatro pontos e o exercício.
Esperar aprovação antes de qualquer produção.

Salvar em `roteiro.md`. Gerar também o **consolidado**: um checklist único com todos os exercícios
na ordem, feito pra ser impresso. Vai em `materiais/`.

### Etapa 6 — Preço, página e validação antes de produzir

> **Primeiro marketing, depois produto.** Não se grava aula sem ter validado que alguém compra.

- **Preço** pelo objetivo do produto (caixa agora, entrada de esteira, qualificação pra oferta maior,
  renda recorrente). Na dúvida, **abaixo do desejo**: é mais fácil subir preço de produto que vende
  demais do que descer preço de produto que não vende.
- **Página:** tratar o **checkout como página de vendas** no início, em vez de manter duas coisas.
  Os quatro elementos obrigatórios estão em `references/venda.md`.
- **Validação:** um post de narrativa ("eu estudei / eu testei / eu trabalhei com"), com oferta e
  desconto real de primeira turma, que faz o interessado **levantar a mão**. Conversa 1:1 com quem
  levantou, colhe feedback e depoimento, e fecha as primeiras vendas.

**A regra dura:** se ninguém levanta a mão, o produto não é feito. Isso não é fracasso, é o teste
funcionando antes de custar semanas de gravação.

Sobre urgência: prazo e desconto de primeira turma só entram se forem **reais** (a data existe, o
preço sobe de fato). Escassez inventada e reaperto empilhado ficam fora — e se
`_contexto/preferencias.md` proibir, ela manda.

Salvar em `oferta.md`.

### Etapa 7 — A esteira de consumo e a porta do próximo

**Fazer o aluno consumir é responsabilidade de quem vendeu, não do aluno.** O trabalho não acaba no
pagamento.

- **Pontos de contato do pós-venda** (boas-vindas com o primeiro passo, resgate de quem não começou,
  reconhecimento de conclusão de módulo, pedido de indicação depois da entrega ter acontecido) e o
  erro clássico de cobrar engajamento cedo demais: `references/esteira.md`.
- **A porta do próximo.** A última aula termina nomeando o **gargalo seguinte** — não como pitch,
  como diagnóstico: "você agora tem X funcionando; o que trava a partir daqui é Y". Quem terminou
  com o artefato na mão já está sentindo Y, e reconhecer isso vale mais que qualquer oferta.
- **Definir o próximo produto antes de lançar este.** Pelo menos o nome do problema seguinte. Sem
  isso o produto acaba em beco sem saída e a recompra vira improviso.

Salvar em `esteira.md`.

---

## Saída

```
produtos/<slug-do-produto>/
  extracao.md      ← Etapa 1a — o inventário do que a pessoa já tem
  problema.md      ← Etapa 1 — candidatos, dado, gate, escolhido
  linha.md         ← Etapa 2 — artefato, objetivo, passos, exclusões
  ancora.md        ← Etapa 3 — frase-âncora, mecanismo nomeado, nome do produto
  roteiro.md       ← Etapa 5 — aula a aula, com exercícios
  oferta.md        ← Etapa 6 — preço, checkout, plano de validação
  esteira.md       ← Etapa 7 — pós-venda e a porta do próximo produto
  materiais/       ← o consolidado impresso, a vitória rápida, os entregáveis
```

---

## Regras

- **O artefato manda.** Toda decisão de escopo se resolve perguntando se aquilo move uma peça do
  artefato. Se não move, sai.
- **Não decidir o problema por intuição.** Todo candidato da Etapa 1 pende de um dado observável.
  Sem dado, ele não entra na lista de três.
- **Não inventar demanda, número, resultado ou depoimento.** Prova é de quem tem. Resultado de
  terceiro ilustra método, nunca vira resultado próprio.
- **Um caminho, não um cardápio.** Bifurcação aberta é variabilidade de resultado.
- **A introdução serve à execução.** Base conceitual entra pra evitar improviso, não pra ensinar
  teoria. Se um trecho de "por quê" não protege nenhum passo, corta.
- **Mais rápido vence melhor.** "Melhor" é subjetivo e ninguém percebe; tempo economizado é sentido
  na hora.
- **Escassez só se for real.** Data que existe, preço que sobe de fato. Sem reaperto empilhado.
- **Vender antes de produzir.** Nenhuma gravação começa antes da Etapa 6 ter devolvido gente
  levantando a mão.
- **Nada de aula sem exercício.** Aula que não termina em ação executada é aula que não move peça.
- Linguagem de todo texto que vai pro aluno (títulos, e-mails, página, material) segue
  `_contexto/preferencias.md`. Sem jargão de guru, sem promessa de ganho garantido.
