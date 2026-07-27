---
name: egresos-sistema
description: Sección de Egresos en la app + pestaña Egresos del sheet — registro de toda la plata que sale
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-23T19:41:56.832Z
---

Creado 22/7/2026. Antes el sistema sólo registraba ingresos; la pestaña Finanzas del sheet sumaba cobros y nada más, así que nunca se sabía cuánto quedaba de verdad.

**Qué hay ahora** (`/admin/egresos`, permiso `view_salaries`):
- Resumen del mes: Ingresos − Egresos = Resultado, + desglose "En qué se va" por rubro.
- Detalle con 4 fuentes: sueldos de profes pagados (`salary_payments`), sueldos de equipo (`staff_payments`), **comisión real de Mercado Pago**, y gastos cargados a mano (`expenses`: alquiler/servicios/publicidad/equipos/impuestos).
- Los egresos cuentan cuando la plata SALIÓ, no lo devengado.

**Comisión de MP**: `sales.amount` guarda lo que paga el alumno (`transaction_amount`), no lo que entra. Se agregaron `sales.mp_fee` y `sales.mp_net`; `syncMpFees()` en [[reconciliacion-pagos-sistema]] las rellena (corre en el cron horario sync-sheet). El fee es el egreso más grande después de sueldos.

**Sheet (Base de Clientes, id 1gj2JHtPqS8CGh2IdNa5vijCM3Zez9rNdFOudcRwFDKs)**: la web escribe estas pestañas de finanzas:
- "Finanzas" — ingresos (mirror). "Egresos" — egresos (12 meses).
- **"Finanzas WEB"** — ingresos + egresos de la web UNIFICADOS (auto, cada sync). Esquema: Fecha, Tipo (Ingreso/Egreso), Categoría, Concepto, Medio, Monto (egresos en negativo), Moneda, Nota.
- **"Finanzas (histórico)"** — volcado ÚNICO (no se re-genera) del sheet viejo "Finanzas - Astronomy Academy" (id 19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs), MISMO esquema. 821 filas (512 ing + 309 egr). Se cargó a mano leyendo el CSV del sheet viejo (via connector Drive) y escribiendo con la SA. Si el sheet viejo cambia, re-correr ese backfill.

Ambas hojas (histórico + WEB) comparten esquema para compararlas/mergearlas en el reporte. Facu decidió (2026-07-23, opción B) esto en vez de tocar el sheet del reporte directamente. Ver [[astronomy-finance-report]].

**Pagar sueldos desde la web / transferir por MP**: se decidió NO automatizar la transferencia. La API money-out de MP existe pero necesita aprobación especial y es compleja; no vale la pena. El flujo es "marcar como pagado" (registra el egreso) y la transferencia real se hace a mano.

Archivos: `lib/egresos.ts`, `app/actions/egresos.ts`, `components/EgresoForm.tsx`, `app/admin/egresos/page.tsx`, `supabase/egresos.sql`.

**Hub Finanzas (2026-07-23):** `/admin/finanzas` (`lib/ingresos.ts` + `lib/egresos.ts`). Split de permisos: el **RESUMEN de plata** (Ingresos/Egresos/Resultado neto + desglose por fuente/rubro + **listas minimizables de TODOS los movimientos** de ingresos y egresos) lo ve SOLO el GrandMaster (`ctx.isMaster`); la **parte operativa** ("¿está todo en orden?": nadie debe, nada sin identificar, egresos cargados + accesos) la ven todos los admin con `view_payments`. **Selector de período:** 12 meses + "Todo AÑO" + "Todo (histórico del sistema)". Motores refactorizados a rango: `resumenIngresosRango(admin,from,to)` y `egresosEnRango(admin,from,to,label)`. Nav: "Finanzas (resumen/estado)" arriba de "Plata que entra". **Renombre:** "Pagos" → **"Pagos a identificar"** (bandeja MP sin dueño) vs "Cobros del mes" (cuota mensual).

