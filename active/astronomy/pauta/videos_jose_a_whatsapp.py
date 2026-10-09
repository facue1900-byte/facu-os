#!/usr/bin/env python3
"""Los 3 videos de José pasan de la web a WhatsApp, con un público más filtrado (Facu, 09/10/2026).

Por qué: del 1 al 9/10 la web recibió 572 visitas pagas (posteos + videos) y 0 cuentas, y los
3 posteos de membresía a WhatsApp trajeron 1 conversación por US$8. Facu: «los posteos no
están vendiendo, no está muy clara la info»; quería pautarle sólo a los que vieron los
videos de José, pero ese público son ~300 personas (271 al 50%), chico para que Meta entregue.
Se arma el mismo filtro con tamaño útil:

    vio el reel de Camille al 95%   (~1.456)
  o vio un video de José al 50%     (~271, y crece mientras los videos corran)

Qué hace:
  1. Crea los 2 públicos de video (60 días) y, EN PAUSA, un conjunto de conversaciones de
     WhatsApp en la campaña de membresías wpp con esos públicos, Nordelta 20 km, 18-34
     (la segmentación que ya tiene el conjunto de posteos), US$3/día, y los 3 videos de José
     con botón de WhatsApp y mensaje autocompletado «… (video)» → el chat dice de dónde viene.
  2. Con --send:
     · pausa los 3 posteos de membresía a WhatsApp y su conjunto;
     · pausa el conjunto web de los videos de José (US$3/día): la plata pasa al nuevo;
     · prende el conjunto y los anuncios nuevos;
     · relee todo de Meta y sale 1 si algo no quedó como se pidió.
  El reel de Camille (US$9/día) no se toca. La cuenta pasa de US$15/día a US$12/día: se
  apagan los posteos (US$3) y los videos siguen con los mismos US$3.

    .venv/bin/python active/astronomy/pauta/videos_jose_a_whatsapp.py          # crea en pausa
    .venv/bin/python active/astronomy/pauta/videos_jose_a_whatsapp.py --send   # y lo prende
"""

import json
import sys

import httpx

from crear_embudo_membresias import CUENTA, IG, PAGE, WHATSAPP, asegurar, bienvenida, existente, post
from membresias_a_whatsapp import cambiar, leer

CAMPANIA_WPP = "120249450574320448"      # «Membresias | vio reel Camille | wpp | oct-26»
CONJUNTO_POSTEOS_WPP = "120249450575100448"
POSTEOS_WPP = ["120249450576240448", "120249450577760448", "120249450578730448"]
CONJUNTO_WEB_VIDEOS = "120249329919700448"
VIDEOS_JOSE_WEB = {  # anuncio web del que se copia el video, el título y el texto
    "silver": "120249372348700448",
    "gold": "120249372356490448",
    "platinum": "120249372367740448",
}
VIDEO_CAMILLE = "27848902684811760"      # el mismo objeto del público «Vio reel Camille (15s)»
PRESUPUESTO = 300                        # centavos de USD por día
NOMBRE_CONJUNTO = "Membresias | Camille 95% o José 50% | video jose | wpp | oct-26"


def publico(cli, nombre, evento, videos):
    """Público de video en el formato del que ya anda (`rule` con event_name/object_id)."""
    return asegurar(cli, f"{CUENTA}/customaudiences", name=nombre, subtype="ENGAGEMENT",
                    retention_days=60, prefill=True,
                    rule=[{"event_name": evento, "object_id": v} for v in videos])


