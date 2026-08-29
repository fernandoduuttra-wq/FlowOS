# FlowOS

> O sistema operacional do seu negócio dentro da IA.

Em alguns minutos, seu negócio passa a ter memória própria, regras de trabalho e skills prontas para transformar tarefas repetidas em processos executáveis. Você continua dirigindo. O sistema lembra, organiza, executa e melhora com o uso.

O FlowOS funciona no VS Code com Claude Code, Codex e outros agentes que leem `AGENTS.md`.

## Antes de começar

Você precisa de:

1. VS Code;
2. Claude Code, Codex ou outro agente compatível dentro do VS Code.

## Ligando o sistema

Abra o agente em uma pasta vazia e cole:

```text
Clona o https://github.com/fernandoduuttra-wq/FlowOS.git na pasta atual,
entra nela e roda o /instalar.
```

O agente vai:

1. baixar o FlowOS;
2. abrir o projeto;
3. entrevistar você sobre negócio, escrita, foco e marca;
4. preencher seu contexto;
5. adaptar o sistema ao seu perfil;
6. criar somente as pastas que sua operação precisa.

A instalação não pede conta no GitHub, GitHub CLI ou autenticação. O `/instalar` remove os remotos
herdados do clone, então sua cópia fica independente do repositório original. Se houver uma
atualização no futuro, peça ao próprio sistema para consultar o repositório público e decidir com
você o que vale incorporar.

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

- nunca versione senhas, tokens ou chaves de API;
- não copie as skills para pastas duplicadas.
