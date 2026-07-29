#!/usr/bin/env python3
"""Reporte de cómo viene la pauta de Astronomy Academy desde los cambios del 28/07/2026.

Compara la ventana actual contra la línea de base de julio y responde las tres
preguntas que quedaron abiertas al hacer los cambios:

  1. ¿Ampliar el radio de 18 a 35 km bajó las impresiones por conversación?
  2. ¿El carrusel le gana a la imagen simple? (formato nunca probado en 35 meses)
  3. ¿El copy de dolor le gana al descriptivo?

La métrica que manda es **impresiones por conversación**, no el costo: el costo se
mueve con el precio de los medios y ensucia la comparación entre períodos. Las
impresiones por conversación miden si la audiencia responde, y eso es lo que se cambió.

    .venv/bin/python active/astronomy/pauta/reporte_pauta.py
    .venv/bin/python active/astronomy/pauta/reporte_pauta.py --desde 2026-08-01
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env", override=True)

TOKEN = os.getenv("META_ACCESS_TOKEN")
CUENTA = os.getenv("META_AD_ACCOUNT_ID")
VERSION = os.getenv("META_API_VERSION", "v23.0")

# Los cambios se aplicaron el 28/07/2026: radio 18→35 km, carrusel de Modo Profesional
# y variante de copy con gancho de dolor.
CAMBIO = "2026-07-29"

# Línea de base: julio 2026 completo, con el radio viejo de 18 km y solo imagen simple.
BASE = {"gasto": 449, "conv": 203, "costo": 2.21, "impr_conv": 1995}

ACCIONES = ("onsite_conversion.total_messaging_connection",
            "onsite_conversion.messaging_conversation_started_7d")


def msgs(fila):
    for a in fila.get("actions") or []:
        if a["action_type"] in ACCIONES:
            return float(a["value"])
    return 0.0


def api(cli, path, **q):
    q["access_token"] = TOKEN
    out, url = [], f"https://graph.facebook.com/{VERSION}/{path}"
    while url:
        j = cli.get(url, params=q).json()
        q = {}
        if "error" in j:
            sys.exit(f"Meta rechazó {path}: {j['error'].get('message')}")
        if "data" not in j:
            return j
        out += j["data"]
        url = j.get("paging", {}).get("next")
    return out


def clasificar(nombre):
    n = nombre.lower()
    if "carrusel" in n and "dolor" in n:
        return "carrusel · copy de dolor"
    if "carrusel" in n:
        return "carrusel · copy descriptivo"
    return "imagen simple"


def main():
    ap = argparse.ArgumentParser(description="Cómo viene la pauta desde los cambios.")
    ap.add_argument("--desde", default=CAMBIO)
    ap.add_argument("--hasta", default=dt.date.today().isoformat())
    args = ap.parse_args()

    if not TOKEN or not CUENTA:
        sys.exit("Faltan META_ACCESS_TOKEN o META_AD_ACCOUNT_ID en el .env")

    # El día que se aplican los cambios, la ventana todavía no existe. Meta rechaza
    # since > until, así que se corta antes con un mensaje claro en vez de un error.
    if dt.date.fromisoformat(args.desde) > dt.date.fromisoformat(args.hasta):
        faltan = (dt.date.fromisoformat(args.desde) - dt.date.today()).days
        print(f"\nLa ventana de medición arranca el {args.desde} — faltan {faltan} día(s).")
        print("Todavía no hay nada que comparar. El lunes va a haber datos.\n")
        return

    with httpx.Client(timeout=90) as cli:
        rango = json.dumps({"since": args.desde, "until": args.hasta})
        cuenta = api(cli, CUENTA, fields="name,currency")
        tot = api(cli, f"{CUENTA}/insights", level="account",
                  fields="spend,impressions,actions", time_range=rango)
        ads = api(cli, f"{CUENTA}/insights", level="ad",
                  fields="ad_id,ad_name,spend,impressions,actions", time_range=rango, limit=200)
        # Solo importan los problemas de anuncios que DEBERÍAN estar entregando. La cuenta
        # arrastra cientos de anuncios de campañas pausadas desde 2024 cuyos `issues_info`
        # son ruido histórico: reportarlos hace que el informe grite por nada.
        vivos = {a["id"] for s in api(cli, f"{CUENTA}/adsets", fields="id,effective_status", limit=300)
                 if s["effective_status"] == "ACTIVE"
                 for a in api(cli, f"{s['id']}/ads", fields="id")}
        rotos = [a for a in api(cli, f"{CUENTA}/ads", fields="id,name,effective_status,issues_info", limit=300)
                 if a.get("issues_info") and a["id"] in vivos and a["effective_status"] == "ACTIVE"]

    dias = (dt.date.fromisoformat(args.hasta) - dt.date.fromisoformat(args.desde)).days or 1
    print(f"\n{cuenta['name']} · {args.desde} → {args.hasta} ({dias} días)\n")

    if not tot:
        print("Todavía no hay entrega en esta ventana. Volvé a correrlo en un par de días.\n")
        return

    t = tot[0]
    g, im, cv = float(t.get("spend", 0)), float(t.get("impressions", 0)), msgs(t)
    if not cv:
        print(f"Gasto US${g:,.0f} · {im:,.0f} impresiones · **cero conversaciones todavía**.")
        print("Con menos de una semana esto es normal si los creativos siguen en revisión.\n")
        return

    ipc, costo = im / cv, g / cv
    print("EL NÚMERO QUE IMPORTA — impresiones por conversación")
    print(f"   julio (radio 18km):  {BASE['impr_conv']:>7,.0f}")
    print(f"   ahora  (radio 35km):  {ipc:>7,.0f}   {'MEJOR' if ipc < BASE['impr_conv'] else 'PEOR'} "
          f"({(ipc/BASE['impr_conv']-1)*100:+.0f}%)\n")
    print(f"Costo por conversación:  US${costo:.2f}   (julio: US${BASE['costo']:.2f})")
    print(f"Gasto US${g:,.0f} · {cv:,.0f} conversaciones · {g/dias:.2f}/día\n")

    grupos = {}
    for a in ads:
        k = clasificar(a.get("ad_name", ""))
        d = grupos.setdefault(k, {"g": 0.0, "cv": 0.0, "im": 0.0})
        d["g"] += float(a.get("spend", 0)); d["cv"] += msgs(a); d["im"] += float(a.get("impressions", 0))

    print(f"{'FORMATO / COPY':<30}{'GASTO':>8}{'CONV':>7}{'US$/CV':>9}{'IMPR/CV':>10}")
    print("-" * 64)
    for k, d in sorted(grupos.items(), key=lambda x: (x[1]["im"] / x[1]["cv"]) if x[1]["cv"] else 9e9):
        cc = f"{d['g']/d['cv']:.2f}" if d["cv"] else "—"
        pc = f"{d['im']/d['cv']:,.0f}" if d["cv"] else "—"
        print(f"{k:<30}{d['g']:>8,.0f}{d['cv']:>7,.0f}{cc:>9}{pc:>10}")

    print(f"\n{'ANUNCIO':<44}{'GASTO':>8}{'CONV':>7}{'IMPR/CV':>10}")
    print("-" * 69)
    for a in sorted(ads, key=lambda x: -float(x.get("spend", 0))):
        cvx, imx = msgs(a), float(a.get("impressions", 0))
        print(f"{a.get('ad_name','?')[:43]:<44}{float(a.get('spend',0)):>8,.0f}{cvx:>7,.0f}"
              f"{(f'{imx/cvx:,.0f}' if cvx else '—'):>10}")

    flojos = [a for a in ads if msgs(a) and msgs(a) < 20]
    if flojos:
        print(f"\n{len(flojos)} anuncios tienen menos de 20 conversaciones: con esa muestra "
              "todavía no se decide nada. No apagar por ahora.")
    if rotos:
        print("\nANUNCIOS CON PROBLEMAS:")
        for a in rotos:
            print(f"   {a['name'][:44]:<46} {a['issues_info'][0].get('error_summary','')[:60]}")
    print()


if __name__ == "__main__":
    main()
