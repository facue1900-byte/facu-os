#!/usr/bin/env python3
"""
Aplica las etiquetas en Gmail. TOCA TU INBOX DE VERDAD: sin --send no hace nada.

    # ver qué haría (default)
    .venv/bin/python .claude/skills/triage-inbox/scripts/apply_labels.py \
        --input .tmp/triage/labels.json

    # aplicar
    .venv/bin/python .claude/skills/triage-inbox/scripts/apply_labels.py \
        --input .tmp/triage/labels.json --send

Necesita los scopes `gmail.modify` y `gmail.labels`, que NO están en
execution/google_auth.py a propósito (ahí solo hay readonly + send). Para
habilitarlo hay que agregarlos a SCOPES, borrar token-facu.json y re-loguearse
con --setup --cuenta facu.
Mientras tanto este script falla con un mensaje claro en vez de romper feo.

Las etiquetas se crean bajo el prefijo "Triage/" para no ensuciar la raíz y
poder borrarlas todas de una si el triage no sirve.
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))

from googleapiclient.errors import HttpError  # noqa: E402

from execution.google_auth import gmail  # noqa: E402

PREFIJO = "Triage"


def id_de_etiqueta(service, nombre):
    """Devuelve el ID de la etiqueta, creándola si no existe."""
    existentes = service.users().labels().list(userId="me").execute()
    for label in existentes.get("labels", []):
        if label["name"].lower() == nombre.lower():
            return label["id"]

    creada = service.users().labels().create(userId="me", body={
        "name": nombre,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }).execute()
    print(f"  etiqueta creada: {nombre}")
    return creada["id"]


def aplicar(service, ids, label_id, tamano=100):
    """Aplica una etiqueta de a 100 mensajes. Devuelve (ok, fallados)."""
    ok = fallados = 0
    for i in range(0, len(ids), tamano):
        tanda = ids[i:i + tamano]
        try:
            service.users().messages().batchModify(userId="me", body={
                "ids": tanda, "addLabelIds": [label_id],
            }).execute()
            ok += len(tanda)
        except HttpError as e:
            fallados += len(tanda)
            print(f"    tanda de {len(tanda)} falló: {e}", file=sys.stderr)
    return ok, fallados


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", "-i", required=True, help="labels.json de merge")
    p.add_argument("--send", action="store_true",
                   help="Aplicar de verdad. Sin esto, solo muestra el plan.")
    args = p.parse_args()

    clasificacion = json.loads(pathlib.Path(args.input).read_text())
    clasificacion = {k: v for k, v in clasificacion.items() if v}
    total = sum(len(v) for v in clasificacion.values())

    if not total:
        sys.exit("labels.json no tiene ningún mail. Nada que aplicar.")

    print(f"Plan ({total} mails):")
    for nombre, ids in clasificacion.items():
        print(f"  {PREFIJO}/{nombre}: {len(ids)}")

    if not args.send:
        print("\n[SIN --send] No toqué nada. Agregá --send para aplicar.")
        return 0

    try:
        service = gmail()
    except HttpError as e:
        sys.exit(f"No pude conectarme a Gmail: {e}")

    ok_total = fallados_total = 0
    for nombre, ids in clasificacion.items():
        completo = f"{PREFIJO}/{nombre}"
        print(f"\nAplicando {completo} a {len(ids)} mails...")
        try:
            label_id = id_de_etiqueta(service, completo)
        except HttpError as e:
            if e.resp.status in (401, 403):
                sys.exit(
                    f"\nGmail rechazó la operación ({e.resp.status}).\n"
                    "Casi seguro faltan los scopes gmail.modify y gmail.labels.\n"
                    "Agregalos a SCOPES en execution/google_auth.py, borrá "
                    "token-facu.json y corré:\n"
                    "  .venv/bin/python execution/google_auth.py --setup --cuenta facu"
                )
            raise

        ok, fallados = aplicar(service, ids, label_id)
        ok_total += ok
        fallados_total += fallados
        print(f"  {ok} etiquetados" + (f", {fallados} fallaron" if fallados else ""))

    print(f"\nTotal: {ok_total} etiquetados, {fallados_total} fallaron")
    return 1 if fallados_total else 0


if __name__ == "__main__":
    sys.exit(main())
