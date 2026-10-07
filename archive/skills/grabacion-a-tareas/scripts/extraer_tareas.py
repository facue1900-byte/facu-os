#!/usr/bin/env python3
"""
Convierte una grabación (audio o video) en la lista de qué hay que hacer.

    .venv/bin/python .claude/skills/grabacion-a-tareas/scripts/extraer_tareas.py \
        --archivo ~/Desktop/reunion.m4a \
        --salida ~/Desktop/reunion-tareas.md

Sirve para cualquier grabación: una reunión, una llamada, una nota de voz de
WhatsApp, una visita a obra, una clase. No asume ningún dominio — si le pasás
`--contexto`, lo usa para desambiguar nombres y jerga.

Lo que sale:
  - tareas, con quién / para cuándo / qué tan urgente
  - decisiones que se tomaron
  - temas que quedaron abiertos, sin resolver
  - números y montos mencionados, marcados como **dichos, no verificados**

Ese último punto importa: lo que alguien dice en una reunión no es un dato
contable. Se transcribe con la cita textual al lado y se verifica aparte.
"""

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4]))

from execution.gemini import leer_media  # noqa: E402

URGENCIAS = ["alta", "media", "baja"]

PROMPT = """Escuchá/mirá esta grabación completa y extraé lo accionable.

Devolvé SOLO un objeto JSON con esta forma exacta:

{{
  "resumen": "2 o 3 oraciones sobre de qué se trató",
  "participantes": ["nombres que hayas podido identificar"],
  "tareas": [
    {{"que": "la acción concreta, en infinitivo",
      "quien": "a quién le queda, o 'sin asignar'",
      "cuando": "la fecha o plazo que se dijo, o 'sin plazo'",
      "urgencia": "alta|media|baja",
      "cita": "la frase textual de la grabación de donde sale esto"}}
  ],
  "decisiones": [
    {{"decision": "qué se resolvió", "cita": "la frase textual"}}
  ],
  "abierto": [
    {{"tema": "qué quedó sin resolver", "cita": "la frase textual"}}
  ],
  "numeros": [
    {{"valor": "el número o monto tal como se dijo",
      "de_que": "a qué se refiere",
      "cita": "la frase textual"}}
  ],
  "audio_dudoso": ["momentos donde no se entendió bien y puede haber error"]
}}

Reglas, en orden de importancia:

1. **Cada ítem lleva su cita textual.** Si no podés citar la frase de donde sale,
   no lo pongas. Nada de inferir una tarea que nadie dijo.
2. **No inventes plazos, nombres ni montos.** Si no se dijo, poné "sin plazo" o
   "sin asignar". Un plazo inventado es peor que ninguno.
3. **Los números van tal cual se dijeron**, sin convertir monedas, sin redondear
   y sin calcular nada. Van en "numeros" aunque también aparezcan en una tarea.
4. Si algo no se entiende por el audio, va en "audio_dudoso" en vez de adivinar.
5. Una lista vacía es una respuesta válida. Si no hubo decisiones, "decisiones"
   va vacío. No rellenes para que parezca completo.

Escribí en español rioplatense.{contexto}"""


def validar(datos):
    """Chequea la forma de lo que devolvió el modelo. Devuelve lista de problemas."""
    problemas = []
    if not isinstance(datos, dict):
        return [f"la respuesta no es un objeto JSON sino {type(datos).__name__}"]

    for clave in ["resumen", "participantes", "tareas", "decisiones",
                  "abierto", "numeros", "audio_dudoso"]:
        if clave not in datos:
            problemas.append(f"falta la clave '{clave}'")

    for i, t in enumerate(datos.get("tareas") or []):
        for campo in ["que", "quien", "cuando", "urgencia", "cita"]:
            if not t.get(campo):
                problemas.append(f"tarea {i + 1}: falta '{campo}'")
        if t.get("urgencia") and t["urgencia"] not in URGENCIAS:
            problemas.append(f"tarea {i + 1}: urgencia '{t['urgencia']}' "
                             f"no es una de {URGENCIAS}")
    return problemas


