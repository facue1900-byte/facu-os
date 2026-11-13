"""Que Facu y Vlado se enteren de lo que hace el otro en Astronomy, sin tener que abrir Claude.

Nació el 13/11/2026: el pedido del tablero de Vlado le llegó a Facu por captura de WhatsApp, y
del pedido del 12/11 quedaron 6 puntos sin que Facu supiera. El hook `al_abrir.sh` de
astronomy-os sólo muestra lo del socio cuando uno abre Claude; esto lo empuja.

Mira los dos repos de Astronomy (astronomy-os y la web astronomy-members), todas las ramas:

  · Lo de VLADO  → Telegram a Facu (bot Jarvis), en cada corrida que haya algo nuevo.
  · Lo de FACU   → un mail a Vlado por día (`--resumen-vlado`), sólo si Facu hizo algo.

"Algo" = commits con autor del otro (sin los automáticos «Log:» e «Inbox:»), pedidos nuevos
o cambiados (`PEDIDO_*.md`) y líneas nuevas de `BITACORA.md`.

Regla 10: el Telegram es a Facu (no sale al mundo). El mail a Vlado lo pidió Facu el
13/11/2026 («si Vlado pide algo, que me lo avises, y viceversa»); igual sólo sale con `--send`.

    .venv/bin/python execution/socios_aviso.py                    # mira y muestra, no manda
    .venv/bin/python execution/socios_aviso.py --send             # Telegram a Facu
    .venv/bin/python execution/socios_aviso.py --resumen-vlado --send   # mail del día a Vlado

El estado (hasta qué commit ya se avisó) vive en data/logs/socios_aviso.json. La primera
corrida sólo marca el punto de partida: no avisa la historia entera.
"""
import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
ESTADO = RAIZ / "data/logs/socios_aviso.json"

REPOS = {
    "astronomy-os": pathlib.Path("/Users/Facu/facu-os/active/astronomy"),
    "web": pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members"),
}
GITHUB = {"astronomy-os": "facue1900-byte/astronomy-os", "web": "facue1900-byte/astronomy-members"}
# Quién es quién, por mail o nombre del autor del commit.
FACU = re.compile(r"facue1900|^facu$", re.I)
VLADO = re.compile(r"vlad", re.I)
MAIL_VLADO = "vladinic@astronomyofficial.com"
AUTOMATICOS = re.compile(r"^(Log:|Inbox:)")


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60).stdout


def quien(nombre, mail):
    if VLADO.search(mail) or VLADO.search(nombre):
        return "Vlado"
    if FACU.search(mail) or FACU.search(nombre):
        return "Facu"
    return nombre


def novedades(clave, repo, visto):
    """Commits nuevos (todas las ramas remotas) que no son ancestros de lo ya visto."""
    git(repo, "fetch", "-q", "--all", "--prune")
    puntas = [l.strip() for l in git(repo, "for-each-ref", "--format=%(objectname)", "refs/remotes/origin").split() if l.strip()]
    if not puntas:
        raise SystemExit(f"{clave}: sin ramas remotas (¿falló el fetch?)")
    vivos = [h for h in visto.get("tips", []) if git(repo, "cat-file", "-t", h).strip() == "commit"]
    if not vivos:
        # Primera vez, o los commits vistos ya no existen (force-push): no se manda la
        # historia entera, se marca el punto de partida.
        return puntas, git(repo, "rev-parse", "origin/main").strip(), None, []
    excl = [f"^{h}" for h in vivos]
    log = git(repo, "log", "--format=%H%x1f%an%x1f%ae%x1f%ad%x1f%s", "--date=format:%d/%m %H:%M", *puntas, *excl)
    commits = []
    for l in log.splitlines():
        h, an, ae, fecha, asunto = l.split("\x1f")
        if AUTOMATICOS.match(asunto):
            continue
        ramas = git(repo, "branch", "-r", "--contains", h).split()
        rama = "main" if "origin/main" in ramas else (ramas[0].replace("origin/", "") if ramas else "?")
        archivos = git(repo, "show", "--name-only", "--format=", h).split()
        commits.append({"h": h[:7], "quien": quien(an, ae), "fecha": fecha, "asunto": asunto,
                        "rama": rama, "archivos": archivos})
    # Líneas nuevas de la bitácora en main (sólo astronomy-os la tiene).
    bitacora = []
    # Contra el main visto, no contra la punta de otra rama.
    base = visto.get("main")
    if base and git(repo, "cat-file", "-t", base).strip() == "commit" and (repo / "BITACORA.md").exists():
        diff = git(repo, "diff", base, "origin/main", "--", "BITACORA.md")
        bitacora = [m.group(1) for m in re.finditer(r"^\+(- .*)$", diff, re.M)]
    return puntas, git(repo, "rev-parse", "origin/main").strip(), commits, bitacora


def titulo_pedido(repo, archivo):
    try:
        txt = git(repo, "show", f"origin/main:{archivo}") or (repo / archivo).read_text()
    except Exception:
        return archivo
    m = re.search(r"^#\s+(.+)$", txt, re.M)
    return m.group(1).strip() if m else archivo


