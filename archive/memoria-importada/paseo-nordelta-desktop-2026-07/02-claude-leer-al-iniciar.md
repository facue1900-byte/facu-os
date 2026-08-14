# MEMORIA — Paseo Nordelta (Claude, leer al iniciar cada sesión)

> Este archivo guarda todo el contexto del proyecto para que Claude retome el trabajo
> aunque se cambie de cuenta o de sesión. Si sos Claude y estás leyendo esto: este es
> tu punto de partida. Facundo (festevez@multum.digital, puede cambiar de mail) administra
> **Paseo Nordelta**, un complejo comercial en Nordelta.
>
> Última actualización: julio 2026.

## Cómo trabaja Facu / preferencias
- Responder **en español**, conciso y directo, sin relleno.
- Habla en criollo (rioplatense). Prefiere que le confirme supuestos antes de inventar números.
- Corrige rápido si algo no cuadra; valora honestidad sobre los cálculos (decir de dónde sale cada número).

## Archivos y accesos
- **Google Sheet "Paseo Nordelta 2026"** (id: 15SKKvr8hp1Fy7gR-O6p5QFAI8VFbDWEGE-NYs9Gj58w). Es el maestro.
- **Sheet "Ctas Ctes Paseo Nordelta - 2026"** (id: 1m0qfn5SgahpceiddWcy1WGxluYZqoLSL). Cuentas corrientes por local.
- Acceso a los sheets = vía navegador (Claude in Chrome) con la sesión de Google logueada. No hay credencial propia de Claude.
- El dólar de referencia usado en el modelo es **blue = $1.525** (parámetro editable, celda B4 de la hoja "proyeccion").

## Estructura del Sheet maestro (pestañas)
- **Movimientos**: A=fecha, B=Tipo(Ingreso/Egreso), C=Medio(Caja/Banco), D=Local, E=Categoria, F=Monto, G=Moneda, H=Obs, I=Mes.
  - ⚠️ **NUNCA escribir en la columna I** (es un ArrayFormula que calcula el Mes solo).
- **Ctas Ctes** (en el otro sheet): una tabla por local con SALDO corriendo. Volta/Peak: Ingreso=D, Egreso=E, Saldo=F. Boss/Fabric/Bigg: Ingreso=E, Egreso=F, Saldo=G (col D extra = FC). Solo Fabric/Bigg cobran IVA. Tabla verde de alquiler trimestral (col N).
- **Expensas Predio**: distribución mensual de expensas. Fecha en A3 (ej 1/6/2026). Columnas: A=local, B=Expensas AVN, C=Agua R&S, D=ABL, E=Recupero de Gastos Total, luego SERVICIOS COMUNES (H=Administrativos, I=Limpieza Baños, J=Limpieza e Insumos, K=Limpieza Predio, L=Mantenimiento, M=Jardineria, N=Fumigacion, O=Comunicación, P=Retiro de basura, Q=Servicios comunes Total, R=**Total Expensas**).
  - **Expensas = Recupero de Gastos + Servicios Comunes**, cobradas **a costo** (total cobrado = total gastado, margen estructural 0; a veces Facu saca margen manual).
  - Método acordado: sacar valores mes a mes; si un mes da 0, usar el del mes anterior.
- Otras pestañas: Dashboard, Dashboard Mensual, Saldo Actual, Inversiones, TIR, Configuración, Alquileres, inflacion.
- Dato histórico: hubo un fix de categoría en Dashboard Mensual ("Retiro de Socios" vs "Retiro de Ganancia Richi"). Caja verificada en −$173.814. Rentabilidad operativa 6 meses ≈ +$14,5M pesos.

## Inquilinos ACTUALES (pagan hoy)
- **Boss** (hamburguesería, locales 29 cerca del 15), **Bigg** (local 11), **Fabric** (local grande ~350 m², "futura parrilla", locales 10/12/13/14/15), **Volta + Open** (~115 m², se va a demoler), **Apex** (salón 750 m², paga SOLO expensas — el salón lo construye él, Facu no lo paga), **Salón** (solo expensas ~$1M/mes).

## Obra / locales nuevos (lo que se construye)
- Todo lo marcado en rojo en los planos se construye. Contrato de terreno: **10 años (ene 2026 – ene 2036)**.
- 3 locales del fondo (pegados al arroyo): **fabric nuevo, pizzería (Canchera), heladería (Shock Ba)** — obra ~US$150k, 3 meses obra + 1 interna.
- 6 locales nuevos + **market** — obra estimada similar por m² × 1,25.
- Permisos municipales ~$175.000.000 pesos. ABL municipal ~$2.000.000/mes. Infraestructura nueva ~US$40.000.
- Obra termina mediados 2027, fines 2027 a más tardar. Wellness/Apex paga expensas hasta ene 2027, después alquiler.

