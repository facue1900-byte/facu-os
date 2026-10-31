"""Manda el mail de early birds de OBSESSION a la base de Puzzle.

--campana:      cuál mail (early, preventa1, ultimas, aumento, repaso).
--sync-bajas:   antes que nada, lee de puzzle.bsas las respuestas "baja" y los rebotes
                ("address not found") y los suma a bajas.txt / rebotes.txt. Obligatorio: cada una tiene su log.
Sin flags:      manda UNA prueba a Facu. No toca a nadie de la base.
--contar:       dice a cuántos le saldría y por qué quedan afuera los que quedan afuera.
--send:         manda de verdad a la base, en tandas de --limite (default 450, Gmail
                personal corta a ~500/día). Cada envío se anota en enviados.csv al
                instante: si se corta, se vuelve a correr y sigue donde quedó.

Quedan afuera siempre: menores de 18, bajas.txt, rebotes.txt y los ya enviados de ESA campaña.
"""
import argparse
import base64
import csv
import pathlib
import re
import sys
import time
import unicodedata
from datetime import date
from email.message import EmailMessage
from email.utils import formataddr

import openpyxl

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "execution"))
import google_auth  # noqa: E402

BASE = pathlib.Path.home() / "Desktop/Productoras/Puzzle/base_contactos_unificada PUZZLE.xlsx"
EVENTO = date(2026, 10, 31)
LINK = "https://planout.ar/eventos/es/comprarEvento?idEvento=1300&affId=FC"
REMITENTE = "OBSESSION"
CUENTA = "puzzle"  # puzzle.bsas@gmail.com: el remitente es Puzzle, no Facu
PRUEBA_A = "facue1900@gmail.com"
BAJAS = AQUI / "bajas.txt"
REBOTES = AQUI / "rebotes.txt"  # "address not found" de tandas anteriores

PIE = "\nSi no querés recibir más, respondé este mail con la palabra baja.\n"

# Cada campaña lleva su propio log: el que recibió una puede recibir la siguiente.
CAMPANAS = {
    "early": {
        "asunto": "OBSESSION: ya se fue la mitad de los early birds",
        "html": "mail.html",
        "log": "enviados.csv",
        "texto": """Hola{nombre},

El 31 de octubre es OBSESSION: LA fiesta de Halloween, en Palacio Alsina.

Ya se vendió la mitad de los early birds. Cuando se terminan, el precio sube fuerte.

EARLY BIRD $20.000
{link}

No lo dejes para el final.

31.10.2026 · PALACIO ALSINA · +27
""" + PIE,
    },
    # 07/10: early birds agotados; en Planout la tanda vigente es "PREVENTA 1" $25.000 + $3.750.
    "preventa1": {
        "asunto": "OBSESSION: se agotaron los early birds",
        "html": "mail-preventa1.html",
        "log": "enviados-preventa1.csv",
        "texto": """Hola{nombre},

El 31 de octubre es OBSESSION: LA fiesta de Halloween, en Palacio Alsina.

Los early birds se agotaron. Ya está a la venta la Preventa 1: cuando se termine, pasa a la tanda siguiente.

PREVENTA 1 $25.000
{link}

No lo dejes para el final.

31.10.2026 · PALACIO ALSINA · +27
""" + PIE,
    },
    # 21/10: la base sale en 4 días (450/día), así que "faltan N días" se calcula al armar
    # cada mail: el que lo recibe el 24/10 lee 7, no 10. "Últimas de Preventa 1" lo dijo
    # Facu el 21/10 (Planout no se lee desde acá): se chequea en el panel antes de cada tanda.
    "ultimas": {
        # 21/10 tarde: Facu avisó que aumentó (Preventa 1 terminada). 450 enviados, el resto NO.
        "cerrada": "la Preventa 1 se terminó el 21/10: este mail ya no es cierto",
        "asunto": "OBSESSION: {faltan} · últimas de Preventa 1",
        "html": "mail-ultimas.html",
        "log": "enviados-ultimas.csv",
        "texto": """Hola{nombre},

{Faltan} para OBSESSION: LA fiesta de Halloween, el sábado 31 de octubre en Palacio Alsina.

Quedan las últimas entradas de la Preventa 1. Cuando se terminen, pasa a la tanda siguiente.

{link}

No lo dejes para el final.

31.10.2026 · PALACIO ALSINA · +27
""" + PIE,
    },
    # 21/10: Facu avisó que aumentó. El texto NO nombra la tanda a propósito: sale 450 por
    # día y la tanda puede volver a cambiar en el medio; "ya subió" sigue siendo cierto.
    # Primero los que no recibieron "ultimas" el 21/10, para no mandarles dos mails seguidos.
    "aumento": {
        "asunto": "OBSESSION: {faltan} · ya subió el precio",
        "html": "mail-aumento.html",
        "log": "enviados-aumento.csv",
        "primero_sin": "enviados-ultimas.csv",
        "texto": """Hola{nombre},

{Faltan}: OBSESSION, LA fiesta de Halloween, el sábado 31 de octubre en Palacio Alsina.

Se agotó la Preventa 1 y el precio ya subió. Cada tanda que se termina, sube de nuevo.

{link}

No lo dejes para el final.

31.10.2026 · PALACIO ALSINA · +27
""" + PIE,
    },
}
# 30/10 noche: Facu pidió volver a mandarle a toda la base, 450 por día, hasta la fiesta.
# Mismo mail que "aumento" con log propio; primero los que lo recibieron hace más tiempo.
CAMPANAS["repaso"] = dict(CAMPANAS["aumento"], log="enviados-repaso.csv", primero_sin=None,
                          orden_por="enviados-aumento.csv")


