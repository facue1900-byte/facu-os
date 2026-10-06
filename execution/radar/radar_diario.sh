#!/bin/bash
# Radar diario: barre todo (recolectar.py) y un Claude headless reescribe el doc
# "Radar Facu" (https://claude.ai/code/artifact/f91c078c-1bf1-4692-a2d7-1120eb970cc3).
# Lo corre launchd todos los días (execution/launchd/com.facu.radar-diario.plist).
# Avisa con notificación de macOS OK o FALLA según el resultado real.
set -o pipefail
OS=/Users/Facu/facu-os
PY=$OS/.venv/bin/python
CLAUDE=/Users/Facu/.local/node/bin/claude
OUT=$OS/data/radar
mkdir -p "$OUT"
LOG="$OUT/ultima-corrida.txt"

avisar() { osascript -e "display notification \"$1\" with title \"Radar Facu\" sound name \"Ping\""; }

{ date; echo; } > "$LOG"
if ! $PY "$OS/execution/radar/recolectar.py" >> "$LOG" 2>&1; then
  avisar "FALLA: la barrida vino vacía o rota. Mirá data/radar/ultima-corrida.txt"
  exit 2
fi
cp "$OUT/digest.md" "$OUT/digest-$(date +%F).md"

cd "$OS" || exit 1
for i in 1 2; do
  "$CLAUDE" -p "$(cat "$OS/execution/radar/PROMPT.md")" \
    --model opus \
    --allowedTools "ToolSearch Read Glob Grep mcp__claude_ai_Claude_Docs__read mcp__claude_ai_Claude_Docs__update mcp__claude_ai_Claude_Docs__batch mcp__claude_ai_Claude_Docs__guide mcp__claude_ai_Claude_Docs__query mcp__claude_ai_Claude_Docs__create" \
    >> "$LOG" 2>&1
  grep -q "^RADAR_OK" "$LOG" && break
  sleep 120
done

# Borra digests de más de 30 días (son copias; el digest se regenera).
find "$OUT" -name 'digest-*.md' -mtime +30 -delete

if grep -q "^RADAR_OK" "$LOG"; then
  avisar "Radar actualizado. $(grep '^RADAR_OK' "$LOG" | tail -1)"
  exit 0
fi
avisar "FALLA: el radar no se actualizó. Mirá data/radar/ultima-corrida.txt"
exit 1
