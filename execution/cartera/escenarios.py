#!/usr/bin/env python3
"""Todas las cajas cripto llevadas a un total de 10.000 USD. Plata FICTICIA.

Lleva cada caja a 10.000 con una regla de tres sobre su resultado real, y arma mezclas que
reparten 10.000 entre las cajas. No simula operaciones: el tamaño de orden no cambia nada acá.
Lee las ramas con `git show`, así corre igual en la Mac y en la rutina del juez (sólo stdlib).

    python3 execution/cartera/escenarios.py

Si falta un dato, la fila y las mezclas que lo usan dicen `falta`: nunca se reparte lo que
falta entre las demás cajas, porque daría un total que parece bueno y no lo es.
"""
from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
from datetime import datetime
from statistics import mean

TOTAL = 10_000.0
VENTANA = datetime(2026, 10, 29, 0, 0)  # largada del Torneo, la última: desde acá corren todas
MIN_ESTRATEGIAS = 30  # con menos, vivo.json está incompleto y su promedio no es el del Torneo

# caja -> (rama, archivo, capital con el que arrancó)
CAJAS = {
    "Original": ("claude/cartera-original", "historial.csv", 10_000.0),
    "3 niveles": ("claude/cartera-cripto", "execution/cartera/estado/historial.csv", 1_000.0),
    "Agresiva": ("claude/cartera-agresiva", "execution/cartera/estado-agresiva/historial.csv", 1_000.0),
    "Laboratorio": ("claude/cartera-laboratorio", "execution/cartera/estado-laboratorio/historial.csv", 1_000.0),
    "DCA": ("claude/cartera-dca", "execution/cartera/estado-dca/historial.csv", 1_000.0),
}
VIVO = ("claude/cartera-torneo", "execution/cartera/estado-torneo/vivo.json")
TORNEO = "Torneo (promedio)"

MEZCLAS = {
    "Sin 3 niveles ni Agresiva": {"Laboratorio": 0.4, TORNEO: 0.3, "Original": 0.3},
    "Parejo": {c: 1 / 6 for c in ("Original", "3 niveles", "Agresiva", "Laboratorio", "DCA", TORNEO)},
    "Prudente": {"Original": 0.4, "3 niveles": 0.3, "Laboratorio": 0.2, "Agresiva": 0.1},
    "Agresivo": {"Agresiva": 0.5, TORNEO: 0.3, "Laboratorio": 0.2},
}


def fecha(texto: str) -> datetime:
    return datetime.strptime(texto.replace(" UTC", "").strip(), "%Y-%m-%d %H:%M")


def leer_csv(texto: str) -> list[dict]:
    filas = [{"fecha": fecha(r["fecha"]), "total": float(r["total_usd"]), "hodl": float(r["hodl_btc"])}
             for r in csv.DictReader(io.StringIO(texto))]
    return sorted(filas, key=lambda r: r["fecha"])


def caja(filas: list[dict], capital: float) -> dict:
    """Resultado desde el inicio y desde VENTANA.

    Falta si no hay fila anterior a VENTANA, y también si la caja se frenó antes: comparar la
    última fila consigo misma daría +0,00%, como si hubiera estado quieta en USDT.
    """
    if not filas:
        return {"inicio": None, "ventana": None, "dato": None}
    ultima = filas[-1]
    previas = [r for r in filas if r["fecha"] <= VENTANA]
    corre = previas and ultima["fecha"] > VENTANA
    return {"inicio": ultima["total"] / capital - 1,
            "ventana": ultima["total"] / previas[-1]["total"] - 1 if corre else None,
            "dato": ultima["fecha"]}


def torneo(vivo: dict) -> dict:
    filas = vivo.get("filas", [])
    if len(filas) < MIN_ESTRATEGIAS:
        return {"inicio": None, "ventana": None, "dato": None, "n": len(filas)}
    rets = [f["ret"] for f in filas]
    return {"inicio": mean(rets), "ventana": mean(rets), "dato": fecha(vivo["generado"]), "n": len(filas),
            "mejor": max(filas, key=lambda f: f["ret"]), "peor": min(filas, key=lambda f: f["ret"])}


