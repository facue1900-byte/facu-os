#!/usr/bin/env python3
"""
Vuelca a la pestaña de cada local los cobros que ya están en `Cobros`.

    volcar_cobros.py [--desde AAAA-MM-DD] [--escribir]

Sin --escribir SOLO propone. Read-only por default.

## Por qué existe

Los cobros que Mati carga en la app bajan solos a la hoja `Cobros` (vía
Movimientos), pero **no llegan a la pestaña del local**, que es lo que ve el
locatario y de donde sale la deuda en efectivo. Un pago que está en Cobros y no
en la pestaña deja al local figurando con un mes entero que ya pagó. Se venía
haciendo a mano —julio el 05/08, agosto el 03/09, septiembre ahora— y cada vez
aparecieron las mismas trampas, que acá están resueltas de una vez.

## Lo que hace distinto a hacerlo a mano

  · **Appendea, no inserta.** Los pagos del mes cancelan el ÚLTIMO bloque, así
    que van debajo de todo. Las filas vacías de abajo YA traen la cadena del
    saldo copiada (verificado en las 5 pestañas), así que no hay que escribir
    ninguna fórmula ni correr filas: se escribe la fila y el saldo se recalcula
    solo. Insertar en el medio es lo que rompió la cadena en agosto.
  · **Cada pestaña tiene sus propias columnas y su propio signo.** Fabric suma
    el ingreso y da saldo negativo cuando el local debe; Bigg, Boss, Volta y
    Peak One lo restan y dan positivo. El signo se lee de la fórmula de la
    pestaña, no se asume.
  · **El medio va donde lo tiene esa pestaña.** En Bigg está en la columna del
    detalle (Facu frenó normalizarlo el 05/08: "por ahora no toques eso"), en
    las otras cuatro en la B.
  · **Cruza por (monto, fecha ±5 días).** Sólo por monto se empareja con un pago
    viejo de igual importe y el cobro nuevo parece ya volcado: a Volta le comía
    dos pagos de septiembre contra unos de abril. Un pago volcado SIN fecha en
    la columna A (Bigg ya tuvo uno) igual se detecta: si no tiene fecha, sólo se
    le pide que coincida el monto.

## La verificación, que es la parte que importa

Después de escribir relee la pestaña y exige que el saldo final se haya movido
**exactamente** lo volcado, con el signo de esa pestaña. Si no da, lo grita. Un
volcado que deja el saldo mal no se nota mirando: la fila está escrita y prolija,
y el número que se le manda al locatario es otro.
"""
import argparse
import collections
import datetime as dt
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402
from cargos_del_mes import CTAS, LOCALES, num, plata  # noqa: E402

# Cómo se llama cada local en la hoja `Cobros`.
ALIAS = {
    "Fabric": ["fabric"],
    "Bigg": ["bigg"],
    "Boss": ["hamburgueseria"],
    "Volta + Open": ["heladeria"],
    "Peak One": ["peak one", "apex"],
}
# Bigg lleva el medio en la columna del DETALLE, no en la B. Es como está hoy la
# pestaña y Facu frenó cambiarlo; cargarlo distinto la deja mitad y mitad.
MEDIO_EN_DETALLE = {"Bigg"}
# En `Cobros` el medio se llama «Caja»/«Banco»; en las pestañas, «efectivo»/«banco».
# Escribirlo como viene deja «caja» en la columna del medio, que no es el
# vocabulario de la cuenta que ve el locatario.
MEDIO = {"caja": "efectivo", "banco": "banco"}
# =+G67+E68-F68  →  el ingreso SUMA (Fabric).  =+G65+F66-E66 → el ingreso RESTA.
CADENA = re.compile(r"^=\+?([A-Z]+)\d+([+-])([A-Z]+)\d+([+-])([A-Z]+)\d+$")


def serial_a_fecha(s):
    try:
        return dt.date(1899, 12, 30) + dt.timedelta(days=int(s))
    except (TypeError, ValueError):
        return None


def col(letra):
    return ord(letra) - ord("A")


