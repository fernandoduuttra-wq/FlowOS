---
name: copy-lp
description: >
  Escreve a copy completa de uma landing page de vendas (headline, dor, solução, benefícios,
  prova social, oferta, quebra de objeções, garantia, urgência, FAQ e CTAs) pro próprio negócio
  de quem usa o sistema ou pra um cliente, extraindo o intake por perguntas antes de escrever e
  se autoavaliando no final. Serve tanto pra página de vendas de uma oferta quanto pra página de
  captura. Use quando o usuário disser "/copy-lp", "escreve a copy da landing page", "monta a
  copy de vendas de [oferta]", "preciso da copy pro site de [cliente/produto]", ou pedir pra
  redigir headline, oferta, quebra de objeção ou FAQ de uma página de vendas.
---

# /copy-lp — Copy de Landing Page de Vendas

Escreve a copy completa de uma LP de vendas, estruturada em blocos prontos pra repassar a quem
for montar o HTML (`/frontend-design` ou o handoff visual do Passo 5). Não é gerador de frase
bonita solta: extrai o que já existe de real sobre produto, público e oferta, e só depois
escreve.

Serve pra dois casos: o **próprio negócio** de quem usa o sistema, ou um **cliente**.

## Dependências

- **Contexto e voz:** se for o próprio negócio, `_contexto/empresa.md`, `_contexto/estrategia.md`,
  `_contexto/preferencias.md` e, se existir, `_contexto/posicionamento.md` (Tese/Mecanismo/Oferta).
  Se for cliente, o `CLAUDE.md` da pasta dele em `clientes/<nome>/` e o diagnóstico que já tiver
  sido feito pra ele.
- **Se não existir posicionamento** (nem `_contexto/posicionamento.md` nem material equivalente do
  cliente): fazer dentro desta skill um intake curto sobre oferta, público, problema, transformação
  e prova antes de escrever. Não inventar tese, mecanismo ou promessa para preencher lacuna.
- **Visual (opcional, Passo 5):** `marca/design.json` se for o próprio negócio, ou o
  equivalente do cliente.

## Escopo (o que faz e o que NÃO faz)

**Faz:** os 15 blocos de uma LP de vendas completa (ver Passo 2), intake estruturado, e
autoavaliação crítica no final.

**NÃO faz:** HTML/CSS (isso é `/frontend-design` ou o handoff visual descrito no Passo 5), peça
de conteúdo social (`/carrossel`, `/publicar-tema`), nem uma consultoria ampla de posicionamento.
Coleta apenas o contexto mínimo necessário para escrever a página.

## Passo 0 — De quem é a copy, e onde salvar

**A regra é uma só: a copy mora junto do que ela serve.** Esta skill escreve texto, não é dona de
uma pasta. Não crie pasta nova pra ela.

Perguntar só se não estiver óbvio pelo contexto da conversa: essa LP é de quem?

| A copy serve... | Salva em |
|---|---|
| Um **cliente já fechado** | na pasta daquele cliente, junto do resto do trabalho dele |
| Um **prospect** (ainda não fechou) | na pasta daquele prospect, junto da proposta e do spec work |
| Uma **oferta do próprio negócio** | junto de onde aquela oferta já vive (o produto, o site, a campanha). Se ela ainda não tem casa, aí sim a pasta de marketing/conteúdo |

Nome do arquivo: `copy-lp-<oferta>.md`.

**Se o `CLAUDE.md` da raiz definir os nomes dessas pastas, ele manda** — ele descreve a estrutura
real daquele workspace, e ela varia de negócio pra negócio. Na dúvida entre dois lugares plausíveis,
perguntar em uma linha em vez de adivinhar: copy salva no lugar errado vira copy perdida.

## Passo 1 — Intake (7 áreas, uma pergunta por vez se faltar dado)

Antes de perguntar qualquer coisa, **puxar o que já existe** nos arquivos de dependência. Só
perguntar o que não estiver lá. Confirmar entendimento antes de escrever.

1. **Produto/oferta e o problema que resolve.**
2. **Público:** quem é, dor principal, desejo principal, e o **nível de consciência** dele: ele
   sabe que tem o problema? Já conhece as soluções possíveis? Já conhece a sua especificamente?
   Isso muda o ângulo da headline e o quanto a copy precisa "educar" antes de vender.
3. **Oferta completa:** preço, o que está incluso, bônus (se houver, real), garantia (se houver,
   real), prazo/vagas (se houver, real).
4. **Diferenciais e prova:** números reais, cases reais, depoimentos reais, autoridade real. Se
   não existir prova pra ESSA oferta específica ainda (oferta nova, sem venda registrada), dizer
   isso explicitamente, não emprestar prova de outra oferta como se fosse dela.
5. **Objeções mais comuns** que esse público levanta antes de comprar algo parecido.
6. **Tom de voz:** puxar de `_contexto/preferencias.md` (ou do `CLAUDE.md` do cliente). Só
   perguntar se não houver nada registrado.
7. **Origem e temperatura do tráfego:** vem de conteúdo que a pessoa já consome (morno/quente) ou
   de anúncio frio? Isso muda quanto a copy precisa se apresentar antes de vender.

## Passo 2 — Escrever os 15 blocos

