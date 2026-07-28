#!/usr/bin/env python3
"""Genera flyers de Astronomy Academy en PNG, listos para Instagram.

Un producto x N ángulos de venta x M formatos. El copy y los precios viven en
`contenido/academy.json` (los precios los sincroniza `sync_precios.py` contra
Supabase); la estética vive en `templates/flyer.html` y usa los mismos tokens de
color que la app en producción.

    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py
    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py --productos membresias
    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py --formatos story

Render con el Chrome que ya está instalado (headless, sin dependencias nuevas).
Cada pieza se verifica de verdad antes de darse por buena: dimensiones exactas,
que el PNG no sea una placa vacía, y que el texto no haya desbordado. Si una
falla, el script termina con error y dice cuál — no exporta 74 buenas y una rota
en silencio.
"""

import argparse
import concurrent.futures
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

SKILL = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Tamaño, escala tipográfica y márgenes por formato. `base` es el font-size raíz:
# todo el template está en rem, así que una sola cifra reescala la pieza entera.
FORMATOS = {
    "feed":   {"w": 1080, "h": 1350, "base": 16.0, "pad": 5.4, "padx": 4.4},
    "story":  {"w": 1080, "h": 1920, "base": 17.0, "pad": 9.5, "padx": 4.6},
    "square": {"w": 1080, "h": 1080, "base": 14.0, "pad": 4.6, "padx": 4.2},
}

# Debajo de esto un PNG de 1080px es una placa vacía o casi: el render se colgó
# antes de pintar el texto. 40 KB es holgado — la pieza más pelada da ~90 KB.
MINIMO_BYTES = 40_000


def pesos(n):
    """143520 -> '$143.520'. Formato argentino, sin decimales y sin redondear."""
    return "$" + f"{int(n):,}".replace(",", ".")


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bloque_html(bloque, producto, planes):
    """Arma el bloque central. Cada tipo es una forma distinta de mostrar la oferta."""
    tipo = bloque.get("tipo", "ninguno")

    if tipo == "ninguno":
        return ""

    if tipo == "precio":
        precio = producto.get("precio_ars")
        if precio is None:
            raise ValueError(
                f"El producto '{producto['id']}' tiene un ángulo de precio pero "
                f"`precio_ars` es null. Corré sync_precios.py o sacá el ángulo: "
                f"un flyer no sale con el precio en blanco."
            )
        nota = bloque.get("nota")
        return (
            '<div class="bloque"><div class="precio">'
            f'<div class="monto">{pesos(precio)}</div>'
            f'<div class="periodo">{esc(bloque.get("periodo", ""))}</div>'
            + (f'<div class="nota">{esc(nota)}</div>' if nota else "")
            + "</div></div>"
        )

    if tipo == "bullets":
        items = "".join(f"<li>{esc(i)}</li>" for i in bloque["items"])
        return f'<div class="bloque"><ul class="bullets">{items}</ul></div>'

    if tipo == "dato":
        return (
            '<div class="bloque"><div class="dato">'
            f'<div class="n">{esc(bloque["numero"])}</div>'
            f'<div class="l">{esc(bloque["etiqueta"])}</div>'
            "</div></div>"
        )

    if tipo == "planes":
        cards = []
        for i, pid in enumerate(producto["planes"]):
            if pid not in planes:
                raise ValueError(f"El plan '{pid}' no está en precios.json. Corré sync_precios.py.")
            p = planes[pid]
            destacado = " destacado" if i == 1 else ""
            cards.append(
                f'<div class="plan{destacado}">'
                f'<div class="n">{esc(p["name"])}</div>'
                f'<div class="p">{pesos(p["price_ars"])}</div>'
                f'<div class="c">{p["monthly_credits"]} créditos</div>'
                "</div>"
            )
        return f'<div class="bloque"><div class="planes">{"".join(cards)}</div></div>'

    raise ValueError(f"Tipo de bloque desconocido: {tipo}")


