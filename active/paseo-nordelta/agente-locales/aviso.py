"""Arma el aviso del buscador de inquilinos del Paseo: mail lindo + texto para Telegram.

Lo corre la rutina en la nube (sin dependencias, Python de sistema):

    python3 active/paseo-nordelta/agente-locales/aviso.py candidatos.json > aviso.json

candidatos.json = [{"marca", "rubro", "local" ("servicios"|"Market"), "por_que",
                    "contacto" (mail o ""), "fuente" (link), "web" (opcional)}]
Salida: {"asunto", "html", "texto", "telegram"}. El mail usa execution/mail_format.py
(formato único de facu-os) y le suma una tarjeta por candidato.
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "execution"))
from mail_format import FUENTE, render  # noqa: E402

COLOR_LOCAL = {"servicios": ("#3B2A8C", "#F0EDFB"), "market": ("#1B7F4B", "#E8F6EE")}


def _e(s):
    return html.escape(str(s or ""))


def _boton(href, texto, color):
    return (f"<a href='{_e(href)}' style='display:inline-block;margin:10px 8px 0 0;background:{color};color:#fff;"
            f"text-decoration:none;font-size:13px;font-weight:600;padding:7px 12px;border-radius:7px'>{_e(texto)}</a>")


def tarjeta(i, c):
    local = (c.get("local") or "servicios").strip()
    color, fondo = COLOR_LOCAL.get(local.lower(), COLOR_LOCAL["servicios"])
    contacto = (c.get("contacto") or "").strip()
    linea_contacto = (f"<a href='mailto:{_e(contacto)}' style='color:#111'>{_e(contacto)}</a>" if "@" in contacto
                      else "<span style='color:#9A5B00'>Sin contacto público todavía</span>")
    botones = ""
    if c.get("fuente"):
        botones += _boton(c["fuente"], "Ver la nota", "#555")
    if c.get("web"):
        botones += _boton(c["web"], "Web de la marca", "#555")
    if "@" in contacto:
        botones += _boton(f"mailto:{contacto}", "Escribirle", color)
    return (
        f"<div style='border:1px solid #E6E6EA;border-left:4px solid {color};border-radius:10px;padding:14px 16px;margin:14px 0 0;font-family:{FUENTE}'>"
        f"<div style='font-size:12px;color:#999'>#{i}</div>"
        f"<div style='font-size:17px;font-weight:700;color:#111;margin:2px 0 6px'>{_e(c.get('marca'))}</div>"
        f"<span style='display:inline-block;background:{fondo};color:{color};font-size:12px;font-weight:700;padding:3px 9px;border-radius:20px;margin-right:6px'>{_e(local.upper() if local.lower() == 'market' else 'SERVICIOS')}</span>"
        f"<span style='display:inline-block;background:#F6F6F8;color:#444;font-size:12px;padding:3px 9px;border-radius:20px'>{_e(c.get('rubro'))}</span>"
        f"<p style='font-size:14px;line-height:1.45;color:#333;margin:10px 0 4px'>{_e(c.get('por_que'))}</p>"
        f"<div style='font-size:13px;color:#555'>Contacto: {linea_contacto}</div>"
        f"{botones}</div>"
    )


def armar(cands):
    n = len(cands)
    n_market = sum(1 for c in cands if (c.get("local") or "").lower() == "market")
    con_mail = sum(1 for c in cands if "@" in (c.get("contacto") or ""))
    plural = "s" if n != 1 else ""
    mail = render(
        area="paseo", nivel="revisar",
        titulo=f"{n} candidato{plural} nuevo{plural} para los locales",
        resumen="Marcas en expansión que encajan en los 8 locales de servicios o en el Market (entrega jul-2027). Nadie fue contactado.",
        kpis=[("Nuevos", n), ("Servicios", n - n_market), ("Market", n_market),
              ("Con mail", con_mail, "verde" if con_mail else "ambar")],
        accion="Elegí a cuáles les escribimos desde paseonordelta@ (sin precios: primero que manden propuesta).",
        html_extra="".join(tarjeta(i, c) for i, c in enumerate(cands, 1)),
        origen="buscador diario de inquilinos",
    )
    tg = [f"🏬 Paseo · {n} candidato{plural} nuevo{plural}"]
    for i, c in enumerate(cands, 1):
        contacto = c.get("contacto") or "sin contacto"
        tg.append(f"{i}. {c.get('marca')} — {c.get('rubro')} → {c.get('local')}. {c.get('por_que')} ({contacto})")
    tg.append("¿A cuál le escribimos?")
    return {"asunto": mail.asunto, "html": mail.html, "texto": mail.texto, "telegram": "\n".join(tg)}


if __name__ == "__main__":
    datos = json.load(open(sys.argv[1], encoding="utf-8"))
    if not datos:
        sys.exit("candidatos.json vacío: sin candidatos no se manda aviso")
    json.dump(armar(datos), sys.stdout, ensure_ascii=False)
