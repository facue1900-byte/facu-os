#!/usr/bin/env python3
"""
Junta lo que clasificó cada subagente, chequea que no falte ningún mail, y
escribe dos cosas: el mapa de etiquetas para aplicar y el reporte para leer.

    .venv/bin/python .claude/skills/triage-inbox/scripts/merge_labels.py \
        --emails .tmp/triage/emails.json \
        --input-dir .tmp/triage/chunks \
        --output .tmp/triage/labels.json \
        --report .tmp/triage/reporte.md

Cada `clasificado_N.json` es una lista de:
    {"id": "...", "etiqueta": "...", "negocio": "...", "motivo": "..."}

Si un mail quedó sin clasificar, el script falla. Un triage que se come mails en
silencio es peor que no tener triage.
"""

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

ETIQUETAS = ["Plata", "Acción", "Esperando", "Referencia"]
NEGOCIOS = ["Paseo Nordelta", "Nordelta Plaza", "Astronomy", "Campos",
            "Personal", "—"]


def cargar_clasificados(carpeta):
    """Lee todos los clasificado_*.json. Devuelve {id: registro}."""
    archivos = sorted(carpeta.glob("clasificado_*.json"))
    if not archivos:
        sys.exit(f"No hay ningún clasificado_*.json en {carpeta}. "
                 "¿Corrieron los subagentes?")

    por_id = {}
    for ruta in archivos:
        try:
            registros = json.loads(ruta.read_text())
        except json.JSONDecodeError as e:
            sys.exit(f"{ruta.name} no es JSON válido: {e}")

        if not isinstance(registros, list):
            sys.exit(f"{ruta.name} tiene que ser una lista, no {type(registros).__name__}")

        for r in registros:
            etiqueta = r.get("etiqueta")
            if etiqueta not in ETIQUETAS:
                sys.exit(f"{ruta.name}: etiqueta inválida {etiqueta!r} "
                         f"en el mail {r.get('id')}. Válidas: {ETIQUETAS}")
            por_id[r["id"]] = r
        print(f"  {ruta.name}: {len(registros)}")

    return por_id


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--emails", "-e", required=True,
                   help="El emails.json original, para chequear cobertura")
    p.add_argument("--input-dir", "-i", required=True,
                   help="Carpeta con los clasificado_*.json")
    p.add_argument("--output", "-o", required=True, help="labels.json de salida")
    p.add_argument("--report", "-r", required=True, help="Reporte .md de salida")
    args = p.parse_args()

    mails = json.loads(pathlib.Path(args.emails).read_text())
    por_id = cargar_clasificados(pathlib.Path(args.input_dir))

    originales = {m["id"] for m in mails}
    faltantes = originales - set(por_id)
    sobrantes = set(por_id) - originales

    if sobrantes:
        print(f"AVISO: {len(sobrantes)} IDs clasificados que no estaban en el "
              f"input; los ignoro.", file=sys.stderr)
        for extra in sobrantes:
            por_id.pop(extra)

    if faltantes:
        sys.exit(
            f"\nFALTAN {len(faltantes)} de {len(originales)} mails sin clasificar.\n"
            f"Ejemplos: {list(faltantes)[:5]}\n"
            "Algún subagente no terminó o escribió mal su archivo. "
            "Recorré el paso de clasificación antes de aplicar nada."
        )

    # Mapa etiqueta -> ids, que es lo que consume apply_labels.py
    etiquetas = {e: [] for e in ETIQUETAS}
    for m in mails:
        etiquetas[por_id[m["id"]]["etiqueta"]].append(m["id"])

    salida = pathlib.Path(args.output)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(etiquetas, indent=2, ensure_ascii=False))

    # Reporte legible: por etiqueta, y adentro por negocio.
    info = {m["id"]: m for m in mails}
    lineas = [f"# Triage de inbox — {len(mails)} mails", ""]

    conteo_negocio = Counter(por_id[m["id"]].get("negocio", "—") for m in mails)
    lineas.append("| Etiqueta | Mails |")
    lineas.append("|---|---:|")
    for e in ETIQUETAS:
        lineas.append(f"| {e} | {len(etiquetas[e])} |")
    lineas.append("")
    lineas.append("| Negocio | Mails |")
    lineas.append("|---|---:|")
    for n, c in conteo_negocio.most_common():
        lineas.append(f"| {n} | {c} |")
    lineas.append("")

    for e in ETIQUETAS:
        if not etiquetas[e]:
            continue
        lineas.append(f"## {e} ({len(etiquetas[e])})")
        lineas.append("")
        por_negocio = defaultdict(list)
        for mid in etiquetas[e]:
            por_negocio[por_id[mid].get("negocio", "—")].append(mid)

        for negocio in sorted(por_negocio, key=lambda n: -len(por_negocio[n])):
            lineas.append(f"**{negocio}**")
            lineas.append("")
            for mid in por_negocio[negocio]:
                m, c = info[mid], por_id[mid]
                de = m["de"].split("<")[0].strip().strip('"') or m["de"]
                lineas.append(f"- **{m['asunto']}** — {de}  ")
                lineas.append(f"  _{c.get('motivo', '')}_")
            lineas.append("")

    reporte = pathlib.Path(args.report)
    reporte.parent.mkdir(parents=True, exist_ok=True)
    reporte.write_text("\n".join(lineas))

    print(f"\n{len(mails)} mails clasificados, ninguno perdido.")
    for e in ETIQUETAS:
        print(f"  {e}: {len(etiquetas[e])}")
    print(f"\nEtiquetas: {salida}")
    print(f"Reporte:   {reporte}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
