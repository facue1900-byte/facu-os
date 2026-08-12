#!/usr/bin/env python3
"""¿Lo que carga Mati en la app llega entero al Dashboard Mensual?

    verificar_dashboard.py [YYYY-MM]

Sigue la plata por los tres saltos y verifica cada uno contra el siguiente:

    app (Supabase)  →  hoja Movimientos  →  Dashboard Mensual

Cada salto tiene su forma propia de romperse en silencio:

  · **app → hoja**: el sync espeja la fila por HTTP. Si el POST se pierde, la
    fila no está y no salta ningún error.
  · **la columna D (Local) y la E (Categoría)**: el Dashboard matchea por NOMBRE
    EXACTO contra `Configuración!A`. Un local que el sync no sabe traducir deja
    la columna vacía y **no lo suma nadie**.
  · **la columna I (Mes)**: el SUMIFS filtra por ella. Una fila con el mes vacío
    o mal escrito existe, se ve, y no entra en ningún total. No se escribe: sale
    de `I6 = ARRAYFORMULA(IF(A6:A="","",TEXT(A6:A,"mmmm yyyy")))`, o sea **de la
    fecha**. Y ahí está la trampa de fondo: si la fecha entra como TEXTO en vez
    de como fecha de verdad, `TEXT()` no la entiende, el mes queda mal y el
    movimiento se cae de todos los totales sin un solo error.

Read-only. No escribe una sola celda.
"""
import datetime
import json
import os
import subprocess
import sys
from collections import defaultdict

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

MP = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
REF = "wujutradczplokjrgmdo"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def base(periodo):
    token = next(l.split("=", 1)[1].strip() for l in
                 open("/Users/Facu/facu-os/.env", encoding="utf-8")
                 if l.startswith("SUPABASE_ACCESS_TOKEN="))
    sql = ("select id::text, fecha::text, tipo, medio, local_id, categoria, "
           f"monto::float8, obs from movimientos where to_char(fecha,'YYYY-MM') = '{periodo}'")
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://api.supabase.com/v1/projects/{REF}/database/query",
         "-H", f"Authorization: Bearer {token}", "-H", "Content-Type: application/json",
         "-d", json.dumps({"query": sql})], capture_output=True, text=True, env=dict(os.environ))
    return json.loads(out.stdout)


def a_iso(v):
    if isinstance(v, (int, float)):
        return (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(v))).isoformat()
    s = str(v).strip()
    if "/" in s:
        d, m, y = s.split("/")[:3]
        return f"{y}-{int(m):02d}-{int(d):02d}"
    return s[:10]


