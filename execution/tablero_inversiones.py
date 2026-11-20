"""Datos del Tablero de inversiones de Facu (personal: no se mezcla con los negocios).

Junta, cada 15 minutos (launchd com.facu.tablero-inversiones):
- Acciones: cantidades y costo de la tabla «CARTERA ACTUAL» de ~/Desktop/Facu/INVERSIONES_Facu.md
  (única fuente de posiciones) × precios de Yahoo (intradiario de hoy y diario de 5 años).
- Valor real de la cuenta a fin de mes, leído de NetX: data/inversiones/netx_mensual.json.
- Cripto: el historial de cada carpeta ficticia (ramas claude/cartera-* del repo), la de 10.000
  de la Mac (data/paper/historial.csv) y el ranking del Torneo.

Escribe el JSON en data/inversiones/tablero.json y en la planilla de Drive que lee la página
(columna A de la hoja «datos», en trozos base64). Nunca opera nada.

    .venv/bin/python execution/tablero_inversiones.py            # arma y sube
    .venv/bin/python execution/tablero_inversiones.py --sin-subir # sólo el JSON local
"""
import argparse
import base64
import csv
import datetime as dt
import io
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "execution"))
from cartera_semanal import DOC, YAHOO, UA, leer_posiciones, fecha_tabla, _num  # noqa: E402

SALIDA = RAIZ / "data/inversiones/tablero.json"
NETX = RAIZ / "data/inversiones/netx_mensual.json"
PAPER = RAIZ / "data/paper/historial.csv"
PAPER_GROK = RAIZ / "data/paper-grok/historial.csv"
HOJA_ID = "1zdFhNK1wecyBvJgsc9EGtj6jTKK2GyxvOcXHGreq0pU"  # «Tablero inversiones · datos (no editar)», Drive de facue1900@
EFECTIVO = {"DIDI"}  # money market: vale 1 USD, no tiene precio en Yahoo

CARPETAS = [  # (id, nombre, rama, ruta del historial, qué es)
    ("original", "Original", "claude/cartera-cripto", "execution/cartera/estado/historial.csv",
     "La primera: Claude opera 1.000 USDT ficticios cada 2 h."),
    ("agresiva", "Agresiva", "claude/cartera-agresiva", "execution/cartera/estado-agresiva/historial.csv",
     "Más riesgo y más operaciones, cada hora."),
    ("laboratorio", "Laboratorio", "claude/cartera-laboratorio", "execution/cartera/estado-laboratorio/historial.csv",
     "Pocas entradas, sólo a favor de la tendencia; la ajusta el Entrenador."),
    ("dca", "DCA BTC", "claude/cartera-dca", "execution/cartera/estado-dca/historial.csv",
     "Compra 100 USD de BTC por semana y no vende."),
]


def yahoo(ticker, rango, intervalo):
    t = YAHOO.get(ticker, ticker)
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}"
           f"?range={rango}&interval={intervalo}&includePrePost=false")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        res = json.load(r)["chart"]["result"][0]
    ts = res.get("timestamp") or []
    cierres = res["indicators"]["quote"][0]["close"]
    serie = [(t_, c) for t_, c in zip(ts, cierres) if c is not None]
    return res["meta"], serie


def leer_costos(texto):
    """Costo de cada posición = Valor − Ganancia no realizada, de la tabla del doc."""
    m = re.search(r"^## CARTERA ACTUAL.*?$(.*?)(?=^## |\Z)", texto, re.S | re.M)
    filas = [l for l in m.group(1).splitlines() if l.startswith("|")]
    cab = [c.strip() for c in filas[0].strip("|").split("|")]
    i_t, i_v, i_g, i_n = cab.index("Ticker"), cab.index("Valor"), cab.index("Ganancia no realizada"), cab.index("Nombre")
    costos, nombres = {}, {}
    for l in filas[2:]:
        c = [x.strip() for x in l.strip("|").split("|")]
        t = c[i_t].replace("*", "")
        nombres[t] = c[i_n]
        g = re.match(r"([+−-])\$([\d.,]+)", c[i_g].replace(" ", ""))
        if g and t not in EFECTIVO:
            gan = _num(g.group(2)) * (-1 if g.group(1) in "−-" else 1)
            costos[t] = round(_num(c[i_v]) - gan, 2)
    return costos, nombres


