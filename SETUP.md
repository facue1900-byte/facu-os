# Qué falta para que esté todo conectado

Estado al 27/07/2026. Lo que está tildado ya funciona; lo que no, está bloqueado
esperando algo que **solo podés hacer vos** (un login, una key, un permiso).

## Ya funciona

- [x] **El OS** — `~/facu-os`, con backup en GitHub (privado), estructura completa.
- [x] **Stack local** — Node 24, `claude` CLI, `gemini` CLI, Python 3.12 + venv con
      todas las dependencias, `gh` CLI. Todo en el home, sin sudo.
- [x] **El `claude` de la terminal** — el PATH vive en `~/.profile` (el shell de login es
      bash, no zsh). Verificar con `env -i HOME=$HOME /bin/bash -lc 'which claude'`.
- [x] **Gemini** — key de AI Studio puesta y `GEMINI_MODEL=gemini-flash-latest`, elegido
      probando 7 candidatos con llamadas reales. Ojo: `--modelos` lista modelos que la key
      **no puede usar** (`gemini-2.5-flash` figura y tira 404). Antes de cambiar el modelo,
      probarlo con un `generate_content` de verdad.
- [x] **Skill `cierre-mes-nordelta`** — probado contra el extracto real de junio 2026.
- [x] **Subagentes** — `code-reviewer`, `qa`, `research`, `numeros`, `auditor-consenso`,
      `clasificador-mails`.
- [x] **Vault y Obsidian** — app 1.12.7 en `/Applications` (no abrirlo desde el `.dmg`: se
      ejecuta translocado y la config no persiste), con `~/Obsidian/facu-vault` registrado
      como vault por defecto y sus convenciones de links aplicadas.
- [x] **Helpers** — `execution/google_auth.py` y `execution/gemini.py`, probados: fallan
      con instrucciones claras cuando falta una credencial, en vez de romperse feo.
      24 tests en `execution/tests/` (`.venv/bin/python -m pytest execution/tests/ -q`):
      13 de gemini + 11 de google_auth, incluida la regresión del bug de identidad.

- [x] **Credenciales de Google** — `credentials.json` puesto y **dos cuentas autorizadas**:
      `facu` (facue1900@gmail.com) y `studio` (studio@astronomyofficial.com). Verificado
      contra las 5 planillas reales, con permiso de escritura (27/07/2026, tabla abajo).

      | Planilla | `facu` (facue1900@) | `studio` (studio@astronomyofficial) |
      |---|---|---|
      | Master Plan Paseo Nordelta | escribe | solo lee |
      | Ctas Ctes Paseo 2026 | escribe | sin acceso |
      | Gastos Obra Paseo | escribe | sin acceso |
      | Finanzas Astronomy Academy | escribe | escribe |
      | Base de Clientes Astronomy | escribe | escribe |

      **`facu` llega a todo y escribe en todo: es el default correcto.** `studio` sirve
      para su propio inbox (6.768 mails) y como respaldo en los sheets de la academia.
      (Desactualizada la nota vieja de que "facue1900 es solo Lector en Finanzas":
      hoy tiene edición.)
- [x] **GitHub** — `facue1900-byte/facu-os`, privado, pusheado.
- [x] **Vercel, Supabase y Netlify** — CLIs instalados y tokens verificados contra las
      cuentas reales.

## Inventario de infraestructura

Verificado con los tokens el 27/07/2026. **Esto vive acá y no en `CLAUDE.md`: envejece,
y un dato viejo en un archivo que se carga en toda sesión miente en todas.**

| Plataforma | Qué hay |
|---|---|
| Vercel | Team `astronomyofficial` · proyecto `astronomy` → **astronomyofficial.com** en producción. **Push a `main` deploya solo.** |
| Supabase | **Dos** proyectos, uno por negocio: `qeakrjnseboiulcojlcw` (Astronomy) y `wujutradczplokjrgmdo` (**Paseo Nordelta**) |
| GitHub | `facue1900-byte/facu-os` (privado), `facue1900-byte/astronomy-members`, `facue1900-byte/app-paseo-nordelta-` |
| Google Cloud | Proyecto `astronomy-app-502618`, service account `astronomy-calendar@…` (Sheets + Calendar, impersona `studio@astronomyofficial.com`) |

> Son **dos bases de Supabase distintas**. Antes de una migración o un query, confirmar
> contra cuál se está pegando: un `ref` equivocado escribe en el negocio equivocado y no
> avisa.

**Vercel y Supabase van por token, no por login interactivo** (el login de navegador no
sirve headless para launchd). Los tokens ya están en el `.env` (`VERCEL_TOKEN`,
`SUPABASE_ACCESS_TOKEN`). Netlify ya autenticado (team Astronomy).

Sitios de Netlify de la app del Paseo — **un deploy por rol** (URLs completas, con
sufijo): `lucent-buttercream-8ac45a` = Mati · `whimsical-alfajores-91122a` = Inversores ·
`dancing-elf-c4ed3f` = Admin. (`dapper-cajeta-537756` es de Astronomy, **no tocar**.)

