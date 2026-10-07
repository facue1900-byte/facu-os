"""El chequeo de tareas del radar tiene que GRITAR cuando algo falló o no corrió.

Un chequeo que nunca falló desde que existe es sospechoso (regla 3): acá se le fabrican
las tres fallas que tiene que ver — falló, no corrió, no está cargada.
"""
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "radar"))
import recolectar  # noqa: E402

PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<!-- un comentario con -- adentro, como reporte-pauta -->
<key>Label</key><string>com.facu.{n}</string>
<key>ProgramArguments</key><array><string>/bin/bash</string><string>correr.sh</string><string>{n}</string></array>
<key>StartCalendarInterval</key><dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
</dict></plist>"""


def _armar(tmp, monkeypatch, registros, cargadas):
    agents, repo, logs = tmp / "agents", tmp / "repo", tmp / "logs"
    for d in (agents, repo, logs):
        d.mkdir()
    for n in ("diaria", "rota", "sin-cargar"):
        (repo / f"com.facu.{n}.plist").write_text(PLIST.format(n=n))
        if n != "sin-cargar":
            (agents / f"com.facu.{n}.plist").write_text(PLIST.format(n=n))
    reg = logs / "tareas.jsonl"
    reg.write_text("".join(json.dumps(r) + "\n" for r in registros))
    for f in agents.iterdir():  # instalados hace mucho: el piso de "instalación" no tapa nada
        os.utime(f, (0, 0))
    monkeypatch.setattr(recolectar, "AGENTS", agents)
    monkeypatch.setattr(recolectar, "REPO_PLISTS", repo)
    monkeypatch.setattr(recolectar, "REGISTRO", reg)
    sh_real = recolectar.sh
    lista = "\n".join(f"-\t0\tcom.facu.{n}" for n in cargadas)
    monkeypatch.setattr(recolectar, "sh", lambda cmd, cwd=None: lista if cmd[0] == "bash" else sh_real(cmd, cwd))


def _reg(tarea, cuando, codigo):
    return {"tarea": tarea, "inicio": cuando.strftime("%Y-%m-%dT%H:%M:%S%z"), "fin": "", "codigo": codigo}


def test_detecta_fallo_no_corrio_y_no_cargada(tmp_path, monkeypatch):
    ahora = datetime.now().astimezone().replace(hour=23, minute=0)
    hace5 = ahora - timedelta(days=5)
    _armar(tmp_path, monkeypatch,
           [_reg("diaria", hace5, 0), _reg("rota", ahora - timedelta(hours=13), 1)],
           cargadas=["diaria", "rota"])
    md, n = recolectar.chequeo_tareas(ahora)
    assert n == 3, md
    assert "diaria: NO CORRIÓ" in md
    assert "rota: FALLÓ" in md
    assert "sin-cargar: NO ESTÁ CARGADA" in md


def test_todo_bien_no_grita(tmp_path, monkeypatch):
    ahora = datetime.now().astimezone().replace(hour=23, minute=0)
    corrio = ahora.replace(hour=9, minute=1)
    _armar(tmp_path, monkeypatch,
           [_reg("diaria", ahora - timedelta(days=5), 0), _reg("diaria", corrio, 0), _reg("rota", corrio, 0),
            _reg("sin-cargar", corrio, 0)],
           cargadas=["diaria", "rota", "sin-cargar"])
    (tmp_path / "agents" / "com.facu.sin-cargar.plist").write_text(PLIST.format(n="sin-cargar"))
    md, n = recolectar.chequeo_tareas(ahora)
    assert n == 0, md
    assert "Ninguna" in md


def test_diaria_a_la_hora_del_radar_que_ayer_no_corrio(tmp_path, monkeypatch):
    # El bug que encontró code-reviewer: radar a las 09:05, tarea diaria a las 09:00, que
    # ayer no corrió. Antes daba "al día" porque juzgaba la de hoy (hace 5 minutos).
    ahora = datetime.now().astimezone().replace(hour=9, minute=5)
    _armar(tmp_path, monkeypatch,
           [_reg("diaria", ahora - timedelta(days=3), 0), _reg("rota", ahora - timedelta(minutes=4), 0)],
           cargadas=["diaria", "rota"])
    md, n = recolectar.chequeo_tareas(ahora)
    assert "diaria: NO CORRIÓ" in md, md
    assert "rota: NO CORRIÓ" not in md, md


def test_linea_rota_del_registro_no_tira_el_radar(tmp_path, monkeypatch):
    ahora = datetime.now().astimezone()
    _armar(tmp_path, monkeypatch, [], cargadas=["diaria", "rota"])
    recolectar.REGISTRO.write_text('{"tarea":"x"}\nbasura\n')
    md, n = recolectar.chequeo_tareas(ahora)
    assert "2 línea(s) ilegibles" in md


def test_memoria_cerca_del_techo_avisa(tmp_path, monkeypatch):
    (tmp_path / "MEMORY.md").write_text("x" * 23_000)
    monkeypatch.setattr(recolectar, "MEMORY_DIR", tmp_path)
    md, n = recolectar.chequeo_memoria()
    assert n == 1 and "hay que podar" in md
    (tmp_path / "MEMORY.md").write_text("x" * 100)
    assert recolectar.chequeo_memoria()[1] == 0
