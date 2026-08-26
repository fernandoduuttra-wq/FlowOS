# Rede: Instagram

`Tipo`: `Reel` ou `Carrossel`.

## Onde mora o gancho

**Reel:** os primeiros 3 segundos, e são **fala + visual ao mesmo tempo**. Registrar os dois no
`Hook original` (formato `Fala:` / `Visual:`). O visual costuma ser metade do gancho — texto na
tela, um objeto na mão, um corte seco, a cara de quem vai contar algo que não devia.

**Carrossel:** o **slide 1**, e ele é quase inteiramente visual. O gancho de carrossel tem que
funcionar sem som, sem contexto e do tamanho de um polegar no feed. Registrar o texto do slide 1
**e** como ele está diagramado (fonte grande? fundo de cor chapada? print? seta?).

**Sinal de força:** priorizar **comentários** (proxy nº1 de viralização real), depois a razão
comentário/like (alta = gerou conversa ou polêmica), likes só de desempate. Compartilhamentos e
salvamentos **não dá pra ver de fora** — o Instagram só mostra pro dono do post. Não prometer esses
números.

---

## Reel — entrada automática

Usar o plugin **`/watch`**: baixa o vídeo, transcreve (legenda nativa ou Whisper) e extrai os frames
pro Claude **assistir**, não só ler.

Ler só a transcrição de um reel é perder metade do conteúdo. A leitura visual pega o que a
transcrição não pega: texto na tela, ritmo de corte, autoridade de cena.

## Carrossel — entrada automática (rota padrão)

**Só o link basta.** Rodar:

```bash
python scripts/instagram-carrossel.py <url-do-post>
```

Baixa todos os slides em ordem (`01.jpg`, `02.jpg`, …) mais a `legenda.txt`, em
`%LOCALAPPDATA%\ig-carrossel\<shortcode>\`. Depois é só **ler as imagens com visão**, na ordem.

**Não pede login, conta, cookie nem sessão.** O script usa o *embed público*
(`instagram.com/p/<code>/embed/captioned/`) — a mesma página que qualquer site usa pra incorporar um
post — renderizando num Chrome headless e clicando o "Avançar" até o fim do carrossel. Como não há
sessão, não há conta pra rate-limitar nem bloquear.

Funciona também pra **foto única** (1 slide) e pra **reel** (baixa o frame de capa — pro reel em si,
usar o `/watch`, que pega áudio e movimento).

Requer `playwright` (`pip install playwright`) e o Chrome instalado. Nada é baixado pro repo — só o
brief destilado volta.

## Carrossel — entrada manual (fallback)

Se o post for privado, tiver sido removido, ou o script não achar slide nenhum:

> "Manda os prints dos slides (pode colar direto aqui). Se tiver a legenda do post, cola junto."

`Origem: Manual (colado)`.

## Como dissecar (vale pras duas rotas)

Dissecar **slide a slide**: slide 1 = gancho, miolo = desenvolvimento (numerar cada slide), último =
CTA. A legenda do post costuma carregar a CTA de verdade — ler junto.

## Coletar links em lote

Pra garimpar candidatos, `coletar-links.js` (nesta pasta) roda no console do Chrome:

1. Abrir `https://www.instagram.com/explore/search/keyword/?q=PALAVRA_CHAVE` no Chrome desktop
2. Rolar pra carregar bastante post
3. F12 → Console → colar o script → Enter
4. Ele copia a lista pro clipboard, separada em **REELS** (`/reel/`) e **CARROSSÉIS** (`/p/`)
5. Colar a lista de volta no chat

Dica: perfis **pequenos** (até ~50 mil) que viralizaram são o melhor sinal. Se um perfil sem
audiência estourou, o mérito é do conteúdo, não do alcance herdado.
