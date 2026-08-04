# El Sistema Operativo de José

`v2 · 04/08/2026` · Auditoría pantalla por pantalla del back office de Astronomy Academy,
desde una sola pregunta: **¿esto la ayuda a hacer su trabajo, o le da software para explorar?**

---

> ## El norte
>
> **Astronomy no es un panel de administración. Es el sistema operativo de trabajo del
> equipo.**
>
> Cada persona entra al sistema para hacer su trabajo, no para administrar información. El
> sistema debe transformar responsabilidades en tareas concretas, guiarlas paso a paso y
> llevar automáticamente al usuario hasta completarlas.
>
> **Si el usuario tiene que decidir qué hacer después, el diseño falló.**
>
> — Facu, 04/08/2026. Está también en el `CLAUDE.md` del repo, que se carga en toda sesión.

**José no usa un sistema: José recibe trabajo.** De ahí salen las tres reglas que gobiernan
todo lo de abajo:

| | |
|---|---|
| **El objeto es el trabajo, no el alumno** | `Trabajo → Objetivo → Casos → Resolver → Terminado`. Contactar alumnos, pagar sueldos, conciliar Mercado Pago y cargar efectivo tienen todos esa forma |
| **"Workflow" es una palabra nuestra** | En el código, `Workflow`. En la pantalla, **tarea**: *"Tarea 2 de 4"*, nunca *"workflow de recuperación de cobranzas"* |
| **Nada de tiempo en pantalla** | "≈27 min" sirve para decidir si vale la pena construir algo. A quien viene a trabajar sólo le pone un cronómetro adelante |

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra el código o la base el 04/08/2026. Reproducible. |
| **[INFERENCIA]** | Calculado desde hechos. Los supuestos van escritos. |
| **[OPINIÓN]** | Mi juicio. Discutible. |

---

## 0. Qué se construyó hoy, antes de la crítica

Está en producción. Para que la auditoría se lea contra lo que hay, no contra lo que había.

| | Antes | Ahora |
|---|---|---|
| `/admin` | 623 líneas: 4 estadísticas, 3 tarjetas de alerta, 20 links en 4 cajas, avisos, accesos compartidos, postulaciones, bajas, equipo | Una lista de tareas. Nada más. |
| El resto | Delante del trabajo | `/admin/herramientas`, entero y sin cambios |
| El motor | `lib/tareasHoy.ts`, 3 trabajos, el ítem era siempre una persona | `lib/workflows.ts`, 7 trabajos, y el caso puede ser una persona **o un problema** |
| Quién ve qué | José, Luqui y Facu veían lo mismo | Cada workflow declara su permiso |

**[HECHO] Verificado corriendo el motor real contra la base** (`npm run ver:workflows`):

| Quién | Tareas | Casos | Plata |
|---|---|---|---|
| Facu (maestro) | 6 | 11 | $1.092.899 |
| **José** | **5** | **10** | **$1.092.899** |
| Luqui | 6 | 11 | $1.092.899 |
| Mateo (profe) | 0 | 0 | — |

Los sueldos no le aparecen a José y sí a Luqui, sin una línea de lógica de roles: sale del
permiso `view_salaries`, que ella no tiene.

**Lo que el motor encontró y no estaba en ninguna pantalla: [HECHO] 3 alumnos que no
pagaron agosto — $430.560.** Aracely Juarez, Rochi Mounier y Martín Cañeque. Vivían en una
tabla de `/admin/cobros-mes` que había que acordarse de abrir.

---

## 1. Pantalla por pantalla

Para cada una: **qué trabajo humano intenta resolver** (no qué muestra), si José lo termina
ahí, y qué haría.

### Las tres del escritorio

#### `/admin` — el Home
**El trabajo:** que José sepa qué hacer sin preguntárselo a nadie.
**Bien:** ya no contiene lógica. Pide las tareas, las ordena por urgencia y plata, y las
renderiza. Un trabajo nuevo aparece solo. No muestra tiempo ni montos: acá sólo se elige
por dónde empezar, y ese orden ya lo resolvió el motor.
**Mal:** [OPINIÓN] el estado vacío ("Terminaste por hoy") todavía no se ganó nunca. Hasta
que José lo vea una vez, no sabemos si la lista es alcanzable o es un reproche permanente.
**Prioridad:** — · **Tiempo:** hecho · **Impacto:** es el único punto de entrada.

