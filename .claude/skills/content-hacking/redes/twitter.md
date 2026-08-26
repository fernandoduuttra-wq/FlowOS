# Rede: Twitter / X

`Tipo`: `Tweet` (avulso) ou `Thread`.

## Onde mora o gancho

**O primeiro tweet, e ele tem que fechar sozinho.** Na timeline não existe "arraste pro lado": se o
tweet 1 não entrega uma ideia inteira, o resto da thread nem é vista. Registrar no
`Hook original` o tweet 1 **completo**, com as quebras de linha — a diagramação do texto (frase
curta, linha em branco, frase curta) é parte do gancho, não formatação.

**Sinal de força:** priorizar **citações** (quote tweets) e respostas — são o proxy de conversa
gerada. Retweet e like desempatam. Visualização aparece pra todo mundo aqui, mas é o número mais
inflado: não usar sozinho como prova de que funcionou.

---

## Entrada

**Manual, por padrão.** O usuário cola o texto do tweet ou da thread, ou manda o print. Não há rota
automática confiável: a API do X é paga e a raspagem quebra a cada mudança de layout.

Se vier print, ler a imagem e transcrever o texto **literal**, inclusive as quebras de linha.

---

## O formato como motor (ler antes de dissecar)

Print de tweet é o caso clássico da segunda trava desta skill: **o formato carrega significado
sozinho.** Ele lê como registro do que aconteceu, não como peça produzida pra convencer. Um tweet
dissecado e reembalado na identidade visual da marca costuma perder exatamente o que fazia
funcionar.

Por isso, ao dissecar conteúdo desta rede, registrar sempre **se o formato é motor ou veículo**:

- **Motor** — a peça derivada deve nascer também em print de tweet. Produção pela skill
  `/post-twitter`, que não usa o `design.json` de propósito.
- **Veículo** — só o texto importa, e a peça pode sair na identidade da marca pela `/carrossel`.

Um sinal prático: se o texto depende de soar como algo que a pessoa *falou*, é motor. Se ele
funciona como argumento diagramado, é veículo.

---

## Da dissecação até a peça

O roteiro cadastrado no Notion é a fonte da verdade. **O usuário edita lá antes de produzir**, e a
peça sai do texto literal do registro — a `/post-twitter` não reescreve nada.

Estrutura desta rede que já tiver provado que funciona vira modelo salvo no banco, e da próxima vez
entra direto, sem passar por dissecação de novo.
