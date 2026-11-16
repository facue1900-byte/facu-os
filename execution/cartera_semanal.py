#!/usr/bin/env python3
"""Guardián de la cartera personal de Facu: una vez por semana mira las posiciones contra SUS
reglas y le manda por Telegram qué se salió del plan y qué noticias pegan en lo que tiene.

Por qué existe (11/11/2026): un reel (Alex Ruiz, "3 agentes de IA para trading") vendía agentes
que te frenan cuando operás fuera de tu plan. Para una cartera de largo plazo lo único que sirve de
eso es: reglas escritas una vez + alguien que avise cuando la cartera se sale de ellas.

Reglas de diseño:
- NUNCA opera ni toca el broker. Avisa; la decisión es de Facu.
- Una sola fuente de verdad: las cantidades y las reglas salen de ~/Desktop/Facu/INVERSIONES_Facu.md
  (tabla «CARTERA ACTUAL» y bloque ```reglas). Este script no guarda posiciones propias.
- Los números se calculan acá en Python. Claude sólo resume noticias y no inventa cifras.
- Si un precio no baja, el total NO se informa (regla 2): se dice qué ticker falló.
- Si la tabla tiene más de 30 días, lo dice arriba de todo: un reporte sobre posiciones viejas miente.
- Cartera PERSONAL: no se mezcla con Astronomy, Paseo ni campos, ni con lo cripto.

Correr:  .venv/bin/python execution/cartera_semanal.py            (imprime, no manda)
         .venv/bin/python execution/cartera_semanal.py --send     (además lo manda por Telegram)
         .venv/bin/python execution/cartera_semanal.py --sin-resumen   (sin llamar a Claude)
"""
import argparse
import datetime as dt
import html
import json
import os
import pathlib
import re
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOC = pathlib.Path.home() / "Desktop/Facu/INVERSIONES_Facu.md"
CARPETA_REPORTES = pathlib.Path.home() / "Desktop/Facu/Inversiones"
ESTADO = RAIZ / "data/cartera_semanal_estado.json"   # sólo la foto anterior, para detectar compras
CLAUDE = pathlib.Path.home() / ".local/node/bin/claude"
UA = {"User-Agent": "Mozilla/5.0"}
EFECTIVO = {"DIDI"}          # money market: vale US$1, no se cotiza
YAHOO = {"BRK.B": "BRK-B"}   # tickers que Yahoo escribe distinto
DIAS_VIEJA = 30


def usd(x):
    return "US$" + f"{x:,.0f}".replace(",", ".")


def pc(x, signo=False):
    return (f"{x:+.1f}" if signo else f"{x:.1f}").replace(".", ",") + "%"


def cargar_env():
    try:
        from dotenv import load_dotenv
        load_dotenv(RAIZ / ".env")
    except ImportError:
        pass


# ---------- lectura del doc ----------

def _num(s):
    """'4.430' -> 4430 ; '869,105' -> 869.105 (formato argentino)."""
    s = s.replace("$", "").replace("*", "").strip()
    return float(s.replace(".", "").replace(",", "."))


def leer_posiciones(texto):
    """Filas de la tabla bajo '## CARTERA ACTUAL': {ticker: cantidad}."""
    m = re.search(r"^## CARTERA ACTUAL.*?$(.*?)(?=^## |\Z)", texto, re.S | re.M)
    if not m:
        raise SystemExit("No encontré la sección «## CARTERA ACTUAL» en el doc.")
    filas = [l for l in m.group(1).splitlines() if l.startswith("|")]
    cab = [c.strip() for c in filas[0].strip("|").split("|")]
    i_t, i_c = cab.index("Ticker"), cab.index("Cant.")
    pos = {}
    for l in filas[2:]:
        celdas = [c.strip() for c in l.strip("|").split("|")]
        if len(celdas) > max(i_t, i_c) and celdas[i_t]:
            pos[celdas[i_t].replace("*", "")] = _num(celdas[i_c])
    if not pos:
        raise SystemExit("La tabla de CARTERA ACTUAL vino vacía: no sigo (regla 2).")
    return pos


def fecha_tabla(texto):
    m = re.search(r"Última actualización: \*\*(\d{1,2}) (\w{3})\w* (\d{4})\*\*", texto)
    meses = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7,
             "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
    if not m or m.group(2).lower() not in meses:
        return None
    return dt.date(int(m.group(3)), meses[m.group(2).lower()], int(m.group(1)))


def leer_reglas(texto):
    m = re.search(r"```reglas\n(.*?)```", texto, re.S)
    if not m:
        raise SystemExit("No encontré el bloque ```reglas en el doc.")
    r = {}
    for l in m.group(1).splitlines():
        l = l.split("#")[0].strip()
        if ":" in l:
            k, v = (x.strip() for x in l.split(":", 1))
            r[k] = [t.strip().upper() for t in v.split(",") if t.strip()] if "," in v or k.startswith("lista_") else float(v)
    return r


# ---------- datos de afuera ----------

