#!/bin/bash
# Bandeja de Vlado → hecha sola (27/11/2026). Pedido de Facu: «hacé las tareas que deja Vlado,
# siempre sin mi ok» y «seguí revisando 24/7 sin parar».
#
# Cada 15 min (launchd: com.facu.bandeja-vlado, a través de correr.sh):
#   1. git pull de astronomy-os.
#   2. Si en bandeja/para/Facu/ no hay nada nuevo, sale sin gastar nada.
#   3. Si hay: un Claude headless (Opus) hace las tareas como lo haría la sesión de Facu
#      (verifica, commitea, pushea, mueve a vistos/ y le contesta a Vlado en para/Vlado/).
#   4. Avisa a Facu por Telegram con lo que hizo.
#
# Lo que NO hace, nunca (regla 10): mandar mails, WhatsApps, posteos, transferencias ni correr
# nada con --send. Si una tarea lo necesita, o necesita una decisión de Facu, la deja en
# para/Facu con «NECESITA A FACU» y no la reintenta hasta que el archivo cambie.
#
# No reintenta en loop: guarda el hash de cada archivo intentado (data/logs/bandeja_vlado.json).
# Una tarea vuelve a correr sólo si Vlado la edita.
# Con la Mac apagada no corre (es launchd); lo pendiente lo agarra en la primera corrida al prender.
set -o pipefail
OS=/Users/Facu/facu-os
AOS=$OS/active/astronomy
PY=$OS/.venv/bin/python
CLAUDE=/Users/Facu/.local/node/bin/claude
export PATH=/Users/Facu/.local/node/bin:/Users/Facu/.local/gh/bin:/Users/Facu/.local/bin:$PATH
ESTADO=$OS/data/logs/bandeja_vlado.json
LOCK=/tmp/bandeja_vlado.lock
MAX_SEG=$((90 * 60))
mkdir -p "$OS/data/logs"

# Una sola corrida a la vez: una tarea larga no se pisa con la siguiente.
if ! mkdir "$LOCK" 2>/dev/null; then
  if [[ -n $(find "$LOCK" -maxdepth 0 -mmin +120 2>/dev/null) ]]; then rm -rf "$LOCK"; mkdir "$LOCK"; else echo "otra corrida en curso"; exit 0; fi
fi
trap 'rm -rf "$LOCK"' EXIT

git -C "$AOS" pull -q --rebase --autostash || { echo "!!! git pull de astronomy-os falló"; exit 1; }

# Tareas nuevas o editadas desde el último intento.
NUEVAS=$("$PY" - "$AOS/bandeja/para/Facu" "$ESTADO" <<'EOF'
import hashlib, json, pathlib, sys
carpeta, estado = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
visto = json.loads(estado.read_text()) if estado.exists() else {}
for f in sorted(carpeta.glob("*.md")):
    h = hashlib.sha1(f.read_bytes()).hexdigest()
    if visto.get(f.name) != h:
        print(f)
EOF
)
if [[ -z $NUEVAS ]]; then echo "$(date '+%F %T') sin tareas nuevas"; exit 0; fi
echo "$(date '+%F %T') tareas: $NUEVAS"

CORRIDA=$(mktemp)
cd "$AOS"
perl -e 'alarm shift; exec @ARGV' "$MAX_SEG" "$CLAUDE" -p "Sos la sesión de Facu en astronomy-os, corriendo sola (tarea programada bandeja-vlado).
Vlado (socio) dejó estas tareas para Facu:
$NUEVAS

Facu pidió (27/11/2026): «hacé las tareas que deja Vlado, siempre sin mi ok». Hacelas enteras como
las haría Facu, con todas las reglas de la Constitución (~/facu-os/os/01-CONSTITUCION.md) y el
CLAUDE.md de cada repo:
- La web es ~/Desktop/Productoras/Astronomy/Academia/astronomy-members (push a main = deploy).
  Antes de tocar: git pull --rebase --autostash. Después: npx tsc --noEmit -p . y, si toca plata o
  Finanzas/Resultado, npm run verificar:resultado. Verificá contra la base real o la página real.
- DDL y queries: Management API de Supabase con SUPABASE_ACCESS_TOKEN de ~/facu-os/.env, SÓLO el
  proyecto de Astronomy qeakrjnseboiulcojlcw. Verificá contra information_schema después.
- Antes de cambiar o borrar filas con plata, guardá cómo estaban en ~/facu-os/archive/.
- Commit (mensaje en inglés que explique qué y por qué, con las líneas
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>) y push, en cada repo que toques.
- Cuando una tarea quede hecha y verificada: git mv del archivo a bandeja/vistos/ (con -f si ya
  existe), escribí la respuesta a Vlado en bandeja/para/Vlado/<fecha>_respuesta-<tema>.md (qué se
  hizo, con números y commits), commit y push de astronomy-os.

PROHIBIDO, sin excepción: mandar mails, WhatsApps, mensajes de Telegram, posteos o transferencias;
correr cualquier script con --send; cambiar algo de Paseo Nordelta, campos o cripto; tocar la base
wujutradczplokjrgmdo. Si una tarea necesita algo de eso, o una decisión que es de Facu (plata nueva,
reparto, algo ambiguo), no la hagas: agregá al final del archivo una línea
«**NECESITA A FACU (<fecha>):** <qué y por qué>», dejalo en para/Facu, commit y push.

Al final, escribí SÓLO un resumen corto para Facu (máx. 12 líneas, español rioplatense, sin
markdown pesado): qué hiciste por tarea, qué verificaste, y qué quedó esperándolo." \
  --model opus \
  --permission-mode dontAsk \
  --strict-mcp-config \
  --allowedTools "Read" "Glob" "Grep" "Edit" "Write" "Bash" \
  --disallowedTools "WebFetch" "WebSearch" \
  < /dev/null > "$CORRIDA" 2>&1
COD=$?
cat "$CORRIDA"

# Marca como intentado el estado ACTUAL de cada archivo que queda (los hechos ya se movieron).
"$PY" - "$AOS/bandeja/para/Facu" "$ESTADO" <<'EOF'
import hashlib, json, pathlib, sys
carpeta, estado = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
estado.write_text(json.dumps({f.name: hashlib.sha1(f.read_bytes()).hexdigest() for f in carpeta.glob("*.md")}, indent=1))
EOF

QUEDAN=$(ls "$AOS/bandeja/para/Facu/"*.md 2>/dev/null | xargs -n1 basename 2>/dev/null)
"$PY" - "$CORRIDA" "$COD" "$QUEDAN" <<'EOF'
import json, os, sys, urllib.parse, urllib.request, pathlib
for l in pathlib.Path("/Users/Facu/facu-os/.env").read_text().splitlines():
    if "=" in l and not l.lstrip().startswith("#"):
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"'))
salida, cod, quedan = pathlib.Path(sys.argv[1]).read_text()[-3000:].strip(), sys.argv[2], sys.argv[3].strip()
cab = "🤖 Bandeja de Vlado" + ("" if cod == "0" else f" — ⚠️ el agente salió con código {cod}")
texto = f"{cab}\n\n{salida or '(sin resumen)'}" + (f"\n\nSigue en para/Facu:\n{quedan}" if quedan else "\n\n✅ Bandeja vacía.")
token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
if token and chat:
    d = urllib.parse.urlencode({"chat_id": chat, "text": texto[:4000]}).encode()
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=d, timeout=30)
    except Exception as e:
        print(f"!!! Telegram: {e!r}")
else:
    print("!!! sin TELEGRAM_BOT_TOKEN/CHAT_ID: no avisé")
EOF
rm -f "$CORRIDA"
exit $COD
