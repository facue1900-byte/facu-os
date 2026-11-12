#!/usr/bin/env python3
"""
Radar de deudores — Paseo Nordelta (Ctas Ctes).

Lee las **pestañas de cada local** del sheet Ctas Ctes (Fabric, Bigg, Boss, Volta,
Peak One) y, para los que no tienen pestaña (Salón, Escuelita, La Jaula), CARGOS
menos Cobros. Dice quién debe qué HOY.

    .venv/bin/python radar_deudores.py <ctas_ctes.xlsx> <AAAA-MM del mes corriente>

**No lee la pestaña consolidada «CUENTA CORRIENTE».** Era una grilla de filas fijas
(período × local) armada a mano hasta jul-26 y nadie la extendió: el 11/11/2026 el
brief de Jarvis mostraba la deuda de julio como si fuera de hoy. La pestaña del
local es la que Facu verifica y la que ve el locatario: es la única fuente.

Convención (verificada en las cinco pestañas, ver `reglas_locales.mes_de_cobro`):
el bloque que se cobra en el mes M es **alquiler de M + expensas de M−1**.
  · exigible  = cargos de bloques anteriores al mes corriente − TODOS los pagos
                (un pago cancela lo más viejo primero)
  · en curso  = el bloque del mes corriente, menos lo que sobre de los pagos
  · futuro    = bloques de meses que vienen

Si la fuente de un local está atrasada (su último período cargado tiene más de un
mes de atraso) o la cadena del saldo no cierra, ese local NO se informa: se avisa.

No manda nada ni escribe en ningún lado: sólo lee y reporta.
"""

import collections
import datetime
import re
import sys
import unicodedata

import openpyxl

from reglas_locales import (REGLAS, PAGAN_POR_BANCO, PAGAN_ADELANTADO,  # noqa: E402
                            PESTANAS, CARGOS_SIN_PESTANA, CARGOS_CON_PESTANA,
                            mes_de_cobro)

MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6,
         "JUL": 7, "AGO": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DIC": 12}
TOLERANCIA = 100.0      # $: menos que esto es redondeo de centavos de los pagos, no deuda
ATRASO_MAX = 1          # meses de atraso del último período antes de dejar de informar


def periodo_de(valor):
    """«OCT'26», «JUL' 26» o una fecha → (año, mes). Si no es período, None."""
    if isinstance(valor, (datetime.datetime, datetime.date)):
        return (valor.year, valor.month)
    m = re.fullmatch(r"\s*([A-Za-z]{3})\s*'\s*(\d{2})\s*", str(valor or ""))
    if m and m.group(1).upper() in MESES:
        return (2000 + int(m.group(2)), MESES[m.group(1).upper()])
    return None


def _num(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else 0.0


def _norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.lower().split())


def meses_de_diferencia(a, b):
    return (b[0] - a[0]) * 12 + (b[1] - a[1])


def leer_pestana(nombre, filas, layout):
    """Movimientos de una pestaña de local. `filas` = filas desde la 1 (lista de listas)."""
    _, cd, cin, ceg, csal, signo = layout
    movs, saldo_final, ultimo = [], None, None
    for i, r in enumerate(filas, 1):
        if i < 6:
            continue
        r = list(r) + [None] * 10
        det, ing, eg = str(r[cd] or "").strip(), _num(r[cin]), _num(r[ceg])
        # El último período cargado cuenta aunque el cargo sea $0 (Peak One no paga
        # alquiler: su NOV'26 está, en cero). Sin esto parecería atrasado.
        per_fila = periodo_de(r[0]) if not isinstance(r[0], (datetime.datetime, datetime.date)) else None
        es_cargo = isinstance(r[ceg], (int, float)) and not isinstance(r[ceg], bool)
        if per_fila and det and es_cargo and (ultimo is None or per_fila > ultimo):
            ultimo = per_fila
        if eg:
            per = periodo_de(r[0])
            if per is None:
                raise ValueError(f"{nombre} fila {i}: cargo de ${eg:,.2f} sin período "
                                 f"legible en A ({r[0]!r})")
            movs.append({"local": nombre, "tipo": "cargo", "periodo": per,
                         "mes_cobro": mes_de_cobro(det, per), "monto": eg})
        if ing:
            f = r[0] if isinstance(r[0], (datetime.datetime, datetime.date)) else None
            movs.append({"local": nombre, "tipo": "pago", "fecha": f, "monto": ing})
        if eg or ing:
            saldo_final = _num(r[csal]) * signo
    return movs, saldo_final, ultimo


