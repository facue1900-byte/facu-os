"""Radar diario — barre repos, sesiones de Claude, memoria, ESTADOs, vault y tareas
programadas, y deja un digest en Markdown para que el agente lo sintetice.

Determinista y de solo lectura: no escribe en ningún repo ni base. El agente
(`radar_diario.sh`) lee el digest y actualiza el doc "Radar Facu".

    .venv/bin/python execution/radar/recolectar.py [--horas 26] [--out data/radar/digest.md]

Sale con código 2 si una fuente que siempre tiene que tener algo vino vacía
(Constitución, regla 2): sin repos, sin carpeta de transcripts, sin MEMORY.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

HOME = Path.home()
OS_DIR = HOME / "facu-os"
PROJECTS = HOME / ".claude" / "projects"
MEMORY_DIR = PROJECTS / "-Users-Facu-facu-os" / "memory"
VAULT = HOME / "Obsidian" / "facu-vault"
LOGS = OS_DIR / "data" / "logs"

# Dónde se buscan repos. "Formación" es material del curso: ruido, no trabajo.
RAIZ_REPOS = [OS_DIR, HOME / "Desktop"]
REPOS_EXCLUIDOS = ("Formación",)
# Carpetas con archivos sueltos que importan (data cruda de los negocios).
RAIZ_ARCHIVOS = [HOME / "Desktop", HOME / "Downloads"]
SALTEAR_DIRS = {".git", "node_modules", ".next", "dist", "build", ".venv", "__pycache__", ".vercel", ".netlify"}

MAX_USER_MSGS = 12
MAX_CHARS_MSG = 400
MAX_CHARS_FINAL = 900
MAX_CHARS_ESTADO = 7000
MAX_ARCHIVOS = 60


def sh(cmd: list[str], cwd: Path | None = None) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
        return r.stdout.strip()
    except Exception as e:  # noqa: BLE001 — se reporta en el digest, no se traga
        return f"[error: {e}]"


def recortar(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def encontrar_repos() -> list[Path]:
    repos = []
    for raiz in RAIZ_REPOS:
        for dirpath, dirnames, _ in os.walk(raiz):
            if any(x in unicodedata.normalize("NFC", dirpath) for x in REPOS_EXCLUIDOS):
                dirnames[:] = []
                continue
            if ".git" in dirnames:
                repos.append(Path(dirpath))
            dirnames[:] = [d for d in dirnames if d not in SALTEAR_DIRS and not d.startswith(".")]
            if dirpath.count(os.sep) - str(raiz).count(os.sep) >= 6:
                dirnames[:] = []
    return sorted(set(repos))


def seccion_repos(desde: datetime) -> tuple[str, int]:
    repos = encontrar_repos()
    out = [f"## Repos ({len(repos)})\n"]
    for r in repos:
        nombre = str(r).replace(str(HOME), "~")
        rama = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], r)
        log = sh(["git", "log", f"--since={desde.isoformat()}", "--date=format:%d/%m %H:%M",
                  "--pretty=%ad %h %s"], r)
        sucio = sh(["git", "status", "--porcelain"], r)
        n_sucio = len([l for l in sucio.splitlines() if l.strip()])
        sin_push = sh(["git", "rev-list", "--count", "@{u}..HEAD"], r)
        if not sin_push.isdigit():
            sin_push = "sin remoto"
        commits = [l for l in log.splitlines() if l.strip()]
        out.append(f"### {nombre} (rama {rama}) — {len(commits)} commits · {n_sucio} archivos sin commitear · sin pushear: {sin_push}")
        out += [f"- {c}" for c in commits] or ["- (sin commits en la ventana)"]
        out.append("")
    return "\n".join(out), len(repos)


def texto_de(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def es_ruido(t: str) -> bool:
    t = t.strip()
    return (not t or t.startswith("<") or t.startswith("[Request interrupted")
            or t.startswith("[Image") or t.startswith("Another Claude session sent")
            or "<system-reminder>" in t[:200] or "<command-" in t[:200])


def seccion_sesiones(desde: datetime) -> tuple[str, int, int]:
    if not PROJECTS.is_dir():
        return "## Sesiones de Claude\n\n**FALTA la carpeta de transcripts.**\n", -1, 0
    corte = desde.timestamp()
    out, n, n_auto = [], 0, 0
    for jl in sorted(PROJECTS.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime):
        if jl.stat().st_mtime < corte:
            continue
        users, final, inicio, fin, cwd, auto = [], "", None, None, "", False
        with jl.open(errors="replace") as f:
            for linea in f:
                try:
                    d = json.loads(linea)
                except json.JSONDecodeError:
                    continue
                ts = d.get("timestamp")
                if d.get("entrypoint") == "sdk-cli" or d.get("promptSource") == "sdk":
                    auto = True
                if d.get("isSidechain"):
                    continue
                if ts:
                    inicio = inicio or ts
                    fin = ts
                cwd = d.get("cwd") or cwd
                msg = d.get("message")
                if not isinstance(msg, dict):
                    continue
                t = texto_de(msg.get("content"))
                if d.get("type") == "user" and not es_ruido(t) and not d.get("toolUseResult"):
                    users.append(recortar(t, MAX_CHARS_MSG))
                elif d.get("type") == "assistant" and t.strip():
                    final = t
        if auto:  # corridas headless (incluido este mismo radar): no son trabajo de Facu
            n_auto += 1
            continue
        if not users:
            continue
        n += 1
        lugar = cwd.replace(str(HOME), "~") or jl.parent.name
        out.append(f"### Sesión {jl.stem[:8]} — {lugar} — {(inicio or '')[:16]} → {(fin or '')[:16]} UTC")
        sel = users if len(users) <= MAX_USER_MSGS else users[:4] + ["(…)"] + users[-(MAX_USER_MSGS - 4):]
        out += [f"- Facu: {u}" for u in sel]
        out.append(f"- Último mensaje de Claude: {recortar(final, MAX_CHARS_FINAL)}")
        out.append("")
    cab = f"## Sesiones de Claude Code ({n} con actividad de Facu; {n_auto} headless salteadas)\n"
    return cab + "\n" + "\n".join(out), n, n_auto


def seccion_memoria(desde: datetime) -> tuple[str, bool]:
    idx = MEMORY_DIR / "MEMORY.md"
    if not idx.exists():
        return "## Memoria\n\n**FALTA MEMORY.md.**\n", False
    out = ["## Memoria — índice completo (MEMORY.md)\n", idx.read_text(errors="replace"), ""]
    tocadas = [p for p in MEMORY_DIR.glob("*.md")
               if p.name != "MEMORY.md" and p.stat().st_mtime >= desde.timestamp()]
    out.append(f"## Memorias escritas o tocadas en la ventana ({len(tocadas)})\n")
    for p in sorted(tocadas, key=lambda p: -p.stat().st_mtime):
        cuerpo = p.read_text(errors="replace")
        out.append(f"### {p.name}\n{cuerpo[:2500]}\n")
    return "\n".join(out), True


def seccion_estados() -> str:
    out = ["## ESTADO.md por frente (active/)\n"]
    for p in sorted((OS_DIR / "active").glob("*/ESTADO.md")):
        mt = datetime.fromtimestamp(p.stat().st_mtime).strftime("%d/%m/%Y")
        txt = p.read_text(errors="replace")
        corte = "" if len(txt) <= MAX_CHARS_ESTADO else f"\n[… recortado, {len(txt)} chars en total]"
        out.append(f"### {p.parent.name} (modificado {mt})\n{txt[:MAX_CHARS_ESTADO]}{corte}\n")
    return "\n".join(out)


def archivos_modificados(raiz: Path, desde: datetime) -> list[tuple[float, Path]]:
    res = []
    for dirpath, dirnames, filenames in os.walk(raiz):
        dirnames[:] = [d for d in dirnames if d not in SALTEAR_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.startswith("."):
                continue
            p = Path(dirpath) / fn
            try:
                mt = p.stat().st_mtime
            except OSError:
                continue
            if mt >= desde.timestamp():
                res.append((mt, p))
    return sorted(res, reverse=True)


def seccion_archivos(desde: datetime) -> str:
    out = ["## Archivos nuevos o tocados (fuera de los repos)\n"]
    for raiz in RAIZ_ARCHIVOS + [VAULT]:
        if not raiz.exists():
            out.append(f"### {raiz} — **no existe**\n")
            continue
        fs = archivos_modificados(raiz, desde)
        out.append(f"### {str(raiz).replace(str(HOME), '~')} — {len(fs)} archivos")
        for mt, p in fs[:MAX_ARCHIVOS]:
            rel = str(p.relative_to(raiz))
            out.append(f"- {datetime.fromtimestamp(mt).strftime('%d/%m %H:%M')} {rel}")
        if len(fs) > MAX_ARCHIVOS:
            out.append(f"- (… y {len(fs) - MAX_ARCHIVOS} más)")
        out.append("")
    return "\n".join(out)


AGENTS = HOME / "Library" / "LaunchAgents"
REPO_PLISTS = OS_DIR / "execution" / "launchd"
REGISTRO = LOGS / "tareas.jsonl"
# Cuánto puede tardar una corrida en quedar registrada después de su hora: espera de red
# (15 min) + la tarea + la Mac dormida que la dispara al despertar.
GRACIA = timedelta(hours=12)


def _ultima_hora_esperada(intervalos: list[dict], ahora: datetime) -> datetime | None:
    """La última vez que launchd TENDRÍA que haber disparado, según StartCalendarInterval."""
    mejor = None
    for d in range(0, 40):
        dia = (ahora - timedelta(days=d)).date()
        for it in intervalos:
            if "Day" in it and dia.day != it["Day"]:
                continue
            if "Month" in it and dia.month != it["Month"]:
                continue
            if "Weekday" in it and (dia.weekday() + 1) % 7 != it["Weekday"] % 7:
                continue
            horas = [it["Hour"]] if "Hour" in it else range(24)
            for h in horas:
                t = datetime(dia.year, dia.month, dia.day, h, it.get("Minute", 0)).astimezone()
                if t <= ahora and (mejor is None or t > mejor):
                    mejor = t
        if mejor:
            return mejor
    return mejor


def chequeo_tareas(ahora: datetime) -> tuple[str, int]:
    """Qué tarea programada falló o no corrió. Determinista: el agente lo copia, no lo interpreta."""
    registros: dict[str, dict] = {}
    desde_registro = None
    invalidas = 0
    if REGISTRO.is_file():
        for linea in REGISTRO.read_text().splitlines():
            if not linea.strip():
                continue
            try:
                r = json.loads(linea)
                ini = datetime.strptime(r["inicio"], "%Y-%m-%dT%H:%M:%S%z")
                r["_ini"] = ini
                registros[r["tarea"]] = r  # queda la última
            except (json.JSONDecodeError, KeyError, ValueError, TypeError):
                invalidas += 1
                continue
            desde_registro = desde_registro or ini
    cargadas = sh(["bash", "-c", "launchctl list | grep com.facu || true"])
    codigos = {l.split()[-1]: l.split()[1] for l in cargadas.splitlines() if l.strip()}

    problemas, ok = [], []
    if invalidas:
        problemas.append(f"- **{REGISTRO.name}: {invalidas} línea(s) ilegibles**: esas corridas no se pueden verificar.")
    nombres = sorted({p.name for p in AGENTS.glob("com.facu.*.plist")} | {p.name for p in REPO_PLISTS.glob("com.facu.*.plist")})
    for archivo in nombres:
        label = archivo[:-len(".plist")]
        tarea = label[len("com.facu."):]
        instalado = AGENTS / archivo
        if not instalado.is_file() or label not in codigos:
            problemas.append(f"- **{tarea}: NO ESTÁ CARGADA** en launchd: nunca va a correr.")
            continue
        # Con plutil, como launchd: plistlib rechaza un "--" adentro de un comentario
        # (reporte-pauta lo tiene) y eso tiraba abajo el radar entero.
        try:
            pl = json.loads(sh(["plutil", "-convert", "json", "-o", "-", str(instalado)]))
        except json.JSONDecodeError:
            problemas.append(f"- **{tarea}: no pude leer su plist** ({instalado}).")
            continue
        envuelta = "correr.sh" in " ".join(pl.get("ProgramArguments", []))
        sci = pl.get("StartCalendarInterval")
        # Se juzga la última hora que YA venció su gracia: una diaria de las 07:30 se
        # juzga con la de ayer cuando el radar corre a las 07:30 de hoy.
        esperada = _ultima_hora_esperada(sci if isinstance(sci, list) else [sci], ahora - GRACIA) if sci else None
        # Piso: no se le reclama una corrida anterior al registro ni a su instalación.
        piso = max(filter(None, [desde_registro, datetime.fromtimestamp(instalado.stat().st_mtime).astimezone()]))
        r = registros.get(tarea)
        if not envuelta:
            cod = codigos.get(label, "?")
            linea = f"- {tarea}: no pasa por correr.sh (sin registro); último código de launchd {cod}."
            (problemas if cod not in ("0", "-") else ok).append(linea)
            continue
        if r and r["codigo"] != 0:
            problemas.append(f"- **{tarea}: FALLÓ** el {r['_ini']:%d/%m %H:%M} (código {r['codigo']}).")
        elif esperada is None:
            problemas.append(f"- **{tarea}: sin horario calculable** (no StartCalendarInterval o fuera de 40 días): no se puede verificar.")
        elif esperada > piso and (r is None or r["_ini"] < esperada):
            problemas.append(f"- **{tarea}: NO CORRIÓ** — le tocaba el {esperada:%d/%m %H:%M} y no hay registro.")
        elif r:
            ok.append(f"- {tarea}: OK, última {r['_ini']:%d/%m %H:%M}.")
        else:
            ok.append(f"- {tarea}: todavía sin corridas registradas.")

    out = ["## ⚠ Tareas programadas que fallaron o no corrieron\n",
           "Calculado por recolectar.py contra data/logs/tareas.jsonl. Copiar tal cual al tope del radar.\n"]
    out += problemas or ["- Ninguna: todas corrieron bien la última vez que les tocaba."]
    out += ["", "Al día:"] + ok + [""]
    return "\n".join(out), len(problemas)


def seccion_tareas() -> str:
    out = ["## Tareas programadas (launchd)\n", "Formato: PID · último código de salida · label (0 = OK)\n"]
    out.append("```\n" + sh(["bash", "-c", "launchctl list | grep com.facu || echo '(ninguna cargada)'"]) + "\n```\n")
    if LOGS.is_dir():
        for log in sorted(LOGS.glob("*")):
            mt = datetime.fromtimestamp(log.stat().st_mtime).strftime("%d/%m %H:%M")
            cola = sh(["tail", "-n", "6", str(log)])
            out.append(f"### {log.name} (última escritura {mt})\n```\n{cola[-1200:]}\n```\n")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--horas", type=int, default=26)
    ap.add_argument("--out", default=str(OS_DIR / "data" / "radar" / "digest.md"))
    a = ap.parse_args()

    ahora = datetime.now().astimezone()
    desde = ahora - timedelta(hours=a.horas)

    repos_md, n_repos = seccion_repos(desde)
    ses_md, n_ses, n_auto = seccion_sesiones(desde)
    mem_md, mem_ok = seccion_memoria(desde)
    tareas_md, n_tareas_mal = chequeo_tareas(ahora)

    partes = [
        f"# Digest del radar — {ahora.strftime('%d/%m/%Y %H:%M')} (ventana: últimas {a.horas} h, desde {desde.strftime('%d/%m %H:%M')})\n",
        "## Cobertura\n",
        f"- Repos encontrados: {n_repos}",
        f"- Sesiones de Claude Code con actividad: {n_ses} (headless salteadas: {n_auto})",
        f"- MEMORY.md leído: {'sí' if mem_ok else 'NO'}",
        "- NO cubre: chats de claude.ai web/app (no quedan en disco), WhatsApp, Gmail, bases de Supabase.\n",
        tareas_md,
        repos_md, ses_md, seccion_estados(), mem_md, seccion_archivos(desde), seccion_tareas(),
    ]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(partes))
    print(f"digest: {out} · {out.stat().st_size // 1024} KB · repos {n_repos} · sesiones {n_ses} · tareas con problema {n_tareas_mal}")

    fallas = []
    if n_repos == 0:
        fallas.append("0 repos")
    if n_ses < 0:
        fallas.append("sin carpeta de transcripts")
    if not mem_ok:
        fallas.append("sin MEMORY.md")
    if fallas:
        print("FALLA: " + ", ".join(fallas), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