**Ingresos/egresos manuales ampliados (2026-07-23):** el form de `/admin/egresos` ahora tiene toggle **Egreso/Ingreso**. Categorías egreso nuevas: **Inversiones y mejoras**, **Retiro de ganancias** (además de alquiler/servicios/publicidad/equipos/impuestos/otro). Categorías ingreso: **Aporte de capital**, Otro ingreso. Todo va a la tabla `expenses` con su `category`; `esCategoriaIngreso(cat)` (aporte/otro_ingreso) decide si se lee como ingreso (lib/ingresos) o egreso (lib/egresos los excluye). NO hizo falta tocar la DB. El sync-sheet también suma los aportes al lado de los ingresos.

**Tablero unificado + dolarización (2026-07-23):** Facu pidió integrar TODO el histórico y ver el negocio dolarizado. Implementado:
- **`lib/fxBlue.json`** — serie del dólar blue (promedio compra/venta) por día desde 2023-06 (fuente bluelytics evolution.csv). `rateAt(iso)` en `lib/finanzas.ts` busca el día o el hábil anterior.
- **`lib/historicalMovements.json`** — 802 movimientos del sheet viejo "Finanzas - Astronomy Academy" ANTERIORES al corte, ya dolarizados (ARS↔USD con el blue del día). Es data ESTÁTICA en el repo (no tabla DB — el intento de crear tablas falló por la pestaña Supabase congelada, y además el histórico no cambia).
- **CORTE = 2026-07-01** (`CUTOVER_ISO` en lib/finanzas): antes → histórico (sheet viejo, 2024-01→2026-06); desde → sistema (sales/manual/expenses/sueldos/mp_fee). Junio 2026 está en ambos → el web se clampea a >= corte para NO duplicar.
- **`lib/finanzas.ts`** — motor unificado: `movimientos(admin,from,to)` (histórico JSON + web dolarizado), `serieMensual`, `totales` (ARS+USD), `porCategoria`, `rangoDe(sel)`. La comisión MP se atribuye POR MES (antes egresosEnRango la agregaba en 1 fila al final del rango → descuadraba el neto y el gráfico).
- **`/admin/finanzas`** (solo master ve plata): selector Todo/Año/Mes (desde 2024); 4 tarjetas (Ingresos, Egresos, Resultado neto, Neto de toda la historia) en ARS+USD; **gráfico de barras mes a mes** (`components/MonthlyChart.tsx`, SVG puro, verde/rojo, período resaltado); desglose por categoría; drill-downs "Ver todos los ingresos/egresos" con lista completa. Cifra clave: **neto histórico total = $9.085.440 / u$6.616**.
- **Criterio contable (respondido a Facu):** resultado por FECHA DE TRANSACCIÓN (cuando se cobró/generó), no cuando MP libera. El desfasaje de 35 días es tema de caja, se puede mostrar aparte como "por liquidar" (pendiente).
- **Sheets dolarizados:** "Finanzas (histórico)" (803 filas, one-time) y "Finanzas WEB" (auto en el sync, con Monto ARS + Monto USD) — egresos en negativo, mismo esquema, comparables.
**Ampliación tablero (2026-07-23 b):**
- **Inversiones - Astronomy** (id 1-WquwJQgvsl0mXwdv1Hwz6LJaYMq2rH9S6d9kfR3PTI) IMPORTADA: filtró Business Unit=="Astronomy Academy", fecha < 2024-05 (corte pre-Finanzas, sin duplicar), usa su USD/ARS propio. Sumó 183 mov (equipos Allen Heath/monitores/JBL + acondicionamiento container + muebles + MIDI ≈ inversión inicial). `historicalMovements.json` ahora = 985 mov (jun 2023 → jun 2026). Base64 en scratchpad/inv.b64.
- **Resultado OPERATIVO vs neto total:** `totalesOperativo()` en lib/finanzas saca aportes de capital, retiros de ganancia e inversión (equipos/obra/muebles/midi) → el número de "cómo va el negocio". Cifras "todo": operativo **+$13.740.648 / +u$10.248** (rentable), neto con TODO **+$4.219.321 / −u$1.658** (arrastrado por inversión+retiros). Se muestran las 4 tarjetas: Ingresos, Egresos, Resultado operativo, Resultado neto (con todo).
- **Panel "Inversión vs recuperado"** (`capital()` en lib/finanzas, matchers esInversion/esAporte/esRetiro): Se invirtió u$12.453 (equipos+obra u$8.788 + aportes u$3.665) · Se retiró u$6.784 · **Falta recuperar u$5.669**.
- **Desgloses:** top-6 categorías + `<details>` "＋ ver N más" (antes eran listas larguísimas).
- **Criterio contable confirmado:** por fecha de transacción. El "por liquidar" de MP se descartó (Facu se confundió, no va).
- "Finanzas (histórico)" sheet = 986 filas dolarizadas (con inversión inicial).

