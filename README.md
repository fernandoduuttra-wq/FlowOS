# FlowOS

> O sistema operacional do seu negócio dentro da IA.

Em alguns minutos, seu negócio passa a ter memória própria, regras de trabalho e skills prontas para transformar tarefas repetidas em processos executáveis. Você continua dirigindo. O sistema lembra, organiza, executa e melhora com o uso.

O FlowOS funciona no VS Code com Claude Code, Codex e outros agentes que leem `AGENTS.md`.

## Antes de começar

Você precisa de:

1. VS Code;
2. uma conta no GitHub;
3. Claude Code, Codex ou outro agente compatível dentro do VS Code.

O agente verifica e instala Git e GitHub CLI quando forem necessários. Se o GitHub pedir autenticação no navegador, ele orienta você durante essa etapa.

## Ligando o sistema

Abra o agente em uma pasta vazia e cole:

```text
Instale meu FlowOS usando este repositório:
https://github.com/fernandoduuttra-wq/FlowOS

Antes de clonar, verifique se Git e GitHub CLI estão instalados. Se algum estiver ausente, instale a versão estável adequada ao meu sistema operacional. Depois confirme se o GitHub CLI está autenticado na minha conta. Se a autenticação exigir o navegador, me conduza por essa etapa e aguarde eu concluir.

Primeiro clone o repositório. Não faça nenhuma alteração nem push no repositório de origem.

Crie um novo repositório privado na minha conta do GitHub usando a cópia local, configure esse novo repositório como origin e mantenha fernandoduuttra-wq/FlowOS apenas como upstream.

Confirme que origin aponta para a minha conta antes de continuar. Depois leia o AGENTS.md e siga .claude/skills/instalar/SKILL.md. Faça a entrevista uma pergunta por vez e conclua a instalação antes de iniciar qualquer outro trabalho.
```

O agente vai:

1. baixar o FlowOS;
2. criar um repositório privado na sua conta;
3. separar sua cópia do repositório de origem;
4. abrir o projeto no VS Code;
5. entrevistar você sobre negócio, escrita, foco e marca;
6. preencher seu contexto;
7. adaptar o sistema ao seu perfil;
8. criar somente as pastas que sua operação precisa.

Ao conferir os remotos, o resultado deve ser:

```text
origin    → seu-usuario/seu-flowos
upstream  → fernandoduuttra-wq/FlowOS
```

O `origin` é sua cópia particular. É para lá que o FlowOS salva seu trabalho. O `upstream` é a instalação de origem e nunca recebe seu contexto ou seus commits.

## O sistema

### Núcleo

- `abrir` carrega o contexto no começo do trabalho;
- `salvar` registra e envia seu trabalho ao GitHub;
- `atualizar` mantém o contexto coerente com o workspace;
- `novo-projeto` cria uma área dedicada quando um trabalho novo começa;
- `mapear-rotinas` encontra processos repetidos que podem virar skills.

### Conteúdo e comunicação

- `carrossel` e `carrossel-tendencia` criam peças visuais;
- `copy-lp` escreve páginas de venda.

### Marketing e operação

O sistema também inclui skills para sites, SEO, anúncios, relatórios, análise de dados, publicação, avaliações, e-mail e outras rotinas. Algumas funcionam imediatamente. Outras pedem configuração somente quando forem usadas.

## Como o FlowOS pensa

`_contexto/` é a memória. Guarda quem é o negócio, como ele escreve, o que está em foco e como você prefere trabalhar.

`AGENTS.md` contém as regras de operação. No Claude Code, `CLAUDE.md` aponta para a mesma fonte. Assim, agentes diferentes trabalham com as mesmas instruções.

`.claude/skills/` reúne os processos reutilizáveis. Quando uma rotina se repete, ela pode virar uma skill nova e passar a fazer parte do sistema.

`marca/` é a identidade visual. `marketing/`, `dados/`, `saidas/` e as pastas criadas na entrevista recebem o trabalho real.

## A tese

IA não é apenas uma ferramenta que seu negócio usa. Ela pode se tornar o ambiente onde contexto, decisões e processos continuam existindo depois que uma conversa termina.

O FlowOS não substitui seu critério. Ele impede que cada trabalho recomece do zero e transforma o que funciona em capacidade reutilizável.

## Segurança

- nunca faça push no repositório de origem;
- mantenha sua cópia privada;
- confirme que o `origin` pertence à sua conta;
- nunca versione senhas, tokens ou chaves de API;
- não copie as skills para pastas duplicadas.
