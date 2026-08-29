---
name: site
description: >
  Constrói sites e landing pages de nível premium — com animação, profundidade e efeitos refinados —
  usando engenharia reversa de uma referência real como parâmetro de qualidade. Baixa o código do site
  de inspiração, disseca as técnicas (smooth scroll, spring, reveal, parallax, 3D), e reconstrói na
  identidade da marca (lê o design.json), com dev server rodando no navegador pra iterar a animação de
  verdade. Dois modos: EFEITO (copiar um efeito específico) ou INSPIRAÇÃO (o site inteiro como padrão,
  recombinado pra fugir de plágio, mesmo nível ou 10x). Serve pros ativos do próprio negócio e pros
  clientes. Use quando o usuário disser "/site", "criar um site", "landing page", "quero um site nesse
  nível", "copia esse efeito", "reconstrói esse site", colar um link de site de referência, ou pedir um
  site com animação/profundidade/efeitos avançados.
---

# /site — Sites premium por engenharia reversa

Skill de construção de site com o teto alto: animação, profundidade, efeito refinado. O que HTML solto
com CSS inline nunca alcança. O método é: **dissecar uma referência excelente → extrair a técnica →
reconstruir na marca**.

## Princípio

Site que impressiona sai de **referência**, não de improviso. Ninguém acerta profundidade e movimento
"de cabeça". Aponta-se uma referência de nível, entende-se **como** ela foi feita, e reconstrói-se com
a identidade própria. Sem referência, o resultado é o denominador comum (o "post HTML genérico").

## Dependências

- **Tokens da marca:** `marca/design.json` — **a fonte da verdade visual.** Cor, tipografia,
  radius, espaçamento e a lista `nunca` saem daqui. O site herda a marca; a referência dá só a
  **técnica e o nível**, nunca a paleta. Se o JSON não existir, rodar `/identidade` antes.
- **Posicionamento:** `_contexto/posicionamento.md` e `_contexto/preferencias.md` — pra copy e tom.
- **Convenção do negócio:** se o `CLAUDE.md` da raiz definir esteira/stack própria, ela manda.
- **Node + npm** (já instalados). **Git** pra versionar.

---

## Os dois modos (perguntar no início)

O motor é o mesmo; muda o escopo do que se extrai da referência.

### Modo EFEITO
"Quero só aquele efeito" (o menu que desliza, o parallax, a transição, o smooth scroll).
→ Extrai **aquele pedaço**, identifica a técnica, e adapta pra marca. Cirúrgico.

### Modo INSPIRAÇÃO
"Quero um site nesse nível."
→ Usa o site inteiro como **parâmetro de qualidade**. **Recombina** com outras referências + o
`design.json` pra fugir de plágio. Mira mesmo nível ou acima.

**Regra da recombinação (anti-plágio E anti-genérico):** nunca clonar um site só. Juntar a TÉCNICA de
2-3 referências + a identidade da marca. O resultado não é cópia de nenhuma e pode superar todas.
Verdade dura: recombinar lixo dá lixo. A curadoria da referência é a parte que mais importa — 2-3
excelentes valem mais que 10 medianas.

**Ética/legal (sempre):** engenharia reversa da **técnica**, nunca cópia de layout+conteúdo. Não puxar
textos, imagens, logos ou fontes proprietárias da referência. O que se reproduz é *como o efeito
funciona*, reconstruído do zero na marca própria. Mesma regra do resto do sistema: método destilado,
não cópia.

---

## Passo 1 — Referência e engenharia reversa

1. Receber o(s) link(s) de referência. Se o usuário não tem, ajudar a achar (Awwwards, Godly,
   Land-book, One Page Love pra o nível; Dribbble pra pedaços).
2. **Baixar o código:**
   ```bash
   curl -sL -A "Mozilla/5.0 ... Chrome/126 Safari/537.36" "<URL>" -o ref.html
   ```
3. **Dissecar** — identificar no código:
   - **Como foi feito:** Framer, Webflow, WordPress, ou codado (React/Next/Astro/HTML). `grep` por
     `generator`, `framer-`, `wp-`, `__next`, `astro-`.
   - **Bibliotecas de movimento:** `grep -oiE 'lenis|gsap|framer|three|spline|lottie|locomotive|swiper|barba'`
   - **Easing/física:** `cubic-bezier`, `spring`, `stiffness`, `damping`, `@keyframes`
   - **Cores e fontes** (só pra entender o nível, NÃO copiar — a paleta vem do design.json)
