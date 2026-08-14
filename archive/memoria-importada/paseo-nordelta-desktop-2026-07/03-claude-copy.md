# MEMORIA — Paseo Nordelta (Claude, leer al iniciar cada sesión)

> Este archivo guarda todo el contexto del proyecto para que Claude retome el trabajo
> aunque se cambie de cuenta o de sesión. Si sos Claude y estás leyendo esto: este es
> tu punto de partida. Facundo administra **Paseo Nordelta**, un complejo comercial en Nordelta.
>
> Última actualización: julio 2026 (sesión 3).

## 🔴🔴 BUG CRÍTICO ENCONTRADO (sesión 3, cont.) — ARREGLAR ANTES QUE NADA
**La fórmula del ledger NO trae los pagos de Cobros. Solo funcionan los cargos manuales.** Descubierto al testear con el cobro real de Salon Multiespacios ($5M Carolas, que sí está en Cobros).
- **Causa:** Cobros es un **array "spilled"** (sale de una fórmula QUERY+IMPORTRANGE en A2). Mi fórmula "robusta" matcheaba los pagos con **aritmética de arrays** `(LOWER(Cobros!B3:B)=ky)*(Cobros!A3:A<>"")...` → esa aritmética **NO lee los valores spilled** (da 0 matches, "noVacioA=1"). En cambio **`FILTER(...)` y `COUNTIF(...)` SÍ los leen** (probado: FILTER trae los 4 pagos de Salon). Mis "tests" anteriores solo probaron cargos (misma hoja) por eso no lo detecté.
- **Afecta a:** las 12 ctas ctes nuevas + los 3 ledgers del tab Futbol (todos usan la fórmula rota). Los pagos NO entran solos todavía en ninguna.
- **EL FIX (fórmula corregida, basada en FILTER en vez de aritmética de arrays):** poner en A5 de cada cuenta (reemplazar `$B$3`/`I5:I`/`J5:J`/`K5:K` por la celda de control y las columnas de cargos del bloque):
```
=IFERROR(LET(ky,LOWER($B$3),pg,IFERROR(FILTER(HSTACK(Cobros!A3:A,Cobros!D3:D,Cobros!E3:E,IF(Cobros!A3:A="","",""),Cobros!C3:C,IF(Cobros!A3:A="","","")),LOWER(Cobros!B3:B)=ky),HSTACK(0,"","","","","")),cg,IFERROR(FILTER(HSTACK(I5:I,IF(I5:I="","",""),J5:J,IF(I5:I="","",""),IF(I5:I="","",""),K5:K),I5:I<>""),HSTACK(0,"","","","","")),tot,VSTACK(pg,cg),keep,FILTER(tot,CHOOSECOLS(tot,1)<>0),srt,SORT(keep,1,TRUE),dlt,MAP(CHOOSECOLS(srt,5),CHOOSECOLS(srt,6),LAMBDA(i,e,N(e)-N(i))),HSTACK(srt,SCAN(0,dlt,LAMBDA(a,x,a+x)))),)
```
  Lógica: `pg`=pagos vía FILTER de Cobros por Local (6 cols: Fecha,Medio,Concepto,FC,Ingreso,Egreso); `cg`=cargos manuales vía FILTER de I:K; IFERROR con fila-sentinela (Fecha=0) para el caso vacío; VSTACK, sacar sentinelas (Fecha<>0), ordenar por fecha, saldo corriendo (Egreso−Ingreso).
