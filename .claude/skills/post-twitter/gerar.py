#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MOLDE — peça no formato print de tweet, 1080x1350.

Copiar pra `marketing/conteudo/<pasta>/tweet/gerar.py`, preencher o bloco CONFIG
e a lista SLIDES, rodar, e renderizar com scripts/render-carrossel.ps1.

O texto dos slides entra LITERAL do roteiro no Notion. Este arquivo diagrama,
não escreve. Ver .claude/skills/post-twitter/SKILL.md.
"""
import base64, os

AQUI = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(AQUI, "..", "assets"))

# ===========================  CONFIG  ======================================

TEMA   = "claro"          # "claro" ou "escuro" — uma versão por peça, nunca misturar
NOME   = "Nome de Exibição"
HANDLE = "@handle"
SELO   = True             # selo verificado ao lado do nome
FOTO   = os.path.join(ASSETS, "avatar-fonte.png")   # retrato com ombro pra cima

# Onde a cabeça começa e termina no retrato, em fração da altura. Medir na foto:
# abrir e estimar a que altura está o topo do crânio e o queixo.
ROSTO_TOPO = 0.09
ROSTO_BASE = 0.57
ALVO_ROSTO = 0.78         # quanto do círculo o rosto ocupa (faixa boa: 0.75 a 0.80)

W, H = 1080, 1350

PALETA = {
    "claro":  {"fundo": "#FFFFFF", "texto": "#0F1419", "handle": "#536471", "borda": "#CFD9DE"},
    "escuro": {"fundo": "#000000", "texto": "#E7E9EA", "handle": "#71767B", "borda": "#2F3336"},
}[TEMA]
AZUL_SELO = "#1D9BF0"

# ===========================================================================


def uri(caminho, mime):
    # Caminho longo (OneDrive + acento) estoura o MAX_PATH de 260 do Windows e o
    # open() falha com "arquivo não encontrado" mesmo o arquivo existindo.
    caminho = os.path.abspath(caminho)
    if os.name == "nt" and not caminho.startswith("\\\\?\\"):
        caminho = "\\\\?\\" + caminho
    return f"data:{mime};base64," + base64.b64encode(open(caminho, "rb").read()).decode("ascii")


def asset(nome):
    """Print anexado. Embutido em base64: o Chrome headless bloqueia file://
    relativo no screenshot e a imagem sairia quebrada."""
    ext = os.path.splitext(nome)[1].lower()
    return uri(os.path.join(ASSETS, nome), "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png")


def montar_avatar():
    """Corta o quadrado do avatar dimensionado PELO ROSTO: lado = altura do rosto
    / ALVO_ROSTO. Exige retrato com folga em volta da cabeça — foto já cortada na
    coroa não tem conserto, e preencher a volta sempre aparece."""
    from PIL import Image

    destino = os.path.join(ASSETS, "avatar-tweet.png")
    src = Image.open("\\\\?\\" + os.path.abspath(FOTO)).convert("RGB")

    topo, base_ = ROSTO_TOPO * src.height, ROSTO_BASE * src.height
    lado = min((base_ - topo) / ALVO_ROSTO, src.width, src.height)
    x = min(max(src.width / 2 - lado / 2, 0), src.width - lado)
    y = min(max((topo + base_) / 2 - lado / 2, 0), src.height - lado)

    src.crop((int(x), int(y), int(x + lado), int(y + lado))) \
       .resize((400, 400), Image.LANCZOS) \
       .save("\\\\?\\" + os.path.abspath(destino))
    return destino


foto_uri = uri(montar_avatar(), "image/png")

SELO_SVG = f"""<svg class="selo" viewBox="0 0 24 24" aria-hidden="true"><path fill="{AZUL_SELO}" d="M22.25 12c0-1.43-.88-2.67-2.19-3.34.46-1.39.2-2.9-.81-3.91s-2.52-1.27-3.91-.81c-.66-1.31-1.91-2.19-3.34-2.19s-2.67.88-3.33 2.19c-1.4-.46-2.91-.2-3.92.81s-1.26 2.52-.8 3.91c-1.31.67-2.2 1.91-2.2 3.34s.89 2.67 2.2 3.34c-.46 1.39-.21 2.9.8 3.91s2.52 1.26 3.91.81c.67 1.31 1.91 2.19 3.34 2.19s2.68-.88 3.34-2.19c1.39.45 2.9.2 3.91-.81s1.27-2.52.81-3.91c1.31-.67 2.19-1.91 2.19-3.34zm-11.71 4.2L6.8 12.46l1.41-1.42 2.26 2.26 4.8-5.23 1.47 1.36-6.2 6.77z"/></svg>""" if SELO else ""

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
@page{{size:{W}px {H}px;margin:0}}
html,body{{width:{W}px;height:{H}px}}
body{{
  font-family:'Inter',-apple-system,'Segoe UI',Arial,sans-serif;
  background:{PALETA['fundo']};color:{PALETA['texto']};-webkit-font-smoothing:antialiased;
}}
.slide{{
  width:{W}px;height:{H}px;overflow:hidden;padding:0 80px;
  display:flex;flex-direction:column;justify-content:center;  /* centralizado vertical */
}}
/* header: avatar à esquerda, nome+handle empilhados. SEM linha separadora abaixo. */
.header{{display:flex;align-items:center;gap:20px;margin-bottom:32px}}
.avatar{{width:100px;height:100px;border-radius:50%;object-fit:cover;flex-shrink:0}}
.nome{{display:flex;align-items:center;gap:8px;font-size:36px;font-weight:700;letter-spacing:-0.01em;line-height:1.2}}
.selo{{width:32px;height:32px;flex-shrink:0}}
.handle{{font-size:28px;font-weight:400;color:{PALETA['handle']};line-height:1.3;margin-top:2px}}

.texto p{{font-size:44px;font-weight:400;line-height:1.35}}
.texto p + p{{margin-top:60px}}
/* p depois de lista ou de print não é irmão de p: precisa do respiro na mão */
.texto .lista + p, .texto .anexo + p{{margin-top:60px}}
.texto strong{{font-weight:700}}   /* ênfase por peso, nunca por cor */

.lista{{list-style:none;margin-top:36px}}
.lista li{{font-size:44px;line-height:1.35;padding-left:40px;text-indent:-40px;margin-bottom:18px}}
.lista li:last-child{{margin-bottom:0}}

/* print anexado: mesmo layout do slide sem imagem, só entra ABAIXO do texto.
   Cantos e hairline são o tratamento que a própria plataforma dá em imagem. */
.anexo{{
  display:block;margin-top:36px;max-width:920px;max-height:600px;
  width:auto;height:auto;border-radius:24px;border:1px solid {PALETA['borda']};
}}
"""


