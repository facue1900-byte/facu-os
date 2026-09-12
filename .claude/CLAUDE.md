# facu-os

El repo que ejecuta. Quién es Facu y los negocios viven en `~/.claude/CLAUDE.md` (global);
las reglas de trabajo, en `os/` (Constitución, Playbook, Empresa). **Valen acá también,
no se repiten.** Este archivo es solo la mecánica: dónde vive cada cosa, cómo se corre,
qué no se toca.

Negocios activos: **Astronomy** (eventos, academia, música), **Paseo Nordelta** (paseo
comercial) y **campos** (Chaco, Pergamino).

> **Pendiente: revisar Nordelta Plaza (NDPL SAS) y Noreventos en un futuro con Facu.**
> Quedó viejo y hoy no se toca — su data cruda sigue en `~/Desktop/Nordelta Plaza/` y
> `~/Desktop/Noreventos/`. Es **otro negocio** que Paseo Nordelta: otra sociedad, otros
> socios, otro banco. Nunca sumar sus números con los del Paseo.

---

## Estructura

| Qué | Para qué |
|---|---|
| `os/` | **El Empresa OS: las reglas.** `01-CONSTITUCION.md` (no negociable, se importa sola en toda sesión), `02-PLAYBOOK.md` (el método) y `03-EMPRESA.md` (KPIs, estándares, dónde se escribe cada cosa). |
| `.claude/skills/` | Las capacidades. Una subcarpeta por skill (`SKILL.md` + `scripts/`). Se auto-descubren. |
| `.claude/agents/` | Subagentes. Los de verificación reportan, no corrigen lo que auditan. |
| `active/` | Estado operativo por negocio. Un `ESTADO.md` por frente abierto, **con sus pendientes de dato**. |
| `archive/` | Lo cerrado y los crudos importados. No se borra nunca: es la historia. |
| `data/` | Data cruda (xlsx, PDFs, exports). Gitignoreada. |
| `execution/` | Utilidades compartidas entre skills, más `launchd/` (plists de tareas programadas). |
| `SETUP.md` | **El estado real de la infra**: qué está conectado, qué falta, el inventario de plataformas y el estado de cada skill. Ese dato no se duplica acá porque envejece. |
| `LAB_NOTES.md` | Todo lo que se rompió, se aprendió o salió bien de forma no obvia. |
| `CATALOGO_SKILLS_CURSO.md` | Los 26 skills del curso indexados: qué hay y qué vale portar. |

**La data real vive fuera del repo**, en el Desktop, y se referencia por path absoluto
(hay scripts y tareas programadas que la abren por path — no mover sin avisar):

| Qué | Dónde |
|---|---|
| Paseo Nordelta (extractos Macro, cierre de mes) | `~/Desktop/Paseo Nordelta/` |
| Guías de traslado de hacienda (Chaco) | `~/Desktop/Chaco/` |
| Astronomy y Puzzle | `~/Desktop/Productoras/` (Astronomy → `Academia/`, `Eventos/`, `Marca Astronomy/`) |
| Segundo cerebro (Obsidian) | `~/Obsidian/facu-vault/` |

`~/Claude-Workspace/` es **read-only**: template del curso, otro rubro. Biblioteca de
código de ejemplo, no una capacidad de este OS.

---

## Los repos de las apps — dónde está el código que se toca todos los días

**Este repo no es donde vive el software de los negocios.** La mayoría de las sesiones
terminan editando uno de estos cuatro, y cada uno pega contra **su propia** base:

| App | Dónde está clonado | Stack | Base | Deploy |
|---|---|---|---|---|
| **Astronomy** (academia + eventos + ticketera) | `~/Desktop/Productoras/Astronomy/Academia/astronomy-members` | Next 16 | Supabase `qeakrjnseboiulcojlcw` | **push a `main` deploya solo** (Vercel, `astronomyofficial.com`) |
| **App del Paseo** | `~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/App Paseo Nordelta` | Vite + TS | Supabase `wujutradczplokjrgmdo` | Netlify, **un sitio por rol** (ver `SETUP.md`) |
| **Aforo** | `~/Desktop/Aforo/aforo-app` | Next | — | sin remoto todavía |
| **IVA Estevez** (Chaco) | `~/Desktop/Chaco/App IVA Estevez` | — | — | sin remoto todavía |