def leer_sin_pestana(cargos, cobros):
    """CARGOS (Período, Local, Concepto, Monto, IVA, Total…) y Cobros (Fecha, Local,
    Monto, Medio…) para los locales sin pestaña. Misma regla de cobro que las pestañas
    (`mes_de_cobro`): Marina paga el alquiler del Salón en el mes y las expensas al
    siguiente — en nov-26 pagó las dos (05 y 09/11)."""
    movs = []
    for r in cargos:
        r = list(r) + [None] * 8
        local = str(r[1] or "").strip()
        if local in CARGOS_CON_PESTANA or not local:
            continue
        per = periodo_de(r[0])
        total = _num(r[5])
        if per is None or not total:
            continue
        if local not in CARGOS_SIN_PESTANA:
            raise ValueError(f"CARGOS tiene el local {local!r} que el radar no conoce — "
                             f"agregarlo en reglas_locales (CARGOS_SIN_PESTANA o PESTANAS)")
        movs.append({"local": local, "tipo": "cargo", "periodo": per,
                     "mes_cobro": mes_de_cobro(str(r[2] or ""), per), "monto": total})
    alias = {_norm(a): loc for loc, als in CARGOS_SIN_PESTANA.items() for a in als}
    for r in cobros:
        r = list(r) + [None] * 5
        loc = alias.get(_norm(r[1]))
        if loc and str(r[3] or "").strip().lower() in ("caja", "banco") and _num(r[2]):
            f = r[0] if isinstance(r[0], (datetime.datetime, datetime.date)) else None
            movs.append({"local": loc, "tipo": "pago", "fecha": f, "monto": _num(r[2])})
    return movs


def leer_fuente(hojas):
    """`hojas` = {nombre de pestaña: filas desde la 1}. Devuelve (movimientos, chequeos)
    donde chequeos[local] = {"saldo_pestana", "neto"} para verificar la cadena."""
    movs, chequeos = [], {}
    for tab, layout in PESTANAS.items():
        if tab not in hojas:
            raise ValueError(f"falta la pestaña {tab!r} en Ctas Ctes")
        m, saldo, ultimo = leer_pestana(tab, hojas[tab], layout)
        if not m:
            raise ValueError(f"la pestaña {tab!r} vino sin movimientos — es un error, no un dato")
        neto = sum(x["monto"] for x in m if x["tipo"] == "cargo") - \
            sum(x["monto"] for x in m if x["tipo"] == "pago")
        chequeos[tab] = {"saldo_pestana": saldo, "neto": neto, "ultimo_periodo": ultimo}
        movs += m
    for h in ("CARGOS", "Cobros"):
        if not hojas.get(h):
            raise ValueError(f"falta la hoja {h!r} en Ctas Ctes (o vino vacía)")
    movs += leer_sin_pestana(hojas["CARGOS"][3:], hojas["Cobros"][2:])
    return movs, chequeos


def leer_xlsx(xlsx):
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    hojas = {n: [list(r) for r in wb[n].iter_rows(values_only=True)]
             for n in list(PESTANAS) + ["CARGOS", "Cobros"] if n in wb.sheetnames}
    return leer_fuente(hojas)


