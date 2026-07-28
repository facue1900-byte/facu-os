# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una entrada acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, se destila como nota en el vault.

### 2026-07-27 · FAIL ✓ — El conector de Drive (read_file_content) devolvió la pestaña…

El conector de Drive (`read_file_content`) devolvió la pestaña Movimientos del Master Plan cortada en 206 de 455 filas, **sin error ni aviso**. Los totales daban más chicos y plausibles.

**La próxima:** Bajar siempre el export `.xlsx` completo. Un resultado uniformemente vacío o corto es un error hasta que se demuestre lo contrario: contar las filas antes de confiar en un total.

### 2026-07-27 · FAIL ✓ — radar_rampa.py calculaba piso = SOLO_EXPENSAS.get(local, 0) if desde…

`radar_rampa.py` calculaba `piso = SOLO_EXPENSAS.get(local, 0) if desde > hoy else 0` dentro de la rama donde `desde <= hoy`: la condición estaba muerta y el piso daba **0 fijo**. Un local que pagaba solo expensas (Peak One, $1,71M) podía cruzar el umbral de medio alquiler y figurar "al día" sin haber pagado un peso de alquiler.

**La próxima:** Fix: descontar las expensas siempre — el local las paga *además* del alquiler. Toda condición que compara con la variable que ya filtró el `continue` de arriba es sospechosa.

### 2026-07-27 · LEARN — Los cargos bancarios chicos del Macro (SIRCREB, Ley 25.413,…

Los cargos bancarios chicos del Macro (SIRCREB, Ley 25.413, comisiones) cargados uno por uno hacían ruido en Movimientos. Agrupados en una línea mensual cada uno, junio 2026 concilió al centavo.

**La próxima:** El criterio de agrupado está verificado contra un mes que cerró exacto. El neto se controla contra el extracto **crudo**, nunca contra el agrupado.

### 2026-07-27 · LEARN — El extracto del Macro no separa débito de crédito por columna de…

El extracto del Macro no separa débito de crédito por columna de forma confiable.

**La próxima:** Deducir el signo de cómo se movió el saldo línea a línea, arrancando de "SALDO ULTIMO EXTRACTO".

### 2026-07-27 · LEARN — El Dashboard Mensual matchea ingresos por Local y egresos por…

El Dashboard Mensual matchea ingresos por **Local** y egresos por **Categoría**, con SUMIFS sensible a acentos y espacios. Un local mal escrito no tira error: suma cero y el mes queda desfasado en silencio.

**La próxima:** Chequeo de categorías huérfanas en todo cierre. "Apex" → "Peak One" fue exactamente esto.

### 2026-07-27 · FAIL ✓ — Traté a Nordelta Plaza como si fuera una unidad de Paseo Nordelta y…

Traté a **Nordelta Plaza** como si fuera una unidad de **Paseo Nordelta** y le atribuí la sociedad NDPL SAS al Paseo. Son dos negocios distintos: otra sociedad, otros socios (Jero Gallo, Tino/Noreventos, Las Carolas), otro banco (BBVA vs Macro). Facu lo corrigió.

**La próxima:** Que compartan la palabra "Nordelta" y estén en carpetas vecinas del Desktop no los hace el mismo negocio. Antes de fusionar dos fuentes, verificar CUIT/sociedad/banco. Separados en `active/paseo-nordelta/` y `active/nordelta-plaza/`.

### 2026-07-27 · FAIL — Las dos "tareas automáticas" que el MEMORIA de Paseo daba por…

Las dos "tareas automáticas" que el MEMORIA de Paseo daba por creadas (conciliación día 10 9am, sync aportes diaria 7am) **no existen**: `RemoteTrigger list` devolvió cero routines. Estuvieron meses documentadas como activas sin correr nunca.

**La próxima:** Persist-or-it-didn't-happen: una automatización que no deja archivo ni corrida verificable no existe. Nunca anotar una tarea como "creada" sin listarla después.

### 2026-07-27 · LEARN — No hay node, npm, brew ni CLI claude en la Mac, y Python es el 3.9…

No hay `node`, `npm`, `brew` ni CLI `claude` en la Mac, y Python es el 3.9 del sistema sin `requests`. Toda la automatización local (launchd + claude headless) está bloqueada hoy.

**La próxima:** Las routines cloud son la única vía automática disponible, y **no ven el Desktop**. Lo que necesite archivos locales tiene que subir a Drive primero.

### 2026-07-27 · FAIL ✓ — claude no arrancaba desde la terminal ("no está instalado")

