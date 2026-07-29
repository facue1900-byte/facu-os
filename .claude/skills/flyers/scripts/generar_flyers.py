#!/usr/bin/env python3
"""Genera flyers de Astronomy Academy en PNG, listos para Instagram.

Un producto x N ángulos de venta x M formatos. El copy y los precios viven en
`contenido/academy.json` (los precios los sincroniza `sync_precios.py` contra
Supabase); la estética vive en `templates/flyer.html` y usa los mismos tokens de
color que la app en producción.

    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py
    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py --productos membresias
    .venv/bin/python .claude/skills/flyers/scripts/generar_flyers.py --formatos story

Render con el Chrome que ya está instalado (headless, sin dependencias nuevas).
Cada pieza se verifica de verdad antes de darse por buena: dimensiones exactas,
que el PNG no sea una placa vacía, y que el texto no haya desbordado. Si una
falla, el script termina con error y dice cuál — no exporta 74 buenas y una rota
en silencio.
"""

import argparse
import concurrent.futures
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

SKILL = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Tamaño, escala tipográfica y márgenes por formato. `base` es el font-size raíz:
# todo el template está en rem, así que una sola cifra reescala la pieza entera.
FORMATOS = {
    "feed":   {"w": 1080, "h": 1350, "base": 16.0, "pad": 5.4, "padx": 4.4, "pad_ed": 3.4, "padx_ed": 3.4},
    "story":  {"w": 1080, "h": 1920, "base": 17.0, "pad": 9.5, "padx": 4.6, "pad_ed": 5.6, "padx_ed": 3.3},
    "square": {"w": 1080, "h": 1080, "base": 14.0, "pad": 4.6, "padx": 4.2, "pad_ed": 3.6, "padx_ed": 3.6},
}

# Debajo de esto un PNG de 1080px es una placa vacía o casi: el render se colgó
# antes de pintar el texto. 40 KB es holgado — la pieza más pelada da ~90 KB.
MINIMO_BYTES = 40_000


def pesos(n):
    """143520 -> '$143.520'. Formato argentino, sin decimales y sin redondear."""
    return "$" + f"{int(n):,}".replace(",", ".")


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bloque_html(bloque, producto, planes):
    """Arma el bloque central. Cada tipo es una forma distinta de mostrar la oferta."""
    tipo = bloque.get("tipo", "ninguno")

    if tipo == "ninguno":
        return ""

    if tipo == "precio":
        precio = producto.get("precio_ars")
        if precio is None:
            raise ValueError(
                f"El producto '{producto['id']}' tiene un ángulo de precio pero "
                f"`precio_ars` es null. Corré sync_precios.py o sacá el ángulo: "
                f"un flyer no sale con el precio en blanco."
            )
        nota = bloque.get("nota")
        return (
            '<div class="bloque"><div class="precio">'
            f'<div class="monto">{pesos(precio)}</div>'
            f'<div class="periodo">{esc(bloque.get("periodo", ""))}</div>'
            + (f'<div class="nota">{esc(nota)}</div>' if nota else "")
            + "</div></div>"
        )

    if tipo == "bullets":
        items = "".join(f"<li>{esc(i)}</li>" for i in bloque["items"])
        return f'<div class="bloque"><ul class="bullets">{items}</ul></div>'

    if tipo == "dato":
        return (
            '<div class="bloque"><div class="dato">'
            f'<div class="n">{esc(bloque["numero"])}</div>'
            f'<div class="l">{esc(bloque["etiqueta"])}</div>'
            "</div></div>"
        )

    if tipo == "planes":
        cards = []
        for i, pid in enumerate(producto["planes"]):
            if pid not in planes:
                raise ValueError(f"El plan '{pid}' no está en precios.json. Corré sync_precios.py.")
            p = planes[pid]
            destacado = " destacado" if i == 1 else ""
            cards.append(
                f'<div class="plan{destacado}">'
                f'<div class="n">{esc(p["name"])}</div>'
                f'<div class="p">{pesos(p["price_ars"])}</div>'
                f'<div class="c">{p["monthly_credits"]} créditos</div>'
                "</div>"
            )
        return f'<div class="bloque"><div class="planes">{"".join(cards)}</div></div>'

    raise ValueError(f"Tipo de bloque desconocido: {tipo}")


