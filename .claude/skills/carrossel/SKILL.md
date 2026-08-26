---
name: carrossel
description: >
  Cria carrosséis e posts visuais pra Instagram, TikTok, LinkedIn com a identidade visual da marca.
  Gera HTML estilizado + renderiza em PNG 1080x1350 via Playwright, com legenda pronta no final.
  Suporta carrossel texto puro, carrossel com foto IA (gerada via OpenAI) e post único.
  Use quando o usuário pedir "carrossel", "post", "conteúdo pro instagram", "criar imagem",
  "gerar foto", "post educativo", ou /carrossel.
---

# /carrossel — Carrossel e posts visuais

Skill central de criação de conteúdo visual. Pega um tema → entrega HTMLs estilizados + PNGs prontos pra postar + legenda no padrão da marca.

## Dependências

- **Tokens da marca:** `marca/design.json` — **A FONTE DA VERDADE VISUAL.** Ler SEMPRE, primeiro.
  Cor, fonte, escala, forma, espaçamento e a lista `nunca` saem DAQUI. **Não improvisar CSS.**
  Se o arquivo não existir, rodar `/identidade` antes — não inventar tokens.
- **Racional da marca (opcional, ler só se existir):** a prosa que explica o porquê dos tokens.
  Costuma viver em `marca/` como `design-guide.md`, `composicao.md` ou `distincao.md`, e o nome varia
  por workspace — ver o `CLAUDE.md` da raiz. **Se qualquer prosa divergir do `design.json`, o JSON
  manda.** Não bloquear a peça se não houver nenhuma: o JSON basta pra desenhar.
- **Contexto do negócio:** `_contexto/empresa.md`
- **Tom de voz:** `_contexto/preferencias.md`
- **Render PNG:** `scripts/render-carrossel.ps1` (Chrome/Edge headless, sem Node/Playwright). É o método padrão nesta máquina.
- **OpenAI API (opcional):** pra gerar fotos realistas — só se o cliente tiver chave configurada
- **Outputs vão em:** `marketing/conteudo/<tipo>-<tema>-<YYYY-MM-DD>/`

---

## Duas rotas de acabamento

O ângulo, o texto e a estrutura dos slides são sempre feitos aqui. O que muda é **onde o visual é
finalizado**:

- **Rota HTML** (default, automatizável) — gera os `slide-NN.html` lendo o `design.json` e renderiza
  em PNG. Boa pra volume, pra cliente, e pra rodar sem supervisão.
- **Rota Claude Design** (quando o acabamento importa) — entrega o roteiro pro Claude Design, que já
  tem o design system da marca carregado. **O usuário ajusta na mão, direto no canvas: seleciona,
  redimensiona, aplica efeito — sem re-promptar cada ajuste.** É onde o julgamento visual volta pra
  mão dele, que é onde ele deve estar.

Se não estiver claro, perguntar. Peça da marca própria tende à rota Claude Design; volume de cliente
tende à rota HTML. Ver o Passo 4 pra cada uma.

---

## Tipos de conteúdo

Ao receber um pedido, identificar qual tipo se encaixa:

### 1. CARROSSEL TEXTO PURO
- **Quando usar:** posts educacionais, dicas, listas, explicações
- **Formato:** 1080x1350 (4:5) — sempre
- **Estilo:** tipografia clean, cores da marca alternadas, sem fotos

### 2. CARROSSEL COM FOTO
- **Quando usar:** apresentação visual, conteúdo aspiracional, capa com personagem
- **Formato:** 1080x1350 (4:5)
- **Estilo:** foto como capa com gradient overlay + slides internos no padrão alternado
- **Foto:** primeiro o acervo próprio da marca (ver Passo 3), depois foto passada pelo usuário, e só
  em último caso IA

### 3. POST ÚNICO
- **Quando usar:** frase de impacto, dado/estatística, depoimento, bastidores
- **Formato:** 1080x1350
- **Estilo:** varia conforme o conteúdo (citação, número grande, foto com overlay)

Se o tipo não estiver claro, perguntar:
> "Que tipo de conteúdo? (1) carrossel texto, (2) carrossel com foto, (3) post único"

---

## Estilo visual base

