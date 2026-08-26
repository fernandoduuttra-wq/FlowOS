---
name: novo-projeto
description: >
  Cria uma pasta de projeto nova com arquivo de instruções dedicado, depois de uma entrevista curta sobre
  o projeto (cliente, objetivo, entregas previstas). Use quando o usuário disser "novo projeto",
  "novo cliente", "/novo-projeto", "começar projeto pra X" ou pedir pra estruturar um trabalho novo.
  Use TAMBÉM quando ele pedir a primeira entrega de um cliente/projeto que ainda não tem pasta —
  mesmo sem falar "novo projeto" (ex: "faz o diagnóstico da X", "monta a proposta pro Y", ou mandando
  áudio/transcrição/prints de alguém novo). Nesse caso, rodar esta skill ANTES da entrega.
---

# /novo-projeto — Pasta de projeto novo com contexto dedicado

Quando o usuário começa um projeto novo (cliente, iniciativa, produto), cria uma pasta com arquivo de instruções próprio que herda contexto da raiz e adiciona o que é específico do projeto.

## Reconhecer o pedido (gatilho implícito)

Na prática o usuário raramente anuncia "projeto novo". Ele já chega pedindo **o trabalho** — ou
simplesmente despeja a **matéria-prima**:

- "faz o diagnóstico da <empresa>"
- "monta a proposta pro <nome>"
- "o <nome> me mandou uns áudios" (+ transcrição, prints, link do perfil, gravação de reunião)

Antes de executar, verificar se o nome citado **já tem pasta**. Se **não tem**, é projeto novo:
rodar esta skill primeiro e só depois fazer a entrega pedida.

Não perguntar "quer que eu rode a skill?" — rodar, avisando em uma linha:
*"Esse é projeto novo, vou abrir a pasta antes de fazer o diagnóstico."*

**Nunca criar pasta de projeto como efeito colateral de salvar um arquivo.** Se o primeiro artefato
de um projeto nasce solto, ele nasce sem contexto — e o arquivo de instruções nunca mais aparece.

## Workflow

### Passo 1 — Entrevista (4 perguntas)

1. "Qual o nome do projeto ou cliente?"
2. "É um cliente novo, projeto interno ou iniciativa pessoal?"
3. "Qual o objetivo principal? (uma frase)"
4. "Que tipo de entrega vai ter? (ex: ads, site, conteúdo, automação, proposta — pode ser mais de uma)"

**Se a matéria-prima já veio junto** (transcrição de áudio, gravação de reunião, prints, conversa
colada), não interrogar: **extrair as respostas de lá e confirmar em bloco**. Perguntar só o que o
material não responde.

> "Do áudio eu tirei: cliente **X**, objetivo **Y**, entregas **A e B**. Confirma? Só me falta saber Z."

Material bruto é insumo, não resposta pronta: usar as palavras do próprio cliente e **não preencher
buraco com suposição**. O que não estiver no material vira pergunta ou vira pendência no briefing.

### Passo 2 — Decidir local

Baseado na resposta 2:

**Antes de escolher a pasta, checar uma coisa: já fechou ou ainda está sendo conquistado?** É a
divisão que mais importa, porque o trabalho é de natureza diferente (conquistar x entregar) e
misturar os dois numa pasta só embaralha o pipeline.

- **Prospect** (ainda não fechou): criar na esteira de prospecção/comercial do workspace
- **Cliente fechado:** criar em `clientes/<Nome>/`
- **Projeto interno:** criar em `projetos/<nome>/` (criar `projetos/` se não existir)
- **Iniciativa pessoal:** perguntar onde o usuário prefere

Quando o prospect fechar, a pasta dele **migra** pra esteira de cliente. É movimento, não cópia.

Se o `CLAUDE.md` da raiz definir uma esteira ou convenção de pastas própria do negócio, **ela manda** —
seguir o que está lá, não o padrão genérico daqui.

### Passo 3 — Estrutura básica

Criar a pasta com:

- `AGENTS.md` do projeto (instruções herdadas + específicas)
- `CLAUDE.md` com **uma linha só**: `@AGENTS.md` — é o import nativo do Claude Code
- `briefing.md` (com o que foi coletado na entrevista)
- Subpastas conforme as entregas mencionadas (ex: se mencionou "ads e conteúdo", criar `ads/` e `conteudo/`)

Quando o material bruto veio junto, o `briefing.md` guarda **matéria-prima, não análise**: o que o
cliente falou e o que foi levantado de fonte pública. Hipótese e leitura do usuário ficam pro
diagnóstico, não aqui. Terminar o briefing pelo que ainda falta descobrir — é o que vira a próxima tarefa.

### Passo 4 — Conteúdo do `AGENTS.md` do projeto

O conteúdo vive **uma vez só**, no `AGENTS.md` — que é o nome que Codex e outros agentes leem.
O `CLAUDE.md` ao lado é só o ponteiro (`@AGENTS.md`); nunca copiar as instruções pra dentro dele,
senão as duas versões divergem. Se o `CLAUDE.md`/`AGENTS.md` da raiz não usar esse par, seguir a
convenção que a raiz usa.

Template:

```markdown
# [Nome do projeto]

> Projeto criado em [data]. Pasta dedicada — instruções aqui sobrescrevem as da raiz quando relevantes.

## Sobre

[Objetivo da resposta 3]

## Tipo

[Cliente novo / Projeto interno / Iniciativa pessoal]

## Entregas previstas

- [entrega 1 da resposta 4]
- [entrega 2 da resposta 4]
- ...

## Como falar com esse cliente

[O que ele valoriza, o nível de familiaridade com o assunto, o que não funciona com ele.
Preencher quando aparecer — é o que evita entregar no tom errado.]

## Onde salvar o que

- Briefings e contexto: nessa pasta na raiz
- Entregas: cada subpasta criada (ads/, conteudo/, site/, etc.)

## Contexto que herda da raiz

Esse projeto herda automaticamente o tom de voz, marca e contexto do negócio definidos em `_contexto/` e `marca/` da raiz. Não duplicar essas informações aqui.

## Específico desse projeto

[Vazio — preencher com regras que valem só pra esse projeto, conforme for descobrindo]
```

### Passo 5 — Resumo

Responder pro usuário:

```
Pasta criada: [caminho]
✓ AGENTS.md do projeto (+ CLAUDE.md apontando pra ele)
✓ briefing.md
✓ Subpastas: [lista]

Quando for trabalhar nesse projeto, abre o terminal já dentro da pasta — assim eu carrego as instruções específicas junto com as da raiz.
```

## Regras

- Nome de pasta: usar o nome como o usuário falou, sem normalizar agressivamente (manter acentos, espaços viram hífen, mas o nome reconhecível)
- Não criar subpastas que não foram pedidas ("pra organizar melhor"). Só o que foi mencionado nas entregas
- Se o cliente/projeto já existe (pasta com mesmo nome), avisar e perguntar se é pra adicionar dentro ou criar com sufixo