def main():
    enviar = "--send" in sys.argv
    with httpx.Client(timeout=60) as cli:
        # Los videos de José para el público: el del POSTEO que generó cada anuncio
        # (`creative.video_id`). El advideo subido a la cuenta no sirve: Meta rechaza un público
        # de video que no esté asociado a la página (#2654, probado el 09/10/2026).
        piezas, videos_jose = {}, []
        for plan, ad in VIDEOS_JOSE_WEB.items():
            cr = leer(cli, ad, "creative{object_story_spec,video_id}")["creative"]
            vd = cr["object_story_spec"]["video_data"]
            piezas[plan] = vd
            videos_jose.append(cr.get("video_id"))
        videos_jose = [v for v in dict.fromkeys(videos_jose) if v]

        p_camille = publico(cli, "Vio reel Camille (95%) | 60d", "video_completed", [VIDEO_CAMILLE])
        p_jose = publico(cli, "Vio video José (50%) | 60d", "video_view_50_percent", videos_jose)

        # La segmentación del conjunto de posteos (Nordelta 20 km, 18-34), con los públicos nuevos.
        t = leer(cli, CONJUNTO_POSTEOS_WPP, "targeting")["targeting"]
        targeting = {"geo_locations": t["geo_locations"], "age_min": t["age_min"], "age_max": t["age_max"],
                     "custom_audiences": [{"id": p_camille}, {"id": p_jose}],
                     "targeting_automation": {"advantage_audience": 0}}
        conj = asegurar(cli, f"{CUENTA}/adsets", name=NOMBRE_CONJUNTO, campaign_id=CAMPANIA_WPP,
                        status="PAUSED", daily_budget=PRESUPUESTO, billing_event="IMPRESSIONS",
                        optimization_goal="CONVERSATIONS", destination_type="WHATSAPP",
                        bid_strategy="LOWEST_COST_WITHOUT_CAP",
                        promoted_object={"page_id": PAGE, "whatsapp_phone_number": WHATSAPP},
                        targeting=targeting)

        ads = {}
        for plan, vd in piezas.items():
            nombre_ad = f"membresia {plan} | video jose | camille95-jose50 | wpp | oct-26"
            ad = existente(cli, f"{CUENTA}/ads", nombre_ad)
            if not ad:
                spec = {"page_id": PAGE, "instagram_user_id": IG, "video_data": {
                    "video_id": vd["video_id"], "title": vd["title"], "message": vd["message"],
                    "image_hash": vd["image_hash"],
                    "call_to_action": {"type": "WHATSAPP_MESSAGE",
                                       "value": {"app_destination": "WHATSAPP",
                                                 "link": "https://api.whatsapp.com/send"}}}}
                cr = post(cli, f"{CUENTA}/adcreatives", name=f"membresia {plan} | video jose | wpp | oct-26",
                          object_story_spec=spec,
                          page_welcome_message=bienvenida(f"Hola! Quiero info de la membresía {plan.capitalize()} (video)"))
                ad = post(cli, f"{CUENTA}/ads", name=nombre_ad, adset_id=conj, status="PAUSED",
                          creative={"creative_id": cr})
            ads[plan] = ad

        print(json.dumps({"publicos": {"camille95": p_camille, "jose50": p_jose}, "videos_jose": videos_jose,
                          "adset": conj, "ads": ads}, indent=1))
        if not enviar:
            print("Creado en PAUSA. Para prenderlo: --send")
            return

        for oid in POSTEOS_WPP + [CONJUNTO_POSTEOS_WPP, CONJUNTO_WEB_VIDEOS]:
            cambiar(cli, oid, status="PAUSED")
        cambiar(cli, conj, status="ACTIVE")
        for ad in ads.values():
            cambiar(cli, ad, status="ACTIVE")

        # Releer de Meta: lo que importa es lo que quedó, no lo que se mandó.
        esperado = {**{a: "PAUSED" for a in POSTEOS_WPP}, CONJUNTO_POSTEOS_WPP: "PAUSED",
                    CONJUNTO_WEB_VIDEOS: "PAUSED", CAMPANIA_WPP: "ACTIVE", conj: "ACTIVE",
                    **{a: "ACTIVE" for a in ads.values()}}
        mal = []
        for oid, st in esperado.items():
            r = leer(cli, oid, "name,status,effective_status")
            ok = r.get("status") == st
            print(f"{'OK ' if ok else 'MAL'} {r.get('name')} → {r.get('status')} / {r.get('effective_status')}")
            if not ok:
                mal.append(oid)
        r = leer(cli, conj, "name,daily_budget,targeting")
        ok = int(r.get("daily_budget", 0)) == PRESUPUESTO
        print(f"{'OK ' if ok else 'MAL'} {r['name']} → US${int(r.get('daily_budget', 0)) / 100:.2f}/día · "
              f"públicos {[a['name'] for a in r['targeting'].get('custom_audiences', [])]}")
        if not ok:
            mal.append(conj)
        for p in (p_camille, p_jose):
            a = leer(cli, p, "name,approximate_count_lower_bound,approximate_count_upper_bound,delivery_status")
            print(f"    público {a.get('name')}: {a.get('approximate_count_lower_bound')}–"
                  f"{a.get('approximate_count_upper_bound')} · {a.get('delivery_status', {}).get('description')}")
        if mal:
            sys.exit(f"{len(mal)} cosa(s) no quedaron como se pidió: {mal}")


if __name__ == "__main__":
    main()
