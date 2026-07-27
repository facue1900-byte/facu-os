# facu-os

El repo que ejecuta. Quién soy y qué quiero está en `~/.claude/CLAUDE.md` (global);
acá va la mecánica: dónde vive cada cosa, cómo se corren los scripts, qué no se toca.

Negocios: **Astronomy** (eventos, academia, música), **Paseo Nordelta** (paseo comercial),
**Nordelta Plaza** (predio, NDPL SAS) y **campos** (Chaco, Pergamino).

> **Paseo Nordelta y Nordelta Plaza son dos negocios distintos.** Otra sociedad, otros
> socios, otro banco (Macro vs BBVA), otras carpetas. Nunca sumar sus números ni asumir
> que un dato de uno aplica al otro.

---

## Estructura

| Carpeta | Para qué |
|---|---|
| `.claude/skills/` | Las capacidades. Una subcarpeta por skill (`SKILL.md` + `scripts/`). Se auto-descubren. |
| `.claude/agents/` | Subagentes read-only: reportan, no arreglan. |
| `active/` | Estado operativo por negocio. Un `.md` o carpeta por frente abierto. |
| `archive/` | Lo cerrado. No se borra nunca: es la historia. |
| `data/` | Data cruda (xlsx, PDFs, exports). Gitignoreada. |
| `execution/` | Utilidades compartidas entre skills. |
| `LAB_NOTES.md` | Todo lo que se rompió, se aprendió o salió bien de forma no obvia. |

**La data real vive fuera del repo**, en el Desktop, y se referencia por path absoluto.
No se mueve sin avisar — hay tareas programadas y scripts que la abren por path:

| Qué | Dónde |
|---|---|
| Paseo Nordelta (extractos Macro, cierre de mes) | `~/Desktop/Paseo Nordelta/` |
| Nordelta Plaza (BBVA, contratos, expensas, societario) | `~/Desktop/Nordelta Plaza/` |
| Noreventos SRL (socio del predio de Nordelta Plaza) | `~/Desktop/Noreventos/` |
| Logos Paseo Nordelta | `~/Desktop/Paseo Nordelta/Logotipos Nordelta Plaza/` |
| Guías de traslado de hacienda (Chaco) | `~/Desktop/Chaco/` |
| Astronomy y Puzzle | `~/Desktop/Productoras/` |
| Segundo cerebro (Obsidian) | `~/Obsidian/facu-vault/` |

`~/Claude-Workspace/` es **read-only**: es el template del curso, de otro rubro. Sirve
como biblioteca de código de ejemplo (Modal, webhooks, scraping). No es una capacidad
de este OS y sus skills no aplican a estos negocios.

---

## Skills

| Skill | Qué hace | Estado |
|---|---|---|
| `cierre-mes-nordelta` | Concilia el extracto del Macro contra el sheet Master Plan, chequea caja, categorías huérfanas y el radar de la rampa de alquileres. | Productivo |
| `triage-inbox` | Clasifica el inbox en Plata / Acción / Esperando / Referencia con subagentes en paralelo y le pone un ámbito a cada mail. Reporte primero; etiquetar en Gmail es opcional y va detrás de `--send`. | Falta el OAuth de Google |
| `grabacion-a-tareas` | Cualquier audio o video (reunión, llamada, nota de voz) → tareas con responsable, plazo y la cita textual de dónde salió cada una. | Productivo |
| `consenso` | Manda N auditores independientes al mismo cálculo sin que se vean, y compara. Para números que salen a un tercero o decisiones caras de revertir. | Productivo |
| `prospectar-gmaps` | Listas de negocios reales desde Google Maps a CSV: candidatos a locatario, venues, frigoríficos. | Falta `APIFY_API_TOKEN` |

`triage-inbox` y `prospectar-gmaps` salieron de portar skills de `~/Downloads/Claude Code
Full Course/All Of My Claude Skills/` (27/07/2026). Ver la Lab Note: no se copian tal cual,
se portan.

