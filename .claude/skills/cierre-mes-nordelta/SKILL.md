---
name: cierre-mes-nordelta
description: Cierre de mes de Paseo Nordelta — concilia el extracto del Banco Macro contra el sheet Master Plan, chequea caja, categorías huérfanas y el radar de la rampa de alquileres. Usar cuando Facu pida "cierre de mes", "conciliar el banco", "principio de mes", "cómo venimos con Nordelta", "cuánto falta cobrar", "quién no pagó", "el resultado del mes", o suba un extracto nuevo.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# Cierre de mes — Paseo Nordelta

## Contexto

**Este skill es de Paseo Nordelta, NO de Nordelta Plaza.** Son dos negocios distintos:
otra sociedad, otros socios, otro banco (Paseo → Macro, Plaza → BBVA, NDPL SAS). Nunca
mezclar sus números. Nordelta Plaza no tiene skill todavía.

Paseo Nordelta es el negocio donde Facu más miedo tiene de pifiarla. Todo
número acá se verifica contra la fuente; nada se estima ni se redondea sin avisarlo.
El destinatario final del reporte es **Richi** (Ricardo, inversor, `re1900@gmail.com`),
que puso el ~87% del capital. La pregunta de fondo que el reporte tiene que responder
siempre es **si el negocio operativo cierra o no cierra**, aparte de la inversión.

## Fuentes

**Sheet "Paseo Nordelta 2026 - Master Plan"**
`fileId: 1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`

- **Movimientos** (gid 478887315) — datos crudos del formulario.
  `A=Fecha · B=Tipo(Ingreso/Egreso) · C=Medio(Caja/Banco) · D=Local · E=Categoria ·
  F=Monto · G=Moneda(ARS/USD) · H=Observaciones · I=Mes(ArrayFormula) · J=Resultado`
  **NUNCA escribir en la columna I** — es ArrayFormula y rompe el Dashboard.
- **Dashboard Mensual** — SUMIFS por mes. Ingresos matchean por LOCAL, egresos por
  CATEGORÍA. Las etiquetas de fila las trae desde *Configuración*, no son texto fijo.
- **Saldo Actual** — Caja/Banco en ARS y USD. Son los saldos reales.
- **Configuración** — listas maestras: col A locales, col C categorías. Los locales y
  categorías nuevos se dan de alta acá, NO en el Dashboard. Dólar oficial en F2.

**Gastos Obra** — `fileId: 1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY` (gid 0).
Se completa A=Fecha · B=Persona · C=Descripción · D=Monto · E=Moneda · F=Fx (blue del
día). El resto es automático. La misma plata que en Movimientos es "aporte de capital",
acá figura como el gasto puntual que pagó.

**Extractos Banco Macro** — CC Especial en Pesos `4-452-0960512147-9`.
`~/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/<año>/`
(ej. `Junio 2026.pdf`). Hay además una CC Bancaria `3-452-0942483045-1` donde caen los
cargos VISA — no es la cuenta de trabajo.

**Bajar el sheet**: exportar a `.xlsx` completo. El conector de Drive (`read_file_content`)
**trunca** las hojas largas sin avisar — Movimientos entró cortada en 206 de 455 filas.

```bash
/Users/Facu/facu-os/.venv/bin/python -c "
import sys; sys.path.insert(0, '/Users/Facu/facu-os')
from execution.google_auth import bajar_xlsx
bajar_xlsx('1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs',
           '/Users/Facu/facu-os/data/master_plan.xlsx')"
```

Lectura rápida en vivo por gviz:
`https://docs.google.com/spreadsheets/d/<fileId>/gviz/tq?tqx=out:csv&sheet=<Pestaña>`

## Definiciones que no se negocian

- **INVERSIÓN** = ingresos con Local que empieza con "Aporte de Capital" + egresos con
  Categoría "Inversiones".
- **NEGOCIO** = el resto: ingresos de locales (sin aportes) − egresos operativos (sin
  "Inversiones").
- **Resultado del negocio del mes** = ingresos negocio − egresos negocio.
- **BANCO = el número exacto del extracto.** Todo movimiento de banco tiene que coincidir.
- El saldo de banco NO se calcula sumando Movimientos desde enero (le falta la base
  previa): sale del "SALDO FINAL AL DIA" del extracto.
- USD es marginal (casi todo enero): se netea aparte, no se mezcla en totales ARS.

## Identidad de pagadores en el extracto

- `TEF DATANET PR SUSHINOR SA` (CUIT 30716663279) = **Fabric**
- `TEF DATANET PR RODOLFO SRL` o `CREDIN:...-30716281457` (CUIT 30716281457) = **Bigg**
- `TRANSF ...APC` o glosa de aporte = **Aporte de Capital** (Richi o Facu) → INVERSIÓN,
  no es un local
