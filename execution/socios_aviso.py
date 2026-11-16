"""Astronomy entre dos socios: publicar lo de Vlado sin pedir permiso, y un mail diario a los dos.

Facu, 13/11/2026: «no me molesta que Vlado pueda hacer algo y cambiarlo, simplemente quiero
saber qué: que a las 20 hs, si hay cambios, nos llegue un mail a los dos con los cambios que
se hicieron y de parte de quién, en vez de tener que pedir permisos».

Dos modos (los dispara launchd, ver execution/launchd/com.facu.socios-*.plist):

  · `--send` (cada 30 min, plist socios-aviso) → PUBLICAR la web:
      1. Completa la serie del dólar (`scripts/actualizar-blue.mjs --write`). Si entran días
         nuevos, commit «Auto FX: …». Antes se clavó dos veces (23/07 y 11/08) porque no había nada
         que la corriera.
      2. Si lo de arriba de `main` no es de Facu (Vlado subió algo), commit vacío de Facu
         «Auto publish: …». Vercel está en Hobby, que es de una sola persona: sólo deploya si el
         commit de arriba es de Facu (probado 13/11/2026, también por `vercel deploy`).
         Si lo de Vlado no compila, Vercel deja la web como estaba y el mail lo dice.
      Trabaja en un clon propio (data/web-publicar), nunca en la carpeta donde edita Facu.

  · `--resumen --send` (20:00, plist socios-resumen-vlado) → un MAIL a Facu y a Vlado con
      todo lo que cambió en los dos repos de Astronomy desde el último mail, separado por
      persona, y si la web quedó publicada. Si no hubo cambios, no sale nada.
      (`--resumen-vlado` es el nombre viejo del flag: el plist cargado lo usa.)

Sin `--send` muestra lo que haría y no toca nada. Estado: data/logs/socios_aviso.json. La
primera corrida sólo marca el punto de partida: no manda la historia entera.
"""
import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
ESTADO = RAIZ / "data/logs/socios_aviso.json"
CLON = RAIZ / "data/web-publicar"
NODE = pathlib.Path.home() / ".local/node/bin/node"

REPOS = {
    "astronomy-os": pathlib.Path("/Users/Facu/facu-os/active/astronomy"),
    "web": pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members"),
}
REMOTO_WEB = "git@github.com:facue1900-byte/astronomy-members.git"
FACU = re.compile(r"facue1900|^facu$", re.I)
VLADO = re.compile(r"vlad", re.I)
MAIL_VLADO = "vladinic@astronomyofficial.com"
# Commits que hace la máquina, no una persona: no van en el mail.
AUTOMATICOS = re.compile(r"^(Log:|Inbox:|Auto FX:|Auto publish:)")
# Si después de actualizar la serie del dólar el último día tiene más de esto, algo anda mal.
FX_VIEJA = timedelta(days=4)


def git(repo, *args, check=False):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=120)
    if check and r.returncode:
        raise SystemExit(f"git {' '.join(args)} falló: {r.stderr.strip()[:300]}")
    return r.stdout


def quien(nombre, mail):
    if VLADO.search(mail) or VLADO.search(nombre):
        return "Vlado"
    if FACU.search(mail) or FACU.search(nombre):
        return "Facu"
    return nombre


# ─────────────────────────────── publicar ───────────────────────────────

