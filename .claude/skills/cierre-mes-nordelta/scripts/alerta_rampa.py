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
import os
import pathlib
import subprocess
import sys
import re

from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))
load_dotenv(RAIZ / ".env")

from execution.google_auth import bajar_xlsx, gmail  # noqa: E402
from execution.mail_format import render  # noqa: E402

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


def _ar(numero):
    """El radar imprime 2,000,000; en el mail va como se lee acá: 2.000.000."""
    return numero.replace(",", ".")


def _mes(aaaa_mm):
    return f"{aaaa_mm[5:]}/{aaaa_mm[:4]}"


def armar_mail(salida, mes):
    """Sólo lo atrasado y la plata. Las próximas altas siguen en el radar, no hacen falta acá."""
    atrasados, acumulado, en_bloque = [], None, False
    for linea in salida.splitlines():
        t = linea.strip()
        if t == "ATRASADOS":
            en_bloque = True
        elif t.startswith("Acumulado no cobrado:"):
            acumulado = "$" + _ar(t.split(":", 1)[1].strip().lstrip("$"))
            en_bloque = False
        elif en_bloque and t:
            m = re.match(r"(.+?)\s+desde (\S+)\s+esperado \$\s*([\d,]+)/mes\s+entró \$\s*([\d,]+)\s+\((.+)\)", t)
            atrasados.append(f"{m[1]}: esperado ${_ar(m[3])}/mes desde {_mes(m[2])}, entró ${_ar(m[4])} ({m[5]})" if m else t)
    return render(
        area="paseo", nivel="urgente" if atrasados else "reporte",
        titulo=(f"{len(atrasados)} alquiler{'es' if len(atrasados) != 1 else ''} atrasado{'s' if len(atrasados) != 1 else ''} · {_mes(mes)}"
                if atrasados else f"Rampa sin atrasos · {_mes(mes)}"),
        resumen="Locales que según el plan ya tendrían que estar pagando y no entró plata.",
        kpis=[("Sin cobrar acumulado", acumulado, "rojo"), ("Locales atrasados", len(atrasados), "rojo")] if acumulado else None,
        accion="Confirmá con cada local si es un atraso real o si cambió su fecha de alta en el Master Plan.",
        secciones=[("Atrasados", atrasados)],
        origen="los montos salen del Master Plan, no de una estimación",
    )


def mandar(cuerpo, mes, para):
    msg = armar_mail(cuerpo, mes).mime(para)
    crudo = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gmail().users().messages().send(userId="me", body={"raw": crudo}).execute()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--send", action="store_true",
                   help="Manda el mail. Sin esto, solo imprime.")
    p.add_argument("--mes", help="Mes de corte AAAA-MM (default: el mes actual)")
    p.add_argument("--para", default=os.environ.get("MAIL_FACU"),
                   help="Destinatario. Default: MAIL_FACU del .env — solo Facu; "
                        "a Richi no se le manda nada sin OK previo.")
    p.add_argument("--siempre", action="store_true",
                   help="Manda el mail aunque no haya atrasos (default: solo si hay).")
    a = p.parse_args()

    if not a.para:
        sys.exit("Falta el destinatario: definí MAIL_FACU en el .env o pasá --para.")

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
