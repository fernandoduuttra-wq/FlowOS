# De onde vem o dado de ads — as três rotas

Três jeitos de o FlowOS enxergar seus anúncios. Não é "uma é melhor" — elas resolvem
coisas diferentes, e a combinação mais comum é usar duas ao mesmo tempo.

| | **CSV** | **Conector MCP** | **API direta** |
|---|---|---|---|
| Setup | nenhum | ~15 min, login | ~30 min, app de dev |
| Cria campanha do zero | não | **sim** | não |
| Pausa / muda verba / agenda | não | sim, **mas pausa o que edita** | **sim, cirúrgico** |
| Roda sem você (agendado) | não | não | **sim** |
| Guarda histórico | manual | não | **sim** |
| Espiona concorrente | não | **sim** | dá trabalho |
| Sua própria lógica de análise | — | não | **sim** |
| Custa token de IA | sim | sim | **não** |
| Depende de terceiro | não | **sim** | não |

---

## Rota 1 — CSV exportado (o padrão de instalação)

Você exporta o relatório no Gerenciador de Anúncios e aponta o arquivo pra
`/relatorio-ads`. Zero configuração, funciona no primeiro dia.

**Boa quando:** você mexe com ads de vez em quando, tem uma conta ou duas, e o
relatório é semanal ou mensal.

**Limite:** é você que exporta, toda vez. Não automatiza, e o recorte do dado é o
que a interface deixou você escolher na hora do export.

---

## Rota 2 — Conector MCP oficial da Meta

Servidor construído pela própria Meta (`https://mcp.facebook.com/ads`). Adiciona nas
configurações de conectores da conta Claude, autentica com o login normal do Facebook.
Sem token, sem app de desenvolvedor, sem código.

Depois de conectado você conversa: *"como foi a campanha X essa semana?"*, *"pausa o
conjunto com frequência alta"*, *"cria uma campanha de tráfego com R$ 30/dia"*.

### O que ele faz bem

- **É a única rota que monta campanha do zero.** Campanha, conjunto, anúncio e
  criativo; público, catálogo, pixel e dataset; teste A/B e teste de lift. Toda ação
  de escrita pede aprovação no chat antes de executar (dá pra liberar tudo de uma vez
  nas permissões, mas o padrão é aprovar uma a uma — mantenha assim).
- **Espiona concorrente.** `ads_library_search` varre a Biblioteca de Anúncios da
  Meta: busca por marca, palavra-chave ou país, devolve criativo, texto, data e link
  do anúncio. Dá pra ver quantos anúncios uma marca tem no ar e que ângulo ela está
  rodando. **Isso a API não te dá de graça** — teria que construir. É o argumento
  mais forte do conector depois da escrita.
- **Diagnóstico da conta:** erros de veiculação, opportunity score, benchmark de
  indústria, sinal de anomalia, tendência de performance, saúde do catálogo.
- **Preview de anúncio** antes de subir.

### Os limites que importam

- **Editar pelo conector PAUSA o que você editou.** Toda edição volta com
  `status_forced_to_paused` — trocar o orçamento de uma campanha no ar a derruba, e
  ela só volta com uma chamada de ativação separada. Em campanha de cliente isso é
  entrega parada sem ninguém perceber. **Para mudar verba, status ou agendamento de
  algo que já roda, use a API direta**; deixe o conector pra montar coisa nova.
- **Ele diz "sucesso" para campo que não gravou.** A resposta ecoa o *pedido*, não o
  estado salvo — a própria documentação da ferramenta avisa. Depois de qualquer
  edição, **leia de volta** antes de dar por feito.
- **Só funciona com você na conversa.** Não roda agendado, não roda de madrugada,
  não alimenta script nenhum. *(Cuidado com o nome `ads_entity_schedule_report` — ele
  NÃO é relatório agendado. É um fallback assíncrono pra consulta que deu timeout
  dentro da mesma conversa.)*
- **Não acumula histórico.** Cada pergunta é consulta nova. Comparar julho com março
  do ano passado só se você tiver guardado antes, por fora.
