# Visual — a gramática do formato

Esta camada **não existe** nas esteiras que só geram texto em blocos: nelas a arte vem de um
arquivo pronto e o texto é injetado. Aqui a peça é construída inteira, então a composição é
responsabilidade da skill.

> **Regra que vence todas as outras desta página:** cor, fonte, escala, forma, espaçamento e a
> lista `nunca` saem de `marca/design.json`. O que está aqui é **composição** — onde o texto senta,
> que massa ele ocupa, que ritmo os slides seguem. O JSON trava reconhecimento; a composição varia.
> Se algo aqui contradisser o JSON, **o JSON manda**.

---

## A moldura fixa

Antes dos slides, o que **não muda entre eles**. Uma barra fina no topo, presente em 100% das
peças, com três marcas: uma assinatura à esquerda, o **@ da conta ao centro** e a **data à direita**
(mês/ano ou só o ano). Corpo pequeno, peso normal, sem caixa alta.

Ela faz três trabalhos ao mesmo tempo, e é por isso que compensa o espaço que ocupa:

- **Assina cada slide isolado.** Peça de carrossel viaja por print e por compartilhamento em story.
  Sem a barra, o slide 6 circula sem dono.
- **Data o conteúdo.** Numa peça sobre fenômeno em curso, a data é credibilidade: mostra que a
  leitura é de agora, não requentada.
- **Substitui o contador de slide.** A posição no carrossel a própria plataforma já mostra.

**A cor da barra acompanha o fundo do slide** — clara sobre foto escura e fundo escuro, escura ou
de acento sobre fundo claro. Ela nunca ganha caixa própria nem fio embaixo.

Se a marca proibir marca d'água ou assinatura em peça, esse elemento cai inteiro — e aí a
assinatura volta pro rodapé da capa, só.

---

## A capa — metade do resultado

De todos os slides, a capa é o que decide se a peça acontece. Duas camadas, nesta ordem de
importância: **a foto** e **a massa do título**.

### A foto

O critério não é "foto bonita". É **reconhecimento ou espanto**:

- **Reconhecimento** — o leitor identifica o assunto antes de ler qualquer palavra. Uma cena que
  ele já viu, um objeto que ele associa ao tema, uma situação que ele viveu.
- **Espanto** — a imagem não bate com o esperado e o cérebro para pra resolver a contradição.

Uma foto que não faz nem uma coisa nem outra é decoração, e decoração não segura rolagem.

**Três testes antes de aceitar a foto:**

1. **Massa vazia.** Precisa ter área contínua e limpa (escura ou clara, conforme a marca) onde o
   título caiba **sem cobrir o assunto** — na prática ~40% da peça, num canto só, de preferência a
   metade de baixo. Sem isso, a foto vira slide interno, nunca capa.
2. **Legibilidade a 1 cm.** No feed a peça aparece pequena. Se o assunto da foto some ao reduzir,
   a foto está detalhada demais.
3. **Cor parasita.** Nenhuma cor forte dentro da foto pode brigar com o acento da marca. Se
   brigar, dessaturar aquela região antes de usar — ou trocar a foto. Duas cores de acento na
   mesma peça é o que mais rápido descaracteriza a identidade.

**Ordem de origem da foto:** acervo próprio da marca (`imagem.fotos` no `design.json`) → foto que
o usuário mandar → banco de imagem com os `imagem.termos_banco` → IA, por último. Acervo próprio é
o que diferencia a peça de qualquer template; IA é o que mais rápido a iguala.

**Tratamento:** escurecer o suficiente pro texto respirar, seguindo `imagem.overlay` do JSON.
A foto trabalha como **fundo**, não como ilustração — ela ocupa a peça inteira e sangra nas bordas.
Nunca foto dentro de moldura na capa.

### A massa do título

O que faz a capa deste formato ler como manchete e não como post: **o título ocupa a metade
inferior inteira**, em caixa alta, com entrelinha apertada, sem margem sobrando. Não é um título
grande — é um **bloco de texto** que preenche a área.

