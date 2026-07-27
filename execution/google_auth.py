#!/usr/bin/env python3
"""
Auth de Google compartida por todos los skills.

Primera vez (abre el navegador una sola vez):

    .venv/bin/python execution/google_auth.py --setup

Necesita `credentials.json` en la raíz del OS: se baja de Google Cloud Console
→ APIs y servicios → Credenciales → ID de cliente OAuth → tipo "App de escritorio".

OJO (esto ya nos mordió una vez): si la pantalla de consentimiento queda en
"Testing", el token se vence **cada 7 días** y hay que rehacer el login. Publicá
la consent screen a Producción y te ahorrás el dolor.

Desde un skill:

    from execution.google_auth import sheets, gmail, drive
    ws = sheets().spreadsheets().values().get(...)
"""

import argparse
import pathlib
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CREDENCIALES = RAIZ / "credentials.json"
TOKEN = RAIZ / "token.json"

# Lectura y escritura de Sheets, lectura de Drive, y enviar mails.
# No pedimos gmail.modify ni drive full: si un script se vuelve loco, que no
# pueda borrar nada.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def credenciales():
    """Devuelve credenciales válidas, refrescando o pidiendo login si hace falta."""
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN.write_text(creds.to_json())
            return creds
        except Exception as e:
            print(f"No pude refrescar el token ({e}). Rehaciendo el login.",
                  file=sys.stderr)

    if not CREDENCIALES.exists():
        sys.exit(
            f"Falta {CREDENCIALES}.\n"
            "Bajalo de Google Cloud Console → Credenciales → ID de cliente OAuth\n"
            "→ tipo 'App de escritorio', y guardalo con ese nombre en la raíz del OS."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENCIALES), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN.write_text(creds.to_json())
    print(f"Token guardado en {TOKEN}. No lo commitees (ya está en .gitignore).")
    return creds


def sheets():
    return build("sheets", "v4", credentials=credenciales())


def drive():
    return build("drive", "v3", credentials=credenciales())


def gmail():
    return build("gmail", "v1", credentials=credenciales())


def bajar_xlsx(file_id, destino):
    """Exporta un Google Sheet completo a .xlsx.

    Se usa el export y NO `files().get_media()` ni el conector de Drive: el
    conector TRUNCA las hojas largas sin avisar (206 de 455 filas, julio 2026).
    """
    destino = pathlib.Path(destino)
    contenido = drive().files().export(
        fileId=file_id,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ).execute()
    destino.write_bytes(contenido)
    return destino


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--setup", action="store_true",
                   help="Corre el flujo de login y guarda el token")
    args = p.parse_args()

    creds = credenciales()
    if args.setup or creds:
        perfil = gmail().users().getProfile(userId="me").execute()
        print(f"Autenticado como {perfil['emailAddress']}")
        print(f"Scopes: {', '.join(s.rsplit('/', 1)[-1] for s in SCOPES)}")


if __name__ == "__main__":
    main()