**Cor, fonte, escala, radius, espaçamento e a lista `nunca` vêm do `marca/design.json`. Ponto.**
Não há "cor padrão" nem "fonte padrão" nesta skill — isso é o que fazia o carrossel sair inconsistente:
cada peça reinventava o CSS. Ler o JSON e usar os valores dele literalmente.

Se o `design.json` não existir: **parar e rodar `/identidade`.** Não improvisar uma paleta.

O que fica aqui é só o que o JSON **não** cobre — a gramática de layout (elementos, layouts nomeados,
ritmo). Isso é vocabulário de composição, não de marca.

**Se o usuário colar uma referência visual** (link, print de post, capa de revista), extrair dela
**duas camadas**: a estrutura (onde o texto senta, hierarquia, respiro, crop) e a **técnica** (grão,
textura, duotone, blend mode, recorte, sobreposição de texto e imagem, máscara, texto em curva,
contraste extremo de escala, halftone). Reconstruir nos tokens da marca.

> **A régua do que se descarta é uma só: o que o `design.json` define é da marca — paleta, fontes,
> símbolo, a lista `nunca`. Todo o resto da referência é absorvível**, inclusive o nível de
> acabamento. Não empobrecer a peça em nome de "fugir da referência": o que separa as duas é a
> identidade, não a ambição.

Dois modos: **TÉCNICA** (copiar um efeito específico pra dentro de uma peça que já existe) e
**DIREÇÃO** (reconstruir a peça inteira no espírito da referência). Perguntar qual se não estiver claro.

Antes de dizer que ficou bom: **renderizar e olhar o PNG**, comparando com a referência lado a lado.
Referência é de uso único — não montar pasta nem coleção. Se a marca tiver arquivo de composição
(`marca/composicao.md` ou equivalente), é lá que a técnica nova fica registrada depois.

### Como o tipo se comporta (independe da fonte escolhida)

A regra de kerning é estrutural e vale pra qualquer marca: **título grande com kerning apertado ×
kicker pequeno com kerning aberto.** Esse contraste é o que faz a peça parecer editorial em vez de
template. Os valores exatos (famílias, pesos, px, letter-spacing) estão em `tipografia` no `design.json`.

### Elementos visuais recorrentes

- **Logo top-left** em todos os slides
- **Nada de régua, fio ou linha divisória.** Sem barrinha de destaque embaixo do título, sem
  `border-top` separando o rodapé do conteúdo, sem divisor entre blocos. É o que mais entrega peça
  feita por template. O respiro separa; o traço não precisa existir. Vale pra qualquer carrossel.
- **Stamps circulares** (200x200, border 3px translúcida, rotate -10deg) pra selos/datas/dados
- **Tags/pills** uppercase, padding generoso, kerning aberto, pra rotular categoria do slide
- Padding lateral: `espacamento.padding_peca` do `design.json`

### Layouts nomeados

Vocabulário de layout — cada slide tem um nome. Variar entre eles pra criar ritmo:

- **CAPA** — eyebrow + título grande + subtítulo + @handle. Fundo: foto com gradient overlay (`rgba(12,10,9,0.55)` → `rgba(12,10,9,0.85)`) OU sólido (escuro/claro/destaque)
- **SOLO** — split horizontal: foto à esquerda 50% + texto à direita 50% (kicker + h2 + régua + parágrafo)
- **DUO** — texto em cima (kicker + h2 + régua + p) + 2 fotos lado a lado embaixo (ou 1 foto larga)
- **NÚMERO** — numeral gigante (200-320px, weight 800, cor de destaque) como elemento gráfico + h2 + parágrafo de apoio
- **CITAÇÃO** — aspas grandes em watermark + frase em h2 + atribuição
- **CTA FINAL** — fundo na cor de destaque, logo centralizado, headline curta, botão/CTA, telefone/@handle

**Ritmo de slide a slide:** alternar fundo escuro ↔ claro ↔ destaque. Nunca dois slides seguidos com o mesmo fundo.

---

## Padrão do carrossel

**Estrutura base (5 a 10 slides):**
- **Slide 1:** layout `CAPA`
- **Slides internos:** usar 2-3 layouts diferentes entre `SOLO` / `DUO` / `NÚMERO` / `CITAÇÃO`
- **Slide final:** layout `CTA FINAL`

Antes de criar qualquer visual: ler `marca/design.json`. Se não existir, rodar `/identidade`.

### Sequência de capas no feed (planejamento de grade)

