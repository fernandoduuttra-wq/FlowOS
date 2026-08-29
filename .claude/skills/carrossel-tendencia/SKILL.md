---
name: carrossel-tendencia
description: >
  Cria carrosséis de tendência e cultura — o formato que parte de algo que já está acontecendo
  no mundo (notícia, movimento cultural, mudança de mercado, case) e traduz o que aquilo significa
  pro público de quem publica, afunilando a consciência do leitor slide a slide até o CTA.
  Faz a pesquisa das âncoras verificáveis, monta a triagem, gera 10 headlines, escreve a espinha
  dorsal, distribui em blocos e entrega os slides renderizados na identidade da marca + legenda.
  Use quando o usuário disser "carrossel de tendência", "carrossel de cultura", "post sobre
  [assunto em alta]", "transforma essa notícia em carrossel", "carrossel de autoridade",
  ou /carrossel-tendencia.
---

# /carrossel-tendencia — Carrossel de tendência e cultura

Formato de carrossel que **não ensina um conceito e não dá dicas soltas**. Ele pega um fenômeno
que o leitor já está percebendo no mundo e organiza o pensamento dele sobre aquilo — terminando
com o leitor consciente do que quem publica resolve.

O que faz esse formato render mais que conteúdo educativo: o assunto é **público**, então a capa
alcança gente muito além do nicho; e o miolo funciona como **funil de consciência**, então essa
gente ampla chega no último slide já sabendo por que deveria te contratar.

## Não confundir com

| Skill | O que faz |
|---|---|
| **esta** | constrói a **narrativa** de tendência do zero, com pesquisa, e entrega a peça |
| `/carrossel` | carrossel genérico da marca (educativo, lista, dica) — outro formato |
| `/post-twitter` | acabamento em print de tweet — pode receber o Template 4 desta skill |

Se o usuário pediu "um carrossel" sem mais contexto, é `/carrossel`. Esta aqui é quando existe um
**fenômeno externo** como ponto de partida, ou quando o objetivo é alcance + autoridade.

## Dependências

- **Tokens da marca:** `marca/design.json` — fonte da verdade visual. Ler sempre, antes de qualquer
  peça. Se não existir, rodar `/identidade`. Não improvisar cor, fonte ou escala.
- **Contexto:** `_contexto/empresa.md` (o que a marca resolve), `_contexto/preferencias.md` (tom),
  `_contexto/estrategia.md` (foco atual), `_contexto/posicionamento.md` (a tese) — quando existirem.
- **Pesquisa:** `WebSearch` + `WebFetch` (nativas). Ver `references/pesquisa.md`.
- **Render:** `scripts/render-carrossel.ps1` (Chrome/Edge headless).
- **Saída:** `marketing/conteudo/tendencia-<tema>-<AAAA-MM-DD>/` — ou o que o `CLAUDE.md` da raiz
  definir. **Se a raiz definir esteira própria de conteúdo, ela manda.**

## Arquivos de apoio

Ler sob demanda, na etapa em que entram:

| Arquivo | Quando |
|---|---|
| `references/pesquisa.md` | Etapa 1 — como levantar âncoras que sustentam a peça |
| `references/narrativa.md` | Etapas 2 e 4 — os 5 eixos, o funil de consciência, triagem e espinha |
| `references/headlines.md` | Etapa 3 — as 10 lógicas de captura |
| `references/templates.md` | Etapa 5 — mapeamento bloco → slide dos 4 templates |
| `references/visual.md` | Etapa 6 — a gramática visual do formato |
| `references/lacunas.md` | leitura de fundo — o que separa quem tem resultado de quem só executa |

---

## O princípio que rege tudo: afunilar do meio pro fim

Esta é a regra que mais muda o resultado, e a que mais gente erra.

> **A capa é a coisa mais ampla que a peça vai dizer. O miolo vai estreitando.
> Só depois da metade a comunicação começa a apontar pro que você resolve.**

O leitor entra pelo assunto público (que qualquer um entende e qualquer um compartilha) e sai
consciente de um problema específico que você resolve — **sem nunca ter sentido que entrou num
anúncio.** O funil não vem depois do conteúdo; o funil **é** o conteúdo.

**As cinco zonas** (num carrossel de 10 slides):

| Zona | Slides | O que acontece | Nível de consciência ao sair |
|---|---|---|---|
| **1. Quebra de padrão** | 1 | A capa. Trabalho **visual** antes de textual: parar o polegar. O fenômeno público nomeado, sem nicho e sem produto. | "isso está acontecendo mesmo" |
| **2. Armadilha de retenção** | 2–3 | A promessa de valor que prende. Cita a crença comum, derruba com âncora, e abre um loop que só fecha adiante. | "tem coisa aqui que eu não sei" |
| **3. Entrega técnica pesada** | 4–6 | O miolo. Nomeia, exclui os vizinhos, mostra a matéria-prima, explica por que funciona. **Sobre-entrega deliberada.** | "existe um mecanismo, e ele é sofisticado" |
| **4. Gatilhos de salvamento** | 7–8 | Slides construídos pra serem **salvos**: checklist, mecanismo numerado, exemplos concretos lado a lado, o erro da maioria com a causa reatribuída. Aqui o nicho entra e a 2ª pessoa também. | "vou precisar disso depois" |
| **5. Colheita** | 9–10 | A prova acumulada e o CTA. | "essa pessoa resolve isso" |

