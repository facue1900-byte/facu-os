#!/usr/bin/env python3
"""Lee los nombres de las guias de traslado y arma los movimientos.

No abre un solo PDF: todo sale del nombre del archivo.

Dos trampas que resuelve:
  1. Cada traslado aparece DOS veces — la guia y su "Salida de provincia".
     Es el mismo movimiento. Se cuenta una sola vez.
  2. Las guias ANULADAS no son movimientos.

Lo que no puede decidir solo, lo marca como DUDOSO en vez de inventar.
"""
import argparse
import pathlib
import re
import sys
import unicodedata
from collections import defaultdict

# plural del nombre de archivo -> categoria de SIGSA
CATEGORIA = {
    "vaca": "Vaca", "vacas": "Vaca",
    "toro": "Toro", "toros": "Toro",
    "novillo": "Novillo", "novillos": "Novillo",
    "novillito": "Novillito", "novillitos": "Novillito",
    "vaquillona": "Vaquillona", "vaquillonas": "Vaquillona",
    "vaquilla": "Vaquillona", "vaquillas": "Vaquillona",
    "ternera": "Ternera", "terneras": "Ternera",
    "ternero": "Ternero", "terneros": "Ternero",
}

# como se llama cada campo propio en la planilla
CAMPOS = {
    "galicia": "Galicia", "victorina": "Victorina", "colmena": "Colmena",
    "fortin cocherek": "Fortin Cocherek", "cocherek": "Fortin Cocherek",
    "facundo": "Facundo", "sabalo": "Sabalo", "canada rica": "Cañada Rica",
    "patroncito": "Patroncito", "camila": "Camila", "horquilla": "Horquilla",
    "magdalena": "Magdalena",
}


