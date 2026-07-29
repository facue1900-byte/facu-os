#!/usr/bin/env python3
"""Cerebro del bot de WhatsApp de Astronomy Academy.

Toma un mensaje de un interesado y devuelve qué contestar, o decide que hay que
pasarle el tema a José. Los precios NO están escritos en ningún lado: se leen en
vivo de la tabla `plans` de Supabase antes de armar la respuesta, así el bot nunca
canta un número viejo.

    # probar una pregunta suelta
    .venv/bin/python active/astronomy/bot/responder.py "cuánto sale el curso de dj?"

    # correr la batería de casos de prueba
    .venv/bin/python active/astronomy/bot/responder.py --tests

Esto es el motor, no el canal. Enchufarlo al WhatsApp real es una capa aparte
(webhook), y va a vivir en la app de Next.js que ya está en Vercel. Se prueba acá
primero porque el criterio de qué contesta y qué escala es lo que hay que tener bien
antes de que le hable a un cliente.
"""

import argparse
import json
import os
import pathlib
import sys
import urllib.request

import anthropic
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
BOT = pathlib.Path(__file__).resolve().parent
load_dotenv(RAIZ / ".env")

MODELO = "claude-sonnet-5"          # genera texto para terceros: Sonnet, no Opus
ENV_APP = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/astronomy-members/.env.local"

# La herramienta que fuerza la salida estructurada. Sin esto habría que parsear
# texto libre para saber si escaló, y ese parseo falla justo cuando importa.
HERRAMIENTA = {
    "name": "responder",
    "description": "Devuelve la respuesta para el interesado, o marca que hay que escalar a José.",
    "input_schema": {
        "type": "object",
        "properties": {
            "respuesta": {
                "type": "string",
                "description": (
                    "El mensaje de WhatsApp que se le manda a la persona. Si escalar es "
                    "true, este texto es lo que se le dice mientras espera a José."
                ),
            },
            "escalar": {
                "type": "boolean",
                "description": "true si hay que avisarle a José que agarre esta conversación.",
            },
            "motivo": {
                "type": "string",
                "description": (
                    "Si escalar es true: por qué, en una línea, para que José sepa qué "
                    "le están preguntando sin leer todo el hilo. Si es false, string vacío."
                ),
            },
            "producto": {
                "type": "string",
                "enum": ["curso-dj", "membresias", "produccion", "produccion-online",
                         "modo-profesional", "dj-delivery", "ninguno"],
                "description": "Sobre qué producto pregunta. Sirve para atribuir la pauta.",
            },
        },
        "required": ["respuesta", "escalar", "motivo", "producto"],
    },
}


