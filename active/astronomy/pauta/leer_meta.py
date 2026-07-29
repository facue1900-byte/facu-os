#!/usr/bin/env python3
"""Lector de la cuenta de Meta Ads de Astronomy — solo lectura.

Trae campañas, conjuntos y anuncios con su gasto y su rendimiento, y los deja en
una tabla y en un JSON crudo para poder cruzarlos después contra la plata real de
la app. **No escribe nada en Meta.** Apagar, crear o mover presupuesto es otro
script, con `--send`.

    # las campañas de los últimos 12 meses
    .venv/bin/python active/astronomy/pauta/leer_meta.py --dias 365

    # bajar a nivel conjunto sobre los últimos 30 días
    .venv/bin/python active/astronomy/pauta/leer_meta.py --nivel adset --dias 30

    # ver la evolución mes a mes de cada campaña
    .venv/bin/python active/astronomy/pauta/leer_meta.py --dias 365 --por-mes

Dos cosas que este script NO hace a propósito:

1. **No convierte monedas.** Reporta en la moneda de la cuenta y la declara. Si la
   cuenta factura en ARS, convertir a USD con un tipo de cambio de hoy sobre gasto
   de hace ocho meses da un número mentiroso.
2. **No llama "cliente" a una conversación de WhatsApp.** Meta cuenta conversaciones
   iniciadas; el que paga aparece en la app. Son dos números distintos y el segundo
   es el que importa.
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.parse

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env")

TOKEN = os.getenv("META_ACCESS_TOKEN")
CUENTA = os.getenv("META_AD_ACCOUNT_ID")
VERSION = os.getenv("META_API_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{VERSION}"

SALIDA = RAIZ / "data" / "pauta"

# La conversación de WhatsApp iniciada desde un anuncio. Es la conversión que
# persigue la campaña de Mensajes; Meta la nombra distinto según la ventana de
# atribución, así que se aceptan las variantes.
ACCIONES_MENSAJE = (
    "onsite_conversion.messaging_conversation_started_7d",
    "onsite_conversion.total_messaging_connection",
)

CAMPOS_INSIGHTS = (
    "spend,impressions,reach,frequency,clicks,ctr,cpm,cpc,"
    "actions,cost_per_action_type,date_start,date_stop"
)

CAMPOS_ENTIDAD = {
    "campaign": "id,name,status,effective_status,objective,daily_budget,lifetime_budget,created_time",
    "adset": "id,name,status,effective_status,campaign{name},daily_budget,lifetime_budget,optimization_goal,targeting",
    "ad": "id,name,status,effective_status,adset{name},campaign{name},creative{thumbnail_url}",
}


class ErrorMeta(RuntimeError):
    pass


def pedir(path, **params):
    """Un GET a la Graph API, siguiendo la paginación hasta el final."""
    params["access_token"] = TOKEN
    url = f"{BASE}/{path}?{urllib.parse.urlencode(params)}"
    filas = []
    with httpx.Client(timeout=60) as cli:
        while url:
            r = cli.get(url)
            cuerpo = r.json()
            if "error" in cuerpo:
                e = cuerpo["error"]
                raise ErrorMeta(
                    f"{e.get('type')} {e.get('code')}: {e.get('message')}\n"
                    f"  (endpoint {path}, versión {VERSION})"
                )
            r.raise_for_status()
            datos = cuerpo.get("data")
            if datos is None:  # objeto suelto, no una colección
                return cuerpo
            filas.extend(datos)
            url = cuerpo.get("paging", {}).get("next")
    return filas


def cuenta_info():
    return pedir(CUENTA, fields="name,account_status,currency,timezone_name,amount_spent,balance")


def conversaciones(insight):
    """Cuántas conversaciones de WhatsApp arrancó esta fila, y a qué costo."""
    cant = 0.0
    for a in insight.get("actions") or []:
        if a["action_type"] in ACCIONES_MENSAJE:
            cant = max(cant, float(a["value"]))
    costo = None
    for c in insight.get("cost_per_action_type") or []:
        if c["action_type"] in ACCIONES_MENSAJE:
            costo = float(c["value"])
    return cant, costo


def plata(v):
    """Los presupuestos vienen en centavos; el gasto viene ya en unidades."""
    return None if v is None else float(v) / 100


def traer(nivel, desde, hasta, por_mes):
    entidades = pedir(f"{CUENTA}/{nivel}s", fields=CAMPOS_ENTIDAD[nivel], limit=500)
    por_id = {e["id"]: e for e in entidades}

    params = {
        "level": nivel,
        "fields": CAMPOS_INSIGHTS,
        "time_range": json.dumps({"since": desde, "until": hasta}),
        "limit": 500,
    }
    if por_mes:
        params["time_increment"] = "monthly"
    insights = pedir(f"{CUENTA}/insights", **params)

    clave = f"{nivel}_id"
    for i in insights:
        i["_entidad"] = por_id.get(i.get(clave), {})
    return entidades, insights


def imprimir(insights, nivel, moneda, por_mes):
    if not insights:
        print("  (sin datos de entrega en esa ventana)")
        return

    filas = []
    for i in insights:
        ent = i["_entidad"]
        conv, costo = conversaciones(i)
        filas.append(
            {
                "nombre": ent.get("name") or i.get(f"{nivel}_name") or i.get(f"{nivel}_id", "?"),
                "estado": ent.get("effective_status", ""),
                "periodo": i["date_start"][:7] if por_mes else "",
                "gasto": float(i.get("spend", 0)),
                "impr": int(i.get("impressions", 0)),
                "clicks": int(i.get("clicks", 0)),
                "ctr": float(i.get("ctr", 0) or 0),
                "cpm": float(i.get("cpm", 0) or 0),
                "frec": float(i.get("frequency", 0) or 0),
                "conv": conv,
                "costo_conv": costo,
            }
        )
    filas.sort(key=lambda f: f["gasto"], reverse=True)

    ancho = min(42, max(len(f["nombre"]) for f in filas))
    cab = f"  {'NOMBRE':<{ancho}}  {'MES':<8}" if por_mes else f"  {'NOMBRE':<{ancho}}"
    print(f"{cab}  {'ESTADO':<10} {'GASTO':>11} {'IMPR':>9} {'CTR%':>6} {'CPM':>8} {'FREC':>5} {'CONV':>6} {'$/CONV':>9}")
    print("  " + "-" * (ancho + (10 if por_mes else 0) + 70))

    for f in filas:
        nom = f["nombre"][: ancho - 1] + "…" if len(f["nombre"]) > ancho else f["nombre"]
        pre = f"  {nom:<{ancho}}  {f['periodo']:<8}" if por_mes else f"  {nom:<{ancho}}"
        cc = f"{f['costo_conv']:>9,.0f}" if f["costo_conv"] else f"{'—':>9}"
        print(
            f"{pre}  {f['estado'][:10]:<10} {f['gasto']:>11,.0f} {f['impr']:>9,} "
            f"{f['ctr']:>6.2f} {f['cpm']:>8,.0f} {f['frec']:>5.2f} {f['conv']:>6,.0f} {cc}"
        )

    tot_g = sum(f["gasto"] for f in filas)
    tot_c = sum(f["conv"] for f in filas)
    print("  " + "-" * (ancho + (10 if por_mes else 0) + 70))
    print(f"  TOTAL: {tot_g:,.0f} {moneda} · {tot_c:,.0f} conversaciones", end="")
    print(f" · {tot_g / tot_c:,.0f} {moneda} por conversación" if tot_c else " · sin conversaciones atribuidas")


def main():
    ap = argparse.ArgumentParser(description="Lee la cuenta de Meta Ads. No escribe nada.")
    ap.add_argument("--nivel", choices=["campaign", "adset", "ad"], default="campaign")
    ap.add_argument("--dias", type=int, default=365)
    ap.add_argument("--desde", help="YYYY-MM-DD (pisa --dias)")
    ap.add_argument("--hasta", help="YYYY-MM-DD")
    ap.add_argument("--por-mes", action="store_true", help="Abre cada fila mes a mes")
    args = ap.parse_args()

    faltan = [n for n, v in (("META_ACCESS_TOKEN", TOKEN), ("META_AD_ACCOUNT_ID", CUENTA)) if not v]
    if faltan:
        sys.exit(f"Falta en el .env: {', '.join(faltan)}")
    if not CUENTA.startswith("act_"):
        sys.exit(f"META_AD_ACCOUNT_ID tiene que empezar con 'act_' — está como '{CUENTA}'")

    hoy = dt.date.today()
    hasta = args.hasta or hoy.isoformat()
    desde = args.desde or (hoy - dt.timedelta(days=args.dias)).isoformat()

    try:
        info = cuenta_info()
        entidades, insights = traer(args.nivel, desde, hasta, args.por_mes)
    except ErrorMeta as e:
        sys.exit(f"Meta rechazó la consulta:\n  {e}")

    moneda = info.get("currency", "?")
    print(f"\nCuenta: {info.get('name')} ({CUENTA})")
    print(f"Moneda: {moneda} · zona horaria {info.get('timezone_name')} · gasto histórico {plata(info.get('amount_spent')):,.0f} {moneda}")
    print(f"Ventana: {desde} → {hasta} · nivel {args.nivel} · {len(entidades)} entidades, {len(insights)} filas con entrega\n")

    imprimir(insights, args.nivel, moneda, args.por_mes)

    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"meta-{args.nivel}-{hoy.isoformat()}.json"
    destino.write_text(
        json.dumps(
            {"cuenta": info, "ventana": {"desde": desde, "hasta": hasta}, "entidades": entidades, "insights": insights},
            ensure_ascii=False,
            indent=2,
        )
    )
    print(f"\nCrudo en {destino}")
    print("Los montos están en la moneda de la cuenta. No se convirtió nada.\n")


if __name__ == "__main__":
    main()
