"""Perfil y banner del canal de YouTube de Paseo Nordelta (@PaseoNordelta).

Reusa el motor de relieve de `youtube_astronomy.py` con la marca del Paseo: monocromo (el "pn"
blanco sobre negro) y los renders fotorrealistas del proyecto como foto del banner.

  .venv/bin/python execution/youtube_paseo.py perfil --out perfil.png
  .venv/bin/python execution/youtube_paseo.py banner --out banner.png [--render RUTA]

OJO: el zip "Logotipos Paseo Nordelta.zip" del Desktop trae logos de NORDELTA PLAZA (otro negocio).
El "pn" bueno está en `Paseo Nordelta/Youtube/FotoPerfil-YouTube (3).png`.
Genera archivos; subirlos es aparte, con OK de Facu.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

import youtube_astronomy as ya

Image.MAX_IMAGE_PIXELS = None
PASEO = Path("/Users/Facu/Desktop/Paseo Nordelta")
LOGO_PN = PASEO / "Youtube/FotoPerfil-YouTube (3).png"
RENDER = PASEO / "Documentación/Obra /Renders/25-12-22_2 - Foto.jpg"


def mascara_pn(alto: int) -> Image.Image:
    """El 'pn' (sin la ®) como máscara limpia.

    Se parte del PNG de 9853 px reducido a 4000 (bordes suaves) y la ® se saca por componentes
    conexas, no con un recorte: el recorte rectangular le comía la esquina a la 'n' (16/11)."""
    from scipy.ndimage import label
    im = Image.open(LOGO_PN).convert("L")
    im = im.resize((4000, 4000), Image.LANCZOS)
    g = np.asarray(im, np.float32)
    m = np.clip((g - 60) / 140, 0, 1)  # antialias suave, sin escalones
    lab, n = label(m > 0.5)
    tam = np.bincount(lab.ravel()); tam[0] = 0
    grande = tam.max()
    chicos = [i for i in range(1, n + 1) if tam[i] < grande * 0.2]
    for i in chicos:  # la ® (círculo y letra) son manchas chicas
        zona = lab == i
        from scipy.ndimage import binary_dilation
        m[binary_dilation(zona, iterations=6)] = 0
    mi = Image.fromarray((m * 255).astype(np.uint8))
    mi = mi.crop(mi.getbbox())
    return mi.resize((round(mi.width * alto / mi.height), alto), Image.LANCZOS)


def blanco_relieve(mask: Image.Image, bisel: float, ss: int = 3) -> Image.Image:
    """Como el vidrio de Astronomy pero neutro: blanco porcelana con canto y reflejo."""
    a, t, nx, ny, nz = ya._relieve(mask, bisel, ss)
    yy = np.linspace(0, 1, a.shape[0])[:, None] * np.ones_like(a)
    base = np.dstack([np.interp(yy, [0, 0.5, 1], [255, 250, 232])] * 3)
    luz = np.array([-0.45, -0.7, 0.55]); luz /= np.linalg.norm(luz)
    ndl = np.clip(nx * luz[0] + ny * luz[1] + nz * luz[2], 0, 1)
    rgb = base * (0.8 + 0.3 * ndl[..., None])
    hv = luz + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
    rgb += 255 * (np.clip(nx * hv[0] + ny * hv[1] + nz * hv[2], 0, 1) ** 80)[..., None]
    out = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA").resize(mask.size, Image.LANCZOS)


def sombra(mask: Image.Image, radio: float, dy: int, fuerza: float = 0.7, pad: int = 80) -> Image.Image:
    m = ImageOps.expand(mask, pad, 0)
    s = Image.new("RGBA", m.size, (0, 0, 0, 0))
    s.putalpha(m.filter(ImageFilter.GaussianBlur(radio)).point(lambda v: int(v * fuerza)))
    out = Image.new("RGBA", (m.width, m.height + dy), (0, 0, 0, 0))
    out.alpha_composite(s, (0, dy))
    return out


def perfil(out: Path, S: int = 1200):
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    r = np.sqrt(((xx - S / 2) / S) ** 2 + ((yy - S * 0.45) / S) ** 2)
    v = np.clip(1 - r * 1.6, 0, 1) ** 1.5
    rgb = (14 + 34 * v)[..., None] * np.ones(3)  # negro con un foco gris suave arriba
    rng = np.random.default_rng(3)
    rgb += rng.normal(0, 2.5, (S, S, 1))
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    m = mascara_pn(int(S * 0.50))
    cx, cy = S / 2, S / 2
    sh = sombra(m, S * 0.02, int(S * 0.018), 0.85)
    img.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - (sh.height - S * 0.018) / 2)))
    pn = blanco_relieve(m, bisel=S * 0.016)
    img.alpha_composite(pn, (int(cx - pn.width / 2), int(cy - pn.height / 2)))
    img.convert("RGB").save(out)


def banner(out: Path, render: Path = RENDER):
    W, H = 2560, 1440
    ph = Image.open(render).convert("RGB")
    ph = ImageOps.fit(ph, (W, H), Image.LANCZOS, centering=(0.5, 0.5))
    c = np.asarray(ph, np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # oscurece el centro (donde va el logo) y los bordes, deja respirar el render
    centro = np.exp(-(((xx - W / 2) / (W * 0.33)) ** 2 + ((yy - H / 2) / (H * 0.2)) ** 2))
    vin = np.clip(1 - (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.7)) ** 2), 0, 1)
    # foto viva: nitidez + un poco de contraste; sólo se oscurece detrás del logo (sin franja gris:
    # el 16/11 la franja dejó el render turbio)
    k = (0.78 + 0.22 * vin) * (1 - 0.42 * centro)
    c = np.asarray(Image.fromarray(c.astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 90, 2)), np.float32)
    c = np.clip((c / 255 - 0.5) * 1.08 + 0.5, 0, 1) * 255
    c = c * k[..., None]
    img = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    # lockup centrado: pn + PASEO NORDELTA + bajada
    m = mascara_pn(190)
    f = ImageFont.truetype(ya.HELV, 92, index=10)
    titulo = "PASEO NORDELTA"
    track = 14
    ancho_t = sum(f.getlength(ch) for ch in titulo) + track * (len(titulo) - 1)
    gap = 70
    total = m.width + gap + ancho_t
    x0 = W / 2 - total / 2
    sh = sombra(m, 14, 8, 0.6, pad=40)
    img.alpha_composite(sh, (int(x0 - 40), int(H / 2 - m.height / 2 - 40)))
    img.alpha_composite(blanco_relieve(m, 5), (int(x0), int(H / 2 - m.height / 2)))
    x = x0 + m.width + gap
    y_t = H / 2 - 30
    for ch in titulo:
        d.text((x + 3, y_t + 4), ch, font=f, fill=(0, 0, 0, 110), anchor="ls")
        d.text((x, y_t), ch, font=f, fill=(255, 255, 255, 255), anchor="ls")
        x += f.getlength(ch) + track
    ya.rotulo(d, (x0 + m.width + gap + 4, y_t + 34), ["NORDELTA  ·  BUENOS AIRES"], 30,
              color=(240, 240, 240, 230))
    img.convert("RGB").save(out, quality=94)


def sesion(foto: Path, cancion: str, artista: str, out: Path, rotulo_sup: str = "EN VIVO EN PASEO NORDELTA"):
    """Portada de un video grabado en el Paseo: foto a color, texto a la derecha (el artista va a la izq)."""
    W, H = 1280, 720
    ph = ImageOps.fit(Image.open(foto).convert("RGB"), (W, H), Image.LANCZOS)
    c = np.asarray(ph.filter(ImageFilter.UnsharpMask(1.5, 60, 2)), np.float32) / 255
    c = np.clip((c - 0.5) * 1.08 + 0.5, 0, 1)
    lum = c.mean(axis=2, keepdims=True)
    c = np.clip(lum + (c - lum) * 1.15, 0, 1)  # un poco más de color
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    der = np.clip((xx / W - 0.42) / 0.58, 0, 1) ** 1.4      # oscurece la mitad derecha, donde va el texto
    abajo = np.clip((yy / H - 0.55) / 0.45, 0, 1) ** 1.5
    vin = np.clip(1 - (((xx - W / 2) / (W * 0.8)) ** 2 + ((yy - H / 2) / (H * 0.85)) ** 2), 0.35, 1)
    k = vin * (1 - 0.5 * der) * (1 - 0.35 * abajo)
    img = Image.fromarray((np.clip(c * k[..., None], 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    pad = 60
    xr = W - pad
    # arriba a la derecha: pn + rótulo
    m = mascara_pn(46)
    img.alpha_composite(blanco_relieve(m, 2), (int(xr - m.width), pad - 6))
    ya.rotulo(d, (xr - m.width - 16, pad + 8), [rotulo_sup], 17, anchor="ra", color=(255, 255, 255, 215))
    # título de la canción enorme, abajo a la derecha
    f_t = ImageFont.truetype(ya.HELV, 150, index=1)
    t = cancion.upper()
    while f_t.getlength(t) > W * 0.52 and f_t.size > 70:
        f_t = ImageFont.truetype(ya.HELV, f_t.size - 6, index=1)
    y_base = H - pad - 4
    d.text((xr + 3, y_base + 4), t, font=f_t, fill=(0, 0, 0, 120), anchor="rs")
    d.text((xr, y_base), t, font=f_t, fill=(255, 255, 255, 255), anchor="rs")
    f_a = ImageFont.truetype(ya.HELV, 36, index=10)
    a = artista.upper()
    tr = 6
    ancho = sum(f_a.getlength(ch) for ch in a) + tr * (len(a) - 1)
    x = xr - ancho
    y_a = y_base - f_t.size * 0.76 - 22
    for ch in a:
        d.text((x, y_a), ch, font=f_a, fill=(255, 255, 255, 240), anchor="ls")
        x += f_a.getlength(ch) + tr
    d.line([(xr - ancho, y_a + 14), (xr, y_a + 14)], fill=(255, 255, 255, 120), width=1)
    img.convert("RGB").save(out, quality=94)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("perfil"); a.add_argument("--out", type=Path, required=True)
    b = sub.add_parser("banner"); b.add_argument("--out", type=Path, required=True)
    b.add_argument("--render", type=Path, default=RENDER)
    c = sub.add_parser("sesion"); c.add_argument("--foto", type=Path, required=True)
    c.add_argument("--cancion", required=True); c.add_argument("--artista", required=True)
    c.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.cmd == "perfil":
        perfil(args.out)
    elif args.cmd == "banner":
        banner(args.out, args.render)
    else:
        sesion(args.foto, args.cancion, args.artista, args.out)
    print(args.out)


if __name__ == "__main__":
    main()