def leer_env(path):
    if not path.exists():
        return {}
    env = {}
    for linea in path.read_text().splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            k, v = linea.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def precios_en_vivo():
    """Lee la tabla `plans` de Supabase. Es la misma que lee el checkout.

    Si falla, NO devuelve precios viejos de fallback: devuelve None y el bot pasa a
    modo "el valor te lo confirma José". Un precio equivocado por WhatsApp es peor
    que no dar el precio.
    """
    env = leer_env(ENV_APP)
    url = env.get("NEXT_PUBLIC_SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        return None
    try:
        req = urllib.request.Request(
            f"{url.rstrip('/')}/rest/v1/plans?select=id,name,price_ars,monthly_credits&order=sort",
            headers={"apikey": key, "Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            planes = json.load(r)
    except Exception as e:
        print(f"[aviso] no pude leer precios de Supabase: {e}", file=sys.stderr)
        return None
    if not planes:
        return None
    # `test` y `bronze` no se ofrecen: uno es de prueba y el otro es secreto, para amigos.
    return [p for p in planes if p["id"] not in ("test", "bronze")]


def bloque_precios(planes):
    if planes is None:
        return (
            "NO SE PUDIERON LEER LOS PRECIOS. No inventes ninguno y no des cifras: "
            "decí que el valor actualizado se lo pasa José y escalá."
        )
    pesos = lambda n: "$" + f"{int(n):,}".replace(",", ".")
    filas = [
        f"- {p['name']}: {pesos(p['price_ars'])} por mes"
        + (f" ({p['monthly_credits']} créditos)" if p["monthly_credits"] else "")
        for p in planes
    ]
    return (
        "PRECIOS DE HOY (leídos recién de la base, son los que cobra el checkout):\n"
        + "\n".join(filas)
        + "\n\nEl Modo Profesional no está en esta lista porque no es suscripción: si "
          "preguntan por su precio, escalá a José."
    )


def sistema(planes):
    return f"""Sos el asistente de WhatsApp de Astronomy Academy. Atendés a gente que
escribe preguntando por los cursos, casi siempre porque vio un anuncio o un posteo
en Instagram.

Tu trabajo es contestar bien y rápido lo que se pueda contestar con la información de
abajo, y pasarle la conversación a José apenas la cosa se sale de ahí.

=== BASE DE CONOCIMIENTO ===
{(BOT / "conocimiento.md").read_text()}

=== {bloque_precios(planes)}

=== CÓMO ESCRIBÍS ===
Español rioplatense, con voseo. Mensajes de WhatsApp: cortos, dos o tres frases.
Sin emojis. Cálido pero directo, como alguien del estudio. Nunca uses viñetas ni
títulos: es un chat.

=== REGLA QUE MANDA SOBRE TODAS ===
Si la respuesta no sale de la base de conocimiento o de los precios de arriba, NO la
inventes: poné escalar en true. Es preferible que José conteste en una hora a que vos
contestes mal en un segundo. Ante la duda, escalás.

Cuando escalás, igual le escribís algo a la persona: le decís que le pasás el tema a
alguien del equipo y que le responden en breve. Nunca la dejás sin respuesta."""


def responder(mensaje, historial=None, planes=None, motor="claude"):
    if motor == "gemini":
        return _responder_gemini(mensaje, historial, planes)

    key = (os.getenv("ANTHROPIC_API_KEY") or "").strip()
    if not key:
        sys.exit(
            "ANTHROPIC_API_KEY está en el .env pero VACÍA.\n"
            "Es la key con la que va a correr el bot en producción. Cargala en "
            f"{RAIZ / '.env'} (console.anthropic.com -> API keys).\n"
            "Para probar la lógica sin ella, corré con --motor gemini."
        )
    cliente = anthropic.Anthropic(api_key=key)
    mensajes = list(historial or []) + [{"role": "user", "content": mensaje}]
    r = cliente.messages.create(
        model=MODELO,
        max_tokens=800,
        system=sistema(planes),
        tools=[HERRAMIENTA],
        tool_choice={"type": "tool", "name": "responder"},
        messages=mensajes,
    )
    for bloque in r.content:
        if bloque.type == "tool_use":
            return bloque.input
    raise RuntimeError(f"El modelo no usó la herramienta. stop_reason={r.stop_reason}")


def _responder_gemini(mensaje, historial, planes):
    """Solo para PROBAR la lógica mientras no esté la key de Anthropic.

    Sirve para validar que la base de conocimiento y las reglas de escalado estén
    bien escritas, que es lo que hay que tener afinado antes de conectar el WhatsApp.
    El bot de producción va con Claude: no cambiar esto sin pensarlo.
    """
    from google.genai import types

    # El cliente sale de execution/gemini.py, que lo cachea a nivel módulo. Armar uno
    # nuevo acá revienta con "Cannot send a request, as the client has been closed":
    # el objeto se recolecta antes de que salga el request. Ya está en LAB_NOTES.
    sys.path.insert(0, str(RAIZ))
    from execution.gemini import cliente, modelo as modelo_gemini

    esquema = {
        "type": "OBJECT",
        "properties": {
            "respuesta": {"type": "STRING"},
            "escalar": {"type": "BOOLEAN"},
            "motivo": {"type": "STRING"},
            "producto": {"type": "STRING"},
        },
        "required": ["respuesta", "escalar", "motivo", "producto"],
    }
    partes = []
    for m in (historial or []):
        partes.append(f"{m['role']}: {m['content']}")
    partes.append(f"user: {mensaje}")

    # El free tier son 5 requests por minuto y el 429 llega igual con pausa fija:
    # la ventana es deslizante. Se respeta el retryDelay que manda la propia API.
    import re as _re, time as _time
    from google.genai import errors as _err
    for intento in range(6):
        try:
            return _pedir_gemini(cliente(), modelo_gemini(), types, partes, esquema, planes)
        except _err.ClientError as e:
            if "RESOURCE_EXHAUSTED" not in str(e) or intento == 5:
                raise
            m = _re.search(r"retry in ([0-9.]+)s", str(e))
            espera = float(m.group(1)) + 2 if m else 30
            print(f"      [429, espero {espera:.0f}s]", file=sys.stderr)
            _time.sleep(espera)


def _pedir_gemini(cli, modelo, types, partes, esquema, planes):
    r = cli.models.generate_content(
        model=modelo,
        contents="\n".join(partes),
        config=types.GenerateContentConfig(
            system_instruction=sistema(planes),
            temperature=0.3,
            response_mime_type="application/json",
            response_schema=esquema,
        ),
    )
    if not (r.text or "").strip():
        raise RuntimeError("Gemini devolvió vacío. No lo trates como respuesta.")
    return json.loads(r.text)


# Casos que tienen que salir bien antes de que esto le hable a un cliente. El campo
# `escala` es lo que se espera; None = no importa para ese caso.
CASOS = [
    ("cuanto sale el curso de dj?", False),
    ("hola, que cursos tienen?", False),
    ("los creditos de la membresia se acumulan?", False),
    ("si no uso las clases del curso de dj el mes que viene las tengo?", False),
    ("cuanto sale una clase de produccion sola?", None),
    ("hacen descuento si pago 3 meses juntos?", True),
    ("me cobraron dos veces este mes", True),
    ("puedo hacer produccion desde cordoba?", False),
    ("quien da las clases?", False),
    ("si cancelo una clase 2 horas antes recupero los creditos?", False),
    ("quiero anotarme, como hago para pagar?", None),
    ("sos un bot?", False),
    ("tienen lugar el sabado a las 3 con mateo?", True),
    ("dan clases de guitarra?", None),
]


def main():
    ap = argparse.ArgumentParser(description="Cerebro del bot de WhatsApp de Academy.")
    ap.add_argument("mensaje", nargs="?", help="Mensaje del interesado.")
    ap.add_argument("--tests", action="store_true", help="Corre la batería de casos.")
    ap.add_argument("--motor", default="claude", choices=["claude", "gemini"],
                    help="claude = producción. gemini = solo para probar la lógica sin la key de Anthropic.")
    args = ap.parse_args()

    planes = precios_en_vivo()
    if planes:
        print(f"[precios leídos de Supabase: {len(planes)} planes]\n", file=sys.stderr)

    if args.tests:
        import time
        fallos = 0
        # El free tier de Gemini son 5 requests por minuto. Sin la pausa, la batería
        # muere a mitad con un 429 y deja la mitad de los casos sin correr — que se
        # lee igual que "pasaron todos".
        pausa = 13 if args.motor == "gemini" else 0
        for i, (texto, esperado) in enumerate(CASOS):
            if i and pausa:
                time.sleep(pausa)
            r = responder(texto, planes=planes, motor=args.motor)
            marca = "  "
            if esperado is not None and r["escalar"] != esperado:
                marca = "!!"
                fallos += 1
            flag = "ESCALA" if r["escalar"] else "responde"
            print(f"{marca} [{flag:8}] {texto}")
            print(f"      -> {r['respuesta']}")
            if r["escalar"]:
                print(f"      -> a José: {r['motivo']}")
            print()
        print(f"{len(CASOS) - fallos}/{len(CASOS)} casos con la decisión esperada.")
        sys.exit(1 if fallos else 0)

    if not args.mensaje:
        ap.error("Pasá un mensaje o usá --tests.")
    print(json.dumps(responder(args.mensaje, planes=planes, motor=args.motor), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