**Por que as zonas caem exatamente aí** — a plataforma mede retenção nos primeiros slides e pesa
compartilhamento privado muito acima de curtida. Daí a armadilha de retenção sentar em 2–3
(onde o tempo de permanência é medido) e os gatilhos de salvamento em 7–8 (onde a decisão de salvar
acontece, depois da entrega ter provado valor). A estrutura não é estética: ela persegue o sinal.

**Os dois erros simétricos:**

- **Afunilar cedo** — capa já nichada ("como advogado deve postar no Instagram"). Perde o alcance
  que justifica o formato. A capa vira um anúncio com cara de post.
- **Nunca afunilar** — capa ampla, miolo raso, fim genérico. Alcança e não colhe: vira conteúdo
  de entretenimento que enche seguidor errado.

**Teste rápido antes de fechar a peça:** ler só o slide 1 — dá pra saber o nicho de quem publicou?
Se dá, afunilou cedo. Ler só o slide 9 — dá pra saber o que essa pessoa resolve? Se não dá,
não afunilou nunca.

### O gate de pauta — seis perguntas antes de produzir

Se o tema não passar, ele não vira peça. Rodar antes de qualquer pesquisa:

1. O tema já interessa a pessoas **fora do nicho**?
2. Qual **tensão** torna esse assunto digno de um carrossel?
3. Que **leitura própria** justifica a entrada nessa conversa?
4. Como a **expertise da marca aparece sem forçar** a conexão?
5. O post entrega algo que **vale salvar ou compartilhar**?
6. Qual **próximo passo** transforma atenção em relação?

> Se o carrossel só resume um tema, ele ainda não constrói marca editorial.

A pergunta 3 é a que mais reprova pauta boa. Assunto quente que qualquer um comentaria não rende:
sem leitura própria, a peça vira notícia requentada e não gera autoridade nenhuma.

**Sobre a 2ª pessoa:** ela acompanha o funil. Zona 1 e 2 falam do fenômeno (3ª pessoa, distância
de observador — é o que dá autoridade). Zona 3 e 4 falam com o leitor ("você"). Trocar de pessoa no
meio não é inconsistência, é o funil mudando de marcha.

---

## Fluxo

Sete etapas. **Só duas têm checkpoint** (headline e texto final). O resto roda direto — o gargalo
de quem produz conteúdo é publicar, não deliberar. Não perguntar item a item.

### Etapa 1 — Pesquisa e âncoras

O formato vive de **âncoras observáveis**: fato público, verificável, datado. Sem âncora, a peça
vira opinião e o leitor não tem o que reconhecer.

1. Identificar o insumo. Três entradas possíveis:
   - **Conteúdo existente** (link, print, transcrição, artigo) → extrair as âncoras dele
   - **Insight/tese** do usuário → pesquisar as âncoras que sustentam
   - **Tema amplo** ("IA no mercado de X") → pesquisar do zero
2. Levantar **3 a 6 âncoras públicas verificáveis** seguindo `references/pesquisa.md`.
3. Se a pesquisa não devolver base suficiente, aí sim pedir material — em uma frase, sem rodeio.

Não transformar a pesquisa numa resposta separada. Ela abastece a Etapa 2 e some.

### Etapa 2 — Triagem

Uma tabela `| Campo | Extrato |` com quatro campos, e nada fora dela:

- **Transformação** — o que mudou, com costura e consequência. Não é resumo do tema.
- **Fricção central** — a tensão real do fenômeno. O que está em disputa.
- **Ângulo narrativo dominante** — a leitura mais forte disponível, escolhida entre as possíveis.
- **Evidências** — prosa + A), B), C) (D/E se precisar), cada uma amarrada numa âncora da Etapa 1.

Detalhe de cada campo em `references/narrativa.md`.

### Etapa 3 — Headlines

Abrir com exatamente duas linhas em prosa: o ângulo dominante selecionado e a tensão que ele
privilegia. Depois **10 opções numeradas**, cada uma com duas linhas:

- **linha 1 = captura** — termina em `?` ou `:`
- **linha 2 = ancoragem** — termina em `.` ou `!`

As 10 precisam variar de **natureza**, não de palavra. As dez lógicas e o checklist de qualidade
estão em `references/headlines.md`.

**CHECKPOINT:** o usuário escolhe 1–10, ou pede "refazer headlines". Não avançar sem escolha.

### Etapa 4 — Espinha dorsal

Tabela `| Campo | Extrato |` com seis campos:

**Headline escolhida** (as duas linhas, separadas por `<br>`) · **Hook** (contextualiza a tensão) ·
**Mecanismo** (por que o fenômeno acontece) · **Prova** (A/B/C, base observável) ·
**Aplicação** (o que isso muda pra quem lê — aqui começa a Zona 3) ·
**Direção** (pra onde a peça caminha, e qual objetivo o CTA vai servir).

