#!/usr/bin/env python3
"""La plata vuelve a comprar conversaciones de WhatsApp (Facu, 26/10/2026).

Por qué: en septiembre la cuenta optimizaba por conversación (US$444 → 289 chats) y entraron 6
alumnos nuevos. Desde el 01/10, US$9 de US$12/día fueron al reel de Camille optimizando ThruPlay
(llenar un público): los chats cayeron de 5-20/día a 0-3 y al 25/10 octubre lleva US$335 y 0
alumnos nuevos (primera compra en sales ∪ payment_links ∪ manual_payments).

Qué hace con --send:
  · pausa el conjunto del reel de Camille (ThruPlay, US$9/día);
  · el conjunto de los videos de José → WhatsApp pasa de US$3 a US$12/día y deja de estar
    restringido al público «vio Camille 95% o José 50%» (~3.000 personas: a US$12/día se
    quema en frecuencia y, sin el reel, deja de crecer). Queda Nordelta 20 km, 18-34, sin
    Advantage+ ni relajación. El autofill «… (video)» no cambia: los chats se siguen atribuyendo.
  · relee todo de Meta y sale 1 si algo no quedó como se pidió.
El total de la cuenta sigue en US$12/día.

    .venv/bin/python active/astronomy/pauta/volver_a_conversaciones.py          # muestra el antes
    .venv/bin/python active/astronomy/pauta/volver_a_conversaciones.py --send   # y lo cambia
"""

import json
import sys

import httpx

from membresias_a_whatsapp import cambiar, leer

REEL_CAMILLE = "120249329518130448"      # «Reel Camille | Nordelta 20km | ThruPlay»
VIDEOS_JOSE = "120249512338470448"       # «Membresias | Camille 95% o José 50% | video jose | wpp | oct-26»
PRESUPUESTO = 1200                       # centavos de USD por día


def main():
    enviar = "--send" in sys.argv
    with httpx.Client(timeout=60) as cli:
        antes = {oid: leer(cli, oid, "name,status,daily_budget,targeting") for oid in (REEL_CAMILLE, VIDEOS_JOSE)}
        for r in antes.values():
            print(f"ANTES {r['name']} → {r['status']} · US${int(r['daily_budget']) / 100:.2f}/día · "
                  f"públicos {[a['name'] for a in r['targeting'].get('custom_audiences', [])]}")
        if not enviar:
            print("Nada cambiado. Para aplicarlo: --send")
            return

        t = antes[VIDEOS_JOSE]["targeting"]
        targeting = {"geo_locations": t["geo_locations"], "age_min": t["age_min"], "age_max": t["age_max"],
                     "targeting_automation": {"advantage_audience": 0}}
        cambiar(cli, REEL_CAMILLE, status="PAUSED")
        cambiar(cli, VIDEOS_JOSE, daily_budget=PRESUPUESTO, targeting=json.dumps(targeting))

        # Releer de Meta: lo que importa es lo que quedó, no lo que se mandó.
        mal = []
        r = leer(cli, REEL_CAMILLE, "name,status")
        ok = r.get("status") == "PAUSED"
        print(f"{'OK ' if ok else 'MAL'} {r['name']} → {r.get('status')}")
        mal += [] if ok else [REEL_CAMILLE]
        r = leer(cli, VIDEOS_JOSE, "name,status,effective_status,daily_budget,targeting")
        tg = r["targeting"]
        ok = (r.get("status") == "ACTIVE" and int(r.get("daily_budget", 0)) == PRESUPUESTO
              and not tg.get("custom_audiences") and tg.get("age_min") == 18 and tg.get("age_max") == 34)
        print(f"{'OK ' if ok else 'MAL'} {r['name']} → {r.get('status')} / {r.get('effective_status')} · "
              f"US${int(r.get('daily_budget', 0)) / 100:.2f}/día · edad {tg.get('age_min')}-{tg.get('age_max')} · "
              f"radio {tg['geo_locations']['custom_locations'][0]['radius']} km · "
              f"públicos {[a['name'] for a in tg.get('custom_audiences', [])]}")
        mal += [] if ok else [VIDEOS_JOSE]
        if mal:
            sys.exit(f"{len(mal)} cosa(s) no quedaron como se pidió: {mal}")


if __name__ == "__main__":
    main()