`claude` no arrancaba desde la terminal ("no está instalado"). Estaba instalado y funcionando (v2.1.220 en `~/.local/node/bin/claude`): el `export PATH` se había escrito **solo en `~/.zshrc`**, pero el shell de login de la Mac es `/bin/bash`, que nunca lo lee. Nada fallaba con error — el comando simplemente no existía.

**La próxima:** Fix: PATH y alias movidos a `~/.profile`, con `~/.bashrc` sourceándolo para shells no-login (terminal de VSCode). Antes de escribir en un rc, chequear el shell real con `dscl . -read ~ UserShell` — no asumir zsh porque es el default de macOS. Verificar con `env -i HOME=$HOME /bin/bash -lc 'which X'`, no en la shell que ya tenés abierta.

### 2026-07-27 · LEARN — Las cuatro copias de MEMORIA - Paseo Nordelta en el Desktop…

Las cuatro copias de `MEMORIA - Paseo Nordelta` en el Desktop divergieron entre sí; ninguna decía cuál era la buena.

**La próxima:** Una sola fuente por tema. El estado vive en la memoria de Claude Code y en `active/`, no en copias sueltas con `copy` en el nombre.

### 2026-07-27 · FAIL ✓ — gemini.py devolvía un genai.Client nuevo en cada llamada

`gemini.py` devolvía un `genai.Client` nuevo en cada llamada. Como `models.list()` es un pager perezoso, el cliente temporal se recolectaba antes de que saliera el request y httpx tiraba `RuntimeError: Cannot send a request, as the client has been closed` — un error que no menciona ni la key, ni la red, ni el modelo, y manda a debuggear para el lado equivocado.

**La próxima:** Fix: `_CLIENTE` singleton de módulo. Un cliente HTTP creado inline y usado con una API perezosa se muere antes del request. Además `.strip()` en la key: un espacio pegado al `=` del `.env` viaja hasta el header de auth.

### 2026-07-27 · FAIL ✓ — GEMINI_MODEL=gemini-2.5-flash daba 404 "no longer available to new…

`GEMINI_MODEL=gemini-2.5-flash` daba 404 `"no longer available to new users"` **aunque el modelo figura en `--modelos`**. La lista de la API incluye modelos que la key no puede invocar. También, en el free tier, `gemini-2.0-*` y `gemini-2.5-pro` dan 429 por cuota.

**La próxima:** `models.list()` no es prueba de que un modelo sirva: probarlo con un `generate_content` real antes de fijarlo. Sondeados 7 candidatos, andan `gemini-flash-latest` y `gemini-flash-lite-latest`. Quedó `gemini-flash-latest`.

### 2026-07-27 · FAIL ✓ — El chequeo "cero modelos es error" de listar_modelos() medía antes…

El chequeo "cero modelos es error" de `listar_modelos()` medía **antes** del filtro de `generateContent`: si la API devolvía modelos pero ninguno servía para generar, el script imprimía cero líneas y salía con código 0. Un chequeo escrito para cazar el silencio que dejaba pasar el silencio. Lo encontró `code-reviewer`, no yo — yo escribí el chequeo y lo di por bueno.

**La próxima:** Contar lo que se **imprime**, no lo que devuelve la fuente. La regla del resultado vacío se aplica al final del pipeline, no al principio. Y el workflow de correr `code-reviewer` sobre código propio se paga solo: el que lo escribió no ve este tipo de error.

### 2026-07-27 · LEARN — Tres fixes más de la misma revisión de gemini.py

Tres fixes más de la misma revisión de `gemini.py`: (1) `except Exception` convertía un typo del script en "la API contestó" — acotado a `genai_errors.APIError` y `httpx.HTTPError`, verificado que toda la jerarquía real de errores de API y red cae ahí; (2) `r.text` puede venir `None` sin error (filtro de safety, respuesta cortada) y `leer_imagen()` lo devolvía tal cual, así que un skill podía guardar `None` como el dato extraído de una guía de SENASA — ahora `_texto()` revienta con el `finish_reason`; (3) `modelo()` no tenía el `.strip()` que sí tenía la key.

**La próxima:** Cuando se arregla un patrón (un `.strip()`, un chequeo de vacío), buscar el mismo patrón en todo el archivo. Arreglarlo en un solo lugar deja el bug vivo al lado.

### 2026-07-27 · LEARN — Los tests de gemini.py vivían en el scratchpad de la sesión, que se…

Los tests de `gemini.py` vivían en el scratchpad de la sesión, que se borra. Reportar "13 tests en verde" con los tests a punto de evaporarse es la misma trampa que las routines fantasma.