**Rediseño tablero (2026-07-23 c):** USD primario, pesos secundarios (chicos). Layout:
- Arriba de todo las **2 cajas clave**: (1) **Caja real hoy** = plata líquida = Σ ingresos − Σ egresos nominal en pesos ($4.219.321), en USD al blue de HOY (u$2.742, NO la suma de mov dolarizados). (2) **Inversión vs recuperado** (capital(): invertido u$12.453, recuperado u$6.784, falta u$5.669).
- Headline: resultado del negocio operativo histórico u$10.248 (+con-todo −u$1.658).
- **Filtro por año con flechas ‹ › + chips** (2023-2026) — reemplazó el `<select>` gigante que scrolleaba mal.
- **Resultado neto del filtro activo** (año o mes, aclarado).
- **Gráfico mes a mes (ene→dic del año)**: barras apiladas con las 4 patas — ingresos (verde, arriba) + egresos (naranja) + inversiones (azul) + retiro de ganancias (dorado) abajo. `serieAno`/`desglose4` en lib/finanzas. `components/MonthlyChart.tsx` reescrito: clickeable (link `?y=&mes=`), en USD.
- **Click en un mes → abre su detalle** (breakdowns top-6 + listas de movimientos), con "✕ cerrar el mes".
- Totales del año abajo del chart (ingresos/egresos/inversiones/retiros/neto).
- PENDIENTE que Facu quería "pensar juntos": la mejor forma del "resultado real del negocio". Hoy: caja real + invertido/recuperado + operativo. Abierto a iterar.

**Ajustes (2026-07-23 d):**
- **CAJA CORREGIDA:** daba $4,2M pero la real es ~$1,5M. NO había duplicados. Causa: el hub sumaba el MES EN CURSO (julio 2026), que tiene ingresos cargados pero egresos/retiros no, y encima MP retiene los cobros ~35 días. Fix: **caja = Σ movimientos AL CIERRE DEL ÚLTIMO MES COMPLETO** (excluye el mes actual) = $1.391.909 ≈ real. La tarjeta aclara "al cierre de {mes} {año}" + muestra el mes en curso como provisional. (Acumulado nominal por año verificado: 2023 −$3,98M · 2024 −$0,44M · 2025 +$6,67M · hasta jun-2026 = +$1,39M.)
- **CHART rediseñado (`components/MonthlyChart.tsx`):** full width (viewBox 0 0 1000 250, width 100%, preserveAspectRatio none, min-width 680, overflow-x auto) y las 4 patas como barras **una al lado de la otra** hacia arriba (no ingresos-arriba/egresos-abajo). Cada mes clickeable. Verificado: 12 meses × 4 series con sus colores.