Antes de definir a capa, considerar a **última capa publicada** pra alternar:
- claro → próxima é foto/escuro
- foto/escuro → próxima é cor da marca
- cor da marca → próxima é claro
- nunca duas capas iguais em sequência

Se o usuário não souber qual foi a última, perguntar.

### Linguagem (regra crítica)

Seguir `_contexto/preferencias.md`. Em geral: frases naturais, sem jargão de marketing, sem corporativês. O público real raramente fala "ticket médio", "performance", "B2B". Falar como ele fala.

### Legenda — sempre gerar junto

Ao terminar de renderizar os PNGs, gerar **automaticamente** a legenda do post e salvar em `legenda.md` na mesma pasta. **Não esperar o usuário pedir.** Estrutura padrão:

1. Hook (pergunta ou afirmação)
2. Contexto (1-2 frases sobre o conteúdo)
3. CTA pra arrastar ("Arraste pro lado e confere")
4. Bloco de oferta (diferenciais da empresa, contato)
5. Hashtags (10-15 — público + nicho + local se aplicável)

### Áudio — sugerir junto com a legenda

Carrossel também leva áudio, e a escolha tem critério. **A música não é trilha de clima, é atalho
semântico.** O leitor reconhece a faixa em meio segundo e já entende do que o post trata, antes de
ler qualquer slide. Sugerir "instrumental noir porque combina com a paleta" é errar o alvo: ninguém
reconhece um instrumental, então ele não comunica nada.

**O que faz a ponte é a LETRA**, de três formas:

| Relação | Como funciona | Quando usar |
|---|---|---|
| **Concordância** | um verso conhecido diz a mesma coisa que a tese do post | o argumento cabe numa frase que já existe numa música famosa |
| **Contraste** | a letra diz o oposto, e a ironia é o recado | o post desmonta uma crença que a música representa |
| **Paródia** | a letra vira piada aplicada ao tema | post leve, território de identificação |

**Como escolher, na ordem:**

1. Isolar a tese do post numa frase (ex: "não basta uma coisa só", "fiz tudo certo e não deu em nada").
2. Procurar uma música MUITO reconhecível pelo público-alvo cujo verso diga isso. Reconhecimento vale
   mais que encaixe perfeito: música que ninguém identifica não é atalho, é ruído.
3. Preferir o verso que aparece no começo da faixa. Em carrossel o leitor dá 20 a 40 segundos, então
   a ponte tem que acontecer nos primeiros segundos.
4. Evitar letra que brigue com a leitura do slide 1 (vocal forte no mesmo idioma, entrando junto com
   o gancho).

**Duas checagens antes de fechar:**

- **Disponibilidade:** conta profissional tem biblioteca de áudio reduzida por direito autoral, e
  faixa comercial famosa às vezes não aparece. Sugerir 2 ou 3 opções, não uma, e mandar o usuário
  conferir quais estão liberadas no app.
- **Alcance x encaixe:** se houver um áudio em alta no nicho, ele ganha do encaixe estético, porque a
  plataforma distribui. Só não vale usar áudio em alta que contradiga a mensagem do post.

Entregar as sugestões junto da `legenda.md`, com o **verso exato** que faz a ponte. Sem o verso, a
sugestão não dá pro usuário julgar.

---

## Workflow

### Passo 1 — Entender e planejar

1. Ler `_contexto/preferencias.md` e `_contexto/empresa.md`
2. **Ler `marca/design.json`** — os tokens. (Se não existir → `/identidade` primeiro.)
3. Identificar o tipo de conteúdo (1, 2 ou 3)
4. Definir o tema e o ângulo
5. Definir a rota de acabamento: **HTML** ou **Claude Design**

### Passo 2 — Texto

Escrever o conteúdo seguindo as regras de tom:

**Pra carrossel (5-10 slides):**
- Slide 1 (Capa): título impactante, máx 8 palavras. Oferecer 3 opções
- Slides internos: um insight por slide, frases naturais, sem bullet points
- Slide final: CTA + logo

**Pra post único:**
- Frase principal em destaque
- Contexto de apoio (se necessário)
- CTA sutil

**CHECKPOINT:** Mostrar o texto completo. Esperar aprovação antes do visual.

### Passo 3 — Escolher a foto (se tipo 2)

