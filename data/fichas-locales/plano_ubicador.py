#!/usr/bin/env python3
"""El plano general de Max, apagado, con un local encendido en naranja.

Copia el plano tal cual —no lo redibuja— y sólo cambia el color: todo el predio
baja a un gris apenas visible sobre el fondo del paseo, y el rectángulo del
local de la ficha queda a full en Corten, con un halo alrededor.

  .venv/bin/python data/fichas-locales/plano_ubicador.py

Escribe `img/ubicador-<slug>.png` y, en `ubicadores.json`, dónde quedó el
centro del local en % — que es lo que usa la ficha para poner la etiqueta.
"""
import json
import pathlib
import sys

import fitz
import numpy as np

BASE = pathlib.Path(__file__).parent
PLANO = BASE / "plano-general.pdf"
DPI = 300

GROUND = np.array([23, 22, 20], dtype=np.float64)       # el negro cálido del paseo
TRAZO = np.array([196, 188, 175], dtype=np.float64)     # el plano apagado
CORTEN = np.array([236, 146, 90], dtype=np.float64)     # el local encendido
ZOOM = 3.1          # cuanto entorno entra en el acercamiento
APAGADO = 0.62                                          # cuánto queda del plano de fondo

# El rectángulo de cada local, en puntos del PDF, sacado del propio dibujo y
# verificado mirando el recorte: tiene que entrar el local entero y nada del
# vecino. Ver README.
LOCALES = {
    "cafe": {
        "rect": (475.0, 213.0, 584.0, 296.5),
        "que": "Deck + GALERIA 13,00 + OFICINA 29 + OFICINA 30 + SALON 28",
    },
    "pizzeria": {
        "rect": (730.0, 394.0, 790.0, 448.0),
        "que": "SEMICUBIERTO + LOCAL 13 + COCINA 14",
    },
}


def recorte_del_dibujo(pag: fitz.Page) -> fitz.Rect:
    """El plano ocupa una parte de la hoja: el resto es margen en blanco.

    Entra tambien el texto: si se toma solo el dibujo, el recorte se come el
    "Av. de los Colegios n 160" que esta fuera de los trazos.
    """
    r = fitz.Rect()
    for d in pag.get_drawings():
        r |= d["rect"]
    for b in pag.get_text("blocks"):
        r |= fitz.Rect(b[:4])
    r = r & pag.rect
    m = 10
    return fitz.Rect(r.x0 - m, r.y0 - m, r.x1 + m, r.y1 + m) & pag.rect


def halo(alto: int, ancho: int, caja, radio: int) -> np.ndarray:
    """Un degradé suave alrededor del local, para que el ojo vaya solo."""
    x0, y0, x1, y1 = caja
    ys = np.arange(alto)[:, None]
    xs = np.arange(ancho)[None, :]
    dx = np.maximum(np.maximum(x0 - xs, xs - x1), 0)
    dy = np.maximum(np.maximum(y0 - ys, ys - y1), 0)
    d = np.sqrt(dx.astype(np.float64) ** 2 + dy.astype(np.float64) ** 2)
    return np.clip(1.0 - d / radio, 0.0, 1.0) ** 2


