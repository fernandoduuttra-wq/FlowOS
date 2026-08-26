# Rede: YouTube

`Tipo`: `Vídeo longo` ou `Short`.

## Onde mora o gancho

**O título é o gancho.** Não a primeira frase do vídeo — o título. É ele que decide se o vídeo é
clicado, e vídeo não clicado não existe. Ogilvy: o título é 80 centavos do seu dólar.

O gancho do YouTube é composto de **três coisas que trabalham juntas**, e as três entram no
`Hook original`:

1. **Título** — a promessa
2. **Thumbnail** — o contraste visual que sustenta a promessa
3. **Primeiros 15 segundos** — a entrega antecipada que impede o "voltar"

No YouTube o espectador já escolheu clicar. O trabalho dos primeiros segundos não é fisgar do zero,
é **confirmar** que a promessa do título vai ser cumprida. Vídeo que abre se apresentando ("fala
galera, aqui é o...") quebra isso.

Por isso, no `Hook com variáveis`, o esqueleto do **título** é o ativo mais valioso da referência.

## Entrada — automática

```powershell
# Garimpar outperformers de um canal (descobrir O QUE dissecar)
scripts/coleta-youtube.ps1 -Nome "<keyword>" -Canal "https://www.youtube.com/@CANAL" -ModoCanal

# Coleta profunda de um vídeo (dissecar de fato)
scripts/coleta-youtube.ps1 -Nome "<keyword>" -Video "https://youtu.be/XXXX"
```

**`-ModoCanal`** gera `canal-videos.json` (uma linha por vídeo, com views). Ordenar por
**views ÷ inscritos**: os que estão muito acima da média do canal são os virais reais. Esse número
é a **demanda comprovada** — e vai pro critério 3 do campo `Por que`.

**Coleta profunda** gera, por vídeo: `metadados.json` (título, views), transcrição `.vtt`/`.srt` e
`frames/` (cenas + os 3 primeiros segundos).

Se o usuário já mandou o link do vídeo, pular o `-ModoCanal` e ir direto pra coleta profunda.

**Requisitos:** `yt-dlp` **nightly** com `yt-dlp-ejs` (o stable dá 403 no download — o YouTube exige
resolver um desafio JS) + `ffmpeg`.

**Onde cai:** cache local em `%LOCALAPPDATA%\mazyos-hack\<Nome>\youtube\video-<id>\`. **Nunca**
apontar `-SaidaBase` pro OneDrive — sob caminho acentuado os arquivos desidratam e somem.

## Como dissecar

Cruzar a transcrição `.srt` com os `frames/`:

- **Título + thumbnail** → o gancho. Analisar os dois juntos: a thumb costuma dizer o que o título
  omite de propósito (a lacuna de curiosidade mora aí).
- **Primeiros 15s** → como ele confirma a promessa e mata o "voltar".
- **Retenção** → onde estão os loops abertos, as promessas de "daqui a pouco eu mostro", os cortes.
- **Ouro** → o dado, o framework, a demonstração. É o que faz o vídeo ser lembrado.
- **CTA** → inscrever / comentar / link.

## Entrada — manual

Se o `yt-dlp` falhar ou o usuário preferir: ele cola o **título + a transcrição** (o próprio YouTube
expõe em "Mostrar transcrição") e, se quiser, um print da thumbnail. Processar normal, com
`Origem: Manual (colado)`.
