#!/usr/bin/env python3
"""
Parte el JSON de mails en N pedazos para clasificar en paralelo.

    .venv/bin/python .claude/skills/triage-inbox/scripts/split_chunks.py \
        --input .tmp/triage/emails.json --chunks 8 --output-dir .tmp/triage/chunks
"""

import argparse
import json
import math
import pathlib
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", "-i", required=True, help="JSON de fetch_emails.py")
    p.add_argument("--chunks", "-n", type=int, default=8,
                   help="Cantidad de pedazos (default: 8)")
    p.add_argument("--output-dir", "-o", required=True, help="Carpeta de salida")
    args = p.parse_args()

    mails = json.loads(pathlib.Path(args.input).read_text())
    total = len(mails)
    if total == 0:
        sys.exit("El archivo de entrada no tiene mails. Nada que partir.")

    destino = pathlib.Path(args.output_dir)
    destino.mkdir(parents=True, exist_ok=True)
    # Los pedazos viejos de una corrida anterior contaminan el merge.
    for viejo in destino.glob("chunk_*.json"):
        viejo.unlink()
    for viejo in destino.glob("clasificado_*.json"):
        viejo.unlink()

    por_chunk = math.ceil(total / args.chunks)
    escritos = 0
    for i in range(args.chunks):
        pedazo = mails[i * por_chunk:(i + 1) * por_chunk]
        if not pedazo:
            break
        (destino / f"chunk_{i}.json").write_text(
            json.dumps(pedazo, indent=2, ensure_ascii=False))
        escritos += 1

    print(f"{total} mails en {escritos} pedazos de hasta {por_chunk}")
    print(f"Salida: {destino}/chunk_0.json .. chunk_{escritos - 1}.json")
    # El SKILL.md necesita saber cuántos subagentes lanzar.
    print(f"CHUNKS={escritos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
