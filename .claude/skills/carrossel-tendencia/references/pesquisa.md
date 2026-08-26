# Pesquisa — as âncoras que sustentam a peça

O formato inteiro se apoia em **âncora**: fato público, verificável, datado, que o leitor pode
conferir sozinho. Âncora é o que separa este formato de opinião com fonte bonita.

> A peça não pede pro leitor acreditar. Ela mostra a tela.

## O que conta como âncora

Uma âncora precisa das quatro:

1. **Pública** — está publicada em algum lugar que o leitor consegue alcançar.
2. **Verificável** — dá pra checar. Tem fonte, autor ou URL.
3. **Datada** — quando aconteceu. "Recentemente" não é data.
4. **Concreta** — número, nome próprio, evento, declaração. Não é tendência genérica.

| É âncora | Não é âncora |
|---|---|
| "A empresa X cortou 30% do time de suporte em março/26 e disse por quê" | "empresas estão cortando times por causa da IA" |
| "O vídeo de fulano sobre isso passou de 2 milhões em 4 dias" | "esse assunto viralizou" |
| "A plataforma mudou a regra Y no dia Z" | "o algoritmo mudou" |
| Um print da própria tela com o resultado e a data | "os resultados foram ótimos" |

**A âncora mais forte de todas é a que quem publica tem em primeira mão** — o print do próprio
painel, o número do próprio cliente, o erro que aconteceu na própria operação. Ela é inimitável e
não precisa de fonte externa. Procurar essa primeiro, no `_contexto/` e perguntando ao usuário,
antes de sair pesquisando fora.

## Quantas

**3 a 6.** Menos que 3, a peça fica frágil e o leitor sente. Mais que 6, vira reportagem e o
argumento se dilui — o formato não é jornalismo, é leitura de fenômeno.

Distribuição típica num carrossel de 10 slides: 1 âncora derruba a crença (Zona 1), 2 a 3
sustentam o mecanismo (Zona 2), 1 serve de contraexemplo (Zona 3), 1 é a prova acumulada de quem
publica (Zona 4).

## Como pesquisar

**Ferramentas nativas, nesta ordem:**

1. **`WebSearch`** — para descobrir o que existe. Buscar em português E em inglês: o fenômeno
   costuma ter sido nomeado lá fora antes. Buscar o termo, o contra-termo, e o nome de quem
   discorda.
2. **`WebFetch`** — para ler a fonte de verdade antes de citar. **Nunca citar a partir do snippet
   de busca.** Snippet corta ressalva e inverte sentido.
3. **O material do próprio usuário** — `_contexto/`, pastas de cliente, o que ele colou na conversa.

**Se o workspace tiver um buscador dedicado configurado** (MCP de pesquisa, API de notícias), o
`CLAUDE.md` da raiz diz qual é e ele vira o passo 1. Não é obrigatório: `WebSearch` + `WebFetch`
resolvem o formato. Um buscador dedicado ganha em duas coisas específicas — recência de horas
(notícia quente) e citação já com URL — que valem quando o eixo é NOTÍCIAS.

## Roteiro de busca por eixo

| Eixo | O que procurar |
|---|---|
| **MERCADO** | mudança de regra, preço, players entrando/saindo, relatório setorial recente |
| **CASES** | quem fez, o número, o prazo, e principalmente **quem tentou e quebrou** |
| **CULTURA** | comportamento com nome próprio, meme, mudança de hábito com dado |
| **NOTÍCIAS** | o fato das últimas 72h + a reação de quem entende do assunto |
| **PRODUTO** | o que a própria operação de quem publica registrou — print, número, cliente |

## Regras duras

- **Não inventar.** Se a busca não confirmou número, data ou autoria, a frase não entra na peça.
  Não arredondar pra cima, não estimar, não escrever "cerca de" pra disfarçar que não se sabe.
- **Ler a fonte antes de citar.** Título e snippet mentem por omissão.
- **Registrar cada âncora com a fonte** durante a Etapa 1, mesmo que a fonte não apareça na peça.
  O usuário pode ser questionado nos comentários e precisa ter onde apoiar.
- **Não acusar.** Âncora sustenta o fenômeno, não vira dossiê contra uma pessoa ou empresa.
  "A prática X se espalhou" passa; "a empresa Y engana o cliente" não.
- **A pesquisa não vira resposta.** Ela abastece a triagem e some. Não devolver ao usuário um
  relatório de pesquisa antes da Etapa 2.

## Quando a pesquisa não fecha

Se depois de buscar não houver 3 âncoras que passem no teste, **não improvisar peça mesmo assim.**
Duas saídas honestas:

1. Pedir material observável ao usuário — em uma frase, dizendo exatamente o que falta
   ("preciso de um caso concreto com nome e data; o que eu achei é tudo genérico").
2. Trocar o ângulo: às vezes o tema não tem âncora, mas o **contra-tema** tem.
