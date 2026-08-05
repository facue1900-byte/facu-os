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

import datetime
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from cargos_del_mes import (  # noqa: E402
    CTAS, LOCALES, Planillas, etiqueta, norm_etiqueta, num, plata,
)

# La cadena del saldo, tolerante al `+` de más que tienen las filas viejas:
#   =+G287+E288-F288   ó   =G51+E52-F52
CADENA = re.compile(
    r"^=\+?([A-Z]+)(\d+)\+([A-Z]+)(\d+)-([A-Z]+)(\d+)$"
)

# Conceptos que llevan IVA cuando el local factura. El resto no debe llevarlo.
CON_IVA = {"alquiler", "servicios comunes"}

# Nombres viejos que se usaron en las pestañas antes de unificar la nomenclatura
# (Volta, MAR'26). Mismo concepto, otro rótulo: si no se mapean, el cruce contra
# CARGOS los reporta como "sobra acá y falta allá" y son la misma plata.
ALIAS = {
    "rec gs fc": "recupero de gastos",
    "alq facturado": "alquiler",
    "gs comunes": "servicios comunes",
    "iva alq": "iva alquiler",
    "dif alq": "diferencia alquiler (sin iva)",
}

# En un local con el alquiler partido, la pestaña lo muestra en dos filas
# ("Alquiler" facturado + "Diferencia Alquiler (sin iva)" en efectivo) mientras
# CARGOS de los meses viejos lo tiene en una sola. Para comparar se suman.
PARTES_DEL_ALQUILER = {"alquiler", "diferencia alquiler (sin iva)"}


def canon(concepto):
    c = concepto.strip().lower()
    return ALIAS.get(c, c)


def col(letra):
    return ord(letra) - ord("A")


def cargos_por_local(p):
    """CARGOS agrupado en {local: {(etiqueta_mes, concepto): total}}.

    CARGOS es la fuente de lo que hay que cobrarle a cada local; la pestaña es
    cómo se le presenta. Si no coinciden, uno de los dos miente — y el que se
    manda al locatario es la pestaña.

    La columna Período es un serial de fecha; se pasa a la etiqueta de la
    pestaña (`ABR'26`) para poder comparar.
    """
    filas = p.leer(CTAS, "CARGOS!A1:H500", render="UNFORMATTED_VALUE")
    out = {}
    for r in filas:
        if len(r) < 4:
            continue
        try:
            serial = int(float(celda(r, 0)))
        except (TypeError, ValueError):
            continue
        fecha = datetime.date(1899, 12, 30) + datetime.timedelta(days=serial)
        local = str(celda(r, 1)).strip()
        concepto = str(celda(r, 2)).strip()
        monto = num(celda(r, 3))
        if not local or not concepto:
            continue
        clave = (norm_etiqueta(etiqueta(fecha.year, fecha.month)),
                 canon(concepto))
        out.setdefault(local, {})
        out[local][clave] = out[local].get(clave, 0.0) + monto
    return out


def celda(fila, idx):
    v = fila[idx] if idx < len(fila) else ""
    return "" if v is None else v


def auditar_local(p, local, cfg, cargos):
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
            # Un concepto puede aparecer DOS VECES bajo el mismo mes de forma
            # legítima: cuando el cargo se partió (a Volta se le saltó un mes de
            # expensas y se le cobró doble al siguiente, en dos filas). Por eso
            # acá sólo se acumula; quién decide si está bien es el cruce contra
            # CARGOS, que tiene el total que se le debe cobrar al local.
            clave = (norm_etiqueta(etq), canon(det))
            previo = vistos[clave][1] if clave in vistos else 0.0
            vistos[clave] = (i, previo + egr)
            if norm_etiqueta(etq) not in bloques:
                orden_bloques.append(norm_etiqueta(etq))
            bloques.setdefault(norm_etiqueta(etq), []).append((i, etq, det, egr))

    # ---- EL cruce: la pestaña contra CARGOS ---------------------------------
    # Lo que se le manda al locatario es la pestaña. Si su total por concepto no
    # es el de CARGOS, se le está cobrando de más o de menos. Se compara la SUMA
    # (un cargo partido en dos filas es válido), y se ignoran las filas de IVA:
    # en CARGOS el IVA va en su propia columna, no como concepto aparte.
    mios = dict(cargos.get(local, {}))
    en_pestania = {k: v for k, (_f, v) in vistos.items()
                   if not k[1].startswith("iva ")}
    if cfg.get("partido"):
        # Se colapsan las dos partes en "alquiler" de los dos lados, porque
        # CARGOS viejo lo tiene entero y el generador nuevo lo parte en dos.
        for tabla in (mios, en_pestania):
            for etq_m in {k[0] for k in tabla}:
                partes = [k for k in tabla
                          if k[0] == etq_m and k[1] in PARTES_DEL_ALQUILER]
                if len(partes) > 1:
                    total = sum(tabla.pop(k) for k in partes)
                    tabla[(etq_m, "alquiler")] = total
    for clave in sorted(set(mios) | set(en_pestania)):
        etq_m, concepto = clave
        # Los alias viejos de Volta ("Gs comunes", "Alq facturado") no matchean
        # por nombre; se avisan aparte y no como diferencia de plata.
        en_c, en_p = mios.get(clave), en_pestania.get(clave)
        if en_c is not None and en_p is not None:
            if abs(en_c - en_p) > 0.01:
                hallazgos.append(
                    (etq_m, "🔴 NO COINCIDE CON CARGOS",
                     f"{concepto}: CARGOS dice {plata(en_c)} y la pestaña "
                     f"{plata(en_p)} — diferencia {plata(en_p - en_c)}"))
        elif en_c is not None and en_c:
            hallazgos.append(
                (etq_m, "🔴 EN CARGOS Y NO EN LA PESTAÑA",
                 f"{concepto} por {plata(en_c)} — no se le está reclamando"))
        elif en_p is not None and en_p:
            hallazgos.append(
                (etq_m, "⚠ EN LA PESTAÑA Y NO EN CARGOS",
                 f"{concepto} por {plata(en_p)} — se le cobra algo que CARGOS "
                 f"no tiene (¿nombre viejo del concepto?)"))

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

    cargos = cargos_por_local(p)
    total_hallazgos = 0
    for local, cfg in LOCALES.items():
        if not cfg.get("pestania"):
            print(f"── {local}: sin pestaña propia (sólo CARGOS) — "
                  f"cobra por {cfg['cobra_por']}\n")
            continue
        hallazgos, bloques, saldo = auditar_local(p, local, cfg, cargos)
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
