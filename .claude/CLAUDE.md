# facu-os

El repo que ejecuta. Quién es Facu, los negocios y las reglas generales de trabajo viven
en `~/.claude/CLAUDE.md` (global) — **valen acá también, no se repiten**. Este archivo es
solo la mecánica: dónde vive cada cosa, cómo se corre, qué no se toca.

Negocios: **Astronomy** (eventos, academia, música), **Paseo Nordelta** (paseo comercial),
**Nordelta Plaza** (predio, NDPL SAS) y **campos** (Chaco, Pergamino).

> **Paseo Nordelta y Nordelta Plaza son dos negocios distintos.** Otra sociedad, otros
> socios, otro banco (Macro vs BBVA), otras carpetas. Nunca sumar sus números ni asumir
> que un dato de uno aplica al otro.

---

## Estructura

| Qué | Para qué |
|---|---|
| `.claude/skills/` | Las capacidades. Una subcarpeta por skill (`SKILL.md` + `scripts/`). Se auto-descubren. |
| `.claude/agents/` | Subagentes de verificación: reportan, no corrigen lo que auditan. |
| `active/` | Estado operativo por negocio. Un `ESTADO.md` por frente abierto, **con sus pendientes de dato**. |
| `archive/` | Lo cerrado y los crudos importados. No se borra nunca: es la historia. |
| `data/` | Data cruda (xlsx, PDFs, exports). Gitignoreada. |
| `execution/` | Utilidades compartidas entre skills, más `launchd/` (plists de tareas programadas). |
| `SETUP.md` | Qué está conectado y qué falta, con el paso a paso. **El estado real de la infra vive ahí.** |
| `LAB_NOTES.md` | Todo lo que se rompió, se aprendió o salió bien de forma no obvia. |
| `CATALOGO_SKILLS_CURSO.md` | Los 26 skills del curso indexados: qué hay y qué vale portar. |

**La data real vive fuera del repo**, en el Desktop, y se referencia por path absoluto
(hay scripts y tareas programadas que la abren por path — no mover sin avisar):

| Qué | Dónde |
|---|---|
| Paseo Nordelta (extractos Macro, cierre de mes) | `~/Desktop/Paseo Nordelta/` |
| Nordelta Plaza (BBVA, contratos, expensas, societario) | `~/Desktop/Nordelta Plaza/` |
| Noreventos SRL (socio del predio de Nordelta Plaza) | `~/Desktop/Noreventos/` |
| Guías de traslado de hacienda (Chaco) | `~/Desktop/Chaco/` |
| Astronomy y Puzzle | `~/Desktop/Productoras/` |
| Segundo cerebro (Obsidian) | `~/Obsidian/facu-vault/` |

`~/Claude-Workspace/` es **read-only**: template del curso, otro rubro. Biblioteca de
código de ejemplo, no una capacidad de este OS.

---

## Skills

| Skill | Qué hace | Estado |
|---|---|---|
| `cierre-mes-nordelta` | Concilia el extracto del Macro contra el Master Plan (`scripts/conciliar.py` hace los chequeos deterministas), caja, categorías huérfanas y radar de la rampa. | Productivo |
| `triage-inbox` | Clasifica el inbox en Plata / Acción / Esperando / Referencia con subagentes en paralelo. Reporte primero; etiquetar en Gmail va detrás de `--send`. | Productivo (etiquetar bloqueado: faltan scopes `gmail.modify`/`gmail.labels`) |
| `grabacion-a-tareas` | Audio o video → tareas con responsable, plazo y cita textual. | Productivo |
| `consenso` | N auditores independientes al mismo cálculo sin verse, y compara. Para números que salen a un tercero. | Productivo |
| `prospectar-gmaps` | Negocios reales desde Google Maps a CSV. | Falta `APIFY_API_TOKEN` |
| `propuestas` | Propuesta comercial en HTML/PDF por tipo de destinatario (`destinatarios.json`). Genera y frena: no manda. | Productivo |
| `flyers` | Tandas de flyers PNG para Astronomy Academy (5 productos × 5 ángulos × 3 formatos). Precios sincronizados desde Supabase; render con Chrome headless. | Productivo |

