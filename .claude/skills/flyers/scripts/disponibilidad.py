#!/usr/bin/env python3
"""La placa de DISPONIBILIDAD de Modo Profesional, generada desde los cupos reales.

    .venv/bin/python .claude/skills/flyers/scripts/disponibilidad.py
    .venv/bin/python .claude/skills/flyers/scripts/disponibilidad.py --formatos story,feed
    .venv/bin/python .claude/skills/flyers/scripts/disponibilidad.py --sin-foto

POR QUÉ EXISTE ESTO
Facu, 11/08/2026: *"a medida que se van completando podemos ir tachando los
bloques"*. Tachar bloques a mano en un diseño es justo el trabajo que este OS
existe para sacar: vuelve cada vez que se vende un lugar, y el día que alguien se
olvida, la story ofrece un martes a las 18 que ya se vendió.

Acá la grilla se lee de la MISMA tabla con la que la web cobra (`pro_cohort_slots`
+ `pro_enrollments`). La placa y el checkout no se pueden separar: si un bloque
aparece tachado es porque está vendido de verdad.

QUÉ TACHA
  · VENDIDO        → cruz blanca. Ese lugar ya no está.
  · FUERA DE VENTA → cruz apagada: no se ofrece en esta edición.
  · LIBRE          → el casillero vacío, como en el diseño original.

Un cupo sin profe asignado se muestra LIBRE, porque para el que compra lo es: lo
que elige es el día y la hora, no el profesor (ver `lib/modoproCohorte.ts`).

Las credenciales salen del `.env.local` de la app, igual que `sync_precios.py`.
"""

import argparse
import base64
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from datetime import date, timedelta

SKILL = pathlib.Path(__file__).resolve().parent.parent
ENV_APP = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/astronomy-members/.env.local"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SALIDA = pathlib.Path.home() / "Desktop/Productoras/Astronomy/Academia/Flyers Academy/disponibilidad"

FORMATOS = {
    "story":  {"w": 1080, "h": 1920},
    "feed":   {"w": 1080, "h": 1350},
    "square": {"w": 1080, "h": 1080},
}
# Debajo de esto un PNG de 1080px es una placa vacía: el render se colgó o el HTML
# no cargó. Mismo criterio que `generar_flyers.py`.
MINIMO_BYTES = 30_000

DIAS = {1: "LUNES", 2: "MARTES", 3: "MIÉRCOLES", 4: "JUEVES", 5: "VIERNES"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


# ---------------------------------------------------------------------------
# LA FUENTE
# ---------------------------------------------------------------------------

def leer_env(path):
    """Parser mínimo de .env: sólo KEY=VALOR, ignora comentarios y vacías."""
    if not path.exists():
        sys.exit(
            f"No encuentro las credenciales en {path}.\n"
            "Sin la base no sé qué cupos están vendidos, y una placa de disponibilidad "
            "inventada es peor que no tener placa. Pasá otro archivo con --env."
        )
    env = {}
    for linea in path.read_text().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def traer(url, key, path):
    req = urllib.request.Request(
        f"{url.rstrip('/')}/rest/v1/{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def hold_vivo(iso, ahora):
    """¿El checkout que retiene este cupo sigue abierto?

    Mismo criterio que `cuposTomados` en lib/modopro.ts. Si acá se contara distinto,
    la placa tacharía un horario que la web sigue vendiendo — o al revés.
    """
    if not iso:
        return False
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")) > ahora


def traer_grilla(url, key, cohorte_id=None):
    """La edición y su grilla, más el set de horarios ya tomados."""
    if cohorte_id:
        q = f"pro_cohorts?id=eq.{urllib.parse.quote(cohorte_id)}&select=*"
    else:
        # La que arranca ANTES entre las que no terminaron: es la que la gente mira.
        q = "pro_cohorts?estado=neq.finalizada&select=*&order=inicio.asc&limit=1"
    cohortes = traer(url, key, q)
    if not cohortes:
        sys.exit("No hay ninguna edición cargada en `pro_cohorts`: no hay disponibilidad que mostrar.")
    coh = cohortes[0]

    cupos = traer(url, key, f"pro_cohort_slots?cohort_id=eq.{coh['id']}&select=*&order=weekday.asc,hora.asc")
    # Un resultado vacío es un error hasta que se demuestre lo contrario (regla 2 de la
    # Constitución): una grilla sin filas daría una placa con TODO libre, que es la
    # mentira más cara de publicar.
    if not cupos:
        sys.exit(f"La edición {coh['id']} no tiene horarios en `pro_cohort_slots`.")

    inscripciones = traer(
        url, key,
        f"pro_enrollments?cohort_id=eq.{coh['id']}&status=in.(pendiente,activa)"
        "&cohort_slot_id=not.is.null&select=cohort_slot_id,status,hold_expires_at",
    )
    ahora = datetime.datetime.now(datetime.timezone.utc)
    tomados = {
        e["cohort_slot_id"] for e in inscripciones
        if e["status"] == "activa" or hold_vivo(e.get("hold_expires_at"), ahora)
    }
    return coh, cupos, tomados


def fecha_larga(iso):
    d = date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month - 1]}"


