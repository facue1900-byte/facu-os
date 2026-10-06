#!/usr/bin/env python3
"""Pauta de Academy: 18 a 34 años y sólo 20 km de Nordelta (Facu, 06/10/2026).

Del 1 al 6/10 el reel de Camille gastó el 46% en mayores de 45: llena el público
«vio reel» con padres de Nordelta, no con chicos. Y los conjuntos de membresía salían a
todo el país (Chaco, Tucumán…) porque tenían `targeting_relaxation_types.custom_audience=1`,
que deja a Meta salir del público. Facu: «lo ideal es que venga gente copada, canchera,
de la edad de la zona» → 18–34, 20 km, sin relajación.

    .venv/bin/python active/astronomy/pauta/ajustar_publico.py          # muestra lo que cambiaría
    .venv/bin/python active/astronomy/pauta/ajustar_publico.py --send   # lo aplica y lo relee
"""

import json
import sys

import httpx

from crear_embudo_membresias import NORDELTA_20KM, PUBLICO_VIO_REEL, TOKEN, VERSION

EDAD_MIN, EDAD_MAX = 18, 34

BASE = {
    "age_min": EDAD_MIN, "age_max": EDAD_MAX,
    "geo_locations": {**NORDELTA_20KM, "location_types": ["home", "recent"]},
    "targeting_automation": {"advantage_audience": 0},
}
CONJUNTOS = {
    "120249329518130448": BASE,  # Reel Camille | Nordelta 20km | ThruPlay
    "120249329919700448": {**BASE, "custom_audiences": [{"id": PUBLICO_VIO_REEL}],   # videos «Comentá» (web)
                           "targeting_relaxation_types": {"lookalike": 0, "custom_audience": 0}},
    "120249450575100448": {**BASE, "custom_audiences": [{"id": PUBLICO_VIO_REEL}],   # posteos → WhatsApp
                           "targeting_relaxation_types": {"lookalike": 0, "custom_audience": 0}},
}


def leer(cli, oid):
    return cli.get(f"https://graph.facebook.com/{VERSION}/{oid}",
                   params={"fields": "name,targeting,effective_status", "access_token": TOKEN}).json()


def main():
    enviar = "--send" in sys.argv
    mal = []
    with httpx.Client(timeout=60) as cli:
        for oid, t in CONJUNTOS.items():
            antes = leer(cli, oid)
            ta = antes.get("targeting", {})
            print(f"{antes.get('name')}: {ta.get('age_min')}-{ta.get('age_max')} · "
                  f"geo {list(ta.get('geo_locations', {}).keys())} · relajación {ta.get('targeting_relaxation_types')}")
            if not enviar:
                continue
            r = cli.post(f"https://graph.facebook.com/{VERSION}/{oid}",
                         data={"targeting": json.dumps(t), "access_token": TOKEN}).json()
            if not r.get("success"):
                print("   ERROR:", r.get("error", {}).get("error_user_msg") or r)
                mal.append(oid)
                continue
            d = leer(cli, oid)["targeting"]
            ok = (d.get("age_min") == EDAD_MIN and d.get("age_max") == EDAD_MAX
                  and "countries" not in d.get("geo_locations", {})
                  and d.get("geo_locations", {}).get("custom_locations", [{}])[0].get("radius") == 20
                  and (d.get("targeting_relaxation_types") or {}).get("custom_audience", 0) == 0)
            print(f"   {'OK ' if ok else 'MAL'} → {d.get('age_min')}-{d.get('age_max')} · "
                  f"{d['geo_locations'].get('custom_locations', [{}])[0].get('radius')} km · "
                  f"relajación {d.get('targeting_relaxation_types')} · público {[a['id'] for a in d.get('custom_audiences', [])]}")
            if not ok:
                mal.append(oid)
    if not enviar:
        print("Nada cambió. Para aplicarlo: --send")
    if mal:
        sys.exit(f"{len(mal)} conjunto(s) no quedaron como se pidió: {mal}")


if __name__ == "__main__":
    main()
