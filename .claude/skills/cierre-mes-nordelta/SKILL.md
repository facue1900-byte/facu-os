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

Queda a mano interpretar (esto sí lo hago yo, leyendo):

1. Detectar el extracto más nuevo sin conciliar. Si no hay, decirlo y terminar.
2. Caja: que *Saldo Actual* (Caja ARS) sea coherente con ingresos Caja − egresos Caja
   (necesita la base previa, no sale de un mes solo).
3. Explicar cada ⚠ del script: qué es, cuánto es, y qué corrección proponer.

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

## Pendientes

- Migrar las dos tareas programadas (`conciliacion-mensual-paseo-nordelta` día 10 9am,
  `sync-aportes-capital-gastos-obra` diaria 7am) para que apunten a este skill. Hoy
  siguen apuntando a `~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/`.
- El reporte branded en PDF para inversores todavía no es un script: se arma a mano.
  Candidato a `scripts/reporte_inversores.py` cuando se haya hecho 3 veces.
