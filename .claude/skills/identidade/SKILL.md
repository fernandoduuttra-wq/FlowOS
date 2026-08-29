---
name: identidade
description: >
  Constrói (ou refaz) a identidade visual de uma marca do zero e gera os tokens que todas as skills
  visuais consomem. Faz a análise de distinção contra os concorrentes, quebra a marca em componentes
  (símbolo, fonte do logo, paleta, pareamento de fontes, estilo de imagem), produz logo vetorial em
  SVG claro/escuro, escreve o brandbook e — o mais importante — gera o `marca/design.json`, que
  vira a fonte única de verdade visual. Também prepara o pacote de assets pro Design System do Claude
  Design. Use quando o usuário disser "/identidade", "criar identidade visual", "rebrand", "refazer a
  marca", "definir a paleta/fonte/logo", "montar o design system", "meu visual tá genérico", ou pedir
  brandbook/manual de marca.
---

# /identidade — Marca, tokens e design system

Skill de fundação visual. Tudo que o sistema desenha (carrossel, proposta, site, slides) herda daqui.

**Regra de ouro:** design ruim feito com IA não é falta de ferramenta, é **prompt genérico**. "Cria
uma marca pra mim" nunca funciona. O método é **quebrar a marca em componentes e atacar cada um com
sua própria referência.**

## Três níveis — não confundir

| Nível | O que é | Quando roda | Onde vive |
|---|---|---|---|
| **Identidade visual** | A marca: símbolo, logo, paleta, fontes, estilo de imagem | Uma vez, ou no rebrand | `marca/brandbook.md` + assets |
| **Design system** | Os tokens: cor, tipo, escala, forma, spacing | Sai do nível 1, depois só herda | `marca/design.json` |
| **Peça** | Post, slide, landing, proposta | Todo dia | Skills de conteúdo, que LEEM o `design.json` |

Esta skill entrega os níveis 1 e 2. O nível 3 é das outras skills.

## Dependências

- `_contexto/empresa.md`, `_contexto/preferencias.md` — quem é a marca, como fala
- `_contexto/posicionamento.md` — Tese/Mecanismo/Oferta, quando existir. Se não existir, extrair no
  Passo 1 o mínimo necessário sobre público, oferta, diferença e percepção desejada antes de decidir
  o visual — **a identidade visual serve ao negócio, não o contrário**.
- Saídas: `marca/design.json` (máquina), `marca/brandbook.md` (humano), `marca/logo*.svg`

---

## Passo 1 — Distinção (nunca pular)

O princípio-mestre da identidade é **ocupar um espaço mental que o concorrente não ocupa**. Bancos
brasileiros são o caso didático: Itaú travou laranja, Bradesco vermelho, Nubank roxo. Ninguém entra
no espaço do outro.

1. Levantar 5-10 concorrentes/referências diretas do nicho.
2. Pra cada um, catalogar: **cor dominante, família tipográfica, estética geral** (corporativo?
   infoproduto? editorial? brutalista?).
3. Montar a tabela e responder: **qual espaço está vago?**

**CHECKPOINT:** mostrar a tabela e o espaço vago identificado. Confirmar antes de seguir.

## Passo 2 — Símbolo

Gerar **10 conceitos de ícone** pra marca — descritos em texto, com a lógica de cada um. O usuário
escolhe um (ou pede outra rodada).

Critério: geométrico, minimalista, funciona a 16px e a 500px, não depende de cor pra ser lido.

## Passo 3 — Referências, uma busca POR COMPONENTE

Aqui está o pulo do gato. **Uma busca só ("identidade visual bonita") produz lixo.** São cinco buscas
separadas, cinco pastas de referência:

| Componente | Onde buscar | O que buscar | Critério |
|---|---|---|---|
| Ícone | Pinterest | "[conceito escolhido] icon" | Simplicidade geométrica |
| Fonte do logo | Pinterest | "logo fonts" | **Personalidade — nunca a fonte genérica** |
| Paleta | Pinterest | "color palettes [cor do espaço vago]" | Coerente com o Passo 1 |
| Pareamento de fontes | Pinterest | "font pairings" | Contraste real entre título e corpo |
| Estilo de imagem | Pinterest / Dribbble | o motivo visual da marca | Reprodutível, não sorte |

Pedir ao usuário que colete e traga as referências (ou traga prints). **Não inventar referência.**

**CHECKPOINT:** referências aprovadas antes de produzir qualquer coisa.

## Passo 4 — Produzir o logo

1. **Parte tipográfica** — o nome na fonte escolhida.
2. **Ícone + nome** — montar num gerador vetorial. O prompt precisa exigir explicitamente que **o
   peso do ícone case com o peso e o estilo da fonte** (senão sai desalinhado).