Diferença importante em relação a como esse formato costuma ser executado: **a Direção aponta o
CTA**, não foge dele. Ver `references/lacunas.md`.

### Etapa 5 — Blocos

Escolher o template e distribuir o conteúdo em blocos numerados (`texto 1 -`, `texto 2 -`, ...).

| Template | Blocos | Slides | Quando |
|---|---|---|---|
| **1. Principal** | 18 | 10 | padrão. Argumento com prova intercalada |
| **2. Compacto** | 14 | 10 | assunto que se resolve rápido; leitura mais veloz |
| **3. Autoral** | 18 | 10 | narrativa contínua em 1ª pessoa, case próprio |
| **4. Fragmentado** | 21 | 10–11 | fala picada em cartões curtos; casa com `/post-twitter` |

Bloco é **campo de texto de um slide**, não é slide: um slide consome de 1 a 3 blocos. O mapeamento
bloco → slide de cada template está em `references/templates.md`.

Salvar a saída numerada em `blocos.md`. Ela força a contagem certa de conteúdo por slide e mantém
aberta a rota de injetar o texto numa esteira de montagem externa, se um dia for útil.

**CHECKPOINT:** mostrar o texto completo, slide a slide. Esperar aprovação antes do visual.

### Etapa 6 — Visual

Ler `marca/design.json` e `references/visual.md`. Montar um HTML por slide
(`slide-01.html` ...), 1080x1350, CSS inline, e renderizar:

```powershell
& ".\scripts\render-carrossel.ps1" -Folder "marketing\conteudo\<pasta>"
```

**Antes de dizer que ficou bom: abrir os PNGs e olhar.** Conferir contra a lista `nunca` do
`design.json`. Mostrar capa, um slide de miolo e o CTA.

### Etapa 7 — Legenda, CTA e áudio

- **Legenda** em `legenda.md`: retoma o fenômeno em 2–3 frases (quem não abriu o carrossel entende),
  crava a tese, e **repete a palavra-chave do CTA**. Se o CTA é comment-gate, a palavra aparece
  na peça **e** na legenda — sem isso o gate perde metade do disparo.
- **CTA:** escolher conforme o objetivo. Comment-gate (palavra + entrega automática na DM),
  link na bio, salvar/compartilhar, ou DM direta. Se o workspace tiver esteira própria de entrega
  (automação de DM, central de material), o `CLAUDE.md` da raiz diz qual é — usar ela.
  - **Nem toda peça colhe.** Peça sem gate fecha em tese, e ela existe pra manter o perfil sendo
    lido como veículo e não como funil. A proporção é decisão de quem publica e vive no `CLAUDE.md`
    da raiz; na falta de definição, **duas peças com gate a cada três** é um ponto de partida
    saudável. Antes de definir o CTA, olhar as duas últimas peças publicadas: se as duas tiveram
    gate, esta fecha em tese.
  - **O slide de CTA é ativo fixo** (ver `visual.md`). Montar uma vez, guardar em
    `marketing/conteudo/_ativos/cta/`, e por peça reescrever só o parágrafo-ponte e a palavra-chave.
- **Áudio:** sugerir pela **letra**, nunca por clima instrumental. Regra completa em `/carrossel`.

### Saída

```
marketing/conteudo/tendencia-<tema>-<AAAA-MM-DD>/
  ancoras.md            ← as 3–6 âncoras com fonte (fica, mesmo sem aparecer na peça)
  triagem.md            ← Etapa 2
  espinha.md            ← Etapa 4
  blocos.md             ← Etapa 5, formato "texto N -"
  slide-01.html → slide-NN.html
  instagram/
    slide-01.png → slide-NN.png
  legenda.md            ← legenda + palavra-chave do CTA + sugestões de áudio
```

---

## Regras

- **Não inventar fato, número, data, local ou fonte.** Toda afirmação forte pende de uma âncora
  levantada na Etapa 1. Se a âncora não existe, a frase não entra.
- **Não fazer acusação direta a pessoa ou empresa.** Nomear o fenômeno, não o culpado.
- **Prova intercalada:** afirmação forte vem seguida de evidência observável — print, número
  datado, nome próprio, captura de tela. Adjetivo não sustenta; imagem sustenta.
  Ver `references/visual.md`.
- **Sem metalinguagem.** A peça nunca comenta a própria estrutura ("neste slide vamos ver").
- **A capa é a coisa mais ampla da peça.** Se ela já entrega o nicho, refazer.
- **Ritmo de fundo:** nunca dois slides seguidos com o mesmo fundo. O slide do mecanismo
  (o miolo do argumento) vai em cor de acento chapada.
- **Tokens sempre do `design.json`** — inclusive quando a referência do formato usa outra paleta.
  O que o JSON define (cor, fonte, símbolo, lista `nunca`) é da marca; o resto da referência
  (composição, técnica, ritmo) é absorvível.
- **Conferir a lista `nunca` antes de renderizar.** Ela vence qualquer convenção do formato.
- Linguagem segue `_contexto/preferencias.md`. Sem jargão de marketing, sem corporativês.
- Formato 1080x1350 (4:5). Sempre.
