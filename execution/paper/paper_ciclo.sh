#!/bin/bash
# Un ciclo de la carpeta ficticia: Claude headless mira el mercado, decide y opera en papel.
# Lo corre launchd cada 4 h (execution/launchd/com.facu.paper-trading.plist).
# Avisa por notificación SÓLO si falla; el resultado se lee con `paper.py estado`.
set -o pipefail
OS=/Users/Facu/facu-os
PY=$OS/.venv/bin/python
PAPER="$PY $OS/execution/paper/paper.py"
CLAUDE=/Users/Facu/.local/node/bin/claude
OUT=$OS/data/paper
mkdir -p "$OUT"
LOG="$OUT/ultima-corrida.txt"

avisar() { osascript -e "display notification \"$1\" with title \"Carpeta ficticia\" sound name \"Basso\""; }

{ date; echo; } > "$LOG"
cd "$OS" || exit 1

"$CLAUDE" -p "$(cat "$OS/execution/paper/PROMPT.md")" \
  --model opus \
  --allowedTools "Read" "Bash($PAPER:*)" \
  >> "$LOG" 2>&1

# El valor se anota siempre, operó o no Claude: así el historial no tiene huecos que mientan.
if ! $PAPER snapshot > /dev/null 2>> "$LOG"; then
  avisar "FALLA: no se pudo valuar la carpeta. Mirá data/paper/ultima-corrida.txt"
  exit 2
fi

# Que el juez de la nube la vea. Va al final de cada salida y su falla no cambia el resultado
# del ciclo: la operación ya está hecha, y en el veredicto queda la fecha vieja a la vista.
publicar() {
  /bin/bash "$OS/execution/paper/publicar_historial.sh" >> "$LOG" 2>&1 \
    || avisar "No se pudo publicar el historial: el juez la ve con dato viejo"
}

# Claude a veces escribe la línea final con formato (`PAPER_OK ...` o **PAPER_OK ...**): el
# 02/11/2026 eso dio una falla falsa con el ciclo terminado bien. Tiene que seguir siendo el
# comienzo de la línea; lo que se saca es sólo el formato.
CIERRE='^[`*[:space:]]*PAPER_OK'
if grep -qE "$CIERRE" "$LOG"; then
  grep -E "$CIERRE" "$LOG" | tail -1 | tr -d '`*' | sed 's/^[[:space:]]*//' >> "$OUT/ciclos.log"
  publicar
  exit 0
fi
avisar "FALLA: el ciclo no cerró. Mirá data/paper/ultima-corrida.txt"
publicar
exit 1
