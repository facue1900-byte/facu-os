#!/usr/bin/env python3
"""
Auditor de las cuentas corrientes — Paseo Nordelta.

    auditar_ctas_ctes.py [AAAA-MM]

Read-only: NO escribe nada, en ningún lado. Revisa pestaña por pestaña que la
cuenta de cada local esté impecable antes de mandársela, y arma el detalle de
qué hay que facturar.

Qué mira, y por qué cada cosa ya falló o puede fallar en silencio:

  · La cadena del SALDO. Cada fila es `=G{n-1}+E{n}-F{n}`. Si en el medio hay
    una constante tipeada a mano o una fórmula que saltea filas, el saldo del
    local es un número perfectamente formado y equivocado. Es EL chequeo: todo
    lo que se le manda al locatario cuelga de acá.
  · Filas con detalle y sin importe, o con importe y sin detalle/mes.
  · Conceptos repetidos bajo el mismo mes — el duplicado se suma solo al saldo.
  · Bloques incompletos: un mes al que le falta un concepto que sus vecinos sí
    tienen (así se detectó que las expensas no llegaban a las pestañas).
  · IVA: que esté donde corresponde y sólo donde corresponde.

Y la parte de facturación: **el efectivo no se factura**. Se factura lo que se
cobra por banco — hoy Fabric entero y la mitad de Bigg (la otra mitad va como
"Diferencia Alquiler (sin iva)", que es la parte en efectivo).
"""

import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cargos_del_mes import (  # noqa: E402
    CTAS, LOCALES, Planillas, norm_etiqueta, num, plata,
)

# La cadena del saldo, tolerante al `+` de más que tienen las filas viejas:
#   =+G287+E288-F288   ó   =G51+E52-F52
CADENA = re.compile(
    r"^=\+?([A-Z]+)(\d+)\+([A-Z]+)(\d+)-([A-Z]+)(\d+)$"
)

# Conceptos que llevan IVA cuando el local factura. El resto no debe llevarlo.
CON_IVA = {"alquiler", "servicios comunes"}


def col(letra):
    return ord(letra) - ord("A")


def celda(fila, idx):
    v = fila[idx] if idx < len(fila) else ""
    return "" if v is None else v


