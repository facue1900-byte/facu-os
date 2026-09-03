#!/usr/bin/env python3
"""
¿La expensa de un mes se puede reconstruir desde sus inputs?

Facu, 02/09/2026: *"cuando yo cambie la fecha arriba de todo, ¿aparece el mismo
número que armaste vos?"*. Esto lo contesta mes por mes.

    verificar_expensas.py                 # todos los meses de EXPENSAS HISTORICO
    verificar_expensas.py 2026-08

**No toca ninguna planilla.** La primera versión copiaba el Master Plan y le
cambiaba la fecha, pero el scope de Drive es `readonly` a propósito
(`google_auth.py`) y ensancharlo para esto sería sacar un candado por comodidad.
Además cambiarle `A3` a una hoja viva y compartida, aunque sean diez segundos,
le mueve los números a cualquiera que la esté mirando — y si el script se corta
a la mitad, queda así.

Así que el reparto se replica en Python, que es lo que la hoja hace de verdad:

    recupero(local)  = AVN·%AE + Agua·%AF + ABL·%AG
    servicios(local) = Utilidades·%AJ + Administrativos·%AK + LimpBaños·%AL
                     + LimpInsumos·%AM + LimpPredio·%AN + Mantenimiento·%AO
                     + Jardinería·%AP + Fumigación·%AQ + Comunicación·%AR
                     + Basura·%AS

Los porcentajes salen de la hoja (`AE:AS`, filas 7-29). Los inputs salen de
`INPUTS EXPENSAS`, un renglón por mes. **Peak One paga la MITAD de
Mantenimiento** — es la única fila con `/2` en la planilla, y se replica.

Un input en blanco no se toma como 0: el mes se reporta como **no
reconstruible** y se dice qué factura falta. Un 0 se reparte entre los locales y
sale una expensa más barata sin que nadie se entere; es la falla que facturó
$875.691,52 de menos en julio.
"""

import sys
import datetime

sys.path.insert(0, "/Users/Facu/facu-os/execution")
from google_auth import sheets  # noqa: E402

MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
TOL = 0.01

# concepto -> (columna del input en la fila 4, columna del % por local)
# El orden es el de la hoja: primero los 3 del recupero, después los 10 de
# servicios comunes.
RECUPERO = [("Expensas AVN", "B", "AE"), ("Agua R&S", "C", "AF"),
            ("ABL (Municipal)", "D", "AG")]
SERVICIOS = [("Utilidades", "G", "AJ"), ("Administrativos", "H", "AK"),
             ("Limpieza Baños", "I", "AL"), ("Limpieza e Insumos", "J", "AM"),
             ("Limpieza Predio", "K", "AN"), ("Mantenimiento", "L", "AO"),
             ("Jardineria", "M", "AP"), ("Fumigacion", "N", "AQ"),
             ("Comunicación", "O", "AR"), ("Retiro de basura", "P", "AS")]
# Única excepción de la planilla: Peak One paga la mitad del Mantenimiento.
MITAD = {("Peak One", "Mantenimiento")}


def col_idx(letras):
    n = 0
    for c in letras:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def desde_serial(n):
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=float(n))


def plata(x):
    return f"${x:,.2f}"


