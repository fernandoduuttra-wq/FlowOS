#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy de site estatico na Vercel pela API (sem Node, sem CLI).

Gemeo do deploy-netlify.py. Existe porque o Netlify bloqueia a conta inteira
quando estoura credito ("Account credit usage exceeded"), e a entrega nao pode
ficar refem de um host so. Os dois sao intercambiaveis pra pagina estatica.

Uso:
  python scripts/deploy-vercel.py <pasta-ou-arquivo.html> --slug <slug>
      Sobe o conteudo. Se for arquivo, vira index.html. Se for pasta, precisa
      ter um index.html dentro. --slug identifica o projeto (reusa no
      re-deploy) e define o subdominio (slug.vercel.app).

  python scripts/deploy-vercel.py <pasta-de-midia> --slug <slug> --assets
      Modo biblioteca de midia: hospeda PNG/JPG/MP4 e imprime a URL publica de
      cada arquivo (mesmo papel do --assets do Netlify: o conector da Meta so
      aceita link publico direto).

  python scripts/deploy-vercel.py --list
      Lista os projetos ja criados (slug -> url).

Token: scripts/.vercel.token.txt (gitignored).
  Gerar em: vercel.com/account/settings/tokens

Mapa local de projetos: scripts/.vercel-projects.json (gitignored).

