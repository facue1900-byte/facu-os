#!/usr/bin/env python3
"""
Radar de rampa — Paseo Nordelta

Cruza los compromisos de alta de alquiler contra lo que realmente entró en
Movimientos, y avisa qué está atrasado.

Uso:
    python3 radar_rampa.py master.xlsx [AAAA-MM]

El xlsx se baja del Master Plan exportando a .xlsx (el conector de Drive
`read_file_content` TRUNCA las hojas largas — Movimientos entra cortada en
~206 de 455 filas. Siempre usar el export xlsx completo).
"""

import sys
import datetime
import collections

import openpyxl

# Precios de oferta del 03/11/2026 (ppt «Presentacion locatarios»), pasados a USD con el
# blue promedio de ese día (compra 1.545 / venta 1.565, api.argentinadatos.com). En el
# radar se vuelven a pesos con el blue vigente del Master Plan (Proyeccion!B4).
BLUE_OFERTA = 1_555


class Usd(float):
    """Monto en USD: el radar lo convierte a ARS con el blue del Master Plan."""


def usd_de(ars):
    return Usd(ars / BLUE_OFERTA)


# Compromisos de alta de ALQUILER: local -> (mes de arranque, alquiler mensual ARS)
# "Local" es el nombre canónico tal como lo escribe el Formulario en Movimientos.
# Fechas confirmadas por Facu el 27/07/2026.
RAMPA = [
    ("La Jaula",            "2026-08",  2_000_000),
    # Cafetería: el alquiler arranca en mar-27, no en nov-26 (Facu, 26/10/2026).
    ("Cafeteria",           "2027-03",  3_500_000),
    # Peak One: la obra arrancó recién en oct-26; alquiler desde mar-27 (Facu, 16/10/2026).
    # Los $4M son el valor BASE: en marzo se cobra ajustado por IPC trimestral.
    ("Peak One",            "2027-03",  4_000_000),
    # $2M es el número que dio Facu el 27/07 para el local nuevo de 47,9 m²
    # (la pestaña Alquileres dice $1,9M, pero para un local de 83,6 m² que no es este).
    # Cerrada con Morton Pizza (Facu 16/11/2026). Monto = oferta del 03/11 ($2,5M) en USD:
    # Facu quiere los precios nuevos en dólares para que no se licúen. Falta el número
    # firmado con Morton y si la fecha de alta sigue siendo ene-27.
    ("Pizzeria",            "2027-01",  usd_de(2_500_000)),
    # El local nuevo de 88,3 m² ($4M) se llena en enero en los dos escenarios —
    # con Fabric si entra la parrilla, con otro inquilino si no. NO va acá porque
    # el radar sigue compromisos, y en el escenario sin parrilla todavía no hay
    # nadie firmado para ese local.
    # Esquema de Marina (22/09, confirmado 02/11/2026): $1M nov-dic 26, ene-feb 27 sólo
    # expensas, $1,5M mar-jun 27, $2M jul 27, llega a $3M en dic 27. El detalle mes a mes
    # vive en `alquiler_por_mes` de cargos_del_mes.py; acá va sólo el primer escalón.
    ("Salon Multiespacios", "2026-11",  1_000_000),
    # Heladería nueva (123,7 m²): $5M + ~$1M de expensas. Hoy la heladería vieja
    # paga ~$1,9M todo concepto porque se demuele, así que el neto es menor.
    ("Heladeria",           "2027-01",  5_000_000),
    ("Market",              "2027-07",  usd_de(4_000_000)),
    # La tira: 8 locales a $2M de la oferta del 03/11 (antes eran 6). Sin fecha firme:
    # fecha del Market + 6 meses como placeholder explícito.
] + [(f"Comercio {i}", "2028-01", usd_de(2_000_000)) for i in range(1, 9)]

# Locales que hoy pagan solo expensas: el cobro existe pero NO es alquiler.
# Monto de expensas segun la pestaña Alquileres, para poder descontarlo.
SOLO_EXPENSAS = {
    "Peak One": 1_710_269,           # hasta febrero 2027 inclusive (alta corrida a mar-27)
    "Salon Multiespacios": 1_000_000,  # expensas pactadas; hasta octubre 2026 sin alquiler
    "Cafeteria": 979_912,            # septiembre y octubre 2026
}

