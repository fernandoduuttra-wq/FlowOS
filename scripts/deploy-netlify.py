#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy de site estatico no Netlify pela API (sem Node, sem arrasta-e-solta).

Substitui o Netlify Drop manual: sobe os arquivos pela API usando o metodo de
digest (SHA1 por arquivo), que preserva o Content-Type certo (index.html vira
text/html, nao text/plain). Cada cliente/slug fica num site proprio e reusavel:
re-deploy no mesmo slug atualiza o mesmo endereco.

Uso:
  python scripts/deploy-netlify.py <pasta-ou-arquivo.html> --slug <slug>
      Sobe o conteudo. Se for arquivo, vira index.html. Se for pasta, precisa
      ter um index.html dentro. --slug identifica o site (reusa no re-deploy) e
      define o subdominio (slug.netlify.app, ou slug-xxxx se o nome ja existir).

  python scripts/deploy-netlify.py <pasta-de-midia> --slug <slug> --assets
      Modo biblioteca de midia: hospeda PNG/JPG/MP4 e imprime a URL publica de
      cada arquivo. Serve pra subir criativo pelo conector MCP da Meta, que so
      aceita link publico direto (arquivo local, Drive e Dropbox nao funcionam).

  python scripts/deploy-netlify.py --list
      Lista os sites ja criados (slug -> url).

  python scripts/deploy-netlify.py --rename <slug> --nome <novo-nome>
      Renomeia o subdominio de um site existente.

Token: scripts/.netlify.token.txt (gitignored).
  Gerar em: app.netlify.com > User settings > Applications > Personal access tokens.
