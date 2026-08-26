---
name: instalar
description: Instala o FlowOS no negócio do usuário. Entrevista, preenche o contexto, adapta o AGENTS.md e cria somente a estrutura necessária. Use no primeiro setup do repositório.
---

# Instalar o FlowOS

Conduza a primeira configuração do sistema. O objetivo é terminar com o workspace reconhecendo o negócio, a escrita, a prioridade atual e o perfil de operação do usuário.

Faça uma pergunta por vez. A conversa inteira deve levar de cinco a dez minutos. Não execute outro trabalho antes de concluir o setup.

## 1. Pré-checagem e cópia particular

1. Confirme que a pasta atual contém `AGENTS.md`, `_contexto/` e `.claude/skills/`.
2. Leia `AGENTS.md` e confira se os arquivos de `_contexto/` estão marcados como `não configurado`.
3. Identifique o sistema operacional e o agente em uso. Não instale ferramentas que este setup não precisa.
4. Se o contexto já estiver preenchido, pergunte se o usuário quer complementar ou reinstalar. Nunca sobrescreva contexto real sem confirmação.
5. Antes de alterar qualquer arquivo, execute `git remote -v` e identifique o usuário autenticado com `gh api user --jq .login`.
6. O `origin` precisa pertencer ao usuário autenticado. Se ainda apontar para o repositório de distribuição do FlowOS ou para outra conta:
   - nunca faça push nesse remoto;
   - confirme o nome desejado para a cópia particular, caso o usuário ainda não tenha informado;
   - renomeie o remoto atual para `upstream`;
   - crie um repositório privado na conta autenticada usando a cópia local;
   - configure o novo repositório como `origin` e envie o estado inicial;
   - confira novamente com `git remote -v`.
7. A operação equivalente, adaptando o nome, é:

```text
git remote rename origin upstream
gh repo create <nome-do-repositorio> --private --source=. --remote=origin --push
```

8. Só continue a entrevista depois de confirmar:

```text
origin    = repositório privado do usuário
upstream  = repositório de distribuição do FlowOS
```

Se o GitHub CLI não estiver autenticado ou a criação falhar, preserve os arquivos locais, explique a correção necessária e não faça push em `upstream`.

## 2. Perfil de operação

Pergunte qual perfil mais se aproxima da realidade atual:

1. criador ou marca pessoal;
2. freelancer ou prestador de serviço;
3. agência ou consultoria;
4. empresa com setores;
5. projeto pessoal sem operação comercial.

Use o template correspondente em `templates/perfis/` quando existir. Para projeto pessoal, adapte o template mais simples sem criar estrutura comercial.

## 3. Entrevista

Pergunte em ordem, uma pergunta por mensagem:

1. Como você chama seu negócio, projeto ou marca?
2. O que você entrega, em uma frase do jeito que explicaria para alguém de fora da sua área?
3. Quem compra, contrata ou usa o que você faz?
4. Você trabalha sozinho ou com outras pessoas? Quem faz o quê?
5. Cole um texto real e recente escrito por você.
6. Que tipo de escrita ou comportamento da IA você quer evitar?
7. Qual é o principal gargalo ou prioridade do negócio agora?
8. Que tarefa ou decisão você repete com frequência e gostaria de tirar das costas?
9. Como você prefere receber o trabalho: direto ou detalhado, pronto ou por etapas, com ou sem aprovação antes de editar?
10. Sua identidade visual já existe? Se sim, quais arquivos, cores e fontes você possui?

Se uma resposta já contiver a seguinte, não repita a pergunta. Não invente o que não foi informado.

## 4. Preencher o contexto

Atualize:

- `_contexto/empresa.md`: nome, atividade, público, entregas e equipe;
- `_contexto/escrita.md`: padrões extraídos do texto real, vocabulário e o que evitar;
- `_contexto/preferencias.md`: formato de entrega, aprovações e modo de trabalho;
- `_contexto/estrategia.md`: gargalo, prioridade atual e rotina candidata a skill;
- `_contexto/posicionamento.md`: somente um resumo factual do público, problema e oferta, quando houver informação suficiente. Se faltar, mantenha a pendência e indique a skill `diagnostico`.

Remova o marcador `não configurado` dos arquivos efetivamente preenchidos.

Se houver informação visual, salve a matéria-prima em `marca/briefing.md`. Não invente `design.json`. Quando a identidade precisar ser construída ou organizada, indique a skill `identidade`.

## 5. Adaptar o AGENTS.md

Leia o template do perfil escolhido em `templates/perfis/`. Use-o como matéria-prima para adicionar ao `AGENTS.md`:

- o que é o workspace;
- quem é o usuário ou negócio;
- o que produz e entrega;
- como trabalha;
- regras de organização específicas;
- ferramentas já conectadas.

Preserve do `AGENTS.md` inicial as seções `Uma fonte de verdade`, `Contexto do negócio`, `Como trabalhar` e `Aprender com o uso`. Remova apenas o aviso de instalação nova.

Mantenha `CLAUDE.md` com uma única linha:

```text
@AGENTS.md
```

## 6. Criar somente a estrutura necessária

Crie pastas de acordo com o perfil e as respostas, sem antecipar uma empresa que ainda não existe:

- marca pessoal: pastas de conteúdo ou produtos somente se fizerem parte da operação atual;
- freelancer: `clientes/` e `propostas/` quando houver esse fluxo;
- agência: `clientes/`, `propostas/` e outras frentes citadas;
- empresa: somente os setores reais informados;
- projeto pessoal: nenhuma pasta comercial por padrão.

`marketing/`, `dados/`, `saidas/`, `scripts/` e `templates/` já fazem parte do núcleo.

## 7. Compatibilidade entre agentes

A pasta de verdade das skills é `.claude/skills/`. Se `.agents/skills` ainda não existir, crie um atalho local:

- Windows: junction `.agents\skills` apontando para `.claude\skills`;
- macOS ou Linux: symlink `.agents/skills` apontando para `../.claude/skills`.

Confirme que `.agents/skills` permanece no `.gitignore`. Não copie as skills para uma segunda pasta.

## 8. Git e encerramento

Confira os remotos com `git remote -v`.

- `origin` deve pertencer ao usuário e receber os salvamentos do FlowOS.
- `upstream`, quando existir, é somente leitura. Nunca enviar contexto ou commits para ele.
- Se `origin` ainda apontar para o repositório de distribuição, não conclua o setup até criar a cópia particular.

Encerre mostrando:

```text
✓ Perfil aplicado
✓ Contexto do negócio
✓ Escrita e preferências
✓ Prioridade atual
✓ AGENTS.md adaptado
✓ Estrutura criada para este perfil
✓ Skills visíveis para o agente em uso
```

Nomeie a rotina citada na pergunta 8 como primeira candidata a virar skill. O sistema deve crescer a partir dessa rotina, não de exemplos genéricos.