Detalhe da API: o endpoint /v13/deployments aceita os arquivos inline no corpo
(base64). Serve pra site estatico pequeno, que e o caso aqui. Arquivo grande
(video) passa pelo upload por SHA em /v2/files antes, e o deploy so referencia
o hash.
"""

import argparse
import base64
import hashlib
import json
import mimetypes
import pathlib
import sys
import time
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TOKEN = RAIZ / "scripts" / ".vercel.token.txt"
MAPA = RAIZ / "scripts" / ".vercel-projects.json"
API = "https://api.vercel.com"

# acima disso o arquivo sobe por /v2/files e o deploy so cita o SHA
LIMITE_INLINE = 3 * 1024 * 1024

EXT_MIDIA = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp4", ".mov", ".pdf"}


def token():
    if not TOKEN.exists() or not TOKEN.read_text(encoding="utf-8").strip():
        sys.exit(
            "Falta o token da Vercel.\n"
            f"  1. Gere em https://vercel.com/account/settings/tokens\n"
            f"  2. Cole em {TOKEN}\n"
            "O arquivo ja e gitignored (*.token.txt)."
        )
    return TOKEN.read_text(encoding="utf-8").strip()


def chamar(metodo, caminho, corpo=None, bruto=None, extra=None):
    cab = {"Authorization": "Bearer " + token()}
    dados = None
    if bruto is not None:
        dados = bruto
        cab["Content-Type"] = "application/octet-stream"
    elif corpo is not None:
        dados = json.dumps(corpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    if extra:
        cab.update(extra)
    req = urllib.request.Request(API + caminho, data=dados, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req) as r:
            texto = r.read().decode("utf-8")
            return json.loads(texto) if texto else {}
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "replace")
        sys.exit(f"Vercel respondeu {e.code} em {metodo} {caminho}:\n{detalhe}")


def ler_mapa():
    return json.loads(MAPA.read_text(encoding="utf-8")) if MAPA.exists() else {}


def gravar_mapa(m):
    MAPA.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")


def juntar_arquivos(origem, so_midia=False):
    """Devolve [(caminho-relativo-com-barra, bytes)]."""
    origem = pathlib.Path(origem)
    itens = []
    if origem.is_file():
        nome = "index.html" if origem.suffix.lower() in (".html", ".htm") else origem.name
        return [(nome, origem.read_bytes())]
    for p in sorted(origem.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if so_midia and p.suffix.lower() not in EXT_MIDIA:
            continue
        itens.append((p.relative_to(origem).as_posix(), p.read_bytes()))
    if not itens:
        sys.exit(f"Nada pra subir em {origem}")
    if not so_midia and not any(c == "index.html" for c, _ in itens):
        sys.exit(f"Falta index.html em {origem} (sem ele a Vercel nao serve a raiz).")
    return itens


def subir_grande(dado):
    """Arquivo grande vai antes pra /v2/files; o deploy so referencia o SHA."""
    sha = hashlib.sha1(dado).hexdigest()
    chamar(
        "POST",
        "/v2/files",
        bruto=dado,
        extra={"x-vercel-digest": sha, "Content-Length": str(len(dado))},
    )
    return sha


def garantir_projeto(slug):
    mapa = ler_mapa()
    if slug in mapa:
        return mapa[slug]
    # nao existe no mapa local: pode existir na conta (mapa e local, some se trocar de maquina)
    try:
        proj = chamar("GET", f"/v9/projects/{slug}")
    except SystemExit:
        proj = None
    if not proj or not proj.get("id"):
        proj = chamar("POST", "/v11/projects", {"name": slug, "framework": None})
    registro = {"id": proj["id"], "name": proj["name"], "url": f"https://{proj['name']}.vercel.app"}
    mapa[slug] = registro
    gravar_mapa(mapa)
    return registro


def deploy(origem, slug, so_midia=False):
    projeto = garantir_projeto(slug)
    itens = juntar_arquivos(origem, so_midia)

    arquivos = []
    for caminho, dado in itens:
        if len(dado) > LIMITE_INLINE:
            sha = subir_grande(dado)
            arquivos.append({"file": caminho, "sha": sha, "size": len(dado)})
            print(f"  {caminho}  ({len(dado)//1024} KB, por SHA)")
        else:
            arquivos.append(
                {
                    "file": caminho,
                    "data": base64.b64encode(dado).decode("ascii"),
                    "encoding": "base64",
                }
            )
            print(f"  {caminho}  ({len(dado)//1024} KB)")

    corpo = {
        "name": projeto["name"],
        "project": projeto["id"],
        "files": arquivos,
        "target": "production",
        "projectSettings": {
            "framework": None,
            "buildCommand": None,
            "outputDirectory": None,
            "installCommand": None,
        },
    }
    dep = chamar("POST", "/v13/deployments?skipAutoDetectionConfirmation=1", corpo)

    # espera sair de QUEUED/BUILDING pra nao anunciar endereco que ainda da 404
    ident = dep.get("id")
    estado = dep.get("readyState") or dep.get("status")
    for _ in range(60):
        if estado in ("READY", "ERROR", "CANCELED"):
            break
        time.sleep(2)
        estado = chamar("GET", f"/v13/deployments/{ident}").get("readyState")
    print(f"\nestado: {estado}")
    if estado != "READY":
        sys.exit("Deploy nao ficou pronto. Confere em vercel.com/dashboard")

    print(f"no ar:  {projeto['url']}")
    if so_midia:
        print("\nURLs publicas:")
        for caminho, _ in itens:
            print(f"  {projeto['url']}/{caminho}")
    return projeto["url"]


def main():
    ap = argparse.ArgumentParser(description="Deploy estatico na Vercel pela API.")
    ap.add_argument("origem", nargs="?", help="pasta ou arquivo .html")
    ap.add_argument("--slug", help="identifica o projeto e vira o subdominio")
    ap.add_argument("--assets", action="store_true", help="modo biblioteca de midia")
    ap.add_argument("--list", action="store_true", help="lista os projetos ja criados")
    a = ap.parse_args()

    if a.list:
        mapa = ler_mapa()
        if not mapa:
            print("Nenhum projeto ainda.")
        for slug, p in mapa.items():
            print(f"  {slug:24} {p['url']}")
        return

    if not a.origem or not a.slug:
        ap.error("passe a pasta/arquivo e o --slug (ou use --list)")
    if not pathlib.Path(a.origem).exists():
        sys.exit(f"Nao achei: {a.origem}")

    deploy(a.origem, a.slug, a.assets)


if __name__ == "__main__":
    main()
