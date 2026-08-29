---
name: abrir
description: >
  Abre uma sessão de trabalho carregando o contexto do negócio (empresa, preferências e estratégia)
  e devolve um resumo curto pro usuário. Use quando o usuário disser "abrir",
  "começar o dia", "/abrir" ou no primeiro turno de uma sessão depois do /instalar.
---

# /abrir — Abertura de sessão

Curto e direto. O objetivo é carregar contexto e devolver uma síntese de uma frase pra o usuário começar a trabalhar.

## Workflow

1. Ler, em ordem:
   - `_contexto/empresa.md`
   - `_contexto/preferencias.md`
   - `_contexto/estrategia.md`
   - `marca/design.json` (somente para saber se a identidade visual já existe)

2. Se empresa, preferências ou estratégia estiverem com `Status: não configurado`, responder:
   > "O FlowOS ainda não foi configurado para este negócio. Vou iniciar a skill `instalar`."
   E parar.

3. Se tudo estiver preenchido, devolver UMA mensagem curta no formato:

```
[Nome do negócio] — [o que faz em 5-8 palavras]
Foco atual: [prioridade da estratégia, em uma frase]
Tom: [resumo de 3-4 palavras do tom de voz]

Pronto. O que vamos fazer?
```

4. Não listar quais arquivos foram lidos. Não confirmar leitura. Só usar o contexto.

## Regras

- Resposta tem que caber em 5 linhas no terminal
- Não fazer perguntas além de "o que vamos fazer?"
- Se `marca/design.json` não existir, não mencionar. Isso só vira pendência quando uma tarefa visual for chamada
