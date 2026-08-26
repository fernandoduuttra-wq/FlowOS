#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formularios instantaneos (Instant Forms) de Lead Ads pela Graph API.

Existe porque NEM o conector MCP da Meta NEM o scripts/meta-ads.py alcancam isso:
formulario e objeto de PAGINA (/{page_id}/leadgen_forms), nao de conta de anuncio.
O conector so mexe em campanha/conjunto/anuncio/criativo.

O ganho real e o campo interno das perguntas. Na interface, montar uma pergunta com
30 opcoes e renomear o valor interno de cada uma na aba "Nomes dos campos" e trabalho
manual e da erro de digitacao. Por JSON o valor sai exato de primeira, e o que o lead
VE nao precisa ser o que o CRM RECEBE:
    o lead ve "Cortinas"  ->  o CRM recebe "Persianas / Cortinas / Toldos"

Uso:
  python scripts/meta-leadform.py pages
      Lista as Paginas que o token enxerga (id + nome).

  python scripts/meta-leadform.py list --page <page_id>
      Lista os formularios da Pagina (id, nome, status).

  python scripts/meta-leadform.py show --form <form_id> [--json]
      Mostra um formulario existente. Use como molde antes de criar outro.

  python scripts/meta-leadform.py create --page <page_id> --spec arquivo.json
      Cria o formulario. SEM --aplicar ele so mostra o que faria (dry-run).
      Formulario nao gasta verba, mas nasce publicado e nao da pra editar depois
      de receber lead -- por isso o dry-run e o padrao.

Token: scripts/.meta.token.txt (o mesmo do meta-ads.py, gitignored por *.token.txt).
  Precisa dos escopos pages_show_list + pages_manage_ads + leads_retrieval.
  O token de USUARIO basta: o script troca ele pelo token de PAGINA sozinho
  (POST em leadgen_forms exige token de Pagina, GET nao).
