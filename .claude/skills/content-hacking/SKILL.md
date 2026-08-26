---
name: content-hacking
description: >
  Recebe link (ou conteúdo colado na mão) de qualquer rede — YouTube, Instagram reel, Instagram
  carrossel, LinkedIn, Substack — disseca a estrutura, extrai o esqueleto com lacunas e devolve
  roteiro pronto pra gravar, cadastrando tudo no Notion (Banco de Referências + Ideias de Conteúdo).
  Gera 3 versões: esqueleto reutilizável, clone fiel e recombinado. Roda automático, sem pedir
  aprovação item a item.
  Use quando o usuário colar link de conteúdo pra modelar, colar prints de um carrossel, colar o
  texto de um post, ou disser "content hacking", "disseca isso", "rouba essa ideia", "extrai a
  fórmula desse viral", "processa os Novo", ou /content-hacking.
---

# /content-hacking — Dissecar conteúdo validado e devolver roteiro

Funnel hacking aplicado a conteúdo: achar o que já funcionou, entender **por que** funcionou, e
refazer melhor. Roda em qualquer rede — o motor é o mesmo, só muda como a matéria-prima entra e
onde mora o gancho.

> **A regra de ouro:** gancho se copia, ouro se melhora, CTA se replica.
> Preserva a estrutura do que deu certo; troca o miolo pelo contexto do usuário.

> **A trava que separa aprender de copiar:** a **psicologia** das versões adaptadas tem que ser a
> MESMA do original. Se o original funcionava por prova social e a sua versão virou curiosidade,
> você copiou a forma e perdeu o motor.

> **A segunda trava: às vezes o FORMATO é o motor, não o veículo.** Print de tweet, foto crua da
> galeria com texto por cima, print de conversa, print de painel — esses formatos carregam
> significado sozinhos: leem como **registro** de algo que aconteceu, não como peça produzida pra
> convencer. Quando o formato é o motor, dissecar o texto e reembalar na identidade visual do
> usuário **joga fora exatamente o que fazia funcionar**.
>
> **O teste:** reescreve o mesmo texto numa peça diagramada padrão da marca. Perdeu força? Então o
> formato era motor, e ele atravessa junto com a psicologia.

## Princípio de operação: automático, sem fricção

**Não pedir aprovação item a item.** Processa tudo que o usuário mandou, do começo ao fim, e só
apresenta o resumo no final. O usuário filtra depois, pelo campo **Potencial**.

O gargalo de quem cria conteúdo nunca é falta de análise — é excesso dela. Cada pergunta que essa
skill faz antes de produzir é uma chance a mais de não publicar. Se der pra inferir, infira.

---

## Setup — ler antes de processar

**Do `CLAUDE.md` da raiz** (é lá que fica tudo que é específico da operação; a skill é genérica):
- IDs dos dois databases do Notion (Banco de Referências e Ideias de Conteúdo)
- Canal primário e secundário
- Convenções próprias de coleta, se a raiz definir alguma

**Contexto de voz e posicionamento** (obrigatório — é o que faz o roteiro sair na voz do usuário,
não na voz genérica de IA). Ler o que existir:
- `_contexto/posicionamento.md` — Tese, Mecanismo, Oferta. O roteiro serve a isso.
- `_contexto/preferencias.md` — tom, estilo, o que evitar, blindagem anti-IA
- `_contexto/empresa.md` e `_contexto/estrategia.md` — quem é, foco atual
- `marketing/comunicacao/doutrina-de-comunicacao.md` — doutrina de persuasão, se existir

> Se a raiz definir convenções próprias (esteira de publicação, territórios de conteúdo, formatos),
> **elas mandam** sobre os defaults desta skill.

**Referências desta skill:**
- `notion.md` — schema dos 2 databases e como escrever neles
- `redes/<rede>.md` — como a matéria-prima entra e onde mora o gancho, por rede

---

## Fluxo

```
0. Dedup        → consulta o Notion pelo Link
1. Entrada      → auto (download) ou manual (colado). Ver redes/<rede>.md
2. Ler          → transcrever / assistir / ler os slides
3. Traduzir     → se for gringo
4. Classificar  → Objetivo, Formato, Gancho, CTA, Psicologia, Potencial
5. Banco        → cadastra a referência dissecada
6. 3 versões    → V0 no corpo do Banco; V1 e V2 viram cards em Ideias
7. Status       → "Virou Ideia"
```

### Passo 0 — Dedup

Antes de baixar qualquer coisa, consultar o **Banco de Referências** no Notion filtrando por `Link`.

- **Não existe** → referência nova, segue pro Passo 1.
- **Existe com `Status: Novo`** → é um item enfileirado à mão. Segue o fluxo, mas no Passo 5
  **completa a página existente** em vez de criar outra.
