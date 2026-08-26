#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cria campanha + conjunto + anuncios na Meta a partir de um spec JSON.

Existe pra conta que o conector MCP nao alcanca (rollout gradual da Meta). Onde o
conector funciona, prefira ele: ele pede aprovacao no chat antes de cada escrita.

REGRA DE SEGURANCA: tudo nasce PAUSED e o dry-run e o padrao.
Isso mexe em verba de cliente. Sem --aplicar, o script so imprime o que faria.
Depois de criado, revisar no Gerenciador de Anuncios e ativar la, na mao.

Uso:
  python scripts/meta-campanha.py criar --spec arquivo.json [--aplicar]

Token: scripts/.meta.token.txt (escopo ads_management).
"""
import sys, os, json, argparse, urllib.request, urllib.parse, urllib.error

API_VERSION = "v25.0"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, ".meta.token.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"Token nao encontrado em {TOKEN_FILE}")
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return f.read().strip()


def post(path, payload):
    body = {}
    for k, v in payload.items():
        body[k] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    body["access_token"] = token()
    url = f"https://graph.facebook.com/{API_VERSION}/{path}"
    data = urllib.parse.urlencode(body).encode("utf-8")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data)) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(raw)["error"]
            msg = err.get("error_user_msg") or err.get("message") or raw
            if err.get("error_user_title"):
                msg = f"{err['error_user_title']}: {msg}"
        except Exception:
            msg = raw
        sys.exit(f"\nERRO HTTP {e.code} em {path}:\n  {msg}")


def brl(cents):
    return f"R$ {int(cents)/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def criar(a):
    with open(a.spec, encoding="utf-8") as f:
        s = json.load(f)

    acct = s["ad_account_id"]
    camp, adset, ads = s["campaign"], s["adset"], s["ads"]
    diario = camp.get("daily_budget")

    print("=" * 70)
    print(f"CONTA ......... {acct}")
    print(f"CAMPANHA ...... {camp['name']}")
    print(f"  objetivo .... {camp['objective']}")
    if diario:
        print(f"  orcamento ... {brl(diario)}/dia  (~{brl(int(diario)*30)}/mes)")
    print(f"  status ...... {camp.get('status', 'PAUSED')}")
    print(f"\nCONJUNTO ...... {adset['name']}")
    print(f"  otimizacao .. {adset['optimization_goal']}")
    print(f"  destino ..... {adset.get('destination_type')}")
    t = adset["targeting"]
    regioes = ", ".join(r["name"] for r in t.get("geo_locations", {}).get("regions", []))
    print(f"  local ....... {regioes or '(ver spec)'}")
    print(f"  idade ....... {t.get('age_min')}-{t.get('age_max')}")
    for ca in t.get("custom_audiences", []) or []:
        print(f"  publico ..... {ca.get('name', ca['id'])}")
    print(f"\nANUNCIOS ({len(ads)}):")
    for ad in ads:
        cta = ad["creative"]["object_story_spec"]["link_data"].get("call_to_action", {})
        form = cta.get("value", {}).get("lead_gen_form_id", "-")
        print(f"  - {ad['name']:<28} formulario={form}")
    print("=" * 70)

    if not a.aplicar:
        print("\n[dry-run] Nada foi criado. Repita com --aplicar pra valer.")
        return

    print("\nCriando campanha...")
    c = post(f"{acct}/campaigns", {
        "name": camp["name"],
        "objective": camp["objective"],
        "status": camp.get("status", "PAUSED"),
        "special_ad_categories": camp.get("special_ad_categories", []),
        "bid_strategy": camp.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"),
        **({"daily_budget": str(diario)} if diario else {}),
    })
    print(f"  campaign_id = {c['id']}")

    print("Criando conjunto...")
    st = post(f"{acct}/adsets", {
        "name": adset["name"],
        "campaign_id": c["id"],
        "optimization_goal": adset["optimization_goal"],
        "billing_event": adset.get("billing_event", "IMPRESSIONS"),
        "destination_type": adset.get("destination_type", "ON_AD"),
        "promoted_object": adset["promoted_object"],
        "targeting": adset["targeting"],
        "status": adset.get("status", "PAUSED"),
    })
    print(f"  adset_id = {st['id']}")

    for ad in ads:
        print(f"Criando anuncio '{ad['name']}'...")
        cr = post(f"{acct}/adcreatives", {
            "name": ad["creative"].get("name", ad["name"]),
            "object_story_spec": ad["creative"]["object_story_spec"],
            "degrees_of_freedom_spec": ad["creative"].get("degrees_of_freedom_spec", {}),
        })
        d = post(f"{acct}/ads", {
            "name": ad["name"],
            "adset_id": st["id"],
            "creative": {"creative_id": cr["id"]},
            "status": ad.get("status", "PAUSED"),
        })
        print(f"  ad_id = {d['id']}  (creative {cr['id']})")

    print("\nOK. TUDO PAUSADO.")
    print("Revise no Gerenciador de Anuncios e ative la. O script nunca ativa nada.")


def get(path, params=None):
    params = dict(params or {})
    params["access_token"] = token()
    url = f"https://graph.facebook.com/{API_VERSION}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO GET {path}: {e.read().decode('utf-8', 'replace')}")


def thumb_do_video(video_id):
    """A Meta exige miniatura em anuncio de video. Pega a marcada como preferida.
    Resolvemos aqui em vez de fixar no spec porque a URL vem assinada e expira."""
    d = get(f"{video_id}/thumbnails", {"fields": "uri,is_preferred"})
    fotos = d.get("data", [])
    if not fotos:
        sys.exit(f"Video {video_id} nao tem miniatura disponivel.")
    for f in fotos:
        if f.get("is_preferred"):
            return f["uri"]
    return fotos[0]["uri"]


def _criar_anuncio(acct, adset_id, ad):
    """Cria criativo + anuncio dentro de um conjunto que ja existe."""
    vd = ad["creative"]["object_story_spec"].get("video_data")
    if vd and not vd.get("image_url") and not vd.get("image_hash"):
        vd["image_url"] = thumb_do_video(vd["video_id"])
    cr = post(f"{acct}/adcreatives", {
        "name": ad["creative"].get("name", ad["name"]),
        "object_story_spec": ad["creative"]["object_story_spec"],
        "degrees_of_freedom_spec": ad["creative"].get("degrees_of_freedom_spec", {}),
    })
    d = post(f"{acct}/ads", {
        "name": ad["name"],
        "adset_id": adset_id,
        "creative": {"creative_id": cr["id"]},
        "status": ad.get("status", "PAUSED"),
    })
    return cr["id"], d["id"]


def anuncios(a):
    """Adiciona anuncios a um conjunto existente. Util quando a campanha ja foi criada
    e so os anuncios faltaram (ex: erro de app em modo de desenvolvimento)."""
    with open(a.spec, encoding="utf-8") as f:
        s = json.load(f)
    acct, ads = s["ad_account_id"], s["ads"]

    print(f"CONTA ..... {acct}")
    print(f"CONJUNTO .. {a.adset}")
    print(f"ANUNCIOS .. {len(ads)}\n")
    for ad in ads:
        spec = ad["creative"]["object_story_spec"]
        d = spec.get("link_data") or spec.get("video_data") or {}
        midia = d.get("image_hash") or d.get("video_id") or "?"
        form = d.get("call_to_action", {}).get("value", {}).get("lead_gen_form_id", "-")
        print(f"  - {ad['name']:<26} midia={midia}  form={form}")

    if not a.aplicar:
        print("\n[dry-run] Nada foi criado. Repita com --aplicar pra valer.")
        return

    print()
    for ad in ads:
        cr_id, ad_id = _criar_anuncio(acct, a.adset, ad)
        print(f"  OK  {ad['name']:<26} ad={ad_id}  creative={cr_id}")
    print("\nTUDO PAUSADO. Revise no Gerenciador e ative la.")


def main():
    ap = argparse.ArgumentParser(description="Cria campanha na Meta a partir de spec JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("criar", help="campanha + conjunto + anuncios")
    p.add_argument("--spec", required=True)
    p.add_argument("--aplicar", action="store_true", help="sem isso, so mostra o que faria")
    p.set_defaults(func=criar)

    p = sub.add_parser("anuncios", help="so os anuncios, num conjunto que ja existe")
    p.add_argument("--adset", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--aplicar", action="store_true", help="sem isso, so mostra o que faria")
    p.set_defaults(func=anuncios)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