#### `/admin/hacer/[id]` — la cola
**El trabajo:** ejecutar sin decidir. Un caso, una acción, el siguiente.
**Bien:** no hay menú, ni tabla, ni filtros. Dice "Tarea 2 de 5" y al terminar ofrece la
que sigue: José nunca vuelve al índice a elegir.
**Mal:** [OPINIÓN] **para los casos que se resuelven en otra pantalla, la cola se rompe.**
José hace click en "Buscar de quién es", cae en `/admin/pagos-sin-asignar`, resuelve, y
tiene que volver sola. Es el único lugar donde el asistente la suelta.
**Qué construiría:** que la pantalla de destino, al resolver, vuelva a la cola en vez de a
sí misma. **Tiempo: 1 h.** **Prioridad: media** — hoy es 1 caso de ese tipo.

#### `/admin/herramientas` — todo lo demás
**El trabajo:** que exista lo que se usa una vez por semana, sin que esté delante de lo que
se usa todos los días.
**Bien:** José pasó de 20 accesos a 15, en 3 grupos ordenados por lo que está haciendo.
**Mal:** [OPINIÓN] 15 sigue siendo mucho. La mitad de abajo es honestamente inspección.

### Las que José usa de verdad

| Pantalla | El trabajo humano | ¿Termina ahí? | Veredicto |
|---|---|---|---|
| **`/admin/alumnos/[id]`** | Mirar a alguien antes de escribirle o corregirle algo | **No** — [HECHO] no tiene botón de WhatsApp | **Es la pantalla más importante que le queda.** Construir el botón: el componente ya existe (`waWebLink` + `VencidoActions`). **30 min · alto impacto** |
| **`/admin/carga-manual`** | Que un pago quede registrado Y acredite créditos | Sí | **Se queda y sube de rango.** Es lo único que acredita: el Google Form no |
| **`/admin/pagos-sin-asignar`** | Saber de quién es una plata que entró | Sí | **Se queda.** Ya ordena por candidatos y guarda el alias |
| **`/admin/auditoria-creditos`** | ¿El saldo que ve el alumno es el que pagó? | Sí | **Se queda, y ahora dice la verdad**: dejó de contar premios, compras sueltas y devoluciones como diferencias. De 9 falsos positivos a 1 caso real |
| **`/admin/cobros-mes`** | Quién debe la cuota | Sí | **Se queda**, pero degradada: su trabajo ya entra como workflow. Queda para consultar |
| **`/admin/agenda-manual`** | Agendar una clase por ella | Sí | **Se queda.** Es la acción que cierra la mitad de sus conversaciones |
| **`/admin/usuarios`** | Encontrar a alguien | Sí | **Se queda.** Es el buscador |
| **`/admin/libro`** | ¿Cómo venimos? | Sí | **Se queda.** Lectura, no trabajo |

### Las que sobran

| Pantalla | Por qué sobra | Qué haría |
|---|---|---|
| **`/admin/revisar`** | 11 contadores de problemas ajenos. Nadie es dueño de ninguno | **Ya no la ve José.** Sus chequeos van pasando a workflows |
| **`/admin/conciliacion`** | 11 chequeos contra MP en vivo. Son de sistema, no de operación | **Ya no la ve José.** Es de Facu |
| **`/admin/registro`** | Describe y resuelve problemas de plata | **Ya no la ve José.** El workflow la lleva directo al caso |
| **`/admin/growth`** | Embudo + a quién llamar hoy | **Se solapa con el Home.** "A quién llamar" ahora es el panel. Lo demás es lectura de Facu |
| **`/admin/finanzas`** (no-master) | Muestra "estado operativo" sin montos = duplica `revisar` | **Borrar esa rama.** ~40 líneas muertas. **20 min** |
| **`/admin/postulaciones`** | [HECHO] 3 filas | **Borrar la pantalla**, el desplegable de Herramientas ya la muestra. **20 min** |
| **`/admin/eventos`** (ticketera) | [HECHO] 0 órdenes | **Sacar del menú.** Ya sólo la ve el maestro |
| **`/admin/ingresos`**, **`/admin/egresos`** | Ya son redirects | Nada |