**La próxima:** Movidos a `execution/tests/`, con el path del repo calculado desde `__file__` en vez de hardcodeado. Un test que no está en el repo no existe.

### 2026-07-27 · FAIL ✓ — Al autorizar la SEGUNDA cuenta de Google, el flujo guardó…

Al autorizar la SEGUNDA cuenta de Google, el flujo guardó `token-facu.json` con las credenciales de **studio@astronomyofficial.com**. `run_local_server()` no pide `prompt`, así que Google reusó la sesión abierta y ni mostró el selector. No hubo ningún error: el token se guardó "bien", con el nombre de otra cuenta. Un `triage-inbox` pidiendo la cuenta `facu` habría ordenado el inbox equivocado y reportado éxito.

**La próxima:** Fix en dos partes: (1) `prompt="select_account"` fuerza el selector; (2) antes de guardar, `_cuenta_con_email()` chequea si ese mail ya está bajo otro nombre y **corta sin guardar**. Todo login que reusa sesión puede autenticar a quien no querés: el token no se da por bueno hasta preguntarle a la API **con qué identidad** quedó.

### 2026-07-27 · FAIL ✓ — Mi propio script de comparación reportó que studio NO llegaba al…

Mi propio script de comparación reportó que `studio` NO llegaba al Master Plan, contradiciendo una verificación mía de veinte minutos antes. La causa era el script, no los permisos: clasificaba las excepciones a mano (`"403" if "403" in str(e) else ... else "no"`) y el cajón "no" se tragaba el motivo real. Reportar esa tabla habría hecho configurar los skills con la cuenta equivocada.

**La próxima:** Cuando un resultado nuevo contradice uno ya verificado, el sospechoso es el medidor. Imprimir la excepción CRUDA antes de clasificarla; un `else` que resume errores desconocidos en una etiqueta corta es un lugar donde se pierde información.

### 2026-07-27 · FAIL ✓ — Obsidian "no estaba instalado" (/Applications/Obsidian.app no…

Obsidian "no estaba instalado" (`/Applications/Obsidian.app` no existía) pero estaba **corriendo**: se había abierto directo desde el `.dmg` de Downloads, y macOS lo ejecutaba translocado desde `/private/var/.../AppTranslocation/` — copia de solo lectura, sin updates y con config que no persiste. Nunca había registrado el vault (`obsidian.json` no existía).

**La próxima:** Instalado de verdad en `/Applications` y vault registrado con ID determinístico (`sha256(path)[:16]`) para que re-correr no duplique la entrada. Una app que corre desde `AppTranslocation` está a medio instalar: `pgrep -fl <app>` lo delata. Mismo patrón que el PATH: el síntoma decía "no existe", la causa era "existe pero mal ubicado".

### 2026-07-27 · LEARN — Revisión de las 27 skills de ~/Downloads/Claude Code Full Course/All…

Revisión de las 27 skills de `~/Downloads/Claude Code Full Course/All Of My Claude Skills/`. Son de una agencia de cold email: 18 dependen de servicios que Facu no tiene (Apify, PandaDoc, Instantly, Anymailfinder, Auphonic, TubeLab, Pinecone) o de negocios ajenos (Skool, Upwork, thumbnails de YouTube). Copiarlas todas habría metido 27 descripciones al auto-descubrimiento de skills para disparar dos.

**La próxima:** Se portaron dos: `triage-inbox` (de `gmail-label` + `gmail-inbox`) y `prospectar-gmaps` (de `gmaps-leads`, solo el scraper). Portar, no copiar: auth propia (`execution/google_auth.py` en vez del registry multi-cuenta), categorías por negocio de Facu, y `--send` apagado donde el original escribía directo. Un skill importado tal cual es deuda con nombre lindo.

### 2026-07-27 · FAIL ✓ — El gmail_label_merge.py original juntaba lo que clasificaba cada…

El `gmail_label_merge.py` original juntaba lo que clasificaba cada subagente **sin chequear cobertura**: si un subagente moría, sus mails quedaban sin etiquetar y el resumen igual decía "listo". El mismo modo de falla que el Drive truncado.

**La próxima:** `merge_labels.py` compara los IDs clasificados contra el `emails.json` original y **corta** si falta uno. Probado a propósito con un chunk faltante antes de darlo por bueno. Todo fan-out a subagentes necesita un chequeo de cobertura del lado del que junta.

### 2026-07-27 · LEARN — El pipeline de gmaps-leads (571 líneas) le pedía a Claude Haiku que…

El pipeline de `gmaps-leads` (571 líneas) le pedía a Claude Haiku que sacara "el email del dueño" scrapeando webs. Eso inventa datos con cara de dato verificado.

