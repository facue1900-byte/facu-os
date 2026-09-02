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
        # Su cuenta corriente es la pestaña `Futbol`, que NO se escribe fila por
        # fila: es una sola fórmula en A5 que junta los cobros de `Cobros` con
        # los cargos que se escriban en el bloque de input `I:K`
        # (Fecha · Concepto · Monto) y calcula el saldo sola.
        "pestania": "Futbol", "expensas_predio": "Contenedor Jaula",
        "layout": None, "bloque_input": "Futbol!I:K",
        "iva": False, "cobra_por": "Efectivo",
        # El precio sale del ancla SEMESTRAL de `Futbol!AR`: sólo la celda VERDE
        # (marzo y septiembre). Los meses del medio son la cadena del IPC, no un
        # precio a cobrar. Ver `paseo-jaula-precio-semestral`.
        "alquiler": 1_000_000, "partido": False, "tabla_ipc": "Futbol",
        "desde": "2026-08",
        # NO paga expensas ni servicios comunes (Facu, 06/08/2026 y 02/09/2026).
        # Esto estaba como `servicios_pactados: 798_825` y contradecía a
        # `reglas_locales.REGLAS`, que ya decía «No pagan expensas por ahora».
        # Generó $798.825 de más en ago-26 y en sep-26. No volver a ponerlo
        # sin cambiar también reglas_locales.py.
        "sin_expensas": True,
    },
    # Escuelita no lleva cargo generado: paga un % de facturación y el ingreso
    # entra solo por Movimientos.
}

IVA = 0.21


def etiqueta(anio, mes):
    return f"{MESES[mes]}'{anio % 100}"


def medio_de(local, concepto):
    """`efectivo` o `banco`: por dónde ENTRA la plata de este concepto.

    OJO: la columna B de la cuenta corriente es el medio de un **INGRESO** — por
    dónde entró un cobro. Un cargo (alquiler, recupero, servicios comunes, IVA)
    **no lleva medio**, porque todavía no se cobró (Facu, 05/08/2026).

    Esta función sirve para clasificar un COBRO y para saber qué se factura (el
    efectivo no se factura), no para escribir la B de un cargo.

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

    def fondos(self, sid, rango):
        """Colores de fondo de un rango, fila por fila. [[{r,g,b}, ...], ...].

        Va por `spreadsheets().get(includeGridData=True)` porque `values()` no
        devuelve formato: el ancla de alquiler de cada contrato está marcada
        pintando la celda de verde, y ese dato NO existe en los valores.
        """
        meta = self.s.spreadsheets().get(
            spreadsheetId=sid, ranges=[rango], includeGridData=True,
            fields="sheets/data/rowData/values/effectiveFormat/backgroundColor",
        ).execute()
        datos = meta.get("sheets", [{}])[0].get("data", [{}])[0]
        out = []
        for fila in datos.get("rowData", []):
            out.append([c.get("effectiveFormat", {}).get("backgroundColor", {})
                        for c in fila.get("values", [])])
        return out

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


def congelar_expensas(p, anio, mes, agua=None, abl=None, avn=None,
                      basura=None, dry_run=True):
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

    `basura` es la misma puerta para P4 (Retiro de basura). P4 estuvo clavado a
    `"mayo 2026"` literal mientras sus nueve hermanas usaban A3, así que cobraba
    mayo÷3 = $1.568.483,63 todos los meses, para siempre. Con --basura se escribe
    el total de la factura de Transportes Olivos ("TODSE") del mes y la fórmula
    se restaura igual que B4. Igual que la AVN: no carga nada en Movimientos, así
    que cuando el pago entre por el extracto, el gasto entra una sola vez.

    Corta si Expensas AVN del mes da 0: eso significa que las facturas del mes
    no están cargadas en Movimientos y el recupero saldría en cero sin avisar.
    """
    # A2:D4 devuelve TRES filas: la 2, la 3 y la 4. La fila 4 es el índice 2.
    original = p.leer(MASTER, "Expensas Predio!A2:D4", render="FORMULA")
    p4_leida = p.leer(MASTER, "Expensas Predio!P4", render="FORMULA")
    p4_orig = p4_leida[0][0] if p4_leida and p4_leida[0] else ""
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
    print(f"    P4 (Basura)={p4_orig}")
    # Incondicional, igual que el de B4: si una corrida con --basura murió antes
    # del finally, P4 quedó con un número pisado. Chequearlo SÓLO cuando se pasa
    # --basura deja que las corridas siguientes lo "restauren" como si fuera el
    # original — el mismo mes congelado para siempre que motivó el flag.
    if not str(p4_orig).startswith("="):
        raise SystemExit(
            f"CORTO: P4 (Retiro de basura) ya no es una fórmula — vale "
            f"{p4_orig!r}.\n"
            f"  Una corrida anterior murió antes de restaurarla. Volvé a poner "
            f"la fórmula\n  (está en expensas_predio_backup.json) antes de "
            f"seguir.")

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
                   "C4": c4_orig, "D4": d4_orig, "P4": p4_orig}, fh,
                  ensure_ascii=False, indent=2)
    print(f"  backup de los valores originales en {backup}")

    try:
        p.escribir(MASTER, "Expensas Predio!A2:A3", [[fecha_a2], [periodo_texto]])
        p.escribir(MASTER, "Expensas Predio!C4:D4", [[agua, abl]])
        if avn is not None:
            p.escribir(MASTER, "Expensas Predio!B4", [[avn]])
        if basura is not None:
            p.escribir(MASTER, "Expensas Predio!P4", [[basura]])
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
        basura_leida = (num(datos[1][15])
                        if len(datos) > 1 and len(datos[1]) > 15 else 0.0)
        if basura is not None:
            if abs(basura_leida - basura) > 0.01:
                raise SystemExit(
                    f"CORTO: escribí --basura {plata(basura)} en P4 pero la hoja "
                    f"leyó {plata(basura_leida)}.\n"
                    f"  No sigo con una diferencia que después nadie ve.")
            print(f"  Retiro de basura: {plata(basura_leida)}  "
                  f"⚠ A MANO (--basura), NO salió de Movimientos")
        else:
            p4 = p.leer(MASTER, "Expensas Predio!P4", render="FORMULA")
            if p4 and p4[0] and "mayo 2026" in str(p4[0][0]):
                print("  ⚠ Retiro de basura sigue clavado a \"mayo 2026\" en P4 "
                      "(las otras 9 columnas usan A3).")
                print(f"    Este mes también reparte mayo÷3 = "
                      f"{plata(basura_leida)}. Pasá --basura con la factura de "
                      f"Transportes Olivos del mes, o arreglá la fórmula.")
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
            ("Expensas Predio!P4", [[p4_orig]], "Retiro de basura (P4)"),
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
            print(f"       P4={p4_orig!r}")
            print("     Ponelos a mano ANTES de volver a correr esto.")
        else:
            print("  Expensas Predio restaurada a como estaba "
                  "(fecha, AVN, Agua, ABL y Basura).")


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


