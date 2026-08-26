# FlowOS

O sistema operacional do seu negócio dentro da IA.

O FlowOS guarda o contexto do negócio, organiza arquivos, transforma processos repetidos em skills e melhora conforme o trabalho real acontece. Você continua decidindo. O sistema ajuda a lembrar, organizar e executar.

Ele funciona com agentes que leem `AGENTS.md`, incluindo Codex e outros agentes compatíveis. No Claude Code, o arquivo `CLAUDE.md` aponta para a mesma fonte de instruções.

## Antes de instalar

Você precisa de:

1. VS Code instalado;
2. Git instalado;
3. uma conta no GitHub;
4. Claude Code, Codex ou outro agente compatível funcionando dentro do VS Code.

O curso mostra cada instalação desde o zero.

## Crie sua cópia

A rota recomendada é criar um repositório seu a partir deste template:

1. Abra `https://github.com/fernandoduuttra-wq/FlowOS`.
2. Clique em **Use this template**.
3. Escolha **Create a new repository**.
4. Dê ao repositório o nome do seu negócio e mantenha-o privado.
5. Copie o link do repositório criado.

Assim, seu contexto e os arquivos do negócio ficam no seu próprio repositório desde o primeiro dia.

## Instale com o agente

Abra Claude Code, Codex ou o agente escolhido e envie:

```text
Clone o repositório <COLE_AQUI_O_LINK_DO_SEU_REPOSITORIO>, abra a pasta clonada, leia o AGENTS.md e siga a skill em .claude/skills/instalar/SKILL.md para configurar meu FlowOS. Faça a entrevista uma pergunta por vez e conclua a instalação antes de iniciar qualquer outra tarefa.
```

O agente vai:

1. clonar e abrir a pasta;
2. identificar seu perfil de operação;
3. entrevistar você sobre negócio, escrita, foco e marca;
4. preencher os arquivos de contexto;
5. adaptar o `AGENTS.md`;
6. criar somente as pastas que combinam com seu negócio;
7. deixar as skills visíveis para os agentes compatíveis.

## Depois da entrevista

O FlowOS passa a usar:

- `_contexto/`: quem é o negócio, como escreve e o que está em foco;
- `AGENTS.md`: regras de operação do workspace;
- `.claude/skills/`: processos reutilizáveis;
- `marca/`: identidade visual quando ela for definida;
- `dados/`: arquivos de entrada;
- `marketing/` e `saidas/`: trabalho produzido pelo sistema.

Quando uma rotina se repetir, peça para o FlowOS mapeá-la e transformá-la em skill. O sistema cresce com o que você realmente faz.

Para experimentar uma skill sem configurar nenhuma integração, envie uma referência de conteúdo e peça para usar a `Content Skill`. Ela faz de uma a três perguntas e constrói a adaptação com você dentro do chat.

## Segurança

Mantenha o repositório privado. Nunca salve senhas, tokens ou chaves de API em arquivos versionados. O `.gitignore` já protege os formatos mais comuns, mas a decisão final continua sendo sua.
