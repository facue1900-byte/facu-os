"""El formato único de los mails automáticos de facu-os.

El asunto siempre arranca por el área y el color:   PASEO · 🔴 Efectivo diario frenado
Adentro: título, qué pasó en una frase, números clave, qué hacer, puntos y link.

Sin dependencias a propósito: también lo usan las rutinas de la nube, que clonan el repo.

    render(area="paseo", nivel="urgente", titulo="...", resumen="...", ...) -> Mail
    echo '{"area": "cripto", "nivel": "bueno", "titulo": "..."}' | python3 execution/mail_format.py
"""
import html
import json
import sys
from dataclasses import dataclass
from email.message import EmailMessage

AREAS = {"astronomy": "ASTRONOMY", "paseo": "PASEO", "campos": "CAMPOS", "cripto": "CRIPTO", "sistema": "SISTEMA"}
NIVELES = {
    "urgente": ("🔴", "URGENTE", "#C62828", "#FDECEA"),
    "revisar": ("🟡", "PARA REVISAR", "#9A5B00", "#FFF4E0"),
    "bueno": ("🟢", "BUENA NOTICIA", "#1B7F4B", "#E8F6EE"),
    "reporte": ("📊", "REPORTE", "#3B2A8C", "#F0EDFB"),
}
TONOS = {"rojo": "#C62828", "ambar": "#9A5B00", "verde": "#1B7F4B", "neutro": "#111111"}
# Sin comillas adentro: va en style='...' y una comilla simple corta el atributo.
FUENTE = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"


@dataclass
class Mail:
    asunto: str
    html: str
    texto: str

    def mime(self, para) -> EmailMessage:
        m = EmailMessage()
        m["To"] = para if isinstance(para, str) else ", ".join(para)
        m["Subject"] = self.asunto
        m.set_content(self.texto)
        m.add_alternative(self.html, subtype="html")
        return m


def _e(s) -> str:
    return html.escape(str(s))


def _tiles(kpis) -> str:
    celdas = "".join(
        f"<td width='{100 // len(kpis)}%' style='padding:12px;background:#F6F6F8;border:4px solid #fff;border-radius:10px'>"
        f"<div style='font-size:12px;color:#666'>{_e(k[0])}</div>"
        f"<div style='font-size:20px;font-weight:700;color:{TONOS.get(k[2] if len(k) > 2 else 'neutro', '#111111')};margin-top:2px'>{_e(k[1])}</div></td>"
        for k in kpis)
    return f"<table width='100%' cellspacing='0' cellpadding='0' style='margin:16px 0 4px;border-collapse:separate'><tr>{celdas}</tr></table>"


def _seccion(titulo, puntos) -> str:
    items = "".join(f"<li style='margin:5px 0'>{_e(p)}</li>" for p in puntos)
    return (f"<div style='font-size:13px;font-weight:700;color:#333;margin:20px 0 4px'>{_e(titulo)}</div>"
            f"<ul style='margin:0;padding-left:20px;font-size:14px;line-height:1.45;color:#222'>{items}</ul>")


def render(area, nivel, titulo, resumen="", kpis=None, accion=None, secciones=None,
           link=None, link_texto="Ver el detalle", detalle=None, html_extra=None, origen=None) -> Mail:
    """`secciones` = [(título, [puntos])] y `kpis` = [(etiqueta, valor, tono)]: se escapan.
    `html_extra` va tal cual: sólo para el HTML que arma el propio script. `detalle` es el
    texto crudo (un log) y va chico al final: nunca es lo primero que se lee."""
    emoji, etiqueta, color, fondo = NIVELES[nivel]
    nombre_area = AREAS[area]
    asunto = f"{nombre_area} · {emoji} {titulo}"[:120]
    secciones = secciones or []
    kpis = list(kpis or [])[:4]

    partes = [
        f"<div style='background:#F2F2F5;padding:16px 8px;font-family:{FUENTE}'>",
        "<div style='max-width:640px;margin:0 auto;background:#fff;border-radius:14px;overflow:hidden;border:1px solid #E6E6EA'>",
        f"<div style='background:{color};color:#fff;padding:10px 20px;font-size:12px;font-weight:700;letter-spacing:.6px'>"
        f"{_e(nombre_area)} &nbsp;·&nbsp; {_e(etiqueta)}</div>",
        "<div style='padding:20px'>",
        f"<h1 style='font-size:21px;line-height:1.25;margin:0;color:#111'>{_e(titulo)}</h1>",
    ]
    if resumen:
        partes.append(f"<p style='font-size:15px;line-height:1.45;color:#333;margin:10px 0 0'>{_e(resumen)}</p>")
    if kpis:
        partes.append(_tiles(kpis))
    if accion:
        partes.append(f"<div style='background:{fondo};border-left:4px solid {color};border-radius:6px;padding:12px 14px;margin:16px 0 0;font-size:14px;line-height:1.4;color:#222'>"
                      f"<b style='color:{color}'>Qué hacer:</b> {_e(accion)}</div>")
    partes += [_seccion(t, p) for t, p in secciones if p]
    if html_extra:
        partes.append(html_extra)
    if link:
        partes.append(f"<p style='margin:20px 0 0'><a href='{_e(link)}' style='display:inline-block;background:{color};color:#fff;"
                      f"text-decoration:none;font-size:14px;font-weight:600;padding:10px 16px;border-radius:8px'>{_e(link_texto)}</a></p>")
    if detalle:
        partes.append("<div style='font-size:12px;color:#888;margin:22px 0 4px'>Detalle técnico</div>"
                      f"<pre style='background:#F6F6F8;border-radius:8px;padding:10px;font-size:11px;line-height:1.35;color:#555;white-space:pre-wrap;word-break:break-word;margin:0'>{_e(detalle)}</pre>")
    partes.append("</div>")
    pie = f"facu-os · {origen}" if origen else "facu-os"
    partes.append(f"<div style='padding:10px 20px;border-top:1px solid #EEE;font-size:11px;color:#999'>{_e(pie)}</div></div></div>")

    texto = [f"{nombre_area} · {etiqueta}", "", titulo]
    if resumen:
        texto += ["", resumen]
    if kpis:
        texto += [""] + [f"{k[0]}: {k[1]}" for k in kpis]
    if accion:
        texto += ["", f"Qué hacer: {accion}"]
    for t, puntos in secciones:
        if puntos:
            texto += ["", f"{t}:"] + [f"- {p}" for p in puntos]
    if link:
        texto += ["", f"{link_texto}: {link}"]
    if detalle:
        texto += ["", "--- detalle técnico ---", detalle]
    return Mail(asunto, "".join(partes), "\n".join(texto))


if __name__ == "__main__":
    d = json.load(sys.stdin)
    d["secciones"] = [tuple(s) for s in d.get("secciones", [])]
    m = render(**d)
    json.dump({"asunto": m.asunto, "html": m.html, "texto": m.texto}, sys.stdout, ensure_ascii=False)