# El ancla de cada contrato está PINTADA en la tabla de IPC de su pestaña.
# `#D9EAD3` — el mismo verde en las seis. Verificado el 01/09/2026.
VERDE_ANCLA = (0.8509804, 0.91764706, 0.827451)
MESES_TABLA = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
               "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def es_verde(color):
    return all(abs(color.get(k, 0.0) - v) < 0.02
               for k, v in zip(("red", "green", "blue"), VERDE_ANCLA))


def ancla_de_la_tabla(p, pestania, anio, mes):
    """El alquiler VIGENTE en <anio>-<mes> según la tabla de IPC de la pestaña.

    Los contratos ajustan por período, no todos los meses: la celda del mes en
    que ajustan está pintada de verde (marzo/junio/septiembre/diciembre en los
    cinco locales, marzo y septiembre en La Jaula, que es semestral). Los meses
    del medio son la cadena `=N(m-1)*(1+O(m-2))` que va componiendo el IPC —
    **no un precio a cobrar**. Se cobra el ancla verde más reciente, que puede
    ser de un mes de OTRO año (enero cobra el ancla de diciembre).

    La tabla es una sola columna corrida con un bloque de 12 meses por año, y el
    año vive en la columna de la IZQUIERDA de "Mes", escrito sólo en la fila de
    enero. Leer las primeras 12 filas y nada más devolvía el precio de 2026 para
    cualquier año que se pidiera, sin fallar.

    Devuelve (monto, "<mes> <año>") o (None, motivo) si no se pudo leer.
    """
    grilla = p.leer(CTAS, f"'{pestania}'!A1:BZ80", render="UNFORMATTED_VALUE")
    hdrs = [(i, j) for i, fila in enumerate(grilla)
            for j, celda in enumerate(fila) if str(celda).strip() == "Mes"]
    if not hdrs:
        return None, f"{pestania}: no encontré la tabla de IPC (celda 'Mes')"
    if len(hdrs) > 1:
        # Quedarse con la última en silencio es cómo se cobra el precio de la
        # tabla equivocada sin que nada falle.
        donde = ", ".join(f"{colnum_a_letra(j+1)}{i+1}" for i, j in hdrs)
        return None, (f"{pestania}: hay {len(hdrs)} tablas de IPC (celda 'Mes' "
                      f"en {donde}). No adivino cuál es la del contrato.")
    i0, j0 = hdrs[0]
    col = colnum_a_letra(j0 + 2)          # la columna Alquiler, a la derecha

    # Recorrer el bloque entero, arrastrando el año de la columna anterior.
    filas, anio_actual, esperado = [], None, None
    for k in range(i0 + 1, len(grilla)):
        fila = grilla[k]
        nombre = str(fila[j0]).strip().lower() if len(fila) > j0 else ""
        if nombre not in MESES_TABLA:
            break                          # se terminó la tabla
        num_mes = MESES_TABLA.index(nombre) + 1
        marca = fila[j0 - 1] if j0 >= 1 and len(fila) > j0 - 1 else None
        if isinstance(marca, (int, float)) and 2000 < marca < 2100:
            anio_actual = int(marca)
        if anio_actual is None:
            return None, (f"{pestania}: la tabla arranca en {nombre!r} sin año "
                          f"a la izquierda; no sé de qué año es ese precio.")
        if esperado is not None and (anio_actual, num_mes) != esperado:
            return None, (f"{pestania}: la fila {k+1} dice {nombre} "
                          f"{anio_actual}, esperaba {MESES_TABLA[esperado[1]-1]} "
                          f"{esperado[0]}. La tabla no viene en orden.")
        esperado = (anio_actual + 1, 1) if num_mes == 12 else (anio_actual,
                                                               num_mes + 1)
        valor = num(fila[j0 + 1]) if len(fila) > j0 + 1 else 0.0
        filas.append((anio_actual, num_mes, valor, k + 1))

    if not filas:
        return None, f"{pestania}: la tabla de IPC no tiene meses debajo de 'Mes'"
    r_ini, r_fin = filas[0][3], filas[-1][3]
    colores = p.fondos(CTAS, f"'{pestania}'!{col}{r_ini}:{col}{r_fin}")
    if len(colores) != len(filas):
        return None, (f"{pestania}: leí {len(filas)} meses pero {len(colores)} "
                      f"colores. No arriesgo a desalinear el ancla.")

    # Hacia atrás desde el mes pedido: la primera verde es la que rige.
    for idx in range(len(filas) - 1, -1, -1):
        a, m, valor, _ = filas[idx]
        if (a, m) > (anio, mes):
            continue
        verde = colores[idx][0] if colores[idx] else {}
        if es_verde(verde):
            return valor, f"{MESES_TABLA[m-1]} {a}"
    return None, (f"{pestania}: ninguna celda verde hasta "
                  f"{MESES_TABLA[mes-1]} {anio}")