**[INFERENCIA] Total a borrar: ~1 hora de trabajo, cero riesgo, y el sistema pasa de 26
pantallas a 21.**

---

## 2. ¿Es sobreingeniería? — la pregunta que pediste que conteste sin darte la razón

**No, y por una razón concreta: no se construyó infraestructura.** [HECHO] El "motor" son
siete consultas, un `filter` y un `sort`. No hay tabla de definiciones, ni editor, ni
prioridades configurables, ni dependencias entre tareas. El tipo `Workflow` reemplazó a
tres tipos que ya existían y decían lo mismo con otro nombre.

**Pero hay una decisión ahí que sí me la jugué y podría estar mal**, y prefiero escribirla
antes de que se note sola:

> Los ítems que se resuelven en otra pantalla **no llevan registro**. Desaparecen porque el
> dato cambió, no porque alguien apretó "listo". Eso hace imposible que la lista mienta —
> pero también hace imposible saber **cuánto tardó** José en resolver uno, o si lo intentó
> y no pudo. Si dentro de un mes querés medir su trabajo, ahí va a faltar el dato.
> **[OPINIÓN] Lo elegí igual: una lista que no puede mentir vale más que una métrica.**

### Lo que sí es riesgo real

**[HECHO] `contact_log` tiene 0 filas.** La cola se puso en producción el 04/08 y **nadie
la usó todavía ni una vez.** Todo lo de arriba está construido sobre la hipótesis de que
José va a trabajar así. **Si no la usa dos semanas, esto fue decoración cara.**

Y hay un hallazgo que me incomoda más:

> **[HECHO] El workflow de créditos nació vacío — y la causa era que el detector estaba
> roto.** De 26 alumnos auditados daba: 0 con crédito faltante, 0 con pago sin producto,
> **9 con créditos de más**.
>
> **[HECHO] Los 9 eran falsos positivos.** `auditarCreditos` comparaba el saldo real contra
> *"lo que otorga el plan del último pago"* y nada más, así que todo lo que entra por otra
> puerta le daba diferencia: Christine +20 = dos premios de 10 · Fernando +20 = una compra
> suelta · Guadalupe +120 = 60 comprados y 60 de premios · Rochi +60 = la devolución de una
> clase cancelada.
>
> **[INFERENCIA] Y eso no era sólo ruido: podía tapar el caso que buscábamos.** A un alumno
> con premios al que ADEMÁS le faltan créditos del plan, las dos cosas se le cancelan y
> queda invisible. **El cero no probaba que no hubiera problema: probaba que el detector no
> podía verlo.**
>
> **Arreglado el 04/08** (`esperado` ahora suma los lotes `premio:`, `buy:` y `refund:`;
> `manual:` y `admin:` no, porque ésos son la corrección de una falta). **[HECHO] 9
> diferencias → 1, y la que queda es real:** a Tomás Álvarez el Libro le anota Curso de DJ
> y Mercado Pago le cobra Silver — 250 créditos a dos meses en vez de 240 a uno, con lo
> cual su vencimiento real es el 01/10 y no el 01/08. Mismo precio, distinto producto.

---

## 3. El hueco que ninguna pantalla tapa

**[HECHO] El 100% de la conversación comercial de José pasa fuera del sistema.** Los leads
hablan por WhatsApp y no existe una sola fila que los represente. El embudo de la app
arranca cuando alguien **ya creó la cuenta dentro del flujo de compra** — es decir, cuando
la venta casi está hecha.

**[INFERENCIA] Todo lo que construí hoy opera sobre 23 alumnos que ya pagaron. El trabajo
de José que mueve la aguja ocurre antes, con gente que el sistema no sabe que existe.**

Y esto **no se arregla con software**: se arregla etiquetando WhatsApp dos semanas a mano,
que es exactamente lo que dice el Sprint 2 del `OS_CRECIMIENTO.md`. Construir un CRM para
esto ahora sería construir la casa antes de saber dónde da el sol.

