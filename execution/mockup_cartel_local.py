from PIL import Image, ImageFilter, ImageChops
import numpy as np, sys

W = "/private/tmp/claude-501/-Users-Facu-facu-os/53924761-26db-4e04-9a3b-88bacd306abd/scratchpad"
M = "/Users/Facu/facu-os/.claude/skills/flyers/assets/marca"
BASE = "/Users/Facu/facu-os/execution/assets/fachada-astronomy-sin-cartel.jpg"

def asset(name):
    im = Image.open(f"{M}/{name}").convert("RGBA")
    a = np.array(im)[..., 3]
    ys, xs = np.nonzero(a > 8)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))

ISO, LOGO = asset("isotipo-blanco.png"), asset("logotipo-blanco.png")

def place(canvas_size, pieces):
    """pieces: (img, cx, top, h) -> devuelve mascara alpha L del conjunto"""
    m = Image.new("L", canvas_size, 0)
    for img, cx, top, h in pieces:
        w = max(1, round(h * img.width / img.height))
        r = img.resize((w, h), Image.LANCZOS)
        m.paste(r.split()[3], (round(cx - w / 2), top), r.split()[3])
    return m

def dia(mask, out):
    base = Image.open(BASE).convert("RGB")
    # sombra propia del corporeo sobre la madera
    sh = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.55))
    base.paste(Image.new("RGB", base.size, (8, 9, 12)), (2, 4), sh)
    base.paste(Image.new("RGB", base.size, (247, 248, 250)), (0, 0), mask)
    base.save(out, quality=94)

def noche(mask, out):
    a = np.array(Image.open(BASE).convert("RGB")).astype(np.float32) / 255
    lum = a.mean(2, keepdims=True)
    k = 0.24 - 0.13 * lum                      # el cielo (claro) se oscurece mas
    n = a * k + np.array([0.038, 0.044, 0.078], np.float32) * (0.30 + 0.70 * lum)
    night = Image.fromarray(np.clip(n * 255, 0, 255).astype(np.uint8))

    # halo: la luz que escapa por detras de la letra corporea
    glow = np.zeros(mask.size[::-1], np.float32)
    for radio, peso in ((6, 0.55), (14, 0.42), (34, 0.26), (70, 0.14)):
        d = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(radio))
        glow += np.array(d, np.float32) / 255 * peso
    glow = np.clip(glow, 0, 1)[..., None]
    tinte = np.array([1.0, 1.0, 1.0], np.float32)
    n2 = np.array(night, np.float32) / 255
    n2 = n2 + glow * tinte * (1 - n2) * 1.05
    night = Image.fromarray(np.clip(n2 * 255, 0, 255).astype(np.uint8))

    # cuerpo opaco de la letra + canto iluminado
    cuerpo = mask.filter(ImageFilter.MinFilter(3))
    canto = ImageChops.subtract(mask, cuerpo)
    night.paste(Image.new("RGB", night.size, (58, 59, 66)), (0, 0), cuerpo)
    night.paste(Image.new("RGB", night.size, (238, 242, 255)), (0, 0),
                canto.filter(ImageFilter.GaussianBlur(0.6)))
    night.save(out, quality=94)

SZ = (900, 1600)
# v3: estrella mas grande, ASTRONOMY mas chico
v3 = place(SZ, [(ISO, 458, 620, 166), (LOGO, 472, 811, 42)])
# v4: ASTRONOMY grande de punta a punta en la pared, estrella chica en el gazebo
v4 = place(SZ, [(LOGO, 455, 668, 64), (ISO, 472, 806, 32)])

dia(v3, f"{W}/v3_dia.jpg");   noche(v3, f"{W}/v3_noche.jpg")
dia(v4, f"{W}/v4_dia.jpg");   noche(v4, f"{W}/v4_noche.jpg")

for f in ("v3_dia", "v3_noche", "v4_dia", "v4_noche"):
    Image.open(f"{W}/{f}.jpg").crop((100, 580, 800, 900)).resize((1225, 560)).save(f"{W}/{f}_zoom.jpg", quality=92)
print("ok")