**Ordem de preferência. Não pular pro fim.** Foto de IA é a última opção, não a primeira: acervo
próprio é o que diferencia a peça de qualquer template.

**1º — O acervo da própria marca.** Ler `marca/design.json` → `imagem.fotos`. Se existir, ele traz as
fotos reais já classificadas por assunto e, separada, a lista das que **aguentam título em cima**.
Regra que vale mesmo sem esse bloco existir:

> Foto só serve de **capa** se tiver massa escura (ou clara, conforme a marca) **vazia** onde o título
> caiba sem cobrir o assunto — na prática ~40% da peça em área contínua e limpa, num canto só. Não é
> sobre a foto ser bonita: é sobre ter onde escrever. Sem isso, ela vira slide interno ou fundo de
> citação, nunca capa.

Ler também as notas por foto, quando houver: costumam registrar armadilhas que não se veem na
miniatura — cor parasita que briga com o acento da marca, texto legível na imagem que contradiz o
posicionamento atual, foto que não é a pessoa da marca (não serve de card de autoria).

**2º — Foto passada pelo usuário na hora.** Aplicar o mesmo teste de massa vazia antes de usar de capa.

**3º — Banco de imagem**, usando os termos de busca do `design.json` (`imagem.termos_banco`), pra
volume.

**4º — IA**, só quando as três acima não resolvem:

1. Montar prompt em inglês (a API funciona melhor em inglês)
2. Padrão genérico de prompt:

```
Professional [TIPO] photography of [ASSUNTO],
[DETALHES], [AMBIENTE/CONTEXTO],
[ESTILO DE LUZ] lighting, shallow depth of field,
shot from [ÂNGULO], [ESTILO/ESTÉTICA],
editorial quality
```

3. Gerar via script (se `scripts/gerar-imagem.js` existir):
```bash
node --env-file=.env scripts/gerar-imagem.js "PROMPT" "marketing/conteudo/<pasta>/foto-<nome>.png"
```

Se não tiver o script ainda, instruir o usuário a configurar `OPENAI_API_KEY` no `.env` e criar o script (ou usar outra ferramenta de geração de imagem).

4. Mostrar a foto pro usuário antes de continuar.

**CHECKPOINT:** Foto escolhida (do acervo) ou gerada → mostrar e esperar aprovação. Se não passar,
trocar a foto ou ajustar o prompt.

Foto nova que o usuário mandar durante o processo e que caiba no clima da marca: perguntar se ele
quer guardar no acervo de referências, e registrar no `design.json` se sim. Acervo que não cresce
empurra a próxima peça de volta pra IA.

### Passo 4A — Rota Claude Design (acabamento na mão)

Usar quando a peça é da marca própria, ou quando o acabamento importa mais que a velocidade.

**Pré-requisito:** o design system da marca já subido no Claude Design (feito uma vez pelo
`/identidade`, Passo 8). **Sem design system, a saída sai genérica — com cara de IA.** Se ainda não
subiu, mandar rodar `/identidade` antes.

1. Entregar ao usuário o **roteiro estruturado** — slide a slide, com o texto aprovado no Passo 2.
   O Claude Design precisa de input estruturado; não funciona com "faz um carrossel pra mim".
2. Ele abre `claude.ai/design` (web ou app, tanto faz), seleciona o **Design system** da marca e o
   template **Slides**, cola o roteiro e gera.
3. Ele **ajusta direto no canvas** — selecionando, redimensionando, aplicando efeito. Sem re-promptar.
   *(O primeiro shot sai ~80% bom; a revisão é esperada, não é falha.)*
4. Exporta as imagens e salva em `marketing/conteudo/<pasta>/instagram/`.
5. Gerar a legenda normalmente (Passo 5).

Avisar sobre o formato: o carrossel é **4:5 (1080x1350)**. Conferir o enquadramento na exportação.

### Passo 4B — Rota HTML (render automático)

