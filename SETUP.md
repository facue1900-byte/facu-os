# Qué falta para que esté todo conectado

Estado al 27/07/2026. Lo que está tildado ya funciona; lo que no, está bloqueado
esperando algo que **solo podés hacer vos** (un login, una key, un permiso).

## Ya funciona

- [x] **El OS** — `~/facu-os`, git con 6 commits, estructura completa.
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
      13 tests en `execution/tests/` (`.venv/bin/python -m pytest execution/tests/ -q`).

## Bloqueado esperándote (en orden de lo que más desbloquea)

### 1. Credenciales de Google — 10 min · desbloquea TODO lo automático

Es el cuello de botella real. Sin esto no hay ni un solo proceso que corra solo.

1. Entrá a [console.cloud.google.com](https://console.cloud.google.com) → creá un
   proyecto (o usá uno que tengas).
2. **APIs y servicios → Biblioteca** → habilitá **Google Sheets API**, **Google Drive
   API** y **Gmail API**.
3. **Pantalla de consentimiento** → publicala en **Producción**.
   ⚠️ Si la dejás en "Testing", el token se vence **cada 7 días** y todo se corta sin avisar.
4. **Credenciales → Crear → ID de cliente OAuth → App de escritorio** → descargá el JSON.
5. Guardalo como `~/facu-os/credentials.json` y corré una sola vez:

```bash
cd ~/facu-os && .venv/bin/python execution/google_auth.py --setup
```

Se abre el navegador, aceptás, y listo para siempre.

**Qué se enciende con esto:** bajar el Master Plan solo (sin truncado), el radar de
rampa automático el día 5, cargar movimientos en el sheet sin abrir el navegador, y
mandar reportes por mail.

### 2. GitHub — 3 min · hoy el OS existe en un solo disco

```bash
gh auth login          # elegí HTTPS y "Login with a web browser"
cd ~/facu-os && gh repo create facu-os --private --source=. --push
```

**Qué se enciende:** backup real (hoy si se rompe el disco perdés el OS), y que las
tareas en la nube corran *tus* scripts en vez de improvisar la lógica.

### 3. Token de Apify — 2 min · solo desbloquea `prospectar-gmaps`

1. [console.apify.com/settings/integrations](https://console.apify.com/settings/integrations)
   → copiá el API token.
2. Pegalo en `~/facu-os/.env` en `APIFY_API_TOKEN=`.

**Qué se enciende:** listas de candidatos a locatario para los locales vacíos del Paseo,
venues y productoras para eventos, frigoríficos y transportistas por zona.

### 4. Encender el radar automático — 1 min, después del punto 1

**Hoy NO está cargado**: el `.plist` está en el repo pero no en `~/Library/LaunchAgents`,
y `launchctl list` no lo muestra. Está bien que sea así — depende del punto 1, y el propio
`.plist` avisa que no se cargue antes de tiempo. Pero que exista el archivo no significa
que corra: verificar siempre con `launchctl list | grep facu`.

Probalo a mano primero, varias veces:

```bash
cd ~/facu-os && .venv/bin/python \
  .claude/skills/cierre-mes-nordelta/scripts/alerta_rampa.py --mes 2026-08
```

Sin `--send` no manda nada, solo muestra. Cuando te convenza:

```bash
cp ~/facu-os/execution/launchd/com.facu.alerta-rampa.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.facu.alerta-rampa.plist
```

Día 5 de cada mes, 9:00, te avisa si un alta se atrasó. **La Jaula arranca en agosto**:
esta es la primera que hay que controlar.

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
