# Astronomy — cómo opera hoy y cómo debería operar

`06/08/2026` · Análisis de organización y operación. **Sin código.**
Complementa `ASTRONOMY_OS.md` (auditoría técnica, mismo día): aquel dice qué software hay,
éste dice cómo trabaja la empresa.

Medido contra producción (`qeakrjnseboiulcojlcw`). Donde un número no se pudo verificar, lo
digo en vez de estimarlo. **Segunda versión**, con las cuatro respuestas de Facu
incorporadas: dos de mis números originales estaban mal y están corregidos abajo.

---

## El hallazgo principal

Veníamos a arreglar la entrada del embudo: los leads de WhatsApp e Instagram que no se
registran. Ese agujero es real. Pero lo que se mide del otro lado es esto:

> **De 24 alumnos activos con clases, 8 están dormidos: ni tomaron clase en el último mes
> ni tienen ninguna agendada. Tres de ellos nunca tomaron una sola clase en su vida.**

| Quién | Plan | Sin venir |
|---|---|---|
| Santiago Pacino | **Gold** | nunca |
| Federico Toninelli | **Gold** | nunca |
| Roberto Fernández López | Curso de DJ | nunca |
| Pedro Fraguas | Curso de DJ | 59 días |
| Clemente Trejo | Curso de DJ | 44 días |
| Tomás Álvarez | Silver | 42 días |
| Javier Basso | Curso de DJ | 35 días |
| Santiago Romero | Curso de DJ | 34 días |

**33% de la base activa.** Y trece personas pierden créditos en los próximos 30 días —
Clemente, Pedro y Felipe los pierden el 13/08.

**Esa plata ya entró.** Recuperarla no cuesta pauta ni leads.

### Dos números que corrijo de la primera versión

Los pongo primero para que nadie use los viejos.

**1. "14 de 25 sin próxima clase agendada" — la métrica no sirve.** Medí con cuánta
anticipación se reserva en Astronomy: **la mediana es 2 días**, y 44 de 73 reservas se hacen
dentro de las 48 horas. Con ese hábito, no tener clase agendada para dentro de una semana es
lo normal, no una alarma. La métrica que aguanta es la de arriba: **sin clase reciente Y sin
clase agendada**, las dos juntas.

**2. "27 bajas en julio" — no son bajas reales.** Confirmado por Facu y verificado en la
base: 22 de ellas se cargaron **el mismo día**, el 22/07, y 25 de las 30 tienen motivo
"Baja administrativa (dejó de pagar / sin pagos)". Es limpieza de la migración. Además, las
30 bajas corresponden a sólo 15 personas —hay duplicados— y **4 de esas personas están
activas hoy**. `cancellations` no sirve como métrica de churn y no hay que usarla.

### Y un dato que cambia el diagnóstico, no el número

Facu: *"a los tres ya los llamamos, pero no vienen."*

**Ese llamado no está registrado en ningún lado.** Lo busqué en las cuatro tablas donde
podría estar: cero rastro. O sea que yo, con acceso completo a la base, saqué la conclusión
equivocada —"nadie los llamó"— cuando la verdad era "los llamaron y no funcionó".

**Son dos problemas distintos y necesitan dos acciones opuestas.** Si nadie llamó, se llama.
Si ya se llamó dos veces y no vienen, se decide otra cosa: pausar el plan, ofrecer clase
online, o dejarlos ir. Hoy el sistema no permite distinguirlos.

Éste es el mejor argumento que vamos a tener para el registro, y no es teórico: acaba de
costar una conclusión equivocada en un análisis hecho con la base entera a la vista.

---

# 1 · QUÉ EXISTE ACTUALMENTE

## 1.1 La empresa que conoce el sistema

Doce personas nombradas. El sistema conoce ocho.

