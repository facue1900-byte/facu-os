#!/usr/bin/env python3
"""Pauta de Academy: 18 a 40 años, 20 km de Nordelta, sólo gente relacionada al Instagram (Facu, 27/10/2026).

Facu: «18 a 40 años, 20 km alrededor de Nordelta, y que funcione para todos los relacionados
a nuestros followers, los que nos comentan… todos los que interactuaron con nuestro Instagram».

El conjunto de los videos de José a WhatsApp pasa a mostrarse SÓLO a:
  - quien interactuó con @astronomy.academy en los últimos 365 días (siguió, comentó, likeó,
    guardó, mandó DM, visitó el perfil). Meta no deja apuntar a «los que seguimos nosotros».
  - el público similar 1% de esa gente (los «relacionados»).
siempre dentro de 18–40 y 20 km, sin que Meta pueda salirse del público.

Los dos públicos se crearon el 27/10 y tardan horas en llenarse. Este script se niega a
aplicar el cambio si alguno todavía no está listo: un público vacío deja de gastar en silencio.

    .venv/bin/python active/astronomy/pauta/publico_instagram.py          # muestra hoy vs nuevo, con tamaño
    .venv/bin/python active/astronomy/pauta/publico_instagram.py --send   # lo aplica y lo relee
"""

import json
import sys

import httpx

from crear_embudo_membresias import NORDELTA_20KM, TOKEN, VERSION

B = f"https://graph.facebook.com/{VERSION}"
CONJUNTO = "120249512338470448"  # Membresias | Camille 95% o José 50% | video jose | wpp | oct-26
CUENTA = "act_628045479472592"
IG_INTERACTUO = "120249851923160448"  # IG @astronomy.academy | interactuó | 365d
SIMILAR = "120249851923170448"        # Similar 1% AR | IG interactuó 365d
EDAD_MIN, EDAD_MAX = 18, 40

NUEVO = {
    "age_min": EDAD_MIN, "age_max": EDAD_MAX,
    "geo_locations": {**NORDELTA_20KM, "location_types": ["home", "recent"]},
    "custom_audiences": [{"id": IG_INTERACTUO}, {"id": SIMILAR}],
    "targeting_relaxation_types": {"lookalike": 0, "custom_audience": 0},
    "targeting_automation": {"advantage_audience": 0},
}


def get(cli, path, **q):
    return cli.get(f"{B}/{path}", params={"access_token": TOKEN, **q}).json()


def tamano(cli, t):
    d = get(cli, f"{CUENTA}/delivery_estimate", optimization_goal="CONVERSATIONS", targeting_spec=json.dumps(t))
    d = (d.get("data") or [{}])[0]
    return d.get("estimate_mau_lower_bound"), d.get("estimate_mau_upper_bound")


def main():
    enviar = "--send" in sys.argv
    with httpx.Client(timeout=60) as cli:
        antes = get(cli, CONJUNTO, fields="name,targeting,effective_status")
        ta = antes["targeting"]
        print(f"{antes['name']} ({antes['effective_status']})")
        print(f"  hoy:   {ta.get('age_min')}-{ta.get('age_max')} · 20 km · públicos "
              f"{[a['id'] for a in ta.get('custom_audiences', [])] or 'ninguno (abierto)'} · tamaño {tamano(cli, ta)}")
        listos = True
        for aid in (IG_INTERACTUO, SIMILAR):
            a = get(cli, aid, fields="name,approximate_count_lower_bound,delivery_status")
            ok = (a.get("delivery_status") or {}).get("code") == 200
            listos &= ok
            print(f"  {a['name']}: ~{a.get('approximate_count_lower_bound')} personas · "
                  f"{'LISTO' if ok else (a.get('delivery_status') or {}).get('description')}")
        print(f"  nuevo: {EDAD_MIN}-{EDAD_MAX} · 20 km · sólo IG interactuó + similar 1% · tamaño {tamano(cli, NUEVO)}")
        if not enviar:
            print("Nada cambió. Para aplicarlo: --send")
            return
        if not listos:
            sys.exit("NO SE APLICÓ: algún público todavía se está llenando. Probar en unas horas.")
        r = cli.post(f"{B}/{CONJUNTO}", data={"targeting": json.dumps(NUEVO), "access_token": TOKEN}).json()
        if not r.get("success"):
            sys.exit(f"ERROR: {r.get('error', {}).get('error_user_msg') or r}")
        d = get(cli, CONJUNTO, fields="targeting")["targeting"]
        ok = (d.get("age_min") == EDAD_MIN and d.get("age_max") == EDAD_MAX
              and d["geo_locations"].get("custom_locations", [{}])[0].get("radius") == 20
              and {a["id"] for a in d.get("custom_audiences", [])} == {IG_INTERACTUO, SIMILAR}
              and (d.get("targeting_relaxation_types") or {}).get("custom_audience", 0) == 0)
        print(f"  {'OK' if ok else 'MAL'} releído de Meta: {d.get('age_min')}-{d.get('age_max')} · "
              f"públicos {[a['id'] for a in d.get('custom_audiences', [])]}")
        if not ok:
            sys.exit("El conjunto no quedó como se pidió.")


if __name__ == "__main__":
    main()