- **Existe com `Status: Analisado` ou `Virou Ideia`** → já processado. **Pula.** Avisa
  ("Já dissequei esse antes ('<título>'), pulando.") e vai pro próximo.

O database é o índice. Não manter arquivo local de processados — seria uma segunda verdade.

### Passo 1 — Entrada

Identificar a rede pelo link (ou pelo que o usuário colou) e ler `redes/<rede>.md`. Resumo:

| Rede | Rota padrão | Origem |
|---|---|---|
| YouTube | `scripts/coleta-youtube.ps1` → metadados + transcrição + frames | Auto |
| Instagram — reel | `/watch` (baixa, transcreve, extrai frames pro Claude assistir) | Auto |
| Instagram — carrossel | `scripts/instagram-carrossel.py <url>` → slides em ordem + legenda, sem login | Auto |
| LinkedIn | **usuário cola o texto** | Manual |
| Substack / newsletter | **usuário cola o texto** (com o assunto do email) | Manual |
| Twitter / X | **usuário cola o texto ou o print** (transcrever literal) | Manual |

**A entrada manual é cidadã de primeira classe, não um fallback.** Se o usuário colar imagem ou
texto em vez de link, processar normalmente — só marcar `Origem: Manual (colado)` e deixar `Link`
vazio se ele não tiver mandado.

