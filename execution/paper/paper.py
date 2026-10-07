"""Carpeta ficticia (paper trading) contra precios reales de Binance.

Prueba si Claude opera bien antes de darle una key real. NO usa key ni toca la cuenta
de Facu: lee precios públicos de Binance y anota todo en un libro local.

Sólo usa la biblioteca estándar, para que corra en cualquier máquina sin instalar nada.

Reglas que el código hace cumplir (no el criterio del que opera):
- Sólo los pares de PARES, contra USDT. Nada de apalancamiento ni cortos.
- Una orden no puede pasar el TOPE_ORDEN del valor total de la carpeta.
- Compra al ask, vende al bid, comisión COMISION (la de Binance spot sin BNB).
- Si Binance no responde, no se opera: no hay precio viejo ni estimado.

Uso:
    paper.py init --capital 10000
    paper.py mercado              # precios y variaciones 1d/7d/30d
    paper.py estado               # carpeta, resultado y contra quién compararla
    paper.py orden --lado buy --par BTCUSDT --usd 1500 --motivo "..."
    paper.py orden --lado sell --par BTCUSDT --todo --motivo "..."
    paper.py snapshot             # anota el valor en historial.csv (lo corre cada ciclo)
    paper.py nota --texto "..."   # deja en el diario por qué no se operó
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import urllib.error
import urllib.parse
import urllib.request

DIR = Path(os.environ.get("PAPER_DIR", "/Users/Facu/facu-os/data/paper"))
LIBRO = DIR / "libro.json"
DIARIO = DIR / "diario.md"
HISTORIAL = DIR / "historial.csv"

# Espejo oficial de datos de mercado: api.binance.com da 451 desde IPs de EE.UU. (la nube).
API = "https://data-api.binance.vision/api/v3"
PARES = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT")
COMISION = 0.001
TOPE_ORDEN = 0.25
MINIMO_USD = 10.0


class ErrorPaper(Exception):
    pass


def ahora() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# --- precios -------------------------------------------------------------------------

def _get(ruta: str, params: dict) -> object:
    url = f"{API}/{ruta}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        raise ErrorPaper(f"Binance no respondió ({ruta}): {e}. No se opera sin precio.")


def libro_de_precios() -> dict[str, dict[str, float]]:
    """{par: {bid, ask}} de todos los PARES. Falla si falta alguno."""
    data = _get("ticker/bookTicker", {"symbols": json.dumps(list(PARES), separators=(",", ":"))})
    precios = {d["symbol"]: {"bid": float(d["bidPrice"]), "ask": float(d["askPrice"])} for d in data}
    faltan = [p for p in PARES if p not in precios or precios[p]["bid"] <= 0 or precios[p]["ask"] <= 0]
    if faltan:
        raise ErrorPaper(f"Faltan precios de {faltan}. No se opera.")
    return precios


def medio(precios: dict, par: str) -> float:
    return (precios[par]["bid"] + precios[par]["ask"]) / 2


# --- libro ---------------------------------------------------------------------------

def leer() -> dict:
    if not LIBRO.exists():
        raise ErrorPaper(f"No hay carpeta. Correr `paper.py init` primero ({LIBRO}).")
    return json.loads(LIBRO.read_text())


def guardar(libro: dict) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=DIR, suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(libro, f, indent=2)
    os.replace(tmp, LIBRO)


def anotar_diario(texto: str) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    with DIARIO.open("a") as f:
        f.write(texto.rstrip() + "\n\n")


def valuar(libro: dict, precios: dict) -> dict:
    """Valor a precio de venta (bid): lo que daría liquidar todo hoy, sin comisión."""
    posiciones = {}
    total = libro["usdt"]
    for par, cant in libro["posiciones"].items():
        if cant <= 0:
            continue
        v = cant * precios[par]["bid"]
        posiciones[par] = {"cantidad": cant, "precio": precios[par]["bid"], "valor_usd": round(v, 2)}
        total += v
    ini = libro["inicio"]
    btc0, eth0 = ini["precios"]["BTCUSDT"], ini["precios"]["ETHUSDT"]
    cap = ini["capital"]
    hodl_btc = cap / btc0 * medio(precios, "BTCUSDT")
    mitad = cap / 2 / btc0 * medio(precios, "BTCUSDT") + cap / 2 / eth0 * medio(precios, "ETHUSDT")
    return {
        "fecha": ahora(),
        "usdt": round(libro["usdt"], 2),
        "posiciones": posiciones,
        "total_usd": round(total, 2),
        "resultado_pct": round((total / cap - 1) * 100, 2),
        "vs": {
            "quedarse_en_usdt": cap,
            "hodl_btc": round(hodl_btc, 2),
            "hodl_50_btc_50_eth": round(mitad, 2),
        },
        "comisiones_pagadas_usd": round(libro["comisiones_usd"], 2),
        "operaciones": len(libro["operaciones"]),
        "desde": ini["fecha"],
    }


# --- comandos ------------------------------------------------------------------------

def cmd_init(capital: float, forzar: bool) -> dict:
    if LIBRO.exists() and not forzar:
        raise ErrorPaper(f"Ya hay una carpeta en {LIBRO}. Para empezar de cero: --forzar.")
    if capital < 100:
        raise ErrorPaper("Capital mínimo: 100 USDT.")
    precios = libro_de_precios()
    libro = {
        "inicio": {"fecha": ahora(), "capital": capital, "precios": {p: medio(precios, p) for p in PARES}},
        "usdt": capital,
        "posiciones": {},
        "comisiones_usd": 0.0,
        "operaciones": [],
    }
    guardar(libro)
    anotar_diario(f"## {ahora()} — arranca la carpeta\nCapital ficticio: {capital:,.2f} USDT.")
    return valuar(libro, precios)


def cmd_orden(lado: str, par: str, usd: float | None, todo: bool, motivo: str) -> dict:
    par = par.upper()
    if par not in PARES:
        raise ErrorPaper(f"{par} no está permitido. Permitidos: {', '.join(PARES)}.")
    if not motivo or len(motivo.strip()) < 10:
        raise ErrorPaper("Toda orden lleva --motivo (mínimo 10 caracteres).")
    if todo == (usd is not None):
        raise ErrorPaper("Pasá --usd N o --todo, uno de los dos.")
    if lado == "buy" and todo:
        raise ErrorPaper("--todo es sólo para vender.")

    libro = leer()
    precios = libro_de_precios()
    total = valuar(libro, precios)["total_usd"]
    tope = total * TOPE_ORDEN

    if lado == "buy":
        if usd < MINIMO_USD:
            raise ErrorPaper(f"Orden mínima {MINIMO_USD} USD.")
        if usd > tope + 1e-9:
            raise ErrorPaper(f"{usd:,.2f} USD pasa el tope del {TOPE_ORDEN:.0%} de la carpeta ({tope:,.2f}).")
        if usd > libro["usdt"] + 1e-9:
            raise ErrorPaper(f"No alcanza: hay {libro['usdt']:,.2f} USDT.")
        precio = precios[par]["ask"]
        comision = usd * COMISION
        cant = (usd - comision) / precio
        libro["usdt"] -= usd
        libro["posiciones"][par] = libro["posiciones"].get(par, 0.0) + cant
        bruto = usd
    else:
        tengo = libro["posiciones"].get(par, 0.0)
        if tengo <= 0:
            raise ErrorPaper(f"No hay {par} para vender.")
        precio = precios[par]["bid"]
        cant = tengo if todo else usd / precio
        if cant > tengo * (1 + 1e-9):
            raise ErrorPaper(f"Hay {tengo:.8f} de {par} (≈{tengo * precio:,.2f} USD), no {cant:.8f}.")
        cant = min(cant, tengo)
        bruto = cant * precio
        if bruto < MINIMO_USD and not todo:
            raise ErrorPaper(f"Orden mínima {MINIMO_USD} USD.")
        if bruto > tope + 1e-9 and not todo:
            raise ErrorPaper(f"{bruto:,.2f} USD pasa el tope del {TOPE_ORDEN:.0%} de la carpeta ({tope:,.2f}). "
                             "Para cerrar la posición entera usá --todo.")
        comision = bruto * COMISION
        libro["usdt"] += bruto - comision
        libro["posiciones"][par] = tengo - cant
        if libro["posiciones"][par] * precio < 0.01:
            del libro["posiciones"][par]

    libro["comisiones_usd"] += comision
    op = {"fecha": ahora(), "lado": lado, "par": par, "cantidad": cant, "precio": precio,
          "usd": round(bruto, 2), "comision": round(comision, 4), "motivo": motivo.strip()}
    libro["operaciones"].append(op)
    guardar(libro)
    verbo = "Compra" if lado == "buy" else "Venta"
    anotar_diario(f"## {op['fecha']} — {verbo} {par}\n{cant:.8f} a {precio:,.2f} = {bruto:,.2f} USD "
                  f"(comisión {comision:,.2f}).\n\n{motivo.strip()}")
    return {"operacion": op, "estado": valuar(libro, precios)}


def cmd_mercado() -> dict:
    precios = libro_de_precios()
    out = {}
    for par in PARES:
        velas = _get("klines", {"symbol": par, "interval": "1d", "limit": 31})
        cierres = [float(v[4]) for v in velas]
        if len(cierres) < 31:
            raise ErrorPaper(f"{par}: Binance devolvió {len(cierres)} velas diarias, se esperaban 31.")
        p = medio(precios, par)
        out[par] = {
            "precio": round(p, 4),
            "var_1d_pct": round((p / cierres[-2] - 1) * 100, 2),
            "var_7d_pct": round((p / cierres[-8] - 1) * 100, 2),
            "var_30d_pct": round((p / cierres[0] - 1) * 100, 2),
            "max_30d": max(float(v[2]) for v in velas),
            "min_30d": min(float(v[3]) for v in velas),
        }
    return {"fecha": ahora(), "pares": out}


def cmd_snapshot() -> dict:
    e = valuar(leer(), libro_de_precios())
    nuevo = not HISTORIAL.exists()
    with HISTORIAL.open("a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["fecha", "total_usd", "resultado_pct", "hodl_btc", "hodl_50_50", "usdt", "operaciones"])
        w.writerow([e["fecha"], e["total_usd"], e["resultado_pct"], e["vs"]["hodl_btc"],
                    e["vs"]["hodl_50_btc_50_eth"], e["usdt"], e["operaciones"]])
    return e


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--capital", type=float, default=10_000)
    i.add_argument("--forzar", action="store_true")
    sub.add_parser("mercado")
    sub.add_parser("estado")
    sub.add_parser("snapshot")
    n = sub.add_parser("nota")
    n.add_argument("--texto", required=True)
    o = sub.add_parser("orden")
    o.add_argument("--lado", choices=["buy", "sell"], required=True)
    o.add_argument("--par", required=True)
    o.add_argument("--usd", type=float)
    o.add_argument("--todo", action="store_true")
    o.add_argument("--motivo", required=True)
    a = ap.parse_args(argv)

    try:
        if a.cmd == "init":
            r = cmd_init(a.capital, a.forzar)
        elif a.cmd == "mercado":
            r = cmd_mercado()
        elif a.cmd == "estado":
            r = valuar(leer(), libro_de_precios())
        elif a.cmd == "snapshot":
            r = cmd_snapshot()
        elif a.cmd == "nota":
            if len(a.texto.strip()) < 10:
                raise ErrorPaper("La nota lleva al menos 10 caracteres.")
            leer()
            anotar_diario(f"## {ahora()} — sin operar\n{a.texto.strip()}")
            r = {"anotado": True}
        else:
            r = cmd_orden(a.lado, a.par, a.usd, a.todo, a.motivo)
    except ErrorPaper as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
