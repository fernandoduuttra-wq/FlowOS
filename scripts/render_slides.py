# -*- coding: utf-8 -*-
r"""
render_slides.py -- renderiza slide-*.html em PNG usando Chrome/Edge headless.

Porte fiel de scripts/render-carrossel.ps1 pra Python. Existe porque toda
politica de execucao persistente desta maquina esta Undefined (= Restricted):
o .ps1 so roda quando quem chama ja esta num processo com policy Bypass. Um
subprocesso lancado pelo painel (ou por qualquer script) morre com
PSSecurityException, e forcar -ExecutionPolicy Bypass e acao de seguranca que
nao se faz por conveniencia. Python nao passa por policy nenhuma.

Uso:
    python scripts/render_slides.py --pasta marketing/conteudo/<pasta>
    python scripts/render_slides.py --pasta <pasta> --largura 1080 --altura 1920 --saida tiktok

ATENCAO -- ha duas implementacoes do mesmo render hoje (esta e o .ps1). Elas
foram verificadas byte a byte quando este arquivo nasceu. Mudanca de flag tem
que entrar nas duas, ou o .ps1 deve virar um wrapper de 2 linhas em cima daqui.
"""

import argparse
import os
import random
import shutil
import subprocess
import sys
import re

EXT_ASSET = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif")


def longo(caminho):
    r"""Prefixa \\?\ pra escapar do MAX_PATH de 260 chars no Windows."""
    p = os.path.abspath(caminho)
    if os.name != "nt":
        return p
    p = p.replace("/", "\\")
    if p.startswith("\\\\?\\"):
        return p
    if p.startswith("\\\\"):
        return "\\\\?\\UNC\\" + p[2:]
    unidade, resto = os.path.splitdrive(p)
    return "\\\\?\\" + unidade.upper() + resto


def achar_navegador():
    pf = os.environ.get("ProgramFiles", r"C:\Program Files")
    pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    for c in (
        os.path.join(pf, "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(pf86, "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(pf, "Microsoft", "Edge", "Application", "msedge.exe"),
        os.path.join(pf86, "Microsoft", "Edge", "Application", "msedge.exe"),
    ):
        if os.path.isfile(c):
            return c
    raise RuntimeError("Nenhum navegador encontrado (Chrome ou Edge). Instale um dos dois.")


def renderizar(pasta, largura=1080, altura=1350, saida="instagram", log=None):
    """Renderiza todos os slide-*.html da pasta. Devolve (ok, linhas_de_log)."""
    linhas = []

    def anotar(txt):
        linhas.append(txt)
        if log:
            log(txt)

    navegador = achar_navegador()
    pasta = os.path.abspath(pasta)
    dir_saida = os.path.join(pasta, saida)
    os.makedirs(longo(dir_saida), exist_ok=True)

    slides = sorted(
        (n for n in os.listdir(longo(pasta)) if re.match(r"^slide-\d+\.html$", n, re.I)),
        key=lambda n: int(re.search(r"\d+", n).group()),
    )
    if not slides:
        raise RuntimeError("Nenhum slide-*.html em %s" % pasta)

    # O Chrome nativo NAO escreve --screenshot em caminho > 260 chars (MAX_PATH),
    # e o repo vive sob um caminho longo e acentuado do OneDrive: renderizar direto
    # no destino falha em todos os slides. Renderizamos num caminho CURTO em
    # %LOCALAPPDATA% e copiamos o PNG de volta (o copy do Python lida com caminho
    # longo via \\?\; o Chrome nao).
    base = os.environ.get("LOCALAPPDATA") or os.environ.get("TMP") or "."
    trabalho = os.path.join(base, "flowos-render-%d" % random.randint(100000, 999999))
    perfil = os.path.join(trabalho, "prof")
    os.makedirs(longo(trabalho), exist_ok=True)

    try:
        # O HTML vai sozinho pro caminho curto, entao imagem referenciada por
        # caminho relativo quebraria. Copiamos os assets junto, com os mesmos nomes.
        for nome in os.listdir(longo(pasta)):
            origem = os.path.join(pasta, nome)
            if os.path.isfile(longo(origem)) and nome.lower().endswith(EXT_ASSET):
                shutil.copyfile(longo(origem), longo(os.path.join(trabalho, nome)))

        falhou = []
        for nome in slides:
            base_nome = os.path.splitext(nome)[0]
            html_curto = os.path.join(trabalho, base_nome + ".html")
            png_curto = os.path.join(trabalho, base_nome + ".png")
            shutil.copyfile(longo(os.path.join(pasta, nome)), longo(html_curto))
            uri = "file:///" + html_curto.replace("\\", "/")

            comando = [
                navegador,
                "--headless=new",          # sem isso o Chrome entrega pra uma janela ja aberta e nao gera o PNG
                "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                # --disable-lcd-text: sem ele o Chrome no Windows usa antialias SUBPIXEL
                # e o PNG sai com franja vermelha/azul na borda das letras (fica feio
                # quando o Instagram redimensiona). O CSS -webkit-font-smoothing NAO
                # resolve: so tem efeito no macOS.
                "--disable-lcd-text", "--font-render-hinting=none",
                "--force-device-scale-factor=1",
                "--window-size=%d,%d" % (largura, altura),
                "--virtual-time-budget=5000",
                "--user-data-dir=" + perfil,
                "--screenshot=" + png_curto,
                uri,
            ]
            subprocess.run(comando, capture_output=True, timeout=120)

            if os.path.isfile(longo(png_curto)):
                shutil.copyfile(longo(png_curto), longo(os.path.join(dir_saida, base_nome + ".png")))
                anotar("OK  %s.png" % base_nome)
            else:
                falhou.append(base_nome)
                anotar("FALHOU  %s" % base_nome)

        anotar("Renderizado em: %s" % dir_saida)
        return (not falhou), linhas
    finally:
        shutil.rmtree(longo(trabalho), ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="Renderiza slide-*.html em PNG (Chrome/Edge headless)")
    ap.add_argument("--pasta", required=True)
    ap.add_argument("--largura", type=int, default=1080)
    ap.add_argument("--altura", type=int, default=1350)
    ap.add_argument("--saida", default="instagram")
    a = ap.parse_args()
    try:
        ok, _ = renderizar(a.pasta, a.largura, a.altura, a.saida, log=lambda t: print(t, flush=True))
    except Exception as exc:
        print("ERRO: %s" % exc)
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
