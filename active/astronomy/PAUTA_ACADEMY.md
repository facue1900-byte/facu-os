# Pauta — Astronomy Academy

Fecha: 2026-07-28 · **Auditado** por el agente `numeros` contra la fuente, y corregido.

**Fuente de todos los números:** `~/Desktop/Productoras/Astronomy/Academia/Reporte
financiero/Finanzas - Astronomy Academy.xlsx` (estaba en `~/Downloads/`, se archivó ahí el
30/07/2026), hoja
`Base` (1.123 movimientos con fecha, **ene-2024** a jul-2026). Los montos en USD salen
de la columna `USD_Ammount` del propio archivo. Tipo de cambio de la hoja `Variables`:
**oficial 1.445 compra / 1.495 venta / 1.470 promedio**, valor spot cacheado al
17/07/2026 — sirve para la conversión de referencia de este documento, no para
convertir montos de otras fechas.

**Ventana de análisis: jun-2025 a may-2026 (12 meses).** Se corta en may-2026 porque
desde el 01/07/2026 la fuente de la plata pasó a ser la app. Jul-2026 está incompleto
en el archivo (guardado el 17/07). **Jun-2026 no está roto** —facturó US$2.324, por
encima del promedio de la ventana— simplemente queda fuera del corte.

---

## 1. De dónde partimos

### El resultado de los últimos 12 meses

| | USD |
|---|---|
| Ingresos | **27.832** |
| Egresos | **29.874** |
| **Resultado** | **−2.042** |

Margen **−7%**. Promedio mensual: ingresos US$2.319, resultado −US$170.

En esta ventana **no hay retiros de ganancia** (los 33 que existen van de feb-2024 a
mar-2025), así que los US$29.874 son los egresos totales. De los ingresos se excluyen
US$1.565 de Aporte de Capital, que no es venta.

Desglose de ingresos: Venta de Curso US$15.290 · Membership US$11.261 ·
DJ Delivery US$529 · resto US$753 (Clase de Prueba 369, Otros 163, Starter Pack 140,
Alquiler de Cabina 80).

> **El −7% descansa casi entero en un solo mes con problema de carga.** Dic-2025 tiene
> **cero** filas de Membership —todos los demás meses tienen entre 5 y 20— y ene-2026
> tiene 20, el máximo de la serie: las membresías de diciembre se cargaron en enero.
> Dic-2025 cierra en **−US$3.145**; **los otros once meses suman +US$1.103**. El total
> anual no cambia (el corrimiento cae dentro de la ventana), pero la lectura correcta
> no es "el negocio pierde plata": es **"el negocio está en el cero"**. Eso no le
> quita urgencia a nada de lo que sigue, pero sí cambia el tono.

> Seis filas de egresos de la ventana tienen un tipo de cambio implícito imposible
> (uno de 9.546, otro de 775) y el `USD_Ammount` está hardcodeado, no es fórmula.
> Recalculadas a la mediana del TC de su propio mes, los egresos suben US$269 y el
> resultado va a −US$2.311 (margen −8,3%). No cambia ninguna conclusión; queda
> declarado como el margen de error que tienen estos totales.

### Ya se está pautando

| Concepto | 12 meses | Por mes |
|---|---|---|
| Pauta Publicitaria | US$1.888 | US$157 |
| Gestión de Pauta | US$2.280 | US$190 |

**Se paga 21% más por gestionar la pauta que lo que se pone en la pauta misma**
(ratio 1,21x). Con este nivel de inversión, esa proporción no cierra.

### Cuánto vale un alumno (retención real)

Cohorte madura: 116 clientes con primer pago ≤ dic-2025, medidos hasta may-2026.
"Meses que paga" = **meses calendario distintos** con un pago de Membership o Venta de
Curso.

| | |
|---|---|
| Meses que paga, promedio | **2,81** (mediana 2) |
| Paga **una sola vez** y no vuelve | **53 de 116 — 46%** |
| Llega a 3 meses o más | 37 de 116 — 32% |
| Ingreso total por cliente | promedio **US$274** · mediana US$167 |
| El 20% que más deja | US$778 |

Adquisición orgánica actual: **7,8 clientes nuevos por mes** (jun-25 a may-26).