3. **Exportar:** fundo removido, vetorizado, **SVG em versão clara E escura**. Salvar em
   `marca/logo.svg` e `marca/logo-branco.svg`.

## Passo 5 — Estilo de imagem reutilizável

Subir as referências de imagem num gerador que suporte *custom style*. Isso trava a estética: toda
imagem futura sai coerente, em vez de cada peça ter uma cara. Registrar o estilo no `design.json`
em `imagem.estilo`.

## Passo 6 — Gerar o `design.json` (a entrega principal)

Fazer **engenharia reversa das REFERÊNCIAS VISUAIS aprovadas** (Passo 3) e escrever os tokens.

**REGRA CRÍTICA (aprendida na marra):** o `design.json` nasce de **imagens de referência reais**, NÃO
de adjetivos de um design-guide. Montar tokens a partir de descrição em texto ("serifa pesada",
"vermelho editorial") produz um sistema *correto e vazio* — o resultado tem cara de template genérico.
O pulo do gato é extrair os valores de uma referência linda de verdade, por engenharia reversa. Se não
houver referência visual, **voltar ao Passo 3** — não inventar os tokens de adjetivo.

O JSON tem que cobrir: `cores`, `tipografia` (famílias, pesos, letter-spacing, escala em px),
`espacamento`, `forma` (radius, borda, sombra), `imagem` (estilo + overlay + estratégia de fonte),
`formatos` (dimensões por canal) e — obrigatório — a lista **`nunca`**.

A lista `nunca` é o antídoto contra os red flags de IA. Sempre incluir, no mínimo:
- gradiente roxo genérico
- fontes default de template
- peça só com ícone, sem imagem de verdade
- mais de uma cor de destaque por peça

**Este arquivo passa a mandar.** Se o `design-guide.md` (prosa) divergir do `design.json` (tokens),
o JSON vence. Nenhuma skill visual improvisa CSS depois disso.

### Quando a entrega é um produto/site em Next.js — fundação de design system em código

Pra carrossel, proposta e slide o `design.json` + o brandbook já bastam: as skills de conteúdo leem o
JSON e renderizam. Mas quando a entrega é um **produto ou site em Next.js**, o design system precisa
existir DENTRO do projeto, rodando de verdade em `localhost` — não como arquivo solto em `marca/`.
É um método de três passos, sempre nessa ordem:

**A — Fundação.** Rodar `npx shadcn@latest init` (estilo Default, base color Neutral — vai ser
sobrescrita —, CSS variables: Yes). Substituir `app/globals.css` pelas variáveis extraídas do
`design.json`, traduzidas pra nomenclatura shadcn. **O `design.json` não tem chave fixa pra cor**
(um projeto usa `cores.fundo`/`cores.destaque`; outro nomeia cada cor pelo próprio nome — `verde_profundo`,
`dourado_tinta` — com um campo `papel` descrevendo o uso) — então o mapeamento é por **papel**, lido no
`$meta`/`papel` de cada token, não por nome de chave:

| shadcn (`globals.css`) | o token cujo papel é... |
|---|---|
| `--background` | fundo padrão da peça |
| `--foreground` | texto principal sobre o fundo |
| `--card` | superfície/bloco/card |
| `--primary` | cor de destaque/marca (a que a lista `nunca` protege — nunca mais de uma) |
| `--muted-foreground` | texto secundário/apagado |
| `--border` / `--input` | borda |
| `--radius` | `forma.radius` (ou o menor raio de card, se for um objeto de escala) |
| `--font-sans` | a família de corpo (`tipografia.corpo`) |
| `--font-serif`/display | a família de título/display (`tipografia.titulo`/`tipografia.display`) |

Cobrir também `--secondary`, `--muted`, `--accent`, `--destructive`, `--ring`, `--popover`, `--sidebar-*`
e as semânticas `--success`/`--warning`/`--info` — a maioria dos `design.json` de hoje só define os
papéis centrais (destaque, fundo, superfície, texto); quando faltar um papel do shadcn, **gerar por
teoria de cor a partir do que já existe** (não inventar cor nova fora do território do Passo 1) e, se a
marca passar a precisar dele de verdade, propagar de volta pro `design.json` com seu próprio `papel` e
`origem`. Instalar a fonte via `next/font/google` no `layout.tsx`.

Criar a rota **`/app/styleguide`** dentro do próprio projeto: layout com sidebar de navegação +
página com TODOS os tokens visíveis (paleta com hex, tipografia, radius, sombra) e os componentes base
(Button, Card, Badge, Alert) já no tema da marca, com toggle de dark mode. É uma página React de
verdade, navegável em `localhost:3000/styleguide` — o "bater o olho e aprovar" acontece ali, rodando,
não num mockup.