def publicar(send):
    if not CLON.exists():
        if not send:
            print(f"(sin --send) clonaría {REMOTO_WEB} en {CLON}")
            return
        subprocess.run(["git", "clone", "-q", REMOTO_WEB, str(CLON)], check=True, timeout=300)
        git(CLON, "config", "user.name", "Facu", check=True)
        git(CLON, "config", "user.email", "facue1900@gmail.com", check=True)
    git(CLON, "fetch", "-q", "origin", check=True)
    # Clon propio: se alinea a la fuerza con origin/main, no hay nada local que cuidar.
    git(CLON, "checkout", "-q", "-B", "main", "origin/main", check=True)
    git(CLON, "reset", "-q", "--hard", "origin/main", check=True)

    commits = []
    # 1. Dólar
    r = subprocess.run([str(NODE), "scripts/actualizar-blue.mjs", *(["--write"] if send else [])],
                       cwd=CLON, capture_output=True, text=True, timeout=120)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:300])
    serie = json.loads((CLON / "lib/fxBlue.json").read_text())
    ultimo = max(serie)
    if send and git(CLON, "status", "--porcelain", "--", "lib/fxBlue.json").strip():
        git(CLON, "commit", "-q", "-m", f"Auto FX: dollar series up to {ultimo}", "--", "lib/fxBlue.json", check=True)
        commits.append(f"dólar hasta {ultimo}")
    fx_vieja = date.today() - date.fromisoformat(ultimo) > FX_VIEJA

    # 2. Lo de Vlado
    arriba = git(CLON, "log", "-1", "--format=%an%x1f%ae%x1f%s", "origin/main").strip().split("\x1f")
    de_otro = quien(arriba[0], arriba[1]) != "Facu"
    if de_otro and not commits:
        msg = f"Auto publish: {quien(arriba[0], arriba[1])}'s changes ({arriba[2][:60]})"
        if send:
            git(CLON, "commit", "-q", "--allow-empty", "-m", msg, check=True)
        commits.append(msg)

    if not commits:
        print("web: nada para publicar.")
    elif not send:
        print("(sin --send) publicaría:", "; ".join(commits))
    else:
        p = subprocess.run(["git", "-C", str(CLON), "push", "-q", "origin", "HEAD:main"],
                           capture_output=True, text=True, timeout=120)
        if p.returncode:
            # Casi siempre: alguien subió algo en el medio. La próxima corrida lo agarra.
            print(f"push rechazado, se reintenta en la próxima corrida: {p.stderr.strip()[:200]}")
        else:
            print("publicado:", "; ".join(commits))
    if fx_vieja:
        raise SystemExit(f"⚠️ la serie del dólar llega sólo al {ultimo}: bluelytics no trae días nuevos.")


# ─────────────────────────────── resumen ────────────────────────────────

def novedades(clave, repo, visto):
    """Commits nuevos (todas las ramas remotas) que no son ancestros de lo ya visto."""
    git(repo, "fetch", "-q", "--all", "--prune")
    puntas = [l.strip() for l in git(repo, "for-each-ref", "--format=%(objectname)", "refs/remotes/origin").split() if l.strip()]
    if not puntas:
        raise SystemExit(f"{clave}: sin ramas remotas (¿falló el fetch?)")
    main = git(repo, "rev-parse", "origin/main").strip()
    vivos = [h for h in visto.get("tips", []) if git(repo, "cat-file", "-t", h).strip() == "commit"]
    if not vivos:
        # Primera vez, o los commits vistos ya no existen (force-push): no se manda la
        # historia entera, se marca el punto de partida.
        return puntas, main, None, []
    log = git(repo, "log", "--format=%H%x1f%an%x1f%ae%x1f%ad%x1f%s", "--date=format:%d/%m %H:%M",
              *puntas, *[f"^{h}" for h in vivos])
    commits = []
    for l in log.splitlines():
        h, an, ae, fecha, asunto = l.split("\x1f")
        if AUTOMATICOS.match(asunto):
            continue
        ramas = git(repo, "branch", "-r", "--contains", h).split()
        rama = "main" if "origin/main" in ramas else (ramas[0].replace("origin/", "") if ramas else "?")
        commits.append({"quien": quien(an, ae), "fecha": fecha, "asunto": asunto, "rama": rama,
                        "nuevos": [l.split("\t")[-1] for l in git(repo, "show", "--name-status", "--format=", h).splitlines() if l.startswith("A")]})
    bitacora = []
    base = visto.get("main")  # contra el main visto, no contra la punta de otra rama
    if base and git(repo, "cat-file", "-t", base).strip() == "commit" and (repo / "BITACORA.md").exists():
        diff = git(repo, "diff", base, "origin/main", "--", "BITACORA.md")
        bitacora = [m.group(1) for m in re.finditer(r"^\+(- .*)$", diff, re.M)]
    return puntas, main, commits, bitacora


def titulo_pedido(repo, archivo):
    txt = git(repo, "show", f"origin/main:{archivo}")
    m = re.search(r"^#\s+(.+)$", txt, re.M)
    return m.group(1).strip() if m else archivo