"""
import sys, os, json, argparse, urllib.request, urllib.parse, urllib.error

API_VERSION = "v25.0"
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(HERE, ".meta.token.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

FORM_FIELDS = ",".join([
    "id", "name", "status", "locale", "questions", "context_card",
    "thank_you_page", "privacy_policy_url", "legal_content",
    "tracking_parameters", "block_display_for_non_targeted_viewer",
    "allow_organic_lead", "created_time",
])
# NAO pedir leadgen_export_csv_url: a Meta aposentou o campo na v5.0 e a chamada
# inteira volta HTTP 400 se ele estiver na lista de fields.


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            f"Token nao encontrado em {TOKEN_FILE}\n"
            "Gere no Graph API Explorer com pages_manage_ads + leads_retrieval."
        )
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return f.read().strip()


def api(path, params=None, post=None, tok=None):
    params = dict(params or {})
    params["access_token"] = tok or token()
    url = f"https://graph.facebook.com/{API_VERSION}/{path}?" + urllib.parse.urlencode(params)
    data = None
    if post is not None:
        data = urllib.parse.urlencode(post).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            err = json.loads(body)["error"]
            msg = err.get("message", body)
            if err.get("error_user_msg"):
                msg += f"\n  Detalhe: {err['error_user_msg']}"
        except Exception:
            msg = body
        sys.exit(f"HTTP {e.code} em {path}: {msg}")


def paged(path, params=None, limit_pages=50, tok=None):
    out = []
    d = api(path, params, tok=tok)
    out.extend(d.get("data", []))
    for _ in range(limit_pages):
        nxt = d.get("paging", {}).get("next")
        if not nxt:
            break
        with urllib.request.urlopen(nxt) as r:
            d = json.loads(r.read().decode("utf-8"))
        out.extend(d.get("data", []))
    return out


def page_token(page_id):
    """POST em leadgen_forms exige token de Pagina. Deriva do token de usuario."""
    d = api(page_id, {"fields": "access_token,name"})
    tok = d.get("access_token")
    if not tok:
        sys.exit(
            f"A Pagina {page_id} nao devolveu token.\n"
            "Confere se o token tem pages_show_list + pages_manage_ads e se voce e admin da Pagina."
        )
    return tok, d.get("name", "")


def cmd_pages(a):
    rows = paged("me/accounts", {"fields": "id,name", "limit": 100})
    print(f"{len(rows)} Paginas visiveis pelo token:\n")
    for p in rows:
        print(f"  {p['id']:<22} {p.get('name','')}")


def cmd_list(a):
    # Listar formulario tambem exige token de Pagina (a Meta responde #190 com token de usuario).
    tok, nome = page_token(a.page)
    rows = paged(f"{a.page}/leadgen_forms",
                 {"fields": "id,name,status,created_time", "limit": 100}, tok=tok)
    print(f"{len(rows)} formularios em '{nome}' ({a.page}):\n")
    for f in rows:
        criado = (f.get("created_time") or "")[:10]
        print(f"  {f['id']:<22} {f.get('status',''):<10} {criado}  {f.get('name','')}")


def cmd_show(a):
    d = api(a.form, {"fields": FORM_FIELDS})
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    print(f"Formulario: {d.get('name')}  ({d.get('id')})")
    print(f"  status ............ {d.get('status')}")
    print(f"  locale ............ {d.get('locale')}")
    print(f"  so quem viu o anuncio: {d.get('block_display_for_non_targeted_viewer')}")
    print(f"  aceita lead organico.: {d.get('allow_organic_lead')}")
    tp = d.get("tracking_parameters")
    print(f"  parametros de rastreamento: {tp if tp else '(nenhum)'}")
    print("\n  Perguntas (o 'key' e o que o CRM recebe):")
    for q in d.get("questions", []):
        print(f"    - type={q.get('type'):<14} key={q.get('key')!r}  label={q.get('label')!r}")
        for o in q.get("options", []) or []:
            print(f"        opcao: mostra {o.get('value')!r}  ->  envia {o.get('key')!r}")


def cmd_create(a):
    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)

    # A Graph API espera os campos compostos como JSON string dentro do form-encoded.
    payload = {}
    for k, v in spec.items():
        payload[k] = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)

    print(f"Pagina .......: {a.page}")
    print(f"Spec .........: {a.spec}")
    print(f"Nome .........: {spec.get('name')}")
    qs = spec.get("questions", [])
    print(f"Perguntas ....: {len(qs)}")
    for q in qs:
        extra = ""
        if q.get("options"):
            extra = f"  ({len(q['options'])} opcoes)"
        print(f"   - {q.get('type','CUSTOM'):<12} key={q.get('key')!r}{extra}")
    for q in qs:
        for o in q.get("options", []) or []:
            print(f"       mostra {o.get('value')!r}  ->  envia {o.get('key')!r}")

    if not a.aplicar:
        print("\n[dry-run] Nada foi criado. Repita com --aplicar pra valer.")
        return

    tok, nome = page_token(a.page)
    print(f"\nCriando em '{nome}'...")
    d = api(f"{a.page}/leadgen_forms", post=payload, tok=tok)
    print(f"OK. form_id = {d.get('id')}")
    print("Confira com: python scripts/meta-leadform.py show --form " + str(d.get("id")))


def main():
    ap = argparse.ArgumentParser(description="Formularios de Lead Ads pela Graph API")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("pages").set_defaults(func=cmd_pages)

    p = sub.add_parser("list"); p.add_argument("--page", required=True); p.set_defaults(func=cmd_list)

    p = sub.add_parser("show")
    p.add_argument("--form", required=True)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("create")
    p.add_argument("--page", required=True)
    p.add_argument("--spec", required=True)
    p.add_argument("--aplicar", action="store_true", help="sem isso, so mostra o que faria")
    p.set_defaults(func=cmd_create)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
