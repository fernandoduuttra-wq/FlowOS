#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponte entre o FlowOS e o FlowDM (o ManyChat proprio).

Cria automacao de "comentario vira DM" sem abrir o painel: um conteudo por dia
significa uma automacao por dia, e abrir o navegador toda vez e o tipo de passo
que some quando a pressa aperta -- e ai o post sai sem entrega.

Uso:
  python scripts/flowdm.py posts [-n 12]
      Lista os posts recentes do Instagram com indice, data e legenda.
      Serve pra escolher o post na mao quando --ultimo nao servir.

  python scripts/flowdm.py nova --palavra MAPA --link <url-do-material> --ultimo
      Cria a automacao ja apontada pro post mais recente. E o uso do dia a dia.

      Alvo do post (escolha um):
        --ultimo            o post mais recente da conta
        --post-url <link>   o post especifico (instagram.com/p/XXXX ou /reel/XXXX)
        --qualquer          vale em qualquer post (cuidado: ver AVISO abaixo)

      Opcionais: --nome, --dm, --botao, --link-texto, --link-botao,
                 --publica "a|b|c", --lembrete, --lembrete-min N, --exato

  python scripts/flowdm.py listar
      Mostra as automacoes, o alvo de cada uma e quantas DMs ja sairam.

  python scripts/flowdm.py pausar <nome-ou-id>   |   ativar <nome-ou-id>

AVISO sobre palavra-chave repetida: quando duas automacoes ATIVAS casam o mesmo
comentario, o app usa a mais antiga e para. Se for repetir a palavra (ex.: "QUERO"
sempre), prenda cada automacao ao seu post -- e o que --ultimo/--post-url fazem.
Este script avisa quando detecta colisao.

