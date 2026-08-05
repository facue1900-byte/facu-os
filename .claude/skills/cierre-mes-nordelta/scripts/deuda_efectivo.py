#!/usr/bin/env python3
"""
Cuánto debe EN EFECTIVO cada local — lo único que Mati puede ir a cobrar.

    deuda_efectivo.py [salida.json]

**No es el saldo.** El saldo mezcla lo que se cobra por banco con lo que se cobra
en mano: Fabric paga todo por banco y nunca le debe efectivo a Mati, y Bigg va
partido — sólo la «Diferencia Alquiler (sin iva)» es efectivo.

**Tampoco es todo deuda.** Todos pagan el mes siguiente al que se les cobra, así
que siempre hay un bloque en la calle que **no está vencido**. Se separa:
  · `delMes`  → el bloque que se está cobrando ahora
  · `vencido` → lo que quedó de antes (negativo = saldo a favor)
El corte es la **última fila de pago** de cada pestaña: lo que hay debajo es el
bloque corriente. No hace falta hardcodear filas ni fechas.

Fuentes, según el local:
  · con pestaña → se camina la pestaña, que es la que Facu verificó y la que ve
    el locatario. Cargos y pagos se clasifican por medio.
  · sin pestaña (Salón, La Jaula, Escuelita) → CARGOS menos la hoja Cobros.

Read-only sobre la planilla. Escribe el JSON que consume la app del Paseo.
"""

import datetime
import json
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
SALIDA_DEFAULT = ("/Users/Facu/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/"
                  "App Paseo Nordelta/src/data/deuda-efectivo.json")

# pestaña → (cómo cobra, col detalle, col ingreso, col egreso, col saldo,
#            signo del saldo: +1 si positivo = debe)
PESTANAS = {
    "Fabric":          ("banco",    2, 4, 5, 6, -1),
    "Bigg":            ("mixto",    2, 4, 5, 6, -1),
    "Boss":            ("efectivo", 2, 4, 5, 6, +1),
    "Volta + Open 25": ("efectivo", 2, 3, 4, 5, +1),
    "Peak One":        ("efectivo", 2, 3, 4, 5, +1),
}
# Cómo se llama el local para Mati (el de la pestaña es interno)
ROTULO = {"Volta + Open 25": "Volta + Open 25"}

# Los que no tienen pestaña: sus cargos viven sólo en CARGOS.
#   alias en Cobros · nota para Mati · si el número es confiable
SIN_PESTANA = {
    "Salón (Alto)": (["salon multiespacios"], None, True),
    "Escuelita": (["beto escuelita", "meta escuelita"],
                  "Paga un % de facturación: no lleva cargo fijo", False),
    "La Jaula / torneo": (["alquiler cancha / cumpleaños"],
                          "Arranca en agosto — confirmar el monto con Facu", False),
}
NO_PAGA_EFECTIVO = "No paga en efectivo"


def medio_del_cargo(cobra, concepto):
    """Un cargo no lleva medio escrito (la columna B es de los INGRESOS). Se
    deduce de la regla del local: Bigg es el único partido, y su parte en efectivo
    es exactamente la «Diferencia Alquiler (sin iva)»."""
    if cobra == "mixto":
        return "efectivo" if "sin iva" in concepto.lower() else "banco"
    return cobra


def medio_del_pago(fila, cd):
    """Está escrito en la fila: en la B en Boss/Volta/Peak One y en las filas
    nuevas de Fabric, en la C (el detalle) en Bigg."""
    txt = f"{fila[1]} {fila[cd]}".lower()
    if "efectivo" in txt or "mp facu" in txt:
        return "efectivo"
    if "banco" in txt:
        return "banco"
    return None


def num(x):
    return float(x) if isinstance(x, (int, float)) else 0.0


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else SALIDA_DEFAULT
    sv = sheets().spreadsheets()
    locales, avisos = [], []

    for tab, (cobra, cd, cin, ceg, csal, signo) in PESTANAS.items():
        vals = sv.values().get(spreadsheetId=CTAS, range=f"{tab}!A1:H200",
                               valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
        # el bloque que se cobra ahora es todo lo que hay DEBAJO del último pago
        ult_pago = max((i for i, r in enumerate(vals, 1)
                        if i >= 6 and len(r) > cin and num(r[cin])), default=5)
        cargos = pagos = del_mes = 0.0
        for i, r in enumerate(vals, 1):
            r = r + [""] * 10
            if i < 6:
                continue
            det, eg, ing = str(r[cd]).strip(), num(r[ceg]), num(r[cin])
            if eg:                                            # CARGO
                if medio_del_cargo(cobra, det) == "efectivo":
                    cargos += eg
                    if i > ult_pago:
                        del_mes += eg
            elif ing:                                         # PAGO
                m = medio_del_pago(r, cd)
                if m == "efectivo" or (m is None and cobra == "efectivo"):
                    pagos += ing
                elif m is None and cobra == "mixto":
                    avisos.append(f"{tab} f{i}: pago de ${ing:,.2f} sin medio "
                                  f"({det!r}) — se contó como banco")
        total = round(cargos - pagos, 2)
        locales.append({
            "nombre": ROTULO.get(tab, tab),
            "efectivo": total,
            "delMes": round(del_mes, 2),
            "vencido": round(total - del_mes, 2),
            "nota": NO_PAGA_EFECTIVO if cobra == "banco" else None,
            "confiable": True,
        })

    cargos_sh = sv.values().get(spreadsheetId=CTAS, range="CARGOS!A1:H1023",
                                valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    cobros_sh = sv.values().get(spreadsheetId=CTAS, range="Cobros!A1:E400",
                                valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    for nombre, (alias, nota, confiable) in SIN_PESTANA.items():
        c = sum(num(r[5]) for r in (x + [""] * 8 for x in cargos_sh[3:])
                if str(r[1]).strip() == nombre)
        p = sum(num(r[2]) for r in (x + [""] * 5 for x in cobros_sh[2:])
                if str(r[1]).strip().lower() in alias and str(r[3]).strip().lower() == "caja")
        total = round(c - p, 2)
        locales.append({"nombre": nombre, "efectivo": total, "delMes": 0.0,
                        "vencido": total, "nota": nota, "confiable": confiable})

    # Al total sólo entra lo que se puede salir a cobrar de verdad.
    total = round(sum(l["efectivo"] for l in locales
                      if l["confiable"] and l["efectivo"] > 0), 2)
    locales.sort(key=lambda l: (-l["efectivo"], l["nombre"]))
    doc = {"generado": datetime.date.today().isoformat(),
           "fuente": "Sheet Ctas Ctes — pestañas por local + CARGOS/Cobros",
           "total": total,
           "cuantosDeben": sum(1 for l in locales if l["confiable"] and l["efectivo"] > 0),
           "locales": locales,
           "avisos": avisos}

    with open(salida, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)

    print(f"OK  {salida}")
    print(f"{'Local':22s} {'efectivo':>14} {'del mes':>14} {'vencido':>12}")
    for l in locales:
        print(f"{l['nombre']:22s} {l['efectivo']:>14,.2f} {l['delMes']:>14,.2f} "
              f"{l['vencido']:>12,.2f}  {l['nota'] or ''}")
    print(f"\nTOTAL a cobrar en efectivo: ${total:,.2f}  ({doc['cuantosDeben']} locales)")
    for a in avisos:
        print(f"  ⚠ {a}")


if __name__ == "__main__":
    main()
