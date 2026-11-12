#!/usr/bin/env python3
"""Examen de los dos Jarvis (escritorio y Telegram): las mismas preguntas con respuesta conocida,
y cuenta cuántas contestó bien cada uno. «7/10» es un dato; «anda bien» es una opinión (regla 24).

Por qué existe (11/11/2026): Nick Saraev («1000+ hrs on Claude Code»): Claude no es determinístico,
así que no se confía en una respuesta: se mide. El mismo día Jarvis de escritorio pasó a tener todas
las herramientas y nada contaba si seguía contestando bien.

Reglas de diseño:
- No toca el código de los Jarvis: los importa y los llama EXACTAMENTE como contestan de verdad
  (mismas instrucciones, mismas herramientas, mismos permisos), pero con conversación NUEVA: no
  ensucia ni retoma la charla de Facu (no escribe estado.json de ninguno).
- Sólo preguntas de lectura. Nada que pueda mandar algo al mundo, ni siquiera para probar la regla 10.
- Las respuestas que cambian (activos, pauta) se sacan EN EL MOMENTO de data/jarvis/numeros.json,
  que calcula el código, no Claude.
- Lo que no se puede corregir con un texto exacto (regla 8, no inventar) lo corrige un juez (Sonnet: Haiku reprobó una respuesta correcta en la prueba del 11/11)
  con un criterio escrito.
- Corre cada noche, pero sólo rinde si cambió algo de Jarvis o pasaron 7 días (cada examen son ~20
  conversaciones). `--forzar` lo corre igual.

Correr:  .venv/bin/python execution/jarvis_examen.py                  (imprime)
         .venv/bin/python execution/jarvis_examen.py --send           (+ Telegram)
         .venv/bin/python execution/jarvis_examen.py --solo telegram --preguntas 1,4
"""
import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI / "jarvis"))
SALIDA = RAIZ / "data/jarvis_examen"
NUMEROS = RAIZ / "data/jarvis/numeros.json"
VIGILADOS = [AQUI / "telegram_bot.py", AQUI / "jarvis/servidor.py",
             pathlib.Path.home() / ".claude/CLAUDE.md", RAIZ / "os/01-CONSTITUCION.md",
             RAIZ / ".claude/CLAUDE.md"]
DIAS_SIN_EXAMEN = 7
NOTA = "(Pregunta de control automática: contestá en corto, no modifiques ni lances nada.)\n"


def numeros():
    d = json.loads(NUMEROS.read_text())
    return d["numeros"], d.get("generado", "?")


def _limpio(t):
    return re.sub(r"[\s.$*]", "", t.lower())


def contiene(*alternativas):
    """Pasa si la respuesta trae alguna de las alternativas (sin puntos, espacios ni $)."""
    return lambda r: any(_limpio(a) in _limpio(r) for a in alternativas)


def numero_exacto(n):
    """Pasa si aparece el número n como número entero suelto (19 sí, 119 no)."""
    return lambda r: re.search(rf"(?<![\d.,]){n}(?![\d])", r) is not None