def faltan(hoy=None):
    """'faltan 10 días' / 'falta 1 día'. Frena si el evento ya pasó o es hoy."""
    n = (EVENTO - (hoy or date.today())).days
    if n < 0:
        sys.exit(f"El evento fue el {EVENTO:%d/%m}. Frenado.")
    # 30/10: la víspera dice "es mañana" (pedido de Facu) y el día del evento, "es hoy".
    return "es hoy" if n == 0 else "es mañana" if n == 1 else f"faltan {n} días"


NOMBRES_PROHIBIDOS = r"\b(puzzle|obsession|astronomy|gay|puto|trolo|cogid\w*|pija|concha|forro|boludo|pete)\b"


def _ascii(s):
    return unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().lower()


def saludo(nombre, apellido, email):
    """' Sofi' si el nombre parece un nombre Y es de ese mail; si no, '' (queda "Hola,").

    Los usuarios de Instagram vienen sin apellido: sin apellido, no se saluda por nombre.
    El nombre de la base a veces es el del VENDEDOR, no el del dueño del mail (07/10: a
    agustin.durigon le llegó "Hola Lucas" porque Lanfranconi le vendió la entrada; "Benjamin
    Brocca" figura en 16 mails). Por eso sólo se saluda si el nombre o el apellido aparece
    en el mail.
    """
    if not str(apellido or "").strip():
        return ""
    primero = str(nombre or "").strip().split(" ")[0]
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]{2,}", primero):
        return ""
    # "Puzzle Meyrelles" = cargado por la productora; "Panchi Gay Cogido" = nombre trucho.
    if re.search(NOMBRES_PROHIBIDOS, _ascii(f"{nombre} {apellido}")):
        return ""
    local = re.sub(r"[^a-z]", "", _ascii(email.split("@")[0]))
    partes = [t for t in re.split(r"[^a-z]+", _ascii(f"{nombre} {apellido}")) if len(t) >= 3]
    if not any(t in local for t in partes):
        return ""
    return " " + primero.capitalize()


