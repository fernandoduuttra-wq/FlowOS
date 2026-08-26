#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
extrair-cores.py — tira o hex exato de um arquivo de marca.

Serve pra quando a identidade existe mas ninguem tem o manual: o arquivo do
logo vira a fonte de verdade e a cor sai medida, nao estimada no olho.

Dois modos:

  logo       Uma imagem so. Procura o "pico exato": num PNG exportado de
             vetor, uma cor chapada ocupa a maior parte dos pixels opacos, e
             esse pico E a cor da marca. Reporta confianca alta quando acha.

  auditoria  Varias imagens. Extrai a cor cromatica dominante de cada uma e
             mostra o quanto elas divergem entre si. Serve pra medir a deriva
             de uma marca que passou por varias maos.

Uso:
  python scripts/extrair-cores.py logo caminho/logo.png
  python scripts/extrair-cores.py auditoria pasta/com/posts/
  python scripts/extrair-cores.py auditoria a.jpg b.jpg c.jpg --md

Notas de ambiente (Windows/OneDrive):
  Caminho com acento e caminho longo (>260) quebram open() mesmo quando o
  listdir enxerga o arquivo. Este script normaliza pra forma \\?\ antes de
  abrir, entao roda de dentro do OneDrive sem gambiarra.
"""

import argparse
import colorsys
import os
import sys
from collections import Counter

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("Falta dependencia. Rode:  python -m pip install pillow numpy")


EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

# Pixel com alfa abaixo disso e borda anti-serrilhada: mistura o fundo na cor
# e contamina a medicao. Fica de fora.
ALFA_MINIMO = 250

# Abaixo dessa saturacao a cor e neutra (preto, branco, cinza). Nao e candidata
# a cor de marca, mas continua sendo reportada em separado.
SATURACAO_MINIMA = 0.18

# Distancia RGB pra considerar duas cores "a mesma, com ruido de compressao".
RAIO_CLUSTER = 14


def caminho_longo(caminho):
    """Normaliza pro formato que o Windows abre mesmo com acento e >260 chars."""
    caminho = os.path.abspath(caminho)
    if os.name == "nt" and not caminho.startswith("\\\\?\\"):
        return "\\\\?\\" + caminho
    return caminho


def abrir(caminho):
    with Image.open(caminho_longo(caminho)) as img:
        return img.convert("RGBA")


def pixels_validos(img):
    """Devolve (rgb_opacos, total_pixels). Descarta transparente e anti-alias."""
    arr = np.asarray(img, dtype=np.uint8)
    rgb = arr[:, :, :3].reshape(-1, 3)
    alfa = arr[:, :, 3].reshape(-1)
    return rgb[alfa >= ALFA_MINIMO], rgb.shape[0]


def hexa(cor):
    return "#{:02X}{:02X}{:02X}".format(int(cor[0]), int(cor[1]), int(cor[2]))


def hsl(cor):
    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in cor])
    return h * 360.0, s * 100.0, l * 100.0


def saturacao(cor):
    return hsl(cor)[1] / 100.0


def agrupar(contagem, raio=RAIO_CLUSTER):
    """Junta cores vizinhas (ruido de JPEG) num representante so.

    Percorre da cor mais frequente pra menos e anexa cada uma ao primeiro
    grupo dentro do raio. O representante do grupo e a cor mais frequente
    dele -- nao a media, porque a media inventa um hex que nao existe em
    pixel nenhum da imagem.
    """
    grupos = []  # [representante, total, [membros]]
    for cor, n in contagem.most_common():
        alvo = np.array(cor, dtype=np.int16)
        for g in grupos:
            if np.linalg.norm(alvo - np.array(g[0], dtype=np.int16)) <= raio:
                g[1] += n
                g[2].append((cor, n))
                break
        else:
            grupos.append([cor, n, [(cor, n)]])
    grupos.sort(key=lambda g: -g[1])
    return grupos


def analisar(caminho):
    img = abrir(caminho)
    rgb, total = pixels_validos(img)
    if len(rgb) == 0:
        return None

    contagem = Counter(map(tuple, rgb))
    grupos = agrupar(contagem)
    opacos = len(rgb)

    cor_topo, n_topo = contagem.most_common(1)[0]
    pico = n_topo / opacos

    cromaticos = [g for g in grupos if saturacao(g[0]) >= SATURACAO_MINIMA]
    neutros = [g for g in grupos if saturacao(g[0]) < SATURACAO_MINIMA]

    return {
        "arquivo": os.path.basename(caminho),
        "caminho": caminho,
        "formato": os.path.splitext(caminho)[1].lower(),
        "dimensoes": img.size,
        "total": total,
        "opacos": opacos,
        "transparencia": 1.0 - (opacos / total),
        "cores_unicas": len(contagem),
        "pico_cor": cor_topo,
        "pico_share": pico,
        "cromaticos": cromaticos,
        "neutros": neutros,
        "grupos": grupos,
    }


def confianca(info):
    """Le o quanto dá pra confiar no hex extraido dessa imagem."""
    lossy = info["formato"] in (".jpg", ".jpeg", ".webp")
    if info["pico_share"] >= 0.30 and not lossy:
        return "ALTA", ("cor chapada dominando os pixels opacos e formato sem "
                        "perda: o hex e o do arquivo, nao uma media")
    if info["pico_share"] >= 0.30 and lossy:
        return "MEDIA", ("cor chapada clara, mas o formato tem compressao com "
                         "perda -- o hex pode variar 1-2 pontos por canal")
    if lossy:
        return "BAIXA", ("formato com perda e sem cor chapada dominante: serve "
                         "pra comparar, nao pra fixar token")
    return "MEDIA", ("sem cor chapada dominante -- imagem com gradiente ou "
                     "foto; o valor e o mais frequente, nao o oficial")


def linha_cor(g, opacos, indice=None):
    cor = g[0]
    h, s, l = hsl(cor)
    prefixo = f"{indice}. " if indice else "   "
    return (f"{prefixo}{hexa(cor):>8}  {g[1] / opacos * 100:5.1f}%  "
            f"rgb({cor[0]:3d},{cor[1]:3d},{cor[2]:3d})  "
            f"hsl({h:5.1f}, {s:4.1f}%, {l:4.1f}%)")


def modo_logo(caminhos, como_md=False):
    for caminho in caminhos:
        info = analisar(caminho)
        if info is None:
            print(f"\n{caminho}: sem pixel opaco (imagem toda transparente?)")
            continue

        nivel, porque = confianca(info)
        print("\n" + "=" * 68)
        print(f"  {info['arquivo']}")
        print("=" * 68)
        print(f"  {info['dimensoes'][0]}x{info['dimensoes'][1]}px  ·  "
              f"{info['cores_unicas']} cores unicas  ·  "
              f"{info['transparencia'] * 100:.1f}% transparente")
        print(f"  Confianca: {nivel} — {porque}")

        print(f"\n  CORES DE MARCA (cromaticas)")
        if info["cromaticos"]:
            for i, g in enumerate(info["cromaticos"][:6], 1):
                print(linha_cor(g, info["opacos"], i))
        else:
            print("   nenhuma — a imagem e so preto/branco/cinza")

        print(f"\n  NEUTROS")
        for g in info["neutros"][:4]:
            print(linha_cor(g, info["opacos"]))

        if como_md and info["cromaticos"]:
            print("\n  --- markdown ---")
            print("  | Hex | Share | RGB | HSL |")
            print("  |---|---|---|---|")
            for g in info["cromaticos"][:6]:
                cor = g[0]
                h, s, l = hsl(cor)
                print(f"  | `{hexa(cor)}` | {g[1] / info['opacos'] * 100:.1f}% | "
                      f"{cor[0]}, {cor[1]}, {cor[2]} | "
                      f"{h:.0f}°, {s:.0f}%, {l:.0f}% |")


def modo_auditoria(caminhos, como_md=False):
    """Mede a deriva: quanto a cor 'da marca' varia de peca pra peca."""
    achados = []
    for caminho in caminhos:
        info = analisar(caminho)
        if info is None or not info["cromaticos"]:
            continue
        dominante = info["cromaticos"][0]
        achados.append((info, dominante))

    if not achados:
        sys.exit("Nenhuma imagem com cor cromatica encontrada.")

    print("\n" + "=" * 78)
    print("  DERIVA — cor cromatica dominante de cada arquivo")
    print("=" * 78)
    for info, g in sorted(achados, key=lambda x: hsl(x[1][0])[0]):
        cor = g[0]
        h, s, l = hsl(cor)
        print(f"  {hexa(cor):>8}  h{h:5.1f}  s{s:4.0f}%  l{l:4.0f}%   "
              f"{info['arquivo'][:44]}")

    hues = [hsl(g[0])[0] for _, g in achados]
    sats = [hsl(g[0])[1] for _, g in achados]
    lums = [hsl(g[0])[2] for _, g in achados]

    print("\n" + "-" * 78)
    print(f"  {len(achados)} arquivos")
    print(f"  Matiz      {min(hues):5.1f} a {max(hues):5.1f}   "
          f"(amplitude {max(hues) - min(hues):.1f} graus)")
    print(f"  Saturacao  {min(sats):5.1f}% a {max(sats):5.1f}%")
    print(f"  Luminancia {min(lums):5.1f}% a {max(lums):5.1f}%")

    amplitude = max(hues) - min(hues)
    print()
    if amplitude <= 4:
        print("  LEITURA: matiz consistente. A marca nao derivou de cor --")
        print("  se ha sensacao de bagunca, ela vem de outra camada")
        print("  (tipografia, composicao, tratamento de imagem).")
    elif amplitude <= 12:
        print("  LEITURA: deriva leve. Provavelmente compressao e ajuste de")
        print("  exportacao, nao decisao de designer. Um hex canonico resolve.")
    else:
        print("  LEITURA: deriva real. A amplitude e grande demais pra ser")
        print("  ruido de arquivo -- as pecas foram feitas com cores")
        print("  diferentes. O hex canonico tem que vir do logo original,")
        print("  nao de media do feed: a media herda a bagunca.")

    if como_md:
        print("\n  --- markdown ---")
        print("  | Arquivo | Hex | Matiz | Sat | Lum |")
        print("  |---|---|---|---|---|")
        for info, g in sorted(achados, key=lambda x: hsl(x[1][0])[0]):
            h, s, l = hsl(g[0])
            print(f"  | {info['arquivo']} | `{hexa(g[0])}` | {h:.1f}° | "
                  f"{s:.0f}% | {l:.0f}% |")


def expandir(entradas):
    arquivos = []
    for entrada in entradas:
        if os.path.isdir(entrada):
            for nome in sorted(os.listdir(caminho_longo(entrada))):
                if os.path.splitext(nome)[1].lower() in EXTENSOES:
                    arquivos.append(os.path.join(entrada, nome))
        elif os.path.isfile(entrada):
            arquivos.append(entrada)
        else:
            print(f"aviso: nao achei '{entrada}'", file=sys.stderr)
    if not arquivos:
        sys.exit("Nenhuma imagem encontrada nos caminhos informados.")
    return arquivos


def main():
    p = argparse.ArgumentParser(
        description="Extrai o hex exato de arquivos de marca.")
    p.add_argument("modo", choices=["logo", "auditoria"])
    p.add_argument("caminhos", nargs="+",
                   help="arquivo(s) de imagem ou pasta")
    p.add_argument("--md", action="store_true",
                   help="imprime tambem em tabela markdown, pra colar em doc")
    args = p.parse_args()

    arquivos = expandir(args.caminhos)
    if args.modo == "logo":
        modo_logo(arquivos, args.md)
    else:
        modo_auditoria(arquivos, args.md)


if __name__ == "__main__":
    main()
