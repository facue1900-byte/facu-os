#!/usr/bin/env python3
"""Láminas del arquitecto -> PNG para la ficha, con el rótulo renombrado.

El arquitecto entregó la planta y las vistas como «Local Fabric», pero el local
sombreado es el de la pizzería. Acá se borra sólo ese texto del rótulo (las
líneas del plano no se tocan) y se escribe el nombre correcto en el mismo lugar,
mismo cuerpo y misma alineación.

  .venv/bin/python data/fichas-locales/laminas.py
"""
import pathlib
import sys

import fitz

BASE = pathlib.Path(__file__).parent
FUENTE = BASE / "planos-pizzeria-arquitecto.pdf"

# (texto a buscar, texto nuevo, cuerpo mínimo para no agarrar "LOCALES" del rótulo chico,
#  alineación). La alineación copia la del original: el nombre va centrado, la lámina a la derecha.
CAMBIOS = [
    ("FABRIC", "PIZZERÍA", 9, "centro"),
    ("PLANTA FABRIC", "PLANTA PIZZERÍA", 6, "derecha"),
    ("VISTAS FABRIC", "VISTAS PIZZERÍA", 6, "derecha"),
]
SALIDAS = ["plano-pizzeria-planta", "plano-pizzeria-vistas"]
# El rótulo original es ArialMT: con Arial la letra empata, y mide bien la «Í»
# (la Helvetica base-14 de PyMuPDF la mide mal y descentraba el nombre).
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"


def main() -> None:
    doc = fitz.open(FUENTE)
    arial = fitz.Font(fontfile=ARIAL)
    for page, nombre in zip(doc, SALIDAS):
        page.remove_rotation()  # el PDF viene girado 270°: así el texto queda horizontal
        escribir = []
        for viejo, nuevo, minimo, alin in CAMBIOS:
            for r in page.search_for(viejo):
                if r.height < minimo:
                    continue
                escribir.append((r, nuevo, alin))
                page.add_redact_annot(r, fill=False)
        if not escribir:
            sys.exit(f"{nombre}: no encontré «FABRIC» en el rótulo — ¿cambió la lámina?")
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                              graphics=fitz.PDF_REDACT_LINE_ART_NONE)
        for r, nuevo, alin in escribir:
            cuerpo = r.height * 0.99
            ancho = arial.text_length(nuevo, fontsize=cuerpo)
            x = (r.x0 + r.x1 - ancho) / 2 if alin == "centro" else r.x1 - ancho
            page.insert_text((x, r.y1 - r.height * 0.21), nuevo,
                             fontname="arial", fontfile=ARIAL, fontsize=cuerpo, color=(0, 0, 0))
        texto = page.get_text()
        if "FABRIC" in texto.upper() or "PIZZER" not in texto.upper():
            sys.exit(f"{nombre}: el rótulo no quedó cambiado")
        page.get_pixmap(dpi=220).save(BASE / "img" / f"{nombre}.png")
        print(f"{nombre}: {len(escribir)} rótulos cambiados")


if __name__ == "__main__":
    main()
