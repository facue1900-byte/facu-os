"""
Tests del radar de deudores del Paseo (lee las pestañas por local, no la consolidada).
Grillas armadas a mano con la forma real de las pestañas: nunca toca Google Sheets.
"""
import datetime as dt
import sys

import pytest

sys.path.insert(0, "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts")

import radar_deudores as rd  # noqa: E402
import reglas_locales as rl  # noqa: E402

CAB = [["CTA CTE"], [], [], ["Locatario:"], ["Mes Origen", "UN", "Detalle", "FC", "Ingreso ", "Egreso", "SALDO"]]


def tab_fgh(filas, signo=+1):
    """Layout Fabric/Bigg/Boss: detalle C, ingreso E, egreso F, saldo G. Encadena el saldo."""
    out, s = list(CAB), 0.0
    for a, det, ing, eg in filas:
        s += (eg or 0) - (ing or 0)
        out.append([a, "", det, "", ing or "", "" if eg is None else eg, s * signo])
    return out


def tab_efg(filas):
    """Layout Volta/Peak One: detalle C, ingreso D, egreso E, saldo F."""
    out, s = [["x"]] * 4 + [["Mes Origen", "", "Detalle", "Ingreso ", "Egreso", "SALDO"]], 0.0
    for a, det, ing, eg in filas:
        s += (eg or 0) - (ing or 0)
        out.append([a, "", det, ing or "", "" if eg is None else eg, s])
    return out


def bloque(mes_alq, mes_exp, alq, exp, pagos=()):
    return ([(mes_alq, "Alquiler", None, alq), (mes_alq, "IVA Alquiler", None, alq * 0.21)]
            + [(f, "parcial", p, None) for f, p in pagos]
            + [(mes_exp, "Recupero de gastos", None, exp), (mes_exp, "Servicios comunes", None, exp)])


def hojas(fabric=None, otros_hasta="NOV'26", cargos=(), cobros=()):
    chico = tab_fgh([(otros_hasta, "Alquiler", None, 100.0)])
    return {
        "Fabric": fabric if fabric is not None else tab_fgh([(otros_hasta, "Alquiler", None, 100.0)], signo=-1),
        "Bigg": chico, "Boss": chico,
        "Volta + Open 25": tab_efg([(otros_hasta, "Alquiler", None, 100.0)]),
        # Peak One no paga alquiler: su último período va en $0 (como en la planilla real)
        "Peak One": tab_efg([("JUL'26", "Recupero de gastos", None, 100.0),
                             (otros_hasta, "Alquiler", None, 0), (otros_hasta, "IVA Alquiler", None, 0)]),
        "CARGOS": [[], [], []] + [list(c) for c in cargos],
        "Cobros": [[], []] + [list(c) for c in cobros],
    }


def correr(h, mes=(2026, 11)):
    movs, ch = rd.leer_fuente(h)
    return rd.clasificar(movs, mes, ch)


def por_nombre(lista):
    return {n: l for n, l in lista}


def fabric_al_dia_nov():
    # OCT: alquiler oct + expensas sep pagado entero en oct; NOV: alquiler nov + expensas oct, sin pagos
    filas = bloque("OCT'26", "OCT'26", 1000.0, 100.0, pagos=[(dt.datetime(2026, 10, 6), 1210.0)])
    filas = [(a, d, i, e) for a, d, i, e in filas]
    # la expensa de OCT va en el bloque de noviembre, como en la planilla
    filas += [("NOV'26", "Alquiler", None, 1000.0), ("NOV'26", "IVA Alquiler", None, 210.0)]
    return filas


def test_periodo_de():
    assert rd.periodo_de("OCT'26") == (2026, 10)
    assert rd.periodo_de("JUL' 26") == (2026, 7)
    assert rd.periodo_de(dt.datetime(2026, 11, 6)) == (2026, 11)
    assert rd.periodo_de("parcial alquiler") is None


def test_mes_de_cobro_alquiler_en_el_mes_expensas_al_siguiente():
    assert rl.mes_de_cobro("Alquiler", (2026, 11)) == (2026, 11)
    assert rl.mes_de_cobro("Diferencia Alquiler (sin iva)", (2026, 11)) == (2026, 11)
    assert rl.mes_de_cobro("IVA Servicios Comunes", (2026, 10)) == (2026, 11)
    assert rl.mes_de_cobro("Recupero de gastos", (2026, 12)) == (2027, 1)
    assert rl.mes_de_cobro("Bonificación expensas (Facu 02/11)", (2026, 10)) == (2026, 11)
    with pytest.raises(ValueError):
        rl.mes_de_cobro("Punitorio raro", (2026, 10))


def test_bloque_del_mes_no_es_deuda_exigible():
    f = fabric_al_dia_nov()
    deudores, al_dia, _, sin_dato = correr(hojas(fabric=tab_fgh(f, signo=-1)))
    assert sin_dato == [] and deudores == []
    fab = por_nombre(al_dia)["Fabric"]
    assert fab["exigible"] == 0
    # en curso = alquiler nov + IVA + expensas oct (recupero + servicios)
    assert fab["en_curso"] == pytest.approx(1210.0 + 200.0)