- ✅ **FIX VALIDADO EN VIVO (plantilla con B3="Salon Multiespacios"):** trajo solos los 4 pagos reales de Salon desde Cobros (27/2 $5M Carolas, 1/4 $1M Marina, 6/5 $1M, 4/6 $1M) con Fecha (sin hora), Caja, Concepto, Ingreso y Saldo corriendo. **FUNCIONA.** La PLANTILLA ya tiene el fix puesto en A5 y B3 vuelto a vacío = molde corregido listo.
- 🔴 **LAS 12 CTAS CTES NUEVAS ESTÁN CORRUPTAS** (verificado Salon y Cafetería; asumir las 12). Durante la sesión de formateo, la interfaz inestable pegó ENCIMA la estructura de una cuenta VIEJA (Peak One): ahora tienen Rubro/Nombre/CUIT/Domicilio, "Locatario:" en fila 4, control en **B4** (no B3), headers en fila 5, todo **corrido una fila hacia abajo**. Su título propio (ej "CTA CTE — Cafeteria") y B4=nombre sí quedaron.
  - **PLAN DE RECUPERACIÓN (recomendado):** BORRAR las 12 cuentas corruptas y RE-CREARLAS duplicando la PLANTILLA (que ya está limpia, con el fix y formateada). Al duplicar heredan fix + formato → NO volver a hacer paste-format (eso fue lo que las rompió). Por cuenta: duplicar plantilla → renombrar → poner B3 = nombre canónico. Están vacías, no se pierde nada.
  - Después: arreglar los 3 bloques de **Futbol** (M5, Y5 con la misma lógica FILTER, adaptando control N3/Z3 y cargos U:W/AG:AI), y **migrar las cuentas viejas** (Boss/Bigg/Fabric/Volta/Peak One) al ledger automático — OJO doble conteo: sus pagos ya están en Cobros; si se les pone el ledger auto hay que sacar la historia manual vieja para no duplicar.
- ⚠️ Dejé celdas de diagnóstico en Salon (M6:O9 un FILTER, M13 un texto). Se borran al recrearla.
- ⚠️ **HACER TODO ESTO EN UNA SESIÓN NUEVA/ESTABLE**, navegando por URL a cada hoja (recarga = estado limpio) y verificando cada paso. NO usar la selección múltiple de pestañas ni paste-format masivo (rompió las cuentas).
- **La interfaz de Sheets vía navegador estuvo MUY inestable esta sesión.** Conviene aplicar el fix en una sesión nueva/tranquila, verificando cada paso y recargando la página si se cuelga.

