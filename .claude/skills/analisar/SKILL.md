---
name: analisar
description: >
  Analisa qualquer coisa (problema, decisão, mercado, conteúdo, processo) escolhendo
  a lente de análise certa — Relação, Fluxo, Ciclo, Hierarquia ou Ecossistema — e
  expõe o raciocínio de forma estruturada e visual. O objetivo é decidir/agir melhor
  e treinar o olho analítico, não só entregar a resposta pronta.
  Use quando o usuário disser "analisa isso", "como eu analiso X", "me ajuda a pensar
  sobre Y", "estrutura essa ideia", "/analisar", ou pedir pra destrinchar um tema antes
  de decidir.
---

# /analisar — Analisar qualquer coisa

Skill pra destrinchar qualquer assunto com método. A graça não é dar uma resposta
pronta — é **escolher a lente certa, dizer por que escolheu, e mostrar o raciocínio
estruturado**, pra o usuário treinar a própria habilidade de análise.

## Dependências

- **Contexto do negócio:** `_contexto/empresa.md`, `_contexto/estrategia.md` (se o objeto da análise for do negócio do usuário).
- **Tom de voz:** `_contexto/preferencias.md`.

---

## As 5 lentes de análise

Toda análise começa escolhendo **a lente que combina com a intenção**. Cada lente
responde a uma pergunta diferente e usa modelos próprios (todos de domínio público):

| Lente | Verbo | Pergunta-chave | Modelos |
|---|---|---|---|
| **1. Relação** | comparar | "O que isso tem a ver com aquilo? Onde cruzam? Qual é melhor?" | comparação direta (A vs B), Diagrama de Venn, Matriz BCG |
| **2. Fluxo** | sequenciar | "Qual a ordem? Onde trava? O que vem antes/depois?" | início/meio/fim, processo, linha do tempo, roadmap, jornada do usuário, mapa mental |
| **3. Ciclo** | melhorar | "O que se repete? Como melhoro a cada volta?" | PDCA (melhoria contínua), sprints, ciclo de hábitos |
| **4. Hierarquia** | priorizar | "O que vem primeiro? O que é base e o que é topo?" | pirâmide (Maslow), Golden Circle (cebola), estrutura modular, árvore de stakeholders |
| **5. Ecossistema** | conectar | "Quem se conecta com quem? Como o sistema todo se sustenta?" | mapa de negócio, ecossistema de mercado, mapa de stakeholders |

Princípio que rege a skill: **você precisa saber como analisar antes de agir.**

---

## Workflow

### Passo 1 — Entender o objeto e o "pra quê"
Identificar o que vai ser analisado e **por quê**. O "pra quê" é o que define a lente.
Se não estiver claro, perguntar:
- "O que exatamente você quer analisar?"
- "Pra quê? (decidir entre opções / melhorar um processo / entender um mercado / priorizar / criar conteúdo)"

### Passo 2 — Escolher a(s) lente(s) e justificar
Casar a intenção com a tabela das 5 lentes. Pode combinar mais de uma quando fizer
sentido (ex: Relação pra comparar + Hierarquia pra ordenar).
**Sempre dizer qual lente escolheu e por que** — e, quando útil, por que descartou as outras.
Isso é o que treina o olho do usuário.

### Passo 3 — Aplicar e expor
Rodar a análise pelo modelo escolhido:
- Quebrar o objeto pelos elementos da lente (ex: Hierarquia → o que é base, o que é topo).
- Apontar o **insight não óbvio** que a lente revela.
- Fechar com a **implicação prática** ("e daí, o que fazer com isso").

### Passo 4 — Output visual
Entregar de forma estruturada: tabelas, listas hierárquicas e diagramas em ASCII/markdown
direto no chat. Nomear sempre a lente usada.

> Camada visual rica (diagramas/mapas estilizados) ainda não está nesta skill. Quando
> houver material visual de referência fornecido pelo usuário, evoluir este passo. Até lá,
> não inventar um estilo visual proprietário.

---

## Regras

- **Sempre nomear a lente e justificar** — o objetivo é o usuário aprender a analisar, não só receber a resposta.
- Pode combinar lentes, mas explicitar quais e por quê.
- Tom conforme `_contexto/preferencias.md`: direto, reflexivo, sem jargão de guru.
- Se analisar algo do negócio, ancorar em `_contexto/empresa.md` e `estrategia.md` — não inventar dados nem vivências.
