#!/usr/bin/env python3
"""Consolida las existencias leidas de SIGSA y arma el mensaje para mandar.

Uso:
    consolidar_stock.py <json de la tanda> [--planilla <stock_ganadero.xlsx>]

Hace tres cosas:
  1. Tabla de bovinos por campo, con totales por categoria.
  2. Diferencias contra la planilla historica (que categoria se movio y cuanto).
  3. El texto listo para WhatsApp. NO manda nada: se imprime y se frena.
"""
import argparse
import json
import pathlib
import sys

CATEGORIAS = ["Vaca", "Toro", "Novillo", "Novillito", "Vaquillona",
              "Ternera", "Ternero", "Torito/MEJ"]

# Como se llama cada campo en la planilla historica
ALIAS_PLANILLA = {
    "Fortin Cocherek": "Fortin Cocherek",
    "Cañada Rica": "Cañada Rica",
}


def cargar_tanda(ruta):
    datos = json.loads(pathlib.Path(ruta).read_text(encoding="utf-8"))
    for c in datos["campos"]:
        faltan = [k for k in c["bovinos"] if k not in CATEGORIAS]
        if faltan:
            sys.exit(f"ERROR: categoria desconocida en {c['campo']}: {faltan}")
    return datos


def cargar_planilla(ruta):
    import openpyxl
    ws = openpyxl.load_workbook(ruta, data_only=True).active
    filas = [r for r in ws.iter_rows(values_only=True) if r and r[0]]
    encabezado = next(r for r in filas if r[0] == "Campo")
    cols = {nombre: i for i, nombre in enumerate(encabezado) if nombre}
    out = {}
    for r in filas:
        if r[0] in ("Campo", "TOTAL GENERAL") or r[0] == encabezado[0]:
            continue
        if r[0].startswith("STOCK GANADERO"):
            continue
        out[r[0]] = {cat: (r[cols[cat]] if isinstance(r[cols[cat]], int) else 0)
                     for cat in CATEGORIAS if cat in cols}
    return out


def n(v):
    return 0 if v in (None, "-", "") else int(v)


def total_campo(bov):
    return sum(n(v) for v in bov.values())


def tabla(datos):
    filas = []
    anchos = [max(12, max(len(c["campo"]) for c in datos["campos"]))]
    hdr = ["Campo"] + CATEGORIAS + ["TOTAL"]
    for c in datos["campos"]:
        filas.append([c["campo"]] +
                     [n(c["bovinos"].get(cat)) for cat in CATEGORIAS] +
                     [total_campo(c["bovinos"])])
    tot = ["TOTAL"] + [sum(f[i] for f in filas) for i in range(1, len(hdr))]
    filas.append(tot)
    anchos = [max(len(str(r[i])) for r in [hdr] + filas) for i in range(len(hdr))]
    def linea(r):
        return "  ".join(str(v).rjust(anchos[i]) if i else str(v).ljust(anchos[0])
                         for i, v in enumerate(r))
    return "\n".join([linea(hdr), "-" * (sum(anchos) + 2 * len(anchos))] +
                     [linea(f) for f in filas])


def diferencias(datos, planilla):
    out = []
    for c in datos["campos"]:
        base = planilla.get(c["campo"])
        if base is None:
            out.append((c["campo"], None, []))
            continue
        difs = []
        for cat in CATEGORIAS:
            hoy, antes = n(c["bovinos"].get(cat)), n(base.get(cat))
            if hoy != antes:
                difs.append((cat, antes, hoy, hoy - antes))
        out.append((c["campo"], base, difs))
    return out


def mensaje(datos, faltantes):
    fecha = datos["fecha"]
    dd = "/".join(reversed(fecha.split("-")))
    lineas = [f"Existencias al {dd} (SIGSA, stock declarado)", ""]
    for c in datos["campos"]:
        det = ", ".join(f"{cat.lower()} {n(c['bovinos'].get(cat))}"
                        for cat in CATEGORIAS if n(c["bovinos"].get(cat)))
        lineas.append(f"*{c['establecimiento']}* — {total_campo(c['bovinos'])} bovinos")
        lineas.append(f"  {det}")
    total = sum(total_campo(c["bovinos"]) for c in datos["campos"])
    lineas += ["", f"Total de los {len(datos['campos'])} campos: {total} bovinos"]
    if faltantes:
        lineas.append(f"(faltan: {', '.join(faltantes)})")
    return "\n".join(lineas)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("json")
    p.add_argument("--planilla",
                   default="/Users/Facu/Desktop/Chaco/stock_ganadero.xlsx")
    args = p.parse_args()

    datos = cargar_tanda(args.json)
    planilla = cargar_planilla(args.planilla)

    leidos = {c["campo"] for c in datos["campos"]}
    faltantes = [k for k in planilla if k not in leidos]

    print("=" * 70)
    print(f"EXISTENCIAS SIGSA al {datos['fecha']} — {len(leidos)} de "
          f"{len(planilla)} campos leidos")
    print("=" * 70)
    print(tabla(datos))

    print("\n" + "=" * 70)
    print("CONTRA LA PLANILLA (stock_ganadero.xlsx)")
    print("=" * 70)
    for campo, base, difs in diferencias(datos, planilla):
        if base is None:
            print(f"{campo}: NO esta en la planilla — revisar el nombre")
        elif not difs:
            print(f"{campo}: coincide exacto")
        else:
            for cat, antes, hoy, d in difs:
                print(f"{campo}: {cat} {antes} -> {hoy} ({d:+d})")

    if faltantes:
        print("\nFALTA LEER EN SIGSA: " + ", ".join(sorted(faltantes)))

    print("\n" + "=" * 70)
    print("MENSAJE (no se manda: copiar y pegar despues del OK de Facu)")
    print("=" * 70)
    print(mensaje(datos, sorted(faltantes)))


if __name__ == "__main__":
    main()
