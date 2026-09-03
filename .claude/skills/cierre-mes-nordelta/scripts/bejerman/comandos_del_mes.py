#!/usr/bin/env python3
"""
Los 6 comandos de `emitir.js` del mes, sacados de CARGOS.

    comandos_del_mes.py 2026-09

Cada mes se emiten seis comprobantes en Bejerman: para **Fabric** y **Bigg**, el
alquiler del mes corriente más el recupero y los servicios comunes del mes
anterior. Los otros locales pagan en efectivo y no llevan factura.

Esto sólo **arma los comandos**: no abre el navegador ni emite nada. La emisión
la dispara Facu, que además tiene que loguearse a mano — el robot no guarda
credenciales (ver README.md).

Dos cosas que no se pueden hacer a ojo y por eso se calculan acá:

- **El importe va redondeado al peso**, y el total tiene que ser el del precio YA
  redondeado (`round(neto) * 1,21`), no el IVA del importe con centavos. Si no,
  el total que se tipea no coincide con el que calcula Bejerman.
- **La mitad en efectivo de Bigg NO se factura.** El renglón
  `Diferencia Alquiler (sin iva)` es su 50% en mano: sale de la cuenta corriente,
  no de una Factura A. Meterlo acá le factura de más.
"""

import sys
import calendar
import datetime

sys.path.insert(0, "/Users/Facu/facu-os/execution")
from google_auth import sheets  # noqa: E402

CTAS = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
IVA = 0.21
MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre",
         11: "Noviembre", 12: "Diciembre"}

# local en CARGOS -> (nombre del cliente en Bejerman, código, alias)
CLIENTES = {"Fabric": ("SUSHINOR", "000001"), "Bigg": ("RODOLFO SRL", "000002")}
# concepto en CARGOS -> (código, descripción, lleva IVA, tipo de comprobante)
#
# 🔴 El recupero NO es una Factura: va como **Nota de Débito**. Se ve en la
# grilla de Bejerman —los recuperos de julio y agosto salieron como `ND A 0002`—
# y una ND además **exige el período**, que es un campo distinto del de servicio
# y hace fallar la emisión si falta. Emitirlo como FC entra igual y queda mal
# tipificado ante ARCA.
CONCEPTOS = {
    "Alquiler": ("015", "Alquiler {mes} {anio}", True, "FC"),
    "Servicios comunes": ("008", "Servicios y Expensas {mes} {anio}", True, "FC"),
    "Recupero de gastos": ("EXE", "Recupero de Gastos {mes} {anio}", False, "ND"),
}
TIPOS = {
    "FC": ("FC", "FC - Factura", "Factura"),
    "ND": ("ND", "ND - Nota de", "Nota de d"),
}


def desde_serial(n):
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=float(n))


def ar(x):
    """1234567.89 -> '1.234.567,89', como lo tipea Bejerman."""
    return f"{x:,.2f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    mes = sys.argv[1]
    anio, m = (int(x) for x in mes.split("-"))
    ant = datetime.date(anio, m, 1) - datetime.timedelta(days=1)

    filas = sheets().spreadsheets().values().get(
        spreadsheetId=CTAS, range="CARGOS!A4:I500",
        valueRenderOption="UNFORMATTED_VALUE").execute().get("values", [])

    quiero = {(mes, "Alquiler"),
              (f"{ant.year}-{ant.month:02d}", "Recupero de gastos"),
              (f"{ant.year}-{ant.month:02d}", "Servicios comunes")}
    encontrado = {}
    for r in filas:
        r = list(r) + [""] * 9
        if not r[0] or r[1] not in CLIENTES:
            continue
        f = desde_serial(r[0])
        clave = (f"{f.year}-{f.month:02d}", str(r[2]).strip())
        if clave in quiero:
            encontrado.setdefault((r[1], clave[1]), []).append(
                (clave[0], float(r[3] or 0)))

    faltan = [(loc, c) for loc in CLIENTES for c in CONCEPTOS
              if (loc, c) not in encontrado]
    if faltan:
        sys.exit("FRENO — faltan cargos en CARGOS para " +
                 ", ".join(f"{l}/{c}" for l, c in faltan) +
                 f".\nCorré primero: cargos_del_mes.py {mes} --escribir")

    print(f"# Facturación Bejerman — {MESES[m]} {anio}")
    print(f"# Alquiler de {MESES[m].lower()} + recupero y servicios de "
          f"{MESES[ant.month].lower()}. Punto de venta 0002.")
    print("#")
    print("# ANTES: abrir el Chrome con --remote-debugging-port=9333 (ver README),")
    print("# loguearse a mano y entrar a Ventas → Facturación.")
    print()

    total_general = 0.0
    for loc, (busca, codigo) in CLIENTES.items():
        print(f"# ---------- {loc} ({busca}, cliente {codigo}) ----------")
        for concepto, (conc, plantilla, lleva_iva, tipo) in CONCEPTOS.items():
            periodo, neto = encontrado[(loc, concepto)][0]
            f = datetime.date(*(int(x) for x in periodo.split("-")), 1)
            precio = round(neto)
            total = precio * (1 + IVA) if lleva_iva else float(precio)
            total_general += total
            desc = plantilla.format(mes=MESES[f.month], anio=f.year)
            bt, pt, et = TIPOS[tipo]
            periodo = ""
            if tipo == "ND":
                # El período de una ND es el mes que se está recuperando, entero.
                ult = calendar.monthrange(f.year, f.month)[1]
                periodo = (f',"desde":"01/{f.month:02d}/{f.year}",'
                           f'"hasta":"{ult}/{f.month:02d}/{f.year}"')
            print(f"# {concepto}: {tipo} · neto ${neto:,.2f} → precio ${precio:,} · "
                  f"{'IVA 21%' if lleva_iva else 'EXENTO'} → total ${total:,.2f}")
            print("node emitir.js '" + (
                '{"buscaCli":"%s","pickCli":"%s","espCli":"%s",'
                '"buscaTipo":"%s","pickTipo":"%s","espTipo":"%s",'
                '"buscaConc":"%s","pickConc":"%s","espConc":"%s",'
                '"desc":"%s","precio":"%d","total":"%s"%s}'
            ) % (busca, codigo, busca, bt, pt, et, conc, conc, conc,
                 desc, precio, ar(total), periodo)
                  + "'")
            print()
    print(f"# TOTAL de los 6 comprobantes: ${total_general:,.2f}")
    print("#")
    print("# DESPUÉS de cada uno: 'Agregar' NO es 'Emitir'. Y verificar bajando el PDF —")
    print("# PROWEB/facturas/101838/0073/<TIPO> A0002-<NRO>.pdf · 404 = no existe.")


if __name__ == "__main__":
    main()