> **La retención está sesgada hacia abajo y sabemos cuánto.** Desde abr-2026 dejaron
> de cargarse los Client Id: 24 pagos por US$2.423 entran como `ID not found`, justo
> en los dos últimos meses de la ventana de medición. Si esos pagos pertenecieran a
> clientes de la cohorte, el promedio sería **2,94 meses y US$287 de LTV** en vez de
> 2,81 y US$274. **Tomamos el número conservador (2,81):** reasignar por nombre es
> exactamente lo que no se hace con plata. Pero la cota importa — el cuadro real es
> algo mejor que el que muestra la tabla. Lo que **no se mueve** es el 46% que paga
> una sola vez.

> Con otros criterios igual de defendibles el promedio cambia: contando pagos da 3,16;
> contando el span del primer al último mes da 3,37. Los tres dan mediana 2 y el 46%
> intacto. El LTV proyectado de la sección 5 usa el denominador 2,81.

### El CAC que te podés permitir

Costos variables: Sueldos Variables (US$3.580) + Sueldos (US$5.295) = US$8.875, o sea
**32% de los ingresos**. Más la comisión de Mercado Pago.

> **Aclaración que el documento anterior se comía:** existe además **Sueldos Fijos por
> US$6.904**, que es la línea de egreso más grande de todas. La nómina completa son
> US$15.779 = **57% de los ingresos**. No entra en el cálculo de contribución por ser
> fija, pero conviene tenerla a la vista: es el motivo por el que el negocio está en
> el cero aun con 62% de margen de contribución.

```
Contribución por cliente = US$274 × 0,62 = US$170
CAC objetivo (regla 1/3)  = US$170 / 3    = US$57
```

**US$57 ≈ ARS 82.000** al oficial de la planilla (1.445).

**Sensibilidad — los tres escenarios, para que el número no parezca más firme de lo que es:**

| Supuesto | Contribución | CAC objetivo |
|---|---|---|
| "Sueldos" es variable + MP 5,95% sobre todo *(el que uso)* | 62% | **US$57** |
| MP efectivo 4,9% (solo el 82,5% de los ingresos entra por MP) | 63% | US$58 |
| "Sueldos" es **fijo** (solo Sueldos Variables es variable) | 81% | US$74 |

El escenario conservador es el que manda las decisiones de abajo. Pero existiendo
`Sueldos Fijos` como categoría propia, que `Sueldos` sea variable es una hipótesis
discutible: si resulta fijo, el CAC que aguantás sube 30%.

---

## 2. Fase 0 — Atribución. Antes de poner un peso más.

Hoy se gastan US$157/mes en ads y **no se puede decir cuántos de los 7,8 clientes
nuevos vinieron de ahí.** Cualquier presupuesto decidido sobre eso es a ciegas.

Los cinco links ya están generados, en
`~/Desktop/Productoras/Astronomy/Academia/Flyers Academy/links-whatsapp.csv`. Cada uno abre el
WhatsApp con el mensaje ya escrito, así el primer mensaje que entra dice de qué pieza
vino — atribución sin construir nada:

| Producto | Mensaje que llega |
|---|---|
| Curso de DJ | "Hola! Vi el Curso de DJ y quiero info" |
| Producción | "Hola! Vi el curso de Produccion Musical y quiero info" |
| Producción online | "Hola! Vi Produccion Musical online y quiero info" |
| Membresías | "Hola! Vi las membresias de la Academy y quiero info" |
| Modo Profesional | "Hola! Vi el Modo Profesional y quiero info" |

**Lo único que hay que sostener a mano:** quien atienda el WhatsApp anota producto,
fecha y si cerró. Cuatro semanas de eso valen más que cualquier dashboard.

**Y una cosa que hay que arreglar sí o sí:** desde abril dejaron de cargarse los
Client Id (24 pagos, US$2.423). Sin ese campo no hay forma de medir retención, que es
justamente la variable de la que depende todo el presupuesto de pauta.

---

## 3. Fase 1 — La campaña

**Objetivo de Meta: Mensajes → WhatsApp** (Click to WhatsApp). No tráfico ni
conversiones en sitio: la venta la cierra José por chat, así que el anuncio tiene que
terminar en la conversación, no en una landing.

### Estructura: 1 campaña, 2 conjuntos

**A) Presencial — 70% del presupuesto**
- Radio de 20 km alrededor de Nordelta Plaza: Nordelta, Tigre, San Isidro,
  Vicente López, Escobar, Pilar.
- 18 a 34 años.
- Creativos: Curso de DJ, Producción, Membresías, Modo Profesional.

**B) Online — 30% del presupuesto**
- Argentina entera, **excluyendo** el radio del conjunto A (si no, compiten entre sí).
- 18 a 34 años.
- Creativos: solo Producción online.

