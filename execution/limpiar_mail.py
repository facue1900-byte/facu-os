"""Limpieza de bandeja + filtros para que deje de llegar ruido.

Token propio (token-limpieza-<cuenta>.json en la raíz del repo, gitignoreado) con
gmail.modify y gmail.settings.basic: NO toca los tokens de google_auth.py, que usan
las tareas programadas (sumarle scopes ahí los invalidaría a todos).

    .venv/bin/python execution/limpiar_mail.py --setup --cuenta facu    # una vez, abre el navegador
    .venv/bin/python execution/limpiar_mail.py --cuenta facu            # sólo cuenta, no toca nada
    .venv/bin/python execution/limpiar_mail.py --cuenta facu --aplicar  # papelera + leídos + filtros
"""
import argparse, pathlib, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

AQUI = pathlib.Path(__file__).resolve().parent.parent
CREDS = pathlib.Path("/Users/Facu/facu-os/credentials.json")
SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.settings.basic"]

# Remitentes que en 30 días mandaron 3+ mails de marketing sin que se abriera ninguno.
A_LA_PAPELERA = [
    "express@b.express.com", "newsletter@email.hm.com", "newsletter@mailing.buquebus.com.ar",
    "contact@essntlframes.com", "gopro@e-mail.gopro.com", "nick+news@leftclick.ai",
    "newsletter@mailing.aerolineas.com.ar", "clublanacion@suscribite.clubln.com.ar",
    "noreply@mixcloudmail.com", "bankofamerica@emcom.bankofamerica.com", "deportes@udesa.edu.ar",
    "alertas+d@mkt.despegar.com", "marketing@marketing.ryanairemail.com", "email@app.hardrockbet.com",
    "info@email.manychat.com", "tickets@fan.intermiamicf.com", "novedades@comunicacion.osde.com.ar",
    "news@ziltec.com.ar", "hello@chess.com", "contacto@svg-ent.com", "customer@meridiangrooming.com",
    "producto@productos.bancomacro.com.ar", "noreply@experiencia.bancomacro.com.ar",
    "newsletter@latroncal.com.ar", "comms@vinesresortandspa.com", "graduado@udesa.edu.ar",
    "info@tiendanewgarden.com.ar", "ypfserviclub@ypf.com", "@simply-jet.ch", "imangadzhi@consulting.com",
    "amigos@malba.org.ar", "ruben@rovesetups.com", "mas@comunicacion.osde.com.ar", "hola@trysmud.com",
    "no-reply@drop.cobrand.com", "info@wearebombo.com", "contenido@laspalapas.com.ar",
    "team@newsletter.artlist.io", "hello@aliveai.app", "noreply@tomorrowland.com",
    "marketing@r.flashpass.com.ar", "iberiaclub@comunicaciones.iberia.com", "noreply@skool.com",
    "rappi@hello.rappi.com.ar", "awards@mp1.tripadvisor.com",
    "no-reply@lyftmail.com", "noreply@woosports.com", "promocion@a.mercadopago.com",
]
# No se borran pero no ensucian la bandeja: se archivan leídos. Meta business-updates
# trae los recibos de la pauta: plata, se guarda.
SIN_BANDEJA = ["notifications@github.com", "noreply-accounts@google.com",
               "noreply@business-updates.facebook.com"]
# Cuenta -> mail esperado: con --setup se puede autorizar la casilla equivocada.
CUENTAS = {"facu": "facue1900@gmail.com", "studio": "studio@astronomyofficial.com",
           "paseo": "paseonordelta@gmail.com", "puzzle": "puzzle.bsas@gmail.com",
           "festevez": "festevez@astronomyofficial.com"}


def servicio(cuenta, setup):
    token = AQUI / f"token-limpieza-{cuenta}.json"
    creds = Credentials.from_authorized_user_file(str(token), SCOPES) if token.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not setup:
            sys.exit(f"Falta el permiso de '{cuenta}'. Corré: python {__file__} --setup --cuenta {cuenta}")
        creds = InstalledAppFlow.from_client_secrets_file(str(CREDS), SCOPES).run_local_server(
            port=0, prompt="select_account consent")
    token.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def ids(g, q):
    out, tok = [], None
    while True:
        r = g.users().messages().list(userId="me", q=q, maxResults=500, pageToken=tok).execute()
        out += [m["id"] for m in r.get("messages", [])]
        tok = r.get("nextPageToken")
        if not tok:
            return out


