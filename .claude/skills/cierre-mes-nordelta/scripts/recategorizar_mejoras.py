#!/usr/bin/env python3
"""
Pasa de "Mejoras" a "Inversiones" las filas del Master Plan que son OBRA.

Mejoras es gasto operativo; Inversiones es obra, que la financian los socios con
su capital. Cuando una fila de obra queda en Mejoras, el resultado del mes baja
por una plata que no es gasto del negocio.

    reporte: .../recategorizar_mejoras.py            (no toca nada, solo muestra)
    aplicar: .../recategorizar_mejoras.py --aplicar

Por defecto solo mueve los pagos a Daniel, que hace la obra nueva — la regla ya
estaba escrita en el OS. Para sumar otros conceptos, agregalos a PATRONES.
"""
import sys, re, datetime as dt

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets

SHEET = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
RANGO = "Movimientos!A1:L2000"

# Cada patron se busca en la columna Observaciones de las filas que hoy son
# "Mejoras". Confirmado por Facu el 10/09/2026: los pagos a Daniel son obra.
PATRONES = [
    ("Daniel (obra nueva)", re.compile(r"daniel", re.I)),
]


def plata(n):
    return f"{n:,.0f}".replace(",", ".")


def main():
    aplicar = "--aplicar" in sys.argv
    sv = sheets("facu")
    v = sv.spreadsheets().values().get(spreadsheetId=SHEET, range=RANGO).execute().get("values", [])
    if len(v) < 2:
        sys.exit("ERROR: la hoja Movimientos vino vacia. No toco nada.")

    objetivo = []
    for i, fila in enumerate(v, 1):
        r = list(fila) + [""] * (12 - len(fila))
        if r[1] != "Egreso" or r[4] != "Mejoras":
            continue
        for etiqueta, pat in PATRONES:
            if pat.search(str(r[7])):
                objetivo.append((i, etiqueta, r[0], r[5], str(r[7])[:45]))
                break

    if not objetivo:
        sys.exit("No encontre ninguna fila de Mejoras que matchee. Reviso PATRONES "
                 "antes de dar esto por hecho.")

    total = 0.0
    print(f"{'FILA':<7}{'FECHA':<12}{'MONTO':>14}  CONCEPTO")
    for i, etiqueta, fecha, monto, obs in objetivo:
        try:
            total += float(str(monto).replace(",", "").replace("$", ""))
        except ValueError:
            sys.exit(f"ERROR: monto ilegible en la fila {i}: {monto!r}")
        print(f"{i:<7}{fecha:<12}{monto:>14}  {obs}  [{etiqueta}]")
    print(f"\n{len(objetivo)} filas · ${plata(total)} pasan de Mejoras a Inversiones.")
    print("Eso SUBE el resultado operativo de esos meses en ese monto.")

    if not aplicar:
        print("\nNada tocado. Corré de nuevo con --aplicar para escribirlo.")
        return

    # Releer justo antes de escribir: si alguien cargo un movimiento mientras
    # tanto, los numeros de fila ya no son los mismos y escribiriamos en la fila
    # equivocada sin que nada avise.
    v2 = sv.spreadsheets().values().get(spreadsheetId=SHEET, range=RANGO).execute().get("values", [])
    for i, _, fecha, monto, _ in objetivo:
        r = list(v2[i - 1]) + [""] * (12 - len(v2[i - 1]))
        if not (r[1] == "Egreso" and r[4] == "Mejoras" and r[0] == fecha and str(r[5]) == str(monto)):
            sys.exit(f"ABORTO: la fila {i} ya no es la que lei ({r[:8]}). "
                     f"Alguien escribio en la hoja: volve a correrlo.")

    res = sv.spreadsheets().values().batchUpdate(spreadsheetId=SHEET, body={
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": f"Movimientos!E{i}", "values": [["Inversiones"]]}
                 for i, *_ in objetivo],
    }).execute()
    print(f"\nCeldas escritas: {res.get('totalUpdatedCells')}")

    v3 = sv.spreadsheets().values().get(spreadsheetId=SHEET, range=RANGO).execute().get("values", [])
    mal = [i for i, *_ in objetivo if (list(v3[i - 1]) + [""] * 12)[4] != "Inversiones"]
    if mal:
        sys.exit(f"ERROR: las filas {mal} NO quedaron en Inversiones.")
    print("Verificado: las {} filas quedaron en Inversiones.".format(len(objetivo)))
    print("\nOJO: el reporte a inversores de agosto ya salio con estos pagos como")
    print("gasto operativo. Si queres el reporte actualizado, hay que regenerarlo.")


if __name__ == "__main__":
    main()