1. Criar **um arquivo HTML por slide** (`slide-01.html`, `slide-02.html`, ...), cada um uma página completa 1080x1350 com a `<div class="slide">`. Inline CSS, Google Fonts como única dependência externa. (Dica: manter um `_head.html` com `<head><style>` e `_foot.html`, e concatenar com o corpo de cada slide pra não repetir CSS na mão; apagar os parciais no final.) Aplicar:
   - **Cor, tipografia, escala, radius e espaçamento LIDOS de `marca/design.json`** — valores literais, não aproximações
   - **Conferir a peça contra a lista `nunca` do `design.json` antes de renderizar**
   - Mínimo 2 layouts diferentes (não repetir o mesmo em todos os slides)
   - Logo top-left + slide-counter top-right em todos os slides
   - Slide final: logo + CTA, fundo na cor principal

   **Pra incluir foto IA no HTML:**
   ```html
   <div class="slide" style="
     background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.7)), url('foto-xxx.png');
     background-size: cover;
     background-position: center;
   ">
     <div class="content">
       <h2>Texto sobre a foto</h2>
     </div>
   </div>
   ```

2. Render PNG (método padrão — Chrome/Edge headless, sem Node/Playwright):

   **Importante:** criar **um arquivo HTML por slide** na pasta do conteúdo, nomeados `slide-01.html`, `slide-02.html`, etc. (cada um uma página completa 1080x1350 com CSS inline). O screenshot headless captura uma página por vez, então não dá pra usar um único `carrossel.html` com vários `.slide` empilhados pro render.

   Depois rodar:
```powershell
& ".\scripts\render-carrossel.ps1" -Folder "marketing\conteudo\<pasta-do-conteudo>"
```
   O script acha Chrome (ou Edge), renderiza todos os `slide-*.html` em `<pasta>/instagram/slide-NN.png` a 1080x1350. Pra TikTok/Reels (9:16): `-Width 1080 -Height 1920 -Out tiktok`.

   Não usar `-ExecutionPolicy Bypass` (é ação de segurança bloqueada). Chamar com o operador `&` direto, como acima.

3. Mostrar slide 1, 2 e o CTA final renderizados. Se aprovado, mostrar os intermediários.

### Passo 5 — Salvar e organizar

```
marketing/conteudo/<tipo>-<tema>-<YYYY-MM-DD>/
  texto.md              ← texto aprovado
  foto-<nome>.png       ← fotos geradas por IA (se houver)
  slide-01.html → slide-NN.html   ← uma página por slide (fonte do render)
  instagram/
    slide-01.png → slide-NN.png
  tiktok/ (se pedido — formato 9:16)
    slide-01.png → ...
  legenda.md            ← legenda Insta+FB
  legenda-linkedin.md   ← (se pedido, mais formal)
```

### Passo 6 — Conexão com blog (opcional)

Depois de criar o conteúdo visual, perguntar:

> "Esse conteúdo dá pra virar artigo no blog também. Quer que eu crie a versão blog pra SEO?"

Se sim, chamar `/publicar-tema` com o mesmo tema.

---

## Regras

- **Sempre ler `marca/design.json` antes de criar qualquer visual. Nunca improvisar cor, fonte,
  escala ou espaçamento — sai tudo do JSON.** Se o JSON não existir, rodar `/identidade`, não inventar.
- **Antes de renderizar, conferir a peça contra a lista `nunca` do `design.json`.** Se violou, refazer.
- Se o `design-guide.md` (prosa) divergir do `design.json` (tokens), **o JSON manda**
- Rota Claude Design exige o design system já subido (`/identidade`, Passo 8). Sem ele, o resultado é genérico
- Carrossel: 1080x1350 (4:5 retrato) — sempre. TikTok/Reels: 1080x1920 (9:16) — só quando pedido explicitamente
- Linguagem segue `_contexto/preferencias.md` estritamente
- Sempre considerar a sequência de capa no feed antes de definir capa nova
- Sempre gerar legenda automaticamente ao final, salvando em `legenda.md`
- Sugestão de áudio vem junto da legenda, e sempre pela LETRA (atalho semântico), nunca por clima
  instrumental. Ver a seção "Áudio"
- Fotos IA: sempre pedir aprovação antes de usar no carrossel
- Fotos IA: prompts em inglês
- Fotos IA: nunca gerar fotos de pessoas/rostos identificáveis
- HTMLs: um arquivo por slide (`slide-01.html`, `slide-02.html`, ...), CSS inline. Sem `carrossel.html` único e sem `render.js`
- Render: usar `scripts/render-carrossel.ps1` (Chrome/Edge headless). Sem Node/Playwright. Nunca usar `-ExecutionPolicy Bypass`
- Não repetir layout entre slides — usar variação visual
