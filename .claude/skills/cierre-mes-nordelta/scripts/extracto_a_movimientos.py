#!/usr/bin/env python3
"""
Extracto Macro -> Movimientos del Master Plan.

Lee el PDF del extracto (CC Especial en Pesos 4-452-0960512147-9), identifica cada
crédito y débito, y arma las filas en el orden de columnas de la pestaña
Movimientos: Fecha, Tipo, Medio, Local, Categoria, Monto, Moneda, Observaciones.

    # sólo mirar
    extracto_a_movimientos.py "Julio 2026.pdf" --facturas "…/Julio 2026"
    # escribir de verdad
    extracto_a_movimientos.py "Julio 2026.pdf" --facturas "…/Julio 2026" --escribir

`--facturas` es lo que evita el trabajo a mano. Varios débitos del extracto
salen como «N/D Transf. MacrOnline E-set D/T» sin CUIT ni nombre: la glosa no
dice a quién se le pagó. En vez de que alguien abra las facturas del mes y las
cruce de a una, el script indexa los PDF de la carpeta, saca CUIT y total de
cada uno y **matchea por importe** (el banco redondea al peso, por eso la
tolerancia de $1). El CUIT decide la categoría.

`--escribir` es el único que toca la planilla, y **se planta si queda un solo
renglón sin resolver**: un movimiento sin categoría entra igual a Movimientos,
no rompe nada y desaparece de todos los SUMIFS. Es exactamente la falla que
deja una expensa más barata sin que nadie se entere.

El dedupe compara (año, mes, monto) contra lo que ya está cargado con Medio
«Banco»: Facu a veces carga un movimiento con fecha distinta a la del extracto.

La columna I (Mes) es ArrayFormula: NO se emite y no hay que tocarla.
"""

import sys
import re
import datetime
import unicodedata

import argparse
import os
import glob

import fitz

sys.path.insert(0, "/Users/Facu/facu-os/execution")

CUENTA = "4-452-0960512147-9"
MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"

# CUIT del proveedor -> (nombre corto, categoría de Movimientos).
# El CUIT sale del nombre del archivo de la factura (convención de AFIP,
# `CUIT_pv_tipo_nro.pdf`) o del texto del PDF. Un CUIT que no esté acá deja el
# movimiento SIN resolver a propósito: se agrega el renglón, no se adivina.
CUIT_CATEGORIA = {
    "27373389973": ("Rhino (Sánchez Yanina)", "Sueldo Mantenimiento Gastronomia"),
    "30690741691": ("Andersen materiales",    "Inversiones"),
    "30517431431": ("Transportes Olivos",     "Retiro de Residuos"),
    "30718796136": ("Estudio Giaccio",        "Contador"),
    "20124767173": ("Oliva (corralón)",       "Inversiones"),
}

# Glosa del extracto -> (Local, Categoria). Local para ingresos, Categoria para egresos.
# El orden importa: gana la primera que matchea.
REGLAS = [
    (r"SUSHINOR",                        "Fabric",                None),
    (r"RODOLFO SRL|30716281457",         "Bigg",                  None),
    # Identificados en el extracto de julio 2026 contra las facturas. El CUIT
    # viaja en la glosa de las TRANSF, así que se matchean solos.
    (r"20286590994",                     None, "Sueldo Administracion (MB)"),   # Matías Barbagrigia
    # Oliva Gustavo Alberto — corralón de Tigre, materiales entregados en obra.
    # Se propone Inversiones porque hasta hoy siempre fue obra; si una compra es
    # gasto operativo hay que cambiarla a mano ANTES de cargarla.
    (r"20124767173",                     None, "Inversiones"),
    # Transferencia entre cuentas propias para cubrir el resumen de la VISA en
    # la CC Bancaria. NO es plata que se queda adentro: del otro lado sale a la
    # tarjeta. En junio 2026 se cargó como Inversiones («cubre VISA luces») y se
    # sigue ese precedente. Si el consumo del mes no fue obra, hay que cambiarla.
    (r"TRANSF AUT SDO MISMO TIT",        None, "Inversiones"),
    (r"RET\.? ING\.? BRUTOS SIRCREB",    None, "Ingresos Brutos"),
    (r"DBCR 25413",                      None, "Gastos bancarios"),
    (r"Comision Trf|COMISION",           None, "Gastos bancarios"),
    (r"IMP\.? AFIP|VEP",                 None, "Impuestos"),
    (r"MANTENIMIENTO|SERV\. CTA",        None, "Gastos bancarios"),
]

MESES = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
         7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre",
         12: "diciembre"}

