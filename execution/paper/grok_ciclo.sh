#!/bin/bash
# Un ciclo de la carpeta de Grok (20/11/2026, pedido de Facu: «una carpeta exclusiva de Grok y
# comparamos»). Mismo motor, reglas y capital que la de 10.000 de Claude (paper_ciclo.sh); cambia
# el que decide: Grok Build con la suscripción de Facu, que además lee X y la web.
# Lo corre launchd cada 4 h, 5 min después de la de Claude (com.facu.paper-grok).
set -o pipefail
OS=/Users/Facu/facu-os
HERR=$OS/execution/paper/grok_paper.sh
GROK=/Users/Facu/.grok/bin/grok
OUT=$OS/data/paper-grok
mkdir -p "$OUT"
LOG="$OUT/ultima-corrida.txt"

avisar() { osascript -e "display notification \"$1\" with title \"Carpeta de Grok\" sound name \"Basso\""; }

{ date; echo; } > "$LOG"
cd "$OS" || exit 1

# Sólo: su herramienta, leer su carpeta y buscar en X/web. `dontAsk` = todo lo no permitido se rechaza.
# Ojo: sin una regla de lectura prohibida, `cat`/`head` de cualquier archivo pasarían como «sólo lectura»;
# el deny de ~/.ssh activa ese control para todas las lecturas. Probado el 20/11/2026: crear archivo y
# `cat` afuera de su carpeta, rechazados; su herramienta y su diario, OK; `ls` (sólo nombres) pasa.
"$GROK" -p "$(cat "$OS/execution/paper/PROMPT_GROK.md")" \
  --output-format plain --max-turns 30 --permission-mode dontAsk \
  --disallowed-tools "write,search_replace" \
  --allow "Bash($HERR *)" --allow "Read($OUT/**)" \
  --deny "Read(/Users/Facu/.ssh/**)" --deny "Write" --deny "Edit" \
  < /dev/null >> "$LOG" 2>&1

# El valor se anota siempre, operó o no: así el historial no tiene huecos que mientan.
if ! "$HERR" snapshot > /dev/null 2>> "$LOG"; then
  avisar "FALLA: no se pudo valuar la carpeta. Mirá data/paper-grok/ultima-corrida.txt"
  exit 2
fi

CIERRE='^[`*[:space:]]*PAPER_OK'
if grep -qE "$CIERRE" "$LOG"; then
  grep -E "$CIERRE" "$LOG" | tail -1 | tr -d '`*' | sed 's/^[[:space:]]*//' >> "$OUT/ciclos.log"
  exit 0
fi
avisar "FALLA: el ciclo de Grok no cerró. Mirá data/paper-grok/ultima-corrida.txt"
exit 1
