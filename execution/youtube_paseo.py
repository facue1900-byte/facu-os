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
    """El 'pn' (sin la ®) como máscara, recortado al contorno."""
    im = Image.open(LOGO_PN)
    im.thumbnail((2400, 2400))
    g = np.asarray(im.convert("L"), np.float32)
    m = Image.fromarray(np.clip((g - 90) * 3, 0, 255).astype(np.uint8))
    m = m.crop(m.getbbox())
    # la ® es una mancha chica arriba a la derecha: se borra para que el relieve no la deforme
    a = np.asarray(m).copy()
    h, w = a.shape
    a[: int(h * 0.16), int(w * 0.88):] = 0
    m = Image.fromarray(a)
    m = m.crop(m.getbbox())
    return m.resize((round(m.width * alto / m.height), alto), Image.LANCZOS)


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
    franja = np.exp(-((yy - H / 2) / (H * 0.085)) ** 2)  # banda oscura detrás del texto
    k = (0.6 + 0.4 * vin) * (1 - 0.35 * centro) * (1 - 0.5 * franja)
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


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("perfil"); a.add_argument("--out", type=Path, required=True)
    b = sub.add_parser("banner"); b.add_argument("--out", type=Path, required=True)
    b.add_argument("--render", type=Path, default=RENDER)
    args = p.parse_args()
    perfil(args.out) if args.cmd == "perfil" else banner(args.out, args.render)
    print(args.out)


if __name__ == "__main__":
    main()