Credenciais: lidas do .env.local do projeto FlowDM (fora do OneDrive). Se o projeto
mudar de lugar, aponte FLOWDM_DIR no ambiente ou crie scripts/.flowdm.env com
SUPABASE_URL= e SUPABASE_SERVICE_ROLE_KEY=. Nada disso vai pro repo.
"""
import sys, os, re, json, argparse, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# --------------------------------------------------------------- credenciais

def _parse_env(caminho):
    dados = {}
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            k, v = linha.split("=", 1)
            dados[k.strip()] = v.strip().strip('"').strip("'")
    return dados


def credenciais():
    """Procura o .env do FlowDM: override > projeto local > fallback no FlowOS."""
    candidatos = []
    if os.environ.get("FLOWDM_DIR"):
        candidatos.append(os.path.join(os.environ["FLOWDM_DIR"], ".env.local"))
    if os.environ.get("LOCALAPPDATA"):
        candidatos.append(os.path.join(os.environ["LOCALAPPDATA"], "sites", "flowdm", ".env.local"))
    candidatos.append(os.path.join(HERE, ".flowdm.env"))

    for c in candidatos:
        if os.path.exists(c):
            env = _parse_env(c)
            url = (env.get("SUPABASE_URL") or "").rstrip("/")
            key = env.get("SUPABASE_SERVICE_ROLE_KEY")
            # A Project URL as vezes vem copiada com o sufixo da Data API.
            url = re.sub(r"/rest/v1/?$", "", url)
            if url and key:
                return url, key

    sys.exit(
        "Nao achei as credenciais do FlowDM.\n"
        "Procurei em:\n  " + "\n  ".join(candidatos) + "\n"
        "Aponte FLOWDM_DIR pro projeto ou crie scripts/.flowdm.env com\n"
        "SUPABASE_URL= e SUPABASE_SERVICE_ROLE_KEY="
    )


def sb(caminho, metodo="GET", corpo=None, params=None, prefer=None):
    """Chamada ao PostgREST do Supabase."""
    url, key = credenciais()
    alvo = url + "/rest/v1/" + caminho
    if params:
        alvo += "?" + urllib.parse.urlencode(params)

    dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
    req = urllib.request.Request(alvo, data=dados, method=metodo)
    req.add_header("apikey", key)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Content-Type", "application/json")
    if prefer:
        req.add_header("Prefer", prefer)

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            texto = r.read().decode("utf-8")
            return json.loads(texto) if texto.strip() else None
    except urllib.error.HTTPError as e:
        sys.exit("Erro do Supabase (%s): %s" % (e.code, e.read().decode("utf-8", "replace")))


# ------------------------------------------------------------------ instagram

GRAPH = "https://graph.instagram.com/v25.0"


def conta():
    linhas = sb("config", params={"id": "eq.1", "select": "ig_user_id,ig_username,access_token"})
    if not linhas:
        sys.exit("Nenhuma conta conectada no FlowDM. Conecte o Instagram pelo painel primeiro.")
    c = linhas[0]
    if not c.get("access_token"):
        sys.exit("A conta esta cadastrada mas sem token. Reconecte pelo painel.")
    return c


def midias(limite=25):
    c = conta()
    p = urllib.parse.urlencode({
        "fields": "id,media_type,caption,permalink,timestamp",
        "limit": limite,
        "access_token": c["access_token"],
    })
    try:
        with urllib.request.urlopen("%s/%s/media?%s" % (GRAPH, c["ig_user_id"], p), timeout=30) as r:
            return json.loads(r.read().decode("utf-8")).get("data", [])
    except urllib.error.HTTPError as e:
        sys.exit("Erro da API do Instagram (%s): %s\n"
                 "Se falar em token expirado, reconecte pelo painel."
                 % (e.code, e.read().decode("utf-8", "replace")))


def shortcode(url):
    m = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", url or "")
    return m.group(1) if m else None


def resolver_post(args):
    """Devolve (media_id, rotulo). media_id None = vale em qualquer post."""
    if args.qualquer:
        return None, "qualquer post"

    posts = midias(50)
    if not posts:
        sys.exit("A conta nao tem posts (ou a API nao devolveu nenhum).")

    if args.ultimo:
        p = posts[0]
        return p["id"], resumo(p)

    alvo = shortcode(args.post_url)
    if not alvo:
        sys.exit("Nao consegui ler o codigo do post em: %s\n"
                 "Esperado algo como https://instagram.com/p/ABC123/" % args.post_url)

    for p in posts:
        if shortcode(p.get("permalink", "")) == alvo:
            return p["id"], resumo(p)

    sys.exit("Nao achei esse post entre os 50 mais recentes.\n"
             "Rode 'python scripts/flowdm.py posts -n 50' pra conferir.")


def resumo(p):
    legenda = re.sub(r"\s+", " ", (p.get("caption") or "")).strip()
    data = (p.get("timestamp") or "")[:10]
    return "%s %s" % (data, legenda[:60] or p.get("media_type", ""))


# ------------------------------------------------------------------- comandos

def cmd_posts(args):
    for i, p in enumerate(midias(args.n), 1):
        print("%2d. %s" % (i, resumo(p)))
        print("    %s" % p.get("permalink", ""))


def cmd_nova(args):
    media_id, rotulo = resolver_post(args)
    palavras = [x.strip() for x in re.split(r"[,\n]", args.palavra) if x.strip()]
    if not palavras:
        sys.exit("Informe ao menos uma palavra-chave em --palavra.")

    avisar_colisao(palavras, media_id)

    registro = {
        "nome": args.nome or ("%s - %s" % (palavras[0], rotulo))[:60],
        "ativo": True,
        "trigger_comment": True,
        "trigger_story": False,
        "trigger_dm": False,
        "keywords": palavras,
        "match_type": "exact" if args.exato else "contains",
        "media_id": media_id,
        "public_replies": [x.strip() for x in (args.publica or "").split("|") if x.strip()],
        "welcome_text": args.dm,
        "quick_reply_label": args.botao,
        "link_text": args.link_texto,
        "link_button_label": args.link_botao,
        "link_url": args.link,
        "reminder_text": args.lembrete,
        "reminder_delay_minutes": args.lembrete_min,
    }

    criado = sb("automations", "POST", registro, prefer="return=representation")
    a = criado[0] if isinstance(criado, list) else criado

    print("Automacao criada: %s" % a["nome"])
    print("  palavra-chave : %s (%s)" % (", ".join(palavras),
                                         "exata" if args.exato else "aparece no comentario"))
    print("  vale em       : %s" % rotulo)
    print("  entrega       : %s" % args.link)
    if args.lembrete:
        print("  lembrete      : %d min depois" % args.lembrete_min)
    print("\nJa esta ativa. Teste comentando de outra conta.")


def avisar_colisao(palavras, media_id):
    """Duas automacoes ativas que casam o mesmo comentario: a mais antiga ganha."""
    ativas = sb("automations", params={
        "ativo": "eq.true",
        "select": "nome,keywords,media_id,match_type",
        "order": "created_at.asc",
    }) or []

    novas = {p.lower() for p in palavras}
    for a in ativas:
        if not novas & {k.lower() for k in (a.get("keywords") or [])}:
            continue
        # So colide se disputarem o mesmo alcance de post.
        outro = a.get("media_id")
        if outro is None or media_id is None or outro == media_id:
            escopo = "qualquer post" if outro is None else "o mesmo post"
            print("AVISO: a automacao ativa \"%s\" ja usa essa palavra em %s." % (a["nome"], escopo))
            print("       A mais antiga ganha, entao a nova pode nunca disparar.")
            print("       Prenda cada uma ao seu post (--ultimo/--post-url) ou pause a antiga.\n")
            break


def cmd_listar(args):
    autos = sb("automations", params={"select": "*", "order": "created_at.desc"}) or []
    if not autos:
        print("Nenhuma automacao cadastrada.")
        return

    enviados = {}
    fila = sb("queue", params={"select": "automation_id,status"}) or []
    for q in fila:
        if q["status"] == "sent":
            enviados[q["automation_id"]] = enviados.get(q["automation_id"], 0) + 1

    posts = {}
    if any(a.get("media_id") for a in autos):
        posts = {p["id"]: resumo(p) for p in midias(50)}

    for a in autos:
        marca = "ativa " if a["ativo"] else "PAUSADA"
        alvo = posts.get(a["media_id"], a["media_id"]) if a.get("media_id") else "qualquer post"
        print("[%s] %s" % (marca, a["nome"]))
        print("        palavras : %s" % ", ".join(a.get("keywords") or []) or "(nenhuma)")
        print("        vale em  : %s" % alvo)
        print("        entrega  : %s" % (a.get("link_url") or "(sem link)"))
        print("        enviadas : %d" % enviados.get(a["id"], 0))
        print("        id       : %s" % a["id"])


def achar(termo):
    autos = sb("automations", params={"select": "id,nome"}) or []
    exatos = [a for a in autos if a["id"] == termo]
    if exatos:
        return exatos[0]
    parciais = [a for a in autos if termo.lower() in a["nome"].lower()]
    if not parciais:
        sys.exit("Nao achei automacao com \"%s\". Rode 'listar' pra ver os nomes." % termo)
    if len(parciais) > 1:
        sys.exit("\"%s\" casa com mais de uma:\n  %s\nUse o id."
                 % (termo, "\n  ".join(a["nome"] for a in parciais)))
    return parciais[0]


def cmd_estado(args, ativo):
    a = achar(args.alvo)
    sb("automations", "PATCH", {"ativo": ativo}, params={"id": "eq." + a["id"]})
    print("%s: %s" % (a["nome"], "ativada" if ativo else "pausada"))


# ----------------------------------------------------------------------- cli

def main():
    p = argparse.ArgumentParser(description="Automacoes do FlowDM pela linha de comando.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("posts", help="lista os posts recentes")
    sp.add_argument("-n", type=int, default=12)

    sn = sub.add_parser("nova", help="cria uma automacao")
    sn.add_argument("--palavra", required=True, help="palavra-chave (varias: separe por virgula)")
    sn.add_argument("--link", required=True, help="URL do material entregue")
    alvo = sn.add_mutually_exclusive_group(required=True)
    alvo.add_argument("--ultimo", action="store_true", help="prende no post mais recente")
    alvo.add_argument("--post-url", help="prende no post desta url")
    alvo.add_argument("--qualquer", action="store_true", help="vale em qualquer post")
    sn.add_argument("--nome")
    sn.add_argument("--exato", action="store_true",
                    help="so dispara se o comentario for exatamente a palavra")
    sn.add_argument("--dm", default="Oi! Vi seu comentario. Responde aqui embaixo "
                                    "que eu te mando o link na hora.")
    sn.add_argument("--botao", default="Quero sim")
    sn.add_argument("--link-texto", default="Prontinho, e so clicar aqui embaixo:")
    sn.add_argument("--link-botao", default="Acessar")
    sn.add_argument("--publica", help='respostas publicas no comentario, separadas por "|"')
    sn.add_argument("--lembrete")
    sn.add_argument("--lembrete-min", type=int, default=60)

    sub.add_parser("listar", help="lista as automacoes")

    for nome in ("pausar", "ativar"):
        s = sub.add_parser(nome, help="%s uma automacao" % nome)
        s.add_argument("alvo", help="nome (parcial) ou id")

    args = p.parse_args()
    if args.cmd == "posts":
        cmd_posts(args)
    elif args.cmd == "nova":
        cmd_nova(args)
    elif args.cmd == "listar":
        cmd_listar(args)
    elif args.cmd == "pausar":
        cmd_estado(args, False)
    elif args.cmd == "ativar":
        cmd_estado(args, True)


if __name__ == "__main__":
    main()
