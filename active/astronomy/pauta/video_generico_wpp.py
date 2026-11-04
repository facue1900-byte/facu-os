#!/usr/bin/env python3
"""Suma el video genérico de la academia al conjunto de WhatsApp activo (Facu, OK 04/11/2026).

No crea conjunto ni toca presupuesto: entra como un anuncio más dentro de lo que ya gasta el
conjunto. El mensaje autocompletado «(video general)» deja contar sus chats aparte.

    .venv/bin/python active/astronomy/pauta/video_generico_wpp.py          # lo crea en PAUSA
    .venv/bin/python active/astronomy/pauta/video_generico_wpp.py --send   # y lo prende

Correrlo dos veces no duplica. Relee de Meta y sale 1 si algo no quedó como se pidió.
"""
import json
import pathlib
import sys
import time

import httpx

from crear_embudo_membresias import CUENTA, IG, PAGE, TOKEN, VERSION, bienvenida, existente, post
from membresias_a_whatsapp import cambiar, leer

CARPETA = pathlib.Path.home() / ("Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/"
                                 "Reels-a-mano/05-generico-membresia")
VIDEO, PORTADA = CARPETA / "generico-sin-capcut.mp4", CARPETA / "portada.jpg"
CONJUNTO = "120249512338470448"
PRESUPUESTO = 1200                       # centavos: el script no lo cambia, sólo lo controla
NOMBRE_AD = "membresia general | video chica | wpp | nov-26"
AUTOFILL = "Hola! Quiero info de las membresías (video general)"
TITULO = "Membresía Astronomy"
TEXTO = ("Clases de DJ y producción en nuestro estudio de Nordelta. Pagás una membresía, "
         "tenés créditos y venís el día que te pinte.")
BASE = f"https://graph.facebook.com/{VERSION}"


def subir_video(cli):
    r = cli.post(f"{BASE}/{CUENTA}/advideos", data={"access_token": TOKEN, "name": NOMBRE_AD},
                 files={"source": (VIDEO.name, VIDEO.read_bytes(), "video/mp4")}, timeout=600).json()
    if "id" not in r:
        sys.exit(f"Meta no aceptó el video: {r}")
    for _ in range(40):  # un creativo con un video sin procesar falla
        st = cli.get(f"{BASE}/{r['id']}", params={"fields": "status", "access_token": TOKEN}).json()
        if st.get("status", {}).get("video_status") == "ready":
            return r["id"]
        time.sleep(15)
    sys.exit(f"El video {r['id']} no terminó de procesarse: {st}")


def subir_portada(cli):
    r = cli.post(f"{BASE}/{CUENTA}/adimages", data={"access_token": TOKEN},
                 files={"filename": (PORTADA.name, PORTADA.read_bytes(), "image/jpeg")}).json()
    try:
        return next(iter(r["images"].values()))["hash"]
    except (KeyError, StopIteration):
        sys.exit(f"Meta no aceptó la portada: {r}")


def main():
    enviar = "--send" in sys.argv
    with httpx.Client(timeout=120) as cli:
        ad = existente(cli, f"{CUENTA}/ads", NOMBRE_AD)
        if not ad:
            spec = {"page_id": PAGE, "instagram_user_id": IG, "video_data": {
                "video_id": subir_video(cli), "title": TITULO, "message": TEXTO,
                "image_hash": subir_portada(cli),
                "call_to_action": {"type": "WHATSAPP_MESSAGE",
                                   "value": {"app_destination": "WHATSAPP",
                                             "link": "https://api.whatsapp.com/send"}}}}
            cr = post(cli, f"{CUENTA}/adcreatives", name=NOMBRE_AD, object_story_spec=spec,
                      page_welcome_message=bienvenida(AUTOFILL))
            ad = post(cli, f"{CUENTA}/ads", name=NOMBRE_AD, adset_id=CONJUNTO, status="PAUSED",
                      creative={"creative_id": cr})
        if enviar:
            cambiar(cli, ad, status="ACTIVE")

        r = leer(cli, ad, "name,status,effective_status,creative{object_story_spec,asset_feed_spec}")
        c = leer(cli, CONJUNTO, "name,status,effective_status,daily_budget")
        crudo = json.dumps(r["creative"], ensure_ascii=False)
        print(json.dumps({"ad": ad, "status": r["status"], "effective": r["effective_status"],
                          "conjunto": c["status"], "presupuesto_centavos": c["daily_budget"]}))
        mal = []
        if r["status"] != ("ACTIVE" if enviar else "PAUSED"):
            mal.append(f"anuncio en {r['status']}")
        if c["status"] != "ACTIVE":
            mal.append(f"conjunto en {c['status']}")
        if int(c["daily_budget"]) != PRESUPUESTO:
            mal.append(f"presupuesto {c['daily_budget']}, esperado {PRESUPUESTO}")
        if TEXTO not in crudo:
            mal.append("el texto no quedó en el creativo")
        if mal:
            sys.exit("; ".join(mal))
        print("ANUNCIO_OK" if enviar else "Creado en PAUSA. Para prenderlo: --send")


if __name__ == "__main__":
    main()
