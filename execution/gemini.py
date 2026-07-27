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
    .venv/bin/python execution/gemini.py "qué se acordó acá" --media reunion.m4a

Desde un skill:

    from execution.gemini import preguntar, leer_imagen, leer_media
    texto = leer_imagen("guia.jpg", "Extraé cantidad, categoría, origen y destino")
    acta = leer_media("reunion.m4a", "Listá los compromisos que se asumieron")

`leer_imagen` manda el archivo inline (sirve para fotos y PDFs cortos).
`leer_media` sube por la Files API y espera el procesamiento: es la única que
banca audio y video largos, y borra el archivo del lado de Google al terminar.

El modelo sale de `GEMINI_MODEL` en el `.env`. No hay un default hardcodeado a
propósito: los IDs de modelo cambian seguido y un ID inventado falla en silencio
al primer uso. Corré `--modelos` para ver cuáles hay disponibles con tu key.
"""

import argparse
import os
import pathlib
import sys
import time

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

RAIZ = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")

MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".webp": "image/webp", ".heic": "image/heic", ".pdf": "application/pdf",
}

# Audio y video van por la Files API, no inline: una reunión de una hora no
# entra en un request. `.opus` es lo que manda WhatsApp en las notas de voz.
MIME_MEDIA = {
    ".mp3": "audio/mp3", ".wav": "audio/wav", ".aiff": "audio/aiff",
    ".aac": "audio/aac", ".ogg": "audio/ogg", ".opus": "audio/ogg",
    ".flac": "audio/flac", ".m4a": "audio/aac",
    ".mp4": "video/mp4", ".mpeg": "video/mpeg", ".mpg": "video/mpg",
    ".mov": "video/mov", ".avi": "video/avi", ".webm": "video/webm",
    ".wmv": "video/wmv", ".3gp": "video/3gpp", ".flv": "video/x-flv",
}


_CLIENTE = None


def cliente():
    """Cliente único y cacheado.

    Tiene que ser un singleton de módulo: si se devuelve un `Client` nuevo por
    llamada, en las APIs perezosas (`models.list()` devuelve un pager) el objeto
    se recolecta antes de que salga el request y httpx muere con
    "Cannot send a request, as the client has been closed" — un error que no
    tiene nada que ver con la causa real y manda a debuggear para el lado
    equivocado.
    """
    global _CLIENTE
    if _CLIENTE is not None:
        return _CLIENTE

    # .strip(): un espacio pegado después del `=` en el .env viaja hasta el
    # header de auth y vuelve como 401 sin explicación.
    key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not key:
        sys.exit("Falta GEMINI_API_KEY en el .env (sacala de aistudio.google.com/apikey).")
    # Nada de validar el prefijo de la key: AI Studio emite tanto 'AIza…' como
    # 'AQ.…' y un chequeo de forma solo genera avisos falsos. Si la key no sirve,
    # la API lo dice — y `listar_modelos()` muestra ese mensaje sin el traceback.
    _CLIENTE = genai.Client(api_key=key)
    return _CLIENTE


def modelo():
    m = (os.getenv("GEMINI_MODEL") or "").strip()
    if not m:
        sys.exit(
            "Falta GEMINI_MODEL en el .env.\n"
            "Corré `--modelos` para ver los disponibles y elegí uno "
            "(flash para volumen, pro para razonar)."
        )
    return m


def listar_modelos():
    # `except Exception` a secas convertiría un typo del script en "la API contestó",
    # que es mentir sobre el origen del error. Solo se traducen los errores que de
    # verdad vienen de la API o de la red; un bug propio revienta con traceback.
    try:
        modelos = list(cliente().models.list())
    except (genai_errors.APIError, httpx.HTTPError) as e:
        # El traceback crudo de google-genai son 40 líneas que esconden el motivo.
        sys.exit(f"No pude listar modelos. La API contestó:\n\n  {e}\n")
    if not modelos:
        sys.exit("La API devolvió CERO modelos. Eso no es una lista vacía válida: revisá la key.")

    # Se cuenta lo que se IMPRIME, no lo que devolvió la API: si la lista viene
    # llena pero el filtro de generateContent la deja en cero, el script salía con
    # éxito y cero líneas — el mismo silencio que el chequeo pretendía evitar.
    mostrados = 0
    for m in modelos:
        acciones = getattr(m, "supported_actions", None) or []
        if not acciones or "generateContent" in acciones:
            print(f"{m.name:<45} {(m.display_name or '')}")
            mostrados += 1
    if not mostrados:
        sys.exit(
            f"La API devolvió {len(modelos)} modelos pero NINGUNO soporta generateContent. "
            "Revisá si la key está restringida."
        )

    # Estar en esta lista no alcanza para poder usarlo: modelos como
    # `gemini-2.5-flash` figuran acá y tiran 404 "no longer available to new users".
    # Antes de fijar uno en GEMINI_MODEL, probarlo con una llamada real.


def _texto(r, contexto):
    """Saca el texto de una respuesta, o revienta.

    `r.text` puede venir vacío o `None` sin que haya habido error: filtro de
    safety, respuesta cortada por límite de tokens, cero candidatos. Devolver eso
    tal cual es peligroso — el que llama guarda `None` como si fuera el dato que
    extrajo de la guía. Acá se corta fuerte y se dice por qué.
    """
    texto = getattr(r, "text", None)
    if texto and texto.strip():
        return texto
    motivo = ""
    candidatos = getattr(r, "candidates", None) or []
    if candidatos:
        razon = getattr(candidatos[0], "finish_reason", None)
        if razon:
            motivo = f" finish_reason={razon}."
    feedback = getattr(r, "prompt_feedback", None)
    if feedback:
        motivo += f" prompt_feedback={feedback}."
    raise RuntimeError(
        f"Gemini devolvió una respuesta VACÍA para {contexto}.{motivo} "
        "No la trates como dato: puede ser filtro de safety o respuesta cortada."
    )


def preguntar(prompt, texto=None, temperatura=0.2):
    """Una pregunta con contexto de texto opcional. Devuelve el string de respuesta."""
    partes = [prompt] if texto is None else [prompt, "\n\n---\n\n", texto]
    r = cliente().models.generate_content(
        model=modelo(),
        contents=partes,
        config=types.GenerateContentConfig(temperature=temperatura),
    )
    return _texto(r, "la pregunta")


def leer_imagen(path, prompt, temperatura=0.0):
    """Lee una imagen o PDF y devuelve lo que se le pida.

    Pensado para las fotos que llegan del campo por WhatsApp: guías de SENASA,
    comprobantes, pizarras con precios. Temperatura 0 porque acá se transcribe,
    no se inventa.
    """
    path = pathlib.Path(path)
    if not path.exists():
        sys.exit(f"No existe {path}")
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
    return _texto(r, path.name)


def _estado(archivo):
    """Devuelve el estado del archivo subido como string, sea enum o str."""
    estado = getattr(archivo, "state", None)
    return getattr(estado, "name", None) or str(estado or "").rsplit(".", 1)[-1]


def leer_media(path, prompt, temperatura=0.0, espera_max=900, verbose=True,
               json_estricto=False):
    """Lee un audio o video largo y devuelve lo que se le pida.

    Va por la Files API porque una grabación de una hora no entra inline. El
    archivo queda del lado de Google hasta 48hs; acá se borra apenas termina.

    Temperatura 0: esto transcribe y extrae, no redacta.

    Con `json_estricto=True` la respuesta viene como JSON válido de la API, sin
    fences de markdown que después haya que limpiar a mano.
    """
    path = pathlib.Path(path)
    if not path.exists():
        sys.exit(f"No existe {path}")

    mime = MIME_MEDIA.get(path.suffix.lower())
    if not mime:
        sys.exit(
            f"No sé qué mime-type tiene {path.suffix}. "
            f"Conocidos: {', '.join(sorted(MIME_MEDIA))}.\n"
            "Si el formato es raro, convertilo con ffmpeg a .mp3 o .mp4."
        )

    c = cliente()
    if verbose:
        mb = path.stat().st_size / 1024 / 1024
        print(f"Subiendo {path.name} ({mb:.1f} MB)...", file=sys.stderr)

    archivo = c.files.upload(file=str(path),
                             config={"mime_type": mime})

    # Google procesa el archivo antes de dejarlo usar. Sin este poll, el
    # generate_content falla con "file is not in an ACTIVE state".
    inicio = time.time()
    while _estado(archivo) == "PROCESSING":
        if time.time() - inicio > espera_max:
            c.files.delete(name=archivo.name)
            sys.exit(f"El archivo siguió en PROCESSING más de {espera_max}s. "
                     "Probá con una grabación más corta.")
        time.sleep(3)
        archivo = c.files.get(name=archivo.name)

    if _estado(archivo) != "ACTIVE":
        c.files.delete(name=archivo.name)
        sys.exit(f"Google no pudo procesar {path.name} (estado {_estado(archivo)}). "
                 "Suele ser un archivo corrupto o un codec raro.")

    if verbose:
        print(f"Procesado en {time.time() - inicio:.0f}s. Analizando...",
              file=sys.stderr)

    config = types.GenerateContentConfig(
        temperature=temperatura,
        response_mime_type="application/json" if json_estricto else None,
    )
    try:
        r = c.models.generate_content(
            model=modelo(), contents=[archivo, prompt], config=config,
        )
        return _texto(r, path.name)
    finally:
        # Que no queden archivos colgados del lado de Google si algo revienta.
        try:
            c.files.delete(name=archivo.name)
        except Exception:
            pass


def main():
    p = argparse.ArgumentParser(description="Helper de Gemini")
    p.add_argument("prompt", nargs="?", help="Qué preguntarle")
    p.add_argument("--archivo", help="Archivo de texto como contexto")
    p.add_argument("--imagen", help="Imagen o PDF a leer")
    p.add_argument("--media", help="Audio o video a escuchar/mirar (va por la Files API)")
    p.add_argument("--modelos", action="store_true", help="Lista los modelos disponibles")
    a = p.parse_args()

    if a.modelos:
        listar_modelos()
        return
    if not a.prompt:
        p.error("falta el prompt (o usá --modelos)")

    if a.imagen:
        print(leer_imagen(a.imagen, a.prompt))
    elif a.media:
        print(leer_media(a.media, a.prompt))
    else:
        texto = pathlib.Path(a.archivo).read_text() if a.archivo else None
        print(preguntar(a.prompt, texto))


if __name__ == "__main__":
    main()
