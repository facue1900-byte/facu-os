# Plan de equipo — Astronomy Academy

`v1` · 08/09/2026 · **Sprint 1: 14/09 → 12/10/2026 (4 semanas)**

Quién entrega qué, qué día, a qué hora, y cómo se verifica sin preguntarle a nadie.

---

## Por qué este plan es distinto del anterior

Hubo dos sprints escritos (04–17/08 y 18–31/08). **No se ejecutaron.** El chequeo del
18/08 dio `contact_log` 0 filas, `ritmo_log` 0 y `expenses` 0; al 01/09 `contact_log`
seguía en 0. Tres causas, y las tres se corrigen acá:

1. **12 de 14 tareas eran de José.** Annie, Lola, pauta, Pastrana, Guini y Valen no
   tenían ninguna, cobrando >$2.000.000/mes entre todos.
2. **No había hora ni lugar de entrega.** "Esta semana" no es una fecha.
3. **Nadie miraba el resultado.** Sin un momento fijo donde se lee el número, una tarea
   sin hacer no tiene consecuencia.

> **Este plan no autoriza escribir una línea de código.** Todo se hace con pantallas y
> herramientas que ya existen. Si algo no se puede hacer sin software nuevo, se anota
> como fricción en el Lunes de Números y se decide ahí — nunca se construye en el medio.

---

## El ritmo: el Lunes de Números

**Todos los lunes 09:00, 30 minutos, por videollamada. Conduce Vlado.** (Es el socio que
maneja las finanzas: que el número lo lea el que responde por él, no el que ejecuta.)

Se leen **6 números** y nada más. Cada uno tiene un dueño que lo dice en voz alta:

| # | Número | Dueño | De dónde sale | Hoy |
|---|---|---|---|---|
| 1 | **Altas del mes** (primeros pagos) | Josefina | `/admin/libro` | 3/mes |
| 2 | **Conversión de WhatsApp** (conversaciones → altas) | Josefina | planilla de contactos | **1,3%** |
| 3 | **Alumnos activos dormidos** (30+ días sin venir) | Josefina | `/admin` | **8 de 24** |
| 4 | **Pesos sin dueño** (pagos sin atribuir) | Luqui | `/admin/pagos-sin-asignar` | 45 mov. |
| 5 | **Costo por lead** | Pauta | `REPORTE_PAUTA.txt` (llega solo, lunes 10:00) | US$1,94 |
| 6 | **Clases dadas en la semana** | Pastrana | `/admin` calendario | ~24/sem |

**Regla del lunes:** el que no entregó lo dice él, primero, sin que se lo pregunten. No se
discute la tarea no hecha en la reunión: se reagenda con fecha nueva y se sigue.

**El norte:** el equilibrio está en **14,5 alumnos** y hoy hay 22 activos cayendo a ~15
con 20% de churn mensual. Todo lo de abajo apunta a lo mismo: **subir altas y frenar la
caída.**

---

## Josefina Meyrelles — Academy Ops + closer

Dueña de: **cobrar el mes · rescatar clases · activar · recuperar · corregir créditos.**

| Cuándo | Qué entrega | Dónde se ve |
|---|---|---|
| **Lun a vie, 10:00–11:30** | La cola de contactos del día, vaciada. **Cada conversación anotada**: a quién · qué se dijo · qué contestó · qué pasó | `contact_log` con filas |
| **Martes 18:00** | Los **14 mensajes pendientes** del 01/09: cobrar septiembre · rescatar clases · destrabar · inactivos | `contact_log` |
| **Jueves 18:00** | Escritos los **8 alumnos dormidos**, con **dos horarios concretos ofrecidos** y el turno agendado por ella | Calendario + `contact_log` |
| **Viernes 17:00** | Reporte de la semana en el grupo: conversaciones · respondidas · clases agendadas · altas | WhatsApp del equipo |

