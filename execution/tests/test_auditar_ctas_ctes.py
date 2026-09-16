"""
Tests para `auditar_local` en
/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/auditar_ctas_ctes.py

Se corre con el Python del venv del OS:
    /Users/Facu/facu-os/.venv/bin/python -m pytest <este archivo> -v

Nunca toca Google Sheets: `Planillas` se reemplaza por un doble (`FakePlanillas`)
que devuelve grillas armadas a mano para los dos renders que usa `auditar_local`
("UNFORMATTED_VALUE" y "FORMULA"). Read-only por diseño, así que no hay nada que
mockear del lado de escritura.

Cubre sólo los dos chequeos que Facu pidió probar:
  1. FILA SIN IMPORTE — dispara con celdas VACÍAS, no con un 0 escrito.
  2. IVA COBRADO A QUIEN NO FACTURA — dispara con egreso > 0 en "iva ..." cuando
     el local no factura, y NO dispara cuando factura.
"""
import sys

sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")

from auditar_ctas_ctes import auditar_local, col  # noqa: E402
from cargos_del_mes import LAYOUT_SIN_FC  # noqa: E402


class FakePlanillas:
    """Doble de `Planillas`: sólo implementa `.leer()`, que es lo único que usa
    `auditar_local`. Ignora `sid` y `rango` a propósito — en estos tests siempre
    hay una sola pestaña en juego, así que no hace falta rutear por nombre."""

    def __init__(self, valores, formulas):
        self._valores = valores
        self._formulas = formulas

    def leer(self, sid, rango, render="FORMATTED_VALUE"):
        return self._formulas if render == "FORMULA" else self._valores


def construir_grillas(filas_datos, layout):
    """Arma (valores, formulas) como si vinieran de la pestaña real.

    `filas_datos` es una lista de (etiqueta_mes, detalle, ingreso, egreso), una
    por movimiento, en el orden en que van a quedar a partir de la fila 7 (la
    6 es el encabezado "Mes Origen..." que `auditar_local` usa para ubicar
    dónde arrancan los movimientos — igual que en la pestaña real).

    `ingreso`/`egreso` van tal cual quedarían en la celda: "" para vacía, "0"
    para un cero escrito, o el monto.

    La cadena del saldo se genera sola (`=F{i-1}+D{i}-E{i}`, con las letras del
    layout) para que el chequeo de la cadena del saldo no dispare hallazgos que
    no vienen al caso en estos tests.
    """
    c_det, c_ing = col(layout["detalle"]), col(layout["ingreso"])
    c_egr, c_sal = col(layout["egreso"]), col(layout["saldo"])

    valores = [[""] * 8 for _ in range(5)]  # filas 1-5: encabezado de arriba
    valores.append(["Mes Origen", "Medio", "Detalle", "Ingreso", "Egreso",
                     "Saldo", "", ""])  # fila 6
    formulas = [[""] * 8 for _ in range(6)]

    primera = 7
    for offset, (etq, det, ing, egr) in enumerate(filas_datos):
        i = primera + offset
        fila = [""] * 8
        fila[0] = etq
        fila[c_det] = det
        fila[c_ing] = ing
        fila[c_egr] = egr
        valores.append(fila)

        ffila = [""] * 8
        if offset > 0:
            ffila[c_sal] = (f"={layout['saldo']}{i - 1}+"
                             f"{layout['ingreso']}{i}-{layout['egreso']}{i}")
        formulas.append(ffila)

    return valores, formulas


def cfg_base(iva, pestania="TestLocal"):
    return {
        "layout": LAYOUT_SIN_FC,
        "pestania": pestania,
        "iva": iva,
        "cobra_por": "Efectivo" if not iva else "Banco",
        "partido": False,
    }


def tipos(hallazgos):
    return [tipo for _, tipo, _ in hallazgos]


# ---------------------------------------------------------- FILA SIN IMPORTE ---

def test_cero_escrito_no_es_fila_sin_importe():
    """(a) Egreso con un 0 tipeado e ingreso vacío: es la regla de Facu del
    06/08/2026, NO es un hallazgo."""
    filas = [("JUL'26", "Servicios comunes", "", "0")]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=False)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    assert "FILA SIN IMPORTE" not in tipos(hallazgos)


def test_celdas_vacias_si_es_fila_sin_importe():
    """(b) Ingreso Y egreso vacíos: sí es un hallazgo — la celda no dice nada."""
    filas = [("JUL'26", "Recupero de gastos", "", "")]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=False)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    disparados = [h for h in hallazgos if h[1] == "FILA SIN IMPORTE"]
    assert len(disparados) == 1
    assert "Recupero de gastos" in disparados[0][2]


def test_las_dos_filas_juntas_solo_dispara_la_vacia():
    """Las dos filas (a) y (b) en la misma pestaña: sólo la vacía es hallazgo,
    el 0 escrito de al lado no contamina el resultado."""
    filas = [
        ("JUL'26", "Servicios comunes", "", "0"),
        ("JUL'26", "Recupero de gastos", "", ""),
    ]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=False)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    disparados = [h for h in hallazgos if h[1] == "FILA SIN IMPORTE"]
    assert len(disparados) == 1
    assert "Recupero de gastos" in disparados[0][2]
    assert "Servicios comunes" not in disparados[0][2]


# --------------------------------------------- IVA COBRADO A QUIEN NO FACTURA ---

def test_iva_cobrado_a_quien_no_factura_dispara():
    """(c) Fila 'IVA Alquiler' con egreso 500000 en un local con iva=False:
    tiene que disparar el hallazgo."""
    filas = [("JUL'26", "IVA Alquiler", "", 500000)]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=False)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    disparados = [h for h in hallazgos
                  if h[1] == "🔴 IVA COBRADO A QUIEN NO FACTURA"]
    assert len(disparados) == 1
    assert "TestLocal" in disparados[0][2]


def test_iva_cobrado_no_dispara_si_el_local_factura():
    """(d) La misma fila, mismo importe, pero en un local con iva=True: no
    tiene que disparar — ahí el IVA es correcto."""
    filas = [("JUL'26", "IVA Alquiler", "", 500000)]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=True)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    assert "🔴 IVA COBRADO A QUIEN NO FACTURA" not in tipos(hallazgos)


def test_iva_sin_egreso_no_dispara_aunque_no_facture():
    """Una fila de IVA sin importe (egreso en 0/vacío) no es plata cobrada de
    más: el chequeo pide egreso > 0, no sólo que exista la fila."""
    filas = [("JUL'26", "IVA Alquiler", "", "0")]
    valores, formulas = construir_grillas(filas, LAYOUT_SIN_FC)
    p = FakePlanillas(valores, formulas)
    cfg = cfg_base(iva=False)

    hallazgos, _, _ = auditar_local(p, "TestLocal", cfg, cargos={})

    assert "🔴 IVA COBRADO A QUIEN NO FACTURA" not in tipos(hallazgos)