Nesta ordem, cada bloco claramente identificado:

1. **Headline principal** — 3 variações, promessa clara, específica, carregada de valor (não
   vaga tipo "transforme seu negócio").
2. **Subheadline** — contexto que reforça a headline.
3. **Bloco de abertura** — 2 a 4 parágrafos curtos: dor → solução → promessa.
4. **CTA primário** (acima da dobra) — texto do botão + micro-copy de apoio.
5. **Identificação da dor** — parágrafo + bullets que fazem o leitor se sentir compreendido.
6. **Apresentação da solução** — como a oferta resolve exatamente aquilo.
7. **Benefícios** (não features) — 5 a 8 bullets de transformação, não de característica técnica.
8. **Prova social** — estrutura pra depoimentos, números, cases. Só entra prova real. Se não
   existir ainda, deixar a estrutura marcada como pendente, nunca preenchida com invenção.
9. **Oferta** — o que está incluso, ancoragem de valor se houver dado real pra ancorar, bônus,
   garantia.
10. **Quebra de objeções** — 3 a 5 objeções reais respondidas direto.
11. **Garantia** — só se for uma garantia que a pessoa realmente vai honrar. Se não estiver
    definida, marcar como pendente de decisão, não inventar política de reembolso.
12. **Urgência/escassez** — só real (vaga limitada de verdade, prazo de verdade). Escassez
    fabricada é a primeira coisa que queima credibilidade com quem já desconfia de copy de venda.
13. **FAQ** — 5 a 8 perguntas que empurram a decisão.
14. **CTA final** — último empurrão + botão.
15. **PS / fechamento** — recapitula a promessa.

## Passo 3 — Autoavaliação

Tabela com: critério, nota de 0 a 10, motivo, o que melhoraria. Critérios fixos:

1. **Headline e gancho** — clareza da promessa, especificidade, força de retenção acima da dobra.
2. **Estrutura persuasiva** — segue o fluxo dor → solução → benefício → prova → oferta →
   objeção → garantia → urgência → CTA sem pular etapa.
3. **Entendimento do público e do nível de consciência** — fala a língua certa pro estágio certo
   (não vende solução pra quem ainda não sabe que tem o problema, não reexplica o óbvio pra quem
   já está pronto pra comprar).
4. **Oferta e ancoragem** — clareza do que está incluso, ancoragem só com dado real.
5. **Prova social e quebra de objeções** — antecipa as objeções certas, usa prova real nos
   momentos certos, sem fabricar o que não existe.
6. **Honestidade da copy** — nenhum número, depoimento, bônus ou garantia inventado. Este
   critério reprova sozinho qualquer nota alta nos outros se houver invenção.
7. **Pronta pra publicar vs. pronta pra tráfego pago** — diferenciar: copy pode estar boa o
   suficiente pra ir ao ar e ainda não estar pronta pra escalar mídia paga, se faltar prova ou
   oferta validada.

Nota geral no final, com o que falta de confirmação do usuário antes de publicar.

## Passo 4 — Entregar

Salvar no destino do Passo 0. Fechar listando, em bullets curtos, todo item marcado
`[CONFIRMAR]` no corpo da copy: são as decisões que só quem é dono da oferta pode tomar (valor de
garantia, número de vagas, o que entra de bônus).

## Passo 5 — Handoff visual (opcional)

Se o usuário quiser ver a copy virar página, não gerar CSS solto: apontar pro
`marca/design.json` (ou o do cliente) e oferecer traduzir os tokens pra escala de site,
mapeando componente por componente da própria copy (hero, bloco de dor, cards de oferta, FAQ,
CTA). Esse mapeamento é um documento próprio (`design-system-lp-<oferta>.md`, mesma pasta da
copy), não uma alteração no `design.json`, que continua sendo só a fonte dos tokens da marca.

---

## Regras

- **Nunca inventar prova, número, depoimento, bônus ou garantia.** Se o dado não existir,
  marcar `[CONFIRMAR]` e seguir. Isso vale mais que deixar a copy "completa" na aparência.
- **Voz.** Seguir sempre `_contexto/preferencias.md` (ou o `CLAUDE.md` do cliente): sem jargão de
  guru, sem promessa milagrosa, sem escassez artificial, sem as construções da Blindagem
  Anti-IA.
- **Uma pergunta por vez** no intake, só perguntando o que os arquivos de dependência não
  respondem sozinhos.
- **Benefício, não feature.** Todo bullet de benefício descreve uma transformação, não uma
  característica.
- **Calibrar pelo nível de consciência do público**, não escrever a mesma copy genérica pra
  tráfego frio e pra quem já consome o conteúdo há meses.

## Quando NÃO usar

- A oferta ainda não está clara e o usuário não quer concluir o intake mínimo → pausar; não escrever
  uma página baseada em suposição.
- Peça de conteúdo social avulsa (post, carrossel, e-mail solto) → `/carrossel` ou
  `/publicar-tema`.
- Reforma de site de prospect sem uma oferta definida → tratar como projeto de prospecção separado;
  esta skill só entra quando houver uma oferta real para apresentar.
- Construção de HTML/CSS de fato → `/frontend-design`, usando esta copy como insumo.