**La próxima:** En `prospectar-gmaps` sale solo lo que Google Maps publica (nombre, dirección, teléfono, web, rating) y nada más. Si un dato hay que adivinarlo, no es un dato.

### 2026-07-27 · FAIL ✓ — El subagente research tenía en su cuerpo la instrucción "escribí el…

El subagente `research` tenía en su cuerpo la instrucción "escribí el resultado en la ruta que te den", pero su frontmatter declaraba `tools: Read, Glob, Grep, WebSearch, WebFetch` — **sin `Write`**. Venía así del template del curso. Nunca había fallado ruidosamente: el agente investiga igual y devuelve texto, así que el hueco solo se nota cuando alguien espera el archivo y no está.

**La próxima:** Fix: `Write` agregado. Auditar los agentes es leer el frontmatter contra el cuerpo: si el cuerpo pide una herramienta que el frontmatter no da, el agente hace algo distinto de lo que dice hacer, y en silencio.

### 2026-07-27 · LEARN — Auditoría de los 6 subagentes del OS

Auditoría de los 6 subagentes del OS. `code-reviewer`, `qa` y `research` seguían en inglés y con el formato de salida del curso (PASS / NEEDS CHANGES): son justo los tres que el workflow de cambios no triviales manda correr, así que sus reportes volvían en otro idioma que el resto del OS. `clasificador-mails` corría en Sonnet para una tarea de clasificación pura, contra la regla del `CLAUDE.md` de mandar eso a Haiku.

**La próxima:** Los tres reescritos en español, con secciones obligatorias de "lo que no pude verificar/probar". `clasificador-mails` bajado a Haiku (con nota de cómo volver a Sonnet si confunde ámbitos). Un agente heredado de un template arrastra el idioma, el formato y el modelo de otro proyecto.

### 2026-07-27 · LEARN — Los skills nuevos arrancaron clavados a los cuatro negocios

Los skills nuevos arrancaron clavados a los cuatro negocios: las reglas de ámbito vivían dentro del agente `clasificador-mails`. Facu pidió que fueran generales.

**La próxima:** Los ámbitos se movieron a `.claude/skills/triage-inbox/contextos.json`, con `senales` y `no_confundir` por ámbito, y el merge **valida** contra ese archivo: un ámbito no declarado corta la corrida. Regla que queda: lo genérico va en el skill, lo específico en un JSON al lado. Un skill clavado a un negocio sirve para uno; parametrizado sirve para los cuatro.

### 2026-07-27 · LEARN — grabacion-a-tareas se probó end-to-end de verdad

`grabacion-a-tareas` se probó end-to-end de verdad: audio generado con `say` de macOS → Files API de Gemini → extracción. Sacó las 2 tareas con responsable y plazo, la decisión, el tema abierto y el monto, cada uno con su cita textual.

**La próxima:** Un extractor validado solo con JSON de mentira no está validado. `say -o x.aiff "..."` alcanza para fabricar un caso de prueba real sin depender de que aparezca una grabación. Los montos dichos en una grabación van a una tabla aparte marcada como **no verificados**: lo que alguien dice en una reunión no es un dato contable.

### 2026-07-27 · FAIL ✓ — La línea de estado nunca mostró el contexto usado

La línea de estado **nunca mostró el contexto usado**. Buscaba `context.used_tokens` / `context.percent_used`; el campo real que manda Claude Code (v2.1.220) es `context_window.used_percentage`. Como ninguna ruta matcheaba, caía en un `else` silencioso y la barra mostraba solo `proyecto \| modelo`. Un chequeo que no falló nunca desde que existe porque nunca corrió.

**La próxima:** Fix contra el payload real, que la propia statusline guarda en `/tmp/claude-statusline-payload.json`. Regla: un script que "prueba varias rutas antes de rendirse" necesita **fallar ruidosamente cuando ninguna pega**, o el fallback tapa el bug para siempre. Antes de escribir rutas defensivas, mirar un payload de verdad.

### 2026-07-27 · FAIL ✓ — El hook aviso-contexto.sh no imprimía nada

El hook `aviso-contexto.sh` no imprimía nada: usaba `python3 - <<'PY'` y leía el payload con `json.load(sys.stdin)` — pero el heredoc **ya ocupa stdin**, así que Python parseaba su propio código fuente como JSON. Con `2>/dev/null` encima, el error era invisible; y los casos de prueba "no debe imprimir nada" pasaban en verde por la razón equivocada.

