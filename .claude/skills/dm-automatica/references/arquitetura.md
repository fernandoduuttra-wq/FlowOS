# Arquitetura

Next.js (App Router, TypeScript) na Vercel + Postgres no Supabase + API
"Instagram com Login do Instagram" (`graph.instagram.com`, v25.0 ou superior).
**Não usa página do Facebook.**

Schema pronto em `../assets/schema.sql`; motor em `../assets/cron.sql`.

---

## Variáveis de ambiente

```
SUPABASE_URL                 Project URL — SEM /rest/v1 no fim
SUPABASE_SERVICE_ROLE_KEY    chave secreta (sb_secret_… nas contas novas)
IG_APP_ID                    ID do app do INSTAGRAM
IG_APP_SECRET                chave secreta do app do INSTAGRAM
IG_WEBHOOK_VERIFY_TOKEN      você gera; repete no cadastro do webhook
CRON_SECRET                  você gera; repete no cron.sql
PAINEL_SENHA                 senha do painel
APP_URL                      endereço de produção — fixe sempre (ver SKILL.md)
```

Nenhuma leva prefixo público. O navegador nunca toca no banco.

Ao pegar a Project URL, o usuário costuma copiar o endpoint da Data API, que
termina em `/rest/v1/`. Isso faz as consultas responderem com `count: null` em
vez de erro — falha silenciosa. Normalize removendo o sufixo.

---

## Fluxo

```
comentário casa palavra-chave
   ├─ resposta pública no comentário           (opcional, sorteia variações)
   └─ resposta privada  → recipient {comment_id}   FURA a janela de 24h
                           texto + botão de resposta rápida
                                    ↓
                       pessoa toca no botão
                                    ↓
                       janela de 24h ABERTA
                                    ↓
              ├─ DM com o link          → recipient {id}
              └─ lembrete (após N min)  → recipient {id}
```

Resposta a story chega como mensagem com `message.reply_to.story`; DM comum
chega como mensagem normal. Nos dois casos a conversa já está aberta, então a
primeira mensagem vai direto pro `id`.

---

## Endpoints

Base `https://graph.instagram.com/v25.0`.

| Ação | Chamada |
|---|---|
| Autorizar | `https://www.instagram.com/oauth/authorize` — `client_id` = ID do app do Instagram; scopes `instagram_business_basic`, `instagram_business_manage_messages`, `instagram_business_manage_comments` |
| Token curto | `POST https://api.instagram.com/oauth/access_token` |
| Token longo (60d) | `GET /access_token?grant_type=ig_exchange_token` |
| Renovar | `GET /refresh_access_token?grant_type=ig_refresh_token` |
| Perfil | `GET /me?fields=user_id,username,name,profile_picture_url` |
| Enviar | `POST /{ig_user_id}/messages` — recipient `{comment_id}` ou `{id}` |
| Responder comentário | `POST /{comment_id}/replies` |
| Assinar webhooks | `POST /{ig_user_id}/subscribed_apps?subscribed_fields=comments,messages` |
| Listar mídias | `GET /{ig_user_id}/media` |

**Assinar os webhooks no callback do login.** Sem essa chamada o app está
conectado mas não recebe nada — e o sintoma é idêntico ao de app não publicado.

Corpos de mensagem: texto simples; `quick_replies` (botão que abre a janela);
`attachment.template` tipo `button` com `web_url` (entrega do link). Títulos de
botão têm limite de 20 caracteres — corte antes de enviar.

---

## Webhook

`GET` responde ao handshake: se `hub.mode=subscribe` e `hub.verify_token` bate,
devolve `hub.challenge` cru.

`POST` valida `X-Hub-Signature-256` = HMAC-SHA256 do **corpo cru** com o app
secret, em comparação de tempo constante.

> Leia o corpo como texto antes de qualquer parse. Chamar `req.json()` primeiro
> consome o stream e a assinatura nunca mais confere.

Ignore eventos cujo `sender.id` é a própria conta e mensagens com `is_echo` —
senão o app responde a si mesmo em loop.

Responda 200 rápido; a Meta reentrega o que demora. Dispare a drenagem em
background (`after()` do Next) pro envio parecer instantâneo.

---

## Fila e trava atômica

Dois processos drenam a fila ao mesmo tempo: o webhook (imediato) e o cron (a
cada minuto). Sem trava, a mesma DM sai duas vezes.

A função `claim_queue` marca os itens como `sending` e devolve numa única
instrução, com `FOR UPDATE SKIP LOCKED`. Quem chegou depois simplesmente não vê
os itens já tomados.

Cada item tem `dedupe_key` única (ex.: `welcome:{comment_id}`). Reentrega do
webhook colide na constraint e é ignorada — trate `23505` como sucesso.

Itens presos em `sending` (deploy no meio do envio) voltam pra fila por
`requeue_stuck`.

**Limites:** ~2 envios/segundo e ~200 DMs automáticas/hora. Respeite com pausa
entre envios.

Antes de enviar item marcado `requires_open_window`, confirme que o contato
respondeu nas últimas 24h. Se não, marque `skipped` — não tente e não falhe.

---

## Painel

Sessão por cookie assinado (HMAC da senha, nunca a senha). Verifique nas páginas
e rotas, não em middleware — menos peça pra quebrar.

Deve permitir criar automação com: nome, ativo, gatilhos (comentário/story/dm),
palavras-chave, tipo de casamento, post específico, respostas públicas, primeira
DM, botão de resposta, link + rótulo, lembrete + atraso.

**O tipo de casamento tem um padrão perigoso:** "qualquer comentário serve" faz
*qualquer* pessoa comentando *qualquer coisa* receber DM. Deixe "a palavra
aparece no comentário" como padrão e avise se o usuário mudar.

Normalize a comparação: minúsculas, sem acento, com fronteira de palavra (pra
"quero" não casar dentro de "querosene").

Páginas `/privacidade` e `/exclusao-de-dados` são **públicas e obrigatórias** —
a Meta exige pra publicar.

---

## Pegadinhas de plataforma

- **Fuso:** servidor em UTC; trave a exibição no fuso local do usuário.
- **Next 16:** `params`, `searchParams` e `cookies()` são assíncronos (`await`).
  `middleware.ts` virou `proxy.ts`.
- **Vercel Hobby não roda cron de minuto.** Use `pg_cron` + `pg_net` do Supabase
  batendo nos endpoints, protegidos por `CRON_SECRET`.
- **Token de 60 dias:** renove semanalmente. Uma semana falha não derruba nada.
