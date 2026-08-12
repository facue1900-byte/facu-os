#!/usr/bin/env python3
"""Separa pesos de dólares en el Dashboard Mensual, y hace entrar las filas 2-5.

Tres cosas, todas en el Master Plan:

1. **La ARRAYFORMULA del Mes arranca en `I6`**, o sea sobre `A6:A`. Las filas 2 a
   5 de `Movimientos` quedan arriba de su rango, con el mes vacío, y el SUMIFS
   —que filtra por esa columna— no las cuenta: **$14.918.105 de enero afuera de
   todos los totales**, viéndose perfectas en la hoja. Se mueve a `I2`.

2. **Ningún SUMIFS filtraba por moneda.** Con la corrección de arriba, los
   US$6.000 de las filas 3 y 4 entrarían sumados como si fueran $6.000 pesos. Y
   con las categorías «Pesos a USD» y «Cambio de USD» abiertas, el próximo
   movimiento en dólares hacía el mismo estropicio. Cada renglón pasa a llevar
   `Movimientos!$G:$G, "ARS"`.

3. **La fila 7 «u$s» apuntaba a `=B23`**, que es el renglón de Pizzería: mostraba
   $0 porque Pizzería está en cero, no porque no hubiera dólares. Pasa a ser el
   neto real en USD del mes.

    separar_monedas.py            dice qué haría, sin escribir
    separar_monedas.py --send     lo aplica

Las fórmulas de antes quedan en `archive/dashboard-mensual-formulas-2026-08-12/`.
"""
import re
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

MP = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
DASH = "Dashboard Mensual"
# Los dos bloques de renglones que suman desde Movimientos
BLOQUES = [(9, 42, "Ingreso"), (46, 76, "Egreso")]
MES_VIEJA, MES_NUEVA = "I6", "I2"
FORMULA_MES = '=ARRAYFORMULA(IF(A{0}:A="","",TEXT(A{0}:A,"mmmm yyyy")))'


def col(j):
    """0 → A, 25 → Z, 26 → AA"""
    s = ""
    j += 1
    while j:
        j, r = divmod(j - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    send = "--send" in sys.argv
    sv = sheets().spreadsheets()
    dash = sv.values().get(spreadsheetId=MP, range=f"{DASH}!A1:AZ85",
                           valueRenderOption="FORMULA").execute()["values"]

    # ---- 1) la ARRAYFORMULA del Mes, de I6 a I2
    print(f"1 · columna Mes: {MES_VIEJA} → {MES_NUEVA}")
    print(f"    {FORMULA_MES.format(2)}")
    print("    hace entrar las filas 2 a 5 (enero-26) que hoy no suma nadie")

    # ---- 2) el filtro de moneda en cada SUMIFS
    print("\n2 · filtro de moneda en los SUMIFS")
    cambios, ya = [], 0
    for desde, hasta, _ in BLOQUES:
        for i in range(desde, hasta + 1):
            fila = (dash[i - 1] if i <= len(dash) else []) + [""] * 60
            for j, f in enumerate(fila):
                if not isinstance(f, str) or not f.startswith("=SUMIFS(Movimientos"):
                    continue
                if 'Movimientos!$G:$G' in f:
                    ya += 1
                    continue
                # el filtro entra antes del criterio de mes, que es el último par
                nueva = re.sub(r"(,\s*Movimientos!\$I:\$I,\s*[A-Z]+\$3\s*\))",
                               r',Movimientos!$G:$G, "ARS"\1', f, count=1)
                if nueva == f:
                    print(f"    ⚠ {col(j)}{i}: no reconocí el patrón, la salteo")
                    continue
                cambios.append((f"{DASH}!{col(j)}{i}", nueva))
    print(f"    {len(cambios)} fórmulas a tocar · {ya} ya lo tenían")
    if cambios:
        c = cambios[0]
        print(f"    ejemplo {c[0]}:\n      {c[1]}")

    # ---- 3) la fila 7 «u$s»: el neto en dólares del mes
    print("\n3 · fila 7 «u$s» (hoy dice =B23, que es el renglón de Pizzería)")
    enc, medios = dash[2] + [""] * 60, dash[4] + [""] * 60
    usd = []
    for j in range(1, 60):
        if not str(enc[j]).strip() or not str(medios[j]).strip():
            continue
        medio = str(medios[j]).strip()
        f = (f'=SUMIFS(Movimientos!$F:$F,Movimientos!$B:$B,"Ingreso",'
             f'Movimientos!$C:$C,"{medio}",Movimientos!$G:$G,"USD",Movimientos!$I:$I,{col(j)}$3)'
             f'-SUMIFS(Movimientos!$F:$F,Movimientos!$B:$B,"Egreso",'
             f'Movimientos!$C:$C,"{medio}",Movimientos!$G:$G,"USD",Movimientos!$I:$I,{col(j)}$3)')
        usd.append((f"{DASH}!{col(j)}7", f))
    print(f"    {len(usd)} columnas (una por mes y medio)")
    print(f"    ejemplo {usd[0][0]}:\n      {usd[0][1]}")

    if not send:
        print("\n(dry-run: no escribí nada. Con --send se aplica.)")
        return

    data = [{"range": r, "values": [[f]]} for r, f in cambios + usd]
    # el Mes se hace aparte y en orden: primero se borra la vieja, si no la nueva
    # choca contra ella al derramar y queda #REF
    sv.values().clear(spreadsheetId=MP, range=f"Movimientos!{MES_VIEJA}").execute()
    sv.values().update(spreadsheetId=MP, range=f"Movimientos!{MES_NUEVA}",
                       valueInputOption="USER_ENTERED",
                       body={"values": [[FORMULA_MES.format(2)]]}).execute()
    for i in range(0, len(data), 400):
        sv.values().batchUpdate(spreadsheetId=MP, body={
            "valueInputOption": "USER_ENTERED", "data": data[i:i + 400]}).execute()
    print(f"\nLISTO — {len(data)} fórmulas + la columna Mes.")
    print("Ahora: verificar_dashboard.py mes por mes.")


if __name__ == "__main__":
    main()