def test_mes_siguiente_el_bloque_viejo_pasa_a_exigible():
    f = fabric_al_dia_nov()
    deudores, _, _, _ = correr(hojas(fabric=tab_fgh(f, signo=-1), otros_hasta="DIC'26"), mes=(2026, 12))
    assert por_nombre(deudores)["Fabric"]["exigible"] == pytest.approx(1410.0)


def test_pago_del_mes_cancela_primero_lo_viejo():
    f = bloque("OCT'26", "SEP'26", 1000.0, 100.0, pagos=[(dt.datetime(2026, 10, 9), 1000.0)])
    f += [("NOV'26", "Alquiler", None, 1000.0), (dt.datetime(2026, 11, 6), "pago", 500.0, None)]
    # exigible al 1/11: 1210 + 200 (expensas sep → cobro oct) − 1000 = 410; pagó 500 en nov → 0, sobran 90
    deudores, al_dia, _, _ = correr(hojas(fabric=tab_fgh(f, signo=-1)))
    fab = por_nombre(al_dia)["Fabric"]
    assert fab["exigible"] == 0 and fab["en_curso"] == pytest.approx(1000.0 - 90.0)


def test_residuo_de_centavos_no_es_deuda():
    f = [("OCT'26", "Alquiler", None, 1000.0), (dt.datetime(2026, 10, 9), "pago", 997.34, None),
         ("NOV'26", "Alquiler", None, 1000.0)]
    _, al_dia, _, _ = correr(hojas(fabric=tab_fgh(f, signo=-1)))
    assert por_nombre(al_dia)["Fabric"]["residuo"] == pytest.approx(2.66)


def test_fuente_atrasada_no_se_informa():
    # todo cargado hasta JUL'26: en noviembre no hay número confiable
    f = [("JUL'26", "Alquiler", None, 1000.0)]
    deudores, al_dia, _, sin_dato = correr(hojas(fabric=tab_fgh(f, signo=-1), otros_hasta="JUL'26"))
    assert deudores == [] and al_dia == []
    assert {n for n, _ in sin_dato} >= {"Fabric", "Bigg", "Boss", "Volta + Open 25", "Peak One"}
    assert "2026-07" in dict(sin_dato)["Fabric"]


def test_cargo_en_cero_cuenta_como_periodo_cargado():
    # Peak One no paga alquiler: su NOV'26 está en $0 y NO es «fuente atrasada»
    _, al_dia, _, sin_dato = correr(hojas())
    assert "Peak One" in por_nombre(al_dia) and sin_dato == []


def test_cadena_de_saldo_rota_no_se_informa():
    f = tab_fgh([("NOV'26", "Alquiler", None, 1000.0)], signo=-1)
    f[-1][6] = 999_999.0           # alguien pisó el SALDO
    _, al_dia, _, sin_dato = correr(hojas(fabric=f))
    assert "Fabric" not in por_nombre(al_dia)
    assert "cadena" in dict(sin_dato)["Fabric"]


def test_cargo_sin_periodo_corta():
    f = tab_fgh([("sin fecha", "Alquiler", None, 1000.0)], signo=-1)
    with pytest.raises(ValueError, match="sin período"):
        rd.leer_fuente(hojas(fabric=f))


def test_salon_desde_cargos_y_cobros():
    cargos = [(dt.datetime(2026, 10, 1), "Salón (Alto)", "Servicios comunes", 1e6, 0, 1e6),
              (dt.datetime(2026, 11, 1), "Salón (Alto)", "Alquiler", 1e6, 0, 1e6),
              (dt.datetime(2026, 11, 1), "Fabric", "Alquiler", 5e6, 0, 5e6)]      # con pestaña: se ignora
    cobros = [(dt.datetime(2026, 11, 5), "Salon Multiespacios", 1e6, "Caja", "")]
    deudores, al_dia, _, _ = correr(hojas(cargos=cargos, cobros=cobros))
    salon = por_nombre(al_dia)["Salón (Alto)"]
    assert salon["exigible"] == 0 and salon["en_curso"] == pytest.approx(1e6)


def test_local_desconocido_en_cargos_corta():
    cargos = [(dt.datetime(2026, 11, 1), "Local Nuevo", "Alquiler", 1e6, 0, 1e6)]
    with pytest.raises(ValueError, match="no conoce"):
        rd.leer_fuente(hojas(cargos=cargos))


def test_regla_propia_nunca_es_deudor():
    cargos = [(dt.datetime(2026, 9, 1), "La Jaula / torneo", "Alquiler", 9e6, 0, 9e6)]
    deudores, _, con_regla, _ = correr(hojas(cargos=cargos))
    assert "La Jaula / torneo" in por_nombre(con_regla)
    assert "La Jaula / torneo" not in por_nombre(deudores)


def test_falta_una_pestana_corta():
    h = hojas()
    del h["Boss"]
    with pytest.raises(ValueError, match="Boss"):
        rd.leer_fuente(h)
