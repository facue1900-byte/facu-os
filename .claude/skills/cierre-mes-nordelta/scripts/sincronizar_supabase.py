#!/usr/bin/env python3
"""
Mete en Supabase los movimientos que solo estan en el Master Plan.

El sync de la app va en UN SOLO SENTIDO: app -> hoja Movimientos. Todo lo que se
carga en el Sheet durante el cierre de mes (la conciliacion del extracto del
Macro, sobre todo) nunca vuelve a Supabase, y la app queda mostrando meses
incompletos sin que nada avise. Al 10/09/2026 faltaban 48 movimientos por
$100.032.674 — julio y agosto no tenian NI UN movimiento de banco — y por eso la
app mostraba julio en -$3,6M cuando el Master Plan da +$14,8M.

    reporte: .../sincronizar_supabase.py             (no escribe)
    aplicar: .../sincronizar_supabase.py --aplicar

Compara por (fecha, tipo, medio, monto) contando repetidos, asi que un movimiento
duplicado a proposito no se pierde ni se duplica de nuevo.
"""
import os, sys, json, collections, datetime as dt
import httpx, openpyxl
from dotenv import load_dotenv

sys.path.insert(0, "/Users/Facu/facu-os")
load_dotenv("/Users/Facu/facu-os/.env")

REF = "wujutradczplokjrgmdo"          # Paseo Nordelta (NO el de Astronomy)
SHEET = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
XLSX = "/Users/Facu/facu-os/data/reportes-inversores/_master_plan.xlsx"

# Local del Master Plan -> local_id de Supabase (mismo criterio que LOCAL_MAP
# del Apps Script; un id que no este aca deja la columna vacia y el cobro no se
# le imputa a nadie).
LOCALES = {
    "Fabric": "fabric", "Bigg": "bigg", "Hamburgueseria": "boss",
    "Heladeria": "volta", "Peak One": "apex", "Salon Multiespacios": "salon",
    "La Jaula": "lajaula", "Beto Escuelita": "escuelita",
    "Meta Escuelita": "meta", "Parrilla": "parrilla", "Pizzeria": "canchera",
    "Cafeteria": "cafeteria", "Mini mercado": "market",
    "Alquiler Cancha / Cumpleaños": None,   # no es un local: no se imputa
}


def sql(query):
    r = httpx.post(f"https://api.supabase.com/v1/projects/{REF}/database/query",
                   headers={"Authorization": f"Bearer {os.environ['SUPABASE_ACCESS_TOKEN']}"},
                   json={"query": query}, timeout=120)
    if r.status_code >= 300:
        sys.exit(f"Supabase respondio {r.status_code}: {r.text[:400]}")
    return r.json()


def bajar_master_plan():
    from execution.google_auth import bajar_xlsx
    bajar_xlsx(SHEET, XLSX)


def clave(f, tipo, medio, monto):
    return (str(f)[:10], tipo, medio, round(float(monto), 2))


def faltantes():
    sb = sql("select fecha, tipo, medio, monto from movimientos where moneda='ARS'")
    if not isinstance(sb, list) or not sb:
        sys.exit("Supabase devolvio 0 movimientos. No sigo: o hay un problema de "
                 "permisos o la tabla esta vacia, y en los dos casos importar a "
                 "ciegas duplicaria todo.")
    S = collections.Counter(clave(x["fecha"], x["tipo"], x["medio"], x["monto"]) for x in sb)

    wb = openpyxl.load_workbook(XLSX, data_only=True)
    falta, total_mp = [], 0
    for r in wb["Movimientos"].iter_rows(min_row=2, values_only=True):
        if not r[0] or r[6] != "ARS":
            continue
        total_mp += 1
        f = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
        k = clave(f, r[1], r[2], r[5])
        if S[k] > 0:
            S[k] -= 1
            continue
        local, cat = r[3], r[4]
        if r[1] == "Ingreso":
            if str(local or "").startswith("Aporte de Capital"):
                categoria, local_id = str(local), None
            else:
                categoria = "Cobro inquilino"
                if local not in LOCALES:
                    sys.exit(f"Local desconocido en el Master Plan: {local!r} "
                             f"({f}, ${r[5]:,.0f}). Agregalo a LOCALES o el cobro "
                             f"queda sin imputar.")
                local_id = LOCALES[local]
        else:
            categoria, local_id = (str(cat) if cat else None), None
        falta.append(dict(fecha=str(f), tipo=r[1], medio=r[2], local_id=local_id,
                          categoria=categoria, monto=float(r[5]), moneda="ARS",
                          obs=str(r[7] or ""), origen="sheet", a_revisar=False))
    sobran = sum(v for v in S.values() if v > 0)
    return falta, total_mp, len(sb), sobran


def main():
    aplicar = "--aplicar" in sys.argv
    print("Bajando el Master Plan...")
    bajar_master_plan()
    falta, n_mp, n_sb, sobran = faltantes()

    print(f"\nMaster Plan: {n_mp} movimientos ARS")
    print(f"Supabase   : {n_sb}")
    print(f"Faltan     : {len(falta)}  (${sum(x['monto'] for x in falta):,.0f})")
    if sobran:
        print(f"\n!! {sobran} movimientos estan en Supabase y NO en el Master Plan.")
        print("   Este script NO los toca: revisalos a mano antes de confiar en la app.")
    if not falta:
        print("\nNada que importar: las dos fuentes dicen lo mismo.")
        return

    por_mes = collections.Counter(x["fecha"][:7] for x in falta)
    print("\npor mes:", dict(sorted(por_mes.items())))
    print("\nprimeros 5:")
    for x in falta[:5]:
        print(f"  {x['fecha']} {x['tipo']:<8}{x['medio']:<6}"
              f"{str(x['categoria'])[:22]:<23}{x['monto']:>13,.0f}")

    if not aplicar:
        print("\nNada escrito. Corré de nuevo con --aplicar.")
        return

    def esc(v):
        if v is None:
            return "null"
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return repr(v)
        return "'" + str(v).replace("'", "''") + "'"

    cols = ["fecha", "tipo", "medio", "local_id", "categoria", "monto",
            "moneda", "obs", "origen", "a_revisar"]
    filas = ",".join("(" + ",".join(esc(x[c]) for c in cols) + ")" for x in falta)
    res = sql(f"insert into movimientos ({','.join(cols)}) values {filas} returning id")
    print(f"\nInsertados: {len(res)}")

    falta2, n_mp2, n_sb2, _ = faltantes()
    print(f"Verificacion — Master Plan {n_mp2} · Supabase {n_sb2} · faltan {len(falta2)}")
    if falta2:
        sys.exit(f"ERROR: quedaron {len(falta2)} sin importar.")
    print("Las dos fuentes dicen lo mismo.")


if __name__ == "__main__":
    main()
