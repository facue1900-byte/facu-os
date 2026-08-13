#!/usr/bin/env python3
"""Manda a su renglón los egresos que habían caído en «Otros».

La categoría no la elige este script: se la pregunta al **parser de la app**, que
es el que ya sabe las reglas nuevas. Así no hay dos criterios distintos — si
mañana Facu carga «pagué a Daniel», la app y este arreglo van a coincidir.

Escribe en los dos lados, porque son dos sistemas: la base (Supabase) y la hoja
`Movimientos` del contador, que se ubica por el id de la columna K.

    recategorizar.py            dice qué haría
    recategorizar.py --send     lo aplica
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

MP = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
REF = "wujutradczplokjrgmdo"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
TOKEN = next(l.split("=", 1)[1].strip() for l in
             open("/Users/Facu/facu-os/.env", encoding="utf-8")
             if l.startswith("SUPABASE_ACCESS_TOKEN="))


def sql(q):
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://api.supabase.com/v1/projects/{REF}/database/query",
         "-H", f"Authorization: Bearer {TOKEN}", "-H", "Content-Type: application/json",
         "-d", json.dumps({"query": q})], capture_output=True, text=True, env=dict(os.environ))
    return json.loads(out.stdout)


def categorias_del_parser(movs):
    """Le pregunta al parser de la app qué categoría le corresponde a cada obs."""
    entrada = json.dumps([{"id": m["id"], "obs": m["obs"]} for m in movs])
    js = """
    import { parseLineaCaja } from "%s/build/lib/parseCaja.js";
    const movs = JSON.parse(process.argv[1]);
    const out = movs.map((m) => {
      const d = parseLineaCaja(m.obs, [], "2026-08-13");
      return { id: m.id, categoria: d && d.tipo === "Egreso" ? d.categoria : null,
               aRevisar: d ? d.aRevisar : true };
    });
    console.log(JSON.stringify(out));
    """ % SCRATCH
    r = subprocess.run(["node", "--input-type=module", "-e", js, entrada],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"el parser falló:\n{r.stderr[:400]}")
    return {x["id"]: x for x in json.loads(r.stdout)}


def main():
    send = "--send" in sys.argv
    movs = sql("select id::text, fecha::text, categoria, monto::float8, obs "
               "from movimientos where tipo='Egreso' and (categoria='Otros' or a_revisar) "
               "order by fecha")
    dictamen = categorias_del_parser(movs)

    cambios = []
    print(f"{'fecha':11} {'monto':>14}  {'ahora':<12} → {'queda en':<28} nota")
    for m in movs:
        d = dictamen[m["id"]]
        nueva = d["categoria"]
        if not nueva or nueva == m["categoria"]:
            estado = "(sin cambio)" if nueva == m["categoria"] else "(el parser no la reconoce)"
            print(f"{m['fecha']:11} {m['monto']:>14,.2f}  {m['categoria']:<12} = {estado}")
            if nueva == m["categoria"]:
                cambios.append((m, m["categoria"]))  # sólo para bajarle la marca de revisar
            continue
        print(f"{m['fecha']:11} {m['monto']:>14,.2f}  {m['categoria']:<12} → {nueva:<28} {m['obs'][:34]}")
        cambios.append((m, nueva))

    mueve = [(m, c) for m, c in cambios if c != m["categoria"]]
    print(f"\n{len(mueve)} movimientos cambian de renglón · ${sum(m['monto'] for m, _ in mueve):,.2f}")
    print(f"{len(cambios) - len(mueve)} quedan igual y sólo se les saca la marca «revisar»")
    if not send:
        print("\n(dry-run: no escribí nada)")
        return

    # ---- 1) la base
    for m, c in cambios:
        sql(f"update movimientos set categoria='{c}', a_revisar=false where id='{m['id']}'")
    print(f"\nbase: {len(cambios)} movimientos actualizados")

    # ---- 2) la hoja del contador, por id en la columna K (columna E = Categoria)
    sv = sheets().spreadsheets()
    ids = sv.values().get(spreadsheetId=MP, range="Movimientos!K1:K2000").execute().get("values", [])
    fila_de = {str(r[0]).strip(): i for i, r in enumerate(ids, 1) if r and str(r[0]).strip()}
    data, sin_fila = [], []
    for m, c in mueve:
        f = fila_de.get(m["id"])
        if not f:
            sin_fila.append(m)
            continue
        data.append({"range": f"Movimientos!E{f}", "values": [[c]]})
    if data:
        sv.values().batchUpdate(spreadsheetId=MP, body={
            "valueInputOption": "RAW", "data": data}).execute()
    print(f"hoja: {len(data)} celdas de categoría actualizadas")
    for m in sin_fila:
        print(f"  ⚠ sin fila en la hoja (no tiene id): {m['fecha']} ${m['monto']:,.2f} {m['obs'][:40]}")


if __name__ == "__main__":
    main()
