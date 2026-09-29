#!/usr/bin/env python3
"""Embudo de membresías en dos etapas — todo se crea en PAUSA.

Etapa 1 (conocer): el reel colaborativo de Camille en el estudio, optimizado a
ThruPlay en 20 km de Nordelta. Su trabajo no es traer leads, es llenar el público.

Etapa 2 (vender): los tres posteos de Silver, Gold y Platinum, a /academy, sólo a
quien vio 15 s o más del reel (público `Vio reel Camille (15s) | 60d`). Cada anuncio
llega con su propio mensaje autocompletado, para poder atribuir el lead a la
membresía sin adivinar.

Por qué el público es 15 s y no 3 s: el 3 s es el que trajo volumen sin intención en
agosto. Advantage+ Audience va APAGADO en la etapa 2: si está prendido, Meta sale del
público y el filtro deja de existir.

Nada de esto gasta: campañas, conjuntos y anuncios quedan en PAUSED. Prenderlos es
un paso aparte, con el OK de Facu.

    .venv/bin/python active/astronomy/pauta/crear_embudo_membresias.py
"""

import json
import os
import pathlib

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env", override=True)

TOKEN = os.getenv("META_ACCESS_TOKEN")
VERSION = os.getenv("META_API_VERSION", "v23.0")
CUENTA = "act_628045479472592"
PAGE = "271070669425605"
IG = "17841460877216598"
WHATSAPP = "5491124005565"

CREATIVO_CAMILLE = "2493861651134617"   # el mismo posteo que ya corre: conserva likes y comentarios
PUBLICO_VIO_REEL = "120249329509740448"  # video_view_15s del reel, 60 días

NORDELTA_20KM = {"custom_locations": [{
    "latitude": -34.414559, "longitude": -58.645394, "radius": 20,
    "distance_unit": "kilometer", "country": "AR"}]}

MEMBRESIAS = [  # (nombre, id del posteo de IG, mensaje con el que llega el lead)
    ("silver", "18117011266952634", "Hola! Quiero info de la membresía Silver"),
    ("gold", "18113377346584219", "Hola! Quiero info de la membresía Gold"),
    ("platinum", "18117929086961490", "Hola! Quiero info de la membresía Platinum"),
]

PRESUPUESTO_CONOCER = 400  # centavos de USD por día
PRESUPUESTO_VENDER = 300


def post(cli, path, **data):
    data = {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in data.items()}
    data["access_token"] = TOKEN
    r = cli.post(f"https://graph.facebook.com/{VERSION}/{path}", data=data).json()
    if "error" in r:
        e = r["error"]
        raise SystemExit(f"{path}: {e.get('error_user_title') or ''} {e.get('error_user_msg') or e.get('message')}")
    return r["id"]


def existente(cli, path, nombre):
    """Lo que ya se creó con este nombre, para que correr dos veces no duplique."""
    j = cli.get(f"https://graph.facebook.com/{VERSION}/{path}", params={
        "fields": "id,name", "limit": 500, "access_token": TOKEN,
        "filtering": json.dumps([{"field": "name", "operator": "EQUAL", "value": nombre}])}).json()
    return next((x["id"] for x in j.get("data", []) if x["name"] == nombre), None)


def asegurar(cli, path, **data):
    return existente(cli, path, data["name"]) or post(cli, path, **data)


def landing(plan):
    """/academy con el posteo de origen en utm_content: la web guarda los UTM en lead_events."""
    return ("https://astronomyofficial.com/academy?utm_source=meta&utm_medium=paid"
            f"&utm_campaign=membresias-vio-reel&utm_content={plan}#membresias")


def bienvenida(texto):
    return json.dumps({
        "type": "VISUAL_EDITOR", "version": 2, "landing_screen_type": "welcome_message",
        "media_type": "text",
        "text_format": {"customer_action_type": "autofill_message", "message": {
            "quick_replies": [], "text": "¡Hola! ¿Cómo podemos ayudarte?",
            "autofill_message": {"content": texto}}},
        "user_edit": True, "autofill_message_edited": True,
    }, ensure_ascii=False)