def precio(ticker):
    """(último, cierre de hace ~5 ruedas) desde Yahoo. None si falla."""
    t = YAHOO.get(ticker, ticker)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?range=1mo&interval=1d"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            res = json.load(r)["chart"]["result"][0]
        cierres = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
        ultimo = res["meta"]["regularMarketPrice"]
        hace_5 = cierres[-6] if len(cierres) >= 6 else cierres[0]
        return float(ultimo), float(hace_5)
    except Exception as e:
        print(f"!!! precio de {ticker} falló: {e!r}")
        return None


def noticias(ticker, dias=7, n=4):
    t = YAHOO.get(ticker, ticker)
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={urllib.parse.quote(t)}&region=US&lang=en-US"
    desde = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=dias)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            raiz = ET.fromstring(r.read())
    except Exception as e:
        print(f"!!! noticias de {ticker} fallaron: {e!r}")
        return []
    out = []
    for it in raiz.iter("item"):
        try:
            if parsedate_to_datetime(it.findtext("pubDate")) < desde:
                continue
        except Exception:
            pass
        out.append(it.findtext("title", "").strip())
        if len(out) >= n:
            break
    return out


def ultimo_reporte_one618():
    archivos = sorted(CARPETA_REPORTES.glob("Visión de Mercado*.html"), key=lambda p: p.stat().st_mtime)
    if not archivos:
        return None, None, ""
    p = archivos[-1]
    txt = re.sub(r"<(script|style).*?</\1>", " ", p.read_text(errors="ignore"), flags=re.S)
    txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt))).strip()
    return p.name, dt.date.fromtimestamp(p.stat().st_mtime), txt[:12000]


# ---------- el análisis ----------

def analizar(pos, reglas, anterior):
    filas, faltan = [], []
    for t, cant in pos.items():
        if t in EFECTIVO:
            filas.append({"t": t, "cant": cant, "px": 1.0, "sem": 0.0, "valor": cant})
            continue
        p = precio(t)
        if p is None:
            faltan.append(t)
            continue
        filas.append({"t": t, "cant": cant, "px": p[0], "sem": (p[0] / p[1] - 1) * 100, "valor": cant * p[0]})
    total = sum(f["valor"] for f in filas)
    for f in filas:
        f["pct"] = f["valor"] / total * 100 if total else 0
    filas.sort(key=lambda f: -f["valor"])

    alertas = []
    if faltan:
        alertas.append(f"⚠️ No bajó el precio de {', '.join(faltan)}: los % de abajo NO cuentan esos papeles y el total está incompleto.")
    tope = reglas.get("tope_por_papel")
    for f in filas:
        if tope and f["t"] not in EFECTIVO and f["pct"] > tope:
            alertas.append(f"🔴 {f['t']} pesa {pc(f['pct'])} (tu tope: {tope:.0f}%).")
    top3 = sum(f["pct"] for f in [x for x in filas if x["t"] not in EFECTIVO][:3])
    if reglas.get("tope_top3") and top3 > reglas["tope_top3"]:
        nombres = "+".join(f["t"] for f in [x for x in filas if x["t"] not in EFECTIVO][:3])
        alertas.append(f"🔴 Los 3 más grandes ({nombres}) son el {pc(top3)} (tu tope: {reglas['tope_top3']:.0f}%).")
    semis = sum(f["pct"] for f in filas if f["t"] in reglas.get("lista_semis", []))
    if reglas.get("tope_semis") and semis > reglas["tope_semis"]:
        alertas.append(f"🟠 Chips: {pc(semis)} (tu tope: {reglas['tope_semis']:.0f}%).")
    efec = sum(f["pct"] for f in filas if f["t"] in EFECTIVO)
    if reglas.get("min_efectivo") and efec < reglas["min_efectivo"]:
        alertas.append(f"🟠 Efectivo: {pc(efec)} (tu mínimo: {reglas['min_efectivo']:.0f}%).")
    afuera = sum(f["pct"] for f in filas if f["t"] in reglas.get("lista_fuera_eeuu", []))
    if reglas.get("min_fuera_eeuu") and afuera < reglas["min_fuera_eeuu"]:
        alertas.append(f"🟠 Fuera de EE.UU.: {pc(afuera)} (tu mínimo: {reglas['min_fuera_eeuu']:.0f}%).")
    caida = reglas.get("alerta_caida_semanal")
    for f in filas:
        if caida and f["t"] not in EFECTIVO and f["sem"] <= -caida:
            alertas.append(f"📉 {f['t']} cayó {pc(f['sem'])} en la semana.")
    prohibidos = set(reglas.get("lista_no_comprar_mas", []))
    for t, cant in pos.items():
        if t in prohibidos and t in anterior and cant > anterior[t]:
            alertas.append(f"🔴 Subió la cantidad de {t} ({anterior[t]:g} → {cant:g}) y está en tu lista de «no comprar más».")
    nuevos = [t for t in pos if anterior and t not in anterior and t not in EFECTIVO]
    if nuevos and reglas.get("sin_nombres_nuevos"):
        alertas.append(f"🟠 Papeles nuevos desde la última vez: {', '.join(nuevos)}. Tu regla: ni un nombre individual más, sólo ETFs.")
    return filas, total, faltan, alertas, {"top3": top3, "semis": semis, "efectivo": efec, "afuera": afuera}


