# Astronomy — cómo opera hoy y cómo debería operar

`06/08/2026` · Análisis de organización y operación. **Sin código.**
Complementa `ASTRONOMY_OS.md` (auditoría técnica, mismo día): aquel dice qué software hay,
éste dice cómo trabaja la empresa.

Todo está medido contra la base de producción (`qeakrjnseboiulcojlcw`) el 06/08/2026. Donde
un número no se pudo verificar, lo digo en vez de estimarlo.

---

## El hallazgo principal, y no es el que veníamos a buscar

Veníamos a arreglar la entrada del embudo: los leads de WhatsApp e Instagram que no se
registran. Ese agujero es real. Pero medido contra la base, **el desagüe más grande está en
la otra punta**:

> **De 25 alumnos activos con clases, 14 no tienen ninguna clase futura agendada.
> Tres de ellos pagaron y nunca tomaron una sola clase en su vida.**

| | |
|---|---|
| Suscripciones activas | 27 (2 son DJ Delivery, que no lleva clases) |
| De los 25 restantes, sin próxima clase agendada | **14 (56%)** |
| Que nunca tomaron ninguna clase | **3** — dos de ellos plan Gold ($195.600) |
| Bajas registradas en julio | **27** |
| Personas que pierden créditos en los próximos 30 días | **13** |

Los tres que nunca tomaron clase: Santiago Pacino (Gold), Federico Toninelli (Gold),
Roberto Fernández López (Curso de DJ). Pagaron, y el servicio no se prestó nunca.

Y seis más no pisan el estudio desde junio o principios de julio: Pedro Fraguas (1 clase,
última el 08/06), Clemente Trejo (3, el 23/06), Tomás Álvarez (4, el 25/06), Javier Basso
(2, el 02/07), Santiago Romero (3, el 03/07).

**Esa plata ya entró.** Retenerla no cuesta pauta ni cuesta leads: cuesta que alguien
escriba. Y tres de esos nombres —Clemente, Pedro y Felipe— son justo los que tienen
créditos venciendo el 13/08.

**Conclusión operativa: la Fase 1 de Academy no es el CRM. Es la retención.** El CRM va
segundo, y va con los ojos abiertos sobre algo que explico en §3.

---

# 1 · QUÉ EXISTE ACTUALMENTE

## 1.1 La empresa que conoce el sistema

Vos nombraste doce personas. El sistema conoce ocho.

| Persona | Rol que le diste | Qué dice el sistema |
|---|---|---|
| Facu | Dirección | Maestro **por variable de entorno, sin fila en `staff`** |
| Vlado | Dirección | Maestro. **Cero acciones en 30 días** |
| José | Academy Operations | 8 permisos. **54 acciones en 30 días — el que más trabaja del equipo** |
| Luqui | Academy Finance | 7 permisos. **4 acciones en 30 días** |
| Mateo Pastrana | Profesor | Profesor + 6 permisos. 119 clases, 10 acciones |
| Mateo Guini | Profesor | Profesor. 44 clases. **0 permisos, 0 acciones desde que existe** |
| Valen Frando | Profesor | Existe **como "Owners of Time"**. 18 clases. 0 permisos, 0 acciones |
| Lucas Lanfran | Profesor (según vos) | **No es profesor en el sistema: 0 clases.** Tiene sello + calendario en lectura |
| **Annie** | Diseño | **No existe** |
| **Lola** | Diseño | **No existe** |
| **Pacha (Fran Otero)** | Marketing | **No existe** |
| **Persona del chatbot** | Soporte con José | **No existe, ni siquiera tiene nombre acá** |

**Cuatro personas trabajan para Astronomy y no están en ningún lado del sistema.** Todo lo
que hacen se coordina por fuera, y si mañana se van no queda registro de qué hacían.

## 1.2 La operación de Academy, en números

| | Jun | Jul | Ago (al día 6) |
|---|---|---|---|
| Clases dadas | 85 | 97 | 28 |
| Alumnos distintos con clase | 18 | 18 | 13 |
| Ventas | 22 | 23 | 13 |
| De ésas, primeras compras | 20 | 4 | 4 |
| Facturado | $3.494.240 | $3.457.200 | $1.285.363 |
| Bajas | — | 27 | 3 |

Carga por profesor en agosto: **Pastrana 16 clases, Guini 9, Valen 2.** Pastrana concentra
el 59% de la operación docente.

Planes activos: Curso de DJ 15, Silver 6, Gold 4, DJ Delivery 2.

## 1.3 Qué software hay

Está detallado en `ASTRONOMY_OS.md`. El resumen: 87 pantallas (48 administrativas), 68
tablas, 16 permisos granulares, un motor de cola de trabajo por persona, un CRM de casos
con seis estados, y un centro de operaciones con 18 detectores de problemas.

