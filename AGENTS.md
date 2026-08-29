# FlowOS

> Esta é uma instalação nova. O contexto ainda precisa ser configurado para o negócio do usuário.

## Primeira execução

Se os arquivos em `_contexto/` ainda estiverem marcados como não configurados, use a skill `instalar` antes de qualquer outro trabalho. Conduza a entrevista uma pergunta por vez e conclua o setup.

## Uma fonte de verdade

- As instruções vivem em `AGENTS.md`.
- `CLAUDE.md` contém somente `@AGENTS.md` para o Claude Code ler a mesma fonte.
- As skills vivem em `.claude/skills/`.
- Quando o ambiente usar `.agents/skills`, crie um atalho para `.claude/skills/`. Nunca mantenha duas cópias.

## Contexto do negócio

Depois da instalação, leia no início de cada trabalho:

1. `_contexto/empresa.md`;
2. `_contexto/preferencias.md`;
3. `_contexto/estrategia.md`.

Para tarefas visuais, use `marca/design.json` como fonte de cores, fontes, formas e espaçamento. Se o arquivo ainda não existir, ajude o usuário a definir a identidade antes de produzir a peça final.

## Como trabalhar

- Antes de executar, procure uma skill relevante em `.claude/skills/`.
- Use contexto real. Não invente clientes, resultados, números ou preferências.
- Crie estrutura somente quando o trabalho pedir. O workspace cresce a partir do uso.
- Preserve mudanças existentes e confirme antes de qualquer ação destrutiva ou publicação externa.
- Nunca versione senhas, tokens, credenciais ou dados sensíveis.

## Aprender com o uso

Quando o usuário der uma correção durável, pergunte se deve salvar no contexto. Quando uma rotina se repetir, proponha transformá-la em skill. O FlowOS melhora com correções e trabalho real, não com pastas criadas por antecipação.

