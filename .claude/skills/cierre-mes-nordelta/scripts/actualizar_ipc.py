#!/usr/bin/env python3
"""
Actualiza la tabla INFLACIÓN de Ctas Ctes con el IPC mensual publicado.

Las pestañas de los locales (Fabric, Bigg, ...) ya leen su columna IPC con
fórmulas `='INFLACIÓN'!C<n>`, y el alquiler se re-indexa trimestralmente con
esas tasas: **llenar INFLACIÓN es lo único manual, y esto lo automatiza.**

Fuente: https://api.argentinadatos.com/v1/finanzas/indices/inflacion (IPC
mensual INDEC). Verificado el 28/07/2026: coincide exactamente con lo que la
tabla ya tenía cargado a mano (mar 3,4 · abr 2,6 · may 2,1 · jun 1,9).

    .venv/bin/python actualizar_ipc.py            # muestra qué falta, no escribe
    .venv/bin/python actualizar_ipc.py --escribir # completa los meses faltantes

La fila de cada mes de 2026 en INFLACIÓN es fija: Enero=C2 ... Diciembre=C13.
Si el año cambia, este script se niega a escribir (hay que extender la tabla).
"""

import json
import sys
import urllib.request

API = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"
FILE_ID = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def main():
    escribir = "--escribir" in sys.argv

    # La API devuelve 403 al user-agent default de urllib; con uno normal anda.
    req = urllib.request.Request(API, headers={"User-Agent": "facu-os/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        serie = json.load(r)
    publicados = {}   # (año, mes) -> tasa decimal
    for punto in serie:
        anio, mes, _ = (int(x) for x in punto["fecha"].split("-"))
        publicados[(anio, mes)] = float(punto["valor"]) / 100.0

    sys.path.insert(0, "/Users/Facu/facu-os")
    from execution.google_auth import sheets
    s = sheets(cuenta="facu")
    tabla = s.spreadsheets().values().get(
        spreadsheetId=FILE_ID, range="INFLACIÓN!B2:C13",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])

    cargados = {}
    for i, fila in enumerate(tabla):
        if fila and fila[0]:
            mes_nombre = str(fila[0]).strip().lower()
            if mes_nombre in MESES:
                tasa = fila[1] if len(fila) > 1 and fila[1] != "" else None
                cargados[MESES.index(mes_nombre) + 1] = tasa

    faltan, difieren = [], []
    for mes, tasa_cargada in sorted(cargados.items()):
        clave = (2026, mes)
        if clave not in publicados:
            continue
        oficial = publicados[clave]
        if tasa_cargada is None:
            faltan.append((mes, oficial))
        elif abs(float(tasa_cargada) - oficial) > 0.0005:
            difieren.append((mes, float(tasa_cargada), oficial))

    ultimo = max(m for (a, m) in publicados if a == 2026)
    print(f"IPC publicado hasta: 2026-{ultimo:02d} "
          f"({publicados[(2026, ultimo)]*100:.1f}%)")
    for mes, tasa, oficial in difieren:
        print(f"⚠ {MESES[mes-1]}: la tabla dice {tasa*100:.1f}% y el publicado es "
              f"{oficial*100:.1f}% — revisar a mano, no lo piso.")
    if not faltan:
        print("La tabla está al día. El próximo IPC (INDEC) sale a mitad del mes "
              "que viene.")
        return
    print("Meses publicados que faltan en la tabla:")
    for mes, oficial in faltan:
        print(f"  {MESES[mes-1]}: {oficial*100:.1f}%")
    if not escribir:
        print("\n[SIN --escribir] No toqué nada.")
        return
    data = [{"range": f"INFLACIÓN!C{mes+1}", "values": [[oficial]]}
            for mes, oficial in faltan]
    s.spreadsheets().values().batchUpdate(
        spreadsheetId=FILE_ID,
        body={"valueInputOption": "RAW", "data": data}).execute()
    print(f"\nEscritos {len(data)} meses. Las pestañas de los locales lo toman "
          f"solas por fórmula.")


if __name__ == "__main__":
    main()
