#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prospeccao por cold mail: coleta leads no Apify, limpa e gerencia a planilha
de disparo do Google Sheets.

Fluxo:
  buscar  -> roda o ator do Apify (Google Maps + contatos do site), limpa o
             resultado e salva um CSV em dados/prospeccao/
  dividir -> parte o CSV em dois (-A e -B), um por conta de disparo
  subir   -> manda os leads limpos pra planilha da conta, ja formatada
  placar  -> le as planilhas e diz quantos ja foram disparados e quantos faltam
  schema  -> mostra os campos de input aceitos pelo ator (util pra ajustar)

Uso:
  python scripts/prospect.py buscar "clinica de estetica" "Caxias do Sul" --limite 300
  python scripts/prospect.py dividir dados/prospeccao/clinica-de-estetica-caxias-do-sul.csv

  # primeira vez de cada conta: passa a planilha, que fica guardada
  python scripts/prospect.py subir <arquivo>-A.csv --conta flow --planilha <URL>
  python scripts/prospect.py subir <arquivo>-B.csv --conta ds   --planilha <URL>
  # depois, so:
  python scripts/prospect.py subir <arquivo>-A.csv --conta flow

  O apelido da conta e livre — use o NOME da conta de disparo (flow, ds), nunca
  "A"/"B": as versoes A e B do texto do e-mail sao outra coisa, e a colisao de
  nome ja causou confusao.

  python scripts/prospect.py placar
  python scripts/prospect.py schema

CADA CONTA DE DISPARO TEM A SUA PLANILHA (nao duas abas na mesma). O Apps Script
manda pelo dono da planilha — duas abas no mesmo arquivo disparariam tudo pela
mesma conta do Gmail.

Credenciais (as duas gitignored):
  scripts/.apify.token.txt       token do Apify (console.apify.com > Settings > API)
  scripts/.gsheets-conta.json    chave da conta de servico do Google Cloud

  A conta de servico so enxerga planilha que foi COMPARTILHADA com o e-mail dela
  (o campo client_email do JSON), como Editor. Ela nao cria planilha: quem cria
  e voce, logado na conta do Gmail que vai disparar.

Config (gitignored, criado no primeiro 'subir'):
  scripts/.prospect-config.json  guarda o id da planilha de cada conta

