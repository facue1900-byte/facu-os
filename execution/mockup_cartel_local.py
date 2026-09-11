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
    """la fuente misma: el bulbo y su halo en el aire. Nunca quema."""
    l = (luz * fuerza)[..., None] * np.array(color, np.float32)
    return img + l * (1 - img)

def iluminar(img, day, luz, color, fuerza=1.0):
    """una superficie iluminada devuelve SU color, no el de la lampara.
    Por eso la luz sobre materia se multiplica por la foto de dia en vez de
    sumarse en blanco: sumando, el arbusto verde termina gris claro."""
    l = (luz * fuerza)[..., None] * np.array(color, np.float32)
    return np.clip(img + day * l, 0, 1)

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

def cielo_nocturno(rng):
    """azul profundo con degrade, no negro: asi se ve un cielo de barrio iluminado"""
    g = (np.linspace(0, 1, SZ[1], dtype=np.float32) ** 1.5).reshape(SZ[1], 1, 1)
    arriba = np.array([0.030, 0.050, 0.105], np.float32)
    horizonte = np.array([0.085, 0.125, 0.205], np.float32)
    cielo = np.broadcast_to(arriba + (horizonte - arriba) * g, (SZ[1], SZ[0], 3)).copy()

    est = Image.new("L", SZ, 0)
    d = ImageDraw.Draw(est)
    for _ in range(120):
        x, y = rng.integers(0, SZ[0]), rng.integers(0, 620)
        d.point((x, y), fill=int(rng.integers(35, 105) * (1 - y / 1100)))
    e = np.array(est, np.float32) / 255
    e = e + np.array(Image.fromarray((e * 255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(1.4)), np.float32) / 255 * 0.6
    return np.clip(cielo + e[..., None] * np.array([0.9, 0.93, 1.0], np.float32), 0, 1)

# --- render ----------------------------------------------------------------
def dia(mask, out):
    base = Image.open(BASE).convert("RGB")
    sh = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.55))
    base.paste(Image.new("RGB", base.size, (8, 9, 12)), (2, 4), sh)
    base.paste(Image.new("RGB", base.size, (247, 248, 250)), (0, 0), mask)
    base.save(out, quality=94)

def noche(mask, out, seed=7):
    """La noche no es la foto apagada: es contraste. Negro donde no llega nada,
    y calido saturado en todo lo que tiene una luminaria cerca."""
    rng = np.random.default_rng(seed)
    day = np.array(Image.open(BASE).convert("RGB"), np.float32) / 255

    # 1. cielo
    sky = mascara_cielo(day)[..., None]
    img = day * (1 - sky) + cielo_nocturno(rng) * sky

    # nada ilumina la copa de las palmeras ni la hoja seca que cuelga a 8 m. Sin este
    # tope quedan flotando en amarillo contra el cielo, y ademas los uplights del piso
    # les llegarian como si la luz no perdiera fuerza con la altura.
    bajo = np.clip((YY - 530) / 140, 0, 1).astype(np.float32)

    # 2. la escena arranca casi a oscuras; la luz se agrega despues, luminaria
    #    por luminaria, en vez de dejar la foto de dia con menos exposicion
    lum = img.mean(2, keepdims=True)
    altura = (0.34 + 0.66 * bajo)[..., None]
    img = (img * (0.17 + 0.13 * lum) * altura
           + np.array([0.014, 0.022, 0.042], np.float32) * (0.3 + 0.7 * lum)) * (1 - sky * 0.96) \
        + img * (sky * 0.96)

    # lo que responde a la luz: la vegetacion y las superficies claras
    veg = np.clip((day[..., 1] - (day[..., 0] + day[..., 2]) / 2) * 5.0, 0, 1)
    sup = np.clip((day.mean(2) - 0.10) * 2.4, 0, 1)
    CALIDO, AMBAR = (1.0, 0.74, 0.40), (1.0, 0.84, 0.55)

    # 3. reflectores de la cancha: lejanos y frios, apenas un punto y su halo
    for cx, cy in ((74, 320), (8, 372), (80, 378)):
        img = sumar(img, foco(cx, cy, 10, 8, 1.5), (1.0, 0.98, 0.94), 0.85)
        img = sumar(img, foco(cx, cy, 55, 46, 2.8), (0.74, 0.82, 1.0), 0.14)
    img = iluminar(img, day, foco(450, 960, 560, 130, 2.0) * veg, (0.72, 0.86, 0.68), 0.50)

    # 4. uplights: las palmeras encendidas desde el pie, no siluetas negras
    for cx, cy in ((28, 830), (872, 810)):
        img = iluminar(img, day, foco(cx, cy, 230, 360, 1.5) * veg * bajo, (1.5, 1.30, 0.72), 1.45)
        img = iluminar(img, day, foco(cx, cy + 150, 170, 130, 2.0) * sup * bajo, AMBAR, 0.80)

    # 5. el interior es la luz principal de la escena, y se derrama al deck
    dentro = foco(450, 980, 340, 175, 1.0) * np.clip((day.mean(2) - 0.03) * 2.6, 0, 1)
    img = iluminar(img, day, dentro, (2.60, 1.95, 1.15), 2.30)
    img = sumar(img, dentro, (1.0, 0.74, 0.42), 0.42)
    img = sumar(img, foco(450, 1000, 320, 170, 2.0), (1.0, 0.68, 0.34), 0.22)
    img = iluminar(img, day, foco(455, 1122, 310, 90, 1.7) * sup, (1.7, 1.25, 0.72), 1.30)
    img = iluminar(img, day, foco(455, 1160, 440, 130, 2.4), (1.3, 0.95, 0.55), 0.55)

    # 6. cantero del frente
    arb = np.clip(foco(195, 1140, 200, 85, 1.5) + foco(755, 1140, 200, 85, 1.5), 0, 1)
    img = iluminar(img, day, arb * veg, (1.6, 1.45, 0.80), 1.40)
    img = iluminar(img, day, arb * sup, AMBAR, 0.55)

    # 7. bolardo del camino y su charco de luz sobre los adoquines
    img = sumar(img, foco(430, 1224, 11, 19, 1.3), (1.0, 0.92, 0.74), 0.90)
    img = sumar(img, foco(430, 1224, 46, 54, 2.6), (1.0, 0.86, 0.62), 0.20)
    img = iluminar(img, day, foco(430, 1340, 190, 85, 1.8) * sup, (1.45, 1.20, 0.80), 1.25)
    img = iluminar(img, day, foco(430, 1300, 460, 150, 2.6), (1.1, 0.92, 0.66), 0.40)
    img = iluminar(img, day, foco(430, 1460, 290, 145, 2.2) * veg, (1.4, 1.25, 0.70), 0.85)

    # 8. letras corporeas: la luz escapa por detras, el frente queda opaco
    glow = np.zeros(SZ[::-1], np.float32)
    for radio, peso in ((5, 0.42), (12, 0.28), (26, 0.15), (58, 0.08)):
        d = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(radio))
        glow += np.array(d, np.float32) / 255 * peso
    img = sumar(img, np.clip(glow, 0, 1), (0.97, 0.97, 1.0), 0.95)

    grano = rng.normal(0, 0.010, img.shape[:2])[..., None].astype(np.float32)
    img = np.clip(img + grano * (1.1 - img), 0, 1)
    night = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8))

    cuerpo = mask.filter(ImageFilter.MinFilter(3))
    canto = ImageChops.subtract(mask, cuerpo)
    night.paste(Image.new("RGB", SZ, (48, 49, 56)), (0, 0), cuerpo)
    night.paste(Image.new("RGB", SZ, (216, 222, 240)), (0, 0),
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