def pagina(corpo):
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="slide">
  <div class="header">
    <img class="avatar" src="{foto_uri}" alt="">
    <div>
      <div class="nome">{NOME}{SELO_SVG}</div>
      <div class="handle">{HANDLE}</div>
    </div>
  </div>
  <div class="texto">
{corpo}
  </div>
</div></body></html>"""


def p(*linhas):
    """Cada argumento é um parágrafo do tweet. <strong> marca a ênfase."""
    return "\n".join(f"<p>{l}</p>" for l in linhas)


def anexo(nome):
    return f'\n<img class="anexo" src="{asset(nome)}" alt="">\n'


# ===========================  SLIDES  ======================================
# Texto LITERAL do roteiro no Notion. Um item = um slide.

SLIDES = [
    p("Primeiro parágrafo do tweet.",
      "Segundo parágrafo, com a <strong>ênfase do slide</strong>."),

    # slide com print de prova:
    # p("Texto.") + anexo("print-da-prova.png") + p("Fecho depois do print."),
]

# ===========================================================================

for i, corpo in enumerate(SLIDES, 1):
    open(os.path.join(AQUI, f"slide-{i:02d}.html"), "w", encoding="utf-8").write(pagina(corpo))
    print(f"slide-{i:02d}.html")
print(f"\n{len(SLIDES)} slides gerados em {AQUI}")
