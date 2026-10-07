#!/usr/bin/env python3
"""
Compara los JSON de varios auditores independientes y arma el reporte de consenso.

    .venv/bin/python .claude/skills/consenso/scripts/comparar_auditorias.py \
        --input-dir .tmp/consenso --output .tmp/consenso/consenso.md

Regla de fondo: **lo que ven varios auditores por separado vale mucho más que lo
que ve uno solo.** Este script no decide quién tiene razón — separa lo que tiene
respaldo múltiple de lo que lo vio uno solo, y deja los dos grupos a la vista.

El veredicto de consenso es el **más conservador** de todos. Si un auditor de tres
dice NO CIERRA, el consenso es NO CIERRA: en algo que toca plata, la duda de uno
alcanza para frenar.

Cruce de hallazgos: se agrupan por `valor_diferencia` exacto, que es el único
campo que se puede comparar de forma determinística entre auditores. Los que no
tienen valor numérico se listan por separado, sin fingir que se pudieron cruzar.
"""

import argparse
import json
import pathlib
import sys
from collections import defaultdict

VEREDICTOS = ["CIERRA", "CIERRA CON OBSERVACIONES", "NO CIERRA"]
GRAVEDADES = ["grave", "medio", "menor"]
CLAVES = ["veredicto", "resumen", "hallazgos", "no_verificado"]


def cargar(carpeta):
    """Lee los auditor_*.json. Corta si alguno está mal formado."""
    archivos = sorted(carpeta.glob("auditor_*.json"))
    if not archivos:
        sys.exit(f"No hay ningún auditor_*.json en {carpeta}. "
                 "¿Corrieron los auditores?")

    auditorias = []
    for ruta in archivos:
        try:
            d = json.loads(ruta.read_text())
        except json.JSONDecodeError as e:
            sys.exit(f"{ruta.name} no es JSON válido: {e}")

        faltan = [k for k in CLAVES if k not in d]
        if faltan:
            sys.exit(f"{ruta.name} no tiene {faltan}. "
                     "El auditor no siguió el formato: recorrelo.")
        if d["veredicto"] not in VEREDICTOS:
            sys.exit(f"{ruta.name}: veredicto {d['veredicto']!r} inválido. "
                     f"Válidos: {VEREDICTOS}")

        d["_auditor"] = ruta.stem.replace("auditor_", "")
        auditorias.append(d)
        print(f"  {ruta.name}: {d['veredicto']}, "
              f"{len(d['hallazgos'])} hallazgos")

    return auditorias


def cruzar(auditorias):
    """Agrupa hallazgos por valor_diferencia exacto.

    Devuelve (con_valor, sin_valor). `con_valor` es {valor: [hallazgos]}, que es
    el único cruce que se puede hacer sin adivinar: dos auditores que reportan la
    misma diferencia exacta están viendo lo mismo.
    """
    con_valor = defaultdict(list)
    sin_valor = []

    for a in auditorias:
        for h in a["hallazgos"]:
            h = dict(h, _auditor=a["_auditor"])
            v = h.get("valor_diferencia")
            if es_numero(v):
                con_valor[float(v)].append(h)
            else:
                sin_valor.append(h)

    return con_valor, sin_valor


def peor(veredictos):
    """El veredicto más conservador de la lista."""
    return max(veredictos, key=VEREDICTOS.index)


def numero(v):
    """Formato argentino: miles con punto, decimales con coma."""
    return f"{v:,.2f}".translate(str.maketrans(",.", ".,"))


