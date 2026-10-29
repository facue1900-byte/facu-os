#!/usr/bin/env python3
"""Portada de un reel con la estética de la grilla de @astronomy.academy.

    .venv/bin/python active/astronomy/contenido/reels_diarios/portada.py SALIDA.jpg \
        --titular "LO QUE NADIE<br>TE MUESTRA" [--ceja "THE BUNKER"] \
        (--video VIDEO.mp4 --segundo 4.2 | --foto FOTO.jpg)

Usa la MISMA plantilla editorial que los flyers (skill `flyers`, templates/editorial.html):
foto desaturada y oscura, titular en mayúsculas abajo a la izquierda, rótulos mono, cruces y
el logo de dos círculos. Se arma la pieza 4:5 (1080x1350, lo que muestra la grilla) y se
monta centrada en un lienzo 9:16 (1080x1920) con la misma foto más oscura arriba y abajo:
así la grilla ve la pieza entera y la pantalla completa no muestra bandas.
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from comun import FF

FLYERS = pathlib.Path(__file__).resolve().parents[4] / ".claude/skills/flyers"
sys.path.insert(0, str(FLYERS / "scripts"))
import generar_flyers as gf  # noqa: E402  (render con Chrome headless + verificar)

W, H = 1080, 1920
Y_GRILLA = (H - 1350) // 2


def armar(salida, titular, ceja=None, video=None, segundo=None, foto=None):
    salida = pathlib.Path(salida)
    marca = gf.json.loads((FLYERS / "contenido/academy.json").read_text())["marca"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        if video:
            foto = tmp / "cuadro.jpg"
            subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(segundo), "-i", str(video),
                            "-frames:v", "1", "-q:v", "2", str(foto)], check=True)
        foto = pathlib.Path(foto)
        if not foto.exists():
            raise SystemExit(f"No existe la foto {foto}")
        # Chrome no lee HEIC ni respeta la rotación EXIF de todas las fotos: se normaliza a JPG.
        base = ImageOps.exif_transpose(Image.open(foto)).convert("RGB")
        limpia = tmp / "foto.jpg"
        base.save(limpia, quality=92)

        f = gf.FORMATOS["feed"]
        reemplazos = {
            "{{FONT_MONO}}": (FLYERS / "assets/fonts/RobotoMono.ttf").as_uri(),
            "{{W}}": str(f["w"]), "{{H}}": str(f["h"]), "{{BASE}}": str(f["base"]),
            "{{PAD}}": str(f["pad_ed"]), "{{PADX}}": str(f["padx_ed"]),
            "{{FONDO}}": f'<img class="foto" src="{limpia.as_uri()}" alt="">\n<div class="velo"></div>',
            "{{CLASE_BODY}}": "con-foto",
            "{{ROT_IZQ}}": gf.rotulos_html(marca["rotulos"]["izq"]),
            "{{ROT_DER}}": gf.rotulos_html(marca["rotulos"]["der"], alinear_derecha=True),
            "{{CEJA}}": f'<div class="ceja">({gf.esc(ceja)})</div>' if ceja else "",
            "{{CLASE_TITULAR}}": " xl" if len(titular.replace("<br>", "")) <= 22 else "",
            "{{TITULAR}}": titular,   # copy nuestro: admite <br> y <em>
            "{{SUB}}": "", "{{BLOQUE}}": "", "{{TAG}}": "<div></div>", "{{FLECHA}}": "&rarr;",
            "{{LEGAL}}": marca["legal_editorial"],
        }
        html = (FLYERS / "templates/editorial.html").read_text()
        for k, v in reemplazos.items():
            html = html.replace(k, v)
        pieza = tmp / "pieza.png"
        veredicto = gf.render(html, pieza, "feed")
        problemas = gf.verificar(pieza, "feed", veredicto)
        if problemas:
            raise SystemExit(f"Portada rechazada: {problemas}")

        # Lienzo 9:16: la misma foto, desaturada, oscura y desenfocada, con la pieza al centro.
        fondo = ImageOps.fit(base, (W, H))
        fondo = ImageEnhance.Color(fondo).enhance(0.25)
        fondo = ImageEnhance.Brightness(fondo).enhance(0.22).filter(ImageFilter.GaussianBlur(18))
        p = Image.open(pieza).convert("RGB")
        # Bordes de la pieza fundidos 40 px para que no se vea el corte contra el fondo.
        mascara = Image.new("L", p.size, 255)
        for i in range(40):
            v = int(255 * i / 40)
            for y in (i, p.height - 1 - i):
                mascara.paste(v, (0, y, p.width, y + 1))
        fondo.paste(p, (0, Y_GRILLA), mascara)
        salida.parent.mkdir(parents=True, exist_ok=True)
        fondo.save(salida, quality=90)
    print("PORTADA_OK", salida, veredicto)
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida")
    ap.add_argument("--titular", required=True)
    ap.add_argument("--ceja")
    ap.add_argument("--video")
    ap.add_argument("--segundo", type=float, default=1.0)
    ap.add_argument("--foto")
    a = ap.parse_args()
    if not (a.video or a.foto):
        ap.error("falta --video o --foto")
    armar(a.salida, a.titular, a.ceja, a.video, a.segundo, a.foto)


if __name__ == "__main__":
    main()
