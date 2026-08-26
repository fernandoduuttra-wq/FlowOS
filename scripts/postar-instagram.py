#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publica carrossel (ou imagem unica) no Instagram pela Graph API.

Por que existe: a Graph API NAO aceita upload de arquivo local. Criativo so entra
por URL publica. Entao a esteira e sempre a mesma:

    renderizar os PNG  ->  hospedar (deploy-netlify.py --assets)  ->  criar um
    container por imagem  ->  container do carrossel  ->  publicar

Este script faz os quatro passos de uma vez. Python puro (urllib), sem dependencia.

Uso:
  python scripts/postar-instagram.py checar
      Diz o que o token enxerga: qual conta do Instagram, quais permissoes, e se
      da pra publicar. Rodar isso PRIMEIRO, sempre que trocar o token.

  python scripts/postar-instagram.py <pasta-do-conteudo>
      Ensaio (nao publica): mostra os slides na ordem, a legenda exata e a conta
      de destino. E o default de proposito — post e acao irreversivel.

  python scripts/postar-instagram.py <pasta-do-conteudo> --publicar
      Faz de verdade.

  Opcoes:
    --legenda <arquivo>  legenda especifica (default: legenda.md da pasta)
    --slug <slug>        site Netlify que hospeda os PNG (default: flowos-criativos;
                         e reusado a cada post, o conteudo anterior e substituido —
                         tudo bem, o Instagram copia a imagem na hora de publicar)
    --so-hospedar        so sobe os PNG e imprime as URLs, sem tocar na Meta

  A pasta pode ser a do conteudo (usa a subpasta instagram/) ou a pasta dos PNG
  direto. Os arquivos entram em ordem alfabetica — por isso slide-01, slide-02...

