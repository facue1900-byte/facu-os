"""Manda el mail de early birds de OBSESSION a la base de Puzzle.

--campana:      cuál mail (early, preventa1). Obligatorio: cada una tiene su log.
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
from email.message import EmailMessage
from email.utils import formataddr

import openpyxl

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "execution"))
import google_auth  # noqa: E402

BASE = pathlib.Path.home() / "Desktop/Productoras/Puzzle/base_contactos_unificada PUZZLE.xlsx"
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
}


def saludo(nombre, apellido):
    """' Sofi' si el nombre parece un nombre; '' si es un usuario tipo 'Vferraritorre'.

    Los usuarios de Instagram vienen sin apellido: sin apellido, no se saluda por nombre.
    """
    if not str(apellido or "").strip():
        return ""
    primero = str(nombre or "").strip().split(" ")[0]
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]{2,}", primero):
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


def destinatarios(log):
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
    return personas, lista, afuera


def armar(c, para, nombre, desde):
    html = (AQUI / c["html"]).read_text()
    html = (html.replace("{{nombre}}", nombre)
                .replace("{{link}}", LINK.replace("&", "&amp;"))
                .replace("{{banner}}", "cid:banner"))
    if "{{" in html:
        sys.exit("Quedó una variable sin reemplazar en mail.html. Frenado.")
    m = EmailMessage()
    m["To"] = para
    m["From"] = formataddr((REMITENTE, desde))
    m["Subject"] = c["asunto"]
    m.set_content(c["texto"].format(nombre=nombre, link=LINK))
    m.add_alternative(html, subtype="html")
    m.get_payload()[1].add_related(
        (AQUI / "obsession-banner.jpg").read_bytes(), "image", "jpeg", cid="<banner>",
        filename="obsession.jpg", disposition="inline")
    return {"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campana", required=True, choices=sorted(CAMPANAS))
    ap.add_argument("--contar", action="store_true")
    ap.add_argument("--send", action="store_true", help="Manda de verdad a la base")
    ap.add_argument("--limite", type=int, default=450)
    ap.add_argument("--cuenta", default=CUENTA, help="Token de google_auth desde el que sale")
    a = ap.parse_args()

    c = CAMPANAS[a.campana]
    log = AQUI / c["log"]
    personas, lista, afuera = destinatarios(log)
    print(f"Campaña: {a.campana} · asunto: {c['asunto']}")
    print(f"Base: {len(personas)} · pendientes de envío: {len(lista)} · afuera: {afuera}")
    if a.contar:
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
                r = svc.send(userId="me", body=armar(c, p["email"], saludo(p["nombre"], p["apellido"]), desde)).execute()
            except Exception as e:
                print(f"FRENADO en {i}/{len(tanda)} ({p['email']}): {e}")
                sys.exit(1)
            w.writerow([p["email"], time.strftime("%Y-%m-%d %H:%M:%S"), r["id"]])
            f.flush()
            if i % 50 == 0:
                print(f"  {i}/{len(tanda)}")
            time.sleep(1.5)
    print(f"Tanda terminada: {len(tanda)} enviados. Quedan {len(lista) - len(tanda)}.")


if __name__ == "__main__":
    main()