**Los skills se escriben genéricos y lo específico va en config** (`contextos.json`,
`--contexto`). Un skill clavado a un negocio sirve para uno; parametrizado sirve para
los cuatro y para el próximo.

Un skill nuevo se crea **solo después de haber hecho la tarea 3 veces a mano**, y solo
si Facu lo pide. Un skill que no se usa es deuda.

## Subagentes

| Agente | Para qué | Modelo |
|---|---|---|
| `numeros` | Audita cualquier cálculo que toque plata, contra la fuente. Su checklist es también el del skill `consenso`. | Opus |
| `auditor-consenso` | Igual que `numeros` pero escribe JSON, para correr de a varios. | Opus |
| `clasificador-mails` | Clasifica un chunk de mails. Lo usa `triage-inbox`. | Haiku |
| `mecanico` | Trabajo de dedos: leer, grepear, contar, extraer campos, resumir. Devuelve datos, no conclusiones. | Haiku |
| `redactor` | Escribe texto para terceros: mails, propuestas, copies. Genera y frena. | Sonnet |
| `code-reviewer` | Revisa código sin contexto del repo. | Sonnet |
| `qa` | Escribe tests, **los corre**, y reporta. | Sonnet |
| `research` | Investiga a fondo sin ensuciar el contexto principal. | Sonnet |

### Ruteo de modelos: la política necesita mecanismo

El hilo principal corre en **Opus** siempre — un skill no puede bajarse el modelo, no
existe esa palanca. **El único ruteo real es delegar.** Si el trabajo mecánico no se
delega, la política de "Haiku clasifica · Sonnet genera · Opus para plata" es una
declaración que no ejecuta nada.

Antes de arrancar una tarea, el hilo principal se pregunta qué parte no necesita criterio:

| Si la tarea es… | Va a |
|---|---|
| Leer varios archivos, grepear, contar filas, extraer campos, resumir un PDF largo | `mecanico` |
| Escribir un mail, una propuesta, un copy, una respuesta a un proveedor | `redactor` |
| Buscar en la web o recorrer código desconocido | `research` |
| Cualquier número que salga a un tercero | `numeros` (o el skill `consenso`) |
| Decidir, arquitectura, estrategia, qué decir | se queda en el hilo principal |

**Un solo archivo chico se lee directo** — delegar cuesta más que leerlo. El umbral es
"más de un par de archivos, o uno grande".

**Lo que decide no se delega.** El `mecanico` trae los datos, el hilo principal saca la
conclusión. El `redactor` escribe el borrador, el hilo principal decide qué se dice.
Delegar el criterio a un modelo más chico es cómo se rompe esto.

Todo se corre con **path absoluto** y con el Python del venv — el `python3` del sistema
es 3.9, sin las dependencias (por eso el linter del IDE marca `Cannot find module`
sobre `httpx` o `dotenv`: es ruido, mira el Python equivocado):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/radar_rampa.py" \
  /Users/Facu/facu-os/data/master_plan.xlsx 2026-08
