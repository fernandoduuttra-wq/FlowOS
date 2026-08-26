---
name: aperitivo
description: >
  Refaz a página/site de um prospect como spec work (trojan horse) pra abrir conversa: pega o site
  atual, mantém a identidade da pessoa, melhora copy e estética e devolve uma versão nova pronta pra
  hospedar de graça. Fluxo LEVE de prospecção, não o pesado de cliente fechado. Use quando o usuário
  disser "faz um aperitivo pra X", "refaz/melhora o site da X pra prospectar", "manda uma isca pra X",
  ou simplesmente colar o link de um site que quer melhorar pra vender depois. NÃO rodar /identidade
  nem /diagnostico aqui — isso é investimento de cliente fechado.
---

# /aperitivo — Página-isca em uma passada

O aperitivo é uma aposta: pode não fechar. Então cada token conta e o objetivo é UM só — uma página
tão melhor que a pessoa queira responder. Não se refaz a identidade dela, não se gera posicionamento
novo, não se inventa nada. Pega o que existe, mantém a marca dela e eleva a execução.

**A regra de ouro:** é uma **nova VERSÃO** da página dela, não uma **página nova**. A pessoa tem que
bater o olho e reconhecer que é a dela, só que melhor. Transformação grande demais gera estranheza e
derruba a conversa.

## Quando roda (e quando NÃO roda)

Roda na **prospecção**: alguém que ainda não é cliente, que a gente quer fisgar com uma amostra.

**NÃO roda dentro do aperitivo:**
- `/identidade` (design system do zero, logo, brandbook, referências de Pinterest)
- `/diagnostico` (posicionamento Tese/Mecanismo/Oferta)
- qualquer coisa que reconstrua a marca dela

Se no meio do caminho der vontade de "aproveitar e refazer a identidade", parar: isso é a esteira
pesada rodando na aposta errada. O aperitivo é rápido de propósito.

**Importante — não é regra dura que "fechou = refaz a identidade".** O redesign completo (identidade
nova, rebrand) é uma **entrega separada e paga**, decidida caso a caso, não uma consequência
automática de fechar. Muito cliente fechado segue com a própria identidade, exatamente como no
aperitivo: mantém logo/paleta/imagens e a gente só executa melhor. A esteira pesada só entra quando
o cliente contrata explicitamente esse redesign. Na dúvida, manter a identidade dele.

## Antes de começar

- **Pasta:** se o prospect ainda não tem pasta, rodar `/novo-projeto` primeiro (ele cai em
  `comercial/prospeccao/<nome>/`). O aperitivo é a primeira entrega, não nasce solto.
- **Identidade visual da raiz vs. da cliente:** aqui a fonte da verdade visual é a **da PROSPECT**
  (paleta, logo, fonte e imagens que ela já usa), não o `design.json` do teu negócio. A raiz manda só
  nas regras de escrita e nas boas práticas anti-"cara de IA".

## Workflow (2 passos)

### Passo 1 — Refazer (no Claude Code, com a skill `/frontend-design`)

Sempre chamar a skill **`/frontend-design`** na hora de montar a página: é o motor de estética. Se ela
não engatar sozinha, invocar na mão.

O que a reconstrução tem que fazer:

1. **Acessar o site atual e extrair TODO o conteúdo real:** serviços, textos, depoimentos, endereço,
   WhatsApp, redes sociais. **Não inventar nada.** O que não existir no site vira pendência, não
   invenção.
2. **Manter a identidade:** logo, paleta de cores e imagens originais. Se o que ela usa for feio,
   escolher a melhor cor que ela já tem e limpar o resto — sem trocar a marca.
3. **Elevar a estética** a um padrão premium, condizente com um negócio que já fatura bem.
4. **Reorganizar com estratégia:** serviços em destaque com link próprio cada, seção de oferta
   (ex.: sessão pontual / plano curto / plano longo), prova social com as avaliações reais.
5. **Todos os CTAs levam ao WhatsApp** da prospect. Incluir "agendar", localização e infos complementares.
6. **100% responsiva** (perfeita no celular). Testar o mobile de verdade antes de dar como pronto.

Seguir as regras de escrita e visuais da raiz (`_contexto/preferencias.md` e as regras anti-"cara de
IA": nada de traço/fio abrindo seção, sombra nunca preta, animação não mexe no texto). Nicho regulado
(saúde, jurídico, financeiro): nada de promessa de resultado.

**Deploy:** subir de graça. Se a raiz definir um deploy automático próprio (ex.: um script que sobe
por API), usar ele; senão, Netlify Drop / Vercel manual. Cada prospect num **slug próprio** e o
re-deploy no mesmo slug **atualiza o mesmo endereço** (não gera link novo a cada ajuste). Devolver o
link público.

#### Prompt-base da reconstrução (personalizar e usar)

```
Use a skill /frontend-design nesta tarefa.

PROSPECT: <nome>
URL DO SITE ATUAL: <url>

Quero uma NOVA VERSÃO da página desta pessoa, não uma página nova.

1. Acesse o site atual e extraia TODO o conteúdo real: serviços, textos, depoimentos,
   endereço, WhatsApp e redes. NÃO invente nada.
2. Mantenha a identidade: logo, paleta de cores e imagens originais. A pessoa precisa
   reconhecer que é a página dela, só que melhor.
3. Eleve a estética a um padrão premium, condizente com um negócio que já fatura bem.
4. Reorganize com estratégia: serviços em destaque com link próprio, seção de oferta e
   prova social com as avaliações.
5. TODOS os CTAs levam ao WhatsApp. Inclua "agendar", localização e infos complementares.
6. Deixe 100% responsiva (perfeita no celular).

Ao terminar, prepare pra subir no Netlify/Vercel no slug "proposta-<nome>" e me devolva o link.
```

### Passo 2 — Ofertar (a mensagem de proposta)

Gerar a mensagem (WhatsApp ou e-mail) a partir do contexto da própria sessão. **Sem preço** no
primeiro contato: preço cedo cheira a spam e faz a pessoa nem abrir o link.

#### Prompt-base da proposta (personalizar e usar)

```
Escreva uma mensagem curta de proposta pra este prospect, usando o contexto desta sessão.

DADOS:
- Nome/contato: <nome>
- Pontos fortes que vi (avaliações, especialidade, detalhe do trabalho): <...>
- Motivo da abordagem (o que estava fraco no site): <...>
- Link da página ANTIGA: <url>
- Link da página NOVA: <url>
- Assinatura: <nome/contato>

Regras:
1. Comece elogiando de verdade (rapport): mostre que viu o trabalho dela.
2. Diga que notou pontos a melhorar no site e que por isso montou uma NOVA VERSÃO da página dela.
3. Cite o que melhorou.
4. CTA claro pra ela ABRIR e navegar na página nova.
5. NÃO fale preço. Tom humano, próximo, sem cara de spam. Curto.
```

**Dica de conversão:** anexar um print do topo da página nova junto da mensagem aumenta o clique.

## O que entregar no fim

- Link público da página nova (Netlify/Vercel)
- A mensagem de proposta pronta pra colar
- (Opcional) print do topo pra anexar

Se a prospect responder e fechar, a pasta migra de `comercial/prospeccao/` pra `clientes/`. O redesign
completo (`/identidade` + `/diagnostico`) é uma entrega **opcional e separada** — roda só se ela
contratar isso. Caso contrário, segue-se mantendo a identidade dela, igual no aperitivo.
