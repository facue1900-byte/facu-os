#!/usr/bin/env python3
"""
Arma una propuesta comercial: JSON de contenido + template → HTML (y PDF).

    .venv/bin/python armar_propuesta.py --contenido prop.json --salida data/propuestas/prop [--pdf]

El contenido lo escribe el modelo (criterio); este script solo ensambla y
renderiza (código). Reglas de plata:
- NO suma ni calcula montos. Si el JSON trae "total", verifica que coincida
  con la suma de los ítems de esa moneda y CORTA si no coincide.
- ARS y USD nunca se mezclan en un mismo total.

El PDF sale de Chrome headless (sin abrir ventanas). Sin Chrome, queda el HTML
y un mensaje claro.
"""

import argparse
import html
import json
import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TEMPLATE = pathlib.Path(__file__).resolve().parents[1] / "template.html"

CAMPOS_OBLIGATORIOS = ["titulo", "para", "de", "fecha", "secciones"]


def parrafos(texto):
    """Texto plano → párrafos HTML (doble salto de línea separa párrafos)."""
    return "\n".join(f"<p>{html.escape(p.strip())}</p>"
                     for p in texto.split("\n\n") if p.strip())


def monto_fmt(valor, moneda):
    if isinstance(valor, str):          # "a confirmar", "según contrato", etc.
        return html.escape(valor)
    simbolo = "USD " if moneda == "USD" else "$"
    return f"{simbolo}{valor:,.0f}".replace(",", ".")


def verificar_totales(inversion):
    """Si hay 'total' declarado por moneda, tiene que cerrar contra los ítems."""
    items = inversion.get("items", [])
    for total in inversion.get("totales", []):
        moneda = total["moneda"]
        declarado = total["monto"]
        numericos = [i["monto"] for i in items
                     if i.get("moneda") == moneda and isinstance(i["monto"], (int, float))]
        con_texto = [i for i in items
                     if i.get("moneda") == moneda and isinstance(i["monto"], str)]
        if con_texto:
            sys.exit(f"Hay un total declarado en {moneda} pero ítems sin monto "
                     f"numérico ({con_texto[0]['concepto']!r}): o se completan, "
                     f"o se saca el total.")
        suma = sum(numericos)
        if abs(suma - declarado) > 0.005:
            sys.exit(f"El total {moneda} declarado ({declarado:,.2f}) NO coincide "
                     f"con la suma de los ítems ({suma:,.2f}). No genero un "
                     f"documento con un total que no cierra.")


def bloque_inversion(inversion):
    if not inversion or not inversion.get("items"):
        return ""
    filas = "\n".join(
        f"<tr><td>{html.escape(i['concepto'])}</td>"
        f"<td class='monto'>{monto_fmt(i['monto'], i.get('moneda', 'ARS'))}</td></tr>"
        for i in inversion["items"])
    totales = "\n".join(
        f"<tr class='total'><td>Total {t['moneda']}</td>"
        f"<td class='monto'>{monto_fmt(t['monto'], t['moneda'])}</td></tr>"
        for t in inversion.get("totales", []))
    nota = (f"<p class='nota'>{html.escape(inversion['nota'])}</p>"
            if inversion.get("nota") else "")
    return (f"<section><h2>{html.escape(inversion.get('titulo', 'Inversión'))}</h2>"
            f"<table>{filas}{totales}</table>{nota}</section>")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--contenido", required=True, help="JSON con el contenido")
    p.add_argument("--salida", required=True,
                   help="Path base de salida, sin extensión")
    p.add_argument("--pdf", action="store_true", help="Además del HTML, un PDF")
    args = p.parse_args()

    contenido = json.loads(pathlib.Path(args.contenido).read_text())
    faltan = [c for c in CAMPOS_OBLIGATORIOS if not contenido.get(c)]
    if faltan:
        sys.exit(f"Al contenido le falta: {', '.join(faltan)}. Se pide, no se inventa.")

    verificar_totales(contenido.get("inversion", {}))

    secciones = "\n".join(
        f"<section><h2>{html.escape(s['titulo'])}</h2>{parrafos(s['cuerpo'])}</section>"
        for s in contenido["secciones"])

    doc = (TEMPLATE.read_text()
           .replace("{{TITULO}}", html.escape(contenido["titulo"]))
           .replace("{{PARA}}", html.escape(contenido["para"]))
           .replace("{{DE}}", html.escape(contenido["de"]))
           .replace("{{FECHA}}", html.escape(contenido["fecha"]))
           .replace("{{INTRO}}", parrafos(contenido.get("intro", "")))
           .replace("{{SECCIONES}}", secciones)
           .replace("{{INVERSION}}", bloque_inversion(contenido.get("inversion", {})))
           .replace("{{CIERRE}}", parrafos(contenido.get("cierre", ""))))

    base = pathlib.Path(args.salida)
    base.parent.mkdir(parents=True, exist_ok=True)
    html_path = base.with_suffix(".html")
    html_path.write_text(doc)
    print(f"HTML: {html_path}")

    if args.pdf:
        if not pathlib.Path(CHROME).exists():
            sys.exit(f"No encontré Chrome en {CHROME}: queda el HTML. "
                     f"Instalá Chrome o generá el PDF a mano.")
        pdf_path = base.with_suffix(".pdf")
        r = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", str(html_path)],
            capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not pdf_path.exists():
            sys.exit(f"Chrome no pudo generar el PDF:\n{r.stderr[-500:]}")
        print(f"PDF:  {pdf_path}")

    print("\nGenerado y FRENADO: no se manda nada sin el OK de Facu.")


if __name__ == "__main__":
    main()
