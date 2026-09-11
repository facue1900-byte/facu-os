#!/usr/bin/env python3
"""Ficha comercial de un local del Paseo Nordelta.

Un JSON por local -> dos piezas, las dos autocontenidas (imágenes y CSS embebidos):

  <slug>.pdf      3 hojas A4 verticales, para mandar por WhatsApp.
  <slug>-story.png  1080x1920, para publicar como historia de Instagram.

El script NO calcula plata: los montos salen tal cual del JSON. Lo único que hace
con números es formatearlos. Ver 01-CONSTITUCION.md, regla 6.

  .venv/bin/python data/fichas-locales/build.py cafe pizzeria
"""
import base64
import json
import pathlib

import subprocess
import sys


BASE = pathlib.Path(__file__).parent
IMG = BASE / "img"
SALIDA = BASE / "salida"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}

CONTACTO = {
    "mail": "paseonordelta@gmail.com",
    "ig": "@paseonordelta",
    "web": "paseonordelta.com",
    "dir": "Av. de los Colegios 160, Nordelta, Tigre",
}


def datauri(nombre: str) -> str:
    for ext in (".jpg", ".png"):
        p = IMG / f"{nombre}{ext}"
        if p.exists():
            return f"data:{MIME[ext]};base64,{base64.b64encode(p.read_bytes()).decode()}"
    sys.exit(f"FALTA la imagen: {nombre}")


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- las hojas

def hoja_portada(d: dict) -> str:
    metas = "".join(
        f'<span>{m["k"]} <b>{m["v"]}</b></span>' for m in d["portada_meta"]
    )
    return f"""
<section class="hoja hoja--foto">
  <div class="foto"><img src="{datauri(d['portada_img'])}" alt="{esc(d['portada_alt'])}"></div>
  <div class="cota"><span>01 &middot; {esc(d['nombre'])}</span></div>
  <div class="portada__body">
    <img class="portada__logo" src="{datauri('logo')}" alt="Paseo Nordelta">
    <p class="chip"><i></i>{esc(d['disponibilidad'])}</p>
    <h1>{d['titulo']}</h1>
    <p class="lede">{d['bajada']}</p>
    <div class="portada__meta">{metas}</div>
  </div>
</section>"""


def hoja_local(d: dict) -> str:
    stats = "".join(
        f'<div class="stat{" stat--acc" if s.get("acc") else ""}">'
        f'<p class="stat__n">{s["n"]}<small>{s["u"]}</small></p>'
        f'<p class="stat__l">{s["l"]}</p></div>'
        for s in d["superficies"]
    )
    pl = d["plano"]
    if pl["tipo"] == "img":
        dibujo = (f'<div class="plano"><img src="{datauri(pl["src"])}" '
                  f'alt="{esc(pl["alt"])}"></div>'
                  f'<p class="plano__cap">{esc(pl["cap"])}</p>')
    else:
        dibujo = f'{pl["svg"]}<p class="plano__cap">{esc(pl["cap"])}</p>'
    puntos = "".join(f"<li>{p}</li>" for p in d["puntos"])
    n = len(d["superficies"])
    return f"""
<section class="hoja">
  <div class="cota"><span>02 &middot; El local</span></div>
  <div class="hoja__body">
    <p class="eyebrow">El local</p>
    <h2>{d['h_local']}</h2>
    <div class="stats{' stats--2' if n == 2 else ''}">{stats}</div>
    {dibujo}
    <ul class="puntos">{puntos}</ul>
  </div>
  <div class="pie"><span>Paseo Nordelta</span><span>{esc(d['nombre'])} &middot; Hoja 2 de 3</span></div>
</section>"""


def ubicador(d: dict, clase: str = "loca") -> str:
    """La aerea apagada con un foco de color encima del local.

    Dos copias de la MISMA imagen: la de abajo en gris y oscura, la de arriba a
    color recortada con un circulo sobre el local. La geometria es la del
    render; lo unico agregado es el foco, el aro y la etiqueta.
    """
    u = d["ubicador"]
    x, y, rx, ry = u["x"], u["y"], u["rx"], u["ry"]
    foco = f"ellipse({rx} {ry} at {x} {y})"
    return f"""
<div class="{clase}" style="--x:{x}; --y:{y}">
  <img class="loca__base" src="{datauri(u['img'])}" alt="">
  <img class="loca__hi" src="{datauri(u['img'])}"
       style="clip-path:{foco}; -webkit-clip-path:{foco}"
       alt="{esc(u['alt'])}">
  <span class="loca__vela"></span>
  <span class="loca__aro" style="left:{x}; top:{y};
        width:calc({rx} * 2); height:calc({ry} * 2)"></span>
  <span class="loca__tag"
        style="left:clamp(22%, {x}, 78%); top:calc({y} + {ry} + 4%)">{esc(u['tag'])}</span>
</div>"""


