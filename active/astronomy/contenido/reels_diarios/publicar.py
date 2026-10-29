#!/usr/bin/env python3
"""Publica como REEL DE PRUEBA un reel que armó armar_reel.py, y lo anota en registro.jsonl.

    .venv/bin/python active/astronomy/contenido/reels_diarios/publicar.py CARPETA [--send]

Sin --send deja el contenedor procesado en Instagram, sin publicar (igual que publicar_reel.py).
Corta si: el reel no pasó el QA (o el QA es más viejo que el reel), ya se publicó (misma carpeta,
mismo archivo o mismo slug), ya hay MAX_POR_DIA publicados hoy, o quedó un intento anterior a
medias (marca `pendiente.lock` sin renglón en el registro: puede estar publicado → lo mira una
persona).
Todo el chequeo-publicación-registro corre bajo un lock de archivo: dos llamadas en paralelo no
pueden pasarse del tope.

Autorización de Facu (28/10/2026): «subir los videos a instagram como trial reels» todos los
días. Vale SÓLO para reels de prueba; un reel directo al feed sigue necesitando su OK.
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

from comun import AQUI, OS, PY, REGISTRO, registro

MAX_POR_DIA = 10
LOCK = AQUI / ".publicar.lock"


def falla(msg):
    sys.exit(f"PUBLICAR_FALLA: {msg}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:20]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--send", action="store_true")
    a = ap.parse_args()
    c = pathlib.Path(a.carpeta).resolve()
    for f in ("reel.mp4", "portada.jpg", "texto-reel.txt", "guion.json", "qa.json", "revision.jpg"):
        if not (c / f).exists():
            falla(f"falta {f} en {c}")
    qa = json.loads((c / "qa.json").read_text())
    if qa.get("problemas") or qa.get("ok") is not True:
        falla(f"{c.name} no pasó el QA ({qa.get('problemas')})")
    viejo = [f for f in ("guion.json", "reel.mp4", "portada.jpg", "texto-reel.txt")
             if (c / f).stat().st_mtime > (c / "qa.json").stat().st_mtime + 1]
    if viejo:
        falla(f"{', '.join(viejo)} cambió después del QA: volvé a correr armar_reel.py")
    if qa.get("sha_reel") != sha(c / "reel.mp4"):
        falla("el reel.mp4 no es el que pasó el QA: volvé a correr armar_reel.py")

    # El día lo fija el que lanza la corrida (reels_diarios.sh): si cruza la medianoche, el tope
    # sigue contando sobre el mismo día.
    hoy = os.environ.get("REELS_HOY") or datetime.date.today().isoformat()
    pendiente = c / "pendiente.lock"

    with open(LOCK, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        reg = registro()
        g = json.loads((c / "guion.json").read_text())
        h = qa["sha_reel"]
        for r in reg:
            if r["carpeta"] == str(c) or r.get("sha") == h:
                falla(f"{c.name} ya está publicado ({r.get('permalink')})")
            if r["slug"] == g["slug"]:
                falla(f"ya hay un reel publicado con el slug «{g['slug']}» ({r.get('permalink')}): cambiá la idea o el slug")
        if pendiente.exists():
            falla(f"quedó un intento anterior a medias ({pendiente}): puede estar publicado. "
                  "Lo tiene que mirar una persona en la app antes de reintentar.")
        if a.send and sum(r["fecha"] == hoy for r in reg) >= MAX_POR_DIA:
            falla(f"ya hay {MAX_POR_DIA} reels publicados hoy")

        cmd = [str(PY), str(OS / "active/astronomy/contenido/publicar_reel.py"), str(c / "reel.mp4"),
               "--texto", str(c / "texto-reel.txt"), "--portada", str(c / "portada.jpg"), "--prueba", "auto"]
        if not a.send:
            p = subprocess.run(cmd, capture_output=True, text=True)
            print(p.stdout[-2000:], p.stderr[-1500:])
            if p.returncode != 0:
                falla(f"publicar_reel.py salió con {p.returncode}")
            print("PUBLICAR_SIN_SEND", c.name)
            return

        pendiente.write_text(datetime.datetime.now().isoformat())
        p = subprocess.run(cmd + ["--send"], capture_output=True, text=True)
        print(p.stdout[-2000:], p.stderr[-1500:])
        mid = re.search(r"^PUBLICADO_ID (\S+)$", p.stdout, re.M)
        if not mid:
            # No llegó a media_publish con éxito (o murió sin decirlo). Si salió con error ANTES de
            # publicar, el lock se puede sacar; si no hay certeza, queda para revisión humana.
            salida = p.stdout + p.stderr
            antes_de_publicar = ("No se pudo crear el bucket", "No se pudo subir", "Instagram no creó el contenedor",
                                 "no se publica", "Instagram no publicó", "El token no es de")
            if p.returncode != 0 and any(x in salida for x in antes_de_publicar):
                pendiente.unlink()
            falla(f"publicar_reel.py salió con {p.returncode} sin confirmar la publicación")
        link = re.search(r"^PUBLICADO_LINK (\S+)$", p.stdout, re.M)
        fila = {
            "fecha": hoy, "carpeta": str(c), "slug": g["slug"], "formato": g["formato"], "tema": g["tema"],
            "media_id": mid.group(1), "permalink": link.group(1) if link else None, "sha": h,
            "voz": (g.get("voz") or {}).get("texto"),
            "tomas": [f"{pathlib.Path(t['archivo']).name}@{t['desde']}" for t in g["tomas"]],
        }
        with REGISTRO.open("a") as f:
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
        pendiente.unlink()
    print("PUBLICADO_OK", fila["permalink"] or fila["media_id"])


if __name__ == "__main__":
    main()
