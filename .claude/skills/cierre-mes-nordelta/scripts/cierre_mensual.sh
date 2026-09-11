#!/usr/bin/env bash
# El cierre de mes del Paseo, entero, sin que nadie apriete nada.
#
# Lo corre launchd (com.facu.reporte-inversores) el 16 de cada mes, cuando el
# extracto del Macro del mes anterior ya entro.
#
#   1. Sincroniza a Supabase lo que solo esta en el Master Plan. El sync de la app
#      va en UN SOLO SENTIDO, asi que todo lo que se carga en el Sheet durante el
#      cierre nunca vuelve a la app: sin este paso, la app muestra meses
#      incompletos y nadie se entera.
#   2. Arma el reporte para inversores y lo deja EN BORRADORES. No manda (regla 10).
#
# El paso 1 puede fallar sin frenar el 2: el reporte sale del Master Plan, que no
# depende de Supabase. Pero el fallo queda gritado en el log, no escondido.

set -uo pipefail
PY=/Users/Facu/facu-os/.venv/bin/python
S=/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts

echo "=================================================================="
echo "CIERRE DE MES — $(date '+%d/%m/%Y %H:%M')"
echo "=================================================================="

echo
echo "--- 1/2 · Sincronizando Supabase con el Master Plan ---"
if "$PY" "$S/sincronizar_supabase.py" --aplicar; then
  echo "    sincronizacion OK"
  sync_ok=1
else
  echo "!!! LA SINCRONIZACION FALLO (codigo $?)."
  echo "!!! La app del Paseo va a seguir mostrando meses incompletos hasta que"
  echo "!!! alguien corra sincronizar_supabase.py --aplicar a mano."
  sync_ok=0
fi

echo
echo "--- 2/2 · Reporte para inversores ---"
if ! "$PY" "$S/reporte_inversores.py" --borrador; then
  echo "!!! EL REPORTE FALLO. No hay borrador nuevo en Gmail."
  exit 1
fi

echo
if [[ $sync_ok -eq 1 ]]; then
  echo "Listo: la app y el Master Plan dicen lo mismo, y el borrador espera en Gmail."
else
  echo "Borrador listo, PERO la sincronizacion con la app fallo — ver arriba."
  exit 1
fi