def clasificar(movs, corriente, chequeos=None):
    """(deudores, al_dia, con_regla, sin_dato). Las tres primeras: listas de (local, saldos).
    `sin_dato`: [(local, motivo)] — locales cuya fuente está atrasada o no cierra; NO se
    informan como deuda ni como al día. La usa también el brief de Jarvis."""
    locales = collections.defaultdict(lambda: {"viejo": 0.0, "corriente_cargo": 0.0,
                                               "futuro": 0.0, "pagos": 0.0,
                                               "corriente_pagos": 0.0, "ultimo_periodo": None})
    for x in movs:
        loc = locales[x["local"]]
        if x["tipo"] == "cargo":
            if x["mes_cobro"] < corriente:
                loc["viejo"] += x["monto"]
            elif x["mes_cobro"] == corriente:
                loc["corriente_cargo"] += x["monto"]
            else:
                loc["futuro"] += x["monto"]
            if loc["ultimo_periodo"] is None or x["periodo"] > loc["ultimo_periodo"]:
                loc["ultimo_periodo"] = x["periodo"]
        else:
            loc["pagos"] += x["monto"]
            if x.get("fecha") and (x["fecha"].year, x["fecha"].month) == corriente:
                loc["corriente_pagos"] += x["monto"]

    deudores, al_dia, con_regla, sin_dato = [], [], [], []
    for nombre in sorted(locales):
        loc = locales[nombre]
        neto = loc["viejo"] - loc["pagos"]               # pagos cancelan lo más viejo
        # Si los pagos superan lo vencido, el excedente cubre el bloque en curso: no es «a favor».
        loc["exigible"] = neto if neto > TOLERANCIA else 0.0
        loc["residuo"] = neto if abs(neto) <= TOLERANCIA else 0.0
        loc["en_curso"] = max(0.0, loc["corriente_cargo"] + min(0.0, neto))
        # A favor de verdad = pagó más que TODO lo cargado (también lo que viene).
        total = neto + loc["corriente_cargo"] + loc["futuro"]
        loc["saldo"] = total
        loc["a_favor"] = -total if total < -TOLERANCIA else 0.0
        if nombre in REGLAS:
            con_regla.append((nombre, loc))
            continue
        ch = (chequeos or {}).get(nombre)
        if ch and ch["saldo_pestana"] is not None and \
                abs(ch["saldo_pestana"] - ch["neto"]) > 1:
            sin_dato.append((nombre, f"la cadena de saldo de la pestaña da "
                             f"${ch['saldo_pestana']:,.2f} y los movimientos ${ch['neto']:,.2f}"))
            continue
        up = max([p for p in (loc["ultimo_periodo"], (ch or {}).get("ultimo_periodo")) if p],
                 default=None)
        if up is None or meses_de_diferencia(up, corriente) > ATRASO_MAX:
            sin_dato.append((nombre, "fuente atrasada: último período cargado "
                             + (f"{up[0]}-{up[1]:02d}" if up else "ninguno")))
            continue
        (deudores if loc["exigible"] > 0 else al_dia).append((nombre, loc))
    return deudores, al_dia, con_regla, sin_dato


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    xlsx, mes = sys.argv[1], sys.argv[2]
    try:
        anio, num = (int(x) for x in mes.split("-"))
        corriente = (anio, num)
    except ValueError:
        sys.exit(f"El mes va como AAAA-MM, no {mes!r}.")
    if not 1 <= num <= 12:
        sys.exit(f"Mes imposible: {mes!r}.")

    movs, chequeos = leer_xlsx(xlsx)
    deudores, al_dia, con_regla, sin_dato = clasificar(movs, corriente, chequeos)

    print(f"RADAR DE DEUDORES — corte {mes} · fuente: pestañas por local de Ctas Ctes "
          f"({len(movs)} movimientos)\n"
          f"(exigible = bloques de meses anteriores − todos los pagos; "
          f"bloque del mes = alquiler {mes} + expensas del mes anterior)\n")

    if sin_dato:
        print("⚠ SIN DATO CONFIABLE (no se informa su deuda)")
        for nombre, motivo in sin_dato:
            print(f"  {nombre:<16} {motivo}")
        print()

    if deudores:
        print("DEBEN (exigible hoy)")
        for nombre, loc in sorted(deudores, key=lambda x: -x[1]["exigible"]):
            banco = "  ⚠ paga por banco: puede haber pagos en tránsito hasta el extracto" \
                if nombre in PAGAN_POR_BANCO else ""
            print(f"  {nombre:<16} ${loc['exigible']:>14,.2f}"
                  f"   + bloque {mes} en curso: ${loc['en_curso']:,.2f}{banco}")
        print(f"\n  Total exigible: ${sum(l['exigible'] for _, l in deudores):,.2f}\n")
    else:
        print(("Del resto, nadie" if sin_dato else "Nadie") + " debe nada exigible.\n")

    if al_dia:
        print("AL DÍA")
        for nombre, loc in al_dia:
            extra = f" (a favor ${loc['a_favor']:,.2f})" if loc["a_favor"] else ""
            extra += f" (residuo de redondeo ${loc['residuo']:,.2f})" if loc["residuo"] else ""
            etiqueta = "ya corriendo" if nombre in PAGAN_ADELANTADO else "en curso"
            print(f"  {nombre:<16} ok{extra}   bloque {mes} {etiqueta}: "
                  f"${loc['en_curso']:,.2f} (pagó ${loc['corriente_pagos']:,.2f} este mes)")
        print()

    if con_regla:
        print("CON REGLA PROPIA (el saldo acá NO es deuda)")
        for nombre, loc in con_regla:
            print(f"  {nombre:<18} saldo ${loc['saldo']:,.2f} — {REGLAS[nombre]}")
        print()

    print("CHEQUEO: saldo de la pestaña vs. cargos − pagos")
    for tab, ch in chequeos.items():
        ok = ch["saldo_pestana"] is not None and abs(ch["saldo_pestana"] - ch["neto"]) <= 1
        print(f"  {'✓' if ok else '✕'} {tab:<16} pestaña ${ch['saldo_pestana'] or 0:,.2f} · "
              f"movimientos ${ch['neto']:,.2f}")


if __name__ == "__main__":
    main()
