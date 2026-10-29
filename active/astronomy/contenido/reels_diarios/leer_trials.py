#!/usr/bin/env python3
"""Lee cómo rindieron los reels de los últimos N días en @astronomy.academy y escribe
resultados.json, que el agente diario usa para repetir lo que funciona y cortar lo que no.

    .venv/bin/python active/astronomy/contenido/reels_diarios/leer_trials.py [--dias 14]

Por reel: vistas, alcance, likes, compartidos, guardados, tiempo medio de visualización y si ya
pasó al feed. Lee TODOS los reels del período (también los de prueba del 27/10, que son
anteriores a este sistema) y les pega formato y tema desde registro.jsonl cuando los tiene.
Un reel con menos de 72 h todavía está en prueba: se marca `en_prueba` y no se juzga.
"""
import argparse
import datetime
import json
import sys

import httpx

from comun import AQUI, OS, registro

sys.path.insert(0, str(OS / "active/astronomy/pauta"))
import reporte_embudo as base  # noqa: E402

API = "https://graph.instagram.com/v23.0"
METRICAS = "views,reach,likes,comments,shares,saved,ig_reels_avg_watch_time"
SALIDA = AQUI / "resultados.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=14)
    a = ap.parse_args()
    desde = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=a.dias)
    por_id = {r["media_id"]: r for r in registro()}
    # Se borra antes de leer: si esta lectura falla, el agente no puede decidir con la de ayer.
    SALIDA.unlink(missing_ok=True)
    filas, salteados = [], []
    with httpx.Client(timeout=60) as cli:
        tok = base.sql(cli, "select token from instagram_cuenta where usuario='astronomy.academy'")[0]["token"]
        url, params = f"{API}/me/media", {
            "fields": "id,permalink,timestamp,media_product_type,is_shared_to_feed,caption", "limit": 50, "access_token": tok}
        medios = []
        while url:
            r = cli.get(url, params=params).json()
            if "error" in r:
                sys.exit(f"LEER_FALLA: {r['error']}")
            medios += r.get("data", [])
            ultimo = medios[-1]["timestamp"] if medios else None
            if not ultimo or datetime.datetime.fromisoformat(ultimo.replace("+0000", "+00:00")) < desde:
                break
            url, params = r.get("paging", {}).get("next"), None
        for m in medios:
            ts = datetime.datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
            if ts < desde or m.get("media_product_type") != "REELS":
                continue
            ins = cli.get(f"{API}/{m['id']}/insights", params={"metric": METRICAS, "access_token": tok}).json()
            if "error" in ins:
                salteados.append({"permalink": m["permalink"], "error": ins["error"].get("message")})
                continue
            # Una métrica que no vino queda en None («n/d»), nunca en 0.
            val = {k: None for k in METRICAS.split(",")}
            val.update({d["name"]: d["values"][0]["value"] for d in ins.get("data", [])})
            reg = por_id.get(m["id"], {})
            horas = (datetime.datetime.now(datetime.timezone.utc) - ts).total_seconds() / 3600
            filas.append({
                "permalink": m["permalink"], "publicado": m["timestamp"], "horas": round(horas),
                "en_prueba": horas < 72, "paso_al_feed": m.get("is_shared_to_feed"),
                "formato": reg.get("formato", "(anterior al sistema: ver caption)"),
                "slug": reg.get("slug"), "tema": reg.get("tema"),
                "caption": (m.get("caption") or "")[:90],
                **val,
            })
    if not filas:
        sys.exit(f"LEER_FALLA: no encontré ningún reel en los últimos {a.dias} días — eso no puede ser cero.")
    filas.sort(key=lambda f: -(f.get("views") or 0))
    SALIDA.write_text(json.dumps({"leido": datetime.datetime.now().isoformat(timespec="minutes"),
                                  "reels": filas, "salteados": salteados}, ensure_ascii=False, indent=1))
    nd = lambda v: "n/d" if v is None else v  # noqa: E731
    for f in filas:
        print(f"{nd(f['views']):>7} vistas {nd(f['reach']):>6} alcance {nd(f['shares']):>3} comp "
              f"{nd(f['saved']):>3} guard {f['horas']:>4}h {'PRUEBA' if f['en_prueba'] else ''} {f['permalink']}")
    for x in salteados:
        print(f"SIN DATOS {x['permalink']}: {x['error']}")
    print(f"LEER_OK {len(filas)} reels ({len(salteados)} sin datos) → {SALIDA}")


if __name__ == "__main__":
    main()
