# Paseo Nordelta — estado

Última actualización: 2026-07-27

## Qué es

Paseo comercial en Nordelta. 2.292 m². Algunos locales operativos, otros en obra.
La obra se financia casi 100% con capital de socios: **Richi ~$150–161M**,
**Facu ~$23M**, invertido en obra ~$166M (a julio 2026).

> **No confundir con [Nordelta Plaza](../nordelta-plaza/ESTADO.md)** — son dos negocios
> distintos, con sociedades, socios, bancos y carpetas separados. Paseo Nordelta opera
> por el **Banco Macro**; Nordelta Plaza (NDPL SAS) por el **BBVA**.

## Dónde está todo

| Qué | Path |
|---|---|
| Extractos Banco Macro | `~/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/<año>/` |
| Cierre de mes (facturas, impuestos, sueldos) | `~/Desktop/Paseo Nordelta/Principio de mes/` |
| Logos | `~/Desktop/Paseo Nordelta/Logotipos Nordelta Plaza/` |
| Web e informes a inversores | `~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/` |

Sheets: **Master Plan** `1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs` ·
**Gastos Obra** `1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY`

Skill: [`cierre-mes-nordelta`](../../.claude/skills/cierre-mes-nordelta/SKILL.md)

## Último cierre verificado

**Junio 2026** — `conciliar.py` da **CIERRA en los 4 chequeos** (27/07/2026, tras las
correcciones de abajo). Resultado operativo del mes: **$5.218.023** (Caja + Banco ARS,
sin aportes de capital, sin Inversiones, con los ajustes de caja como egreso operativo).
Banco al cierre: $4.119.498,46 (= extracto, al centavo) · USD 0.
**Caja contable al 30/06: −$172.716 (negativa — ver investigación de faltantes abajo).**
Caja contable hoy (libro, 27/07): $3.137.080.

## La rampa de alquileres (lo que más plata mueve)

A julio 2026 cobra alquiler de 5 locales. **$27,4M/mes están sin generar** sobre un
potencial de $51,4M/mes. Cada mes de atraso en un alta cuesta entre $2M y $15M.

| Mes | Alta | Alquiler |
|---|---|---|
| ago-2026 | La Jaula | $2M |
| nov-2026 | Cafetería | $3,5M |
| dic-2026 | Peak One | $4M |
| ene-2027 | Pizzería $2M + Salón Multiespacios $2,5M + Heladería nueva $5M | $9,5M |
| ~jul-2027 | Market | $4M |
| post-Market | Comercios 1 a 6 | $12M |

Run-rate neto comprometido a enero 2027: **$17,12M/mes**.
Peak One y Salón pagan solo expensas hasta nov y dic. La Cafetería paga dos meses de
expensas solas (sep y oct) antes del alquiler.

**Próxima alta a controlar: La Jaula, agosto 2026.**

## Frentes abiertos

- Parrilla para los 354 m² de Fabric: sin firmar. Mudar a Fabric al local de 88,3 m² no
  genera plata ($13,5M en los dos escenarios) — no moverlo sin la parrilla firmada.
- Comercios 1-6 y Market: no construidos. La fecha de los Comercios (2028-01) es un
  placeholder, no un compromiso.
- Se demuele solo la heladería vieja, cuando arranque la nueva.

## Pendientes operativos (de la memoria migrada, 27/07/2026)

- **Bigg debe la mitad en efectivo de julio** (~$1.910.387, "Diferencia Alquiler").
  Es el único que debe efectivo hoy. Ver memoria `paseo-ctas-ctes-import`.
- **La Jaula**: tenía saldo a favor; se le cobra recién desde agosto 2026. Los ~$12,6M
  cargados ene–jul en Ctas Ctes son un estimado inventado y hay que borrarlos.
- Ctas Ctes: `generarCargosDelMes` todavía lee CONTRATOS (valores viejos) en vez de
  Expensas Predio — no activar la generación automática hasta arreglarlo.