def main() -> None:
    if not PLANO.exists():
        sys.exit(f"FALTA el plano general: {PLANO}")
    pag = fitz.open(PLANO)[0]
    clip = recorte_del_dibujo(pag)
    pix = pag.get_pixmap(dpi=DPI, clip=clip)
    esc = DPI / 72.0
    rgb = np.frombuffer(pix.samples, dtype=np.uint8)
    rgb = rgb.reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(np.float64)

    # El plano viene negro sobre blanco: se invierte para que sea luz sobre el
    # fondo oscuro del paseo. `tinta` es cuánto trazo hay en cada píxel.
    tinta = 1.0 - rgb.mean(axis=2) / 255.0
    alto, ancho = tinta.shape
    print(f"plano {ancho}x{alto} px  ({clip})")

    centros = {}
    for slug, cfg in LOCALES.items():
        x0, y0, x1, y1 = cfg["rect"]
        caja = (round((x0 - clip.x0) * esc), round((y0 - clip.y0) * esc),
                round((x1 - clip.x0) * esc), round((y1 - clip.y0) * esc))
        cx0, cy0, cx1, cy1 = caja
        if not (0 <= cx0 < cx1 <= ancho and 0 <= cy0 < cy1 <= alto):
            sys.exit(f"{slug}: el rectángulo cae fuera del plano ({caja})")

        dentro = np.zeros((alto, ancho), dtype=bool)
        dentro[cy0:cy1, cx0:cx1] = True
        if tinta[dentro].mean() < 0.02:
            sys.exit(f"{slug}: el rectángulo agarró una zona vacía del plano")

        # Fondo: el plano entero, apagado. Encima, el local a full en Corten.
        peso = (tinta * APAGADO)[:, :, None]
        img = GROUND + (TRAZO - GROUND) * np.clip(peso, 0, 1)

        g = halo(alto, ancho, caja, radio=int(0.9 * DPI))
        img += (CORTEN - GROUND) * (g * 0.13)[:, :, None]

        fuerte = (tinta * dentro)[:, :, None]
        img = img * (1 - fuerte) + CORTEN * fuerte

        # El marco del local, en Corten, para que se lea el limite exacto.
        gr = max(2, round(DPI / 90))
        for a, b in ((cy0 - gr, cy0), (cy1, cy1 + gr)):
            img[max(a, 0):b, max(cx0 - gr, 0):cx1 + gr] = CORTEN
        for a, b in ((cx0 - gr, cx0), (cx1, cx1 + gr)):
            img[max(cy0 - gr, 0):cy1 + gr, max(a, 0):b] = CORTEN

        listo = np.clip(img, 0, 255).astype(np.uint8)

        def guardar(nombre, arr):
            h, w = arr.shape[:2]
            fitz.Pixmap(fitz.csRGB, w, h, arr.tobytes(), False).save(
                BASE / "img" / nombre)
            return w, h

        def porcentajes(x0p, y0p, x1p, y1p, w, h):
            return {"x": f"{(cx0 + cx1) / 2 - x0p:.0f}",
                    "y": f"{(cy0 + cy1) / 2 - y0p:.0f}",
                    "_w": w, "_h": h}

        # Entero: para la historia, donde el plano va grande y se lee.
        w, h = guardar(f"ubicador-{slug}.png", listo)
        entero = {"x": f"{(cx0 + cx1) / 2 / w * 100:.2f}%",
                  "y": f"{(cy0 + cy1) / 2 / h * 100:.2f}%",
                  "alto_caja": f"{(cy1 - cy0) / h * 100:.2f}%"}

        # Acercamiento: para el PDF, donde a 85 mm el local entero no se lee.
        lado = max(cx1 - cx0, cy1 - cy0) * ZOOM
        mx, my = (cx0 + cx1) // 2, (cy0 + cy1) // 2
        zx0 = int(max(0, min(mx - lado / 2, ancho - lado)))
        zy0 = int(max(0, min(my - lado / 2, alto - lado)))
        zx1, zy1 = int(min(ancho, zx0 + lado)), int(min(alto, zy0 + lado))
        rec = listo[zy0:zy1, zx0:zx1]
        zw, zh = guardar(f"ubicador-{slug}-zoom.png", rec)
        zoom = {"x": f"{((cx0 + cx1) / 2 - zx0) / zw * 100:.2f}%",
                "y": f"{((cy0 + cy1) / 2 - zy0) / zh * 100:.2f}%",
                "alto_caja": f"{(cy1 - cy0) / zh * 100:.2f}%"}

        centros[slug] = {"entero": entero, "zoom": zoom, "que": cfg["que"]}
        print(f"  {slug:<9} entero {w}x{h}  zoom {zw}x{zh}  "
              f"local en {zoom['x']} {zoom['y']} del zoom")

    (BASE / "ubicadores.json").write_text(
        json.dumps(centros, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
