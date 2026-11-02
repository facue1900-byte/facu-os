#!/bin/bash
# Por acá pasa TODA tarea programada de facu-os. Hace tres cosas que antes cada plist
# hacía a su manera (o no hacía):
#
#   1. Espera la red hasta 15 minutos. launchd dispara apenas la Mac despierta, muchas
#      veces sin red: así se perdieron el reporte a inversores del 16/09 y el efectivo
#      del 27/09, 29/09 y 01/10/2026.
#   2. Anota cada corrida en data/logs/tareas.jsonl (tarea, inicio, fin, código). El
#      radar de las 7:30 lo lee y dice qué tarea falló o NO corrió (Mac apagada,
#      plist sin cargar): ese caso no lo puede avisar la tarea misma.
#   3. Si sale con error: notificación de macOS, y avisar.py decide si además va un mail
#      a Facu (a él solo): no por cada falla, ver la regla ahí. Es el ÚNICO mail de falla:
#      las tareas no mandan el suyo, así no llegan dos por lo mismo.
#
# NO reintenta la tarea entera a propósito: casi todas escriben o mandan algo, y repetir
# una corrida a medias duplica plata o mails. El reintento va adentro de cada script, en
# el paso que sólo lee (ver juntar() en execution/reporte_equipo.py).
#
#   correr.sh <nombre> -- <comando como un solo string>
#   <nombre> TIENE que ser el sufijo del label (com.facu.<nombre>): el radar los cruza.
#
# Ejemplo (desde un plist):
#   /bin/bash /Users/Facu/facu-os/execution/launchd/correr.sh reporte-equipo -- \
#     "/Users/Facu/facu-os/.venv/bin/python /Users/Facu/facu-os/execution/reporte_equipo.py --send"

OS=/Users/Facu/facu-os
PY=$OS/.venv/bin/python
REG=$OS/data/logs/tareas.jsonl
mkdir -p "$OS/data/logs"

NOMBRE=$1; shift
[[ $1 == -- ]] && shift
CMD=$1
if [[ -z $NOMBRE || -z $CMD ]]; then
  echo "Uso: correr.sh <nombre> -- <comando>" >&2
  exit 64
fi

INICIO=$(date '+%Y-%m-%dT%H:%M:%S%z')
SAL=$(mktemp); ERR=$(mktemp)

notificar() { osascript -e "display notification \"$1\" with title \"Tarea: $NOMBRE\" sound name \"Basso\"" 2>/dev/null; }
registrar() {
  printf '{"tarea":"%s","inicio":"%s","fin":"%s","codigo":%d}\n' \
    "$NOMBRE" "$INICIO" "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$1" >> "$REG"
}

echo "=== $NOMBRE · $(date '+%d/%m/%Y %H:%M') ==="

# La red se decide UNA vez. Volver a preguntar después del loop perdió el radar y el efectivo
# del 01/11 y el reporte de pauta del 02/11/2026: la Mac recién despierta contestó bien la
# primera y mal la segunda, y la tarea moría con "15 minutos" escrito a los 19 segundos.
HAY_RED=0
for i in $(seq 1 30); do
  if host -W 3 www.googleapis.com >/dev/null 2>&1; then HAY_RED=1; break; fi
  [[ $i -eq 1 ]] && echo "Sin red todavía: espero hasta 15 minutos..."
  sleep 30
done
if [[ $HAY_RED -eq 0 ]]; then
  echo "!!! Sin red después de 15 minutos: no corrió."
  registrar 75
  notificar "No corrió: sin red 15 minutos. El radar lo va a marcar."
  exit 75
fi

# Cada stream a su archivo y recién al final a los logs del plist: sin process
# substitution, que en bash 3.2 no se puede esperar y dejaba el mail sin la cola.
/bin/bash -lc "$CMD" > "$SAL" 2> "$ERR"
CODIGO=$?
cat "$SAL"; cat "$ERR" >&2
registrar $CODIGO

if [[ $CODIGO -ne 0 ]]; then
  notificar "FALLÓ (código $CODIGO). Detalle en data/logs/."
  cat "$SAL" "$ERR" > "$SAL.cola"
  "$PY" "$OS/execution/avisar.py" --tarea "$NOMBRE" --codigo "$CODIGO" "$SAL.cola" \
    || echo "!!! Tampoco pude mandar el mail de aviso. Queda el registro para el radar."
  rm -f "$SAL.cola"
fi
rm -f "$SAL" "$ERR"
exit $CODIGO
