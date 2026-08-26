# -*- coding: utf-8 -*-
r"""
editor-carrossel.py -- painel local de edicao visual dos slides de carrossel.

Sobe um servidor em 127.0.0.1 e abre o navegador. O painel carrega os
slide-NN.html da pasta do conteudo em iframe (mesmo Chrome que renderiza o PNG,
entao o que aparece na tela e exatamente o que sai na imagem), deixa editar
texto no lugar, ajustar tipo/cor/espaco/posicao, trocar imagem, reordenar
slides e disparar o render.

Uso:
    python scripts/editor-carrossel.py
    python scripts/editor-carrossel.py --pasta marketing/conteudo/<pasta>
    python scripts/editor-carrossel.py --porta 8790 --nao-abrir

Como o ajuste e salvo:
    o painel escreve style="" inline no proprio elemento do slide-NN.html e
    anota em data-ed quais propriedades ele tocou. Nada de camada nova: o
    arquivo continua sendo HTML legivel, e o "Limpar ajustes" sabe desfazer
    exatamente o que foi mexido. Antes da primeira escrita de cada slide, o
    original vai pra .editor-backup/ (dai o "Restaurar original").

Gotcha desta maquina: o repo vive sob caminho longo e acentuado do OneDrive, e
o MAX_PATH de 260 chars quebra open() em Python puro. Todo acesso a arquivo
aqui passa por longo(), que prefixa \\?\.
"""

import argparse
import io
import json
import os
import re
import shutil
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote, quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_slides  # noqa: E402  (vizinho em scripts/)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "editor-carrossel", "app.html")
BACKUP = ".editor-backup"
LIXO = ".editor-lixo"

TIPOS = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".avif": "image/avif",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
}
EXT_IMG = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif")


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
    # O prefixo \\?\ desliga a normalizacao do Windows, entao o caminho tem que
    # chegar canonico: com \\?\d:\... (unidade minuscula) o open() morre com
    # Errno 22. abspath NAO conserta a caixa da unidade -- fazemos na mao.
    unidade, resto = os.path.splitdrive(p)
    return "\\\\?\\" + unidade.upper() + resto


def ler_texto(caminho):
    with io.open(longo(caminho), "r", encoding="utf-8") as f:
        return f.read()