def de_persona(de, por_repo):
    """(pedidos, cambios, bitácora) de una persona, en puntos legibles."""
    pedidos, cambios, bitacora = [], [], []
    for clave, (repo, commits, lineas) in por_repo.items():
        for c in (c for c in commits if c["quien"] == de):
            for a in c["nuevos"]:  # sólo un PEDIDO_*.md NUEVO es un pedido; editarlo es un cambio
                if re.match(r"PEDIDO_.*\.md$", a):
                    p = f"{titulo_pedido(repo, a)} ({a})"
                    if p not in pedidos:
                        pedidos.append(p)
            donde = "web" if clave == "web" else "astronomy-os"
            rama = "" if c["rama"] == "main" else f" · rama {c['rama']}, sin publicar"
            cambios.append(f"{c['fecha']} · {donde}{rama} · {c['asunto']}")
        bitacora += [re.sub(r"^- \S+ \S+ · [^·]+ · ", "", l) for l in lineas if f"· {de} ·" in l]
    return pedidos, cambios, bitacora


def estado_web():
    """Cómo quedó producción, del último deploy de Vercel. None si no se pudo leer."""
    try:
        tok = json.load(open(pathlib.Path.home() / "Library/Application Support/com.vercel.cli/auth.json"))["token"]
        prj = json.load(open(REPOS["web"] / ".vercel/project.json"))
        url = (f"https://api.vercel.com/v6/deployments?teamId={prj['orgId']}&projectId={prj['projectId']}"
               "&target=production&limit=1")
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"}), timeout=30))["deployments"][0]
        return d["state"]
    except Exception as e:
        print(f"!!! no pude leer el estado de Vercel: {e!r}")
        return None


def resumen(send):
    from dotenv import load_dotenv
    load_dotenv(RAIZ / ".env")
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    vistos = estado.get("resumen", {})

    por_repo, nuevas, primera = {}, {}, False
    for clave, repo in REPOS.items():
        v = vistos.get(clave)
        puntas, main, commits, lineas = novedades(clave, repo, v if isinstance(v, dict) else {})
        nuevas[clave] = {"tips": puntas, "main": main}
        primera |= commits is None
        por_repo[clave] = (repo, commits or [], lineas)

    def guardar():
        estado["resumen"] = nuevas
        estado.pop("a_facu", None), estado.pop("a_vlado", None)  # formato del 13/11 a la mañana
        ESTADO.write_text(json.dumps(estado, indent=1))

    if primera:
        print("primera corrida: marco el punto de partida, no mando la historia.")
        if send:
            guardar()
        return

    secciones, total, quienes = [], 0, []
    for de in ("Vlado", "Facu"):
        pedidos, cambios, bitacora = de_persona(de, por_repo)
        if not (pedidos or cambios or bitacora):
            continue
        quienes.append(de)
        total += len(cambios)
        if pedidos:
            secciones.append((f"📌 {de} dejó un pedido", pedidos))
        if bitacora:
            secciones.append((f"{de} · lo que anotó", bitacora))
        if cambios:
            secciones.append((f"{de} · cambios ({len(cambios)})", cambios[:40]))
    if not secciones:
        print("nada nuevo hoy: no sale mail.")
        if send:
            guardar()
        return

    web = estado_web()
    nivel = "urgente" if web == "ERROR" else "reporte"
    resumen_txt = f"Hoy cambiaron cosas en Astronomy: {' y '.join(quienes)}. "
    resumen_txt += {"READY": "La web quedó publicada con todo.",
                    "ERROR": "OJO: el último deploy de la web FALLÓ; la web sigue con la versión anterior.",
                    "BUILDING": "La web se está publicando ahora.",
                    None: "No pude leer si la web quedó publicada."}.get(web, f"Estado de la web: {web}.")
    from execution.mail_format import render
    m = render("astronomy", nivel, f"Cambios de hoy · {' y '.join(quienes)}", resumen=resumen_txt,
               secciones=secciones, origen="facu-os/execution/socios_aviso.py")
    if not send:
        print(m.texto)
        return
    from execution.google_auth import gmail
    para = [os.environ["MAIL_FACU"], MAIL_VLADO]
    msg = m.mime(para)
    gmail().users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
    print(f"mail a {', '.join(para)}: {total} cambio(s) de {', '.join(quienes)}")
    guardar()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="hace de verdad (si no, sólo muestra)")
    ap.add_argument("--resumen", "--resumen-vlado", dest="resumen", action="store_true",
                    help="mail del día a los dos (si no: publicar la web)")
    a = ap.parse_args()
    print(f"=== {datetime.now():%d/%m %H:%M} · {'resumen' if a.resumen else 'publicar'} ===")
    resumen(a.send) if a.resumen else publicar(a.send)


if __name__ == "__main__":
    main()
