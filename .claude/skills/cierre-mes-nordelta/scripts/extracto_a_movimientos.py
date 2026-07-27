#!/usr/bin/env python3
"""
Extracto Macro -> filas listas para pegar en Movimientos.

Lee el PDF del extracto (CC Especial en Pesos 4-452-0960512147-9), identifica cada
crédito y débito, y escupe las filas en el orden de columnas de la pestaña
Movimientos: Fecha, Tipo, Medio, Local, Categoria, Monto, Moneda, Observaciones.

    python3 extracto_a_movimientos.py "Junio 2026.pdf" [master.xlsx]

Si se pasa el master.xlsx, marca cuáles de esos movimientos YA están cargados
(match por fecha + monto en Banco) para no duplicar.

La columna I (Mes) es ArrayFormula: NO se emite y no hay que tocarla.
"""

import sys
import re
import datetime
import unicodedata

import fitz

CUENTA = "4-452-0960512147-9"

# Glosa del extracto -> (Local, Categoria). Local para ingresos, Categoria para egresos.
# El orden importa: gana la primera que matchea.
REGLAS = [
    (r"SUSHINOR",                        "Fabric",                None),
    (r"RODOLFO SRL|30716281457",         "Bigg",                  None),
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


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    crudos = parsear(sys.argv[1])
    movs = agrupar(crudos)
    cargados = ya_cargados(sys.argv[2]) if len(sys.argv) > 2 else set()

    nuevos = [m for m in movs
              if (m["fecha"].year, m["fecha"].month, round(m["monto"], 2))
              not in cargados]
    # El neto se controla contra el extracto CRUDO, no contra el agrupado.
    ing = sum(m["monto"] for m in crudos if m["tipo"] == "Ingreso")
    egr = sum(m["monto"] for m in crudos if m["tipo"] == "Egreso")

    print(f"# {len(movs)} movimientos en el extracto — "
          f"ingresos ${ing:,.2f} · egresos ${egr:,.2f} · neto ${ing - egr:,.2f}")
    if cargados:
        print(f"# {len(movs) - len(nuevos)} ya estaban cargados, "
              f"{len(nuevos)} para agregar")
    print("#")
    print("# Fecha\tTipo\tMedio\tLocal\tCategoria\tMonto\tMoneda\tObservaciones")

    for m in nuevos:
        falta = " ← COMPLETAR" if not (m["local"] or m["categoria"]) else ""
        print("\t".join([
            m["fecha"].strftime("%-d/%-m/%Y"),
            m["tipo"],
            "Banco",
            m["local"] or "",
            m["categoria"] or "",
            f"{m['monto']:.2f}",
            "ARS",
            f"{m['obs']} - {MESES[m['fecha'].month]} {m['fecha'].year}{falta}",
        ]))


if __name__ == "__main__":
    main()