"""
import sys, os, json, time, hashlib, argparse
import urllib.request, urllib.error

API = "https://api.netlify.com/api/v1"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, ".netlify.token.txt")
SITES_FILE = os.path.join(HERE, ".netlify-sites.json")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            "Token nao encontrado.\n"
            "  1. Gere um Personal access token em app.netlify.com (User settings >\n"
            "     Applications > Personal access tokens > New access token).\n"
            f"  2. Cole SO o token em: {TOKEN_FILE}"
        )
    with open(TOKEN_FILE, encoding="utf-8") as f:
        t = f.read().strip()
    if not t:
        sys.exit(f"Arquivo de token vazio: {TOKEN_FILE}")
    return t


def request(method, path, data=None, ctype="application/json"):
    """Retorna (status, obj). Nao aborta em erro HTTP: devolve o status."""
    headers = {"Authorization": "Bearer " + token()}
    body = None
    if data is not None:
        if ctype == "application/json":
            body = json.dumps(data).encode()
        else:
            body = data
        headers["Content-Type"] = ctype
    req = urllib.request.Request(API + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            raw = r.read().decode()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"_raw": raw}


def api(method, path, data=None, ctype="application/json"):
    """Como request(), mas aborta em erro (pros casos em que erro e fatal)."""
    st, obj = request(method, path, data, ctype)
    if st >= 400:
        sys.exit(f"Netlify respondeu {st} em {method} {path}:\n{json.dumps(obj, ensure_ascii=False)}")
    return obj


def load_sites():
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sites(m):
    with open(SITES_FILE, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)


def collect_files(caminho, assets=False):
    """Mapa {"/caminho": bytes}.

    Modo site (padrao): arquivo unico vira /index.html; pasta precisa ter index.html.
    Modo assets: mantem o nome de cada arquivo e nao exige index.html — serve pra
    hospedar midia (PNG/JPG/MP4) e ter URL publica direta de cada uma.
    """
    files = {}
    if os.path.isfile(caminho):
        with open(caminho, "rb") as f:
            nome = "/" + os.path.basename(caminho) if assets else "/index.html"
            files[nome] = f.read()
        return files
    tem_index = False
    for base, _, arqs in os.walk(caminho):
        for a in arqs:
            full = os.path.join(base, a)
            rel = "/" + os.path.relpath(full, caminho).replace("\\", "/")
            with open(full, "rb") as f:
                files[rel] = f.read()
            if rel == "/index.html":
                tem_index = True
    if not files:
        sys.exit(f"Nenhum arquivo em {caminho}.")
    if not tem_index and not assets:
        sys.exit(f"A pasta {caminho} nao tem index.html. "
                 "Se a intencao e so hospedar midia, use --assets.")
    return files


def cria_site(slug):
    """Cria site com nome = slug; se ja existir globalmente, tenta slug-xxxx."""
    for nome in [slug, f"{slug}-{os.urandom(2).hex()}", f"{slug}-{os.urandom(3).hex()}"]:
        st, obj = request("POST", "/sites", {"name": nome})
        if st < 400:
            return obj
        if st != 422:  # 422 = nome ja em uso; qualquer outro erro e fatal
            sys.exit(f"Netlify {st} ao criar site:\n{json.dumps(obj, ensure_ascii=False)}")
    sys.exit("Nao consegui um nome de subdominio livre. Tente outro slug.")


def site_para_slug(slug):
    sites = load_sites()
    if slug in sites:
        return sites[slug]["id"], sites
    site = cria_site(slug)
    sites[slug] = {"id": site["id"], "url": site.get("ssl_url", ""), "name": site.get("name", slug)}
    save_sites(sites)
    return site["id"], sites


def deploy(caminho, slug, assets=False):
    if not os.path.exists(caminho):
        sys.exit(f"Nao existe: {caminho}")
    site_id, sites = site_para_slug(slug)
    files = collect_files(caminho, assets)
    digest = {p: hashlib.sha1(b).hexdigest() for p, b in files.items()}

    # 1) declara os arquivos; Netlify responde quais faltam ('required')
    dep = api("POST", f"/sites/{site_id}/deploys", {"files": digest})
    dep_id = dep["id"]
    required = set(dep.get("required", []))

    # 2) faz upload dos que faltam (por sha)
    total_kb = sum(len(b) for b in files.values()) // 1024
    print(f"Subindo {len(files)} arquivo(s), {total_kb} KB, pro site '{slug}'...")
    for p, b in files.items():
        if digest[p] in required:
            api("PUT", f"/deploys/{dep_id}/files{p}", b, "application/octet-stream")

    # 3) espera ficar pronto
    for _ in range(90):
        d = api("GET", f"/deploys/{dep_id}")
        if d.get("state") == "ready":
            url = d.get("ssl_url") or sites[slug]["url"]
            sites[slug]["url"] = url
            save_sites(sites)
            print("\nNo ar:", url)
            if assets:
                # URL direta de cada arquivo: e isso que se cola no upload de
                # criativo da Meta (o conector MCP so aceita link publico).
                print("\nURLs publicas dos arquivos:")
                for p in sorted(files):
                    print(f"  {url}{p}")
            return url
        if d.get("state") == "error":
            sys.exit("Deploy falhou: " + str(d.get("error_message")))
        time.sleep(2)
    sys.exit("Deploy demorou demais (timeout no polling).")


def rename(slug, novo):
    sites = load_sites()
    if slug not in sites:
        sys.exit(f"Slug '{slug}' nao esta no mapa. Rode --list.")
    st, obj = request("PATCH", f"/sites/{sites[slug]['id']}", {"name": novo})
    if st >= 400:
        sys.exit(f"Netlify {st} ao renomear:\n{json.dumps(obj, ensure_ascii=False)}")
    sites[slug]["url"] = obj.get("ssl_url", sites[slug]["url"])
    sites[slug]["name"] = obj.get("name", novo)
    save_sites(sites)
    print("Renomeado. Novo endereco:", sites[slug]["url"])


def listar():
    sites = load_sites()
    if not sites:
        print("Nenhum site ainda.")
        return
    for slug, s in sites.items():
        print(f"  {slug:24} {s.get('url','')}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("caminho", nargs="?", help="pasta com index.html, arquivo .html, ou midia (com --assets)")
    p.add_argument("--slug", help="identifica o site (reusa no re-deploy)")
    p.add_argument("--assets", action="store_true",
                   help="modo biblioteca de midia: nao exige index.html, mantem o nome dos "
                        "arquivos e imprime a URL publica de cada um (pra subir criativo na Meta)")
    p.add_argument("--list", action="store_true", help="lista sites ja criados")
    p.add_argument("--rename", metavar="SLUG", help="renomeia o subdominio de um site")
    p.add_argument("--nome", help="novo nome (usar com --rename)")
    a = p.parse_args()
    if a.list:
        listar(); return
    if a.rename:
        if not a.nome:
            sys.exit("Uso: --rename <slug> --nome <novo-nome>")
        rename(a.rename, a.nome); return
    if not a.caminho or not a.slug:
        sys.exit("Uso: python scripts/deploy-netlify.py <pasta-ou-arquivo> --slug <slug> [--assets]")
    deploy(a.caminho, a.slug, a.assets)


if __name__ == "__main__":
    main()