def edad(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def leer_base():
    wb = openpyxl.load_workbook(BASE, read_only=True)
    filas = list(wb["Unificada"].iter_rows(values_only=True))
    if filas[1][:3] != ("Nombre", "Apellido", "Email"):
        sys.exit(f"La base cambió de formato: encabezado {filas[1]}")
    personas = [
        {"nombre": r[0], "apellido": r[1], "email": (r[2] or "").strip().lower(), "edad": edad(r[5]),
         "tickets": r[7] or 0}
        for r in filas[2:]
    ]
    if len(personas) < 1000:
        sys.exit(f"La base trae {len(personas)} personas; esperaba ~1.367. Frenado.")
    return personas


def ya_enviados(log):
    if not log.exists():
        return set()
    with log.open() as f:
        return {row["email"] for row in csv.DictReader(f)}


def leer_lista(archivo):
    if not archivo.exists():
        return set()
    return {l.strip().lower() for l in archivo.read_text().splitlines() if l.strip()}


def recibido(log):
    """email → cuándo le llegó en esa campaña ('' si nunca)."""
    with log.open() as f:
        return {row["email"]: row["enviado"] for row in csv.DictReader(f)}


def destinatarios(log, primero_sin=None, orden_por=None):
    personas = leer_base()
    enviados, baja, rebote = ya_enviados(log), leer_lista(BAJAS), leer_lista(REBOTES)
    afuera = {"menor de 18": 0, "baja": 0, "rebotó": 0, "ya enviado": 0, "mail inválido": 0}
    lista, vistos = [], set()
    for p in personas:
        e = p["email"]
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", e) or e in vistos:
            afuera["mail inválido"] += 1
        elif p["edad"] is not None and p["edad"] < 18:
            afuera["menor de 18"] += 1
        elif e in baja:
            afuera["baja"] += 1
        elif e in rebote:
            afuera["rebotó"] += 1
        elif e in enviados:
            afuera["ya enviado"] += 1
        else:
            lista.append(p)
        vistos.add(e)
    # Primero los que compran para el grupo.
    lista.sort(key=lambda p: -p["tickets"])
    if primero_sin:
        # sorted es estable: dentro de cada grupo se mantiene el orden por entradas.
        ya = ya_enviados(AQUI / primero_sin)
        lista.sort(key=lambda p: p["email"] in ya)
    if orden_por:
        cuando = recibido(AQUI / orden_por)
        lista.sort(key=lambda p: cuando.get(p["email"], ""))
    return personas, lista, afuera


def sync_bajas(svc):
    """Suma a bajas.txt los que contestaron "baja" y a rebotes.txt los "address not found".

    Lee la bandeja de puzzle.bsas de los últimos 30 días. Una respuesta cuenta como baja si la
    palabra aparece en lo que escribió la persona (el snippet arranca por ahí), no en la cita
    del mail nuestro, que también dice "baja".
    """
    def ids(q):
        out, tok = [], None
        while True:
            r = svc.list(userId="me", q=q, maxResults=500, pageToken=tok).execute()
            out += [m["id"] for m in r.get("messages", [])]
            tok = r.get("nextPageToken")
            if not tok:
                return out
    nuevas_b, nuevas_r = set(), set()
    for mid in ids("in:inbox newer_than:30d -from:mailer-daemon -from:me"):
        m = svc.get(userId="me", id=mid, format="metadata", metadataHeaders=["From"]).execute()
        propio = re.split(r"\b(El|On) .{0,80}(escribió|wrote)", m.get("snippet", ""))[0]
        if re.search(r"\bbaja\b", propio, re.I):
            frm = m["payload"]["headers"][0]["value"]
            e = (re.search(r"[\w.+-]+@[\w.-]+", frm) or [None])[0]
            if e:
                nuevas_b.add(e.lower())
    for mid in ids("from:mailer-daemon newer_than:30d \"address not found\""):
        sn = svc.get(userId="me", id=mid, format="metadata").execute().get("snippet", "")
        e = re.search(r"delivered to ([\w.+-]+@[\w.-]+?)\.? because", sn)
        if e:
            nuevas_r.add(e.group(1).lower())
    for archivo, nuevas in ((BAJAS, nuevas_b), (REBOTES, nuevas_r)):
        faltan_ = sorted(nuevas - leer_lista(archivo))
        if faltan_:
            with archivo.open("a") as f:
                f.write("".join(e + "\n" for e in faltan_))
        print(f"{archivo.name}: +{len(faltan_)} {faltan_}")


def armar(c, para, nombre, desde):
    html = (AQUI / c["html"]).read_text()
    f = faltan()
    html = (html.replace("{{nombre}}", nombre)
                .replace("{{faltan}}", f).replace("{{Faltan}}", f.capitalize())
                .replace("{{link}}", LINK.replace("&", "&amp;"))
                .replace("{{banner}}", "cid:banner"))
    if "{{" in html:
        sys.exit("Quedó una variable sin reemplazar en mail.html. Frenado.")
    m = EmailMessage()
    m["To"] = para
    m["From"] = formataddr((REMITENTE, desde))
    m["Subject"] = c["asunto"].format(faltan=f)
    m.set_content(c["texto"].format(nombre=nombre, link=LINK, faltan=f, Faltan=f.capitalize()))
    m.add_alternative(html, subtype="html")
    m.get_payload()[1].add_related(
        (AQUI / "obsession-banner.jpg").read_bytes(), "image", "jpeg", cid="<banner>",
        filename="obsession.jpg", disposition="inline")
    return {"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}


def salio(svc, email):
    """Id del mail a `email` en Enviados de los últimos 10 minutos, o None."""
    try:
        time.sleep(5)
        r = svc.list(userId="me", q=f"in:sent to:{email} newer_than:1d", maxResults=1).execute()
        m = r.get("messages")
        if not m:
            return None
        meta = svc.get(userId="me", id=m[0]["id"], format="minimal").execute()
        return m[0]["id"] if time.time() - int(meta["internalDate"]) / 1000 < 600 else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campana", required=True, choices=sorted(CAMPANAS))
    ap.add_argument("--contar", action="store_true")
    ap.add_argument("--send", action="store_true", help="Manda de verdad a la base")
    ap.add_argument("--limite", type=int, default=450)
    ap.add_argument("--sync-bajas", action="store_true", help="Lee bajas y rebotes de la bandeja antes")
    ap.add_argument("--cuenta", default=CUENTA, help="Token de google_auth desde el que sale")
    ap.add_argument("--auto", action="store_true",
                    help="Tarea programada: no hace nada (sale 0) si es el día del evento o después, "
                         "si la última tanda fue hace menos de 24 h o si no queda nadie")
    a = ap.parse_args()

    c = CAMPANAS[a.campana]
    if c.get("cerrada") and a.send:
        sys.exit(f"Campaña '{a.campana}' cerrada: {c['cerrada']}. No se manda.")
    log = AQUI / c["log"]
    if a.auto:
        # 23/10: Facu pidió que la tanda diaria salga sola. Gmail corta a ~500 en 24 h
        # corridas (puzzle.bsas ya fue suspendida el 28/09): sin 24 h desde el último
        # envío, no se manda.
        if date.today() >= EVENTO:
            print(f"Auto: ya es {date.today():%d/%m}, el evento fue/es el {EVENTO:%d/%m}. Nada que mandar.")
            return
        if log.exists():
            filas = list(csv.DictReader(log.open()))
            if filas:
                ultimo = time.mktime(time.strptime(filas[-1]["enviado"], "%Y-%m-%d %H:%M:%S"))
                horas = (time.time() - ultimo) / 3600
                if horas < 24:
                    print(f"Auto: el último envío fue hace {horas:.1f} h (< 24). No se manda.")
                    return
    if a.sync_bajas:
        sync_bajas(google_auth.gmail(a.cuenta).users().messages())
    personas, lista, afuera = destinatarios(log, c.get("primero_sin"), c.get("orden_por"))
    print(f"Campaña: {a.campana} · asunto: {c['asunto'].format(faltan=faltan())}")
    print(f"Base: {len(personas)} · pendientes de envío: {len(lista)} · afuera: {afuera}")
    if a.contar:
        return
    if a.auto and not lista:
        print("Auto: no queda nadie pendiente en esta campaña. Nada que mandar.")
        return

    gm = google_auth.gmail(a.cuenta).users()
    desde = gm.getProfile(userId="me").execute()["emailAddress"]
    print(f"Sale desde: {desde}")
    svc = gm.messages()
    if not a.send:
        svc.send(userId="me", body=armar(c, PRUEBA_A, " Facu", desde)).execute()
        print(f"Prueba mandada a {PRUEBA_A}. Nadie de la base recibió nada.")
        return

    tanda = lista[: a.limite]
    nuevo = not log.exists()
    with log.open("a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["email", "enviado", "gmail_id"])
        for i, p in enumerate(tanda, 1):
            try:
                r = svc.send(userId="me", body=armar(c, p["email"], saludo(p["nombre"], p["apellido"], p["email"]), desde)).execute()
            except Exception as e:
                # 21/10 se cortó por "read timeout" y el mail SÍ había salido: si Gmail lo
                # tiene en Enviados, se anota, así la próxima corrida no se lo repite.
                ya = salio(svc, p["email"])
                if ya:
                    w.writerow([p["email"], time.strftime("%Y-%m-%d %H:%M:%S"), ya])
                    f.flush()
                print(f"FRENADO en {i}/{len(tanda)} ({p['email']}, {'sí salió, anotado' if ya else 'no salió'}): {e}")
                sys.exit(1)
            w.writerow([p["email"], time.strftime("%Y-%m-%d %H:%M:%S"), r["id"]])
            f.flush()
            if i % 50 == 0:
                print(f"  {i}/{len(tanda)}")
            time.sleep(1.5)
    print(f"Tanda terminada: {len(tanda)} enviados. Quedan {len(lista) - len(tanda)}.")


if __name__ == "__main__":
    main()
