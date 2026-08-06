#!/usr/bin/env python3
"""
Exporta el estado de cuentas corrientes a JSON, para que lo consuma la app del Paseo.

    .venv/bin/python exportar_ctas_ctes.py <ctas_ctes.xlsx> <AAAA-MM> <salida.json>

Misma lógica y mismas convenciones que radar_deudores.py — si una regla cambia,
cambia en los dos lados. No manda nada ni escribe en el sheet: sólo lee y exporta.
"""

import collections
import datetime
import json
import sys

import openpyxl

# Reglas por local confirmadas por Facu (22/07 y 27/07/2026). Un saldo "raro" en
# estos locales no es deuda: es una regla del negocio.
from reglas_locales import REGLAS, PAGAN_POR_BANCO, PAGAN_ADELANTADO  # noqa: E402  (las reglas viven en UN solo lugar)

# Plata que ya se cobró o acreditó pero todavía no está en Movimientos/CARGOS.
# Cada entrada se muestra en la app como aviso, y NO se suma al saldo.
# Se saca cuando el dato entra al sheet por su canal normal.
PENDIENTES_DE_CARGA = {
    "Bigg": [
        {"concepto": "Pago por banco del 14/07 — entra con el extracto de julio",
         "monto": 3796788.00},
    ],
}


def leer_cuenta_corriente(xlsx):
    ws = openpyxl.load_workbook(xlsx, data_only=True)["CUENTA CORRIENTE"]
    filas = []
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] is None or r[1] is None:
            continue
        if not isinstance(r[0], datetime.datetime):
            continue
        filas.append({
            "periodo": (r[0].year, r[0].month),
            "local": str(r[1]).strip(),
            "cargado": float(r[5] or 0),
            "pagado": float(r[8] or 0),
        })
    return filas


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    xlsx, mes, salida = sys.argv[1], sys.argv[2], sys.argv[3]
    try:
        anio, num = (int(x) for x in mes.split("-"))
        corriente = (anio, num)
    except ValueError:
        sys.exit(f"El mes va como AAAA-MM, no {mes!r}.")

    filas = leer_cuenta_corriente(xlsx)
    if not filas:
        sys.exit("CUENTA CORRIENTE no tiene filas — eso es un error, no un dato.")

    acum = collections.defaultdict(
        lambda: {"exigible": 0.0, "corriente_cargo": 0.0, "futuro": 0.0})
    meses = collections.defaultdict(dict)
    for f in filas:
        loc = acum[f["local"]]
        meses[f["local"]][f["periodo"]] = f
        if f["periodo"] < corriente:
            loc["exigible"] += f["cargado"] - f["pagado"]
        elif f["periodo"] == corriente:
            loc["corriente_cargo"] += f["cargado"]
            loc["exigible"] -= f["pagado"]      # los pagos del mes pagan el anterior
        else:
            loc["futuro"] += f["cargado"] - f["pagado"]

    locales = []
    for nombre in sorted(acum):
        loc = acum[nombre]
        exigible = round(loc["exigible"], 2)
        if nombre in REGLAS:
            estado = "regla-propia"
        elif exigible > 1:
            estado = "debe"
        else:
            estado = "al-dia"
        locales.append({
            "nombre": nombre,
            "estado": estado,
            "exigible": exigible,
            "aFavor": round(-exigible, 2) if exigible < -1 else 0.0,
            "cargoCorriente": round(loc["corriente_cargo"], 2),
            "cargoCorrienteYaCorriendo": nombre in PAGAN_ADELANTADO,
            "pagaPorBanco": nombre in PAGAN_POR_BANCO,
            "regla": REGLAS.get(nombre),
            "pendientesDeCarga": PENDIENTES_DE_CARGA.get(nombre, []),
            "meses": [
                {"periodo": f"{p[0]}-{p[1]:02d}",
                 "cargado": round(m["cargado"], 2),
                 "pagado": round(m["pagado"], 2)}
                for p, m in sorted(meses[nombre].items())
            ],
        })

    # Huecos del generador: meses ya exigibles sin cargo, para locales que sí facturan.
    huecos = []
    for nombre, por_mes in sorted(meses.items()):
        if nombre in REGLAS:
            continue
        con_cargo = [p for p, f in por_mes.items() if f["cargado"] > 0]
        if not con_cargo:
            continue
        desde = min(con_cargo)
        for p in sorted(por_mes):
            if desde <= p <= corriente and por_mes[p]["cargado"] == 0:
                huecos.append({"local": nombre,
                               "periodo": f"{p[0]}-{p[1]:02d}",
                               "pagoEseMes": round(por_mes[p]["pagado"], 2)})

    deben = [l for l in locales if l["estado"] == "debe"]
    doc = {
        "generado": datetime.date.today().isoformat(),
        "corte": mes,
        "fuente": "Sheet Ctas Ctes — pestaña CUENTA CORRIENTE",
        "totales": {
            "exigible": round(sum(l["exigible"] for l in deben), 2),
            "cargoCorriente": round(sum(l["cargoCorriente"] for l in locales), 2),
            "cuantosDeben": len(deben),
        },
        "locales": locales,
        "huecosDeCargos": huecos,
    }

    with open(salida, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)

    print(f"OK  {salida}")
    print(f"    corte {mes} · {len(locales)} locales · {len(deben)} deben "
          f"· exigible ${doc['totales']['exigible']:,.2f}")
    if huecos:
        print(f"    {len(huecos)} hueco(s) de cargos")


if __name__ == "__main__":
    main()