**B — Componente novo (sob demanda).** Antes de construir do zero, checar se o shadcn já tem o
componente (`npx shadcn@latest add [nome]`) — ele já nasce plugado nas variáveis do `globals.css`.
Só customizar/estender quando o shadcn não cobrir o caso. Todo componente novo ganha uma página de
showcase em `/app/styleguide/components/[nome]/` e entra no `navigation.ts` — o styleguide cresce
junto com o produto, nunca fica defasado.

**C — Página nova.** Antes de codar, mapear cada elemento visual do brief/referência pra um componente
já existente no styleguide (sidebar → `Sidebar`, card de conteúdo → `Card`, ação primária → `Button`
variant default...). Instalar só o que faltar, montar a página com classes Tailwind que apontam pras
variáveis (`bg-card`, `text-muted-foreground`, `border-border`), mobile-first.

**Regra que fecha o ciclo:** nenhuma peça em React usa hex direto no JSX/CSS — sempre a variável do
`globals.css`. É esse tema plugado (não o `zinc`/`slate` default do `shadcn init`) que evita a peça em
React sair com cara de template do shadcn em vez de cara da marca. Rodar `/frontend-design` pro
critério de composição depois que o tema estiver plugado — ela cuida de hierarquia, tipografia e
restrição; este passo aqui só cuida do tema estar correto.

## Passo 7 — Brandbook

Escrever `marca/brandbook.md`: a versão em prosa, pra humano — o racional da distinção, o que a
marca é e o que ela nunca é, onde cada asset se usa. Ele **explica**; o `design.json` **executa**.

---

## Passo 8 — Empacotar pro Claude Design

O Claude Design gera peças na identidade da marca **só se receber o design system**. Sem ele, a
saída é genérica — tem cara de IA. Com ele, o primeiro shot sai ~80% bom e o resto se ajusta na mão.

**O pacote de upload manual** (juntar tudo numa pasta `marca/claude-design/`):

1. **`design.json`** — os tokens
2. **As duas fontes** — arquivos de título e de corpo
3. **Todas as imagens da marca** — o motivo visual
4. **Logos em todas as versões** — normal, ícone, branco, preto

**Fluxo no Claude Design:**
1. `claude.ai/design` (web ou app — tanto faz) → aba **Design systems** → **Create**
2. Upload manual dos 4 itens acima. *(Também aceita repositório do GitHub, projeto local ou Figma —
   mas o manual dá mais controle e é o recomendado.)*
3. Revisar asset por asset. Marcar **"Needs work"** no que saiu errado e deixar ele corrigir.
4. A partir daí, toda peça criada lá já nasce na identidade.

**O que o Claude Design 2.0 resolve (e por que ele entra no fluxo):**
- **Edição direta no canvas** — selecionar, redimensionar, aplicar efeito **sem re-promptar cada
  ajuste**. É onde o julgamento visual volta pra mão do usuário.
- **Design ⇄ Código nos dois sentidos** — manda a peça pro Claude Code e puxa de volta.
- **Templates:** Prototype · Slides · Document · Wireframe · Animation.
- **Export:** painel de destinos (Claude Code, Vercel e afins) ou download do zip.

**Limitações (avisar o usuário):**
- Ele **não cria identidade do zero** — por isso esta skill roda ANTES dele.
- Precisa de **input estruturado** (roteiro/copy pronta), não "faz um post pra mim".
- Primeiro shot é ~80%: **sempre revisar**.

**A rota HTML (render local via CSS + screenshot) é o plano B, não o A.** Ela tem teto de qualidade
baixo: sai com cara de "post HTML genérico". Serve pra volume/rascunho. Pra peça de marca que precisa
ficar premium, é o Claude Design que entrega — porque o motor de design dele compõe hierarquia e
tratamento que HTML escrito à mão não alcança. Não vender a rota HTML como equivalente.

**Pacote pronto pra subir:** quando o pacote de upload já existir (ex: `marca/claude-design/`
com `design.json` + `fontes/` + `logos/` + `imagens/` + um `GUIA-passo-a-passo.md`), apontar o
usuário pra lá em vez de remontar.

---

## Regras

- Nunca pular o Passo 1 (distinção). Marca sem distinção é marca invisível, por mais bonita que seja.
- Nunca fazer uma busca de referência só — são cinco, uma por componente.
- Nunca inventar referência visual. Se não tem referência, pedir ao usuário.
- O `design.json` é a fonte da verdade. O `design-guide.md`/brandbook explica; o JSON manda.
- A identidade serve ao negócio. Se não houver contexto estratégico suficiente, coletar o mínimo no
  Passo 1 antes de tomar qualquer decisão visual.
- Logo sempre em SVG, sempre em versão clara e escura.
- Toda vez que o `design.json` mudar, avisar quais skills consomem ele (hoje: `/carrossel`, propostas de cliente, site).