- Cargos del banco: `DBCR 25413` (Ley 25.413), `Comision Trf MacrOL`,
  `RET ING BRUTOS SIRCREB`, `IMP AFIP` (VEPs)

## Cómo ejecutar

**1. Extracto → filas para Movimientos** (marca las que ya están cargadas):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/extracto_a_movimientos.py" \
  "/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/2026/Junio 2026.pdf" \
  /Users/Facu/facu-os/data/master_plan.xlsx
```

Los cargos bancarios chicos (SIRCREB, Ley 25413, comisiones) se agrupan en una línea
mensual cada uno — criterio verificado contra junio 2026, que cerró al centavo. El neto
se controla contra el extracto **crudo**, no contra el agrupado.

**2. Radar de la rampa de alquileres** (qué alta se atrasó y cuánta plata cuesta):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/radar_rampa.py" \
  /Users/Facu/facu-os/data/master_plan.xlsx 2026-08
```

El mes de corte se pasa siempre a mano: el script no adivina la fecha.

**2-bis. Alerta automática de rampa** (baja el sheet solo y avisa por mail):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/alerta_rampa.py" --mes 2026-08
```

Sin `--send` no manda nada. Flags: `--para` (destinatario; default `MAIL_FACU` del
`.env` — a Richi nunca sin OK) y `--siempre` (manda aunque no haya atrasos). Hay un
plist para correrlo el día 5 de cada mes (`execution/launchd/com.facu.alerta-rampa.plist`)
pero **hoy NO está cargado** en `~/Library/LaunchAgents` — ver `SETUP.md`.

**2-ter. Radar de deudores** (quién debe qué, hoy — Ctas Ctes, sheet
`10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/radar_deudores.py" \
  /Users/Facu/facu-os/data/ctas_ctes.xlsx 2026-07
```

Convención clave: **todos pagan el mes siguiente** — exigible = hasta el mes pasado;
lo del mes corriente está en la calle pero no vencido. Los locales con regla propia
(Escuelita %, Salón solo expensas, La Jaula desde ago-26) viven en `REGLAS` dentro
del script. Los mensajes de cobro los arma el `redactor` y los manda Facu: **nunca
salen solos**.

**2-bis-bis. Publicar el radar en la app del Paseo** (después de correr el radar):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/exportar_ctas_ctes.py" \
  /Users/Facu/facu-os/data/ctas_ctes.xlsx 2026-07 \
  "/Users/Facu/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/App Paseo Nordelta/src/data/ctas-ctes.json"
```

Alimenta la pestaña **Deuda** (`/ctas-ctes`) de la app. Usa las mismas convenciones
que `radar_deudores.py`: si una regla cambia, **cambia en los dos scripts**. La plata
que ya se cobró pero todavía no entró al sheet va en `PENDIENTES_DE_CARGA` — se
muestra como aviso, nunca se suma al saldo, y se saca cuando el dato entra por su
canal normal. Para ver la página sin login: `npm run dev` y abrir
`/preview-ctas.html?w=390&open=1` (`w` simula el ancho del celular, `open` expande
el mes a mes).

**2-quater. Verificar/completar los cargos del mes** (antes del radar):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/generar_cargos.py" \
  /Users/Facu/facu-os/data/ctas_ctes.xlsx 2026-07            # solo reporta
# ... y con --escribir corrige/agrega en CARGOS (no pisa nada con valor)
```

El bloque entero (alquiler del mes + expensas del anterior) lo arma
`cargos_del_mes.py`. Los cuatro números que dependen de un tercero van por flag,
cada uno con su factura archivada en `Facturas de Compra/2026/<Mes>/`:

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/cargos_del_mes.py" \
  2026-09 --congelar-expensas \
  --agua 592225.96 --abl 978731 --avn 2694956.61 --basura 1295041.59 --escribir
```

| Flag | Qué es | De dónde sale |
|---|---|---|
| `--agua` | Agua R&S (C4) | factura de **Redes y Servicios**, dice "Club de Futbol" |
| `--abl` | Municipal (D4) | liquidación de Tigre: **sólo** Tasa Servicios + Cont. Hospital |
| `--avn` | Expensas AVN (B4) | las **4** liquidaciones de la carpeta del mes |
| `--basura` | Retiro de basura (P4) | factura de **Transportes Olivos** ("TODSE") |

**El mes de la factura es el de PAGO**, no el que dice adentro: la expensa del mes M
toma lo que se paga en M, que es lo emitido en M−1.

