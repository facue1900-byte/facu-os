#!/usr/bin/env python3
"""Compara la hoja Movimientos del Master Plan contra la base (fuente de verdad).

La base de la app es la verdad; la hoja es el espejo que lee el contador. Se
desincronizan solas: hay filas cargadas a mano en la hoja, y hasta el 12/08/2026
el sync escribia las filas sin id, asi que un update apendaba en vez de pisar.
Chequeo de cierre de mes: el neto por mes tiene que dar CERO de diferencia.

Read-only por defecto. Con --backfill escribe SOLO la columna K (el ID de la app)
de las filas que matchean 1 a 1 y hoy la tienen vacía — sin tocar ningún importe.
"""
import datetime
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

MP = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
REF = "wujutradczplokjrgmdo"
LOCAL_MAP = {
    "fabric": "Fabric", "bigg": "Bigg", "boss": "Hamburgueseria", "volta": "Heladeria",
    "apex": "Peak One", "salon": "Salon Multiespacios", "escuelita": "Beto Escuelita",
    "meta": "Meta Escuelita", "pole-position": "Pole Position", "lajaula": "La Jaula",
    "cafeteria": "Cafeteria", "fabric-nuevo": "Fabric", "parrilla": "Parrilla",
    "shockba": "Heladeria", "canchera": "Pizzeria", "market": "Mini mercado",
    **{f"comercio-{i}": f"Comercio {i}" for i in range(1, 7)},
}


def base():
    sql = ("select id::text, fecha::text, tipo, medio, local_id, categoria, "
           "monto::float8, obs from movimientos order by fecha")
    env = dict(os.environ)
    for line in open("/Users/Facu/facu-os/.env", encoding="utf-8"):
        if line.strip().startswith("SUPABASE_ACCESS_TOKEN="):
            env["SUPABASE_ACCESS_TOKEN"] = line.split("=", 1)[1].strip()
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://api.supabase.com/v1/projects/{REF}/database/query",
         "-H", f"Authorization: Bearer {env['SUPABASE_ACCESS_TOKEN']}",
         "-H", "Content-Type: application/json",
         "-d", json.dumps({"query": sql})], capture_output=True, text=True, env=env)
    return json.loads(out.stdout)


def a_fecha(v):
    if isinstance(v, (int, float)):
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))).isoformat()
    s = str(v).strip()
    if "/" in s:
        d, m, y = s.split("/")[:3]
        return f"{y}-{int(m):02d}-{int(d):02d}"
    return s[:10]


def clave(fecha, tipo, monto, obs):
    return (fecha, tipo, round(float(monto), 2), (obs or "").strip().lower())


def main():
    sv = sheets().spreadsheets()
    vals = sv.values().get(spreadsheetId=MP, range="Movimientos!A1:K2000",
                           valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    filas = []
    for i, r in enumerate(vals[1:], 2):
        r = list(r) + [""] * 11
        if not str(r[1]).strip():
            continue
        filas.append({"fila": i, "fecha": a_fecha(r[0]), "tipo": str(r[1]).strip(),
                      "medio": str(r[2]).strip(), "local": str(r[3]).strip(),
                      "cat": str(r[4]).strip(),
                      "monto": float(r[5]) if isinstance(r[5], (int, float)) else 0.0,
                      "obs": str(r[7]).strip(), "id": str(r[10]).strip()})
    movs = base()
    print(f"base: {len(movs)} movimientos · hoja: {len(filas)} filas\n")

    ch, cf = Counter(), Counter()
    por_clave_hoja = defaultdict(list)
    for f in filas:
        k = clave(f["fecha"], f["tipo"], f["monto"], f["obs"])
        ch[k] += 1
        por_clave_hoja[k].append(f)
    por_clave_base = defaultdict(list)
    for m in movs:
        k = clave(m["fecha"], m["tipo"], m["monto"], m["obs"])
        cf[k] += 1
        por_clave_base[k].append(m)

    faltan = [(k, cf[k] - ch[k]) for k in cf if cf[k] > ch[k]]
    sobran = [(k, ch[k] - cf[k]) for k in ch if ch[k] > cf[k]]

    def plata(items):
        return sum(k[2] * n for k, n in items)

    print(f"EN LA BASE Y NO EN LA HOJA: {sum(n for _, n in faltan)} filas  "
          f"${plata(faltan):,.2f}")
    for k, n in sorted(faltan):
        print(f"   {k[0]}  {k[1]:<8} ${k[2]:>13,.2f} ×{n}  {k[3][:60]}")
    print(f"\nEN LA HOJA Y NO EN LA BASE: {sum(n for _, n in sobran)} filas  "
          f"${plata(sobran):,.2f}")
    for k, n in sorted(sobran):
        fs = ", ".join(str(f["fila"]) for f in por_clave_hoja[k])
        print(f"   {k[0]}  {k[1]:<8} ${k[2]:>13,.2f} ×{n}  {k[3][:50]}  (filas {fs})")

    # ---- neto por mes, que es lo que ve el contador
    print("\nNETO POR MES (Ingresos − Egresos)")
    print(f"{'mes':10} {'base':>16} {'hoja':>16} {'dif':>14}")
    meses = sorted({m["fecha"][:7] for m in movs} | {f["fecha"][:7] for f in filas})
    for mes in meses:
        nb = sum((1 if m["tipo"] == "Ingreso" else -1) * m["monto"] for m in movs if m["fecha"][:7] == mes)
        nh = sum((1 if f["tipo"] == "Ingreso" else -1) * f["monto"] for f in filas if f["fecha"][:7] == mes)
        flag = "" if abs(nb - nh) < 0.01 else "  ←"
        print(f"{mes:10} {nb:>16,.2f} {nh:>16,.2f} {nb - nh:>14,.2f}{flag}")

    # ---- backfill del ID (columna K), sólo donde el match es 1 a 1
    sin_id = [f for f in filas if not f["id"]]
    updates = []
    for f in sin_id:
        k = clave(f["fecha"], f["tipo"], f["monto"], f["obs"])
        if len(por_clave_base[k]) == 1 and len(por_clave_hoja[k]) == 1:
            updates.append({"range": f"Movimientos!K{f['fila']}",
                            "values": [[por_clave_base[k][0]["id"]]]})
    print(f"\nID de la app: {len(filas) - len(sin_id)} filas lo tienen, {len(sin_id)} no.")
    print(f"Se puede completar sin ambigüedad en {len(updates)} de esas {len(sin_id)}.")
    if "--backfill" not in sys.argv:
        print("(read-only: no escribí nada — corré con --backfill para completar la columna K)")
        return
    for i in range(0, len(updates), 500):
        sv.values().batchUpdate(spreadsheetId=MP, body={
            "valueInputOption": "RAW", "data": updates[i:i + 500]}).execute()
    print(f"escritas {len(updates)} celdas de la columna K (ningún importe tocado)")


if __name__ == "__main__":
    main()
