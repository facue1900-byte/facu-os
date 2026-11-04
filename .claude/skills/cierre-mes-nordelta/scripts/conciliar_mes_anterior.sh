#!/usr/bin/env bash
# Concilia el extracto de cierre del mes anterior contra el Master Plan vivo. Sólo lee.
#
#   conciliar_mes_anterior.sh [AAAA-MM]
#
# Sale con 0 sólo si conciliar.py dice CIERRA. Falta de extracto o de datos = 1: un
# control que no se pudo hacer no es un control que dio bien.
# Un PDF "ultimos movimientos" no sirve: es parcial, no trae el cierre del mes.

set -uo pipefail
PY=/Users/Facu/facu-os/.venv/bin/python
S=/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts
BASE="/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta"
MASTER=1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs

mes="${1:-$(date -v-1m +%Y-%m)}"
meses=(Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre)
nombre="${meses[$((10#${mes#*-} - 1))]}"
pdf="$BASE/${mes%-*}/$nombre ${mes%-*}.pdf"

if [[ ! -f "$pdf" ]]; then
  echo "!!! FALTA EL EXTRACTO DE CIERRE: $pdf"
  echo "!!! $mes queda SIN conciliar hasta que esté ese PDF."
  exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
cd /Users/Facu/facu-os || exit 1
if ! "$PY" -c "import sys; sys.path.insert(0,'execution'); from google_auth import bajar_xlsx; bajar_xlsx(sys.argv[1], sys.argv[2])" "$MASTER" "$tmp/master.xlsx"; then
  echo "!!! No pude bajar el Master Plan: $mes queda SIN conciliar."
  exit 1
fi
"$PY" "$S/conciliar.py" "$pdf" "$tmp/master.xlsx" "$mes"
