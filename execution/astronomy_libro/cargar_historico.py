"""Carga historico.json (lo que genera build_historico.py) en `libro_historico` de la base
de Astronomy (qeakrjnseboiulcojlcw). Recarga ENTERA: borra y vuelve a insertar, porque la
tabla es una copia de la fuente y no tiene trabajo humano adentro.

Después de cargar cuenta filas y suma pesos por cierre CONTRA EL ARCHIVO: si no dan igual,
sale con error (una carga a medias es peor que ninguna).

Uso: .venv/bin/python execution/astronomy_libro/cargar_historico.py
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REF = "qeakrjnseboiulcojlcw"  # Astronomy. NO es la base del Paseo.


def env_app():
    p = Path.home() / "Desktop/Productoras/Astronomy/Academia/astronomy-members/.env.local"
    out = {}
    for line in p.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


E = env_app()
URL, KEY = E["NEXT_PUBLIC_SUPABASE_URL"], E["SUPABASE_SERVICE_ROLE_KEY"]
assert REF in URL, f"La URL de Supabase no es la de Astronomy: {URL}"
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def req(method, path, body=None, extra=None):
    r = urllib.request.Request(f"{URL}/rest/v1/{path}", method=method,
                               data=json.dumps(body).encode() if body is not None else None,
                               headers={**H, **(extra or {})})
    with urllib.request.urlopen(r) as resp:
        return resp.read().decode(), resp.headers


def main():
    rows = json.load(open(AQUI / "historico.json"))
    campos = ("cierre", "fecha", "unidad", "caja", "clase", "operativo", "categoria", "concepto",
              "persona", "ars", "usd", "nota", "fuente")
    rows = [{k: r.get(k) if k != "caja" else r.get("caja") for k in campos} for r in rows]
    for r in rows:
        for k in ("categoria", "concepto", "persona", "nota"):
            r[k] = str(r[k] or "")
    req("DELETE", "libro_historico?id=gte.0")
    for i in range(0, len(rows), 500):
        req("POST", "libro_historico", rows[i:i + 500], {"Prefer": "return=minimal"})
    # verificación: filas y pesos por cierre, base contra archivo
    _, h = req("HEAD", "libro_historico?select=id", extra={"Prefer": "count=exact"})
    n = int(h["Content-Range"].split("/")[1])
    got = {}
    for c in (1, 2, 3, 4):
        off, tot = 0, 0.0
        while True:  # PostgREST corta en 1000
            body, _ = req("GET", f"libro_historico?select=ars&cierre=eq.{c}&order=id&offset={off}&limit=1000")
            b = json.loads(body); tot += sum(float(x["ars"]) for x in b)
            if len(b) < 1000: break
            off += 1000
        got[c] = round(tot, 2)
    want = {c: round(sum(r["ars"] for r in rows if r["cierre"] == c), 2) for c in (1, 2, 3, 4)}
    print("filas en la base", n, "· en el archivo", len(rows))
    for c in (1, 2, 3, 4):
        print(f"  cierre {c}: base {got[c]:,.2f} · archivo {want[c]:,.2f}")
    if n != len(rows) or any(abs(got[c] - want[c]) > 0.01 for c in got):
        sys.exit("LA CARGA NO COINCIDE CON EL ARCHIVO")
    print("CARGA OK")


if __name__ == "__main__":
    main()
