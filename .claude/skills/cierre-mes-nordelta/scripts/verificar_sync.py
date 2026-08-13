#!/usr/bin/env python3
"""¿El Apps Script publicado conoce los locales nuevos?

No hay forma de leer el código publicado sin la Apps Script API, así que se lo
pregunta por su comportamiento: se le manda un cobro de Meta y otro de Pole
Position y se mira qué escribió en la columna Local. Si dice «Meta Escuelita» y
«Pole Position», el LOCAL_MAP nuevo está arriba.

Dos recaudos para no ensuciar la contabilidad:
  · **fecha 2030** — el Dashboard llega hasta diciembre 2026, así que ninguna
    fórmula mira esas filas ni aunque queden.
  · **la limpieza no depende del script**: las filas se borran con la Sheets API
    por número de fila. Confiar el borrado a lo mismo que estoy probando es cómo
    quedó viva tres semanas la fila de prueba de $1 del 22/07.
"""
import json
import sys
import urllib.request

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

URL = ("https://script.google.com/macros/s/AKfycbzkHrs9PsaTLfHt4bO-jOHuTaVEf-"
       "O9qTSBsZuoaIoh21ESa-BAhzpuJATBQgc9Uvem/exec?token=pn-sync-7k2x9")
MP = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
HOJA = "Movimientos"

CASOS = [
    ("meta", "Meta Escuelita", "11111111-aaaa-4aaa-aaaa-111111111111"),
    ("pole-position", "Pole Position", "22222222-bbbb-4bbb-bbbb-222222222222"),
    # un id que el script NO conoce: tiene que avisar en Observaciones
    ("local-inventado", "", "33333333-cccc-4ccc-cccc-333333333333"),
]


def post(record):
    req = urllib.request.Request(
        URL, data=json.dumps({"action": "insert", "record": record}).encode(),
        headers={"Content-Type": "text/plain"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode().strip()


def main():
    sv = sheets().spreadsheets()
    hoja_id = next(s["properties"]["sheetId"] for s in sv.get(spreadsheetId=MP).execute()["sheets"]
                   if s["properties"]["title"] == HOJA)
    antes = len(sv.values().get(spreadsheetId=MP, range=f"{HOJA}!A1:A2000").execute()["values"])
    print(f"la hoja tiene {antes} filas antes de la prueba\n")

    for local_id, _, mov_id in CASOS:
        print(f"  → mando un cobro de «{local_id}»: {post({
            'id': mov_id, 'fecha': '2030-01-15', 'tipo': 'Ingreso', 'medio': 'Caja',
            'local_id': local_id, 'categoria': 'Cobro inquilino', 'monto': 1,
            'moneda': 'ARS', 'obs': 'PRUEBA DEL SYNC - se borra en el acto'})}")

    vals = sv.values().get(spreadsheetId=MP, range=f"{HOJA}!A1:K2000").execute()["values"]
    filas = [(i, r) for i, r in enumerate(vals, 1)
             if len(r) > 7 and "PRUEBA DEL SYNC" in str(r[7])]
    print(f"\n{len(filas)} filas de prueba escritas:")
    fallas = 0
    for (local_id, esperado, mov_id) in CASOS:
        fila = next((f for f in filas if len(f[1]) > 10 and str(f[1][10]).strip() == mov_id), None)
        if not fila:
            print(f"  ✗ «{local_id}»: no encontré su fila POR ID → el id no viajó")
            fallas += 1
            continue
        i, r = fila
        r = list(r) + [""] * 11
        local, obs = str(r[3]).strip(), str(r[7])
        ok = local == esperado
        print(f"  {'✓' if ok else '✗'} «{local_id}» → fila {i}, columna Local: "
              f"{local!r} (esperaba {esperado!r})")
        if not ok:
            fallas += 1
        if local_id == "local-inventado":
            aviso = "REVISAR" in obs
            print(f"  {'✓' if aviso else '✗'} y avisa en Observaciones: {obs[-60:]!r}")
            if not aviso:
                fallas += 1

    # ---- limpieza, de abajo hacia arriba y sin pedirle permiso al script
    print()
    for i, _ in sorted(filas, reverse=True):
        sv.batchUpdate(spreadsheetId=MP, body={"requests": [{"deleteDimension": {
            "range": {"sheetId": hoja_id, "dimension": "ROWS",
                      "startIndex": i - 1, "endIndex": i}}}]}).execute()
        print(f"  borrada la fila {i}")

    vals = sv.values().get(spreadsheetId=MP, range=f"{HOJA}!A1:K2000").execute()["values"]
    quedan = [i for i, r in enumerate(vals, 1) if len(r) > 7 and "PRUEBA DEL SYNC" in str(r[7])]
    despues = len(vals)
    print(f"\nla hoja quedó con {despues} filas (antes {antes}) · rastros de la prueba: {len(quedan)}")
    if quedan or despues != antes:
        print("  ✗ QUEDÓ ALGO — revisar a mano")
        fallas += 1
    print("\n" + ("TODO OK — el script publicado es el nuevo" if not fallas
                  else f"{fallas} PROBLEMAS"))
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
