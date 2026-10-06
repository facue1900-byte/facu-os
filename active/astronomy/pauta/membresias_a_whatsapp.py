#!/usr/bin/env python3
"""Los 3 posteos de membresía pasan de la web a WhatsApp (Facu, 06/10/2026).

Por qué: del 1 al 6/10 los posteos con destino web (objetivo Tráfico) compraron 413 clics
a US$0,04 y trajeron 2 contactos de WhatsApp y 0 cuentas. La landing se midió y carga
bien (2,3 s en iPhone/Instagram con 4G lento): el problema es que el objetivo «Tráfico»
compra gente que toca sin intención. Ver memoria `landing-no-era-la-landing`.

Qué hace:
  1. Crea (en PAUSA) campaña + conjunto de conversaciones de WhatsApp con el mismo público
     (vio 15 s del reel de Camille, 60 d, Advantage+ apagado) y los 3 posteos, cada uno con
     su mensaje autocompletado → el chat dice de qué membresía viene.
  2. Con --send:
     · pausa los 3 posteos que mandan a la web (los 3 videos de José, «Comentá SILVER»,
       siguen igual: Facu pidió dejarlos);
     · reel de Camille US$12 → US$9 y WhatsApp US$3 (el reparto de la semana 2 del plan de
       octubre: reel 9 / membresías 6, con el público ya en +10.000). Total sigue US$15/día;
     · prende campaña, conjunto y anuncios nuevos;
     · relee todo de Meta y sale 1 si algo no quedó como se pidió.

    .venv/bin/python active/astronomy/pauta/membresias_a_whatsapp.py          # sólo crea en pausa
    .venv/bin/python active/astronomy/pauta/membresias_a_whatsapp.py --send   # y lo prende
"""

import json
import sys

import httpx

from crear_embudo_membresias import (CUENTA, IG, MEMBRESIAS, PAGE, PUBLICO_VIO_REEL, TOKEN,
                                     VERSION, WHATSAPP, asegurar, bienvenida, existente, post)

POSTEOS_WEB = {  # los que se pausan
    "silver": "120249329920240448",
    "gold": "120249329921030448",
    "platinum": "120249329924850448",
}
VIDEOS_JOSE = ["120249372348700448", "120249372356490448", "120249372367740448"]  # NO se tocan
CONJUNTO_CAMILLE = "120249329518130448"
PRESUPUESTO_CAMILLE = 900   # centavos de USD por día
PRESUPUESTO_WPP = 300


def cambiar(cli, oid, **data):
    """Un update de Meta devuelve {"success": true}, no un id: `post` es para crear."""
    data["access_token"] = TOKEN
    r = cli.post(f"https://graph.facebook.com/{VERSION}/{oid}", data=data).json()
    if not r.get("success"):
        raise SystemExit(f"{oid}: {r.get('error', {}).get('error_user_msg') or r}")


def leer(cli, oid, campos):
    return cli.get(f"https://graph.facebook.com/{VERSION}/{oid}",
                   params={"fields": campos, "access_token": TOKEN}).json()


def main():
    enviar = "--send" in sys.argv
    with httpx.Client(timeout=60) as cli:
        camp = asegurar(cli, f"{CUENTA}/campaigns", name="Membresias | vio reel Camille | wpp | oct-26",
                        objective="OUTCOME_ENGAGEMENT", status="PAUSED", special_ad_categories=[],
                        is_adset_budget_sharing_enabled=False)
        conj = asegurar(cli, f"{CUENTA}/adsets", name="Membresias | Vio reel Camille 15s | wpp | oct-26",
                        campaign_id=camp, status="PAUSED", daily_budget=PRESUPUESTO_WPP,
                        billing_event="IMPRESSIONS", optimization_goal="CONVERSATIONS",
                        destination_type="WHATSAPP", bid_strategy="LOWEST_COST_WITHOUT_CAP",
                        promoted_object={"page_id": PAGE, "whatsapp_phone_number": WHATSAPP},
                        targeting={"geo_locations": {"countries": ["AR"]}, "age_min": 18, "age_max": 65,
                                   "custom_audiences": [{"id": PUBLICO_VIO_REEL}],
                                   "targeting_automation": {"advantage_audience": 0}})
        ads = {}
        for nombre, media, mensaje in MEMBRESIAS:
            nombre_ad = f"membresia {nombre} | post IG | vio reel | wpp | oct-26"
            ad = existente(cli, f"{CUENTA}/ads", nombre_ad)
            if not ad:
                cr = post(cli, f"{CUENTA}/adcreatives", name=f"membresia {nombre} | post IG | wpp | oct-26",
                          object_id=PAGE, instagram_user_id=IG, source_instagram_media_id=media,
                          call_to_action={"type": "WHATSAPP_MESSAGE",
                                          "value": {"app_destination": "WHATSAPP",
                                                    "link": "https://api.whatsapp.com/send"}},
                          page_welcome_message=bienvenida(mensaje))
                ad = post(cli, f"{CUENTA}/ads", name=nombre_ad, adset_id=conj, status="PAUSED",
                          creative={"creative_id": cr})
            ads[nombre] = ad
        print(json.dumps({"campaign": camp, "adset": conj, "ads": ads}, indent=1))

        if not enviar:
            print("Creado en PAUSA. Para prenderlo: --send")
            return

        for ad in POSTEOS_WEB.values():
            cambiar(cli, ad, status="PAUSED")
        cambiar(cli, CONJUNTO_CAMILLE, daily_budget=PRESUPUESTO_CAMILLE)
        cambiar(cli, camp, status="ACTIVE")
        cambiar(cli, conj, status="ACTIVE")
        for ad in ads.values():
            cambiar(cli, ad, status="ACTIVE")

        # Releer de Meta: lo que importa es lo que quedó, no lo que se mandó.
        esperado = {**{a: "PAUSED" for a in POSTEOS_WEB.values()},
                    **{a: "ACTIVE" for a in VIDEOS_JOSE},
                    **{a: "ACTIVE" for a in ads.values()}, camp: "ACTIVE", conj: "ACTIVE"}
        mal = []
        for oid, st in esperado.items():
            r = leer(cli, oid, "name,status,effective_status")
            ok = r.get("status") == st
            print(f"{'OK ' if ok else 'MAL'} {r.get('name')} → {r.get('status')} / {r.get('effective_status')}")
            if not ok:
                mal.append(oid)
        for oid, centavos in [(CONJUNTO_CAMILLE, PRESUPUESTO_CAMILLE), (conj, PRESUPUESTO_WPP),
                              ("120249329919700448", 300)]:
            r = leer(cli, oid, "name,daily_budget")
            ok = int(r.get("daily_budget", 0)) == centavos
            print(f"{'OK ' if ok else 'MAL'} {r.get('name')} → US${int(r.get('daily_budget', 0)) / 100:.2f}/día")
            if not ok:
                mal.append(oid)
        if mal:
            sys.exit(f"{len(mal)} cosa(s) no quedaron como se pidió: {mal}")


if __name__ == "__main__":
    main()
