"""Carpeta cripto ficticia de 1.000 USD, vigilada minuto a minuto aunque la Mac esté apagada.

Corre en rutinas en la nube de Claude Code: PROMPT.md (3 niveles, cada 2 h) y PROMPT_AGRESIVA.md
`claude/cartera-cripto`, en `execution/cartera/estado/`. No usa key: precios públicos de
Binance (data-api.binance.vision, el espejo que responde desde servidores de EE.UU.).

Cómo es "24/7" sin un servidor prendido: cada posición lleva su stop, su trailing stop y
sus tomas de ganancia. `vigilar` recorre TODAS las velas de 1 minuto desde la última
pasada y ejecuta cada regla en el minuto exacto en que se habría disparado, al precio
del disparo. Es lo mismo que haría un vigilante mirando cada segundo — y es lo mismo
que hacen las órdenes stop/OCO reales de Binance, que viven en el exchange.

Reglas que hace cumplir el código, no el criterio del que opera:
- Sólo pares USDT en estado TRADING, sin stablecoins, oro ni acciones tokenizadas.
- Nivel `conservador`: sólo BTC, ETH, BNB. `medio`: volumen 24 h ≥ 20 M USD.
  `riesgo`: volumen ≥ 5 M USD y máximo 5% de la carpeta por posición.
- Ninguna compra pasa el 35% de la carpeta. Mínimo 5 USD por orden.
- Compra al ask, vende al bid (o al precio del disparo), comisión 0,1% por lado.
- Si Binance no responde, no se opera ni se vigila con precios viejos.

Uso:
    cartera.py init --capital 1000
    cartera.py radar [--top 60]          # pares líquidos con 1d/7d/30d/90d y volatilidad
    cartera.py orden --lado buy --par NEARUSDT --usd 30 --nivel riesgo --motivo "..."
    cartera.py orden --lado sell --par NEARUSDT (--usd N | --todo) --motivo "..."
    cartera.py reglas --par NEARUSDT [--stop 12] [--trail 15] [--tp 40:0.5,100:0.5] --motivo "..."
    cartera.py vigilar                   # ejecuta stops y tomas de ganancia minuto a minuto
    cartera.py estado
    cartera.py nota --texto "..."
    cartera.py snapshot
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DIR = Path(os.environ.get("CARTERA_DIR", Path(__file__).resolve().parent / "estado"))
LIBRO = DIR / "libro.json"
DIARIO = DIR / "diario.md"
HISTORIAL = DIR / "historial.csv"
RESUMEN = DIR / "RESUMEN.md"
PERFIL = DIR / "perfil.json"

API = "https://data-api.binance.vision/api/v3"
COMISION = 0.001
TOPE_POSICION = 0.35
TOPE_RIESGO = 0.05
MINIMO_USD = 5.0
CONSERVADORES = ("BTC", "ETH", "BNB")
VOLUMEN_MINIMO = {"conservador": 0.0, "medio": 20e6, "riesgo": 5e6, "trading": 20e6}
EXCLUIDOS = {"USDC", "FDUSD", "TUSD", "DAI", "USDP", "EUR", "USDE", "USD1", "XUSD", "BFUSD",
             "RLUSD", "PAXG", "EURI", "AEUR", "USDS", "PYUSD", "XAUT", "U"}
# Reglas por defecto: stop % bajo la compra, trailing % bajo el máximo, tomas [(+%, fracción)].
REGLAS = {
    "conservador": {"stop": 25.0, "trail": 25.0, "tp": []},
    "medio": {"stop": 18.0, "trail": 20.0, "tp": [[50.0, 0.33]]},
    "riesgo": {"stop": 15.0, "trail": 15.0, "tp": [[40.0, 0.5], [100.0, 0.5]]},
    # Carpeta agresiva: entrar y salir en horas o días. Vende la mitad a +8% y el resto a +15%.
    "trading": {"stop": 5.0, "trail": 5.0, "tp": [[8.0, 0.5], [15.0, 1.0]]},
}
# Sin perfil.json en la carpeta: la estrategia de 3 niveles. Con perfil: lo que diga.
PERFIL_BASE = {"nombre": "Carpeta cripto ficticia", "niveles": ["conservador", "medio", "riesgo"],
               "tope_posicion": TOPE_POSICION}


def perfil() -> dict:
    return PERFIL_BASE | (json.loads(PERFIL.read_text()) if PERFIL.exists() else {})
MINUTO_MS = 60_000


class ErrorCartera(Exception):
    pass


def ahora_ms() -> int:
    return int(time.time() * 1000)


def fecha(ms: int | None = None) -> str:
    t = datetime.fromtimestamp((ms if ms is not None else ahora_ms()) / 1000, timezone.utc)
    return t.strftime("%Y-%m-%d %H:%M UTC")


# --- Binance -------------------------------------------------------------------------

def _get(ruta: str, params: dict | None = None) -> object:
    url = f"{API}/{ruta}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    for intento in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            if intento == 2:
                raise ErrorCartera(f"Binance no respondió ({ruta}): {e}. No se opera sin precio.")
            time.sleep(2 * (intento + 1))


def es_accion_tokenizada(base: str) -> bool:
    # Binance lista acciones y ETFs tokenizados con una B al final (NVDAB, QQQB, MSTRB...).
    # Ninguna cripto líquida de 4+ letras termina en B; las de 3 que sí son acciones, a mano.
    return (len(base) >= 4 and base.endswith("B")) or base in {"MUB", "BEB", "GSB"}


def pares_validos() -> dict[str, str]:
    """{símbolo: activo base} de los pares USDT operables: sin stables, oro ni acciones."""
    info = _get("exchangeInfo", {"permissions": "SPOT", "showPermissionSets": "false", "symbolStatus": "TRADING"})
    return {s["symbol"]: s["baseAsset"] for s in info["symbols"]
            if s["status"] == "TRADING" and s["quoteAsset"] == "USDT" and s["baseAsset"].isascii()
            and s["baseAsset"] not in EXCLUIDOS and not es_accion_tokenizada(s["baseAsset"])}


def tickers_24h(simbolos: list[str] | None = None) -> dict[str, dict]:
    params = {"symbols": json.dumps(simbolos, separators=(",", ":"))} if simbolos else None
    return {d["symbol"]: d for d in _get("ticker/24hr", params)}


def libro_de_precios(simbolos: list[str]) -> dict[str, dict[str, float]]:
    if not simbolos:
        return {}
    data = _get("ticker/bookTicker", {"symbols": json.dumps(sorted(simbolos), separators=(",", ":"))})
    p = {d["symbol"]: {"bid": float(d["bidPrice"]), "ask": float(d["askPrice"])} for d in data}
    faltan = [s for s in simbolos if s not in p or p[s]["bid"] <= 0 or p[s]["ask"] <= 0]
    if faltan:
        raise ErrorCartera(f"Faltan precios de {faltan}. No se opera.")
    return p


def velas(simbolo: str, intervalo: str, desde_ms: int | None = None, limite: int = 1000) -> list:
    params = {"symbol": simbolo, "interval": intervalo, "limit": limite}
    if desde_ms is not None:
        params["startTime"] = desde_ms
    return _get("klines", params)


# --- libro ---------------------------------------------------------------------------

def leer() -> dict:
    if not LIBRO.exists():
        raise ErrorCartera(f"No hay carpeta. Correr `cartera.py init` primero ({LIBRO}).")
    return json.loads(LIBRO.read_text())


def guardar(libro: dict) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=DIR, suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(libro, f, indent=2, ensure_ascii=False)
    os.replace(tmp, LIBRO)


def anotar(texto: str) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    with DIARIO.open("a") as f:
        f.write(texto.rstrip() + "\n\n")


def stop_vigente(pos: dict) -> float:
    r = pos["reglas"]
    return max(pos["entrada"] * (1 - r["stop"] / 100), pos["maximo"] * (1 - r["trail"] / 100))


def valuar(libro: dict, precios: dict) -> dict:
    total = libro["usdt"]
    posiciones = {}
    for par, pos in sorted(libro["posiciones"].items()):
        bid = precios[par]["bid"]
        v = pos["cantidad"] * bid
        total += v
        posiciones[par] = {
            "nivel": pos["nivel"], "valor_usd": round(v, 2), "precio": bid,
            "resultado_pct": round((bid / pos["entrada"] - 1) * 100, 2),
            "stop": round(stop_vigente(pos), 8),
            "tomas_pendientes": [t for t in pos["reglas"]["tp"] if t[0] not in pos["tomas_hechas"]],
        }
    ini = libro["inicio"]
    plan = ini.get("plan_sin_tocar")
    bench = {"quedarse_en_usdt": ini["capital"]}
    if "BTCUSDT" in precios:
        bench["hodl_btc"] = round(ini["capital"] / ini["btc"] * (precios["BTCUSDT"]["bid"]), 2)
    if plan and all(p in precios for p in plan["cantidades"]):
        bench["plan_inicial_sin_tocar"] = round(
            plan["usdt"] + sum(c * precios[p]["bid"] for p, c in plan["cantidades"].items()), 2)
    return {
        "fecha": fecha(), "total_usd": round(total, 2), "usdt": round(libro["usdt"], 2),
        "resultado_pct": round((total / ini["capital"] - 1) * 100, 2),
        "por_nivel_usd": {n: round(sum(p["valor_usd"] for p in posiciones.values() if p["nivel"] == n), 2)
                          for n in REGLAS},
        "posiciones": posiciones, "vs": bench,
        "comisiones_usd": round(libro["comisiones_usd"], 2),
        "operaciones": len(libro["operaciones"]), "desde": fecha(ini["ms"]),
    }


def precios_de(libro: dict) -> dict:
    return libro_de_precios(sorted(set(libro["posiciones"]) | {"BTCUSDT"} |
                                   set((libro["inicio"].get("plan_sin_tocar") or {}).get("cantidades", {}))))


def _registrar(libro: dict, op: dict) -> None:
    libro["operaciones"].append(op)
    libro["comisiones_usd"] += op["comision"]


def _vender(libro: dict, par: str, cant: float, precio: float, ms: int, motivo: str) -> dict:
    pos = libro["posiciones"][par]
    cant = min(cant, pos["cantidad"])
    bruto = cant * precio
    com = bruto * COMISION
    libro["usdt"] += bruto - com
    pos["cantidad"] -= cant
    op = {"ms": ms, "fecha": fecha(ms), "lado": "sell", "par": par, "cantidad": cant, "precio": precio,
          "usd": round(bruto, 4), "comision": round(com, 6), "motivo": motivo,
          "resultado_pct": round((precio / pos["entrada"] - 1) * 100, 2)}
    _registrar(libro, op)
    if pos["cantidad"] * precio < 0.01:
        del libro["posiciones"][par]
    return op


# --- comandos ------------------------------------------------------------------------

def cmd_init(capital: float, forzar: bool) -> dict:
    if LIBRO.exists() and not forzar:
        raise ErrorCartera(f"Ya hay una carpeta en {LIBRO}. Para empezar de cero: --forzar.")
    p = libro_de_precios(["BTCUSDT"])
    ms = ahora_ms()
    libro = {"inicio": {"ms": ms, "capital": capital, "btc": p["BTCUSDT"]["ask"]},
             "usdt": capital, "posiciones": {}, "comisiones_usd": 0.0, "operaciones": []}
    guardar(libro)
    anotar(f"## {fecha(ms)} — arranca la carpeta\nCapital ficticio: {capital:,.2f} USDT.")
    return valuar(libro, p)


def _parse_tp(texto: str) -> list[list[float]]:
    out = []
    for parte in filter(None, texto.split(",")):
        pct, frac = parte.split(":")
        pct, frac = float(pct), float(frac)
        if pct <= 0 or not 0 < frac <= 1:
            raise ErrorCartera(f"Toma inválida {parte}: va +%:fracción, ej. 40:0.5.")
        out.append([pct, frac])
    return sorted(out)


def _reglas_validas(r: dict) -> dict:
    if not 1 <= r["stop"] <= 60 or not 1 <= r["trail"] <= 60:
        raise ErrorCartera("Stop y trailing van entre 1% y 60%.")
    return r


def cmd_comprar(par: str, usd: float, nivel: str, motivo: str, stop, trail, tp) -> dict:
    validos = pares_validos()
    if par not in validos:
        raise ErrorCartera(f"{par} no es un par USDT operable (o es stable/oro/acción).")
    base = validos[par]
    if nivel not in perfil()["niveles"]:
        raise ErrorCartera(f"Esta carpeta opera {', '.join(perfil()['niveles'])}, no {nivel}.")
    if nivel == "conservador" and base not in CONSERVADORES:
        raise ErrorCartera(f"Conservador es sólo {', '.join(CONSERVADORES)}.")
    t = tickers_24h([par])[par]
    vol = float(t["quoteVolume"])
    if vol < VOLUMEN_MINIMO[nivel]:
        raise ErrorCartera(f"{par} movió {vol / 1e6:,.1f} M USD en 24 h; nivel {nivel} pide "
                           f"{VOLUMEN_MINIMO[nivel] / 1e6:,.0f} M.")
    libro = leer()
    pos = libro["posiciones"].get(par)
    if pos and pos["nivel"] != nivel:
        raise ErrorCartera(f"{par} ya está en la carpeta como {pos['nivel']}.")
    precios = precios_de(libro) | libro_de_precios([par])
    total = valuar(libro, precios)["total_usd"]
    ya = pos["cantidad"] * precios[par]["bid"] if pos else 0.0
    tope = total * (TOPE_RIESGO if nivel == "riesgo" else perfil()["tope_posicion"])
    if usd < MINIMO_USD:
        raise ErrorCartera(f"Orden mínima {MINIMO_USD} USD.")
    if ya + usd > tope + 1e-9:
        raise ErrorCartera(f"{par} quedaría en {ya + usd:,.2f} USD y el tope de {nivel} es {tope:,.2f}.")
    if usd > libro["usdt"] + 1e-9:
        raise ErrorCartera(f"No alcanza: hay {libro['usdt']:,.2f} USDT.")

    precio = precios[par]["ask"]
    com = usd * COMISION
    cant = (usd - com) / precio
    ms = ahora_ms()
    libro["usdt"] -= usd
    if pos:
        nueva = pos["cantidad"] + cant
        pos["entrada"] = (pos["entrada"] * pos["cantidad"] + precio * cant) / nueva
        pos["cantidad"] = nueva
        pos["maximo"] = max(pos["maximo"], precio)
    else:
        r = dict(REGLAS[nivel], tp=[list(x) for x in REGLAS[nivel]["tp"]])
        if stop is not None:
            r["stop"] = stop
        if trail is not None:
            r["trail"] = trail
        if tp is not None:
            r["tp"] = _parse_tp(tp)
        libro["posiciones"][par] = {"nivel": nivel, "cantidad": cant, "entrada": precio, "maximo": precio,
                                    "reglas": _reglas_validas(r), "tomas_hechas": [],
                                    "vigilado_hasta": (ms // MINUTO_MS + 1) * MINUTO_MS}
    op = {"ms": ms, "fecha": fecha(ms), "lado": "buy", "par": par, "nivel": nivel, "cantidad": cant,
          "precio": precio, "usd": round(usd, 4), "comision": round(com, 6), "motivo": motivo}
    _registrar(libro, op)
    guardar(libro)
    p = libro["posiciones"][par]
    anotar(f"## {op['fecha']} — Compra {par} ({nivel})\n{usd:,.2f} USD a {precio:,.8g}. "
           f"Stop {p['reglas']['stop']}% · trailing {p['reglas']['trail']}% · tomas {p['reglas']['tp']}.\n\n{motivo}")
    return {"operacion": op}


def cmd_vender(par: str, usd: float | None, todo: bool, motivo: str) -> dict:
    libro = leer()
    if par not in libro["posiciones"]:
        raise ErrorCartera(f"No hay {par} en la carpeta.")
    pos = libro["posiciones"][par]
    precio = libro_de_precios([par])[par]["bid"]
    cant = pos["cantidad"] if todo else usd / precio
    if cant > pos["cantidad"] * (1 + 1e-9):
        raise ErrorCartera(f"Hay {pos['cantidad'] * precio:,.2f} USD de {par}, no {usd:,.2f}.")
    if not todo and cant * precio < MINIMO_USD:
        raise ErrorCartera(f"Orden mínima {MINIMO_USD} USD.")
    op = _vender(libro, par, cant, precio, ahora_ms(), motivo)
    guardar(libro)
    anotar(f"## {op['fecha']} — Venta {par}\n{op['usd']:,.2f} USD a {precio:,.8g} "
           f"({op['resultado_pct']:+.2f}% contra la compra).\n\n{motivo}")
    return {"operacion": op}


def cmd_reglas(par: str, stop, trail, tp, motivo: str) -> dict:
    libro = leer()
    if par not in libro["posiciones"]:
        raise ErrorCartera(f"No hay {par} en la carpeta.")
    r = libro["posiciones"][par]["reglas"]
    antes = dict(r)
    if stop is not None:
        r["stop"] = stop
    if trail is not None:
        r["trail"] = trail
    if tp is not None:
        r["tp"] = _parse_tp(tp)
    _reglas_validas(r)
    guardar(libro)
    anotar(f"## {fecha()} — Reglas {par}\nAntes {antes} → ahora {r}.\n\n{motivo}")
    return {"par": par, "reglas": r}


def vigilar_posicion(libro: dict, par: str, velas_1m: list) -> list[dict]:
    """Recorre velas de 1 minuto en orden y dispara stops y tomas como un vigilante en vivo.

    Dentro de una vela no se sabe qué vino primero: se asume lo peor (el stop antes que la
    toma) y el máximo de la vela recién cuenta para el trailing de la vela siguiente.
    Si la vela abre ya del otro lado del stop (un gap), se vende a la apertura, no al stop.
    """
    ops = []
    for v in velas_1m:
        pos = libro["posiciones"].get(par)
        if pos is None:
            break
        abre, alto, bajo, ms = float(v[1]), float(v[2]), float(v[3]), int(v[0])
        stop = stop_vigente(pos)
        if bajo <= stop:
            precio = min(abre, stop)
            ops.append(_vender(libro, par, pos["cantidad"], precio, ms,
                               f"Stop automático en {precio:,.8g} (entrada {pos['entrada']:,.8g}, "
                               f"máximo {pos['maximo']:,.8g})."))
            break
        for pct, frac in pos["reglas"]["tp"]:
            if pct in pos["tomas_hechas"]:
                continue
            objetivo = pos["entrada"] * (1 + pct / 100)
            if alto >= objetivo:
                precio = max(abre, objetivo)
                pos["tomas_hechas"].append(pct)
                ops.append(_vender(libro, par, pos["cantidad"] * frac, precio, ms,
                                   f"Toma de ganancia +{pct:g}% en {precio:,.8g}: vende {frac:.0%} de lo que quedaba."))
                if par not in libro["posiciones"]:
                    return ops
        pos["maximo"] = max(pos["maximo"], alto)
        pos["vigilado_hasta"] = ms + MINUTO_MS
    return ops


def cmd_vigilar() -> dict:
    libro = leer()
    corte = (ahora_ms() // MINUTO_MS) * MINUTO_MS  # sólo velas cerradas
    resumen = {}
    for par in sorted(list(libro["posiciones"])):
        pos = libro["posiciones"][par]
        desde = pos["vigilado_hasta"]
        minutos = 0
        while par in libro["posiciones"] and desde < corte:
            tanda = [v for v in velas(par, "1m", desde) if int(v[0]) >= desde and int(v[6]) < corte]
            if not tanda:
                break
            minutos += len(tanda)
            ops = vigilar_posicion(libro, par, tanda)
            for op in ops:
                anotar(f"## {op['fecha']} — {op['motivo'].split(' ')[0]} {par} (vigilante)\n"
                       f"{op['usd']:,.2f} USD a {op['precio']:,.8g} ({op['resultado_pct']:+.2f}%). {op['motivo']}")
            if ops:
                resumen.setdefault(par, []).extend(o["motivo"] for o in ops)
            if par in libro["posiciones"]:
                desde = libro["posiciones"][par]["vigilado_hasta"]
        resumen.setdefault(par, [])
        resumen[par] = {"minutos_revisados": minutos, "disparos": resumen[par]}
    guardar(libro)
    return {"fecha": fecha(), "vigilancia": resumen}


def cmd_radar_corto(top: int) -> dict:
    """Radar para la carpeta agresiva: velas de 1 h de las últimas 48 h."""
    validos = pares_validos()
    t = [d for s, d in tickers_24h().items() if s in validos and float(d["quoteVolume"]) >= VOLUMEN_MINIMO["trading"]]
    t.sort(key=lambda d: -float(d["quoteVolume"]))
    out = []
    for d in t[:top]:
        k = velas(d["symbol"], "1h", limite=49)
        if len(k) < 49:
            continue
        c = [float(v[4]) for v in k]
        vq = [float(v[7]) for v in k]
        p = c[-1]
        prom4 = sum(vq[:-4]) / (len(vq) - 4) * 4
        out.append({"par": d["symbol"], "vol_24h_musd": round(float(d["quoteVolume"]) / 1e6, 1),
                    "var_1h": round((p / c[-2] - 1) * 100, 2), "var_4h": round((p / c[-5] - 1) * 100, 2),
                    "var_24h": round((p / c[-25] - 1) * 100, 2), "var_48h": round((p / c[0] - 1) * 100, 2),
                    "volumen_4h_vs_promedio": round(sum(vq[-4:]) / prom4, 2) if prom4 else None,
                    "vs_max_48h": round((p / max(float(v[2]) for v in k) - 1) * 100, 2),
                    "vs_min_48h": round((p / min(float(v[3]) for v in k) - 1) * 100, 2)})
    return {"fecha": fecha(), "pares": out}


def cmd_radar(top: int) -> dict:
    validos = pares_validos()
    t = [d for s, d in tickers_24h().items() if s in validos]
    t.sort(key=lambda d: -float(d["quoteVolume"]))
    out = []
    for d in t:
        if len(out) >= top:
            break
        s = d["symbol"]
        k = velas(s, "1d", limite=91)
        c = [float(v[4]) for v in k]
        if len(c) < 31:
            continue
        rets = [math.log(c[i] / c[i - 1]) for i in range(len(c) - 30, len(c))]
        vol = statistics.pstdev(rets) * math.sqrt(365) * 100
        p = c[-1]
        out.append({"par": s, "vol_24h_musd": round(float(d["quoteVolume"]) / 1e6, 1),
                    "var_1d": round((p / c[-2] - 1) * 100, 1), "var_7d": round((p / c[-8] - 1) * 100, 1),
                    "var_30d": round((p / c[-31] - 1) * 100, 1),
                    "var_90d": round((p / c[0] - 1) * 100, 1) if len(c) == 91 else None,
                    "volatilidad_anual": round(vol), "vs_max_90d": round((p / max(float(v[2]) for v in k) - 1) * 100, 1)})
    return {"fecha": fecha(), "pares": out}


def escribir_resumen(e: dict, libro: dict) -> None:
    """RESUMEN.md: lo que Facu abre desde el celular en GitHub."""
    L = [f"# {perfil()['nombre']} — {e['fecha']}", "",
         f"**Total: {e['total_usd']:,.2f} USD ({e['resultado_pct']:+.2f}%)** desde {e['desde']} · "
         f"USDT libre {e['usdt']:,.2f} · comisiones {e['comisiones_usd']:,.2f} · {e['operaciones']} operaciones", "",
         "| Contra qué | USD |", "|---|---:|", f"| **Esta carpeta** | **{e['total_usd']:,.2f}** |"]
    L += [f"| {k.replace('_', ' ')} | {v:,.2f} |" for k, v in e["vs"].items()]
    L += ["", "| Par | Nivel | USD | vs compra | Stop vigente |", "|---|---|---:|---:|---:|"]
    for par, p in sorted(e["posiciones"].items(), key=lambda x: -x[1]["valor_usd"]):
        L.append(f"| {par.removesuffix('USDT')} | {p['nivel']} | {p['valor_usd']:,.2f} | {p['resultado_pct']:+.2f}% | {p['stop']:,.6g} |")
    L += ["", "## Últimas operaciones", ""]
    for op in libro["operaciones"][-10:][::-1]:
        L.append(f"- {op['fecha']} · {'compra' if op['lado'] == 'buy' else 'venta'} {op['par'].removesuffix('USDT')} "
                 f"{op['usd']:,.2f} USD a {op['precio']:,.6g} — {op['motivo'][:140]}")
    L += ["", "El diario completo con cada decisión está en `diario.md`, al lado de este archivo."]
    RESUMEN.write_text("\n".join(L) + "\n")


def cmd_snapshot() -> dict:
    libro = leer()
    e = valuar(libro, precios_de(libro))
    escribir_resumen(e, libro)
    nuevo = not HISTORIAL.exists()
    with HISTORIAL.open("a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha", "total_usd", "resultado_pct", "hodl_btc", "plan_sin_tocar", "usdt", "posiciones", "operaciones"])
        w.writerow([e["fecha"], e["total_usd"], e["resultado_pct"], e["vs"].get("hodl_btc"),
                    e["vs"].get("plan_inicial_sin_tocar"), e["usdt"], len(e["posiciones"]), e["operaciones"]])
    return e


def cmd_fijar_plan() -> dict:
    """Congela las posiciones actuales como 'plan inicial sin tocar' para comparar después."""
    libro = leer()
    if libro["inicio"].get("plan_sin_tocar"):
        raise ErrorCartera("El plan inicial ya está fijado.")
    libro["inicio"]["plan_sin_tocar"] = {"usdt": libro["usdt"],
                                         "cantidades": {p: x["cantidad"] for p, x in libro["posiciones"].items()}}
    guardar(libro)
    return libro["inicio"]["plan_sin_tocar"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--capital", type=float, default=1000)
    i.add_argument("--forzar", action="store_true")
    r = sub.add_parser("radar")
    r.add_argument("--top", type=int, default=60)
    r.add_argument("--corto", action="store_true", help="velas de 1 h, últimas 48 h (carpeta agresiva)")
    for nombre in ("estado", "vigilar", "snapshot", "fijar-plan"):
        sub.add_parser(nombre)
    n = sub.add_parser("nota")
    n.add_argument("--texto", required=True)
    o = sub.add_parser("orden")
    o.add_argument("--lado", choices=["buy", "sell"], required=True)
    o.add_argument("--par", required=True)
    o.add_argument("--usd", type=float)
    o.add_argument("--todo", action="store_true")
    o.add_argument("--nivel", choices=list(REGLAS))
    o.add_argument("--stop", type=float)
    o.add_argument("--trail", type=float)
    o.add_argument("--tp")
    o.add_argument("--motivo", required=True)
    g = sub.add_parser("reglas")
    g.add_argument("--par", required=True)
    g.add_argument("--stop", type=float)
    g.add_argument("--trail", type=float)
    g.add_argument("--tp")
    g.add_argument("--motivo", required=True)
    a = ap.parse_args(argv)

    try:
        if a.cmd in ("orden", "reglas") and len(a.motivo.strip()) < 10:
            raise ErrorCartera("Toda orden o cambio de reglas lleva --motivo (mínimo 10 caracteres).")
        if a.cmd == "init":
            res = cmd_init(a.capital, a.forzar)
        elif a.cmd == "radar":
            res = cmd_radar_corto(a.top) if a.corto else cmd_radar(a.top)
        elif a.cmd == "estado":
            libro = leer()
            res = valuar(libro, precios_de(libro))
        elif a.cmd == "vigilar":
            res = cmd_vigilar()
        elif a.cmd == "snapshot":
            res = cmd_snapshot()
        elif a.cmd == "fijar-plan":
            res = cmd_fijar_plan()
        elif a.cmd == "nota":
            if len(a.texto.strip()) < 10:
                raise ErrorCartera("La nota lleva al menos 10 caracteres.")
            leer()
            anotar(f"## {fecha()} — nota\n{a.texto.strip()}")
            res = {"anotado": True}
        elif a.cmd == "reglas":
            res = cmd_reglas(a.par.upper(), a.stop, a.trail, a.tp, a.motivo.strip())
        elif a.lado == "buy":
            if a.usd is None or a.todo or a.nivel is None:
                raise ErrorCartera("Una compra lleva --usd N y --nivel.")
            res = cmd_comprar(a.par.upper(), a.usd, a.nivel, a.motivo.strip(), a.stop, a.trail, a.tp)
        else:
            if a.todo == (a.usd is not None):
                raise ErrorCartera("Una venta lleva --usd N o --todo, uno de los dos.")
            res = cmd_vender(a.par.upper(), a.usd, a.todo, a.motivo.strip())
    except ErrorCartera as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
