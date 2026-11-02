"""Escenarios cripto a 10.000: regla de tres, ventana común y nada de repartir lo que falta."""
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cartera"))
import escenarios as e


def fila(dia, total, hodl=1000.0):
    return {"fecha": datetime(2026, 10, dia), "total": total, "hodl": hodl}


def test_csv_ordena_por_fecha_y_lee_formato_real():
    texto = ("fecha,total_usd,resultado_pct,hodl_btc\n"
             "2026-10-29 10:00 UTC,900.0,-10,950\n2026-10-07 21:04 UTC,998.11,-0.19,999.17\n")
    filas = e.leer_csv(texto)
    assert [f["total"] for f in filas] == [998.11, 900.0]


def test_caja_mide_desde_inicio_y_desde_la_ultima_fila_previa_a_la_ventana():
    r = e.caja([fila(7, 1000), fila(28, 900), fila(30, 810)], 1000)
    assert r["inicio"] == pytest.approx(-0.19)
    assert r["ventana"] == pytest.approx(-0.10)


def test_caja_sin_fila_previa_a_la_ventana_dice_que_falta():
    assert e.caja([fila(30, 810)], 1000)["ventana"] is None
    assert e.caja([], 1000) == {"inicio": None, "ventana": None, "dato": None}


def test_caja_frenada_antes_de_la_ventana_falta_y_no_da_cero():
    filas = [fila(7, 1000), fila(27, 900)]
    assert e.caja(filas, 1000)["ventana"] is None
    assert e.hodl_ventana(filas) is None


def test_torneo_incompleto_no_da_promedio():
    filas = [{"ret": 0.1, "estrategia": "x"}] * (e.MIN_ESTRATEGIAS - 1)
    assert e.torneo({"filas": filas, "generado": "2026-11-02 12:48"})["ventana"] is None


def test_torneo_promedia_y_marca_extremos():
    filas = [{"ret": 0.0, "estrategia": "x"}] * (e.MIN_ESTRATEGIAS - 2)
    filas += [{"ret": 0.3, "estrategia": "mejor"}, {"ret": -0.3, "estrategia": "peor"}]
    r = e.torneo({"filas": filas, "generado": "2026-11-02 12:48"})
    assert r["ventana"] == pytest.approx(0.0)
    assert r["mejor"]["estrategia"] == "mejor" and r["peor"]["estrategia"] == "peor"


def test_mezcla_suma_lo_de_cada_caja():
    res = {"A": {"ventana": 0.10}, "B": {"ventana": -0.10}}
    assert e.mezcla({"A": 0.75, "B": 0.25}, res) == pytest.approx(7500 * 1.1 + 2500 * 0.9)


def test_mezcla_con_una_caja_sin_dato_no_reparte_entre_las_demas():
    assert e.mezcla({"A": 0.5, "B": 0.5}, {"A": {"ventana": 0.1}, "B": {"ventana": None}}) is None
    assert e.mezcla({"A": 0.5, "B": 0.5}, {"A": {"ventana": 0.1}}) is None


def test_mezcla_rechaza_pesos_que_no_suman_uno():
    with pytest.raises(ValueError):
        e.mezcla({"A": 0.5}, {"A": {"ventana": 0.1}})


@pytest.mark.parametrize("pesos", e.MEZCLAS.values())
def test_las_mezclas_definidas_suman_uno_y_usan_cajas_que_existen(pesos):
    assert sum(pesos.values()) == pytest.approx(1)
    assert set(pesos) <= set(e.CAJAS) | {e.TORNEO}


def test_informe_escribe_falta_y_no_un_numero():
    res = {c: {"inicio": 0.0, "ventana": 0.0, "dato": datetime(2026, 11, 2)} for c in e.CAJAS}
    res[e.TORNEO] = {"inicio": None, "ventana": None, "dato": None, "n": 3}
    texto = e.informe(res, -0.04)
    assert "| Torneo (promedio) | falta (falta) | falta (falta) | falta |" in texto
    assert "| Agresivo |" in texto and "| falta | falta |" in texto
    assert "9.600 (-4,00%)" in texto
