---
name: grabacion-a-tareas
description: Convierte cualquier grabación de audio o video en una lista de tareas con responsable y plazo, más las decisiones que se tomaron y lo que quedó abierto. Usar cuando haya una reunión, llamada, nota de voz de WhatsApp, visita a obra, clase o entrevista grabada y haya que sacar en limpio qué hay que hacer.
allowed-tools: Bash, Read, Write
---

# Grabación a tareas

Le pasás una grabación y sale un `.md` con las tareas tildables, quién las tiene,
para cuándo, y la **frase textual** de donde sale cada una.

No asume ningún dominio: sirve igual para una reunión de obra, una llamada con un
proveedor, una nota de voz, o una clase. Lo específico se pasa por `--contexto`.

## Cómo se corre

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/grabacion-a-tareas/scripts/extraer_tareas.py" \
  --archivo "/Users/Facu/Desktop/reunion.m4a" \
  --salida "/Users/Facu/Desktop/reunion-tareas.md"
```

| Flag | Qué hace |
|---|---|
| `--archivo` | Audio o video. Formatos: mp3, m4a, **opus** (notas de voz de WhatsApp), wav, aiff, flac, ogg, mp4, mov, webm, avi. |
| `--contexto` | Opcional pero **conviene**: de qué se trata, quiénes participan, qué jerga se usa. Sin esto los nombres propios salen mal escritos. |
| `--salida` | El `.md` con las tareas. |
| `--json` | Opcional, el JSON crudo por si hay que procesarlo después. |

Ejemplo con contexto:

```bash
  --contexto "Reunión de obra de un local comercial. Ana y Luis son de administración; \
Toldos Sur es un proveedor."
```

## Qué sale

- **Tareas** agrupadas por urgencia (alta / media / baja), como checkboxes.
- **Decisiones** que se tomaron.
- **Quedó abierto** — lo que se pateó para después. Esto es lo que se suele
  perder entre una reunión y la siguiente.
- **Números mencionados**, en una tabla aparte y marcados como dichos, no
  verificados.
- **Audio dudoso** — dónde no se entendió bien, para ir a escuchar ese pedazo.

## Reglas

- **Cada ítem tiene su cita textual.** Si no se puede citar la frase, no entra.
  Nada de inferir una tarea que nadie dijo.
- **Un número dicho en una reunión no es un dato.** Van todos a su propia tabla
  con la advertencia puesta. Antes de que uno entre a una planilla o salga hacia
  un tercero, se verifica contra la fuente. Para eso está el skill `consenso`.
- **Cero tareas es un resultado posible**, no un error: hay charlas donde nadie
  se compromete a nada. El script lo dice explícitamente en vez de dejar la
  sección vacía y que parezca que falló.
- **Si el script avisa que la respuesta vino incompleta, no lo ignores.** Sale
  con código 1 y lista qué faltó. El `.md` igual se escribe, pero no está
  completo.

## Costo y tiempo

Corre con Gemini (`GEMINI_MODEL` del `.env`), que es lo barato. Una grabación de
una hora tarda unos minutos entre subir, procesar y analizar. El archivo se sube
a la Files API de Google y **se borra apenas termina**, incluso si el análisis
falla.

## Lecciones

- **Probado con audio real, no con un mock.** Se generó una reunión con `say` de
  macOS y se corrió el pipeline completo contra Gemini: extrajo las 2 tareas con
  su responsable y plazo, la decisión, el tema abierto y el monto, cada uno con
  su cita. Un extractor de tareas validado solo con JSON de mentira no está
  validado.
- **El audio dudoso se declara, no se adivina.** Si el modelo no entendió un
  pedazo, eso va en su propia sección. Una transcripción que rellena los huecos
  con lo más probable es la peor clase de error: no se nota.