def fondo_y_cabecera(estilo, marca, producto, assets):
    """Devuelve (clase del body, HTML del fondo, HTML de la cabecera).

    `plano` = degradado violeta sobre negro, el look de la app.
    `foto`  = foto del estudio a sangre + velo, el look de la cuenta de Instagram.
    """
    if estilo == "plano":
        return (
            "",
            '<div class="bg"></div>\n<div class="grid"></div>',
            f'<img src="{(assets / "marca" / marca["isotipo"]).as_uri()}" alt="">'
            f'<div class="nombre">{esc(marca["nombre"])}</div>',
        )

    foto = producto.get("foto")
    if not foto:
        raise ValueError(
            f"El producto '{producto['id']}' no declara `foto` y el estilo es 'foto'. "
            f"Agregale una de assets/fotos/ o generá ese producto con --estilo plano."
        )
    ruta = assets / "fotos" / foto
    if not ruta.exists():
        raise ValueError(f"No existe la foto {ruta}. Están: {[p.name for p in (assets / 'fotos').glob('*')]}")
    return (
        "con-foto",
        f'<img class="foto" src="{ruta.as_uri()}" alt="">\n<div class="velo"></div>',
        f'<img class="firma" src="{(assets / "marca" / marca["firma"]).as_uri()}" alt="">',
    )


def bloque_editorial(bloque, producto, planes):
    """Mismo contenido que `bloque_html`, en el lenguaje de la cuenta: alineado a la
    izquierda, monocromo, índices mono entre corchetes y planes separados por reglas."""
    tipo = bloque.get("tipo", "ninguno")

    if tipo == "ninguno":
        return ""

    if tipo == "precio":
        # Decisión de Facu (28/07/2026): las piezas de Instagram NO llevan precio en
        # pesos. Con la inflación, un flyer publicado con un número queda viejo en
        # semanas. El guard va acá y no en el JSON para que no alcance con editar el
        # contenido: si alguien vuelve a poner un bloque de precio, el script corta.
        raise ValueError(
            f"El producto '{producto['id']}' pide un bloque de precio en pesos, y las "
            "piezas de Instagram no llevan precio (decisión del 28/07/2026: inflación). "
            "Usá un bloque `dato` con créditos, clases o módulos, y que el valor del "
            "mes se pida por DM."
        )

    if tipo == "bullets":
        items = "".join(
            f'<li><span class="i">[{i:02d}]</span><span>{esc(t)}</span></li>'
            for i, t in enumerate(bloque["items"], 1)
        )
        return f'<div class="bloque"><ul class="bullets">{items}</ul></div>'

    if tipo == "dato":
        return (
            '<div class="bloque"><div class="dato">'
            f'<div class="n">{esc(bloque["numero"])}</div>'
            f'<div class="l">{esc(bloque["etiqueta"])}</div>'
            "</div></div>"
        )

    if tipo == "planes":
        # Sin pesos: lo que diferencia a los planes en la pieza son los CRÉDITOS,
        # que no se mueven con la inflación. El valor del mes se pide por DM.
        cards = []
        for i, pid in enumerate(producto["planes"]):
            if pid not in planes:
                raise ValueError(f"El plan '{pid}' no está en precios.json. Corré sync_precios.py.")
            p = planes[pid]
            destacado = " destacado" if i == 1 else ""
            cards.append(
                f'<div class="plan{destacado}">'
                f'<div class="n">{esc(p["name"])}</div>'
                f'<div class="p">{p["monthly_credits"]}</div>'
                '<div class="c">créditos por mes</div>'
                "</div>"
            )
        return f'<div class="bloque"><div class="planes">{"".join(cards)}</div></div>'

    raise ValueError(f"Tipo de bloque desconocido: {tipo}")


def rotulos_html(lineas, alinear_derecha=False):
    """Cada rótulo es un bloque de 1 o 2 líneas mono; van apilados en la esquina."""
    clase = "rot der" if alinear_derecha else "rot"
    return "".join(
        f'<div class="{clase}">' + "<br>".join(esc(l) for l in bloque) + "</div>"
        for bloque in lineas
    )


def foto_del_angulo(producto, angulo):
    """Qué foto le toca a este ángulo. None = fondo negro.

    El ángulo manda sobre el producto: un carrusel con la misma foto en las cinco
    tarjetas parece un error de carga, no una pieza. Ver `chequear_fotos`.
    """
    if angulo.get("fondo") == "negro":
        return None
    return angulo.get("foto") or producto.get("foto")