LINEA = re.compile(r"^\s*(\d{2}/\d{2}/\d{2})\s+(.*?)\s+((?:\d{1,3}\.)*\d{1,3},\d{2})"
                   r"\s+((?:-?\d{1,3}\.)*-?\d{1,3},\d{2})\s*$")


def plata(s):
    return float(s.replace(".", "").replace(",", "."))


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def bloque_cuenta(texto):
    """Aísla el detalle de la cuenta en pesos: el extracto trae tres cuentas."""
    ini = texto.find(f"CUENTA CORRIENTE ESPECIAL EN PESOS NRO.: {CUENTA}")
    if ini < 0:
        sys.exit(f"No encontré la cuenta {CUENTA} en el PDF.")
    resto = texto[ini + 10:]
    fin = resto.find("CUENTA CORRIENTE BANCARIA NRO.")
    return resto[:fin] if fin > 0 else resto


def clasificar(desc):
    d = sin_tildes(desc).upper()
    for patron, local, categoria in REGLAS:
        if re.search(patron, d, re.I):
            return local, categoria
    return None, None


def parsear(pdf_path):
    doc = fitz.open(pdf_path)
    texto = "\n".join(p.get_text() for p in doc)
    bloque = bloque_cuenta(texto)

    saldo_prev, movs = None, []
    for linea in bloque.split("\n"):
        if "SALDO ULTIMO EXTRACTO" in linea:
            m = re.search(r"((?:\d{1,3}\.)*\d{1,3},\d{2})\s*$", linea)
            if m:
                saldo_prev = plata(m.group(1))
            continue
        m = LINEA.match(linea)
        if not m or saldo_prev is None:
            continue
        fecha_s, desc, monto_s, saldo_s = m.groups()
        monto, saldo = plata(monto_s), plata(saldo_s)
        # El extracto no separa débito de crédito por columna de forma confiable:
        # lo deduzco de cómo se movió el saldo.
        tipo = "Ingreso" if saldo > saldo_prev else "Egreso"
        saldo_prev = saldo
        d, mth, y = (int(x) for x in fecha_s.split("/"))
        local, categoria = clasificar(desc)
        movs.append({
            "fecha": datetime.date(2000 + y, mth, d),
            "tipo": tipo,
            "local": local if tipo == "Ingreso" else None,
            "categoria": categoria if tipo == "Egreso" else None,
            "monto": monto,
            "obs": " ".join(desc.split()),
        })
    return movs


def ya_cargados(xlsx):
    """(año, mes, monto) de los movimientos de Banco que ya están en el sheet.

    El match es por mes y no por día: Facu a veces carga un movimiento con
    fecha distinta a la del extracto (ej. el sueldo del 26/6 quedó al 30/6).
    """
    import openpyxl
    ws = openpyxl.load_workbook(xlsx, data_only=True)["Movimientos"]
    out = set()
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None or str(r[2]).strip().lower() != "banco":
            continue
        f = r[0].date() if isinstance(r[0], datetime.datetime) else None
        if f:
            out.add((f.year, f.month, round(float(r[5] or 0), 2)))
    return out


# Cargos chicos del banco que NO se cargan uno por uno: se agrupan en una sola
# línea al último día del mes. Criterio verificado contra junio 2026, que cerró
# al centavo. patrón -> (etiqueta, categoría)
AGRUPADOS = [
    (r"SIRCREB",        "IIBB SIRCREB",              "Ingresos Brutos"),
    (r"DBCR 25413",     "Impuesto Ley 25413",        "Gastos bancarios"),
    (r"COMISION",       "Comisiones transferencias", "Gastos bancarios"),
]


def agrupar(movs):
    """Colapsa los cargos bancarios chicos en una línea mensual cada uno."""
    sueltos, bolsas = [], {}
    for m in movs:
        d = sin_tildes(m["obs"]).upper()
        for patron, etiqueta, categoria in AGRUPADOS:
            if re.search(patron, d):
                clave = (m["fecha"].year, m["fecha"].month, etiqueta)
                if clave not in bolsas:
                    bolsas[clave] = {
                        "fecha": m["fecha"], "tipo": "Egreso", "local": None,
                        "categoria": categoria, "monto": 0.0,
                        "obs": f"{etiqueta} {MESES[m['fecha'].month]} "
                               f"{m['fecha'].year} (extracto)",
                    }
                b = bolsas[clave]
                b["monto"] += m["monto"]
                b["fecha"] = max(b["fecha"], m["fecha"])   # queda al cierre
                break
        else:
            sueltos.append(m)
    return sueltos + sorted(bolsas.values(), key=lambda x: x["obs"])


