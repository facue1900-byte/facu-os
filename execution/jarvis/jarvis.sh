#!/bin/bash
# Abre la pantalla de Jarvis. Si el servidor no está corriendo, lo levanta en segundo plano.
#   ~/facu-os/execution/jarvis/jarvis.sh
OS=/Users/Facu/facu-os
LOG=$OS/data/logs/jarvis.log
mkdir -p "$OS/data/logs"
if ! /usr/bin/curl -s -o /dev/null --max-time 2 http://127.0.0.1:7777/; then
  nohup "$OS/.venv/bin/python" "$OS/execution/jarvis/servidor.py" >>"$LOG" 2>&1 &
  for i in $(seq 1 40); do /usr/bin/curl -s -o /dev/null --max-time 1 http://127.0.0.1:7777/ && break; sleep 0.25; done
fi
if ! /usr/bin/curl -s -o /dev/null --max-time 2 http://127.0.0.1:7777/; then
  /usr/bin/osascript -e 'display notification "El servidor no levantó: mirá data/logs/jarvis.log" with title "Jarvis"'
  exit 1
fi
# Ventana propia de Chrome, sin barras y con un perfil APARTE: el micrófono y el botón «Sí» no
# comparten pestañas ni extensiones con la navegación de todos los días.
open -na "Google Chrome" --args --app=http://127.0.0.1:7777 --start-fullscreen \
  --user-data-dir="$OS/data/jarvis/chrome-perfil" --no-first-run --no-default-browser-check
