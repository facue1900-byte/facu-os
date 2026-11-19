#!/usr/bin/env python3
"""Vigía del bot de WhatsApp de Astronomy, del lado del SERVIDOR (VPS astro-bot, /root/vigia/).

Fuente de verdad: este archivo en facu-os (`execution/vps/vigia_vps.py`). En el servidor se copia
con `scp execution/vps/vigia_vps.py astro-bot:/root/vigia/vigia.py`. Sólo stdlib (python3 del
sistema); cron cada 5 minutos (`crontab -l` de root).

Por qué existe (19/11/2026): el vigía de la Mac (`execution/vigia_bot_whatsapp.py`) no mira nada
cuando la Mac está apagada o sin red — la noche del 18/11 no corrió de 21:18 en adelante. Éste
corre en el mismo servidor del bot, 24/7.

Qué chequea:
  1. `conexion`: el estado de la instancia `astronomy_01` en Evolution ≠ open.
  2. `sordo`: conectado pero ningún mensaje ENTRANTE (no grupos) guardado en la base `evolution`
     durante SORDO_HORAS horas «de día» (sólo cuentan las horas entre 10 y 22, hora AR). Con la
     pauta apagada hay días de 1–3 mensajes, así que 10 h de día ≈ una jornada entera sin que
     escriba nadie: puede ser silencio real, por eso el aviso pide mandar un «hola» de prueba.
     Sólo avisa entre 10 y 22 h.
  3. `contenedores`: alguno de los 5 contenedores del compose no está corriendo.
Cada problema avisa UNA vez al empezar y una vez al resolverse (archivo de estado).

Cómo avisa:
  - Si existe /root/vigia/telegram.env (TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID de un bot de
    Telegram SÓLO para alertas), manda directo.
  - Si no, encola el aviso en /root/vigia/pendientes.jsonl y el vigía de la Mac lo retransmite
    con el bot de Jarvis la próxima vez que corre. El token de Jarvis NO va a este servidor:
    Vlado y Mateo tienen root acá, y con ese token se pueden leer (y robar, por getUpdates) los
    mensajes que Facu le manda a Jarvis.

    python3 /root/vigia/vigia.py                 # chequea y avisa (lo corre el cron)
    python3 /root/vigia/vigia.py --probar        # muestra qué avisaría, sin mandar ni guardar
    python3 /root/vigia/vigia.py --forzar sordo  # simula una condición (con --probar: dry-run)
    python3 /root/vigia/vigia.py --pendientes    # imprime y vacía la cola (lo usa la Mac)
    python3 /root/vigia/vigia.py --encolar "txt" # encola un aviso a mano (prueba de punta a punta)
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

DIR = "/root/vigia"
ESTADO = f"{DIR}/estado.json"
COLA = f"{DIR}/pendientes.jsonl"
TG_ENV = f"{DIR}/telegram.env"
LOG = f"{DIR}/vigia.log"
COMPOSE = "/opt/astronomy"
CONTENEDORES = ["astronomy-caddy-1", "astronomy-evolution_api-1", "astronomy-n8n-1",
                "astronomy-postgres-1", "astronomy-redis-1"]
SORDO_HORAS = 10.0
DIA_DESDE, DIA_HASTA = 10, 22
AR = timezone(timedelta(hours=-3))


def sh(cmd, timeout=60):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip()


def estado_conexion():
    cmd = (f"cd {COMPOSE} && K=$(grep '^EVOLUTION_API_KEY=' .env | cut -d= -f2-) && "
           "docker compose exec -T n8n wget -q -O- --header=\"apikey: $K\" "
           "http://evolution_api:8080/instance/connectionState/astronomy_01 </dev/null")
    try:
        _, out = sh(cmd)
        return json.loads(out)["instance"]["state"]
    except Exception:
        return None  # Evolution no contesta: lo marca el chequeo de contenedores o sale como caído


def ultimo_entrante():
    q = ("select max(\"messageTimestamp\") from \"Message\" where coalesce((key->>'fromMe')::boolean,false)=false "
         "and key->>'remoteJid' not like '%@g.us' and key->>'remoteJid' <> 'status@broadcast';")
    rc, out = sh(f"docker exec -i astronomy-postgres-1 psql -U astronomy -d evolution -At -c \"{q.replace(chr(34), chr(92)+chr(34))}\"")
    if rc != 0 or not out:
        return None
    return datetime.fromtimestamp(int(out), AR)


def horas_de_dia(desde, hasta):
    """Horas entre `desde` y `hasta` que caen dentro de 10–22 h AR."""
    total, d = 0.0, desde.astimezone(AR)
    hasta = hasta.astimezone(AR)
    while d < hasta:
        ini = d.replace(hour=DIA_DESDE, minute=0, second=0, microsecond=0)
        fin = d.replace(hour=DIA_HASTA, minute=0, second=0, microsecond=0)
        a, b = max(d, ini), min(hasta, fin)
        if b > a:
            total += (b - a).total_seconds() / 3600
        d = (d + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return total


def contenedores_caidos():
    rc, out = sh("docker ps --format '{{.Names}}'")
    if rc != 0:
        return ["docker no responde"]
    vivos = set(out.split())
    return [c for c in CONTENEDORES if c not in vivos]


def chequear(ahora, forzar=None):
    """{problema: detalle | None}. `forzar` simula una condición para probar los avisos."""
    caidos = contenedores_caidos()
    conn = estado_conexion()
    ult = ultimo_entrante()
    p = {"contenedores": None, "conexion": None, "sordo": None}
    if caidos or forzar == "contenedores":
        p["contenedores"] = ", ".join(caidos or ["astronomy-n8n-1 (simulado)"])
    if conn != "open" or forzar == "conexion":
        p["conexion"] = (conn or "sin respuesta de Evolution") + (" (simulado)" if forzar == "conexion" else "")
    elif ult is not None or forzar == "sordo":
        h = horas_de_dia(ult, ahora) if ult else 0
        es_de_dia = DIA_DESDE <= ahora.astimezone(AR).hour < DIA_HASTA
        if forzar == "sordo" or (h >= SORDO_HORAS and es_de_dia):
            p["sordo"] = f"último mensaje entrante: {ult:%d/%m %H:%M}" if ult else "sin dato (simulado)"
    return p, conn, ult


TEXTOS = {
    "contenedores": ("🔴 Servidor del bot de Astronomy: contenedores caídos ({d}). El bot no contesta. "
                     "Abrí Claude y decí «el servidor del bot se cayó».",
                     "✅ Servidor del bot: los contenedores volvieron."),
    "conexion": ("🔴 El WhatsApp del bot de Astronomy está DESCONECTADO (estado: {d}). Nadie que escriba al "
                 "11 2400-5565 recibe respuesta. Abrí Claude y decí «reconectar el bot», con el teléfono de "
                 "Astronomy en mano.",
                 "✅ El WhatsApp del bot de Astronomy volvió a estar conectado."),
    "sordo": ("🟠 El bot de Astronomy figura conectado pero no le entra ningún mensaje hace más de "
              f"{SORDO_HORAS:.0f} h de día ({{d}}). Puede ser que no escribió nadie, o que está sordo: mandale "
              "un «hola» desde tu celular al 11 2400-5565 y fijate si llega.",
              "✅ Al bot de Astronomy le volvieron a entrar mensajes."),
}


def decidir(prev, problemas, ahora):
    """(nuevo_estado, [textos]). Un aviso al empezar cada problema y uno al resolverse."""
    nuevo, textos = {}, []
    for k, det in problemas.items():
        antes = prev.get(k)
        if det and not antes:
            textos.append(TEXTOS[k][0].format(d=det))
            nuevo[k] = ahora.isoformat()
        elif det:
            nuevo[k] = antes
        elif antes:
            mins = int((ahora - datetime.fromisoformat(antes)).total_seconds() // 60)
            textos.append(f"{TEXTOS[k][1]} (duró ~{mins} min)")
    return nuevo, textos


def leer_tg():
    if not os.path.exists(TG_ENV):
        return None
    env = dict(l.strip().split("=", 1) for l in open(TG_ENV) if "=" in l and not l.startswith("#"))
    return env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")


def entregar(texto):
    """Telegram directo si hay bot de alertas; si no, a la cola para la Mac. True si quedó entregado o encolado."""
    tg = leer_tg()
    if tg and all(tg):
        datos = urllib.parse.urlencode({"chat_id": tg[1], "text": texto}).encode()
        try:
            with urllib.request.urlopen(f"https://api.telegram.org/bot{tg[0]}/sendMessage", data=datos, timeout=30) as r:
                if json.load(r).get("ok"):
                    return True
        except Exception as e:
            log(f"telegram falló: {e!r}; va a la cola")
    with open(COLA, "a") as f:
        f.write(json.dumps({"t": datetime.now(AR).isoformat(), "texto": texto}, ensure_ascii=False) + "\n")
    os.chmod(COLA, 0o600)
    return True


def log(txt):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now(AR):%d/%m %H:%M} {txt}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probar", action="store_true")
    ap.add_argument("--forzar", choices=["conexion", "sordo", "contenedores"])
    ap.add_argument("--pendientes", action="store_true")
    ap.add_argument("--encolar")
    a = ap.parse_args()
    os.makedirs(DIR, mode=0o700, exist_ok=True)

    if a.pendientes:
        if os.path.exists(COLA):
            os.replace(COLA, COLA + ".enviando")
            sys.stdout.write(open(COLA + ".enviando").read())
            os.remove(COLA + ".enviando")
        return
    if a.encolar:
        entregar(a.encolar)
        return

    ahora = datetime.now(AR)
    problemas, conn, ult = chequear(ahora, a.forzar)
    prev = json.load(open(ESTADO)) if os.path.exists(ESTADO) and not a.forzar else {}
    nuevo, textos = decidir(prev, problemas, ahora)
    linea = (f"conexion={conn} ultimo_entrante={ult:%d/%m %H:%M}" if ult else f"conexion={conn} ultimo_entrante=-")
    linea += f" problemas={[k for k, v in problemas.items() if v]} avisos={len(textos)}"
    if a.probar or a.forzar:
        print(linea)
        for t in textos:
            print("  AVISARÍA:", t)
        if not a.probar:
            print("(--forzar sin --probar tampoco manda ni guarda)")
        return
    for t in textos:
        entregar(t)
    with open(ESTADO, "w") as f:
        json.dump(nuevo, f)
    log(linea)


if __name__ == "__main__":
    main()
