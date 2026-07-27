#!/usr/bin/env python3
"""
Auth de Google compartida por todos los skills.

Primera vez (abre el navegador una sola vez por cuenta):

    .venv/bin/python execution/google_auth.py --setup                  # cuenta "facu"
    .venv/bin/python execution/google_auth.py --setup --cuenta studio  # otra cuenta
    .venv/bin/python execution/google_auth.py --listar                 # qué hay autorizado

Necesita `credentials.json` en la raíz del OS: se baja de Google Cloud Console
→ APIs y servicios → Credenciales → ID de cliente OAuth → tipo "App de escritorio".

**Un solo `credentials.json` alcanza para todas las cuentas.** Ese archivo
identifica a la *aplicación*, no a la persona: en el navegador elegís con qué
cuenta autorizás. Cada cuenta guarda su propio `token-<cuenta>.json`, así que
podés tener a la vez la personal (que ve tu Gmail) y la de la empresa (que es
dueña de los sheets que desde la personal solo se leen).

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

# Una cuenta = un token. El `credentials.json` es UNO SOLO y es de la *app*, no
# de la persona: identifica al cliente OAuth, no a quién autoriza. Tener dos
# clientes OAuth no sirve de nada; tener dos cuentas sí, porque hay sheets que
# son de studio@/it@ y desde facue1900 solo se leen.
CUENTA_DEFAULT = "facu"


def token_de(cuenta=CUENTA_DEFAULT):
    return RAIZ / f"token-{cuenta}.json"

# Lectura y escritura de Sheets, lectura de Drive, y enviar mails.
# No pedimos gmail.modify ni drive full: si un script se vuelve loco, que no
# pueda borrar nada.
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def credenciales(cuenta=CUENTA_DEFAULT, interactivo=None):
    """Devuelve credenciales válidas de `cuenta`, refrescando o pidiendo login.

    `interactivo` se autodetecta: si no hay terminal (launchd, cron), NO abre el
    navegador — corta con un mensaje. Un `run_local_server()` disparado desde
    launchd no falla: se queda esperando un click que nunca llega, con el proceso
    colgado y el log vacío. Pasar True/False fuerza el comportamiento.
    """
    if interactivo is None:
        interactivo = sys.stdin.isatty() and sys.stdout.isatty()
    token = token_de(cuenta)
    creds = None
    if token.exists():
        creds = Credentials.from_authorized_user_file(str(token), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            token.write_text(creds.to_json())
            return creds
        except Exception as e:
            print(f"No pude refrescar el token de '{cuenta}' ({e}).", file=sys.stderr)

    if not interactivo:
        sys.exit(
            f"La cuenta '{cuenta}' no tiene un token válido y estoy en modo no "
            f"interactivo.\nCorré a mano:  .venv/bin/python execution/google_auth.py "
            f"--setup --cuenta {cuenta}"
        )

    if not CREDENCIALES.exists():
        sys.exit(
            f"Falta {CREDENCIALES}.\n"
            "Bajalo de Google Cloud Console → Credenciales → ID de cliente OAuth\n"
            "→ tipo 'App de escritorio', y guardalo con ese nombre en la raíz del OS."
        )

    print(f"Abriendo el navegador. Elegí la cuenta que corresponde a '{cuenta}'.",
          file=sys.stderr)
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENCIALES), SCOPES)
    # prompt="select_account": sin esto Google reusa la sesión ya abierta y NO
    # muestra el selector. Autorizar una segunda cuenta terminaba guardando la
    # primera con otro nombre — y eso no falla, solo miente en silencio.
    creds = flow.run_local_server(port=0, prompt="select_account")

    email = _email_de(creds)
    ajena = _cuenta_con_email(email, excepto=cuenta)
    if ajena:
        sys.exit(
            f"\nAutorizaste {email}, que YA está guardada como cuenta '{ajena}'.\n"
            f"No guardo nada: tendrías dos nombres para el mismo buzón y los skills\n"
            f"leerían el inbox equivocado sin dar error.\n\n"
            f"Volvé a correrlo y en el selector de Google elegí OTRA cuenta. Si no\n"
            f"aparece el selector, deslogueate en accounts.google.com o usá una\n"
            f"ventana de incógnito."
        )

    token.write_text(creds.to_json())
    print(f"Token de '{cuenta}' guardado en {token.name} → {email}")
    return creds


def _email_de(creds):
    """El mail que quedó autorizado. Es el único dato que prueba con quién entramos."""
    return build("gmail", "v1", credentials=creds).users().getProfile(
        userId="me").execute()["emailAddress"]


def _cuenta_con_email(email, excepto=None):
    """Si otro token ya tiene ese mail, devuelve su nombre de cuenta."""
    for p in RAIZ.glob("token-*.json"):
        nombre = p.stem.removeprefix("token-")
        if nombre == excepto:
            continue
        try:
            otras = Credentials.from_authorized_user_file(str(p), SCOPES)
            if otras and otras.valid and _email_de(otras) == email:
                return nombre
        except Exception:
            continue
    return None


def cuentas_configuradas():
    """Qué cuentas ya tienen token. Para no adivinar qué hay disponible."""
    return sorted(p.stem.removeprefix("token-") for p in RAIZ.glob("token-*.json"))


def sheets(cuenta=CUENTA_DEFAULT):
    return build("sheets", "v4", credentials=credenciales(cuenta))


def drive(cuenta=CUENTA_DEFAULT):
    return build("drive", "v3", credentials=credenciales(cuenta))


def gmail(cuenta=CUENTA_DEFAULT):
    return build("gmail", "v1", credentials=credenciales(cuenta))


def bajar_xlsx(file_id, destino, cuenta=CUENTA_DEFAULT):
    """Exporta un Google Sheet completo a .xlsx.

    Se usa el export y NO `files().get_media()` ni el conector de Drive: el
    conector TRUNCA las hojas largas sin avisar (206 de 455 filas, julio 2026).
    """
    destino = pathlib.Path(destino)
    contenido = drive(cuenta).files().export(
        fileId=file_id,
        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ).execute()
    destino.write_bytes(contenido)
    return destino


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--setup", action="store_true",
                   help="Corre el flujo de login y guarda el token")
    p.add_argument("--cuenta", default=CUENTA_DEFAULT,
                   help=f"Qué cuenta autorizar o usar (default: {CUENTA_DEFAULT})")
    p.add_argument("--listar", action="store_true",
                   help="Muestra qué cuentas ya tienen token")
    args = p.parse_args()

    if args.listar:
        cuentas = cuentas_configuradas()
        if not cuentas:
            sys.exit("No hay ninguna cuenta autorizada todavía. Corré --setup.")
        for c in cuentas:
            try:
                perfil = gmail(c).users().getProfile(userId="me").execute()
                print(f"  {c:<10} → {perfil['emailAddress']}")
            except Exception as e:
                print(f"  {c:<10} → TOKEN ROTO: {e}")
        return

    credenciales(args.cuenta)
    perfil = gmail(args.cuenta).users().getProfile(userId="me").execute()
    print(f"Cuenta '{args.cuenta}' autenticada como {perfil['emailAddress']}")
    print(f"Scopes: {', '.join(s.rsplit('/', 1)[-1] for s in SCOPES)}")


if __name__ == "__main__":
    main()
