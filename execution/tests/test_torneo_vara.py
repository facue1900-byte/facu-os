"""La vara del Torneo: toda fila de vivo.json se compara contra P1, no contra el precio crudo."""
import importlib.util
import json
import sys
from pathlib import Path

RUTA = Path(__file__).resolve().parents[1] / "cartera" / "torneo.py"


def _cargar(tmp_path, monkeypatch):
    monkeypatch.setenv("TORNEO_DIR", str(tmp_path))
    spec = importlib.util.spec_from_file_location("torneo_test", RUTA)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["torneo_test"] = mod
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "DIR", tmp_path)
    return mod


class _D:
    t = [0, 14400000, 28800000]
    n = 3


class _E:
    def __init__(self, nombre):
        self.nombre, self.personalidad = nombre, "x"


def test_hodl_de_cada_fila_es_p1_y_el_crudo_queda_aparte(tmp_path, monkeypatch):
    m = _cargar(tmp_path, monkeypatch)
    rets = {"P1 HODL BTC": -0.0202, "L9 otra": 0.0203}
    monkeypatch.setattr(m, "Datos", _D)
    monkeypatch.setattr(m, "estrategias", lambda: [_E(k) for k in rets])
    monkeypatch.setattr(m, "con_noticias", lambda e: e)
    monkeypatch.setattr(m, "regimen", lambda D, i: "r")
    monkeypatch.setattr(m, "ms", lambda s: 0)
    monkeypatch.setattr(m, "correr", lambda e, D, a, b: {
        "final": 1000 * (1 + rets[e.nombre]), "ret": rets[e.nombre], "dd": 0.0, "ops": 1, "hodl_btc": -0.0352})
    (tmp_path / "noticias.jsonl").write_text(
        '{"fecha": "2026-11-02 00:41", "sesgo": "neutral", "busqueda": "sin_dato"}\n'
        '{"fecha": "2026-11-03 00:41", "sesgo": "neutral"}\n')
    out = m.vivo("2026-10-29")
    guardado = json.loads((tmp_path / "vivo.json").read_text())
    assert out["noticias_sin_dato"] == 1 and out["noticias_lecturas"] == 2
    for f in guardado["filas"]:
        assert f["hodl_btc"] == -0.0202
        assert f["btc_precio_crudo"] == -0.0352
    assert "sin dato fresco: 1 de 2" in (tmp_path / "RESUMEN.md").read_text()
