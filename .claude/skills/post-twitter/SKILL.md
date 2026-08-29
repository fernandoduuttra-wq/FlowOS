---
name: post-twitter
description: >
  Produz a peça visual no formato print de tweet (Twitter/X) — carrossel 1080x1350 pro Instagram
  ou card avulso — em versão clara ou escura, com header de perfil (avatar, nome, selo, @).
  O texto vem de uma referência analisada, de um registro do banco no Notion ou de um modelo já
  validado — e, se o usuário preferir, a própria skill escreve a partir de um tema. Use quando o
  usuário disser "post de twitter", "post no formato tweet", "carrossel estilo print de tweet",
  "monta em print de tweet", ou /post-twitter.
---

# /post-twitter — a peça no formato print de tweet

O formato **é** o argumento. Print de tweet lê como **registro** de algo que aconteceu, não como
peça produzida pra convencer. É por isso que ele não usa a identidade visual da marca: diagramar
esse texto no padrão da marca joga fora exatamente o que faz o formato funcionar.

> **Consequência prática:** esta skill **não lê o `marca/design.json`.** É a única peça do sistema
> onde isso é correto. Cor, fonte e mobiliário aqui imitam a plataforma, não a marca. Se a lista
> `nunca` da marca proibir algo que a plataforma usa (fonte de sistema, por exemplo), **a
> plataforma manda** — senão o print deixa de parecer print.

---

## De onde vem o texto — perguntar sempre

**Nunca assumir a origem.** Se o pedido não deixar claro, perguntar, com as opções uma embaixo da
outra:

```
De onde vem o texto?

A) Uma referência para analisar (manda o link ou o print)

B) Um registro que já existe no banco do Notion (eu escolho o que combina com o tema)

C) Um modelo de estrutura já validado pra essa rede

D) Eu escrevo, a partir de um tema ou de um texto seu pra fatiar

Qual?
```

- **A — referência:** o usuário colou um link/print. Esta própria skill identifica a estrutura,
  adapta o texto ao contexto real do usuário e apresenta o rascunho para aprovação. Se houver um
  banco de conteúdo configurado, pode registrar a versão aprovada nele.
- **B — banco do Notion:** uma Ideia de Conteúdo, ou uma referência do Banco cuja estrutura combine
  com o tema. Escolher a que **ressoa com o assunto pedido**, não a mais recente, e mostrar qual
  escolheu antes de seguir.
- **C — modelo validado:** ver "Estruturas validadas". Entra direto, sem dissecar de novo.
- **D — a skill escreve:** ver "Quando a skill escreve o texto". É a rota mais rápida e a mais fácil
  de sair genérica — por isso ela tem regra própria.

**Toda rota tem uma parada obrigatória para aprovação do texto.** Se a origem estiver no Notion, o
usuário edita lá. Nos demais casos, o checkpoint acontece no chat. Não produzir em cima de rascunho
não revisado, e não "melhorar" o texto na hora de montar.

**Nas rotas A, B e C o texto entra literal.** Copiar do Notion palavra por palavra, incluindo as
linhas que parecerem sobrando. Se algo precisar mudar, muda no Notion primeiro e puxa de novo —
senão a fonte da verdade racha.

---

## Quando a skill escreve o texto (rota D)

Duas entradas: **um tema** ("5 erros de quem começa a vender online") ou **um texto longo pra
fatiar** (transcrição, post antigo, artigo). Detectar sozinho: frase curta = tema; texto corrido =
fatiar; blocos já separados = só diagramar.

Ao fatiar texto longo: achar o **ponto de virada** (a ideia que sozinha já seria um tweet),
reescrever no formato da rede e distribuir. Não copiar o texto original literalmente — o que
funciona em artigo não funciona em tweet.

### Estrutura

**AIDA**, distribuída assim num carrossel de 10 slides:

| Slides | Papel |
|---|---|
| 1 | **Atenção** — a frase que para o scroll. Provoca, contradiz expectativa, ou nega um ritual que todo mundo cumpre |
| 2-3 | **Interesse** — o problema. O sintoma que o leitor sente e não consegue articular |
| 4-7 | **Desejo** — o miolo. Aqui mora 60% do conteúdo: o método, os princípios, a virada |
| 8-9 | **Reforço** — consolida, dá o exemplo concreto, amplifica a tese |
| 10 | **Ação** — o CTA que o autor quer |

Menos slides: comprimir mantendo a proporção (gancho 1 + problema 1 + solução 3 + CTA 1). Mais
slides: expandir Interesse e Desejo, **nunca** o gancho nem o CTA.

### Regras de copy

- **Frases curtas.** Teto de 12 palavras. Quanto mais curta, melhor
- **Uma ideia por slide**, com quebra de parágrafo entre ideias diferentes
- **Tom de tweet:** declarativo, opinativo, sem rodeio. É pensamento curto, não tutorial
- **Português falado**, não tradução de inglês nem corporativês
- **Sem emoji, sem hashtag** no corpo
- **Sem travessão (— ou –).** Vírgula, ponto ou quebra de linha. Travessão dá cara de blog post
- Se houver `_contexto/preferencias.md`, ele manda sobre estas regras gerais

