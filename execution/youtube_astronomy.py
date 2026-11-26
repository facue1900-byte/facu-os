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


def _relieve(mask: Image.Image, bisel: float, ss: int):
    big = mask.resize((mask.width * ss, mask.height * ss), Image.LANCZOS)
    bisel = bisel * ss
    a = np.asarray(big, dtype=np.float32) / 255.0
    d = gaussian_filter(distance_transform_edt(a > 0.5), max(1.5, bisel * 0.12))
    t = np.clip(d / bisel, 0, 1)
    h = gaussian_filter(np.sqrt(1 - (1 - t) ** 2) * bisel, max(1.5, bisel * 0.1))
    gy, gx = np.gradient(h)
    n = np.dstack([-gx, -gy, np.ones_like(h) * 0.9])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return a, t, n[..., 0], n[..., 1], n[..., 2]


def vidrio(mask: Image.Image, bisel: float, ss: int = 3) -> Image.Image:
    """Cristal violeta: degradé de la paleta (lila → violeta → marino), canto brillante y reflejo."""
    a, t, nx, ny, nz = _relieve(mask, bisel, ss)
    alto = a.shape[0]
    yy = np.linspace(0, 1, alto)[:, None] * np.ones_like(a)
    stops = [0.0, 0.45, 1.0]
    cols = np.array([[205, 190, 255], [118, 70, 245], [34, 8, 96]], np.float32)
    base = np.dstack([np.interp(yy, stops, cols[:, k]) for k in range(3)])
    luz = np.array([-0.45, -0.7, 0.55]); luz /= np.linalg.norm(luz)
    ndl = np.clip(nx * luz[0] + ny * luz[1] + nz * luz[2], 0, 1)
    rgb = base * (0.55 + 0.6 * ndl[..., None])
    fres = np.clip(1 - nz, 0, 1) ** 1.3
    rgb += np.array([235, 225, 255], np.float32) * (fres * 0.9)[..., None]
    hv = luz + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
    spec = np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1) ** 90
    rgb += 255 * spec[..., None]
    # brillo de "vidrio": una franja suave en la mitad de arriba de la cara plana
    banda = np.clip(1 - np.abs(yy - 0.3) / 0.16, 0, 1) ** 2 * (t > 0.95)
    rgb += 255 * 0.22 * banda[..., None]
    alfa = a * (0.9 + 0.1 * fres)
    out = np.dstack([np.clip(rgb, 0, 255), alfa * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA").resize(mask.size, Image.LANCZOS)


def neon(mask: Image.Image, ancho: float, pad: int, ss: int = 2) -> Image.Image:
    """Tubo de neón siguiendo el contorno, como los carteles del Bunker. Devuelve con `pad` de margen."""
    m = ImageOps.expand(mask, pad, 0)
    big = m.resize((m.width * ss, m.height * ss), Image.LANCZOS)
    a = np.asarray(big, np.float32) / 255.0
    adentro = a > 0.5
    borde = distance_transform_edt(adentro) + distance_transform_edt(~adentro)
    w = ancho * ss
    tubo = np.clip(1 - borde / w, 0, 1) ** 0.6
    tubo_img = Image.fromarray((tubo * 255).astype(np.uint8)).resize(m.size, Image.LANCZOS)
    out = Image.new("RGBA", m.size, (0, 0, 0, 0))
    for radio, color, f in [(pad * 0.55, (110, 40, 255), 1.4), (pad * 0.22, (150, 90, 255), 1.6), (ancho * 1.5, (200, 170, 255), 1.5)]:
        out.alpha_composite(glow(tubo_img, color, radio, f))
    nucleo = Image.new("RGBA", m.size, (250, 246, 255, 0))
    nucleo.putalpha(tubo_img.point(lambda v: 255 if v > 150 else int(v * 1.2)))
    out.alpha_composite(nucleo)
    return out


def relieve(mask: Image.Image, estilo: str, bisel: float) -> Image.Image:
    if estilo == "vidrio":
        return vidrio(mask, bisel)
    return cromo(mask, bisel)


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


def perfil(out: Path, S: int = 1200, estilo: str = "vidrio"):
    img = fondo(S, S, centro=(0.5, 0.5), radio=0.62, intensidad=1.0)
    # sin anillos y estrella grande: el avatar se ve a 40-48 px en comentarios
    m = _mask_de_png(ISOTIPO, int(S * 0.76))
    _pegar_centrado(img, glow(m, VIOLETA, S * 0.05, 0.9, pad=int(S * 0.12)), S / 2, S / 2)
    if estilo == "neon":
        pad = int(S * 0.12)
        _pegar_centrado(img, neon(m, ancho=S * 0.013, pad=pad), S / 2, S / 2)
    else:
        _pegar_centrado(img, relieve(m, estilo, S * 0.022), S / 2, S / 2)
    img.convert("RGB").save(out)


def banner(out: Path, estilo: str = "vidrio"):
    W, H = 2560, 1440
    img = fondo(W, H, centro=(0.5, 0.5), radio=0.42, intensidad=1.0)
    d = ImageDraw.Draw(img)
    # zona segura 1546x423 centrada
    sx0, sy0 = (W - 1546) / 2, (H - 423) / 2
    sx1, sy1 = sx0 + 1546, sy0 + 423
    iso = _mask_de_png(ISOTIPO, 330)
    logo = _mask_de_png(LOGOTIPO, 78)
    gap = 150
    total = iso.width + gap + logo.width
    x_iso = W / 2 - total / 2 + iso.width / 2
    x_logo = x_iso + iso.width / 2 + gap + logo.width / 2
    hud(img, x_iso, H / 2, 132, color=(190, 190, 230, 40))
    _pegar_centrado(img, glow(iso, VIOLETA, 40, 0.8, pad=120), x_iso, H / 2)
    if estilo == "neon":
        _pegar_centrado(img, neon(iso, ancho=2.4, pad=110), x_iso, H / 2)
    else:
        _pegar_centrado(img, relieve(iso, estilo, 8), x_iso, H / 2)
    _pegar_centrado(img, plata(logo), x_logo, H / 2)
    # Rótulos de punta a punta (pedido de Facu 16/11: "MUSIC" chocaba con el anillo).
    # En desktop YouTube muestra el ancho entero (2560) y sólo 423 de alto; en celular sólo los 1546
    # del centro. Los rótulos van FUERA de esos 1546: en compu quedan en las puntas, en celular no
    # aparecen (enteros, nunca cortados a la mitad) y queda sólo el logo.
    mx = 150
    assert mx + 340 < sx0 and W - mx - 340 > sx1, "los rótulos tienen que quedar fuera de la zona del celular"
    rotulo(d, (mx, sy0 + 48), ["ASTRONOMY", "ACADEMY · EVENTS · MUSIC"], 22)
    rotulo(d, (W - mx, sy0 + 48), ["WHERE MUSIC", "CONNECTS US"], 22, anchor="ra")
    rotulo(d, (mx, sy1 - 108), ["NORDELTA, BA", "34°24'S 58°39'W"], 22)
    rotulo(d, (W - mx, sy1 - 108), ["[ THE BUNKER ]", "ASTRONOMYOFFICIAL.COM"], 22, anchor="ra")
    for x, y in [(mx - 40, sy0 + 22), (W - mx + 40, sy0 + 22), (mx - 40, sy1 - 22), (W - mx + 40, sy1 - 22)]:
        cruz(d, x, y, 14)
    img.convert("RGB").save(out)


def bunker(foto: Path, numero: int, artista: str, out: Path, foco: float = 0.5, brillo: float = 1.0,
           zoom: float = 1.0, foco_y: float = 0.35, estilo: str = "vidrio", color: bool = True,
           recortar_firma: bool = False, tag: str = "THE BUNKER",
           arriba: tuple = ("LIVE SET", "ASTRONOMY ACADEMY"), tam_nombre: int = 104, oscuro_abajo: float = 0.82):
    W, H = 1280, 720
    ph = Image.open(foto).convert("RGB")
    if recortar_firma:  # fotogramas del video traen la firma quemada abajo a la derecha
        ph = ph.crop((0, 0, int(ph.width * 0.9), int(ph.height * 0.9)))
    cw, ch = ph.width / zoom, ph.height / zoom
    x0 = (ph.width - cw) * foco
    y0 = (ph.height - ch) * foco_y
    ph = ph.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    ph = ImageOps.fit(ph, (W, H), Image.LANCZOS)
    if color:
        # color real del estudio (ya es violeta/magenta): curva en S y sombras hacia el marino
        c = np.asarray(ph, np.float32) / 255.0
        c = np.clip((c - 0.02) * 1.12 * brillo, 0, 1)
        c = c * c * (3 - 2 * c) * 0.5 + c * 0.5
        lum = c.mean(axis=2, keepdims=True)
        c = np.clip(lum + (c - lum) * 1.12, 0, 1)  # un toque más de saturación
        sombra = np.array([10, 2, 32], np.float32) / 255.0
        c = c + sombra * (1 - lum) * 0.6
        rgb = c * 255
    else:
        g = np.asarray(ImageOps.grayscale(ph), np.float32) / 255.0
        g = np.clip((g - 0.05) * 1.45 * brillo, 0, 1)
        g = g * g * (3 - 2 * g) * 0.6 + g * 0.4
        sombra = np.array([6, 2, 22], np.float32)
        luz = np.array([236, 238, 248], np.float32)
        rgb = sombra + (luz - sombra) * g[..., None]
    # viñeta y degradé inferior para el texto
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vin = np.clip(1 - (((xx - W * 0.5) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.8)) ** 2), 0.15, 1)
    abajo = np.clip((yy / H - 0.45) / 0.55, 0, 1) ** 1.3
    izq = np.clip(1 - xx / (W * 0.55), 0, 1) ** 1.5
    oscuro = np.clip(vin * (1 - oscuro_abajo * abajo) * (1 - 0.45 * izq * abajo), 0, 1)
    rgb = rgb * oscuro[..., None]
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    d = ImageDraw.Draw(img)
    pad = 56
    num = f"{numero:02d}"  # minimalista: va chico, en la línea de THE BUNKER (Facu: el número gigante era feo)
    # isotipo chico arriba a la izquierda
    iso = _mask_de_png(ISOTIPO, 92)
    _pegar_centrado(img, relieve(iso, estilo, 3), pad + iso.width / 2, pad + iso.height / 2)
    rotulo(d, (pad + iso.width + 18, pad + 22), ["ASTRONOMY"], 17, color=(255, 255, 255, 200))
    if any(arriba):  # vacío en colabs: arriba a la derecha va la marca de agua del otro
      rotulo(d, (W - pad, pad + 4), list(arriba), 17, anchor="ra", color=(255, 255, 255, 180))
    # tipografía: rótulo + artista, alineado a la izquierda y anclado abajo
    f_art = ImageFont.truetype(HELV, tam_nombre, index=1)
    nombre = artista.upper()
    while f_art.getlength(nombre) > W * 0.56 and f_art.size > 56:
        f_art = ImageFont.truetype(HELV, f_art.size - 4, index=1)
    y_base = H - pad - 6
    d.text((pad - 4, y_base), nombre, font=f_art, fill=(255, 255, 255, 255), anchor="ls")
    f_tag = ImageFont.truetype(HELV, 30, index=10)
    y_tag = y_base - f_art.size * 0.78 - 26
    d.text((pad, y_tag), tag, font=f_tag, fill=(255, 255, 255, 235), anchor="ls")
    if numero:  # 0 = sin número (colaboraciones fuera del ciclo The Bunker)
        x_l = pad + f_tag.getlength(tag) + 22
        d.line([(x_l, y_tag - 11), (x_l + 64, y_tag - 11)], fill=(200, 185, 255, 220), width=2)
        f_num = ImageFont.truetype(HELV, 30, index=7)  # Light
        d.text((x_l + 86, y_tag), num, font=f_num, fill=(215, 200, 255, 255), anchor="ls")
    borde_degrade(img, inset=18, grosor=3, glow_r=9)
    for x, y in [(30, 30), (W - 30, 30), (30, H - 30), (W - 30, H - 30)]:
        cruz(d, x, y, 9, color=(255, 255, 255, 120), ancho=1)
    img.convert("RGB").save(out, quality=93)


def especial(titulo: str, episodio: str, bajada: str, fecha: str, out: Path, estilo: str = "vidrio"):
    """Portada sin foto, tipográfica, para ciclos que no son The Bunker (ej. Free for All)."""
    W, H = 1280, 720
    img = fondo(W, H, centro=(0.72, 0.45), radio=0.6, intensidad=1.25, semilla=11)
    # aurora: dos manchas de color de la paleta, muy difusas
    aur = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    da = ImageDraw.Draw(aur)
    da.ellipse([700, -200, 1500, 520], fill=(118, 70, 245, 120))
    da.ellipse([-300, 380, 600, 1000], fill=(60, 20, 160, 110))
    img.alpha_composite(aur.filter(ImageFilter.GaussianBlur(140)))
    # estrella gigante de fondo, cortada por el borde derecho
    big = _mask_de_png(ISOTIPO, 900)
    estrella = relieve(big, estilo, 20)
    estrella.putalpha(estrella.getchannel("A").point(lambda v: int(v * 0.55)))
    _pegar_centrado(img, glow(big, VIOLETA, 60, 0.6, pad=150), 1010, 360)
    _pegar_centrado(img, estrella, 1010, 360)
    d = ImageDraw.Draw(img)
    pad = 64
    f = ImageFont.truetype(HELV, 150, index=9)  # Condensed Black
    lineas = titulo.upper().split()
    y = 120
    for l in lineas:
        d.text((pad - 6, y), l, font=f, fill=(255, 255, 255, 255), anchor="lt")
        y += 140
    f_ep = ImageFont.truetype(HELV, 34, index=10)
    d.text((pad, y + 30), f"{episodio.upper()}  —  {bajada.upper()}", font=f_ep, fill=(225, 215, 255, 255), anchor="lt")
    rotulo(d, (pad, pad - 18), ["ASTRONOMY ACADEMY"], 17, color=(255, 255, 255, 200))
    rotulo(d, (W - pad, pad - 18), [fecha.upper()], 17, anchor="ra", color=(255, 255, 255, 200))
    rotulo(d, (pad, H - pad), ["[ DJ SESSION ]"], 17, color=(255, 255, 255, 170))
    borde_degrade(img, inset=18, grosor=3, glow_r=9)
    for x, yy in [(30, 30), (W - 30, 30), (30, H - 30), (W - 30, H - 30)]:
        cruz(d, x, yy, 9, color=(255, 255, 255, 120), ancho=1)
    img.convert("RGB").save(out, quality=93)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("perfil")
    a.add_argument("--out", type=Path, required=True)
    a.add_argument("--estilo", default="vidrio", choices=["vidrio", "neon", "cromo"])
    b = sub.add_parser("banner")
    b.add_argument("--out", type=Path, required=True)
    b.add_argument("--estilo", default="vidrio", choices=["vidrio", "neon", "cromo"])
    e = sub.add_parser("especial")
    e.add_argument("--titulo", required=True)
    e.add_argument("--episodio", required=True)
    e.add_argument("--bajada", required=True)
    e.add_argument("--fecha", required=True)
    e.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("bunker")
    c.add_argument("--foto", type=Path, required=True)
    c.add_argument("--numero", type=int, required=True)
    c.add_argument("--artista", required=True)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--foco", type=float, default=0.5, help="0=izquierda 1=derecha, para el recorte")
    c.add_argument("--brillo", type=float, default=1.0)
    c.add_argument("--zoom", type=float, default=1.0, help=">1 acerca; da margen para mover el foco")
    c.add_argument("--foco-y", type=float, default=0.35)
    c.add_argument("--byn", action="store_true", help="foto en blanco y negro (Facu la prefiere en color)")
    c.add_argument("--tag", default="THE BUNKER", help="rótulo sobre el nombre (colabs: 'ASTRONOMY × MONKEY MUSIC')")
    c.add_argument("--arriba", default="LIVE SET|ASTRONOMY ACADEMY", help="rótulo arriba a la derecha, líneas separadas por |")
    c.add_argument("--tam-nombre", type=int, default=104, help="tamaño del nombre; más chico deja ver la consola")
    c.add_argument("--oscuro-abajo", type=float, default=0.82, help="0 = no oscurece la parte de abajo")
    c.add_argument("--recortar-firma", action="store_true", help="para fotogramas con la firma quemada")
    args = p.parse_args()
    if args.cmd == "perfil":
        perfil(args.out, estilo=args.estilo)
    elif args.cmd == "banner":
        banner(args.out, estilo=args.estilo)
    elif args.cmd == "especial":
        especial(args.titulo, args.episodio, args.bajada, args.fecha, args.out)
    else:
        bunker(args.foto, args.numero, args.artista, args.out, args.foco, args.brillo, args.zoom, args.foco_y,
               color=not args.byn, recortar_firma=args.recortar_firma,
               tag=args.tag, arriba=tuple(args.arriba.split("|")) if args.arriba else ("",),
               tam_nombre=args.tam_nombre, oscuro_abajo=args.oscuro_abajo)
    print(args.out)


if __name__ == "__main__":
    main()
