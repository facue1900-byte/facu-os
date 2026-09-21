"""Reporte semanal del equipo de Astronomy Academy: qué hizo cada uno en la web y qué no.

Pedido de Facu, 21/09/2026: todos los viernes a las 17:00 un mail a Facu y a Vlado con lo
que José y Luqui hicieron en la web en la semana y lo que les quedó sin hacer.

Los datos los junta `npm run reporte:equipo` en astronomy-members (sólo lee la base): lo
hecho sale de lo que la web registra sola y lo pendiente, del mismo motor que arma el
escritorio de cada uno. Este script sólo arma el mail.

    .venv/bin/python execution/reporte_equipo.py              # arma el HTML, no manda nada
    .venv/bin/python execution/reporte_equipo.py --send --para facue1900@gmail.com
    .venv/bin/python execution/reporte_equipo.py --send       # a los tres destinatarios

Por defecto NO manda (regla 10). El `--send` lo pone el plist de launchd.
Si juntar los datos falla, con `--send` le llega a Facu un mail de error en vez del reporte:
un viernes sin mail no puede confundirse con una semana sin novedades.
"""
import argparse
import base64
import html
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timedelta
from email.message import EmailMessage

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from execution.google_auth import gmail  # noqa: E402

APP = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/astronomy-members"
NODE_BIN = pathlib.Path.home() / ".local/node/bin"
PARA = ["facue1900@gmail.com", "festevez@astronomyofficial.com", "vladinic@astronomyofficial.com"]
SALIDA = RAIZ / "data" / "reportes-equipo"

# Lo que registra la web, dicho en castellano. Una acción que no está acá sale con su
# nombre técnico: mejor feo que escondido.
ACCIONES = {
    "espejo_mp.sync": "bajó los movimientos de Mercado Pago",
    "espejo_mp.egreso": "clasificó un egreso de Mercado Pago",
    "espejo_mp.alumno": "asignó un cobro de Mercado Pago a un alumno",
    "agenda_manual": "agendó una clase a mano",
    "clase.mover": "movió una clase",
    "clase.cancelar": "canceló una clase",
    "clase.proponer_cambio": "propuso un cambio de clase",
    "membership": "cambió una membresía",
    "phone": "cargó un teléfono",
    "credits": "ajustó créditos",
    "pagos.ignorar": "descartó un pago",
    "closer.quitar": "sacó un closer",
    "rental_assigned": "asignó un alquiler",
    "block": "bloqueó un horario",
    "salary_paid": "marcó un sueldo como pagado",
    "announcement": "publicó un aviso",
}
CONTACTOS = {
    "contacto:mandado": "le escribió a un alumno",
    "contacto:enviado": "le escribió a un alumno",
    "contacto:leyo": "anotó que lo leyó",
    "contacto:no_leyo": "anotó que no lo leyó",
    "contacto:pospuesto": "pospuso un contacto",
    "contacto:pago": "anotó que pagó",
    "estado:contactado": "marcó un caso como contactado",
    "estado:resuelto": "cerró un caso",
    "accion:wsp": "abrió un WhatsApp desde la cola",
    "accion:asignar_pago_libro": "asignó un pago al Libro",
    "respuesta": "contestó una pregunta",
}
# En `staff` Valen figura con su nombre de artista.
NOMBRES_PROFES = {"Owners of Time": "Valen Frando (Owners of Time)"}
DIAS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


def plata(n):
    return "$" + f"{round(n):,}".replace(",", ".")