# ---------------------------------------------------------------------------
# Cruce contra las facturas de la carpeta del mes
# ---------------------------------------------------------------------------
# Cada proveedor escribe el importe distinto: AFIP saca «1936000,00» sin
# separador de miles, Andersen imprime «$ 599,251.55» en formato yanqui y las
# liquidaciones usan «1.234,56». Se captura crudo y se normaliza abajo.
NUM = r"[\d][\d.,]{2,18}[\d]"
ETIQ = r"(?:TOTAL|Importe Total)"
# La etiqueta puede ir ANTES del número (AFIP) o DESPUÉS (Andersen: el texto
# sale «… NETO: $ 599,251.55 TOTAL:» porque la tabla se extrae por columnas).
# Se guardan TODOS los candidatos y gana el que matchee un débito del extracto
# al peso: un candidato de más no inventa nada, sólo no matchea.
TOTAL_PDF = re.compile(rf"{ETIQ}[^0-9\-]{{0,40}}({NUM})", re.I)
TOTAL_PDF_ATRAS = re.compile(rf"({NUM})[^0-9\-]{{0,20}}{ETIQ}", re.I)
CUIT_PDF = re.compile(r"\b(\d{11})\b")
# El CUIT del EMISOR, no el nuestro: Mahni aparece en todas las facturas.
CUIT_PROPIO = "30719012503"


def plata_libre(s):
    """Un importe escrito en cualquiera de los tres formatos -> float.

    El separador DECIMAL es el último punto o coma que quede seguido de
    exactamente dos dígitos al final. Todo lo anterior es separador de miles y
    se tira. Sin esto, «599,251.55» se lee como $599,25.
    """
    s = s.strip()
    if not re.search(r"[.,]\d{2}$", s):
        return float(re.sub(r"[.,]", "", s))
    entero, dec = s[:-3], s[-2:]
    return float(re.sub(r"[.,]", "", entero) + "." + dec)


def indexar_facturas(carpeta):
    """[(cuit, nombre_archivo, total)] de cada PDF de la carpeta.

    El CUIT sale primero del nombre del archivo (convención de AFIP) y, si el
    archivo no la respeta, del texto. Un PDF sin total legible se saltea con
    aviso: mejor que un match inventado.
    """
    facturas, ilegibles = [], []
    for ruta in sorted(glob.glob(os.path.join(carpeta, "*.pdf"))):
        base = os.path.basename(ruta)
        try:
            texto = fitz.open(ruta)[0].get_text()
        except Exception as e:
            ilegibles.append(f"{base}: no se pudo abrir ({e})")
            continue
        m = re.match(r"(\d{11})_", base)
        cuit = m.group(1) if m else next(
            (c for c in CUIT_PDF.findall(texto) if c != CUIT_PROPIO), None)
        totales = sorted({plata_libre(t) for t in
                          TOTAL_PDF.findall(texto) + TOTAL_PDF_ATRAS.findall(texto)})
        if not totales:
            ilegibles.append(f"{base}: no le encontré el total")
            continue
        facturas.append((cuit, base, totales))
    return facturas, ilegibles


def resolver_con_facturas(movs, facturas):
    """Le pone categoría a los egresos que la glosa del banco no identifica.

    Matchea por importe con tolerancia de $1: el banco redondea al peso
    (Andersen facturó $599.251,55 y el débito salió $599.251,00).
    """
    resueltos = []
    for m in movs:
        if m["local"] or m["categoria"] or m["tipo"] != "Egreso":
            continue
        cand = [f for f in facturas
                if any(abs(t - m["monto"]) < 1.0 for t in f[2])]
        if len(cand) != 1:
            if len(cand) > 1:
                m["ambiguo"] = [c[1] for c in cand]
            continue
        cuit, archivo, totales = cand[0]
        total = min(totales, key=lambda t: abs(t - m["monto"]))
        if cuit not in CUIT_CATEGORIA:
            m["ambiguo"] = [f"{archivo} (CUIT {cuit} no está en CUIT_CATEGORIA)"]
            continue
        nombre, categoria = CUIT_CATEGORIA[cuit]
        m["categoria"] = categoria
        m["obs"] = f"{m['obs']} — {nombre} {archivo.replace('.pdf', '')}"
        resueltos.append((m, nombre, total))
    return resueltos


# ---------------------------------------------------------------------------
# La planilla
# ---------------------------------------------------------------------------
def movimientos_del_sheet():
    from google_auth import sheets
    return sheets().spreadsheets().values().get(
        spreadsheetId=MASTER_PLAN, range="Movimientos!A1:H2000",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])