## Rent Roll REAL (alquileres PUROS, sin expensas) — a maduración
Fuente: Ctas Ctes (valores reales) + acuerdos de Facu. Está cargado en la hoja "proyeccion" (tabla "RENT ROLL COMPLETO", fila 24 hacia abajo).

| Inquilino | Alquiler $/mes | Arranca alquiler | Nota |
|---|---|---|---|
| Boss | 1.060.884 | hoy | actual (cta cte) |
| Bigg | 3.820.774 | hoy | actual (cta cte) |
| Fabric nuevo | 5.000.000 | nov-27 | Fabric se muda acá |
| Futura parrilla (ex-Fabric grande) | 7.956.630 | dic-27 | ocupa ex-Fabric, 1 mes gracia |
| Cafetería | 3.500.000 | sep-26 | expensas jul-sep |
| Salón (Alto) | 2.500.000 | ene-27 | expensas hasta ene-27 |
| Apex | 4.000.000 | ene-27 | $4M o 10% facturación (el mayor) |
| Shock Ba (heladería) | 4.500.000 | dic-27 | = lugar de Volta cuando se va |
| Canchera (pizzería) | 1.900.000 | dic-27 | local nuevo |
| 6 comercios | 2.000.000 c/u (=12M) | fin-27 | algunos meses vacíos |
| Market | 3.000.000 | fin-27 | abajo de los 6 comercios en Expensas Predio |
| La Jaula / torneo | 1.000.000 → 2.000.000 desde mar-29 | ago-26 | contrato hasta mar-29 al 50%, aumento IPC semestral |
| Escuelita | ~500.000 | hoy | todos los meses |
| Contenedores (x3) | 750.000 c/u (mitad hoy, 3 en 2028) + 350k expensas c/u | hoy | |

- **Salientes** (se van / demuelen): Fabric grande (se muda a nuevo+parrilla, nov-27) y Volta+Open ($732.672, ~2027; se convierte en Shock Ba).
- Total rent roll a maduración ≈ **$53.988.288/mes ≈ US$ 35.402/mes ≈ US$ 424.826/año**.
- Otros ingresos variables: torneo de fútbol de La Jaula, eventos (varían), sponsors (hoy ninguno).

## Modelo en la hoja "proyeccion" (gid=1852246175)
Tab creada por Claude. Contiene, a la izquierda, el modelo de inversión de los locales nuevos (parámetros editables amarillos, tabla de locales, resultados, comparador de escenarios Optimista/Base/Conservador). A la derecha (columnas I–Q) el **PANORAMA 10 AÑOS**.

### Panorama 10 años (columnas I–Q, filas 5–16)
- I=Año, J=Ingreso op (alquileres), K=Gasto fijo (overhead), L=Result op (=J−K−Q), M=Inversión, N=Flujo neto (=L−M), O=Acumulado, P=Egreso+Inv (=K+Q+M, alimenta el gráfico combinado), Q=**Exp. absorbidas**.
- Valores clave (USD):
  - Ingreso: 2026 132.034 / 2027 220.544 / 2028 416.957 / 2029 423.514 / 2030-35 424.826.
  - Gasto fijo (overhead, crece 12,5% a 2028): 52.000 / 55.000 / 58.500 (×8).
  - Exp. absorbidas: 2026 **62.207** / 2027 **51.728** / 2028+ **0**.
  - Inversión: 348.000 (2026) / 293.000 (2027) / 0. Total US$ 641.000.
- **Resultados**: Inversión total 10 años US$ 641.000 · Resultado op total US$ 3.053.070 · **Neto acumulado a 2036 US$ 2.412.070** · **Da vuelta (break-even) en 2029**.
- Dos gráficos (flotando a la derecha, sobre columna Q): (1) columnas del Acumulado; (2) combinado (barras ingreso azul + egreso amarillo + acumulado rojo).

### Lógica de "Exp. absorbidas" (expensas que Facu absorbe)
- Los locales **sin construir** tienen su expensa asignada en "Expensas Predio" pero **nadie la paga** → Facu la absorbe. Es un costo que baja a 0 a medida que se construyen (con las fechas del rent roll).
- Está DENTRO del opex real de 2026 (por eso se separó en línea propia sin romper la calibración de 2026).
- Locales sin construir y su Total Expensas (de la hoja, junio 2026): Cafetería $1.093.337, Futuro fabric $857.176, Canchera $857.176, Contenedor Jaula $798.825, Comercios 1-6 $777.248 c/u. Suma ≈ **$8.269.982/mes ≈ US$ 65k/año**.
- ⚠️ PENDIENTE: falta sumar **Market** (está en Expensas Predio abajo de los 6 comercios) a la línea de absorbidas. Shock Ba NO se suma (es el lugar de Volta, que hoy paga).