Os CSVs vao pra dados/prospeccao/, que e gitignored de proposito: lista de lead
tem e-mail de terceiro e nao deve subir pro GitHub.
"""
import sys, os, json, csv, time, re, argparse, unicodedata
import urllib.request, urllib.error
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
TOKEN_FILE = os.path.join(HERE, ".apify.token.txt")
GS_KEY_FILE = os.path.join(HERE, ".gsheets-conta.json")
CONFIG_FILE = os.path.join(HERE, ".prospect-config.json")
SAIDA = os.path.join(RAIZ, "dados", "prospeccao")
BASE = os.path.join(SAIDA, "_base.csv")

ATOR = "lukaskrivka~google-maps-with-contact-details"
API = "https://api.apify.com/v2"

# Caixas que nunca respondem uma abordagem comercial.
PREFIXO_MORTO = {
    "no-reply", "noreply", "nao-responda", "naoresponda", "sac", "financeiro",
    "cobranca", "faturamento", "rh", "curriculo", "curriculos", "vagas",
    "suporte", "atendimento-automatico", "postmaster", "abuse", "webmaster",
}
# Se o mesmo e-mail aparece em N negocios diferentes, e escritorio de
# contabilidade / agencia / franqueadora. Nao e o dono, nao converte.
LIMITE_REPETICAO = 3

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ----------------------------------------------------------------- utilitarios

def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "sem-nome"


def token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit(f"Token do Apify nao encontrado em {TOKEN_FILE}")
    linhas = [
        l.strip() for l in open(TOKEN_FILE, encoding="utf-8")
        if l.strip() and not l.strip().startswith("#")
    ]
    if not linhas:
        sys.exit(
            "O arquivo do token esta vazio.\n"
            "  Cole o Personal API token do Apify em scripts/.apify.token.txt\n"
            "  (console.apify.com > Settings > API & Integrations)."
        )
    return linhas[0]


def http(url, dados=None, metodo=None, timeout=180):
    corpo = json.dumps(dados).encode() if dados is not None else None
    req = urllib.request.Request(url, data=corpo, method=metodo)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            bruto = r.read().decode("utf-8")
            return json.loads(bruto) if bruto else {}
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "ignore")[:500]
        sys.exit(f"Erro HTTP {e.code} em {url.split('?')[0]}\n{detalhe}")


def carrega_config():
    if os.path.exists(CONFIG_FILE):
        return json.load(open(CONFIG_FILE, encoding="utf-8"))
    return {}


def salva_config(cfg):
    json.dump(cfg, open(CONFIG_FILE, "w", encoding="utf-8"), indent=2)


# --------------------------------------------------------------------- limpeza

def extrai_email(item):
    """O ator devolve e-mail em formatos diferentes conforme a versao."""
    for chave in ("emails", "email"):
        v = item.get(chave)
        if isinstance(v, list) and v:
            return str(v[0]).strip().lower()
        if isinstance(v, str) and v.strip():
            return v.strip().lower()
    contatos = item.get("contactDetails") or {}
    if isinstance(contatos, dict):
        v = contatos.get("emails")
        if isinstance(v, list) and v:
            return str(v[0]).strip().lower()
    return ""


def valido(email):
    if not email or "@" not in email:
        return False, "sem e-mail"
    if not re.match(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", email):
        return False, "formato invalido"
    if email.split("@")[0] in PREFIXO_MORTO:
        return False, "caixa morta"
    if email.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        return False, "lixo de scraping"
    return True, ""


def emails_ja_vistos():
    """Conta em quantos negocios diferentes cada e-mail ja apareceu."""
    if not os.path.exists(BASE):
        return Counter(), set()
    contagem, conhecidos = Counter(), set()
    with open(BASE, encoding="utf-8", newline="") as f:
        for linha in csv.DictReader(f):
            e = (linha.get("Email") or "").lower()
            if e:
                contagem[e] += 1
                conhecidos.add(e)
    return contagem, conhecidos


def limpa(itens):
    contagem_base, ja_conhecidos = emails_ja_vistos()

    # Primeira passada: conta repeticao dentro do proprio lote.
    nesse_lote = Counter()
    for it in itens:
        e = extrai_email(it)
        if e:
            nesse_lote[e] += 1

    leads, cortes = [], Counter()
    vistos_agora = set()

    for it in itens:
        email = extrai_email(it)
        ok, motivo = valido(email)
        if not ok:
            cortes[motivo] += 1
            continue
        if email in vistos_agora:
            cortes["duplicado no lote"] += 1
            continue
        if email in ja_conhecidos:
            cortes["ja coletado antes"] += 1
            continue
        if nesse_lote[email] + contagem_base[email] >= LIMITE_REPETICAO:
            cortes["contador/agencia (e-mail repetido)"] += 1
            continue

        vistos_agora.add(email)
        leads.append({
            "Email": email,
            "Empresa": (it.get("title") or it.get("name") or "").strip(),
            "Cidade": (it.get("city") or "").strip(),
            "Categoria": (it.get("categoryName") or "").strip(),
            "Telefone": (it.get("phone") or "").strip(),
            "Site": (it.get("website") or "").strip(),
            "Maps": (it.get("url") or "").strip(),
            "Email Sent": "",
        })

    return leads, cortes


COLUNAS = ["Email", "Empresa", "Cidade", "Categoria", "Telefone", "Site", "Maps", "Email Sent"]


def escreve_csv(caminho, leads, append=False):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    novo = append and os.path.exists(caminho)
    with open(caminho, "a" if novo else "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        if not novo:
            w.writeheader()
        w.writerows(leads)


# ---------------------------------------------------------------------- apify

def cmd_schema(args):
    t = token()
    info = http(f"{API}/acts/{ATOR}/builds/default?token={t}")
    schema = (info.get("data", {}).get("actorDefinition", {}) or {}).get("input", {})
    props = schema.get("properties", {})
    if not props:
        print("Nao consegui ler o schema. Resposta crua:")
        print(json.dumps(info, indent=2)[:2000])
        return
    print(f"Campos de input do ator {ATOR}:\n")
    for nome, d in props.items():
        print(f"  {nome:35s} {d.get('type','?'):8s} {d.get('title','')}")


def cmd_buscar(args):
    t = token()
    entrada = {
        "searchStringsArray": [args.nicho],
        "locationQuery": f"{args.cidade}, Brazil",
        "maxCrawledPlacesPerSearch": args.limite,
        "language": "pt-BR",
        "skipClosedPlaces": True,
    }
    if args.extra:
        entrada.update(json.loads(args.extra))

    print(f"Rodando o ator no Apify: '{args.nicho}' em {args.cidade} (max {args.limite})...")
    run = http(f"{API}/acts/{ATOR}/runs?token={t}", dados=entrada)
    run_id = run["data"]["id"]
    dataset = run["data"]["defaultDatasetId"]

    espera = 0
    while True:
        time.sleep(10)
        espera += 10
        st = http(f"{API}/actor-runs/{run_id}?token={t}")["data"]["status"]
        print(f"  [{espera:>4}s] {st}")
        if st in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        if espera > args.timeout:
            sys.exit(f"Passou de {args.timeout}s. Ve o run em console.apify.com/actors/runs/{run_id}")

    if st != "SUCCEEDED":
        sys.exit(f"O run terminou como {st}. Detalhes: console.apify.com/actors/runs/{run_id}")

    itens = http(f"{API}/datasets/{dataset}/items?token={t}&clean=true")
    if not isinstance(itens, list):
        sys.exit(f"Resposta inesperada do dataset: {str(itens)[:300]}")

    leads, cortes = limpa(itens)

    nome = f"{slug(args.nicho)}-{slug(args.cidade)}.csv"
    caminho = os.path.join(SAIDA, nome)
    escreve_csv(caminho, leads)
    escreve_csv(BASE, leads, append=True)

    print(f"\n  Lugares coletados : {len(itens)}")
    for motivo, n in cortes.most_common():
        print(f"  - {motivo:35s} {n}")
    print(f"  LEADS APROVEITAVEIS: {len(leads)}")
    if itens:
        print(f"  Taxa de e-mail    : {len(leads)/len(itens)*100:.0f}%")
    print(f"\n  Salvo em: {os.path.relpath(caminho, RAIZ)}")
    if leads:
        print(f"\n  Amostra:")
        for l in leads[:5]:
            print(f"    {l['Email']:40s} {l['Empresa'][:35]}")


# -------------------------------------------------------------------- dividir

def cmd_dividir(args):
    """Parte o CSV em dois, um por conta de disparo.

    Existe porque cada conta do Gmail dispara da sua propria planilha, e a mesma
    pessoa NAO pode receber as duas versoes do texto: alem de queimar a
    credibilidade, mistura o teste A/B.

    Intercala (par/impar) em vez de cortar no meio pra que as duas metades
    fiquem com a mesma mistura de bairro, categoria e porte — o ator devolve
    ordenado por relevancia do Maps, entao cortar no meio daria uma metade
    sistematicamente melhor que a outra.
    """
    with open(args.arquivo, encoding="utf-8", newline="") as f:
        leads = list(csv.DictReader(f))
    if not leads:
        sys.exit("O CSV esta vazio.")

    base, _ = os.path.splitext(args.arquivo)
    partes = [(f"{base}-A.csv", leads[0::2]), (f"{base}-B.csv", leads[1::2])]

    for caminho, parte in partes:
        escreve_csv(caminho, parte)
        print(f"  {len(parte):4d} leads -> {os.path.relpath(caminho, RAIZ)}")

    print(f"\n  Total dividido: {len(leads)}")
    print("  A -> conta que leva a versao A | B -> conta que leva a versao B")


# --------------------------------------------------------------------- sheets

def servico_sheets():
    if not os.path.exists(GS_KEY_FILE):
        sys.exit(
            f"Chave da conta de servico nao encontrada em {GS_KEY_FILE}\n"
            "  Baixe o JSON no Google Cloud (IAM > Contas de servico > Chaves)\n"
            "  e salve com esse nome exato."
        )
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    cred = service_account.Credentials.from_service_account_file(
        GS_KEY_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("sheets", "v4", credentials=cred, cache_discovery=False)


def so_id(pid):
    """Aceita tanto o ID cru quanto a URL inteira da planilha."""
    if "/" in pid:
        m = re.search(r"/d/([a-zA-Z0-9_-]+)", pid)
        return m.group(1) if m else pid
    return pid


def id_planilha(args):
    """Cada conta de disparo tem a SUA planilha, guardada por apelido.

    Sao duas planilhas separadas (nao duas abas) porque o Apps Script dispara
    pelo dono da planilha — duas abas no mesmo arquivo mandariam tudo pela
    mesma conta do Gmail.
    """
    cfg = carrega_config()
    planilhas = cfg.setdefault("planilhas", {})

    # migra o formato antigo (uma planilha so, sem apelido)
    if "planilha" in cfg and not planilhas:
        planilhas["A"] = cfg.pop("planilha")
        salva_config(cfg)

    conta = (getattr(args, "conta", None) or "A").upper()
    pid = getattr(args, "planilha", None)

    if pid:
        pid = so_id(pid)
        if planilhas.get(conta) != pid:
            planilhas[conta] = pid
            salva_config(cfg)
            print(f"  Planilha da conta {conta} guardada.")
        return pid

    if conta not in planilhas:
        conhecidas = ", ".join(sorted(planilhas)) or "nenhuma ainda"
        sys.exit(
            f"Nao sei qual planilha e a da conta {conta}.\n"
            f"  Rode uma vez com --planilha <ID ou URL> que eu guardo.\n"
            f"  Contas ja configuradas: {conhecidas}"
        )
    return planilhas[conta]


def garante_aba(svc, pid, aba):
    """Cria a aba se nao existir. Devolve o gid (id numerico da aba)."""
    meta = svc.spreadsheets().get(spreadsheetId=pid).execute()
    for s in meta["sheets"]:
        if s["properties"]["title"] == aba:
            return s["properties"]["sheetId"]
    novo = svc.spreadsheets().batchUpdate(
        spreadsheetId=pid,
        body={"requests": [{"addSheet": {"properties": {"title": aba}}}]},
    ).execute()
    print(f"  Aba '{aba}' criada.")
    return novo["replies"][0]["addSheet"]["properties"]["sheetId"]


def formata_aba(svc, pid, gid, aba):
    """Deixa a aba usavel: cabecalho congelado, negrito, colunas no tamanho.

    Idempotente — pode rodar toda vez que sobe lead novo. A regra de cor
    condicional so entra se a aba ainda nao tiver nenhuma, senao cada execucao
    empilharia uma regra nova.
    """
    fim = len(COLUNAS)
    col_enviado = chr(ord("A") + COLUNAS.index("Email Sent"))  # -> "H"

    # ja tem regra condicional aqui?
    meta = svc.spreadsheets().get(
        spreadsheetId=pid, fields="sheets(properties.sheetId,conditionalFormats)").execute()
    tem_regra = any(
        s["properties"]["sheetId"] == gid and s.get("conditionalFormats")
        for s in meta.get("sheets", []))

    pedidos = [
        # congela a linha do cabecalho
        {"updateSheetProperties": {
            "properties": {"sheetId": gid, "gridProperties": {"frozenRowCount": 1}},
            "fields": "gridProperties.frozenRowCount"}},
        # cabecalho em negrito, fundo cinza
        {"repeatCell": {
            "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 1,
                      "startColumnIndex": 0, "endColumnIndex": fim},
            "cell": {"userEnteredFormat": {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.93, "green": 0.93, "blue": 0.93}}},
            "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        # largura das colunas pelo conteudo
        {"autoResizeDimensions": {
            "dimensions": {"sheetId": gid, "dimension": "COLUMNS",
                           "startIndex": 0, "endIndex": fim}}},
    ]

    if not tem_regra:
        # "Email Sent" preenchida = linha ja disparada, fica esverdeada
        pedidos.append({"addConditionalFormatRule": {"index": 0, "rule": {
            "ranges": [{"sheetId": gid, "startRowIndex": 1,
                        "startColumnIndex": 0, "endColumnIndex": fim}],
            "booleanRule": {
                "condition": {"type": "CUSTOM_FORMULA", "values": [
                    {"userEnteredValue": f"=NOT(ISBLANK(${col_enviado}2))"}]},
                "format": {"backgroundColor": {
                    "red": 0.90, "green": 0.96, "blue": 0.90}}}}}})
    try:
        svc.spreadsheets().batchUpdate(
            spreadsheetId=pid, body={"requests": pedidos}).execute()
    except Exception as e:
        # formatacao e cosmetica: se falhar, os dados ja subiram e isso basta
        print(f"  (aviso: nao consegui formatar a aba — {str(e)[:120]})")


def cmd_subir(args):
    pid = id_planilha(args)
    svc = servico_sheets()
    gid = garante_aba(svc, pid, args.aba)

    with open(args.arquivo, encoding="utf-8", newline="") as f:
        leads = list(csv.DictReader(f))
    if not leads:
        sys.exit("O CSV esta vazio.")

    atual = svc.spreadsheets().values().get(
        spreadsheetId=pid, range=f"'{args.aba}'!A:H"
    ).execute().get("values", [])

    ja_la = {l[0].lower() for l in atual[1:] if l}
    novos = [l for l in leads if l["Email"].lower() not in ja_la]
    if not novos:
        print("Nenhum lead novo — todos ja estao na aba.")
        formata_aba(svc, pid, gid, args.aba)
        return

    valores = [] if atual else [COLUNAS]
    valores += [[l.get(c, "") for c in COLUNAS] for l in novos]

    svc.spreadsheets().values().append(
        spreadsheetId=pid,
        range=f"'{args.aba}'!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": valores},
    ).execute()

    formata_aba(svc, pid, gid, args.aba)

    print(f"  {len(novos)} leads novos na aba '{args.aba}'.")
    if len(leads) - len(novos):
        print(f"  {len(leads)-len(novos)} ja estavam la e foram ignorados.")
    print(f"  https://docs.google.com/spreadsheets/d/{pid}/edit")


def cmd_placar(args):
    """Sem --conta, mostra o placar de TODAS as planilhas configuradas."""
    svc = servico_sheets()

    if args.conta or args.planilha:
        alvos = [((args.conta or "A").upper(), id_planilha(args))]
    else:
        planilhas = carrega_config().get("planilhas", {})
        if not planilhas:
            sys.exit("Nenhuma planilha configurada. Rode 'subir' uma vez com --planilha.")
        alvos = sorted(planilhas.items())

    for conta, pid in alvos:
        print(f"=== Conta {conta}")
        placar_de(svc, pid)
        print()


def placar_de(svc, pid):
    meta = svc.spreadsheets().get(spreadsheetId=pid).execute()

    print(f"Planilha: {meta['properties']['title']}\n")
    for s in meta["sheets"]:
        aba = s["properties"]["title"]
        linhas = svc.spreadsheets().values().get(
            spreadsheetId=pid, range=f"'{aba}'!A:H"
        ).execute().get("values", [])
        if len(linhas) < 2:
            continue
        cab = linhas[0]
        try:
            col = cab.index("Email Sent")
        except ValueError:
            continue
        corpo = linhas[1:]
        enviados = sum(1 for l in corpo if len(l) > col and l[col].strip())
        print(f"  {aba}")
        print(f"    total     {len(corpo)}")
        print(f"    enviados  {enviados}")
        print(f"    na fila   {len(corpo)-enviados}")


# ------------------------------------------------------------------------ cli

def main():
    p = argparse.ArgumentParser(description="Prospeccao por cold mail: Apify + Google Sheets")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("buscar", help="roda o ator do Apify e salva o CSV limpo")
    b.add_argument("nicho")
    b.add_argument("cidade")
    b.add_argument("--limite", type=int, default=50)
    b.add_argument("--timeout", type=int, default=900)
    b.add_argument("--extra", help="JSON com campos extras de input do ator")
    b.set_defaults(func=cmd_buscar)

    d = sub.add_parser("dividir", help="parte o CSV em dois, um por conta de disparo")
    d.add_argument("arquivo")
    d.set_defaults(func=cmd_dividir)

    s = sub.add_parser("subir", help="manda um CSV limpo pra planilha, ja formatada")
    s.add_argument("arquivo")
    s.add_argument("--conta", default="flow",
                   help="apelido da conta de disparo (use o nome dela: flow, ds...)")
    s.add_argument("--aba", default="Leads")
    s.add_argument("--planilha", help="ID ou URL (so na primeira vez de cada conta)")
    s.set_defaults(func=cmd_subir)

    pl = sub.add_parser("placar", help="quantos ja foram disparados (todas as contas)")
    pl.add_argument("--conta", help="so uma conta; sem isso mostra todas")
    pl.add_argument("--planilha")
    pl.set_defaults(func=cmd_placar)

    sc = sub.add_parser("schema", help="campos de input aceitos pelo ator")
    sc.set_defaults(func=cmd_schema)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
