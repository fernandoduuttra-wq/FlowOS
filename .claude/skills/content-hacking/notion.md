# Notion — schema dos databases

Os IDs dos databases ficam no `CLAUDE.md` da raiz, nunca aqui.

**Conexão:** connector do claude.ai (Settings → Connectors → Notion), via OAuth — o mesmo mecanismo
do Gmail/Drive. As ferramentas aparecem como `mcp__claude_ai_Notion__*`. Se não estiverem
disponíveis, avisar o usuário pra conectar o Notion nos connectors do claude.ai e reiniciar —
**nunca** pedir token nem colar credencial em arquivo versionado.

**Parent ao criar página:** usar o `data_source_id` do database (não o ID de página). Ambos estão
no `CLAUDE.md` da raiz.

---

## Database 1 — Banco de Referências

Uma linha por conteúdo dissecado. É o banco de conteúdo validado.

| Propriedade | Tipo | Valores |
|---|---|---|
| Nome | title | — |
| Link | url | vazio se o usuário colou o conteúdo sem link |
| Rede | select | YouTube / Instagram / LinkedIn / Substack / X |
| Tipo | select | Vídeo longo / Short / Reel / Carrossel / Post texto / Newsletter / Thread |
| Criador | rich_text | @ do autor |
| Conteúdo original | rich_text | transcrição (auto) ou texto/slides (manual) |
| Objetivo | select | Viral / Útil / Vendas |
| Formato de Produção | select | Talking head / Mãozinha / Tela dividida / Lifestyle / Clone / Depoimento / Estático |
| Hook original | rich_text | `Fala:` + linha em branco + `Visual:` |
| Hook com variáveis | rich_text | o esqueleto do gancho, com `[colchetes]` |
| Hook adaptado | rich_text | o esqueleto já preenchido com o contexto do usuário |
| Tipo de Gancho | select | Curiosidade / Identificação / Revolta / Benefício direto / Novidade |
| Psicologia | rich_text | o mecanismo mental. Texto livre. Ver SKILL.md — é o campo que sustenta a V2. |
| Tipo de Sustentação | select | Série numerada / Lista / Narrativa / Loop de curiosidade / Passo a passo / Prova intercalada / Contraste / Argumento — indexa o MEIO por tipo |
| CTA identificada | rich_text | "Nenhuma" se não houver |
| Tipo de CTA | select | Comment-gate / Follow / Salvar / Compartilhar / DM / Link na bio / Venda direta / Nenhuma — indexa a CTA por tipo |
| Autoria | select | Meu / Terceiro. `Meu` = peça própria validada que graduou pro banco (alto alcance/save/venda). Filtro pra separar teu repertório do de terceiros. |
| Idioma | select | Português / Inglês / Outro |
| Potencial | select | Alto / Médio / Baixo |
| Por que | rich_text | 3 critérios numerados (alinhamento / replicabilidade / métricas) |
| Origem | select | Auto (transcrição) / Manual (colado) |
| Status | select | Novo / Analisado / Virou Ideia |
| Data | date | — |

**Corpo da página:** a estrutura dissecada (`## Gancho` / `## Desenvolvimento` / `## CTA`) seguida
da **V0 — Esqueleto**. Ver SKILL.md, Passos 5 e 6.

**`Status: Novo`** é o estado de fila: o usuário cola um link no Notion pra dissecar depois. Quando
ele pedir "processa os Novo", buscar por esse filtro e rodar o fluxo em cada um, **completando** a
página existente em vez de criar outra.

---

## Database 2 — Ideias de Conteúdo

A pauta. É onde a produção acontece — inclusive a produção feita **na mão** (card sem Referência).

| Propriedade | Tipo | Valores |
|---|---|---|
| Título da Ideia | title | — |
| Rede | multi-select | YouTube / Instagram / LinkedIn / Substack / X |
| Formato de Produção | select | igual ao do Banco |
| Hook | rich_text | o gancho escolhido pra essa peça |
| Versão | select | Clone fiel / Recombinado / Autoral |
| Objetivo | select | Viral / Útil / Vendas |
| Nível de Consciência | select | Topo / Meio / Fundo |
| Pilar | select | conforme os territórios definidos no `CLAUDE.md` da raiz |
| CTA Sugerida | rich_text | — |
| Status | select | Ideia / Em Produção / Publicado |
| Referência | relation | → Banco de Referências |
| Publicação | date | — |
| Views | number | preenchido depois de publicar |
| Salvos | number | preenchido depois de publicar |
| Comentários | number | preenchido depois de publicar |
| Aprendizado | rich_text | o que o número ensinou |

**Corpo da página:** o roteiro completo, pronto pra gravar. Ver SKILL.md, Passo 6.

**`Rede` é multi-select, mas o default é UMA rede — a do original.** Carrossel vira carrossel, YT
vira YT, newsletter vira newsletter. Só marcar mais de uma rede quando o usuário pedir cross-post
explicitamente (Passo 6 da SKILL.md).

**`Versão: Autoral`** é o card que nasceu sem referência — ideia do próprio usuário. A pauta serve
os dois caminhos.

### O loop se fecha aqui

As 4 últimas propriedades (Views, Salvos, Comentários, Aprendizado) existem por um motivo: **peça do
próprio usuário que performou bem deve virar referência no Banco.** Sem isso, o banco vira museu de
post dos outros e nunca aprende com o que funciona pra ele.

Quando o usuário trouxer os números de uma peça publicada, avaliar: se performou acima da média
dele, oferecer cadastrar no Banco de Referências (`Rede` = a dele, `Criador` = ele, `Origem` =
Manual). O esqueleto dela passa a estar disponível pra reuso, igual ao de qualquer outro.

---

## Views a manter

| View | Onde | Pra quê |
|---|---|---|
| Por Rede | Ideias | a separação por rede social |
| Kanban por Status | Ideias | o fluxo de produção |
| Calendário por Publicação | Ideias | o que sai quando |
| Fila (`Status = Novo`) | Banco | links esperando dissecação |
| Por Potencial | Banco | filtrar o que vale adaptar — é o filtro que substitui perguntar antes |
