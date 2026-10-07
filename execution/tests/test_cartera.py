"""Carpeta cripto: el vigilante minuto a minuto (stops, trailing, tomas) sin red."""
import importlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cartera"))


@pytest.fixture
def c(tmp_path, monkeypatch):
    monkeypatch.setenv("CARTERA_DIR", str(tmp_path))
    import cartera as m
    return importlib.reload(m)


def libro(c, nivel="riesgo", entrada=100.0, **reglas):
    r = dict(c.REGLAS[nivel], tp=[list(x) for x in c.REGLAS[nivel]["tp"]]) | reglas
    return {"inicio": {"ms": 0, "capital": 1000, "btc": 1}, "usdt": 0.0, "comisiones_usd": 0.0, "operaciones": [],
            "posiciones": {"XUSDT": {"nivel": nivel, "cantidad": 1.0, "entrada": entrada, "maximo": entrada,
                                     "reglas": r, "tomas_hechas": [], "vigilado_hasta": 0}}}


def vela(minuto, abre, alto, bajo):
    return [minuto * 60_000, str(abre), str(alto), str(bajo), str(abre), "0", minuto * 60_000 + 59_999]


def test_stop_fijo_vende_al_precio_del_stop(c):
    lb = libro(c)  # riesgo: stop 15%
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(0, 100, 100, 90), vela(1, 90, 91, 84)])
    assert len(ops) == 1 and ops[0]["precio"] == pytest.approx(85.0)
    assert "XUSDT" not in lb["posiciones"]
    assert lb["usdt"] == pytest.approx(85 * 0.999)


def test_gap_vende_a_la_apertura_no_al_stop(c):
    lb = libro(c)
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(0, 70, 72, 69)])
    assert ops[0]["precio"] == 70


def test_trailing_sube_con_el_maximo(c):
    lb = libro(c, tp=[])  # trailing 15%
    velas = [vela(0, 100, 130, 100), vela(1, 128, 129, 112)]  # stop pasa a 110.5
    ops = c.vigilar_posicion(lb, "XUSDT", velas)
    assert ops == [] and c.stop_vigente(lb["posiciones"]["XUSDT"]) == pytest.approx(110.5)
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(2, 112, 112, 110)])
    assert ops[0]["precio"] == pytest.approx(110.5)


def test_el_maximo_de_la_vela_no_sube_el_stop_de_esa_misma_vela(c):
    lb = libro(c, tp=[])
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(0, 100, 130, 100)])  # sube a 130 y baja a 100 en el mismo minuto
    assert ops == []


def test_tomas_de_ganancia_parciales(c):
    lb = libro(c)  # tomas +40% la mitad, +100% la mitad de lo que queda
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(0, 100, 141, 100)])
    assert len(ops) == 1 and ops[0]["cantidad"] == pytest.approx(0.5) and ops[0]["precio"] == pytest.approx(140)
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(1, 141, 201, 140)])
    assert len(ops) == 1 and ops[0]["cantidad"] == pytest.approx(0.25)
    assert lb["posiciones"]["XUSDT"]["cantidad"] == pytest.approx(0.25)
    assert c.vigilar_posicion(lb, "XUSDT", [vela(2, 200, 260, 199)]) == []  # no repite tomas


def test_stop_y_toma_en_la_misma_vela_asume_lo_peor(c):
    lb = libro(c)
    ops = c.vigilar_posicion(lb, "XUSDT", [vela(0, 100, 150, 80)])
    assert len(ops) == 1 and "Stop" in ops[0]["motivo"]


def test_acciones_tokenizadas_afuera(c):
    for b in ("NVDAB", "QQQB", "MSTRB", "MUB"):
        assert c.es_accion_tokenizada(b)
    for b in ("BNB", "ARB", "BTC", "NEAR"):
        assert not c.es_accion_tokenizada(b)
