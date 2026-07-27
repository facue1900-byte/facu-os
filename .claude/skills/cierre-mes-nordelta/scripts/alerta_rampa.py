#!/usr/bin/env python3
"""
Alerta automática de la rampa de alquileres — Paseo Nordelta.

Baja el Master Plan solo, corre el radar y, si hay un alta atrasada, avisa por mail.
Pensado para correr desde launchd el día 5 de cada mes.

    .venv/bin/python .../alerta_rampa.py                  # solo muestra, NO manda
    .venv/bin/python .../alerta_rampa.py --send           # manda el mail

Por defecto NO manda nada. El `--send` es deliberado: un script que avisa de plata
tiene que probarse a mano varias veces antes de dejarlo suelto.

El mes de corte se toma del sistema, pero se puede forzar con --mes 2026-08.
"""

import argparse
import base64
import datetime
import pathlib
import subprocess
import sys
from email.message import EmailMessage

RAIZ = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))

from execution.google_auth import bajar_xlsx, gmail  # noqa: E402

MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
RADAR = pathlib.Path(__file__).with_name("radar_rampa.py")
DESTINO = RAIZ / "data" / "master_plan.xlsx"


def correr_radar(xlsx, mes):
    r = subprocess.run(
        [sys.executable, str(RADAR), str(xlsx), mes],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"El radar falló:\n{r.stderr}")
    return r.stdout


def mandar(cuerpo, mes, para):
    msg = EmailMessage()
    msg["To"] = para
    msg["Subject"] = f"Radar de rampa — Paseo Nordelta, corte {mes}"
    msg.set_content(
        f"{cuerpo}\n\n--\nGenerado por alerta_rampa.py. Los montos salen del Master "
        f"Plan, no de una estimación.\n"
    )
    crudo = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gmail().users().messages().send(userId="me", body={"raw": crudo}).execute()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--send", action="store_true",
                   help="Manda el mail. Sin esto, solo imprime.")
    p.add_argument("--mes", help="Mes de corte AAAA-MM (default: el mes actual)")
    p.add_argument("--para", default="facue1900@gmail.com",
                   help="Destinatario. Solo Facu por default: a Richi no se le manda "
                        "nada sin OK previo.")
    p.add_argument("--siempre", action="store_true",
                   help="Manda el mail aunque no haya atrasos (default: solo si hay).")
    a = p.parse_args()

    hoy = datetime.date.today()
    mes = a.mes or f"{hoy.year}-{hoy.month:02d}"

    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    bajar_xlsx(MASTER_PLAN, DESTINO)
    salida = correr_radar(DESTINO, mes)
    print(salida)

    hay_atraso = "ATRASADOS" in salida
    if not a.send:
        print(f"[dry-run] {'HAY ATRASOS' if hay_atraso else 'sin atrasos'} — "
              f"con --send esto {'se mandaría' if hay_atraso or a.siempre else 'no se mandaría'} "
              f"a {a.para}")
        return

    if hay_atraso or a.siempre:
        mandar(salida, mes, a.para)
        print(f"Mail enviado a {a.para}")
    else:
        print("Sin atrasos: no mando nada.")


if __name__ == "__main__":
    main()
