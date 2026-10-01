#!/usr/bin/env python3
"""Lanza la pauta de octubre 2026: embudo Camille + videos de membresías, y apaga el resto.

Decisión de Facu (01/10/2026): "armemos todo el plan de pauta con embudo y videos que
propusiste y demos de baja el resto". Lo que hace, en orden:

1. Sube los tres videos (Silver, Gold, Platinum, voz de José, 9:16) a la cuenta.
2. Crea un anuncio por video en el conjunto del paso 2 (los que vieron 15 s del reel),
   como DARK POST: no se publica en el perfil, sólo existe como anuncio. Cada uno lleva
   `utm_content=<plan>-video`, así el reporte /admin/leads/pauta lo separa del posteo.
3. Prende el embudo: paso 1 (reel Camille, ThruPlay) a US$12/día, paso 2 a US$3/día.
4. Apaga los conjuntos de productos sueltos (Curso de DJ, Modo Profesional, Membresía
   online): desde el 23/09 sólo se venden membresías.
5. Relee todo de Meta y lo imprime. Un "ok" de la API dice que el pedido entró, no que
   quedó como queríamos.

Sin `--send` no escribe nada: muestra el plan. Se puede volver a correr: busca por
nombre antes de crear.

    .venv/bin/python active/astronomy/pauta/lanzar_embudo_octubre.py          # plan
    .venv/bin/python active/astronomy/pauta/lanzar_embudo_octubre.py --send   # ejecuta
"""

import argparse
import json
import os
import pathlib
import time

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env", override=True)

TOKEN = os.getenv("META_ACCESS_TOKEN")
VERSION = os.getenv("META_API_VERSION", "v23.0")
CUENTA = "act_628045479472592"
PAGE = "271070669425605"
IG = "17841460877216598"
G = f"https://graph.facebook.com/{VERSION}"

VIDEOS_DIR = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/Membresias-borrador-2026-09-30"

# Paso 1 y paso 2 del embudo, creados el 29/09 por crear_embudo_membresias.py
CAMP_CONOCER, SET_CONOCER, AD_CONOCER = "120249329517930448", "120249329518130448", "120249329519490448"
CAMP_VENDER, SET_VENDER = "120249329919360448", "120249329919700448"
ADS_POSTEOS = ["120249329920240448", "120249329921030448", "120249329924850448"]  # silver, gold, platinum

PRESUPUESTO_CONOCER = 1200  # centavos de USD por día
PRESUPUESTO_VENDER = 300

APAGAR = {  # conjuntos de productos que ya no se venden sueltos
    "120245002157210448": "Curso de DJ (IntWpp1 PresCurso Nordelta 20km)",
    "120248181844100448": "Modo Profesional (MP | Nordelta 20km | wpp)",
    "120248181844670448": "Membresía online (Prov Bs As + CABA | wpp)",
}

# El texto sale de la oferta vigente (active/astronomy/OFERTA_2026.md). Sin precio: el precio
# lo da la web, que es adonde lleva el anuncio.
VIDEOS = [
    ("silver", "Silver Member",
     "Aprendé a mezclar y a producir en nuestro estudio de Nordelta. Con Silver tenés 240 "
     "créditos por mes para 4 clases de DJ o producción: vos elegís el día, el horario y el profe."),
    ("gold", "Gold Member",
     "Clases de DJ y producción, cabina para practicar tu set y producción online uno a uno. "
     "Con Gold tenés 360 créditos por mes para combinarlos como necesites."),
    ("platinum", "Platinum Member",
     "Para el que va en serio: la Carrera Profesional, 8 clases en 2 meses con temario y "
     "horario fijo, tu presskit al terminarla y todo lo de Gold."),
]


def landing(pieza):
    return ("https://astronomyofficial.com/academy?utm_source=meta&utm_medium=paid"
            f"&utm_campaign=membresias-vio-reel&utm_content={pieza}#membresias")


def chequear(r, que):
    if isinstance(r, dict) and "error" in r:
        e = r["error"]
        raise SystemExit(f"{que}: {e.get('error_user_title') or ''} {e.get('error_user_msg') or e.get('message')}")
    return r


def get(cli, path, **p):
    p["access_token"] = TOKEN
    return chequear(cli.get(f"{G}/{path}", params=p).json(), path)


def post(cli, path, **data):
    data = {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in data.items()}
    data["access_token"] = TOKEN
    return chequear(cli.post(f"{G}/{path}", data=data).json(), path)


def anuncio_existente(cli, nombre):
    j = get(cli, f"{SET_VENDER}/ads", fields="id,name", limit=100)
    return next((x["id"] for x in j.get("data", []) if x["name"] == nombre), None)


