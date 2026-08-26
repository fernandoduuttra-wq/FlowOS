"""Baixa todos os slides de um post do Instagram (carrossel, foto ou reel) sem login.

Usa o embed publico (instagram.com/p/<code>/embed/captioned/), que o Instagram
serve pra qualquer visitante — nao precisa de conta, cookie nem sessao, entao
nao ha risco de rate-limit ou bloqueio como no instaloader.

O embed carrega os slides sob demanda, entao o script abre a pagina num Chrome
headless e clica o "Avancar" ate o fim, guardando a URL assinada de cada slide.

Uso:
    python scripts/instagram-carrossel.py <url-ou-shortcode> [--saida DIR] [--visivel]

Saida (default): %LOCALAPPDATA%\\ig-carrossel\\<shortcode>\\
    01.jpg, 02.jpg, ...   os slides, na ordem
    legenda.txt           a legenda do post
Fica FORA do OneDrive de proposito (caminho acentuado + MAX_PATH quebram
midia por la); so o brief destilado deve voltar pro repo.

Requer: playwright (pip install playwright) e o Chrome ja instalado.
"""

import argparse
import os
import re
import sys
import urllib.request

from playwright.sync_api import sync_playwright

# aria-label do botao muda com o idioma que o Instagram detecta
ROTULOS_AVANCAR = ("Avançar", "Next", "Siguiente", "Suivant", "Weiter", "Avanti")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

MAX_SLIDES = 40  # trava de seguranca: carrossel do IG vai ate 20


def shortcode(alvo):
    m = re.search(r"instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)", alvo)
    if m:
        return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{5,}", alvo):
        return alvo
    sys.exit(f"nao reconheci '{alvo}' como URL ou shortcode do Instagram")


def id_midia(url):
    m = re.search(r"/([0-9]{6,}_[0-9]+_[0-9]+_n)\.", url)
    return m.group(1) if m else None


def coletar(code, visivel):
    """Abre o embed, percorre o carrossel e devolve (urls dos slides, legenda)."""
    url = f"https://www.instagram.com/p/{code}/embed/captioned/"
    slides, legenda = [], ""

    with sync_playwright() as p:
        navegador = p.chromium.launch(channel="chrome", headless=not visivel)
        pagina = navegador.new_page(viewport={"width": 700, "height": 1000},
                                    user_agent=UA)
        pagina.goto(url, wait_until="networkidle", timeout=60000)
        pagina.wait_for_timeout(1500)

        if "não está disponível" in pagina.content() or "isn't available" in pagina.content():
            navegador.close()
            sys.exit(f"post {code} indisponivel (removido, privado ou shortcode errado)")

        # a foto do perfil vive noutro host; so o t51.*-15 e midia do post
        def visiveis():
            return pagina.eval_on_selector_all(
                "img",
                "els => els.filter(e => e.naturalWidth > 200).map(e => e.src)",
            )

        for u in visiveis():
            if id_midia(u):
                slides.append(u)

        for _ in range(MAX_SLIDES):
            botao = None
            for rotulo in ROTULOS_AVANCAR:
                cand = pagina.locator(f'button[aria-label="{rotulo}"]')
                if cand.count() and cand.first.is_visible():
                    botao = cand.first
                    break
            if botao is None:  # foto unica, reel, ou fim do carrossel
                break

            botao.click()
            pagina.wait_for_timeout(900)
            novos = [u for u in visiveis() if id_midia(u)]
            if not any(id_midia(u) not in {id_midia(s) for s in slides} for u in novos):
                break  # nada novo entrou: chegamos no fim
            slides.extend(novos)

        try:
            legenda = pagina.locator(".Caption").first.inner_text(timeout=3000)
        except Exception:
            legenda = ""

        navegador.close()

    # dedup preservando a ordem em que os slides apareceram
    unicos, vistos = [], set()
    for u in slides:
        k = id_midia(u)
        if k not in vistos:
            vistos.add(k)
            unicos.append(u)
    return unicos, legenda


def baixar(urls, legenda, destino):
    os.makedirs(destino, exist_ok=True)
    cab = {"User-Agent": UA, "Referer": "https://www.instagram.com/"}
    salvos = []
    for i, u in enumerate(urls, 1):
        req = urllib.request.Request(u, headers=cab)
        dados = urllib.request.urlopen(req, timeout=60).read()
        caminho = os.path.join(destino, f"{i:02d}.jpg")
        with open(caminho, "wb") as f:
            f.write(dados)
        salvos.append(caminho)
        print(f"  {i:02d}.jpg  {len(dados) // 1024} kb")
    if legenda:
        with open(os.path.join(destino, "legenda.txt"), "w", encoding="utf8") as f:
            f.write(legenda)
    return salvos


def main():
    ap = argparse.ArgumentParser(description="Baixa os slides de um post do Instagram sem login")
    ap.add_argument("alvo", help="URL do post ou shortcode")
    ap.add_argument("--saida", help="pasta de destino")
    ap.add_argument("--visivel", action="store_true", help="mostra o navegador (pra depurar)")
    args = ap.parse_args()

    code = shortcode(args.alvo)
    destino = args.saida or os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "ig-carrossel", code)

    print(f"post {code} -> {destino}")
    urls, legenda = coletar(code, args.visivel)
    if not urls:
        sys.exit("nenhum slide encontrado — rode com --visivel pra ver o que a pagina mostrou")
    print(f"{len(urls)} slide(s):")
    baixar(urls, legenda, destino)
    print("pronto" + (f" | legenda: {len(legenda)} chars" if legenda else " | sem legenda"))


if __name__ == "__main__":
    main()