| Persona | Rol | Qué dice el sistema |
|---|---|---|
| Facu | Dirección | Maestro **por variable de entorno, sin fila en `staff`** |
| Vlado | Dirección | Maestro. **Cero acciones en 30 días** |
| José | Academy Operations | 8 permisos. **54 acciones en 30 días — el que más trabaja** |
| Luqui | Academy Finance | 7 permisos. **4 acciones en 30 días** |
| Mateo Pastrana | Profesor | Profesor + 6 permisos. 119 clases, 10 acciones |
| Mateo Guini | Profesor | Profesor. 44 clases. **0 permisos, 0 acciones desde que existe** |
| Valen Frando | Profesor | Cargado **como "Owners of Time"**. 18 clases. 0 permisos, 0 acciones |
| Lucas Lanfran | Sello + estudio | **Correcto: no da clases** (confirmado). Sello y calendario en lectura |
| **Annie** | Diseño | **No existe** |
| **Lola** | Diseño | **No existe** |
| **Pacha (Fran Otero)** | Marketing | **No existe** |
| **Gonza** | Programa el chatbot, nada más | **No existe** |

**Cuatro personas trabajan para Astronomy y no están en el sistema.**

## 1.2 La operación de Academy, en números

| | Jun | Jul | Ago (al día 6) |
|---|---|---|---|
| Clases dadas | 85 | 97 | 28 |
| Alumnos distintos con clase | 18 | 17 | 12 |
| Ventas | 22 | 23 | 13 |
| De ésas, primeras compras | 20 | 4 | 4 |
| Facturado | $3.494.240 | $3.457.200 | $1.285.363 |

Carga docente de agosto: **Pastrana 16 clases, Guini 9, Valen 2.** Pastrana concentra el 59%
de la operación docente.

Planes activos: Curso de DJ 15, Silver 6, Gold 4, DJ Delivery 2.

Ritmo semanal de clases, junio a hoy: entre 13 y 22 por semana, sin caída. **La operación
docente está estable**; el problema es de composición, no de volumen.

---

# 2 · QUÉ FUNCIONA

1. **El cobro.** En 30 días: 37 pagos acreditados solos, 9 ya estaban, 11 ignorados
   correctamente. El circuito de plata está sano.
2. **La agenda.** 175 reservas activas. Los profesores tienen calendario, los alumnos
   reservan, los créditos se descuentan solos.
3. **El reparto de trabajo por persona.** El concepto de **dueño** (José / Luqui / Facu)
   está construido: el permiso dice quién *puede*, el dueño dice de quién *es*. Es la
   separación de responsabilidades que se está pidiendo.
4. **El escalamiento José → Luqui ya existe en la base.** `incidencias` tiene `consulta`,
   `consulta_para`, `consulta_vence`, `respuesta`, `respuesta_por`. El circuito "José
   registra → Luqui revisa → Luqui resuelve → José sigue" está modelado. No hay que
   diseñarlo: hay que hacerlo andar.
5. **José usa el sistema.** 54 acciones en 30 días. Es el único del equipo, y es el dato más
   esperanzador que hay acá.

> **Para no sacar conclusiones falsas:** el "último login" de José figura el 17/07. **Eso no
> significa que no entre.** La sesión no se cierra, así que no se registra un login nuevo
> aunque trabaje todos los días. El dato válido de uso es `audit_log`.

---

# 3 · QUÉ ESTÁ INCOMPLETO

## 3.1 El agujero del CRM es real, y su tamaño no se puede medir hoy

Un lead sólo existe si tocó la web. Quien escribe por Instagram o WhatsApp no tiene fila en
ninguna tabla.

Intenté medir cuánto pesa cruzando quiénes pagaron contra quiénes dejaron rastro web. **El
resultado no sirve**: el rastreo (`lead_events`) empezó el **04/08/2026**, hace dos días. De
los 3 que pagaron desde entonces, los 3 tienen rastro. Cualquier número más grande compara
gente de junio con un sistema que no existía en junio.

**Sabemos que el agujero existe por construcción; no sabemos si es grande.**

**Y hay una pieza nueva que cambia el diseño: Gonza y el chatbot.** Si el chatbot atiende
WhatsApp o Instagram, entonces **el chatbot ya tiene los leads** — y la solución no es que
José los cargue a mano (eso es agregarle trabajo manual, justo al revés de lo que
queremos), sino que el chatbot los escriba solo. Cambia por completo quién construye qué.
Es la pregunta 1 de §9.

## 3.2 Dos profesores tienen cuenta y no pueden hacer nada

