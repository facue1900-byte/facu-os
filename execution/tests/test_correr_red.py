"""correr.sh: la red se decide UNA vez. El 01/11 y el 02/11/2026 la primera consulta dio OK,
una segunda consulta justo después de despertar la Mac falló, y la tarea se perdió con un
"sin red después de 15 minutos" escrito a los 19 segundos."""
import json
import os
import stat
import subprocess
from pathlib import Path

ORIGINAL = Path(__file__).resolve().parents[1] / "launchd" / "correr.sh"
GUION = os.environ.get("CORRER_SH", str(ORIGINAL))


def stub(carpeta: Path, nombre: str, cuerpo: str) -> None:
    p = carpeta / nombre
    p.write_text(f"#!/bin/bash\n{cuerpo}\n")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)


def correr(tmp_path: Path, host: str) -> tuple[subprocess.CompletedProcess, list[dict], Path]:
    bin_ = tmp_path / "bin"
    bin_.mkdir()
    stub(bin_, "host", host)
    stub(bin_, "sleep", "exit 0")
    stub(bin_, "osascript", "exit 0")
    os_dir = tmp_path / "os"
    guion = tmp_path / "correr.sh"
    # Nunca contra el registro real: tareas.jsonl lo lee el radar.
    guion.write_text(Path(GUION).read_text().replace("OS=/Users/Facu/facu-os", f"OS={os_dir}"))
    marca = tmp_path / "corrio"
    env = {**os.environ, "PATH": f"{bin_}:{os.environ['PATH']}", "CUENTA": str(tmp_path / "cuenta")}
    r = subprocess.run(["/bin/bash", str(guion), "prueba", "--", f"touch {marca}"],
                       capture_output=True, text=True, env=env, timeout=60)
    reg = os_dir / "data" / "logs" / "tareas.jsonl"
    filas = [json.loads(l) for l in reg.read_text().splitlines()] if reg.exists() else []
    return r, filas, marca


# Contesta bien sólo la primera vez, como la Mac recién despierta.
SOLO_LA_PRIMERA = 'n=$(cat "$CUENTA" 2>/dev/null || echo 0); echo $((n+1)) > "$CUENTA"; [ "$n" -eq 0 ]'


def test_si_la_primera_consulta_anda_la_tarea_corre(tmp_path):
    r, filas, marca = correr(tmp_path, SOLO_LA_PRIMERA)
    assert r.returncode == 0, r.stdout + r.stderr
    assert marca.exists()
    assert filas[-1]["codigo"] == 0


def test_la_red_que_vuelve_a_mitad_de_la_espera_alcanza(tmp_path):
    r, filas, marca = correr(tmp_path, 'n=$(cat "$CUENTA" 2>/dev/null || echo 0); echo $((n+1)) > "$CUENTA"; [ "$n" -ge 3 ]')
    assert r.returncode == 0
    assert marca.exists()
    assert "espero hasta 15 minutos" in r.stdout


def test_sin_red_de_verdad_no_corre_y_queda_registrado(tmp_path):
    r, filas, marca = correr(tmp_path, "exit 1")
    assert r.returncode == 75
    assert not marca.exists()
    assert filas[-1]["codigo"] == 75
    assert "no corrió" in r.stdout