Legenda: le o .md e corta o que e anotacao interna — remove linhas de titulo
markdown (#) e para no primeiro '---'. O que sobra e o que vai pro Instagram.
O ensaio imprime isso literal pra conferir antes.

Token: scripts/.instagram.token.txt (gitignored pelo padrao *.token.txt).

  Use um app da Meta DEDICADO a publicar, separado do app que faz outras coisas
  (DM, webhook, anuncio). Nao e questao de performance — o limite de publicacao e
  por conta do Instagram (50 posts/24h), nao por app, entao separar nao da mais
  cota. Os motivos sao outros dois:
    - raio do estrago: token que so publica nao le mensagem se vazar;
    - App Review: escopo estreito passa mais facil, e um app cujo caso de uso e
      outro nao precisa explicar por que pede permissao de publicar.
  A conta do Instagram pode estar autorizada em varios apps ao mesmo tempo.

  Permissoes, conforme a rota:
    Rota Facebook Login (app com Pagina + conta profissional vinculada):
      instagram_basic, instagram_content_publish, pages_show_list,
      pages_read_engagement
    Rota Instagram Login (login direto pelo Instagram, sem Pagina):
      instagram_business_content_publish

  Gerar em developers.facebook.com > seu app > Ferramentas > Explorador de Graph
  API > marcar as permissoes > Gerar token (dura 1-2h) e depois estender no
  Depurador de token (~60 dias). Permissao nova exige gerar token NOVO: token
  antigo nao ganha escopo retroativo.

Limites da Meta que este script respeita/checa: 10 imagens por carrossel, legenda
de 2200 caracteres, 30 hashtags, 50 publicacoes por 24h.
"""
import sys, os, json, time, argparse, importlib.util
import urllib.request, urllib.parse, urllib.error

# Mesma versao que o scripts/meta-ads.py usa. Se um dia der erro de versao,
# os dois sobem juntos.
API_VERSION = "v25.0"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, ".instagram.token.txt")
CONTA_FILE = os.path.join(HERE, ".instagram-conta.json")

MAX_ITENS = 10
MAX_LEGENDA = 2200
MAX_HASHTAGS = 30
EXT_IMAGEM = (".png", ".jpg", ".jpeg")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- token e API

def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            "Token do Instagram nao encontrado.\n"
            f"  Cole SO o token em: {TOKEN_FILE}\n"
            "  Como gerar: veja o cabecalho deste arquivo (precisa da permissao de\n"
            "  publicacao — instagram_content_publish ou instagram_business_content_publish)."
        )
    with open(TOKEN_FILE, encoding="utf-8") as f:
        t = f.read().strip()
    if not t:
        sys.exit(f"Arquivo de token vazio: {TOKEN_FILE}")
    return t


def graph(host, path, params=None, metodo="GET"):
    """Retorna (status, obj). Nao aborta em erro: devolve o status."""
    p = dict(params or {})
    p["access_token"] = token()
    url = f"https://{host}/{API_VERSION}/{path.lstrip('/')}"
    dados = None
    if metodo == "GET":
        url += "?" + urllib.parse.urlencode(p)
    else:
        dados = urllib.parse.urlencode(p).encode()
    req = urllib.request.Request(url, data=dados, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        bruto = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(bruto)
        except Exception:
            return e.code, {"_raw": bruto}
    except urllib.error.URLError as e:
        sys.exit(f"Sem resposta da Meta ({e.reason}). Sem internet?")


def erro_meta(obj):
    e = obj.get("error", {})
    msg = e.get("message", json.dumps(obj, ensure_ascii=False))
    detalhe = e.get("error_user_msg")
    return msg + (f"\n  {detalhe}" if detalhe else "")


def exigir(status, obj, contexto):
    if status >= 400:
        sys.exit(f"Meta respondeu {status} em {contexto}:\n  {erro_meta(obj)}")
    return obj


# ------------------------------------------------------------- achar a conta

def descobrir_conta():
    """Descobre o ig_user_id sozinho. Tenta as duas rotas da Meta.

    Rota 'facebook': token de usuario/Pagina > /me/accounts > cada Pagina traz o
    instagram_business_account vinculado.
    Rota 'instagram': token do proprio Instagram (Instagram Login) > graph.instagram.com/me.
    """
    st, obj = graph("graph.facebook.com", "me/accounts",
                    {"fields": "name,instagram_business_account{id,username}"})
    if st < 400:
        for pag in obj.get("data", []):
            iba = pag.get("instagram_business_account")
            if iba:
                return {"host": "graph.facebook.com", "rota": "facebook",
                        "ig_user_id": iba["id"], "username": iba.get("username", "?"),
                        "pagina": pag.get("name", "?"), "pagina_id": pag.get("id", "")}

    st, obj = graph("graph.instagram.com", "me", {"fields": "id,username"})
    if st < 400 and obj.get("id"):
        return {"host": "graph.instagram.com", "rota": "instagram",
                "ig_user_id": obj["id"], "username": obj.get("username", "?")}

    sys.exit(
        "O token nao chega em nenhuma conta do Instagram.\n"
        f"  Ultima resposta da Meta: {erro_meta(obj)}\n"
        "  Causas comuns:\n"
        "   - o token foi gerado sem as permissoes de Instagram (gere um token NOVO\n"
        "     depois de marcar as permissoes; o antigo nao ganha escopo retroativo)\n"
        "   - a conta do Instagram nao e Profissional (Comercial ou Criador)\n"
        "   - a conta nao esta vinculada a uma Pagina do Facebook (rota Facebook Login)"
    )


def conta(recarregar=False):
    if not recarregar and os.path.exists(CONTA_FILE):
        with open(CONTA_FILE, encoding="utf-8") as f:
            return json.load(f)
    c = descobrir_conta()
    with open(CONTA_FILE, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    return c


def checar():
    c = conta(recarregar=True)
    print(f"Conta:  @{c['username']}  (id {c['ig_user_id']})")
    if c.get("pagina"):
        print(f"Pagina: {c['pagina']}")
    print(f"Rota:   {c['rota']}  ({c['host']})")

    permissoes = None
    if c["rota"] == "facebook":
        st, obj = graph("graph.facebook.com", "me/permissions")
        if st < 400:
            permissoes = sorted(p["permission"] for p in obj.get("data", [])
                                if p.get("status") == "granted")
            print("\nPermissoes concedidas:")
            for p in permissoes:
                print("  " + p)

    publica = permissoes is None or any(
        p in permissoes for p in ("instagram_content_publish",
                                  "instagram_business_content_publish"))
    if publica and permissoes is not None:
        print("\nOK: o token tem permissao de publicar.")
    elif permissoes is not None:
        print("\nFALTA a permissao de publicar (instagram_content_publish).")
        print("  Nao precisa de app novo: adicione a permissao no MESMO app e gere")
        print("  um token NOVO — token antigo nao ganha escopo retroativo.")
        return 1

    # Teste real: pergunta o limite de publicacao. So responde se o escopo estiver certo.
    st, obj = graph(c["host"], f"{c['ig_user_id']}/content_publishing_limit",
                    {"fields": "quota_usage,config"})
    if st >= 400:
        print("\nNao consegui ler a cota de publicacao:")
        print("  " + erro_meta(obj))
        return 1
    d = (obj.get("data") or [{}])[0]
    cfg = d.get("config", {})
    print(f"\nCota: {d.get('quota_usage', 0)} de {cfg.get('quota_total', 50)} "
          f"publicacoes nas ultimas {cfg.get('quota_duration', 86400) // 3600}h.")
    print("Pronto pra publicar.")
    return 0


# ------------------------------------------------------------ pasta e legenda

def achar_imagens(caminho):
    if not os.path.isdir(caminho):
        sys.exit(f"Nao e uma pasta: {caminho}")
    pasta = caminho
    sub = os.path.join(caminho, "instagram")
    if os.path.isdir(sub):
        pasta = sub
    arqs = sorted(a for a in os.listdir(pasta)
                  if a.lower().endswith(EXT_IMAGEM))
    if not arqs:
        sys.exit(f"Nenhum PNG/JPG em {pasta}. Renderizou os slides? "
                 "(scripts/render-carrossel.ps1)")
    if len(arqs) > MAX_ITENS:
        sys.exit(f"{len(arqs)} imagens em {pasta}, mas o carrossel do Instagram "
                 f"aceita no maximo {MAX_ITENS}.")
    return pasta, arqs


def ler_legenda(caminho_pasta, arquivo=None):
    alvo = arquivo or os.path.join(caminho_pasta, "legenda.md")
    if not os.path.exists(alvo):
        print(f"(sem legenda: {alvo} nao existe — o post vai sem texto)")
        return ""
    with open(alvo, encoding="utf-8") as f:
        bruto = f.read()
    linhas = []
    for linha in bruto.splitlines():
        if linha.strip().startswith("---"):
            break  # daqui pra baixo e anotacao interna, nao vai pro post
        s = linha.lstrip()
        if s.startswith("#"):
            # Titulo markdown ("# Legenda", "## Nota") e estrutura do arquivo, nao
            # texto do post. Hashtag de verdade nao tem espaco depois do #.
            n = len(s) - len(s.lstrip("#"))
            if 1 <= n <= 6 and s[n:n + 1] == " ":
                continue
        linhas.append(linha)
    texto = "\n".join(linhas).strip()

    if len(texto) > MAX_LEGENDA:
        sys.exit(f"Legenda com {len(texto)} caracteres; o Instagram corta em {MAX_LEGENDA}.")
    tags = sum(1 for p in texto.split() if p.startswith("#") and len(p) > 1)
    if tags > MAX_HASHTAGS:
        sys.exit(f"{tags} hashtags; o Instagram aceita {MAX_HASHTAGS}.")
    return texto


# ---------------------------------------------------------------- hospedagem

def hospedar(pasta, arqs, slug):
    """Sobe os PNG no Netlify e devolve as URLs publicas, na ordem dos arquivos."""
    spec = importlib.util.spec_from_file_location(
        "deploy_netlify", os.path.join(HERE, "deploy-netlify.py"))
    dn = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dn)
    base = dn.deploy(pasta, slug, assets=True).rstrip("/")
    return [f"{base}/{urllib.parse.quote(a)}" for a in arqs]


# ---------------------------------------------------------------- publicacao

def esperar_container(host, container_id, rotulo):
    """Container de midia e assincrono: a Meta baixa a imagem antes de liberar."""
    for _ in range(60):
        st, obj = graph(host, container_id, {"fields": "status_code,status"})
        if st >= 400:
            sys.exit(f"Erro checando {rotulo}:\n  {erro_meta(obj)}")
        codigo = obj.get("status_code")
        if codigo == "FINISHED":
            return
        if codigo in ("ERROR", "EXPIRED"):
            sys.exit(f"{rotulo} falhou ({codigo}): {obj.get('status', '')}")
        time.sleep(3)
    sys.exit(f"{rotulo} nao ficou pronto a tempo.")


def publicar(c, urls, legenda):
    host, ig = c["host"], c["ig_user_id"]

    if len(urls) == 1:
        print("\nCriando o container da imagem...")
        obj = exigir(*graph(host, f"{ig}/media",
                            {"image_url": urls[0], "caption": legenda}, "POST"),
                     contexto="criar container")
        alvo = obj["id"]
        esperar_container(host, alvo, "container da imagem")
    else:
        filhos = []
        for i, u in enumerate(urls, 1):
            print(f"Container do slide {i:02d}/{len(urls)}...")
            obj = exigir(*graph(host, f"{ig}/media",
                                {"image_url": u, "is_carousel_item": "true"}, "POST"),
                         contexto=f"criar container do slide {i}")
            filhos.append(obj["id"])
        for i, f in enumerate(filhos, 1):
            esperar_container(host, f, f"container do slide {i:02d}")

        print("\nCriando o container do carrossel...")
        obj = exigir(*graph(host, f"{ig}/media",
                            {"media_type": "CAROUSEL",
                             "children": ",".join(filhos),
                             "caption": legenda}, "POST"),
                     contexto="criar container do carrossel")
        alvo = obj["id"]
        esperar_container(host, alvo, "container do carrossel")

    print("Publicando...")
    obj = exigir(*graph(host, f"{ig}/media_publish", {"creation_id": alvo}, "POST"),
                 contexto="publicar")
    post_id = obj["id"]

    st, info = graph(host, post_id, {"fields": "permalink"})
    link = info.get("permalink", "") if st < 400 else ""
    print(f"\nNo ar: {link or post_id}")
    return post_id


# --------------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("caminho", nargs="?",
                   help="pasta do conteudo (usa a subpasta instagram/) ou a pasta dos PNG; "
                        "ou o comando 'checar'")
    p.add_argument("--publicar", action="store_true",
                   help="publica de verdade (sem isso e so ensaio)")
    p.add_argument("--legenda", help="arquivo de legenda (default: legenda.md da pasta)")
    p.add_argument("--slug", default="flowos-criativos",
                   help="site Netlify que hospeda os PNG (default: flowos-criativos)")
    p.add_argument("--so-hospedar", action="store_true",
                   help="so sobe os PNG e imprime as URLs, sem tocar na Meta")
    a = p.parse_args()

    if not a.caminho:
        p.print_help(); return
    if a.caminho == "checar":
        sys.exit(checar())

    pasta_png, arqs = achar_imagens(a.caminho)
    legenda = ler_legenda(a.caminho, a.legenda)

    if a.so_hospedar:
        for u in hospedar(pasta_png, arqs, a.slug):
            print("  " + u)
        return

    c = conta()

    print(f"\nConta:   @{c['username']}")
    print(f"Slides:  {len(arqs)} — {', '.join(arqs)}")
    print(f"Pasta:   {pasta_png}")
    print("\n--- legenda que vai pro post ---")
    print(legenda if legenda else "(vazia)")
    print("--- fim da legenda ---")

    if not a.publicar:
        print("\nEnsaio. Nada foi publicado nem hospedado.")
        print("Pra publicar de verdade, repita o comando com --publicar")
        return

    urls = hospedar(pasta_png, arqs, a.slug)
    publicar(c, urls, legenda)


if __name__ == "__main__":
    main()
