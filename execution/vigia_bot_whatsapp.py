"""Vigía del bot de WhatsApp de Astronomy: avisa a Facu por Telegram si el número se desconecta.

18/11/2026: WhatsApp desvinculó al bot a las 17:56 («device_removed») y nadie se enteró hasta que
fallaron los recordatorios de las 18:00 (4 alumnos sin aviso, que ya no reciben mail). El bot no
puede avisar de su propia caída por WhatsApp, así que el aviso sale de la Mac, por Telegram (el
token queda acá: el servidor lo comparten Vlado y Mateo).

Cada 10 minutos (launchd, `com.facu.vigia-bot-whatsapp`): pregunta por SSH el estado de la
instancia `astronomy_01` en Evolution.
  - Pasa a caído → aviso inmediato. Mientras siga caído, un recordatorio cada 2 horas.
  - Vuelve → aviso de que volvió y cuánto estuvo caído.
  - El servidor no responde dos veces seguidas → aviso (una sola falla suele ser la red de la Mac).
Si la Mac está apagada no avisa nada: eso lo marca el radar (tareas.jsonl, vía correr.sh).

    .venv/bin/python execution/vigia_bot_whatsapp.py            # chequea y avisa
    .venv/bin/python execution/vigia_bot_whatsapp.py --probar   # muestra el estado, sin avisar
"""
import argparse
import json
import os
import pathlib
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESTADO = RAIZ / "data/logs/vigia-bot-whatsapp.json"
RECORDAR_CADA = timedelta(hours=2)
COMANDO = ("cd /opt/astronomy && K=$(grep '^EVOLUTION_API_KEY=' .env | cut -d= -f2-) && "
           "docker compose exec -T n8n wget -q -O- --header=\"apikey: $K\" "
           "http://evolution_api:8080/instance/connectionState/astronomy_01 </dev/null")


def estado_instancia():
    """'open' | 'close' | 'connecting' | ... ; None si el servidor no respondió."""
    try:
        r = subprocess.run(["ssh", "-o", "ConnectTimeout=20", "-o", "BatchMode=yes", "astro-bot", COMANDO],
                           capture_output=True, text=True, timeout=90)
        return json.loads(r.stdout)["instance"]["state"]
    except Exception as e:
        print(f"sin respuesta del servidor: {e!r}")
        return None


def telegram(texto):
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("!!! falta TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID en .env")
        return False
    datos = urllib.parse.urlencode({"chat_id": chat, "text": texto}).encode()
    try:
        with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=datos, timeout=30) as r:
            return bool(json.load(r).get("ok"))
    except Exception as e:
        print(f"!!! No pude avisar por Telegram: {e!r}")
        return False


def decidir(prev, estado, ahora):
    """(nuevo_estado_guardado, texto_a_mandar | None). Pura, para poder probarla."""
    prev = prev or {}
    caido_desde = prev.get("caido_desde")
    ultimo_aviso = prev.get("ultimo_aviso")
    sin_respuesta = prev.get("sin_respuesta", 0)

    if estado is None:
        sin_respuesta += 1
        nuevo = {**prev, "sin_respuesta": sin_respuesta}
        if sin_respuesta == 2:
            return nuevo, ("🟠 No puedo chequear el bot de WhatsApp: el servidor de Astronomy no responde "
                           "(dos intentos seguidos). Puede ser la red de la Mac o el servidor.")
        return nuevo, None

    if estado == "open":
        nuevo = {"estado": "open", "sin_respuesta": 0}
        if caido_desde:
            mins = int((ahora - datetime.fromisoformat(caido_desde)).total_seconds() // 60)
            return nuevo, f"✅ El WhatsApp del bot de Astronomy volvió a estar conectado (estuvo caído ~{mins} min)."
        return nuevo, None

    # caído
    texto_caido = (f"🔴 El WhatsApp del bot de Astronomy está DESCONECTADO (estado: {estado}).\n\n"
                   "Nadie que escriba al 11 2400-5565 recibe respuesta, y no salen los recordatorios de clase.\n\n"
                   "Para reconectar: abrí Claude y decí «reconectar el bot», con el teléfono de Astronomy en mano.")
    if not caido_desde:
        return {"estado": estado, "caido_desde": ahora.isoformat(), "ultimo_aviso": ahora.isoformat(), "sin_respuesta": 0}, texto_caido
    if not ultimo_aviso or ahora - datetime.fromisoformat(ultimo_aviso) >= RECORDAR_CADA:
        mins = int((ahora - datetime.fromisoformat(caido_desde)).total_seconds() // 60)
        return ({**prev, "estado": estado, "ultimo_aviso": ahora.isoformat(), "sin_respuesta": 0},
                f"{texto_caido}\n\n(Sigue caído hace {mins} min.)")
    return {**prev, "estado": estado, "sin_respuesta": 0}, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probar", action="store_true", help="muestra el estado sin avisar ni guardar")
    a = ap.parse_args()
    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")

    estado = estado_instancia()
    prev = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    nuevo, texto = decidir(prev, estado, datetime.now())
    print(f"{datetime.now():%d/%m %H:%M} estado={estado} aviso={'sí' if texto else 'no'}")
    if a.probar:
        print(texto or "(sin aviso)")
        return
    if texto and not telegram(texto):
        nuevo.pop("ultimo_aviso", None)  # no se perdió: se reintenta en la próxima corrida
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(nuevo))
    if estado is None and nuevo.get("sin_respuesta", 0) >= 2:
        raise SystemExit(75)  # correr.sh lo registra como «sin red»


if __name__ == "__main__":
    main()
