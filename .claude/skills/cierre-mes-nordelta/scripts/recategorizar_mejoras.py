#!/usr/bin/env python3
"""
Pasa de "Mejoras" a "Inversiones" las filas del Master Plan que son OBRA.

Mejoras es gasto operativo; Inversiones es obra, que la financian los socios con
su capital. Cuando una fila de obra queda en Mejoras, el resultado del mes baja
por una plata que no es gasto del negocio.

    reporte: .../recategorizar_mejoras.py 2026-07            (no toca nada)
    aplicar: .../recategorizar_mejoras.py 2026-07 --aplicar

Mueve TODAS las Mejoras del mes indicado. Facu, 10/09/2026, sobre julio: "esos 6M
metelos todo en inversion" — la obra de julio (Daniel, materiales y los oficios que
la ejecutaron) se cargo entera como Mejoras.

Sin mes, solo mueve los pagos a Daniel de todo el ano, que es la regla que ya
estaba escrita en el OS: Daniel hace la obra nueva.
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


def mes_de(fecha_txt):
    """'17/7/2026' -> '2026-07'. La hoja escribe D/M/AAAA."""
    try:
        d, m, a = [int(x.strip(" .")) for x in str(fecha_txt).split("/")]
        return f"{a}-{m:02d}"
    except Exception:
        return None


def main():
    aplicar = "--aplicar" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mes = args[0] if args else None
    sv = sheets("facu")
    v = sv.spreadsheets().values().get(spreadsheetId=SHEET, range=RANGO).execute().get("values", [])
    if len(v) < 2:
        sys.exit("ERROR: la hoja Movimientos vino vacia. No toco nada.")

    objetivo = []
    for i, fila in enumerate(v, 1):
        r = list(fila) + [""] * (12 - len(fila))
        if r[1] != "Egreso" or r[4] != "Mejoras":
            continue
        if mes:
            # todas las Mejoras de ese mes
            if mes_de(r[0]) != mes:
                continue
            objetivo.append((i, "obra del mes", r[0], r[5], str(r[7])[:45]))
        else:
            for etiqueta, pat in PATRONES:
                if pat.search(str(r[7])):
                    objetivo.append((i, etiqueta, r[0], r[5], str(r[7])[:45]))
                    break

    if not objetivo:
        sys.exit(f"No encontre ninguna fila de Mejoras{' en ' + mes if mes else ''}. "
                 f"No doy esto por hecho sin mirar.")

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