---

# 2 · QUÉ FUNCIONA

Esto no se toca y conviene decirlo primero, porque es más de lo que parece.

1. **El cobro.** Mercado Pago acredita solo. En 30 días: 37 acreditados, 9 que ya estaban,
   11 ignorados correctamente. El circuito de plata está sano.
2. **La agenda.** 210 reservas en el sistema propio, 175 activas. Los profesores tienen
   calendario, los alumnos reservan, los créditos se descuentan solos.
3. **El reparto de trabajo por persona.** El concepto de **dueño** (José / Luqui / Facu)
   está construido y es correcto: el permiso dice quién *puede*, el dueño dice de quién
   *es*. Es exactamente la separación de responsabilidades que estás pidiendo.
4. **El escalamiento José → Luqui que describís ya existe en la base.** La tabla
   `incidencias` tiene `consulta`, `consulta_para`, `consulta_vence`, `respuesta`,
   `respuesta_por`. El circuito "José registra → Luqui revisa → Luqui resuelve → José
   sigue" está modelado. No hay que diseñarlo: hay que hacerlo andar.
5. **José usa el sistema.** 54 acciones en 30 días, la última el 05/08. Es el único del
   equipo que lo hace, y es el dato más esperanzador que hay acá.

> **Aclaración para no sacar conclusiones falsas:** el "último login" de José figura el
> 17/07. **Eso no significa que no entre.** La sesión no se cierra, así que Supabase no
> registra un login nuevo aunque entre todos los días. El dato válido de uso es
> `audit_log`, y ahí José aparece trabajando.

---

# 3 · QUÉ ESTÁ INCOMPLETO

## 3.1 El agujero del CRM es real, pero su tamaño NO se puede medir hoy

Confirmado: un lead sólo existe si tocó la web. Quien escribe por Instagram o WhatsApp no
tiene fila en ninguna tabla. **No hay dónde anotarlo, así que el trabajo pasa afuera.**

Intenté medir cuánto pesa ese agujero cruzando quiénes pagaron contra quiénes dejaron
rastro en la web. **El resultado no sirve y lo digo antes de que alguien lo use**: el
rastreo (`lead_events`) empezó el **04/08/2026**, hace dos días. De los 3 que pagaron desde
entonces, los 3 tienen rastro. Cualquier número más grande que ése compara gente de junio
con un sistema que no existía en junio.

**Traducción: sabemos que el agujero existe por construcción, no sabemos si es grande.**
Y ésa es justamente una pregunta que se contesta gratis, mirando a José una mañana.

## 3.2 Dos profesores tienen cuenta y no pueden hacer nada

Guini da 44 clases y Valen 18. Los dos tienen **cero permisos** y **cero acciones desde que
existen**. Sus clases las agenda otro. Si el objetivo es que la empresa no dependa de una
persona, hoy la agenda de dos profesores depende de que José o Pastrana la carguen.

## 3.3 Lanfran figura como profesor y no lo es

Vos lo listás entre los profesores. En el sistema tiene cero clases y ningún permiso de
enseñanza; tiene el sello y el calendario en lectura. **O da clases y le falta el acceso, o
no da clases y sobra en la lista.** Es una pregunta de una línea que cambia su alta.

## 3.4 Valen está cargado con nombre de artista

Aparece como **"Owners of Time"**, no como Valen Frando. Sus 18 clases y su sueldo cuelgan
de ese string. Un profesor nuevo que entre a mirar no sabe quién es.

## 3.5 Las ocho preguntas escaladas vencen mañana y pasado

Las 8 filas de `incidencias` son consultas que **abrimos nosotros**, no el equipo: cinco
para Luqui, tres para José. **Ninguna está contestada.** Vencen el 07 y el 08/08.

Ése es el primer experimento real de adopción y llega antes que el 18/08.

## 3.6 Lo que no existe todavía

- **Dominé**: 1 evento cargado, sin producción, sin proveedores, sin gastos, sin Splitwise.
- **Label**: hay bandeja de demos y lanzamientos; no hay tracks, versiones ni metadata.
- **Dirección**: no hay ninguna vista que conteste "cómo está cada unidad".

---

# 4 · QUÉ PROCESOS ESTÁN DESORDENADOS

Ordenados por lo que cuestan, no por lo que molestan.

### 4.1 Nadie es dueño de que el alumno vuelva a agendar

Es el desorden más caro. Hoy el sistema detecta al que no pagó, al que se dio de baja y al
que tiene un problema de plata. **No hay un responsable declarado de que un alumno que pagó
tome su próxima clase.** Por eso hay 14 alumnos activos sin fecha y tres que nunca vinieron:
no falló nadie, es que no es tarea de nadie.

