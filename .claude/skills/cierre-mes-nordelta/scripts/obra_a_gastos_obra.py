#!/usr/bin/env python3
"""
Anota en Gastos Obra la obra que el Paseo pago de su propia caja.

Cuando un gasto pasa de "Mejoras" a "Inversiones" en el Master Plan, sube el
resultado del negocio — pero esa plata salio igual. Si no se anota tambien del
lado de LO INVERTIDO, el modelo de recupero se queda con el beneficio y sin el
costo, y los anos para recuperar bajan sin que nada haya mejorado.

    reporte: .../obra_a_gastos_obra.py 2026-07
    aplicar: .../obra_a_gastos_obra.py 2026-07 --aplicar

    otro aportante y un subconjunto:
      .../obra_a_gastos_obra.py 2026-07 --quien Richi --solo "cuota" --aplicar

Toma los egresos de Inversiones pagados por CAJA en ese mes que todavia no esten
en Gastos Obra, y los agrega como aporte de "Paseo Nordelta". Solo escribe A:F:
las columnas H e I ya traen su formula puesta hasta la fila 130.
"""
import sys, collections, datetime as dt
import httpx, openpyxl

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets, bajar_xlsx

MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
GASTOS_OBRA = "1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY"
XLSX = "/Users/Facu/facu-os/data/reportes-inversores/_master_plan.xlsx"
QUIEN = "Paseo Nordelta"
ULTIMA_FILA_CON_FORMULA = 130

# Egresos que YA estaban en Inversiones antes de la recategorizacion del 10/09/2026
# y que Facu no pidio anotar todavia. Las cuotas municipales son un plan de pagos
# que ademas aparece con los mismos importes en julio, agosto y septiembre: hay
# que mirarlo antes de sumarlo a lo invertido.
EXCLUIR = ["derechos de construccion", "plan de pagos fondo y aridos",
           "pague daniel 700.000"]