**La próxima:** Fix: `payload=$(cat)` y pasarlo por `argv`, igual que `statusline.sh`. Un test cuyo criterio de éxito es "salida vacía" no distingue funciona-y-calla de está-roto: cada suite necesita al menos un caso que **exija** output.

### 2026-07-27 · FAIL ✓ — cierre-mes invocaba el python3 del sistema

Los pasos 1 y 2 de `cierre-mes-nordelta/SKILL.md` invocaban `python3` pelado (3.9, sin PyMuPDF ni openpyxl) → `ModuleNotFoundError` garantizado en el cierre. Era el único skill con el bug; el paso 2-bis del mismo archivo ya lo hacía bien. Además `triage-inbox` referenciaba un `token.json` que ya no existe (multi-cuenta lo partió en `token-facu.json`/`token-studio.json`) y `consenso` hacía `cd` a un directorio que nunca se creaba.

**La próxima:** cuando cambia una convención (venv, nombres de token, directorios), grepear TODOS los SKILL.md y scripts por la convención vieja en el mismo commit. Una referencia rota en un skill es un skill que falla recién cuando se lo necesita.

### 2026-07-27 · FAIL ✓ — conciliar.py v1: chequeo más permisivo que el sistema que replica

La primera versión de `conciliar.py` normalizaba categorías sacando tildes y colapsando espacios. El SUMIFS real del Dashboard es sensible a acentos y espacios: una categoría con tilde distinta queda FUERA del Dashboard en la vida real, y el chequeo la daba por buena → falso CIERRA sobre plata. Lo agarró el code-reviewer antes del primer uso real.

**La próxima:** un chequeo que replica el comportamiento de otro sistema (un SUMIFS, un matcher, un parser ajeno) tiene que ser EXACTAMENTE igual de estricto. Cada normalización "por las dudas" que el sistema real no hace es una clase de error que el chequeo deja de ver.

### 2026-07-27 · LEARN — Saldo Actual es histórico: descomponer antes de culpar al mes

`conciliar.py` encontró $0,69 de diferencia entre el extracto de junio y Saldo Actual. El agente `numeros` recalculó los 6 meses contra sus PDFs: junio cierra al centavo — la diferencia es de MARZO (fila 95 de Movimientos, "Tubomarket galeria" cargada $391.325,00 cuando el banco movió $391.324,31). Saldo Actual es un SUMIFS sobre todo el historial, así que arrastra errores viejos al presente. El script ahora descompone: cuánto viene arrastrado y cuánto es del mes.

**La próxima:** cuando un acumulado histórico no cierra, bisectar por período contra las fuentes antes de tocar nada del mes corriente. Y auditar con un agente independiente un script nuevo de plata ANTES del primer uso real: acá el auditor encontró además gastos VISA sin registrar ($4.887) y aportes de capital mezclados como ingresos en el Dashboard ($10,4M en junio).

### 2026-07-27 · FAIL ✓ — La memoria quedaba en el proyecto equivocado

La memoria de Claude Code se guarda según la carpeta desde donde se abre la sesión: 224 KB de memoria de los negocios (35 archivos, incluidas las reglas de membresías que el CLAUDE.md listaba como "hueco por completar") estaban repartidos entre el proyecto del Curso y el de Astronomy, y la memoria de facu-os estaba VACÍA. Unificada el 27/07/2026: 27 memorias + MEMORY.md en facu-os, crudos grandes en `archive/memoria-importada/`, orígenes vaciados tras verificar byte a byte.

**La próxima:** las sesiones de los negocios se abren SIEMPRE desde `~/facu-os` — es lo que decide dónde vive la memoria. Si una sesión se abrió desde otra carpeta y guardó memoria valiosa, migrarla en el momento.

### 2026-07-27 · LEARN — La política de modelos no rutea nada si no hay a quién delegar

El global declaraba "Haiku clasifica · Sonnet genera · Opus para plata" desde siempre, pero el hilo principal corre en Opus y **un skill no puede bajarse el modelo: no existe esa palanca en el frontmatter de `SKILL.md`**. El único ruteo real es delegar a un subagente con `model:` clavado. Resultado: los 6 subagentes estaban bien ruteados, pero todo el trabajo mecánico (leer archivos, extraer campos, escribir borradores) se lo comía Opus 1M porque no había ningún agente genérico a quien mandárselo — `clasificador-mails` estaba clavado a mails.

**El fix:** agentes `mecanico` (Haiku, trabajo de dedos) y `redactor` (Sonnet, texto para terceros), más la tabla de ruteo en `.claude/CLAUDE.md`. Regla que los sostiene: **lo que decide no se delega** — el `mecanico` trae datos, el hilo principal saca la conclusión.