def hoja_cierre(d: dict) -> str:
    filas = "".join(
        f'<div class="cond__row"><p class="cond__k">{esc(c["k"])}</p>'
        f'<p class="cond__v">{c["v"]}</p><p class="cond__n">{c["n"]}</p></div>'
        for c in d["condiciones"]
    )
    return f"""
<section class="hoja">
  <div class="cota"><span>03 &middot; D&oacute;nde est&aacute; y cu&aacute;nto sale</span></div>
  <div class="hoja__body">
    <p class="eyebrow">D&oacute;nde est&aacute;</p>
    <h2>{d['h_cierre']}</h2>
    {ubicador(d)}
    <p class="loca__pie">{esc(d['mapa_ref'])}</p>
    <div class="cond">{filas}</div>
    <p class="nota">{d['nota']}</p>
    <div class="cta">
      <div><p class="cta__l">Escribinos</p>
        <p class="cta__v"><a href="mailto:{CONTACTO['mail']}">{CONTACTO['mail']}</a></p></div>
      <div><p class="cta__l">Instagram</p><p class="cta__v">{CONTACTO['ig']}</p></div>
      <div><p class="cta__l">D&oacute;nde</p><p class="cta__v">{CONTACTO['dir']}</p></div>
    </div>
  </div>
  <div class="pie"><span>{CONTACTO['web']}</span><span>{esc(d['nombre'])} &middot; Hoja 3 de 3</span></div>
</section>"""


def ficha_html(d: dict) -> str:
    css = (BASE / "estilo.css").read_text()
    cuerpo = hoja_portada(d) + hoja_local(d) + hoja_cierre(d)
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<title>{esc(d["nombre"])} &middot; Paseo Nordelta</title>'
            f'<style>{css}</style></head><body>{cuerpo}</body></html>')


# ---------------------------------------------------------------- la historia

def historia_html(d: dict) -> str:
    css = (BASE / "story.css").read_text()
    s = d["story"]
    pl = d["plano"]
    if pl["tipo"] == "img":
        dibujo = f'<div class="s-plano"><img src="{datauri(pl["src"])}" alt=""></div>'
    else:
        dibujo = f'<div class="s-svg">{pl["svg"]}</div>'
    datos = "".join(
        f'<div class="s-dato"><p class="s-dato__n">{x["n"]}<small>{x["u"]}</small></p>'
        f'<p class="s-dato__l">{x["l"]}</p></div>'
        for x in s["datos"]
    )
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{esc(d['nombre'])}</title><style>{css}</style></head><body>
<div class="story">
  <div class="s-bg"><img src="{datauri(d['portada_img'])}" alt=""></div>
  <div class="s-body">
    <img class="s-logo" src="{datauri('logo')}" alt="Paseo Nordelta">
    <p class="s-chip">{esc(d['disponibilidad'])}</p>
    <h1 class="s-h1">{s['titulo']}</h1>
    <p class="s-lede">{s['bajada']}</p>
    {dibujo}
    <div class="s-datos">{datos}</div>
    <div class="s-cta">
      <p class="s-cta__l">{esc(s['cta_l'])}</p>
      <p class="s-cta__v">{CONTACTO['mail']}</p>
    </div>
  </div>
</div></body></html>"""


def historia_ubicacion_html(d: dict) -> str:
    """Segunda historia: solo donde esta el local dentro del paseo."""
    css = (BASE / "story.css").read_text()
    s = d["story2"]
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{esc(d['nombre'])} &middot; d&oacute;nde est&aacute;</title><style>{css}</style></head><body>
<div class="story">
  <div class="s-bg"><img src="{datauri(d['portada_img'])}" alt=""></div>
  <div class="s-body s-body--loca">
    <img class="s-logo" src="{datauri('logo')}" alt="Paseo Nordelta">
    <p class="s-chip">D&oacute;nde est&aacute;</p>
    <h1 class="s-h1">{s['titulo']}</h1>
    <p class="s-lede">{s['bajada']}</p>
    {ubicador(d, "s-loca s-loca--grande")}
    <div class="s-cta">
      <p class="s-cta__l">{esc(d['story']['cta_l'])}</p>
      <p class="s-cta__v">{CONTACTO['mail']}</p>
    </div>
  </div>
</div></body></html>"""