- **Escala:** `tipografia.escala_px.titulo_capa` do JSON, subindo até encher a área. Três a cinco
  linhas de texto é o alvo. Uma linha só desperdiça a massa.
- **Entrelinha apertada** (0.95 a 1.05). É o que transforma linhas soltas em bloco.
- **Um a três termos no acento.** São as palavras que carregam a tensão — normalmente o que morre
  e o que nasce, ou o nome próprio que o leitor reconhece. Marcar a frase inteira mata o efeito;
  marcar uma palavra qualquer não cria hierarquia. **Se o `design.json` disser "um acento por peça",
  essa regra vence e só um termo é marcado.**
- **A linha curta de contexto**, pequena, em sans, caixa baixa. Vai **acima** do título quando é
  provocação ou setup (*"Os jovens estão mais idiotas"*, *"A maior rede social do mundo está de
  volta?"*), e **abaixo** quando é a promessa de método (*"e como aplicar isso na prática"*,
  *"o guia para criar X que gera Y"*). Alternar entre as duas posições é o que evita que as capas
  fiquem com a mesma silhueta.
- **Assinatura de autoria** entre a linha de contexto e o título — pílula pequena com o símbolo da
  marca e o handle. Ela existe porque a peça circula por print e compartilhamento; sem ela o
  conteúdo viaja sem dono.

### A camada de anotação

O elemento que mais separa essas capas de "foto com título em cima", e o que menos aparece em
qualquer descrição do formato: **uma camada que anota a foto**, como se alguém tivesse marcado a
tela pra explicar algo.

O vocabulário completo:

| Elemento | O que faz |
|---|---|
| **Recorte circular** | um segundo personagem (o fundador, o rival, o antes) num círculo sobreposto à foto principal |
| **Seta desenhada à mão** | branca, curva, apontando da margem pro ponto de interesse |
| **Micro-legenda** | 2 a 4 linhas em corpo pequeno, com o dado em negrito (*"Ela ganhou **100k seguidores** nos últimos 30 dias"*) |
| **Print do perfil** | captura da tela do sujeito, em mockup de celular, atrás ou ao lado dele |
| **Pessoa recortada** | o sujeito com o fundo removido, sobreposto ao próprio print |
| **Logo de terceiro** | quando a peça é sobre uma marca/ferramenta nomeada, o logo dela entra num canto |

**Não usar todos.** Uma capa leva um ou dois. A combinação mais forte pra peça sobre uma pessoa é
**print do perfil + pessoa recortada + seta + micro-legenda com o número** — ela já entrega a prova
antes do leitor arrastar, e faz a peça ler como análise em vez de anúncio.

A capa de "elenco" é o outro extremo: três a cinco pessoas recortadas, alinhadas lado a lado sobre
fundo neutro. Serve pra peça sobre um grupo, uma geração ou uma categoria.

### Duas famílias de título

O formato roda em duas construções, e o feed alterna entre elas em **blocos** — várias peças numa,
depois várias na outra. Isso não é indecisão: é o que impede o perfil de virar catálogo sem forçar
variação dentro de cada peça.

| Família | Como é | Tende a pegar |
|---|---|---|
| **Condensada em caixa alta** | manchete, entrelinha travada, massa cheia na metade inferior | fenômeno, notícia, estudo, número, mudança de mercado |
| **Serifa display** | caixa baixa, quebra em 3–4 linhas, ar entre elas | pessoa nomeada, trajetória, leitura interpretativa ("por que", "o que explica") |

A correlação é forte mas **não é lei** — há capa de pessoa em condensada e de fenômeno em serifa.
Tratar como tendência, não como regra: quando as duas servirem, decide a alternância com as
últimas peças publicadas.

**Dentro da família serifa há três marcações com funções diferentes**, e é o uso combinado delas
que dá o acabamento editorial:

- **Itálico** marca o termo-conceito ou o papel (*delegado*, *psicologia*, *conteúdo*)
- **Cor de acento** marca a tensão da frase
- **Peso/romano** marca o nome próprio

Três marcações no mesmo título é o teto. Mais que isso e o olho não sabe onde pousar.

