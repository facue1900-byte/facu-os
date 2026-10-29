#!/usr/bin/env python3
"""Indexa el material REAL de Academy (videos del estudio y de The Bunker) para que el agente
diario sepa qué hay sin abrir cada archivo.

    .venv/bin/python active/astronomy/contenido/reels_diarios/indexar_material.py

Escribe material.json (archivo, duración, tamaño, orientación) y una hoja de contacto por video
en Pauta Online/Reels-diarios/_material/ (un cuadro cada `paso` segundos, con el segundo
escrito arriba). El agente mira las hojas para elegir tomas por segundo exacto.
Se corre de nuevo cuando entra material nuevo (ej. la filmación del profe con un alumno).
"""
import json
import pathlib
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

from comun import FF, MATERIAL, SALIDA, info

CARPETAS = [
    pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/The Bunker"),
    pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/Fotos del estudio"),
    pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/Material filmado"),
]
EXT = {".mp4", ".mov", ".m4v"}


def hoja(video, dur, destino):
    paso = 5 if dur < 120 else 30
    ts = [round(t, 1) for t in frange(0.5, dur - 0.5, paso)]
    fuente = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
    cuadros = []
    with tempfile.TemporaryDirectory() as tmp:
        for t in ts:
            out = pathlib.Path(tmp) / f"{t}.jpg"
            subprocess.run([FF, "-nostdin", "-v", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1",
                            "-vf", "scale=320:-2", str(out)], check=False)
            if out.exists():
                im = Image.open(out).convert("RGB")
                ImageDraw.Draw(im).text((6, 4), f"{t:.0f}s", fill="yellow", font=fuente,
                                        stroke_width=2, stroke_fill="black")
                cuadros.append(im)
    if not cuadros:
        return None
    w, h = cuadros[0].size
    cols = min(8, len(cuadros))
    filas = (len(cuadros) + cols - 1) // cols
    lienzo = Image.new("RGB", (w * cols, h * filas))
    for i, im in enumerate(cuadros):
        lienzo.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    destino.parent.mkdir(parents=True, exist_ok=True)
    lienzo.save(destino, quality=70)
    return paso


def frange(a, b, p):
    while a <= b:
        yield a
        a += p


def main():
    previo = {m["archivo"]: m for m in json.loads(MATERIAL.read_text())} if MATERIAL.exists() else {}
    items = []
    for c in CARPETAS:
        if not c.exists():
            continue
        for v in sorted(c.rglob("*")):
            if v.suffix.lower() not in EXT or v.name.startswith("."):
                continue
            dur, w, h = info(v)
            dest = SALIDA / "_material" / (v.relative_to(c.parent).as_posix().replace("/", "__") + ".jpg")
            m = previo.get(str(v), {})
            if not dest.exists():
                m["paso_hoja"] = hoja(v, dur, dest)
            items.append({
                "archivo": str(v), "duracion": round(dur, 2), "ancho": w, "alto": h,
                "orientacion": "vertical" if h > w else "horizontal",
                "hoja": str(dest), "paso_hoja": m.get("paso_hoja"),
                # Lo que el agente aprendió mirando la hoja (qué se ve, segundos buenos). Se conserva.
                "notas": m.get("notas", ""),
            })
            print(f"{dur:8.1f}s {w}x{h} {v.name}")
    if not items:
        raise SystemExit("No encontré ningún video: el índice quedaría vacío.")
    MATERIAL.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    print(f"{len(items)} videos indexados → {MATERIAL}")


if __name__ == "__main__":
    main()