def dia(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{DIAS[d.weekday()]} {d.day:02d}/{d.month:02d}"


def juntar():
    r = subprocess.run(
        ["npm", "run", "-s", "reporte:equipo"], cwd=APP, capture_output=True, text=True,
        env={"PATH": f"{NODE_BIN}:/usr/bin:/bin", "HOME": str(pathlib.Path.home())}, timeout=300,
    )
    if r.returncode != 0:
        raise RuntimeError(f"npm run reporte:equipo salió con {r.returncode}:\n{r.stderr[-3000:]}")
    datos = json.loads(r.stdout)
    # Regla 2: un reporte sin José y Luqui no es "no hicieron nada", es un reporte roto.
    nombres = {p["nombre"] for p in datos["personas"] if p.get("principal")}
    if not {"José", "Luqui"} <= nombres:
        raise RuntimeError(f"El reporte no trae a José y Luqui (trajo: {sorted(nombres)})")
    return datos


def corto(texto, n=220):
    """Corta en la última palabra entera, no en el medio de una."""
    return texto if len(texto) <= n else texto[:n].rsplit(" ", 1)[0] + "…"


def lista(items):
    return "<ul style='margin:4px 0 12px;padding-left:20px'>" + "".join(
        f"<li style='margin:2px 0'>{i}</li>" for i in items) + "</ul>"


def bloque_persona(p, habiles):
    h = p["hizo"]
    hecho = []
    # Se suma por texto: dos códigos que dicen lo mismo («mandado» y «enviado») son una línea.
    por_texto = {}
    for accion, n in h["acciones_web"].items():
        t = ACCIONES.get(accion, accion)
        por_texto[t] = por_texto.get(t, 0) + n
    for que, n in h["contactos"].items():
        t = CONTACTOS.get(que, que)
        por_texto[t] = por_texto.get(t, 0) + n
    for t, n in sorted(por_texto.items(), key=lambda x: -x[1]):
        hecho.append(f"{n} × {html.escape(t)}")
    if h["gastos_cargados"]["filas"]:
        hecho.append(f"{h['gastos_cargados']['filas']} gasto(s) cargado(s) por {plata(h['gastos_cargados']['total'])}")
    if h["movimientos_mp_decididos"]:
        hecho.append(f"{h['movimientos_mp_decididos']} movimiento(s) de Mercado Pago identificados")
    if h["dias_ritmo_declarados"]:
        hecho.append(f"{h['dias_ritmo_declarados']} día(s) declarados sin nada para cargar")
    for v in h["primeras_ventas"]:
        hecho.append(f"<b>Venta nueva:</b> {html.escape(v['alumno'])}, {plata(v['monto'])} ({dia(v['fecha'])})")

    sin = p["dias_habiles_sin_actividad"]
    activos = len(habiles) - len(sin)
    color = "#2E7D32" if activos >= len(habiles) - 1 else "#B26A00" if activos >= 2 else "#C62828"
    out = [f"<h2 style='margin:24px 0 4px;font-size:18px'>{html.escape(p['nombre'])}</h2>",
           f"<p style='margin:0 0 8px;color:{color}'><b>Días con registros en la web: {activos} de {len(habiles)} hábiles</b>"
           + (f" · sin registros: {', '.join(dia(d) for d in sin)}" if sin else "") + "</p>",
           "<p style='margin:8px 0 0'><b>Lo que hizo en la web</b></p>",
           lista(hecho) if hecho else "<p style='margin:4px 0 12px;color:#C62828'>No hay ningún registro suyo en la web esta semana.</p>"]

    pend = p["pendientes"]
    out.append("<p style='margin:8px 0 0'><b>Lo que le quedó sin hacer</b> (su escritorio, hoy)</p>")
    if not pend:
        out.append("<p style='margin:4px 0 12px;color:#2E7D32'>Escritorio vacío: no tiene nada pendiente.</p>")
    else:
        filas = []
        for w in pend:
            monto = f" · {plata(w['plata'])} en juego" if w["plata"] else ""
            urg = " <span style='color:#C62828'>(urgente)</span>" if w["urgencia"] == "alta" else ""
            ej = "".join(f"<div style='color:#666;font-size:13px'>– {html.escape(corto(e))}</div>" for e in w["ejemplos"])
            filas.append(f"{html.escape(w['titulo'])}{urg} · {w['casos']} caso(s){monto}{ej}")
        out.append(lista(filas))
    return "\n".join(out)


def armar(d):
    desde, hasta = d["desde"], d["hasta"]
    principales = [p for p in d["personas"] if p.get("principal")]
    profes = [p for p in d["personas"] if not p.get("principal")]
    cuerpo = [
        "<div style='font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:14px;color:#111;max-width:720px'>",
        f"<h1 style='font-size:20px;margin:0 0 4px'>Reporte del equipo · {dia(desde)} al {dia(hasta)}</h1>",
        "<p style='margin:0;color:#555'>Lo hecho sale de lo que la web registra sola. Lo pendiente es lo que "
        "hoy muestra el escritorio de cada uno. Lo que alguien hizo fuera de la web (un WhatsApp sin la cola, "
        "una planilla) no aparece acá.</p>",
    ]
    for p in principales:
        cuerpo.append(bloque_persona(p, d["dias_habiles"]))
    cuerpo.append("<h2 style='margin:24px 0 4px;font-size:18px'>Profes</h2>")
    clases = d["clasesPorProfe"]
    filas = []
    for p in profes:
        n = clases.get(p["nombre"], 0)
        nombre = NOMBRES_PROFES.get(p["nombre"], p["nombre"])
        filas.append(f"{html.escape(nombre)}: {n} clase(s) en agenda en la semana · {p['total_registros']} registro(s) en el panel")
    otros = {k: v for k, v in clases.items() if k not in {p['nombre'] for p in profes}}
    for k, v in otros.items():
        filas.append(f"{html.escape('Alquileres de cabina' if k == 'Alquiler de cabina' else k)}: {v}")
    cuerpo.append(lista(filas))
    cuerpo.append("<p style='color:#888;font-size:12px'>Generado por facu-os/execution/reporte_equipo.py "
                  "desde la base de astronomyofficial.com. Sólo lee: no cambia nada.</p></div>")
    asunto = f"Astronomy · reporte del equipo · {dia(desde)} al {dia(hasta)}"
    return asunto, "\n".join(cuerpo)


def mandar(asunto, cuerpo_html, para):
    msg = EmailMessage()
    msg["To"] = ", ".join(para)
    msg["Subject"] = asunto
    msg.set_content("Este reporte es HTML: abrilo en un cliente de mail que lo muestre.")
    msg.add_alternative(cuerpo_html, subtype="html")
    crudo = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    gmail().users().messages().send(userId="me", body={"raw": crudo}).execute()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--send", action="store_true", help="Manda el mail. Sin esto, sólo guarda el HTML.")
    ap.add_argument("--para", nargs="+", default=PARA, help="Destinatarios (default: Facu, festevez y Vlado).")
    a = ap.parse_args()

    SALIDA.mkdir(parents=True, exist_ok=True)
    try:
        asunto, cuerpo = armar(juntar())
    except Exception as e:  # noqa: BLE001 — cualquier falla se avisa, no se traga
        print(f"FALLÓ: {e}", file=sys.stderr)
        if a.send:
            mandar("⚠ El reporte del equipo de Astronomy no se pudo armar",
                   f"<pre>{html.escape(str(e))}</pre><p>Log: facu-os/data/logs/reporte-equipo.err</p>",
                   ["facue1900@gmail.com"])
        sys.exit(1)

    archivo = SALIDA / f"reporte-{datetime.now():%Y-%m-%d}.html"
    archivo.write_text(cuerpo)
    print(f"{asunto}\nHTML: {archivo}")
    if a.send:
        mandar(asunto, cuerpo, a.para)
        print(f"Mandado a: {', '.join(a.para)}")
    else:
        print("(sin --send: no se mandó nada)")


if __name__ == "__main__":
    main()