- **Um breakdown por chamada.** Se você pedir dois cruzamentos (ex: dispositivo ×
  hora do dia), ele usa o primeiro e **ignora o resto** — avisa na resposta, mas
  ignora. Cruzamento multidimensional é território da API.
- **Campos curados, não os da Graph API.** O conjunto de métricas é específico por
  nível e menor que o da API. Campo que existe na Marketing API pode simplesmente não
  estar exposto aqui.
- **Upload de criativo pode não estar liberado na sua conta.** A ferramenta de upload
  existe, mas a Meta libera por conta — em conta não liberada ela responde *"this tool
  is new and is being gradually rolled out"*. Enquanto não liberar, **só dá pra montar
  anúncio com imagem que já esteja na biblioteca da conta**. **Teste chamando antes de
  prometer:** a documentação da ferramenta não diz se a sua conta está liberada.
  Quando liberar, ela aceita **só URL pública** — arquivo local, Google Drive e Dropbox
  não funcionam (devolvem página de login em vez do arquivo). Contorno:
  `python scripts/deploy-netlify.py <pasta-de-criativos> --slug <slug> --assets`
  hospeda e imprime a URL pública de cada arquivo. (Se a raiz definir outra esteira de
  hospedagem, ela manda.) Vídeo processa em segundo plano: só usar depois de virar "ready".
- **Ao criar anúncio de clique-para-WhatsApp, o link é obrigatório aqui** — diferente do
  Gerenciador, onde o destino vem da página. E o conector **não lê esse número de volta**
  (o criativo devolve link vazio e o `promoted_object` do ad set não é exposto), então o
  número precisa vir de outra fonte sua.
- **Instagram só pelo que é anunciável.** Lista conta e mídia do IG (post, reel,
  story) e impulsiona post existente — mas exige o IG vinculado à conta de anúncio e
  a permissão `instagram_basic`. Não é acesso geral ao Instagram.
- **Listagem de criativo vem incompleta.** Listar criativos devolve só id, nome,
  conta e status. Corpo, headline, link, image_hash e CTA exigem **uma segunda
  chamada**. Campo faltando na primeira resposta não significa campo vazio — erro
  fácil de cometer ao montar relatório de criativo.
- **Não faz:** reativar conta desativada, criar/editar Página do Facebook, postar
  orgânico, gerenciar método de pagamento.
- **Rollout gradual.** Nem toda conta está habilitada — a Meta libera aos poucos.
  Conta não habilitada volta com aviso e não pode ser usada.
- **Você depende da Meta.** O servidor é deles. Se mudarem, limitarem ou desligarem,
  não há o que fazer. A API é contrato público e estável; o MCP é produto.
- **Gasta token de IA.** Cada consulta passa pelo modelo.

**Boa quando:** você quer perguntar e agir na hora, sem sair da conversa. É a rota do
dia a dia e da pesquisa de concorrente.

---

## Rota 3 — API direta (Marketing API)

`scripts/meta-ads.py` fala direto com a Graph API usando um token seu. É código, não
conversa: roda no terminal, roda agendado, cospe CSV ou JSON.

```bash
python scripts/meta-ads.py accounts
python scripts/meta-ads.py insights --account act_123 --preset last_30d
python scripts/meta-ads.py insights --account act_123 --since 2026-01-01 --until 2026-07-31 \
       --daily --csv dados/meta-2026.csv

# escrita — sem --aplicar é ensaio: mostra o de->para e não altera nada
python scripts/meta-ads.py pausar    --id 123
python scripts/meta-ads.py orcamento --id 123 --diario 26.67 --aplicar
python scripts/meta-ads.py agendar   --id 123 --fim 2026-09-05 --aplicar
```

### O que ela faz bem

- **Roda sem ninguém olhando.** Tarefa agendada puxa todo dia e vai empilhando.
  `--daily` quebra linha por dia — é assim que se constrói histórico de verdade.
- **Banco de dados e dashboard.** Joga em SQLite, Postgres, Sheets, Metabase, ou num
  painel HTML próprio: investimento, receita, CTR, CPC, CPM, custo por compra, funil,
  UTMs, tudo numa tela só, na sua identidade visual, no celular se quiser.