### 4.2 El registro de lo que se habla no ocurre

`incidencia_eventos` tiene **cero filas**. Cada conversación de José con un alumno vive en
WhatsApp y en su cabeza. Mientras eso siga así, ninguna de las cuatro unidades puede tener
la propiedad que pediste: *que una persona nueva se incorpore leyendo el sistema.*

### 4.3 Cuatro personas operan por fuera

Annie, Lola, Pacha y quien maneja el chatbot. Diseño y marketing no tienen dónde recibir un
pedido ni dónde entregar. Lo que hacen se pide por WhatsApp y se entrega por Drive.

### 4.4 El escalamiento existe y nunca se usó

El circuito José → Luqui está construido y tiene cero uso real. No es un problema de
software.

### 4.5 Dirección no tiene ritual, sólo tiene acceso

Vlado es maestro y no entró nunca. "Ver todo" no es un rol: sin una reunión con una agenda
fija y un lugar donde queden las decisiones, el acceso total se convierte en no mirar nada.

---

# 5 · QUÉ DEBERÍA CAMBIAR

Cada cambio contesta las cuatro preguntas que pediste. Los ordené por plata.

### Cambio 1 — Un dueño para la retención

| | |
|---|---|
| Qué problema resuelve | 14 alumnos activos sin próxima clase; 3 que nunca tomaron ninguna |
| Quién lo usa | José, todos los días |
| Frecuencia | Diaria |
| Si no existe | Se siguen yendo callados. Julio ya tuvo 27 bajas |

**No es software todavía.** Es una decisión: *"que cada alumno activo tenga su próxima clase
agendada es trabajo de José, y se mide todos los días."* Si después de dos semanas eso se
hace y se nota, entonces sí vale una tarea en el escritorio.

Arrancar hoy a mano con los 14 nombres, que ya están identificados.

### Cambio 2 — Cerrar el circuito de las 8 preguntas

| | |
|---|---|
| Qué problema resuelve | El escalamiento existe y nadie lo usó nunca |
| Quién lo usa | José y Luqui |
| Frecuencia | Vencen el 07 y 08/08 |
| Si no existe | El 18/08 no vamos a saber si el sistema no sirve o si nadie lo abrió |

Cuesta cero. Es el experimento más barato disponible y es el que decide todo lo demás.

### Cambio 3 — Dar de alta a las cuatro personas que faltan

| | |
|---|---|
| Qué problema resuelve | Diseño, marketing y chatbot operan sin registro |
| Quién lo usa | Annie, Lola, Pacha, la persona del chatbot |
| Frecuencia | Semanal |
| Si no existe | Si alguno se va, no queda rastro de qué hacía ni cómo |

Empezar por lo más chico: una cuenta y el permiso mínimo. No hace falta un módulo de diseño.

### Cambio 4 — Arreglar las tres fichas mal cargadas

Guini y Valen sin permisos, Valen con nombre de artista, Lanfran mal clasificado, y Facu
sin fila en `staff`. Es media hora y saca cuatro mentiras del organigrama.

### Cambio 5 — Recién acá, el CRM de leads externos

| | |
|---|---|
| Qué problema resuelve | Los leads de WhatsApp e Instagram no tienen dónde anotarse |
| Quién lo usa | José |
| Frecuencia | Depende de cuántos lleguen — **y eso no lo sabemos** |
| Si no existe | Se pierden contactos, en cantidad desconocida |

Va quinto y no primero por una razón: es el único de los cinco cuya frecuencia de uso no
podemos contestar. Eso se contesta mirando a José una mañana, y esa mañana ya está
planificada.

---

# 6 · QUÉ NO TOCAR

| No tocar | Por qué |
|---|---|
| Mercado Pago, webhook, créditos, acreditación | Sano y con plata real. Módulo congelado por decisión previa |
| El panel de profesores | Anda y lo usan |
| El motor de cola (`lib/workflows.ts`) | Es el mejor activo del sistema. Se le agregan tareas, no se rediseña |
| El modelo de casos (`lib/casos.ts`) | Seis estados que ya funcionan. **No superponerle un embudo nuevo** |
| Los permisos | Son la única reja real. Los roles con nombre se apoyan encima, no los reemplazan |
| El Libro anterior al 14/07/2026 | 195 renglones sin confirmar son historia archivada, no deuda. Desde el corte hay 10 |
| `unassigned_payments` | Los 30 "sin asignar" están en `ignored`: ya se triaron. **No hay backlog. Verificado — la alarma era falsa** |

---

# 7 · LAS CUATRO UNIDADES

## 7.1 Academy

**Está viva y es la única que produce.** El orden que le falta no es de software:

