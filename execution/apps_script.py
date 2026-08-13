#!/usr/bin/env python3
"""Editar y publicar Apps Script sin abrir el navegador.

Los scripts que pegan datos en las planillas (el sync de la app del Paseo, el
endpoint de Inversores) viven **ligados a su planilla**, y hasta ahora la única
forma de actualizarlos era: abrir la planilla → Extensiones → Apps Script →
pegar → Implementar → Nueva versión. Un paso manual en el medio de un deploy
automático es un paso que se olvida — y cuando se olvida, el sync sigue
corriendo el código viejo sin avisar.

    apps_script.py --setup                     autoriza (una vez, abre el navegador)
    apps_script.py --ver <scriptId>            baja el código actual
    apps_script.py --push <scriptId> <archivo> sube, versiona y publica
    apps_script.py --deployments <scriptId>    qué está publicado hoy

**El token es aparte** (`token-appsscript.json`): agregar estos scopes al token
principal lo invalidaría y dejaría sin Sheets a todo lo demás hasta re-autorizar.

Requisito de una sola vez, del lado de Facu: activar «Google Apps Script API» en
https://script.google.com/home/usersettings — sin eso la API contesta 403 aunque
los scopes estén bien.
"""
import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

RAIZ = Path("/Users/Facu/facu-os")
CREDENCIALES = RAIZ / "credentials.json"
TOKEN = RAIZ / "token-appsscript.json"
SCOPES = [
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/script.deployments",
]


def credenciales():
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not sys.stdin.isatty():
            sys.exit("Falta autorizar: corré  apps_script.py --setup  desde una terminal.")
        creds = InstalledAppFlow.from_client_secrets_file(
            str(CREDENCIALES), SCOPES).run_local_server(port=0)
    TOKEN.write_text(creds.to_json())
    TOKEN.chmod(0o600)
    return creds


def api():
    return build("script", "v1", credentials=credenciales(), cache_discovery=False)


def contenido(script_id):
    return api().projects().getContent(scriptId=script_id).execute()


def push(script_id, archivo, nombre=None, descripcion="actualizado desde facu-os"):
    """Reemplaza UN archivo del proyecto, crea versión y la publica.

    No toca los demás archivos ni el `appsscript.json`: se baja el proyecto
    entero, se cambia sólo el que corresponde y se sube completo, que es como
    pide la API (un PUT del proyecto, no un PATCH de un archivo).
    """
    sv = api()
    proyecto = sv.projects().getContent(scriptId=script_id).execute()
    fuente = Path(archivo).read_text(encoding="utf-8")
    nombre = nombre or Path(archivo).stem

    archivos = proyecto["files"]
    destino = next((f for f in archivos if f["name"] == nombre and f["type"] == "SERVER_JS"), None)
    if destino is None:
        # si no existe con ese nombre y hay UN solo .gs, es ése; si hay varios,
        # no adivinamos cuál pisar
        candidatos = [f for f in archivos if f["type"] == "SERVER_JS"]
        if len(candidatos) != 1:
            sys.exit(f"No sé cuál pisar: el proyecto tiene {len(candidatos)} archivos .gs "
                     f"({', '.join(f['name'] for f in candidatos)}). Pasá --nombre.")
        destino = candidatos[0]
    previo = destino["source"]
    if previo == fuente:
        print(f"  el código ya está igual en «{destino['name']}» — no subo nada")
    else:
        destino["source"] = fuente
        sv.projects().updateContent(scriptId=script_id, body={"files": archivos}).execute()
        print(f"  subido a «{destino['name']}»  ({len(previo)} → {len(fuente)} caracteres)")

    version = sv.projects().versions().create(
        scriptId=script_id, body={"description": descripcion}).execute()["versionNumber"]
    print(f"  versión {version} creada")

    # Publicar = apuntar los deployments existentes a la versión nueva. Crear uno
    # nuevo daría otra URL /exec y la app seguiría llamando a la vieja.
    deploys = sv.projects().deployments().list(scriptId=script_id).execute().get("deployments", [])
    publicados = 0
    for d in deploys:
        cfg = d.get("deploymentConfig", {})
        if not d.get("deploymentId") or d["deploymentId"] == "HEAD":
            continue
        sv.projects().deployments().update(
            scriptId=script_id, deploymentId=d["deploymentId"],
            body={"deploymentConfig": {
                "scriptId": script_id, "versionNumber": version,
                "manifestFileName": cfg.get("manifestFileName", "appsscript"),
                "description": cfg.get("description", descripcion)}}).execute()
        publicados += 1
        print(f"  deployment {d['deploymentId'][:24]}… → versión {version}")
    if not publicados:
        print("  ⚠ no había ningún deployment publicado: la URL /exec no existe todavía")
    return version


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--setup":
        credenciales()
        print(f"OK — autorizado. Token en {TOKEN}")
        return
    if args[0] == "--ver":
        c = contenido(args[1])
        for f in c["files"]:
            print(f"=== {f['name']}.{ {'SERVER_JS': 'gs', 'JSON': 'json', 'HTML': 'html'}.get(f['type'], '?') } "
                  f"({len(f['source'])} caracteres) ===")
            if "--full" in args:
                print(f["source"])
        return
    if args[0] == "--deployments":
        for d in api().projects().deployments().list(
                scriptId=args[1]).execute().get("deployments", []):
            cfg = d.get("deploymentConfig", {})
            print(f"  {d['deploymentId']}  versión {cfg.get('versionNumber', 'HEAD')}  "
                  f"{cfg.get('description', '')}")
            for e in d.get("entryPoints", []):
                url = (e.get("webApp") or {}).get("url")
                if url:
                    print(f"      {url}")
        return
    if args[0] == "--push":
        nombre = args[args.index("--nombre") + 1] if "--nombre" in args else None
        push(args[1], args[2], nombre)
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
