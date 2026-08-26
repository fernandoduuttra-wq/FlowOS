<#
  coleta-youtube.ps1 — Coleta completa de um ALVO no YouTube.
  Gera: numeros (JSON), transcricao (.srt/.vtt), frames por mudanca de cena, thumbnail.

  Dois usos:
    PROSPECCAO (padrao) — analisa um alvo/concorrente. Saida em prospects\<Nome>\youtube\.
    CONTENT HACKING — modelar virais. A skill /content-hacking passa -SaidaBase
                      apontando pro _hacking, e o material alimenta a analise das 5 dimensoes.

  ARQUITETURA (importante): o trabalho pesado (yt-dlp/ffmpeg) roda numa pasta TEMP fora do
  OneDrive. Dentro do OneDrive, sob caminho acentuado, os arquivos que o yt-dlp/ffmpeg gravam
  somem/desidratam e a releitura falha. No fim, o PowerShell COPIA o resultado pro destino
  (a copia feita pelo PowerShell persiste no OneDrive). Caminhos curtos 8.3 evitam o bug de acento.

  USO:
    # Numeros de TODOS os videos do canal (rapido, sem baixar video):
    .\coleta-youtube.ps1 -Nome "alvo" -Canal "https://www.youtube.com/@canal" -ModoCanal

    # Coleta profunda de UM video (numeros + transcricao + frames):
    .\coleta-youtube.ps1 -Nome "alvo" -Video "https://youtu.be/XXXX"

    # Mesma coleta, mas direcionando a saida (content hacking):
    .\coleta-youtube.ps1 -Nome "viral" -Video "https://youtu.be/XXXX" -SaidaBase "D:\...\_hacking\palavra-data\youtube"
#>
param(
  [Parameter(Mandatory=$true)][string]$Nome,
  [string]$Canal,
  [string]$Video,
  [switch]$ModoCanal,
  [double]$LimiarCena = 0.30,  # sensibilidade da deteccao de cena (0.2 = mais frames, 0.4 = menos)
  [string]$SaidaBase           # opcional: pasta-base de saida. Vazio = prospects\<Nome>\youtube (prospeccao).
                               # A skill /content-hacking passa o _hacking aqui pra modelagem de virais.
)

# --- garante PATH com yt-dlp/ffmpeg nesta sessao ---
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

$fso = New-Object -ComObject Scripting.FileSystemObject
function ShortPath($p) { $fso.GetFolder((Resolve-Path -LiteralPath $p).Path).ShortPath }

# Saida SEMPRE num cache local FORA do OneDrive. Motivo: dentro do OneDrive, sob caminho acentuado,
# os arquivos que o yt-dlp/ffmpeg gravam somem/desidratam e a releitura falha (ate o Copy-Item falha).
# Midia pesada (video + frames) nao deve mesmo ir pro repo sincronizado. A analise le deste cache;
# so os briefs destilados vao pro repo (gravados pelas ferramentas do Claude, que funcionam).
# -SaidaBase so deve ser usado se apontar pra um caminho NAO-OneDrive; senao deixa o padrao.
if ($SaidaBase) { $work = $SaidaBase } else { $work = Join-Path $env:LOCALAPPDATA ("flowos-content\" + $Nome + "\youtube") }
$null = New-Item -ItemType Directory -Force -Path $work
$workShort = ShortPath $work

if ($ModoCanal) {
  if (-not $Canal) { Write-Error "Informe -Canal no modo canal."; exit 1 }
  Write-Host ">> Coletando numeros do canal: $Canal" -ForegroundColor Cyan
  yt-dlp --flat-playlist --dump-json "$Canal/videos" | Out-File -FilePath "$workShort\canal-videos.json" -Encoding utf8
  Write-Host ">> Salvo: $work\canal-videos.json" -ForegroundColor Green
  exit 0
}

if (-not $Video) { Write-Error "Informe -Video (ou use -ModoCanal com -Canal)."; exit 1 }

# Pasta de trabalho isolada do video (na TEMP)
$id = (yt-dlp --print id "$Video").Trim()
$vwork = Join-Path $work "video-$id"
$null = New-Item -ItemType Directory -Force -Path (Join-Path $vwork "frames")
$vwShort = ShortPath $vwork

Write-Host ">> 1/4 Metadados e numeros..." -ForegroundColor Cyan
yt-dlp --dump-json "$Video" | Out-File "$vwShort\metadados.json" -Encoding utf8

Write-Host ">> 2/4 Transcricao..." -ForegroundColor Cyan
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "pt.*,en.*" `
       --convert-subs srt -o "$vwShort\%(id)s.%(ext)s" "$Video"

Write-Host ">> 3/4 Baixando video (qualidade media p/ frames)..." -ForegroundColor Cyan
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" --merge-output-format mp4 -o "$vwShort\fonte.mp4" "$Video"

Write-Host ">> 4/4 Extraindo frames por mudanca de cena..." -ForegroundColor Cyan
ffmpeg -hide_banner -loglevel error -i "$vwShort\fonte.mp4" -vf "select='gt(scene,$LimiarCena)',showinfo" -vsync vfr "$vwShort\frames\cena_%03d.jpg"
ffmpeg -hide_banner -loglevel error -i "$vwShort\fonte.mp4" -vf "fps=1" -frames:v 3 "$vwShort\frames\inicio_%02d.jpg"

$n = (Get-ChildItem (Join-Path $vwork "frames") -Filter *.jpg -ErrorAction SilentlyContinue).Count
Write-Host ">> CONCLUIDO. Frames: $n" -ForegroundColor Green
Write-Host ">> Pasta (cache local, ler daqui): $vwork" -ForegroundColor Green