---

## 4. Roadmap, por impacto

| # | Qué | Impacto | Tiempo | Por qué en ese orden |
|---|---|---|---|---|
| 1 | **Que José use la cola dos semanas** | Cobranza + retención · $1.092.899 en pantalla | **0 hs** | Es lo único que valida todo lo demás. No hay nada que construir |
| 2 | **Resolver el caso de Tomás Álvarez**: ¿Curso de DJ o Silver? | Define si sus créditos vencen el 01/08 o el 01/10 | **5 min** | Ya está en el panel como caso, con la ficha a un click |
| 3 | **Botón de WhatsApp en la ficha del alumno** | Le saca un copiar-pegar por conversación | **30 min** | El componente ya existe, se copia |
| 4 | **Que la pantalla de destino vuelva a la cola** | Cierra el único lugar donde el asistente la suelta | **1 h** | Hoy son 0 ítems: no urge |
| 5 | **Borrar lo muerto** (finanzas no-master, postulaciones, ticketera) | Menos superficie que mantener | **1 h** | Barato y no rompe nada |
| 6 | **Guardar `utm_source`/`referrer` al crear la cuenta** | Habilita saber de dónde viene cada venta | **30 min** | Sin esto la pauta se decide a ciegas |
| 7 | **Etiquetar WhatsApp a mano, 2 semanas** | Es el 100% del trabajo comercial invisible | **10 hs de José** | Sprint 2. **No es software** |
| 8 | **El OS de Luqui** | Que no quede un peso sin explicar | Ver `OS_WORKFLOWS.md` | Depende de que la plata entre a la app primero |

**[OPINIÓN] Del 1 al 3 son 32 minutos de desarrollo. Todo lo demás puede esperar a que
alguien haya usado esto una semana.**

---

## 5. La pregunta

> *¿Estamos construyendo software que ayuda a José a trabajar mejor, o software por el
> simple hecho de construir?*

**Hasta esta mañana: las dos cosas, y la segunda ganaba.** No es una opinión blanda, tiene
evidencia:

- [HECHO] `/admin` dedicaba su mejor lugar a cuatro estadísticas. Nadie hace nada distinto
  porque el número diga 51 o 52.
- [HECHO] Había **tres tipos de dato distintos** describiendo el mismo concepto y **22
  detectores de problemas repartidos en dos pantallas** que nadie abría.
- [HECHO] Existían dos motores separados detectando cobros duplicados, que pueden discrepar
  sin que nadie se entere.
- [HECHO] `/admin/eventos` tiene 0 órdenes. `/admin/postulaciones`, 3 filas. `expenses`, 0.
- [HECHO] Y mientras tanto, **3 alumnos que no pagaron agosto por $430.560 no aparecían en
  ninguna pantalla que alguien fuera a abrir.**

Eso es la definición de construir por construir: mucha superficie, poca cobranza.

**Desde hoy, la balanza se dio vuelta — pero todavía no está ganada.** Lo que se construyó
no agregó capacidades: sacó duplicación, mudó ruido y puso adelante trabajo que ya se sabía
hacer. Eso es lo más parecido a "software que ayuda" que se puede escribir sin haber visto
a la persona usarlo.

**La respuesta definitiva no la da este documento: la da `contact_log`.** Si en dos semanas
tiene filas, construimos bien. Si sigue en cero, construimos para nosotros — y entonces el
próximo paso no es una pantalla más, es sentarse al lado de José una mañana y mirar qué
hace en vez de suponerlo.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08 | v1 — auditoría del back office + el escritorio de José en producción | Pedido de Facu |
| 04/08 | v2 — el norte arriba · fuera el tiempo y la palabra "workflow" de la interfaz · `ítems` → `casos` | *"José no usa un sistema: José recibe trabajo"* |
| 04/08 | v2 — **la auditoría de créditos estaba rota**: 9 diferencias eran premios, compras y devoluciones. Arreglada, quedó 1 y es real | Salió de contestar *"¿por qué preguntás?"* |
