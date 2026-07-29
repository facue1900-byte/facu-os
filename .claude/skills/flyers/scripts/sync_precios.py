#!/usr/bin/env python3
"""Refresca los precios del contenido de flyers contra la fuente de verdad.

Un flyer con un precio viejo es peor que no tener flyer: sale publicado, alguien
lo compara con el checkout y no coincide. Por eso los precios NO se escriben a
mano en `contenido/academy.json` — se sincronizan desde la tabla `plans` de
Supabase (la misma que lee la app en producción).

    .venv/bin/python .claude/skills/flyers/scripts/sync_precios.py
    .venv/bin/python .claude/skills/flyers/scripts/sync_precios.py --dry-run

Escribe dos cosas:
  · `contenido/precios.json` — snapshot completo de `plans`, con fecha.
  · `contenido/academy.json` — actualiza los `precio_ars` de los productos que
    declaran `plan_id`, y avisa cuáles cambiaron.

Las credenciales salen del `.env.local` de la app (no se duplican secretos en
este repo). Si el archivo no está, el script corta: sin fuente no hay precio.
"""

import argparse
import datetime
import json
import pathlib
import sys
import urllib.request

SKILL = pathlib.Path(__file__).resolve().parent.parent
ENV_APP = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/astronomy-members/.env.local"


def leer_env(path):
    """Parser mínimo de .env: solo KEY=VALOR, ignora comentarios y vacías."""
    if not path.exists():
        sys.exit(
            f"No encuentro las credenciales en {path}.\n"
            "Sin la base no hay precio verificado: no voy a inventar uno. "
            "Pasá otro archivo con --env."
        )
    env = {}
    for linea in path.read_text().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def traer_planes(url, key):
    req = urllib.request.Request(
        f"{url.rstrip('/')}/rest/v1/plans?select=id,name,price_ars,monthly_credits,credit_months&order=sort",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        planes = json.load(r)

    # Una tabla vacía no es "no hay planes": es que el query salió mal o la key
    # no tiene permiso. Reportarlo como dato dejaría los flyers sin precio y sin
    # que nadie se entere.
    if not planes:
        sys.exit("La tabla `plans` devolvió CERO filas. Eso no es un dato válido: revisá la key.")
    return planes


def main():
    ap = argparse.ArgumentParser(description="Sincroniza precios de flyers contra Supabase.")
    ap.add_argument("--contenido", default=str(SKILL / "contenido/academy.json"))
    ap.add_argument("--env", default=str(ENV_APP))
    ap.add_argument("--dry-run", action="store_true", help="Muestra qué cambiaría y no escribe.")
    args = ap.parse_args()

    env = leer_env(pathlib.Path(args.env))
    url = env.get("NEXT_PUBLIC_SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if not url or not key:
        sys.exit(f"Faltan NEXT_PUBLIC_SUPABASE_URL o la key en {args.env}.")

    planes = traer_planes(url, key)
    por_id = {p["id"]: p for p in planes}
    hoy = datetime.date.today().isoformat()

    cont_path = pathlib.Path(args.contenido)
    cont = json.loads(cont_path.read_text())

    cambios = []
    for prod in cont["productos"]:
        pid = prod.get("plan_id")
        if not pid:
            continue
        if pid not in por_id:
            sys.exit(f"El producto '{prod['id']}' apunta a plan_id '{pid}' que no existe en `plans`.")
        nuevo = por_id[pid]["price_ars"]
        viejo = prod.get("precio_ars")
        if nuevo != viejo:
            cambios.append((prod["id"], viejo, nuevo))
        prod["precio_ars"] = nuevo
        if prod.get("creditos") is not None:
            prod["creditos"] = por_id[pid]["monthly_credits"]

    cont["_fuente_datos"]["verificado"] = hoy

    snapshot = {"verificado": hoy, "origen": url, "planes": planes}

    if args.dry_run:
        print("— dry-run, no escribo nada —")
    else:
        (SKILL / "contenido/precios.json").write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
        )
        cont_path.write_text(json.dumps(cont, ensure_ascii=False, indent=2) + "\n")

    print(f"Planes leídos de la base: {len(planes)}")
    for p in planes:
        print(f"  {p['id']:<14} ${p['price_ars']:>10,}  {p['monthly_credits']:>4} créditos".replace(",", "."))
    if cambios:
        print("\nCAMBIOS DE PRECIO:")
        for pid, viejo, nuevo in cambios:
            print(f"  {pid}: {viejo} -> {nuevo}   (hay que regenerar los flyers de este producto)")
    else:
        print("\nSin cambios de precio.")


if __name__ == "__main__":
    main()