**Objetivo del sprint:** conversión de WhatsApp de **1,3% → 3%**. Con 232 conversaciones
al mes eso son **7 altas mensuales en vez de 3**.

**Su bono es por cantidad de ventas**, así que este objetivo y su plata apuntan al mismo
lado. No hace falta inventarle otro incentivo.

---

## Luqui — Finanzas y registro

Dueño de: **que todo el dinero que entró y salió exista en el sistema, y que ningún peso
quede sin dueño.**

| Cuándo | Qué entrega | Dónde se ve |
|---|---|---|
| **Lun a vie, 18:00** | Cargado lo que entró y lo que salió del día — o declarado que no hubo nada | `ritmo_log`, `expenses` |
| **Jueves 12:00** | **Pagos sin dueño en cero.** Hoy hay 45 movimientos sin identificar, incluidos $4.071.127 que SALIERON | `/admin/pagos-sin-asignar` |
| **Día 3 hábil de cada mes** | El mes anterior cerrado: ingresos, egresos y resultado. **Sin esto el margen miente** | `/admin/libro` |
| **Por única vez, vie 18/09** | **Cargados los egresos de julio y agosto**, que hoy no están | `expenses` (hoy 0 filas de por vida) |

**Objetivo del sprint:** que `expenses` deje de tener 0 filas y que el resultado mensual
salga solo el día 3, sin que nadie lo arme a mano.

---

## Annie Hoffer — Diseño de performance (pauta)

$350.000/mes. **Hasta hoy no tenía ningún entregable definido ni fecha.**

| Cuándo | Qué entrega |
|---|---|
| **Lunes 12:00** | Recibe el brief: qué producto se empuja esa semana y qué dijo el reporte de pauta |
| **Jueves 12:00** | **3 piezas nuevas para pauta** (feed + story), sobre el producto de la semana |
| **Lunes siguiente** | Escucha cuál de las 3 rindió mejor y con eso arma las de la semana |

**Objetivo del sprint:** 12 piezas entregadas y **saber cuál convierte**. Hoy se diseña
sin que nadie devuelva el resultado, así que se diseña a ciegas.

---

## Lola Gallal — Diseño de marca (orgánico)

$350.000/mes. Mismo caso: sin entregable con fecha hasta hoy.

| Cuándo | Qué entrega |
|---|---|
| **Lunes 12:00** | Recibe el calendario de contenido de la semana |
| **Miércoles 12:00** | **Los posteos orgánicos de la semana** (feed + stories), en marca |
| **Viernes** | Las piezas de la fecha de eventos que corresponda, si hay |

**Annie hace pauta, Lola hace marca.** Separado a propósito: hoy no está claro quién hace
qué y el riesgo es que las dos hagan lo mismo, o ninguna haga lo que falta.

---

## Equipo de pauta — $228.000/mes

| Cuándo | Qué entrega |
|---|---|
| **Lunes 10:00** | El reporte ya les llega solo (`REPORTE_PAUTA.txt`, launchd). Lo leen antes del Lunes de Números |
| **Lunes, en la reunión** | Costo por lead y leads de la semana, dicho en voz alta |
| **Miércoles** | Los cambios de campaña de la semana, con qué se cambió y por qué |

**Objetivo del sprint:** bajar el **CAC de US$170**. Hoy el LTV es de US$109 a US$319:
con un CAC de 170 el negocio pierde plata en la mitad de los alumnos que compra.

---

## Mateo Pastrana — Profesor + Studio Manager

Concentra el 59% de la operación docente y además es la cara del día a día.

| Cuándo | Qué entrega |
|---|---|
| **Diario** | Estudio abierto en horario y en condiciones |
| **Lunes y viernes** | **Checklist de equipos**: qué anda, qué falla, qué falta comprar. Foto al grupo |
| **Viernes 17:00** | Las clases de la semana, y qué alumno vino flojo o dejó de venir |

