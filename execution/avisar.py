"""Le avisa a Facu (a él solo) que una tarea programada falló, y decide si vale un mail.

Lo usa `execution/launchd/correr.sh`. No es "salir al mundo" (regla 10): el único destinatario
posible es MAIL_FACU del .env.

Facu, 02/11/2026: «no quiero que me lleguen muchos mails, solo en días clave o cuando pasa algo
inesperado». En 30 días llegaron 47 automáticos, 18 de una misma tarea fallando. Por eso:
  - una tarea diaria o más seguida avisa recién a la SEGUNDA falla seguida (casi siempre la
    primera es la red de la Mac), salvo las de A_LA_PRIMERA;
  - la misma tarea no vuelve a mandar mail hasta 3 días después.
Lo que no manda mail no se pierde: queda en tareas.jsonl y el radar lo marca como FALLÓ.

    .venv/bin/python execution/avisar.py --tarea reporte-equipo --codigo 1 data/logs/x.log
"""
import argparse
import base64
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timedelta

RAIZ = pathlib.Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "data/logs/tareas.jsonl"
ESTADO = RAIZ / "data/logs/avisos.json"
sys.path.insert(0, str(RAIZ))

ENTRE_MAILS = timedelta(days=3)
FRECUENTE = timedelta(hours=36)
# Una sola falla ya es información: gasto de pauta frenado, o la caja del Paseo sin actualizar.
A_LA_PRIMERA = {"chequeo-pauta", "efectivo-diario"}
# Facu, 02/11/2026, ante «paper-trading salió con código 1»: «si me mandás algo, que sea súper
# claro y clave para tomar decisiones». Un ciclo caído de plata ficticia no le pide ninguna
# decisión: no manda mail nunca y lo marca el radar.
SIN_MAIL = {"paper-trading"}

# tarea: (área, nivel, nombre para el asunto, qué significa)
TAREAS = {
    "efectivo-diario": ("paseo", "urgente", "Efectivo diario frenado", "La caja de efectivo del Paseo puede haber quedado sin actualizar."),
    "alerta-rampa": ("paseo", "urgente", "Alerta de rampa sin correr", "Este mes no se chequeó si hay alquileres atrasados."),
    "reporte-inversores": ("paseo", "urgente", "Cierre de mes: mirar antes de mandar", "No se generó el borrador para inversores, o el banco no concilió, o falta el extracto. No mandes el borrador sin ver data/logs/reporte-inversores.log."),
    "chequeo-pauta": ("astronomy", "revisar", "Pauta: algo dejó de funcionar", "Un anuncio puede no estar gastando, o algo dejó de registrarse."),
    "reporte-pauta": ("astronomy", "revisar", "Reporte de pauta con problemas", "El informe de la semana falló, o algo dejó de registrarse."),
    "reporte-equipo": ("astronomy", "revisar", "Reporte del equipo sin salir", "El mail de los viernes no llegó al equipo."),
    "verificar-leads": ("astronomy", "revisar", "Verificador de leads caído", "El control diario de los leads no terminó."),
    "reels-diarios": ("astronomy", "revisar", "Reels diarios sin publicar", "Hoy no se publicó ningún reel de prueba."),
    "paper-trading": ("cripto", "revisar", "Carpeta de 10.000 frenada", "La carpeta ficticia de la Mac no completó su ciclo."),
    "radar-diario": ("sistema", "revisar", "Radar diario sin actualizar", "El doc del radar de hoy puede estar viejo."),
}


def decidir(tarea, codigo, registros, ultimo_mail, ahora):
    """(mandar, motivo). `registros` = corridas de esta tarea, la actual al final."""
    if codigo == 75:
        return False, "sin red: lo marca el radar"
    if tarea in SIN_MAIL:
        return False, "no pide ninguna decisión: lo marca el radar"
    previas = registros[:-1]
    if tarea not in A_LA_PRIMERA and len(registros) >= 2:
        gap = datetime.fromisoformat(registros[-1]["inicio"]) - datetime.fromisoformat(previas[-1]["inicio"])
        if gap < FRECUENTE and previas[-1]["codigo"] == 0:
            return False, "primera falla de una tarea frecuente: lo marca el radar"
    if ultimo_mail and ahora - ultimo_mail < ENTRE_MAILS:
        return False, f"ya se avisó el {ultimo_mail:%d/%m %H:%M}"
    return True, "avisar"


def _iso(s):
    # correr.sh escribe -0300, que fromisoformat acepta desde Python 3.11.
    return datetime.fromisoformat(s)


def leer_registros(tarea):
    filas = []
    for linea in REGISTRO.read_text().splitlines() if REGISTRO.is_file() else []:
        try:
            r = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if r.get("tarea") == tarea:
            filas.append(r)
    return filas


def leer_estado():
    try:
        return json.loads(ESTADO.read_text())
    except (OSError, json.JSONDecodeError):
        return {}  # Sin estado se avisa de más: mejor que callarse.


def lineas_clave(log, n=6):
    vistas, salida = set(), []
    for l in log.splitlines():
        t = l.strip()
        if re.search(r"FALLA|FALLÓ|!!!|Traceback|Error\b|error:|No pude", t) and t not in vistas:
            vistas.add(t)
            salida.append(t.lstrip("! ")[:200])
    return salida[-n:]


def armar(tarea, codigo, log):
    from execution.mail_format import render

    area, nivel, titulo, significa = TAREAS.get(tarea, ("sistema", "revisar", f"Tarea «{tarea}» con error", "Una tarea programada no terminó bien."))
    cola = "\n".join(log.splitlines()[-10:])
    return render(
        area=area, nivel=nivel, titulo=titulo, resumen=significa,
        accion=f"Abrí una sesión de Claude y escribí «falló {tarea}». Se revisa y se arregla ahí.",
        secciones=[("Qué se vio", lineas_clave(log))],
        detalle=cola or None,  # Sin log no hay detalle: un «código 1» solo no le dice nada a Facu.
        origen="tareas programadas de la Mac",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tarea", required=True)
    ap.add_argument("--codigo", type=int, required=True)
    ap.add_argument("log", nargs="?")
    a = ap.parse_args()

    ahora = datetime.now().astimezone()
    estado = leer_estado()
    previo = estado.get(a.tarea)
    mandar, motivo = decidir(a.tarea, a.codigo, leer_registros(a.tarea), _iso(previo) if previo else None, ahora)
    if not mandar:
        print(f"sin mail ({motivo})")
        return

    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")
    from execution.google_auth import gmail

    log = pathlib.Path(a.log).read_text(errors="replace")[-6000:] if a.log and pathlib.Path(a.log).is_file() else ""
    para = os.environ["MAIL_FACU"]
    m = armar(a.tarea, a.codigo, log).mime(para)
    gmail().users().messages().send(
        userId="me", body={"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}).execute()
    estado[a.tarea] = ahora.isoformat()
    ESTADO.write_text(json.dumps(estado, indent=1))
    print(f"aviso mandado a {para}")


if __name__ == "__main__":
    main()