La fuente de verdad de cada cargo es la **pestaña del local** (alquiler indexado por
IPC, expensas desde Expensas Predio); CARGOS es lo que consume CUENTA CORRIENTE
(pura fórmula, no hay Apps Script que correr). Regla de contrato Bigg: 50%
facturado con IVA + 50% "Diferencia Alquiler" en efectivo sin IVA — el script
avisa si un mes tiene una sola mitad. Las expensas del mes corriente aparecen
recién cuando Expensas Predio cierra el mes: hasta ahí figuran PENDIENTES, no se
inventan. **No activar la "generación automática (día 1)" del menú Apps Script**:
este script la reemplaza con control.

**2-quinquies. Congelar el detalle de expensas** (después de congelar el mes, antes
de mandarle nada a un locatario):

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/congelar_detalle_expensas.py" \
  2026-07 --escribir
```

Facu le manda a cada locatario una **captura del bloque de las filas 40-58 de
Expensas Predio** (locales en columnas), y eso tiene que dar exactamente lo mismo
que su cuenta corriente. Pero ese bloque son dos `TRANSPOSE` sobre la tabla viva de
arriba, **que es de un solo mes**: apenas `A3` vuelve al mes anterior, la captura
muestra otro número que el de la cuenta. El script escribe abajo un bloque literal
por mes, sin fórmulas, con el mismo formato — y **se niega a escribir** si el
detalle no coincide con `EXPENSAS HISTORICO` y con la fila del mes en la pestaña de
cada local. `EXPENSAS HISTORICO` guarda sólo los dos totales, así que el detalle se
reconstruye: los servicios recalculando los `SUMIFS` contra Movimientos, y la AVN
**despejándola** del recupero congelado de un local y validándola contra los otros
16. No congela dos veces el mismo mes.

**2-sexies. Deuda en efectivo, para la app de Mati:**

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/deuda_efectivo.py"
# escribe src/data/deuda-efectivo.json en la app; después: npm run build y deploy
```

Mati sólo ve `/caja`, y ahí arriba está la tarjeta **«A cobrar en efectivo»** con
lo que puede salir a buscar hoy. **No es el saldo**: el saldo mezcla banco con
efectivo. Fabric paga todo por banco y nunca le debe efectivo; Bigg va partido y
sólo la «Diferencia Alquiler (sin iva)» es en mano. **Tampoco es todo deuda**:
todos pagan el mes siguiente, así que se separa lo del mes corriente de lo
vencido cortando por la **última fila de pago** de cada pestaña. Lo que no está
verificado no se muestra como cobrable. La tarjeta se ve aislada en
`preview-deuda.html?w=390`, sin login.

Los locales **sin pestaña** no tienen cargo generado, así que cada uno lleva su
regla explícita en `SIN_PESTANA` (con fecha y con quién la dijo):

| Local | Regla |
|---|---|
| Salón (Alto) | cargos de CARGOS menos cobros |
| **Beto** | fijo, $350.000/mes **desde sep-26**. La deuda vieja quedó saldada |
| **Meta** · **Pole Position** | % de facturación: **no hay cargo fijo**, nunca hay nada que cobrar en mano |
| **La Jaula / torneo** | ago-26 = $372.644 (neto del saldo a favor); de sep-26 en adelante, el precio semestral de `Futbol!AR` |

⚠️ **`Futbol!AR` tiene los doce meses, pero sólo se cobra el pintado de verde**
(marzo y septiembre): el contrato se ajusta por semestre y los meses del medio
son la cadena que va componiendo el IPC, no un precio. Y la cadena atrasa dos
meses — el precio de **septiembre necesita el IPC de julio**, que el INDEC
publica el **15/08**. Si falta en la hoja `INFLACIÓN`, el script lo marca
provisorio y lo saca del total en vez de darlo por bueno.

**3. Conciliación** — los chequeos deterministas los hace el script; yo interpreto:

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/cierre-mes-nordelta/scripts/conciliar.py" \
  "/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/2026/Junio 2026.pdf" \
  /Users/Facu/facu-os/data/master_plan.xlsx 2026-06
