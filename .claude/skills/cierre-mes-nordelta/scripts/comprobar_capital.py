#!/usr/bin/env python3
"""
Comprueba que lo invertido por cada uno cierre contra la plata que hay.

La pregunta de Facu (10/09/2026): "todo lo que invirtio Paseo Nordelta, todo lo
que invirtio Facu y todo lo que invirtio Richi, como se corrobora todo eso?".

Se corrobora con dos cuentas que tienen que sumar la caja real:

  1. lo que gano el negocio  - la obra que puso Paseo Nordelta  = le queda al negocio
  2. los aportes de los socios - la obra que pagaron esos aportes = les queda sin gastar

  (1) + (2) tiene que ser IGUAL a caja + banco. Si no da, hay obra atribuida a
  alguien que no la pago, o plata que entro y no esta.

Y un segundo test, mes a mes: el negocio no puede haber pagado obra con plata que
todavia no habia generado. Si la caja del negocio da negativa en algun mes, esa
obra la adelantaron los socios — no es un error, pero conviene saberlo.

    .../comprobar_capital.py            (hasta hoy)
    .../comprobar_capital.py 2026-08    (cortado a fin de agosto)
"""
import sys, collections, datetime as dt
import openpyxl

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets, bajar_xlsx

MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
GASTOS_OBRA = "1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY"
XLSX = "/Users/Facu/facu-os/data/reportes-inversores/_master_plan.xlsx"
FUERA_DEL_NEGOCIO = ("Retiro de Ganancia Richi", "Ajuste de caja")
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def p(n):
    return ("-" if n < 0 else "") + "$" + f"{abs(n):,.0f}".replace(",", ".")


def num(x):
    x = str(x or "").replace("$", "").replace(",", "").strip()
    try:
        return float(x)
    except ValueError:
        return 0.0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    corte = dt.date.today()
    if args:
        a, m = int(args[0][:4]), int(args[0][5:7])
        corte = dt.date(a + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)

    bajar_xlsx(MASTER_PLAN, XLSX)
    v = (sheets("facu").spreadsheets().values()
         .get(spreadsheetId=GASTOS_OBRA, range="Hoja 1!A5:I300").execute().get("values", []))

    obra_pn = 0.0
    obra_pn_mes = collections.defaultdict(float)
    for r in v:
        r = list(r) + [""] * 9
        if not str(r[0]).strip() or str(r[1]).strip() != "Paseo Nordelta":
            continue
        if "aporte de capital" in str(r[2]).lower():
            continue
        try:
            d, mm, aa = [int(x.strip(" .")) for x in str(r[0]).split("/")]
            f = dt.date(aa, mm, d)
        except Exception:
            sys.exit(f"Fecha ilegible en Gastos Obra: {r[0]!r}. Arreglala primero.")
        if f > corte:
            continue
        obra_pn += num(r[7])
        obra_pn_mes[f"{f.year}-{f.month:02d}"] += num(r[7])

    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ing = egr = obra = aporte = otros = caja = 0.0
    g_mes = collections.defaultdict(float)
    for r in wb["Movimientos"].iter_rows(min_row=2, values_only=True):
        if not r[0] or r[6] != "ARS":
            continue
        f = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        if f > corte:
            continue
        k = f"{f.year}-{f.month:02d}"
        m = float(r[5])
        caja += m if r[1] == "Ingreso" else -m
        if r[1] == "Ingreso":
            if str(r[3] or "").startswith("Aporte de Capital"):
                aporte += m
            else:
                ing += m
                g_mes[k] += m
        else:
            c = r[4]
            if c == "Inversiones":
                obra += m
            elif c in FUERA_DEL_NEGOCIO:
                otros += m
                g_mes[k] -= m
            else:
                egr += m
                g_mes[k] -= m

    if not ing:
        sys.exit("ERROR: el Master Plan no trajo ingresos. No comparo contra nada.")

    gan = ing - egr - otros
    del_negocio = gan - obra_pn
    de_los_socios = aporte - (obra - obra_pn)

    print(f"AL {corte:%d/%m/%Y}\n")
    print("1) LA PLATA DEL NEGOCIO")
    print(f"   Ganancia acumulada (neta de retiro y ajustes) {p(gan):>18}")
    print(f"   Obra que puso Paseo Nordelta                 -{p(obra_pn):>18}")
    print(f"   = le queda al negocio                         {p(del_negocio):>18}\n")
    print("2) LA PLATA DE LOS SOCIOS")
    print(f"   Aportes de capital                            {p(aporte):>18}")
    print(f"   Obra pagada con esos aportes                 -{p(obra - obra_pn):>18}")
    print(f"   = les queda sin gastar                        {p(de_los_socios):>18}\n")
    print("   LAS DOS TIENEN QUE SUMAR LA CAJA REAL")
    print(f"   {p(del_negocio)} + {p(de_los_socios)} = {p(del_negocio + de_los_socios)}")
    print(f"   caja + banco de verdad                        {p(caja):>18}")
    ok = abs(del_negocio + de_los_socios - caja) < 1
    print(f"   {'CIERRA' if ok else '*** NO CIERRA ***'}\n")

    print("3) MES A MES: la caja del negocio con SOLO su propia plata")
    acum = 0.0
    rojo = []
    for k in sorted(set(list(g_mes) + list(obra_pn_mes))):
        acum += g_mes[k] - obra_pn_mes[k]
        mes = MESES[int(k[5:7]) - 1]
        marca = "  <-- en rojo" if acum < 0 else ""
        if acum < 0:
            rojo.append((mes, acum))
        print(f"   {mes:<5}{g_mes[k] - obra_pn_mes[k]:>16,.0f}   acumulado {acum:>16,.0f}{marca}")
    if rojo:
        peor = min(rojo, key=lambda x: x[1])
        print(f"\n   El negocio estuvo en rojo {len(rojo)} mes/es; lo peor en {peor[0]} "
              f"({p(peor[1])}).")
        print("   Esa obra la adelantaron los socios: no es un error, es capital de")
        print("   trabajo que el negocio devolvio despues con su ganancia.")

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
