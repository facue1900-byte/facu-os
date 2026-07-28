#!/usr/bin/env python3
"""
Radar de deudores — Paseo Nordelta (Ctas Ctes).

Lee la pestaña CUENTA CORRIENTE del sheet Ctas Ctes y dice quién debe qué HOY,
con la convención real del paseo: **todos pagan el mes siguiente al del cargo**.
Por eso la deuda exigible es el acumulado hasta el mes PASADO inclusive; el cargo
del mes corriente está "en la calle" pero no vencido.

    .venv/bin/python radar_deudores.py <ctas_ctes.xlsx> <AAAA-MM del mes corriente>

No manda nada ni escribe en ningún lado: solo lee y reporta. Los borradores de
mensaje de cobro los arma el modelo aparte, y los manda Facu.
"""

import collections
import datetime
import sys

import openpyxl

# Reglas por local confirmadas por Facu (22/07 y 27/07/2026). Un saldo "raro" en
# estos locales no es deuda: es una regla del negocio.
REGLAS = {
    "Escuelita": "Paga % de facturación: no lleva cargo generado. Sus pagos figuran "
                 "como saldo a favor — es normal, no es plata a devolver.",
    "La Jaula / torneo": "Se le cobra recién desde agosto 2026 (tenía saldo a favor).",
}

# Locales que pagan (parte) por banco: esos pagos NO se ven hasta que el extracto
# del mes se anota en Movimientos. Su exigible puede estar sobreestimado mientras
# el mes está abierto (Facu, 27/07/2026).
PAGAN_POR_BANCO = {"Fabric", "Bigg"}

# Bigg paga POR ADELANTADO (el cargo del mes se paga durante el mismo mes, no el
# siguiente). Su cargo "por vencer" en realidad ya está corriendo (Facu, 28/07).
PAGAN_ADELANTADO = {"Bigg"}


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
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    xlsx, mes = sys.argv[1], sys.argv[2]
    try:
        anio, num = (int(x) for x in mes.split("-"))
        corriente = (anio, num)
    except ValueError:
        sys.exit(f"El mes va como AAAA-MM, no {mes!r}.")

    filas = leer_cuenta_corriente(xlsx)
    if not filas:
        sys.exit("CUENTA CORRIENTE no tiene filas — eso es un error, no un dato.")

    locales = collections.defaultdict(lambda: {"exigible": 0.0, "corriente_cargo": 0.0,
                                               "corriente_pagos": 0.0, "futuro": 0.0})
    for f in filas:
        loc = locales[f["local"]]
        if f["periodo"] < corriente:
            loc["exigible"] += f["cargado"] - f["pagado"]
        elif f["periodo"] == corriente:
            loc["corriente_cargo"] += f["cargado"]
            loc["corriente_pagos"] += f["pagado"]
            # Los pagos del mes corriente casi siempre pagan el mes anterior:
            loc["exigible"] -= f["pagado"]
        else:
            loc["futuro"] += f["cargado"] - f["pagado"]

    print(f"RADAR DE DEUDORES — corte {mes} "
          f"(exigible = cargos hasta el mes pasado − todos los pagos)\n")

    deudores, al_dia, con_regla = [], [], []
    for nombre in sorted(locales):
        loc = locales[nombre]
        if nombre in REGLAS:
            con_regla.append((nombre, loc))
        elif loc["exigible"] > 1:
            deudores.append((nombre, loc))
        else:
            al_dia.append((nombre, loc))

    if deudores:
        print("DEBEN (exigible hoy)")
        for nombre, loc in sorted(deudores, key=lambda x: -x[1]["exigible"]):
            banco = "  ⚠ paga por banco: puede haber pagos en tránsito hasta el extracto" \
                if nombre in PAGAN_POR_BANCO else ""
            etiqueta_corriente = ("ya corriendo (paga adelantado)"
                                  if nombre in PAGAN_ADELANTADO else "por vencer")
            print(f"  {nombre:<14} ${loc['exigible']:>13,.0f}"
                  + (f"   + cargo {mes} {etiqueta_corriente}: ${loc['corriente_cargo']:,.0f}"
                     if loc["corriente_cargo"] else "") + banco)
        print(f"\n  Total exigible: ${sum(l['exigible'] for _, l in deudores):,.0f}")
        print("  Antes de reclamar a los que pagan por banco, esperar el extracto "
              "del mes o chequear el homebanking.\n")
    else:
        print("Nadie debe nada exigible.\n")

    if al_dia:
        print("AL DÍA")
        for nombre, loc in al_dia:
            extra = f" (a favor ${-loc['exigible']:,.0f})" if loc["exigible"] < -1 else ""
            print(f"  {nombre:<14} ok{extra}"
                  + (f"   cargo {mes} por vencer: ${loc['corriente_cargo']:,.0f}"
                     if loc["corriente_cargo"] else ""))
        print()

    if con_regla:
        print("CON REGLA PROPIA (el saldo acá NO es deuda)")
        for nombre, loc in con_regla:
            print(f"  {nombre:<18} saldo ${loc['exigible']:,.0f} — {REGLAS[nombre]}")
        print()

    # Huecos del generador: cargos en cero en meses ya exigibles para locales activos
    print("HUECOS DEL GENERADOR DE CARGOS (mes exigible sin cargo generado)")
    hay = False
    por_local_mes = collections.defaultdict(dict)
    for f in filas:
        por_local_mes[f["local"]][f["periodo"]] = f
    for nombre, meses in sorted(por_local_mes.items()):
        if nombre in REGLAS:
            continue
        con_cargo = [p for p, f in meses.items() if f["cargado"] > 0]
        if not con_cargo:
            continue
        desde = min(con_cargo)
        for p in sorted(meses):
            if desde <= p <= corriente and meses[p]["cargado"] == 0:
                hay = True
                print(f"  {nombre}: {p[0]}-{p[1]:02d} sin cargo "
                      f"(pagó ${meses[p]['pagado']:,.0f} ese mes)")
    if not hay:
        print("  ninguno")


if __name__ == "__main__":
    main()