### O que se absorve e o que não

**Absorve-se a estrutura: caixa alta, a massa ocupando a metade inferior, a entrelinha apertada,
os dois termos no acento. As fontes são as da marca, sempre.**

O formato de referência varia entre três construções de título — sans condensada pesada, serifa
grande sozinha, e as duas misturadas dentro do mesmo título. **Essas três variações já existem
como técnica na maioria das marcas maduras** e costumam estar registradas no arquivo de composição
(`marca/composicao.md` ou equivalente, apontado pelo `CLAUDE.md` da raiz). Quando existirem, é de
lá que a construção sai — e a regra de rotação daquele arquivo continua valendo: **não repetir a
mesma construção em peças seguidas.**

O que esta skill acrescenta a elas é a **caixa alta e a massa**, que é o que faz a capa ler como
manchete. Cuidados ao subir uma família para caixa alta:

- **Serifa display em caixa alta pede tracking levemente aberto** (0.01em a 0.02em). Em caixa
  baixa ela fecha sozinha; em caixa alta, sem esse respiro, as hastes colam.
- **Família com um peso só** (muitas serifas display têm apenas o regular) **não vira bold.**
  O peso vem do tamanho e da massa, não da espessura — subir escala e apertar entrelinha, nunca
  simular bold com `font-weight` falso, que engorda a letra e denuncia.
- **No título misto, quem vira acento é palavra inteira**, nunca sílaba. E os dois termos de acento
  da capa são os mesmos que carregam a tensão da frase — não se escolhe por ritmo visual.

**Trocar a família de título é decisão de marca, não de peça.** Se o resultado renderizado não
carregar peso suficiente, o caminho é escala e entrelinha. Se ainda assim não resolver, é conversa
com o usuário e atualização do `design.json` junto — nunca por conta própria dentro de uma peça.

---

## Ritmo dos slides internos

**Nunca dois slides seguidos com o mesmo fundo.** A alternância é o que dá sensação de progressão
e o que mantém o dedo arrastando.

| Fundo | Papel | Onde |
|---|---|---|
| **Escuro** (`cores.fundo`) | peso, autoridade, prova | slide 2 e slide 9 (as duas âncoras da peça) |
| **Claro** (`cores.claro`) | leitura, respiro, explicação | o miolo argumentativo |
| **Acento chapado** (`cores.destaque`) | "aqui está o miolo" | **só uma vez na peça**, no slide do mecanismo |

O slide de acento chapado é um evento. Usado duas vezes, deixa de significar. O leitor não sabe
explicar por que aquele slide parece o mais importante — ele só sente, e é exatamente esse o
trabalho do fundo.

**A alternância é estrita, não aproximada.** A sequência observada em peça de 10 slides é
`foto → claro → escuro → claro → escuro → ACENTO → escuro → claro → escuro → claro`. Dois slides
seguidos no mesmo fundo é o defeito que faz o carrossel parecer longo mesmo tendo o mesmo tamanho.

### A célula de slide interno

Todo slide de miolo é feito de **duas peças e nada mais**: um bloco de **texto grande** e um bloco
de **imagem**. O que varia é a ordem e a proporção — e é só isso que varia.

| Arranjo | Como fica | Serve pra |
|---|---|---|
| **Imagem em cima** | foto sangrada ocupando 60–70%, título dentro dela na base, texto de apoio embaixo no fundo chapado | slide de fato, evento, cena |
| **Texto em cima** | título grande no fundo chapado ocupando o topo, foto sangrada embaixo com a frase-remate dentro | slide de tese, conclusão, virada |
| **Sanduíche** | título / imagem em card com radius / texto de apoio | slide de dado ou de prova, quando a imagem é captura e não cena |
| **Texto puro** | só tipografia e respiro, sem imagem | a frase que precisa ser lida devagar. No máximo dois por peça |

**Alternar o arranjo a cada slide.** Imagem-em-cima seguido de texto-em-cima, e assim por diante.
Essa alternância faz os slides variarem sem parecer aleatórios: a estrutura é sempre
a mesma célula binária, e o ritmo vem de inverter a ordem, não de inventar layout novo.

