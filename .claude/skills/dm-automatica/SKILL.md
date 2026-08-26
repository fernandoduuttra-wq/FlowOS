---
name: dm-automatica
description: >
  Constrói do zero um sistema próprio de "comentário vira DM" no Instagram — o substituto do
  ManyChat/Manychat-likes, sem mensalidade. Quando alguém comenta uma palavra-chave num post/reels
  (ou responde um story), a pessoa recebe automaticamente uma DM com o link do lead magnet. Roda em
  plano grátis (Next.js na Vercel + Postgres no Supabase + API do Instagram com login do Instagram).
  Entrega app publicado, painel com senha pra criar automações e o motor de fila rodando. Use quando
  o usuário disser "/dm-automatica", "quero um ManyChat próprio", "comentário vira DM", "automatizar
  entrega de lead magnet no Instagram", "responder comentário com DM automática", "sair do ManyChat",
  ou pedir automação de direct/comentário do Instagram sem ferramenta paga.
---

# /dm-automatica — ManyChat próprio, sem mensalidade

Constrói um app que escuta comentários do Instagram e entrega o lead magnet por DM.
O usuário fica dono do sistema: sem assinatura, sem limite de contato, sem
plataforma no meio.

**A parte difícil não é o código — é o console da Meta.** O código sai em uma
passada; o cadastro na Meta tem seis armadilhas que quebram tudo em silêncio.
Elas estão em `references/meta-console.md`. Leia ANTES de guiar o usuário.

---

## Antes de começar: o que só o usuário pode fazer

Peça e confirme, nesta ordem. Nada avança sem os quatro:

1. **Conta profissional do Instagram** (Comercial ou Criador). Conta pessoal
   **não funciona** — a API não conecta e o convite de testador nem aparece.
   As duas modalidades servem igual pra API.
2. **Contas grátis** em Supabase, Vercel e Meta for Developers. Criar conta não
   tem API — é o usuário no navegador. Sugira entrar com GitHub nos dois
   primeiros (a Vercel exige repositório Git de qualquer forma).
3. **Uma segunda conta de Instagram** pra testar. Não dá pra testar comentando
   na própria conta.
4. **O lead magnet pode ficar pra depois.** O painel deixa cadastrar palavra-chave
   e link sem tocar em código. Não trave a construção esperando isso.

### Acelere pedindo dois tokens (opcional, mas muda o jogo)

Sem eles, o usuário vira o "braço" pra cada variável de ambiente e cada SQL —
e cada ida e volta custa minutos. Com eles, você faz sozinho:

| Token | Onde ele gera | O que passa a ser seu |
|---|---|---|
| **Vercel** — Account Settings → Tokens | escopo no projeto | criar projeto, cadastrar env vars, deploy, desligar Deployment Protection, domínios |
| **Supabase** — Account → Access Tokens | conta | criar projeto, rodar SQL (Management API), ler as chaves |

Ofereça no início, explicando o custo real: **são tokens amplos**; oriente criar
com o menor escopo possível e revogar ao terminar. Se o usuário preferir não
gerar, siga no modo manual — só avise que ele vai colar bastante coisa.

**O console da Meta não tem API.** Criar o app, assinar webhook, cadastrar
redirect e publicar é sempre navegador. Não prometa automatizar isso.

---

## O que o sistema faz (e o que não faz)

Diga os limites **antes** de construir. Eles são da API, não do código, e
quebram expectativa se aparecerem só no fim:

- **Não dá pra exigir que a pessoa siga** antes de entregar o link — a API não
  permite verificar seguidor. Só dá pra pedir na mensagem.
- **Não dá pra saber se a pessoa clicou.** O lembrete dispara por tempo.
- **Não dá pra disparar em massa pra base fria.** A Meta proíbe e derruba a
  conta. O que funciona é comentário → DM.

### A janela de 24 horas (o conceito que rege tudo)

A Meta só deixa mandar DM pra quem falou com você nas últimas 24h. A exceção é
a **resposta privada**: uma mensagem endereçada ao `comment_id`, permitida uma
vez por comentário, até 7 dias depois.

Por isso o fluxo é sempre este, e não outro:

1. Comentário casa a palavra-chave → **resposta privada** (fura a janela) pedindo
   uma resposta, com botão de resposta rápida.
2. A pessoa **toca no botão** → isso abre a janela de 24h.
3. Só então entram a **entrega do link** e o **lembrete**.

Quem tenta mandar o link direto na primeira mensagem toma erro ou entrega vazio.
A arquitetura em `references/arquitetura.md` implementa exatamente esse ciclo.

---

## Fluxo de execução

### 1. Projeto

