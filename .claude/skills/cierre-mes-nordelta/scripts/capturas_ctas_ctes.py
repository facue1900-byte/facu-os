#!/usr/bin/env python3
"""
Las capturas de cada cuenta corriente para mandar por WhatsApp.

    capturas_ctas_ctes.py 2026-09            # todas
    capturas_ctas_ctes.py 2026-09 Bigg Boss  # sólo esas

Facu, 03/09/2026: una captura «chiquita» por local con **los datos del locatario,
los pagos que hizo, lo que se le cobra y el TOTAL al costado**. Se guarda en
`Cuentas Corrientes/<año>/<Mes año>/<Local>/Cta Cte <Local> - <Mes año>.png`.

Sin navegador: se exporta la pestaña a PDF con el token de `google_auth`
(`…/export?format=pdf&gid=&range=`) y se rasteriza con PyMuPDF. Sale idéntico a
la planilla. Se exporta UN solo rango: el bloque del mes, que arranca en la
primera fila de pago posterior al cartucho del bloque anterior (así se ven los
pagos que cerraron ese bloque) y termina en el último renglón con datos. **El
encabezado (CTA CTE — LOCAL, Rubro, CUIT, la fila azul) viene solo**: son las
filas congeladas de la pestaña y Sheets las repite en cada export. Apilarle
encima `A1:H5` lo duplicaba — pasó el 03/09/2026.

Google contesta 429 si las exportaciones van seguidas: 4 s entre una y otra, y
reintento con espera creciente. Nunca pisa una captura existente.
"""

import io
import os
import re
import sys
import time
import datetime

import fitz
import requests
from PIL import Image, ImageChops

sys.path.insert(0, "/Users/Facu/facu-os/execution")
from google_auth import credenciales, sheets  # noqa: E402
from google.auth.transport.requests import Request  # noqa: E402

CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
BASE = "/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Cuentas Corrientes"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
# carpeta del local -> (pestaña, columna del total, layout: 'bloques' o 'jaula')
LOCALES = {
    "Fabric": ("Fabric", "H"), "Bigg": ("Bigg", "H"), "Boss": ("Boss", "H"),
    "Volta + Open": ("Volta + Open 25", "H"), "Peak One": ("Peak One", "H"),
    "La Jaula": ("Futbol", "G"),
}


def serial_a_fecha(x):
    try:
        return datetime.date(1899, 12, 30) + datetime.timedelta(days=float(x))
    except (TypeError, ValueError):
        return None


def exportar(token, gid, rango, dpi=200):
    p = {"format": "pdf", "gid": str(gid), "range": rango, "portrait": "false",
         "fitw": "true", "gridlines": "false", "printtitle": "false", "sheetnames": "false",
         "pagenum": "UNDEFINED", "size": "A4", "top_margin": "0.1", "bottom_margin": "0.1",
         "left_margin": "0.1", "right_margin": "0.1"}
    for intento in range(6):
        r = requests.get(f"https://docs.google.com/spreadsheets/d/{CTAS}/export", params=p,
                         headers={"Authorization": f"Bearer {token}"}, timeout=90)
        if r.status_code == 429:
            time.sleep(10 * (intento + 1))
            continue
        if r.status_code != 200 or "pdf" not in r.headers.get("content-type", ""):
            sys.exit(f"export {rango}: HTTP {r.status_code}")
        break
    else:
        sys.exit(f"429 persistente exportando {rango}")
    doc = fitz.open(stream=r.content, filetype="pdf")
    if doc.page_count != 1:
        sys.exit(f"{rango} salió en {doc.page_count} páginas: achicá el rango")
    pix = doc[0].get_pixmap(dpi=dpi, alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    bbox = ImageChops.difference(im.convert("L"), Image.new("L", im.size, 255)).getbbox()
    if not bbox:
        sys.exit(f"{rango}: la imagen salió vacía")
    return im.crop((max(0, bbox[0] - 8), max(0, bbox[1] - 8),
                    min(im.width, bbox[2] + 8), min(im.height, bbox[3] + 8)))


def rango_del_bloque(filas, col_total):
    """Desde el primer pago que cerró el bloque anterior hasta el último cargo.

    Se lee la estructura, no los cartuchos: desde el final hacia arriba, primero
    los CARGOS del bloque corriente (filas con etiqueta de mes en A, sin fecha) y
    después los PAGOS que los preceden (filas con fecha en A). Buscar «el último
    cartucho» fallaba en Bigg, cuyo cartucho tiene cuatro celdas y quedaba
    adentro del propio bloque.
    """
    def con_dato(r):
        r = list(r) + [""] * 3
        return bool(str(r[0]).strip() or str(r[2]).strip())   # A o Detalle, NO el saldo:
    # la columna de saldo arrastra la fórmula cientos de filas hacia abajo (Volta llegaba a la 337)
    ult = max(i for i, r in enumerate(filas, 1) if con_dato(r))
    es_pago = lambda i: serial_a_fecha((list(filas[i - 1]) + [""])[0]) is not None
    i = ult
    while i > 6 and not es_pago(i):
        i -= 1
    fin_pagos = i
    while i > 6 and es_pago(i):
        i -= 1
    ini = i + 1 if fin_pagos > 6 else 6
    return ini, ult


def main():
    if len(sys.argv) < 2 or not re.fullmatch(r"\d{4}-\d{2}", sys.argv[1]):
        sys.exit(__doc__)
    anio, mes = (int(x) for x in sys.argv[1].split("-"))
    pedidos = sys.argv[2:] or list(LOCALES)
    carpeta_mes = os.path.join(BASE, str(anio), f"{MESES[mes - 1].capitalize()} {anio}")

    cr = credenciales("facu")
    if not cr.valid:
        cr.refresh(Request())
    s = sheets()
    gids = {x["properties"]["title"]: x["properties"]["sheetId"]
            for x in s.spreadsheets().get(spreadsheetId=CTAS).execute()["sheets"]}

    for local in pedidos:
        tab, col_total = LOCALES[local]
        filas = s.spreadsheets().values().get(
            spreadsheetId=CTAS, range=f"'{tab}'!A1:H400",
            valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
        if tab == "Futbol":
            ult = max(i for i, r in enumerate(filas, 1) if any(str(c).strip() for c in r))
            rangos = [f"A1:G{ult}"]
        else:
            ini, ult = rango_del_bloque(filas, col_total)
            rangos = [f"A{ini}:H{ult}"]   # las filas congeladas 1-5 vienen solas
        partes = []
        for rg in rangos:
            partes.append(exportar(cr.token, gids[tab], rg))
            time.sleep(4)
        W = max(p.width for p in partes)
        partes = [p if p.width == W else p.resize((W, round(p.height * W / p.width))) for p in partes]
        out = Image.new("RGB", (W, sum(p.height for p in partes) + 6 * (len(partes) - 1)), "white")
        y = 0
        for p in partes:
            out.paste(p, (0, y))
            y += p.height + 6
        carpeta = os.path.join(carpeta_mes, local)
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"Cta Cte {local} - {MESES[mes - 1].capitalize()} {anio}.png")
        if os.path.exists(ruta):
            print(f"  · {local}: ya existe, no la piso → {ruta}")
            continue
        out.save(ruta, optimize=True)
        print(f"  ✅ {local:<14} {'+'.join(rangos):<16} {out.width}x{out.height}px → {ruta}")


if __name__ == "__main__":
    main()
