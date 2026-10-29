"""Torneo de estrategias cripto: muchas estrategias, mismo capital, mismas velas, mismo costo.

Cada estrategia pertenece a una de las personalidades de las carpetas (prudente = "3 niveles",
agresiva, laboratorio, DCA) y varía monedas, riesgo, stops y plazo. Todas arrancan con el mismo
capital en la misma fecha y se miden contra quedarse en USDT y contra HODL BTC.

Dos modos, el mismo motor:
- `historia`: corre cada estrategia en ventanas de 30 y 90 días desde 2021, ARRANCANDO DE CERO en
  cada ventana (mismo capital), y agrupa los resultados por el régimen de mercado que se veía al
  arrancar (BTC arriba/abajo de su media de 200 días, subiendo/bajando en los 30 días previos).
  Responde "en un mercado como el de hoy, qué funcionó antes". Sin estado: se puede repetir.
- `vivo`: corre las mismas estrategias desde una fecha fija (default 29/10/2026) hasta la última
  vela cerrada. Como son deterministas, "operar en vivo" y "recalcular desde la fecha" dan lo
  mismo: no hay libro que se pueda romper.

Modelo de ejecución (igual para todas): se decide al cierre de una vela de 4 h y se ejecuta en la
apertura de la siguiente, con 0,1% de comisión y 0,05% de deslizamiento por lado. Stops y tomas
se miran contra el mínimo y el máximo de cada vela de 4 h (si una vela toca stop y toma, cuenta
el stop). Las carpetas reales usan velas de 1 h y de 1 min: acá las reglas "1 h" se aproximan
con 4 h, y eso se dice en el reporte.

Sesgo que no se puede sacar: el universo son monedas que hoy siguen grandes (sesgo de
supervivencia). Lo que funcionó con ellas en 2021 se ve mejor de lo que se habría visto.

Uso:
    torneo.py bajar [--desde 2020-06-01] # baja/actualiza velas de 4 h a la caché
    torneo.py historia [--desde 2021-01-01] [--json salida.json]
    torneo.py vivo [--desde 2026-10-29]  # escribe RESUMEN y JSON en TORNEO_DIR
    torneo.py lista                      # las estrategias con su personalidad
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://data-api.binance.vision/api/v3"
CACHE = Path(os.environ.get("TORNEO_CACHE", Path(__file__).resolve().parent / "torneo-cache"))
DIR = Path(os.environ.get("TORNEO_DIR", Path(__file__).resolve().parent / "estado-torneo"))
COMISION = 0.001
DESLIZ = 0.0005
CAPITAL = 1000.0
H4 = 4 * 3600 * 1000
DIA = 24 * 3600 * 1000
INICIO_DATOS = "2020-06-01"
# Existían en Binance antes de 2021 y siguen entre las grandes. Sesgo de supervivencia: ver arriba.
UNIVERSO = ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "LINK", "AVAX", "LTC", "DOT", "TRX",
            "NEAR", "ATOM"]
MAYORES = ["BTC", "ETH", "BNB"]


def ms(fecha: str) -> int:
    return int(datetime.strptime(fecha, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)


def fecha(t: int) -> str:
    return datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


# ---------------------------------------------------------------- datos

def _get(ruta: str, params: dict) -> list:
    q = "&".join(f"{k}={v}" for k, v in params.items())
    for intento in range(4):
        try:
            with urllib.request.urlopen(f"{API}/{ruta}?{q}", timeout=20) as r:
                return json.loads(r.read())
        except Exception:
            if intento == 3:
                raise
            time.sleep(2 * (intento + 1))
    return []


def bajar(inicio: str = INICIO_DATOS) -> dict:
    """Velas de 4 h desde `inicio`, incrementales sobre la caché. Sólo velas CERRADAS."""
    CACHE.mkdir(parents=True, exist_ok=True)
    ahora = int(time.time() * 1000)
    hechas = {}
    for base in UNIVERSO:
        arch = CACHE / f"{base}USDT_4h.json"
        filas = json.loads(arch.read_text()) if arch.exists() else []
        desde = filas[-1][0] + H4 if filas else ms(inicio)
        while desde < ahora:
            k = _get("klines", {"symbol": f"{base}USDT", "interval": "4h", "startTime": desde, "limit": 1000})
            if not k:
                break
            filas += [[int(v[0]), float(v[1]), float(v[2]), float(v[3]), float(v[4]), float(v[7])]
                      for v in k if int(v[6]) < ahora]
            if len(k) < 1000:
                break
            desde = int(k[-1][0]) + H4
        # dedupe por si una corrida previa cortó a mitad
        vistas, limpias = set(), []
        for f in filas:
            if f[0] not in vistas:
                vistas.add(f[0])
                limpias.append(f)
        arch.write_text(json.dumps(limpias))
        hechas[base] = len(limpias)
    return hechas


class Datos:
    """Velas de 4 h alineadas en una grilla común + indicadores diarios precalculados."""

    def __init__(self):
        crudas = {}
        for base in UNIVERSO:
            arch = CACHE / f"{base}USDT_4h.json"
            if not arch.exists():
                raise SystemExit(f"falta {arch}: correr `torneo.py bajar`")
            crudas[base] = {f[0]: f for f in json.loads(arch.read_text())}
        self.t = sorted(crudas["BTC"])
        huecos = [fecha(a) for a, z in zip(self.t, self.t[1:]) if z - a != H4]
        if huecos:  # "24 h" pasarían a contar 28 h en silencio
            raise SystemExit(f"faltan velas de 4 h en la caché después de {huecos[:5]}: borrar torneo-cache y bajar de nuevo")
        self.n = len(self.t)
        self.idx = {t: i for i, t in enumerate(self.t)}
        self.o, self.h, self.l, self.c, self.v = ({b: [None] * self.n for b in UNIVERSO} for _ in range(5))
        for b, filas in crudas.items():
            for i, t in enumerate(self.t):
                f = filas.get(t)
                if f:
                    self.o[b][i], self.h[b][i], self.l[b][i], self.c[b][i], self.v[b][i] = f[1:6]
        # cierre diario = cierre de la vela que abre 20:00 UTC; d_de[i] = último día CERRADO en la vela i
        self.cierre_dia = [i for i, t in enumerate(self.t) if (t % DIA) == 20 * 3600 * 1000]
        self.d_de = [-1] * self.n
        d = -1
        for i in range(self.n):
            if d + 1 < len(self.cierre_dia) and self.cierre_dia[d + 1] == i:
                d += 1
            self.d_de[i] = d
        self.dc = {b: [self.c[b][i] for i in self.cierre_dia] for b in UNIVERSO}
        self.dh = {b: [self._max_dia(b, k) for k in range(len(self.cierre_dia))] for b in UNIVERSO}
        self.dl = {b: [self._min_dia(b, k) for k in range(len(self.cierre_dia))] for b in UNIVERSO}
        self._sma_cache: dict = {}

    def _rango(self, k):
        fin = self.cierre_dia[k]
        return range(max(0, fin - 5), fin + 1)

    def _max_dia(self, b, k):
        xs = [self.h[b][i] for i in self._rango(k) if self.h[b][i] is not None]
        return max(xs) if xs else None

    def _min_dia(self, b, k):
        xs = [self.l[b][i] for i in self._rango(k) if self.l[b][i] is not None]
        return min(xs) if xs else None

    def sma(self, b: str, n: int, d: int):
        """Media de los últimos n cierres diarios hasta el día d inclusive."""
        clave = (b, n)
        if clave not in self._sma_cache:
            xs, acum, out, cuenta = self.dc[b], 0.0, [], 0
            for k, x in enumerate(xs):
                if x is None:
                    acum, cuenta = 0.0, 0
                    out.append(None)
                    continue
                acum += x
                cuenta += 1
                if cuenta > n:
                    acum -= xs[k - n]
                    cuenta = n
                out.append(acum / n if cuenta == n else None)
            self._sma_cache[clave] = out
        return self._sma_cache[clave][d] if d >= 0 else None

    def ret_dias(self, b: str, n: int, d: int):
        if d - n < 0:
            return None
        a, z = self.dc[b][d - n], self.dc[b][d]
        return z / a - 1 if a and z else None

    def rsi(self, b: str, n: int, d: int):
        if d - n < 1:
            return None
        sube = baja = 0.0
        for k in range(d - n + 1, d + 1):
            a, z = self.dc[b][k - 1], self.dc[b][k]
            if a is None or z is None:
                return None
            sube += max(z - a, 0)
            baja += max(a - z, 0)
        return 100.0 if baja == 0 else 100 - 100 / (1 + sube / baja)

    def atr(self, b: str, n: int, d: int):
        if d - n < 1:
            return None
        trs = []
        for k in range(d - n + 1, d + 1):
            h, l, cp = self.dh[b][k], self.dl[b][k], self.dc[b][k - 1]
            if None in (h, l, cp):
                return None
            trs.append(max(h - l, abs(h - cp), abs(l - cp)))
        return sum(trs) / n

    def max_dias(self, b: str, n: int, d: int):
        xs = self.dh[b][max(0, d - n + 1):d + 1]
        return max(xs) if xs and None not in xs else None

    def min_dias(self, b: str, n: int, d: int):
        xs = self.dl[b][max(0, d - n + 1):d + 1]
        return min(xs) if xs and None not in xs else None

    def ret_velas(self, b: str, n: int, i: int):
        if i - n < 0:
            return None
        a, z = self.c[b][i - n], self.c[b][i]
        return z / a - 1 if a and z else None

    def vol_ratio(self, b: str, i: int, n: int = 42):
        """Volumen de la última vela de 4 h contra el promedio de las n anteriores (7 días)."""
        if i - n < 0 or self.v[b][i] is None:
            return None
        xs = [self.v[b][k] for k in range(i - n, i) if self.v[b][k] is not None]
        return self.v[b][i] / (sum(xs) / len(xs)) if xs and sum(xs) else None


# ---------------------------------------------------------------- motor

class Cartera:
    def __init__(self, capital: float):
        self.usdt = capital
        self.pos: dict[str, dict] = {}   # base -> {cant, entrada, maximo, t_entrada, reglas, tp_hechas}
        self.comisiones = 0.0
        self.ops = 0
        self.vueltas: list[float] = []   # resultado % de cada posición cerrada entera

    def valor(self, D: Datos, i: int) -> float:
        return self.usdt + sum(p["cant"] * (D.c[b][i] or p["entrada"]) for b, p in self.pos.items())

    def comprar(self, b: str, usd: float, precio: float, t: int, reglas: dict | None):
        usd = min(usd, self.usdt)
        if usd < 5:
            return
        px = precio * (1 + DESLIZ)
        com = usd * COMISION
        cant = (usd - com) / px
        self.usdt -= usd
        self.comisiones += com
        self.ops += 1
        p = self.pos.get(b)
        if p:
            costo = p["cant"] * p["entrada"] + cant * px
            p["cant"] += cant
            p["entrada"] = costo / p["cant"]
        else:
            self.pos[b] = {"cant": cant, "entrada": px, "maximo": px, "t_entrada": t,
                           "reglas": reglas or {}, "tp_hechas": 0}

    def vender(self, b: str, frac: float, precio: float):
        p = self.pos.get(b)
        if not p:
            return
        cant = p["cant"] * (1.0 if frac >= 0.999 else frac)
        px = precio * (1 - DESLIZ)
        bruto = cant * px
        com = bruto * COMISION
        self.usdt += bruto - com
        self.comisiones += com
        self.ops += 1
        p["cant"] -= cant
        if frac >= 0.999 or p["cant"] * px < 1:
            self.vueltas.append(px / p["entrada"] - 1)
            del self.pos[b]


class Ctx:
    """Lo que ve una estrategia al cierre de la vela i. Las órdenes se ejecutan en i+1."""

    def __init__(self, D: Datos, cart: Cartera, i: int, inicio: int):
        self.D, self.cart, self.i, self.inicio = D, cart, i, inicio
        self.d = D.d_de[i]
        self.es_cierre_dia = D.cierre_dia[self.d] == i if self.d >= 0 else False
        self.ordenes: list = []

    def precio(self, b):
        return self.D.c[b][self.i]

    def total(self):
        return self.cart.valor(self.D, self.i)

    def disponibles(self, monedas):
        return [b for b in monedas if self.D.c[b][self.i] is not None and self.D.dc[b][self.d] is not None]

    def comprar(self, b, usd, **reglas):
        self.ordenes.append(("buy", b, usd, reglas))

    def vender(self, b, frac=1.0):
        self.ordenes.append(("sell", b, frac, None))

    def objetivo(self, pesos: dict[str, float], tolerancia=0.03, **reglas):
        """Lleva la cartera a esos pesos (el resto, USDT). Ignora desvíos menores a la tolerancia."""
        tot = self.total()
        for b in list(self.cart.pos):
            if b not in pesos:
                self.vender(b)
        for b, w in pesos.items():
            actual = self.cart.pos[b]["cant"] * self.precio(b) if b in self.cart.pos else 0.0
            dif = w * tot - actual
            if abs(dif) < tolerancia * tot:
                continue
            if dif < 0:
                self.vender(b, -dif / actual)
            else:
                self.ordenes.append(("buy_last", b, dif, reglas))

    def dias_desde_inicio(self):
        return (self.D.t[self.i] - self.D.t[self.inicio]) / DIA


def vigilar(cart: Cartera, D: Datos, i: int):
    """Stops, trailing, tomas y salida por tiempo contra la vela i (mínimo/máximo)."""
    for b in list(cart.pos):
        p = cart.pos[b]
        r = p["reglas"]
        o, h, l = D.o[b][i], D.h[b][i], D.l[b][i]
        if o is None:
            continue
        niveles = []
        if r.get("stop"):
            niveles.append(p["entrada"] * (1 - r["stop"]))
        if r.get("trail"):
            niveles.append(p["maximo"] * (1 - r["trail"]))
        if r.get("stop_abs"):
            niveles.append(r["stop_abs"])
        if niveles:
            nivel = max(niveles)
            if l <= nivel:
                cart.vender(b, 1.0, min(o, nivel))
                continue
        tps = r.get("tp") or []
        while p["tp_hechas"] < len(tps):
            sube, frac = tps[p["tp_hechas"]]
            objetivo = p["entrada"] * (1 + sube)
            if h < objetivo:
                break
            p["tp_hechas"] += 1
            restante = 1.0 if frac >= 1 else frac
            cart.vender(b, restante, max(o, objetivo))
            if b not in cart.pos:
                break
        if b in cart.pos:
            p["maximo"] = max(p["maximo"], h)
            if r.get("tiempo_h") and (D.t[i] - p["t_entrada"]) >= r["tiempo_h"] * 3600 * 1000 \
                    and p["tp_hechas"] == 0:
                cart.vender(b, 1.0, D.c[b][i])


def correr(est: "Estrategia", D: Datos, inicio: int, fin: int, capital=CAPITAL) -> dict:
    """Corre una estrategia de la vela `inicio` a la `fin` (inclusive) arrancando de cero."""
    est.reiniciar()
    cart = Cartera(capital)
    curva, pisos = [], []
    pendientes: list = []
    for i in range(inicio, fin + 1):
        # 1) ejecutar lo decidido en la vela anterior, a la apertura de ésta
        ventas = [x for x in pendientes if x[0] == "sell"]
        compras = [x for x in pendientes if x[0] != "sell"]
        for _, b, frac, _ in ventas:
            if D.o[b][i] is not None:
                cart.vender(b, frac, D.o[b][i])
        for tipo, b, usd, reglas in compras:
            if D.o[b][i] is not None:
                cart.comprar(b, usd, D.o[b][i], D.t[i], reglas)
        pendientes = []
        # piso de la vela: lo que valía la cartera si todo tocaba su mínimo (antes de los stops,
        # que venden en o arriba del mínimo). Sin esto la caída de las de stops cortos sale chica.
        pisos.append(cart.usdt + sum(p["cant"] * (D.l[b][i] or p["entrada"]) for b, p in cart.pos.items()))
        # 2) stops y tomas durante la vela
        vigilar(cart, D, i)
        # 3) decidir al cierre
        if i < fin:
            ctx = Ctx(D, cart, i, inicio)
            est.decidir(ctx)
            pendientes = ctx.ordenes
        curva.append(cart.valor(D, i))
    pico, peor = capital, 0.0
    for piso, x in zip(pisos, curva):
        peor = min(peor, piso / pico - 1, x / pico - 1)
        pico = max(pico, x)
    # lo que queda si se vende todo al cierre: así las que terminan invertidas pagan su salida
    final = cart.usdt + sum(p["cant"] * D.c[b][fin] * (1 - DESLIZ) * (1 - COMISION) for b, p in cart.pos.items())
    btc0, btc1 = D.o["BTC"][inicio], D.c["BTC"][fin]
    return {"final": final, "ret": final / capital - 1, "dd": peor, "ops": cart.ops,
            "comisiones": cart.comisiones, "hodl_btc": btc1 / btc0 - 1,
            "vueltas": len(cart.vueltas),
            "ganadoras": sum(1 for v in cart.vueltas if v > 0) / len(cart.vueltas) if cart.vueltas else None,
            "posiciones": {b: round(p["cant"] * D.c[b][fin], 2) for b, p in cart.pos.items()},
            "usdt": round(cart.usdt, 2)}


# ---------------------------------------------------------------- estrategias

class Estrategia:
    personalidad = ""
    nombre = ""
    idea = ""

    def reiniciar(self):
        self.s = {}

    def decidir(self, ctx: Ctx):
        raise NotImplementedError


class Hodl(Estrategia):
    def __init__(self, nombre, pesos, idea, personalidad="prudente"):
        self.nombre, self.pesos, self.idea, self.personalidad = nombre, pesos, idea, personalidad

    def decidir(self, ctx):
        if not self.s.get("hecho"):
            ctx.objetivo(self.pesos)
            self.s["hecho"] = True


class Rebalanceo(Estrategia):
    def __init__(self, nombre, pesos, cada_dias, idea, personalidad="prudente"):
        self.nombre, self.pesos, self.cada, self.idea, self.personalidad = nombre, pesos, cada_dias, idea, personalidad

    def decidir(self, ctx):
        if not ctx.es_cierre_dia and self.s.get("ultimo") is not None:
            return
        if self.s.get("ultimo") is None or ctx.dias_desde_inicio() - self.s["ultimo"] >= self.cada:
            ctx.objetivo(self.pesos)
            self.s["ultimo"] = ctx.dias_desde_inicio()


class FiltroMedia(Estrategia):
    """Cada moneda adentro (peso fijo) sólo si cierra arriba de su media de n días; si no, USDT."""

    def __init__(self, nombre, pesos, n, idea, personalidad="prudente", filtro_btc=False):
        self.nombre, self.pesos, self.n, self.idea, self.personalidad = nombre, pesos, n, idea, personalidad
        self.filtro_btc = filtro_btc

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        D, d = ctx.D, ctx.d
        btc_ok = (D.dc["BTC"][d] or 0) > (D.sma("BTC", self.n, d) or math.inf)
        pesos = {}
        for b, w in self.pesos.items():
            m = D.sma(b, self.n, d)
            if m and D.dc[b][d] and D.dc[b][d] > m and (btc_ok or not self.filtro_btc):
                pesos[b] = w
        ctx.objetivo(pesos)


class Cruce(Estrategia):
    """Media corta arriba de la larga = adentro, por moneda, pesos iguales entre las elegidas."""

    def __init__(self, nombre, monedas, corta, larga, idea, personalidad="laboratorio"):
        self.nombre, self.monedas, self.corta, self.larga, self.idea = nombre, monedas, corta, larga, idea
        self.personalidad = personalidad

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        D, d = ctx.D, ctx.d
        w = 1 / len(self.monedas)
        pesos = {}
        for b in ctx.disponibles(self.monedas):
            a, z = D.sma(b, self.corta, d), D.sma(b, self.larga, d)
            if a and z and a > z:
                pesos[b] = w
        ctx.objetivo(pesos)


class Rotacion(Estrategia):
    """Cada `cada` días, se queda con las top-k monedas por retorno de `mirar` días (pesos iguales).
    Con filtro: si BTC está debajo de su media de 200 días, todo a USDT. Con `minimo`: sólo entra
    si el retorno de la moneda es positivo."""

    def __init__(self, nombre, monedas, k, mirar, cada, idea, filtro=False, minimo=None,
                 personalidad="agresiva", stop=None):
        self.nombre, self.monedas, self.k, self.mirar, self.cada = nombre, monedas, k, mirar, cada
        self.idea, self.filtro, self.minimo, self.personalidad, self.stop = idea, filtro, minimo, personalidad, stop

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        hoy = ctx.dias_desde_inicio()
        if self.s.get("ultimo") is not None and hoy - self.s["ultimo"] < self.cada - 0.01:
            return
        self.s["ultimo"] = hoy
        D, d = ctx.D, ctx.d
        if self.filtro and not ((D.dc["BTC"][d] or 0) > (D.sma("BTC", 200, d) or math.inf)):
            ctx.objetivo({})
            return
        rets = [(D.ret_dias(b, self.mirar, d), b) for b in ctx.disponibles(self.monedas)]
        rets = sorted([x for x in rets if x[0] is not None], reverse=True)
        if self.minimo is not None:
            rets = [x for x in rets if x[0] > self.minimo]
        elegidas = [b for _, b in rets[:self.k]]
        reglas = {"stop": self.stop} if self.stop else {}
        ctx.objetivo({b: 0.98 / self.k for b in elegidas}, **reglas)


class Donchian(Estrategia):
    """Ruptura: compra al superar el máximo de `entrada` días; sale al perder el mínimo de
    `salida` días o por trailing de `atr_x` ATR. Tamaño por posición fijo."""

    def __init__(self, nombre, monedas, entrada, salida, tamano, idea, atr_x=None, filtro=False,
                 personalidad="laboratorio"):
        self.nombre, self.monedas, self.entrada, self.salida, self.tamano = nombre, monedas, entrada, salida, tamano
        self.idea, self.atr_x, self.filtro, self.personalidad = idea, atr_x, filtro, personalidad

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        D, d = ctx.D, ctx.d
        btc_ok = not self.filtro or (D.dc["BTC"][d] or 0) > (D.sma("BTC", 200, d) or math.inf)
        tot = ctx.total()
        for b in ctx.disponibles(self.monedas):
            px = D.dc[b][d]
            if b in ctx.cart.pos:
                piso = D.min_dias(b, self.salida, d - 1)
                if piso and px < piso:
                    ctx.vender(b)
                continue
            techo = D.max_dias(b, self.entrada, d - 1)
            if btc_ok and techo and px > techo:
                reglas = {}
                if self.atr_x:
                    a = D.atr(b, 14, d)
                    if a:
                        reglas["trail"] = min(0.5, self.atr_x * a / px)
                ctx.comprar(b, self.tamano * tot, **reglas)


class Reversion(Estrategia):
    """Compra lo que cayó fuerte (RSI diario bajo), vende al recuperarse o por stop."""

    def __init__(self, nombre, monedas, rsi_in, rsi_out, tamano, stop, idea, filtro_tendencia=False,
                 personalidad="laboratorio"):
        self.nombre, self.monedas, self.rsi_in, self.rsi_out, self.tamano, self.stop = \
            nombre, monedas, rsi_in, rsi_out, tamano, stop
        self.idea, self.filtro_tendencia, self.personalidad = idea, filtro_tendencia, personalidad

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        D, d = ctx.D, ctx.d
        tot = ctx.total()
        for b in ctx.disponibles(self.monedas):
            r = D.rsi(b, 14, d)
            if r is None:
                continue
            if b in ctx.cart.pos:
                if r > self.rsi_out:
                    ctx.vender(b)
                continue
            if r < self.rsi_in:
                if self.filtro_tendencia and not (D.dc[b][d] > (D.sma(b, 200, d) or math.inf)):
                    continue
                ctx.comprar(b, self.tamano * tot, stop=self.stop)


class CompraCaida(Estrategia):
    """Compra cuando BTC cae X% desde su máximo de 30 días; vende al recuperar +Y% o por stop."""

    def __init__(self, nombre, caida, sube, tamano, stop, idea, personalidad="prudente"):
        self.nombre, self.caida, self.sube, self.tamano, self.stop, self.idea = nombre, caida, sube, tamano, stop, idea
        self.personalidad = personalidad

    def decidir(self, ctx):
        if not ctx.es_cierre_dia or "BTC" in ctx.cart.pos:
            return
        D, d = ctx.D, ctx.d
        m = D.max_dias("BTC", 30, d)
        if m and D.dc["BTC"][d] < m * (1 - self.caida):
            ctx.comprar("BTC", self.tamano * ctx.total(), stop=self.stop, tp=[(self.sube, 1.0)])


class MomentoCorto(Estrategia):
    """Las reglas de las carpetas Agresiva y Laboratorio, en velas de 4 h (aproximación de las de
    1 h): moneda que viene subiendo fuerte en 24 h, sigue subiendo, con volumen, cerca del máximo."""

    def __init__(self, nombre, monedas, ret24, vs_max, vol, tamano, max_pos, reglas, idea,
                 filtro_btc=None, max_dia=None, personalidad="agresiva"):
        self.nombre, self.monedas, self.ret24, self.vs_max, self.vol = nombre, monedas, ret24, vs_max, vol
        self.tamano, self.max_pos, self.reglas, self.idea = tamano, max_pos, reglas, idea
        self.filtro_btc, self.max_dia, self.personalidad = filtro_btc, max_dia, personalidad

    def decidir(self, ctx):
        D, i = ctx.D, ctx.i
        if len(ctx.cart.pos) >= self.max_pos:
            return
        if self.filtro_btc:
            r24, r4 = D.ret_velas("BTC", 6, i), D.ret_velas("BTC", 1, i)
            if r24 is None or r24 < self.filtro_btc[0] or r4 < self.filtro_btc[1]:
                return
        dia = D.t[i] // DIA
        if self.max_dia and self.s.get("dia") == dia and self.s.get("n", 0) >= self.max_dia:
            return
        candidatas = []
        for b in self.monedas:
            if b in ctx.cart.pos or D.c[b][i] is None:
                continue
            r24, r4, vr = D.ret_velas(b, 6, i), D.ret_velas(b, 1, i), D.vol_ratio(b, i)
            hs = [D.h[b][k] for k in range(max(0, i - 11), i + 1) if D.h[b][k] is not None]
            if None in (r24, r4, vr) or not hs:
                continue
            if r24 >= self.ret24 and r4 > 0 and D.c[b][i] / max(hs) - 1 >= self.vs_max and vr >= self.vol:
                candidatas.append((vr, b))
        if candidatas:
            b = max(candidatas)[1]
            ctx.comprar(b, self.tamano * ctx.total(), **self.reglas)
            if self.s.get("dia") != dia:
                self.s["dia"], self.s["n"] = dia, 0
            self.s["n"] = self.s.get("n", 0) + 1


class DCA(Estrategia):
    """Compra fija cada 7 días hasta gastar el capital. `inteligente`: x2 debajo de la media de
    200 días de BTC, x0,5 si está más de 30% arriba."""

    def __init__(self, nombre, pesos, cuota, idea, inteligente=False):
        self.nombre, self.pesos, self.cuota, self.idea, self.inteligente = nombre, pesos, cuota, idea, inteligente
        self.personalidad = "dca"

    def decidir(self, ctx):
        if not ctx.es_cierre_dia:
            return
        hoy = ctx.dias_desde_inicio()
        if self.s.get("ultimo") is not None and hoy - self.s["ultimo"] < 6.99:
            return
        self.s["ultimo"] = hoy
        cuota = self.cuota
        if self.inteligente:
            D, d = ctx.D, ctx.d
            m, px = D.sma("BTC", 200, d), D.dc["BTC"][d]
            if m and px < m:
                cuota *= 2
            elif m and px > m * 1.3:
                cuota *= 0.5
        for b, w in self.pesos.items():
            ctx.comprar(b, cuota * w)


class ConNoticias(Estrategia):
    """La misma estrategia, pero con freno de noticias: si la última lectura de noticias anterior a
    la vela es `riesgo_fuera`, se pasa todo a USDT y no se abre nada hasta que cambie. Sólo existe
    en `vivo`: las noticias no se pueden reconstruir hacia atrás sin mirar el futuro."""

    def __init__(self, base: Estrategia, lecturas: list[dict]):
        self.base, self.lecturas = base, sorted(lecturas, key=lambda x: x["t"])
        self.nombre, self.personalidad = base.nombre.split(" ", 1)[0] + "N " + base.nombre.split(" ", 1)[1] + \
            " + freno de noticias", base.personalidad
        self.idea = base.idea + " Con freno de noticias."

    def reiniciar(self):
        self.s = {}
        self.base.reiniciar()

    def decidir(self, ctx):
        t = ctx.D.t[ctx.i] + H4  # la lectura vale si se escribió antes del cierre de la vela
        sesgo = None
        for x in self.lecturas:
            if x["t"] <= t:
                sesgo = x["sesgo"]
        if sesgo == "riesgo_fuera":
            ctx.objetivo({})
            return
        self.base.decidir(ctx)


def leer_noticias() -> list[dict]:
    """`noticias.jsonl` en TORNEO_DIR: una línea por lectura, {"fecha": "YYYY-MM-DD HH:MM", "sesgo":
    "riesgo_dentro"|"neutral"|"riesgo_fuera", "motivo": ..., "fuentes": [...]}. Fecha en UTC."""
    arch = DIR / "noticias.jsonl"
    if not arch.exists():
        return []
    out = []
    for linea in arch.read_text().splitlines():
        if not linea.strip():
            continue
        x = json.loads(linea)
        if x.get("sesgo") not in ("riesgo_dentro", "neutral", "riesgo_fuera"):
            raise SystemExit(f"noticias.jsonl: sesgo inválido en {linea[:80]}")
        x["t"] = int(datetime.strptime(x["fecha"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp() * 1000)
        out.append(x)
    return out


TOP = UNIVERSO
MEDIANAS = ["SOL", "XRP", "ADA", "DOGE", "LINK", "AVAX", "LTC", "DOT", "TRX", "NEAR", "ATOM"]
REGLAS_AGRESIVA = {"stop": 0.05, "trail": 0.05, "tp": [(0.08, 0.5), (0.15, 1.0)]}
REGLAS_LAB = {"stop": 0.07, "trail": 0.08, "tp": [(0.10, 0.5), (0.20, 1.0)], "tiempo_h": 48}


def estrategias() -> list[Estrategia]:
    return [
        # --- prudente (la personalidad de "3 niveles"): poco movimiento, monedas grandes
        Hodl("P0 USDT quieto", {}, "Referencia: no hacer nada."),
        Hodl("P1 HODL BTC", {"BTC": 0.999}, "Referencia: comprar BTC y no tocar."),
        Hodl("P2 HODL 50/50 BTC-ETH", {"BTC": 0.5, "ETH": 0.499}, "Referencia de las carpetas."),
        Rebalanceo("P3 canasta BTC/ETH/BNB rebalanceo mensual", {"BTC": 0.5, "ETH": 0.3, "BNB": 0.19}, 30,
                   "Lo conservador de 3 niveles, sin tocar más que una vez por mes."),
        Rebalanceo("P4 60% BTC / 40% USDT rebalanceo mensual", {"BTC": 0.6}, 30,
                   "Medio riesgo: vende cuando sube, compra cuando baja."),
        FiltroMedia("P5 BTC sólo arriba de su media de 200 d", {"BTC": 0.99}, 200,
                    "Afuera en los bajistas largos, adentro en los alcistas."),
        FiltroMedia("P6 BTC sólo arriba de su media de 100 d", {"BTC": 0.99}, 100, "Igual que P5, más rápido."),
        FiltroMedia("P7 canasta grande con media de 200 d por moneda", {b: 0.99 / 3 for b in MAYORES}, 200,
                    "Cada grande entra o sale según su propia tendencia."),
        CompraCaida("P8 compra BTC tras caer 15% (vende +10%)", 0.15, 0.10, 0.5, 0.15,
                    "Comprar el miedo, con stop."),
        # --- agresiva: rota rápido, busca lo que más sube
        MomentoCorto("A1 reglas de la Agresiva actual (4 h)", TOP, 0.05, -0.03, 1.0, 0.2, 5, REGLAS_AGRESIVA,
                     "Lo que hace hoy la carpeta Agresiva, en velas de 4 h."),
        MomentoCorto("A2 Agresiva con filtro BTC y stops anchos", TOP, 0.05, -0.03, 1.3, 0.2, 3,
                     {"stop": 0.10, "trail": 0.12, "tp": [(0.20, 0.5), (0.40, 1.0)]},
                     "Misma idea, sin operar cuando BTC cae y dejando correr la ganancia.",
                     filtro_btc=(-0.02, -0.015)),
        Rotacion("A3 la que más subió en 7 d, rota cada día", TOP, 1, 7, 1, "Todo a la más fuerte."),
        Rotacion("A4 top 3 por 30 d, rota cada semana", TOP, 3, 30, 7, "Momentum clásico."),
        Rotacion("A5 top 3 por 30 d, semanal, sólo con BTC alcista", TOP, 3, 30, 7,
                 "Momentum con freno de mercado.", filtro=True),
        Rotacion("A6 top 3 por 30 d, semanal, filtro + sólo si suben", TOP, 3, 30, 7,
                 "Momentum con freno y sin comprar lo que baja.", filtro=True, minimo=0.0),
        Rotacion("A7 top 5 por 90 d, mensual, con filtro", TOP, 5, 90, 30, "Momentum lento.", filtro=True),
        Rotacion("A8 medianas top 2 por 14 d, semanal, filtro, stop 15%", MEDIANAS, 2, 14, 7,
                 "Riesgo alto: sólo medianas.", filtro=True, minimo=0.0, stop=0.15),
        # --- laboratorio: tendencia, pocas entradas, reglas escritas
        MomentoCorto("L1 reglas del Laboratorio v1 (4 h)", TOP, 0.03, -0.015, 1.3, 0.2, 3, REGLAS_LAB,
                     "Lo que hace hoy el Laboratorio, en velas de 4 h.", filtro_btc=(-0.02, -0.015), max_dia=4,
                     personalidad="laboratorio"),
        Cruce("L2 cruce de medias 20/50 en las grandes", MAYORES, 20, 50, "Tendencia media."),
        Cruce("L3 cruce de medias 50/200 en BTC", ["BTC"], 50, 200, "Cruz dorada / de la muerte."),
        Cruce("L4 cruce 20/50 en las 14", TOP, 20, 50, "Tendencia media, todo el universo."),
        Donchian("L5 ruptura de 20 d en las grandes, sale en 10 d", MAYORES, 20, 10, 0.33,
                 "Sigue rupturas cortas."),
        Donchian("L6 ruptura de 55 d (tortugas), sale en 20 d, 14 monedas", TOP, 55, 20, 0.15,
                 "Sistema de las tortugas.", atr_x=3),
        Donchian("L7 ruptura de 20 d con filtro BTC, 14 monedas", TOP, 20, 10, 0.15,
                 "Rupturas sólo con mercado alcista.", atr_x=2.5, filtro=True),
        Reversion("L8 compra pánico (RSI<30), vende RSI>55, grandes", MAYORES, 30, 55, 0.33, 0.12,
                  "Contra la corriente."),
        Reversion("L9 compra pánico sólo en tendencia alcista, 14 monedas", TOP, 35, 60, 0.2, 0.10,
                  "Comprar la baja dentro de una suba.", filtro_tendencia=True),
        # --- DCA: compra fija, no vende
        DCA("D1 DCA BTC 100 por semana", {"BTC": 1.0}, 100, "Lo que hace hoy la carpeta DCA."),
        DCA("D2 DCA 50/50 BTC-ETH 100 por semana", {"BTC": 0.5, "ETH": 0.5}, 100, "DCA repartido."),
        DCA("D3 DCA inteligente BTC (x2 abajo de la media 200)", {"BTC": 1.0}, 100,
            "Compra más cuando está barato.", inteligente=True),
        DCA("D4 DCA BTC 77 por semana (todo en 13 semanas)", {"BTC": 1.0}, 1000 / 13, "Reparte el capital en 13 semanas."),
    ]


# ---------------------------------------------------------------- régimen

def regimen(D: Datos, i: int) -> str:
    """Lo que se veía al arrancar (sin mirar el futuro): BTC vs su media de 200 d y su retorno 30 d."""
    d = D.d_de[i]
    m, px, r30 = D.sma("BTC", 200, d), D.dc["BTC"][d], D.ret_dias("BTC", 30, d)
    if m is None or r30 is None:
        return "sin dato"
    arriba = "BTC arriba de la media 200" if px > m else "BTC abajo de la media 200"
    sube = "subiendo 30 d" if r30 > 0 else "bajando 30 d"
    return f"{arriba}, {sube}"


# ---------------------------------------------------------------- modos

def _pct(x):
    return f"{x * 100:+.1f}%" if x is not None else "—"


def historia(desde: str, salida: str | None) -> dict:
    D = Datos()
    ests = estrategias()
    i0 = D.idx.get(ms(desde)) or next(i for i, t in enumerate(D.t) if t >= ms(desde))
    corte_oos = ms("2025-01-01")
    res = {"generado": fecha(int(time.time() * 1000)), "desde": desde, "hasta": fecha(D.t[-1]),
           "hoy": regimen(D, D.n - 1), "ventanas": {}}
    for dias, paso in ((30, 15), (90, 30)):
        largo = dias * 6
        filas = []
        for ini in range(i0, D.n - largo, paso * 6):
            fin = ini + largo - 1
            reg = regimen(D, ini)
            por = {}
            for e in ests:
                r = correr(e, D, ini, fin)
                por[e.nombre] = {k: r[k] for k in ("ret", "dd", "ops", "comisiones", "hodl_btc")}
            filas.append({"inicio": fecha(D.t[ini]), "regimen": reg, "oos": D.t[ini] >= corte_oos, "res": por})
            print(f"  {dias} d · {fecha(D.t[ini])} · {reg}", file=sys.stderr)
        res["ventanas"][str(dias)] = filas
    res["resumen"] = resumir(res, ests)
    if salida:
        Path(salida).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def _agregar(filas, nombre):
    rs = [f["res"][nombre]["ret"] for f in filas]
    if not rs:
        return None
    # contra la misma estrategia HODL BTC (mismo costo y mismo momento de entrada), no contra el precio crudo
    hodl = [f["res"]["P1 HODL BTC"]["ret"] for f in filas]
    rs_ord = sorted(rs)
    return {"n": len(rs), "mediana": statistics.median(rs), "media": statistics.mean(rs),
            "peor_10": statistics.quantiles(rs, n=10, method="inclusive")[0] if len(rs) >= 2 else rs_ord[0],
            "positivas": sum(1 for r in rs if r > 0) / len(rs),
            "le_gana_a_usdt_y_btc": sum(1 for r, h in zip(rs, hodl) if r > 0 and r > h + 1e-9) / len(rs),
            "llega_20": sum(1 for r in rs if r >= 0.20) / len(rs),
            "dd_mediana": statistics.median(f["res"][nombre]["dd"] for f in filas),
            "ops_mediana": statistics.median(f["res"][nombre]["ops"] for f in filas)}


def resumir(res, ests) -> dict:
    out = {}
    for dias, filas in res["ventanas"].items():
        regs = sorted({f["regimen"] for f in filas})
        bloque = {"todas": {}, "dentro_muestra": {}, "fuera_muestra": {}, "por_regimen": {r: {} for r in regs}}
        for e in ests:
            bloque["todas"][e.nombre] = _agregar(filas, e.nombre)
            bloque["dentro_muestra"][e.nombre] = _agregar([f for f in filas if not f["oos"]], e.nombre)
            bloque["fuera_muestra"][e.nombre] = _agregar([f for f in filas if f["oos"]], e.nombre)
            for r in regs:
                bloque["por_regimen"][r][e.nombre] = _agregar([f for f in filas if f["regimen"] == r], e.nombre)
        out[dias] = bloque
    return out


def con_noticias(ests: list[Estrategia]) -> list[Estrategia]:
    """Las tres que se duplican con freno de noticias: una por personalidad que puede salirse."""
    lect = leer_noticias()
    base = {e.nombre.split(" ", 1)[0]: e for e in ests}
    return ests + [ConNoticias(copy.deepcopy(base[k]), lect) for k in ("P5", "A5", "L1")]


def vivo(desde: str) -> dict:
    D = Datos()
    ests = con_noticias(estrategias())
    inicio = next((i for i, t in enumerate(D.t) if t >= ms(desde)), D.n)
    fin = D.n - 1
    if fin <= inicio:  # recién arrancado: no es una falla, pero tampoco hay tabla que mostrar
        DIR.mkdir(parents=True, exist_ok=True)
        (DIR / "RESUMEN.md").write_text(f"# Torneo cripto en vivo\n\nArranca el {desde}: todavía no cerró "
                                        f"ninguna vela de 4 h desde entonces (última: {fecha(D.t[fin])} UTC).\n")
        return {"hasta": fecha(D.t[fin] + H4), "filas": [{"estrategia": "ninguna todavía", "final": CAPITAL}]}
    filas = []
    for e in ests:
        r = correr(e, D, inicio, fin)
        filas.append({"estrategia": e.nombre, "personalidad": e.personalidad, **r})
    filas.sort(key=lambda x: -x["final"])
    out = {"generado": fecha(int(time.time() * 1000)), "desde": fecha(D.t[inicio]), "hasta": fecha(D.t[fin] + H4),
           "regimen_hoy": regimen(D, fin), "capital": CAPITAL, "filas": filas}
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "vivo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    lineas = [f"# Torneo cripto en vivo — {out['hasta']} UTC", "",
              f"Todas arrancaron con **{CAPITAL:,.0f} USD** el {out['desde']} UTC, mismas velas de 4 h y mismo costo "
              f"(0,1% + 0,05% por lado). Mercado hoy: **{out['regimen_hoy']}**. Plata ficticia.", "",
              "| # | Estrategia | Personalidad | USD | Resultado | Peor caída | Ops |", "|---:|---|---|---:|---:|---:|---:|"]
    for k, f in enumerate(filas, 1):
        lineas.append(f"| {k} | {f['estrategia']} | {f['personalidad']} | {f['final']:,.2f} | {_pct(f['ret'])} | "
                      f"{_pct(f['dd'])} | {f['ops']} |")
    p1 = next(f for f in filas if f["estrategia"].startswith("P1 "))
    lineas += ["", f"Le ganan a USDT y a HODL BTC (P1, {_pct(p1['ret'])}): "
               f"{sum(1 for f in filas if f['ret'] > 0 and f['ret'] > p1['ret'])} de {len(filas)}. "
               "Qué funcionó antes en cada tipo de mercado: `HISTORIA.md`."]
    (DIR / "RESUMEN.md").write_text("\n".join(lineas) + "\n")
    return out


def escribir_historia_md(res: dict, destino: Path, ests) -> None:
    per = {e.nombre: e.personalidad for e in ests}
    L = [f"# Torneo cripto — qué funcionó antes, según el mercado", "",
         f"Generado {res['generado']} UTC con velas de 4 h de Binance, {res['desde']} → {res['hasta']}. "
         f"Cada ventana arranca **de cero con 1.000 USD**; mismo costo para todas (0,1% + 0,05% por lado). "
         f"Ventanas de 30 días (cada 15) y de 90 días (cada 30).", "",
         f"**Mercado hoy: {res['hoy']}.**", "",
         "Columnas: *mediana* = el resultado típico de una ventana; *peor 10%* = lo que pasa en una ventana mala; "
         "*le gana* = % de ventanas que terminan arriba de USDT **y** de HODL BTC; *+20%* = % de ventanas que "
         "llegan a +20%; *caída* = peor caída típica dentro de la ventana.", "",
         "> Límites: universo de 14 monedas que hoy siguen grandes (sesgo de supervivencia); reglas de 1 h "
         "aproximadas con velas de 4 h; noticias no se pueden reconstruir hacia atrás. Elegir la mejor de 30 "
         "sobre el pasado sobreajusta: por eso se muestra aparte 2025-2026 (fuera de muestra). Las ventanas se "
         "superponen (cada día cae en 2 de 30 d y en 3 de 90 d): los % no son observaciones independientes, y un "
         "bloque con menos de 15 ventanas es una pista, no una prueba.", ""]

    def tabla(bloque, titulo, top=None):
        filas = [(n, a) for n, a in bloque.items() if a]
        filas.sort(key=lambda x: -x[1]["mediana"])
        if top:
            filas = filas[:top]
        n = filas[0][1]["n"] if filas else 0
        L.extend([f"### {titulo} ({n} ventanas)", "",
                  "| Estrategia | Personalidad | Mediana | Peor 10% | Positivas | Le gana | +20% | Caída | Ops |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|"])
        for nombre, a in filas:
            L.append(f"| {nombre} | {per[nombre]} | {_pct(a['mediana'])} | {_pct(a['peor_10'])} | "
                     f"{a['positivas'] * 100:.0f}% | {a['le_gana_a_usdt_y_btc'] * 100:.0f}% | "
                     f"{a['llega_20'] * 100:.0f}% | {_pct(a['dd_mediana'])} | {a['ops_mediana']:.0f} |")
        L.append("")

    for dias in ("30", "90"):
        b = res["resumen"][dias]
        L.append(f"## Ventanas de {dias} días")
        L.append("")
        hoy = b["por_regimen"].get(res["hoy"])
        if hoy:
            tabla(hoy, f"En un mercado como el de hoy — {res['hoy']}")
        tabla(b["todas"], "Todas las ventanas")
        tabla(b["fuera_muestra"], "Sólo 2025-2026 (fuera de muestra)")
        for reg, bl in b["por_regimen"].items():
            if reg != res["hoy"] and reg != "sin dato":
                tabla(bl, reg, top=10)
    destino.write_text("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bajar")
    b.add_argument("--desde", default=INICIO_DATOS, help="en la nube alcanza con ~8 meses antes de `vivo --desde`")
    sub.add_parser("lista")
    h = sub.add_parser("historia")
    h.add_argument("--desde", default="2021-01-01")
    h.add_argument("--json")
    v = sub.add_parser("vivo")
    v.add_argument("--desde", default="2026-10-29")
    a = ap.parse_args()
    if a.cmd == "bajar":
        print(json.dumps(bajar(a.desde)))
    elif a.cmd == "lista":
        for e in estrategias():
            print(f"{e.personalidad:12} {e.nombre} — {e.idea}")
    elif a.cmd == "historia":
        res = historia(a.desde, a.json)
        DIR.mkdir(parents=True, exist_ok=True)
        escribir_historia_md(res, DIR / "HISTORIA.md", estrategias())
        print(f"listo: {DIR / 'HISTORIA.md'}")
    elif a.cmd == "vivo":
        out = vivo(a.desde)
        f = out["filas"][0]
        print(f"TORNEO_OK hasta={out['hasta']} lider=\"{f['estrategia']}\" {f['final']:.2f}")


if __name__ == "__main__":
    main()
