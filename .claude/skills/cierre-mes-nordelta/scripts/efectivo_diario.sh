#!/usr/bin/env bash
# Lo que Mati cobra en efectivo, volcado solo a las Ctas Ctes.
#
# Lo corre launchd (com.facu.efectivo-diario) todos los días a las 7:30.
#
# Lo que Mati carga en la app (cobros Y egresos) ya llega solo a Movimientos por
# el POST al Apps Script. Lo que se hacía a mano era:
#
#   1. Chequear que la app y la planilla digan lo mismo (--estricto). Un cobro que
#      está en la app y no en la planilla no se vuelca a ninguna pestaña. Si no
#      coinciden, NO se sigue.
#   2. Volcar a la pestaña de cada local los cobros por Caja (--solo-efectivo).
#      Lo de banco espera al extracto: automatizarlo arriesga duplicar un pago.
#      volcar_cobros.py verifica cada local releyendo el saldo.
#
# NO publica el link de Mati. No hace falta a diario: la app le resta a la foto
# publicada los cobros posteriores a su `cobrosDesde`, así que la tarjeta de Mati
# se mantiene al día sola. La foto se vuelve a publicar cuando cambian los CARGOS
# (principio de mes): `deuda_efectivo.py --cobros-en-planilla` + deploy.sh.
#
# Cualquier falla corta en ese paso; el aviso a Facu sale de correr.sh.

set -uo pipefail
PY=/Users/Facu/facu-os/.venv/bin/python
S=/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts
LOG=$(mktemp)
DESDE=$(date -v-60d +%Y-%m-%d)

exec > >(tee "$LOG") 2>&1

# El mail lo decide correr.sh (execution/avisar.py). Mandaba uno propio además: llegaban dos.
avisar() {
  echo "!!! $1"
  exit 1
}

echo "=================================================================="
echo "EFECTIVO DIARIO — $(date '+%d/%m/%Y %H:%M')"
echo "=================================================================="

# La espera de red la hace correr.sh, UNA vez. Este script tenía una segunda espera
# propia: el 10/11/2026 la Mac cerrada despertó 45 s (DarkWake), correr.sh vio red, y
# esta segunda espera la perdió y quemó sus 15 minutos entre DarkWakes hasta morir a
# las 08:44, con un mail de falla y los datos sanos. No volver a agregarla acá.
# Un día perdido se recupera solo: el volcado mira los últimos 60 días.

echo; echo "--- 1/2 · ¿La app y la planilla dicen lo mismo? ---"
"$PY" "$S/sincronizar_supabase.py" --aplicar --estricto \
  || avisar "paso 1 cortado: o la app y la planilla no coinciden, o no se pudo bajar una de las dos (mirar el error de arriba; el 05 y 06/11/2026 fue timeout de red, no diferencia)"

echo; echo "--- 2/2 · Volcando cobros en efectivo a las pestañas ---"
"$PY" "$S/volcar_cobros.py" --desde "$DESDE" --solo-efectivo --escribir \
  || avisar "el volcado a las pestañas quedó mal (paso 2)"

echo; echo "Listo."