- **Faltantes de caja — investigado el 27/07/2026** (fuente: Movimientos + Gastos Obra
  + Dashboard, recalculado en Python):
  - **El problema de fondo no son los $882.814: es que falta el saldo inicial de caja
    de 2026.** El libro arranca en $0 y da negativo en enero (−$2,4M), febrero (−$6,8M)
    y al cierre de junio (−$172.716) — físicamente imposible. Había efectivo previo a
    2026 que nunca se cargó (mismo patrón que el saldo pre-2026 de la CC Bancaria).
    Sin ese ancla, cada "diferencia de caja" mide la deriva de un libro que ya flota.
  - $120.000 de Gastos Obra de junio ("focos de luz" + "flete durlock", 03/06, pagados
    por Facundo) **no están en Movimientos** — si salieron de la caja, son un cuarto de
    la diferencia de junio. El resto de Gastos Obra de junio cruza 1:1 con Movimientos.
  - El ajuste de abril ($409.000, 23/04 "sin detalle") coincide con un día de
    conciliación de la **caja de Mati** (mismo día: "efectivo caja Mati", "Diferencia
    Edenor caja Mati vs facturado"). Hay al menos dos cajas físicas y el libro las
    mezcla en una.
  - Los $19,5M de obra en efectivo de junio están cargados como bolsones al 30/06
    ("Demolición — parte en efectivo", "Galería obra", "Max arquitecto"): con
    reconstrucción a esa escala, $473.814 (2,4% del bolsón) huele a acumulación de
    pagos chicos sin comprobante, no a un faltante puntual.
  - **Actualización (misma noche, del crudo de la app):** gran parte del "nivel que
    flota" ya está explicado y **Facu lo confirmó en julio**: el saldo de caja del
    libro (~$3,4M hoy) incluye **~$3.024.987 que Facu le debe al Paseo** (parte del
    aporte de Richi que entró a su banco personal). La caja física chica sería
    ~$377K. O sea: el número del libro es correcto *con esa deuda adentro*.
  - Lo que queda para que el chequeo mensual (`--caja-contada`) sirva tal cual:
    **bookear la deuda de Facu como movimiento** (egreso de caja "Préstamo a Facu",
    y el ingreso cuando la devuelva). Ahí libro = caja física y cualquier diferencia
    futura es real. El arqueo sigue valiendo como verificación, no como ancla.

## Correcciones aplicadas al Master Plan (27/07/2026, con OK de Facu)

1. `Movimientos!F95` (Tubomarket, marzo): $391.325,00 → **$391.324,31** (lo que movió
   el banco). Saldo Actual quedó = extracto al centavo.
2. Nota en `Movimientos!H312`: el gasto VISA real de junio fue $310.942,98 — $4.887,43
   salieron del saldo pre-2026 de la CC Bancaria, que quedó en $0.
3. `conciliar.py` ahora imprime el resultado operativo del mes separando aportes de
   capital (en junio: $10,4M de aportes sobre $37,4M de ingresos totales).
4. Categoría nueva **"Ajuste de caja"** (`Configuración!C31`, Dashboard fila 76) y
   recategorizadas las dos "Diferencia de caja" que estaban infladas en Inversiones.
   Inversiones bajó $882.814. La caja no cambió ni un centavo (verificado).

## Cuentas corrientes — repaso local por local (cerrado 28/07/2026)

Todos triple-verificados (Movimientos ↔ Cobros ↔ extractos) y con la vía de cobro
marcada en CARGOS ("Cobra por"):

| Local | Vía | Convención | Estado |
|---|---|---|---|
| Fabric | Banco (factura todo) | mes vencido | debe $2.301.918 (esperar extracto jul) |
| Bigg | mitad factura banco + mitad efectivo; expensas banco | **adelantado** | al día |
| Boss | efectivo, redondea | mes vencido | al día |
| Volta + Open | efectivo | mensual | al día · **se va, fecha desconocida** |
| Peak One | efectivo, solo expensas | mes vencido | al día |
| Salón (Alto) | efectivo, expensas $1M (Marina desde mar; penalidad Carolas feb neteada) | mes vencido | al día |
| Escuelita | % de facturación, sin cargo | — | regla propia |
| La Jaula | arranca **agosto 2026** ($1M + $798.825 serv.) | — | primera alta a vigilar |

IPC: `actualizar_ipc.py` completa la tabla INFLACIÓN desde el dato oficial; las
pestañas indexan solas (trimestral). Correr en cada cierre (el IPC sale a mitad de mes).

## Pendiente de dato

- **Fecha de salida de Volta + Open** (Facu: "se va pero no sé exactamente cuándo").
  Atada a la heladería nueva (Shock Ba, dic-26 en CONTRATOS / ene-27 en la rampa).
- **OK de Facu al aumento del Salón por IPC desde agosto** (propuesto: $1.135.751 con
  IPC publicado a junio; recalcular cuando salga julio).
- Bajo qué sociedad opera Paseo Nordelta (NDPL SAS es Nordelta Plaza, no esto).
- Qué relación societaria hay, si hay alguna, entre Paseo Nordelta y Nordelta Plaza.