def subir_video(cli, plan):
    archivo = VIDEOS_DIR / f"{plan}-v5-9x16.mp4"
    if not archivo.exists():
        raise SystemExit(f"falta el video: {archivo}")
    with open(archivo, "rb") as f:
        r = cli.post(f"{G}/{CUENTA}/advideos", data={"access_token": TOKEN, "name": f"membresia {plan} | voz jose | 9x16 | oct-26"},
                     files={"source": (archivo.name, f, "video/mp4")}, timeout=600).json()
    vid = chequear(r, f"subir {plan}")["id"]
    # Meta procesa el video antes de dejar usarlo en un anuncio.
    for _ in range(60):
        st = get(cli, vid, fields="status").get("status", {})
        if st.get("video_status") == "ready":
            break
        time.sleep(10)
    else:
        raise SystemExit(f"el video de {plan} ({vid}) no terminó de procesarse en 10 minutos")
    thumbs = get(cli, f"{vid}/thumbnails", fields="uri,is_preferred").get("data", [])
    if not thumbs:
        raise SystemExit(f"el video de {plan} ({vid}) no tiene miniatura")
    thumb = next((t["uri"] for t in thumbs if t.get("is_preferred")), thumbs[0]["uri"])
    return vid, thumb


def leer_estado(cli):
    print("\n── Estado leído de Meta ──")
    for cid in (CAMP_CONOCER, CAMP_VENDER):
        c = get(cli, cid, fields="name,status,effective_status")
        print(f"campaña  {c['effective_status']:<16} {c['name']}")
    for sid in (SET_CONOCER, SET_VENDER, *APAGAR):
        s = get(cli, sid, fields="name,status,effective_status,daily_budget")
        print(f"conjunto {s['effective_status']:<16} US${int(s.get('daily_budget') or 0) / 100:>5.2f}/día  {s['name']}")
    for sid in (SET_CONOCER, SET_VENDER):
        for a in get(cli, f"{sid}/ads", fields="name,status,effective_status", limit=50).get("data", []):
            print(f"  anuncio {a['effective_status']:<16} {a['name']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="ejecuta en Meta (sin esto, sólo muestra el plan)")
    args = ap.parse_args()

    print("Plan:")
    for plan, titulo, _ in VIDEOS:
        print(f"  subir {plan}-v5-9x16.mp4 → anuncio dark post «{titulo}» → {landing(plan + '-video')}")
    print(f"  prender paso 1 (reel Camille) a US${PRESUPUESTO_CONOCER / 100:.2f}/día y paso 2 a US${PRESUPUESTO_VENDER / 100:.2f}/día")
    for sid, nombre in APAGAR.items():
        print(f"  apagar {nombre} ({sid})")

    with httpx.Client(timeout=120) as cli:
        if not args.send:
            leer_estado(cli)
            print("\nNo se escribió nada. Correr con --send para ejecutar.")
            return

        # 1-2. Videos y anuncios (en pausa hasta el final, para prender todo junto)
        nuevos = {}
        for plan, titulo, texto in VIDEOS:
            nombre = f"membresia {plan} | video jose | vio reel | web | oct-26"
            ya = anuncio_existente(cli, nombre)
            if ya:
                nuevos[plan] = ya
                continue
            vid, thumb = subir_video(cli, plan)
            cr = post(cli, f"{CUENTA}/adcreatives", name=f"membresia {plan} | video jose | web",
                      object_story_spec={"page_id": PAGE, "instagram_user_id": IG, "video_data": {
                          "video_id": vid, "image_url": thumb, "message": texto, "title": titulo,
                          "call_to_action": {"type": "LEARN_MORE", "value": {"link": landing(f"{plan}-video")}}}},
                      # Que Meta no le ponga música, texto ni recortes por su cuenta: el video
                      # ya tiene su voz, su música y sus subtítulos.
                      degrees_of_freedom_spec={"creative_features_spec": {
                          "audio": {"enroll_status": "OPT_OUT"},
                          "add_text_overlay": {"enroll_status": "OPT_OUT"},
                          "text_optimizations": {"enroll_status": "OPT_OUT"},
                          "video_auto_crop": {"enroll_status": "OPT_OUT"}}})["id"]
            nuevos[plan] = post(cli, f"{CUENTA}/ads", name=nombre, adset_id=SET_VENDER,
                                status="PAUSED", creative={"creative_id": cr})["id"]
            print(f"  creado {nombre}: video {vid}, creativo {cr}, anuncio {nuevos[plan]}")

        # 3. Presupuestos y encendido del embudo
        post(cli, SET_CONOCER, daily_budget=PRESUPUESTO_CONOCER)
        post(cli, SET_VENDER, daily_budget=PRESUPUESTO_VENDER)
        for oid in (AD_CONOCER, *ADS_POSTEOS, *nuevos.values(), SET_CONOCER, SET_VENDER, CAMP_CONOCER, CAMP_VENDER):
            post(cli, oid, status="ACTIVE")

        # 4. Apagar lo que ya no se vende suelto
        for sid in APAGAR:
            post(cli, sid, status="PAUSED")

        # 5. Verificar contra Meta
        leer_estado(cli)


if __name__ == "__main__":
    main()