def a_markdown(datos, origen, contexto):
    """Arma el .md legible."""
    L = [f"# Tareas de {origen}", ""]
    if contexto:
        L += [f"_Contexto dado: {contexto}_", ""]
    L += [datos.get("resumen", ""), ""]

    if datos.get("participantes"):
        L += ["**Participantes:** " + ", ".join(datos["participantes"]), ""]

    tareas = datos.get("tareas") or []
    L += [f"## Tareas ({len(tareas)})", ""]
    if not tareas:
        L += ["_Ninguna. Nadie se comprometió a nada concreto._", ""]
    for u in URGENCIAS:
        del_nivel = [t for t in tareas if t.get("urgencia") == u]
        if not del_nivel:
            continue
        L += [f"### Urgencia {u} ({len(del_nivel)})", ""]
        for t in del_nivel:
            L.append(f"- [ ] **{t['que']}**")
            L.append(f"  - quién: {t['quien']} · cuándo: {t['cuando']}")
            L.append(f"  - _\"{t['cita']}\"_")
        L.append("")

    if datos.get("decisiones"):
        L += [f"## Decisiones ({len(datos['decisiones'])})", ""]
        for d in datos["decisiones"]:
            L += [f"- **{d['decision']}**", f"  - _\"{d['cita']}\"_"]
        L.append("")

    if datos.get("abierto"):
        L += [f"## Quedó abierto ({len(datos['abierto'])})", ""]
        for a in datos["abierto"]:
            L += [f"- {a['tema']}", f"  - _\"{a['cita']}\"_"]
        L.append("")

    if datos.get("numeros"):
        L += [f"## Números mencionados ({len(datos['numeros'])})", "",
              "> **Esto es lo que se dijo, no un dato verificado.** Antes de que "
              "cualquiera de estos números entre a una planilla o salga hacia un "
              "tercero, hay que chequearlo contra la fuente.", ""]
        L += ["| Valor | De qué | Se dijo |", "|---|---|---|"]
        for n in datos["numeros"]:
            cita = n["cita"].replace("|", "\\|")
            L.append(f"| {n['valor']} | {n['de_que']} | _\"{cita}\"_ |")
        L.append("")

    if datos.get("audio_dudoso"):
        L += ["## Audio dudoso", "",
              "Momentos donde no se entendió bien. Si alguno toca algo "
              "importante, escuchalo vos:", ""]
        for d in datos["audio_dudoso"]:
            L.append(f"- {d}")
        L.append("")

    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archivo", "-a", required=True,
                   help="Audio o video (mp3, m4a, opus, wav, mp4, mov...)")
    p.add_argument("--contexto", "-c", default="",
                   help="Contexto del dominio: de qué se trata, quiénes son, "
                        "qué jerga se usa. Ayuda a no confundir nombres.")
    p.add_argument("--salida", "-o", required=True, help="Markdown de salida")
    p.add_argument("--json", help="Opcional: guardar también el JSON crudo")
    args = p.parse_args()

    origen = pathlib.Path(args.archivo)

    extra = (f"\n\nContexto de esta grabación, para que no confundas nombres "
             f"ni jerga: {args.contexto}") if args.contexto else ""
    crudo = leer_media(args.archivo, PROMPT.format(contexto=extra),
                       json_estricto=True)

    try:
        datos = json.loads(crudo)
    except json.JSONDecodeError as e:
        sys.exit(f"El modelo no devolvió JSON válido ({e}).\n"
                 f"Devolvió esto:\n\n{crudo[:800]}")

    problemas = validar(datos)
    if problemas:
        # No se arregla a mano lo que el modelo devolvió mal: se avisa.
        print("La respuesta vino incompleta:", file=sys.stderr)
        for x in problemas:
            print(f"  - {x}", file=sys.stderr)
        print("\nRevisá el .md que igual se escribió, pero no lo des por "
              "completo.", file=sys.stderr)

    salida = pathlib.Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(a_markdown(datos, origen.name, args.contexto))

    if args.json:
        j = pathlib.Path(args.json)
        j.parent.mkdir(parents=True, exist_ok=True)
        j.write_text(json.dumps(datos, indent=2, ensure_ascii=False))

    t = len(datos.get("tareas") or [])
    print(f"\n{t} tareas · {len(datos.get('decisiones') or [])} decisiones · "
          f"{len(datos.get('abierto') or [])} abiertos · "
          f"{len(datos.get('numeros') or [])} números")
    print(f"Escrito en {salida}")

    if t == 0:
        print("\nOJO: cero tareas. Puede ser una charla sin compromisos, o "
              "puede ser que el audio no se haya entendido.", file=sys.stderr)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