def armar_html(template, marca, producto, angulo, fmt, planes, assets):
    f = FORMATOS[fmt]
    kicker = angulo.get("kicker")
    sub = angulo.get("sub")
    reemplazos = {
        "{{FONT}}": (assets / "fonts/Montserrat.ttf").as_uri(),
        "{{ISOTIPO}}": (assets / "marca" / marca["isotipo"]).as_uri(),
        "{{W}}": str(f["w"]),
        "{{H}}": str(f["h"]),
        "{{BASE}}": str(f["base"]),
        "{{PAD}}": str(f["pad"]),
        "{{PADX}}": str(f["padx"]),
        "{{MARCA}}": esc(marca["nombre"]),
        "{{KICKER}}": f'<div class="kicker">{esc(kicker)}</div>' if kicker else "",
        # El titular admite <em> (palabra en violeta) y <br>: es copy nuestro,
        # no entrada de usuario.
        "{{TITULAR}}": angulo["titular"],
        "{{SUB}}": f'<p class="sub">{esc(sub)}</p>' if sub else "",
        "{{BLOQUE}}": bloque_html(angulo["bloque"], producto, planes),
        "{{CTA}}": f'<div class="cta">{esc(angulo["cta"])}</div>' if angulo.get("cta") else "",
        "{{LEGAL}}": esc(marca["legal"]),
    }
    html = template
    for k, v in reemplazos.items():
        html = html.replace(k, v)

    faltantes = re.findall(r"\{\{[A-Z]+\}\}", html)
    if faltantes:
        raise ValueError(f"Quedaron placeholders sin reemplazar: {sorted(set(faltantes))}")
    return html


def render(html, destino, fmt):
    """HTML -> PNG con Chrome headless. Devuelve el veredicto del auto-ajuste."""
    f = FORMATOS[fmt]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="flyer-"))
    try:
        pagina = tmp / "flyer.html"
        pagina.write_text(html, encoding="utf-8")
        salida = tmp / "out.png"
        # Nada de `--user-data-dir`: con un perfil nuevo en /tmp, el Chrome de macOS
        # se cuelga indefinidamente (probado: 25s sin escribir nada, ni con
        # --no-first-run --no-default-browser-check --disable-sync). Sin el flag
        # anda, y cinco corridas en paralelo dan PNGs byte a byte idénticos, así
        # que compartir el perfil por defecto no molesta.
        proc = subprocess.run(
            [
                CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--virtual-time-budget=4000",
                f"--window-size={f['w']},{f['h']}",
                "--dump-dom",
                f"--screenshot={salida}",
                pagina.as_uri(),
            ],
            capture_output=True, text=True, timeout=120,
        )
        if not salida.exists():
            raise RuntimeError(f"Chrome no escribió el PNG.\n{proc.stderr[-800:]}")

        # El template deja el veredicto del auto-ajuste en el <title>. Se lee del
        # DOM volcado en la misma corrida, así no hay que renderizar dos veces.
        m = re.search(r"<title>([^<]*)</title>", proc.stdout)
        veredicto = m.group(1) if m else "SIN-TITULO"

        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(salida), destino)
        return veredicto
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verificar(path, fmt, veredicto):
    """Devuelve la lista de problemas de una pieza. Vacía = está bien."""
    f = FORMATOS[fmt]
    problemas = []
    tam = path.stat().st_size
    if tam < MINIMO_BYTES:
        problemas.append(f"pesa {tam} bytes: parece una placa vacía")
    with Image.open(path) as im:
        if im.size != (f["w"], f["h"]):
            problemas.append(f"mide {im.size[0]}x{im.size[1]}, esperaba {f['w']}x{f['h']}")
    if veredicto == "DESBORDA":
        problemas.append("el texto no entra ni achicando al 62%: acortá el copy")
    elif not veredicto.startswith("OK:"):
        problemas.append(f"el auto-ajuste no reportó nada ({veredicto})")
    return problemas