- Responsable de **venta** → José. Ya está.
- Responsable de **cobro** → Luqui. Ya está.
- Responsable de **que el alumno vuelva** → **hoy nadie.** Es el hueco.
- Responsable de **que el profesor tenga agenda** → hoy José y Pastrana, para tres profes.

Regla que propongo, en una línea: **cada alumno activo tiene una próxima fecha, o tiene un
motivo escrito de por qué no.** Es la única métrica de Academy que hace falta al principio.

## 7.2 Dominé

**No construir, y coincido.** Pero sí definir ahora dos cosas que no cuestan nada y después
cuestan caro:

1. **Qué es un evento cerrado.** Un evento termina cuando su resultado está calculado y los
   cuatro socios lo vieron. Sin esa definición, el Splitwise reparte sobre números en
   discusión.
2. **Quién paga qué, por defecto.** El Splitwise ordena lo que ya pasó; si no hay una regla
   previa de quién adelanta, el sistema sólo documenta el desorden más rápido.

Los porcentajes (35/35/15/15) van en configuración, no en la base: cambian por acuerdo entre
socios, no por transacción.

## 7.3 Label

Tu flujo de siete estados contra lo que ya existe:

| Tu estado | Hoy |
|---|---|
| Recibido | Existe |
| En revisión | Existe |
| Seleccionado | Existe |
| **Producción** | **Falta** |
| **Aprobado** | **Falta** |
| Lanzado | Existe, como release publicado |
| Rechazado | Existe |

Faltan dos estados y el vínculo demo → release. Es poco trabajo.

**Coincido en que los archivos van a Drive.** Y agrego la regla que lo hace funcionar: *el
sistema guarda el link, Drive guarda el archivo, y el link vive en la ficha de la demo — no
en un chat.* Sin eso, "está en Drive" significa "está en el Drive de alguien".

Advertencia: `label_demos` tiene **cero filas**. El sello salió ayer, así que es esperable —
pero ordenar un flujo que todavía no recibió su primera demo es diseñar sin evidencia. Yo
esperaría a las primeras diez.

## 7.4 Empresa

Lo que falta acá no es un dashboard: es un **ritual**. Un tablero sin reunión se mira dos
semanas y después no.

Propongo lo mínimo que se sostiene solo:

- **Una reunión quincenal, Facu y Vlado, 30 minutos**, con agenda fija: cómo está cada
  unidad, qué problema está sin dueño, qué decisión está trabada.
- **Cuatro métricas, ni una más.** Alumnos activos · alumnos con próxima clase agendada ·
  ventas del mes · problemas abiertos sin responsable.
- **Las decisiones se escriben donde se toman.** Si una decisión de esa reunión no queda
  escrita en el sistema, la reunión no ocurrió.

La segunda métrica es la nueva y es la que importa: hoy daría **11 de 25**.

El dashboard de Dirección se construye **después** de que la reunión exista y haya pedido
algo. Al revés, es una pantalla más que nadie abre — que es exactamente el problema que
tenemos.

---

# 8 · EL ORDEN QUE PROPONGO

Cambia el tuyo en un punto: la retención entra antes que el CRM.

| | Qué | Cuándo | Es software |
|---|---|---|---|
| 0 | Contestar las 8 preguntas escaladas | 07–08/08 | No |
| 0 | Escribirle a los 14 sin próxima clase, y a los 3 que nunca vinieron | Esta semana | No |
| 0 | Las dos mañanas mirando a José y a Luqui | Antes del 18/08 | No |
| 1 | Arreglar las fichas mal cargadas del equipo | 30 min | Mínimo |
| 2 | Alta de Annie, Lola, Pacha y chatbot | 1 día | Mínimo |
| 3 | Retención como tarea con dueño, en el escritorio | Después del 18/08 | Sí |
| 4 | CRM de leads externos | Después de la mañana con José | Sí |
| 5 | Ritual de Dirección, después su tablero | Septiembre | Primero no |
| 6 | Label: los dos estados que faltan | Cuando haya 10 demos reales | Sí |
| 7 | Dominé | Cuando haya un evento | Sí |

**Nada de lo que está en los puestos 0 cuesta una línea de código, y son los cuatro que más
plata mueven.**

---

# 9 · LO QUE NECESITO DE VOS

1. **Lanfran: ¿da clases o no?** Cambia su alta.
2. **La persona del chatbot: ¿cómo se llama y qué hace exactamente?** Es la única de las
   doce que no tiene ni nombre acá.
3. **Los 3 que nunca tomaron clase** (Pacino, Toninelli, Fernández López): ¿los conocés?
   ¿Pasó algo o simplemente nadie los llamó?
4. **Las 27 bajas de julio:** ¿son bajas reales o quedaron de la migración del 14/07?
   Cambia si el problema de retención es nuevo o viene de antes.