**Los skills se escriben genéricos y lo específico va en config.** `triage-inbox` no sabe
nada de los negocios: los ámbitos viven en su `contextos.json` y se editan sin tocar código.
`grabacion-a-tareas` recibe el dominio por `--contexto`. Un skill clavado a un negocio
sirve para uno solo; el mismo skill parametrizado sirve para los cuatro y para el próximo.

## Subagentes

| Agente | Para qué | Modelo |
|---|---|---|
| `numeros` | Audita cualquier cálculo que toque plata, contra la fuente. Read-only. Su checklist es también el del skill `consenso`. | Opus |
| `auditor-consenso` | Igual que `numeros` pero escribe JSON, para correr de a varios y comparar. Lo usa el skill `consenso`. | Opus |
| `clasificador-mails` | Clasifica un chunk de mails. Lo usa `triage-inbox`. | Haiku |
| `code-reviewer` | Revisa código sin contexto del repo. | Sonnet |
| `qa` | Escribe tests, **los corre**, y reporta. | Sonnet |
| `research` | Investiga a fondo sin ensuciar el contexto principal. | Sonnet |

Se corren siempre con **path absoluto** y con el Python del venv — el `python3` del
sistema es 3.9 y no tiene las dependencias:

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/radar_rampa.py" \
  master.xlsx 2026-08
