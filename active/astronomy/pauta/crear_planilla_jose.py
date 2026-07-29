#!/usr/bin/env python3
"""Crea la planilla de registro de conversaciones de WhatsApp de Astronomy Academy.

El único dato que falta para decidir el presupuesto de pauta es la tasa de cierre:
de cada conversación que entra por un anuncio, cuántas terminan en un alumno que
paga. Meta no lo puede saber (la venta se cierra por WhatsApp y por Mercado Pago,
fuera de todo píxel), así que se registra a mano durante cuatro semanas.

La planilla está diseñada para que cargar una conversación tarde menos de quince
segundos: todo es desplegable, no hay texto libre obligatorio. Si tarda más, José
no la va a completar y no vamos a tener el dato.

    .venv/bin/python active/astronomy/pauta/crear_planilla_jose.py

**No comparte la planilla con nadie.** La crea en el Drive de Facu y devuelve el
link; compartirla con José es una decisión de Facu, no del script.
"""

import sys

sys.path.insert(0, "/Users/Facu/facu-os/execution")
from google_auth import sheets  # noqa: E402

TITULO = "Astronomy Academy — Registro de conversaciones de WhatsApp"

# El costo por conversación nueva sale del histórico de Meta (US$7.071 / 3.639
# contactos nuevos, cuenta CP - Astronomy Academy, ago-2023 a jul-2026). El CAC
# objetivo sale del análisis de retención en PAUTA_ACADEMY.md.
COSTO_LEAD_USD = 1.94
CAC_OBJETIVO_USD = 57

PRODUCTOS = ["Curso de DJ", "Producción presencial", "Producción online", "Membresías", "Modo Profesional", "Otro / no sé"]
ORIGENES = ["Pauta (mensaje automático)", "Orgánico (escribió solo)", "Referido", "No sé"]
ESTADOS = ["Nuevo", "En conversación", "Agendó clase de prueba", "CERRÓ — pagó", "Perdido", "Fantasma (no contestó más)"]

CABECERAS = ["Fecha", "Nombre", "Teléfono", "Producto", "De dónde vino", "Estado", "Fecha de cierre", "Monto ARS", "Nota"]

INSTRUCCIONES = [
    ["CÓMO SE COMPLETA ESTO"],
    [""],
    ["Una fila por CADA persona que escribe al WhatsApp. Aunque no conteste nunca."],
    ["Se completa apenas entra el mensaje: no lo dejes para el final del día."],
    [""],
    ["LA COLUMNA QUE MÁS IMPORTA: 'De dónde vino'"],
    [""],
    ["Si el primer mensaje que te llega es uno de estos textos exactos, vino de un anuncio:"],
    ["      'Hola! Vi el Curso de DJ y quiero info'"],
    ["      'Hola! Vi el curso de Produccion Musical y quiero info'"],
    ["      'Hola! Vi Produccion Musical online y quiero info'"],
    ["      'Hola! Vi las membresias de la Academy y quiero info'"],
    ["      'Hola! Vi el Modo Profesional y quiero info'"],
    [""],
    ["Esos mensajes los escribe el anuncio solo, la persona no los tipea."],
    ["Si el mensaje es cualquier otra cosa, es orgánico o referido."],
    [""],
    ["LOS ESTADOS"],
    [""],
    ["Nuevo                       Escribió y todavía no le contestaste"],
    ["En conversación             Están hablando"],
    ["Agendó clase de prueba      Reservó, todavía no pagó"],
    ["CERRÓ — pagó                Pagó. Poné fecha de cierre y monto"],
    ["Perdido                     Habló, no compró"],
    ["Fantasma (no contestó más)  Escribió una vez y desapareció"],
    [""],
    ["'Perdido' y 'Fantasma' son distintos y la diferencia importa:"],
    ["muchos fantasmas = los anuncios traen gente que no era;"],
    ["muchos perdidos = el problema está en el precio o en el cierre."],
    [""],
    ["Cuatro semanas de esto deciden si la pauta sube a US$600 por mes o se apaga."],
]


def col(i):
    return chr(ord("A") + i)