**O slide de texto puro pede serifa.** Quando não há imagem competindo, a serifa em corpo grande com
respiro largo transforma a frase em citação — o leitor desacelera. É o oposto do que a condensada
faz. Título condensado sobre foto acelera; serifa em texto puro freia. Usar os dois de propósito.

---

## Os elementos de apoio

### Card de prova — o que sustenta a peça

**Toda afirmação forte vem seguida de evidência visível.** É o que mais separa este formato de
conteúdo educativo: o print faz o trabalho que adjetivo nenhum faz — transfere o ônus da dúvida.
O leitor não precisa acreditar em quem escreveu, ele vê a tela.

Três tipos:

| Tipo | O que é | Quando |
|---|---|---|
| **Captura** | print de tela real: perfil, painel, mensagem, resultado, publicação | prova de primeira mão. A mais forte |
| **Número** | o dado isolado em corpo grande, com a fonte pequena embaixo | prova externa, ou métrica sem print disponível |
| **Ilustração** | foto que encena o fato citado | quando não há captura possível (evento, notícia) |

**Como o card senta na peça:**

- Sobre `cores.superficie`, com `forma.radius_medio` e a sombra quente do JSON — nunca sombra preta.
- Levemente rotacionado (−2° a 3°) quando forem dois ou três empilhados. Rotação idêntica em todos
  entrega template; variar o ângulo de cada um.
- **Nunca esticar a captura.** Recortar, sim; deformar, não — a distorção denuncia montagem e
  destrói justamente a credibilidade que o card foi buscar.
- **O contraexemplo vai borrado.** Quando o card mostra o que *não* se deve fazer, desfocar o
  suficiente pra não identificar o autor. Isso não é só estética: é a regra de não acusar ninguém
  diretamente, resolvida no visual.
- Dado sensível (nome de cliente, valor de contrato, e-mail, telefone) sai da captura antes de
  entrar na peça. Tarjar de verdade, não cobrir com retângulo semitransparente.

### Lista de exclusão ✗ ✗ ✓

O padrão de nomeação da Zona 2. Duas negações e uma afirmação, cada uma em sua linha, com o marcador
alinhado. As negações em `cores.texto_secundario`, a afirmação em texto pleno — o contraste de peso
faz o olho pousar na linha certa sem precisar de seta nem grifo.

### Grifo inline — três marcações, três funções

Não existe "grifo" genérico. Cada marcação carrega um sentido, e misturar as três na mesma frase
anula todas:

| Marcação | Marca | Onde |
|---|---|---|
| **Peso bold** | o dado ou o termo técnico dentro da frase | corpo de apoio |
| **Sublinhado** | a frase que é a conclusão do slide | fecho de bloco, mini-título de lista |
| **Cor de acento** | a tensão — o que muda, o que morre, o que está em jogo | título, ou a primeira frase de um bloco |

**O sublinhado é o mais subutilizado e o mais seguro.** Ele grifa sem gastar o acento da marca, o
que resolve o problema de peças que já usaram a cor no título. Aplicar na frase inteira, não em
palavra solta, e sempre com um respiro entre a linha e o texto.

Se o `design.json` limitar a um acento por peça, ele foi gasto na capa: no miolo sobra bold e
sublinhado, e está tudo bem — a peça não fica pobre por isso.

### Prova empilhada (slide 9)

Três a quatro números em corpo grande, um por linha, em fundo escuro, com o rótulo pequeno ao lado.
O número é o elemento gráfico; não precisa de ícone, moldura nem ilustração. Fecha com a frase de
reatribuição de mérito em corpo normal.

### O slide de CTA é um ativo fixo, não uma peça nova

O achado mais valioso operacionalmente: **o último slide se repete entre carrosséis.** Mesma foto,
mesmo mockup, mesma pílula, mesmo layout. Só duas coisas mudam de peça pra peça:

1. **O parágrafo-ponte** no topo — a frase que generaliza o caso daquela peça na tese que se vende.
   Esse sim é escrito toda vez.