## Reporte a inversores — MOSTRAR USD (pedido de Facu, jul 2026) — desde julio 2026
> A los inversores les interesa MÁS el USD que los pesos. En el PDF mensual, sección "CAPITAL Y OBRA",
> al lado de cada monto en pesos agregar el equivalente en USD. El USD es fiel porque cada aporte/gasto
> se valúa al dólar de SU fecha (no a un dólar único) → es el número que quieren ver.
- **Sheet VIGENTE (el de Facu):** "Gastos Obra - PASEO NORDELTA 2026", fileId
  `1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY` (gid=0, pestaña "Hoja 1"). Leer EN VIVO con gviz.
  El del mail de multum (`1ayenDzKoSFx7l69tNvYzMG9kw9gvXaAwpIEpWSzpNkM`) SE VA A BORRAR — no usar.
- Estructura Hoja 1: A Fecha · B Persona (Facundo/Richi/Paseo Nordelta/Mariana/Soledad/Tomas) · C Descripción ·
  D Monto · E Moneda · F **Fx Fecha** (dólar del día) · H **Monto en ARS** · I **Monto en USD** (valuado al FX de la fecha).
- **Cuadro "Acumulado" (de acá salen los valores):** columnas L/M/N → **L=Persona, M=Monto en ARS, N=Monto en USD**.
  Filas: Facundo, Richi, Mariana, Paseo Nordelta, Soledad, Tomas, **Total**. (Hay un 2º cuadro en S/T/U que es
  la reconciliación "Facu debe a Richi" agrupando "Mariana y Richi" — ESE NO se usa para el reporte.)
  - Snapshot al 10/jul/2026 (incluye ya movs de julio): Facundo $25.797.282 / US$17.921 · Richi $161.235.000 /
    US$110.753 · Paseo Nordelta $22.141.629 / US$15.483 · Mariana US$180.380 · Soledad US$91.530 · Tomas US$0 ·
    **Total $209.173.911 / US$324.537**.
- **Regla de consistencia (importante):** el ARS del cuadro Acumulado debe COINCIDIR con los aportes de
  Movimientos del mes que se cierra. Si da de más, es porque hay movimientos del mes siguiente ya cargados
  (ej. en jun el master daba Richi $150.085.000 y acá $161.235.000 = ~$11M de julio). Al cerrar, filtrar por
  fecha ≤ fin del mes de cierre (recalcular por persona desde las filas crudas A/B/H/I) o confirmar que sólo
  estén cargadas filas hasta ese mes. NO inventar la conversión con un dólar único.
- **DECIDIDO (Facu, jul 2026):** en "Capital y obra" mostrar TODOS los aportantes del cuadro Acumulado de la
  izquierda (Facundo, Richi, Mariana, Paseo Nordelta, Soledad, Tomas) con **ARS y USD**, y la fila **Total**
  (ej. Total US$324.537). Usar SIEMPRE ese cuadro (cols L/M/N), no el de "Facu debe a Richi".
- Junio 2026 YA se envió sin USD (Facu dijo que no hace falta rehacerlo).

## Pendientes / próximos pasos
- [ ] **Reporte inversores (desde julio): agregar USD** en "Capital y obra", tomado del cuadro "Acumulado"
      (cols L/M/N) del sheet "Gastos Obra - PASEO NORDELTA 2026" (`1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY`).
      Filtrar por fecha ≤ mes de cierre para que el ARS ate con Movimientos. Definir con Facu si van sólo
      Richi/Facu o todos los aportantes + Total.
- [ ] Sumar Market a "Exp. absorbidas" (buscar su Total Expensas en Expensas Predio, abajo de Comercio 6, y agregarlo con fecha fin-27). Requiere sesión de Google logueada.
- [ ] IPC del mes (tarea vieja, no publicado aún) → cargar en hoja "inflacion".
- Recordatorios automáticos ya configurados: reconciliación día 5, carga ctas ctes día 1.

## Notas técnicas para editar el Sheet vía navegador
- Navegar por el cuadro de nombres (name box ~45,117), escribir la celda, Enter.
- Entre celdas de una fila usar la tecla **Tab** (no "\t" literal, que no cambia de columna). "\n" actúa como Enter (baja).
- Formato número personalizado USD: `"US$ "#,##0` (el `US$ ` debe ir entre comillas). Pesos: `$#,##0`.
- Verificar SIEMPRE la pestaña activa antes de escribir (hubo errores de escribir en el local equivocado).