def auditar_local(p, local, cfg):
    """Devuelve (hallazgos, bloques, saldo_final)."""
    hallazgos = []
    lay = cfg["layout"]
    c_det, c_ing = col(lay["detalle"]), col(lay["ingreso"])
    c_egr, c_sal = col(lay["egreso"]), col(lay["saldo"])

    valores = p.leer(CTAS, f"{cfg['pestania']}!A1:H400",
                     render="UNFORMATTED_VALUE")
    formulas = p.leer(CTAS, f"{cfg['pestania']}!A1:H400", render="FORMULA")

    # ---- dónde arrancan los movimientos --------------------------------------
    # Arriba hay un encabezado (Rubro / Nombre / CUIT / Domicilio) y la fila de
    # títulos. Auditarlo da decenas de falsos positivos que entrenan a ignorar
    # el informe, que es exactamente lo que un chequeo no puede hacer.
    primera = 6
    for i, r in enumerate(valores, 1):
        if str(celda(r, 0)).strip().lower().startswith(("mes origen", "fecha")):
            primera = i + 1
            break

    # ---- la cadena del saldo -------------------------------------------------
    # Se audita sólo el tramo con movimientos: abajo hay cientos de filas vacías
    # con la fórmula ya copiada, y ahí un hueco no significa nada.
    ultima = 0
    for i, r in enumerate(valores, 1):
        if str(celda(r, 0)).strip() or str(celda(r, c_det)).strip():
            ultima = i

    anterior = None
    for i in range(primera, ultima + 1):
        # La primera fila de movimientos no arrastra de ninguna: su fórmula es
        # `=E6-F6` o `=+F6`, y eso está bien.
        if i == primera:
            anterior = i
            continue
        f = formulas[i - 1] if i - 1 < len(formulas) else []
        fs = str(celda(f, c_sal)).strip()
        if not fs:
            continue
        if not fs.startswith("="):
            hallazgos.append(
                (f"f{i}", "SALDO TIPEADO A MANO",
                 f"la celda {lay['saldo']}{i} vale {fs!r} en vez de la fórmula "
                 f"— el saldo de acá para abajo no se recalcula"))
            anterior = i
            continue
        m = CADENA.match(fs.replace(" ", ""))
        if not m:
            hallazgos.append(
                (f"f{i}", "SALDO CON FÓRMULA RARA",
                 f"{lay['saldo']}{i} = {fs} (se esperaba "
                 f"={lay['saldo']}{i-1}+{lay['ingreso']}{i}-{lay['egreso']}{i})"))
            anterior = i
            continue
        prev_col, prev_fila = m.group(1), int(m.group(2))
        if prev_col != lay["saldo"]:
            hallazgos.append((f"f{i}", "SALDO ENCADENADO A OTRA COLUMNA",
                              f"{lay['saldo']}{i} = {fs}"))
        elif anterior is not None and prev_fila != i - 1:
            hallazgos.append(
                (f"f{i}", "CADENA DEL SALDO CORTADA",
                 f"{lay['saldo']}{i} arrastra de la fila {prev_fila}, no de la "
                 f"{i-1}: lo que haya entre medio NO se suma al saldo"))
        if int(m.group(4)) != i or int(m.group(6)) != i:
            hallazgos.append((f"f{i}", "SALDO MIRA OTRA FILA", f"{fs}"))
        anterior = i

    # ---- filas y bloques -----------------------------------------------------
    factura = bool(cfg["iva"])
    bloques, vistos, orden_bloques = {}, {}, []
    for i in range(primera, ultima + 1):
        r = valores[i - 1] if i - 1 < len(valores) else []
        etq = str(celda(r, 0)).strip()
        det = str(celda(r, c_det)).strip()
        ing, egr = num(celda(r, c_ing)), num(celda(r, c_egr))
        if not etq and not det and not ing and not egr:
            continue
        # Las etiquetas de mes son texto (JUL'26); un pago lleva la FECHA, que
        # viene como serial. Sólo los cargos entran a los bloques.
        es_mes = bool(etq) and not str(etq).replace(".", "").isdigit()

        if det and not ing and not egr:
            if det.lower().startswith("iva ") and not factura:
                hallazgos.append(
                    (f"f{i}", "fila de IVA que sobra",
                     f"{etq} · {det!r} en $0 — {local} cobra por "
                     f"{cfg['cobra_por']} y no factura"))
            else:
                hallazgos.append((f"f{i}", "FILA SIN IMPORTE",
                                  f"{etq or '(sin mes)'} · {det!r}"))
        if (ing or egr) and not det:
            que = "PAGO SIN DESCRIPCIÓN" if ing else "CARGO SIN DESCRIPCIÓN"
            hallazgos.append(
                (f"f{i}", que,
                 f"{plata(ing or egr)} sin decir de qué — el locatario lo ve así"))
        if egr and not es_mes and det:
            hallazgos.append((f"f{i}", "CARGO SIN MES ORIGEN",
                              f"{det!r} por {plata(egr)} — no cae en ningún bloque"))

        if es_mes and egr:
            clave = (norm_etiqueta(etq), det.lower())
            if clave in vistos:
                fila_previa, monto_previo = vistos[clave]
                if abs(monto_previo - egr) < 0.01:
                    hallazgos.append(
                        (f"f{i}", "🔴 DUPLICADO EXACTO",
                         f"{etq} · {det!r} {plata(egr)} ya estaba en la fila "
                         f"{fila_previa} — se cobra DOS VECES"))
                else:
                    hallazgos.append(
                        (f"f{i}", "🔴 CARGADO DOS VECES CON DISTINTO MONTO",
                         f"{etq} · {det!r}: f{fila_previa} {plata(monto_previo)} "
                         f"y f{i} {plata(egr)} — los DOS suman al saldo "
                         f"({plata(monto_previo + egr)} en total)"))
            vistos[clave] = (i, egr)
            if norm_etiqueta(etq) not in bloques:
                orden_bloques.append(norm_etiqueta(etq))
            bloques.setdefault(norm_etiqueta(etq), []).append((i, etq, det, egr))

    # ---- IVA donde corresponde ----------------------------------------------
    for etq, filas in bloques.items():
        dets = {d.lower() for _, _, d, _ in filas}
        for _, _etq_txt, det, monto in filas:
            base = det.lower()
            if base.startswith("iva "):
                continue
            if base in CON_IVA and factura and f"iva {base}" not in dets:
                hallazgos.append((etq, "FALTA EL IVA",
                                  f"{det} de {plata(monto)} sin su fila de IVA"))
            if base in CON_IVA and not factura and f"iva {base}" in dets:
                hallazgos.append((etq, "IVA DE MÁS",
                                  f"{local} cobra por {cfg['cobra_por']} y no factura"))

    # ---- bloques incompletos -------------------------------------------------
    # Un concepto que aparece en la mayoría de los meses y falta en uno.
    # Se saltean el PRIMER bloque (el local puede haber arrancado a mitad de un
    # concepto) y el ÚLTIMO (sus expensas se calculan recién el mes que viene:
    # el bloque de agosto no tiene las de agosto y eso es correcto).
    medio = orden_bloques[1:-1]
    if len(medio) >= 2:
        frec = {}
        for etq in medio:
            for _, _, det, _ in bloques[etq]:
                if not det.lower().startswith("iva "):
                    frec[det.lower()] = frec.get(det.lower(), 0) + 1
        habituales = {d for d, n in frec.items() if n >= len(medio) - 1}
        for etq in medio:
            dets = {d.lower() for _, _, d, _ in bloques[etq]}
            for falta in sorted(habituales - dets):
                hallazgos.append((etq, "BLOQUE INCOMPLETO",
                                  f"no tiene {falta!r}, que está en los otros meses"))

    saldo = 0.0
    for i in range(ultima, 0, -1):
        r = valores[i - 1] if i - 1 < len(valores) else []
        v = celda(r, c_sal)
        if v not in ("", None):
            saldo = num(v)
            break
    return hallazgos, bloques, saldo


