#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponte entre o FlowOS e a Meta Marketing API (Graph API).

Rota ALTERNATIVA ao conector MCP oficial da Meta. As duas coexistem de proposito;
o comparativo de quando usar cada uma esta em
.claude/skills/relatorio-ads/references/fontes-de-dados.md

Resumo: o conector MCP e conversa (voce pergunta, ele responde, ele executa). Este
script e dado bruto (roda sozinho, agendado, cospe CSV/JSON pra empilhar historico
ou jogar num banco). Python puro (urllib), sem dependencia pra instalar.

Uso:
  python scripts/meta-ads.py accounts
      Lista as contas de anuncio que o token enxerga.

  python scripts/meta-ads.py insights --account act_123 [--level campaign]
                                      [--preset last_7d | --since AAAA-MM-DD --until AAAA-MM-DD]
                                      [--daily] [--csv arquivo.csv] [--json]
      Puxa performance. Default: nivel campanha, ultimos 7 dias, tabela no terminal.
      --daily quebra dia a dia (time_increment=1), que e o formato pra empilhar historico.
      --csv escreve no formato que a /relatorio-ads ja le.

  python scripts/meta-ads.py entities --account act_123 --type campaigns|adsets|ads
      Lista as entidades da conta (id, nome, status, objetivo, orcamento).

  ESCRITA (mexe na conta de verdade). Todo comando abaixo e ENSAIO por padrao:
  mostra o de->para e nao altera nada. So aplica com --aplicar.

  python scripts/meta-ads.py pausar   --id 123 [--aplicar]
  python scripts/meta-ads.py ativar   --id 123 [--aplicar]
      Liga/desliga campanha, conjunto ou anuncio (o nivel e detectado sozinho).

  python scripts/meta-ads.py orcamento --id 123 --diario 26.67 [--aplicar]
  python scripts/meta-ads.py orcamento --id 123 --total 800    [--aplicar]
      Orcamento em REAIS (o script converte pra centavos). --diario e o de cada
      dia; --total e o vitalicio do periodo. Trocar diario<->vitalicio numa
      entidade que ja roda reinicia a fase de aprendizado da Meta.

  python scripts/meta-ads.py agendar --id 123 --fim 2026-09-05 [--aplicar]
      Data de inicio/termino. So data (AAAA-MM-DD) vale dia inteiro: --inicio
      comeca 00:00 e --fim termina 23:59, no fuso da propria entidade.

Token: scripts/.meta.token.txt (gitignored pelo padrao *.token.txt).
  1. developers.facebook.com > seu app > Ferramentas > Explorador de Graph API,
     permissao ads_read (leitura) > Gerar token. Esse e "short-lived": dura 1-2 HORAS.
  2. Ferramentas > Depurador de token > colar > Depurar > Estender token de acesso.
     Vira "long-lived": ~60 dias. (A Meta avisa que o prazo pode mudar sem aviso.)
  3. Pra rotina agendada, nao use nenhum dos dois: gere um token de System User na
     Business Manager (Business Settings > Usuarios do sistema). Esse nao expira.

Este script LE e ESCREVE (o token precisa de ads_management pra escrever; so com
ads_read os comandos de escrita falham com erro de permissao).