def chequear_fotos(productos):
    """Ninguna foto puede repetirse dentro de un mismo producto.

    Las cinco piezas de un producto se ven juntas —como tarjetas del carrusel de
    Meta o como fila de la grilla— y ahí la repetición se lee como un bug. Esto
    salió de un anuncio real (29/07/2026): cuatro de las cinco tarjetas del
    carrusel de Modo Profesional tenían la misma foto. Se chequea acá y no a ojo
    porque a ojo ya se pasó una vez.
    """
    errores = []
    for producto in productos:
        vistas = {}
        for angulo in producto["angulos"]:
            foto = foto_del_angulo(producto, angulo)
            if foto:
                vistas.setdefault(foto, []).append(angulo["id"])
        for foto, angulos in vistas.items():
            if len(angulos) > 1:
                errores.append(
                    f"  {producto['id']}: '{foto}' se repite en {', '.join(angulos)}"
                )
    if errores:
        raise ValueError(
            "Hay fotos repetidas dentro de un mismo producto. Poné `foto` en cada "
            "ángulo (assets/fotos/):\n" + "\n".join(errores)
        )


def armar_html_editorial(template, marca, producto, angulo, fmt, planes, assets):
    f = FORMATOS[fmt]
    rot = {**marca.get("rotulos", {}), **producto.get("rotulos", {})}
    foto = foto_del_angulo(producto, angulo)
    if not foto:
        fondo = ""
    else:
        ruta = assets / "fotos" / foto
        if not ruta.exists():
            disponibles = sorted(p.name for p in (assets / "fotos").glob("*.jpg"))
            raise ValueError(f"No existe la foto {ruta}. Están: {disponibles}")
        fondo = f'<img class="foto" src="{ruta.as_uri()}" alt="">\n<div class="velo"></div>'

    kicker = angulo.get("kicker")
    sub = angulo.get("sub")
    cta = angulo.get("cta")
    reemplazos = {
        "{{FONT_MONO}}": (assets / "fonts/RobotoMono.ttf").as_uri(),
        "{{W}}": str(f["w"]),
        "{{H}}": str(f["h"]),
        "{{BASE}}": str(f["base"]),
        "{{PAD}}": str(f["pad_ed"]),
        "{{PADX}}": str(f["padx_ed"]),
        "{{FONDO}}": fondo,
        "{{CLASE_BODY}}": "con-foto" if foto else "sin-foto",
        "{{ROT_IZQ}}": rotulos_html(rot.get("izq", [])),
        "{{ROT_DER}}": rotulos_html(rot.get("der", []), alinear_derecha=True),
        "{{CEJA}}": f'<div class="ceja">({esc(kicker)})</div>' if kicker else "",
        # `escala: xl` es para la tarjeta que abre un carrusel: titular corto y grande,
        # sin bloque abajo. Es lo único que frena el scroll.
        "{{CLASE_TITULAR}}": " xl" if angulo.get("escala") == "xl" else "",
        "{{TITULAR}}": angulo["titular"],
        "{{SUB}}": f'<p class="sub">{esc(sub)}</p>' if sub else "",
        "{{BLOQUE}}": bloque_editorial(angulo["bloque"], producto, planes),
        "{{TAG}}": f'<div class="tag">[ {esc(cta)} ]</div>' if cta else "<div></div>",
        "{{FLECHA}}": "&rarr;",
        # Sin escapar: admite <br> para partirlo en dos líneas, igual que el titular.
        "{{LEGAL}}": marca["legal_editorial"],
    }
    html = template
    for k, v in reemplazos.items():
        html = html.replace(k, v)
    faltantes = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if faltantes:
        raise ValueError(f"Quedaron placeholders sin reemplazar: {sorted(set(faltantes))}")
    return html


def armar_html(template, marca, producto, angulo, fmt, planes, assets, estilo):
    f = FORMATOS[fmt]
    kicker = angulo.get("kicker")
    sub = angulo.get("sub")
    clase, fondo, cabecera = fondo_y_cabecera(estilo, marca, producto, assets)
    reemplazos = {
        "{{CLASE}}": clase,
        "{{FONDO}}": fondo,
        "{{CABECERA}}": cabecera,
        "{{W}}": str(f["w"]),
        "{{H}}": str(f["h"]),
        "{{BASE}}": str(f["base"]),
        "{{PAD}}": str(f["pad"]),
        "{{PADX}}": str(f["padx"]),
        "{{KICKER}}": f'<div class="kicker">{esc(kicker)}</div>' if kicker else "",
        # El titular admite <em> (palabra en violeta) y <br>: es copy nuestro,
        # no entrada de usuario.
        "{{TITULAR}}": angulo["titular"],
        "{{SUB}}": f'<p class="sub">{esc(sub)}</p>' if sub else "",
        "{{BLOQUE}}": bloque_html(angulo["bloque"], producto, planes),
        "{{CTA}}": f'<div class="cta">{esc(angulo["cta"])}</div>' if angulo.get("cta") else "",
        "{{LEGAL}}": esc(marca["legal"]),
    }
    html = template
    for k, v in reemplazos.items():
        html = html.replace(k, v)

    faltantes = re.findall(r"\{\{[A-Z]+\}\}", html)
    if faltantes:
        raise ValueError(f"Quedaron placeholders sin reemplazar: {sorted(set(faltantes))}")
    return html