def armar(de, por_repo):
    """Junta lo de una persona en puntos legibles. Devuelve (pedidos, cambios, bitacora)."""
    pedidos, cambios, bitacora = [], [], []
    for clave, (repo, commits, lineas) in por_repo.items():
        suyos = [c for c in commits if c["quien"] == de]
        for c in suyos:
            for a in c["archivos"]:
                if re.match(r"PEDIDO_.*\.md$", a):
                    p = f"{titulo_pedido(repo, a)} → {clave}/{a}"
                    if p not in pedidos:
                        pedidos.append(p)
            donde = "la web" if clave == "web" else "astronomy-os"
            rama = "" if c["rama"] == "main" else f" (rama {c['rama']}, sin publicar)"
            cambios.append(f"{c['fecha']} · {donde}{rama}: {c['asunto']}")
        bitacora += [l for l in lineas if f"· {de} ·" in l]
    return pedidos, cambios, bitacora


def prs_abiertos(de):
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not tok:
        return []
    out = []
    for clave, slug in GITHUB.items():
        req = urllib.request.Request(f"https://api.github.com/repos/{slug}/pulls?state=open",
                                     headers={"Authorization": f"Bearer {tok}", "User-Agent": "facu-os"})
        try:
            for p in json.load(urllib.request.urlopen(req, timeout=30)):
                if bool(VLADO.search(p["user"]["login"])) == (de == "Vlado"):
                    out.append(f"#{p['number']} {p['title']} → {p['html_url']}")
        except Exception as e:
            print(f"!!! no pude leer los PR de {slug}: {e!r}")
    return out


def telegram(texto):
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        raise SystemExit("faltan TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID en el .env")
    datos = urllib.parse.urlencode({"chat_id": chat, "text": texto[:4000], "disable_web_page_preview": "true"}).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data=datos, timeout=30) as r:
        if not json.load(r).get("ok"):
            raise SystemExit("Telegram no aceptó el mensaje")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="manda de verdad (si no, sólo muestra)")
    ap.add_argument("--resumen-vlado", action="store_true", help="mail del día a Vlado con lo de Facu")
    a = ap.parse_args()

    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")

    canal = "a_vlado" if a.resumen_vlado else "a_facu"
    de = "Facu" if a.resumen_vlado else "Vlado"
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    vistos = estado.get(canal, {})

    por_repo, puntas_nuevas, primera = {}, {}, False
    for clave, repo in REPOS.items():
        visto = vistos.get(clave)
        puntas, main, commits, lineas = novedades(clave, repo, visto if isinstance(visto, dict) else {})
        puntas_nuevas[clave] = {"tips": puntas, "main": main}
        if commits is None:
            primera = True
        por_repo[clave] = (repo, commits or [], lineas)

    pedidos, cambios, bitacora = armar(de, por_repo)
    prs = prs_abiertos(de)
    hay = bool(pedidos or cambios or bitacora)

    def guardar():
        estado[canal] = puntas_nuevas
        ESTADO.parent.mkdir(parents=True, exist_ok=True)
        ESTADO.write_text(json.dumps(estado, indent=1))

    if primera:
        print(f"[{canal}] primera corrida: marco el punto de partida, no aviso la historia.")
        if a.send:
            guardar()
        return
    if not hay:
        print(f"[{canal}] nada nuevo de {de}.")
        if a.send:
            guardar()
        return

    if a.resumen_vlado:
        from execution.mail_format import render
        secciones = []
        if pedidos:
            secciones.append(("Pedidos nuevos o cambiados", pedidos))
        if bitacora:
            secciones.append(("Lo que anotó en la bitácora", [re.sub(r"^- ", "", l) for l in bitacora]))
        secciones.append(("Cambios (commits)", cambios[:40]))
        if prs:
            secciones.append(("PR abiertos de Facu", prs))
        m = render("astronomy", "reporte", "Lo que hizo Facu hoy",
                   resumen=f"{len(cambios)} cambio(s) de Facu en Astronomy desde el último resumen. "
                           "Si algo choca con lo que estás armando, avisale antes de seguir.",
                   secciones=secciones, origen="socios_aviso.py")
        if not a.send:
            print(m.texto)
            return
        from execution.google_auth import gmail
        msg = m.mime(MAIL_VLADO)
        gmail().users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
        print(f"mail mandado a {MAIL_VLADO}: {len(cambios)} cambio(s)")
    else:
        partes = ["🤝 Astronomy: Vlado hizo cosas"]
        if pedidos:
            partes.append("📌 PEDIDO PARA VOS:\n" + "\n".join("· " + p for p in pedidos))
        if bitacora:
            partes.append("Bitácora:\n" + "\n".join("· " + re.sub(r"^- \S+ \S+ · Vlado · ", "", l) for l in bitacora))
        if cambios:
            partes.append("Cambios:\n" + "\n".join("· " + c for c in cambios[:15])
                          + (f"\n… y {len(cambios) - 15} más" if len(cambios) > 15 else ""))
        if prs:
            partes.append("PR de Vlado esperando:\n" + "\n".join("· " + p for p in prs))
        partes.append("Decime acá «¿qué pidió Vlado?» y lo miro.")
        texto = "\n\n".join(partes)
        if not a.send:
            print(texto)
            return
        telegram(texto)
        print(f"Telegram a Facu: {len(cambios)} cambio(s), {len(pedidos)} pedido(s)")
    guardar()


if __name__ == "__main__":
    main()
