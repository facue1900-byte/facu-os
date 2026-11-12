"""
Cómo cobra cada local del Paseo — **en un solo lugar**.

Esto estaba copiado y pegado en `radar_deudores.py`, `exportar_ctas_ctes.py` y
`deuda_efectivo.py`. El 06/08/2026 Facu cambió las reglas de Beto y de La Jaula,
se tocó **un** script de los tres, y los otros dos siguieron reportando lo viejo
sin que nada fallara: el radar decía «La Jaula: se le cobra recién desde agosto»
mientras la tarjeta de Mati ya mostraba $372.644.

Un dato que vive en tres lados miente en dos. Todo lo que sea *regla de cobro* de
un local va acá y los scripts lo importan.
"""

# ---------------------------------------------------------------------------
# Los que NO se leen como deuda: su saldo en CUENTA CORRIENTE no es plata a
# reclamar. La clave es el nombre tal cual figura en la hoja CARGOS.
# ---------------------------------------------------------------------------
REGLAS = {
    # Ojo: en la planilla «Escuelita» es UN renglón pero son DOS cobradores,
    # Beto y Meta. Partirlos de verdad implica tocar CARGOS y CUENTA CORRIENTE,
    # que es la contabilidad de Facu — hasta entonces, el saldo agrupado no se
    # puede leer como deuda de nadie.
    "Escuelita": "Son DOS cobradores en un renglón: Beto (alquiler fijo de "
                 "$350.000/mes desde sep-26) y Meta (% de facturación, sin cargo "
                 "fijo). La deuda vieja de Beto quedó saldada. El saldo a favor "
                 "que se ve acá es de los pagos sin cargo generado, no es plata "
                 "a devolver.",
    "La Jaula / torneo": "Agosto-26 se le cobra $372.644 (neto del saldo a favor "
                         "que tenían). Desde sep-26 el alquiler sale del precio "
                         "SEMESTRAL de Futbol!AR, el pintado de verde. No pagan "
                         "expensas por ahora.",
}

# Locales que pagan (parte) por banco: esos pagos NO se ven hasta que el extracto
# del mes se anota en Movimientos. Su exigible puede estar sobreestimado mientras
# el mes está abierto (Facu, 27/07/2026).
PAGAN_POR_BANCO = {"Fabric", "Bigg"}

# Pagan el ALQUILER del mes durante el mismo mes (Bigg: Facu 28/07; Fabric: en
# parciales, Facu 11/11/2026). Su cargo "por vencer" en realidad ya está corriendo.
PAGAN_ADELANTADO = {"Bigg", "Fabric"}

# ---------------------------------------------------------------------------
# Las pestañas de cuenta corriente: la FUENTE de la deuda (radar, brief de Jarvis
# y tarjeta de Mati). La consolidada «CUENTA CORRIENTE» era una grilla de filas
# fijas período × local que nadie extendió después de jul-26: el 11/11/2026 el
# brief mostraba la deuda de julio. No se vuelve a leer.
#
# pestaña → (cómo cobra, col detalle, col ingreso, col egreso, col saldo,
#            signo del saldo: +1 si positivo = debe)   — índices 0-based
# El signo se verificó leyendo la cadena el 11/11/2026: Fabric resta los cargos
# (negativo = debe); Bigg, Boss, Volta y Peak One los suman.
# ---------------------------------------------------------------------------
PESTANAS = {
    "Fabric":          ("banco",    2, 4, 5, 6, -1),
    "Bigg":            ("mixto",    2, 4, 5, 6, +1),
    "Boss":            ("efectivo", 2, 4, 5, 6, +1),
    "Volta + Open 25": ("efectivo", 2, 3, 4, 5, +1),
    "Peak One":        ("efectivo", 2, 3, 4, 5, +1),
}

# Cómo se llama en CARGOS / Cobros cada local que NO tiene pestaña. Su deuda sale
# de CARGOS menos Cobros (Caja + Banco), que es lo que hacía la consolidada.
CARGOS_SIN_PESTANA = {
    "Salón (Alto)": ["salon multiespacios"],
    "Escuelita": ["beto escuelita", "meta escuelita", "escuelita"],
    "La Jaula / torneo": ["la jaula"],
}
# Los locales con pestaña aparecen en CARGOS con otro nombre: no se cuentan dos veces.
CARGOS_CON_PESTANA = {"Fabric", "Bigg", "Boss", "Volta + Open", "Volta + Open 25", "Peak One"}