def contacto(piezas, destino, columnas=6, ancho=300):
    """Hoja de contacto con todas las piezas, para revisar de un vistazo."""
    if not piezas:
        return None
    minis = []
    for p in piezas:
        with Image.open(p) as im:
            alto = round(im.height * ancho / im.width)
            minis.append(im.convert("RGB").resize((ancho, alto), Image.LANCZOS))
    alto_fila = max(m.height for m in minis)
    filas = (len(minis) + columnas - 1) // columnas
    pad = 14
    hoja = Image.new(
        "RGB",
        (columnas * ancho + pad * (columnas + 1), filas * alto_fila + pad * (filas + 1)),
        (5, 6, 10),
    )
    for i, m in enumerate(minis):
        x = pad + (i % columnas) * (ancho + pad)
        y = pad + (i // columnas) * (alto_fila + pad)
        hoja.paste(m, (x, y))
    hoja.save(destino)
    return destino


def main():
    ap = argparse.ArgumentParser(description="Genera los flyers de Astronomy Academy.")
    ap.add_argument("--contenido", default=str(SKILL / "contenido/academy.json"))
    ap.add_argument("--salida", default=str(pathlib.Path.home() / "Desktop/Productoras/Astronomy/Flyers Academy"))
    ap.add_argument("--productos", help="IDs separados por coma. Default: todos.")
    ap.add_argument("--angulos", help="IDs separados por coma. Default: todos.")
    ap.add_argument("--formatos", default="feed,story,square")
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()

    cont = json.loads(pathlib.Path(args.contenido).read_text())
    template = (SKILL / "templates/flyer.html").read_text()
    assets = SKILL / "assets"

    precios_path = SKILL / "contenido/precios.json"
    if not precios_path.exists():
        sys.exit("Falta contenido/precios.json. Corré sync_precios.py antes de generar.")
    snap = json.loads(precios_path.read_text())
    planes = {p["id"]: p for p in snap["planes"]}

    formatos = [f.strip() for f in args.formatos.split(",") if f.strip()]
    for f in formatos:
        if f not in FORMATOS:
            sys.exit(f"Formato desconocido: {f}. Hay: {', '.join(FORMATOS)}")

    filtro_prod = {p.strip() for p in args.productos.split(",")} if args.productos else None
    filtro_ang = {a.strip() for a in args.angulos.split(",")} if args.angulos else None

    salida = pathlib.Path(args.salida)
    trabajos = []
    for producto in cont["productos"]:
        if filtro_prod and producto["id"] not in filtro_prod:
            continue
        for angulo in producto["angulos"]:
            if filtro_ang and angulo["id"] not in filtro_ang:
                continue
            for fmt in formatos:
                destino = salida / producto["id"] / f"{angulo['id']}__{fmt}.png"
                html = armar_html(template, cont["marca"], producto, angulo, fmt, planes, assets)
                trabajos.append((html, destino, fmt))

    if not trabajos:
        sys.exit("Cero piezas para generar: revisá los filtros --productos / --angulos.")

    print(f"Precios verificados el {snap['verificado']}.")
    print(f"Generando {len(trabajos)} piezas en {salida} ...\n")

    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futuros = {pool.submit(render, h, d, f): (d, f) for h, d, f in trabajos}
        for fut in concurrent.futures.as_completed(futuros):
            destino, fmt = futuros[fut]
            veredicto = fut.result()
            resultados.append((destino, fmt, verificar(destino, fmt, veredicto)))

    resultados.sort(key=lambda r: str(r[0]))
    malas = [(d, p) for d, _, p in resultados if p]
    for destino, _, problemas in resultados:
        marca = "  " if not problemas else "!!"
        print(f"{marca} {destino.relative_to(salida)}" + ("" if not problemas else f"   <- {'; '.join(problemas)}"))

    hoja = contacto([d for d, _, p in resultados if not p], salida / "_hoja-de-contacto.jpg")

    print(f"\n{len(resultados) - len(malas)}/{len(resultados)} piezas OK.")
    if hoja:
        print(f"Hoja de contacto: {hoja}")

    if malas:
        print(f"\n{len(malas)} piezas con problemas:")
        for destino, problemas in malas:
            print(f"  {destino.name}: {'; '.join(problemas)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