def escrever_texto(caminho, texto):
    with io.open(longo(caminho), "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def dentro(base, alvo):
    """Impede path traversal: alvo tem que viver debaixo de base."""
    base = os.path.normcase(os.path.abspath(base))
    alvo = os.path.normcase(os.path.abspath(alvo))
    return alvo == base or alvo.startswith(base + os.sep)


def resolver_pasta(caminho):
    """Resolve o que o usuario apontou numa pasta de slides, em caminho absoluto seguro.

    Aceita de proposito tudo que da pra colar sem pensar:
      - relativo a raiz do repo:  marketing/conteudo/<pasta>
      - caminho absoluto do Windows, com ou sem acento e com \\ ou /
      - entre aspas (e o que o Explorer e o "Copiar caminho" do VS Code entregam)
      - o caminho de um slide-NN.html: a gente sobe pra pasta dele
    """
    bruto = (caminho or "").strip().strip('"').strip("'").strip()
    if not bruto:
        raise ValueError("nao veio caminho nenhum")

    bruto = bruto.replace("\\", "/")

    if os.path.isabs(bruto) or re.match(r"^[A-Za-z]:/", bruto):
        alvo = os.path.abspath(bruto)
    else:
        alvo = os.path.join(RAIZ, *[p for p in bruto.split("/") if p not in ("", ".")])

    # apontou pro arquivo em vez da pasta: usa a pasta que o contem
    if os.path.isfile(longo(alvo)):
        alvo = os.path.dirname(alvo)

    if not dentro(RAIZ, alvo):
        raise ValueError("esse caminho esta fora do FlowOS -- o painel so abre pasta de dentro do repo")
    if not os.path.isdir(longo(alvo)):
        raise ValueError("nao achei essa pasta: %s" % bruto)
    if not slides_de(alvo):
        raise ValueError("a pasta existe mas nao tem nenhum slide-NN.html dentro: %s"
                         % os.path.relpath(alvo, RAIZ).replace("\\", "/"))
    return alvo


def slides_de(pasta):
    nomes = [
        n for n in os.listdir(longo(pasta))
        if re.match(r"^slide-\d+\.html$", n, re.I)
    ]
    return sorted(nomes, key=lambda n: int(re.search(r"\d+", n).group()))


def imagens_de(pasta):
    # As pastas de saida do render (instagram/, tiktok/) ficam de fora: sao o
    # resultado, nao insumo. Listar os PNGs renderizados aqui so entupiria o
    # seletor de "trocar imagem" com 10 itens inuteis.
    fora = {BACKUP, LIXO, "instagram", "tiktok"}
    achadas = []
    for raiz_, dirs, arquivos in os.walk(longo(pasta)):
        dirs[:] = [d for d in dirs if d not in fora]
        for a in arquivos:
            if a.lower().endswith(EXT_IMG):
                abs_ = os.path.join(raiz_, a)
                rel = os.path.relpath(abs_, longo(pasta)).replace("\\", "/")
                achadas.append(rel)
    return sorted(achadas)


def achatar_cores(no, prefixo="", saida=None):
    """Extrai {nome, hex} de qualquer profundidade do bloco cores do design.json."""
    if saida is None:
        saida = []
    if not isinstance(no, dict):
        return saida
    valor = no.get("valor")
    if isinstance(valor, str) and re.match(r"^(#|rgba?\()", valor.strip()):
        saida.append({
            "nome": prefixo or "cor",
            "hex": valor.strip(),
            "papel": no.get("papel", ""),
        })
    for chave, filho in no.items():
        if isinstance(filho, dict):
            achatar_cores(filho, ("%s / %s" % (prefixo, chave)) if prefixo else chave, saida)
    return saida


def tokens():
    """Le marca/design.json e devolve so o que o painel precisa expor."""
    caminho = os.path.join(RAIZ, "marca", "design.json")
    if not os.path.isfile(longo(caminho)):
        return {"cores": [], "fontes": [], "espacamento": {}, "forma": {}, "nunca": [], "erro": "design.json nao encontrado"}
    d = json.loads(ler_texto(caminho))

    fontes, vistas = [], set()
    for papel, bloco in (d.get("tipografia") or {}).items():
        if not isinstance(bloco, dict):
            continue
        familia = bloco.get("familia")
        if familia and familia not in vistas:
            vistas.add(familia)
            fontes.append({"familia": familia, "papel": papel, "peso": bloco.get("peso")})

    nunca = d.get("nunca") or d.get("$meta", {}).get("nunca") or []
    if isinstance(nunca, dict):
        nunca = list(nunca.values())

    # O design.json repete o mesmo hex em papeis diferentes (o "destaque" e o
    # "vermelho/rubi" sao ambos #9E1420, por exemplo). Sem juntar, o painel
    # mostra tres quadradinhos identicos e o usuario fica escolhendo entre
    # clones. Mantemos o primeiro nome e somamos os papeis na dica.
    cores, por_hex = [], {}
    for c in achatar_cores(d.get("cores") or {}):
        chave = c["hex"].lower().replace(" ", "")
        if chave in por_hex:
            anterior = por_hex[chave]
            anterior["nome"] += " / " + c["nome"].split(" / ")[-1]
            if c["papel"] and c["papel"] not in anterior["papel"]:
                anterior["papel"] += " · " + c["papel"]
        else:
            por_hex[chave] = c
            cores.append(c)

    return {
        "marca": d.get("$meta", {}).get("marca", ""),
        "cores": cores,
        "fontes": fontes,
        "espacamento": d.get("espacamento") or {},
        "forma": d.get("forma") or {},
        "nunca": [str(n) for n in nunca] if isinstance(nunca, list) else [],
    }


def pastas_de_conteudo():
    """Toda pasta do repo que tenha slide-*.html, pra alimentar o seletor."""
    achadas = []
    ignorar = {".git", "node_modules", "__pycache__", BACKUP, LIXO}
    for raiz_, dirs, arquivos in os.walk(longo(RAIZ)):
        dirs[:] = [d for d in dirs if d not in ignorar and not d.startswith(".")]
        quantos = len([a for a in arquivos if re.match(r"^slide-\d+\.html$", a, re.I)])
        if quantos:
            rel = os.path.relpath(raiz_, longo(RAIZ)).replace("\\", "/")
            achadas.append({"pasta": rel, "slides": quantos})
    achadas.sort(key=lambda x: x["pasta"], reverse=True)
    return achadas


def guardar_original(pasta, nome):
    """Copia o slide pro backup na primeira vez que ele e salvo."""
    destino_dir = os.path.join(pasta, BACKUP)
    if not os.path.isdir(longo(destino_dir)):
        os.makedirs(longo(destino_dir), exist_ok=True)
    destino = os.path.join(destino_dir, nome)
    if not os.path.isfile(longo(destino)):
        shutil.copyfile(longo(os.path.join(pasta, nome)), longo(destino))


def renumerar(pasta, ordem):
    """Renomeia a sequencia pra slide-01..slide-NN na ordem dada (via nomes temporarios)."""
    temporarios = []
    for i, nome in enumerate(ordem, start=1):
        tmp = os.path.join(pasta, "__ed_tmp_%02d.html" % i)
        os.replace(longo(os.path.join(pasta, nome)), longo(tmp))
        temporarios.append(tmp)
    finais = []
    for i, tmp in enumerate(temporarios, start=1):
        final = os.path.join(pasta, "slide-%02d.html" % i)
        os.replace(longo(tmp), longo(final))
        finais.append(os.path.basename(final))
    return finais


def rodar_render(pasta_abs, largura, altura, saida):
    """Renderiza pelo render_slides.py.

    Nao passa por PowerShell de proposito: nesta maquina toda politica de
    execucao persistente esta Undefined (= Restricted), entao chamar o
    render-carrossel.ps1 de um subprocesso morre com PSSecurityException --
    e forcar -ExecutionPolicy Bypass e acao de seguranca, nao atalho.
    O modulo Python gera PNG byte a byte identico ao do .ps1 (verificado).
    """
    try:
        ok, linhas = render_slides.renderizar(pasta_abs, largura, altura, saida)
        return (0 if ok else 1), "\n".join(linhas)
    except Exception as exc:
        return 1, "render falhou: %s" % exc


class Handler(BaseHTTPRequestHandler):
    server_version = "EditorCarrossel/1.0"

    def log_message(self, formato, *args):
        pass  # sem log de acesso: o terminal fica pro que importa

    # ---------- utilidades de resposta ----------

    def _enviar(self, codigo, corpo, tipo="application/json; charset=utf-8", cache=False):
        if isinstance(corpo, str):
            corpo = corpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        if not cache:
            self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(corpo)

    def _json(self, dados, codigo=200):
        self._enviar(codigo, json.dumps(dados, ensure_ascii=False), cache=False)

    def _erro(self, mensagem, codigo=400):
        self._json({"ok": False, "erro": str(mensagem)}, codigo)

    def _corpo(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        if not tamanho:
            return {}
        return json.loads(self.rfile.read(tamanho).decode("utf-8"))

    # ---------- GET ----------

    def do_GET(self):
        url = urlparse(self.path)
        rota = unquote(url.path)
        query = parse_qs(url.query)
        try:
            if rota in ("/", "/index.html"):
                return self._enviar(200, ler_texto(UI), TIPOS[".html"])

            if rota == "/api/pastas":
                return self._json({"ok": True, "pastas": pastas_de_conteudo()})

            if rota == "/api/estado":
                pasta = resolver_pasta((query.get("pasta") or [""])[0])
                rel = os.path.relpath(pasta, RAIZ).replace("\\", "/")
                backup = os.path.join(pasta, BACKUP)
                return self._json({
                    "ok": True,
                    "pasta": rel,
                    "slides": slides_de(pasta),
                    "imagens": imagens_de(pasta),
                    "comBackup": sorted(os.listdir(longo(backup))) if os.path.isdir(longo(backup)) else [],
                    "tokens": tokens(),
                })

            if rota.startswith("/f/"):
                return self._servir_arquivo(rota[len("/f/"):])

            return self._erro("rota desconhecida: %s" % rota, 404)
        except ValueError as exc:
            # caminho torto, pasta sem slide: erro DO PEDIDO, nao do servidor.
            # Devolver 500 aqui faria o navegador logar falha de servidor a cada
            # caminho digitado errado -- e mentiria sobre de quem e o problema.
            return self._erro(exc, 400)
        except Exception as exc:  # devolve o erro pro painel em vez de morrer calado
            return self._erro(exc, 500)

    def _servir_arquivo(self, rel):
        rel = rel.replace("\\", "/").strip("/")
        alvo = os.path.join(RAIZ, *[p for p in rel.split("/") if p not in ("", ".", "..")])
        if not dentro(RAIZ, alvo) or not os.path.isfile(longo(alvo)):
            return self._erro("arquivo nao encontrado: %s" % rel, 404)
        ext = os.path.splitext(alvo)[1].lower()
        with io.open(longo(alvo), "rb") as f:
            dados = f.read()
        return self._enviar(200, dados, TIPOS.get(ext, "application/octet-stream"))

    # ---------- POST ----------

    def do_POST(self):
        rota = unquote(urlparse(self.path).path)
        try:
            dados = self._corpo()
            pasta = resolver_pasta(dados.get("pasta"))
            rel = os.path.relpath(pasta, RAIZ).replace("\\", "/")

            if rota == "/api/salvar":
                nome = self._slide(pasta, dados.get("slide"))
                html = dados.get("html") or ""
                if len(html) < 60 or "<html" not in html.lower():
                    return self._erro("html suspeito (vazio ou truncado) -- nao salvei")
                guardar_original(pasta, nome)
                escrever_texto(os.path.join(pasta, nome), html)
                return self._json({"ok": True, "slide": nome})

            if rota == "/api/restaurar":
                nome = self._slide(pasta, dados.get("slide"))
                origem = os.path.join(pasta, BACKUP, nome)
                if not os.path.isfile(longo(origem)):
                    return self._erro("nao existe backup de %s" % nome)
                shutil.copyfile(longo(origem), longo(os.path.join(pasta, nome)))
                return self._json({"ok": True, "slide": nome})

            if rota == "/api/duplicar":
                nome = self._slide(pasta, dados.get("slide"))
                ordem = slides_de(pasta)
                indice = ordem.index(nome)
                copia = os.path.join(pasta, "__ed_dup.html")
                shutil.copyfile(longo(os.path.join(pasta, nome)), longo(copia))
                ordem.insert(indice + 1, "__ed_dup.html")
                return self._json({"ok": True, "slides": renumerar(pasta, ordem),
                                   "atual": "slide-%02d.html" % (indice + 2)})

            if rota == "/api/apagar":
                nome = self._slide(pasta, dados.get("slide"))
                ordem = slides_de(pasta)
                if len(ordem) <= 1:
                    return self._erro("nao dou pra apagar o unico slide da peca")
                lixo = os.path.join(pasta, LIXO)
                os.makedirs(longo(lixo), exist_ok=True)
                os.replace(longo(os.path.join(pasta, nome)),
                           longo(os.path.join(lixo, "%s-%d.html" % (nome[:-5], os.getpid()))))
                ordem.remove(nome)
                return self._json({"ok": True, "slides": renumerar(pasta, ordem)})

            if rota == "/api/reordenar":
                ordem = dados.get("ordem") or []
                atuais = slides_de(pasta)
                if sorted(ordem) != sorted(atuais):
                    return self._erro("a ordem enviada nao bate com os slides da pasta")
                return self._json({"ok": True, "slides": renumerar(pasta, ordem)})

            if rota == "/api/renderizar":
                formato = (dados.get("formato") or "instagram").lower()
                largura, altura, saida = (1080, 1920, "tiktok") if formato == "tiktok" else (1080, 1350, "instagram")
                codigo, log = rodar_render(pasta, largura, altura, saida)
                pngs = []
                dir_saida = os.path.join(pasta, saida)
                if os.path.isdir(longo(dir_saida)):
                    pngs = sorted(n for n in os.listdir(longo(dir_saida)) if n.lower().endswith(".png"))
                return self._json({"ok": codigo == 0, "log": log, "saida": saida, "pngs": pngs})

            return self._erro("rota desconhecida: %s" % rota, 404)
        except ValueError as exc:
            return self._erro(exc, 400)   # pedido torto, nao servidor quebrado
        except Exception as exc:
            return self._erro(exc, 500)

    def _slide(self, pasta, nome):
        if not nome or not re.match(r"^slide-\d+\.html$", nome, re.I):
            raise ValueError("nome de slide invalido: %r" % nome)
        if not os.path.isfile(longo(os.path.join(pasta, nome))):
            raise ValueError("slide inexistente: %s" % nome)
        return nome


def main():
    ap = argparse.ArgumentParser(description="Painel de edicao visual dos carrosseis do FlowOS")
    ap.add_argument("--pasta", help="pasta do conteudo (relativa a raiz do repo)")
    ap.add_argument("--porta", type=int, default=8788)
    ap.add_argument("--nao-abrir", action="store_true", help="nao abrir o navegador")
    args = ap.parse_args()

    if not os.path.isfile(longo(UI)):
        print("ERRO: interface nao encontrada em %s" % UI)
        return 1

    inicial = ""
    if args.pasta:
        try:
            pasta = resolver_pasta(args.pasta)
        except ValueError as exc:
            print("ERRO: %s" % exc)
            return 1
        inicial = "?pasta=" + quote(os.path.relpath(pasta, RAIZ).replace("\\", "/"))

    # Se a porta estiver ocupada (painel ja aberto, outra coisa no 8788), anda
    # pra frente em vez de morrer -- o erro "Address already in use" nao diz nada
    # pra quem so quer editar um slide.
    servidor = None
    for porta in range(args.porta, args.porta + 20):
        try:
            servidor = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
            break
        except OSError:
            continue
    if servidor is None:
        print("ERRO: nenhuma porta livre entre %d e %d" % (args.porta, args.porta + 19))
        return 1

    endereco = "http://127.0.0.1:%d/%s" % (porta, inicial)
    print("Editor de carrossel em %s" % endereco)
    print("Ctrl+C pra encerrar.")
    if not args.nao_abrir:
        threading.Timer(0.6, lambda: webbrowser.open(endereco)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nencerrado.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