def signo_del_ingreso(sv, pestania, lay, fila):
    """+1 si un pago SUMA al saldo de esta pestaña, -1 si lo resta.

    Se lee de la fórmula real. Asumirlo es exactamente cómo se escribe un saldo
    perfectamente formado y al revés.
    """
    fx = sv.values().get(spreadsheetId=CTAS,
                         range=f"{pestania}!{lay['saldo']}{fila}",
                         valueRenderOption="FORMULA").execute().get("values")
    if not fx or not fx[0]:
        return None, f"{pestania}!{lay['saldo']}{fila} no tiene fórmula de saldo"
    m = CADENA.match(str(fx[0][0]).replace(" ", ""))
    if not m:
        return None, f"{pestania}!{lay['saldo']}{fila} = {fx[0][0]!r}, no es la cadena"
    _prev, op1, c1, op2, c2 = m.groups()
    for op, c in ((op1, c1), (op2, c2)):
        if c == lay["ingreso"]:
            return (1 if op == "+" else -1), None
    return None, f"{pestania}!{lay['saldo']}{fila} no referencia la columna de ingreso"


def ultima_fila(vals, lay):
    """La última fila con contenido real. Abajo hay cientos de filas vacías que
    ya traen la fórmula del saldo copiada: ahí es donde se appendea."""
    ult = 0
    for i, r in enumerate(vals, 1):
        det = str(r[col(lay["detalle"])]).strip() if col(lay["detalle"]) < len(r) else ""
        etq = str(r[0]).strip() if r and r[0] is not None else ""
        ing = num(r[col(lay["ingreso"])]) if col(lay["ingreso"]) < len(r) else 0
        egr = num(r[col(lay["egreso"])]) if col(lay["egreso"]) < len(r) else 0
        if det or etq or ing or egr:
            ult = i
    return ult


def saldo_en(vals, lay, hasta):
    for i in range(hasta, 0, -1):
        r = vals[i - 1] if i - 1 < len(vals) else []
        c = col(lay["saldo"])
        v = r[c] if c < len(r) else None
        if v not in ("", None):
            return num(v)
    return 0.0