def blue(fecha):
    """Promedio compra/venta del blue de ese dia. Sin cotizacion no se inventa."""
    r = httpx.get(f"https://api.argentinadatos.com/v1/cotizaciones/dolares/blue/"
                  f"{fecha.year}/{fecha.month:02d}/{fecha.day:02d}", timeout=30)
    if r.status_code >= 300:
        sys.exit(f"No pude traer el blue del {fecha:%d/%m/%Y} ({r.status_code}). "
                 f"Sin cotizacion no escribo la fila.")
    d = r.json()
    return round((float(d["compra"]) + float(d["venta"])) / 2, 2)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("Uso: obra_a_gastos_obra.py AAAA-MM [--aplicar]")
    anio, mes = int(args[0][:4]), int(args[0][5:7])
    aplicar = "--aplicar" in sys.argv
    quien = QUIEN
    solo = None
    for i, a in enumerate(sys.argv):
        if a == "--quien" and i + 1 < len(sys.argv):
            quien = sys.argv[i + 1]
        if a == "--solo" and i + 1 < len(sys.argv):
            solo = sys.argv[i + 1].lower()

    print("Bajando el Master Plan...")
    bajar_xlsx(MASTER_PLAN, XLSX)
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    obra, excluidas = [], []
    for r in wb["Movimientos"].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        f = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        if (f.year, f.month) != (anio, mes):
            continue
        if r[1] == "Egreso" and r[4] == "Inversiones" and r[2] == "Caja" and r[6] == "ARS":
            obs = str(r[7] or "").strip()
            if solo is not None:
                # --solo manda: se anota exactamente lo que matchea, sin EXCLUIR
                (obra if solo in obs.lower() else excluidas).append((f, float(r[5]), obs))
                continue
            if any(x in obs.lower() for x in EXCLUIR):
                excluidas.append((f, float(r[5]), obs))
                continue
            obra.append((f, float(r[5]), obs))
    if not obra:
        sys.exit(f"No hay Inversiones pagadas por caja en {anio}-{mes:02d}.")

    sv = sheets("facu")
    v = sv.spreadsheets().values().get(spreadsheetId=GASTOS_OBRA,
                                       range="Hoja 1!A1:I200").execute().get("values", [])
    # Lo que ya esta anotado, para no duplicar: (fecha, monto) contando repetidos
    ya = collections.Counter()
    ultima = 0
    for i, fila in enumerate(v, 1):
        fila = list(fila) + [""] * (9 - len(fila))
        if not str(fila[0]).strip():
            continue
        ultima = i
        try:
            d, m, a = [int(x.strip(" .")) for x in str(fila[0]).split("/")]
            monto = float(str(fila[3]).replace("$", "").replace(",", "").strip())
            ya[(dt.date(a, m, d), round(monto, 2))] += 1
        except Exception:
            continue

    nuevas = []
    for f, monto, obs in sorted(obra):
        k = (f, round(monto, 2))
        if ya[k] > 0:
            ya[k] -= 1
            continue
        nuevas.append((f, monto, obs))

    print(f"\nInversiones por caja en {anio}-{mes:02d}: {len(obra)} filas, "
          f"${sum(x[1] for x in obra):,.0f}")
    if excluidas:
        print(f"Excluidas por EXCLUIR: {len(excluidas)} filas, "
              f"${sum(x[1] for x in excluidas):,.0f} — NO se anotan:")
        for f, m, o in excluidas:
            print(f"   {f:%d/%m}  {m:>13,.0f}  {o[:50]}")
    print(f"Ya estaban en Gastos Obra: {len(obra) - len(nuevas)}")
    print(f"A agregar como '{quien}': {len(nuevas)}  (${sum(x[1] for x in nuevas):,.0f})")
    if not nuevas:
        print("\nNada que agregar.")
        return

    desde = ultima + 1
    hasta = desde + len(nuevas) - 1
    print(f"Irian en las filas {desde} a {hasta} (ultima con datos hoy: {ultima})")
    if hasta > ULTIMA_FILA_CON_FORMULA:
        sys.exit(f"ABORTO: la fila {hasta} pasa de la {ULTIMA_FILA_CON_FORMULA}, "
                 f"que es hasta donde llegan las formulas de H e I. Copialas mas "
                 f"abajo primero: si no, esa plata no suma en ningun total.")

    # Ninguna de esas filas puede tener algo escrito en A:F
    for i in range(desde, hasta + 1):
        fila = list(v[i - 1]) + [""] * 9 if i - 1 < len(v) else [""] * 9
        if any(str(x).strip() for x in fila[:6]):
            sys.exit(f"ABORTO: la fila {i} no esta vacia: {fila[:6]}")

    print("\nTrayendo el dolar blue de cada fecha...")
    fx = {f: blue(f) for f in sorted({x[0] for x in nuevas})}
    for f, c in fx.items():
        print(f"  {f:%d/%m/%Y}  ${c:,.2f}")

    filas = [[f"{f.day}/{f.month}/{f.year}", quien, obs, monto, "ARS", fx[f]]
             for f, monto, obs in nuevas]
    print(f"\n{'FILA':<7}{'FECHA':<12}{'MONTO':>13}  CONCEPTO")
    for i, (fila, (f, monto, obs)) in enumerate(zip(filas, nuevas), desde):
        print(f"{i:<7}{fila[0]:<12}{monto:>13,.0f}  {obs[:45]}")

    if not aplicar:
        print("\nNada escrito. Corré de nuevo con --aplicar.")
        return

    res = sv.spreadsheets().values().update(
        spreadsheetId=GASTOS_OBRA, range=f"Hoja 1!A{desde}:F{hasta}",
        valueInputOption="USER_ENTERED", body={"values": filas}).execute()
    print(f"\nCeldas escritas: {res.get('updatedCells')}")

    # Verificar leyendo de vuelta, incluido que H se haya calculado
    v2 = sv.spreadsheets().values().get(spreadsheetId=GASTOS_OBRA,
                                        range=f"Hoja 1!A{desde}:I{hasta}").execute().get("values", [])
    suma = 0.0
    for fila in v2:
        fila = list(fila) + [""] * 9
        try:
            suma += float(str(fila[7]).replace("$", "").replace(",", "").strip())
        except ValueError:
            sys.exit(f"ERROR: la columna H no calculo en la fila {fila[:4]}")
    print(f"Verificado: {len(v2)} filas, la columna H suma ${suma:,.0f}")
    if abs(suma - sum(x[1] for x in nuevas)) > 1:
        sys.exit("ERROR: lo que quedo escrito no suma lo que mande.")
    print(f"\n'{quien}' sube ${suma:,.0f} en Gastos Obra.")


if __name__ == "__main__":
    main()