### O gancho

Precisa **contradizer uma expectativa** ou **provocar**. Padrões que funcionam:

- "A maioria quer [a parte boa de X], mas evita [o que X exige]."
- "Ninguém te conta que [verdade desconfortável]."
- "[N] anos fazendo [X], e a lição mais importante foi [Z]."
- "Pare de [ação comum]. Comece a [ação contraintuitiva]."
- "[Resultado concreto] sem [o ritual que todo mundo cumpre]."

**Não usar dado, número ou vivência que não seja real.** Se o gancho precisa de um número, ele sai
do que o usuário já entregou ou já viveu — nunca de estimativa inventada pra soar melhor.

### Checkpoint

**Mostrar o texto completo, slide a slide, e esperar aprovação antes de montar o visual.** Na rota D
esse checkpoint substitui a parada no Notion. Se o post for aprovado, cadastrar o roteiro no banco
de Ideias depois — assim a rota D alimenta o banco em vez de furá-lo.

Os IDs dos databases e as convenções da operação estão no `CLAUDE.md` da raiz. Esta skill é
genérica; a raiz é que sabe o nome do perfil, o @ e onde mora a foto.

---

## Setup — ler antes de montar

Do **`CLAUDE.md` da raiz**:
- Nome de exibição, @ do perfil e caminho da foto de avatar
- IDs dos databases do Notion
- Se a raiz definir esteira própria de render ou de publicação, ela manda

Do **`_contexto/`**: `preferencias.md` (o que evitar) e `posicionamento.md`. Serve pra julgar se o
texto puxado do Notion está na voz certa — não pra reescrever.

---

## Duas versões: clara e escura

Perguntar qual, se o usuário não disser. Regra de bolso: **clara** parece print de timeline no
padrão antigo e destaca num feed escuro; **escura** é o modo mais usado hoje e some menos em feed
claro. Alternar entre os posts evita a grade repetida.

| Token | Clara | Escura |
|---|---|---|
| Fundo | `#FFFFFF` | `#000000` |
| Texto | `#0F1419` | `#E7E9EA` |
| @handle | `#536471` | `#71767B` |
| Selo verificado | `#1D9BF0` | `#1D9BF0` |
| Borda de imagem anexada | `#CFD9DE` | `#2F3336` |

**Uma peça inteira numa versão só.** Nunca misturar slide claro e escuro no mesmo carrossel: quebra
a ilusão de que é o mesmo perfil printado várias vezes.

---

## Anatomia do slide (não negociável)

```
[avatar]  Nome de Exibição ✓
          @handle
                                ← 32px de respiro, e só. Sem linha, sem régua.
Texto do tweet, 44px, parágrafos
separados por uma linha em branco.

[print anexado, opcional]
```

| Elemento | Medida |
|---|---|
| Canvas | 1080x1350 (4:5) |
| Margem lateral | 80px (texto de x=80 a x=1000) |
| Avatar | 100px, circular |
| Gap avatar → nome | 20px |
| Nome | 36px, bold |
| Selo | 32px, ao lado do nome |
| @handle | 28px, regular |
| Gap header → texto | 32px |
| Texto | 44px, line-height 1.35 |
| Entre parágrafos | 60px (uma linha em branco) |
| Imagem anexada | abaixo do texto, radius 24px, máx 920x600, hairline 1px |

**O bloco inteiro (header + texto + anexo) fica centralizado na vertical.** Não no topo. Ao
adicionar imagem, recalcular a centralização considerando ela — não empurrar o header pra cima.

**Todos os slides têm o mesmo layout.** A capa não é especial, o CTA não é especial. A
diferenciação vem do texto, nunca da diagramação. Uma fonte só na peça inteira.

### O que NÃO existe neste formato

Nada disso é enfeite ausente: é o que denuncia a peça como produzida.

- Barra de topo ou de rodapé, ícones de like/retweet/resposta, contagem de visualização
- Contador de slide (1/7), indicador de progresso, "arraste pro lado"
- Logo da marca, logo da plataforma, watermark de ferramenta
- Data ou horário do tweet
- Linha separando o header do texto (no tweet real ela não existe)
- Emoji e hashtag no corpo do texto
- Travessão (—, –). Vírgula, ponto ou quebra de linha no lugar: travessão dá cara de artigo de blog
- Bullet de caractere exótico (▫ ▪ ☐). Só `•`, ou número

Espaço vazio faz parte do desenho. Não preencher.

### Ênfase

