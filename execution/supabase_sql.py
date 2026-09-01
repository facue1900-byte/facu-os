#!/usr/bin/env python3
"""
Correr SQL contra una base de Supabase por la Management API.

Existe porque las migraciones de este OS se aplican sin que Facu entre al panel, y
porque un `curl` largo con el SQL embebido es ilegible y se rompe con las comillas.

    .venv/bin/python execution/supabase_sql.py --proyecto astronomy --archivo mi.sql
    .venv/bin/python execution/supabase_sql.py --proyecto astronomy --sql "select 1;"

Los `ref` de cada proyecto están abajo a propósito: son dos bases distintas, una por
negocio, y pegarle a la equivocada escribe en el negocio equivocado sin avisar.
"""

import argparse
import json
import pathlib
import sys
import urllib.request

from dotenv import load_dotenv
import os

RAIZ = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

PROYECTOS = {
    "astronomy": "qeakrjnseboiulcojlcw",
    "paseo": "wujutradczplokjrgmdo",
}


def correr(proyecto: str, sql: str):
    token = os.environ.get("SUPABASE_ACCESS_TOKEN", "").strip()
    if not token:
        sys.exit("Falta SUPABASE_ACCESS_TOKEN en el .env")
    ref = PROYECTOS.get(proyecto)
    if not ref:
        sys.exit(f"Proyecto desconocido: {proyecto}. Hay {list(PROYECTOS)}")

    req = urllib.request.Request(
        f"https://api.supabase.com/v1/projects/{ref}/database/query",
        data=json.dumps({"query": sql}).encode(),
        # El User-Agent NO es decoración: la Management API está detrás de Cloudflare,
        # que rechaza el de urllib con un 403 "error code: 1010" — un error que no dice
        # nada del token y manda a buscar el problema donde no está.
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "facu-os/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:800]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--proyecto", required=True, choices=sorted(PROYECTOS))
    p.add_argument("--archivo")
    p.add_argument("--sql")
    a = p.parse_args()
    if not a.archivo and not a.sql:
        sys.exit("Pasá --archivo o --sql")
    texto = pathlib.Path(a.archivo).read_text() if a.archivo else a.sql
    print(json.dumps(correr(a.proyecto, texto), indent=2, ensure_ascii=False)[:4000])
