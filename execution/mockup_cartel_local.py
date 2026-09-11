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
    """pieces: (img, centro_x, top, alto) -> mascara L del cartel completo.

    El ancho se fuerza impar: con ancho par el centro de una pieza cae medio pixel
    al costado del eje, y dos piezas de distinta paridad quedan desalineadas entre si.
    """
    m = Image.new("L", SZ, 0)
    for img, cx, top, h in pieces:
        w = max(1, round(h * img.width / img.height))
        w += 1 - w % 2
        r = img.resize((w, h), Image.LANCZOS).split()[3]
        m.paste(r, (cx - (w - 1) // 2, top), r)
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

    # 8. letras corporeas retroiluminadas.
    #    El halo no es una mancha blanca apoyada encima de la pared: es la PARED
    #    iluminada. Por eso va multiplicativo y se le sigue viendo la veta a la
    #    madera, igual que en una corporea real se ven las juntas del ladrillo
    #    dentro del resplandor. Solo una fraccion chica se suma, que es la luz
    #    dispersa en el aire.
    letra = np.array(mask, np.float32) / 255
    halo = np.zeros(SZ[::-1], np.float32)
    for radio, peso in ((2, 0.80), (5, 0.62), (12, 0.40), (28, 0.20), (72, 0.07)):
        halo += np.array(mask.filter(ImageFilter.GaussianBlur(radio)), np.float32) / 255 * peso
    # curva: el resplandor casi quema pegado a la letra y cae rapido, no se difumina
    # parejo en una bruma gris
    halo = np.clip(halo, 0, 1) ** 0.70 * (1 - letra)   # la luz sale por detras: la letra tapa
    img = iluminar(img, day, halo, (7.8, 7.6, 7.2), 1.0)
    img = sumar(img, halo ** 1.5, (1.0, 0.985, 0.95), 0.72)

    # la corporea esta separada de la pared unos centimetros: contra la luz queda
    # una linea de sombra pegada al borde de abajo
    sombra = np.array(ImageChops.subtract(
        mask.filter(ImageFilter.GaussianBlur(2)),
        ImageChops.offset(mask, 0, -3)), np.float32) / 255
    img = np.clip(img * (1 - sombra[..., None] * 0.55 * (1 - letra)[..., None]), 0, 1)

    grano = rng.normal(0, 0.010, img.shape[:2])[..., None].astype(np.float32)
    img = np.clip(img + grano * (1.1 - img), 0, 1)
    night = Image.fromarray(np.clip(img * 255, 0, 255).astype(np.uint8))

    # el frente de la letra es opaco. No se enciende: apenas recibe el rebote de la
    # pared, y un poco mas sobre el canto. Un contorno brillante dibujado alrededor
    # es lo que hace que un cartel se lea como neon en vez de como corporea.
    borde = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(5)))
    night.paste(Image.new("RGB", SZ, (62, 62, 66)), (0, 0), mask)
    night.paste(Image.new("RGB", SZ, (100, 99, 100)), (0, 0),
                borde.point(lambda v: int(v * 0.55)).filter(ImageFilter.GaussianBlur(0.4)))

    night.save(out, quality=94)

if __name__ == "__main__":
    # EJE = centro real de la pared de madera, medido en las filas que no tapan las
    # palmeras (620, 640, 660 y 740): 456 +-3 px. Las dos piezas van sobre el mismo
    # eje, si no el conjunto se lee torcido aunque cada pieza este bien puesta.
    EJE = 456
    # v3: la estrella al maximo que da la pared, el logotipo bien chico debajo
    v3 = place([(ISO, EJE, 617, 172), (LOGO, EJE, 804, 35)])
    # v4: ASTRONOMY de punta a punta en la pared, estrella chica en la viga
    v4 = place([(LOGO, EJE, 668, 64), (ISO, EJE, 806, 32)])

    for nombre, m in (("v3", v3), ("v4", v4)):
        dia(m, f"{W}/{nombre}_dia.jpg")
        noche(m, f"{W}/{nombre}_noche.jpg")
    print("ok")