Negrito em ênfase e palavra-chave é permitido, e é o **único** destaque: nunca cor, nunca tamanho
diferente, nunca bloco colorido. Default: **uma marcação por slide** — a frase que carrega a virada,
ou o número. Se o usuário pedir mais, atender; se não pedir, segurar a mão. Peça toda em negrito
não destaca nada.

### Prints anexados

Anexo só entra onde **ele é a prova** do que a frase afirma (a página que ficou pronta, o painel, a
conversa). Anexo decorativo em todo slide vira ruído e mata o efeito de "esse aqui tem prova".

Usar material real que já existe no repositório. **Não inventar print, não montar mockup de algo que
não aconteceu, e não usar peça de cliente sem checar o `CLAUDE.md` daquele cliente.**

---

## Avatar — o detalhe que entrega tudo

O rosto deve ocupar **75% a 80% do círculo**, com a cabeça inteira visível. É o enquadramento que
todo avatar de rede social tem; fora dessa faixa o olho estranha antes de saber por quê.

O `gerar.py` faz o recorte sozinho a partir de um retrato: mede a altura do rosto no arquivo e corta
o quadrado em `altura_do_rosto / alvo`. Precisa de **um retrato com folga em volta da cabeça**
(ombro pra cima). Foto que já vem cortada rente na coroa não tem conserto: não existe pixel pra
recuperar, e qualquer preenchimento (blur, cor chapada) aparece.

Se o único arquivo disponível for um close cortado, **falar isso e pedir o retrato**, em vez de
entregar um avatar com a cabeça raspada pela borda.

---

## Workflow

**Passo 1 — Origem do texto.** Perguntar (A/B/C/D) se não estiver claro. A → analisar a referência e
adaptar o texto. B → escolher o registro que ressoa com o tema e mostrar qual escolheu. D → escrever
seguindo "Quando a skill escreve o texto".

**Passo 2 — Aprovação do texto.** Se a fonte estiver no Notion, o usuário revisa e edita lá. Nos
demais casos, mostrar o texto slide a slide no chat. Só seguir depois do "pode produzir".

**Passo 3 — Fatiar em slides.** Usar o texto **literalmente aprovado**, venha ele do Notion ou do
chat. Um tweet por slide; quebra de parágrafo do roteiro vira parágrafo no slide.

**Passo 4 — Versão e identidade.** Clara ou escura. Nome, @ e foto vêm do `CLAUDE.md` da raiz.

**Passo 5 — Montar e renderizar.** Copiar `gerar.py` desta skill pra pasta do conteúdo, preencher o
bloco de config e a lista de slides, e rodar:

```powershell
python "marketing/conteudo/<pasta>/tweet/gerar.py"
& ".\scripts\render-carrossel.ps1" -Folder "marketing\conteudo\<pasta>\tweet" -Out "png"
```

O render sai em 1080x1350 por padrão. Não usar `-ExecutionPolicy Bypass`.

**Passo 6 — Olhar antes de entregar.** Abrir os PNGs e ler. Conferir: bloco centralizado, nada de
texto colado no anexo, avatar na faixa de 75-80%, mesma diagramação em todos os slides, nenhum item
da lista de proibições. Só depois dizer que ficou pronto.

**Passo 7 — Legenda.** Se a peça for pro Instagram, a legenda sai do mesmo registro do Notion. Não
inventar legenda nova aqui.

---

## Estruturas validadas

Quando uma estrutura de post desta rede provar que funciona (métrica real, não achismo), registrar
como modelo no banco do Notion e reusar direto — sem dissecar a referência de novo. Com o
tempo, essa vira a terceira origem de texto e a mais barata.

Registrar sempre **por que** funcionou, não só o esqueleto. Estrutura sem a psicologia por trás vira
template, e template envelhece.

---

## Saída

```
marketing/conteudo/<tipo>-<tema>-<YYYY-MM-DD>/
  tweet/
    gerar.py            ← config + slides desta peça
    slide-01.html …     ← uma página por slide
    png/
      slide-01.png …    ← 1080x1350, prontos pra postar
  assets/
    avatar-tweet.png    ← recorte gerado do retrato
```

## Regras

- Perguntar a origem do texto (A/B/C/D) em vez de assumir. Escrever a copy é a rota D, escolhida
  pelo usuário — nunca o default silencioso
- Rotas A/B/C: texto literal do Notion. Mudou? Muda lá e puxa de novo
- Rota D: AIDA + frases de até 12 palavras + gancho que contradiz expectativa, e **checkpoint de
  texto aprovado antes de montar o visual**. Nada de número ou vivência inventada
- Não ler nem aplicar o `marca/design.json` nesta peça
- Uma versão (clara **ou** escura) por peça
- Mesmo layout em todos os slides, uma fonte só
- Negrito é o único destaque, e por padrão um por slide
- Anexo só quando é prova; material real, nunca mockup inventado
- Avatar com o rosto em 75-80% e a cabeça inteira. Sem retrato adequado, pedir o retrato
- Renderizar e **olhar** antes de dizer que está pronto