Guini da 44 clases y Valen 18. Los dos con **cero permisos** y **cero acciones desde que
existen**. Sus agendas las carga otro. Si el objetivo es que la empresa no dependa de una
persona, hoy la agenda de dos profesores depende de que José o Pastrana la carguen.

## 3.3 Valen está cargado con nombre de artista

Aparece como **"Owners of Time"**. Sus 18 clases y su sueldo cuelgan de ese string.

## 3.4 Las ocho preguntas escaladas vencen mañana y pasado

Las 8 filas de `incidencias` son consultas que **abrimos nosotros**, no el equipo: cinco
para Luqui, tres para José. **Ninguna contestada.** Vencen el 07 y el 08/08. Es el primer
experimento real de adopción y llega antes que el 18/08.

## 3.5 Lo que no existe todavía

- **Dominé**: 1 evento cargado, sin producción, proveedores, gastos ni Splitwise.
- **Label**: bandeja de demos y lanzamientos sí; tracks, versiones y metadata no.
- **Dirección**: ninguna vista contesta "cómo está cada unidad".

---

# 4 · QUÉ PROCESOS ESTÁN DESORDENADOS

### 4.1 Nadie es dueño de que el alumno vuelva

El sistema detecta al que no pagó, al que se dio de baja y al que tiene un problema de
plata. **No hay responsable declarado de que un alumno que ya pagó siga viniendo.** Por eso
hay 8 dormidos y 3 que nunca vinieron: no falló nadie, no es tarea de nadie.

### 4.2 El registro de lo que se habla no ocurre

`incidencia_eventos`: **cero filas**. Cada conversación vive en WhatsApp y en la cabeza de
José. Es lo que acaba de hacerme sacar una conclusión equivocada sobre los tres que nunca
vinieron. Mientras siga así, ninguna unidad puede tener la propiedad que se pidió: *que una
persona nueva se incorpore leyendo el sistema.*

### 4.3 Cuatro personas operan por fuera

Annie, Lola, Pacha y Gonza. Diseño, marketing y el chatbot no tienen dónde recibir un pedido
ni dónde entregar. Se pide por WhatsApp y se entrega por Drive.

### 4.4 El escalamiento existe y nunca se usó

Construido, cero uso real. No es un problema de software.

### 4.5 Dirección tiene acceso y no tiene ritual

Vlado es maestro y no entró nunca. "Ver todo" no es un rol: sin una reunión con agenda fija
y un lugar donde queden las decisiones, el acceso total se convierte en no mirar nada.

---

# 5 · QUÉ DEBERÍA CAMBIAR

Cada cambio contesta las cuatro preguntas pedidas. Ordenados por plata.

### Cambio 1 — Decidir qué se hace con los 8 dormidos

| | |
|---|---|
| Qué problema resuelve | 8 de 24 activos no vienen; 3 nunca vinieron. Dos son Gold |
| Quién lo usa | José, y la decisión es de Facu |
| Frecuencia | Una vez ahora, después semanal |
| Si no existe | Pagan hasta que se cansan y se van sin avisar |

**No es software.** Los tres que nunca vinieron ya fueron llamados: ahí la decisión no es
"llamar otra vez", es **elegir qué se les ofrece** — pausar el plan, clase online, o dejarlos
ir. Los otros cinco llevan entre 34 y 59 días: ésos sí es llamar.

### Cambio 2 — Que quede escrito lo que se habla

| | |
|---|---|
| Qué problema resuelve | No se puede distinguir "no lo llamamos" de "lo llamamos y no vino" |
| Quién lo usa | José |
| Frecuencia | Cada conversación |
| Si no existe | Cada decisión se toma sobre información que sólo tiene una persona |

**La pantalla ya existe.** Esto es un hábito, no una función. Y es lo que el 18/08 se mide.

### Cambio 3 — Cerrar el circuito de las 8 preguntas

| | |
|---|---|
| Qué problema resuelve | El escalamiento existe y nadie lo usó nunca |
| Quién lo usa | José y Luqui |
| Frecuencia | Vencen el 07 y 08/08 |
| Si no existe | El 18/08 no sabremos si el sistema no sirve o si nadie lo abrió |

Cuesta cero y decide todo lo demás.

### Cambio 4 — Arreglar las fichas mal cargadas