4. **Nomear as técnicas** que produzem o "premium". Quase sempre são poucas e nomeáveis (ver
   `references/efeitos.md`). Resumir pro usuário: "o que faz esse site parecer caro é X, Y, Z".

> **Cuidado do código compilado:** site feito em Framer/Webflow ou em React vem minificado/gerado por
> máquina. Dá pra ler as TÉCNICAS perfeitamente, mas não é fonte limpa pra copiar. E tudo bem — as
> técnicas são replicáveis fora da ferramenta original (Lenis, GSAP, Framer Motion são todas livres).

**CHECKPOINT:** apresentar a dissecação (o que faz o nível) e confirmar o alvo antes de construir.

## Passo 2 — Escolher a stack (proporcional ao alvo)

Não usar canhão pra matar mosca. Escalar a stack ao que a peça precisa:

| Alvo | Stack |
|---|---|
| Página simples, sóbria (Lo-fi) | Vite + Tailwind, CSS puro. Sem lib de motion. |
| Landing premium com animação | **Vite + React + Tailwind + Framer Motion + Lenis** (o padrão) |
| Scroll-driven / timeline complexa | + **GSAP + ScrollTrigger** |
| 3D | + **Spline** (embed no-code) ou **React Three Fiber** (código) |
| Micro-animação (ícone, loader) | + **Lottie** |
| Precisa de SEO forte / blog | trocar Vite por **Next.js** |

Consistência com o resto: Tailwind + a estrutura de tokens do `design.json`. Pra direção estética
(evitar cara de template, escolher tipografia/layout com intenção),
apoiar na skill `frontend-design` quando existir.

## Passo 3 — Onde o projeto roda (regra dura do ambiente)

**O projeto Node NÃO vive no OneDrive.** `node_modules` é enorme, o caminho tem acento, e o OneDrive
desidrata/quebra os paths. Rodar em `%LOCALAPPDATA%\<projeto>\` (fora do OneDrive). Só o resultado
final (build, ou o link publicado) volta pro repo.

```bash
mkdir -p "$LOCALAPPDATA/sites/<nome>" && cd "$LOCALAPPDATA/sites/<nome>"
npm create vite@latest . -- --template react
npm install && npm install framer-motion @studio-freight/lenis
```

## Passo 4 — Construir lendo o design.json

Aplicar **os tokens da marca** (não os da referência): cores, tipografia, radius, espaçamento. A
referência entra só como a técnica de movimento e o nível de acabamento. Conferir a peça contra a
lista `nunca` do `design.json`.

## Passo 5 — O LOOP (ver a animação rodar, não screenshot)

Esta é a diferença entre refinar e chutar. Animação não se ajusta em print congelado.

1. Subir o dev server: `npm run dev` (Vite serve em `localhost:5173`).
2. **Ver rodando de verdade** com um browser que executa o JS (Playwright/Chrome headless dirigido),
   capturando o estado real da página — com as animações executadas, não o HTML estático.
3. Ajustar timing/easing/camada → o hot-reload atualiza na hora → ver de novo. Iterar até refinar.

Sem este loop, movimento é invisível e vira loteria. Com ele, refina-se de verdade.

## Passo 6 — Aprovação e deploy

**Aprovação visual do usuário ANTES de publicar.**
Só depois de aprovado: build (`npm run build`), e deploy (Netlify/Vercel). O link publicado e/ou o
build entram no repo; `node_modules` nunca (gitignore).

---

## Regras

- Referência dá TÉCNICA e NÍVEL; a marca (design.json) dá cor, fonte e forma. Nunca copiar a paleta da referência.
- Nunca clonar um site só — recombinar 2-3 + a identidade. Cópia de layout/conteúdo é plágio, é proibido.
- Não puxar textos, imagens, logos nem fontes proprietárias da referência.
- Stack proporcional ao alvo. Site sóbrio não precisa de 3D.
- Projeto Node roda FORA do OneDrive (%LOCALAPPDATA%). Só o resultado vai pro repo.
- Sempre o loop de dev server + ver rodando antes de dar por pronta uma animação.
- Aprovação visual antes de qualquer deploy.
- Serve pros dois donos: ativos do próprio negócio e sites de cliente. O design.json muda por projeto
  (cliente tem o seu); o método é o mesmo.
