"""Carpeta ficticia: topes, comisión y valuación con precios fijos (sin red)."""
import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "paper"))

PRECIOS = {"BTCUSDT": {"bid": 99_990.0, "ask": 100_010.0}, "ETHUSDT": {"bid": 1_999.0, "ask": 2_001.0},
           "SOLUSDT": {"bid": 99.0, "ask": 101.0}, "BNBUSDT": {"bid": 499.0, "ask": 501.0}}


@pytest.fixture
def paper(tmp_path, monkeypatch):
    monkeypatch.setenv("PAPER_DIR", str(tmp_path))
    import paper as m
    m = importlib.reload(m)
    monkeypatch.setattr(m, "libro_de_precios", lambda: PRECIOS)
    m.cmd_init(10_000, False)
    return m


def test_compra_al_ask_con_comision(paper):
    r = paper.cmd_orden("buy", "BTCUSDT", 2_000, False, "tesis de prueba larga")
    assert r["operacion"]["cantidad"] == pytest.approx(1_998 / 100_010)
    assert r["estado"]["usdt"] == 8_000
    assert r["estado"]["comisiones_pagadas_usd"] == 2.0


def test_tope_del_25_por_ciento(paper):
    with pytest.raises(paper.ErrorPaper, match="tope"):
        paper.cmd_orden("buy", "BTCUSDT", 2_500.01, False, "tesis de prueba larga")


def test_par_no_permitido_y_sin_motivo(paper):
    with pytest.raises(paper.ErrorPaper, match="no está permitido"):
        paper.cmd_orden("buy", "DOGEUSDT", 100, False, "tesis de prueba larga")
    with pytest.raises(paper.ErrorPaper, match="motivo"):
        paper.cmd_orden("buy", "BTCUSDT", 100, False, "")


def test_no_se_vende_lo_que_no_hay(paper):
    with pytest.raises(paper.ErrorPaper, match="No hay"):
        paper.cmd_orden("sell", "ETHUSDT", None, True, "tesis de prueba larga")


def test_vuelta_completa_pierde_spread_y_comisiones(paper):
    paper.cmd_orden("buy", "ETHUSDT", 2_000, False, "tesis de prueba larga")
    r = paper.cmd_orden("sell", "ETHUSDT", None, True, "tesis de prueba larga")
    cant = 1_998 / 2_001
    esperado = 8_000 + cant * 1_999 * 0.999
    assert r["estado"]["total_usd"] == pytest.approx(esperado, abs=0.01)
    assert "ETHUSDT" not in r["estado"]["posiciones"]


def test_init_no_pisa_una_carpeta_existente(paper):
    with pytest.raises(paper.ErrorPaper, match="Ya hay"):
        paper.cmd_init(10_000, False)