def num(x):
    """None si la celda está en blanco. 0 sólo si dice 0."""
    if x is None or (isinstance(x, str) and not x.strip()):
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def porcentajes(s):
    """{local: {concepto: %}} desde AE:AS de Expensas Predio."""
    g = s.spreadsheets().values().get(
        spreadsheetId=MASTER_PLAN, range="'Expensas Predio'!A7:AS29",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    base = col_idx("A")
    out = {}
    for fila in g:
        fila = list(fila) + [""] * (col_idx("AS") + 1)
        loc = str(fila[0]).strip()
        if not loc:
            continue
        out[loc] = {c: (num(fila[col_idx(pc) - base]) or 0.0)
                    for c, _, pc in RECUPERO + SERVICIOS}
    return out


def inputs_por_mes(s):
    """{'AAAA-MM': {concepto: valor o None}} desde INPUTS EXPENSAS."""
    v = s.spreadsheets().values().get(
        spreadsheetId=MASTER_PLAN, range="'INPUTS EXPENSAS'!A1:P40",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    # La fila de encabezados se BUSCA en vez de hardcodearse: la hoja tiene
    # arriba un título y una leyenda, y si alguien agrega un renglón de texto
    # un índice fijo lee la fila equivocada y no falla, sólo da otra cosa.
    hdr = None
    for i, fila in enumerate(v):
        if fila and str(fila[0]).strip() == "Período":
            hdr = [str(x).strip() for x in fila]
            v = v[i:]
            break
    if hdr is None:
        sys.exit("No encontré la fila de encabezados ('Período') en INPUTS EXPENSAS.")
    out = {}
    for fila in v[1:]:
        fila = list(fila) + [""] * len(hdr)
        # La tabla de meses termina donde arranca el bloque de reparto por
        # local: la primera fila cuyo período no es una fecha corta la lectura.
        if num(fila[0]) is None:
            break
        f = desde_serial(fila[0])
        out[f"{f.year}-{f.month:02d}"] = {
            c: num(fila[hdr.index(c)]) for c, _, _ in RECUPERO + SERVICIOS
            if c in hdr}
    return out


def cobrado(s):
    """{(mes, local): (recupero, servicios)} de lo que YA se le cobró."""
    filas = s.spreadsheets().values().get(
        spreadsheetId=CTAS, range="'EXPENSAS HISTORICO'!A2:E500",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])
    out = {}
    for r in filas:
        r = list(r) + [""] * 5
        if not r[0] or not r[1]:
            continue
        f = desde_serial(r[0])
        out[(f"{f.year}-{f.month:02d}", str(r[1]).strip())] = (
            num(r[2]) or 0.0, num(r[3]) or 0.0)
    return out


def repartir(inp, pct):
    """{local: (recupero, servicios)} — el mismo producto que hace la hoja."""
    out = {}
    for loc, p in pct.items():
        rec = sum(inp[c] * p[c] for c, _, _ in RECUPERO)
        ser = sum(inp[c] * p[c] / (2 if (loc, c) in MITAD else 1)
                  for c, _, _ in SERVICIOS)
        out[loc] = (round(rec, 2), round(ser, 2))
    return out


def main():
    pedidos = sys.argv[1:]
    s = sheets()
    pct, inputs, real = porcentajes(s), inputs_por_mes(s), cobrado(s)

    meses = sorted({m for m, _ in real})
    if pedidos:
        meses = [m for m in meses if m in pedidos]
    if not meses:
        sys.exit("No hay meses para comparar en EXPENSAS HISTORICO.")

    fallados = []
    for mes in meses:
        inp = inputs.get(mes)
        if inp is None:
            fallados.append(mes)
            print(f"✗ {mes} — no tiene renglón en INPUTS EXPENSAS.\n")
            continue
        faltan = [c for c, v in inp.items() if v is None]
        if faltan:
            fallados.append(mes)
            print(f"✗ {mes} — NO se puede reconstruir: falta el input de "
                  f"{', '.join(faltan)}. Conseguí esa(s) factura(s) y cargala "
                  f"en INPUTS EXPENSAS.\n")
            continue

        calc = repartir(inp, pct)
        esperados = {l: v for (m, l), v in real.items() if m == mes}
        difs = []
        for loc, (rec_ok, ser_ok) in sorted(esperados.items()):
            if loc not in calc:
                difs.append((loc, None, None, rec_ok, ser_ok))
                continue
            rec, ser = calc[loc]
            if abs(rec - rec_ok) > TOL or abs(ser - ser_ok) > TOL:
                difs.append((loc, rec, ser, rec_ok, ser_ok))

        t_calc = sum(a + b for l, (a, b) in calc.items() if l in esperados)
        t_real = sum(a + b for a, b in esperados.values())
        if not difs:
            print(f"✓ {mes} — los {len(esperados)} locales reproducen al "
                  f"centavo ({plata(t_real)})")
            continue

        fallados.append(mes)
        print(f"✗ {mes} — {len(difs)} de {len(esperados)} locales no "
              f"reproducen.")
        print(f"    total desde los inputs {plata(t_calc)} · se cobró "
              f"{plata(t_real)} · diferencia {plata(t_calc - t_real)}")
        print(f"    {'local':<20}{'recupero calc':>16}{'cobrado':>16}"
              f"{'servicios calc':>17}{'cobrado':>16}")
        for loc, rec, ser, rec_ok, ser_ok in difs:
            if rec is None:
                print(f"    {loc:<20} no está en la grilla de Expensas Predio")
                continue
            print(f"    {loc:<20}{plata(rec):>16}{plata(rec_ok):>16}"
                  f"{plata(ser):>17}{plata(ser_ok):>16}")
        print()

    if fallados:
        sys.exit(f"\n{len(fallados)} de {len(meses)} meses NO se reconstruyen: "
                 f"{', '.join(fallados)}. Mientras sea así, el historial de "
                 f"expensas no se puede auditar.")
    print(f"\nLos {len(meses)} meses se reconstruyen al centavo desde sus inputs.")


if __name__ == "__main__":
    main()
