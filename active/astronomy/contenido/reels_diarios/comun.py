"""Lo compartido por los scripts de reels diarios: rutas, ffmpeg y lectura de duraciones."""
import json
import pathlib
import re
import subprocess

import imageio_ffmpeg

AQUI = pathlib.Path(__file__).resolve().parent
OS = AQUI.parents[3]
PY = OS / ".venv/bin/python"
FF = imageio_ffmpeg.get_ffmpeg_exe()

CONTENIDO = pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido")
SALIDA = CONTENIDO / "Pauta Online/Reels-diarios"     # una carpeta por día
REGISTRO = AQUI / "registro.jsonl"                     # un renglón por reel publicado
MATERIAL = AQUI / "material.json"                      # índice del material real (indexar_material.py)
TEMAS = AQUI / "temas.json"                            # música de Sin City con su drop medido
WHATSAPP = "+54 9 11 2400-5565"


def ff(*a):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", *map(str, a)], check=True)


def info(path):
    """(duración en s, ancho, alto) leyendo el banner de ffmpeg: no hay ffprobe en la Mac."""
    txt = subprocess.run([FF, "-nostdin", "-i", str(path)], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", txt)
    v = re.search(r"Video: .*?(\d{3,5})x(\d{3,5})", txt)
    rot = re.search(r"rotation of (-?\d+)", txt) or re.search(r"rotate\s*:\s*(-?\d+)", txt)
    if not d or not v:
        raise ValueError(f"No pude leer {path}")
    w, h = int(v.group(1)), int(v.group(2))
    if rot and abs(int(rot.group(1))) in (90, 270):
        w, h = h, w
    return int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3)), w, h


def duracion(path):
    """Duración en s de cualquier archivo (también audio)."""
    txt = subprocess.run([FF, "-nostdin", "-i", str(path)], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", txt)
    if not d:
        raise ValueError(f"No pude leer la duración de {path}")
    return int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))


def registro():
    if not REGISTRO.exists():
        return []
    return [json.loads(l) for l in REGISTRO.read_text().splitlines() if l.strip()]
