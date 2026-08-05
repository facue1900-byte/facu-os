#!/usr/bin/env python3
"""
Congela el DETALLE de expensas de un mes dentro de `Expensas Predio`, local por
local, con los mismos números que quedaron en las cuentas corrientes.

    congelar_detalle_expensas.py <AAAA-MM> [--escribir]

## Por qué existe

El bloque de las filas 40-58 de `Expensas Predio` —locales en columnas, conceptos
en filas— es el que Facu le manda por captura a cada locatario. Son DOS fórmulas
`TRANSPOSE` sobre la tabla viva de arriba, y **esa tabla es de un solo mes**: se
recalcula contra la fecha de `A3`. Después de generar los cargos, `A3` vuelve al
mes anterior, así que una captura sacada más tarde le manda al locatario un
número que **no** es el de su cuenta corriente. Esto escribe abajo un bloque
literal, sin fórmulas, que no se mueve.

## Cómo reconstruye el mes sin inventar nada

`EXPENSAS HISTORICO` (Ctas Ctes) guarda sólo los dos totales por local, no el
detalle. Los inputs de la fila 4 se recuperan así:

  · **Servicios comunes**: son `SUMIFS` contra Movimientos filtrando por `A3`.
    Se recalculan acá para el mes pedido. Ojo: `Movimientos!I` guarda el mes como
    TEXTO (`"julio 2026"`) y Sheets lo parsea como fecha al compararlo — hay que
    replicar esa semántica, no comparar literal.
  · **Expensas AVN**: cuando el extracto del Macro no está importado se pone a
    mano, así que no se puede leer. Se **despeja** de un local a partir del
    recupero congelado, y se verifica que ese mismo valor reproduzca a los demás.

Si algún local no cierra contra `EXPENSAS HISTORICO` **y** contra la fila del mes
en su propia pestaña, no escribe nada. Un detalle que no coincide con la cuenta
es exactamente lo que este script existe para evitar.
"""

import argparse
import datetime
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

MASTER = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
EPOCA = datetime.date(1899, 12, 30)
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
L = {c: i for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}

# concepto → (celda de input en la fila 4, columna del % por local)
REC = [("Expensas AVN", "B", "AE"), ("Agua R&S ", "C", "AF"), ("ABL (Municipal) ", "D", "AG")]
SERV = [("Utilidades", "G", "AJ"), ("Administrativos", "H", "AK"),
        ("Limpieza Baños", "I", "AL"), ("Limpieza e Insumos", "J", "AM"),
        ("Limpieza Predio", "K", "AN"), ("Mantenimiento", "L", "AO"),
        ("Jardineria", "M", "AP"), ("Fumigacion", "N", "AQ"),
        ("Comunicación", "O", "AR"), ("Retiro de basura", "P", "AS")]

# El local se llama distinto en Expensas Predio que en su pestaña de cta cte
EN_CTA_CTE = {"Fabric": "Fabric", "Bigg": "Bigg", "Hamburgueseria": "Boss",
              "Heladeria": "Volta + Open 25", "Peak One": "Peak One"}
SIN_FC = {"Peak One", "Volta + Open 25"}          # les corre una columna a la izquierda

FILA_BLOQUE_VIVO = (41, 58)                        # de dónde se copia el formato


def col(s):
    return 26 + L[s[1]] if len(s) == 2 else L[s]


def num(x):
    return float(x) if x not in ("", None) else 0.0


def serial(anio, mes):
    return (datetime.date(anio, mes, 1) - EPOCA).days