## Estado de cada skill

| Skill | Estado |
|---|---|
| `cierre-mes-nordelta` | Productivo — `scripts/conciliar.py` hace los chequeos deterministas |
| `triage-inbox` | Productivo. **Etiquetar en Gmail bloqueado**: faltan los scopes `gmail.modify` / `gmail.labels` |
| `grabacion-a-tareas` | Productivo |
| `consenso` | Productivo |
| `propuestas` | Productivo — genera y frena, no manda |
| `flyers` | Productivo — precios desde Supabase, render con Chrome headless |
| `prospectar-gmaps` | **Bloqueado**: falta `APIFY_API_TOKEN` |

## Bloqueado esperándote (en orden de lo que más desbloquea)

### ~~1. Credenciales de Google~~ ✅ HECHO (27/07/2026)

Era el cuello de botella real: sin esto no corría ni un proceso solo. Queda el
procedimiento documentado por si hay que rehacerlo o sumar una tercera cuenta.

1. Entrá a [console.cloud.google.com](https://console.cloud.google.com) → creá un
   proyecto (o usá uno que tengas).
2. **APIs y servicios → Biblioteca** → habilitá **Google Sheets API**, **Google Drive
   API** y **Gmail API**.
3. **Pantalla de consentimiento** → publicala en **Producción**.
   ⚠️ Si la dejás en "Testing", el token se vence **cada 7 días** y todo se corta sin avisar.
4. **Credenciales → Crear → ID de cliente OAuth → App de escritorio** → descargá el JSON.
5. Guardalo como `~/facu-os/credentials.json` y corré una sola vez:

```bash
cd ~/facu-os && .venv/bin/python execution/google_auth.py --setup --cuenta facu
```

El cliente OAuth vive en el proyecto `astronomy-app-502618` de Google Cloud (App de
escritorio). **Un solo `credentials.json` sirve para todas las cuentas.**

### 1. Token de Apify — 2 min · solo desbloquea `prospectar-gmaps`

1. [console.apify.com/settings/integrations](https://console.apify.com/settings/integrations)
   → copiá el API token.
2. Pegalo en `~/facu-os/.env` en `APIFY_API_TOKEN=`.

**Qué se enciende:** listas de candidatos a locatario para los locales vacíos del Paseo,
venues y productoras para eventos, frigoríficos y transportistas por zona.

### 2. Radar de rampa (`alerta-rampa`) — CARGADO el 07/10/2026

Probado a mano el 07/10 (dry-run, corte 2026-10): detecta La Jaula atrasada desde 2026-08.
Corre el día 5 de cada mes, 9:00, y manda el mail sólo a `MAIL_FACU`.
🔴 **Número a revisar:** dice "entró $185.000" y "acumulado no cobrado $6.000.000" (3 ×
$2M), sin restar lo que entró. Hasta revisarlo, el acumulado del mail no es un número
para pasarle a nadie.

### Tareas programadas: todas pasan por `execution/launchd/correr.sh`

Desde el 07/10/2026 cada plist corre su comando a través de `correr.sh <nombre> -- "<cmd>"`:
espera la red hasta 15 min, anota cada corrida en `data/logs/tareas.jsonl`, y si falla
avisa (notificación + mail a Facu vía `execution/avisar.py`, siempre). El radar de las 7:30 lee ese registro y marca las que **fallaron, no
corrieron o no están cargadas** (`chequeo_tareas` en `execution/radar/recolectar.py`).
**Una tarea nueva se escribe así o el radar la marca como "no pasa por correr.sh".**
No reintenta la tarea entera (duplicaría mails o plata): el reintento va adentro del
script, en el paso que sólo lee. Instalar o cambiar un plist:
`cp execution/launchd/com.facu.X.plist ~/Library/LaunchAgents/ && launchctl unload … && launchctl load …`,
y verificar con `launchctl list | grep facu`.

## Lo que hay que decidir todavía

- **Los extractos del Macro los bajás vos del homebanking al Desktop.** Eso es lo único
  del cierre de mes que sigue siendo manual, y no hay forma de automatizarlo sin
  credenciales del banco. Lo razonable es que sigas bajándolo vos: son 2 minutos por mes
  y el resto se encadena solo.
- **Nordelta Plaza no tiene skill.** Su informe base es de abril 2022. Antes de
  automatizar nada ahí hay que actualizar el estado (ver `active/nordelta-plaza/`).
- **Chaco**: falta definir de dónde sale el precio de referencia del kilo. Sin eso no hay
  skill de precios, por más Gemini que haya.

## Lo que NO se automatiza, a propósito

- Mandarle cualquier cosa a Richi, a un locatario o a un frigorífico. Se prepara entero
  y se frena esperando tu OK.
- Escribir en el Master Plan sin que lo revises.
- Cualquier número que salga de una estimación en vez de la fuente.
