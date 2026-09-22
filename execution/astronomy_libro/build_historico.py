"""Libro histórico de Astronomy: todos los movimientos de ene-2023 al corte de la web
(25/07/2026), fila por fila, con su caja, su clase y su cierre.

Reemplaza la planilla vieja que la web leía en vivo (`Finanzas - Astronomy Academy`,
hoja Base): esa planilla no tenía ninguna de las correcciones de los cierres que se
hicieron con Vlado el 22/09/2026 (ficticios, cajas, pases, aportes, retiros).

Fuentes (todas congeladas; son historia):
  - "Revisión 22-09" del sheet `Astronomy - Finanzas` (la planilla general "Base",
    clasificada fila por fila con Facu). Se lee EN VIVO: la columna CLASE FINAL es la
    que Facu corrige.
  - Las planillas de cada unidad (Academy, Dominé, Talent), snapshot del 22/09/2026 en
    `archive/cierres-astronomy-2026-09-22/unidades.json`.

Criterios: los de `archive/cierres-astronomy-2026-09-22/` (c2v2.py, c3.py), que son los
que dieron los números aprobados. Este script NO termina si un total no da igual al
resumen (`RESUMEN 2023-2026` y las pestañas Cierre 2/3/4): un libro que no reproduce los
cierres es un libro que miente.

Uso:
  .venv/bin/python execution/astronomy_libro/build_historico.py  → escribe historico.json
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
ARCH = AQUI.parents[1] / "archive" / "cierres-astronomy-2026-09-22"
sys.path.insert(0, str(AQUI.parents[0]))

SHEET = "1Rczor21G1sttkQJU2CsiFi88SiW6EKVauY4sOs_JRN8"
CORTE_WEB = "2026-07-25"  # CUTOVER_ISO de la web: 25/07/2026 00:00 AR

# unidad → caja/unidad de la web (UnidadId): la caja maestra ("Astronomy General") es "empresa".
UNIDAD = {"Academy": "academy", "Dominé": "domine", "Talent": "label", "General": "empresa",
          "Astronomy Academy": "academy", "Astronomy Dominé": "domine", "Astronomy Talent": "label",
          "Astronomy General": "empresa", "Socios": "empresa"}


def fila(**k):
    """Un movimiento. `ars`/`usd` van CON signo desde el punto de vista del negocio:
    + entra, − sale. `caja` es de qué caja salió o entró la plata (None = la puso o la
    cobró un socio de su bolsillo, no pasó por ninguna caja). `operativo` dice si cuenta
    en el resultado del negocio."""
    base = dict(persona="", categoria="", concepto="", caja=None, operativo=False, nota="")
    base.update(k)
    return base


# ── fuentes ──────────────────────────────────────────────────────────────────
def leer_revision():
    from google_auth import sheets
    v = sheets().spreadsheets().values().get(
        spreadsheetId=SHEET, range="'Revisión 22-09'!A1:Q", valueRenderOption="UNFORMATTED_VALUE"
    ).execute()["values"]
    h = v[0]
    out = []
    for i, r in enumerate(v[1:]):
        r = r + [""] * (len(h) - len(r))
        d = dict(zip(h, r))
        d["fecha"] = (dt.date(1899, 12, 30) + dt.timedelta(days=int(d["Fecha"]))).isoformat() \
            if isinstance(d["Fecha"], (int, float)) else str(d["Fecha"])[:10]
        d["fila"] = i + 2  # misma numeración que Base (ordenada por timestamp) y que c2v2
        out.append(d)
    return out


def leer_unidades():
    """Las planillas de Academy/Dominé/Talent, con el arreglo de fechas de unid.py."""
    U = json.load(open(ARCH / "unidades.json"))
    B = dt.date(1899, 12, 30)
    todate = lambda t: B + dt.timedelta(days=int(t)) if isinstance(t, (int, float)) and t > 0 else None
    out = {}
    for u in U.values():
        name = u["title"].replace("Finanzas - Astronomy ", "")
        h = u["values"][0]
        rows = [r + [""] * (len(h) - len(r)) for r in u["values"][1:]]
        ix = {k: h.index(k) for k in h if k}
        L = []
        for n, r in enumerate(rows, start=2):
            ts = todate(r[ix["Timestamp"]]); rd = todate(r[ix["Real Date"]])
            f = rd
            if rd is None:
                f = ts
            elif rd.day <= 12:
                try:
                    sw = rd.replace(day=rd.month, month=rd.day)
                except ValueError:
                    sw = None
                if sw and ts and sw <= ts + dt.timedelta(days=3) and abs((ts - sw).days) < abs((ts - rd).days):
                    f = sw
            L.append(dict(unidad=name, fila=n, fecha=f.isoformat(), tipo=str(r[ix["Category"]]).strip(),
                          sub=str(r[ix["Sub Category"]]).strip(), ars=float(r[ix["ARS_Ammount"]] or 0),
                          usd=float(r[ix["USD_Ammount"]] or 0), desc=str(r[ix["Descripción"]]).strip()))
        out[name] = L
    return out


# ── cierre 1: ene-2023 → 31/05/2024. No había caja: pagaban y cobraban los socios ──
CLASE_REV = {"Venta": "venta", "Costo": "costo", "Inversión": "inversion", "Pase entre cajas": "pase",
             "Retiro de socios": "retiro", "Aporte de socios": "aporte", "Ajuste (no es plata)": "ajuste",
             "No existió (ficticio)": "ficticio"}


def cierre1(rev):
    out = []
    for d in rev:
        if d["fecha"] > "2024-05-31":
            continue
        cl = CLASE_REV[d["CLASE FINAL"]]
        out.append(fila(cierre=1, fecha=d["fecha"], unidad=UNIDAD[d["Caja"]], clase=cl,
                        categoria=d["CATEGORÍA FINAL"], concepto=str(d["Descripción"] or d["Categoría (planilla)"]),
                        persona=d["Quién pagó/cobró"], ars=float(d["ARS con signo"] or 0), usd=float(d["USD con signo"] or 0),
                        operativo=cl in ("venta", "costo"), fuente=f"Base fila {d['fila']}"))
    return out


# ── cierre 2: 01/06/2024 → 10/04/2025. Caja maestra + Academy, Dominé, Talent ──
FIC_COSTO = {"Academy": {323, 324, 325, 328, 349, 350, 354, 382, 383}, "Dominé": {91, 92, 101}, "Talent": {13, 17, 32}}
FIC_APORTE = {"Academy": {371, 418, 419}, "Dominé": {90, 103}, "Talent": {12, 39}}
BASE_FIC_PAR = {330, 332}


def clase_unidad(x):  # c2.py
    s = x["sub"].lower(); d = x["desc"].lower()
    if x["tipo"] == "Egreso" and s.startswith("retiro de ganancia"): return "a maestra"
    if x["tipo"] == "Ingreso" and s == "aporte de capital": return "de maestra"
    if x["tipo"] == "Ingreso" and "aporte de capital" in d: return "de maestra"
    if "devolucion facu" in d: return "devuelve aporte a Facu"
    if "seña" in d and "domos" in d: return "seña domos"
    if x["tipo"] == "Ingreso": return "venta"
    return "costo"


def cierre2(rev, U):
    out = []
    I, F = "2024-06-01", "2025-04-10"
    sg = lambda x: 1 if x["tipo"] == "Ingreso" else -1
    # apertura de Academy: lo neto de su planilla antes del 01/06/2024 (c2v2)
    pre = [x for x in U["Academy"] if x["fecha"] < I]
    out.append(fila(cierre=2, fecha=I, unidad="academy", caja="academy", clase="ajuste",
                    categoria="Saldo inicial", concepto="Saldo de la planilla de Academy al 31/05/2024",
                    ars=sum(sg(x) * x["ars"] for x in pre), usd=sum(sg(x) * x["usd"] for x in pre),
                    fuente=f"planilla Academy, {len(pre)} filas antes del 01/06/2024"))
    dev_facu = None
    for u, L in U.items():
        uid = UNIDAD[u]
        for x in L:
            if not (I <= x["fecha"] <= F):
                continue
            c = clase_unidad(x); s = sg(x)
            base = dict(cierre=2, fecha=x["fecha"], unidad=uid, caja=uid, concepto=x["desc"] or x["sub"],
                        ars=s * x["ars"], usd=s * x["usd"], fuente=f"planilla {u} fila {x['fila']}")
            if x["fila"] in FIC_COSTO[u]:
                out.append(fila(**base, clase="pase", categoria="Gasto ficticio: pase a la caja maestra",
                                nota="Anotado como alquiler/expensas/luz, pero ese gasto nunca existió: la plata fue a la maestra"))
            elif x["fila"] in FIC_APORTE[u]:
                out.append(fila(**base, clase="pase", categoria="Llega de la caja maestra (para un gasto ficticio)"))
            elif c == "venta":
                out.append(fila(**base, clase="venta", categoria=x["sub"], operativo=True))
            elif c == "costo":
                out.append(fila(**base, clase="costo", categoria=x["sub"], operativo=True))
            elif c == "seña domos":
                out.append(fila(**base, clase="costo" if s < 0 else "venta", categoria="Seña de los domos", operativo=True))
            elif c == "devuelve aporte a Facu":
                out.append(fila(**base, clase="retiro", categoria="Devolución de aporte a Facu", persona="Facu"))
                dev_facu = x
            elif c == "a maestra":
                out.append(fila(**base, clase="pase", categoria="Pase a la caja maestra"))
            elif c == "de maestra":
                out.append(fila(**base, clase="pase", categoria="Llega de la caja maestra"))
    # Cierre 2 v2 (Facu 22/09): Facu puso $530.000 de su bolsillo para la seña de los domos.
    # Es costo de Dominé y aporte de Facu; no pasó por ninguna caja.
    assert dev_facu is not None
    out.append(fila(cierre=2, fecha=dev_facu["fecha"], unidad="domine", caja=None, clase="costo", operativo=True,
                    categoria="Seña de los domos", concepto="Parte de la seña de los domos que pagó Facu de su bolsillo",
                    persona="Facu", ars=-dev_facu["ars"], usd=-dev_facu["usd"], fuente="Cierre 2 v2 (Facu, 22/09/2026)"))

    # lado caja maestra: filas de Base desde la 255 (c2m.py + c2v2.py)
    UNM = {"Astronomy Academy": "Academy", "Astronomy Dominé": "Dominé", "Astronomy Talent": "Talent"}
    X = json.load(open(ARCH / "c2m.json"))
    par = {x["fila"]: x.get("par") for x in X["mb"]}
    for d in rev:
        if d["fila"] < 255:
            continue
        bu = d["Caja"]; per = d["Quién pagó/cobró"]; cl = d["CLASE FINAL"]; desc = str(d["Descripción"])
        tipo = d["Tipo (planilla)"]; sub = d["Categoría (planilla)"]
        s = 1 if tipo == "Ingreso" else -1
        a, u_ = abs(float(d["ARS"] or 0)), abs(float(d["USD"] or 0))
        base = dict(cierre=2, fecha=d["fecha"], caja="empresa", concepto=desc or sub, persona=per,
                    ars=s * a, usd=s * u_, fuente=f"Base fila {d['fila']}")
        f = d["fila"]
        if cl == "No existió (ficticio)":
            out.append(fila(**base, unidad="empresa", clase="pase", categoria="Gastos ficticios recibidos de las unidades"))
            continue
        if str(bu).startswith("Socios"): continue                                          # espejo del socio
        if per != "Astronomy" and sub == "Aporte de Capital": continue                    # espejo del aporte
        if per != "Astronomy" and "consola" in desc.lower():                              # retiro consola
            out.append(fila(**dict(base, ars=-a, usd=-u_, concepto=f"Venta de la consola: u$s 100 para {per}"),
                            unidad="empresa", clase="retiro", categoria="Retiro de socios"))
            continue
        if cl == "Retiro de socios":
            if f == 311:
                out.append(fila(**dict(base, ars=-a, usd=-u_), unidad="domine", clase="pase", categoria="Pase a Dominé",
                                nota="$530.000 a Dominé, que se los devuelve a Facu"))
            else:
                out.append(fila(**dict(base, ars=-a, usd=-u_), unidad="empresa", clase="retiro", categoria="Retiro de socios"))
            continue
        if bu in UNM:
            u = "Dominé" if f == 381 else UNM[bu]
            uid = UNIDAD[u]
            if f in BASE_FIC_PAR or f == 302:
                continue
            if par.get(f) or f in (289, 381):
                out.append(fila(**base, unidad=uid, clase="pase",
                                categoria=("Llega de " if s > 0 else "Pase a ") + u))
            elif cl == "Inversión":
                out.append(fila(**base, unidad=uid, clase="inversion", categoria=d["CATEGORÍA FINAL"],
                                nota=f"La pagó la caja maestra para {u}"))
            elif cl in ("Venta", "Costo"):
                out.append(fila(**base, unidad=uid, clase=cl.lower(), categoria=d["CATEGORÍA FINAL"], operativo=True,
                                nota=f"Cobrado/pagado directo por la caja maestra para {u}"))
            continue
        # maestra propia
        if f in (382, 384):
            out.append(fila(**base, unidad="empresa", clase="aporte", categoria="Aporte de socios"))
        elif cl == "Inversión":
            out.append(fila(**base, unidad="empresa", clase="inversion", categoria=d["CATEGORÍA FINAL"]))
        elif cl.startswith("Ajuste"):
            out.append(fila(**base, unidad="empresa", clase="ajuste", categoria=d["CATEGORÍA FINAL"], operativo=True))
        else:
            out.append(fila(**base, unidad="empresa", clase="costo", categoria=d["CATEGORÍA FINAL"], operativo=True))
    # consola: Academy le pasó a la maestra la venta de la consola (Academy fila 105)
    ac = [x for x in U["Academy"] if x["fila"] == 105][0]
    out.append(fila(cierre=2, fecha=ac["fecha"], unidad="academy", caja="empresa", clase="pase",
                    categoria="Llega de Academy", concepto=ac["desc"], ars=ac["ars"], usd=ac["usd"],
                    fuente="planilla Academy fila 105 (contracara en la maestra)"))
    # La caja maestra cerró el cierre 2 en −$52.371 y desde el 11/04/2025 no se usó más: la
    # cadena de caja del resumen ($959.909 al 22/09/2026) sigue sólo con Academy. Se lleva a
    # cero con un ajuste a la vista, para que el total del libro sea el de los cierres.
    saldo_m = sum(r["ars"] for r in out if r["caja"] == "empresa")
    saldo_mu = sum(r["usd"] for r in out if r["caja"] == "empresa")
    out.append(fila(cierre=2, fecha="2025-04-10", unidad="empresa", caja="empresa", clase="ajuste",
                    categoria="Cierre de la caja maestra", concepto="La caja maestra se cierra y se lleva a cero",
                    ars=-saldo_m, usd=-saldo_mu, fuente="Cierre 2 (22/09/2026)",
                    nota=f"Cerró en ${saldo_m:,.0f} y no siguió: diferencia no explicada del cierre 2"))
    return out


# ── cierre 3: 11/04/2025 → 30/06/2026. Una sola caja: Academy ──
def cierre3(U, desde="2025-04-11", hasta="2026-06-30", cierre=3):
    out = []
    for x in U["Academy"]:
        if not (desde <= x["fecha"] <= hasta):
            continue
        s = 1 if x["tipo"] == "Ingreso" else -1
        base = dict(cierre=cierre, fecha=x["fecha"], caja="academy", concepto=x["desc"] or x["sub"],
                    ars=s * x["ars"], usd=s * x["usd"], fuente=f"planilla Academy fila {x['fila']}")
        f = x["fila"]
        if cierre == 3 and f == 597:
            out.append(fila(**base, unidad="academy", clase="aporte", categoria="Aporte de socios",
                            persona="Facu, Jaime y Vlado", nota="$300.000 cada uno"))
        elif cierre == 3 and f == 877:
            out.append(fila(**base, unidad="domine", clase="venta", categoria="Resultado de Dominé", operativo=True,
                            nota="Lo que ganó Dominé y le mandó a Academy"))
        elif cierre == 3 and f in (512, 602):
            out.append(fila(**base, unidad="domine", clase="venta", categoria="Eventos (Creta)", operativo=True))
        elif cierre == 3 and f == 612:
            out.append(fila(**dict(base, concepto=(x["desc"] or "") + " (cables/parlantes domos)"),
                            unidad="domine", clase="inversion", categoria="Equipos"))
        elif s > 0:
            out.append(fila(**base, unidad="academy", clase="venta", categoria=x["sub"], operativo=True))
        else:
            out.append(fila(**base, unidad="academy", clase="costo", categoria=x["sub"], operativo=True))
    return out


# ── verificación contra los cierres aprobados ────────────────────────────────
def suma(rows, cond, k="ars"):
    return sum(r[k] for r in rows if cond(r))


def verificar(C1, C2, C3):
    errs = []
    def eq(nombre, got, want, tol=1.0):
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'MAL'} {nombre}: {got:,.2f} (resumen {want:,.2f})")
        if not ok: errs.append(nombre)
    print("Cierre 1")
    eq("resultado $", suma(C1, lambda r: r["operativo"]), 1341938)
    eq("resultado USD", suma(C1, lambda r: r["operativo"], "usd"), 1072, 1)
    eq("inversión $", -suma(C1, lambda r: r["clase"] == "inversion"), 5509675)
    print("Cierre 2")
    for u, want in (("academy", 5080398), ("domine", -733925), ("label", 1490853), ("empresa", -124162)):
        eq(f"resultado {u} $", suma(C2, lambda r: r["operativo"] and r["unidad"] == u), want)
    eq("resultado total $", suma(C2, lambda r: r["operativo"]), 5713164)
    eq("resultado USD", suma(C2, lambda r: r["operativo"], "usd"), 4895, 2)
    eq("inversión $", -suma(C2, lambda r: r["clase"] == "inversion"), 3702018)
    for c, want in (("academy", 605), ("domine", 0), ("label", 0), ("empresa", 0)):
        eq(f"caja {c} al 10/04/2025", suma(C2, lambda r: r["caja"] == c), want, 2)
    print("Cierre 3")
    eq("resultado $", suma(C3, lambda r: r["operativo"]), -1871079)
    eq("inversión $", -suma(C3, lambda r: r["clase"] == "inversion"), 60000)
    eq("aporte $", suma(C3, lambda r: r["clase"] == "aporte"), 900000)
    # el resumen sumó componentes ya redondeados al peso: $1,18 de diferencia es redondeo
    eq("caja academy al 30/06/2026", suma(C2 + C3, lambda r: r["caja"] == "academy"), -1030473, 2)
    return errs


if __name__ == "__main__":
    rev = leer_revision()
    assert len(rev) == 383, f"Revisión 22-09 tiene {len(rev)} filas, se esperaban 383"
    U = leer_unidades()
    C1, C2, C3 = cierre1(rev), cierre2(rev, U), cierre3(U)
    # Cierre 4, la parte de julio anterior al corte de la web: los ingresos de la planilla y
    # sus dos gastos que la web no tiene (Balance $116.520 y Bot $76.000). El resto de los
    # gastos de julio ya está cargado en la web: traerlos de la planilla los contaría dos veces.
    C4 = cierre3(U, "2026-07-01", "2026-07-24", cierre=4)
    errs = verificar(C1, C2, C3)
    print("Cierre 4 (julio, antes del corte)")
    ing = suma(C4, lambda r: r["ars"] > 0); egr = -suma(C4, lambda r: r["ars"] < 0)
    print(f"  ingresos planilla {ing:,.2f} · egresos planilla {egr:,.2f}")
    if abs(egr - 192520) > 0.5:
        errs.append("julio: los egresos de la planilla no son los dos del cierre 4")
    if errs:
        sys.exit(f"NO CIERRA: {errs}. No se escribe nada.")
    todo = C1 + C2 + C3 + C4
    for r in todo:
        r["ars"] = round(r["ars"], 2); r["usd"] = round(r["usd"], 2)
    json.dump(todo, open(AQUI / "historico.json", "w"), ensure_ascii=False, indent=0)
    print("TODO CIERRA ·", len(todo), "movimientos →", AQUI / "historico.json")