# ---------------------------------------------------------------- render

def chrome(args: list[str], destino: pathlib.Path) -> None:
    """Render con el Chrome de /Applications, headless.

    NUNCA agregarle --user-data-dir: en esta Mac cuelga el proceso para siempre.
    Es la misma trampa que documenta el skill `flyers`.
    """
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"No está Chrome en {CHROME}: sin PDF ni PNG, queda el HTML.")
    destino.unlink(missing_ok=True)
    r = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
         "--virtual-time-budget=6000"] + args,
        capture_output=True, text=True, timeout=180)
    if not destino.exists() or destino.stat().st_size == 0:
        sys.exit(f"Chrome no escribió {destino} (código {r.returncode}):\n"
                 f"{r.stderr[-1500:]}")


def main(slugs: list[str]) -> None:
    SALIDA.mkdir(exist_ok=True)
    for slug in slugs:
        fuente = BASE / f"{slug}.json"
        if not fuente.exists():
            sys.exit(f"FALTA el JSON del local: {fuente}")
        d = json.loads(fuente.read_text())

        html = SALIDA / f"{slug}.html"
        html.write_text(ficha_html(d))
        pdf = SALIDA / f"{slug}.pdf"
        chrome(["--print-to-pdf-no-header", f"--print-to-pdf={pdf}",
                html.as_uri()], pdf)

        shtml = SALIDA / f"{slug}-story.html"
        shtml.write_text(historia_html(d))
        png = SALIDA / f"{slug}-story.png"
        chrome(["--window-size=1080,1920", "--force-device-scale-factor=1",
                f"--screenshot={png}", shtml.as_uri()], png)

        s2html = SALIDA / f"{slug}-story-2.html"
        s2html.write_text(historia_ubicacion_html(d))
        png2 = SALIDA / f"{slug}-story-2.png"
        chrome(["--window-size=1080,1920", "--force-device-scale-factor=1",
                f"--screenshot={png2}", s2html.as_uri()], png2)

        verificar(pdf, png, slug)
        verificar_historia(png2, f"{slug} (historia 2)")
        for f in (pdf, png, png2):
            print(f"{slug:<10} {f.name:<22} {f.stat().st_size/1024:>6.0f} KB")


def verificar(pdf: pathlib.Path, png: pathlib.Path, slug: str) -> None:
    """Que el archivo exista no alcanza: se abren y se miran.

    El PDF tiene que traer 3 hojas A4 verticales con texto adentro, y el PNG
    tiene que medir 1080x1920 exactos y no ser una placa de un solo color.
    """
    import fitz
    doc = fitz.open(pdf)
    if len(doc) != 3:
        sys.exit(f"{slug}: el PDF salió con {len(doc)} hojas, tienen que ser 3")
    for i, p in enumerate(doc, 1):
        ancho, alto = round(p.rect.width), round(p.rect.height)
        if (ancho, alto) != (595, 842):
            sys.exit(f"{slug}: la hoja {i} mide {ancho}x{alto} pt, no A4 vertical")
        if len(p.get_text().strip()) < 40:
            sys.exit(f"{slug}: la hoja {i} salió casi sin texto")
    doc.close()

    verificar_historia(png, slug)


def verificar_historia(png: pathlib.Path, quien: str) -> None:
    import fitz
    pix = fitz.Pixmap(str(png))
    if (pix.width, pix.height) != (1080, 1920):
        sys.exit(f"{quien}: la historia mide {pix.width}x{pix.height}, no 1080x1920")
    muestra = {pix.pixel(x, y) for x in range(0, pix.width, 60)
               for y in range(0, pix.height, 60)}
    if len(muestra) < 50:
        sys.exit(f"{quien}: la historia salió casi lisa ({len(muestra)} colores)")


if __name__ == "__main__":
    main(sys.argv[1:] or ["cafe", "pizzeria"])