def acciones():
    texto = DOC.read_text()
    pos = leer_posiciones(texto)
    costos, nombres = leer_costos(texto)
    filas, diario, intra, fallas = [], {}, {}, []
    for t, cant in pos.items():
        if t in EFECTIVO:
            filas.append({"ticker": t, "nombre": nombres.get(t, t), "cantidad": cant, "precio": 1.0,
                          "valor": round(cant, 2), "cambio_dia_pct": 0.0, "cambio_dia_usd": 0.0,
                          "costo": round(cant, 2), "efectivo": True})
            continue
        try:
            _, d = yahoo(t, "5y", "1d")
            meta, i = yahoo(t, "1d", "5m")
        except Exception as e:  # noqa: BLE001
            fallas.append(f"{t}: {e!r}")
            continue
        p = float(meta["regularMarketPrice"])
        # el cierre anterior sale del intradiario: en el de 5 años «chartPreviousClose» es el de hace 5 años
        prev = float(meta.get("chartPreviousClose") or meta.get("previousClose") or p)
        filas.append({"ticker": t, "nombre": nombres.get(t, t), "cantidad": cant, "precio": round(p, 4),
                      "valor": round(cant * p, 2), "cambio_dia_pct": round((p / prev - 1) * 100, 2),
                      "cambio_dia_usd": round(cant * (p - prev), 2), "costo": costos.get(t),
                      "cierre_anterior": round(prev, 4)})
        for ts, c in d:
            diario.setdefault(dt.datetime.fromtimestamp(ts, dt.timezone.utc).date().isoformat(), {})[t] = c
        for ts, c in i:
            intra.setdefault(ts - ts % 300, {})[t] = c
    if fallas:
        raise SystemExit("Yahoo falló para " + "; ".join(fallas) + " — no subo un total incompleto (regla 2).")

    efectivo = sum(f["valor"] for f in filas if f.get("efectivo"))
    cants = {f["ticker"]: f["cantidad"] for f in filas if not f.get("efectivo")}

    def valuar(puntos):
        """Suma cantidad × último precio conocido de cada papel; arranca cuando todos tienen precio."""
        ult, out = {}, []
        for k in sorted(puntos):
            ult.update(puntos[k])
            if len(ult) == len(cants):
                out.append([k, round(efectivo + sum(cants[t] * ult[t] for t in cants), 2)])
        return out

    total = round(sum(f["valor"] for f in filas), 2)
    prev_total = round(efectivo + sum(f["cantidad"] * f["cierre_anterior"] for f in filas if not f.get("efectivo")), 2)
    for f in filas:
        f["peso_pct"] = round(f["valor"] / total * 100, 2)
        if f.get("costo") is not None and not f.get("efectivo"):
            f["ganancia_usd"] = round(f["valor"] - f["costo"], 2)
            f["ganancia_pct"] = round((f["valor"] / f["costo"] - 1) * 100, 2) if f["costo"] else None
    filas.sort(key=lambda f: -f["valor"])
    costo_total = sum(f["costo"] for f in filas if f.get("costo") is not None)
    return {
        "posiciones_al": fecha_tabla(texto).isoformat() if fecha_tabla(texto) else None,
        "total": total, "cierre_anterior": prev_total,
        "cambio_dia_usd": round(total - prev_total, 2),
        "cambio_dia_pct": round((total / prev_total - 1) * 100, 2) if prev_total else None,
        "ganancia_usd": round(total - costo_total, 2),
        "filas": filas,
        "serie_diaria": valuar(diario),
        "serie_hoy": [[dt.datetime.fromtimestamp(k, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:00Z"), v] for k, v in valuar(intra)],
    }


def _historial(texto, col_total="total_usd"):
    out = []
    for r in csv.DictReader(io.StringIO(texto)):
        try:
            f = dt.datetime.strptime(r["fecha"].replace(" UTC", ""), "%Y-%m-%d %H:%M").strftime("%Y-%m-%dT%H:%M:00Z")
            out.append([f, float(r[col_total]), float(r["hodl_btc"]) if r.get("hodl_btc") else None])
        except (ValueError, KeyError):
            continue
    return out


def git_show(rama, ruta):
    return subprocess.run(["git", "-C", str(RAIZ), "show", f"origin/{rama}:{ruta}"],
                          capture_output=True, text=True, check=True).stdout


def cripto():
    subprocess.run(["git", "-C", str(RAIZ), "fetch", "-q", "origin"], check=True, timeout=120)
    carpetas = []
    for cid, nombre, rama, ruta, que in CARPETAS:
        serie = _historial(git_show(rama, ruta))
        if not serie:
            raise SystemExit(f"El historial de {nombre} vino vacío (regla 2).")
        carpetas.append({"id": cid, "nombre": nombre, "que_es": que, "capital": 1000.0,
                         "serie": [[f, v] for f, v, _ in serie], "hodl_btc": [[f, h] for f, _, h in serie if h]})
    if PAPER.exists():
        serie = _historial(PAPER.read_text())
        carpetas.append({"id": "paper", "nombre": "La de 10.000 (Mac)", "capital": 10000.0,
                         "que_es": "Paper trading de 10.000 USDT en la Mac, cada 4 h.",
                         "serie": [[f, v] for f, v, _ in serie], "hodl_btc": [[f, h] for f, _, h in serie if h]})
    if PAPER_GROK.exists():
        serie = _historial(PAPER_GROK.read_text())
        if serie:
            carpetas.append({"id": "grok", "nombre": "Grok (Mac)", "capital": 10000.0,
                             "que_es": "Mismo motor y reglas que la de 10.000 de Claude, pero decide Grok, que además lee X y noticias. Desde el 20/11.",
                             "serie": [[f, v] for f, v, _ in serie], "hodl_btc": [[f, h] for f, _, h in serie if h]})
    vivo = json.loads(git_show("claude/cartera-torneo", "execution/cartera/estado-torneo/vivo.json"))
    torneo = {"desde": vivo.get("desde"), "hasta": vivo.get("hasta"), "regimen": vivo.get("regimen_hoy"),
              "capital": vivo.get("capital"),
              "filas": sorted(({"estrategia": f["estrategia"], "personalidad": f.get("personalidad"),
                                "final": round(f["final"], 2), "ret_pct": round(f["ret"] * 100, 2),
                                "hodl_btc_pct": round(f["hodl_btc"] * 100, 2) if f.get("hodl_btc") is not None else None,
                                "ops": f.get("ops")} for f in vivo["filas"]), key=lambda f: -f["ret_pct"])}
    return {"carpetas": carpetas, "torneo": torneo}


def subir(datos):
    from google_auth import sheets
    b64 = base64.b64encode(json.dumps(datos, ensure_ascii=False, separators=(",", ":")).encode()).decode()
    trozos = [[b64[i:i + 40000]] for i in range(0, len(b64), 40000)]
    s = sheets().spreadsheets().values()
    s.clear(spreadsheetId=HOJA_ID, range="datos!A:A").execute()
    s.update(spreadsheetId=HOJA_ID, range="datos!A1", valueInputOption="RAW", body={"values": trozos}).execute()
    return len(trozos), len(b64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-subir", action="store_true")
    a = ap.parse_args()
    datos = {"generado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "acciones": acciones(), "netx_mensual": json.loads(NETX.read_text()), "cripto": cripto()}
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False))
    a_ = datos["acciones"]
    print(f"acciones: {len(a_['filas'])} filas, total {a_['total']}, día {a_['cambio_dia_pct']}%, "
          f"{len(a_['serie_diaria'])} días, {len(a_['serie_hoy'])} puntos hoy")
    print("cripto: " + ", ".join(f"{c['nombre']} {len(c['serie'])}" for c in datos["cripto"]["carpetas"])
          + f", torneo {len(datos['cripto']['torneo']['filas'])}")
    if not a.sin_subir:
        n, largo = subir(datos)
        print(f"subido a la planilla: {n} trozos, {largo} caracteres")


if __name__ == "__main__":
    main()