Guini y Valen sin permisos, Valen con nombre de artista, Facu sin fila en `staff`. Media
hora, y saca tres mentiras del organigrama. **Lanfran ya está bien: no da clases.**

### Cambio 5 — Annie, Lola, Pacha y Gonza

| | |
|---|---|
| Qué problema resuelve | Cuatro personas operan sin registro |
| Quién lo usa | Ellos cuatro |
| Frecuencia | Semanal |
| Si no existe | Si alguno se va, no queda rastro de qué hacía |

Empezar por lo mínimo: una cuenta y el permiso más chico. **Gonza puede no necesitar
cuenta** — si sólo programa el chatbot, lo que hay que integrar es el chatbot, no a él.

### Cambio 6 — El CRM de leads externos

| | |
|---|---|
| Qué problema resuelve | Los leads de WhatsApp e Instagram no tienen dónde anotarse |
| Quién lo usa | José — **o el chatbot, que es distinto** |
| Frecuencia | Desconocida |
| Si no existe | Se pierden contactos, en cantidad desconocida |

Va último de los seis porque es el único cuya frecuencia no podemos contestar, y porque su
diseño depende de qué hace el chatbot.

---

# 6 · QUÉ NO TOCAR

| No tocar | Por qué |
|---|---|
| Mercado Pago, webhook, créditos | Sano y con plata real. Módulo congelado por decisión previa |
| El panel de profesores | Anda y lo usan |
| El motor de cola (`lib/workflows.ts`) | El mejor activo del sistema. Se le agregan tareas, no se rediseña |
| El modelo de casos (`lib/casos.ts`) | Seis estados que funcionan. **No superponerle un embudo nuevo** |
| Los permisos | La única reja real. Los roles con nombre se apoyan encima |
| El Libro anterior al 14/07/2026 | 195 renglones sin confirmar son historia archivada. Desde el corte hay 10 |
| `unassigned_payments` | Los 30 "sin asignar" están en `ignored`: ya triados. **No hay backlog — verificado** |
| `cancellations` | **No usarla como métrica.** 25 de 30 son limpieza administrativa |
| La ficha de Lanfran | Está bien como está |

---

# 7 · LAS CUATRO UNIDADES

## 7.1 Academy

Está viva y es la única que produce. Lo que falta no es software:

- Responsable de **venta** → José. Está.
- Responsable de **cobro** → Luqui. Está.
- Responsable de **que el alumno siga viniendo** → **hoy nadie.** Es el hueco.
- Responsable de **que el profesor tenga agenda** → José y Pastrana, para tres profes.

Métrica única de Academy, para empezar: **alumnos activos dormidos.** Hoy da **8 de 24**.
Regla en una línea: *un alumno que pasa un mes sin venir tiene una acción registrada, o deja
de ser un alumno activo.*

## 7.2 Dominé

**No construir, y coincido.** Pero definir ahora dos cosas que después cuestan caro:

1. **Qué es un evento cerrado.** Termina cuando su resultado está calculado y los cuatro
   socios lo vieron. Sin esa definición, el Splitwise reparte sobre números en discusión.
2. **Quién adelanta la plata, por defecto.** El Splitwise ordena lo que ya pasó; sin regla
   previa, sólo documenta el desorden más rápido.

Los porcentajes (35/35/15/15) van en configuración, no en la base: cambian por acuerdo, no
por transacción.

## 7.3 Label

| Tu estado | Hoy |
|---|---|
| Recibido · En revisión · Seleccionado | Existen |
| **Producción** · **Aprobado** | **Faltan** |
| Lanzado | Existe, como release publicado |
| Rechazado | Existe |

Faltan dos estados y el vínculo demo → release. Es poco trabajo.

**De acuerdo con archivos en Drive.** La regla que lo hace funcionar: *el sistema guarda el
link, Drive guarda el archivo, y el link vive en la ficha de la demo — no en un chat.* Sin
eso, "está en Drive" significa "está en el Drive de alguien".

`label_demos` tiene **cero filas** — el sello salió ayer, es esperable. Ordenar un flujo que
no recibió su primera demo es diseñar sin evidencia. Esperar a las primeras diez.

## 7.4 Empresa

