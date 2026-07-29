#!/usr/bin/env python3
"""Crea un anuncio de carrusel Click-to-WhatsApp dentro de un conjunto que ya existe.

Es el movimiento más barato disponible: entra como un anuncio más al conjunto que ya
está corriendo, así que no parte el presupuesto ni reinicia la fase de aprendizaje.
Meta reparte la entrega entre los anuncios y en dos semanas se ve cuál gana. La cuenta
nunca pautó un carrusel en 35 meses, así que es una variable entera sin explorar.

    # ver qué haría, sin tocar nada (por defecto)
    .venv/bin/python active/astronomy/pauta/crear_carrusel.py --producto curso-dj

    # crearlo de verdad, en pausa para revisarlo antes de que entregue
    .venv/bin/python active/astronomy/pauta/crear_carrusel.py --producto curso-dj --send

Las imágenes salen de `data/pauta/creativos.json`, que genera `subir_creativos.py`.

**Requiere que la app `astronomy-ads` esté en modo "Activo".** En modo Desarrollo Meta
crea el anuncio pero lo marca `WITH_ISSUES` y nunca entrega. El script lo verifica antes
de escribir para no ensuciar la cuenta con anuncios muertos.
"""

import argparse
import datetime
import json
import os
import pathlib
import re
import sys

import httpx
from dotenv import load_dotenv

RAIZ = pathlib.Path(__file__).resolve().parents[3]
load_dotenv(RAIZ / ".env")

TOKEN = os.getenv("META_ACCESS_TOKEN")
CUENTA = os.getenv("META_AD_ACCOUNT_ID")
VERSION = os.getenv("META_API_VERSION", "v23.0")
MANIFIESTO = RAIZ / "data" / "pauta" / "creativos.json"

PAGINA = "271070669425605"
WHATSAPP = "5491124005565"
CONJUNTO_ACTIVO = "120245002157210448"  # IntWpp1 PresCurso Nordelta

# El orden de las tarjetas es narrativo: gancho, cómo funciona, qué incluye, quién te
# enseña, cómo empezar. Los bullets van TERCEROS y no segundos: la tarjeta 2 todavía
# tiene que hacer que el otro siga deslizando, y una lista no hace eso.
ORDEN = ["que-es", "como-funciona", "beneficios", "profe", "contacto"]

# Los titulares van por ÁNGULO, no por posición: si algún día cambia ORDEN, cambia
# también qué placa es la tercera, y una lista posicional dejaría cada titular sobre
# la imagen equivocada sin que nada falle.
COPY = {
    "curso-dj": {
        "texto": ("Cabina profesional en Nordelta Plaza, clases uno a uno y profes que están "
                  "tocando hoy. No es un curso grabado: venís, te sentás en los platos y "
                  "aprendés con alguien al lado. Escribinos y te contamos cómo arrancar."),
        "titulares": {
            "que-es": "Aprendé a mezclar en cabina real",
            "como-funciona": "Elegís día y horario desde tu cuenta",
            "beneficios": "Cuatro clases por mes, uno a uno",
            "profe": "Con DJs que tocan de verdad",
            "contacto": "Escribinos y arrancás esta semana",
        },
    },
    "produccion-online": {
        "texto": ("Producí música desde tu casa, con un profe que corrige lo que hacés. Clases "
                  "uno a uno por videollamada, en Ableton, adaptadas a tu nivel y a lo que "
                  "querés hacer. Estés donde estés. Escribinos y te contamos cómo empezar."),
        "titulares": {
            "que-es": "Producí en Ableton desde tu casa",
            "como-funciona": "A tu ritmo y a tu nivel",
            "beneficios": "Clases uno a uno por videollamada",
            "profe": "Con productores en actividad",
            "contacto": "Escribinos y empezás esta semana",
        },
    },
    "membresias": {
        "texto": ("Una membresía, todos los créditos que quieras usar. Clases de DJ, producción "
                  "en Ableton, alquiler de cabina y de estudio: elegís vos en qué los gastás, "
                  "mes a mes, y lo que no usás se acumula. Escribinos y te armamos el plan que "
                  "te sirve."),
        "titulares": {
            "que-es": "Una membresía, todo el estudio",
            "como-funciona": "Los créditos que no usás se acumulan",
            "beneficios": "Clases, cabina y estudio",
            "profe": "Con los profes de la academia",
            "contacto": "Escribinos y armamos tu plan",
        },
    },
    "modo-profesional": {
        "texto": ("Ya sabés lo básico y querés dar el salto. Modo Profesional es para el que "
                  "quiere vivir de esto: producción, identidad sonora y salida real a tocar. "
                  "Escribinos y charlamos si es para vos."),
        "titulares": {
            "que-es": "Nunca tocaste para nadie",
            "como-funciona": "Ocho módulos, dos meses, un show",
            "beneficios": "Qué incluye el Modo Profesional",
            "profe": "Cabina real, con alguien al lado",
            "contacto": "Escribinos y te pasamos el programa",
        },
    },
}