def main():
    creado = {}
    with httpx.Client(timeout=60) as cli:
        # Etapa 1 — conocer el estudio
        c1 = asegurar(cli, f"{CUENTA}/campaigns", name="Estudio | reel Camille | ThruPlay | sep-26",
                  objective="OUTCOME_ENGAGEMENT", status="PAUSED", special_ad_categories=[],
                  is_adset_budget_sharing_enabled="false")
        s1 = asegurar(cli, f"{CUENTA}/adsets", name="Reel Camille | Nordelta 20km | ThruPlay",
                  campaign_id=c1, status="PAUSED", daily_budget=PRESUPUESTO_CONOCER,
                  billing_event="IMPRESSIONS", optimization_goal="THRUPLAY",
                  destination_type="ON_VIDEO", bid_strategy="LOWEST_COST_WITHOUT_CAP",
                  targeting={"geo_locations": NORDELTA_20KM, "age_min": 18, "age_max": 65,
                             "targeting_automation": {"advantage_audience": 0}})
        a1 = asegurar(cli, f"{CUENTA}/ads", name="camille | colab | reel | estudio | sep-26",
                  adset_id=s1, status="PAUSED", creative={"creative_id": CREATIVO_CAMILLE})
        creado["conocer"] = {"campaign": c1, "adset": s1, "ad": a1}

        # Etapa 2 — membresías a quien vio el reel, a la WEB (29/09/2026).
        # Primero se armó a WhatsApp; Facu pidió mandarla a /academy (las tres membresías
        # juntas, con el WhatsApp a mano). La web ahora dispara Purchase por membresía, así
        # que se puede saber qué anuncio vendió. Optimiza visitas a la página: con 0 compras
        # en el pixel, Meta no tiene de dónde aprender a optimizar por venta todavía.
        c2 = asegurar(cli, f"{CUENTA}/campaigns", name="Membresias | vio reel Camille | web | sep-26",
                  objective="OUTCOME_TRAFFIC", status="PAUSED", special_ad_categories=[],
                  is_adset_budget_sharing_enabled="false")
        s2 = asegurar(cli, f"{CUENTA}/adsets", name="Membresias | Vio reel Camille 15s | web",
                  campaign_id=c2, status="PAUSED", daily_budget=PRESUPUESTO_VENDER,
                  billing_event="IMPRESSIONS", optimization_goal="LANDING_PAGE_VIEWS",
                  destination_type="WEBSITE", bid_strategy="LOWEST_COST_WITHOUT_CAP",
                  targeting={"geo_locations": {"countries": ["AR"]}, "age_min": 18, "age_max": 65,
                             "custom_audiences": [{"id": PUBLICO_VIO_REEL}],
                             "targeting_automation": {"advantage_audience": 0}})
        creado["vender"] = {"campaign": c2, "adset": s2, "ads": {}}
        for nombre, media, _ in MEMBRESIAS:
            nombre_ad = f"membresia {nombre} | post IG | vio reel | web | sep-26"
            if existente(cli, f"{CUENTA}/ads", nombre_ad):
                continue
            cr = post(cli, f"{CUENTA}/adcreatives", name=f"membresia {nombre} | post IG | web",
                      object_id=PAGE, instagram_user_id=IG, source_instagram_media_id=media,
                      call_to_action={"type": "LEARN_MORE", "value": {"link": landing(nombre)}})
            ad = asegurar(cli, f"{CUENTA}/ads", name=nombre_ad,
                      adset_id=s2, status="PAUSED", creative={"creative_id": cr})
            creado["vender"]["ads"][nombre] = {"creative": cr, "ad": ad}

    print(json.dumps(creado, indent=1))


if __name__ == "__main__":
    main()