```

Un skill nuevo se crea **solo después de haber hecho la tarea 3 veces a mano**, y
solo si me lo pedís. Un skill que no se usa es deuda: hay que mantenerlo y ensucia
el contexto.

---

## Stack

Todo instalado en el home, **sin sudo** (27/07/2026). El shell de login es **bash**, así
que el PATH vive en `~/.profile` (y `~/.bashrc` lo sourcea para las shells no-login, como
la terminal de VSCode). `~/.zshrc` tiene una copia por si algún día se cambia a zsh.

| Qué | Dónde | Para qué |
|---|---|---|
| Node 24 LTS + npm | `~/.local/node/bin/` | CLIs |
| `claude` CLI | vía npm | correr Claude headless desde launchd |
| `gemini` CLI | vía npm | segunda opinión desde la terminal |
| `uv` + Python 3.12 | `~/.local/bin/` | gestor de Python y paquetes |
| venv del OS | `~/facu-os/.venv/` | PyMuPDF, openpyxl, pandas, gspread, google-genai |
| `gh` CLI | `~/.local/gh/bin/` | GitHub |
| `netlify` CLI | vía npm | Deploys de la app del Paseo. **Ya autenticado** (team Astronomy). |
| `vercel` CLI | vía npm | Deploys de `astronomy-members`. Falta `VERCEL_TOKEN`. |
| `supabase` CLI | vía npm | Base de `astronomy-members` y del Paseo. Falta `SUPABASE_ACCESS_TOKEN`. |
| Obsidian 1.12.7 | `/Applications/Obsidian.app` | Segundo cerebro. Abre `~/Obsidian/facu-vault/` por defecto. |

**Vercel y Supabase van por token, no por `login` interactivo.** El login de navegador se
vence y no sirve headless: cuando el `launchd` corra a las 9 de la mañana no hay nadie para
clickear. Los tokens viven en el `.env` (`VERCEL_TOKEN`, `SUPABASE_ACCESS_TOKEN`).

**Sitios de Netlify de la app del Paseo** — un deploy por rol, credencial aislada en cada build:
`lucent-buttercream` = Mati · `whimsical-alfajores` = Inversores · `dancing-elf` = Admin.
(`dapper-cajeta` es de Astronomy, no tocar.)

**Obsidian se abre desde `/Applications`, nunca desde el `.dmg`.** Si se abre desde el
dmg, macOS lo corre translocado (`/private/var/.../AppTranslocation/`) en una copia de
solo lectura: no actualiza y la config no persiste. Chequeo: `pgrep -fl Obsidian`.

El `python3` del sistema es 3.9 y no sirve: usar siempre `.venv/bin/python` (alias `py`).
Por lo mismo, el linter del IDE marca `Cannot find module` sobre `httpx`, `google.genai`
y `dotenv`: está mirando el 3.9 del sistema, no el venv. Es ruido, no un error.

Tests: `.venv/bin/python -m pytest execution/tests/ -q`. Van solo sobre `execution/`,
que es código compartido y de largo plazo; los skills se verifican corriéndolos.

## Utilidades compartidas (`execution/`)

- **`google_auth.py`** — OAuth único para Sheets, Drive y Gmail. `sheets()`, `drive()`,
  `gmail()`, y `bajar_xlsx(file_id, destino)` que exporta el sheet **completo** (el
  conector de Drive trunca). Setup: `.venv/bin/python execution/google_auth.py --setup`.
- **`gemini.py`** — `preguntar()` y `leer_imagen()`. Para volumen barato, leer fotos y
  capturas (guías del campo, comprobantes) y pedir segunda opinión. El modelo sale de
  `GEMINI_MODEL` en el `.env`; no hay default hardcodeado a propósito. Hoy:
  `gemini-flash-latest`, verificado con una llamada real. **`--modelos` lista modelos que
  la key no puede usar** (`gemini-2.5-flash` figura y tira 404): antes de fijar uno nuevo,
  probarlo con un `generate_content` de verdad.

**Cuándo usar Gemini y cuándo no:** Gemini para volumen, transcripción de imágenes y
contraste. **Nunca** para decidir un número que va a un reporte de plata — eso se calcula
en Python contra la fuente, no se le pregunta a un modelo.

---

## Reglas

**Plata real = cero improvisación.** Cualquier número de Paseo Nordelta, de una venta
de hacienda o de un reparto de ganancias: sin estimar, sin redondear en silencio. Si
falta un dato para que cierre, se pide. Un número inventado ahí cuesta caro.

**Lo que puede ser código, es código.** Si un skill me pide "calculá el promedio", está
mal escrito: eso va en Python. Yo decido *cuál* local y *qué* decir, no cuánto da la
cuenta.

**Nada sale al mundo sin OK.** Todo script que manda un mail, un WhatsApp o publica
algo lleva flag `--send`, apagado por defecto. Se prepara el mensaje entero y se frena.

**Verificar antes de decir "listo".** Correr el script, abrir el archivo, mostrar el
output. "Debería andar" no cuenta como terminado.

**Nunca parchear alrededor de un chequeo que falla.** Si una verificación salta, se
arregla la causa, no el chequeo. Una verificación que nunca falló desde que existe es
sospechosa.

**Los secretos van en `.env`.** Si falta una key, se pide — no se inventa ni se usa un
placeholder que después falle en silencio.

---

## Workflow para cambios no triviales

1. Escribo el código.
2. Corro `code-reviewer` y `qa` en paralelo (y `numeros` si el cambio toca plata).
3. Leo los reportes y aplico los fixes yo, en el hilo principal.
4. Recién ahí se usa.

El agente que escribió el código está sesgado a decir que está bien. Uno con contexto
cero encuentra cosas.

## El loop de aprendizaje

Se rompe → arreglo la causa raíz → lo pruebo → actualizo el `SKILL.md` → escribo la
Lab Note en `LAB_NOTES.md`. El sistema queda más fuerte que antes.

Doble escritura: el postmortem completo va a `LAB_NOTES.md`; la lección corta (dos
oraciones) va al `SKILL.md` del skill afectado, para que se cargue en contexto cuando
ese skill se use. Si la lección es un patrón transferible (no trivia del repo), se
destila como nota en el vault.

## Las tres capas

| Capa | Dónde | Qué va |
|---|---|---|
| Ejecución | este repo (`skills/`, `active/`) | Código y estado operativo. |
| Estado | memoria de Claude Code | En qué quedó cada cosa. Cambia todo el tiempo. |
| Conocimiento | `~/Obsidian/facu-vault/` | Lo que sigue siendo cierto dentro de un año. |

Si se mezclan, el `CLAUDE.md` se llena de data vieja y empieza a mentir.

## Modelos

IDs actuales: `claude-opus-5` · `claude-sonnet-5` · `claude-haiku-4-5-20251001`.
Clasificar/rutear → Haiku. Generar contenido y analizar → Sonnet. Arquitectura,
estrategia y cualquier cosa que toque plata → Opus.
