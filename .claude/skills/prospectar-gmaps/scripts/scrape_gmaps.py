#!/usr/bin/env python3
"""
Saca listados de Google Maps (nombre, dirección, teléfono, web, rating) y los
deja en un CSV para abrir en Sheets.

    .venv/bin/python .claude/skills/prospectar-gmaps/scripts/scrape_gmaps.py \
        --buscar "heladerías en Nordelta, Tigre" --limite 30 \
        --salida data/prospectos/heladerias-nordelta.csv

Usa el actor `compass/crawler-google-places` de Apify por HTTP directo, sin el
SDK: es un POST y un JSON, no hace falta sumar una dependencia al venv.

Necesita APIFY_API_TOKEN en el .env. Apify cobra por uso (~USD 0,015 por
listado, o sea ~USD 1,50 cada 100). No es gratis: no lo corras en loop.
"""

import argparse
import csv
import json
import os
import pathlib
import sys

import requests
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[4]
load_dotenv(RAIZ / ".env")

ACTOR = "compass~crawler-google-places"
ENDPOINT = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items"

COLUMNAS = ["nombre", "categoria", "direccion", "telefono", "web",
            "rating", "reviews", "maps_url"]


def scrapear(busqueda, limite, idioma="es", timeout=600):
    """Corre el actor y devuelve los items crudos del dataset."""
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        sys.exit(
            "Falta APIFY_API_TOKEN en el .env.\n"
            "Se saca en apify.com → Settings → API & Integrations. "
            "Tiene free tier mensual; pasado eso cobra por uso."
        )

    payload = {
        "searchStringsArray": [busqueda],
        "maxCrawledPlacesPerSearch": limite,
        "language": idioma,
        "deeperCityScrape": False,
        "oneReviewPerRow": False,
    }

    print(f"Buscando en Google Maps: '{busqueda}' (hasta {limite})...")
    r = requests.post(
        ENDPOINT,
        params={"token": token, "timeout": timeout},
        json=payload,
        timeout=timeout + 30,
    )

    if r.status_code == 401:
        sys.exit("Apify rechazó el token (401). Revisá APIFY_API_TOKEN.")
    if not r.ok:
        sys.exit(f"Apify devolvió {r.status_code}: {r.text[:300]}")

    return r.json()


def normalizar(items):
    """Deja solo las columnas que sirven para prospectar."""
    filas = []
    for it in items:
        filas.append({
            "nombre": it.get("title", ""),
            "categoria": it.get("categoryName", ""),
            "direccion": it.get("address", ""),
            "telefono": it.get("phone", "") or "",
            "web": it.get("website", "") or "",
            "rating": it.get("totalScore", ""),
            "reviews": it.get("reviewsCount", ""),
            "maps_url": it.get("url", ""),
        })
    return filas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--buscar", "-b", required=True,
                   help="Qué buscar, con la zona incluida. "
                        "Ej: 'gastronomía en Nordelta, Tigre'")
    p.add_argument("--limite", "-l", type=int, default=20,
                   help="Máximo de listados (default: 20). Cada uno cuesta.")
    p.add_argument("--idioma", default="es")
    p.add_argument("--salida", "-o", required=True, help="CSV de salida")
    p.add_argument("--json", help="Opcional: guardar también el JSON crudo")
    args = p.parse_args()

    items = scrapear(args.buscar, args.limite, args.idioma)
    filas = normalizar(items)

    if not filas:
        # Cero resultados casi siempre es la query, no el mercado.
        sys.exit("Cero resultados. Poné la zona en la búsqueda "
                 "('X en Nordelta, Tigre') antes de darlo por bueno.")

    salida = pathlib.Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)

    if args.json:
        crudo = pathlib.Path(args.json)
        crudo.parent.mkdir(parents=True, exist_ok=True)
        crudo.write_text(json.dumps(items, indent=2, ensure_ascii=False))

    con_tel = sum(1 for f in filas if f["telefono"])
    con_web = sum(1 for f in filas if f["web"])
    print(f"\n{len(filas)} listados en {salida}")
    print(f"  con teléfono: {con_tel}")
    print(f"  con web:      {con_web}")
    if len(filas) < args.limite:
        print(f"  OJO: pediste {args.limite} y salieron {len(filas)}. "
              "Puede ser que no haya más, o que la query sea muy angosta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