**Base real + corte agosto (2026-07-23 e):**
- **FUENTE ÚNICA DEL HISTÓRICO = pestaña "Base" del sheet 19N6 (gid=1400774963)** — la SA ya tiene acceso. Es la base reconciliada de Jose (cols: Timestamp, Real Date, ARS_Ammount, USD_Ammount, Category Ingreso/Egreso, Sub Category, Descripción...). 1129 mov, 2024-01 → 2026-07. Acumulado ARS = **$1.697.328 ≈ caja real** (antes daba $4,2M por sumar el mes en curso web). `historicalMovements.json` regenerado desde esta base (USD viene del sheet). OJO: empieza 2024, así que NO tiene la inversión 2023 en equipos → "invertido" ahora es solo aportes de capital (equipos+obra u$0). Si Facu quiere los equipos, agregarlos a la Base.
- **CORTE_ISO → 2026-08-01** (`lib/finanzas`). El web toma la posta en AGOSTO. Caja = cumulative completo (se sacó el truco de "excluir mes en curso" y la mención de los 35 días — Facu dijo que NO retienen 35 días).
- **"Finanzas (histórico)" sheet = réplica EXACTA de la pestaña Base** (1130 filas, script vía SA, one-time). **"Finanzas WEB" arranca agosto** (sync filtra `CORTE_WEB=2026-08-01`; se limpió a mano).
- Bugs UI: scroll de detalle (data-lenis-prevent + overscroll contain) y toggle "ver más/ver menos" (CSS `.fin-det[open]`).
- **Reconciliación jun/jul:** Olivia Sanchez Dubini dada de baja (import no en la base). Aracely (=Ary Juarez, sí está) y Sofía (MP real) se dejaron.

**HISTÓRICO VIVO + inversión 2023 (2026-07-23 f):**
- **`lib/historico.ts` — el histórico ahora se lee EN VIVO** de la pestaña "Base" del 19N6 (gid=1400774963) con la SA (`readSheetValues` en gsheets.ts), cacheado 5 min (`unstable_cache`). Si Jose edita la base, el tablero se actualiza solo. Se eliminó `historicalMovements.json` estático. `lib/finanzas` refactorizado: `histMovs` es async.
- **CAJA = base "base" SOLA** = $1.697.328 ≈ real. NO se le suma el 2023: sumar todos los movimientos 2023 dejaba la caja en −$2,4M (la inversión inicial ya está hundida; la base "base" de 2024→ ya refleja la plata real).
- **Inversión 2023 (equipos+obra, u$7.772) = `lib/inversion2023.json`** (estático, del sheet Inversiones 1-WquwJQ que la SA NO puede leer; el 2023 no cambia). Se suma SOLO al panel "invertido vs recuperado" (const `INVERSION_2023` sumada en `capital()`), no a la caja/totales. Invertido total ahora = u$11.372.
- **"Finanzas (histórico)" sheet ahora se re-sincroniza HORARIO** desde el histórico vivo (se agregó TAB_HISTORICO al cron sync-sheet, 7 pestañas). "Finanzas WEB" arranca agosto.
- Selector de años: 2023→actual (rangoDisponible fijo, ya no depende del array).

