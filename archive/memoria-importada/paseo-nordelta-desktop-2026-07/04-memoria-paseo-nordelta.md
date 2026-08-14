# MEMORIA — Paseo Nordelta (finanzas)

Persona: Facundo (Facu). Idioma: español rioplatense, conciso.

## 1. Sheets

**Principal — "Paseo Nordelta 2026 - Master Plan"**
`fileId: 1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`
- Pestaña **Movimientos** (gid 478887315): datos crudos del formulario. Columnas: A=Marca temporal(fecha) · B=Tipo(Ingreso/Egreso) · C=Medio(Caja/Banco) · D=Local · E=Categoria · F=Monto (punto decimal) · G=Moneda(ARS/USD) · H=Observaciones · **I=Mes (AUTOMÁTICO por ArrayFormula — NUNCA escribir)** · J=Resultado.
- **Dashboard Mensual** ("CASHFLOW MENSUAL"): SUMIFS por mes. Ingresos matchean por LOCAL, egresos por CATEGORÍA. Las etiquetas de fila las trae por celda desde **Configuración** (NO son texto fijo).
- **Saldo Actual**: Caja/Banco en ARS y USD. Son los saldos reales (Banco coincide con el extracto).
- **Configuración**: listas maestras — col A = locales (ingresos), col C = categorías (egresos). Acá se editan las listas, NO en el Dashboard. Dólar oficial de referencia en F2.
- Otras: Proyeccion, Dashboard, Expensas Predio, Inversiones, TIR, Alquileres.

**Gastos Obra — "Gastos Obra - PASEO NORDELTA 2026"**
`fileId: 1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY` (pestaña única, gid 0)
- Columnas a completar ("Modificar"): A=Fecha · B=Persona(Richi/Facundo/Paseo Nordelta) · C=Descripción · D=Monto · E=Moneda · F=Fx Fecha (dólar blue del día). El resto (Monto en ARS/USD, "Facu debe a Richi", acumulados) es AUTOMÁTICO — no tocar.
- Registra tanto gastos de obra como aportes puros. Ojo: la misma plata que en Movimientos es "aporte de capital" acá suele figurar como el gasto puntual que pagó (a nombre de quien lo pagó).

## 2. Definiciones

- **INVERSIÓN** = (a) ingresos con Local que empieza con "Aporte de Capital" (aportes de socios: Richi / Facu); (b) egresos con Categoría "Inversiones".
- **NEGOCIO** = el resto: ingresos de locales (excluye aportes) − egresos operativos (excluye "Inversiones").
- **Resultado del negocio (mes)** = ingresos negocio − egresos negocio. Es lo que dice si el negocio es rentable sin contar la inversión.
- USD marginal (casi todo enero): netear aparte, no mezclar en totales ARS.

## 3. Reglas / convenciones acordadas

- **BANCO = número exacto del extracto bancario.** Todo movimiento de banco debe coincidir con el extracto.
- Categorías/locales nuevos: agregarlos en la pestaña **Configuración** (no en el Dashboard). NUNCA escribir en la columna I de Movimientos.
- Para escribir/corregir en los sheets hace falta el navegador (Claude in Chrome). Leer en vivo con gviz (el conector de Drive a veces trae copia vieja):
  `https://docs.google.com/spreadsheets/d/<fileId>/gviz/tq?tqx=out:csv&sheet=<NombrePestaña>`
- Saldos de cierre: Banco del extracto ("SALDO FINAL AL DIA"); Caja y USD de "Saldo Actual". NO calcular el saldo de banco sumando Movimientos desde enero (le falta la base previa).

## 4. Banco Macro — extracto

Cuenta de trabajo: **CUENTA CORRIENTE ESPECIAL EN PESOS 4-452-0960512147-9**. Hay además una Cuenta Corriente Bancaria (3-452-0942483045-1) donde caen los cargos VISA de tarjeta.
Carpeta de extractos: `/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/2026/` (ej. "Junio 2026.pdf"). Extraer con `pdftotext -layout`.