def resumen_claude(filas, notis, rep_nombre, rep_texto):
    tenencia = ", ".join(f"{f['t']} {f['pct']:.0f}%" for f in filas if f["t"] not in EFECTIVO)
    bloque_n = "\n".join(f"{t}: " + " | ".join(n) for t, n in notis.items() if n) or "(sin noticias)"
    prompt = (
        "Sos el analista de la cartera personal de largo plazo de Facu (argentino; hablale en rioplatense, con voseo). "
        f"Su cartera hoy: {tenencia}.\n\nTitulares de la última semana por papel:\n{bloque_n}\n\n"
        + (f"Último reporte de su asesor ({rep_nombre}):\n{rep_texto}\n\n" if rep_texto else "")
        + "Escribí como máximo 10 líneas, texto plano sin markdown:\n"
        "1) Las 2-4 noticias que de verdad pueden mover SUS papeles y para qué lado, con el ticker adelante.\n"
        "2) Si algo del reporte del asesor choca con lo que tiene, en una línea.\n"
        "No inventes cifras ni precios que no estén arriba. No le digas qué comprar o vender: "
        "eso lo decide él contra sus reglas. Si los titulares no dicen nada importante, decilo en una línea."
    )
    try:
        r = subprocess.run([str(CLAUDE), "-p", prompt, "--model", "sonnet", "--tools", "",
                            "--permission-mode", "dontAsk"],
                           capture_output=True, text=True, timeout=240, cwd="/tmp",
                           # Entorno mínimo (sin el token de Telegram), pero con USER: sin él no encuentra el login.
                           env={"PATH": "/usr/bin:/bin:" + str(CLAUDE.parent), "HOME": str(pathlib.Path.home()),
                                "USER": os.environ.get("USER", "Facu"), "LANG": "es_AR.UTF-8"})
        salida = r.stdout.strip()
        if r.returncode != 0 or not salida:
            return f"(No salió el resumen de noticias: código {r.returncode}. {r.stderr.strip()[:200]})"
        return salida
    except Exception as e:
        return f"(No salió el resumen de noticias: {e!r})"


def armar(texto_doc, con_resumen=True):
    pos, reglas = leer_posiciones(texto_doc), leer_reglas(texto_doc)
    anterior = json.loads(ESTADO.read_text()).get("posiciones", {}) if ESTADO.exists() else {}
    filas, total, faltan, alertas, agg = analizar(pos, reglas, anterior)
    hoy = dt.date.today()
    fecha = fecha_tabla(texto_doc)
    rep_nombre, rep_fecha, rep_texto = ultimo_reporte_one618()

    L = [f"📊 Tu cartera — semana del {hoy:%d/%m/%Y}", ""]
    if fecha is None or (hoy - fecha).days > DIAS_VIEJA:
        cuando = f"del {fecha:%d/%m}" if fecha else "sin fecha"
        L += [f"⚠️ Las cantidades son {cuando}: si operaste después, esto está mal. Pasame el broker y lo actualizo.", ""]
    L.append(("Total aprox." if faltan else "Total") + f": {usd(total)} (precios de Yahoo, no del broker)")
    for f in filas:
        sem = "" if f["t"] in EFECTIVO else f" · {pc(f['sem'], True)} en la semana"
        L.append(f"· {f['t']} {pc(f['pct'])} — {usd(f['valor'])}{sem}")
    L += ["", "Contra tus reglas:"] + (alertas or ["✅ Todo dentro del plan."])
    notis = {}
    if con_resumen:
        notis = {f["t"]: noticias(f["t"]) for f in filas if f["t"] not in EFECTIVO}
        L += ["", "Lo que pasó en la semana (titulares de Yahoo, resumidos por Claude):", resumen_claude(filas, notis, rep_nombre, rep_texto)]
    if rep_fecha and (hoy - rep_fecha).days > 14:
        L += ["", f"ℹ️ El último reporte de one618 que tengo es del {rep_fecha:%d/%m}. Si te llegó uno nuevo, guardalo en Desktop/Facu/Inversiones."]
    L += ["", "No opero nada: avisar y decidir es tuyo."]
    return "\n".join(L), pos


def mandar_telegram(texto):
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("!!! Falta TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en .env")
        return False
    datos = urllib.parse.urlencode({"chat_id": chat, "text": texto[:4000]}).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=datos, timeout=30) as r:
        return bool(json.load(r).get("ok"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="mandarlo por Telegram (apagado por defecto)")
    ap.add_argument("--sin-resumen", action="store_true", help="sin noticias ni Claude")
    a = ap.parse_args()
    cargar_env()
    texto, pos = armar(DOC.read_text(), con_resumen=not a.sin_resumen)
    print(texto)
    if a.send:
        ok = mandar_telegram(texto)
        print("\n→ Telegram:", "enviado" if ok else "NO SALIÓ")
        if not ok:
            raise SystemExit(1)
        ESTADO.parent.mkdir(exist_ok=True)
        ESTADO.write_text(json.dumps({"fecha": dt.date.today().isoformat(), "posiciones": pos}, indent=1))


if __name__ == "__main__":
    main()