def ya_cargados_sheet(filas):
    """(año, mes, monto) de lo que ya está cargado con Medio «Banco»."""
    out = set()
    for r in filas[1:]:
        r = list(r) + [""] * (8 - len(r))
        if str(r[2]).strip().lower() != "banco":
            continue
        try:
            f = datetime.date(1899, 12, 30) + datetime.timedelta(days=float(r[0]))
            out.add((f.year, f.month, round(float(r[5] or 0), 2)))
        except (ValueError, TypeError):
            continue
    return out


def escribir(filas_nuevas, cantidad_actual):
    """Appendea al final de Movimientos y RELEE para confirmar."""
    from google_auth import sheets
    s = sheets()
    s.spreadsheets().values().append(
        spreadsheetId=MASTER_PLAN, range="Movimientos!A:H",
        valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS",
        body={"values": filas_nuevas}).execute()
    despues = movimientos_del_sheet()
    agregadas = len(despues) - cantidad_actual
    if agregadas != len(filas_nuevas):
        sys.exit(f"ERROR: quise escribir {len(filas_nuevas)} filas y la planilla "
                 f"creció {agregadas}. Revisá Movimientos a mano.")
    return agregadas


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pdf", help="el PDF del extracto del Macro")
    ap.add_argument("--facturas", help="carpeta de Facturas de Compra del mes")
    ap.add_argument("--escribir", action="store_true",
                    help="escribe en Movimientos (por defecto NO toca nada)")
    ap.add_argument("--forzar", action="store_true",
                    help="escribe aunque queden renglones sin categoría")
    args = ap.parse_args()

    crudos = parsear(args.pdf)
    movs = agrupar(crudos)

    # El neto se controla contra el extracto CRUDO, no contra el agrupado.
    ing = sum(m["monto"] for m in crudos if m["tipo"] == "Ingreso")
    egr = sum(m["monto"] for m in crudos if m["tipo"] == "Egreso")
    print(f"# {len(movs)} movimientos en el extracto — "
          f"ingresos ${ing:,.2f} · egresos ${egr:,.2f} · neto ${ing - egr:,.2f}")

    if args.facturas:
        facturas, ilegibles = indexar_facturas(args.facturas)
        resueltos = resolver_con_facturas(movs, facturas)
        print(f"# {len(facturas)} facturas indexadas en la carpeta, "
              f"{len(resueltos)} débitos identificados por importe")
        for m, nombre, total in resueltos:
            print(f"#   ${m['monto']:,.2f} → {nombre} (la factura dice "
                  f"${total:,.2f})")
        for x in ilegibles:
            print(f"#   ⚠ {x}")

    filas_sheet = movimientos_del_sheet()
    cargados = ya_cargados_sheet(filas_sheet)
    nuevos = [m for m in movs
              if (m["fecha"].year, m["fecha"].month, round(m["monto"], 2))
              not in cargados]
    print(f"# {len(movs) - len(nuevos)} ya estaban cargados, "
          f"{len(nuevos)} para agregar")
    print("#")

    filas = []
    sin_resolver = []
    for m in nuevos:
        falta = not (m["local"] or m["categoria"])
        if falta:
            sin_resolver.append(m)
        filas.append([
            m["fecha"].strftime("%-d/%-m/%Y"),
            m["tipo"], "Banco",
            m["local"] or "", m["categoria"] or "",
            round(m["monto"], 2), "ARS",
            f"{m['obs']} - {MESES[m['fecha'].month]} {m['fecha'].year}",
        ])
        marca = "  ← SIN CATEGORIA" if falta else ""
        if m.get("ambiguo"):
            marca = f"  ← {len(m['ambiguo'])} facturas posibles: {m['ambiguo']}"
        print(f"{filas[-1][0]}\t{m['tipo']}\tBanco\t{m['local'] or ''}\t"
              f"{m['categoria'] or ''}\t{m['monto']:.2f}\tARS\t"
              f"{filas[-1][7]}{marca}")

    if not args.escribir:
        print(f"\n[SIN --escribir] No toqué nada. {len(filas)} filas listas.")
        return
    if sin_resolver and not args.forzar:
        sys.exit(f"\nFRENO: {len(sin_resolver)} movimiento(s) sin categoría. "
                 f"Entrarían a Movimientos y desaparecerían de todos los SUMIFS "
                 f"sin fallar. Resolvelos (agregá el CUIT a CUIT_CATEGORIA o la "
                 f"glosa a REGLAS) o corré con --forzar si de verdad van vacíos.")
    if not filas:
        print("\nNada nuevo para escribir.")
        return
    n = escribir(filas, len(filas_sheet))
    print(f"\n✅ {n} filas escritas en Movimientos y verificadas releyendo.")


if __name__ == "__main__":
    main()
