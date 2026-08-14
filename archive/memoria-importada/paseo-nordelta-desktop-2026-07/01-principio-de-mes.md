# MEMORIA — Paseo Nordelta (Claude, leer al iniciar cada sesión)

> Este archivo guarda todo el contexto del proyecto para que Claude retome el trabajo
> aunque se cambie de cuenta o de sesión. Si sos Claude y estás leyendo esto: este es
> tu punto de partida. Facundo administra **Paseo Nordelta**, un complejo comercial en Nordelta.
>
> Última actualización: julio 2026 (sesión 4).

## 🔵🔵 REGLA FIJA — VERIFICAR SIEMPRE DESPUÉS DE CARGAR MOVIMIENTOS
**Cada vez que cargues movimientos (por formulario o a mano), verificá SIEMPRE:**
1. **Dashboard Mensual** (maestro): que los números cuadren / que el/los movimiento(s) se hayan reflejado en el mes y medio (Caja/Banco) correctos.
2. **Ingresos → cta cte:** si hay un ingreso a un local, chequear que quedó bien anotado en la cta cte que corresponde (panel "COBROS DEL INQUILINO (auto)" de las viejas, ledger de las nuevas, o la lista de Alquiler Cancha en Futbol).
- Es una **rutina fija**, no opcional. Ya cazó un bug real (ver sesión 4: filtro de Alquiler Cancha).
- Preferencia de Facu: hacerlo directo en el momento (no hace falta scheduled).

## ⚡ ESTADO ACTUAL (jul 2026, sesión 4) — leer primero
- **CTAS CTES — nuevo esquema (sesión 4):** decisión de Facu de unificar cómo se muestran los cobros.
  - **Cuentas nuevas (12): Cafetería, Salon Multiespacios, Shock Ba, Futura Parrilla, Canchera, Market, Comercio 1-6.** Quedaron con layout: **título (A1) + "Inquilino (Local)" (A3/B3, B3 = local, NO borrar, la usa el panel) + panel "COBROS DEL INQUILINO (auto)" (A4 título, A5 fórmula QUERY que se auto-adapta por B3, spillea Fecha/Monto/Detalle) + cuadro de inflación (L7:O31)**. Se les **sacó el ledger** y la **sección de cargos (I:K)**. El panel usa: `=QUERY(Cobros!A3:E,"select Col1,Col3,Col5 where lower(Col2)='"&LOWER($B$3)&"' order by Col1 label Col1 'Fecha',Col3 'Monto',Col5 'Detalle'",0)`. Salon es el molde (tiene 5 cobros reales). PLANTILLA quedó también con el cuadro de inflación en blanco.
  - **Cuentas viejas (5): Boss, Bigg, Fabric, Volta+Open 25, Peak One.** Se dejaron con su **ledger detallado intacto** (IVA, servicios, cajas de TOTAL, tabla IPC) + se les agregó/verificó el **panel "COBROS DEL INQUILINO (auto)"** al costado (en **columna Q**, con una columna de espacio (P) respecto al cuadro de inflación). Boss ya lo tenía; a Bigg/Fabric/Volta/Peak se los agregué. Panel de las viejas usa nombre de local **hardcodeado** (Boss='hamburgueseria', Volta='heladeria', Bigg='bigg', Fabric='fabric', Peak='peak one'). Formato del panel: header navy, fecha date, monto currency rounded.
  - **Cuadro de inflación en blanco** agregado a las 12 nuevas + PLANTILLA (Mes/Alquiler/IPC Trimestral en L7:O31, meses 2026-2027, con % de IPC pero **Alquiler en blanco y sin verde** — Facu completa alquiler + verde).
- **Futbol NO se tocó** (Facu: no les cobra expensas). Los 3 bloques (La Jaula, Beto Escuelita, Meta Escuelita) siguen mostrando el cobro en el ledger. La lista **Alquiler Cancha** (AK) SÍ se arregló (ver bug abajo).
- **Formato lindo** aplicado a las 12 nuevas + Cobros (header navy, negritas). Futbol ya tenía navy.

### 🔴 BUG ARREGLADO (sesión 4) — filtro Alquiler Cancha
La lista **Alquiler Cancha / Cumpleaños** del tab Futbol (AK5) y su Total (AL2) filtraban el local `="alquiler cancha"` **exacto**, pero el **Formulario carga el local como "Alquiler Cancha / Cumpleaños"** → nunca matcheaba (lista vacía siempre). **Arreglado** con filtro *contiene*: `ISNUMBER(SEARCH("alquiler cancha",LOWER(Cobros!B3:B)))` en AK5 y AL2. Ahora aparecen todos los cobros de cancha (recuperó 3 de abril + el nuevo). También se le puso formato de fecha a la columna AK.
- **LECCIÓN:** el nombre de local canónico que produce el Formulario es **"Alquiler Cancha / Cumpleaños"** (no "Alquiler Cancha"). Cualquier fórmula que filtre ese local debe usar el nombre completo o un *contains*.