```

Chequea NETO banco vs extracto, saldo de cierre vs *Saldo Actual*, presencia de cada
movimiento en los dos sentidos, y categorías huérfanas contra el Dashboard Mensual.
Sale 0 solo si todo CIERRA; cualquier ⚠ da 1 — eso es algo para mirar, no un fallo
del script. **Un ⚠ nunca se esquiva ni se "redondea": se investiga o se le muestra
a Facu.**

**La caja se chequea el mismo día que se anota el extracto** (decisión de Facu,
27/07/2026): pedirle el conteo físico (caja grande + caja de Mati, por separado) y
correr el script con `--caja-contada <total>`. Sin conteo, el script solo recuerda.
**Pendiente estructural**: falta cargar el saldo inicial de caja 2026 — el libro dio
negativo en ene/feb/jun, señal de efectivo pre-2026 nunca cargado. Hasta que Facu
haga un arqueo y se cargue "Saldo inicial caja", el nivel del libro flota.

Queda a mano interpretar (esto sí lo hago yo, leyendo):

1. Detectar el extracto más nuevo sin conciliar. Si no hay, decirlo y terminar.
2. Explicar cada ⚠ del script: qué es, cuánto es, y qué corrección proponer.

**Dólar blue** (para Gastos Obra): histórico
`https://api.argentinadatos.com/v1/cotizaciones/dolares/blue/AAAA/MM/DD` → promedio
(compra+venta)/2. Hoy: `https://dolarapi.com/v1/dolares/blue`.

## Reglas

- **No editar el sheet automáticamente.** Se propone la corrección y se espera el OK de
  Facu. Escribir en los sheets requiere el navegador (Claude in Chrome) y hay que
  preservar todas las fórmulas y la ArrayFormula de la columna I.
- **No mandar el reporte a Richi sin OK.** Si algo no cierra o hay una observación
  clave, avisar primero SÓLO a Facu.
- Si falta un dato, se pide. No se inventa ni se redondea.
- Locales/categorías nuevos: alta en *Configuración*, nunca en el Dashboard.

## Lecciones cargadas

- El conector de Drive truncó Movimientos en 206 de 455 filas **sin error**. Un
  resultado uniformemente vacío o corto es un error hasta que se demuestre lo contrario:
  siempre el export xlsx completo.
- El radar comparaba el cobro del mes sin descontar las expensas (el `piso` daba 0 fijo
  por una condición muerta). Un local que paga expensas altas y cero alquiler aparecía
  como "al día". Arreglado el 27/07/2026.
- El chequeo de huérfanas de `conciliar.py` v1 normalizaba sacando tildes y espacios —
  **más permisivo que el SUMIFS real**, que es sensible a los dos. Un chequeo que replica
  a otro sistema tiene que ser exactamente igual de estricto, ni más ni menos.
- *Saldo Actual* es un SUMIFS sobre TODO el historial, no el cierre del mes: una
  diferencia ahí puede venir arrastrada de meses viejos. `conciliar.py` la descompone
  (el $0,69 "de junio" era en realidad de marzo, fila 95 de Movimientos).
- **Un bloque de cobro son DOS períodos** (expensas de M + alquiler de M+1). Filtrar por
  un solo período dejaba las expensas afuera de la pestaña del local: entraban a CARGOS,
  el script decía "✅ verificado" y "ya estaba", y **el saldo del locatario no las
  reclamaba**. Verificar la tabla principal no protege a la secundaria. (05/08/2026)
- **En la pestaña, la columna "Mes Origen" es el período DEL CARGO, no el del bloque**:
  las expensas de julio van bajo `JUL'26` aunque se cobren junto al alquiler de agosto.
  Se lee mirando un bloque viejo de la planilla, no el docstring del script. Por eso el
  dedupe de pestañas va por el par **(mes, concepto)**: "Servicios comunes" aparece
  legítimamente bajo dos etiquetas.
- **Cada cuenta corriente tiene SUS PROPIAS letras de columna.** No hay un layout único
  y no se puede asumir ninguno: hay que mirar la fila de encabezado de esa pestaña.
  Verificado el 05/08/2026 (Facu lo confirmó):

  | Pestaña | Encabezado | Cargo (egreso) | Saldo | Total del bloque |
  |---|---|---|---|---|
  | `PLANTILLA` | Fecha·Medio·Concepto·FC·Ingreso·Egreso·Saldo | F | G | — |
  | Fabric · Bigg · Boss | Mes Origen·UN·Detalle·FC·Ingreso·Egreso·SALDO | **F** | G | **H** |
  | Peak One | Mes Origen·UN·Detalle·Ingreso·Egreso·SALDO | **E** | F | **G** |
  | Volta + Open 25 | Mes Origen··Detalle·Ingreso·Egreso·SALDO | **E** | F | **G** |

  Peak One y Volta **no tienen columna FC**, así que todo corre una letra a la izquierda.
  Escribir en la columna equivocada pisa el SALDO, que es una cadena encadenada.
- **"Egreso" es lo que hay que COBRARLE al local**, no plata que sale de la caja (Facu,
  05/08/2026). Ingreso = lo que el local pagó.
