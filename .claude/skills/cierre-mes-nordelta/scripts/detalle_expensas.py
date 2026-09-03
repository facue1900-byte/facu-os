#!/usr/bin/env python3
"""
El detalle de expensas de cada local, en PNG, para mandar por WhatsApp.

    detalle_expensas.py 2026-08            # todos los locales con cuenta corriente
    detalle_expensas.py 2026-08 Bigg Boss  # sólo esos

Facu, 03/09/2026: además de la cuenta corriente, cada locatario tiene que poder
ver **de qué se compone** lo que se le cobra de expensas — concepto por concepto,
no un total suelto.

**De dónde sale.** Del bloque CONGELADO del mes en `Expensas Predio` (Master
Plan), que es exactamente lo que está cargado en las cuentas corrientes. NO del
bloque vivo de arriba (filas 7-30): ése se recalcula al cambiar la fecha en `A3`
y no coincide con lo ya cobrado. Un bloque se congela con
`congelar_detalle_expensas.py`.

**La verificación que corre siempre:** el «Rec. de Gastos Total» y el «Servicios
comunes Total» de cada local tienen que coincidir, al peso, con los cargos
`Recupero de gastos` y `Servicios comunes` de su pestaña de cuenta corriente. Si
uno no cierra, el script FRENA y no escribe nada: un detalle que no cuadra con lo
cobrado es peor que no mandar nada.

**Los nombres no coinciden entre hojas** (Boss es «Hamburgueseria» en Expensas
Predio, Volta es «Heladeria»): el mapeo vive en `reglas_locales.ALIAS_EXPENSAS`.

La Jaula y Salón (Alto) **no llevan detalle**: la Jaula no paga expensas y el
Salón paga $1.000.000 pactado, no la fórmula de reparto.

Sale a `Cuentas Corrientes/<año>/<Mes año>/<Local>/Expensas <Local> - <Mes año>.png`,
al lado de la captura de la cuenta corriente.
"""

import datetime
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, "/Users/Facu/facu-os/execution")
from google_auth import sheets  # noqa: E402

MASTER = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
BASE = "/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Cuentas Corrientes"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]

# carpeta del local -> (columna en el bloque de Expensas Predio, pestaña de cta cte)
LOCALES = {
    "Fabric":       ("Fabric",         "Fabric"),
    "Bigg":         ("Bigg",           "Bigg"),
    "Boss":         ("Hamburgueseria", "Boss"),
    "Volta + Open": ("Heladeria",      "Volta + Open 25"),
    "Peak One":     ("Peak One",       "Peak One"),
}
# columna del detalle en cada pestaña de cta cte (las que no tienen FC corren una
# letra a la izquierda) -> (col detalle, col egreso), 0-indexed
CTA_COLS = {"Fabric": (2, 5), "Bigg": (2, 5), "Boss": (2, 5),
            "Volta + Open 25": (2, 4), "Peak One": (2, 4)}

TOL = 1.0   # un peso: las fórmulas de la planilla arrastran centavos


def num(x):
    if isinstance(x, (int, float)):
        return float(x)
    s = re.sub(r"[^\d,.-]", "", str(x)).replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def pesos(v):
    return "$" + f"{round(v):,}".replace(",", ".")


def bloque_congelado(filas, anio, mes):
    """Encuentra el bloque CONGELADO del mes: su fila de encabezado es la que
    dice «<mes> <año>» en A y tiene los locales al lado, y viene DESPUÉS del
    cartel «— CONGELADO». El bloque vivo de arriba (fila 7) se descarta.

    Recibe las filas FORMATEADAS: en crudo, la celda del mes es un serial de
    fecha y no matchea con nada."""
    etiqueta = f"{MESES[mes - 1]} {anio}".lower()
    congelado = None
    for i, r in enumerate(filas, 1):
        a = str((list(r) + [""])[0]).strip().lower()
        if "congelado" in a and a.startswith(MESES[mes - 1]) and str(anio) in a:
            congelado = i
        if congelado and i > congelado and a.startswith(etiqueta) and len(r) > 3:
            return i
    raise SystemExit(
        f"No hay bloque CONGELADO de {MESES[mes - 1]} {anio} en «Expensas Predio».\n"
        f"  Se congela con: congelar_detalle_expensas.py {anio}-{mes:02d}")