def modificar(g, lista, add=(), remove=()):
    for i in range(0, len(lista), 1000):
        g.users().messages().batchModify(userId="me", body={
            "ids": lista[i:i + 1000], "addLabelIds": list(add), "removeLabelIds": list(remove)}).execute()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cuenta", default="facu")
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    g = servicio(a.cuenta, a.setup)
    yo = g.users().getProfile(userId="me").execute()["emailAddress"]
    print(f"Cuenta: {yo}")
    if CUENTAS.get(a.cuenta, yo).lower() != yo.lower():
        sys.exit(f"El token de '{a.cuenta}' es de {yo}, no de {CUENTAS[a.cuenta]}. Borrá token-limpieza-{a.cuenta}.json y rehacé --setup.")

    remitentes = " OR ".join(f"from:{s}" for s in A_LA_PAPELERA)
    pasos = [
        ("Promociones a la papelera", "in:inbox category:promotions -is:starred -is:important", ["TRASH"], ["INBOX"]),
        ("Remitentes de marketing a la papelera", f"in:inbox ({remitentes})", ["TRASH"], ["INBOX"]),
        ("Rebotes (mailer-daemon) a la papelera", "in:inbox from:mailer-daemon older_than:3d", ["TRASH"], ["INBOX"]),
        ("GitHub y avisos de Google: archivar leídos",
         "in:inbox (" + " OR ".join(f"from:{s}" for s in SIN_BANDEJA) + ")", [], ["INBOX", "UNREAD"]),
        ("Resto de la bandeja de +14 días: marcar leído", "in:inbox is:unread older_than:14d -is:starred", [], ["UNREAD"]),
    ]
    for nombre, q, add, rem in pasos:
        lista = ids(g, q)
        print(f"{len(lista):>6}  {nombre}")
        if a.aplicar and lista:
            modificar(g, lista, add, rem)

    if a.aplicar:
        # Remitentes ya cubiertos por un filtro con la MISMA acción: sólo se crean los que faltan.
        def cubiertos(accion):
            out = set()
            for f in g.users().settings().filters().list(userId="me").execute().get("filter", []):
                if f.get("action", {}) == accion:
                    out |= {x.strip().lower() for x in f.get("criteria", {}).get("from", "").split(" OR ")}
            return out
        papelera = {"addLabelIds": ["TRASH"], "removeLabelIds": ["INBOX"]}
        archivar = {"removeLabelIds": ["INBOX", "UNREAD"]}
        hechos = 0
        for lista, accion in ((A_LA_PAPELERA, papelera), (SIN_BANDEJA, archivar)):
            ya = cubiertos(accion) | (cubiertos(archivar) if accion is papelera else set())
            faltan = [x for x in lista if x.lower() not in ya]
            print(f"Filtros: {len(lista) - len(faltan)} remitentes ya cubiertos, {len(faltan)} por crear")
            for k in range(0, len(faltan), 15):
                crit = {"from": " OR ".join(faltan[k:k + 15])}
                try:
                    g.users().settings().filters().create(userId="me", body={"criteria": crit, "action": accion}).execute()
                except HttpError as e:
                    # Sólo un 400 por la acción TRASH tiene plan B (archivar leído); el resto se corta.
                    if accion is not papelera or e.resp.status != 400:
                        raise
                    print(f"  Gmail no aceptó la papelera en un filtro ({e}); esta tanda queda como archivar leído")
                    g.users().settings().filters().create(userId="me", body={"criteria": crit, "action": archivar}).execute()
                hechos += 1
        print(f"Filtros creados: {hechos}")
        r = g.users().labels().get(userId="me", id="INBOX").execute()
        print(f"Bandeja después: {r['messagesUnread']} sin leer de {r['messagesTotal']}")
    else:
        print("\nModo prueba: no se tocó nada. Para aplicar: --aplicar")


if __name__ == "__main__":
    main()