**La próxima:** Una política sin mecanismo es un comentario. Antes de escribir una regla en un CLAUDE.md, preguntarse qué la ejecuta.

### 2026-07-27 · LEARN — Los subagentes nuevos no existen hasta reiniciar la sesión

Recién creado `.claude/agents/mecanico.md`, invocarlo devolvió `Agent type 'mecanico' not found`. El registro de agentes se arma **al arrancar la sesión**; escribir el archivo no lo registra en caliente.

**La próxima:** Un agente nuevo se prueba en la sesión siguiente, no en la que lo creó. El frontmatter sí se puede validar en el momento (`name` == nombre del archivo, `model` en haiku/sonnet/opus).

### 2026-07-28 · LEARN — Skill `flyers`: `--user-data-dir` cuelga al Chrome headless de macOS

Armando el generador de flyers de Academy, los 75 renders se colgaban a los 120s sin
escribir el PNG ni tirar error. Aislando flag por flag, el culpable era
`--user-data-dir` apuntando a un perfil nuevo en `/tmp`: se queda esperando para
siempre, ni siquiera con `--no-first-run --no-default-browser-check --disable-sync`.
Sin el flag anda, y cinco corridas en paralelo producen PNGs **byte a byte idénticos**
— o sea que compartir el perfil por defecto no genera contención.

De paso: **`timeout` no existe en macOS**, así que el primer intento de acotar el
render "colgado" no corrió Chrome en absoluto y dio un falso negativo. El corte tiene
que ir en el `subprocess.run(timeout=...)` de Python.

**La próxima:** cuando un subproceso se cuelga, bisectar los flags antes de tocar el
código. Y desconfiar de un test que "falla rápido": verificar que la herramienta que
usás para acotarlo exista (`command -v timeout`) — un 127 se lee igual que un fallo
real si no mirás el stderr.

### 2026-07-28 · LEARN — Un flyer con precio a mano es un precio que se desactualiza

Los precios de los flyers de Academy no se escriben en el JSON de contenido: los pisa
`sync_precios.py` leyendo la tabla `plans` de Supabase, la misma que lee el checkout.
Un flyer publicado con precio viejo lo compara el alumno contra Mercado Pago y no
coincide. Además el generador **revienta** si un ángulo de tipo `precio` se encuentra
con `precio_ars: null`, en vez de dibujar el precio en blanco.

Excepción registrada: `modo-profesional` tiene el precio hardcodeado en
`app/actions/buyCursoPro.ts` (`PRECIO_UNICO` $440.000 / `PRECIO_CUOTA` $250.000), no
en la base. Si cambia allá, hay que actualizarlo a mano en `contenido/academy.json`.

**La próxima:** todo número que sale a un tercero se sincroniza desde su fuente o el
script no corre. "Lo actualizo cuando cambie" es cómo se publica un precio viejo.

### 2026-07-28 · LEARN — La convención de pago de cada local cambia la deuda

El radar de deudores mostraba a Bigg debiendo $2,2M. Facu aclaró que Bigg **paga por adelantado** (el cargo del mes se paga en el mismo mes) y que dic'25 se pagó fuera del registro 2026 → deuda real: cero. Lo mismo con el Salón: un pago de $5M que parecía adelanto de expensas era la **penalidad de una inquilina saliente**. Los números estaban bien calculados; la interpretación estaba mal porque cada local tiene su convención (vencido/adelantado, efectivo/banco, redondeos).

**La próxima:** antes de reportar deuda de un local, confirmar su convención de pago con Facu. Las convenciones viven en `radar_deudores.py` (`REGLAS`, `PAGAN_ADELANTADO`, `PAGAN_POR_BANCO`) — un local nuevo se agrega ahí el día uno.

### 2026-07-28 · FAIL ✓ — CUENTA CORRIENTE solo suma conceptos que matchean sus SUMIFS

Cargué un cargo "Penalidad rescisión" en CARGOS y la CUENTA CORRIENTE lo ignoró en silencio: sus columnas suman por concepto con SUMIFS (`"Alquiler*"`, `"Servicios comunes"`, `"Recupero*"`) y un concepto nuevo no matchea ninguno. El saldo quedó $5M mal hasta que el radar lo delató. Fix: renombrar a "Alquiler - Penalidad rescisión" para entrar por el comodín.

**La próxima:** antes de inventar un concepto nuevo en una tabla que otra hoja consume por SUMIFS, leer las fórmulas del consumidor y usar un nombre que matchee. Y después de cada escritura al sheet, re-bajar y re-correr el reporte que lo lee: esa verificación fue la que agarró el error.