def leer_detalle(fmt, raw, cab, col):
    """Del encabezado hacia abajo hasta «Total Expensas»: (concepto, monto, tipo).

    Los rótulos salen de las filas formateadas y los montos de las crudas: en
    crudo no hay texto de mes, y formateado los montos vienen con separadores."""
    cabecera = list(fmt[cab - 1])
    try:
        j = next(i for i, c in enumerate(cabecera) if str(c).strip() == col)
    except StopIteration:
        raise SystemExit(f"La columna «{col}» no está en el bloque congelado.")
    filas_out, seccion = [], "recupero"
    for i in range(cab + 1, cab + 30):
        r = (list(fmt[i - 1]) if i <= len(fmt) else []) + [""] * 40
        crudo = (list(raw[i - 1]) if i <= len(raw) else []) + [""] * 40
        concepto = str(r[0]).strip()
        if not concepto:
            continue
        monto = num(crudo[j])
        if concepto.lower().startswith("rec. de gastos total"):
            filas_out.append(("Total recupero de gastos", monto, "subtotal"))
            seccion = "servicios"
        elif concepto.lower().startswith("servicios comunes total"):
            filas_out.append(("Total servicios comunes", monto, "subtotal"))
        elif concepto.lower().startswith("total expensas"):
            filas_out.append(("TOTAL EXPENSAS", monto, "total"))
            break
        else:
            filas_out.append((concepto, monto, seccion))
    return filas_out


