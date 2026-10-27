#!/usr/bin/env python3
"""Sube un reel a @astronomy.academy por la API de Instagram (token de `instagram_cuenta`).

Sin --send: crea el contenedor, sube el video y espera a que Instagram lo procese (FINISHED),
pero NO publica — el contenedor queda listo y vence a las 24 h. Con --send, además publica y
relee el posteo de Instagram.

    .venv/bin/python active/astronomy/contenido/publicar_reel.py VIDEO.mp4 --texto TEXTO.txt [--prueba auto|manual] [--send]

--prueba: reel de prueba (sólo a no seguidores). `auto` = Instagram lo pasa a los seguidores si
rinde bien en 72 h (graduation_strategy=SS_PERFORMANCE); `manual` = lo pasás vos desde la app.
"""
import argparse
import json
import os
import pathlib
import sys
import time

import httpx

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "pauta"))
import reporte_embudo as base  # noqa: E402  (sql() contra la base de Astronomy, qeakrjnseboiulcojlcw)

API = "https://graph.instagram.com/v23.0"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--texto", required=True, help="archivo con el caption")
    ap.add_argument("--prueba", choices=["auto", "manual"])
    ap.add_argument("--send", action="store_true")
    a = ap.parse_args()
    video = pathlib.Path(a.video)
    caption = pathlib.Path(a.texto).read_text().strip()

    with httpx.Client(timeout=120) as cli:
        tok = base.sql(cli, "select token from instagram_cuenta where usuario='astronomy.academy'")[0]["token"]
        yo = cli.get(f"{API}/me", params={"fields": "id,username", "access_token": tok}).json()
        if yo.get("username") != "astronomy.academy":
            sys.exit(f"El token no es de @astronomy.academy: {yo}")

        # Con login de Instagram la API no acepta subida directa: pide un link. El video va a un bucket
        # privado temporal de Supabase y se pasa un link firmado de 1 h; al final se borra todo.
        sb, sbh = storage()
        nombre = f"{int(time.time())}-{video.name.replace(' ', '_')}"
        try:
            r = cli.post(f"{sb}/storage/v1/bucket", headers=sbh,
                         json={"id": BUCKET, "name": BUCKET, "public": False, "file_size_limit": 50 * 1024 * 1024})
            if r.status_code >= 300 and "already exists" not in r.text:
                sys.exit(f"No se pudo crear el bucket temporal: {r.text}")
            r = cli.post(f"{sb}/storage/v1/object/{BUCKET}/{nombre}", content=video.read_bytes(),
                         headers={**sbh, "content-type": "video/mp4"})
            if r.status_code >= 300:
                sys.exit(f"No se pudo subir el video al storage: {r.text}")
            firmado = cli.post(f"{sb}/storage/v1/object/sign/{BUCKET}/{nombre}", headers=sbh, json={"expiresIn": 3600}).json()
            link = f"{sb}/storage/v1{firmado['signedURL']}"
            print(f"video en storage temporal ({video.stat().st_size / 1e6:.1f} MB)")

            datos = {"media_type": "REELS", "video_url": link, "caption": caption, "access_token": tok}
            if a.prueba:
                datos["trial_params"] = json.dumps({"graduation_strategy": "SS_PERFORMANCE" if a.prueba == "auto" else "MANUAL"})
            c = cli.post(f"{API}/{yo['id']}/media", data=datos).json()
            if "id" not in c:
                sys.exit(f"Instagram no creó el contenedor: {c}")
            print("contenedor", c["id"])

            for _ in range(60):  # hasta 10 min
                st = cli.get(f"{API}/{c['id']}", params={"fields": "status_code,status", "access_token": tok}).json()
                if st.get("status_code") in ("FINISHED", "ERROR", "EXPIRED"):
                    break
                time.sleep(10)
            print("estado", st)
            if st.get("status_code") != "FINISHED":
                sys.exit("Instagram no terminó de procesar el video: no se publica.")
            if not a.send:
                print(f"Listo para publicar, SIN publicar. Para publicarlo: --send (contenedor {c['id']}, vence en 24 h).")
                return

            pub = cli.post(f"{API}/{yo['id']}/media_publish", data={"creation_id": c["id"], "access_token": tok}).json()
            if "id" not in pub:
                sys.exit(f"Instagram no publicó: {pub}")
            m = cli.get(f"{API}/{pub['id']}", params={
                "fields": "id,permalink,media_product_type,timestamp,caption", "access_token": tok}).json()
            print("PUBLICADO", json.dumps(m, ensure_ascii=False, indent=1))
        finally:
            cli.request("DELETE", f"{sb}/storage/v1/object/{BUCKET}", headers=sbh, json={"prefixes": [nombre]})
            r = cli.delete(f"{sb}/storage/v1/bucket/{BUCKET}", headers=sbh)
            print("storage temporal borrado" if r.status_code < 300 else f"OJO: quedó el bucket {BUCKET}: {r.text}")


BUCKET = "reels-temp"


def storage():
    """URL y headers del storage de Supabase de Astronomy (service role del .env.local de la app)."""
    from dotenv import dotenv_values
    e = dotenv_values("/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members/.env.local")
    url = e["NEXT_PUBLIC_SUPABASE_URL"]
    if "qeakrjnseboiulcojlcw" not in url:
        sys.exit(f"El storage no es el de Astronomy: {url}")
    k = e["SUPABASE_SERVICE_ROLE_KEY"]
    return url, {"Authorization": f"Bearer {k}", "apikey": k}


if __name__ == "__main__":
    main()