**Identidad de pagadores en el extracto:**
- "TEF DATANET PR SUSHINOR SA" (CUIT 30716663279) = **FABRIC**.
- "TEF DATANET PR RODOLFO SRL" o "CREDIN:...-30716281457" (CUIT 30716281457) = **BIGG**.
- "TRANSF ...APC" / glosa de aporte = **Aporte de Capital** (Richi o Facu), no es un local → INVERSIÓN.
- Cargos del banco: DBCR 25413 (Ley 25.413), Comision Trf MacrOL, RET ING BRUTOS SIRCREB, IMP AFIP (VEPs) → suelen ir como "Gastos bancarios" / "Ingresos Brutos".

## 5. Dólar blue (para Gastos Obra)

- Histórico por fecha: `https://api.argentinadatos.com/v1/cotizaciones/dolares/blue/AAAA/MM/DD` → promedio = (compra+venta)/2.
- Hoy: `https://dolarapi.com/v1/dolares/blue`.

## 6. Locales y logo

- Locales/ingresos: Fabric, Bigg, Heladeria, Hamburgueseria, Salon Multiespacios, Peak One (antes "Apex" — renombrado), Beto/Meta Escuelita, Parrilla, Alquiler Cancha/Cumpleaños, etc.
- Logos oficiales: `/Users/Facu/Desktop/Paseo Nordelta/Logotipos Nordelta Plaza/` (Isotipo Blanco.png = monograma "pn"; Logotipo Negativo/Positivo = wordmark PASEO NORDELTA). Branding: negro/blanco, sans-serif bold, acentos verdes.

## 7. Tareas automáticas creadas

1. **conciliacion-mensual-paseo-nordelta** — día 10 de cada mes, 9am. Concilia extracto+caja (control interno) y envía el **reporte branded para inversores en PDF** (párrafo + PDF adjunto) a `re1900@gmail.com` (Ricardo "Richi", inversor) y `facue1900@gmail.com` (Facu). Si algo no cierra o hay observación clave, avisa primero SÓLO a Facu. El PDF: header negro con isotipo+wordmark, resultado del negocio, negocio mes a mes, ¿es rentable?, saldos al cierre (Caja/USD/Banco), capital y obra (aportes Richi/Facu vs invertido).
2. **sync-aportes-capital-gastos-obra** — diario 7am. Detecta aportes de capital nuevos en Movimientos y los agrega a Gastos Obra (Fecha, Persona, Descripción, Monto, Moneda, dólar blue del día). Match por monto+moneda para no duplicar. Reporta a Facu gastos de Gastos Obra que falten en Movimientos.

> Recordar: darles "Run now" una vez desde Scheduled para pre-aprobar permisos.

## 8. Estado / hechos verificados (a julio 2026)

- Cierre **JUNIO 2026**: conciliación banco impecable (neto y saldo al centavo). Resultado del negocio +$5,4M (2º mejor mes). Saldos al cierre: Caja ~$4,37M · Banco $4.119.498 · USD 0.
- Capital aportado hasta la fecha: **Richi ~$150–161M** · **Facu ~$23M**. Invertido en obra ~$166M. La obra se financia casi 100% con capital de socios.
- **34 luces para camino = $2.473.885** = 10 luces ($674.696, ya en Movimientos) + 24 luces (**$1.799.188,80**, comprado 24/4 en Iluminacion Center / Mercado Pago, VISA Macro, **6 cuotas de $299.864,80**). El cargo VISA mensual del extracto (ej. junio $309.088,45) = cuota de luces + otros cargos/intereses; no es 100% luces.

### Correcciones/altas hechas esta sesión
- Dashboard: renombrado "Apex" → "Peak One" en Configuración (A8), así el Dashboard toma el ingreso.
- Gastos Obra: backfill de aportes faltantes (10/3, 7/7, 8/7 ×3) con dólar blue; agregado herrero (30/6, Facu, $400.000, dólar $1.505).
- Movimientos: TOSDE (18/6) corregido a **$1.149.538**; NOREVENTOS Redes&Servicios (22/6) corregido a **$572.964**; durlock+materiales (29/5) agregado como aporte Facu + egreso Inversiones (Caja, $332.944); movimiento VISA junio (2/6, $306.055,55) recategorizado a **Inversiones**.
- Chequeo final: Caja, Banco, extracto y Dashboard Mensual — todo cuadra al peso, sin categorías huérfanas.