2. **Uma palavra na pílula** ("acesso a essa aula" / "a essa ferramenta").

Por que isso importa: o trabalho criativo por peça fica concentrado onde ele rende — capa e miolo.
O fecho vira montagem. Uma operação que redesenha o CTA toda semana está gastando esforço no slide
que menos precisa de novidade.

**Montar o ativo uma vez, guardar, reusar.** A composição que funciona:

- **Parágrafo-ponte** em corpo grande, com a virada de tese em cor ou bold.
- **A prova visual da própria operação**: mockup de celular mostrando o post anterior com as
  métricas visíveis, ao lado de uma foto de bastidor (a pessoa trabalhando, o quadro branco).
  Prova social e humanidade na mesma imagem, e ela não envelhece rápido.
- **Pílula de CTA** com borda fina (outline, não preenchida), largura quase total, texto centralizado,
  e a **palavra-chave em destaque dentro dela**.

Se o CTA for comment-gate, a palavra precisa ser lida e digitada de primeira por alguém no celular:
curta, sem acento, sem ambiguidade de grafia. A assinatura de como a entrega chega vai em corpo
pequeno no rodapé.

**Atenção à ponte.** É o único ponto onde a peça pode quebrar: se o parágrafo não amarra o assunto
à oferta, o slide 10 vira um anúncio colado no fim de um bom conteúdo, e o leitor sente. A ponte
boa generaliza — pega o caso específico e o transforma na tese que o produto resolve.

---

## Conflitos conhecidos com a lista `nunca`

Convenções deste formato que **não** se copiam se a marca proibir. A lista `nunca` do `design.json`
sempre vence:

| Convenção do formato | Se a marca proíbe |
|---|---|
| Barra ou contador de progresso (1/10) no rodapé | não usar. O carrossel já mostra a posição |
| Kicker rotulando o slide ("O MÉTODO", "A PROVA") | não usar. Rótulo só entra se carregar informação que a peça não tem sem ele |
| Fio ou barrinha embaixo do título | não usar. O respiro separa |
| Selo de verificado desenhado na pílula de autoria | não replicar selo de plataforma que a conta não tem |
| Cor forte dentro da foto | se o JSON disser que o acento não entra na foto, dessaturar |

---

## Ritmo vertical: o defeito que mais aparece no primeiro render

**O conteúdo tem que preencher a peça.** Slide com um bolsão de 200 a 500px vazio não lê como
respiro, lê como erro, e é o defeito que mais sobrevive à primeira renderização.

Ele tem duas causas, e as duas se corrigem juntas:

**1. Espaçador flexível único.** Um elemento que cresce (`flex:1`, ou margem automática) despeja
toda a sobra num ponto só. Com pouco conteúdo, isso vira um buraco. A correção é **subir o corpo do
texto** (causa 2, abaixo) e deixar a sobra virar margem **em volta** do grupo.

> **A correção que NÃO se faz: espalhar os itens.** `justify-content: space-between / space-around /
> space-evenly` numa lista joga a sobra **entre irmãos** e destrói o agrupamento: os itens deixam de
> ler como um bloco e passam a parecer três blocos soltos. É o defeito que mais aparece nas peças e
> ele é pior que o buraco que estava tentando resolver. Ver a seção **Proximidade** logo abaixo.

**2. Tipografia pequena demais pro quadro.** É a causa de fundo, e a mais fácil de subestimar.
Peças desse formato usam texto grande a ponto de parecer exagerado numa tela de computador, e é
justamente isso que faz elas lerem no feed. **Se sobrou espaço, o primeiro instinto certo é aumentar
o corpo do texto**, não empurrar os blocos pros cantos. Lista de 3 a 5 itens costuma pedir corpo
bem maior que o parágrafo do mesmo slide.

Regra prática: se depois de renderizar existe uma faixa vazia maior que a altura de duas linhas de
texto, o slide precisa de ajuste. **A faixa vazia em volta de um grupo é respiro; dentro do grupo é
defeito.**

## Proximidade: onde o espaço branco pode e onde não pode