> **Onde a mídia mora:** download pesado (vídeo, frames) vai pra cache local **fora do OneDrive**
> (`%LOCALAPPDATA%\mazyos-hack\`). Sob caminho acentuado do OneDrive os arquivos que o yt-dlp/ffmpeg
> gravam desidratam e somem. Nada de mídia no repo.

### Passo 2 — Ler o conteúdo

Transcrição não basta. **Ver** o conteúdo:

- **Vídeo (YT / reel):** cruzar a transcrição com os frames. A transcrição não pega o texto na tela,
  o corte, o cenário, a autoridade de cena (uniforme, lapela, estúdio). O gancho quase sempre é
  fala **+** visual ao mesmo tempo.
- **Carrossel:** slide a slide. Slide 1 = gancho. Miolo = desenvolvimento. Último = CTA.
- **Texto (LinkedIn / Substack):** o gancho é o que aparece **antes do corte** — ver `redes/<rede>.md`.

**Se não houver fala** (vídeo puramente visual — meme, lifestyle, ação sem narração), marcar como
**modo "Sem fala"**: muda o corpo da página (Passo 5) e a geração de versões (Passo 6).

### Passo 3 — Traduzir

Se o original for em outra língua, traduzir pra português. Manter tom e adaptar gíria ao público
brasileiro quando fizer sentido. Guardar o idioma original no campo `Idioma`.

### Passo 4 — Classificar

| Campo | Como preencher |
|---|---|
| **Objetivo** | `Viral` (entretenimento, identificação, alcance) / `Útil` (tutorial, autoridade, salvos) / `Vendas` (posicionamento, prova, oferta) |
| **Formato de Produção** | Talking head / Mãozinha (câmera na tela) / Tela dividida / Lifestyle / Clone / Depoimento / Estático |
| **Formato: veículo ou motor** | Aplicar o teste da segunda trava (lá em cima). `Veículo` = o texto sobrevive rediagramado, então a peça adaptada pode ir na identidade do usuário. `Motor` = o formato carrega significado e **precisa atravessar**. Anotar no `Por que`, critério 2. |
| **Tipo de Gancho** | Curiosidade / Identificação / Revolta / Benefício direto / Novidade |
| **Hook original** | A frase exata dos primeiros segundos (ou o slide 1 / as 2 primeiras linhas). Formato abaixo. |
| **CTA identificada** | A CTA usada. `Nenhuma` se não houver. |
| **Psicologia** | **O campo mais importante.** Por que isso funciona — o mecanismo mental, em texto livre. Não é resumo do conteúdo. |
| **Potencial** | Alto / Médio / Baixo — alinhamento com o território do usuário + replicabilidade |
| **Por que** | 3 critérios numerados. Formato abaixo. |
| **Idioma** | Português / Inglês / Outro |

**Formato do `Hook original`** — fala primeiro, visual depois, uma linha em branco entre os dois.
No modo "Sem fala", deixar `Fala: (sem fala)`.

```
Fala: "<frase exata dos primeiros segundos>"

Visual: <o que aparece na tela ao mesmo tempo — texto, ação, elemento gráfico>
```

**Formato do `Por que`** — sempre 3 critérios numerados, 1 frase cada:

```
1. Alinhamento: <como o tema/estrutura conecta com o território do usuário>
2. Replicabilidade: <quão fácil é refazer isso com os recursos que ele tem>
3. Métricas: <números do original — views, comentários, razão comentário/like; ou "não disponível">
```

**Sobre `Psicologia` — escrever o mecanismo, não o assunto.**

- ❌ "Fala sobre produtividade e organização."  ← isso é resumo, não psicologia
- ✅ "Abre admitindo um fracasso concreto e datado ('perdi R$ 40 mil'). A confissão de perda compra
  permissão pra ensinar: quem já pagou o preço tem direito de falar. O espectador baixa a guarda
  porque ninguém inventa uma humilhação específica. O número exato é o que torna a confissão
  verificável — e é ele que sustenta os 40 segundos seguintes."

O campo `Psicologia` é o que permite o Passo 6 recombinar sem descaracterizar. Se ele estiver vago,
a V2 vai sair genérica.

### Passo 5 — Cadastrar no Banco de Referências

Criar a página (ou completar o stub, se o Passo 0 achou um com `Status: Novo`). Ver `notion.md` pro
schema completo. `Status: Analisado`, `Data: hoje`.

**Corpo da página** — nesta ordem, três blocos:

### 1. Conteúdo na íntegra
O conteúdo ORIGINAL COMPLETO, **card a card** (slide a slide no carrossel; parágrafo a
parágrafo no texto; fala + descrição de cena no vídeo). Traduzido, mas **sem resumir e sem
colchetes** — é a transcrição crua, o material de estudo. **Nunca condensar** ("3 slides
parecidos", "e segue assim"): cada slide/bloco entra por extenso, com o texto real. É aqui que
o usuário lê o contexto inteiro pra recriar na mão depois.

```markdown
## Conteúdo na íntegra
**Slide 1:** <texto completo do slide, traduzido, sem cortar>
**Slide 2:** <...>
(um por um, até o último — nada de resumir bloco de slides)
```

### 2. Dissecação
A estrutura decomposta (Gancho / Desenvolvimento / CTA), pra enxergar a engenharia por cima do
conteúdo cru acima.

```markdown
## Gancho
<o gancho, do jeito que está no original>

## Desenvolvimento
**1.** <frase / slide / parágrafo>
**2.** <...>

## CTA
<a CTA — "Nenhuma" se não houver>
```

### 3. V0 — Esqueleto
(o esqueleto com `[lacunas]`, gerado no Passo 6)

No modo **"Sem fala"**, o bloco 1 vira o passo a passo do que acontece na tela, e o bloco 2 usa
`## O que acontece` + `## Gancho visual`.

### Passo 6 — As 3 versões

Aqui mora o valor da skill. Toda referência gera três saídas.

> **Mesma rede, mesmo formato (padrão).** A peça adaptada nasce na MESMA rede e MESMO formato do
> original: carrossel vira carrossel, vídeo do YouTube vira vídeo do YouTube, newsletter vira
> newsletter. Só cruza pra outro formato/rede **se o usuário pedir**. Por isso o card em Ideias
> nasce com uma rede só (a do original); multi-rede é escolha explícita dele, não default.

> **Se o Passo 4 classificou o formato como MOTOR, ele atravessa pra V1 e V2**, e o card em Ideias
> diz isso na primeira linha do corpo (ex.: *"Formato é motor: manter estilo print de tweet. Peça
> diagramada na identidade perde o efeito de registro."*). A identidade visual do usuário não
> proíbe emprestar gênero — ela trava paleta, fonte e símbolo, não a forma da peça.
>
> **Duas ressalvas honestas, pra não virar regra cega:**
> - **A tese da peça adaptada pode ser outra.** Formato cru sustenta "é fácil de produzir"; ele
>   contradiz "eu entrego trabalho bem-acabado". Se a tese virou de lado, o formato não atravessa,
>   e vale dizer isso ao usuário em vez de decidir sozinho.
> - **Se a raiz tiver arquivo de composição** (`marca/composicao.md` ou equivalente), a decisão de
>   gênero mora lá. Ler antes de escolher.

#### V0 — Esqueleto (vai no corpo da página do Banco)

A peça **inteira** com `[lacunas]` — não só o gancho. Engenharia reversa: trocar tudo que é concreto
do nicho por `[colchetes]`, **preservando ordem, ritmo e pontuação**.

**Regra dura — um item por slide/beat, nunca agrupar.** Se o original tem 8 slides, o esqueleto tem
8 itens numerados, um pra cada. Proibido escrever "slides 5 a 7, um por camada, mesma estrutura nos
três" e mostrar o molde uma vez só: cada slide sai escrito por inteiro, com as lacunas dele. O mesmo
vale pra beat de vídeo, parágrafo de newsletter e bloco de post. Repetição não é redundância aqui —
o esqueleto é pra preencher, não pra ler.

**Teste do esqueleto:** troca o assunto e ainda funciona? Se não, você marcou lacuna demais (virou
molde genérico) ou de menos (ainda está preso ao tema).

```markdown
## V0 — Esqueleto

**Gancho (slide 1):** "<gancho com [lacunas]>"

**Desenvolvimento:**
**1.** (slide 2) "<frase com [lacunas]>"
**2.** (slide 3) "<frase com [lacunas]>"
**3.** (slide 4) "<...>"
(um item por slide/beat até o último — nada de "slides X a Y")

**CTA:** "<CTA com [lacunas]>"
```

O esqueleto fica no Banco pra sempre. É o ativo — as peças são descartáveis.

#### V1 — Clone fiel (vira card em Ideias, `Versão: Clone fiel`)

Espelha o original **INTEIRO, não só o gancho**. Preenche o esqueleto completo (gancho **+
desenvolvimento + CTA**) card a card, beat a beat, **na mesma ordem, mesma quantidade de blocos e
mesmo ritmo do original** — trocando só o miolo pelo contexto do usuário. É o mesmo raciocínio que
se aplicou ao hook, agora aplicado à peça toda: o meio do V1 é o esqueleto do original preenchido,
não uma estrutura nova.

**Nada novo é inventado** — é a mesma peça, outro assunto. É a versão do "feio e no ar".

**Onde o original usa número/prova que o usuário não tem** (ex: prints de views), adaptar pra honesto
(documentando, case real), **nunca inventar métrica**. Essa é a única licença; o resto é espelho fiel.

#### V2 — Recombinado (vira card em Ideias, `Versão: Recombinado`)

**Parte do V1 fiel já pronto e recombina a partir dele** — não volta ao original. Mantém a psicologia,
a ordem de tensão e os beats que o V1 herdou, mas troca o conteúdo por **autoral**: o ouro do usuário,
o caso real, o bastidor, o sistema que só ele tem. O recombinado é o V1 fiel levado adiante, não uma
peça montada do zero.

**É onde se faz o 10x.** Gancho se copia; ouro se melhora.

> **Tema fora do nicho:** se a referência for de outro mercado, mantenha estrutura, gancho e
> condução, e **troque o tema** pelo cenário do usuário. Referência de fora do nicho é boa — fura a
> bolha. Só não replicar o assunto literalmente.

**Regra dura, vale pras três:** nunca inventar vivência, número ou case que o usuário não tem. Ouro
real vem do repertório dele (diário, clientes, experiência) ou de pesquisa marcada como externa.

**Modo "Sem fala":** gera só V0 e V1 — um conceito visual adaptado. Não inventar fala que o vídeo
não tinha.

#### Formato do roteiro (corpo do card em Ideias)

```markdown
## Gancho
**Opção 1:** "<frase>"
**Opção 2:** "<frase>"
**Opção 3:** "<frase>"

## Desenvolvimento
**1.** "<frase>"
**2.** "<frase>"
(frase a frase até o fim)

## CTA
**Opção 1:** "<frase>"
**Opção 2:** "<frase>"

## Título / texto na tela
<headline curta>

## Legenda
<pronta pra colar>
```

### Passo 7 — Fechar

Atualizar a referência no Banco pra `Status: Virou Ideia`.

Apagar a mídia baixada do cache local.

---

## Resumo final (o único momento em que a skill fala com o usuário)

```
| Referência | Rede | Potencial | Formato | Versões | Notion |
|---|---|---|---|---|---|
```

Na coluna **Formato**, escrever `veículo` ou **`MOTOR`**. Quando for motor, dizer numa frase qual é
o formato e por que ele carrega significado. **Isso não é decoração do resumo:** é a única chance
de o usuário perceber que a peça precisa sair fora da diagramação padrão, antes de ela ser
produzida.

Depois: *"Quer que eu transforme alguma dessas em peça agora? (`/carrossel` pro visual,
`/publicar-tema` pro pacote completo)"*

---

## Princípios

1. **Gancho se copia, ouro se melhora, CTA se replica.** O 10x mora no ouro, nunca em desfigurar o
   gancho que já provou que funciona.
2. **A psicologia é a unidade, não o tema.** Copiar a estrutura sem entender o mecanismo é cargo cult.
3. **Automático > deliberado.** Processa tudo, filtra depois. Pergunta antes de produzir é fricção,
   e fricção é o que faz não publicar.
4. **O esqueleto é o ativo; a peça é descartável.** Por isso a V0 fica no banco.
5. **Nada de vivência inventada.** O ouro é do usuário ou é pesquisa marcada como tal.
6. **A curadoria é humana.** A skill executa e organiza; o critério, o peso e o momento são do usuário.