# Variantes de copy para probar contra el texto base. La imagen no cambia: se prueba
# solo qué se dice. Cada variante corre en el MISMO conjunto que su control, así
# compiten por la misma entrega y la comparación no depende de la audiencia.
VARIANTES = {
    "modo-profesional": {
        "dolor": {
            "texto": ("Mezclás hace dos años. Nunca tocaste para nadie.\n\n"
                      "No es que te falte talento. Es que nadie te dijo qué sigue después de "
                      "aprender a mezclar: producir tu propio sonido, tener algo que suene a vos, "
                      "y saber a quién mandárselo. Eso lo trabajamos con vos, en cabina real, con "
                      "gente que está tocando esta semana.\n\n"
                      "Mandanos un tema tuyo y te decimos qué le falta."),
        },
    },
}


def api(cli, metodo, path, **datos):
    datos["access_token"] = TOKEN
    r = getattr(cli, metodo)(f"https://graph.facebook.com/{VERSION}/{path}",
                             **({"data": datos} if metodo == "post" else {"params": datos}))
    j = r.json()
    if "error" in j:
        e = j["error"]
        raise SystemExit(f"Meta rechazó {path}:\n  {e.get('message')}\n  {e.get('error_user_msg','')}")
    return j


def app_activa(cli):
    """En modo Desarrollo el anuncio se crea pero nace muerto. Mejor no crearlo."""
    try:
        j = api(cli, "get", os.getenv("META_APP_ID", "2994790630727835"), fields="name")
        return True, j.get("name", "")
    except SystemExit:
        return None, ""  # no podemos leer la app con este token; no es concluyente


MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]


def nombrar(cli, conjunto, producto, variante):
    """`producto | carrusel | square | variante | vN | mmm-aa`, con N sin repetir.

    El 29/07/2026 se creó un carrusel nuevo que quedó con EL MISMO nombre exacto que
    el viejo que venía a reemplazar: el nombre se armaba con producto+formato+variante
    y la variante no había cambiado. En el Administrador se distinguían solo por el
    estado — un click de distancia de pausar el equivocado. Así que la versión no se
    escribe a mano: se lee de la cuenta y se incrementa.
    """
    base = f"{producto} | carrusel | square | {variante or 'base'}"
    hoy = datetime.date.today()
    sello = f"{MESES[hoy.month - 1]}-{hoy.strftime('%y')}"

    usados = set()
    for ad in api(cli, "get", f"{conjunto}/ads", fields="name", limit=200).get("data", []):
        if ad.get("name", "").startswith(base + " |"):
            m = re.search(r"\|\s*v(\d+)\s*\|", ad["name"])
            if m:
                usados.add(int(m.group(1)))
    # Arranca en v2: v1 es el nombre viejo, el que no llevaba versión explícita.
    n = max(usados, default=1) + 1
    return f"{base} | v{n} | {sello}"