def main():
    api = sheets(cuenta="facu")

    libro = api.spreadsheets().create(
        body={
            "properties": {"title": TITULO, "locale": "es_AR", "timeZone": "America/Argentina/Buenos_Aires"},
            "sheets": [
                {"properties": {"sheetId": 0, "title": "Conversaciones", "gridProperties": {"frozenRowCount": 1, "columnCount": len(CABECERAS)}}},
                {"properties": {"sheetId": 1, "title": "Resumen"}},
                {"properties": {"sheetId": 2, "title": "Instrucciones"}},
            ],
        }
    ).execute()
    sid = libro["spreadsheetId"]

    resumen = [
        ["RESUMEN — se calcula solo, no toques nada acá", ""],
        ["", ""],
        ["Costo por conversación (US$)", COSTO_LEAD_USD],
        ["CAC que aguanta el negocio (US$)", CAC_OBJETIVO_USD],
        ["", ""],
        ["TODAS LAS CONVERSACIONES", ""],
        ["Total", "=COUNTA(Conversaciones!A2:A)"],
        ["Cerradas", '=COUNTIF(Conversaciones!F2:F;"CERRÓ — pagó")'],
        ["Tasa de cierre", "=IFERROR(B8/B7;0)"],
        ["", ""],
        ["SOLO LAS QUE VINIERON DE PAUTA", ""],
        ["Conversaciones de pauta", '=COUNTIF(Conversaciones!E2:E;"Pauta (mensaje automático)")'],
        ["Cerradas de pauta", '=COUNTIFS(Conversaciones!E2:E;"Pauta (mensaje automático)";Conversaciones!F2:F;"CERRÓ — pagó")'],
        ["Fantasmas de pauta", '=COUNTIFS(Conversaciones!E2:E;"Pauta (mensaje automático)";Conversaciones!F2:F;"Fantasma (no contestó más)")'],
        ["Tasa de cierre de pauta", "=IFERROR(B13/B12;0)"],
        ["", ""],
        ["EL NÚMERO QUE DECIDE TODO", ""],
        ["CAC real (US$)", "=IFERROR(B3/B15;\"faltan datos\")"],
        ["Veredicto", '=IF(B13<5;"Todavía no hay suficientes cierres para concluir. Seguí cargando.";IF(B18<B4;"ESCALAR — el CAC está por debajo de lo que el negocio aguanta";IF(B18<90;"NO ESCALAR todavía — optimizar creativo y segmentación";"APAGAR — el problema no es la pauta")))'],
        ["", ""],
        ["Facturado en el período (ARS)", '=SUMIF(Conversaciones!F2:F;"CERRÓ — pagó";Conversaciones!H2:H)'],
    ]

    api.spreadsheets().values().batchUpdate(
        spreadsheetId=sid,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "Conversaciones!A1", "values": [CABECERAS]},
                {"range": "Resumen!A1", "values": resumen},
                {"range": "Instrucciones!A1", "values": INSTRUCCIONES},
            ],
        },
    ).execute()

    def validacion(idx, opciones):
        return {
            "setDataValidation": {
                "range": {"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2000, "startColumnIndex": idx, "endColumnIndex": idx + 1},
                "rule": {
                    "condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": o} for o in opciones]},
                    "showCustomUi": True,
                    "strict": True,
                },
            }
        }

    pedidos = [
        validacion(3, PRODUCTOS),
        validacion(4, ORIGENES),
        validacion(5, ESTADOS),
        # Cabecera en negro
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {"userEnteredFormat": {
                    "backgroundColor": {"red": 0.08, "green": 0.08, "blue": 0.10},
                    "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True},
                }},
                "fields": "userEnteredFormat(backgroundColor,textFormat)",
            }
        },
        # Verde para los que cerraron, gris para los fantasmas
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2000, "endColumnIndex": len(CABECERAS)}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$F2="CERRÓ — pagó"'}]},
                        "format": {"backgroundColor": {"red": 0.85, "green": 0.94, "blue": 0.86}},
                    },
                },
                "index": 0,
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": 0, "startRowIndex": 1, "endRowIndex": 2000, "endColumnIndex": len(CABECERAS)}],
                    "booleanRule": {
                        "condition": {"type": "CUSTOM_FORMULA", "values": [{"userEnteredValue": '=$F2="Fantasma (no contestó más)"'}]},
                        "format": {"backgroundColor": {"red": 0.94, "green": 0.94, "blue": 0.94}},
                    },
                },
                "index": 1,
            }
        },
        {"updateSheetProperties": {"properties": {"sheetId": 1, "gridProperties": {"frozenRowCount": 1}}, "fields": "gridProperties.frozenRowCount"}},
        {"autoResizeDimensions": {"dimensions": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": len(CABECERAS)}}},
        {"autoResizeDimensions": {"dimensions": {"sheetId": 1, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 2}}},
        {"autoResizeDimensions": {"dimensions": {"sheetId": 2, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1}}},
        # Porcentajes
        {
            "repeatCell": {
                "range": {"sheetId": 1, "startRowIndex": 8, "endRowIndex": 9, "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}},
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": 1, "startRowIndex": 14, "endRowIndex": 15, "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {"userEnteredFormat": {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}}},
                "fields": "userEnteredFormat.numberFormat",
            }
        },
    ]
    api.spreadsheets().batchUpdate(spreadsheetId=sid, body={"requests": pedidos}).execute()

    url = f"https://docs.google.com/spreadsheets/d/{sid}/edit"
    print(f"Planilla creada: {TITULO}")
    print(url)
    print("\nNo se compartió con nadie. Para que José la use hay que darle acceso a mano.")
    return url


if __name__ == "__main__":
    main()