def fin_del_curso(coh):
    """El viernes de la última semana. Misma cuenta que `finDelCurso` en la app."""
    return (date.fromisoformat(coh["inicio"]) + timedelta(days=(coh["semanas"] - 1) * 7 + 4)).isoformat()


# ---------------------------------------------------------------------------
# LA PLACA
# ---------------------------------------------------------------------------

def armar_html(coh, cupos, tomados, fmt, con_foto):
    f = FORMATOS[fmt]
    horas = sorted({c["hora"] for c in cupos})
    dias = sorted({c["weekday"] for c in cupos})
    por_clave = {(c["weekday"], c["hora"]): c for c in cupos}
    libres = sum(1 for c in cupos if c["abierto"] and c["id"] not in tomados)

    # La foto va embebida como data URI: Chrome renderiza el HTML desde /tmp y no
    # vería una ruta relativa al skill.
    fondo = "background:#000;"
    foto = SKILL / "assets/fotos/cdj-cerca.jpg"
    if con_foto and foto.exists():
        b64 = base64.b64encode(foto.read_bytes()).decode()
        fondo = (
            "background-image:linear-gradient(180deg,rgba(0,0,0,.86) 0%,rgba(0,0,0,.55) 42%,"
            f"rgba(0,0,0,.9) 100%),url(data:image/jpeg;base64,{b64});"
            "background-size:cover;background-position:center 55%;background-color:#000;"
        )

    cruz = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none">'
            '<line x1="8" y1="8" x2="92" y2="92"/><line x1="92" y1="8" x2="8" y2="92"/></svg>')

    filas = []
    for h in horas:
        celdas = [f'<div class="hh">{h:02d}:00 HS -<br>{h + 1:02d}:00 HS</div>']
        for d in dias:
            c = por_clave.get((d, h))
            if c is None:
                celdas.append('<div class="cel"></div>')
            elif c["id"] in tomados:
                celdas.append(f'<div class="cel tachada">{cruz}</div>')
            elif not c["abierto"]:
                celdas.append(f'<div class="cel tachada apagada">{cruz}</div>')
            else:
                celdas.append('<div class="cel"></div>')
        filas.append("".join(celdas))

    encabezados = "".join(f'<div class="dia">{DIAS.get(d, "?")}</div>' for d in dias)

    # El pie es lo que convierte una grilla en una razón para escribir hoy: cuántos
    # quedan y desde cuándo. El número sale contado de la grilla, nunca inventado.
    if libres == 0:
        pie = "SIN LUGARES · ESCRIBINOS PARA LA PRÓXIMA EDICIÓN"
    elif libres == 1:
        pie = f"QUEDA 1 LUGAR · ARRANCA EL {fecha_larga(coh['inicio']).upper()}"
    else:
        pie = f"QUEDAN {libres} LUGARES · ARRANCA EL {fecha_larga(coh['inicio']).upper()}"

    # Escala: el diseño está pensado en 1080 de ancho; los otros formatos son más
    # bajos, así que la grilla se achica para que entre sin recortarse.
    alto_cel = {"story": 108, "feed": 84, "square": 66}[fmt]
    pad_v = {"story": 130, "feed": 74, "square": 56}[fmt]

    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>DISPONIBILIDAD</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:{f['w']}px; height:{f['h']}px; }}
  body {{
    {fondo}
    color:#fff;
    /* Aktiv Grotesk es de pago y no está instalada: Helvetica Neue es su pariente
       más cercano y ya viene en la Mac. Misma pila que el resto de las piezas. */
    font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
    display:flex; flex-direction:column; justify-content:center;
    padding:{pad_v}px 56px;
  }}
  .marco {{ position:absolute; font-size:30px; color:rgba(255,255,255,.55); line-height:1; }}
  .m1 {{ top:44px; left:52px; }} .m2 {{ top:44px; right:52px; }}
  .m3 {{ bottom:44px; left:52px; }} .m4 {{ bottom:44px; right:52px; }}

  .cabecera {{ display:flex; justify-content:space-between; align-items:flex-start; gap:24px; }}
  h1 {{ font-size:46px; font-weight:700; line-height:1.06; letter-spacing:-.01em; text-transform:uppercase; }}
  .rotulo {{ font-family:"Roboto Mono",ui-monospace,Menlo,monospace; font-size:27px; letter-spacing:.02em; color:#fff; white-space:nowrap; }}
  .regla {{ height:1px; background:rgba(255,255,255,.85); margin:26px 0 0; }}

  .tarjeta {{
    margin-top:56px; padding:34px 30px 30px;
    border:1px solid rgba(255,255,255,.16); border-radius:22px;
    background:rgba(255,255,255,.04); backdrop-filter:blur(2px);
  }}
  .grilla {{ display:grid; grid-template-columns:170px repeat({len(dias)},1fr); }}
  .dia {{
    font-family:"Roboto Mono",ui-monospace,Menlo,monospace;
    font-size:21px; letter-spacing:.02em; text-align:center; padding-bottom:22px; color:#fff;
  }}
  .hh {{
    font-family:"Roboto Mono",ui-monospace,Menlo,monospace;
    font-size:21px; line-height:1.35; color:#fff;
    display:flex; align-items:center; padding-right:22px;
  }}
  .cel {{
    height:{alto_cel}px; border:1px solid rgba(255,255,255,.85);
    margin:-.5px 0 0 -.5px; position:relative;
  }}
  /* EL TACHADO. Una cruz dibujada en SVG y no un carácter: tiene que llegar a las
     cuatro esquinas de la celda sin importar cuánto mida, y verse igual a 1080 que
     en la miniatura de la story. */
  .cel svg {{ position:absolute; inset:0; width:100%; height:100%; }}
  .cel svg line {{ stroke:#fff; stroke-width:2.4; vector-effect:non-scaling-stroke; }}
  .tachada {{ background:rgba(255,255,255,.07); }}
  .apagada svg line {{ stroke:rgba(255,255,255,.3); }}
  .apagada {{ background:transparent; }}

  .pie {{
    font-family:"Roboto Mono",ui-monospace,Menlo,monospace;
    font-size:23px; letter-spacing:.06em; margin-top:34px; text-align:center; color:#fff;
  }}
  .leyenda {{
    display:flex; gap:34px; justify-content:center; align-items:center; margin-top:20px;
    font-family:"Roboto Mono",ui-monospace,Menlo,monospace; font-size:17px; color:rgba(255,255,255,.62);
  }}
  .swatch {{ display:inline-block; width:20px; height:20px; border:1px solid rgba(255,255,255,.7); vertical-align:-4px; margin-right:9px; position:relative; }}
  .swatch.x::after {{ content:"✕"; position:absolute; inset:0; font-size:16px; line-height:19px; text-align:center; color:#fff; }}
</style></head><body>
  <span class="marco m1">+</span><span class="marco m2">+</span>
  <span class="marco m3">+</span><span class="marco m4">+</span>

  <div class="cabecera">
    <h1>Curso<br>Profesional de DJ</h1>
    <div class="rotulo">[DISPONIBILIDAD]</div>
  </div>
  <div class="regla"></div>

  <div class="tarjeta">
    <div class="grilla">
      <div></div>{encabezados}
      {"".join(filas)}
    </div>
  </div>

  <div class="pie">{pie}</div>
  <div class="leyenda">
    <span><span class="swatch"></span>LIBRE</span>
    <span><span class="swatch x"></span>TOMADO</span>
  </div>
</body></html>"""


def render(html, destino, fmt):
    f = FORMATOS[fmt]
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="dispo-"))
    try:
        pagina = tmp / "placa.html"
        pagina.write_text(html, encoding="utf-8")
        salida = tmp / "out.png"
        # Nada de `--user-data-dir`: con un perfil nuevo en /tmp el Chrome de macOS
        # se cuelga indefinidamente. Es la misma trampa que documenta generar_flyers.py.
        proc = subprocess.run(
            [
                CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--virtual-time-budget=4000",
                f"--window-size={f['w']},{f['h']}",
                f"--screenshot={salida}", pagina.as_uri(),
            ],
            capture_output=True, text=True, timeout=120,
        )
        if not salida.exists():
            raise RuntimeError(f"Chrome no escribió el PNG.\n{proc.stderr[-800:]}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(salida), destino)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verificar(path, fmt):
    """Problemas de una pieza. Lista vacía = está bien.

    Sin esto, una placa negra de 8 KB pasa por buena y se publica: el render falla
    escribiendo un PNG válido y vacío, no tirando error.
    """
    problemas = []
    if path.stat().st_size < MINIMO_BYTES:
        problemas.append(f"pesa {path.stat().st_size} bytes: parece una placa vacía")
    try:
        from PIL import Image
        with Image.open(path) as im:
            f = FORMATOS[fmt]
            if im.size != (f["w"], f["h"]):
                problemas.append(f"mide {im.size[0]}x{im.size[1]}, esperaba {f['w']}x{f['h']}")
    except ImportError:
        pass
    return problemas


def main():
    ap = argparse.ArgumentParser(description="Placa de disponibilidad de Modo Profesional")
    ap.add_argument("--formatos", default="story", help="story,feed,square")
    ap.add_argument("--cohorte", default=None, help="id de la edición (default: la próxima)")
    ap.add_argument("--sin-foto", action="store_true", help="fondo negro puro, sin la foto de la cabina")
    ap.add_argument("--env", default=str(ENV_APP))
    ap.add_argument("--salida", default=str(SALIDA))
    args = ap.parse_args()

    env = leer_env(pathlib.Path(args.env))
    url = env.get("NEXT_PUBLIC_SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if not url or not key:
        sys.exit("Faltan NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY en el .env.")

    coh, cupos, tomados = traer_grilla(url, key, args.cohorte)
    libres = sum(1 for c in cupos if c["abierto"] and c["id"] not in tomados)
    vendidos = sum(1 for c in cupos if c["id"] in tomados)
    cerrados = sum(1 for c in cupos if not c["abierto"])

    print(f"\nEdición: {coh['nombre']} ({coh['id']}) · {coh['estado']}")
    print(f"  {fecha_larga(coh['inicio'])} al {fecha_larga(fin_del_curso(coh))} · {coh['semanas']} semanas")
    print(f"  {len(cupos)} horarios: {libres} libres · {vendidos} vendidos · {cerrados} fuera de venta\n")

    destino_dir = pathlib.Path(args.salida)
    hechas, rotas = [], []
    for fmt in [x.strip() for x in args.formatos.split(",") if x.strip()]:
        if fmt not in FORMATOS:
            sys.exit(f"Formato desconocido: {fmt}. Son {', '.join(FORMATOS)}.")
        destino = destino_dir / f"disponibilidad__{coh['id']}__{fmt}.png"
        render(armar_html(coh, cupos, tomados, fmt, not args.sin_foto), destino, fmt)
        problemas = verificar(destino, fmt)
        if problemas:
            rotas.append((destino, problemas))
            print(f"  ROTA  {destino.name} — {'; '.join(problemas)}")
        else:
            hechas.append(destino)
            print(f"  ok    {destino}")

    if rotas:
        sys.exit(f"\n{len(rotas)} placa(s) salieron mal. No se publica ninguna de esas.")
    print(f"\n{len(hechas)} placa(s) listas. Se generan de nuevo cada vez que cambia la grilla.\n")


if __name__ == "__main__":
    main()