```

Tests: `.venv/bin/python -m pytest execution/tests/ -q`. Van solo sobre `execution/`;
los skills se verifican corriéndolos.

---

## Stack

Todo en el home, sin sudo. Shell de login **bash**: el PATH vive en `~/.profile`
(`~/.bashrc` lo sourcea; `~/.zshrc` tiene copia). Detalle y verificaciones en `SETUP.md`.

| Qué | Dónde |
|---|---|
| Node 24 + npm, `claude`, `gemini`, `netlify`, `vercel`, `supabase` CLIs | `~/.local/node/bin/` |
| `uv` + Python 3.12 | `~/.local/bin/` |
| venv del OS (PyMuPDF, openpyxl, google-api, dotenv) | `~/facu-os/.venv/` |
| `gh` CLI | `~/.local/gh/bin/` |
| Obsidian (abrir siempre desde `/Applications`, nunca desde el `.dmg`) | `/Applications/Obsidian.app` |

**Vercel y Supabase van por token, no por login interactivo** (el login de navegador no
sirve headless para launchd). Los tokens ya están cargados en el `.env` (`VERCEL_TOKEN`,
`SUPABASE_ACCESS_TOKEN`). Netlify ya autenticado (team Astronomy).

**Inventario de infraestructura** (verificado con los tokens el 27/07/2026):

| Plataforma | Qué hay |
|---|---|
| Vercel | Team `astronomyofficial` · proyecto `astronomy` → **astronomyofficial.com** en producción |
| Supabase | **Dos** proyectos, los dos sanos: `qeakrjnseboiulcojlcw` (Astronomy Oficial) y `wujutradczplokjrgmdo` (**Paseo Nordelta**) |
| GitHub | `facue1900-byte/facu-os` (privado) y `facue1900-byte/astronomy-members` |
| Google Cloud | Proyecto `astronomy-app-502618`, service account `astronomy-calendar@…` (Sheets + Calendar, impersona `studio@astronomyofficial.com`) |

> Son **dos bases de Supabase distintas**, igual que Paseo Nordelta y Nordelta Plaza son
> dos negocios distintos. Antes de una migración o un query, confirmar contra cuál.

Sitios de Netlify de la app del Paseo — un deploy por rol (URLs completas, con sufijo):
`lucent-buttercream-8ac45a` = Mati · `whimsical-alfajores-91122a` = Inversores ·
`dancing-elf-c4ed3f` = Admin. (`dapper-cajeta-537756` es de Astronomy, no tocar.)

## Utilidades compartidas (`execution/`)

- **`google_auth.py`** — OAuth **multi-cuenta** para Sheets, Drive y Gmail. `sheets()`,
  `drive()`, `gmail()` y `bajar_xlsx()` aceptan `cuenta=` (default `facu`). Cuentas:
  `facu` (facue1900@) y `studio` (studio@astronomyofficial). **`facu` llega a todo y
  escribe en todo: es el default correcto** — la matriz de acceso por planilla está en
  `SETUP.md`.

  ```bash
  .venv/bin/python execution/google_auth.py --setup --cuenta facu
  .venv/bin/python execution/google_auth.py --listar
  ```

- **`gemini.py`** — `preguntar()`, `leer_imagen()`, `leer_media()`. Para volumen barato:
  fotos, capturas, transcripciones. El modelo sale de `GEMINI_MODEL` en el `.env` (sin
  default hardcodeado a propósito; antes de fijar uno nuevo, probarlo con un
  `generate_content` real — `--modelos` lista modelos que la key no puede usar).
  **Nunca** para decidir un número que va a un reporte de plata — eso se calcula en
  Python contra la fuente.

---

## Reglas del repo

Las reglas generales (plata sin improvisar, verificar antes de "listo", nada sale al
mundo sin OK, no parchear chequeos) están en el global y **rigen acá**. Las propias de
este repo:

**Lo que puede ser código, es código.** Si un skill me pide "calculá el promedio", está
mal escrito: eso va en Python. Yo decido *cuál* y *qué decir*, no cuánto da la cuenta.

**Los secretos van en `.env`.** Si falta una key, se pide — no se inventa ni se usa un
placeholder que falle en silencio.

## Workflow para cambios no triviales

1. Escribo el código.
2. Corro `code-reviewer` y `qa` en paralelo (y `numeros` si toca plata).
3. Leo los reportes y aplico los fixes yo, en el hilo principal.
4. Recién ahí se usa.

El agente que escribió el código está sesgado a decir que está bien.

## El loop de aprendizaje

Se rompe → arreglo la causa raíz → lo pruebo → actualizo el `SKILL.md` → Lab Note en
`LAB_NOTES.md`. Doble escritura: postmortem completo en `LAB_NOTES.md`, lección corta
en el `SKILL.md` afectado. Si es un patrón transferible, se destila al vault.

## Las tres capas

| Capa | Dónde | Qué va |
|---|---|---|
| Ejecución | este repo | Código y estado operativo. |
| Estado | memoria de Claude Code (`~/.claude/projects/-Users-Facu-facu-os/memory/`) | En qué quedó cada cosa. |
| Conocimiento | `~/Obsidian/facu-vault/` | Lo que sigue siendo cierto dentro de un año. |

Si se mezclan, este archivo se llena de data vieja y empieza a mentir.

Modelos por tarea: la política y los IDs viven en el global (Haiku clasifica · Sonnet
genera · Opus para plata y arquitectura).