- **Cruza com o que a Meta não tem.** Venda real do CRM, margem por produto, LTV,
  receita do financeiro. Um painel que junta Meta + Google + site + CRM em vez de
  cinco abas abertas. **Esse é o caso mais forte da API** — o conector não faz.
- **Sua lógica de análise, não a dele.** Se você tem um método próprio de ler
  campanha — seus limiares, sua ordem de corte, seu jeito de decidir o que pausa —
  você programa isso uma vez e roda sempre igual. No conector você recebe a análise
  que o modelo achou boa naquela hora.
- **Multi-cliente de verdade.** Varre todas as contas de uma vez, um painel por
  cliente. Numa agência isso é a diferença entre escalar e não escalar.
- **Campos e cruzamentos completos**, sem a curadoria do conector.
- **Webhooks e evento em tempo real** são possíveis aqui (não no conector).
- **Não gasta token de IA** — é Python puro.

### Os limites que importam

- **Não monta campanha do zero.** Ela edita o que existe (`pausar`, `ativar`,
  `orcamento`, `agendar`); criar campanha, conjunto, anúncio e criativo continua no
  conector. Escrever aqui exige `ads_management` no token — só com `ads_read` os
  comandos de escrita falham com erro de permissão.
- **Setup mais chato:** app no [developers.facebook.com](https://developers.facebook.com),
  permissões (`ads_read` pra ler, `ads_management` pra escrever), gerar e estender token.
- **Token expira.** O do Graph API Explorer é *short-lived*: dura **1–2 horas**.
  Estendido pelo Depurador vira *long-lived*: ~60 dias. Pra rotina agendada, use
  **System User** da Business Manager: não expira.
- **A Meta aposenta versão de API rápido — mais rápido do que parece.** Sai versão
  nova ~3x por ano e cada uma vive **~1 ano**, não dois. Conferido em 28/jul/2026:
  **v25.0** é a atual (18/fev/2026), **v24.0 expira 06/out/2026** e **v23.0 já morreu
  em 09/jun/2026**. Quando quebrar (`Unsupported get request`), é só subir a constante
  `API_VERSION` no topo do script — mas **coloque no calendário**, porque a parede
  chega uma vez por ano e derruba rotina agendada sem avisar.
- **O número vem cru.** Análise, alerta e recomendação continuam sendo trabalho da
  `/relatorio-ads` em cima do CSV.

**Boa quando:** você já tem estrutura montada e quer bater o olho num painel; quer
histórico; quer cruzar com venda real; ou atende vários clientes.

---

## Como escolher

- **Só quero o relatório da semana** → CSV. Não invente complexidade.
- **Quero perguntar, montar campanha nova e espiar concorrente** → conector MCP.
- **Quero mexer em campanha que já está no ar** (verba, pausa, agendamento) → **API**.
  O conector pausa o que edita, e em conta de cliente isso custa entrega.
- **Quero histórico, painel, ou cruzar com venda real do CRM** → API.
- **Quero as duas** → é o normal quando a operação cresce: **conector pra explorar e
  montar, API pra operar o que já roda e pra rotina.** Uma não substitui a outra.

---

## Setup da rota API

1. [developers.facebook.com](https://developers.facebook.com) → **Criar aplicativo**
   (dê um nome tipo "Claude Ads"), escolher o caso de uso de **conta de anúncio** e
   adicionar o produto **Marketing API**.
2. No app: **Ferramentas → Explorador de Graph API**. Selecionar o app, marcar as
   permissões (`ads_read` basta pra leitura) e **Gerar token**.
3. Esse token dura **1–2 horas**. Estender: **Ferramentas → Depurador de token** →
   colar → **Depurar** → **Estender token de acesso**. Agora dura ~60 dias.
4. Salvar **só o token**, sem aspas, em `scripts/.meta.token.txt`.
   Já está no `.gitignore` — nunca vai pro repositório. **Token de ads no GitHub =
   qualquer um gastando seu orçamento.**
5. Testar: `python scripts/meta-ads.py accounts`

**Pra rotina agendada**, trocar por token de **System User**: Business Settings →
Usuários do sistema → criar → gerar token com acesso às contas de anúncio. Esse não
expira, e é o único que sustenta tarefa diária sem manutenção.