def render(html, destino, fmt, intentos=3):
    """HTML -> PNG con Chrome headless, con reintento. Devuelve el veredicto del auto-ajuste.

    Con 5 Chrome en paralelo, cada tanto uno se queda colgado y nunca escribe el PNG.
    No es el contenido —la misma pieza renderiza bien al segundo intento—, así que se
    reintenta en vez de tumbar la tanda entera. Si se agotan los intentos, revienta:
    una pieza que no se pudo renderizar no puede quedar como la versión vieja en disco.
    """
    ultimo = None
    for intento in range(1, intentos + 1):
        try:
            return _render_una(html, destino, fmt)
        except subprocess.TimeoutExpired as e:
            ultimo = e
            print(f"   (timeout de Chrome en {destino.name}, intento {intento}/{intentos})")
    raise RuntimeError(f"Chrome se colgó {intentos} veces con {destino}") from ultimo


def _render_una(html, destino, fmt):
    f = FORMATOS[fmt]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="flyer-"))
    try:
        pagina = tmp / "flyer.html"
        pagina.write_text(html, encoding="utf-8")
        salida = tmp / "out.png"
        # Nada de `--user-data-dir`: con un perfil nuevo en /tmp, el Chrome de macOS
        # se cuelga indefinidamente (probado: 25s sin escribir nada, ni con
        # --no-first-run --no-default-browser-check --disable-sync). Sin el flag
        # anda, y cinco corridas en paralelo dan PNGs byte a byte idénticos, así
        # que compartir el perfil por defecto no molesta.
        proc = subprocess.run(
            [
                CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--virtual-time-budget=4000",
                f"--window-size={f['w']},{f['h']}",
                "--dump-dom",
                f"--screenshot={salida}",
                pagina.as_uri(),
            ],
            capture_output=True, text=True, timeout=120,
        )
        if not salida.exists():
            raise RuntimeError(f"Chrome no escribió el PNG.\n{proc.stderr[-800:]}")

        # El template deja el veredicto del auto-ajuste en el <title>. Se lee del
        # DOM volcado en la misma corrida, así no hay que renderizar dos veces.
        m = re.search(r"<title>([^<]*)</title>", proc.stdout)
        veredicto = m.group(1) if m else "SIN-TITULO"

        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(salida), destino)
        return veredicto
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verificar(path, fmt, veredicto):
    """Devuelve la lista de problemas de una pieza. Vacía = está bien."""
    f = FORMATOS[fmt]
    problemas = []
    tam = path.stat().st_size
    if tam < MINIMO_BYTES:
        problemas.append(f"pesa {tam} bytes: parece una placa vacía")
    with Image.open(path) as im:
        if im.size != (f["w"], f["h"]):
            problemas.append(f"mide {im.size[0]}x{im.size[1]}, esperaba {f['w']}x{f['h']}")
    if veredicto == "DESBORDA":
        problemas.append("el texto no entra ni achicando al 62%: acortá el copy")
    elif not veredicto.startswith("OK:"):
        problemas.append(f"el auto-ajuste no reportó nada ({veredicto})")
    return problemas