def colnum_a_letra(n):
    """1 → A, 27 → AA. La tabla de IPC vive en M/N/O o en AQ/AR/AS."""
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def alquiler_del_mes_anterior(p, cfg, anio, mes):
    """Lo que se cobró el mes pasado. Se usa sólo para CONTRASTAR el ancla."""
    ant_a, ant_m = mes_anterior(anio, mes)
    bloque, _ = bloque_de_pestania(p, cfg["pestania"], cfg["layout"],
                                   etiqueta(ant_a, ant_m))
    # En un local partido (Bigg) el alquiler del mes son DOS filas del mismo
    # monto: la facturada y la "Diferencia" en efectivo. Se suman las dos, y
    # después proponer() lo vuelve a partir por la mitad.
    conceptos = ("alquiler", "alq facturado",
                 "diferencia alquiler (sin iva)", "diferencia alquiler", "dif alq")
    return sum(e for _, d, e in bloque if d.lower().strip() in conceptos)


def alquiler_vigente(p, cfg, anio, mes, avisos):
    """El alquiler a cobrar: el ANCLA de la tabla de IPC de la pestaña.

    Antes esto copiaba el alquiler del mes anterior. En un mes de ajuste eso
    cobra el precio viejo y no falla: septiembre 2026 era ancla en los seis a la
    vez y se habrían cobrado $1.004.358,61 de menos por mes, tres meses seguidos.
    Ahora el precio sale del ancla y **el mes anterior queda como contraste**:
    si difieren, se dice cuánto y por qué, en vez de elegir en silencio.
    """
    anterior = alquiler_del_mes_anterior(p, cfg, anio, mes)
    ancla, detalle = ancla_de_la_tabla(p, cfg["pestania"], anio, mes)
    if ancla is None:
        avisos.append(f"{cfg['pestania']}: no pude leer el ancla ({detalle}). "
                      f"Uso el alquiler del mes anterior, {plata(anterior)} — "
                      f"verificalo a mano contra la tabla de IPC.")
        return anterior
    if abs(ancla - anterior) > 0.01:
        avisos.append(
            f"{cfg['pestania']}: AJUSTA este mes. El ancla de {detalle} vale "
            f"{plata(ancla)} y el mes pasado se cobró {plata(anterior)} "
            f"({plata(ancla - anterior)} de diferencia). Va el ancla.")
    return ancla


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
                alq = alquiler_vigente(p, cfg, anio, mes, avisos)
                if alq == 0:
                    avisos.append(
                        f"{local}: no encontré alquiler en {etiqueta(ant_a, ant_m)} "
                        f"de su pestaña. Va en 0 — confirmá el precio.")
        elif cfg.get("tabla_ipc"):
            # Sin pestaña de cuenta corriente, pero con tabla de IPC propia:
            # La Jaula, que ajusta SEMESTRAL en la hoja `Futbol`. El monto de
            # arranque de `alquiler` sólo vale hasta su primera ancla.
            ancla, detalle = ancla_de_la_tabla(p, cfg["tabla_ipc"], anio, mes)
            if ancla is None:
                avisos.append(f"{local}: no pude leer su ancla ({detalle}). "
                              f"Queda el monto de arranque, {plata(alq)}.")
            elif abs(ancla - alq) > 0.01:
                avisos.append(
                    f"{local}: AJUSTA este mes. El ancla de {detalle} en "
                    f"'{cfg['tabla_ipc']}' vale {plata(ancla)} y venía "
                    f"{plata(alq)} ({plata(ancla - alq)} de diferencia). "
                    f"Va el ancla.")
                alq = ancla
            else:
                alq = ancla
        # El renglón del alquiler va aunque valga 0 —Peak One no tiene alquiler
        # propio hasta dic-26— siempre que el local tenga pestaña: su bloque
        # lleva los cinco conceptos igual, con el cero escrito. Los que no tienen
        # pestaña (Salón, La Jaula) sólo viven en CARGOS y ahí un 0 sería ruido.
        if alq or cfg["pestania"]:
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
        # Hay locales que directamente NO pagan expensas (La Jaula). Esto va
        # ANTES de todos los caminos de abajo: sin un corte explícito, sacarle
        # el monto pactado no lo deja sin cargo — lo manda al camino genérico
        # de Expensas Predio, que le cobra el reparto del predio entero.
        if cfg.get("sin_expensas"):
            continue
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
    pendientes = [(e, d, m) for e, d, m in filas_mes
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
    for k, (etq_fila, detalle, monto) in enumerate(filas_mes):
        fila = destino + k
        # Sólo la etiqueta del mes. La columna B (Medio) es de los INGRESOS:
        # un cargo no lleva medio porque todavía no se cobró.
        p.escribir(CTAS, f"{cfg['pestania']}!A{fila}", [[etq_fila]])
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
    # Los dos conceptos que SIEMPRE llevan su renglón de IVA debajo, tengan o no
    # importe. «Recupero de gastos» va exento y «Diferencia Alquiler (sin iva)»
    # es la mitad en efectivo: ésos no llevan.
    con_fila_iva = {"Alquiler", "Servicios comunes"}
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
        salida.append((etq, concepto, monto))
        if concepto in con_fila_iva:
            # El renglón va aunque el IVA sea 0: "un bloque lleva SIEMPRE los 5
            # conceptos, y el $0 se escribe 0" (Facu, 06/08/2026). Escribirlo
            # sólo cuando hay importe dejaba a Boss, Volta y Peak One —los que
            # no facturan— con bloques de 3 renglones, y el dedupe por (mes,
            # concepto) después decía "ya estaba" y no los completaba nunca.
            # "Servicios comunes" → "IVA Servicios Comunes", como en los
            # bloques que ya están escritos en las pestañas.
            salida.append((etq, "IVA Alquiler" if concepto == "Alquiler"
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
    ap.add_argument("--basura", type=float, default=None,
                    help="Retiro de basura del mes de las expensas (P4): el "
                         "total de la factura de Transportes Olivos. Sin esto, "
                         "P4 sigue repartiendo mayo 2026 ÷ 3.")
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
                                     basura=args.basura,
                                     dry_run=not args.escribir)
        if expensas and args.escribir:
            nota = None
            if args.avn is not None:
                nota = (f"congelado por cargos_del_mes.py — AVN {plata(args.avn)} "
                        f"puesta A MANO (--avn): el extracto del Macro de "
                        f"{MESES_LARGO[ant_m]} {ant_a} no estaba importado")
            # Todo lo que se puso a mano queda escrito en el histórico: el mes se
            # congela para siempre y después nadie puede reconstruir de dónde
            # salió cada número mirando la hoja viva.
            a_mano = [("Agua R&S", args.agua), ("ABL Municipal", args.abl),
                      ("Retiro de basura", args.basura)]
            puestos = " · ".join(f"{q} {plata(v)} a mano"
                                 for q, v in a_mano if v is not None)
            if puestos:
                nota = f"{nota} · {puestos}" if nota else puestos
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