def main():
    mes = sys.argv[1] if len(sys.argv) > 1 else None
    p = Planillas()
    print("AUDITORÍA DE CUENTAS CORRIENTES — Paseo Nordelta")
    print("(read-only: no se escribe nada)\n")

    total_hallazgos = 0
    for local, cfg in LOCALES.items():
        if not cfg.get("pestania"):
            print(f"── {local}: sin pestaña propia (sólo CARGOS) — "
                  f"cobra por {cfg['cobra_por']}\n")
            continue
        hallazgos, bloques, saldo = auditar_local(p, local, cfg)
        estado = "✅ impecable" if not hallazgos else f"⚠ {len(hallazgos)} hallazgo/s"
        print(f"── {local}  «{cfg['pestania']}»  ·  cobra por {cfg['cobra_por']}"
              f"  ·  {'FACTURA' if cfg['iva'] else 'no factura'}")
        print(f"   saldo actual: {plata(saldo)}   {estado}")
        for donde, tipo, detalle in hallazgos:
            print(f"     {donde:>6}  {tipo}: {detalle}")
        total_hallazgos += len(hallazgos)
        if mes:
            filas = bloques.get(norm_etiqueta(mes), [])
            if filas:
                print(f"   bloque {mes}:")
                for _, _, det, monto in filas:
                    print(f"     · {det:<34} {plata(monto)}")
                print(f"     {'TOTAL':<36} {plata(sum(m for _,_,_,m in filas))}")
        print()

    print(f"{'Sin hallazgos.' if not total_hallazgos else f'{total_hallazgos} hallazgo/s en total.'}")


if __name__ == "__main__":
    main()