**Moneda: PESOS primario (2026-07-23 g):** Facu se arrepintió del USD primario. Ahora **pesos grande + dólar al lado en violeta**, EXCEPTO el panel "inversión vs recuperado" (USD primario, pesos = USD×blue hoy). Caja/operativo/resultado neto/totales año/desglose/movimientos/chart → pesos. Chart usa ingArs/egrArs/invArs/retArs. Helpers `arsHoy(usd)=usd×blueHoy` y `usdHoy(ars)=ars/blueHoy`. Los pesos de montos que cruzan años (invertido, operativo, caja) van a valor de HOY (no suma nominal, que mezclaba pesos de años distintos = daban mal). Para los NETOS de un período, el dólar secundario = `usdHoy(netArs)` así peso y dólar coinciden en signo (antes 2025 daba −$397k / +u$44).
- **Aporte de capital = inversión en el estudio (aclaración de Facu):** son lo mismo, plata que pusieron los dueños. El panel "invertido" ya los suma (equipos+obra u$7.772 + aportes u$3.600 = u$11.372 = total que pusieron los dueños). Se SACÓ el "flujo" operativo que había puesto (mezclaba aportes con la operación, mal planteado). El resultado operativo (u$3.822) es la rentabilidad pura del negocio, APARTE de la plata de los dueños.
- **Waterfall (`components/WaterfallChart.tsx`):** cascada en el panel de inversión: Invirtieron u$11.372 → Recuperaron u$5.478 → Falta recuperar u$5.894. En dólares. (H achicado a 150.)
- **Operativo "sin sentido" — RESUELTO (2026-07-23 h):** mostraba $5,88M porque hacía doble conversión (dolarizado-al-momento × blue hoy). El número REAL de la base = **$3.925.613** (ingresos operativos $65.863.093 − egresos $61.937.480 / u$3.822 dolarizado). Fix: mostrar el NOMINAL de la base + la cuenta a la vista, así Facu lo verifica.
- **REGLA de moneda definitiva:** pesos = NOMINAL (lo que dice la base), dólar secundario = `usdHoy(pesos)` = pesos/blue hoy (mismo signo siempre, valor de hoy). En TODOS lados (caja, operativo, neto período, totales año). EXCEPCIÓN: panel inversión/waterfall = USD dolarizado-al-momento (u$11.372, necesario porque el 2023 tiene inflación extrema), pesos = USD×blue hoy. NO usar dolarizado-al-momento en el resto (confunde).
- **Criterio de moneda DEFINITIVO por Facu (2026-07-23 j):** son DOS criterios distintos a propósito:
  - **Inversión vs recuperado + waterfall → DÓLARES** (dolarizado al día de cada transacción): invirtieron u$11.372 (equipos u$7.772 + aportes u$3.600), recuperaron u$5.478, falta **u$5.894**. La FALTA se muestra en dólares porque hay que recuperarla en dólares sí o sí; su peso va al **blue de HOY EN VIVO**. Pesos secundarios = USD × blue hoy. FilaCap y WaterfallChart → USD-primero. (Se revirtió el intento de ponerlo en pesos nominales.)
  - **Operativo + puente + caja + períodos → PESOS** (nominal del momento): operativo = ingresos−egresos $3.925.613; puente = operativo + aportes $4.631.116 − retiros $6.859.401 = caja $1.697.328. Los retiros dan distinto en el panel USD (u$5.478) vs el puente (pesos $6.859.401) A PROPÓSITO — distinto criterio para distinto fin.
- **Blue EN VIVO (`getBlueHoy` en lib/finanzas):** fetch a bluelytics `/v2/latest`, cacheado 1h (unstable_cache), fallback a la serie fija. El tablero usa este para las conversiones "a hoy" (arsHoy/usdHoy), así la falta-recuperar en pesos está activa 24/7.
- **BridgeChart = fila de números (2026-07-23 k):** Facu odió las barras (anchas, pixeladas por el preserveAspectRatio="none"). Ahora NO es SVG: es una fila HTML limpia — nombre arriba + monto grande abajo por paso, con operadores +/−/= entre medio, caja resaltada. "OPERATIVO $3.925.613 + APORTES $4.631.116 − RETIROS $6.859.401 = CAJA $1.697.328". (El WaterfallChart de inversión SÍ sigue siendo barras SVG, ese no lo criticó.)
- **Puente operativo→caja (`components/BridgeChart.tsx`):** mini-waterfall abajo del resultado operativo: **Operativo +$3.925.613 → +Aportes +$4.631.116 → −Retiros −$6.859.401 → =Caja $1.697.328**. Explica que la CAJA (todos los ingresos−egresos = $1.697.328) ≠ el OPERATIVO (solo operativos = $3.925.613); la diferencia son aportes(+) y retiros(−). Componente genérico de waterfall bridge (steps con delta + total).