## ⚡ ESTADO ACTUAL (jul 2026, sesión 3) — leer primero
- **Pestaña "Futbol" CREADA y FUNCIONA** en Ctas Ctes (gid **440311341**). Es una sola pestaña con **3 ledgers lado a lado + 1 lista simple**:
  - **La Jaula** (bloque 1): output A5:G, control **B3**, cargos manuales en **I:K** (I=Fecha, J=Concepto, K=Monto). VALIDADO con cargo de prueba (cargo 1M → Egreso 1M, Saldo 1M ✓).
  - **Beto Escuelita** (bloque 2): output M5:S, control **N3**, cargos en **U:W**.
  - **Meta Escuelita** (bloque 3): output Y5:AE, control **Z3**, cargos en **AG:AI**.
  - **Alquiler Cancha / Cumpleaños** (lista simple): título AK1, "Total cobrado" en AK2/AL2, headers AK4 (Fecha/Monto/Medio/Detalle), lista auto en **AK5**. Sin cargos ni saldo (solo registro de ingresos).
  - Los 3 ledgers usan una **FÓRMULA ROBUSTA NUEVA** (ver abajo) que muestra vacío limpio cuando la cuenta no tiene datos (la fórmula vieja de la plantilla daba #N/A con cuentas vacías). Etiquetas canónicas: **La Jaula, Beto Escuelita, Meta Escuelita, Alquiler Cancha**.
  - Formato de fecha aplicado a columnas A, M, Y (Fecha de cada ledger). PENDIENTE (cosmético): moneda en columnas de Ingreso/Egreso/Saldo/Monto (E:G, Q:S, AC:AE, K, W, AI, AL) y colores. Facu pone colores si hace falta.
- **Etiqueta "Salon multiespacios" → "Salon Multiespacios"** UNIFICADA en Movimientos (era 1 celda, D35, el ingreso de $5.000.000 de Carolas). HECHO.
- **12 CTAS CTES NUEVAS CREADAS** en Ctas Ctes (duplicando la PLANTILLA): **Cafetería, Salon Multiespacios, Shock Ba, Futura Parrilla, Canchera, Market, Comercio 1, Comercio 2, Comercio 3, Comercio 4, Comercio 5, Comercio 6**. Cada una: A1 = auto-título `="CTA CTE — "&B3`; **B3 = nombre canónico del Local** (celda de control que filtra Cobros); fórmula robusta del ledger en A5; cargos manuales en I:K. Están **vacías** (esos inquilinos aún no cobran); cuando empiecen a pagar (Movimientos→Cobros con ese Local exacto) los pagos entran solos, y Facu carga alquiler/expensas como cargos en I:K.
- **PLANTILLA mejorada** (gid 1893149501): ahora tiene la **fórmula robusta** en A5, **A1 con auto-título** (`=IF(B3="","PLANTILLA CTA CTE...","CTA CTE — "&B3)`), **B3 vacío** y **sin cargos de ejemplo**. Es el template limpio: duplicar → poner B3 → listo.
  - ⚠️ **La plantilla NO es solo el ledger A:K**: hacia la derecha (columnas ~AQ-AS) tiene una **tabla verde "Alquiler / IPC Trimestral"** (proyección del alquiler creciendo por IPC, meses 2026-2027) y **columnas agrupadas/colapsadas** (los "+" arriba de L, X, AJ, AO). Todo esto lo heredaron las 12 cuentas nuevas → cada una viene con su tabla de proyección de alquiler (como Boss/Fabric/Bigg). **Facu la customiza por cuenta** (trae el alquiler base de ejemplo 1.000.000; hay que poner el real). Decisión de Facu (sesión 3): dejarla, la customiza él.
- **Dropdown de Local: PROBADO Y LUEGO QUITADO** (sesión 3). Se armó un dropdown en Movimientos!D con lista canónica, pero Facu decidió sacarlo porque **los movimientos entran por el Formulario de Google** (opciones fijas) → no hay forma de escribir mal el Local, el dropdown era redundante. La columna D volvió a texto plano (Edit column type → None) y la pestaña "Listas" se borró. Si algún día se cargan movimientos a mano (no por Formulario), reconsiderar.

### Lista canónica de Locales (Listas!A2:A22, y contenido del dropdown)
Boss · Bigg · Fabric · Volta + Open 25 · Peak One · Salon Multiespacios · Cafetería · Shock Ba · Futura Parrilla · Canchera · Market · Comercio 1 · Comercio 2 · Comercio 3 · Comercio 4 · Comercio 5 · Comercio 6 · La Jaula · Beto Escuelita · Meta Escuelita · Alquiler Cancha

### FÓRMULA ROBUSTA del ledger auto (usar para las ctas ctes nuevas también)
Combina cargos manuales + pagos de Cobros (filtrados por la celda de control), ordena por fecha, saldo corriendo (Egreso−Ingreso). Devuelve 7 columnas: Fecha, Medio, Concepto, FC, Ingreso, Egreso, Saldo. Muestra vacío si no hay datos (IFERROR). Reemplazar `$B$3` por la celda de control y `I5:I/J5:J/K5:K` por las columnas de cargos del bloque:
```
=IFERROR(LET(ky,LOWER($B$3),P,HSTACK(Cobros!A3:A,Cobros!D3:D,Cobros!E3:E,IF(Cobros!A3:A="","",""),Cobros!C3:C,IF(Cobros!A3:A="","",""),(LOWER(Cobros!B3:B)=ky)*(Cobros!A3:A<>"")),G,HSTACK(I5:I,IF(I5:I="","",""),J5:J,IF(I5:I="","",""),IF(I5:I="","",""),K5:K,(I5:I<>"")*1),V,VSTACK(P,G),F,FILTER(V,CHOOSECOLS(V,7)=1),S,SORT(CHOOSECOLS(F,1,2,3,4,5,6),1,TRUE),D,MAP(CHOOSECOLS(S,5),CHOOSECOLS(S,6),LAMBDA(i,e,N(e)-N(i))),HSTACK(S,SCAN(0,D,LAMBDA(a,x,a+x)))),)
```
- Mapeo Cobros: A=Fecha, B=Local, C=Monto, D=Medio, E=Detalle. Pago → Ingreso; Cargo (columna K/Monto) → Egreso; Saldo sube con cargo, baja con pago.
- Lista simple Alquiler Cancha (AK5): `=IFERROR(SORT(FILTER({Cobros!A3:A,Cobros!C3:C,Cobros!D3:D,Cobros!E3:E},LOWER(Cobros!B3:B)="alquiler cancha"),1,TRUE),)`

## Estado heredado de sesión 2 (sigue vigente)
- **Maestro** = "Paseo Nordelta 2026 - Master Plan" (id `1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`).
- **Ctas Ctes NATIVO** id **`10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`** (título "Ctas Ctes Paseo Nordelta - 2026"). El .xlsx viejo (16XnRT…) DEPRECADO.
- Pestaña **"Cobros"** (gid 904807272) = ÚNICO IMPORTRANGE al maestro. FUNCIONA. Columnas: A=Fecha, B=Local, C=Monto, D=Medio, E=Detalle. Datos desde fila 3. Fórmula A2: `=QUERY(IMPORTRANGE("1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs","Movimientos!A2:H"),"select Col1,Col4,Col6,Col3,Col8 where lower(Col2)='ingreso' and Col4 is not null order by Col1 label Col1 'Fecha',Col4 'Local',Col6 'Monto',Col3 'Medio',Col8 'Detalle'",0)`. Falta formato lindo (cosmético).
- **PLANTILLA (gid 1893149501):** ledger auto. Estructura: A1 título; A3 "Inquilino (Local):" + **B3 = celda de control**; A4 headers `={"Fecha","Medio","Concepto","FC","Ingreso","Egreso","Saldo"}`; CARGOS input manual en I3/I4:K (I=Fecha, J=Concepto, K=Monto); fórmula en A5. ⚠️ La plantilla original todavía tiene su fórmula VIEJA (da #N/A si no hay cargos ni pagos) y 2 cargos de EJEMPLO en I5:K6. Al crear cuentas nuevas, **usar la FÓRMULA ROBUSTA de arriba** y borrar los ejemplos.
- **Decisiones de locales:** Apex = Peak One (no lleva cta cte propia). Salón (Alto) = "Salon Multiespacios" (sí lleva cta cte). Fabric solo se muda (~nov), NO cta cte nueva. Contenedores: afuera por ahora. Parrilla momentánea: sin cta cte. Shock Ba: pestaña nueva (Volta+Open queda histórica).
- **"Parrilla" (momentánea) ≠ "Futura Parrilla" (ex-Fabric)** — confirmado por Facu (sesión 3): son **negocios DISTINTOS**, quedan como cuentas/etiquetas separadas. Ojo: ya existe la etiqueta "Parrilla" con movimientos en Movimientos (la momentánea), por eso NO renombrar "Futura Parrilla" a "Parrilla".
- **Regla de nombres de Local (recomendación):** el nombre del Local es la LLAVE que une Movimientos→Cobros→cta cte, así que debe ser ESTABLE (idealmente por local físico, no por inquilino). Si cambia el inquilino: mantener la misma cuenta/llave y actualizar el "Locatario" + nota, así la historia del local queda junta. Si hay que renombrar un Local que YA tiene movimientos: cambiar B3 + pestaña + Buscar y Reemplazar del nombre viejo→nuevo en la columna Local de Movimientos.
- **Cta ctes a CREAR (en blanco, con la fórmula robusta):** Cafetería, Salon Multiespacios, Shock Ba, Futura Parrilla (ex-Fabric), Canchera, Market, Comercio 1 a 6.
- ⚠️ Interfaz de Sheets vía navegador inestable: ir despacio, verificar cada escritura. El **name box a veces trae basura ("A255A1AP")** → hacer Cmd+A antes de escribir la celda. La **tecla Tab REAL** cambia de columna en una fila (el "\t" literal NO). El "\n" en un type actúa como Enter (baja) — útil para cargar listas de una.

## Cómo trabaja Facu / preferencias
- Responder **en español**, conciso y directo, sin relleno. Criollo (rioplatense).
- Prefiere confirmar supuestos antes de inventar números. Valora honestidad sobre cálculos (decir de dónde sale cada número). Corrige rápido.

## Archivos y accesos
- ⚠️ **CAMBIO DE CUENTA (jul-2026):** originales eran de festevez@multum.digital (Workspace, se cerraba). No se pudo transferir propiedad → Facu **copió** todo a **facue1900@gmail.com**. IDs nuevos (arriba).
- **Maestro** id `1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`. Pestañas: Movimientos, Proyeccion, Dashboard, Expensas Predio, Dashboard Mensual, Saldo Actual, Inversiones, TIR, Configuración, Alquileres, **Listas (nueva sesión 3)**. La inflación NO está acá (está en Ctas Ctes).
- **Ctas Ctes** id `10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`. Pestañas: INFLACIÓN, Cobros, PLANTILLA, **Futbol (nueva sesión 3)**, Volta + Open 25, Peak One, Boss, Fabric, Bigg.
  - **INFLACIÓN**: A=año, B=mes, C=Inflación % mensual. Cargado hasta mayo-2026 (2,10%); junio+ vacío. Tarea automática corre el 15 de cada mes.
  - Estructura cuentas viejas: Boss/Fabric/Bigg → Ingreso=E, Egreso=F, Saldo=G (D=FC). Volta/Peak → Ingreso=D, Egreso=E, Saldo=F. Solo Fabric/Bigg cobran IVA.
- **Formulario Google** id `1ilw3XodJXkswLaqgAjmbFhN-Kf_KHNdNLmFDjtIigEk`. Escribe directo en Movimientos (por eso col A = "Marca temporal"). ⚠️ Movimientos es una **Tabla** de Sheets.
- Acceso a los sheets = vía navegador (Claude in Chrome), sesión de Google logueada (facue1900). No hay credencial propia de Claude.
- Dólar de referencia del modelo: **blue = $1.525** (celda **B4** de "Proyeccion").

## Estructura del Sheet maestro (pestañas)
- **Movimientos** (Tabla): A=fecha/Marca temporal, B=Tipo(Ingreso/Egreso), C=Medio(Caja/Banco), D=**Local (con dropdown, sesión 3)**, E=Categoria, F=Monto, G=Moneda, H=Obs, I=Mes. ⚠️ **NUNCA escribir en la columna I** (ArrayFormula que calcula el Mes). ⚠️ Es Tabla → el dropdown de D se edita en "Edit column type", no en Data validation.
- **Expensas Predio**: distribución mensual. A=local, B=Expensas AVN, C=Agua R&S, D=ABL, E=Recupero Total, H-P=Servicios comunes, Q=Serv comunes Total, R=**Total Expensas**=Q+E. Expensas = Recupero + Servicios comunes, cobradas a costo (margen 0). Snapshot 1/6/2026 filas: 7 Peak One, 8 Cafetería, 9 Salon Alto, 10 Bigg, 11 Fabric, 12 Volta+Open25, 13 Hamburgueseria(Boss), 14 Futuro fabric, 15 Canchera, 16 Contenedor Jaula, 17-28 Comercio 1-12 (7-12 en $0), **29 Market (R29=$1.072.946/mes)**.
- **Configuración**: E=Parámetro, F=Valor. **F2 = "Dólar ARS/USD" = `=Proyeccion!B4`** (arreglado jul-2026, antes IMPORTRANGE roto). Inversiones depende de F2.
- **Listas (nueva)**: A2:A22 lista canónica de Locales. Fuente del dropdown de Movimientos!D.
- Dato histórico: Caja verificada en −$173.814. Rentabilidad operativa 6 meses ≈ +$14,5M pesos.

## Inquilinos ACTUALES (pagan hoy)
- **Boss** (hamburguesería, ~local 29/15), **Bigg** (local 11), **Fabric** (~350 m², "futura parrilla", locales 10/12/13/14/15), **Volta + Open** (~115 m², se demuele), **Apex** (salón 750 m², paga SOLO expensas), **Salón** (solo expensas ~$1M/mes).

## Obra / locales nuevos
- Rojo en planos = se construye. Terreno: **10 años (ene 2026 – ene 2036)**.
- 3 locales del fondo (arroyo): fabric nuevo, pizzería (Canchera), heladería (Shock Ba) — obra ~US$150k.
- 6 locales + **market** — obra similar por m² × 1,25. Permisos ~$175M pesos. ABL ~$2M/mes. Infra ~US$40k.
- Obra termina mediados/fines 2027. Wellness/Apex paga expensas hasta ene 2027, después alquiler.

## Rent Roll REAL (alquileres puros, sin expensas) — a maduración
Cargado en "Proyeccion" (tabla "RENT ROLL COMPLETO", fila 24+).

| Inquilino | Alquiler $/mes | Arranca | Nota |
|---|---|---|---|
| Boss | 1.060.884 | hoy | actual |
| Bigg | 3.820.774 | hoy | actual |
| Fabric nuevo | 5.000.000 | nov-27 | Fabric se muda |
| Futura parrilla (ex-Fabric) | 7.956.630 | dic-27 | 1 mes gracia |
| Cafetería | 3.500.000 | sep-26 | expensas jul-sep |
| Salón (Alto) | 2.500.000 | ene-27 | expensas hasta ene-27 |
| Apex | 4.000.000 | ene-27 | $4M o 10% facturación |
| Shock Ba (heladería) | 4.500.000 | dic-27 | lugar de Volta |
| Canchera (pizzería) | 1.900.000 | dic-27 | local nuevo |
| 6 comercios | 2.000.000 c/u (=12M) | fin-27 | algunos vacíos |
| Market | 3.000.000 | fin-27 | |
| La Jaula / torneo | 1.000.000 → 2.000.000 desde mar-29 | ago-26 | contrato hasta mar-29 al 50%, IPC semestral |
| Escuelita | ~500.000 | hoy | todos los meses |
| Contenedores (x3) | 750.000 c/u + 350k expensas c/u | hoy | |

- Total rent roll a maduración ≈ **$53.988.288/mes ≈ US$ 35.402/mes ≈ US$ 424.826/año**.

## Modelo "Proyeccion" (gid=1852246175)
- Izquierda: modelo de inversión de locales nuevos (escenarios Optimista/Base/Conservador). Derecha (cols I–Q): **PANORAMA 10 AÑOS** (filas 6–15 = 2026-2035, 16=TOTAL). L=Result op (=J−K−Q), Q=**Exp. absorbidas**.
- **Resultados (post-Market):** Inversión total US$ 641.000 · Result op total US$ **3.036.888** · **Neto acumulado a 2036 US$ 2.395.888** · break-even 2029.
- **Exp. absorbidas** (ACTUALIZADO con Market): 2026 **70.650** (Q6=`=62207+8443`) / 2027 **59.467** (Q7=`=51728+7739`) / 2028+ 0. Metodología: sumar Total Expensas mensual de cada local sin construir × meses absorbidos ÷ 1.525.

## Pendientes / próximos pasos
- [x] Sumar Market a Exp. absorbidas (sesión 2).
- [x] Auditoría #REF! del maestro (sesión 2).
- [x] Unificar "Salon multiespacios" (sesión 3).
- [x] Pestaña Futbol con ledgers auto (sesión 3).
- [x] ~~Dropdown de Local en Movimientos~~ PROBADO Y QUITADO (redundante: los movimientos entran por el Formulario).
- [x] Crear las 12 ctas ctes nuevas en blanco (sesión 3): Cafetería, Salon Multiespacios, Shock Ba, Futura Parrilla, Canchera, Market, Comercio 1-6. HECHO.
- [x] Dejar la PLANTILLA con fórmula robusta + auto-título A1 (sesión 3).
- [x] Formato (fecha + moneda $#,##0) de las 12 ctas ctes + PLANTILLA + los 3 ledgers del tab Futbol (sesión 3). Método que FUNCIONA: formatear una cuenta (A=date, E:G=Currency rounded, I=date, K=Currency rounded), copiar A1:K1000 y **pegar solo formato con Cmd+Alt+V** en las demás (agrupar pestañas NO propaga número-formato). Para Futbol los 3 bloques: pegar el mismo A1:K1000 en A1, M1 e Y1. FALTA (mínimo): columna Monto (AL) de la lista Alquiler Cancha del tab Futbol — el name box se puso inestable.
- [ ] Cuando arranquen a cobrar los inquilinos nuevos, cargar en Movimientos con el Local EXACTO (canónico) para que entren solos en su cta cte, y cargar alquiler/expensas como cargos en I:K de cada cuenta.
- [ ] Customizar la **tabla verde de Alquiler/IPC** en cada cta cte nueva (ver nota abajo): poner el alquiler base real del inquilino (viene con el valor de ejemplo 1.000.000).
- [ ] IPC: cargar junio-2026+ en INFLACIÓN col C (tarea automática corre el 15).
- [ ] (Opcional) Reconectar planilla externa "Variables" para dólar en vivo en Configuración!F2.
- [ ] Formato lindo de Cobros (cosmético).
- Recordatorios automáticos ya configurados: reconciliación día 5, carga ctas ctes día 1, IPC día 15.

## Notas técnicas para editar el Sheet vía navegador
- Name box ~(45,117): Cmd+A para limpiar basura, escribir celda, Enter.
- Tecla **Tab** real cambia de columna; "\n" en type = Enter (baja). Útil: cargar listas en una sola celda con varios "\n".
- Formato número: USD `"US$ "#,##0` (US$ entre comillas). Pesos `$#,##0`.
- Verificar SIEMPRE la pestaña activa antes de escribir.
- **Dropdown de una Tabla**: se edita en el menú del encabezado → "Edit column type" → "Dropdown". La referencia de rango debe ser **ABSOLUTA** ($) o se corre por fila.
- Formato de fecha (columna Fecha de ledgers): Format → Number → Date.
