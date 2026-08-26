# Templates — o mapeamento bloco → slide

## O que é um "bloco"

Um bloco é **um campo de texto de um slide** — não é um slide, e não é um parágrafo solto.
`texto 1 -`, `texto 2 -`, `texto 3 -` são slots numerados que se distribuem pelos 10 slides:
um slide costuma consumir 1 a 3 blocos (título, corpo, fecho).

Essa numeração nasceu de esteiras que **injetam o texto automaticamente numa arte já montada** —
cada bloco cai numa camada de texto correspondente. É por isso que a saída em blocos ignora
completamente imagem, cor e layout: nessas esteiras a arte não vem do texto, vem do arquivo.

**Aqui a arte vem junto.** Como o render é HTML próprio (ver `visual.md`), esta skill assume as
duas camadas. A numeração em blocos continua sendo gerada e salva em `blocos.md` por dois motivos:
ela força a contagem certa de conteúdo por slide, e mantém aberta a rota de jogar o texto numa
esteira de montagem externa se um dia for útil.

> **Os mapeamentos abaixo são reconstruídos** por engenharia reversa de peças publicadas, não
> copiados de um arquivo de origem. Ajustar conforme peças novas forem dissecadas — e registrar o
> ajuste em `lacunas.md`.

---

## Template 1 — PRINCIPAL (18 blocos / 10 slides)

O padrão. Argumento com prova intercalada. É o que o funil de consciência do `SKILL.md` descreve
slide a slide.

**A regra que organiza tudo: cada slide leva um bloco de TÍTULO e um bloco de APOIO.** É a célula
binária descrita em `visual.md`. A capa é a exceção — leva a linha de contexto e o título.

| Bloco | Slide | Papel | Zona |
|---|---|---|---|
| texto 1 | 1 | linha curta de contexto (provocação ou promessa de método) | 1 |
| texto 2 | 1 | **a headline** — a massa da capa | 1 |
| texto 3 | 2 | título: a crença comum, entre aspas | 2 |
| texto 4 | 2 | apoio: admite o senso comum, abre a dúvida e crava a âncora que derruba | 2 |
| texto 5 | 3 | título: o loop — o que ainda falta explicar | 2 |
| texto 6 | 3 | apoio: de onde vem a informação (a fonte, o dado, a autoridade) | 2 |
| texto 7 | 4 | título: nomeação — "estou falando de X" | 3 |
| texto 8 | 4 | apoio: as exclusões ✗ ✗ e a definição ✓ | 3 |
| texto 9 | 5 | título: de onde a coisa tira matéria-prima | 3 |
| texto 10 | 5 | apoio: a lista das fontes + a pergunta que o mecanismo responde | 3 |
| texto 11 | 6 | título: **o mecanismo nomeado e numerado** — fundo de acento chapado | 3 |
| texto 12 | 6 | apoio: o que se ganha ao combinar as partes | 3 |
| texto 13 | 7 | título: o erro da maioria | 4 |
| texto 14 | 7 | apoio: a reatribuição da causa ("o problema nem sempre é...") + contraexemplo | 4 |
| texto 15 | 8 | título: **o slide que vale salvar** — checklist, lista numerada ou exemplos lado a lado | 4 |
| texto 16 | 8 | apoio: a frase-remate que fecha o argumento | 4 |
| texto 17 | 9 | a prova empilhada + o mérito atribuído ao método | 5 |
| texto 18 | 10 | o parágrafo-ponte + o CTA | 5 |

**Alternância de densidade:** bloco de título é curto; bloco de apoio é denso. Nunca dois slides
densos seguidos — o leitor abandona. E os slides 7 e 8 concentram o que a peça tem de mais
"printável": se nenhum dos dois justifica um print, a peça não vai ser salva.

---

## Template 2 — COMPACTO (14 blocos / 10 slides)

Mais rápido de ler. Para assunto que se resolve sem tanta construção, ou quando as âncoras são
poucas mas fortes. Perde a etapa de exclusão e comprime a nomeação.

| Bloco | Slide | Papel |
|---|---|---|
| texto 1–2 | 1 | headline (captura + ancoragem) |
| texto 3–4 | 2 | crença comum + a âncora que derruba |
| texto 5 | 3 | nomeação direta |
| texto 6 | 4 | de onde a coisa vem |
| texto 7 | 5 | por que funciona |
| texto 8–9 | 6 | o erro da maioria + reatribuição da causa |
| texto 10 | 7 | o mecanismo nomeado — fundo de acento |
| texto 11 | 8 | o efeito composto |
| texto 12 | 9 | a prova |
| texto 13–14 | 10 | direção + CTA |

---

## Template 3 — AUTORAL (18 blocos / 10 slides)

Progressão narrativa contínua, em 1ª pessoa. O fenômeno é contado **através de uma experiência
própria** — o que aconteceu, o que se tentou, o que quebrou, o que se aprendeu.

Diferenças em relação ao Principal:

- A âncora principal é a própria operação de quem publica, não fonte externa.
- A crença derrubada é uma crença **que o autor tinha** ("eu também achava que...").
- A 2ª pessoa entra mais tarde (só na Zona 4), porque a Zona 3 é o espelho da história.
- Não há slide de exclusão ✗✗✓; no lugar entra o momento de virada.

| Bloco | Slide | Papel |
|---|---|---|
| texto 1–2 | 1 | headline |
| texto 3–4 | 2 | a situação de partida, datada |
| texto 5–6 | 3 | o que se acreditava, e por quê |
| texto 7–8 | 4 | o que se fez com base nisso |
| texto 9–10 | 5 | o que quebrou — com o número real |
| texto 11–12 | 6 | a virada: o que foi percebido |
| texto 13 | 7 | o mecanismo que saiu daí — fundo de acento |
| texto 14–15 | 8 | o que mudou depois, medido |
| texto 16 | 9 | o que isso significa pra quem lê |
| texto 17–18 | 10 | direção + CTA |

**Cuidado:** peça autoral não pode virar narração de processo em aberto. Conta o que já aconteceu
e já foi resolvido. Se o `CLAUDE.md` da raiz tiver regra de conteúdo sobre isso, ela manda.

---

## Template 4 — FRAGMENTADO (21 blocos / 10–11 slides)

Fala picada em cartões curtos, cada bloco quase autossuficiente. Bom pra assunto polêmico e pra
leitura rápida. **Casa com `/post-twitter`**: se o acabamento for print de tweet, gerar os blocos
aqui e passar pra lá.

- 2 blocos na capa, 2 blocos por slide de miolo, 1–3 no fecho.
- Cada bloco é uma frase inteira que se sustenta sozinha. Nada de frase cortada em dois blocos.
- A continuidade lógica é obrigatória mesmo com a fragmentação: bloco N+1 responde ou contraria
  o bloco N.
- O funil de consciência continua valendo — só muda o tamanho da respiração.

---

## Checklist antes de fechar os blocos

- [ ] Contagem exata do template escolhido (18 / 14 / 18 / 21)
- [ ] Nomenclatura `texto N -` correta e sequencial
- [ ] Cada bloco cabe no slide sem truncar. **Se estourar, comprimir — nunca cortar no meio**
- [ ] Nenhum bloco inventou fato que não está na espinha dorsal
- [ ] A capa não entrega o nicho (teste do funil)
- [ ] O slide 9 deixa claro o que quem publica resolve (teste do funil)
- [ ] A 2ª pessoa aparece só a partir da Zona 3
- [ ] Nenhum bloco comenta a própria estrutura
- [ ] Salvo em `blocos.md`, copiável