### 2026-07-28 · FAIL ✓ — Diseñé dos tandas contra la estética equivocada

Para los flyers de Academy inferí la estética de dos fuentes indirectas: los tokens
de la app (`--violet:#8b5cf6`, Montserrat, centrado) y el material viejo del Desktop
(PDFs de curso de 2023, portadas de The Bunker). Salieron 150 piezas. Ninguna se
parecía a la cuenta.

La grilla real de **@astronomy.academy** es un sistema editorial monocromo: negro
puro o foto muy desaturada, Helvetica Neue en MAYÚSCULAS **alineada a la izquierda
y anclada abajo**, micro-rótulos mono en las cuatro esquinas, cruces de registro,
logo de dos círculos, y el CTA como etiqueta entre corchetes. **Cero violeta, cero
botones, cero centrado.** El énfasis dentro de un titular se hace con peso, no con
color.

El `WebFetch` a instagram.com no sirvió: pega contra el muro de login y el modelo
chico que resume la página devolvió una descripción inventada ("rojos, naranjas y
azules") que contradecía todos los assets reales. Se descartó a tiempo por eso mismo
— por contradecir la fuente— pero el costo ya estaba pagado en las dos tandas.

**La próxima:** la estética de una cuenta se ve o no se diseña. Antes de generar la
primera pieza, pedir capturas de la grilla. Inferir una identidad visual desde el
sistema de diseño de otro producto de la misma empresa es exactamente el error:
Academy y la app comparten dueño, no lenguaje. Y una descripción de imagen que
contradice los archivos que sí podés abrir es un dato falso, no una segunda opinión.

### 2026-07-28 · LEARN — En Argentina, un precio impreso es deuda técnica

Facu bajó los precios de las 75 piezas de Academy: con la inflación, un flyer
publicado con un número queda viejo en semanas y obliga a rehacer la tanda entera.
Las piezas ahora muestran solo lo que **no se desactualiza** —créditos por mes,
cantidad de clases, cantidad de módulos— y el valor del mes se pide por DM.

El guard quedó en el código, no en el contenido: `bloque_editorial()` revienta si le
llega un bloque de tipo `precio`. Puesto solo en el JSON, alcanzaba con editar el
contenido para que volviera a salir un número.

Efecto secundario que importa: la tanda pasó de tener una fecha de vencimiento a no
tener ninguna. Antes había que regenerar con cada lista de precios; ahora solo si
cambia el catálogo.

**La próxima:** en cualquier pieza que se publica y queda dando vueltas —flyer, PDF,
landing— preguntarse qué dato tiene fecha de vencimiento y sacarlo. Un número que
obliga a rehacer el material es peor que un número ausente.

### 2026-07-28 · FAIL ✓ — Una tanda que se cae a la mitad deja mezcla, no vacío

Regenerando los 75 flyers sobre la carpeta ya poblada, un Chrome se colgó a los 120s
y el script murió. En disco quedaron 75 PNGs —el conteo daba bien— pero eran una
mezcla de la corrida nueva y la vieja. El chequeo de cantidad no lo veía: los
archivos viejos existen, pesan bien y miden bien.

**El fix:** `render()` reintenta 3 veces antes de darse por vencido (el cuelgue es de
Chrome bajo carga, no del contenido: la misma pieza sale bien al segundo intento), y
una regeneración total borra la carpeta primero.

**La próxima:** un contador de archivos no verifica una regeneración; verifica que
haya archivos. Si el proceso escribe sobre lo que ya estaba, o se borra el destino
antes, o se compara algo que distinga la corrida (fecha, hash, versión).

### 2026-07-28 · FAIL ✓ — El agente `numeros` frenó dos errores en la estrategia de pauta

Primer borrador de `active/astronomy/PAUTA_ACADEMY.md`: los 8 cálculos centrales
reprodujeron exactos (retención de cohorte al segundo decimal, CAC, márgenes). Pero
el auditor encontró dos cosas que sí importaban:

1. **El margen −7% descansaba casi entero en un solo mes con problema de carga.**
   Dic-2025 tiene CERO filas de Membership (el resto de los meses tienen entre 5 y 20)
   y ene-2026 tiene 20, el máximo de la serie: las membresías de diciembre se cargaron
   en enero. Dic-2025 cierra en −US$3.145 y **los otros once meses suman +US$1.103**.
   El total anual no cambia, pero "el negocio pierde plata" era una lectura falsa:
   está en el cero. Iba a un documento que decide presupuesto.
2. **Un escenario alternativo mal derivado.** "Si Sueldos es fijo, la contribución
   sube a ~75% y el CAC a US$68" — la cuenta real da 81% y US$74. Aparecía dos veces.

Y varias menores reales: un subtotal de US$549 que era US$753 (la planilla tiene la
misma subcategoría con dos grafías — `Clase de Prueba` / `Clase de prueba` — y el
conteo tomó una sola), "1,2x más" leído como 120% cuando es 21%, seis filas con tipo
de cambio implícito imposible (una de 9.546 ARS/USD) que mueven el resultado US$269,
y `Sueldos Fijos` —la línea de egreso más grande, US$6.904— sin mencionar en ningún
lado del análisis de costos.

**La próxima:** dos cosas. Una, antes de promediar una serie mensual, mirar si algún
mes tiene cero de una categoría que todos los demás tienen: es carga corrida, no
negocio, y contamina cualquier conclusión de tendencia. Dos, agrupar por una columna
de texto libre sin normalizar mayúsculas parte la categoría en dos y el subtotal
queda corto en silencio.

**Lo que salió bien:** el auditor corrió ANTES de que el documento se usara, y su
propio reporte se autolimitó donde correspondía — reconstruyó la retención real
matcheando Client Id faltantes por nombre, dio el número (2,94 en vez de 2,81), y
aclaró que no lo tomaba como bueno porque matchear por nombre es exactamente lo que
la regla de atribución prohíbe. Lo reportó como cota del sesgo, no como dato.

---

## 2026-07-28 — Bigg: una etiqueta de mes movió $1,9M de lugar

**Qué pasó.** Revisando cuentas corrientes, junio de Bigg aparecía con el alquiler
cargado **tres veces** ($5.731.160,59 cuando el contrato 50/50 da $3.820.773,73) y
mayo con una sola mitad. Ni uno ni otro eran errores de plata: los pagos estaban
perfectos. Era una etiqueta de mes mal puesta en la pestaña del local.

**La causa.** En las pestañas de Ctas Ctes, el alquiler de un mes se carga en dos
filas: `Alquiler` (mitad facturada, con IVA) y `Diferencia Alquiler (sin iva)` (la
mitad en efectivo). En los bloques viejos la Diferencia llevaba **el mes anterior**
al que corresponde. Mientras las dos mitades valieron lo mismo ($1.750.000) el
desfase fue invisible; cuando el ajuste por IPC las movió a $1.910.386,86, un mes
quedó con tres mitades y otro con una.

**La regla que faltaba escrita:** en una pestaña de local, **cada fila pertenece al
mes del bloque donde se paga, no al mes que dice la etiqueta**. El bloque es
"expensas del mes anterior + alquiler del mes corriente", y cierra contra el pago
de ese mes. Verificarlo así es lo que permitió fechar el ajuste de IPC sin
adivinar: el pago de mayo usa la tarifa vieja y el de junio la nueva, los dos al
centavo.

**La próxima:** cuando un local paga en dos canales (banco / efectivo), reconstruir
el pago esperado por canal y compararlo contra lo pagado. Banco = mitad facturada +
IVA + expensas del mes anterior; efectivo = mitad sin IVA. Si los dos cierran al
peso, los movimientos están bien y el problema está en los cargos. Eso convierte
"algo no cuadra" en "esta celda está mal" en cinco minutos.

**Dos errores míos, para no repetirlos:**

1. **Calculé el saldo contra CARGOS en vez de contra la pestaña del local.** La
   pestaña es la contabilidad viva: su saldo corre secuencialmente y no le importa
   la etiqueta de mes, así que estaba bien mientras CARGOS estaba mal. Le pasé a
   Facu $1.171.137,46 cuando el número correcto —el suyo— era **$961.345**. Antes
   de dar un saldo, mirar la pestaña del local, no la tabla derivada.
2. **Prometí que dos celdas iban a arreglar el radar y no lo arreglaron.** Corregí
   junio, dije "con esto el radar deja de mentir", y el radar siguió marcando a Bigg
   al día. Faltaban el desfase de las otras tres etiquetas, el crédito por error de
   expensas y un pago en tránsito. **No anunciar el efecto de un fix antes de
   correrlo:** aplicar, correr, y recién ahí decir qué cambió.

**Lo que quedó construido.** `exportar_ctas_ctes.py` (radar → JSON) y la pestaña
**Deuda** en la app del Paseo, con un bloque `PENDIENTES_DE_CARGA` que muestra la
plata ya cobrada que todavía no entró al sheet **sin sumarla al saldo** — el saldo
sigue saliendo de la fuente, y el aviso evita reclamar algo ya pagado.
