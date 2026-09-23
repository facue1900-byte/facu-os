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
# Cualquier falla corta en ese paso y le manda un mail a Facu (a él solo).

set -uo pipefail
PY=/Users/Facu/facu-os/.venv/bin/python
S=/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts
LOG=$(mktemp)
DESDE=$(date -v-60d +%Y-%m-%d)

exec > >(tee "$LOG") 2>&1

avisar() {
  echo "!!! $1"
  "$PY" - "$1" "$LOG" <<'EOF'
import sys, os, base64
from email.mime.text import MIMEText
sys.path.insert(0, "/Users/Facu/facu-os")
from dotenv import load_dotenv
load_dotenv("/Users/Facu/facu-os/.env")
from execution.google_auth import gmail
para = os.environ["MAIL_FACU"]
cuerpo = open(sys.argv[2]).read()[-6000:]
m = MIMEText(f"{sys.argv[1]}\n\n--- log ---\n{cuerpo}")
m["to"], m["subject"] = para, f"🔴 Paseo · efectivo diario frenado: {sys.argv[1][:60]}"
gmail().users().messages().send(
    userId="me", body={"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}).execute()
print(f"    mail a {para}")
EOF
  exit 1
}

echo "=================================================================="
echo "EFECTIVO DIARIO — $(date '+%d/%m/%Y %H:%M')"
echo "=================================================================="

echo; echo "--- 1/2 · ¿La app y la planilla dicen lo mismo? ---"
"$PY" "$S/sincronizar_supabase.py" --aplicar --estricto \
  || avisar "la app y la planilla no coinciden (paso 1)"

echo; echo "--- 2/2 · Volcando cobros en efectivo a las pestañas ---"
"$PY" "$S/volcar_cobros.py" --desde "$DESDE" --solo-efectivo --escribir \
  || avisar "el volcado a las pestañas quedó mal (paso 2)"

echo; echo "Listo."
