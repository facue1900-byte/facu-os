#!/usr/bin/env python3
"""Brief del día de Jarvis: junta los números en CÓDIGO, le pide a Claude que los cuente en voz
alta, lo graba con la voz de la Mac y deja todo en data/jarvis/ para que la pantalla lo muestre.

    /Users/Facu/facu-os/.venv/bin/python /Users/Facu/facu-os/execution/jarvis/brief.py [--sin-voz] [--sin-claude]

Reglas:
- Cada número sale de la función que ya lo calcula (app de Astronomy, leer_meta, radar_deudores):
  acá no se redefine nada. Cada número lleva su fuente.
- Una fuente que falla NO se muestra en cero: va a la lista «Sin dato» con el error (regla 2).
- Cada negocio en su panel: nunca se suman entre sí (regla 8). Meta en USD, Astronomy en ARS,
  sin convertir (regla 7).
- Solo lee. No manda nada a nadie. Sale con código 1 si TODAS las fuentes fallaron.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
import traceback

AQUI = pathlib.Path(__file__).resolve().parent
OS_DIR = AQUI.parents[1]
sys.path.insert(0, str(AQUI.parent))
DATA = OS_DIR / "data" / "jarvis"
APP_ASTRONOMY = pathlib.Path("/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members")
NODE = "/Users/Facu/.local/node/bin/node"
CTAS_CTES_ID = "10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs"
TECHO_PAUTA_USD = 500        # os/03-EMPRESA.md: techo de pauta, sólo Meta, por mes
RADAR_DOC = "https://claude.ai/code/artifact/f91c078c-1bf1-4692-a2d7-1120eb970cc3"


def pesos(n):
    return "$" + f"{round(n):,}".replace(",", ".")


def usd(n):
    return "US$" + f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --- fuentes: cada una devuelve un dict, o tira excepción -------------------------------------

def astronomy():
    p = subprocess.run([NODE, "--env-file=.env.local", "--import", "./scripts/_registrar.mjs",
                        str(AQUI / "astronomy_numeros.mjs")], cwd=APP_ASTRONOMY,
                       capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip().splitlines()[-1] if p.stderr.strip() else f"código {p.returncode}")
    return json.loads(p.stdout.strip().splitlines()[-1])


def pauta():
    sys.path.insert(0, str(OS_DIR / "active" / "astronomy" / "pauta"))
    import leer_meta as lm
    if not lm.TOKEN or not lm.CUENTA:
        raise RuntimeError("falta META_ACCESS_TOKEN o META_AD_ACCOUNT_ID en .env")
    hoy = dt.date.today()
    moneda = lm.cuenta_info().get("currency")
    if moneda not in ("USD", "ARS"):
        raise RuntimeError(f"Meta no devolvió una moneda conocida ({moneda!r})")
    ents, ins7 = lm.traer("ad", (hoy - dt.timedelta(days=6)).isoformat(), hoy.isoformat(), False)
    _, insm = lm.traer("campaign", hoy.replace(day=1).isoformat(), hoy.isoformat(), False)
    if not ents:
        raise RuntimeError("Meta no devolvió ningún anuncio: no informo «0 prendidos» sin dato")
    gasto7 = sum(float(i.get("spend", 0)) for i in ins7)
    chats7 = sum(lm.conversaciones(i)[0] for i in ins7)
    return {
        "moneda": moneda,
        "gasto_7d": round(gasto7, 2),
        "chats_7d": int(chats7),
        "costo_chat_7d": round(gasto7 / chats7, 2) if chats7 else None,
        "gasto_mes": round(sum(float(i.get("spend", 0)) for i in insm), 2),
        "anuncios_activos": sum(1 for e in ents if e.get("effective_status") == "ACTIVE"),
    }


def paseo():
    """Deuda del Paseo desde las PESTAÑAS POR LOCAL de Ctas Ctes (radar_deudores). La consolidada
    «CUENTA CORRIENTE» quedó clavada en jul-26 y el panel mostraba esa deuda vieja (11/11/2026).
    Si la fuente de un local está atrasada, el total NO se muestra: se dice que falta el dato."""
    sys.path.insert(0, str(OS_DIR / ".claude" / "skills" / "cierre-mes-nordelta" / "scripts"))
    import radar_deudores as rd
    from google_auth import bajar_xlsx
    with tempfile.TemporaryDirectory() as d:
        xlsx = pathlib.Path(d) / "ctas_ctes.xlsx"
        bajar_xlsx(CTAS_CTES_ID, xlsx)          # siempre fresco: la copia local envejece
        movs, chequeos = rd.leer_xlsx(xlsx)
    if not movs:
        raise RuntimeError("las pestañas de Ctas Ctes vinieron sin movimientos")
    hoy = dt.date.today()
    deudores, al_dia, con_regla, sin_dato = rd.clasificar(movs, (hoy.year, hoy.month), chequeos)
    deudores.sort(key=lambda x: -x[1]["exigible"])
    return {
        # None = no hay número confiable: alguna fuente está atrasada o no cierra (regla 2)
        "exigible_total": None if sin_dato else round(sum(l["exigible"] for _, l in deudores)),
        "deudores": [{"local": n, "exigible": round(l["exigible"]), "por_banco": n in rd.PAGAN_POR_BANCO}
                     for n, l in deudores],
        "en_curso_total": None if sin_dato else round(sum(l["en_curso"] for _, l in deudores + al_dia)),
        "sin_dato": [{"local": n, "motivo": m} for n, m in sin_dato],
        "al_dia": len(al_dia),
        "con_regla": len(con_regla),
        "movimientos_leidos": len(movs),
        "fuente": "Ctas Ctes · pestañas por local",
    }


def mails():
    from google_auth import cuentas_configuradas, gmail
    out = {}
    configuradas = cuentas_configuradas()
    faltan = [c for c in ("facu", "paseo", "studio") if c not in configuradas]
    if faltan:   # una cuenta que no está no es «0 sin leer»
        print(f"⚠ Gmail sin token para: {', '.join(faltan)}", flush=True)
    for cuenta in ("facu", "paseo", "studio"):
        if cuenta in faltan:
            continue
        lab = gmail(cuenta).users().labels().get(userId="me", id="INBOX").execute()
        out[cuenta] = lab.get("messagesUnread", 0)
    if not out:
        raise RuntimeError("no hay ninguna cuenta de Gmail configurada")
    return out


def tareas():
    sys.path.insert(0, str(AQUI.parent / "radar"))
    import recolectar
    texto, problemas = recolectar.chequeo_tareas(dt.datetime.now().astimezone())
    return {"problemas": problemas, "detalle": texto}


FUENTES = [("Astronomy Academy", astronomy), ("Pauta Meta", pauta), ("Paseo Nordelta", paseo),
           ("Mails", mails), ("Tareas programadas", tareas)]


# --- paneles: los arma el código, no el modelo ------------------------------------------------

def paneles(n):
    out = []
    a = n.get("Astronomy Academy")
    if a:
        out.append({"titulo": "Astronomy Academy", "lado": "izq", "items": [
            {"etiqueta": f"Ingresos {a['mes']}", "valor": pesos(a["ingresos_mes"]),
             "nota": f"{a['movimientos_mes']} movimientos · lib/ingresos (lo mismo que el admin)"},
            {"etiqueta": "Últimos 7 días", "valor": pesos(a["ingresos_7d"]), "nota": f"{a['movimientos_7d']} movimientos"},
            {"etiqueta": "Alumnos activos", "valor": str(a["activos"]), "nota": "sin cuentas internas"},
            {"etiqueta": "Cuotas vencidas", "valor": str(a["vencidos"]), "tono": "alerta" if a["vencidos"] else "bien",
             "nota": ", ".join(f"{v['plan']} ({v['vencia'][8:10]}/{v['vencia'][5:7]})" for v in a["vencidos_detalle"][:4])},
        ]})
    p = n.get("Pauta Meta")
    if p:
        m = p["moneda"]
        fmt = usd if m == "USD" else (lambda x: f"{m} {x:,.2f}")
        out.append({"titulo": "Pauta · Meta Ads", "lado": "izq", "items": [
            {"etiqueta": "Anuncios prendidos", "valor": str(p["anuncios_activos"]),
             "tono": "alerta" if p["anuncios_activos"] == 0 else None},
            {"etiqueta": "Gasto 7 días", "valor": fmt(p["gasto_7d"]),
             "nota": f"{p['chats_7d']} chats de WhatsApp" + (f" · {fmt(p['costo_chat_7d'])} c/u" if p["costo_chat_7d"] else "")},
            {"etiqueta": "Gasto del mes", "valor": fmt(p["gasto_mes"]),
             "tono": "mal" if m == "USD" and p["gasto_mes"] > TECHO_PAUTA_USD else None,
             "nota": f"techo {usd(TECHO_PAUTA_USD)}/mes" if m == "USD" else None},
        ]})
    s = n.get("Paseo Nordelta")
    if s:
        if s["exigible_total"] is None:
            items = [{"etiqueta": "Deuda exigible", "valor": "sin dato", "tono": "mal",
                      "nota": "fuente atrasada o que no cierra: " + "; ".join(
                          f"{x['local']} ({x['motivo']})" for x in s["sin_dato"][:3])}]
        else:
            items = [{"etiqueta": "Deuda exigible", "valor": pesos(s["exigible_total"]),
                      "tono": "alerta" if s["exigible_total"] else "bien",
                      "nota": f"{s['fuente']} · {len(s['deudores'])} deben, {s['al_dia']} al día"}]
        items += [{"etiqueta": d["local"], "valor": pesos(d["exigible"]),
                   "nota": "paga por banco: puede estar en tránsito" if d["por_banco"] else None}
                  for d in s["deudores"][:4]]
        if s.get("en_curso_total") is not None:
            items.append({"etiqueta": "Cobrándose este mes", "valor": pesos(s["en_curso_total"]),
                          "nota": "bloque del mes (alquiler + expensas del anterior): todavía no vencido"})
        out.append({"titulo": "Paseo Nordelta", "lado": "der", "items": items})
    m = n.get("Mails")
    t = n.get("Tareas programadas")
    if m or t:
        items = [{"etiqueta": f"Sin leer · {c}", "valor": str(v), "tono": "alerta" if v > 20 else None} for c, v in (m or {}).items()]
        if t:
            items.append({"etiqueta": "Tareas automáticas con problema", "valor": str(t["problemas"]),
                          "tono": "mal" if t["problemas"] else "bien"})
        out.append({"titulo": "Bandeja y sistema", "lado": "der", "items": items})
    return out


# --- texto hablado ----------------------------------------------------------------------------

PEDIDO = """Armá el brief hablado de esta mañana para Facu. Se va a LEER EN VOZ ALTA apenas se siente.

