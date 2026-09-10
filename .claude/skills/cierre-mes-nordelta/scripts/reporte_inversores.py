#!/usr/bin/env python3
"""
Reporte mensual para los inversores del Paseo Nordelta.

Baja el Master Plan (la fuente: el Sheet, no el .xlsx viejo de data/), calcula el
resultado operativo mes a mes contra la hoja Movimientos, y arma el PDF + el
borrador de mail. NO MANDA NADA: deja el borrador en Gmail (regla 10).

    .venv/bin/python .../reporte_inversores.py 2026-08
    .venv/bin/python .../reporte_inversores.py 2026-08 --borrador   # crea el draft

Qué entra en el resultado operativo, y por qué (esto es lo que el reporte de
agosto tenia mal):

  ingreso operativo = Ingreso cuyo Local NO es "Aporte de Capital ..."
  egreso  operativo = Egreso cuya Categoria NO esta en NO_OPERATIVO

  - "Inversiones" es la OBRA: la pagan los socios con su capital, no la operacion.
  - "Retiro de Ganancia Richi" es reparto de utilidad, no un gasto del negocio.
  - "Ajuste de caja" es un descuadre sin detalle: es plata real que falto, pero no
    dice nada sobre si la operacion cierra. Se muestra en su propio renglon para
    que no quede escondida en ningun lado.
"""
import sys, os, subprocess, collections, datetime as dt
from pathlib import Path

sys.path.insert(0, "/Users/Facu/facu-os")

SHEET_MASTER_PLAN = "1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs"
# El capital NO sale del Master Plan: sale de Gastos Obra, que es lo que cada socio
# PUSO (aportes + obra que pago de su bolsillo). El Master Plan solo tiene lo que
# entro por la caja o el banco del Paseo, que es menos. Son dos cosas distintas,
# no dos versiones de la misma -> memoria [[donde-va-un-aporte-de-capital]].
SHEET_GASTOS_OBRA = "1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY"
# Facu, 10/09/2026: al inversor van estos tres. Mariana, Soledad y Tomas figuran
# en Gastos Obra solo en USD y no entran en este reporte.
SOCIOS_DEL_REPORTE = ["Richi", "Facundo", "Paseo Nordelta"]

# Aclaraciones que van en el PDF de un mes puntual, cuando un numero necesita
# contexto para no enganar. Sin esto el lector ve la ganancia y no la razon.
# Cuando un reporte ya enviado se corrige, el que lo recibio tiene que entender
# que cambio y por que. Un segundo mail con otros numeros y sin explicacion es
# peor que no mandarlo.
CORRECCIONES = {
    "2026-08": ("Va de nuevo el reporte de agosto, con una correcci\u00f3n sobre el que "
                "te mand\u00e9 hace un rato. Revisando los movimientos vimos que la obra "
                "de julio \u2014 $6.210.228 entre mano de obra y materiales \u2014 estaba "
                "cargada como gasto de operaci\u00f3n cuando en realidad es inversi\u00f3n en "
                "el paseo, que se financia con el capital de los socios y no con los "
                "alquileres. Corregido, julio cierra en +$14,8M en vez de +$8,6M y el "
                "acumulado del a\u00f1o pasa de +$24,1M a +$30,3M. Los n\u00fameros de agosto "
                "no cambian."),
}

NOTAS_DEL_MES = {
    "2026-08": ("Expensas AVN, que ven\u00eda entre $2,1M y $3,3M por mes, no se pag\u00f3 "
                "en julio ni en agosto: est\u00e1 retenida a prop\u00f3sito mientras se "
                "resuelve una deuda que AVN tiene con el Paseo. Son unos $5,6M que "
                "hoy siguen en la caja y que van a salir cuando se destrabe, as\u00ed "
                "que el resultado de esos dos meses no es comparable con el de los "
                "anteriores."),
}
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SALIDA = Path("/Users/Facu/facu-os/data/reportes-inversores")

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
ABREV = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