def contacto(piezas, destino, columnas=6, ancho=300):
    """Hoja de contacto con todas las piezas, para revisar de un vistazo."""
    if not piezas:
        return None
    minis = []
    for p in piezas:
        with Image.open(p) as im:
            alto = round(im.height * ancho / im.width)
            minis.append(im.convert("RGB").resize((ancho, alto), Image.LANCZOS))
    alto_fila = max(m.height for m in minis)
    filas = (len(minis) + columnas - 1) // columnas
    pad = 14
    hoja = Image.new(
        "RGB",
        (columnas * ancho + pad * (columnas + 1), filas * alto_fila + pad * (filas + 1)),
        (5, 6, 10),
    )
    for i, m in enumerate(minis):
        x = pad + (i % columnas) * (ancho + pad)
        y = pad + (i // columnas) * (alto_fila + pad)
        hoja.paste(m, (x, y))
    hoja.save(destino)
    return destino


def main():
    ap = argparse.ArgumentParser(description="Genera los flyers de Astronomy Academy.")
    ap.add_argument("--contenido", default=str(SKILL / "contenido/academy.json"))
    ap.add_argument("--salida", default=str(pathlib.Path.home() / "Desktop/Productoras/Astronomy/Flyers Academy"))
    ap.add_argument("--productos", help="IDs separados por coma. Default: todos.")
    ap.add_argument("--angulos", help="IDs separados por coma. Default: todos.")
    ap.add_argument("--formatos", default="feed,story,square")
    ap.add_argument("--estilo", default="editorial", choices=["editorial", "foto", "plano"],
                    help="editorial = el sistema real de @astronomy.academy (default). "
                         "foto / plano = variantes con el lenguaje de la app.")
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()

    cont = json.loads(pathlib.Path(args.contenido).read_text())
    plantilla = "editorial.html" if args.estilo == "editorial" else "flyer.html"
    template = (SKILL / "templates" / plantilla).read_text()
    assets = SKILL / "assets"

    precios_path = SKILL / "contenido/precios.json"
    if not precios_path.exists():
        sys.exit("Falta contenido/precios.json. Corré sync_precios.py antes de generar.")
    snap = json.loads(precios_path.read_text())
    planes = {p["id"]: p for p in snap["planes"]}

    formatos = [f.strip() for f in args.formatos.split(",") if f.strip()]
    for f in formatos:
        if f not in FORMATOS:
            sys.exit(f"Formato desconocido: {f}. Hay: {', '.join(FORMATOS)}")

    filtro_prod = {p.strip() for p in args.productos.split(",")} if args.productos else None
    filtro_ang = {a.strip() for a in args.angulos.split(",")} if args.angulos else None

    # Se chequea sobre el contenido entero, no sobre lo filtrado: la repetición es
    # una propiedad del producto, y generar un solo ángulo no la haría desaparecer.
    if args.estilo == "editorial":
        chequear_fotos(cont["productos"])

    # Cada estilo tiene su carpeta: la idea es poder comparar la tanda entera de uno
    # contra la del otro, no mezclarlas en el mismo directorio.
    salida = pathlib.Path(args.salida) / args.estilo
    trabajos = []
    for producto in cont["productos"]:
        if filtro_prod and producto["id"] not in filtro_prod:
            continue
        for angulo in producto["angulos"]:
            if filtro_ang and angulo["id"] not in filtro_ang:
                continue
            for fmt in formatos:
                destino = salida / producto["id"] / f"{angulo['id']}__{fmt}.png"
                if args.estilo == "editorial":
                    html = armar_html_editorial(template, cont["marca"], producto, angulo, fmt, planes, assets)
                else:
                    html = armar_html(template, cont["marca"], producto, angulo, fmt, planes, assets, args.estilo)
                trabajos.append((html, destino, fmt))

    if not trabajos:
        sys.exit("Cero piezas para generar: revisá los filtros --productos / --angulos.")

    print(f"Precios verificados el {snap['verificado']}.")
    print(f"Generando {len(trabajos)} piezas en {salida} ...\n")

    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futuros = {pool.submit(render, h, d, f): (d, f) for h, d, f in trabajos}
        for fut in concurrent.futures.as_completed(futuros):
            destino, fmt = futuros[fut]
            veredicto = fut.result()
            resultados.append((destino, fmt, verificar(destino, fmt, veredicto)))

    resultados.sort(key=lambda r: str(r[0]))
    malas = [(d, p) for d, _, p in resultados if p]
    for destino, _, problemas in resultados:
        marca = "  " if not problemas else "!!"
        print(f"{marca} {destino.relative_to(salida)}" + ("" if not problemas else f"   <- {'; '.join(problemas)}"))

    hoja = contacto([d for d, _, p in resultados if not p], salida / "_hoja-de-contacto.jpg")

    print(f"\n{len(resultados) - len(malas)}/{len(resultados)} piezas OK.")
    if hoja:
        print(f"Hoja de contacto: {hoja}")

    if malas:
        print(f"\n{len(malas)} piezas con problemas:")
        for destino, problemas in malas:
            print(f"  {destino.name}: {'; '.join(problemas)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