def hodl_ventana(filas: list[dict]) -> float | None:
    previas = [r for r in filas if r["fecha"] <= VENTANA]
    if not previas or filas[-1]["fecha"] <= VENTANA:
        return None
    return filas[-1]["hodl"] / previas[-1]["hodl"] - 1


def mezcla(pesos: dict, resultados: dict) -> float | None:
    """Valor final de repartir TOTAL según pesos, o None si falta alguna caja."""
    if abs(sum(pesos.values()) - 1) > 1e-9:
        raise ValueError(f"los pesos suman {sum(pesos.values())}, no 1")
    valor = 0.0
    for nombre, peso in pesos.items():
        ret = resultados.get(nombre, {}).get("ventana")
        if ret is None:
            return None
        valor += TOTAL * peso * (1 + ret)
    return valor


def usd(ret: float | None) -> str:
    return "falta" if ret is None else f"{TOTAL * (1 + ret):,.0f}".replace(",", ".")


def pct(ret: float | None) -> str:
    return "falta" if ret is None else f"{ret:+.2%}".replace(".", ",")


def informe(resultados: dict, hodl: float | None) -> str:
    salida = [f"Todo llevado a 10.000 USD. La ventana común arranca el {VENTANA:%d/%m/%Y} (largada del Torneo).",
              "", "| Caja | Desde su inicio | Desde la ventana | Dato al |", "|---|---:|---:|---|"]
    orden = sorted(resultados, key=lambda c: -(resultados[c]["ventana"] if resultados[c]["ventana"] is not None else -9))
    for nombre in orden:
        r = resultados[nombre]
        dato = f"{r['dato']:%d/%m %H:%M}" if r["dato"] else "falta"
        salida.append(f"| {nombre} | {usd(r['inicio'])} ({pct(r['inicio'])}) "
                      f"| {usd(r['ventana'])} ({pct(r['ventana'])}) | {dato} |")
    salida += [f"| *Quedarse en USDT* | — | {usd(0.0)} ({pct(0.0)}) | — |",
               f"| *HODL BTC* | — | {usd(hodl)} ({pct(hodl)}) | — |", "",
               "| Reparto de 10.000 | Pesos | Hoy | Resultado |", "|---|---|---:|---:|"]
    for nombre, pesos in MEZCLAS.items():
        valor = mezcla(pesos, resultados)
        ret = None if valor is None else valor / TOTAL - 1
        detalle = ", ".join(f"{p:.0%} {c}" for c, p in pesos.items())
        salida.append(f"| {nombre} | {detalle} | {usd(ret)} | {pct(ret)} |")
    t = resultados[TORNEO]
    if t.get("mejor"):
        salida += ["", f"Torneo, {t['n']} estrategias: mejor {t['mejor']['estrategia']} {usd(t['mejor']['ret'])}; "
                       f"peor {t['peor']['estrategia']} {usd(t['peor']['ret'])}."]
    salida += ["", "Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. "
                   "El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye "
                   "esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT."]
    return "\n".join(salida)


def git_show(rama: str, ruta: str) -> str | None:
    p = subprocess.run(["git", "show", f"origin/{rama}:{ruta}"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def main() -> int:
    # `git show origin/...` lee refs locales: sin esto, en la Mac daría números viejos.
    if subprocess.run(["git", "fetch", "-q", "origin"], capture_output=True).returncode != 0:
        print("AVISO: no se pudo actualizar desde origin; mirá la columna «Dato al».", file=sys.stderr)
    resultados, filas_ref = {}, []
    for nombre, (rama, ruta, capital) in CAJAS.items():
        texto = git_show(rama, ruta)
        filas = leer_csv(texto) if texto else []
        resultados[nombre] = caja(filas, capital)
        if nombre == "3 niveles":
            filas_ref = filas
    texto = git_show(*VIVO)
    resultados[TORNEO] = torneo(json.loads(texto) if texto else {})
    print(informe(resultados, hodl_ventana(filas_ref)))
    faltan = [c for c, r in resultados.items() if r["ventana"] is None]
    if faltan:
        print(f"\nFALTA EL DATO DE: {', '.join(faltan)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