Scaffold Next.js (App Router, TypeScript, Tailwind) **fora de pasta
sincronizada por nuvem** — `node_modules` em OneDrive/Dropbox corrompe. Se o
`CLAUDE.md` da raiz definir onde projetos Node moram, ela manda.

Repositório próprio e **privado** no GitHub. Não misture com o repo do
workspace. Push no branch principal = deploy automático na Vercel.

### 2. Banco

Rode `assets/schema.sql` no SQL Editor do Supabase. Resposta esperada:
`Success. No rows returned` — **avise o usuário que isso é sucesso**, porque
"0 rows" parece erro pra quem não é técnico.

Todas as tabelas ficam com RLS ligado e **sem políticas**: o navegador não
acessa o banco, só o servidor com a chave secreta.

### 3. Código

Escreva conforme `references/arquitetura.md`. Não improvise o schema nem o
fluxo da fila — a trava atômica existe porque o webhook e o cron drenam a fila
ao mesmo tempo, e sem ela a mesma DM sai duas vezes.

Rode `npm run build` antes de deployar. Se houver identidade visual definida no
workspace (tokens de marca), o painel usa ela; senão, escolha uma paleta sóbria
e consistente.

### 4. Deploy

Cadastre as variáveis do `.env.example` na Vercel. **Variável nova só vale
depois de um redeploy** — a Vercel não reaplica em build existente. Avise, ou o
usuário vai testar e achar que está quebrado.

Depois do primeiro deploy, **fixe `APP_URL`** com o endereço final. Sem isso o
app pergunta o próprio endereço à Vercel, que às vezes responde um nome gerado
(`projeto-abc123.vercel.app`) diferente do que foi cadastrado na Meta — e o
OAuth passa a ser recusado com `Invalid redirect_uri`.

**Desligue a Deployment Protection** (Settings → Deployment Protection →
Vercel Authentication → Disabled). Ela vem ligada e desvia *tudo* pro SSO da
Vercel: o webhook toma 302 em vez de entregar, e a Meta não consegue ler a
política de privacidade pra aprovar a publicação. Esse é o erro mais silencioso
de todos — teste com `curl` em vez de confiar no navegador (que loga sozinho).

### 5. Meta

Siga `references/meta-console.md` passo a passo, **pedindo print a cada tela**.
O fluxo muda com frequência e as telas são parecidas entre si; guiar no escuro
custa mais caro que conferir.

### 6. Motor

Rode `assets/cron.sql` (com URL e segredo preenchidos) no SQL Editor. O plano
grátis da Vercel não roda cron de minuto — quem bate o ponto é o `pg_cron` do
Supabase.

### 7. Teste real

Peça pra comentar a palavra-chave **de outra conta**. Depois confira no banco:
`events` recebeu o webhook, `queue` mostra `public_reply`/`welcome` como `sent`.
Não pergunte "funcionou?" — verifique.

---

## Verificação (não confie em "parece que foi")

Teste em produção, com `curl`, e confirme cada linha:

| Rota | Esperado |
|---|---|
| `/privacidade` e `/exclusao-de-dados` | 200 (públicas, a Meta precisa ler) |
| `/` sem sessão | redireciona pro login |
| `/api/webhook?hub.verify_token=errado` | 403 |
| `/api/webhook` com o token certo | 200 devolvendo o `hub.challenge` |
| `POST /api/webhook` sem assinatura | 401 |
| `POST /api/drain` sem segredo | 403 |
| `/api/oauth/start` | 302 com `redirect_uri` **idêntico** ao cadastrado na Meta |

O último é o que mais falha. Compare caractere por caractere.

---

## Erros e o que significam

| Sintoma | Causa real |
|---|---|
| `Invalid redirect_uri` | URI não cadastrado, ou `APP_URL` diferente do que está na Meta |
| `Função de desenvolvedor é insuficiente` | testador não adicionado, ou convite não aceito no celular |
| 500 em `/api/oauth/start` | variável de ambiente faltando na Vercel (ou faltou redeploy) |
| Comentário não dispara nada | app não publicado — em desenvolvimento a Meta **não entrega webhook** |
| Tudo redireciona pro login da Vercel | Deployment Protection ligada |
| DM duplicada | fila sem trava atômica |
| Painel some depois de conectar | `APP_URL` apontando pro domínio errado |

---

## Ao entregar

Diga em uma frase o que ficou pronto e **o que o usuário faz sozinho daqui pra
frente**: trocar link, palavra-chave e mensagens pelo painel, sem tocar em código.

Confira se a automação criada não ficou com o casamento em "qualquer comentário
serve" — nesse modo *qualquer* pessoa comentando *qualquer coisa* recebe DM. É o
padrão mais perigoso do painel e passa despercebido.

Registre na memória do projeto o endereço de produção, onde o projeto mora e as
pegadinhas que apareceram — a próxima montagem começa do zero sem isso.