- **Columna B = Medio** (`efectivo` / `banco`): hoy sólo está puesta en algunas filas de
  pago. Es la que permite saber cuánto se le cobra en efectivo a cada local — lo que
  necesita Mati en `/caja`.
- **Los cobros del inquilino NO se cargan a mano: bajan solos a Q·R·S** (Fecha, Monto,
  Detalle) desde la hoja `Cobros`, que a su vez sale de Movimientos. Nunca inventar ni
  reescribir un pago: se toma de ahí.
- **El total del bloque vive al costado, y cada pestaña lo arma distinto**: Fabric y Boss
  un `TOTAL` en H; Bigg desglosa `Efectivo` y `Total` en H; Volta pone `Banco`/`Efectivo`
  y el total en G; Peak One un `TOTAL` en G. Son fórmulas escritas a mano que referencian
  filas concretas — al agregar un bloque nuevo hay que armarle el suyo.
- **`Salon Multiespacios` NO es una cuenta corriente**: es una pestaña con un `QUERY` en
  `A5` que derrama solo los cobros desde la hoja `Cobros`. No tiene columna de cargos ni
  saldo. Escribir abajo del derrame hace que el próximo cobro choque y tire `#REF!`.
  Va sin pestaña, como La Jaula: sus cargos viven **sólo en CARGOS**. (05/08/2026)
- **El efectivo no se factura.** Se factura lo que se cobra por banco: hoy Fabric entero
  y de Bigg sólo la parte "Alquiler" + su IVA — la "Diferencia Alquiler (sin iva)" es
  justamente la mitad en efectivo. `cobra_por` e `iva` en `LOCALES` ya lo codifican y
  coinciden uno a uno: los que facturan son los que llevan IVA.
- 🚨 **El alquiler NO sube todos los meses: sube en su ANCLA, que está pintada de
  verde** (`#D9EAD3`) en la tabla de IPC de cada pestaña. Fabric, Bigg, Boss, Volta y
  Peak One ajustan **por trimestre** (marzo · junio · septiembre · diciembre); La Jaula
  **por semestre** (marzo · septiembre, en la hoja `Futbol`, columna AR). Los meses del
  medio son la cadena `=N(m-1)*(1+O(m-2))` que va componiendo el IPC — **no un precio a
  cobrar**. Y la cadena atrasa dos meses: septiembre necesita el IPC de julio, que el
  INDEC publica ~el 15/08 y Facu carga en la hoja `INFLACIÓN`.
  Hasta el 01/09/2026 `alquiler_vigente()` copiaba el alquiler del mes anterior, que es
  correcto **en todos los meses menos los de ancla** — y en un mes de ancla cobraba el
  precio viejo sin que nada fallara. Septiembre 2026 era ancla en los seis a la vez:
  **$1.004.358,61 por mes, tres meses seguidos**. Ahora el precio sale del ancla y el mes
  anterior queda como contraste: si difieren, el script dice cuánto y por qué.
- **`--basura` es el gemelo de `--avn` para P4** (Retiro de basura), que estaba clavado a
  `"mayo 2026"` literal y repartía $4.705.450,90 ÷ 3 = $1.568.483,63 todos los meses.
  «TODSE» es **Transportes Olivos S.A.** Sin el flag, el script avisa y dice cuánto está
  repartiendo de más.
- **Una etiqueta de mes se compara normalizada.** En las pestañas conviven `JUL'26`,
  `JUL' 26` y `jul'26`. Un chequeo que comparaba el texto crudo reportó "a Boss no se le
  cobró julio" sobre un alquiler que estaba cobrado: **un faltante de plata se confirma
  mirando la pestaña antes de decirlo.**
- **`--avn` desbloquea el cobro cuando el extracto del Macro no está importado.** `B4`
  es un SUMIFS contra Movimientos: sin extracto da $0 y el generador corta. El flag
  escribe el total de las 4 liquidaciones y restaura la fórmula; **no** carga una fila
  en Movimientos, así que cuando entre el extracto el gasto entra una sola vez. El mes
  queda marcado en `EXPENSAS HISTORICO` como puesto a mano.

## Pendientes

- Migrar las dos tareas programadas (`conciliacion-mensual-paseo-nordelta` día 10 9am,
  `sync-aportes-capital-gastos-obra` diaria 7am) para que apunten a este skill. Hoy
  siguen apuntando a `~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/`.
- El reporte branded en PDF para inversores todavía no es un script: se arma a mano.
  Candidato a `scripts/reporte_inversores.py` cuando se haya hecho 3 veces.