# Puente plano <-> negocio. Los tres locales nuevos son los de "propuesta 16-07.pdf";
# el plano municipal los numera por arquitectura y el sheet por inquilino.
# OJO: la pestaña Alquileres tiene la pizzería y el Fabric nuevo CRUZADOS
# respecto de este plan (ver CLAUDE.md).
LOCALES_NUEVOS = {
    "Pizzeria":     47.9,    # el que Facu llama "el de 45"
    "Fabric nuevo": 88.3,    # el que Facu llama "el de 80"
    "Heladeria nueva": 123.7,
}


def mes_de(v):
    """Normaliza la columna A (fecha) a 'AAAA-MM'."""
    if isinstance(v, datetime.datetime):
        return f"{v.year}-{v.month:02d}"
    s = str(v).strip().split()[0]
    for sep in ("/", "-"):
        if sep in s:
            p = [x for x in s.split(sep) if x]
            if len(p) == 3:
                try:
                    return f"{int(p[2])}-{int(p[1]):02d}"
                except ValueError:
                    pass
    return "?"


def cobros_por_local(path):
    """Suma ingresos ARS por local y por mes. Excluye aportes de capital."""
    ws = openpyxl.load_workbook(path, data_only=True)["Movimientos"]
    out = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None or str(r[1]).strip().lower() != "ingreso":
            continue
        if str(r[6]).strip() != "ARS":
            continue
        loc = str(r[3] or "").strip()
        if not loc or loc.lower().startswith(("aporte", "cambio")):
            continue
        out[loc][mes_de(r[0])] += float(r[5] or 0)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    hoy = sys.argv[2] if len(sys.argv) > 2 else None
    if not hoy:
        sys.exit("Pasá el mes de corte como AAAA-MM (no adivino la fecha).")

    cobros = cobros_por_local(path)
    blue = openpyxl.load_workbook(path, data_only=True)["Proyeccion"]["B4"].value
    if not isinstance(blue, (int, float)) or blue <= 0:
        sys.exit(f"Proyeccion!B4 no trae un dólar válido ({blue!r}): no convierto los USD a ojo.")
    rampa = [(l, d, m * blue if isinstance(m, Usd) else m, isinstance(m, Usd)) for l, d, m in RAMPA]
    en_usd = {l for l, _, _, u in rampa if u}
    print(f"Dólar para los montos en USD: blue ${blue:,.0f} (Proyeccion!B4 del Master Plan).")

    vencidos, proximos, ok = [], [], []
    for local, desde, monto, _ in rampa:
        if desde > hoy:
            proximos.append((local, desde, monto))
            continue
        # Ya deberia estar pagando. ¿Entró plata este mes por encima de expensas?
        # El local sigue pagando expensas ADEMAS del alquiler, así que se descuentan
        # siempre. (Antes esto era `if desde > hoy else 0`, que en esta rama daba
        # 0 fijo: un local con expensas altas parecía al día cobrando solo expensas.)
        entro = cobros.get(local, {}).get(hoy, 0.0)
        piso = SOLO_EXPENSAS.get(local, 0)
        if entro - piso >= monto * 0.5:      # tolerancia: medio alquiler
            ok.append((local, desde, monto, entro))
        else:
            meses = mes_diff(desde, hoy) + 1
            vencidos.append((local, desde, monto, entro, meses))

    plata = sum(v[2] * v[4] for v in vencidos)

    print(f"RADAR DE RAMPA — corte {hoy}\n")
    if vencidos:
        print("ATRASADOS")
        for local, desde, monto, entro, meses in vencidos:
            print(f"  {local:<14} desde {desde}  "
                  f"esperado ${monto:>11,.0f}/mes  entró ${entro:>11,.0f}  "
                  f"({meses} {'mes' if meses == 1 else 'meses'})")
        print(f"\n  Acumulado no cobrado: ${plata:,.0f}\n")
    else:
        print("Sin atrasos.\n")

    if ok:
        print("AL DIA")
        for local, desde, monto, entro in ok:
            print(f"  {local:<14} desde {desde}  entró ${entro:,.0f}")
        print()

    print("PROXIMAS ALTAS")
    acum = 0
    for local, desde, monto in sorted(proximos, key=lambda x: x[1]):
        acum += monto
        marca = " (USD)" if local in en_usd else ""
        print(f"  {desde}  {local:<14} +${monto:>11,.0f}{marca}   run-rate ${acum:,.0f}")


def mes_diff(a, b):
    ay, am = (int(x) for x in a.split("-"))
    by, bm = (int(x) for x in b.split("-"))
    return (by - ay) * 12 + (bm - am)


if __name__ == "__main__":
    main()