### 🔴 FORMULARIO se quedó sin filas (sesión 4) — arreglado, ojo a futuro
Movimientos es una **Tabla** ("Form_Responses"). La grilla se quedó **sin filas vacías debajo de los datos** (terminaba justo en la última fila), y el Formulario **no tenía dónde escribir** → los envíos fallaban por completo (ni en la hoja ni en las respuestas del form). Pasó porque se borraron filas (impuestos duplicados) y quedó sin colchón.
- **Arreglado:** agregué **~50 filas vacías** de colchón al final (Insert → filas abajo). Probado con una carga de prueba: funciona.
- **REGLA:** **NUNCA dejar Movimientos sin filas vacías debajo de los datos.** Si borrás filas cerca del final, agregá colchón. Si el form deja de escribir, la causa #1 es esta.
- Los movimientos que Facu cargó mientras estaba sin espacio **se perdieron** (no quedaron ni en el form). Se recargaron a mano (ver abajo).
- **Para cargar movimientos a mano en Movimientos** (rápido y confiable): posicionarse en la primera celda vacía de la fila (columna A) y tipear con **Tab real** entre columnas y **Enter** al final (el Enter vuelve a la columna A de la fila siguiente). El **name box es poco confiable** (trae basura "A255A1AP"); mejor navegar clickeando una celda de datos y bajar. Columnas: A=fecha (ej "8/7/2026" = 8 de julio, formato d/m/yyyy), B=Tipo, C=Medio, D=Local (solo ingresos de local), E=Categoria (solo egresos), F=Monto, G=Moneda (ARS/USD), H=Obs. **NO escribir en la columna I (Mes, ArrayFormula).**

### Movimientos cargados a mano (sesión 4, 7-8/jul)
Aportes de Capital Richi (Caja/efectivo): $9.000.000, $6.000.000, $14.000.000 (el $5.530.000 del 7/7 ya estaba, no se duplicó). Egresos (Caja): Municipal $5.527.103; Inversiones $10.284.052 (1ra cuota 1/3 derechos de construcción); Inversiones $15.690.961 (1ra cuota 1/6 plan de pagos fondo y áridos); Ladrillos $10.647; Caños $140.558; Diferencia sueldo Matías $793.056 (Sueldo Admin MB); Trabajo canaletas galería $500.000; Rejilla y desagüe café $360.000; Rejillas/codos $67.507 (todos Mejoras). Ingresos (Caja): Marina evento alquiler de cancha $400.000 (Local "Alquiler Cancha / Cumpleaños"); Volta $200.000 (Local "Heladeria"). NO se cargó "recibí de Facu $300.000" (pedido de Facu).

