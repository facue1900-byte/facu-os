#!/usr/bin/env python3
"""Manda a Facu y a Vlado el pedido de tomas para filmar que escribió el agente diario.

    .venv/bin/python active/astronomy/contenido/reels_diarios/pedir_filmacion.py ARCHIVO.md [--send]

Destinatarios FIJOS (pedido de Facu, 28/10/2026: «mandame mail a mi y a vladinic con tareas para
grabar contenido»). No se pueden cambiar por parámetro a propósito: el agente corre solo y no
puede mandarle un mail a nadie más.
Como mucho UN pedido cada DIAS_ENTRE días: un pedido por día se vuelve ruido y se deja de leer.
Sin --send sólo muestra el mail.
"""
import argparse
import base64
import datetime
import html
import json
import re
import sys

from comun import AQUI, OS

PARA = ["facue1900@gmail.com", "vladinic@astronomyofficial.com"]
DIAS_ENTRE = 3
LOG = AQUI / "pedidos_filmacion.jsonl"
CARPETA_SUBIDA = "Desktop/Productoras/Astronomy/Academia/Contenido/Material filmado"


def a_html(md):
    """Markdown mínimo (títulos, listas, negrita) a HTML: el pedido lo escribe el agente."""
    out = []
    for linea in md.splitlines():
        t = html.escape(linea)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
        if t.startswith("# "):
            out.append(f"<h2>{t[2:]}</h2>")
        elif t.startswith("## "):
            out.append(f"<h3>{t[3:]}</h3>")
        elif re.match(r"^\s*[-*] ", t):
            out.append(f"<li>{re.sub(r'^\s*[-*] ', '', t)}</li>")
        elif t.strip():
            out.append(f"<p>{t}</p>")
    return "<div style='font-size:14px;line-height:1.45;color:#222;margin-top:12px'>" + "\n".join(out) + "</div>"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--send", action="store_true")
    a = ap.parse_args()
    md = open(a.archivo).read().strip()
    if len(md) < 200:
        sys.exit("PEDIDO_FALLA: el pedido es demasiado corto para que alguien sepa qué filmar")
    titulo = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "Tomas para filmar")
    sys.path.insert(0, str(OS / "execution"))
    from mail_format import render
    # El título ya encabeza el mail: el cuerpo arranca después de la línea "# ...".
    cuerpo = "\n".join(l for l in md.splitlines() if not l.startswith("# "))
    correo = render(
        area="astronomy", nivel="revisar", titulo=f"Para filmar: {titulo}",
        accion=f"Cuando lo tengan, pásenlo (AirDrop o Drive) a la Mac de Facu, carpeta ~/{CARPETA_SUBIDA}. El agente de reels lo levanta solo al día siguiente.",
        html_extra=a_html(cuerpo), origen="reels diarios de Astronomy",
    )
    asunto = correo.asunto
    if not a.send:
        print(f"PARA: {', '.join(PARA)}\nASUNTO: {asunto}\n\n{md}\n\nPEDIDO_SIN_SEND")
        return
    if LOG.exists():
        ultimo = json.loads(LOG.read_text().strip().splitlines()[-1])
        dias = (datetime.date.today() - datetime.date.fromisoformat(ultimo["fecha"])).days
        if dias < DIAS_ENTRE:
            sys.exit(f"PEDIDO_FALLA: el último pedido salió hace {dias} días ({ultimo['asunto']}); "
                     f"se espera {DIAS_ENTRE}. Sumá las tomas nuevas al próximo.")
    from google_auth import gmail
    msg = correo.mime(PARA)
    gmail().users().messages().send(userId="me", body={"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}).execute()
    with LOG.open("a") as f:
        f.write(json.dumps({"fecha": datetime.date.today().isoformat(), "asunto": asunto, "archivo": a.archivo},
                           ensure_ascii=False) + "\n")
    print("PEDIDO_OK", ", ".join(PARA))


if __name__ == "__main__":
    main()