def main():
    ap = argparse.ArgumentParser(description="Crea un carrusel Click-to-WhatsApp. Dry-run por defecto.")
    ap.add_argument("--producto", required=True, choices=sorted(COPY))
    ap.add_argument("--conjunto", default=CONJUNTO_ACTIVO, help="ID del conjunto destino")
    ap.add_argument("--variante", help="Nombre de una variante de copy definida en VARIANTES")
    ap.add_argument("--send", action="store_true", help="Crearlo de verdad (si no, solo muestra)")
    args = ap.parse_args()

    if not TOKEN or not CUENTA:
        sys.exit("Faltan META_ACCESS_TOKEN o META_AD_ACCOUNT_ID en el .env")
    if not MANIFIESTO.exists():
        sys.exit(f"No existe {MANIFIESTO}. Corré antes subir_creativos.py")

    piezas = json.loads(MANIFIESTO.read_text()).get(args.producto)
    if not piezas:
        sys.exit(f"No hay placas subidas para '{args.producto}'")

    copy = dict(COPY[args.producto])
    if args.variante:
        v = (VARIANTES.get(args.producto) or {}).get(args.variante)
        if not v:
            disp = ", ".join((VARIANTES.get(args.producto) or {})) or "(ninguna)"
            sys.exit(f"No existe la variante '{args.variante}' para {args.producto}. Definidas: {disp}")
        copy.update(v)

    sin_titular = [a for a in ORDEN if a not in copy["titulares"]]
    if sin_titular:
        sys.exit(f"Faltan titulares para: {', '.join(sin_titular)} en {args.producto}")

    tarjetas, faltan = [], []
    for angulo in ORDEN:
        img = (piezas.get(angulo) or {}).get("square")
        if not img:
            faltan.append(angulo)
            continue
        tarjetas.append({
            "image_hash": img["hash"],
            "name": copy["titulares"][angulo],
            "link": f"https://wa.me/{WHATSAPP}",
            "call_to_action": {"type": "WHATSAPP_MESSAGE",
                               "value": {"app_destination": "WHATSAPP"}},
        })
    if faltan:
        sys.exit(f"Faltan placas square para: {', '.join(faltan)}")

    # El nombre se resuelve contra la cuenta también en dry-run: es una lectura, y así
    # se ve de antemano con qué versión va a entrar.
    with httpx.Client(timeout=120) as cli:
        nombre = nombrar(cli, args.conjunto, args.producto, args.variante)

    print(f"\nCarrusel: {nombre}")
    print(f"Conjunto destino: {args.conjunto}")
    print(f"\nTexto:\n  {copy['texto']}\n")
    for i, t in enumerate(tarjetas, 1):
        print(f"  {i}. {t['name']:<42} {t['image_hash'][:16]}…")

    if not args.send:
        print("\n[dry-run] No se creó nada. Agregá --send para crearlo.")
        return

    with httpx.Client(timeout=120) as cli:
        creativo = api(cli, "post", f"{CUENTA}/adcreatives",
            name=nombre,
            object_story_spec=json.dumps({
                "page_id": PAGINA,
                "link_data": {
                    "message": copy["texto"],
                    "link": f"https://wa.me/{WHATSAPP}",
                    "child_attachments": tarjetas,
                    "multi_share_optimized": True,
                    "multi_share_end_card": False,
                    "call_to_action": {"type": "WHATSAPP_MESSAGE",
                                       "value": {"app_destination": "WHATSAPP"}},
                },
            }),
        )
        # Nota: no se manda `degrees_of_freedom_spec`. Meta discontinuó el campo de
        # "mejoras estándar" a nivel global; ahora las mejoras se configuran de a una.
        # Sin el campo, la cuenta aplica su default.
        print(f"\nCreativo creado: {creativo['id']}")

        anuncio = api(cli, "post", f"{CUENTA}/ads",
            name=nombre, adset_id=args.conjunto,
            creative=json.dumps({"creative_id": creativo["id"]}), status="PAUSED")
        print(f"Anuncio creado EN PAUSA: {anuncio['id']}")

        estado = api(cli, "get", anuncio["id"], fields="effective_status,issues_info")
        print(f"Estado: {estado.get('effective_status')}")
        if estado.get("issues_info"):
            print("PROBLEMAS:")
            for i in estado["issues_info"]:
                print(f"   {i.get('error_summary')}")
            print("\nSi dice 'app en modo de desarrollo', pasá astronomy-ads a Activo y volvé a intentar.")
        else:
            print("\nSin problemas. Revisalo en el Administrador y activalo cuando quieras.")


if __name__ == "__main__":
    main()
