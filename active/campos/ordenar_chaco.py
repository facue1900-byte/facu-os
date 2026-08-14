#!/usr/bin/env python3
"""Ordena ~/Desktop/Chaco: ~650 PDFs sueltos en una sola carpeta.

Estructura que deja:

    Chaco/
      Guias de traslado/2022..2026/   <- las guías de SENASA, por año
      Reportes historicos/            <- los "reporte historico <campo>", que no son guías
      Otros/                          <- lo que no es ni guía ni reporte
      App IVA Estevez/ Facturas IVA/  <- ya existían, no se tocan
      *.xlsx                          <- las planillas quedan a la vista en la raíz

El año sale del nombre, que sigue la convención
    <cantidad y categoría> <Origen> - <Destino> (DD:MM:AAAA).pdf
con variantes históricas (separador `.`/`-`, día de un dígito, año de dos, sin
paréntesis, y algún typo). Cuando el nombre no dice fecha se usa la fecha de
modificación del archivo: se verificó contra los 504 PDFs que sí la traen en el
nombre y coincide en 502 (99,6%). Cuál de las dos vías se usó queda en el informe.
"""
import argparse
import pathlib
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime

BASE = pathlib.Path.home() / "Desktop" / "Chaco"
GUIAS = BASE / "Guias de traslado"
REPORTES = BASE / "Reportes historicos"
OTROS = BASE / "Otros"

# Formatos de fecha que aparecen de verdad en los nombres, de más a menos estricto.
PATRONES = [
    re.compile(r"(\d{1,2})[:./-](\d{1,2})[:./-](\d{4})"),   # 16:03:2025  01.10.2025  18-11-2025
    re.compile(r"(\d{1,2})[:./-](\d{1,2})[:./-](\d{2})\b"),  # 20:01:23
    re.compile(r"(\d{1,2})[:./-](\d{1,2})(\d{4})"),          # 19:052026 — falta un separador
]

# Reportes de stock / históricos: son fotos del rodeo, no movimientos de hacienda.
ES_REPORTE = re.compile(r"reporte\s+historico|historico\s+stock|reporte\s+stock", re.IGNORECASE)

# PDFs que están en Chaco pero no son del campo.
NO_ES_DEL_CAMPO = {
    "Comunicado IMPORTANTE.pdf",
    "Crew Passport - Juana ;).pdf",
}

# No son papeles del campo: no van a ninguna carpeta de Chaco.
AJENOS = {
    # lista de precios de whisky de la barra de eventos, traspapelada acá
    "Lista 22 de Julio AUTOGESTIONADOS.xlsx",
}


def anio_del_nombre(nombre: str):
    """Primer año plausible que aparezca en el nombre, o None."""
    for patron in PATRONES:
        for m in patron.finditer(nombre):
            dia, mes, anio = (int(g) for g in m.groups())
            if anio < 100:
                anio += 2000
            if not (2015 <= anio <= 2030):
                continue          # 22026 / 2202: es un typo, no un año
            if not (1 <= mes <= 12 and 1 <= dia <= 31):
                continue
            return anio
    return None


def clasificar(p: pathlib.Path):
    """-> (carpeta destino, origen del año) para un archivo suelto."""
    if p.name in NO_ES_DEL_CAMPO:
        return OTROS, "no es del campo"
    if ES_REPORTE.search(p.name):
        return REPORTES, "reporte"
    if p.suffix.lower() != ".pdf":
        return None, "queda en la raiz"      # las planillas xlsx se quedan a la vista

    anio = anio_del_nombre(p.stem)
    if anio:
        return GUIAS / str(anio), "nombre"

    # Sin fecha en el nombre: la fecha de modificación, verificada arriba.
    anio = datetime.fromtimestamp(p.stat().st_mtime).year
    if 2015 <= anio <= 2030:
        return GUIAS / str(anio), "mtime"
    return OTROS, "sin fecha"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mover", action="store_true", help="mueve de verdad (por defecto: dry-run)")
    args = ap.parse_args()

    if not BASE.is_dir():
        sys.exit(f"No existe {BASE}")

    sueltos = [p for p in BASE.iterdir()
               if p.is_file() and not p.name.startswith(".") and not p.name.startswith("~$")]

    plan = []
    cuenta = Counter()
    por_via = Counter()
    muestra_mtime = []

    for p in sorted(sueltos):
        if p.name in AJENOS:
            cuenta["(ajeno, se avisa aparte)"] += 1
            continue
        destino, via = clasificar(p)
        if destino is None:
            cuenta["(xlsx, queda en la raiz)"] += 1
            continue
        plan.append((p, destino / p.name))
        cuenta[str(destino.relative_to(BASE))] += 1
        por_via[via] += 1
        if via == "mtime" and len(muestra_mtime) < 10:
            muestra_mtime.append((p.name, destino.name))

    print(f"Sueltos en la raíz: {len(sueltos)}  |  a mover: {len(plan)}\n")
    for k in sorted(cuenta):
        print(f"  {k:28} {cuenta[k]:4}")
    print("\nDe dónde salió el año:")
    for k, v in por_via.most_common():
        print(f"  {k:12} {v:4}")
    if muestra_mtime:
        print("\nMuestra de los datados por fecha de modificación:")
        for n, a in muestra_mtime:
            print(f"  {a}  <-  {n}")

    # Rule: no se pisa nada. Si el destino existe, se frena entero.
    choques = [d for _, d in plan if d.exists()]
    if choques:
        print(f"\nFRENO: {len(choques)} destinos ya existen. No se movió nada:")
        for d in choques[:20]:
            print(f"  {d}")
        sys.exit(1)

    # Dos archivos distintos que caen al mismo destino también son un choque.
    destinos = defaultdict(list)
    for o, d in plan:
        destinos[d].append(o)
    colisiones = {d: os for d, os in destinos.items() if len(os) > 1}
    if colisiones:
        print(f"\nFRENO: {len(colisiones)} nombres repetidos. No se movió nada:")
        for d, os in list(colisiones.items())[:10]:
            print(f"  {d} <- {[str(o) for o in os]}")
        sys.exit(1)

    if not args.mover:
        print("\n(dry-run — nada se movió. Correr con --mover)")
        return

    for origen, destino in plan:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(origen), str(destino))

    quedan = sorted(p.name for p in BASE.iterdir()
                    if p.is_file() and not p.name.startswith("."))
    movidos = sum(1 for _ in GUIAS.rglob("*.pdf")) if GUIAS.exists() else 0
    print(f"\nMovidos {len(plan)} archivos.")
    print(f"Verificación — PDFs bajo 'Guias de traslado': {movidos}")
    print(f"Quedan sueltos en la raíz ({len(quedan)}): {quedan}")


if __name__ == "__main__":
    main()