def cargos_cta_cte(sv, tab, anio, mes):
    """Recupero y servicios comunes que la cuenta corriente le cobra por ese mes.
    La etiqueta del cargo es el mes de ORIGEN (AGO'26), no el del bloque."""
    vals = sv.values().get(spreadsheetId=CTAS, range=f"'{tab}'!A1:H400",
                           valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    cd, ceg = CTA_COLS[tab]
    etiqueta = f"{MESES[mes - 1][:3].upper()}'{str(anio)[2:]}"
    out = {}
    for r in vals[5:]:
        r = list(r) + [""] * 10
        if str(r[0]).strip().upper() != etiqueta:
            continue
        det = str(r[cd]).strip().lower()
        if det.startswith("recupero"):
            out["recupero"] = num(r[ceg])
        elif det.startswith("servicios comunes"):
            out["servicios"] = num(r[ceg])
    return out


CSS = """
<style>
  @page { margin: 0 }
  body { margin: 0; font-family: Calibri, "Helvetica Neue", Arial, sans-serif;
         background: #fff; color: #000 }
  .hoja { padding: 26px 30px 30px }
  h1 { font-size: 26px; margin: 0 0 2px; letter-spacing: .01em }
  .sub { font-size: 17px; color: #444; margin: 0 0 18px }
  table { border-collapse: collapse; width: 100% }
  td { padding: 7px 14px; font-size: 17px; border: 1px solid #cfd6e4 }
  td.m { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums }
  tr.sec td { background: #4472c4; color: #fff; font-weight: 700; font-size: 15px;
              letter-spacing: .06em; border-color: #4472c4 }
  tr.sub td { background: #eef2f9; font-weight: 700 }
  tr.tot td { background: #b7ace0; font-weight: 700; font-size: 19px;
              border-color: #8f83c4 }
  tr.cero td { color: #9aa3b2 }
</style>
"""


def armar_html(local, etiqueta_mes, filas):
    def fila(concepto, monto, clase=""):
        return (f'<tr class="{clase}"><td>{html.escape(concepto)}</td>'
                f'<td class="m">{pesos(monto)}</td></tr>')

    cuerpo, seccion_abierta = [], None
    cuerpo.append('<tr class="sec"><td colspan="2">RECUPERO DE GASTOS</td></tr>')
    seccion_abierta = "recupero"
    for concepto, monto, tipo in filas:
        if tipo == "servicios" and seccion_abierta != "servicios":
            cuerpo.append('<tr class="sec"><td colspan="2">SERVICIOS COMUNES</td></tr>')
            seccion_abierta = "servicios"
        clase = {"subtotal": "sub", "total": "tot"}.get(tipo, "")
        if not clase and monto == 0:
            clase = "cero"
        cuerpo.append(fila(concepto, monto, clase))
    return (f"<!doctype html><meta charset='utf-8'>{CSS}<div class='hoja'>"
            f"<h1>EXPENSAS — {html.escape(local.upper())}</h1>"
            f"<p class='sub'>{etiqueta_mes}</p>"
            f"<table>{''.join(cuerpo)}</table></div>")


def render(html_txt, destino):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="expensas-"))
    try:
        pagina = tmp / "d.html"
        pagina.write_text(html_txt, encoding="utf-8")
        salida = tmp / "out.png"
        proc = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=2", "--virtual-time-budget=3000",
             "--window-size=760,1200", f"--screenshot={salida}", pagina.as_uri()],
            capture_output=True, text=True, timeout=120)
        if not salida.exists():
            raise RuntimeError(f"Chrome no escribió el PNG.\n{proc.stderr[-600:]}")
        from PIL import Image, ImageChops
        im = Image.open(salida).convert("RGB")
        bbox = ImageChops.difference(im.convert("L"),
                                     Image.new("L", im.size, 255)).getbbox()
        im = im.crop((0, 0, im.width, min(im.height, bbox[3] + 30)))
        destino.parent.mkdir(parents=True, exist_ok=True)
        im.save(destino, optimize=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    if len(sys.argv) < 2 or not re.fullmatch(r"\d{4}-\d{2}", sys.argv[1]):
        sys.exit(__doc__)
    anio, mes = (int(x) for x in sys.argv[1].split("-"))
    pedidos = sys.argv[2:] or list(LOCALES)
    etiqueta = f"{MESES[mes - 1].capitalize()} {anio}"
    # las expensas de un mes se cobran en el bloque del mes SIGUIENTE
    sig = datetime.date(anio, mes, 28) + datetime.timedelta(days=7)
    carpeta_mes = os.path.join(BASE, str(sig.year),
                               f"{MESES[sig.month - 1].capitalize()} {sig.year}")

    sv = sheets().spreadsheets()
    rango = "Expensas Predio!A1:AS200"
    fmt = sv.values().get(spreadsheetId=MASTER, range=rango,
                          valueRenderOption="FORMATTED_VALUE").execute().get("values", [])
    raw = sv.values().get(spreadsheetId=MASTER, range=rango,
                          valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    cab = bloque_congelado(fmt, anio, mes)
    print(f"Bloque congelado de {etiqueta}: fila {cab} de «Expensas Predio»\n")

    listos, problemas = [], []
    for local in pedidos:
        col, tab = LOCALES[local]
        detalle = leer_detalle(fmt, raw, cab, col)
        rec = next(m for c, m, t in detalle if c == "Total recupero de gastos")
        ser = next(m for c, m, t in detalle if c == "Total servicios comunes")
        cta = cargos_cta_cte(sv, tab, anio, mes)
        d_rec = abs(rec - cta.get("recupero", 0))
        d_ser = abs(ser - cta.get("servicios", 0))
        if d_rec > TOL or d_ser > TOL:
            problemas.append(
                f"  {local}: el detalle NO cierra contra su cuenta corriente\n"
                f"     recupero  detalle {pesos(rec)}  vs cta cte {pesos(cta.get('recupero', 0))}"
                f"   (dif {pesos(d_rec)})\n"
                f"     servicios detalle {pesos(ser)}  vs cta cte {pesos(cta.get('servicios', 0))}"
                f"   (dif {pesos(d_ser)})")
            continue
        listos.append((local, detalle, rec, ser))
        print(f"  ✓ {local:<14} recupero {pesos(rec):>12} · servicios {pesos(ser):>12}"
              f" · total {pesos(rec + ser):>12}   (cierra contra la cta cte)")

    if problemas:
        sys.exit("\n🔴 FRENO, no escribo nada:\n" + "\n".join(problemas))

    print()
    for local, detalle, _, _ in listos:
        destino = pathlib.Path(carpeta_mes) / local / f"Expensas {local} - {etiqueta}.png"
        render(armar_html(local, etiqueta, detalle), destino)
        print(f"  ✅ {local:<14} → {destino}")


if __name__ == "__main__":
    main()
