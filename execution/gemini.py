#!/usr/bin/env python3
"""
Helper de Gemini — para volumen barato, lectura de imágenes y segunda opinión.

Necesita `GEMINI_API_KEY` en el `.env` de la raíz. La key se saca de
https://aistudio.google.com/apikey — **no** de Google Cloud Console: la de Cloud
cobra a Cloud, la de AI Studio usa los créditos gratis.

Uso desde la línea de comandos:

    .venv/bin/python execution/gemini.py --modelos
    .venv/bin/python execution/gemini.py "resumime esto" --archivo nota.txt
    .venv/bin/python execution/gemini.py "qué dice esta guía" --imagen foto.jpg

Desde un skill:

    from execution.gemini import preguntar, leer_imagen
    texto = leer_imagen("guia.jpg", "Extraé cantidad, categoría, origen y destino")

El modelo sale de `GEMINI_MODEL` en el `.env`. No hay un default hardcodeado a
propósito: los IDs de modelo cambian seguido y un ID inventado falla en silencio
al primer uso. Corré `--modelos` para ver cuáles hay disponibles con tu key.
"""

import argparse
import os
import pathlib
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

RAIZ = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".webp": "image/webp", ".heic": "image/heic", ".pdf": "application/pdf",
}


def cliente():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        sys.exit("Falta GEMINI_API_KEY en el .env (sacala de aistudio.google.com/apikey).")
    return genai.Client(api_key=key)


def modelo():
    m = os.getenv("GEMINI_MODEL")
    if not m:
        sys.exit(
            "Falta GEMINI_MODEL en el .env.\n"
            "Corré `--modelos` para ver los disponibles y elegí uno "
            "(flash para volumen, pro para razonar)."
        )
    return m


def listar_modelos():
    for m in cliente().models.list():
        acciones = getattr(m, "supported_actions", None) or []
        if not acciones or "generateContent" in acciones:
            print(f"{m.name:<45} {(m.display_name or '')}")


def preguntar(prompt, texto=None, temperatura=0.2):
    """Una pregunta con contexto de texto opcional. Devuelve el string de respuesta."""
    partes = [prompt] if texto is None else [prompt, "\n\n---\n\n", texto]
    r = cliente().models.generate_content(
        model=modelo(),
        contents=partes,
        config=types.GenerateContentConfig(temperature=temperatura),
    )
    return r.text


def leer_imagen(path, prompt, temperatura=0.0):
    """Lee una imagen o PDF y devuelve lo que se le pida.

    Pensado para las fotos que llegan del campo por WhatsApp: guías de SENASA,
    comprobantes, pizarras con precios. Temperatura 0 porque acá se transcribe,
    no se inventa.
    """
    path = pathlib.Path(path)
    mime = MIME.get(path.suffix.lower())
    if not mime:
        sys.exit(f"No sé qué mime-type tiene {path.suffix}. Agregalo al dict MIME.")
    r = cliente().models.generate_content(
        model=modelo(),
        contents=[
            types.Part.from_bytes(data=path.read_bytes(), mime_type=mime),
            prompt,
        ],
        config=types.GenerateContentConfig(temperature=temperatura),
    )
    return r.text


def main():
    p = argparse.ArgumentParser(description="Helper de Gemini")
    p.add_argument("prompt", nargs="?", help="Qué preguntarle")
    p.add_argument("--archivo", help="Archivo de texto como contexto")
    p.add_argument("--imagen", help="Imagen o PDF a leer")
    p.add_argument("--modelos", action="store_true", help="Lista los modelos disponibles")
    a = p.parse_args()

    if a.modelos:
        listar_modelos()
        return
    if not a.prompt:
        p.error("falta el prompt (o usá --modelos)")

    if a.imagen:
        print(leer_imagen(a.imagen, a.prompt))
    else:
        texto = pathlib.Path(a.archivo).read_text() if a.archivo else None
        print(preguntar(a.prompt, texto))


if __name__ == "__main__":
    main()
