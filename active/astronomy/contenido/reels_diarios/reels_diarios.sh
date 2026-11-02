#!/bin/bash
# Reels diarios: un Claude headless busca tendencias, arma 5 reels con material real y los
# publica como reels de prueba en @astronomy.academy (instrucciones en PROMPT.md).
# Lo corre launchd todos los días (execution/launchd/com.facu.reels-diarios.plist), a través de
# execution/launchd/correr.sh (red, registro de corridas y mail si falla).
#
# --permission-mode dontAsk: ~/.claude/settings.json tiene defaultMode «auto» y el headless lo heredaba
# — el 29/10 el agente hizo un git commit que no estaba en la lista. Con dontAsk, lo que no está
# en --allowedTools se niega sin preguntar (probado headless: git y `echo >` DENEGADOS, ls permitido).
# Reglas de archivos: sólo Edit(...) (cubre también Write); rutas absolutas con // adelante (con
# una sola / son relativas al repo). Probado headless el 28/10/2026: qa.json, pendiente.lock y
# los .py quedan DENEGADOS; guion.json en la carpeta del día, permitido.
# Los controles (QA, tope de 10, duplicados) viven en los .py y en registro.jsonl, y el agente
# NO los puede tocar: --disallowedTools le niega editar código, el registro y los qa.json, y sólo
# puede escribir en la carpeta del día y en sus tres archivos de memoria. Avisa según lo que dice
# registro.jsonl, no según el texto del agente.
set -o pipefail
OS=/Users/Facu/facu-os
RD=$OS/active/astronomy/contenido/reels_diarios
PY=$OS/.venv/bin/python
CLAUDE=/Users/Facu/.local/node/bin/claude
export REELS_HOY=$(date +%F)          # publicar.py cuenta el tope sobre ESTE día aunque cruce la medianoche
HOY=$REELS_HOY
BASE="/Users/Facu/Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/Reels-diarios"
DIA="$BASE/$HOY"
MAX_SEG=$((3 * 3600))                 # una corrida colgada no puede comerse la de mañana
mkdir -p "$DIA"
LOG="$DIA/corrida.log"
CORRIDA=$(mktemp -t reels-corrida)    # sólo lo de ESTA corrida (el LOG acumula las del día)

# El texto va por argv, nunca adentro del AppleScript: viene de afuera.
avisar() { osascript -e 'on run a' -e 'display notification (item 1 of a) with title "Reels diarios" sound name "Ping"' -e 'end run' "$1"; }
publicados() { local n; n=$(grep -c "\"fecha\": \"$HOY\"" "$RD/registro.jsonl" 2>/dev/null); echo "${n:-0}"; }

# Una sola corrida a la vez.
CANDADO=/tmp/facu-reels-diarios.lock
if ! mkdir "$CANDADO" 2>/dev/null; then
  echo "$(date) ya hay una corrida en curso ($CANDADO); salgo" >> "$LOG"
  exit 0
fi
trap 'rmdir "$CANDADO"; rm -f "$CORRIDA"' EXIT

{ date; echo; } >> "$LOG"
ANTES=$(publicados)
if [ "$ANTES" -ge 5 ]; then
  echo "ya hay $ANTES publicados hoy: nada que hacer" >> "$LOG"
  exit 0
fi

cd "$OS" || exit 1
# perl alarm = timeout (macOS no trae `timeout`).
perl -e 'alarm shift; exec @ARGV' "$MAX_SEG" "$CLAUDE" -p "$(cat "$RD/PROMPT.md")

Hoy es $HOY. DIA = $DIA
Comandos exactos (otro camino al Python está bloqueado):
  $PY $RD/indexar_material.py
  $PY $RD/leer_trials.py
  $PY $RD/armar_reel.py \"\$DIA/NN-slug/guion.json\"
  $PY $RD/publicar.py \"\$DIA/NN-slug\" --send
  $PY $RD/pedir_filmacion.py \"\$DIA/filmar.md\" --send" \
  --model sonnet \
  --permission-mode dontAsk \
  --allowedTools "WebSearch" "WebFetch" "Read" "Glob" "Grep" \
    "Edit(/$DIA/**)" \
    "Edit(/$RD/aprendizajes.md)" "Edit(/$RD/competencia.md)" "Edit(/$RD/referencias.md)" "Edit(/$RD/material.json)" \
    "Bash(mkdir -p $DIA/:*)" "Bash(mkdir -p \"$DIA/:*)" "Bash(ls:*)" \
    "Bash($PY $RD/leer_trials.py:*)" "Bash($PY $RD/armar_reel.py:*)" "Bash($PY $RD/publicar.py:*)" \
    "Bash($PY $RD/portada.py:*)" "Bash($PY $RD/indexar_material.py:*)" "Bash($PY $RD/pedir_filmacion.py:*)" \
  --disallowedTools "Edit(//**/qa.json)" "Edit(//**/registro.jsonl)" "Edit(//**/pendiente.lock)" \
    "Edit(/$OS/**/*.py)" "Edit(/$OS/**/*.sh)" "Edit(/$RD/PROMPT.md)" \
  > "$CORRIDA" 2>&1
COD=$?
cat "$CORRIDA" >> "$LOG"

DESPUES=$(publicados)
NUEVOS=$((DESPUES - ANTES))
echo "publicados hoy: $DESPUES (esta corrida: $NUEVOS) · claude salió con $COD" >> "$LOG"

if [ "$NUEVOS" -ge 1 ]; then
  avisar "$NUEVOS reels de prueba publicados hoy ($DESPUES en total). Resumen en Reels-diarios/$HOY/resumen.md"
  exit 0
fi
[ "$COD" -eq 142 ] && MOTIVO="se pasó de 3 horas" || MOTIVO="claude salió con $COD"
avisar "FALLA: no se publicó ningún reel ($MOTIVO). Mirá Reels-diarios/$HOY/corrida.log"
exit 1