## Estado heredado (sesiones previas, sigue vigente)
- **Maestro** = "Paseo Nordelta 2026 - Master Plan" (id `1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`).
- **Ctas Ctes NATIVO** id **`10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`**.
- Pestaña **"Cobros"** (gid 904807272) = ÚNICO IMPORTRANGE al maestro. FUNCIONA. Columnas: A=Fecha, B=Local, C=Monto, D=Medio, E=Detalle. Datos desde fila 3. Fórmula A2: `=QUERY(IMPORTRANGE("1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs","Movimientos!A2:H"),"select Col1,Col4,Col6,Col3,Col8 where lower(Col2)='ingreso' and Col4 is not null order by Col1 ...",0)`.
- **PLANTILLA (gid 1893149501):** template. OJO: en sesión 4 se le cambió el layout a las cuentas nuevas (panel a la izquierda, sin ledger/cargos) pero la PLANTILLA quedó con su estructura anterior + cuadro de inflación en blanco. Si creás una cuenta nueva, mejor duplicar Salon Multiespacios (ya tiene el layout nuevo).
- **Reconciliación banco junio 2026:** conciliado al centavo. Dashboard Mensual banco cierre junio = $4.119.498,46 = extracto. Los "DBCR 25413 feb/mar/abril" que estaban cargados eran **duplicados** (el impuesto ley 25413 ya venía en el saldo como líneas chicas) → se borraron, y TODOS los meses cuadran contra el banco. La cuenta bancaria del Dashboard es la PESOS especial 4-452-0960512147-9.
- **Caja / los $300.000 (NO es un desfasaje real):** el Dashboard ya incluía $300.000 que Facu le debía dar a Mati (estaban contabilizados en el accounting, pero Mati todavía no los tenía físicamente en la caja). Mati registró en su conteo **"recibí de Facu $300.000"** = ya los recibió → su caja física ahora **coincide** con el Dashboard, sin diferencia. ⚠️ **NO cargar ese "recibí de Facu $300.000" en Movimientos**: lo duplicaría porque el Dashboard ya lo tiene contado.
- **Estructura cuentas viejas:** Boss/Fabric/Bigg → Ingreso=E, Egreso=F, Saldo=G. Volta/Peak → Ingreso=D, Egreso=E, Saldo=F (control en B4, no B3). Solo Fabric/Bigg cobran IVA.
- **Formulario Google** id `1ilw3XodJXkswLaqgAjmbFhN-Kf_KHNdNLmFDjtIigEk`. Escribe directo en Movimientos (Tabla). Multi-página con ramas Ingreso/Egreso. Los **radios están flojos** (a veces hace falta 2 clicks: 1° foco, 2° selección). Opciones de Local del form incluyen "Alquiler Cancha / Cumpleaños", "Heladeria", "Hamburgueseria", "Aporte de Capital Richi", etc.
- **Dashboard Mensual (gid 1279589072):** "CASHFLOW MENSUAL". Fila 6 = saldo running por mes (columnas de a pares Caja/Banco por mes). M6 fórmula `=K6+M43-M79` (chain de banco). Fila 6 es el acumulado a fin de mes.

### Lista canónica de Locales
Boss · Bigg · Fabric · Volta + Open 25 · Peak One · Salon Multiespacios · Cafetería · Shock Ba · Futura Parrilla · Canchera · Market · Comercio 1-6 · La Jaula · Beto Escuelita · Meta Escuelita · **Alquiler Cancha / Cumpleaños** (⚠️ nombre completo, así lo produce el form).
⚠️ Mapeo local↔cuenta: Boss = "Hamburgueseria"; Volta+Open25 = "Heladeria" (en Movimientos los cobros entran con esos nombres).

## Cómo trabaja Facu / preferencias
- Responder **en español**, conciso y directo, sin relleno. Criollo (rioplatense).
- Prefiere confirmar supuestos antes de inventar números. Valora honestidad sobre cálculos. Corrige rápido.
- No duplicar movimientos: si algo ya está cargado, no lo cargues de nuevo. Ante duda, preguntar.
- **Verificar Dashboard + cta cte después de cada carga** (ver REGLA FIJA arriba).

## Estructura del Sheet maestro (pestañas)
- **Movimientos** (Tabla "Form_Responses"): A=Marca temporal, B=Tipo, C=Medio, D=Local, E=Categoria, F=Monto, G=Moneda, H=Obs, I=Mes (ArrayFormula, NO escribir). Mantener colchón de filas vacías al final.
- Otras: Proyeccion, Dashboard, Expensas Predio, Dashboard Mensual, Saldo Actual, Inversiones, TIR, Configuración, Alquileres, Listas.
- **Saldo Actual:** Caja y Banco totales actuales.
- Dólar de referencia: blue = $1.525 (Proyeccion!B4).

## Inquilinos ACTUALES (pagan hoy)
Boss (hamburguesería), Bigg (local 11), Fabric (~350 m², "futura parrilla"), Volta+Open (~115 m², se demuele), Apex/Peak One (salón, paga solo expensas), Salón/Salon Multiespacios (solo expensas ~$1M/mes). Escuelitas (Beto/Meta) y La Jaula/Alquiler Cancha = Futbol (sin expensas).

## Notas técnicas para editar el Sheet vía navegador
- El **name box (~50,118) es poco confiable** (basura "A255A1AP"). Para navegar: clickear una celda de datos + flechas/Cmd+Down. Para cargar filas: Tab real entre columnas, Enter al final (vuelve a col A).
- La **interfaz se pone inestable** (ventana se redimensiona 1556x784 ↔ 1568x738, los clicks de pestaña a veces no registran → verificar la pestaña activa antes de operar, sobre todo antes de acciones destructivas). Navegar por **URL con #gid=** es lo más confiable entre hojas.
- Formato número: 123 dropdown → "Currency rounded" (=$#,##0) / "Date". Pesos `$#,##0`.
- Tabs colapsados en Futbol: los "+" arriba expanden grupos de columnas.