def es_numero(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def orden_gravedad(h):
    g = h.get("gravedad", "menor")
    return GRAVEDADES.index(g) if g in GRAVEDADES else len(GRAVEDADES)


def reporte(auditorias, con_valor, sin_valor):
    n = len(auditorias)
    veredictos = [a["veredicto"] for a in auditorias]
    consenso = peor(veredictos)
    unanime = len(set(veredictos)) == 1

    L = [f"# Consenso de {n} auditores independientes", ""]
    L += [f"## Veredicto: {consenso}", ""]

    if unanime:
        L += [f"Los {n} auditores coincidieron.", ""]
    else:
        L += ["**Los auditores NO coincidieron.** Se toma el más conservador. "
              "Que uno solo haya visto un problema no lo hace falso: lo hace "
              "algo que tenés que mirar vos.", ""]
        L += ["| Auditor | Veredicto |", "|---|---|"]
        for a in auditorias:
            L.append(f"| {a['_auditor']} | {a['veredicto']} |")
        L.append("")

    # Confirmados: mismo valor de diferencia visto por 2 o más.
    confirmados = {v: hs for v, hs in con_valor.items() if len(hs) >= 2}
    solitarios = {v: hs for v, hs in con_valor.items() if len(hs) == 1}

    L += [f"## Confirmados por varios ({len(confirmados)})", ""]
    if not confirmados:
        L += ["_Ninguno. Ningún hallazgo numérico fue visto por dos auditores "
              "con el mismo valor._", ""]
    else:
        L += ["Misma diferencia exacta encontrada por más de un auditor que no "
              "se vieron entre sí. Esto es lo más sólido del reporte.", ""]
        for v in sorted(confirmados, key=lambda x: -abs(x)):
            hs = confirmados[v]
            hs.sort(key=orden_gravedad)
            L += [f"### {hs[0]['concepto']} — diferencia de {numero(v)}", "",
                  f"Visto por {len(hs)} de {n} auditores "
                  f"({', '.join(h['_auditor'] for h in hs)}). "
                  f"Gravedad máxima: **{hs[0].get('gravedad', '?')}**.", ""]
            for h in hs:
                L += [f"- _{h['_auditor']}_: {h['descripcion']}",
                      f"  - fuente: {h.get('fuente', '(no la dijo)')}"]
            L.append("")

    # Lo que vio uno solo: numérico + no numérico.
    uno_solo = [hs[0] for hs in solitarios.values()] + sin_valor
    uno_solo.sort(key=orden_gravedad)

    L += [f"## Vistos por un solo auditor ({len(uno_solo)})", ""]
    if not uno_solo:
        L += ["_Ninguno._", ""]
    else:
        L += ["Puede ser que uno haya sido más fino, o que se haya equivocado. "
              "**Acá hay que decidir a mano.**", ""]
        for h in uno_solo:
            v = h.get("valor_diferencia")
            monto = f" — diferencia {numero(v)}" if es_numero(v) else ""
            L += [f"- **[{h.get('gravedad', '?')}]** {h['concepto']}{monto}  ",
                  f"  {h['descripcion']}  ",
                  f"  _visto solo por {h['_auditor']} · fuente: "
                  f"{h.get('fuente', '(no la dijo)')}_"]
        L.append("")

    # Lo que nadie pudo verificar.
    sin_verificar = [(a["_auditor"], x) for a in auditorias
                     for x in (a["no_verificado"] or [])]
    L += [f"## Sin verificar ({len(sin_verificar)})", ""]
    if not sin_verificar:
        L += ["_Los auditores dicen haber podido verificar todo._", "",
              "Ojo con esto: que ninguno declare huecos es raro. Vale la pena "
              "chequear que efectivamente tuvieron todas las fuentes.", ""]
    else:
        L += ["Lo que quedó sin respaldo. Un número acá **no está verificado**, "
              "aunque el veredicto general diga CIERRA.", ""]
        for auditor, x in sin_verificar:
            L.append(f"- {x}  _({auditor})_")
        L.append("")

    L += ["## Resumen de cada auditor", ""]
    for a in auditorias:
        L += [f"- **{a['_auditor']}** ({a['veredicto']}): {a['resumen']}"]
    L.append("")

    return "\n".join(L), consenso, unanime, len(confirmados), len(uno_solo)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-dir", "-i", required=True,
                   help="Carpeta con los auditor_*.json")
    p.add_argument("--output", "-o", required=True, help="Reporte .md de salida")
    p.add_argument("--minimo", type=int, default=2,
                   help="Mínimo de auditorías para que el consenso valga (default: 2)")
    args = p.parse_args()

    auditorias = cargar(pathlib.Path(args.input_dir))

    if len(auditorias) < args.minimo:
        sys.exit(f"\nSolo hay {len(auditorias)} auditoría(s) y el mínimo es "
                 f"{args.minimo}. Un consenso de uno no es un consenso: "
                 "es una opinión con nombre pomposo.")

    texto, consenso, unanime, n_conf, n_solos = reporte(auditorias,
                                                        *cruzar(auditorias))

    salida = pathlib.Path(args.output)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto)

    print(f"\nVeredicto de consenso: {consenso}"
          f"{'' if unanime else '  (NO fue unánime)'}")
    print(f"  confirmados por varios: {n_conf}")
    print(f"  vistos por uno solo:    {n_solos}")
    print(f"\nReporte: {salida}")

    # Código de salida útil para encadenar: 0 solo si cierra limpio y unánime.
    return 0 if (consenso == "CIERRA" and unanime) else 1


if __name__ == "__main__":
    sys.exit(main())