def serial_de_texto(txt):
    """`Movimientos!I` guarda 'junio 2026'; Sheets lo lee como 01/06/2026."""
    try:
        m, a = str(txt).strip().lower().split()
        return serial(int(a), MESES.index(m) + 1)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("periodo", help="AAAA-MM del mes a congelar")
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()
    anio, mes = (int(x) for x in args.periodo.split("-"))
    per = serial(anio, mes)
    etiqueta = f"{MESES[mes - 1].upper()} {anio}"

    sv = sheets().spreadsheets()
    pred = sv.values().get(spreadsheetId=MASTER, range="Expensas Predio!A1:AS31",
                           valueRenderOption="UNFORMATTED_VALUE").execute()["values"]

    def fila(i):
        return (pred[i - 1] if i - 1 < len(pred) else []) + [""] * 46

    mov = sv.values().get(spreadsheetId=MASTER, range="Movimientos!A1:N2000",
                          valueRenderOption="UNFORMATTED_VALUE").execute()["values"]

    def sumifs(cat, p):
        return sum(num(r[5]) for r in (x + [""] * 14 for x in mov[1:])
                   if str(r[1]).strip() == "Egreso" and str(r[4]).strip() == cat
                   and serial_de_texto(r[8]) == p)

    hist = sv.values().get(spreadsheetId=CTAS, range="EXPENSAS HISTORICO!A2:D200",
                           valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    congelado = {r[1]: (float(r[2]), float(r[3])) for r in hist if r and int(r[0]) == per}
    if not congelado:
        sys.exit(f"⚠ {args.periodo} no está en EXPENSAS HISTORICO: primero hay que "
                 f"correr cargos_del_mes.py --congelar-expensas")

    # ── inputs de la fila 4 tal como estaban al congelar el mes
    inp = list(fila(4))
    inp[L["I"]] = sumifs("Sueldo Mantenimiento Gastronomia", per) / 2
    inp[L["K"]] = inp[L["I"]]                                   # K4 = I4
    inp[L["J"]] = sumifs("Productos de limpieza", per)
    inp[L["N"]] = sumifs("Fumigación", per)
    # P4 está clavado a "mayo 2026"/3 en la hoja: no depende del mes elegido
    inp[L["P"]] = sumifs("Retiro de Residuos", serial(2026, 5)) / 3

    locales = [(i, fila(i)[0]) for i in range(7, 30) if fila(i)[0]]
    porc = {loc: fila(i) for i, loc in locales}

    # ── la AVN se despeja de un local y se valida contra todos los demás
    ancla = next(loc for _, loc in locales if loc in congelado
                 and num(porc[loc][col("AE")]) > 0)
    r = porc[ancla]
    avn = ((congelado[ancla][0] - num(inp[L["C"]]) * num(r[col("AF")])
            - num(inp[L["D"]]) * num(r[col("AG")])) / num(r[col("AE")]))
    inp[L["B"]] = avn
    print(f"AVN de {etiqueta} despejada desde {ancla}: ${avn:,.2f}")

    detalle = {}
    for i, loc in locales:
        r, d = porc[loc], {}
        for n, ci, pi in REC:
            d[n] = num(inp[L[ci]]) * num(r[col(pi)])
        d["Rec. de Gastos Total"] = sum(d[n] for n, _, _ in REC)
        for n, ci, pi in SERV:
            v = num(inp[L[ci]]) * num(r[col(pi)])
            if n == "Mantenimiento" and i == 7:      # sólo Peak One va a la mitad
                v /= 2
            d[n] = v
        d["Servicios comunes Total"] = sum(d[n] for n, _, _ in SERV)
        d["Total Expensas"] = d["Rec. de Gastos Total"] + d["Servicios comunes Total"]
        detalle[loc] = d

    # ── verificación 1: contra EXPENSAS HISTORICO
    ok = True
    for loc, (rh, sh) in sorted(congelado.items()):
        d = detalle.get(loc)
        if not d or abs(d["Rec. de Gastos Total"] - rh) > 0.01 \
                 or abs(d["Servicios comunes Total"] - sh) > 0.01:
            ok = False
            print(f"   MAL {loc}: recupero {d and d['Rec. de Gastos Total']:.2f} vs {rh:.2f} · "
                  f"servicios {d and d['Servicios comunes Total']:.2f} vs {sh:.2f}")
    print(f"   {'OK ' if ok else 'MAL'} 1/2 · {len(congelado)} locales contra EXPENSAS HISTORICO")

    # ── verificación 2: contra lo que el locatario ve en su cuenta corriente
    etq = f"{MESES[mes - 1][:3].upper()}'{anio % 100}"
    ok2 = True
    for loc, pest in EN_CTA_CTE.items():
        if loc not in detalle:
            continue
        vals = sv.values().get(spreadsheetId=CTAS, range=f"{pest}!A1:G200",
                               valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
        ceg = 4 if pest in SIN_FC else 5
        halla = {}
        for f in vals:
            f = f + [""] * 8
            if str(f[0]).strip().upper().replace(" ", "") == etq and isinstance(f[ceg], (int, float)):
                halla[str(f[2]).strip().lower()] = float(f[ceg])
        d = detalle[loc]
        bien = all(halla.get(k) is not None and abs(halla[k] - d[v]) < 0.01
                   for k, v in (("recupero de gastos", "Rec. de Gastos Total"),
                                ("servicios comunes", "Servicios comunes Total")))
        ok2 &= bien
        print(f"   {'OK ' if bien else 'MAL'}   {pest:18s} recupero ${d['Rec. de Gastos Total']:>13,.2f}"
              f"  servicios ${d['Servicios comunes Total']:>13,.2f}")
    print(f"   {'OK ' if ok2 else 'MAL'} 2/2 · contra la cuenta que ve el locatario")
    if not (ok and ok2):
        sys.exit("\n⚠ NO se escribe: el detalle no coincide con la cuenta corriente")

    CONCEPTOS = ([n for n, _, _ in REC] + ["Rec. de Gastos Total", ""]
                 + [n for n, _, _ in SERV] + ["Servicios comunes Total", "Total Expensas"])
    nombres = [loc for _, loc in locales]
    salida = [[per] + nombres + ["Total"]]
    for c in CONCEPTOS:
        if not c:
            salida.append([""] * (len(nombres) + 2))
            continue
        vals = [detalle[loc][c] for loc in nombres]
        salida.append([c] + vals + [sum(vals)])

    # ── dónde va: después de todo lo escrito, y nunca dos veces el mismo mes
    usadas = sv.values().get(spreadsheetId=MASTER, range="Expensas Predio!A1:A400",
                             valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    for i, f in enumerate(usadas, 1):
        if f and str(f[0]).startswith(etiqueta):
            sys.exit(f"⚠ {etiqueta} ya está congelado en la fila {i} — borrarlo a mano si "
                     f"hay que rehacerlo")
    titulo = max(len(usadas) + 2, FILA_BLOQUE_VIVO[1] + 3)
    r0 = titulo + 1
    print(f"\nBloque «{etiqueta}» → filas {r0}:{r0 + len(salida) - 1} "
          f"({len(nombres)} locales × {len([c for c in CONCEPTOS if c])} conceptos)")
    if not args.escribir:
        print("(dry-run: no se escribió nada)")
        return

    sid = next(s["properties"]["sheetId"] for s in sv.get(spreadsheetId=MASTER).execute()["sheets"]
               if s["properties"]["title"] == "Expensas Predio")
    sv.values().batchUpdate(spreadsheetId=MASTER, body={
        "valueInputOption": "RAW", "data": [
            {"range": f"Expensas Predio!A{titulo}",
             "values": [[f"{etiqueta} — CONGELADO · es lo que está en las cuentas corrientes. "
                         f"No tiene fórmulas: no cambia cuando arriba se cambia de mes."]]},
            {"range": f"Expensas Predio!A{r0}", "values": salida}]}).execute()
    v0, v1 = FILA_BLOQUE_VIVO
    sv.batchUpdate(spreadsheetId=MASTER, body={"requests": [{"copyPaste": {
        "source": {"sheetId": sid, "startRowIndex": v0 - 1, "endRowIndex": v1,
                   "startColumnIndex": 0, "endColumnIndex": 26},
        "destination": {"sheetId": sid, "startRowIndex": r0 - 1,
                        "endRowIndex": r0 - 1 + len(salida),
                        "startColumnIndex": 0, "endColumnIndex": 26},
        "pasteType": "PASTE_FORMAT"}}]}).execute()

    leido = sv.values().get(spreadsheetId=MASTER,
                            range=f"Expensas Predio!A{r0}:Z{r0 + len(salida) - 1}",
                            valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    malas = sum(1 for esp, got in zip(salida, leido)
                for a, b in zip(esp, got + [""] * (len(esp) - len(got)))
                if (abs(a - b) > 0.01 if isinstance(a, (int, float)) and isinstance(b, (int, float))
                    else str(a) != str(b)))
    print("✅ escrito y releído: idéntico" if not malas else f"⚠ {malas} celdas no coinciden")
    sys.exit(0 if not malas else 1)


if __name__ == "__main__":
    main()