Números de hoy, calculados por código (es la única fuente de cifras que podés usar; si un número no
está acá, no lo digas):
{numeros}

Fuentes que fallaron hoy (decilo en una frase, sin inventar el dato): {errores}

Además podés leer el doc «Radar Facu» ({radar}) para los pendientes con fecha de hoy o vencidos,
y la memoria de facu-os para el contexto. No leas mails.

Cómo tiene que sonar:
- Arrancá con un saludo de mayordomo según la hora ({hora}), tratándolo de «jefe», con humor seco.
- Después, por negocio y sin mezclar sus números: Astronomy (plata del mes, activos, vencidos, pauta),
  Paseo (quién debe), y el sistema si algo se rompió. Montos redondeados a palabras que se digan bien
  («un millón y medio»), pero sin cambiar el número.
- Cerrá con «Mi recomendación de hoy:» y UNA sola cosa, la que más plata mueve, y preguntá por dónde arranca.
- 120 a 180 palabras. Sin markdown, sin listas, sin links: es audio. Español rioplatense.
Devolvé SOLO el texto a leer."""


def texto_hablado(numeros, errores):
    import telegram_bot as tb
    tb.cargar_env()
    h = dt.datetime.now().hour
    hora = "mañana" if h < 13 else "tarde" if h < 20 else "noche"
    pedido = PEDIDO.format(numeros=json.dumps(numeros, ensure_ascii=False, indent=1),
                           errores=", ".join(f"{e['fuente']}: {e['error']}" for e in errores) or "ninguna",
                           radar=RADAR_DOC, hora=hora)
    texto, _ = tb._correr_claude(pedido, None, instrucciones=(
        "Sos Jarvis, el asistente de Facu. Trabajás en solo lectura. Contestá solamente con el texto pedido."))
    return texto.strip()


def escribir_atomico(p, datos):
    tmp = p.with_name(f"{p.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(datos, ensure_ascii=False, indent=1))
    tmp.replace(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-voz", action="store_true")
    ap.add_argument("--sin-claude", action="store_true", help="sólo números (para probar rápido)")
    args = ap.parse_args()

    import telegram_bot as tb
    tb.cargar_env()
    numeros, errores = {}, []
    for nombre, fn in FUENTES:
        t0 = time.time()
        try:
            numeros[nombre] = fn()
            print(f"✓ {nombre} ({time.time() - t0:.1f}s)", flush=True)
        except Exception as e:
            errores.append({"fuente": nombre, "error": f"{type(e).__name__}: {str(e)[:200]}"})
            print(f"✕ {nombre}: {e}", flush=True)
            traceback.print_exc()
    if not numeros:
        print("Fallaron TODAS las fuentes: no armo brief.", file=sys.stderr)
        return 1

    ahora = dt.datetime.now().astimezone()
    DATA.mkdir(parents=True, exist_ok=True)
    escribir_atomico(DATA / "numeros.json", {"generado": ahora.isoformat(), "numeros": numeros, "errores": errores})
    if args.sin_claude:
        texto = "Brief sólo con números (corrida de prueba sin Claude)."
    else:
        try:
            texto = texto_hablado({k: v for k, v in numeros.items() if k != "Tareas programadas"}
                                  | ({"Tareas programadas": {"problemas": numeros["Tareas programadas"]["problemas"]}}
                                     if "Tareas programadas" in numeros else {}), errores)
        except Exception as e:
            # Sin Claude (red caída a las 07:50, login vencido) los números igual valen: se escriben
            # con un texto de respaldo y el error queda a la vista. Antes se perdía el brief entero.
            errores.append({"fuente": "Texto hablado (Claude)", "error": f"{type(e).__name__}: {str(e)[:200]}"})
            texto = ("Jefe, hoy no pude redactar el resumen hablado, pero los números de la pantalla son de "
                     "recién. Mirá el panel «Sin dato» para ver qué falló.")
    audio = None
    if not args.sin_voz:
        import servidor
        audio = servidor.sintetizar_seguro(texto)
    brief = {"generado": ahora.isoformat(), "texto": texto, "audio": audio,
             "paneles": paneles(numeros), "errores": errores}
    escribir_atomico(DATA / "brief.json", brief)
    print(f"Brief listo: {len(brief['paneles'])} paneles, {len(errores)} fuentes sin dato, audio={audio}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
