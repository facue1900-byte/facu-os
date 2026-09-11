"""Mockups del cartel del local de Astronomy sobre la foto real de la fachada.

Genera version dia y version noche. La noche NO es la foto bajada de exposicion:
se le cambia el cielo por uno estrellado y se encienden las luces que existen en la
escena (los reflectores del poste, el bolardo del camino, el interior del local) y
la retroiluminacion de las letras corporeas.
"""
from PIL import Image, ImageFilter, ImageChops, ImageDraw
import numpy as np

W = "/private/tmp/claude-501/-Users-Facu-facu-os/53924761-26db-4e04-9a3b-88bacd306abd/scratchpad"
M = "/Users/Facu/facu-os/.claude/skills/flyers/assets/marca"
BASE = "/Users/Facu/facu-os/execution/assets/fachada-astronomy-sin-cartel.jpg"
SZ = (900, 1600)                       # ancho, alto

# --- piezas de marca -------------------------------------------------------
def asset(name):
    im = Image.open(f"{M}/{name}").convert("RGBA")
    a = np.array(im)[..., 3]
    ys, xs = np.nonzero(a > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

ISO, LOGO = asset("isotipo-blanco.png"), asset("logotipo-blanco.png")

def place(pieces):
    """pieces: (img, centro_x, top, alto) -> mascara L del cartel completo"""
    m = Image.new("L", SZ, 0)
    for img, cx, top, h in pieces:
        w = max(1, round(h * img.width / img.height))
        r = img.resize((w, h), Image.LANCZOS).split()[3]
        m.paste(r, (round(cx - w / 2), top), r)
    return m

# --- helpers de luz --------------------------------------------------------
YY, XX = np.mgrid[0:SZ[1], 0:SZ[0]].astype(np.float32)

def foco(cx, cy, rx, ry, dureza=2.2):
    """caida radial normalizada 0..1"""
    d = np.sqrt(((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2)
    return np.clip(1 - d, 0, 1) ** dureza

def sumar(img, luz, color, fuerza=1.0):
    """suma de luz que respeta el blanco: nunca quema, aclara lo que queda oscuro"""
    l = (luz * fuerza)[..., None] * np.array(color, np.float32)
    return img + l * (1 - img)

# --- cielo -----------------------------------------------------------------
def mascara_cielo(rgb):
    mx, mn = rgb.max(2), rgb.min(2)
    sat = np.where(mx > 0.01, (mx - mn) / np.maximum(mx, 1e-6), 0)
    lum = rgb.mean(2)
    m = ((lum > 0.55) & (sat < 0.20) & (YY < 815)).astype(np.float32)
    # se dilata 1px: el borde de transicion palmera/cielo queda del lado del cielo,
    # si no la hoja conserva su luminancia de dia y se ve un halo gris flotando
    m = np.array(Image.fromarray((m * 255).astype(np.uint8))
                 .filter(ImageFilter.MaxFilter(3))
                 .filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255
    return m

def cielo_estrellado(rng):
    g = np.linspace(0, 1, SZ[1], dtype=np.float32)[:, None]
    arriba = np.array([0.022, 0.031, 0.070], np.float32)
    horizonte = np.array([0.090, 0.115, 0.180], np.float32)
    cielo = arriba + (horizonte - arriba) * (g ** 1.6)
    cielo = np.repeat(cielo[:, None, :], SZ[0], 1) if cielo.ndim == 3 else cielo
    cielo = np.broadcast_to(cielo.reshape(SZ[1], 1, 3), (SZ[1], SZ[0], 3)).copy()

    # polvo de estrellas lejanas
    capa = Image.new("L", SZ, 0)
    d = ImageDraw.Draw(capa)
    for _ in range(620):
        x, y = rng.integers(0, SZ[0]), rng.integers(0, 900)
        b = int(rng.integers(45, 150) * (1 - y / 1400))
        d.point((x, y), fill=max(b, 0))
    # estrellas con cuerpo
    brillo = Image.new("L", SZ, 0)
    db = ImageDraw.Draw(brillo)
    for _ in range(90):
        x, y = rng.integers(0, SZ[0]), rng.integers(0, 760)
        r = rng.choice([0, 0, 1, 1, 2])
        b = int(rng.integers(150, 255) * (1 - y / 1500))
        db.ellipse([x - r, y - r, x + r, y + r], fill=b)
    halo = brillo.filter(ImageFilter.GaussianBlur(3.5))
    est = (np.array(capa, np.float32) + np.array(brillo, np.float32)
           + np.array(halo, np.float32) * 0.85) / 255
    cielo = cielo + np.clip(est, 0, 1.4)[..., None] * np.array([0.85, 0.88, 1.0], np.float32)
    return np.clip(cielo, 0, 1)

# --- render ----------------------------------------------------------------
def dia(mask, out):
    base = Image.open(BASE).convert("RGB")
    sh = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.55))
    base.paste(Image.new("RGB", base.size, (8, 9, 12)), (2, 4), sh)
    base.paste(Image.new("RGB", base.size, (247, 248, 250)), (0, 0), mask)
    base.save(out, quality=94)

def noche(mask, out, seed=7):
    rng = np.random.default_rng(seed)
    day = np.array(Image.open(BASE).convert("RGB"), np.float32) / 255

    # 1. cielo nocturno con estrellas, detras de palmeras y edificio
    sky = mascara_cielo(day)[..., None]
    img = day * (1 - sky) + cielo_estrellado(rng) * sky

    # 2. resplandor de ciudad sobre el horizonte, para que el cielo no sea negro plano
    img = sumar(img, foco(470, 700, 700, 260, 2.4) * sky[..., 0], (0.42, 0.34, 0.26), 0.30)

    # 3. la escena a oscuras: se conserva el contraste y se enfria la sombra.
    #    lo alto (copas, palma seca, poste) cae casi a silueta contra el cielo;
    #    el piso, que de noche igual recibe luz, se oscurece bastante menos.
    lum = img.mean(2, keepdims=True)
    silueta = (0.26 + 0.74 * np.clip((YY - 340) / 470, 0, 1))[..., None]
    escena = img * (0.24 + 0.15 * lum) * silueta \
        + np.array([0.018, 0.025, 0.048], np.float32) * (0.35 + 0.65 * lum) * silueta
    img = escena * (1 - sky * 0.94) + img * (sky * 0.94)

    # 4. reflectores del poste de la cancha
    for cx, cy in ((74, 320), (8, 372), (80, 378)):
        img = sumar(img, foco(cx, cy, 16, 12, 1.6), (1.0, 0.98, 0.92), 0.95)
        img = sumar(img, foco(cx, cy, 120, 100, 2.6), (0.72, 0.80, 1.0), 0.30)
    img = sumar(img, foco(60, 640, 340, 620, 3.0), (0.60, 0.70, 0.95), 0.13)

    # 5. interior del local: luz calida que se derrama al deck
    interior = foco(450, 985, 310, 160, 1.3) * np.clip((day.mean(2) - 0.08) * 3.0, 0, 1)
    img = sumar(img, interior, (1.0, 0.78, 0.48), 1.00)
    img = sumar(img, foco(450, 950, 250, 120, 2.2), (1.0, 0.72, 0.40), 0.30)
    img = sumar(img, foco(455, 1120, 280, 80, 2.0), (1.0, 0.76, 0.46), 0.34)

    # 6. bolardo del camino + el charco de luz en los adoquines
    img = sumar(img, foco(430, 1224, 13, 22, 1.3), (1.0, 0.88, 0.65), 1.0)
    img = sumar(img, foco(430, 1224, 70, 80, 2.4), (1.0, 0.82, 0.55), 0.38)
    img = sumar(img, foco(430, 1360, 190, 70, 2.2), (1.0, 0.84, 0.60), 0.34)
    img = sumar(img, foco(430, 1290, 430, 130, 2.8), (0.95, 0.85, 0.70), 0.14)

    # 7. letras corporeas: la luz escapa por detras, el frente queda opaco
    glow = np.zeros(SZ[::-1], np.float32)
    for radio, peso in ((6, 0.50), (14, 0.40), (34, 0.26), (80, 0.16)):
        d = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(radio))
        glow += np.array(d, np.float32) / 255 * peso
    img = sumar(img, np.clip(glow, 0, 1), (0.96, 0.97, 1.0), 1.05)

    night = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8))
    cuerpo = mask.filter(ImageFilter.MinFilter(3))
    canto = ImageChops.subtract(mask, cuerpo)
    night.paste(Image.new("RGB", SZ, (52, 53, 60)), (0, 0), cuerpo)
    night.paste(Image.new("RGB", SZ, (236, 240, 255)), (0, 0),
                canto.filter(ImageFilter.GaussianBlur(0.6)))
    night.save(out, quality=94)

if __name__ == "__main__":
    # v3: estrella mas grande, ASTRONOMY mas chico
    v3 = place([(ISO, 458, 620, 166), (LOGO, 472, 811, 42)])
    # v4: ASTRONOMY de punta a punta en la pared, estrella chica en la viga
    v4 = place([(LOGO, 455, 668, 64), (ISO, 472, 806, 32)])

    for nombre, m in (("v3", v3), ("v4", v4)):
        dia(m, f"{W}/{nombre}_dia.jpg")
        noche(m, f"{W}/{nombre}_noche.jpg")
    print("ok")