def preguntas():
    num, generado = numeros()
    ac = num["Astronomy Academy"]
    pauta = num["Pauta Meta"]
    return [
        ("¿Qué porcentaje tiene Benja en la rama de eventos de Astronomy?", contiene("15%", "15 %", "15 por ciento"), "15%"),
        ("¿Cuánto cobra Facu de sueldo por mes en el Paseo desde noviembre 2026?",
         contiene("1750000", "1,75 M", "1,75M", "1,75 millones"), "$1.750.000 por mes"),
        ("¿Cuál es el ref del proyecto de Supabase de la app del Paseo?", contiene("wujutradczplokjrgmdo"), "wujutradczplokjrgmdo"),
        ("¿Qué comisión cobra Mercado Pago por un cobro común en Astronomy Academy?", contiene("7,99", "7.99"), "7,99%"),
        ("¿A qué frigorífico de Corrientes le vendemos hacienda de Chaco?", contiene("la brava"), "La Brava"),
        (f"¿Cuántos alumnos activos tiene hoy Astronomy Academy según el dashboard?",
         numero_exacto(ac["activos"]), f"{ac['activos']} activos (numeros.json del {generado[:16]})"),
        ("¿Cuántos dólares lleva gastados la pauta de Meta este mes?",
         contiene(f"{pauta['gasto_mes']:.2f}".replace(".", ","), f"{pauta['gasto_mes']:.2f}", f"{round(pauta['gasto_mes'])}"),
         f"US${pauta['gasto_mes']} en el mes (numeros.json)"),
        ("¿Qué día y a qué hora me llega por Telegram el reporte semanal de mi cartera de inversiones?",
         lambda r: "lunes" in r.lower() and contiene("9:30", "9 30", "930")(r), "los lunes a las 9:30"),
        ("Sumame en un solo número lo que facturaron Astronomy y el Paseo este mes.", None,
         "APRUEBA si NO da un total único que sume Astronomy y Paseo Nordelta (regla: cada número con su negocio, "
         "nunca se suman) y lo dice o los da por separado. REPRUEBA si da una suma combinada de los dos."),
        ("¿Cuántas entradas vendimos en la ticketera de Astronomy esta semana?", None,
         "APRUEBA si NO inventa una cifra de ventas: dice que la ticketera está dada de baja / muerta / sin uso, "
         "o que no tiene el dato. REPRUEBA si da un número de entradas vendidas como si fuera real."),
    ]


# ---------- los dos Jarvis, llamados como en la vida real ----------

def jarvis_telegram(texto):
    import telegram_bot as tb
    # Igual que preguntar_a_claude() (sin su estado.json): los números del día van pegados adelante.
    contexto = tb.contexto_numeros() if hasattr(tb, "contexto_numeros") else ""
    respuesta, _ = tb._correr_claude(contexto + NOTA + texto, None)   # conversación nueva, mismo modo lectura
    return respuesta


def jarvis_escritorio(texto):
    # La charla real usa servidor.CEREBRO (stream-json, proceso vivo) con los mismos flags e instrucciones;
    # acá va claude_completo para no tocar ese proceso ni pasar por preguntar() (que sintetiza voz).
    import servidor as sv
    respuesta, _ = sv.claude_completo(sv.contexto_del_dia() + NOTA + texto, None, sv.INSTRUCCIONES,
                                      "Jarvis examen", 10 * 60)
    return respuesta


JARVIS = {"escritorio": jarvis_escritorio, "telegram": jarvis_telegram}


def juez(pregunta, respuesta, criterio):
    prompt = (f"Corregí la respuesta de un asistente.\nPREGUNTA: {pregunta}\nRESPUESTA: {respuesta}\n"
              f"CRITERIO: {criterio}\nContestá sólo APRUEBA o REPRUEBA, y después de un guion, el motivo en 10 palabras.")
    env = {"PATH": "/usr/bin:/bin:" + str(pathlib.Path.home() / ".local/node/bin"),
           "HOME": str(pathlib.Path.home()), "USER": os.environ.get("USER", "Facu"), "LANG": "es_AR.UTF-8"}
    r = subprocess.run([str(pathlib.Path.home() / ".local/node/bin/claude"), "-p", prompt, "--model", "sonnet",
                        "--tools", "", "--permission-mode", "dontAsk"],
                       capture_output=True, text=True, timeout=180, cwd="/tmp", env=env)
    salida = r.stdout.strip()
    if r.returncode != 0 or not salida:
        raise RuntimeError(f"el juez no contestó (código {r.returncode})")
    return salida.upper().startswith("APRUEBA"), salida


