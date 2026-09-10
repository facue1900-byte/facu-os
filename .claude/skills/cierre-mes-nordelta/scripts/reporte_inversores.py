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
                cierre=cierre, fuera_moneda=fuera_moneda)


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
.tapa { background: #000; color: #fff; padding: 26px 12mm 22px; margin-bottom: 24px; }
.tapa .logo { font-size: 17px; letter-spacing: .22em; font-weight: 600; }
.tapa .sub { font-size: 9px; letter-spacing: .18em; color: #999; margin-top: 5px; }
.hero { text-align: center; margin: 26px 0 30px; }
.hero .lbl { font-size: 9px; letter-spacing: .2em; color: #777; }
.hero .big { font-size: 52px; font-weight: 700; margin: 6px 0 4px; letter-spacing: -.02em; }
.hero .det { font-size: 11px; color: #555; }
.pos { color: #1a7f37; } .neg { color: #b42318; }
h2 { font-size: 12px; letter-spacing: .1em; margin: 26px 0 8px;
     border-bottom: 1.5px solid #111; padding-bottom: 5px; }
table { width: 100%; border-collapse: collapse; }
.barras td { padding: 4px 0; vertical-align: middle; }
.barras .mes { width: 42px; color: #444; }
.barras .val { width: 74px; font-weight: 600; text-align: right; padding-right: 12px; }
.bar { height: 13px; border-radius: 2px; }
.bar.p { background: #a9d5b4; } .bar.n { background: #eab6b0; }
.bar.hoy { background: #1a7f37; }
.nota { font-size: 10px; color: #555; margin-top: 7px; }
.caja { background: #f2f8f4; border-left: 3px solid #1a7f37; padding: 11px 14px;
        margin: 14px 0; font-size: 11px; }
.caja b { color: #1a7f37; }
.caja.gris { background: #f6f6f6; border-left-color: #999; }
.caja.gris b { color: #333; }
.tiles { display: flex; gap: 10px; margin-top: 10px; }
.tile { flex: 1; background: #f6f6f6; border-radius: 4px; padding: 12px 14px; }
.tile .k { font-size: 8px; letter-spacing: .14em; color: #777; }
.tile .v { font-size: 19px; font-weight: 700; margin-top: 4px; }
.lineas td { padding: 5px 0; border-bottom: 1px solid #eee; }
.lineas td.n { text-align: right; font-variant-numeric: tabular-nums; }
.lineas tr.tot td { font-weight: 700; border-bottom: 2px solid #111; }
.pie { margin-top: 26px; padding-top: 9px; border-top: 1px solid #ddd;
       font-size: 8px; letter-spacing: .1em; color: #888; text-align: center; }
"""


def html(d, anio, mes_corte):
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

    cap = d["capital"]
    cap_tot = sum(cap.values())
    cap_usd = sum(d["capital_usd"].values())
    lineas_cap = "".join(
        f'<tr><td>Aporte de {s}</td><td class="n">${plata(v)}</td></tr>'
        for s, v in sorted(cap.items(), key=lambda x: -x[1]))
    if cap_usd:
        lineas_cap += (f'<tr><td>Aportes en dólares (Richi, ene-26)</td>'
                       f'<td class="n">US$ {plata(cap_usd)}</td></tr>')

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

    return f"""<meta charset="utf-8"><style>{CSS}</style>
<div class="tapa">
  <div class="logo">PASEO NORDELTA</div>
  <div class="sub">REPORTE PARA INVERSORES &nbsp;&middot;&nbsp; {nombre_mes} {anio}</div>
</div>
<div class="cuerpo">

<div class="hero">
  <div class="lbl">RESULTADO DEL NEGOCIO &middot; {nombre_mes}</div>
  <div class="big {'pos' if mm['res']>0 else 'neg'}">{millones(mm['res'])}</div>
  <div class="det">Ingresos ${plata(mm['ing'])} &nbsp;&minus;&nbsp;
       gastos operativos ${plata(mm['egr'])}</div>
</div>

<h2>EL NEGOCIO, MES A MES</h2>
<table class="barras">{''.join(filas)}</table>
<div class="nota"><b class="{'pos' if acum>0 else 'neg'}">{millones(acum)}</b>
  acumulado en el año (enero&ndash;{MESES[mes_corte-1]})
  {f'&middot; {racha}º mes seguido en positivo' if racha > 1 else ''}</div>

{veredicto}
{bloque_no_op}

<h2>SALDOS AL CIERRE &middot; {nombre_mes} {anio}</h2>
<div class="tiles">
  <div class="tile"><div class="k">EFECTIVO (CAJA)</div><div class="v">${plata(caja)}</div></div>
  <div class="tile"><div class="k">DÓLARES</div><div class="v">US$ {plata(usd)}</div></div>
  <div class="tile"><div class="k">BANCO</div><div class="v">${plata(banco)}</div></div>
</div>
<div class="nota">Total disponible ${plata(caja+banco)} en pesos, al {d['cierre'].strftime('%d/%m/%Y')}.</div>

<h2>CAPITAL Y OBRA &middot; AL CIERRE DE {nombre_mes}</h2>
<table class="lineas">
  {lineas_cap}
  <tr class="tot"><td>Capital aportado (total)</td><td class="n">${plata(cap_tot)}
    {f'+ US$ {plata(cap_usd)}' if cap_usd else ''}</td></tr>
  <tr><td>Invertido en obra y equipamiento</td><td class="n neg">${plata(d['obra'])}
    {f'+ US$ {plata(d["obra_usd"])}' if d['obra_usd'] else ''}</td></tr>
</table>
<div class="nota">La obra se financia con el capital aportado por los socios, aparte
  del resultado del negocio. Las dos cifras están cortadas al {d['cierre'].strftime('%d/%m/%Y')}.</div>

<div class="pie">PASEO NORDELTA &nbsp;&middot;&nbsp; CIERRE {nombre_mes} {anio}
  &nbsp;&middot;&nbsp; FUENTE: MASTER PLAN, HOJA MOVIMIENTOS
  &nbsp;&middot;&nbsp; CIFRAS EN PESOS (ARS) SALVO ACLARACIÓN</div>
</div>
"""


# ------------------------------------------------------------------ el mail

DESTINATARIOS = ["re1900@gmail.com", "facue1900@gmail.com"]


def cuerpo_mail(d, anio, mes_corte):
    m, mm = d["meses"], d["meses"][mes_corte]
    acum = sum(m[i]["res"] for i in m)
    racha = rachas(m, mes_corte)
    nm = MESES[mes_corte - 1]
    cap = sum(d["capital"].values())
    cap_usd = sum(d["capital_usd"].values())
    usd_txt = f" m\u00e1s US$ {plata(cap_usd)}" if cap_usd else ""

    signo = "un resultado positivo de" if mm["res"] > 0 else "un resultado negativo de"
    seguido = (f" Es el {racha}\u00ba mes consecutivo en positivo y deja"
               if racha > 1 else " Deja")
    cierra = ("as\u00ed que los alquileres ya cubren la operaci\u00f3n del paseo"
              if acum > 0 else
              "as\u00ed que la operaci\u00f3n todav\u00eda no se cubre sola en el a\u00f1o")

    return f"""Hola,

Va el reporte de {nm} {anio} del Paseo.

En {nm} el negocio cerr\u00f3 con {signo} {millones(mm['res'])}: los locales facturaron \
${plata(mm['ing'])} y los gastos operativos fueron ${plata(mm['egr'])}.{seguido} \
el acumulado del a\u00f1o en {millones(acum)}, {cierra}.

La obra se financia aparte, con el capital aportado por los socios, que al cierre \
de {nm} suma ${plata(cap)}{usd_txt}.

El detalle completo est\u00e1 en el PDF adjunto. Todos los n\u00fameros salen del Master \
Plan (hoja Movimientos), cortados al {d['cierre'].strftime('%d/%m/%Y')}.

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
    if (d["cierre"] - ult_banco).days > 7:
        print(f"\n  !! OJO: el ultimo movimiento de BANCO es del {ult_banco:%d/%m/%Y}, "
              f"{(d['cierre']-ult_banco).days} dias antes del cierre ({d['cierre']:%d/%m/%Y}).")
        print("     El extracto del Macro puede no estar cargado entero: el saldo de banco")
        print("     y los gastos pagados por banco pueden estar incompletos. Verificalo")
        print("     antes de mandar el reporte.")

    base = f"Paseo_Nordelta_Inversores_{anio}-{mes_corte:02d}"
    fh = SALIDA / f"{base}.html"
    fp = SALIDA / f"{base}.pdf"
    fh.write_text(html(d, anio, mes_corte), encoding="utf-8")

    if not os.path.exists(CHROME):
        sys.exit(f"No encontre Chrome en {CHROME}: queda el HTML en {fh}")
    r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={fp}", str(fh)],
                       capture_output=True, text=True, timeout=90)
    if not fp.exists() or fp.stat().st_size < 5000:
        sys.exit(f"Chrome no genero un PDF valido:\n{r.stderr[-500:]}")
    print(f"\nPDF: {fp}  ({fp.stat().st_size/1024:.0f} KB)")

    asunto = f"Paseo Nordelta \u2014 Reporte para inversores \u00b7 {MESES[mes_corte-1].capitalize()} {anio}"
    cuerpo = cuerpo_mail(d, anio, mes_corte)
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