**Lo que falta y te lo dejo anotado:** su sueldo de studio manager está adentro de la
bolsa de «Profesores» ($1.140.000). Mientras siga ahí, **el costo por clase de Academy
está inflado y no se puede calcular**. Separarlo en dos renglones es el arreglo.

---

## Mateo Guini y Valen Frando — Profesores

Hoy **su agenda la carga otro** y tienen cero permisos en el sistema. Eso es trabajo de
José que no debería existir.

| Cuándo | Qué entrega |
|---|---|
| **Viernes 17:00** | Sus horas disponibles de la semana siguiente, cargadas **por ellos** |
| **Después de cada clase** | La clase marcada como dada |

**Requisito previo (Facu, 30 min):** darles permisos y arreglar la ficha de Valen, que
está cargada como "Owners of Time" (su nombre de artista) — su sueldo cuelga de ese string.

---

## Vlado — Socio, finanzas y visión

| Cuándo | Qué entrega |
|---|---|
| **Lunes 09:00** | **Conduce el Lunes de Números** |
| **Día 5 de cada mes** | El resultado del mes anterior leído y comentado: cerró o no cerró |

---

## Facu — Dirección

| Cuándo | Qué entrega |
|---|---|
| **Lunes, en la reunión** | Las decisiones que traban a otro. Ninguna tarea de nadie espera más de una semana por una decisión tuya |
| **Miércoles 09/09** | Permisos de Guini y Valen + ficha de Valen |
| **Viernes 11/09** | Cuánto de los $1.140.000 de «Profesores» es el fijo de studio manager |

---

## Calendario del sprint

**Semana 0 · 09 al 13/09 — puesta a punto.** No arranca el ciclo todavía.

| Día | Quién | Qué |
|---|---|---|
| Mié 09/09 | Facu | Permisos de Guini y Valen; ficha de Valen |
| Mié 09/09 | Facu | Manda este plan a cada uno, uno por uno, no al grupo |
| Jue 10/09 | Todos | Confirman por escrito su día y hora de entrega |
| Vie 11/09 | Facu | Define el fijo de studio manager |
| Vie 11/09 | Luqui | Deja los 6 números del tablero cargados por primera vez |

**Semanas 1 a 4 — el ciclo corre.**

| Lunes 09:00 | Qué se mira además del tablero |
|---|---|
| **14/09** | Primer Lunes de Números. Se fija la línea de base de los 6 |
| **21/09** | Cómo salió Dominé (sáb 19/09). Primera lectura de conversión de Josefina |
| **28/09** | Media semana de sprint: ¿la conversión se movió de 1,3%? |
| **05/10** | Cierre de septiembre de Luqui, ya cargado el día 3 |
| **12/10** | **Cierre del sprint.** Se decide qué sigue |

**Eventos — Dominé, sábado 19/09.** La única línea de eventos acá adentro, porque es lo
que tiene plata arriba en estos 11 días:

| Día | Quién | Qué |
|---|---|---|
| Mié 09/09 | Facu | Cargar la fecha en la ticketera |
| Vie 11/09 | Lola | Flyer y banner del evento |
| Lun 14/09 | Facu | Abrir venta y repartir links de RRPP |
| Sáb 19/09 | Todos | La fecha |

---

## Cómo se sabe si esto funcionó, sin opiniones

Al **lunes 12/10** se cuentan filas. No se pregunta a nadie:

| Prueba | Cómo se cuenta | Hoy | Meta |
|---|---|---|---|
| Josefina usó la cola | filas en `contact_log` | **0** | >80 |
| Luqui carga la plata | filas en `expenses` | **0** | >30 |
| No hay plata sin dueño | `/admin/pagos-sin-asignar` | 45 | 0 |
| El diseño entrega | piezas en el Drive con fecha | — | 12 + 4 |
| El negocio creció | altas del mes | 3 | 7 |

**Si al 12/10 `contact_log` y `expenses` siguen en 0, el problema no es de tareas: es de
adopción, y no se escribe una línea más hasta entender por qué** (Ley 9).