> **Las dos bases de Supabase son de negocios distintos.** Un `ref` equivocado escribe en
> el negocio equivocado y no avisa. Antes de un query o una migración, confirmar cuál.

En `astronomy-members` hay **44 verificadores** ya escritos (`npm run verificar:*` y
`test:*`): antes de escribir uno nuevo, `npm run` y buscar si ya existe el que hace falta.
Corren contra la base real, así que valen las reglas del Playbook: **un verificador que
escribe se crea su propio objeto descartable, y ninguno manda nada al mundo.**

---

## Skills

`cierre-mes-nordelta` · `triage-inbox` · `grabacion-a-tareas` · `consenso` ·
`prospectar-gmaps` · `propuestas` · `flyers`. Qué hace cada uno está en su `SKILL.md`;
**cuál está productivo y cuál bloqueado, en `SETUP.md`.**

**Los skills se escriben genéricos y lo específico va en config** (`contextos.json`,
`--contexto`). Un skill clavado a un negocio sirve para uno; parametrizado sirve para
los cuatro y para el próximo.

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

**Cuándo va cada uno: la tabla de ruteo está en `os/02-PLAYBOOK.md` §2.** Lo único que
hay que tener presente siempre: el hilo principal corre en Opus y **el único ruteo real
es delegar** — si el trabajo mecánico no se delega, la política de modelos no ejecuta
nada. Y **lo que decide no se delega**: el `mecanico` trae los datos, la conclusión la
saca el hilo principal.

---

## Stack

Todo en el home, sin sudo. Shell de login **bash**: el PATH vive en `~/.profile`
(`~/.bashrc` lo sourcea; `~/.zshrc` tiene copia). Detalle, tokens e inventario de
plataformas en `SETUP.md`.

| Qué | Dónde |
|---|---|
| Node 24 + npm, `claude`, `gemini`, `netlify`, `vercel`, `supabase` CLIs | `~/.local/node/bin/` |
| `uv` + Python 3.12 | `~/.local/bin/` |
| venv del OS (PyMuPDF, openpyxl, google-api, dotenv) | `~/facu-os/.venv/` |
| `gh` CLI | `~/.local/gh/bin/` |
| Obsidian (abrir siempre desde `/Applications`, nunca desde el `.dmg`) | `/Applications/Obsidian.app` |

Todo se corre con **path absoluto** y con el Python del venv — el `python3` del sistema
es 3.9, sin las dependencias (por eso el linter del IDE marca `Cannot find module` sobre
`httpx` o `dotenv`: es ruido, mira el Python equivocado):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/radar_rampa.py" \
  /Users/Facu/facu-os/data/master_plan.xlsx 2026-08
```

Tests: `.venv/bin/python -m pytest execution/tests/ -q`. Van solo sobre `execution/`;
los skills se verifican corriéndolos.

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

## Cómo se trabaja acá

Las reglas generales están en `os/` y **rigen acá**: plata sin improvisar, verificar
antes de decir "listo", nada sale al mundo sin OK, no parchear un chequeo que falla.
Lo propio de este repo:

**Cambios no triviales, el orden es:** escribo el código → corro `code-reviewer` y `qa`
en paralelo (y `numeros` si toca plata) → leo los reportes y aplico los fixes yo, en el
hilo principal → recién ahí se usa. **El agente que escribió el código está sesgado a
decir que está bien.**

**Se rompe algo:** causa raíz → lo pruebo → actualizo el `SKILL.md` o el doc afectado →
Lab Note en `LAB_NOTES.md`. Postmortem completo allá, lección corta en el doc. Si es un
patrón que va a seguir siendo cierto en un año, se destila al vault.

**Las tres capas** (repo / memoria / vault): la tabla vive en `os/03-EMPRESA.md` →
*Dónde se escribe cada cosa*. La parte del repo es código, skills y estado operativo por
frente. Si las capas se mezclan, este archivo se llena de data vieja y empieza a mentir.

**El índice de memoria tiene techo.** `~/.claude/projects/-Users-Facu-facu-os/memory/MEMORY.md`
se corta pasados ~24 KB y las líneas de abajo dejan de cargarse **sin avisar**. Una
memoria nueva entra como **una línea corta** y el detalle va en su archivo; el detalle de
Paseo Nordelta ya se mudó a `indice-paseo.md` por esto mismo. Si el índice vuelve a pasar
el techo, se poda antes de seguir agregando.
