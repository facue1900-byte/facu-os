# Catálogo — skills del curso

Índice de los 26 skills de `~/Downloads/Claude Code Full Course/All Of My Claude Skills/.claude/skills/`.
Es material del curso, de otro rubro (agencia de automatización + canal de YouTube): **los skills no se
copian, se portan** — se reescribe lo genérico y lo específico va a config (ver Lab Note del 27/07/2026).
Advertencia ya aprendida: los skills de leads del curso "extraen el email del dueño" scrapeando la web
del negocio (`gmaps-leads`) o comprándolo a AnyMailFinder (`scrape-leads`) — eso inventa/adivina datos
de contacto y **no se porta**. `prospectar-gmaps` quedó sin esa parte a propósito.

## Leads / outreach

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `gmaps-leads` | Scrapea Google Maps y "enriquece" cada lead scrapeando su web para sacar contactos. | **Portado → `prospectar-gmaps`** (sin el enriquecimiento de emails, que inventa datos). |
| `scrape-leads` | Leads vía Apify + verificación de rubro + emails comprados a AnyMailFinder + Google Sheets. | **Portado → `prospectar-gmaps`** (misma decisión: la parte de emails quedó afuera). |
| `classify-leads` | Clasifica leads con un LLM para distinciones finas (SaaS vs agencia). | Biblioteca de referencia — el patrón (clasificar en batch con Haiku) ya vive en `clasificador-mails`. |
| `casualize-names` | Convierte nombres formales a versiones casuales para cold email en inglés ("William" → "Will"). | No aplica — truco de cold email en inglés; los apodos no se trasladan al español. |
| `instantly-campaigns` | Crea campañas de cold email en Instantly con A/B testing y secuencias de follow-up. | No aplica — stack de agencia. Si algún día hay outreach masivo (locatarios), se rediseña desde cero con `--send`. |
| `instantly-autoreply` | Responde solo los mails entrantes de campañas usando una base de conocimiento. | No aplica — además contradice la regla de acá: nada sale al mundo sin OK. |
| `upwork-apply` | Scrapea trabajos de Upwork y genera propuestas con cover letter. | No aplica — negocio de freelancing del curso. |

## YouTube / video

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `youtube-outliers` | Busca videos virales del propio nicho y los puntúa (views vs promedio del canal). | Portable si algún día la academia o la rama música apuestan a YouTube; hoy no mueve plata. |
| `cross-niche-outliers` | Lo mismo pero en nichos adyacentes, para robar hooks y estructuras (API TubeLab). | Portable en el mismo escenario que `youtube-outliers`; van juntos o no van. |
| `title-variants` | Genera variantes de títulos de YouTube a partir de los outliers. | Portable solo como acompañante de los dos anteriores. |
| `recreate-thumbnails` | Face-swap de miniaturas de YouTube con la cara del creador del curso (Gemini imagen). | No aplica — está clavado a la cara y al canal del autor. |
| `video-edit` | Corta silencios de videos a cámara (VAD neuronal) y agrega un teaser con transición 3D. | Biblioteca de referencia (ffmpeg + Silero VAD) — está pensado para talking-head, no para aftermovies de eventos. |
| `pan-3d-transition` | La transición 3D "swivel" suelta, renderizada con Remotion. | Biblioteca de referencia (código de Remotion); solo no hace nada útil acá. |

## Infra / deploy

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `modal-deploy` | Deploya los scripts del curso a Modal como funciones serverless y crons. | Biblioteca de referencia (código de Modal) — acá lo programado corre con `launchd` local. |
| `add-webhook` | Alta de un webhook nuevo en la arquitectura de directivas del curso (directive + webhooks.json + deploy). | Biblioteca de referencia (patrón directiva→webhook) — depende de toda la infra Modal del curso. |
| `local-server` | Corre el orquestador local con FastAPI + túnel de Cloudflare para probar webhooks. | Biblioteca de referencia (código de webhooks locales); útil el día que algo externo tenga que llamarnos. |

## Gmail

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `gmail-inbox` | Gestión unificada de varias cuentas de Gmail: buscar, etiquetar, archivar, filtros. | **Portado → `triage-inbox`** (y el multi-cuenta ya vive en `execution/google_auth.py`). |
| `gmail-label` | Clasifica el inbox con subagentes en paralelo (Action/Waiting/Reference) y etiqueta en bulk. | **Portado → `triage-inbox`** (con Plata como categoría propia y ámbitos en `contextos.json`). |

## Skool

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `skool-monitor` | Lee, postea y responde en comunidades Skool vía API reverseada. | No aplica — comunidad del curso. No operamos Skool. |
| `skool-rag` | RAG sobre el contenido de la comunidad (embeddings OpenAI + Pinecone + rerank). | No aplica como skill; el pipeline RAG queda como referencia si la academia arma base de conocimiento consultable. |

## Cliente / propuestas

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `create-proposal` | Genera propuestas en PandaDoc desde datos estructurados o transcript de una llamada de venta. | **Portándose → `propuestas`** (esta pasada). |
| `onboarding-kickoff` | Orquesta el alta de un cliente de agencia: leads + campañas + auto-reply, todo encadenado. | No aplica — encadena tres skills que no portamos. El patrón de orquestación sí es lindo de mirar. |
| `welcome-email` | Manda una secuencia de 3 mails de bienvenida firmados por distintas personas del equipo. | No aplica — plantillas de la agencia del curso; y mandaría mails solo, cosa que acá no existe sin `--send`. |
| `design-website` | Genera un mockup de landing premium para un prospecto desde una fila de un Sheet. | Biblioteca de referencia (generación de HTML editorial); Astronomy ya tiene web en producción. |

## Research

| Skill | Qué hace | ¿Sirve acá? |
|---|---|---|
| `literature-research` | Busca papers en PubMed y arma reviews de literatura. | No aplica — académico, de otro mundo. |
| `generate-report` | Baja data real de una API (clima de Canadá) y arma un PDF prolijo con template de reporte anual. | Portable: el contenido no sirve, pero el patrón data→PDF con template es exactamente lo que falta para reportes a terceros. |

---

## Si hubiera que portar uno más

**`generate-report`, reconvertido en reporte PDF mensual para inversores del Paseo.** El clima de
Canadá no importa; lo que vale es el esqueleto: script que junta data real → PDF con template
presentable, sin que el modelo toque un número. Los números ya existen — los produce
`cierre-mes-nordelta` contra el extracto del Macro — así que el porte es solo la capa de
presentación, y respeta la regla de que lo que puede ser código es código. Es el único de la lista
que toca plata directamente este mes: inversores, recupero y plan de financiación necesitan un
entregable prolijo y hoy eso se arma a mano. Los de YouTube son los más tentadores, pero no mueven
ingresos ni ahorran horas hasta que exista un canal; quedan anotados, no se construyen.