def pendientes(sv, local, cfg, cobros, desde):
    """Los cobros de este local que todavía no están en su pestaña.

    El pareo es por CONTEO por monto dentro de la ventana, no "buscá uno
    parecido". Con ±5 días, dos pagos reales del mismo importe —cosa común acá,
    donde los alquileres son fijos y los pagos parciales se repiten— hacían que
    el segundo matcheara contra el primero ya volcado y **se descartara un pago
    real sin decir nada**. Contando de los dos lados, si hay 3 cobros de
    $500.000 y 1 volcado, faltan 2: no hay nada que elegir.

    El universo de volcados son los pagos con fecha DENTRO de la ventana, más
    los que no tienen fecha en la columna A (Bigg ya tuvo uno). Los pagos viejos
    quedan afuera y no se comen un cobro nuevo.
    """
    lay = cfg["layout"]
    vals = sv.values().get(spreadsheetId=CTAS, range=f"{cfg['pestania']}!A1:H400",
                           valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    volcados = collections.Counter()
    for r in vals:
        c = col(lay["ingreso"])
        m = num(r[c]) if c < len(r) else 0
        if not m:
            continue
        f = serial_a_fecha(r[0]) if r and r[0] not in ("", None) else None
        if f is None or f >= desde:
            volcados[round(m, 2)] += 1

    mios = []
    for r in cobros:
        if str(r[1]).strip().lower() not in ALIAS[local]:
            continue
        f, monto = serial_a_fecha(r[0]), round(num(r[2]), 2)
        if not f or not monto or f < desde:
            continue
        mios.append((f, monto, str(r[3]).strip(), str(r[4]).strip()))

    faltan, avisos, usados = [], [], collections.Counter()
    for f, monto, medio, det in sorted(mios):
        if usados[monto] < volcados[monto]:
            usados[monto] += 1
            continue
        faltan.append((f, monto, medio, det))
    # Del otro lado: un pago en la pestaña, dentro de la ventana, que no tiene
    # cobro que lo explique. O se cargó a mano y no bajó a Cobros, o está de más.
    for monto, n in volcados.items():
        sobran = n - sum(1 for x in mios if x[1] == monto)
        if sobran > 0:
            avisos.append(f"{local}: {sobran} pago/s de {plata(monto)} en la "
                          f"pestaña sin cobro que los explique en `Cobros`")
    return vals, sorted(faltan), avisos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", default="2026-08-26",
                    help="no mirar cobros anteriores a esta fecha (AAAA-MM-DD)")
    ap.add_argument("--escribir", action="store_true")
    a = ap.parse_args()
    desde = dt.date.fromisoformat(a.desde)

    sv = sheets().spreadsheets()
    crudo = sv.values().get(spreadsheetId=CTAS, range="Cobros!A1:E600",
                            valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
    # Cuántas filas de encabezado tiene `Cobros` se LEE, no se asume: si mañana
    # gana o pierde una, saltear un número fijo se come la primera fila de plata
    # y no lo nota nadie.
    inicio = next((i + 1 for i, r in enumerate(crudo)
                   if r and str(r[0]).strip().lower() == "fecha"), None)
    if inicio is None:
        sys.exit("No encontré la fila de títulos ('Fecha') en `Cobros`. "
                 "Sin saber dónde arrancan los datos no leo nada.")
    cobros = [x + [""] * 5 for x in crudo[inicio:]]

    # Un cobro cuyo local no matchea ningún ALIAS no entra a NINGUNA pestaña y
    # hoy desaparecía sin aviso: el informe decía "al día" con plata sin volcar.
    conocidos = {a for v in ALIAS.values() for a in v}
    huerfanos = []
    for r in cobros:
        f, monto = serial_a_fecha(r[0]), round(num(r[2]), 2)
        nombre = str(r[1]).strip()
        if not f or not monto or f < desde or not nombre:
            continue
        if nombre.lower() not in conocidos:
            huerfanos.append((f, monto, nombre, str(r[4]).strip()))

    print(f"VOLCAR COBROS A LAS PESTAÑAS — cobros desde {desde}")
    print("(sin --escribir no se toca nada)\n" if not a.escribir else "")

    plan, total, sueltos = [], 0.0, []
    for local, cfg in LOCALES.items():
        if not cfg.get("pestania") or not cfg.get("layout"):
            continue
        vals, faltan, avisos = pendientes(sv, local, cfg, cobros, desde)
        lay = cfg["layout"]
        ult = ultima_fila(vals, lay)
        if not ult:
            print(f"── {local}: NO SE TOCA — la pestaña {cfg['pestania']!r} no "
                  f"tiene ninguna fila con contenido")
            continue
        signo, err = signo_del_ingreso(sv, cfg["pestania"], lay, ult)
        if signo is None:
            print(f"── {local}: NO SE TOCA — {err}")
            continue
        saldo = saldo_en(vals, lay, ult)
        print(f"── {local}  «{cfg['pestania']}»  última fila {ult}  "
              f"saldo {plata(saldo)}  (un pago {'suma' if signo > 0 else 'resta'})")
        if not faltan:
            print("   al día: no hay cobros sin volcar\n")
            continue
        for k, (f, monto, medio, det) in enumerate(faltan):
            print(f"   f{ult + 1 + k:<4}{f:%d/%m}  {plata(monto):>16}  {medio:<9}{det[:44]}")
        print(f"   {'':6}{'':10}{plata(sum(x[1] for x in faltan)):>16}  a volcar\n")
        plan.append((local, cfg, ult, signo, saldo, faltan))
        total += sum(x[1] for x in faltan)
        sueltos.extend(avisos)

    print(f"TOTAL A VOLCAR: {plata(total)}")
    if huerfanos:
        print(f"\n⚠ {len(huerfanos)} cobro/s en `Cobros` que NO son de ninguna "
              f"pestaña — no se vuelcan acá, revisar a mano:")
        for f, monto, nombre, det in sorted(huerfanos):
            print(f"   {f:%d/%m}  {plata(monto):>16}  {nombre:<24}{det[:40]}")
    for aviso in sueltos:
        print(f"⚠ {aviso}")
    if not plan:
        return
    if not a.escribir:
        print("\n[SIN --escribir] No toqué nada. Revisá y volvé a correr con --escribir.")
        return

    # ---- escribir y verificar, LOCAL POR LOCAL ------------------------------
    # Cada local se escribe y se verifica en el acto. Antes la verificación
    # entera corría al final: si el tercer local fallaba (red, o un medio que no
    # entiendo), los dos primeros YA estaban escritos en la planilla real y no
    # los verificaba nadie — el operador veía un traceback en vez del "revisar a
    # mano" que es la razón de ser de este script.
    print("\nEscribiendo (cada local se verifica apenas se escribe)...")
    fallados, ok_todo = [], True
    for local, cfg, ult, signo, saldo_antes, faltan in plan:
        lay, pest = cfg["layout"], cfg["pestania"]
        try:
            datos, esperadas = [], []
            for k, (f, monto, medio, det) in enumerate(faltan):
                fila = ult + 1 + k
                m = MEDIO.get(medio.strip().lower())
                if m is None:
                    raise ValueError(f"medio {medio!r} desconocido en Cobros "
                                     f"({f:%d/%m}, {plata(monto)})")
                if local in MEDIO_EN_DETALLE:
                    celdas = {"A": f"{f:%d/%m/%Y}", lay["detalle"]: m}
                else:
                    celdas = {"A": f"{f:%d/%m/%Y}", "B": m, lay["detalle"]: det}
                celdas[lay["ingreso"]] = monto
                for letra, valor in celdas.items():
                    datos.append({"range": f"{pest}!{letra}{fila}",
                                  "values": [[valor]]})
                esperadas.append((fila, m, monto))
            sv.values().batchUpdate(
                spreadsheetId=CTAS,
                body={"valueInputOption": "USER_ENTERED", "data": datos}).execute()
        except Exception as e:                                    # noqa: BLE001
            ok_todo = False
            fallados.append(local)
            print(f"   🔴 {local}: NO se pudo escribir — {e}")
            print(f"      Revisá {pest} a mano antes de mandar esa cuenta.")
            continue

        # --- verificación de ESTE local, releyendo ---
        vals = sv.values().get(spreadsheetId=CTAS, range=f"{pest}!A1:H400",
                               valueRenderOption="UNFORMATTED_VALUE").execute()["values"]
        saldo_desp = saldo_en(vals, lay, ultima_fila(vals, lay))
        volcado = sum(x[1] for x in faltan)
        esperado = round(saldo_antes + signo * volcado, 2)
        bien = abs(round(saldo_desp, 2) - esperado) < 0.01
        # El saldo agregado puede cuadrar con el MEDIO mal escrito, y el medio es
        # lo que decide si ese peso es efectivo de Mati o banco. Se relee celda
        # por celda, no sólo el total.
        malas = []
        for fila, m_esp, monto_esp in esperadas:
            r = list(vals[fila - 1]) + [""] * 8 if fila - 1 < len(vals) else [""] * 8
            c_medio = col(lay["detalle"]) if local in MEDIO_EN_DETALLE else 1
            if str(r[c_medio]).strip().lower() != m_esp:
                malas.append(f"f{fila} medio={r[c_medio]!r} (esperaba {m_esp!r})")
            if abs(num(r[col(lay["ingreso"])]) - monto_esp) > 0.01:
                malas.append(f"f{fila} monto={r[col(lay['ingreso'])]!r}")
        if bien and not malas:
            print(f"   OK  {local:<14}{len(faltan)} fila/s  "
                  f"{plata(saldo_antes)} → {plata(saldo_desp)}")
        else:
            ok_todo = False
            fallados.append(local)
            print(f"   🔴 {local:<14}{plata(saldo_antes)} → {plata(saldo_desp)} "
                  f"(esperaba {plata(esperado)})")
            for x in malas:
                print(f"      {x}")

    if not ok_todo:
        sys.exit(f"\n🔴 QUEDÓ MAL EN: {', '.join(fallados)}. NO mandar esas "
                 f"cuentas ni correr `deuda_efectivo.py --cobros-en-planilla` "
                 f"hasta arreglarlo a mano.")
    print("\nTodos los saldos se movieron exactamente lo volcado, y cada fila "
          "quedó con su medio y su monto.")
    print("Ahora corré `deuda_efectivo.py --cobros-en-planilla` para que la app "
          "de Mati deje de descontar estos cobros dos veces.")


if __name__ == "__main__":
    main()