def mes_de_cobro(concepto, periodo):
    """En qué mes se cobra un cargo de una pestaña.

    Cada bloque de cobro del mes M es: **alquiler de M + expensas de M−1**
    (verificado en las cinco pestañas el 11/11/2026: Fabric, Bigg, Boss, Volta y
    Peak One pagan así). O sea: el alquiler se cobra en su propio período; el
    recupero, los servicios comunes, su IVA y las bonificaciones de expensas, al
    mes siguiente. Un concepto que no es ninguna de las dos cosas NO se adivina.
    """
    c = concepto.lower()
    y, m = periodo
    if "alq" in c:
        return periodo
    if any(k in c for k in ("recupero", "servicios", "gs comunes", "rec gs", "expensa")):
        return (y + 1, 1) if m == 12 else (y, m + 1)
    raise ValueError(f"concepto sin regla de cobro: {concepto!r} — agregarlo a "
                     f"reglas_locales.mes_de_cobro, no adivinarlo")

# ---------------------------------------------------------------------------
# Los que no tienen pestaña propia: sus cargos no se generan solos, así que cada
# uno lleva su regla con fecha. Lo consume `deuda_efectivo.py`.
#
#   cta        → cargos de CARGOS menos cobros.
#   porcentaje → paga un % de facturación: NO hay cargo fijo, nunca hay nada que
#                salir a cobrar en mano. Siempre "al día".
#   fijo       → un monto por mes desde `desde` (inclusive).
#   jaula      → agosto-26 es un monto puntual dicho por Facu; de septiembre en
#                adelante sale del precio semestral de la hoja Futbol.
# ---------------------------------------------------------------------------
SIN_PESTANA = {
    "Salón (Alto)": dict(
        regla="cta", alias=["salon multiespacios"], nota=None),
    # Facu, 06/08/2026: la deuda vieja de Beto quedó saldada; hoy está al día y
    # el alquiler de $350.000/mes arranca en septiembre.
    "Beto": dict(
        regla="fijo", alias=["beto escuelita"], monto=350_000, desde=(2026, 9),
        nota="Alquiler $350.000/mes desde septiembre"),
    "Meta": dict(
        regla="porcentaje", alias=["meta escuelita"],
        nota="Paga un % de facturación: no lleva cargo fijo"),
    # Lavadero de autos. Ingreso nuevo, mismo esquema que Meta.
    "Pole Position": dict(
        regla="porcentaje", alias=["pole position"],
        nota="Lavadero — paga un % de facturación: no lleva cargo fijo"),
    # Sus pagos entran bajo «La Jaula». El alias «Alquiler Cancha / Cumpleaños»
    # es OTRA cosa: alquileres sueltos de cancha, que no son el contrato.
    "La Jaula / torneo": dict(
        regla="jaula", alias=["la jaula"], desde=(2026, 8), nota=None),
}

# La Jaula, agosto-26: dicho por Facu el 06/08/2026. NO es el alquiler pleno —
# tenían saldo a favor y esto es lo que queda neto para cobrarles este mes.
JAULA_AGOSTO = 372_644

# ---------------------------------------------------------------------------
# Con qué se matchea, en la APP, un cobro de cada local.
#
# La tarjeta de Mati resta de la foto de la planilla los cobros que él va
# cargando en la app; para eso tiene que saber que la pestaña «Volta + Open 25»
# y el local `volta` son el mismo. Sin esto, un local que ya pagó sigue
# figurando como deudor hasta que alguien toque la planilla a mano.
#
# El valor es el `localId` de la app (tabla `locales`), o la etiqueta de
# categoría cuando NO es un local (Meta cobra aparte pero comparte el renglón
# «Escuelita» con Beto). Tiene que coincidir con `ORIGENES_COBRO` de
# `src/lib/categorias.ts`: si se agrega un local allá, se agrega acá.
# ---------------------------------------------------------------------------
ORIGEN_APP = {
    "Fabric": "fabric",
    "Bigg": "bigg",
    "Boss": "boss",
    "Volta + Open 25": "volta",
    "Peak One": "apex",
    "Salón (Alto)": "salon",
    # Beto y Meta comparten el renglón «Escuelita» en la planilla pero en la app
    # son dos locales (12/08/2026). El id de Beto sigue siendo `escuelita`: los
    # cobros ya cargados y el mapa del sync cuelgan de ese id.
    "Beto": "escuelita",
    "Meta": "meta",
    "Pole Position": "pole-position",
    "La Jaula / torneo": "lajaula",
}