Por que escrever aqui e nao no conector MCP: o conector PAUSA a entidade que voce
edita (devolve status_forced_to_paused) -- editar orcamento de campanha no ar a
derruba, e ela so volta com uma chamada de ativacao separada. Ele tambem responde
"sucesso" para campo que nao gravou, porque ecoa o pedido, nao o estado salvo.
Aqui a edicao e cirurgica e todo comando le de volta pra provar o que ficou.
"""
import sys, os, csv, json, argparse, urllib.request, urllib.parse, urllib.error

# Meta lanca versao nova ~3x por ano e aposenta cada uma em ~1 ano.
# Conferido na fonte oficial (developers.facebook.com/docs/graph-api/changelog/versions)
# em 28/jul/2026:
#   v25.0  lancada 18/fev/2026  <- atual, a que usamos
#   v24.0  expira  06/out/2026  <- proxima parede: subir pra v26 quando ela sair (~set/2026)
#   v23.0  EXPIROU 09/jun/2026  <- nao usar
# Se a API responder "Unsupported get request" ou erro de versao invalida, e isto aqui.
API_VERSION = "v25.0"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOKEN_FILE = os.path.join(HERE, ".meta.token.txt")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

INSIGHT_FIELDS = [
    "impressions", "reach", "frequency", "clicks", "inline_link_clicks",
    "ctr", "inline_link_click_ctr", "cpc", "cpm", "spend",
    "actions", "cost_per_action_type",
]
LEVEL_NAME_FIELD = {
    "account": ("account_id", "account_name"),
    "campaign": ("campaign_id", "campaign_name"),
    "adset": ("adset_id", "adset_name"),
    "ad": ("ad_id", "ad_name"),
}
# action_type da Meta -> coluna legivel. Varios tipos somam na mesma coluna
# (a Meta reporta a mesma conversao por caminhos diferentes conforme a config).
ACTION_MAP = {
    "compras": ("purchase", "omni_purchase", "offsite_conversion.fb_pixel_purchase"),
    "leads": ("lead", "onsite_conversion.lead_grouped", "offsite_conversion.fb_pixel_lead"),
    "conversas": ("onsite_conversion.messaging_conversation_started_7d",),
}


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(
            f"Token nao encontrado em {TOKEN_FILE}\n"
            "Crie o arquivo com o access token da Meta (so o token, sem aspas).\n"
            "Onde pegar: developers.facebook.com > app > Graph API Explorer (permissao ads_read)."
        )
    with open(TOKEN_FILE, encoding="utf-8") as f:
        return f.read().strip()


def api(path, params=None):
    params = dict(params or {})
    params["access_token"] = token()
    url = f"https://graph.facebook.com/{API_VERSION}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(body)["error"]["message"]
        except Exception:
            msg = body
        sys.exit(f"HTTP {e.code} em {path}: {msg}")


def paged(path, params=None, limit_pages=50):
    """Junta as paginas de um endpoint da Graph API ({data, paging.next})."""
    out = []
    d = api(path, params)
    out.extend(d.get("data", []))
    for _ in range(limit_pages):
        nxt = d.get("paging", {}).get("next")
        if not nxt:
            break
        with urllib.request.urlopen(nxt) as r:
            d = json.loads(r.read().decode("utf-8"))
        out.extend(d.get("data", []))
    return out


def sum_actions(rows, types):
    """Soma o valor dos action_types pedidos. rows = lista [{action_type, value}]."""
    total = 0.0
    for r in rows or []:
        if r.get("action_type") in types:
            total += float(r.get("value") or 0)
    return total


def flatten(row, level):
    id_field, name_field = LEVEL_NAME_FIELD[level]
    out = {
        "nivel": level,
        "id": row.get(id_field, ""),
        "nome": row.get(name_field, ""),
        "data_inicio": row.get("date_start", ""),
        "data_fim": row.get("date_stop", ""),
        "impressoes": row.get("impressions", ""),
        "alcance": row.get("reach", ""),
        "frequencia": row.get("frequency", ""),
        "cliques": row.get("clicks", ""),
        "cliques_link": row.get("inline_link_clicks", ""),
        "ctr": row.get("ctr", ""),
        "ctr_link": row.get("inline_link_click_ctr", ""),
        "cpc": row.get("cpc", ""),
        "cpm": row.get("cpm", ""),
        "gasto": row.get("spend", ""),
    }
    for col, types in ACTION_MAP.items():
        n = sum_actions(row.get("actions"), types)
        out[col] = int(n) if n else 0
        custo = sum_actions(row.get("cost_per_action_type"), types)
        out[f"custo_por_{col[:-1] if col.endswith('s') else col}"] = round(custo, 2) if custo else ""
    return out


def estado_do_token():
    """Devolve (dias_restantes, texto). None se a Meta nao informar prazo.

    Sao DOIS relogios diferentes e o que pega e sempre o segundo:
      expires_at ............ validade do token. 0 = nunca expira.
      data_access_expires_at  'Expiracao do acesso a dados': 90 dias de consentimento.
                              Quando vence, as chamadas param mesmo com token valido.
    So o usuario destrava isso, reautorizando no navegador -- e de proposito, e
    controle de privacidade da Meta. Nenhum script renova (nem com App Secret).
    """
    import datetime
    d = api("debug_token", {"input_token": token()}).get("data", {})
    ts = d.get("data_access_expires_at") or 0
    if not ts:
        return None, "sem prazo informado"
    quando = datetime.datetime.fromtimestamp(ts)
    dias = (quando - datetime.datetime.now()).days
    return dias, quando.strftime("%d/%m/%Y")


def aviso_token():
    """Chamado antes de qualquer comando: some quando falta muito, grita quando falta pouco."""
    try:
        dias, quando = estado_do_token()
    except SystemExit:
        return
    except Exception:
        return
    if dias is None or dias > 21:
        return
    if dias < 0:
        print(f"!! ACESSO A DADOS VENCIDO em {quando}. Reautorize antes de seguir.\n")
    else:
        print(f"!! Acesso a dados vence em {dias} dia(s) ({quando}). Reautorize no Graph API Explorer.\n")


def cmd_token(a):
    d = api("debug_token", {"input_token": token()}).get("data", {})
    dias, quando = estado_do_token()
    print(f"app ............... {d.get('application')} ({d.get('app_id')})")
    print(f"tipo .............. {d.get('type')}")
    print(f"valido ............ {d.get('is_valid')}")
    exp = d.get("expires_at") or 0
    print(f"token expira ...... {'nunca' if not exp else exp}")
    print(f"acesso a dados .... {quando}" + (f"  ({dias} dias)" if dias is not None else ""))
    print(f"escopos ........... {', '.join(d.get('scopes', []))}")
    if dias is not None and dias <= 21:
        print("\nRenovar: Graph API Explorer > gerar token > Depurador > Estender.")
        print("Nao da pra automatizar: reautorizacao exige o usuario no navegador.")


def cmd_accounts(a):
    fields = "id,name,account_status,currency,business{id,name}"
    rows = paged("me/adaccounts", {"fields": fields, "limit": 100})
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    print(f"{len(rows)} contas visiveis pelo token:\n")
    for r in rows:
        biz = (r.get("business") or {}).get("name", "-")
        ativo = "ATIVA" if r.get("account_status") == 1 else f"status {r.get('account_status')}"
        print(f"  {r['id']:<24} {ativo:<10} {r.get('currency','')}  {r.get('name','(sem nome)')}  [{biz}]")


def cmd_insights(a):
    params = {
        "level": a.level,
        "fields": ",".join(INSIGHT_FIELDS + list(LEVEL_NAME_FIELD[a.level])),
        "limit": 500,
    }
    if a.since or a.until:
        if not (a.since and a.until):
            sys.exit("--since e --until andam juntos.")
        params["time_range"] = json.dumps({"since": a.since, "until": a.until})
    else:
        params["date_preset"] = a.preset
    if a.daily:
        params["time_increment"] = 1

    rows = [flatten(r, a.level) for r in paged(f"{a.account}/insights", params)]
    if not rows:
        print("Nenhum dado no periodo (conta sem veiculacao ou intervalo vazio).")
        return

    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    cols = list(rows[0].keys())
    if a.csv:
        path = a.csv if os.path.isabs(a.csv) else os.path.join(ROOT, a.csv)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"{len(rows)} linhas escritas em {path}")
        return

    gasto = sum(float(r["gasto"] or 0) for r in rows)
    print(f"{len(rows)} linhas | nivel {a.level} | gasto total {gasto:,.2f}\n")
    for r in rows:
        print(f"  {r['data_inicio']}  {r['nome'][:44]:<44} gasto {float(r['gasto'] or 0):>9,.2f}  "
              f"cliques {r['cliques'] or 0:>6}  compras {r['compras']:>4}  leads {r['leads']:>4}")


def cmd_entities(a):
    fields = {
        "campaigns": "id,name,status,objective,daily_budget,lifetime_budget,start_time",
        "adsets": "id,name,status,campaign_id,daily_budget,optimization_goal,start_time",
        "ads": "id,name,status,adset_id,creative{id,name}",
    }[a.type]
    rows = paged(f"{a.account}/{a.type}", {"fields": fields, "limit": 200})
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    print(f"{len(rows)} {a.type}:\n")
    for r in rows:
        extra = r.get("objective") or r.get("optimization_goal") or ""
        print(f"  {r['id']:<20} {r.get('status',''):<10} {extra:<28} {r.get('name','')}")


# --------------------------------------------------------------------- escrita
# Daqui pra baixo o script mexe na conta. Tres guardas, sempre nessa ordem:
#   1. le a entidade ANTES e imprime o de->para;
#   2. nao aplica nada sem --aplicar (sem a flag, e ensaio);
#   3. le de novo DEPOIS e imprime o que ficou salvo -- porque "sucesso" na
#      resposta da API nao e prova de que o campo gravou.

# Campo exclusivo de cada nivel (a "sonda") + como cada um chama data de inicio
# e de fim. Campanha e conjunto discordam no nome do fim, e essa e a pegadinha
# que mais custa tempo: agendar no campo errado passa sem erro e nao faz nada.
NIVEL = {
    "conjunto": {"sonda": "optimization_goal", "inicio": "start_time", "fim": "end_time"},
    "campanha": {"sonda": "objective", "inicio": "start_time", "fim": "stop_time"},
    "anuncio": {"sonda": "adset_id", "inicio": None, "fim": None},
}


def api_ok(path, params=None):
    """GET que devolve (deu_certo, dados) em vez de derrubar o processo."""
    p = dict(params or {})
    p["access_token"] = token()
    url = f"https://graph.facebook.com/{API_VERSION}/{path}?" + urllib.parse.urlencode(p)
    try:
        with urllib.request.urlopen(url) as r:
            return True, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError:
        return False, {}


def api_post(path, campos):
    dados = dict(campos)
    dados["access_token"] = token()
    req = urllib.request.Request(
        f"https://graph.facebook.com/{API_VERSION}/{path}",
        data=urllib.parse.urlencode(dados).encode(),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            msg = json.loads(body)["error"]["message"]
        except Exception:
            msg = body
        sys.exit(f"HTTP {e.code} ao escrever em {path}: {msg}")


def detectar(oid):
    """Descobre se o ID e conjunto, campanha ou anuncio sondando um campo exclusivo."""
    for nivel, cfg in NIVEL.items():
        ok, _ = api_ok(oid, {"fields": cfg["sonda"]})
        if ok:
            return nivel
    sys.exit(f"ID {oid} nao encontrado, ou o token nao enxerga essa entidade.")


def estado(oid, nivel):
    campos = ["id", "name", "status", "effective_status"]
    cfg = NIVEL[nivel]
    if nivel != "anuncio":
        campos += ["daily_budget", "lifetime_budget"]
        campos += [c for c in (cfg["inicio"], cfg["fim"]) if c]
    ok, d = api_ok(oid, {"fields": ",".join(campos)})
    if not ok:
        sys.exit(f"Nao consegui ler {oid}.")
    return d


def bateu(campo, esperado, salvo):
    """Compara pedido x salvo. Em data, so o dia -- a Meta normaliza o fuso."""
    if salvo in (None, ""):
        return False
    if campo.endswith("_time"):
        return str(salvo)[:10] == str(esperado)[:10]
    return str(salvo) == str(esperado)


def escrever(oid, mudancas, a, nivel=None):
    nivel = nivel or detectar(oid)
    antes = estado(oid, nivel)
    print(f"{nivel} {oid} | {antes.get('name', '')}\n")
    for campo, novo in mudancas.items():
        print(f"  {campo:<16} {antes.get(campo) or '(vazio)':<32} ->  {novo}")
    if not a.aplicar:
        print("\nENSAIO: nada foi alterado. Repita com --aplicar pra valer.")
        return
    api_post(oid, mudancas)
    depois = estado(oid, nivel)
    print("\nLido de volta da Meta:")
    falhou = False
    for campo, novo in mudancas.items():
        salvo = depois.get(campo)
        ok = bateu(campo, novo, salvo)
        falhou = falhou or not ok
        print(f"  {campo:<16} {salvo or '(vazio)':<32} [{'ok' if ok else 'NAO GRAVOU'}]")
    if falhou:
        sys.exit("\n!! Pelo menos um campo nao gravou. Confira no Gerenciador antes de seguir.")


def centavos(reais):
    return int(round(float(str(reais).replace(",", ".")) * 100))


def com_fuso(data, fim, referencia):
    """AAAA-MM-DD -> ISO completo no MESMO fuso que a entidade ja usa.

    O fuso sai do start_time da propria entidade em vez de ser fixo no codigo:
    conta de cliente em outro pais agenda no horario dela, nao no nosso.
    """
    if "T" in data:
        return data
    fuso = str(referencia or "")[-5:]
    if not (len(fuso) == 5 and fuso[0] in "+-"):
        fuso = "+0000"
    return f"{data}T{'23:59:00' if fim else '00:00:00'}{fuso}"


def cmd_pausar(a):
    escrever(a.id, {"status": "PAUSED"}, a)


def cmd_ativar(a):
    escrever(a.id, {"status": "ACTIVE"}, a)


def cmd_orcamento(a):
    if bool(a.diario) == bool(a.total):
        sys.exit("Escolha um: --diario OU --total (em reais).")
    campo = "daily_budget" if a.diario else "lifetime_budget"
    escrever(a.id, {campo: centavos(a.diario or a.total)}, a)


def cmd_agendar(a):
    if not (a.inicio or a.fim):
        sys.exit("Informe --inicio e/ou --fim (AAAA-MM-DD).")
    nivel = detectar(a.id)
    cfg = NIVEL[nivel]
    if not cfg["fim"]:
        sys.exit("Anuncio nao tem agendamento proprio: agende no conjunto.")
    atual = estado(a.id, nivel)
    ref = atual.get(cfg["inicio"])
    mudancas = {}
    if a.inicio:
        mudancas[cfg["inicio"]] = com_fuso(a.inicio, False, ref)
    if a.fim:
        mudancas[cfg["fim"]] = com_fuso(a.fim, True, ref)
    escrever(a.id, mudancas, a, nivel)


def main():
    ap = argparse.ArgumentParser(description="Ponte FlowOS <-> Meta Marketing API (le e escreve)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    tk = sub.add_parser("token", help="quanto tempo falta pro acesso a dados vencer")
    tk.set_defaults(func=cmd_token)

    ac = sub.add_parser("accounts", help="lista as contas que o token enxerga")
    ac.add_argument("--json", action="store_true")
    ac.set_defaults(func=cmd_accounts)

    ins = sub.add_parser("insights", help="puxa performance")
    ins.add_argument("--account", required=True, help="ex: act_1234567890")
    ins.add_argument("--level", default="campaign", choices=list(LEVEL_NAME_FIELD))
    ins.add_argument("--preset", default="last_7d",
                     help="date_preset da Meta: today, yesterday, last_7d, last_30d, this_month, last_month...")
    ins.add_argument("--since", help="AAAA-MM-DD (usar junto com --until)")
    ins.add_argument("--until", help="AAAA-MM-DD")
    ins.add_argument("--daily", action="store_true", help="quebra dia a dia (pra empilhar historico)")
    ins.add_argument("--csv", help="caminho do CSV de saida (relativo a raiz do FlowOS)")
    ins.add_argument("--json", action="store_true")
    ins.set_defaults(func=cmd_insights)

    en = sub.add_parser("entities", help="lista campanhas / conjuntos / anuncios")
    en.add_argument("--account", required=True)
    en.add_argument("--type", default="campaigns", choices=["campaigns", "adsets", "ads"])
    en.add_argument("--json", action="store_true")
    en.set_defaults(func=cmd_entities)

    # --- escrita: todo comando daqui nasce em ensaio e so aplica com --aplicar
    for nome, ajuda, func in [
        ("pausar", "desliga campanha, conjunto ou anuncio", cmd_pausar),
        ("ativar", "liga campanha, conjunto ou anuncio", cmd_ativar),
    ]:
        p = sub.add_parser(nome, help=ajuda)
        p.add_argument("--id", required=True, help="id da campanha, conjunto ou anuncio")
        p.add_argument("--aplicar", action="store_true", help="sem isso e so ensaio")
        p.set_defaults(func=func)

    orc = sub.add_parser("orcamento", help="muda o orcamento (em reais)")
    orc.add_argument("--id", required=True)
    orc.add_argument("--diario", help="orcamento de cada dia, em reais. ex: 26.67")
    orc.add_argument("--total", help="orcamento vitalicio do periodo, em reais. ex: 800")
    orc.add_argument("--aplicar", action="store_true", help="sem isso e so ensaio")
    orc.set_defaults(func=cmd_orcamento)

    ag = sub.add_parser("agendar", help="define inicio e/ou termino")
    ag.add_argument("--id", required=True)
    ag.add_argument("--inicio", help="AAAA-MM-DD (comeca 00:00)")
    ag.add_argument("--fim", help="AAAA-MM-DD (termina 23:59)")
    ag.add_argument("--aplicar", action="store_true", help="sem isso e so ensaio")
    ag.set_defaults(func=cmd_agendar)

    args = ap.parse_args()
    if args.func is not cmd_token:
        aviso_token()
    args.func(args)


if __name__ == "__main__":
    main()