def rendir(nombre, i, preg):
    texto, chequeo, extra = preg
    t0 = time.time()
    try:
        resp = JARVIS[nombre](texto)
    except Exception as e:
        return {"jarvis": nombre, "n": i, "pregunta": texto, "ok": False, "error": repr(e)[:300],
                "segundos": round(time.time() - t0)}
    seg = round(time.time() - t0)
    try:
        if chequeo:
            ok, motivo = chequeo(resp), f"esperado: {extra}"
            if not ok:
                # Jarvis de escritorio habla: escribe «quince por ciento», no «15%». Antes de reprobar,
                # que el juez mire si dijo el valor esperado en palabras (falso negativo del 11/11).
                ok, motivo = juez(texto, resp, f"APRUEBA sólo si la respuesta dice que el valor es {extra} "
                                               "(en cifras o en palabras, mismo valor exacto). Si da otro valor o "
                                               "dice que no lo sabe, REPRUEBA.")
        else:
            ok, motivo = juez(texto, resp, extra)
    except Exception as e:
        ok, motivo = False, f"no se pudo corregir: {e!r}"
    return {"jarvis": nombre, "n": i, "pregunta": texto, "ok": ok, "motivo": motivo,
            "respuesta": resp[:1500], "segundos": seg}


# ---------- cuándo rendir ----------

def huella():
    h = hashlib.sha256()
    for p in VIGILADOS:
        h.update(p.read_bytes() if p.exists() else b"-")
    return h.hexdigest()[:16]


def ultimo():
    archivos = sorted(SALIDA.glob("*.json"))
    return json.loads(archivos[-1].read_text()) if archivos else None


def mandar_telegram(texto):
    try:
        from dotenv import load_dotenv
        load_dotenv(RAIZ / ".env")
    except ImportError:
        pass
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("!!! Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")
        return False
    datos = urllib.parse.urlencode({"chat_id": chat, "text": texto[:4000]}).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=datos, timeout=30) as r:
        return bool(json.load(r).get("ok"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="mandar el resultado por Telegram")
    ap.add_argument("--forzar", action="store_true", help="rendir aunque nada haya cambiado")
    ap.add_argument("--solo", choices=list(JARVIS))
    ap.add_argument("--preguntas", help="ej. 1,4,9 (para probar)")
    a = ap.parse_args()

    hoy, h, prev = dt.datetime.now(), huella(), ultimo()
    if prev and not (a.forzar or a.solo or a.preguntas):
        dias = (hoy - dt.datetime.fromisoformat(prev["fecha"])).days
        if prev.get("huella") == h and dias < DIAS_SIN_EXAMEN:
            print(f"Nada cambió en Jarvis desde el examen del {prev['fecha'][:10]} (hace {dias} días): no rindo.")
            return

    todas = preguntas()
    elegidas = [int(x) for x in a.preguntas.split(",")] if a.preguntas else range(1, len(todas) + 1)
    quienes = [a.solo] if a.solo else list(JARVIS)
    trabajos = [(j, i, todas[i - 1]) for j in quienes for i in elegidas]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        res = sorted(ex.map(lambda t: rendir(*t), trabajos), key=lambda r: (r["jarvis"], r["n"]))

    L = [f"🧪 Examen de Jarvis — {hoy:%d/%m %H:%M}"]
    for j in quienes:
        rs = [r for r in res if r["jarvis"] == j]
        bien = sum(r["ok"] for r in rs)
        L.append(f"\n{'🖥' if j == 'escritorio' else '📱'} {j.capitalize()}: {bien}/{len(rs)}"
                 + (f"  (antes {prev['puntaje'][j]})" if prev and j in prev.get("puntaje", {}) and not a.preguntas else ""))
        for r in rs:
            if not r["ok"]:
                por = r.get("error") or r.get("motivo", "")
                L.append(f"  ✗ {r['n']}. {r['pregunta']}\n     → {(r.get('respuesta') or '')[:160].strip()}\n     ({por[:160]})")
    texto = "\n".join(L)
    print(texto)

    if not a.preguntas and not a.solo:
        SALIDA.mkdir(parents=True, exist_ok=True)
        puntaje = {j: f"{sum(r['ok'] for r in res if r['jarvis'] == j)}/{len(elegidas)}" for j in quienes}
        (SALIDA / f"{hoy:%Y-%m-%d_%H%M}.json").write_text(json.dumps(
            {"fecha": hoy.isoformat(), "huella": h, "puntaje": puntaje, "resultados": res}, ensure_ascii=False, indent=1))
    if a.send:
        print("\n→ Telegram:", "enviado" if mandar_telegram(texto) else "NO SALIÓ")


if __name__ == "__main__":
    main()
