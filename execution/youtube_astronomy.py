"""Piezas del canal de YouTube de Astronomy: foto de perfil, banner y portadas de The Bunker.

Estética: la del manual de identidad (Marca Astronomy/Branding/AstronomyIDENTIDAD.pdf):
isotipo en cromo/plata con relieve, negro, azul marino #180040, Helvetica Neue + Roboto Mono,
cruces de registro y micro-rótulos mono como el Instagram de @astronomy.academy.

El cromo se calcula, no es un filtro: mapa de altura desde la distancia al borde del logo,
normales, y reflexión contra un "cielo" de estudio (gradiente con línea de horizonte).

Uso (siempre con el Python del venv):
  .venv/bin/python execution/youtube_astronomy.py perfil  --out perfil.png
  .venv/bin/python execution/youtube_astronomy.py banner  --out banner.png
  .venv/bin/python execution/youtube_astronomy.py bunker  --foto frame.jpg --numero 5 \
      --artista "NOMBRE" --out portada.jpg [--foco 0.5]

No sube nada a YouTube: genera archivos. Subirlos es un paso aparte, con OK de Facu.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from scipy.ndimage import distance_transform_edt, gaussian_filter

MARCA = Path("/Users/Facu/Desktop/Productoras/Astronomy/Marca Astronomy/Logos")
ISOTIPO = MARCA / "Isotipo/PNG/Isotipo Blanco Large.png"
LOGOTIPO = MARCA / "Logotipo/PNG/Logotipo Blanco.png"
HELV = "/System/Library/Fonts/HelveticaNeue.ttc"  # 1 Bold, 4 Condensed Bold, 9 Condensed Black, 10 Medium
MONO = Path(__file__).resolve().parents[1] / ".claude/skills/flyers/assets/fonts/RobotoMono.ttf"

NEGRO = (0, 0, 0)
MARINO = (24, 0, 64)  # #180040, paleta oficial
VIOLETA = (92, 52, 214)  # brillo del marino, sólo para glow y bordes
PLATA = (214, 218, 232)


# ---------------------------------------------------------------- cromo


def _mask_de_png(path: Path, alto: int) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    a = a.crop(a.getbbox())
    ancho = round(a.width * alto / a.height)
    return a.resize((ancho, alto), Image.LANCZOS)


def _mask_de_texto(texto: str, alto_px: int, font_index: int = 1, tracking: float = 0.0) -> Image.Image:
    f = ImageFont.truetype(HELV, alto_px, index=font_index)
    letras = [(c, f.getbbox(c)) for c in texto]
    total = sum(f.getlength(c) for c in texto) + tracking * alto_px * (len(texto) - 1)
    lienzo = Image.new("L", (int(total + alto_px), int(alto_px * 1.5)), 0)
    d = ImageDraw.Draw(lienzo)
    x = alto_px * 0.5
    for c, _ in letras:
        d.text((x, alto_px * 0.25), c, font=f, fill=255)
        x += f.getlength(c) + tracking * alto_px
    return lienzo.crop(lienzo.getbbox())


def _env(e: np.ndarray) -> np.ndarray:
    """Cielo de estudio: suelo oscuro, horizonte brillante, banda negra, cielo blanco."""
    xs = [-1.6, -0.7, -0.25, -0.04, 0.0, 0.05, 0.18, 0.45, 0.8, 1.6]
    ys = [0.05, 0.22, 0.55, 0.98, 1.00, 0.02, 0.06, 0.45, 0.95, 1.0]
    return np.interp(e, xs, ys)


def cromo(mask: Image.Image, bisel: float, inclinacion: float = 0.9, ss: int = 3) -> Image.Image:
    """Devuelve RGBA con la máscara convertida en metal pulido con relieve.

    Se calcula a `ss`x y se reduce: sin eso las puntas finas salen rayadas."""
    big = mask.resize((mask.width * ss, mask.height * ss), Image.LANCZOS)
    bisel = bisel * ss
    a = np.asarray(big, dtype=np.float32) / 255.0
    adentro = a > 0.5
    d = distance_transform_edt(adentro)
    d = gaussian_filter(d, max(1.5, bisel * 0.12))
    t = np.clip(d / bisel, 0, 1)
    h = np.sqrt(1 - (1 - t) ** 2) * bisel  # perfil redondeado
    h = gaussian_filter(h, max(1.5, bisel * 0.1))
    gy, gx = np.gradient(h)
    n = np.dstack([-gx, -gy, np.ones_like(h) * 0.9])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    nx, ny, nz = n[..., 0], n[..., 1], n[..., 2]
    # reflexión de la vista (0,0,1)
    rx, ry = 2 * nz * nx, 2 * nz * ny
    alto, ancho = a.shape
    yy = np.linspace(-1, 1, alto)[:, None]
    xx = np.linspace(-1, 1, ancho)[None, :]
    e = -ry * 1.4 + 0.25 * rx - yy * inclinacion * 0.55 + xx * 0.08
    lum = _env(e)
    luz = np.array([-0.45, -0.65, 0.62])
    luz /= np.linalg.norm(luz)
    spec = np.clip(nx * luz[0] + ny * luz[1] + nz * luz[2], 0, 1) ** 60
    lum = np.clip(lum + spec * 0.9, 0, 1)
    # oclusión suave en el canto interior
    lum *= 0.82 + 0.18 * t
    # color: sombras hacia el marino, medios plata fría, altas blancas
    stops = np.array([0.0, 0.35, 0.75, 1.0])
    cols = np.array([[6, 4, 16], [64, 60, 92], [200, 203, 216], [255, 255, 255]], dtype=np.float32)
    rgb = np.dstack([np.interp(lum, stops, cols[:, k]) for k in range(3)])
    out = np.dstack([rgb, a * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA").resize(mask.size, Image.LANCZOS)


def plata(mask: Image.Image) -> Image.Image:
    """Relleno plata plano (para trazos finos, donde el cromo ensucia)."""
    h = mask.height
    t = np.linspace(0, 1, h)[:, None]
    lum = np.interp(t, [0, 0.48, 0.52, 1], [1.0, 0.86, 0.66, 0.92])
    rgb = np.dstack([lum * 236, lum * 238, lum * 250]) * np.ones((1, mask.width, 1))
    out = np.dstack([rgb, np.asarray(mask, np.float32)]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def glow(mask: Image.Image, color, radio: float, fuerza: float = 1.0, pad: int = 0) -> Image.Image:
    m = ImageOps.expand(mask, pad, 0) if pad else mask
    g = m.filter(ImageFilter.GaussianBlur(radio))
    arr = np.asarray(g, dtype=np.float32) * fuerza
    capa = Image.new("RGBA", m.size, color + (0,))
    capa.putalpha(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)))
    return capa


# ---------------------------------------------------------------- fondo y adornos


def fondo(w: int, h: int, centro=(0.5, 0.55), radio=0.75, intensidad=1.0, semilla=7) -> Image.Image:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = centro[0] * w, centro[1] * h
    r = np.sqrt(((xx - cx) / (w * radio)) ** 2 + ((yy - cy) / (h * radio)) ** 2)
    k = np.clip(1 - r, 0, 1) ** 1.6 * intensidad
    base = np.array(NEGRO, np.float32)
    mar = np.array(MARINO, np.float32) * 1.9
    rgb = base + (mar - base) * k[..., None]
    rng = np.random.default_rng(semilla)
    rgb += rng.normal(0, 3.2, (h, w, 1))  # grano de película
    # estrellas: pocas, finas
    n = int(w * h / 9000)
    sx, sy = rng.integers(0, w, n), rng.integers(0, h, n)
    br = rng.uniform(40, 160, n)
    rgb[sy, sx] += br[:, None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def cruz(d: ImageDraw.ImageDraw, x, y, s, color=(255, 255, 255, 150), ancho=2):
    d.line([(x - s, y), (x + s, y)], fill=color, width=ancho)
    d.line([(x, y - s), (x, y + s)], fill=color, width=ancho)


def rotulo(d, xy, lineas, tam, color=(255, 255, 255, 170), anchor="la", interlinea=1.35):
    f = ImageFont.truetype(str(MONO), tam)
    x, y = xy
    for i, l in enumerate(lineas):
        d.text((x, y + i * tam * interlinea), l, font=f, fill=color, anchor=anchor)


def hud(capa: Image.Image, cx, cy, r, color=(200, 200, 230, 46)):
    d = ImageDraw.Draw(capa)
    for k, rr in enumerate([r, r * 0.72, r * 1.18]):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color, width=2 if k == 0 else 1)
    for ang in range(0, 360, 6):
        a = np.radians(ang)
        l = 18 if ang % 30 == 0 else 8
        x0, y0 = cx + np.cos(a) * r, cy + np.sin(a) * r
        x1, y1 = cx + np.cos(a) * (r - l), cy + np.sin(a) * (r - l)
        d.line([(x0, y0), (x1, y1)], fill=color, width=1)


def borde_degrade(img: Image.Image, inset: int, grosor: int, glow_r: float = 10):
    """Marco fino con degradé marino → violeta → plata, con brillo."""
    w, h = img.size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle([inset, inset, w - inset, h - inset], outline=255, width=grosor)
    t = np.linspace(0, 1, w)[None, :] * 0.7 + np.linspace(0, 1, h)[:, None] * 0.3
    stops = [0, 0.45, 1]
    cols = np.array([MARINO, VIOLETA, PLATA], np.float32) * np.array([[2.2], [1.0], [1.0]])
    cols = np.clip(cols, 0, 255)
    rgb = np.dstack([np.interp(t, stops, cols[:, k]) for k in range(3)]).astype(np.uint8)
    col = Image.fromarray(rgb, "RGB").convert("RGBA")
    brillo = col.copy()
    brillo.putalpha(m.filter(ImageFilter.GaussianBlur(glow_r)).point(lambda v: min(255, v * 3)))
    linea = col.copy()
    linea.putalpha(m)
    img.alpha_composite(brillo)
    img.alpha_composite(linea)


def _pegar_centrado(img, capa, cx, cy):
    img.alpha_composite(capa, (int(cx - capa.width / 2), int(cy - capa.height / 2)))


# ---------------------------------------------------------------- piezas


def perfil(out: Path, S: int = 1200):
    img = fondo(S, S, centro=(0.5, 0.5), radio=0.62, intensidad=1.0)
    hud(img, S / 2, S / 2, S * 0.40, color=(190, 190, 230, 26))
    m = _mask_de_png(ISOTIPO, int(S * 0.64))
    _pegar_centrado(img, glow(m, VIOLETA, S * 0.05, 0.9, pad=int(S * 0.12)), S / 2, S / 2)
    _pegar_centrado(img, cromo(m, bisel=S * 0.022), S / 2, S / 2)
    img.convert("RGB").save(out)


def banner(out: Path):
    W, H = 2560, 1440
    img = fondo(W, H, centro=(0.5, 0.5), radio=0.42, intensidad=1.0)
    d = ImageDraw.Draw(img)
    # zona segura 1546x423 centrada
    sx0, sy0 = (W - 1546) / 2, (H - 423) / 2
    sx1, sy1 = sx0 + 1546, sy0 + 423
    iso = _mask_de_png(ISOTIPO, 330)
    logo = _mask_de_png(LOGOTIPO, 70)
    logo = logo.resize((int(logo.width * 1.0), logo.height), Image.LANCZOS)
    gap = 120
    total = iso.width + gap + logo.width
    x_iso = W / 2 - total / 2 + iso.width / 2
    x_logo = x_iso + iso.width / 2 + gap + logo.width / 2
    hud(img, x_iso, H / 2, 138, color=(190, 190, 230, 40))
    _pegar_centrado(img, glow(iso, VIOLETA, 40, 0.8, pad=120), x_iso, H / 2)
    _pegar_centrado(img, cromo(iso, bisel=8), x_iso, H / 2)
    _pegar_centrado(img, plata(logo), x_logo, H / 2)
    # micro-rótulos dentro de la zona segura, como el IG de Academy
    rotulo(d, (sx0 + 10, sy0 + 10), ["ASTRONOMY", "ACADEMY · EVENTS · MUSIC"], 22)
    rotulo(d, (sx1 - 10, sy0 + 10), ["WHERE MUSIC", "CONNECTS US"], 22, anchor="ra")
    rotulo(d, (sx0 + 10, sy1 - 52), ["NORDELTA, BA", "34°24'S 58°39'W"], 22)
    rotulo(d, (sx1 - 10, sy1 - 52), ["[ THE BUNKER ]", "ASTRONOMYOFFICIAL.COM"], 22, anchor="ra")
    for x, y in [(sx0 - 30, sy0 - 30), (sx1 + 30, sy0 - 30), (sx0 - 30, sy1 + 30), (sx1 + 30, sy1 + 30)]:
        cruz(d, x, y, 14)
    img.convert("RGB").save(out)


def bunker(foto: Path, numero: int, artista: str, out: Path, foco: float = 0.5, brillo: float = 1.0,
           zoom: float = 1.0, foco_y: float = 0.35):
    W, H = 1280, 720
    ph = Image.open(foto).convert("RGB")
    # recorte 16:9 enfocado; se recorta un 10% abajo-derecha para matar la firma quemada
    ph = ph.crop((0, 0, int(ph.width * 0.9), int(ph.height * 0.9)))
    cw, ch = ph.width / zoom, ph.height / zoom
    x0 = (ph.width - cw) * foco
    y0 = (ph.height - ch) * foco_y
    ph = ph.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    ph = ImageOps.fit(ph, (W, H), Image.LANCZOS)
    # monocromo con un tinte marino en las sombras (dúotono)
    g = np.asarray(ImageOps.grayscale(ph), np.float32) / 255.0
    g = np.clip((g - 0.05) * 1.45 * brillo, 0, 1)
    g = g * g * (3 - 2 * g) * 0.6 + g * 0.4  # curva en S: más contraste
    sombra = np.array([6, 2, 22], np.float32)
    luz = np.array([236, 238, 248], np.float32)
    rgb = sombra + (luz - sombra) * g[..., None]
    # viñeta y degradé inferior para el texto
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vin = np.clip(1 - (((xx - W * 0.5) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2), 0.15, 1)
    abajo = np.clip((yy / H - 0.45) / 0.55, 0, 1) ** 1.3
    izq = np.clip(1 - xx / (W * 0.55), 0, 1) ** 1.5
    oscuro = np.clip(vin * (1 - 0.82 * abajo) * (1 - 0.45 * izq * abajo), 0, 1)
    rgb = rgb * oscuro[..., None]
    # glow marino desde abajo-derecha, detrás del número
    gl = np.clip(1 - np.sqrt(((xx - W * 0.82) / (W * 0.45)) ** 2 + ((yy - H * 0.78) / (H * 0.6)) ** 2), 0, 1) ** 2
    rgb += np.array(VIOLETA, np.float32) * gl[..., None] * 0.35
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    d = ImageDraw.Draw(img)
    pad = 56
    # número cromado gigante, abajo a la derecha
    num = f"{numero:02d}"
    m = _mask_de_texto(num, 330, font_index=9, tracking=-0.02)
    nx, ny = W - pad - m.width / 2 + 6, H - pad - m.height / 2 + 4
    _pegar_centrado(img, glow(m, VIOLETA, 26, 0.75, pad=80), nx, ny)
    _pegar_centrado(img, cromo(m, bisel=9, inclinacion=0.7), nx, ny)
    # isotipo cromado chico arriba a la izquierda
    iso = _mask_de_png(ISOTIPO, 92)
    _pegar_centrado(img, cromo(iso, bisel=3), pad + iso.width / 2, pad + iso.height / 2)
    rotulo(d, (pad + iso.width + 18, pad + 22), ["ASTRONOMY", "ACADEMY"], 17, color=(255, 255, 255, 200))
    rotulo(d, (W - pad, pad + 4), ["LIVE SET", "NORDELTA, BA"], 17, anchor="ra", color=(255, 255, 255, 180))
    # tipografía: rótulo + artista, alineado a la izquierda y anclado abajo
    f_art = ImageFont.truetype(HELV, 104, index=1)
    nombre = artista.upper()
    while f_art.getlength(nombre) > W * 0.56 and f_art.size > 56:
        f_art = ImageFont.truetype(HELV, f_art.size - 4, index=1)
    y_base = H - pad - 6
    d.text((pad - 4, y_base), nombre, font=f_art, fill=(255, 255, 255, 255), anchor="ls")
    f_tag = ImageFont.truetype(HELV, 30, index=10)
    y_tag = y_base - f_art.size * 0.78 - 26
    d.text((pad, y_tag), "THE BUNKER", font=f_tag, fill=(255, 255, 255, 235), anchor="ls")
    borde_degrade(img, inset=18, grosor=3, glow_r=9)
    for x, y in [(30, 30), (W - 30, 30), (30, H - 30), (W - 30, H - 30)]:
        cruz(d, x, y, 9, color=(255, 255, 255, 120), ancho=1)
    img.convert("RGB").save(out, quality=93)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("perfil")
    a.add_argument("--out", type=Path, required=True)
    b = sub.add_parser("banner")
    b.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("bunker")
    c.add_argument("--foto", type=Path, required=True)
    c.add_argument("--numero", type=int, required=True)
    c.add_argument("--artista", required=True)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--foco", type=float, default=0.5, help="0=izquierda 1=derecha, para el recorte")
    c.add_argument("--brillo", type=float, default=1.0)
    c.add_argument("--zoom", type=float, default=1.0, help=">1 acerca; da margen para mover el foco")
    c.add_argument("--foco-y", type=float, default=0.35)
    args = p.parse_args()
    if args.cmd == "perfil":
        perfil(args.out)
    elif args.cmd == "banner":
        banner(args.out)
    else:
        bunker(args.foto, args.numero, args.artista, args.out, args.foco, args.brillo, args.zoom, args.foco_y)
    print(args.out)


if __name__ == "__main__":
    main()