Lo que falta no es un dashboard: es un **ritual**. Un tablero sin reunión se mira dos semanas
y después no.

- **Reunión quincenal, Facu y Vlado, 30 minutos**, agenda fija: cómo está cada unidad, qué
  problema está sin dueño, qué decisión está trabada.
- **Cuatro métricas, ni una más.** Alumnos activos · **alumnos dormidos** · ventas del mes ·
  problemas abiertos sin responsable.
- **Las decisiones se escriben donde se toman.** Si no queda escrita, la reunión no ocurrió.

El tablero se construye **después** de que la reunión exista y haya pedido algo. Al revés es
una pantalla más que nadie abre, que es exactamente el problema que ya tenemos.

---

# 8 · EL ORDEN QUE PROPONGO

| | Qué | Cuándo | Es software |
|---|---|---|---|
| 0 | Contestar las 8 preguntas escaladas | 07–08/08 | No |
| 0 | Decidir qué se hace con los 8 dormidos | Esta semana | No |
| 0 | Las dos mañanas mirando a José y a Luqui | Antes del 18/08 | No |
| 1 | Arreglar las fichas del equipo | 30 min | Mínimo |
| 2 | Alta de Annie, Lola y Pacha | 1 día | Mínimo |
| 3 | Dormidos como tarea con dueño en el escritorio | Después del 18/08 | Sí |
| 4 | Leads externos — **diseño según qué hace el chatbot** | Después de la mañana con José | Sí |
| 5 | Ritual de Dirección; su tablero después | Septiembre | Primero no |
| 6 | Label: los dos estados que faltan | Cuando haya 10 demos reales | Sí |
| 7 | Dominé | Cuando haya un evento | Sí |

**Los tres primeros no cuestan una línea de código y son los que más plata mueven.**

---

# 9 · LAS TRES PREGUNTAS, CONTESTADAS EL 06/08

**1. El chatbot de Gonza atiende WhatsApp.** Confirmado por Facu. Entonces el diseño del CRM
queda decidido: **el bot escribe el lead, no José.** Cargar a mano sería agregarle trabajo
manual a la persona más ocupada del equipo, justo al revés de lo que se busca. Lo que hay que
definir con Gonza es una sola cosa: dónde deja el bot el nombre, el contacto y qué pidió.

**2. Los dos Gold SÍ reciben créditos — mi "no reciben nada" estaba mal.** Corregido:

| | Créditos vigentes | Equivalen a | Vencen |
|---|---|---|---|
| Federico Toninelli | 6.960 | **116 clases** | 01/09/2026 |
| Santiago Pacino | 6.730 | **112 clases** | 01/09/2026 |

Y ahí aparece lo que sí es un problema: **13.690 créditos vencen el 01/09**, en 26 días, y
**pagar de nuevo no los salva.** `grant_credits` inserta un lote nuevo con su propio
vencimiento; **no extiende el de los lotes viejos.** O sea que van a pagar agosto y
septiembre y perder igual todo lo acumulado.

El detector de la cola de José los va a levantar, pero recién el **22/08** — su ventana es de
10 días. Llega a tiempo por poco.

**Lo que hay que decidir antes es otra cosa: si ese saldo es correcto.** Los dos lotes
grandes vienen de `recalc-calendly:2026-07-01`, un recálculo de la migración. 116 clases de
crédito para alguien que nunca tomó ninguna es un número que conviene mirar antes de que
entre a una cola que va a decir "rescatar $4.176.000".

**3. Guini y Valen YA PUEDEN manejar su disponibilidad. No hay nada que construir.**
`/profe/horarios` **no pide ningún permiso**: sólo tener `professor_name`, y los dos lo
tienen. De hecho ya hay franjas cargadas — Guini 2, Valen 5, Pastrana 7.

Y lo de Valen online también está resuelto desde antes: está marcado `online: true` en
`lib/profes.ts`, con su link de Discord, y `ONLINE_PROFES` significa literalmente *"profes que
NO se rigen por los horarios del estudio"*. Se adapta a Valen exactamente como se pidió.

**El problema no es de software: es que ninguno de los dos lo sabe.** Cero acciones desde que
tienen cuenta. Se resuelve con un mensaje, no con código.