### Segmentación

Dos públicos por conjunto, corriendo en paralelo:

1. **Intereses:** Ableton Live, Pioneer DJ, Beatport, Boiler Room, Cercle, Anyma,
   Tale of Us, Hernán Cattáneo, festivales locales de electrónica.
2. **Abierto (Advantage+ sin intereses).** En cuentas de este tamaño suele ganarle al
   segmentado, porque el algoritmo tiene más lugar para buscar. No lo saltees.

### Creativos

Arrancar con **6 por conjunto**: los ángulos `contacto` y `que-es` de cada producto,
en `feed` y `story`. Los otros 63 quedan de banco para rotar cuando se gasten.

Regla de rotación: si un creativo pasa 4 días con el costo por conversación 50% arriba
del promedio del conjunto, se apaga y entra otro del banco.

---

## 4. Presupuesto y umbrales de decisión

| | |
|---|---|
| Hoy | US$157/mes en ads |
| **Test propuesto** | **US$300/mes, 4 semanas** (≈ ARS 433.500 al oficial) |

Se propone US$300 y no más porque todavía no hay un CAC medido. Con US$300 y un CAC
de US$57 salen ~5 clientes nuevos por mes de pauta: suficiente volumen para leer el
número, chico para el riesgo.

**A las 4 semanas, con el CAC real en la mano:**

| CAC medido | Qué hacer |
|---|---|
| Menos de US$57 | Escalar a US$600/mes y sostener |
| Entre US$57 y US$90 | No escalar. Optimizar creativo y segmentación primero |
| Más de US$90 | Apagar. El problema no es la pauta |

**La gestión de pauta:** hoy son US$190/mes contra US$157 de inversión real. Con un
presupuesto de US$300, la gestión no debería pasar de US$100 o tiene que ir por dentro
del mismo número. Es la línea más fácil de recuperar de todo el P&L.

---

## 5. Lo que vale más que la pauta

El negocio está en el cero. Con esa estructura, **cada alumno nuevo que se va al mes
no deja margen para el siguiente.** Escalar la pauta sobre esto compra volumen de
gente que paga una sola vez.

El 46% que paga una vez es la palanca más grande del negocio:

```
Hoy:              2,81 meses  →  LTV US$274  →  CAC que aguanta: US$57
Llevándolo a 4:   4,00 meses  →  LTV US$390  →  CAC que aguanta: US$80
```

**+42% de LTV sin gastar un peso en ads**, y de paso te deja pagar 40% más caro cada
alumno, que es exactamente lo que hace competitiva a una cuenta de pauta chica.

La extrapolación aguanta: el ingreso por mes activo es plano a lo largo de la vida del
cliente (mes 1: US$92 · mes 2: US$99 · mes 3: US$94 · mes 4: US$100). No es que los
que se quedan pagan menos.

Palancas anotadas, sin construir todavía:

- **El mes 2 es donde se cae.** Un contacto al día 20 del mes 1, a mano, a los que no
  reservaron ninguna clase todavía.
- **Los créditos vencen a los 2 meses del último pago.** Un aviso automático a los 45
  días es a la vez servicio y recordatorio de renovación.
- **Clase de Prueba: 16 usos en 31 meses, y 13 de esos caen dentro de la ventana.**
  O sea que es algo que está pasando ahora, no una función abandonada. Vale la pena
  medir cuántas de esas 13 se convirtieron en cliente pago: si convierte bien, es el
  destino natural de la pauta (que el anuncio venda la clase de prueba, no la
  membresía).

---

## Pendientes de dato

- **Atribución de los US$157/mes actuales.** Sin esto no se sabe si la pauta que ya
  corre funciona.
- **Client Id sin cargar desde abr-2026** (24 pagos, US$2.423). Rompe la medición de
  retención hacia adelante.
- **Qué incluye "Gestión de Pauta"** y quién la hace (el equipo de pauta sigue sin
  nombre en el CLAUDE.md global). No tengo factura ni contrato, solo las 12 filas.
- **Si "Sueldos" es fijo o variable.** Mueve el CAC objetivo de US$57 a US$74.
- **Si los montos están cargados brutos o netos de comisión de Mercado Pago.** Si ya
  vienen netos, restar la comisión otra vez es doble conteo y la contribución real
  sería ~68%.
- El número de WhatsApp del posteo viejo (+54 11 2829-9151) no es el actual
  (+54 9 11 2400-5565). Conviene corregir el posteo.