O espaço não é neutro. Ele é o que diz ao olho o que é uma coisa só e o que são coisas diferentes.
Dois elementos perto lêem como um bloco; os mesmos dois afastados lêem como dois assuntos.

**A hierarquia de espaçamento, e ela é uma escada com proporção:**

| Nível | O que separa | Referência numa peça 1080x1350 |
|---|---|---|
| Entrelinha | linhas da mesma frase | 1.2 a 1.4 do corpo |
| **Gap interno** | itens irmãos de uma lista, linhas de uma estrofe | 18 a 44px |
| **Gap de bloco** | título → lista → fecho | 2 a 3x o gap interno |
| Margem da peça | conteúdo → borda | `espacamento.margem_peca` do JSON |

**O gap entre irmãos precisa ser visivelmente menor que o gap entre blocos.** Se os dois ficam
parecidos, o slide perde a hierarquia e o leitor não sabe onde um assunto termina.

**Como preencher um slide que sobrou espaço, nesta ordem:**

1. **Subir o corpo do texto.** É quase sempre a resposta certa, e a que mais melhora a leitura no
   feed.
2. **Centralizar o grupo** (`justify-content: center` com `gap` fixo), deixando a sobra virar
   margem em cima e embaixo do bloco inteiro.
3. **Só então** rever se falta conteúdo naquele slide.

**Nunca:** aumentar o gap entre itens de uma lista pra "encher" a peça.

### Simetria antes de preenchimento

Título grudado no topo e fecho grudado na base, com um vão no meio, é o mesmo defeito por outro
caminho: os dois somem na beirada e a peça fica torta. **O miolo é um bloco só, centrado na peça
inteira.**

- **A moldura de topo sai do fluxo** (`position:absolute`). Ela é mobiliário fixo. Se entrar no
  fluxo, o miolo centraliza só na área abaixo dela e a peça fica pesada embaixo — erro que passa
  despercebido porque o CSS *parece* centrado.
- **A régua do quadrado:** o formato é 1080x1350, mas quando sobra muito espaço o conteúdo pode ser
  composto dentro dos **1080x1080 centrais**. Mais simétrico que esticar pra ocupar os 1350.
- **Pílula de CTA em uma linha.** Duas linhas engordam o fecho. Encurtar o texto, nunca o balão.

**Cartões lado a lado seguem a mesma lógica:** eles se alinham pelo topo e têm a mesma altura
(`align-items: stretch`), mesmo que um tenha menos itens. Cartão de altura diferente, flutuando no
meio, quebra o alinhamento e desequilibra a dupla. Se os títulos dos cartões tiverem número de
linhas diferente, travar a altura do título pros dois começarem a lista na mesma linha.

## Foto de capa escura: clarear a foto, não tirar o véu

Foto noturna sob véu de gradiente escurece duas vezes e some. A correção é **subir o brilho da
imagem** e manter o véu forte onde o texto senta. Tirar o véu resolve a foto e quebra a legibilidade.

E o véu precisa de **muitos pontos de parada**. Com dois ou três, a transição vira uma borda
horizontal visível atrás do título, que lê como um retângulo colado na peça.

Crédito de fonte, quando houver, vai no **rodapé da capa**, não flutuando no meio da imagem: no meio
ele cai sobre a área clara da foto e fica ilegível, além de disputar com o título.

## Execução

1. Ler `marca/design.json` inteiro antes de escrever a primeira linha de CSS.
2. Um arquivo HTML por slide (`slide-01.html` ... `slide-NN.html`), 1080x1350, CSS inline,
   Google Fonts como única dependência externa.
3. Renderizar:

```powershell
& ".\scripts\render-carrossel.ps1" -Folder "marketing\conteudo\<pasta>"
```

4. **Abrir os PNGs e olhar.** Conferir a capa em tamanho pequeno (o teste do feed), conferir cada
   card de prova contra a versão original, conferir a peça inteira contra a lista `nunca`.
   Não afirmar que ficou bom sem ter olhado.
5. Mostrar ao usuário: capa, um slide de miolo, o slide de acento e o CTA.
