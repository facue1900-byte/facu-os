#!/usr/bin/env python3
"""Sube las placas de Astronomy Academy a la biblioteca de imágenes de Meta.

Subir una imagen no crea ningún anuncio, no gasta un peso y no publica nada: deja el
archivo en la biblioteca de la cuenta con un `hash` que después se referencia al armar
los creativos. Por eso esto se puede correr aunque la app esté en modo Desarrollo,
que es lo que hoy bloquea la creación de anuncios.

    # ver qué subiría, sin tocar la cuenta (por defecto)
    .venv/bin/python active/astronomy/pauta/subir_creativos.py

    # subirlas de verdad
    .venv/bin/python active/astronomy/pauta/subir_creativos.py --send

Deja un manifiesto en `data/pauta/creativos.json` con el hash de cada pieza, indexado
por producto / ángulo / formato. Es idempotente: Meta devuelve el mismo hash para el
mismo archivo, así que volver a correrlo no duplica nada.

El manifiesto se MEZCLA con el que ya está en disco y solo se escribe si algo subió.
Antes se sobrescribía siempre: con el token vencido (29/07/2026) las 75 fallaron y el
archivo quedó en `{}`, borrando los hashes de los anuncios que estaban corriendo.
"""

import argparse
import json
import os
import pathlib
import sys

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env")

TOKEN = os.getenv("META_ACCESS_TOKEN")
CUENTA = os.getenv("META_AD_ACCOUNT_ID")
VERSION = os.getenv("META_API_VERSION", "v23.0")
PLACAS = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/Flyers Academy/editorial"
DESTINO = RAIZ / "data" / "pauta" / "creativos.json"


def main():
    ap = argparse.ArgumentParser(description="Sube las placas a la biblioteca de Meta. Dry-run por defecto.")
    ap.add_argument("--send", action="store_true", help="Subirlas de verdad (si no, solo muestra)")
    args = ap.parse_args()

    if not TOKEN or not CUENTA:
        sys.exit("Faltan META_ACCESS_TOKEN o META_AD_ACCOUNT_ID en el .env")
    if not PLACAS.is_dir():
        sys.exit(f"No encuentro las placas en {PLACAS}")

    archivos = sorted(PLACAS.glob("*/*.png"))
    if not archivos:
        sys.exit(f"No hay PNGs en {PLACAS}")

    if not args.send:
        print(f"{len(archivos)} placas listas en {PLACAS}")
        for f in archivos[:5]:
            print(f"   {f.parent.name}/{f.name}")
        print(f"   … y {len(archivos) - 5} más\n[dry-run] No se subió nada. Agregá --send.")
        return

    previo = json.loads(DESTINO.read_text()) if DESTINO.exists() else {}
    manifiesto, fallos = json.loads(json.dumps(previo)), []
    with httpx.Client(timeout=180) as cli:
        for n, f in enumerate(archivos, 1):
            producto = f.parent.name
            angulo, _, formato = f.stem.partition("__")
            with f.open("rb") as fh:
                r = cli.post(
                    f"https://graph.facebook.com/{VERSION}/{CUENTA}/adimages",
                    data={"access_token": TOKEN},
                    files={"file": (f.name, fh, "image/png")},
                )
            j = r.json()
            if "error" in j:
                e = j["error"]
                # Un token vencido no se arregla reintentando 74 veces: se corta acá y
                # el manifiesto que ya estaba en disco queda intacto.
                if e.get("code") == 190:
                    sys.exit(
                        f"\nToken de Meta inválido: {e.get('message')}\n"
                        "Generá uno nuevo y actualizá META_ACCESS_TOKEN en el .env. "
                        "No se subió nada y el manifiesto quedó como estaba."
                    )
                fallos.append((f"{producto}/{f.name}", e.get("message", "")[:90]))
                print(f"  [{n:>2}/{len(archivos)}] FALLÓ {producto}/{f.name}")
                continue
            img = next(iter((j.get("images") or {}).values()), None)
            if not img:
                fallos.append((f"{producto}/{f.name}", "respuesta sin hash"))
                continue
            manifiesto.setdefault(producto, {}).setdefault(angulo, {})[formato] = {
                "hash": img["hash"],
                "archivo": str(f),
            }
            print(f"  [{n:>2}/{len(archivos)}] {producto}/{angulo}/{formato}  {img['hash'][:16]}…")

    if manifiesto == previo:
        sys.exit("\nNo subió ninguna pieza. El manifiesto queda como estaba, sin tocar.")

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2))

    total = sum(len(fm) for p in manifiesto.values() for fm in p.values())
    print(f"\n{total} piezas en la biblioteca · {len(manifiesto)} productos")
    for prod, angulos in sorted(manifiesto.items()):
        formatos = {f for a in angulos.values() for f in a}
        print(f"   {prod:<20} {len(angulos)} ángulos × {len(formatos)} formatos")
    if fallos:
        print(f"\n{len(fallos)} fallaron:")
        for nombre, err in fallos:
            print(f"   {nombre}: {err}")
    print(f"\nManifiesto: {DESTINO}")


if __name__ == "__main__":
    main()