def pelar(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().strip()
    s = re.sub(r"\(.*?\)", " ", s)          # (Talabera), (Don Lucas)
    s = re.sub(r"^(el|la|los|las)\s+", "", s)
    return re.sub(r"\s+", " ", s).strip()


# el mismo destino escrito de dos maneras en los nombres de archivo
ALIAS_DESTINO = {"carnifort": "carfinort", "frigochaco": "frigochaco"}


def destino_norm(nombre):
    d = pelar(nombre)
    return ALIAS_DESTINO.get(d, d)


def campo_propio(nombre):
    return CAMPOS.get(pelar(nombre))


def parse_fecha(txt):
    """Devuelve (aaaa, mm, dd) tolerando los typos del nombre."""
    d = re.findall(r"\d+", txt)
    if len(d) == 2:          # "19:052026" -> dd=19, mm+aa pegados
        dd, resto = d
        mm, aa = resto[:2], resto[2:]
    elif len(d) == 3:
        dd, mm, aa = d
        if len(mm) > 2:
            aa, mm = mm[2:], mm[:2]
    else:
        return None
    aa = aa[-4:] if len(aa) > 4 else aa   # "22026" -> 2026
    try:
        return (int(aa), int(mm), int(dd))
    except ValueError:
        return None


def parse(nombre):
    base = nombre[:-4] if nombre.lower().endswith(".pdf") else nombre
    anulada = "anulada" in base.lower()
    salida = bool(re.match(r"\s*salida de provincia\s+", base, re.I))
    cuerpo = re.sub(r"^\s*salida de provincia\s+", "", base, flags=re.I)
    cuerpo = re.sub(r"^\s*boleta\s+", "", cuerpo, flags=re.I)
    cuerpo = re.sub(r"\s*ANULADA\s*", " ", cuerpo, flags=re.I)

    m = re.search(r"\(([^)]*\d{4}[^)]*)\)", cuerpo)
    if not m:
        return None
    fecha = parse_fecha(m.group(1))
    cuerpo = cuerpo[:m.start()].strip()

    # separar "<cantidades y categorias> <origen> - <destino>"
    if " - " not in cuerpo:
        return None
    izq, destino = cuerpo.rsplit(" - ", 1)
    izq = izq.rstrip(" -")

    # todos los pares "<numero> <categoria>" del principio
    lotes, resto = [], izq
    while True:
        m2 = re.match(r"\s*(\d+)\s+([A-Za-zÀ-ÿ]+)\s*(?:y\s+)?", resto)
        if not m2:
            break
        cat = CATEGORIA.get(pelar(m2.group(2)))
        if cat is None:
            break
        lotes.append((cat, int(m2.group(1))))
        resto = resto[m2.end():]

    origen = resto.strip().lstrip("-").strip()
    if not lotes or not origen:
        return None

    # "Guia 1"/"Guia 2" el mismo dia son traslados DISTINTOS, no duplicados
    mg = re.search(r"gu[ií]a\s*(\d+)", base, re.I)

    return {
        "archivo": nombre, "fecha": fecha, "nro": mg.group(1) if mg else None, "anulada": anulada,
        "es_salida": salida, "lotes": lotes,
        "origen": origen, "destino": destino,
        "origen_campo": campo_propio(origen),
        "destino_campo": campo_propio(destino),
    }


def clave(mv):
    """Identidad del traslado, para juntar la guia con su salida de provincia."""
    return (mv["fecha"], mv["nro"], tuple(sorted(mv["lotes"])),
            pelar(mv["origen"]), destino_norm(mv["destino"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--desde", help="AAAA-MM-DD: solo movimientos posteriores")
    args = ap.parse_args()

    pdfs = sorted(p.name for p in pathlib.Path(args.carpeta).glob("*.pdf"))
    movs, ilegibles = [], []
    for n in pdfs:
        mv = parse(n)
        (movs if mv else ilegibles).append(mv or n)

    if ilegibles:
        print("NO SE PUDO LEER EL NOMBRE (revisar a mano):")
        for n in ilegibles:
            print("  -", n)
        print()

    anuladas = [m for m in movs if m["anulada"]]
    vivas = [m for m in movs if not m["anulada"]]

    # juntar guia + salida de provincia
    grupos = defaultdict(list)
    for m in vivas:
        grupos[clave(m)].append(m)

    unicos, solo_salida = [], []
    for k, g in grupos.items():
        plano = [m for m in g if not m["es_salida"]]
        unicos.append(plano[0] if plano else g[0])
        if not plano:
            solo_salida.append(g[0])

    if anuladas:
        print("ANULADAS (no se cuentan):")
        for m in anuladas:
            print("  -", m["archivo"])
            gemelas = [x["archivo"] for x in unicos if clave(x) == clave(m)]
            if gemelas:
                print("    OJO: hay una guia igual sin ANULADA ->", gemelas[0])
        print()

    if solo_salida:
        print("SOLO EXISTE LA 'Salida de provincia', sin su guia (DUDOSO):")
        for m in solo_salida:
            print("  -", m["archivo"])
        print()

    desde = None
    if args.desde:
        desde = tuple(int(x) for x in args.desde.split("-"))
    post = [m for m in unicos if desde is None or (m["fecha"] and m["fecha"] > desde)]

    print(f"{len(pdfs)} archivos -> {len(unicos)} traslados reales"
          f"{f' -> {len(post)} posteriores a {args.desde}' if desde else ''}\n")

    saldo = defaultdict(lambda: defaultdict(int))
    fuera, dentro = [], []
    for m in sorted(post, key=lambda x: x["fecha"] or (0, 0, 0)):
        f = "{2:02d}/{1:02d}/{0}".format(*m["fecha"]) if m["fecha"] else "??"
        det = " + ".join(f"{c} {cat}" for cat, c in m["lotes"])
        tipo = "interno" if m["destino_campo"] else "SALE"
        print(f"  {f}  {det:32s} {m['origen']:20s} -> {m['destino']:22s} [{tipo}]")
        for cat, c in m["lotes"]:
            if m["origen_campo"]:
                saldo[m["origen_campo"]][cat] -= c
            if m["destino_campo"]:
                saldo[m["destino_campo"]][cat] += c
            else:
                fuera.append((m, cat, c))
        (dentro if m["destino_campo"] else fuera and None)

    print("\nMOVIMIENTO NETO POR CAMPO")
    for campo in sorted(saldo):
        difs = {k: v for k, v in saldo[campo].items() if v}
        if difs:
            print(f"  {campo:16s} " +
                  ", ".join(f"{k} {v:+d}" for k, v in sorted(difs.items())))

    salieron = defaultdict(int)
    for m, cat, c in fuera:
        salieron[cat] += c
    if salieron:
        tot = sum(salieron.values())
        print(f"\nSALIERON DEL CIRCUITO (venta): {tot} cabezas — " +
              ", ".join(f"{k} {v}" for k, v in sorted(salieron.items())))


if __name__ == "__main__":
    main()
