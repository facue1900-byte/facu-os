#!/usr/bin/env python3
"""
Generador del bloque mensual de cuentas corrientes — Paseo Nordelta.

Un bloque de cobro es, para cada local:

    expensas del mes M  +  alquiler del mes M+1

que es lo que se le manda junto. Este script lo arma entero.

    cargos_del_mes.py <AAAA-MM del ALQUILER> [--escribir] [--congelar-expensas]

Sin --escribir SOLO propone: imprime la tabla y no toca nada. El generador
propone, la edición de Facu manda (una expensa de mejoras alta se parte en
cuotas a mano — eso no lo decide un script).

## Por qué existe "congelar"

Las expensas salen de `Expensas Predio` del Master Plan, que es una hoja de UN
SOLO MES VIVO: la celda A3 tiene la fecha y todo se recalcula contra ella. Sacar
julio ahí BORRA junio. Con --congelar-expensas el script cambia la fecha, lee el
resultado, lo guarda como filas en la hoja `EXPENSAS HISTORICO` de Ctas Ctes y
**restaura la fecha original** (try/finally). A partir de ahí ningún mes vuelve a
depender de una hoja viva.

Verificaciones que corre siempre, porque cada una ya falló o puede fallar en
silencio:

  - Expensas AVN del mes en Movimientos: si da 0, el recupero sale 0 para los 8
    locales y nadie se entera. Corta.
  - Columnas por pestaña: Fabric/Bigg/Boss tienen columna FC y Volta/Peak One no,
    así que el egreso va en F en unas y en E en otras. Escribir en la columna
    equivocada pisa el SALDO. El layout es por pestaña, nunca asumido.
  - Dedupe: no escribe un concepto que ya existe para ese local y mes.
  - Post-escritura: relee lo escrito y lo compara contra lo propuesto.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, "/Users/Facu/facu-os")
from execution.google_auth import sheets  # noqa: E402

CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
MASTER = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
HOJA_HISTORICO = "EXPENSAS HISTORICO"

MESES = {1: "ENE", 2: "FEB", 3: "MAR", 4: "ABR", 5: "MAY", 6: "JUN",
         7: "JUL", 8: "AGO", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DIC"}
MESES_LARGO = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo",
               6: "junio", 7: "julio", 8: "agosto", 9: "septiembre",
               10: "octubre", 11: "noviembre", 12: "diciembre"}

# Layout de cada pestaña. Fabric/Bigg/Boss tienen una columna "FC" que Volta y
# Peak One no tienen, así que ingreso/egreso/saldo caen corridos una columna.
# Verificado leyendo la fila de encabezado de cada pestaña el 05/08/2026.
LAYOUT_CON_FC = {"detalle": "C", "ingreso": "E", "egreso": "F", "saldo": "G"}
LAYOUT_SIN_FC = {"detalle": "C", "ingreso": "D", "egreso": "E", "saldo": "F"}

# local en CARGOS → cómo se llama en cada lado
LOCALES = {
    "Fabric": {
        "pestania": "Fabric", "expensas_predio": "Fabric",
        "layout": LAYOUT_CON_FC, "iva": True, "cobra_por": "Banco",
        "alquiler": "del mes anterior", "partido": False,
    },
    "Bigg": {
        "pestania": "Bigg", "expensas_predio": "Bigg",
        "layout": LAYOUT_CON_FC, "iva": True,
        "cobra_por": "Mixto (facturado banco + mitad efectivo)",
        "alquiler": "del mes anterior",
        # 50% facturado con IVA + 50% "Diferencia Alquiler" en efectivo sin IVA
        "partido": True,
    },
    "Boss": {
        "pestania": "Boss", "expensas_predio": "Hamburgueseria",
        "layout": LAYOUT_CON_FC, "iva": False, "cobra_por": "Efectivo",
        "alquiler": "del mes anterior", "partido": False,
    },
    "Volta + Open": {
        "pestania": "Volta + Open 25", "expensas_predio": "Heladeria",
        "layout": LAYOUT_SIN_FC, "iva": False, "cobra_por": "Efectivo",
        "alquiler": "del mes anterior", "partido": False,
    },
    "Peak One": {
        "pestania": "Peak One", "expensas_predio": "Peak One",
        "layout": LAYOUT_SIN_FC, "iva": False, "cobra_por": "Efectivo",
        # sin alquiler propio hasta dic-26: solo recupero + servicios
        "alquiler": 0, "partido": False,
    },
    "Salón (Alto)": {
        # «Salon Multiespacios» NO es una cuenta corriente: es una pestaña con un
        # QUERY en A5 que derrama solo los cobros desde la hoja `Cobros`. No tiene
        # columna de cargos ni saldo encadenado. Escribir abajo del derrame hace
        # que el próximo cobro choque y tire #REF!, rompiendo la pestaña entera.
        # Por eso va sin pestaña, como La Jaula: sus cargos viven sólo en CARGOS.
        "pestania": None, "expensas_predio": "Salon Alto",
        "layout": None, "iva": False, "cobra_por": "Efectivo",
        # expensas PACTADAS en $1.000.000, no las de la hoja (Facu 27/07/2026)
        "alquiler": 0, "partido": False, "expensas_pactadas": 1_000_000,
    },
    "La Jaula / torneo": {
        "pestania": None, "expensas_predio": "Contenedor Jaula",
        "layout": None, "iva": False, "cobra_por": "Efectivo",
        # primera alta: agosto 2026, $1.000.000 + $798.825 de servicios
        "alquiler": 1_000_000, "partido": False,
        "desde": "2026-08", "servicios_pactados": 798_825,
    },
    # Escuelita no lleva cargo generado: paga un % de facturación y el ingreso
    # entra solo por Movimientos.
}

IVA = 0.21


def etiqueta(anio, mes):
    return f"{MESES[mes]}'{anio % 100}"


def medio_de(local, concepto):
    """`efectivo` o `banco`: cómo se cobra ESTE concepto de ESTE local.

    Va a la columna B de la cuenta corriente. Es el dato del que cuelga todo lo
    demás: **el efectivo no se factura**, y es lo único que Mati ve y cobra.

    Bigg es el único partido: cobra la mitad por banco (la fila "Alquiler", que
    es la que lleva IVA y se factura) y la otra mitad en efectivo, que es
    exactamente lo que significa "Diferencia Alquiler (sin iva)".
    """
    cobra = LOCALES[local]["cobra_por"].lower()
    if cobra.startswith("mixto"):
        return "efectivo" if "sin iva" in concepto.lower() else "banco"
    return "efectivo" if "efectivo" in cobra else "banco"


def mes_anterior(anio, mes):
    return (anio - 1, 12) if mes == 1 else (anio, mes - 1)


def parse_mes(txt):
    m = re.fullmatch(r"(\d{4})-(\d{2})", txt or "")
    if not m or not 1 <= int(m.group(2)) <= 12:
        sys.exit(f"El mes va como AAAA-MM, no {txt!r}.")
    return int(m.group(1)), int(m.group(2))


def plata(x):
    return f"${x:,.2f}"


class Planillas:
    def __init__(self):
        self.s = sheets(cuenta="facu")

    def leer(self, sid, rango, render="FORMATTED_VALUE"):
        return self.s.spreadsheets().values().get(
            spreadsheetId=sid, range=rango, valueRenderOption=render
        ).execute().get("values", [])

    def escribir(self, sid, rango, valores):
        return self.s.spreadsheets().values().update(
            spreadsheetId=sid, range=rango, valueInputOption="USER_ENTERED",
            body={"values": valores},
        ).execute()

    def append(self, sid, rango, filas):
        return self.s.spreadsheets().values().append(
            spreadsheetId=sid, range=rango, valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS", body={"values": filas},
        ).execute()

    def hojas(self, sid):
        meta = self.s.spreadsheets().get(spreadsheetId=sid).execute()
        return [h["properties"]["title"] for h in meta["sheets"]]

    def crear_hoja(self, sid, titulo):
        self.s.spreadsheets().batchUpdate(
            spreadsheetId=sid,
            body={"requests": [{"addSheet": {"properties": {"title": titulo}}}]},
        ).execute()


def num(x):
    """Un valor de Sheets a float. '$1,205,581' → 1205581.0, vacío → 0.0."""
    if x is None or x == "":
        return 0.0
    if isinstance(x, (int, float)):
        return float(x)
    limpio = str(x).replace("$", "").replace(",", "").replace("−", "-").strip()
    if limpio.startswith("(") and limpio.endswith(")"):
        limpio = "-" + limpio[1:-1]
    try:
        return float(limpio)
    except ValueError:
        return 0.0


# ---------------------------------------------------------------- expensas ---

def expensas_del_historico(p, anio, mes):
    """Lee el mes de EXPENSAS HISTORICO. {local_predio: (recupero, servicios)}."""
    if HOJA_HISTORICO not in p.hojas(CTAS):
        return {}
    filas = p.leer(CTAS, f"{HOJA_HISTORICO}!A2:E500")
    clave = f"{anio}-{mes:02d}"
    return {r[1]: (num(r[2]), num(r[3]))
            for r in filas if len(r) >= 4 and r[0] == clave}


def congelar_expensas(p, anio, mes, agua=None, abl=None, avn=None, dry_run=True):
    """Pone la fecha del mes en Expensas Predio, lee, y RESTAURA todo lo tocado.

    Devuelve {local_predio: (recupero, servicios_comunes)}.

    `agua` y `abl` son los dos números que Facu tipea a mano cada mes (C4 y D4):
    no salen de Movimientos ni de ningún PDF del Desktop. Si no se pasan, la hoja
    queda con los del mes anterior y el recupero sale mal — por eso se exigen.

      · Agua R&S      → factura de la prestataria, la pasa Facu
      · ABL Municipal → liquidación de Tigre: SOLO "Tasa por Servicios
        Municipales" + "Cont. Esp. Hospital". Los DERECHOS DE CONSTRUCCIÓN y el
        PLAN DE PAGOS FONDO Y ÁRIDOS de la misma liquidación son obra (CAPEX) y
        NO se le cobran a los locales: van a Inversiones.

    `avn` es la puerta de escape para cuando el extracto del Macro todavía no se
    importó: B4 es un SUMIFS contra Movimientos, así que sin extracto da $0 y el
    script corta. Pasando --avn se escribe el total de las liquidaciones (los 4
    PDFs de `~/Desktop/Paseo Nordelta/Principio de mes/Facturas de Compra/`) y la
    FÓRMULA SE RESTAURA igual que todo lo demás. No se carga una fila falsa en
    Movimientos: cuando entre el extracto, el gasto entra una sola vez.

    Corta si Expensas AVN del mes da 0: eso significa que las facturas del mes
    no están cargadas en Movimientos y el recupero saldría en cero sin avisar.
    """
    # A2:D4 devuelve TRES filas: la 2, la 3 y la 4. La fila 4 es el índice 2.
    original = p.leer(MASTER, "Expensas Predio!A2:D4", render="FORMULA")
    a2 = original[0][0] if original and original[0] else ""
    a3 = original[1][0] if len(original) > 1 and original[1] else ""
    fila4 = original[2] if len(original) > 2 else []
    b4_orig = fila4[1] if len(fila4) > 1 else ""
    c4_orig = fila4[2] if len(fila4) > 2 else ""
    d4_orig = fila4[3] if len(fila4) > 3 else ""
    if b4_orig == "" or c4_orig == "" or d4_orig == "":
        raise SystemExit(
            f"CORTO: no pude leer los valores actuales de B4 (AVN), C4 (Agua) y "
            f"D4 (ABL) — leí B4={b4_orig!r} C4={c4_orig!r} D4={d4_orig!r}.\n"
            f"  Sin ellos no puedo restaurarlos después, y escribir arriba los "
            f"perdería para siempre. No toco nada."
        )
    # B4 tiene que ser el SUMIFS. Si es un número suelto, una corrida anterior
    # murió a mitad del finally y dejó pisada la fórmula: sin este corte la
    # próxima corrida "restauraría" ese número como si fuera el original y la
    # pérdida se volvería permanente, confirmada mes a mes sin que nadie avise.
    if not str(b4_orig).startswith("="):
        raise SystemExit(
            f"CORTO: B4 (Expensas AVN) ya no es una fórmula — vale {b4_orig!r}.\n"
            f"  Debería ser el SUMIFS contra Movimientos. Alguien la pisó, o una\n"
            f"  corrida anterior murió a mitad de la restauración. Volvé a poner\n"
            f"  la fórmula en B4 antes de seguir; el backup de la última corrida\n"
            f"  está en expensas_predio_backup.json, al lado de este script."
        )
    print(f"  Expensas Predio está hoy en A2={a2} A3={a3}")
    print(f"    B4 (AVN)={b4_orig}")
    print(f"    C4 (Agua)={c4_orig}  D4 (ABL)={d4_orig}  — se restaura todo al final")

    # El SUMIFS compara Movimientos!I:I contra A3. La columna I es texto
    # ("junio 2026"), así que se escribe en ese formato y NO como fecha.
    periodo_texto = f"{MESES_LARGO[mes]} {anio}"
    fecha_a2 = f"1/{mes}/{anio}"

    if dry_run:
        print("  [dry-run] no se toca la fecha de Expensas Predio.")
        return None
    if agua is None or abl is None:
        raise SystemExit(
            "CORTO: faltan --agua y/o --abl.\n"
            "  Son los dos números que se tipean a mano (C4 y D4 de Expensas\n"
            "  Predio). Sin ellos la hoja calcularía el recupero de este mes con\n"
            "  los importes del mes anterior y nadie se enteraría."
        )

    # Si el proceso muere entre el escribir y el finally (Ctrl-C, kill, caída de
    # red), el Master Plan queda con el mes y los importes de otro período
    # puestos, y eso no avisa. Se deja el backup en disco ANTES de tocar nada.
    backup = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "expensas_predio_backup.json")
    with open(backup, "w", encoding="utf-8") as fh:
        json.dump({"A2": a2, "A3": a3, "B4": b4_orig,
                   "C4": c4_orig, "D4": d4_orig}, fh,
                  ensure_ascii=False, indent=2)
    print(f"  backup de los valores originales en {backup}")

    try:
        p.escribir(MASTER, "Expensas Predio!A2:A3", [[fecha_a2], [periodo_texto]])
        p.escribir(MASTER, "Expensas Predio!C4:D4", [[agua, abl]])
        if avn is not None:
            p.escribir(MASTER, "Expensas Predio!B4", [[avn]])
        # UNFORMATTED_VALUE, no el formateado: de estas columnas salen el
        # recupero y los servicios comunes que se le cobran a cada local. La
        # celda MUESTRA "$1.176.363" pero vale 1176362,725 — leerla formateada
        # redondea la expensa de todos los locales y no avisa.
        datos = p.leer(MASTER, "Expensas Predio!A3:R30",
                       render="UNFORMATTED_VALUE")
        avn_leida = num(datos[1][1]) if len(datos) > 1 and len(datos[1]) > 1 else 0.0
        if avn_leida == 0:
            raise SystemExit(
                f"CORTO: Expensas AVN de {periodo_texto} da $0 en Movimientos.\n"
                f"  Sin esa factura el recupero sale 0 para todos los locales y "
                f"no avisa. Cargá el movimiento y volvé a correr,\n"
                f"  o pasá --avn <total de las 4 liquidaciones> si el extracto "
                f"del Macro todavía no se importó."
            )
        if avn is not None:
            # Si el valor a mano no llega entero a la celda, el recupero sale mal
            # y la única señal sería un total raro. Se compara acá.
            if abs(avn_leida - avn) > 0.01:
                raise SystemExit(
                    f"CORTO: escribí --avn {plata(avn)} en B4 pero la hoja leyó "
                    f"{plata(avn_leida)}.\n"
                    f"  No sigo con una diferencia que después nadie ve."
                )
            print(f"  Expensas AVN {periodo_texto}: {plata(avn_leida)}  "
                  f"⚠ A MANO (--avn), NO salió de Movimientos")
            print(f"    El extracto del Macro de {periodo_texto} no está importado. "
                  f"El gasto sigue faltando en Movimientos:")
            print(f"    esto NO lo carga — sólo lo usa para calcular la expensa.")
        else:
            print(f"  Expensas AVN {periodo_texto}: {plata(avn_leida)}")
        print(f"  Agua R&S: {plata(agua)} · ABL Municipal: {plata(abl)}")
        # P4 (Retiro de basura) está clavado a "mayo 2026" literal mientras sus
        # nueve hermanas usan A3. Se avisa siempre hasta que se arregle: si no,
        # el concepto viaja congelado de mes en mes sin que nadie lo note.
        p4 = p.leer(MASTER, "Expensas Predio!P4", render="FORMULA")
        if p4 and p4[0] and "mayo 2026" in str(p4[0][0]):
            print("  ⚠ Retiro de basura sigue clavado a \"mayo 2026\" en P4 "
                  "(las otras 9 columnas usan A3).")
            print("    Este mes también se reparte mayo÷3. Arreglar la fórmula.")
        out = {}
        for fila in datos[4:]:          # los locales arrancan en la fila 7
            if not fila or not fila[0]:
                continue
            recupero = num(fila[4]) if len(fila) > 4 else 0.0
            servicios = num(fila[16]) if len(fila) > 16 else 0.0
            if recupero or servicios:
                out[fila[0]] = (recupero, servicios)
        return out
    finally:
        # Cada restauración va en su propio try: si la primera falla (timeout,
        # 429, red), la segunda TIENE que correr igual. Encadenadas, un corte de
        # red al restaurar la fecha se llevaba puesta la fórmula de B4 para
        # siempre — el finally que existe para proteger era el que perdía.
        # B4 se restaura SIEMPRE, se haya pasado --avn o no: volver a escribir
        # el mismo SUMIFS no cuesta nada, perderlo sí.
        fallaron = []
        for rango, valores, que in (
            ("Expensas Predio!A2:A3", [[a2], [a3]], "la fecha (A2:A3)"),
            ("Expensas Predio!B4:D4", [[b4_orig, c4_orig, d4_orig]],
             "AVN, Agua y ABL (B4:D4)"),
        ):
            try:
                p.escribir(MASTER, rango, valores)
            except Exception as e:      # noqa: BLE001 — hay que seguir igual
                fallaron.append(f"{que}: {e}")
        if fallaron:
            print("\n  ⚠⚠ NO PUDE RESTAURAR Expensas Predio. La hoja quedó con "
                  "los valores de este mes puestos.")
            for f in fallaron:
                print(f"     · {f}")
            print(f"     Los valores originales están en {backup}:")
            print(f"       A2={a2!r}  A3={a3!r}")
            print(f"       B4={b4_orig!r}")
            print(f"       C4={c4_orig!r}  D4={d4_orig!r}")
            print("     Ponelos a mano ANTES de volver a correr esto.")
        else:
            print("  Expensas Predio restaurada a como estaba "
                  "(fecha, AVN, Agua y ABL).")


def guardar_historico(p, anio, mes, expensas, nota=None):
    """`nota` deja escrito en la hoja de dónde salió el número.

    Importa cuando el mes se congeló con --avn: el histórico es definitivo por
    diseño, así que sin la marca un valor puesto a mano queda indistinguible de
    uno que salió del extracto, y nadie vuelve a revisarlo.
    """
    if HOJA_HISTORICO not in p.hojas(CTAS):
        p.crear_hoja(CTAS, HOJA_HISTORICO)
        p.escribir(CTAS, f"{HOJA_HISTORICO}!A1:E1", [[
            "Período", "Local (Expensas Predio)", "Recupero de gastos",
            "Servicios comunes", "Nota"]])
    ya = expensas_del_historico(p, anio, mes)
    nota = nota or "congelado por cargos_del_mes.py"
    filas = [[f"{anio}-{mes:02d}", local, rec, serv, nota]
             for local, (rec, serv) in sorted(expensas.items()) if local not in ya]
    if filas:
        p.append(CTAS, f"{HOJA_HISTORICO}!A:E", filas)
    return len(filas)


# ------------------------------------------------------------------ cargos ---

def norm_etiqueta(x):
    """`JUL' 26` y `JUL'26` son el mismo mes: en Boss está tipeado con espacio."""
    return str(x or "").upper().replace(" ", "").replace("’", "'").strip()


def bloque_de_pestania(p, pestania, layout, etiqueta_mes):
    """Filas de un mes en la pestaña del local: [(fila, detalle, egreso)].

    UNFORMATTED_VALUE y no el formateado: la celda MUESTRA "732,672" pero vale
    732671.57, y leer lo que se muestra se come los centavos en silencio.
    """
    filas = p.leer(CTAS, f"{pestania}!A1:H400", render="UNFORMATTED_VALUE")
    col_det = ord(layout["detalle"]) - ord("A")
    col_egr = ord(layout["egreso"]) - ord("A")
    objetivo = norm_etiqueta(etiqueta_mes)
    out = []
    for i, r in enumerate(filas, 1):
        if not r or norm_etiqueta(r[0]) != objetivo:
            continue
        det = r[col_det].strip() if len(r) > col_det else ""
        egr = num(r[col_egr]) if len(r) > col_egr else 0.0
        out.append((i, det, egr))
    return out, len(filas)


def alquiler_vigente(p, cfg, anio, mes):
    """El alquiler del mes anterior en la pestaña — la verdad operativa de hoy.

    NO aplica ajuste por IPC: el IPC de julio sale ~15/08 y el ajuste trimestral
    de Bigg rige desde septiembre. Si un local tiene ajuste este mes, se corrige
    la propuesta a mano. El script nunca inventa un precio nuevo.
    """
    ant_a, ant_m = mes_anterior(anio, mes)
    bloque, _ = bloque_de_pestania(p, cfg["pestania"], cfg["layout"],
                                   etiqueta(ant_a, ant_m))
    # En un local partido (Bigg) el alquiler del mes son DOS filas del mismo
    # monto: la facturada y la "Diferencia" en efectivo. Se suman las dos, y
    # después proponer() lo vuelve a partir por la mitad.
    conceptos = ("alquiler", "alq facturado",
                 "diferencia alquiler (sin iva)", "diferencia alquiler", "dif alq")
    return sum(e for _, d, e in bloque if d.lower().strip() in conceptos)


def cargos_existentes(p, anio, mes):
    """Los (local, concepto) que YA tienen cargo en CARGOS para ese mes.

    Una fila en **$0 no cuenta**: son placeholders viejos, y tomarlos por cargo
    real hacía que el dedupe se comiera el cargo del mes en silencio. Le pasó a
    Boss ($470.167,09) y Peak One ($365.127,75) con los servicios comunes de
    julio: la pestaña los tenía y CARGOS no.
    """
    filas = p.leer(CTAS, "CARGOS!A4:I500")
    clave = f"{anio}-{mes:02d}"
    return {(r[1].strip(), r[2].strip()) for r in filas
            if len(r) >= 4 and str(r[0]).strip() == clave and num(r[3])}


def proponer(p, anio, mes, expensas):
    """Arma el bloque: expensas del mes anterior + alquiler del mes."""
    ant_a, ant_m = mes_anterior(anio, mes)
    propuesta = []
    avisos = []

    for local, cfg in LOCALES.items():
        desde = cfg.get("desde")
        if desde and f"{anio}-{mes:02d}" < desde:
            continue

        # --- alquiler del mes corriente
        alq = cfg["alquiler"]
        if alq == "del mes anterior":
            if not cfg["pestania"]:
                avisos.append(f"{local}: sin pestaña, no puedo leer el alquiler.")
                alq = 0
            else:
                alq = alquiler_vigente(p, cfg, anio, mes)
                if alq == 0:
                    avisos.append(
                        f"{local}: no encontré alquiler en {etiqueta(ant_a, ant_m)} "
                        f"de su pestaña. Va en 0 — confirmá el precio.")
        if alq:
            if cfg["partido"]:
                mitad = alq / 2
                propuesta.append((local, f"{anio}-{mes:02d}",
                                  "Diferencia Alquiler (sin iva)", mitad, 0.0))
                propuesta.append((local, f"{anio}-{mes:02d}", "Alquiler", mitad,
                                  mitad * IVA if cfg["iva"] else 0.0))
            else:
                propuesta.append((local, f"{anio}-{mes:02d}", "Alquiler", alq,
                                  alq * IVA if cfg["iva"] else 0.0))

        # --- expensas del mes anterior
        if cfg.get("expensas_pactadas"):
            propuesta.append((local, f"{ant_a}-{ant_m:02d}", "Servicios comunes",
                              float(cfg["expensas_pactadas"]), 0.0))
            continue
        if cfg.get("servicios_pactados"):
            propuesta.append((local, f"{anio}-{mes:02d}", "Servicios comunes",
                              float(cfg["servicios_pactados"]), 0.0))
            continue
        if expensas is None:
            avisos.append(f"{local}: expensas de {ant_a}-{ant_m:02d} sin congelar.")
            continue
        clave = cfg["expensas_predio"]
        if clave not in expensas:
            avisos.append(f"{local}: no está '{clave}' en Expensas Predio.")
            continue
        recupero, servicios = expensas[clave]
        if recupero:
            propuesta.append((local, f"{ant_a}-{ant_m:02d}",
                              "Recupero de gastos", recupero, 0.0))
        if servicios:
            propuesta.append((local, f"{ant_a}-{ant_m:02d}", "Servicios comunes",
                              servicios, servicios * IVA if cfg["iva"] else 0.0))

    return propuesta, avisos


def imprimir(propuesta, avisos, anio, mes):
    ant_a, ant_m = mes_anterior(anio, mes)
    print(f"\nBLOQUE DE COBRO — alquiler {MESES_LARGO[mes]} {anio} "
          f"+ expensas {MESES_LARGO[ant_m]} {ant_a}\n")
    print(f"  {'Local':<20}{'Período':<10}{'Concepto':<32}"
          f"{'Monto':>16}{'IVA':>14}{'Total':>16}")
    print("  " + "─" * 108)
    actual = None
    tot_general = 0.0
    for local, per, concepto, monto, iva in propuesta:
        if local != actual:
            if actual is not None:
                print()
            actual = local
        total = monto + iva
        tot_general += total
        print(f"  {local:<20}{per:<10}{concepto:<32}"
              f"{plata(monto):>16}{plata(iva) if iva else '—':>14}{plata(total):>16}")
    print("  " + "─" * 108)
    print(f"  {'TOTAL A COBRAR':<62}{plata(tot_general):>46}\n")
    if avisos:
        print("PENDIENTES (no se inventa nada):")
        for a in avisos:
            print(f"  · {a}")
        print()
    return tot_general


def escribir_cargos(p, propuesta, anio, mes):
    """Escribe en CARGOS lo que todavía no está, y verifica releyendo."""
    filas = []
    for local, per, concepto, monto, iva in propuesta:
        a, m = (int(x) for x in per.split("-"))
        ya = cargos_existentes(p, a, m)
        if (local, concepto) in ya:
            print(f"  ya estaba: {local} {per} {concepto} — no lo toco")
            continue
        cobra = LOCALES[local]["cobra_por"]
        filas.append([f"1/{m}/{a}", local, concepto, monto, iva, monto + iva,
                      "", cobra, "cargos_del_mes.py"])
    if not filas:
        print("  Nada nuevo para escribir en CARGOS.")
        return 0
    p.append(CTAS, "CARGOS!A:I", filas)
    print(f"  {len(filas)} filas agregadas a CARGOS.")

    # verificación: releer y confirmar que están, con el monto correcto
    faltan = []
    for f in filas:
        a, m = (int(x) for x in (f[0].split("/")[2], f[0].split("/")[1]))
        if (f[1], f[2]) not in cargos_existentes(p, a, m):
            faltan.append(f"{f[1]} {f[2]}")
    if faltan:
        print("  ⚠ NO quedaron escritas: " + ", ".join(faltan))
    else:
        print("  ✅ verificado: las filas están en CARGOS.")
    return len(filas)


def escribir_en_pestania(p, local, cfg, anio, mes, filas_mes):
    """Agrega el bloque del mes al final de la pestaña del local.

    NO escribe la columna SALDO: las filas de abajo del último bloque ya vienen
    con la fórmula encadenada copiada (`=G{n-1}+E{n}-F{n}`), así que el saldo se
    calcula solo. Escribirlo a mano rompería la cadena.

    Sólo toca filas vacías en Mes y Detalle, y verifica releyendo.
    """
    if not cfg["pestania"] or not cfg["layout"]:
        return None, f"{local}: no tiene pestaña con bloques mensuales — sólo CARGOS."

    layout = cfg["layout"]
    datos = p.leer(CTAS, f"{cfg['pestania']}!A1:H400")
    col_det = ord(layout["detalle"]) - ord("A")

    # DEDUPE por (mes, concepto): si ese concepto ya está bajo esa etiqueta, no
    # se vuelve a escribir. Sin esto, correr el script dos veces duplica el mes
    # entero en la pestaña — y como el saldo es una cadena de fórmulas, el
    # duplicado se suma solo al saldo del local sin que nada avise.
    # Va por par y no sólo por concepto: un bloque trae dos meses (las expensas
    # de M y el alquiler de M+1), así que "Servicios comunes" puede aparecer
    # legítimamente bajo dos etiquetas distintas.
    etq = etiqueta(anio, mes)
    ya_estan = {(norm_etiqueta(r[0]), str(r[col_det]).strip().lower())
                for r in datos if r and len(r) > col_det}
    pendientes = [(e, med, d, m) for e, med, d, m in filas_mes
                  if (norm_etiqueta(e), d.strip().lower()) not in ya_estan]
    if not pendientes:
        return [], f"{local}: {etq} ya estaba en su pestaña — no escribo nada."
    if len(pendientes) < len(filas_mes):
        saltados = len(filas_mes) - len(pendientes)
        print(f"    ({local}: {saltados} concepto/s ya estaban)")
    filas_mes = pendientes

    # última fila con algo en Mes o Detalle
    ultima = 0
    for i, r in enumerate(datos, 1):
        mes_c = str(r[0]).strip() if r else ""
        det_c = str(r[col_det]).strip() if len(r) > col_det else ""
        if mes_c or det_c:
            ultima = i
    destino = ultima + 1

    # las filas destino tienen que estar libres en Mes y Detalle
    for k in range(len(filas_mes)):
        fila = destino + k
        r = datos[fila - 1] if fila - 1 < len(datos) else []
        mes_c = str(r[0]).strip() if r else ""
        det_c = str(r[col_det]).strip() if len(r) > col_det else ""
        if mes_c or det_c:
            return None, (f"{local}: la fila {fila} de su pestaña no está vacía "
                          f"({mes_c!r} / {det_c!r}) — no escribo nada ahí.")

    escritas = []
    for k, (etq_fila, medio, detalle, monto) in enumerate(filas_mes):
        fila = destino + k
        # A y B van juntas en una sola escritura: son contiguas en TODAS las
        # pestañas (la B es "Medio"/"UN"), aunque el resto de las letras cambie
        # de local en local.
        p.escribir(CTAS, f"{cfg['pestania']}!A{fila}:B{fila}",
                   [[etq_fila, medio]])
        p.escribir(CTAS, f"{cfg['pestania']}!{layout['detalle']}{fila}", [[detalle]])
        p.escribir(CTAS, f"{cfg['pestania']}!{layout['egreso']}{fila}", [[monto]])
        escritas.append((fila, detalle, monto))

    # verificación: releer las filas escritas, sin formato — la celda muestra
    # "1,670,892" pero vale 1670892.3, y comparar contra lo mostrado da falsos
    # negativos en todo importe con centavos.
    rango = f"{cfg['pestania']}!A{destino}:H{destino + len(filas_mes) - 1}"
    control = p.leer(CTAS, rango, render="UNFORMATTED_VALUE")
    problemas = []
    for k, (fila, detalle, monto) in enumerate(escritas):
        r = control[k] if k < len(control) else []
        leido_det = str(r[col_det]).strip() if len(r) > col_det else ""
        col_egr = ord(layout["egreso"]) - ord("A")
        leido_mon = num(r[col_egr]) if len(r) > col_egr else 0.0
        if leido_det != detalle or abs(leido_mon - monto) > 0.01:
            problemas.append(f"fila {fila}: quedó {leido_det!r} {leido_mon}")
    return escritas, ("; ".join(problemas) if problemas else None)


def filas_para_pestania(propuesta, local, anio, mes):
    """Las filas del BLOQUE de un local, en el orden de la pestaña.

    Un bloque es alquiler del mes M+1 **+ expensas del mes M**: las dos cosas
    van juntas bajo la misma etiqueta (AGO'26), que es como se le manda al
    locatario y como están los bloques viejos de la planilla.

    Filtrar sólo por el período del alquiler dejaba las expensas afuera de la
    pestaña — entraban a CARGOS y el bloque quedaba con el alquiler solo. Como
    el SALDO de la pestaña es la cadena `saldo anterior + Ingreso − Egreso`, esa
    expensa no se le reclamaba nunca al locatario, y nada avisaba: el script
    escribía en CARGOS, decía "verificado" y después "ya estaba, no escribo".
    Pasó en JUL'26 y AGO'26 de Fabric, Bigg, Boss y Volta.

    El IVA sale de la propuesta, no se recalcula: ahí ya está resuelto qué
    concepto lleva IVA para cada local.
    """
    orden = ["Diferencia Alquiler (sin iva)", "Alquiler", "Recupero de gastos",
             "Servicios comunes"]
    ant_a, ant_m = mes_anterior(anio, mes)
    # La columna "Mes Origen" de la pestaña lleva el PERÍODO DEL CARGO, no el
    # del bloque: en JUN'26 de Fabric están el alquiler de junio Y el recupero
    # de junio. Así que cada fila viaja con su propia etiqueta — las expensas
    # de julio van bajo JUL'26 aunque se cobren junto al alquiler de agosto.
    periodos = {f"{anio}-{mes:02d}": etiqueta(anio, mes),
                f"{ant_a}-{ant_m:02d}": etiqueta(ant_a, ant_m)}
    del_mes = [(per, c, m, iva) for (l, per, c, m, iva) in propuesta
               if l == local and per in periodos]
    del_mes.sort(key=lambda x: (x[0],
                                orden.index(x[1]) if x[1] in orden else 99))
    salida = []
    for per, concepto, monto, iva in del_mes:
        etq = periodos[per]
        medio = medio_de(local, concepto)
        salida.append((etq, medio, concepto, monto))
        if iva:
            # "Servicios comunes" → "IVA Servicios Comunes", como en los
            # bloques que ya están escritos en las pestañas. El IVA sigue al
            # concepto que lo generó: si eso se cobra por banco, su IVA también.
            salida.append((etq, medio,
                           "IVA Alquiler" if concepto == "Alquiler"
                           else f"IVA {concepto.title()}", iva))
    return salida


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mes", help="AAAA-MM del ALQUILER (las expensas son del mes anterior)")
    ap.add_argument("--escribir", action="store_true",
                    help="escribe en CARGOS (sin esto solo propone)")
    ap.add_argument("--congelar-expensas", action="store_true",
                    help="toca la fecha de Expensas Predio y la restaura")
    ap.add_argument("--agua", type=float, default=None,
                    help="Agua R&S del mes de las expensas (C4, se tipea a mano)")
    ap.add_argument("--abl", type=float, default=None,
                    help="ABL Municipal: SOLO Tasa por Servicios + Cont. Hospital. "
                         "Los derechos de construcción y el plan de pagos de la "
                         "misma liquidación son obra y NO van acá.")
    ap.add_argument("--avn", type=float, default=None,
                    help="Expensas AVN del mes, a mano, para cuando el extracto "
                         "del Macro todavía no se importó. Es la suma de las 4 "
                         "liquidaciones de la carpeta del mes SIGUIENTE (la "
                         "carpeta es el mes de pago). Sin esto B4 sale del "
                         "SUMIFS contra Movimientos, que es lo normal.")
    args = ap.parse_args()

    anio, mes = parse_mes(args.mes)
    ant_a, ant_m = mes_anterior(anio, mes)
    p = Planillas()

    print(f"Cuentas corrientes — Paseo Nordelta")
    print(f"Alquiler de {MESES_LARGO[mes]} {anio} + expensas de "
          f"{MESES_LARGO[ant_m]} {ant_a}\n")

    expensas = expensas_del_historico(p, ant_a, ant_m)
    if expensas:
        print(f"Expensas de {ant_a}-{ant_m:02d}: {len(expensas)} locales "
              f"desde {HOJA_HISTORICO} (ya congeladas).")
    elif args.congelar_expensas:
        print(f"Congelando expensas de {MESES_LARGO[ant_m]} {ant_a}…")
        expensas = congelar_expensas(p, ant_a, ant_m, agua=args.agua,
                                     abl=args.abl, avn=args.avn,
                                     dry_run=not args.escribir)
        if expensas and args.escribir:
            nota = None
            if args.avn is not None:
                nota = (f"congelado por cargos_del_mes.py — AVN {plata(args.avn)} "
                        f"puesta A MANO (--avn): el extracto del Macro de "
                        f"{MESES_LARGO[ant_m]} {ant_a} no estaba importado")
            n = guardar_historico(p, ant_a, ant_m, expensas, nota=nota)
            print(f"  {n} filas guardadas en {HOJA_HISTORICO}.")
    else:
        print(f"Expensas de {ant_a}-{ant_m:02d}: NO están congeladas.")
        print(f"  Corré con --congelar-expensas para traerlas "
              f"(toca y restaura la fecha del Master Plan).")
        expensas = None
    print()

    propuesta, avisos = proponer(p, anio, mes, expensas)
    imprimir(propuesta, avisos, anio, mes)

    if not args.escribir:
        print("[SIN --escribir] No toqué nada. Revisá la tabla y volvé a correr "
              "con --escribir.")
        return
    print("Escribiendo en CARGOS…")
    escribir_cargos(p, propuesta, anio, mes)

    print("\nEscribiendo en las pestañas de cada local…")
    for local in dict.fromkeys(l for l, *_ in propuesta):
        filas_mes = filas_para_pestania(propuesta, local, anio, mes)
        if not filas_mes:
            continue
        escritas, problema = escribir_en_pestania(
            p, local, LOCALES[local], anio, mes, filas_mes)
        if escritas is None:
            print(f"  ⚠ {problema}")
        elif not escritas:
            print(f"  · {problema}")
        elif problema:
            print(f"  ⚠ {local}: escrito pero la relectura NO coincide → {problema}")
        else:
            r0, r1 = escritas[0][0], escritas[-1][0]
            print(f"  ✅ {local}: filas {r0}-{r1} de «{LOCALES[local]['pestania']}» "
                  f"({len(escritas)} conceptos), verificado.")


if __name__ == "__main__":
    main()