def main():
    periodo = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().strftime("%Y-%m")
    anio, mes = int(periodo[:4]), int(periodo[5:])
    etiqueta = f"{MESES[mes - 1]} {anio}"
    sv = sheets().spreadsheets()

    movs = base(periodo)
    hoja = sv.values().get(spreadsheetId=MP, range="Movimientos!A1:K2000",
                           valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    filas, fecha_texto = [], []
    for i, r in enumerate(hoja[1:], 2):
        r = list(r) + [""] * 11
        if not str(r[1]).strip() or a_iso(r[0])[:7] != periodo:
            continue
        # una fecha en texto rompe la ARRAYFORMULA del Mes y saca la fila de
        # todos los totales; se ve idéntica a una fecha buena
        if not isinstance(r[0], (int, float)):
            fecha_texto.append((i, r[0]))
        filas.append({"fila": i, "fecha": a_iso(r[0]), "tipo": str(r[1]).strip(),
                      "medio": str(r[2]).strip(), "local": str(r[3]).strip(),
                      "cat": str(r[4]).strip(),
                      "monto": float(r[5]) if isinstance(r[5], (int, float)) else 0.0,
                      "moneda": (str(r[6]).strip() or "ARS").upper(),
                      "obs": str(r[7]).strip(), "mes": str(r[8]).strip(),
                      "id": str(r[10]).strip()})

    print(f"=== {etiqueta} ===")
    print(f"app: {len(movs)} movimientos · hoja: {len(filas)} filas\n")
    fallas = 0

    # ---- salto 1: cada movimiento de la app tiene su fila
    ids_hoja = {f["id"] for f in filas if f["id"]}
    por_monto = defaultdict(list)
    for f in filas:
        por_monto[(f["fecha"], f["tipo"], round(f["monto"], 2))].append(f)
    print("1 · APP → HOJA")
    huerf = []
    for m in movs:
        k = (m["fecha"], m["tipo"], round(m["monto"], 2))
        if m["id"] not in ids_hoja and not por_monto.get(k):
            huerf.append(m)
    if huerf:
        fallas += 1
        print(f"  ✗ {len(huerf)} movimientos de la app NO están en la hoja:")
        for m in huerf:
            print(f"      {m['fecha']} {m['tipo']:8} ${m['monto']:>12,.2f}  {m['obs'][:44]}")
    else:
        print(f"  ✓ los {len(movs)} movimientos de la app están en la hoja")
    sin_id = [f for f in filas if not f["id"]]
    print(f"  {'✓' if not sin_id else '·'} {len(filas) - len(sin_id)} de {len(filas)} filas "
          f"llevan el id de la app (sin id no se pueden editar ni borrar desde la app)")
    for f in sin_id:
        print(f"      fila {f['fila']}  {f['fecha']} ${f['monto']:>12,.2f}  {f['obs'][:40]}")

    # ---- salto 2: la fila entra en algún renglón del dashboard
    print("\n2 · LA FILA ES SUMABLE (columnas D/E y la I)")
    # Los renglones de INGRESO salen de Configuración!A y los de EGRESO de la C.
    # Son dos listas distintas: validar todo contra la A da un falso positivo que
    # tapa justo los egresos, que son la mitad de la plata.
    cfg = sv.values().get(spreadsheetId=MP, range="Configuración!A1:C40").execute().get("values", [])
    conf = {
        "Ingreso": {str(r[0]).strip() for r in cfg if r and str(r[0]).strip()},
        "Egreso": {str((r + ["", "", ""])[2]).strip() for r in cfg
                   if len(r) > 2 and str(r[2]).strip()},
    }
    print(f"  renglones válidos: {len(conf['Ingreso'])} de ingreso (Configuración!A) · "
          f"{len(conf['Egreso'])} de egreso (Configuración!C)")
    if fecha_texto:
        fallas += 1
        print(f"  ✗ {len(fecha_texto)} filas con la FECHA COMO TEXTO: la columna Mes "
              f"no se calcula y se caen de todos los totales")
        for i, v in fecha_texto:
            print(f"      fila {i}: {v!r}  → arreglar con arreglarFechas() del Apps Script")
    malas = []
    for f in filas:
        etiq = f["local"] if f["tipo"] == "Ingreso" else f["cat"]
        if not etiq:
            malas.append((f, "sin renglón (columna Local/Categoría vacía)"))
        elif etiq not in conf[f["tipo"]]:
            col = "A" if f["tipo"] == "Ingreso" else "C"
            malas.append((f, f"«{etiq}» no existe en Configuración!{col}"))
        elif f["mes"] != etiqueta:
            malas.append((f, f"la columna Mes dice «{f['mes']}»"))
    if malas:
        fallas += 1
        print(f"  ✗ {len(malas)} filas que NINGÚN total del dashboard suma:")
        for f, por in malas:
            print(f"      fila {f['fila']}  ${f['monto']:>12,.2f}  {por}  ({f['obs'][:30]})")
    else:
        print(f"  ✓ las {len(filas)} filas tienen renglón válido y el mes bien escrito")

    # ---- salto 3: el número del dashboard = la suma de las filas
    print("\n3 · HOJA → DASHBOARD (el SUMIFS, recalculado)")
    dash = sv.values().get(spreadsheetId=MP, range="Dashboard Mensual!A1:AZ80",
                           valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    enc, medios = dash[2] + [""] * 60, dash[4] + [""] * 60
    cols = {medios[j].strip(): j for j in range(1, 60)
            if str(enc[j]).strip() == etiqueta and str(medios[j]).strip()}
    if not cols:
        print(f"  ✗ el Dashboard no tiene todavía la columna de {etiqueta}")
        sys.exit(1)
    print(f"  columnas de {etiqueta} en el Dashboard: "
          + ", ".join(f"{m}={chr(ord('A') + j)}" for m, j in cols.items()))
    peor, evaluados, con_plata = 0.0, {"Ingreso": 0, "Egreso": 0}, 0
    for i, r in enumerate(dash, 1):
        etiq = str((r + [""])[0]).strip()
        # el mismo nombre puede ser renglón de ingreso y de egreso («Eventos»):
        # lo desempata en qué mitad del dashboard está la fila
        tipo = "Ingreso" if i < 44 else "Egreso"
        if not etiq or etiq not in conf[tipo]:
            continue
        evaluados[tipo] += 1
        for medio, j in cols.items():
            visto = float(r[j]) if len(r) > j and isinstance(r[j], (int, float)) else 0.0
            # los renglones del dashboard son de PESOS: los dólares van a la fila 7
            calc = sum(f["monto"] for f in filas if f["mes"] == etiqueta and f["medio"] == medio
                       and f["tipo"] == tipo and f["moneda"] == "ARS"
                       and (f["local"] if tipo == "Ingreso" else f["cat"]) == etiq)
            if visto or calc:
                con_plata += 1
            if abs(visto - calc) > 0.01:
                fallas += 1
                print(f"  ✗ fila {i:2d} {etiq:<32} {medio}: dashboard ${visto:,.2f} "
                      f"≠ movimientos ${calc:,.2f}")
            peor = max(peor, abs(visto - calc))
    # un chequeo que no evaluó nada también da verde: por eso se cuenta
    print(f"  renglones comparados: {evaluados['Ingreso']} de ingreso + "
          f"{evaluados['Egreso']} de egreso · {con_plata} con plata este mes")
    if not evaluados["Ingreso"] or not evaluados["Egreso"]:
        fallas += 1
        print("  ✗ no comparé alguno de los dos lados: el verde no significa nada")
    elif peor <= 0.01:
        print("  ✓ todos los renglones del dashboard dan exactamente la suma de sus filas")

    # ---- los dólares no se cuelan entre los pesos: van a la fila 7 «u$s»
    print("\n4 · DÓLARES (fila 7 «u$s»)")
    usd = [f for f in filas if f["moneda"] != "ARS"]
    if not usd:
        print(f"  · no hubo movimientos en dólares en {etiqueta}")
    for medio, j in cols.items():
        visto = float(dash[6][j]) if len(dash[6]) > j and isinstance(dash[6][j], (int, float)) else 0.0
        calc = sum((1 if f["tipo"] == "Ingreso" else -1) * f["monto"]
                   for f in usd if f["medio"] == medio and f["mes"] == etiqueta)
        estado = "✓" if abs(visto - calc) < 0.01 else "✗"
        if estado == "✗":
            fallas += 1
        print(f"  {estado} {medio}: dashboard US${visto:,.2f} · movimientos US${calc:,.2f}")

    print("\n" + ("TODO OK" if not fallas else f"{fallas} PROBLEMAS"))
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
