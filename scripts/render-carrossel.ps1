<#
  render-carrossel.ps1 — renderiza slides HTML em PNG 1080x1350 usando Chrome/Edge headless.
  Não precisa de Node nem Playwright. Substitui o render.js da skill /carrossel.

  Uso:
    powershell -ExecutionPolicy Bypass -File scripts/render-carrossel.ps1 -Folder "marketing/conteudo/<pasta-do-conteudo>"

  O que faz:
    - Procura todos os arquivos slide-*.html dentro de -Folder
    - Renderiza cada um em <Folder>/instagram/slide-NN.png a 1080x1350
    - Usa Chrome se existir, senão Edge (ambos vêm com headless screenshot)

  Parâmetros:
    -Folder    (obrigatório) pasta do conteúdo, com os slide-*.html
    -Width     largura (default 1080)
    -Height    altura  (default 1350)
    -Out       subpasta de saída (default "instagram"); use "tiktok" pra 1080x1920
#>
param(
  [Parameter(Mandatory=$true)][string]$Folder,
  [int]$Width = 1080,
  [int]$Height = 1350,
  [string]$Out = "instagram"
)

$ErrorActionPreference = "Stop"

function Find-Browser {
  $candidates = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
  )
  foreach ($c in $candidates) { if (Test-Path $c) { return $c } }
  throw "Nenhum navegador encontrado (Chrome ou Edge). Instale um dos dois."
}

$browser = Find-Browser
$Folder  = (Resolve-Path $Folder).Path
$outDir  = Join-Path $Folder $Out
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

$slides = Get-ChildItem -Path $Folder -Filter "slide-*.html" | Sort-Object Name
if ($slides.Count -eq 0) { throw "Nenhum slide-*.html em $Folder" }

# IMPORTANTE (gotcha desta maquina): o Chrome nativo NAO escreve --screenshot em
# caminho > 260 chars (MAX_PATH). O repo vive sob um caminho longo e acentuado do
# OneDrive, entao renderizar direto no destino FALHA em todos os slides. Solucao:
# renderizar num caminho CURTO em %LOCALAPPDATA% e copiar o PNG de volta (o copy
# do PowerShell/.NET lida com caminho longo; o Chrome nao).
$work = Join-Path $env:LOCALAPPDATA "flowos-render-$(Get-Random)"
$tmp  = Join-Path $work "prof"
New-Item -ItemType Directory -Path $work -Force | Out-Null

# O HTML vai sozinho pro caminho curto, entao imagem referenciada por caminho
# relativo (foto de capa, print de tela) quebraria. Copiamos os assets junto,
# mantendo os mesmos nomes que o HTML usa.
Get-ChildItem -Path $Folder -File |
  Where-Object { $_.Extension -match '^\.(png|jpg|jpeg|webp|gif|svg|avif)$' } |
  ForEach-Object { Copy-Item $_.FullName (Join-Path $work $_.Name) -Force }

# Chrome/Edge escrevem no stderr mesmo quando dão certo. Redirecionamos pra nao
# poluir o stream de erro do PowerShell.
$errLog = Join-Path $work "chrome-stderr.log"

foreach ($s in $slides) {
  $name = [System.IO.Path]::GetFileNameWithoutExtension($s.Name)  # slide-01
  # copia o HTML pro caminho curto, renderiza ao lado, copia o PNG de volta
  $shortHtml = Join-Path $work "$name.html"
  Copy-Item $s.FullName $shortHtml -Force
  $shortPng  = Join-Path $work "$name.png"
  $uri = ([uri]$shortHtml).AbsoluteUri
  # --disable-lcd-text: sem ele o Chrome no Windows renderiza o texto com antialias
  # SUBPIXEL, e o PNG sai com franja vermelha/azul na borda das letras (aparece feio
  # quando o Instagram redimensiona). A flag força antialias em escala de cinza.
  # O CSS -webkit-font-smoothing NAO resolve: so tem efeito no macOS.
  $args = @(
    '--headless=new','--disable-gpu','--no-sandbox','--hide-scrollbars',
    '--disable-lcd-text','--font-render-hinting=none',
    '--force-device-scale-factor=1', "--window-size=$Width,$Height",
    '--virtual-time-budget=5000', "--user-data-dir=$tmp",
    "--screenshot=$shortPng", $uri
  )
  # --headless=new evita o Chrome entregar pra uma janela já aberta (que não gera o PNG)
  Start-Process -FilePath $browser -ArgumentList $args -Wait -NoNewWindow -RedirectStandardError $errLog
  if (Test-Path $shortPng) {
    Copy-Item $shortPng (Join-Path $outDir "$name.png") -Force
    Write-Host "OK  $name.png"
  } else {
    Write-Host "FALHOU  $name"
  }
}

if (Test-Path $work) { Remove-Item $work -Recurse -Force -ErrorAction SilentlyContinue }
Write-Host "Renderizado em: $outDir"