OBRA = {"Inversiones"}
REPARTO = {"Retiro de Ganancia Richi"}
DESCUADRE = {"Ajuste de caja"}
NO_OPERATIVO = OBRA | REPARTO | DESCUADRE


def plata(n, dec=0):
    """1234567.4 -> '1.234.567'  (formato AR)"""
    s = f"{n:,.{dec}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def millones(n):
    """5963500 -> '+$6,0M'"""
    signo = "-" if n < 0 else "+"
    return f"{signo}${abs(n)/1_000_000:.1f}".replace(".", ",") + "M"


def bajar_master_plan(destino):
    from execution.google_auth import bajar_xlsx
    bajar_xlsx(SHEET_MASTER_PLAN, str(destino))
    return destino


def capital_de_gastos_obra(cierre):
    """Lo que cada socio puso, cortado a la misma fecha que el resto del reporte.

    Columnas: A fecha, B persona, H monto en ARS, I monto en USD (la conversion al
    dolar del dia, no un aporte aparte). El acumulado que la planilla trae en L:N
    es "hasta hoy", por eso se suma fila por fila.
    """
    from execution.google_auth import sheets
    v = (sheets("facu").spreadsheets().values()
         .get(spreadsheetId=SHEET_GASTOS_OBRA, range="Hoja 1!A5:I1000")
         .execute().get("values", []))

    def num(x):
        x = str(x or "").replace("$", "").replace(",", "").strip()
        try:
            return float(x)
        except ValueError:
            return 0.0

    ars = collections.defaultdict(float)
    usd = collections.defaultdict(float)
    solo_aportes = collections.defaultdict(float)
    leidas = ilegibles = 0
    for r in v:
        r = list(r) + [""] * (9 - len(r))
        f = str(r[0]).strip()
        if not f:
            continue
        try:
            # hay fechas tipeadas "20/05./2026": el punto de mas no puede tirar
            # una fila de plata afuera del total en silencio
            d, m, a = [int(x.strip(" .")) for x in f.split("/")]
            fecha = dt.date(a, m, d)
        except Exception:
            ilegibles += 1
            print(f"     !! fecha ilegible en Gastos Obra: {f!r} ({r[1]}, {r[3]})")
            continue
        if fecha > cierre:
            continue
        persona = str(r[1]).strip()
        ars[persona] += num(r[7])
        usd[persona] += num(r[8])
        if "aporte de capital" in str(r[2]).strip().lower():
            solo_aportes[persona] += num(r[7])
        leidas += 1

    if leidas == 0:
        sys.exit("ERROR: Gastos Obra vino vacia. No reporto un capital de cero.")
    if ilegibles:
        sys.exit(f"ERROR: {ilegibles} fila(s) de Gastos Obra con fecha ilegible. "
                 f"Arreglalas en la planilla: si no, ese aporte no entra en el total.")
    return ({k: ars[k] for k in SOCIOS_DEL_REPORTE if ars.get(k)},
            {k: usd[k] for k in SOCIOS_DEL_REPORTE if usd.get(k)},
            dict(solo_aportes), leidas)


def capital_cuadra(cap_mp, aportes_go, tol=1000.0):
    """El capital sale al inversor SOLO si las dos fuentes dicen lo mismo.

    Master Plan tiene lo que entro por la caja o el banco del Paseo; Gastos Obra
    tiene lo que cada socio pago (aportes + obra de su bolsillo). Si los aportes
    de una no son los de la otra, hay un dato que vive en dos lados y uno miente:
    no se manda a un inversor hasta resolverlo.

    Al 31/08/2026 no cuadraban por $15.384.058, sobre todo por la fila del
    16/07/2026 de Gastos Obra: -$51.793.000 en Richi, "ingreso aporte de facu en
    acciones" — un traspaso entre socios que el Master Plan no registra.
    """
    alias = {"Richi": "Richi", "Facundo": "Facu"}
    difs = []
    for socio in SOCIOS_DEL_REPORTE:
        mp = cap_mp.get(alias.get(socio, socio), 0.0)
        go = aportes_go.get(socio, 0.0)
        if abs(mp - go) > tol:
            difs.append((socio, mp, go, mp - go))
    return difs


