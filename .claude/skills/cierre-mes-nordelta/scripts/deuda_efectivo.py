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
  · sin pestaña → cada uno lleva su REGLA explícita (ver `SIN_PESTANA`), porque
    sus cargos no se generan solos en CARGOS. Los pagos siempre salen de Cobros.

Read-only sobre la planilla. Escribe el JSON que consume la app del Paseo.
"""

import datetime
import json
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402
from reglas_locales import SIN_PESTANA, JAULA_AGOSTO  # noqa: E402

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

NO_PAGA_EFECTIVO = "No paga en efectivo"
# `SIN_PESTANA` y `JAULA_AGOSTO` viven en reglas_locales.py, junto con las reglas
# que usan el radar y el export: son la misma verdad y no pueden divergir.
# La Jaula no paga expensas / servicios comunes por ahora (Facu, 06/08/2026): el
# precio semestral de la hoja Futbol es TODO lo que se le cobra.


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


def a_fecha(serial):
    """Sheets guarda las fechas como serial desde el 30/12/1899."""
    if not isinstance(serial, (int, float)):
        return None
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(serial))


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def meses_entre(desde, hasta):
    """Lista de (año, mes) desde `desde` hasta `hasta`, ambos inclusive."""
    y, m = desde
    out = []
    while (y, m) <= hasta:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def precios_semestrales_jaula(sv):
    """El alquiler de La Jaula sale de la hoja **Futbol, columna AR**.

    Ojo con la columna: los valores de TODOS los meses están, pero el que se
    cobra es sólo el del mes pintado de **verde** (marzo y septiembre) — el
    contrato se ajusta por semestre. Los meses del medio son la cadena que va
    componiendo el IPC, no un precio a cobrar.

    Y la cadena tiene dos meses de atraso: el valor de un mes es el del mes
    anterior por (1 + IPC de dos meses antes). O sea que el precio de
    **septiembre necesita el IPC de julio**, que el INDEC publica el 15/08. Si
    todavía no está cargado en la hoja INFLACIÓN, el precio no es definitivo y
    se avisa en vez de darlo por bueno.

    Devuelve [(año, mes, precio, [meses de IPC que faltan])], en orden.
    """
    g = sv.get(spreadsheetId=CTAS, ranges=["Futbol!AP7:AS200"],
               includeGridData=True,
               fields=("sheets.data.rowData.values("
                       "effectiveValue,effectiveFormat.backgroundColor)")).execute()
    filas = g["sheets"][0]["data"][0].get("rowData", [])

    tabla, anio = [], None
    for fila in filas:
        cels = (fila.get("values", []) + [{}] * 4)[:4]
        ev = [c.get("effectiveValue", {}) for c in cels]
        if ev[0].get("numberValue"):
            anio = int(ev[0]["numberValue"])
        mes = str(ev[1].get("stringValue", "")).strip().lower()
        if anio is None or mes not in MESES:
            continue
        bg = cels[2].get("effectiveFormat", {}).get("backgroundColor", {})
        verde = (round(bg.get("green", 0), 2) > round(bg.get("red", 0), 2)
                 and round(bg.get("green", 0), 2) > 0.5
                 and round(bg.get("blue", 0), 2) < round(bg.get("green", 0), 2))
        tabla.append({"anio": anio, "mes": MESES.index(mes) + 1,
                      "precio": ev[2].get("numberValue"),
                      "ipc": ev[3].get("numberValue"),
                      "verde": verde})

    anclas, anterior = [], 0
    for i, r in enumerate(tabla):
        if not r["verde"]:
            continue
        # El precio de la fila i se compone desde el ancla anterior usando los
        # IPC de las filas (anterior-1) .. (i-2). El que falte lo vuelve provisorio.
        faltan = [MESES[tabla[j]["mes"] - 1] for j in range(max(anterior - 1, 0), max(i - 1, 0))
                  if tabla[j]["ipc"] is None]
        anclas.append((r["anio"], r["mes"], r["precio"], faltan))
        anterior = i
    return anclas


def precio_jaula(anclas, anio, mes):
    """El precio vigente para un mes es el del último ancla verde <= ese mes."""
    vigentes = [a for a in anclas if (a[0], a[1]) <= (anio, mes)]
    return vigentes[-1] if vigentes else None


def main():
    salida = sys.argv[1] if len(sys.argv) > 1 else SALIDA_DEFAULT
    hoy = datetime.date.today()
    mes_actual = (hoy.year, hoy.month)
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
    anclas = precios_semestrales_jaula(sv)

    def cobrado(alias, desde=None):
        """Lo que ya pagó en caja. `desde` = (año, mes) para no arrastrar plata
        de un régimen anterior al que estamos cobrando."""
        tot = 0.0
        for r in (x + [""] * 5 for x in cobros_sh[2:]):
            if str(r[1]).strip().lower() not in alias:
                continue
            if str(r[3]).strip().lower() != "caja":
                continue
            f = a_fecha(r[0])
            if desde and (not f or (f.year, f.month) < desde):
                continue
            tot += num(r[2])
        return tot

    for nombre, cfg in SIN_PESTANA.items():
        regla, alias, nota = cfg["regla"], cfg["alias"], cfg.get("nota")
        confiable, del_mes = True, 0.0

        if regla == "porcentaje":
            # No hay cargo fijo: nunca hay nada que salir a cobrar en mano.
            total = 0.0

        elif regla == "cta":
            c = sum(num(r[5]) for r in (x + [""] * 8 for x in cargos_sh[3:])
                    if str(r[1]).strip() == nombre)
            total = round(c - cobrado(alias), 2)

        elif regla == "fijo":
            meses = meses_entre(cfg["desde"], mes_actual)
            del_mes = float(cfg["monto"]) if meses else 0.0
            total = round(len(meses) * cfg["monto"] - cobrado(alias, cfg["desde"]), 2)

        elif regla == "jaula":
            cargado = 0.0
            for (y, m) in meses_entre(cfg["desde"], mes_actual):
                if (y, m) == (2026, 8):
                    monto = float(JAULA_AGOSTO)
                    nota = ("Alquiler de agosto — ya descontado el saldo a favor. "
                            "No paga expensas")
                else:
                    ancla = precio_jaula(anclas, y, m)
                    if ancla is None or ancla[2] is None:
                        avisos.append(f"La Jaula {MESES[m-1]} {y}: sin precio en "
                                      f"Futbol!AR — no se cobra en la tarjeta")
                        confiable = False
                        continue
                    monto = float(ancla[2])
                    nota = (f"Alquiler semestral de Futbol!AR "
                            f"({MESES[ancla[1]-1]} {ancla[0]}). No paga expensas")
                    if ancla[3]:
                        avisos.append(f"La Jaula: el precio del semestre de "
                                      f"{MESES[ancla[1]-1]} {ancla[0]} todavía no es "
                                      f"definitivo, falta el IPC de {', '.join(ancla[3])}")
                        nota += " — falta cargar IPC, precio provisorio"
                        confiable = False
                cargado += monto
                del_mes = monto
            total = round(cargado - cobrado(alias, cfg["desde"]), 2)

        else:
            raise ValueError(f"regla desconocida para {nombre}: {regla}")

        locales.append({"nombre": nombre, "efectivo": total,
                        "delMes": round(min(del_mes, total), 2) if total > 0 else 0.0,
                        "vencido": round(total - min(del_mes, total), 2) if total > 0 else total,
                        "nota": nota, "confiable": confiable})

    # Al total sólo entra lo que se puede salir a cobrar de verdad.
    total = round(sum(l["efectivo"] for l in locales
                      if l["confiable"] and l["efectivo"] > 0), 2)
    locales.sort(key=lambda l: (-l["efectivo"], l["nombre"]))
    doc = {"generado": hoy.isoformat(),
           "fuente": "Sheet Ctas Ctes — pestañas por local + CARGOS/Cobros/Futbol",
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
    print("\nPrecios semestrales de La Jaula (Futbol!AR, en verde):")
    for a in anclas:
        falta = f"  ⚠ falta IPC de {', '.join(a[3])}" if a[3] else ""
        print(f"  {MESES[a[1]-1]:>10} {a[0]}  ${a[2]:,.2f}{falta}")
    for a in avisos:
        print(f"  ⚠ {a}")


if __name__ == "__main__":
    main()