def leer(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    filas = []
    for r in wb["Movimientos"].iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        filas.append(dict(fecha=r[0], tipo=r[1], medio=r[2], local=r[3],
                          cat=r[4], monto=float(r[5] or 0), moneda=r[6],
                          obs=r[7], mes=r[8]))
    if not filas:
        sys.exit("ERROR: la hoja Movimientos vino vacia. No sigo.")
    return filas


def calcular(filas, anio, mes_corte):
    """Devuelve el resultado operativo por mes hasta mes_corte, mas capital y obra."""
    es_aporte = lambda l: bool(l) and str(l).startswith("Aporte de Capital")
    m = {i: dict(ing=0.0, egr=0.0, reparto=0.0, descuadre=0.0, obra=0.0, aporte=0.0)
         for i in range(1, mes_corte + 1)}
    porcat = collections.defaultdict(lambda: collections.defaultdict(float))

    capital = collections.defaultdict(float)      # ARS por socio, hasta el corte
    capital_usd = collections.defaultdict(float)
    obra_total = 0.0
    obra_usd = 0.0
    fuera_moneda = []

    cierre = dt.date(anio, mes_corte, 1)
    cierre = (dt.date(anio + (mes_corte == 12), mes_corte % 12 + 1, 1) - dt.timedelta(days=1))

    for f in filas:
        fecha = f["fecha"].date() if isinstance(f["fecha"], dt.datetime) else f["fecha"]
        if fecha > cierre:
            continue
        ars = f["moneda"] == "ARS"
        if not ars:
            fuera_moneda.append(f)

        if f["tipo"] == "Ingreso" and es_aporte(f["local"]):
            socio = str(f["local"]).replace("Aporte de Capital ", "")
            (capital if ars else capital_usd)[socio] += f["monto"]
        elif f["tipo"] == "Egreso" and f["cat"] in OBRA:
            if ars:
                obra_total += f["monto"]
            else:
                obra_usd += f["monto"]

        if not ars or fecha.year != anio:
            continue
        i = fecha.month
        if i not in m:
            continue
        if f["tipo"] == "Ingreso":
            if not es_aporte(f["local"]):
                m[i]["ing"] += f["monto"]
            else:
                m[i]["aporte"] += f["monto"]
        else:
            if f["cat"] in OBRA:
                m[i]["obra"] += f["monto"]
            elif f["cat"] in REPARTO:
                m[i]["reparto"] += f["monto"]
            elif f["cat"] in DESCUADRE:
                m[i]["descuadre"] += f["monto"]
            else:
                m[i]["egr"] += f["monto"]
            porcat[f["cat"]][i] += f["monto"]

    for i in m:
        m[i]["res"] = m[i]["ing"] - m[i]["egr"]

    saldos = collections.defaultdict(float)
    for f in filas:
        fecha = f["fecha"].date() if isinstance(f["fecha"], dt.datetime) else f["fecha"]
        if fecha > cierre:
            continue
        saldos[(f["medio"], f["moneda"])] += (1 if f["tipo"] == "Ingreso" else -1) * f["monto"]

    return dict(meses=m, capital=dict(capital), capital_usd=dict(capital_usd),
                obra=obra_total, obra_usd=obra_usd, saldos=dict(saldos),
                cierre=cierre, fuera_moneda=fuera_moneda,
                porcat={k: dict(v) for k, v in porcat.items()})


def gastos_que_desaparecieron(porcat, mes_corte, minimo=3, piso=500_000):
    """Categorias que se pagaban con regularidad y ahora estan en cero.

    Es el agujero mas caro de este reporte: un gasto fijo que falta cargar no da
    error, sube el resultado y hace que el mes parezca mejor de lo que fue.
    Expensas AVN corrio $2,1M-$3,3M de enero a junio 2026 y aparecio en $0 en
    julio Y agosto: $5,6M de gasto que el reporte no mostraba.

    Por eso NO se piden meses seguidos hasta el corte (cuando el gasto lleva dos
    meses faltando, el mes anterior ya esta en cero y esa cuenta da 0): se pide
    que se haya pagado en al menos `minimo` de los meses previos.
    """
    avisos = []
    for cat, meses in porcat.items():
        if cat in NO_OPERATIVO or meses.get(mes_corte, 0.0) > 0:
            continue
        pagados = [meses[i] for i in range(1, mes_corte) if meses.get(i, 0.0) > 0]
        if len(pagados) < minimo:
            continue
        # hace cuantos meses que no se paga
        seco = 0
        for i in range(mes_corte, 0, -1):
            if meses.get(i, 0.0) > 0:
                break
            seco += 1
        prom = sum(pagados) / len(pagados)
        if prom < piso:      # ruido: gastos chicos que se pagan cuando caen
            continue
        avisos.append((cat, len(pagados), mes_corte - 1, prom, seco))
    return sorted(avisos, key=lambda x: -x[3])


def rachas(m, mes_corte):
    n = 0
    for i in range(mes_corte, 0, -1):
        if m[i]["res"] > 0:
            n += 1
        else:
            break
    return n


# ---------------------------------------------------------------- el documento

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
       color: #111; margin: 0; font-size: 11px; background: #fff; }
.cuerpo { padding: 0 12mm 14mm; }
.tapa { background: #000; color: #fff; padding: 20px 12mm 17px; margin-bottom: 16px; }
.tapa .logo { font-size: 17px; letter-spacing: .22em; font-weight: 600; }
.tapa .sub { font-size: 9px; letter-spacing: .18em; color: #999; margin-top: 5px; }
.hero { text-align: center; margin: 18px 0 20px; }
.hero .lbl { font-size: 9px; letter-spacing: .2em; color: #777; }
.hero .big { font-size: 44px; font-weight: 700; margin: 6px 0 4px; letter-spacing: -.02em; }
.hero .det { font-size: 11px; color: #555; }
.pos { color: #1a7f37; } .neg { color: #b42318; }
h2 { font-size: 12px; letter-spacing: .1em; margin: 17px 0 7px;
     border-bottom: 1.5px solid #111; padding-bottom: 5px; }
table { width: 100%; border-collapse: collapse; }
.barras td { padding: 2.5px 0; vertical-align: middle; }
.barras .mes { width: 42px; color: #444; }
.barras .val { width: 74px; font-weight: 600; text-align: right; padding-right: 12px; }
.bar { height: 13px; border-radius: 2px; }
.bar.p { background: #a9d5b4; } .bar.n { background: #eab6b0; }
.bar.hoy { background: #1a7f37; }
.nota { font-size: 10px; color: #555; margin-top: 7px; }
.caja { background: #f2f8f4; border-left: 3px solid #1a7f37; padding: 8px 12px;
        margin: 9px 0; font-size: 10.5px; line-height: 1.4; }
.caja b { color: #1a7f37; }
.caja.gris { background: #f6f6f6; border-left-color: #999; }
.caja.gris b { color: #333; }
.tiles { display: flex; gap: 10px; margin-top: 10px; }
.tile { flex: 1; background: #f6f6f6; border-radius: 4px; padding: 9px 12px; }
.tile .k { font-size: 8px; letter-spacing: .14em; color: #777; }
.tile .v { font-size: 17px; font-weight: 700; margin-top: 4px; }
.lineas td { padding: 3.5px 0; border-bottom: 1px solid #eee; }
.lineas td.n { text-align: right; font-variant-numeric: tabular-nums; }
.lineas tr.tot td { font-weight: 700; border-bottom: 2px solid #111; }
.pie { margin-top: 16px; padding-top: 9px; border-top: 1px solid #ddd;
       font-size: 8px; letter-spacing: .1em; color: #888; text-align: center; }
"""


def html(d, anio, mes_corte, cap_ars, cap_usd, nota_mes=None):
    m, mm = d["meses"], d["meses"][mes_corte]
    acum = sum(m[i]["res"] for i in m)
    tope = max(abs(m[i]["res"]) for i in m) or 1
    racha = rachas(m, mes_corte)
    nombre_mes = MESES[mes_corte - 1].upper()

    filas = []
    for i in range(1, mes_corte + 1):
        r = m[i]["res"]
        ancho = abs(r) / tope * 100
        cls = "hoy" if i == mes_corte else ("p" if r > 0 else "n")
        filas.append(
            f'<tr><td class="mes">{ABREV[i-1]}</td>'
            f'<td class="val {"pos" if r>0 else "neg"}">{millones(r)}</td>'
            f'<td><div class="bar {cls}" style="width:{ancho:.1f}%"></div></td></tr>')

    cap_tot = sum(cap_ars.values())
    usd_tot = sum(cap_usd.values())
    lineas_cap = "".join(
        f'<tr><td>{s}</td><td class="n">${plata(v)}</td>'
        f'<td class="n" style="color:#777">US$ {plata(cap_usd.get(s, 0))}</td></tr>'
        for s, v in sorted(cap_ars.items(), key=lambda x: -x[1]))

    caja = d["saldos"].get(("Caja", "ARS"), 0)
    banco = d["saldos"].get(("Banco", "ARS"), 0)
    usd = d["saldos"].get(("Caja", "USD"), 0) + d["saldos"].get(("Banco", "USD"), 0)

    no_op = sum(m[i]["reparto"] + m[i]["descuadre"] for i in m)
    bloque_no_op = ""
    if no_op:
        det = []
        for i in m:
            if m[i]["reparto"]:
                det.append(f'{ABREV[i-1]}: reparto de ganancia ${plata(m[i]["reparto"])}')
            if m[i]["descuadre"]:
                det.append(f'{ABREV[i-1]}: descuadre de caja ${plata(m[i]["descuadre"])}')
        bloque_no_op = (
            f'<div class="caja gris"><b>Fuera del resultado operativo: '
            f'${plata(no_op)}</b><br>{" &middot; ".join(det)}.<br>'
            f'Son movimientos que no son gasto del negocio (un reparto de utilidad '
            f'y diferencias de caja sin detalle), y por eso se muestran aparte.</div>')

    veredicto = (
        f'<div class="caja"><b>El negocio operativo se sostiene solo.</b><br>'
        f'Los alquileres y expensas de los locales cubren los gastos de operación, '
        f'y en {MESES[mes_corte-1]} dejaron {millones(mm["res"])} en el mes.</div>'
        if mm["res"] > 0 and acum > 0 else
        f'<div class="caja gris"><b>Atención: {MESES[mes_corte-1]} cerró en '
        f'{millones(mm["res"])}.</b><br>Los ingresos de los locales no alcanzaron '
        f'a cubrir los gastos de operación del mes.</div>')

    bloque_capital = "" if not cap_ars else f"""
<h2>LO QUE PUSIERON LOS SOCIOS &middot; AL CIERRE DE {nombre_mes}</h2>
<table class="lineas">
  {lineas_cap}
  <tr class="tot"><td>Total puesto por los socios</td><td class="n">${plata(cap_tot)}</td>
    <td class="n" style="color:#777">US$ {plata(usd_tot)}</td></tr>
</table>
<div class="nota">Incluye los aportes de capital <b>y</b> la obra que cada uno pag\u00f3
  de su bolsillo. Sale de la planilla <b>Gastos Obra</b>, cortado al
  {d['cierre'].strftime('%d/%m/%Y')}.</div>"""

    return f"""<meta charset="utf-8"><style>{CSS}</style>
<div class="tapa">
  <div class="logo">PASEO NORDELTA</div>
  <div class="sub">REPORTE PARA INVERSORES &nbsp;&middot;&nbsp; {nombre_mes} {anio}</div>
</div>
<div class="cuerpo">

<div class="hero">
  <div class="lbl">RESULTADO DEL NEGOCIO &middot; {nombre_mes}</div>
  <div class="big {'pos' if mm['res']>0 else 'neg'}">{millones(mm['res'])}</div>
  <div class="det">${plata(mm['res'])} exactos &nbsp;&middot;&nbsp;
       ingresos ${plata(mm['ing'])} &nbsp;&minus;&nbsp;
       gastos operativos ${plata(mm['egr'])}</div>
</div>

<h2>EL NEGOCIO, MES A MES</h2>
<table class="barras">{''.join(filas)}</table>
<div class="nota"><b class="{'pos' if acum>0 else 'neg'}">{millones(acum)}</b>
  (${plata(acum)}) acumulado en el año (enero&ndash;{MESES[mes_corte-1]})
  {f'&middot; {racha}º mes seguido en positivo' if racha > 1 else ''}</div>

{veredicto}
{bloque_no_op}
{f'<div class="caja gris">{nota_mes}</div>' if nota_mes else ''}

<h2>SALDOS AL CIERRE &middot; {nombre_mes} {anio}</h2>
<div class="tiles">
  <div class="tile"><div class="k">EFECTIVO (CAJA)</div><div class="v">${plata(caja)}</div></div>
  <div class="tile"><div class="k">DÓLARES</div><div class="v">US$ {plata(usd)}</div></div>
  <div class="tile"><div class="k">BANCO</div><div class="v">${plata(banco)}</div></div>
</div>
<div class="nota">Total disponible ${plata(caja+banco)} en pesos, al {d['cierre'].strftime('%d/%m/%Y')}.</div>

{bloque_capital}
<div class="pie">
PASEO NORDELTA &nbsp;&middot;&nbsp; CIERRE {nombre_mes} {anio}
  &nbsp;&middot;&nbsp; {"FUENTES: MASTER PLAN (MOVIMIENTOS) Y GASTOS OBRA" if cap_ars else "FUENTE: MASTER PLAN, HOJA MOVIMIENTOS"}
  &nbsp;&middot;&nbsp; CIFRAS EN PESOS (ARS) SALVO ACLARACIÓN</div>
</div>
"""


# ------------------------------------------------------------------ el mail

DESTINATARIOS = ["re1900@gmail.com", "facue1900@gmail.com"]


def cuerpo_mail(d, anio, mes_corte, cap_ars, cap_usd, nota_mes=None, correccion=None):
    m, mm = d["meses"], d["meses"][mes_corte]
    acum = sum(m[i]["res"] for i in m)
    racha = rachas(m, mes_corte)
    nm = MESES[mes_corte - 1]
    cap = sum(cap_ars.values())
    parr_cap = ("" if not cap_ars else
                f"\nLa obra se financia aparte, con lo que pusieron los socios "
                f"\u2014 aportes de capital m\u00e1s la obra que cada uno pag\u00f3 de su "
                f"bolsillo \u2014, que al cierre de {nm} suma ${plata(cap)} "
                f"(US$ {plata(sum(cap_usd.values()))}).\n")

    signo = "un resultado positivo de" if mm["res"] > 0 else "un resultado negativo de"
    seguido = (f" Es el {racha}\u00ba mes consecutivo en positivo y deja"
               if racha > 1 else " Deja")
    cierra = ("as\u00ed que los alquileres ya cubren la operaci\u00f3n del paseo"
              if acum > 0 else
              "as\u00ed que la operaci\u00f3n todav\u00eda no se cubre sola en el a\u00f1o")

    apertura = correccion if correccion else f"Va el reporte de {nm} {anio} del Paseo."

    return f"""Hola,

{apertura}

En {nm} el negocio cerr\u00f3 con {signo} {millones(mm['res'])}: los locales facturaron \
${plata(mm['ing'])} y los gastos operativos fueron ${plata(mm['egr'])}.{seguido} \
el acumulado del a\u00f1o en {millones(acum)}, {cierra}.

{parr_cap}{(nota_mes + chr(10)) if nota_mes else ''}

El detalle completo est\u00e1 en el PDF adjunto. Los n\u00fameros salen del Master Plan \
(hoja Movimientos), cortados al {d['cierre'].strftime('%d/%m/%Y')}.

Quedo a disposici\u00f3n. Saludos,

Facundo
"""


def crear_borrador(asunto, cuerpo, pdf, para):
    """Deja el mail EN BORRADORES. Nunca manda (regla 10)."""
    import base64
    from email.message import EmailMessage
    from execution.google_auth import gmail

    msg = EmailMessage()
    msg["To"] = ", ".join(para)
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    with open(pdf, "rb") as fh:
        msg.add_attachment(fh.read(), maintype="application", subtype="pdf",
                           filename=Path(pdf).name)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    svc = gmail(cuenta="facu")
    dr = svc.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    return dr["id"]


# ------------------------------------------------------------------ main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        anio, mes_corte = int(args[0][:4]), int(args[0][5:7])
    else:
        # sin argumento: el mes anterior al de hoy (asi lo llama launchd)
        hoy = dt.date.today()
        primero = hoy.replace(day=1)
        anterior = primero - dt.timedelta(days=1)
        anio, mes_corte = anterior.year, anterior.month
        print(f"Sin mes indicado: reporto {MESES[mes_corte-1]} {anio}")
    hacer_borrador = "--borrador" in sys.argv

    SALIDA.mkdir(parents=True, exist_ok=True)
    xlsx = SALIDA / "_master_plan.xlsx"
    print(f"Bajando el Master Plan (Sheet {SHEET_MASTER_PLAN[:12]}...)")
    bajar_master_plan(xlsx)

    filas = leer(xlsx)
    print(f"  {len(filas)} movimientos leidos")
    d = calcular(filas, anio, mes_corte)

    m = d["meses"]
    if not any(m[i]["ing"] for i in m):
        sys.exit("ERROR: ningun ingreso en el ano. Reviso la hoja antes de reportar.")
    if not m[mes_corte]["ing"]:
        sys.exit(f"ERROR: {MESES[mes_corte-1]} no tiene ingresos cargados. No reporto un mes vacio.")

    print(f"\n{'MES':<6}{'INGRESOS':>16}{'GASTOS OP.':>16}{'RESULTADO':>16}")
    for i in range(1, mes_corte + 1):
        print(f"{ABREV[i-1]:<6}{m[i]['ing']:>16,.0f}{m[i]['egr']:>16,.0f}{m[i]['res']:>16,.0f}")
    print(f"{'ACUM':<6}{'':>16}{'':>16}{sum(m[i]['res'] for i in m):>16,.0f}")

    # El extracto del Macro entra tarde (llega alrededor del 15). Si el banco no
    # tiene movimientos en la ultima semana del mes, el saldo bancario esta viejo
    # y el reporte lo diria como si fuera el cierre. Aviso fuerte, no lo escondo.
    ult_banco = max((f["fecha"].date() if isinstance(f["fecha"], dt.datetime) else f["fecha"])
                    for f in filas if f["medio"] == "Banco"
                    and (f["fecha"].date() if isinstance(f["fecha"], dt.datetime)
                         else f["fecha"]) <= d["cierre"])
    if (d["cierre"] - ult_banco).days > 3:
        print(f"\n  !! OJO: el ultimo movimiento de BANCO es del {ult_banco:%d/%m/%Y}, "
              f"{(d['cierre']-ult_banco).days} dias antes del cierre ({d['cierre']:%d/%m/%Y}).")
        print("     El extracto del Macro puede no estar cargado entero: el saldo de banco")
        print("     y los gastos pagados por banco pueden estar incompletos. Verificalo")
        print("     antes de mandar el reporte.")

    faltantes = gastos_que_desaparecieron(d["porcat"], mes_corte)
    if faltantes:
        print(f"\n  !! GASTOS QUE SE PAGABAN SEGUIDO Y ESTE MES ESTAN EN CERO:")
        for cat, n, de, prom, seco in faltantes:
            print(f"     - {cat}: se pago en {n} de los {de} meses previos "
                  f"(promedio ${plata(prom)}/mes) y lleva {seco} mes/es en $0.")
        print("     Si falta cargarlos, el resultado del mes esta INFLADO por esa plata.")
        print("     Confirmalo antes de mandar el reporte.")

    print("\n  Capital: leyendo Gastos Obra...")
    cap_ars, cap_usd, aportes_go, nfilas = capital_de_gastos_obra(d["cierre"])
    print(f"     {nfilas} filas hasta el corte | " +
          " | ".join(f"{k} ${plata(v)}" for k, v in cap_ars.items()))
    difs = capital_cuadra(d["capital"], aportes_go)
    if difs:
        print("\n  !! EL CAPITAL NO CUADRA entre Master Plan y Gastos Obra:")
        for socio, mp, go, dif in difs:
            print(f"     - {socio}: Master Plan ${plata(mp)} vs Gastos Obra "
                  f"${plata(go)}  ({dif:+,.0f})".replace(",", "."))
        print("     El bloque de capital NO va en el reporte: un dato que vive en dos")
        print("     lados y no coincide no sale a un inversor. El resultado del mes y")
        print("     los saldos si van: esos salen de una sola fuente y estan verificados.")
        cap_ars, cap_usd = {}, {}

    nota_mes = NOTAS_DEL_MES.get(f"{anio}-{mes_corte:02d}")

    base = f"Paseo_Nordelta_Inversores_{anio}-{mes_corte:02d}"
    fh = SALIDA / f"{base}.html"
    fp = SALIDA / f"{base}.pdf"
    fh.write_text(html(d, anio, mes_corte, cap_ars, cap_usd, nota_mes), encoding="utf-8")

    if not os.path.exists(CHROME):
        sys.exit(f"No encontre Chrome en {CHROME}: queda el HTML en {fh}")
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={fp}", str(fh)],
                       capture_output=True, text=True, timeout=90)
    if not fp.exists() or fp.stat().st_size < 5000:
        sys.exit(f"Chrome no genero un PDF valido:\n{r.stderr[-500:]}")
    print(f"\nPDF: {fp}  ({fp.stat().st_size/1024:.0f} KB)")

    correccion = CORRECCIONES.get(f"{anio}-{mes_corte:02d}")
    asunto = (f"Paseo Nordelta \u2014 Reporte para inversores \u00b7 "
              f"{MESES[mes_corte-1].capitalize()} {anio}"
              + (" (corregido)" if correccion else ""))
    cuerpo = cuerpo_mail(d, anio, mes_corte, cap_ars, cap_usd, nota_mes, correccion)
    (SALIDA / f"{base}_mail.txt").write_text(
        f"Para: {', '.join(DESTINATARIOS)}\nAsunto: {asunto}\n\n{cuerpo}", encoding="utf-8")

    if hacer_borrador:
        did = crear_borrador(asunto, cuerpo, fp, DESTINATARIOS)
        print(f"Borrador creado en Gmail (id {did}). NO se mando: abrilo, revisalo y envialo vos.")
    else:
        print(f"Mail preparado en {SALIDA / (base + '_mail.txt')}")
        print("Corre de nuevo con --borrador para dejarlo en Gmail.")


if __name__ == "__main__":
    main()
