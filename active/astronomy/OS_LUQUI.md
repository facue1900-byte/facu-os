# El Sistema Operativo de Luqui

`v2 · 04/08/2026` · **Documento de análisis. No hay una línea de código acá.**
Recorrido completo del sistema financiero de Astronomy — código y base — para contestar una
sola pregunta: *¿qué trabajo hace Luqui, y qué parte de ese trabajo el sistema puede ver?*

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra el código, la base o la planilla el 04/08/2026. Reproducible. |
| **[INFERENCIA]** | Calculado desde hechos. Los supuestos van escritos. |
| **[OPINIÓN]** | Mi juicio. Discutible. |

---

## 0. Las leyes, reconciliadas

Tu último mensaje trae seis leyes; el repo tenía cinco, y no son la misma lista. Las junto
acá para que exista **un solo juego**, y las numero por orden de importancia, no de
aparición. Las dos nuevas están marcadas.

| | Ley | Estado |
|---|---|---|
| **1** | Cada tarea tiene **un único dueño**. Nunca dos, nunca nadie | En código, obligatorio |
| **2** | Una tarea desaparece **sólo porque fue resuelta**, nunca porque pasó el tiempo | En código — **faltaba escribirla** |
| **3** | Toda tarea contesta: *¿por qué apareció? · ¿cuándo termina? · ¿qué pasa si no hago nada?* | En código, obligatorio |
| **4** | Sólo existe **una tarea activa**. Las demás están En espera y no se pueden abrir | En producción |
| **5** | Al terminar, el sistema **continúa solo** con la siguiente. Nunca vuelve al Home | En producción |
| **6** | El sistema **nunca muestra información que no termine en una acción** | En producción |
| **7** | El Home **jamás cambia** cuando aparece un trabajo nuevo: consume una tarea más | En código — **faltaba escribirla** |

**[HECHO] La 2 y la 7 ya se cumplen, sólo no estaban escritas.** La 2 vive en `historial()`:
cada resolución declara su `tipo` (`cierra`, `reintenta`, `pospone`, `descarta`) y el motor
lo aplica; con `reintenta` el tiempo **trae de vuelta** la tarea en vez de borrarla. La 7 es
por qué el Home tiene 140 líneas: pide la lista y la renderiza.

---

## 1. Lo que recorrí

**Código:** `lib/` → `finanzas.ts` · `ingresos.ts` · `egresos.ts` · `salaries.ts` ·
`pagos.ts` · `payments.ts` · `conciliacion.ts` · `registroIngresos.ts` ·
`auditoriaCreditos.ts` · `historico.ts` · `syncSheet.ts` · `workflows.ts`.
**Acciones:** `cargaManual` · `egresos` · `pagosSinAsignar` · `atribuirPago` ·
`incidencias` · `salaries` · `conciliacion`.
**Rutas:** `/api/mp/webhook` · `/api/cron/sync-sheet`.
**Pantallas:** libro · registro · revisar · conciliación · finanzas · carga-manual ·
pagos-sin-asignar · pagos-sin-atribuir · auditoria-creditos · cobros-mes · sueldos.
**Base:** las 10 tablas donde vive plata, más la planilla `Finanzas - Astronomy Academy`
leída en vivo.

### El inventario de la plata, medido

| Tabla | Filas | Desde | Hasta | Quién la escribe |
|---|---|---|---|---|
| `sales` | 52 | 02/06/26 | **04/08/26** | El webhook de MP y el puente horario. **Sola** |
| `payment_events` | 5 | 14/07/26 | 04/08/26 | El webhook. **Sola** |
| `unassigned_payments` | 38 | 18/04/26 | 17/07/26 | El webhook cuando no puede atribuir. **Sola** |
| `manual_payments` | **3** | 30/07/26 | 04/08/26 | **Una persona**, desde `/admin/carga-manual` |
| `expenses` | **0** | — | — | **Una persona**, desde `/admin/libro`. **Nunca se usó** |
| `salary_payments` | **3** | 01/07/26 | 01/07/26 | Una persona, al marcar pagado en `/admin/sueldos` |
| `staff_payments` | **0** | — | — | Ídem. **Nunca se usó** |
| `payment_links` | 614 | 08/02/24 | **24/07/26** | El cron, desde la planilla. **Parado** |
| `ledger_aliases` | 66 | — | — | Una persona, al atribuir un pago |
| `incidencias` | **0** | — | — | Una persona, al marcar un problema resuelto |

**La lectura de esa tabla es todo el diagnóstico: las cuatro tablas que se escriben solas
están al día; las cinco que dependen de una persona están vacías o paradas.**

---

## 2. El hallazgo que cambia la prioridad de todo

**[HECHO] `CUTOVER_ISO = "2026-08-01T03:00:00.000Z"`** (`lib/finanzas.ts`). Desde el 1 de
agosto —hace cuatro días— **la fuente de verdad de las finanzas dejó de ser la planilla y
pasó a ser la app.** Antes de esa fecha, el tablero lee el histórico congelado; desde ahí,
lee `sales`, `manual_payments`, `expenses`, `salary_payments`, `staff_payments` y `mp_fee`.

**[HECHO] Esto es lo que la app tiene de agosto:**

| | Filas | Monto |
|---|---|---|
| Ingresos · `sales` | 9 | $998.293 |
| Ingresos · `manual_payments` | 1 | $5.000 |
| **Egresos · `expenses`** | **0** | **$0** |
| **Egresos · sueldos de profes** | **0** | **$0** |
| **Egresos · sueldos del equipo** | **0** | **$0** |
| Egresos · comisión de Mercado Pago | 9 | $81.883 |
| | | **Resultado que muestra: +$921.410** |

**[INFERENCIA] Ese +$921.410 no existe.** El único egreso que el sistema conoce de agosto es
la comisión de MP, que se registra sola. El promedio de egresos de enero a junio es
**$2.950.801/mes**; con cuatro días corridos ya deberían figurar del orden de $380.000, y
figuran cero. El supuesto es que agosto gasta como el promedio del semestre.

> **[OPINIÓN] El corte pasó y del lado nuevo no hay nadie cargando.** No es que falte una
> pantalla: `/admin/libro` tiene el formulario de egresos, funciona, y **Luqui tiene el
> permiso** (`view_salaries`). Lo que falta es que algo le diga que le toca. Ése es
> exactamente el trabajo de un escritorio.

### Y el lado viejo también se apagó

**[HECHO] La planilla no tiene una fila desde el 24/07** — leída hoy con la service account:
1.133 filas, la última *"Matilda Goldy - Silver Member - Agosto 2026"*. **No es el sync:**
`payment_links` no tiene **ni una** fila escrita por el cron; sus 614 son la importación del
24/07 más una fila cargada a mano hoy. No hay nada que traer.

**[HECHO] Parte del hueco de julio es una convención, no un olvido:** los sueldos de julio
se cargan a principio de agosto con fecha de julio, porque se pagan recién ahí (dicho por
vos el 31/07). Estamos en esa ventana. **Lo que la convención no explica:** que los
*ingresos* también estén parados, y que agosto tenga 1 ingreso en la planilla contra 9
ventas en la app.

**Quedó un hueco de once días entre las dos fuentes: la vieja dejó de cargarse el 24/07 y la
nueva empieza el 01/08. Del 25 al 31 de julio no hay nada en ningún lado.**

---

## 3. Qué trabajo hace realmente Luqui

No pantallas. Responsabilidades.

### R1 · Hacer que todo el dinero que entró exista en el sistema
Mercado Pago se registra solo. **Todo lo demás depende de él**: efectivo, transferencias,
clases de prueba, y cualquier cobro que no haya pasado por MP. Si no lo carga, ese dinero
**no existe para nadie** — ni para el margen, ni para el alumno, que además se queda sin
sus créditos.

### R2 · Hacer que todos los gastos reales existan en el sistema
Es la mitad que nadie automatiza y la que más pesa: **[HECHO] los sueldos fueron el 72% de
los egresos de junio.** Es la única responsabilidad cuyo incumplimiento hace que el negocio
**parezca mejor de lo que es**.

### R3 · Asegurar que ningún peso que entró quede sin dueño
Cuando MP cobra con un mail que no reconocemos, la plata entra y **el alumno no recibe nada**.
Hasta que alguien decide de quién es, hay una persona que pagó y está esperando.

### R4 · Garantizar que el dinero real coincida con el registrado
La pregunta de una línea: *¿la plata que hay es la que decimos que hay?* Hoy **nadie la
puede contestar** — ver la sección 5.

### R5 · Que nadie del equipo se quede sin cobrar
Del 1 al 5, el mes anterior. Es la única responsabilidad donde **el perjudicado es de casa**.

### R6 · Que el número que mira Facu sea el real
No es una responsabilidad aparte: es **la consecuencia** de R1 + R2 + R4. La escribo porque
es la razón por la que las otras importan, no porque genere trabajo propio.

> **Corrección a tu lista de siete.** *"Verificar que todo lo que entró esté registrado"* y
> *"verificar que todo lo registrado exista"* son **las dos direcciones de R1 y R4**, y
> ninguna de las dos es trabajo diario: son el resultado. Convertirlas en tareas propias
> haría que Luqui abra una pantalla "a verificar" sin nada concreto para hacer — que es
> exactamente el panel de administración del que venimos.

---

## 4. Las tareas que salen de eso

### Ya existen y funcionan

| Tarea | Responsabilidad | Casos | Estado |
|---|---|---|---|
| **Encontrar el dueño de N pagos** | R3 | `unassigned_payments` en `pending` | **Viva.** Hoy son 0 casos, así que no aparece — correcto |
| **Pagar los sueldos de \<mes\>** | R5 | El período sin liquidar | **Viva ahora mismo** en su escritorio |

**[HECHO] Su escritorio hoy muestra 1 tarea.** No es un bug: es el diagnóstico. Cuatro de
sus seis responsabilidades no pueden convertirse en tarea todavía.

### Faltan, y se pueden construir ya

| Tarea | Responsabilidad | Qué la dispara |
|---|---|---|
| **Cargar los movimientos de hoy** | R1 | El día. Efectivo, transferencias y clases de prueba |
| **Cargar los gastos de hoy** | R2 | El día |
| **Cerrar julio** *(una vez)* | R1+R2 | El hueco del 25 al 31/07, que no está en ninguna fuente |

### Faltan y NO se pueden construir todavía

| Tarea | Por qué no |
|---|---|
| **Cerrar la caja** | No existe ningún saldo real contra el cual comparar. Ver sección 5 |
| **Conciliar el banco** | No existe **nada** bancario en el sistema: ni cuenta, ni saldo, ni movimiento |

---

## 5. El dato que falta, y por qué su ausencia impide la tarea

Pediste que si una tarea no puede existir, explique primero el dato que falta. Es una sola,
y es la más importante de las que no existen.

### "Cerrar la caja" no se puede construir hoy

**Conciliar es comparar dos números.** El sistema tiene el primero —lo que dice haber
cobrado— y **no tiene el segundo.**

**[HECHO] En las 10 tablas de plata no hay ningún saldo.** `sales` dice *cuánto se cobró*,
no *cuánta plata hay*. No existe el saldo de Mercado Pago, ni el efectivo en la caja, ni
nada bancario. Un pago registrado dos veces, un cobro que MP devolvió, o un billete que
salió del cajón **son todos invisibles**, porque el sistema sólo conoce el lado que él mismo
escribió.

**Por qué eso impide automatizar el trabajo:** no es que el cálculo sea difícil — es que
falta un operando. Cualquier pantalla de "conciliación" que se construya hoy sólo puede
comparar el sistema **contra sí mismo**, y eso siempre cierra. Sería una tarjeta verde
permanente: la peor clase de mentira, porque tranquiliza.

### El cambio mínimo para que exista

**Un saldo declarado.** Nada más. Luqui abre la app de Mercado Pago, mira el número y lo
escribe; cuenta el efectivo del cajón y lo escribe. Dos campos y una fecha.

Con eso —y sólo con eso— el sistema puede decir *"faltan $12.500"* en vez de mostrar una
tabla. **[OPINIÓN] Es la única pieza de datos genuinamente nueva de todo este documento.**

> **Y va DESPUÉS de R1 y R2, no antes.** Si se construye primero, la diferencia va a ser de
> millones todos los días —porque faltan los movimientos, no porque falte plata— y la
> tarjeta se deja de mirar en una semana.

---

## 6. El tipo de tarea que José no tiene

Todas las tareas de José nacen de **evidencia**: el sistema ve un dato y arma el caso. Las
tareas de R1, R2 y R4 **no pueden nacer así**, porque su disparador ocurre *fuera* del
sistema: un billete, una transferencia, un gasto. Nadie se lo va a contar.

**[OPINIÓN] Nacen de un ritmo, y hay que llamarlas por su nombre** en vez de disfrazarlas
de evidencia:

| | Tarea de evidencia | Tarea de ritmo |
|---|---|---|
| Aparece porque | el sistema encontró algo | pasó el tiempo |
| Se cierra porque | el dato cambió | **una persona declaró** que no hay nada |
| ¿Puede mentir? | No | **Sí**, y hay que asumirlo |
| Ejemplos | las 5 de José, sueldos, pagos sin dueño | cargar movimientos, cerrar la caja |

**Esto choca de frente con la Ley 2** (*una tarea desaparece sólo porque fue resuelta*).
Una tarea de ritmo desaparece porque alguien dijo *"no hubo nada"*, y puede equivocarse o
mentir. **No conozco forma de evitarlo**, y prefiero decirlo antes que fingir que el sistema
puede saber lo que no puede.

Lo que sí se puede es que **mentir cueste**:

1. Declarar *"no hubo movimientos"* es **explícito**, un botón aparte, y queda registrado
   con nombre y fecha.
2. **Tres días seguidos sin una sola carga vuelven como problema.** [HECHO] Ese chequeo
   hubiera avisado el 27/07; nos enteramos el 04/08, y sólo porque alguien fue a mirar.

Cumple la Ley 3 sin esfuerzo:

> **Por qué apareció:** hoy todavía no cargaste los movimientos.
> **Termina cuando:** cargaste lo que hubo, o declaraste que no hubo nada.
> **Si no hago nada:** el mes queda a medias con cara de completo. Agosto muestra
> +$921.410 y el único egreso que conoce es la comisión de Mercado Pago.

---

## 7. Pantallas: qué se reutiliza, qué se va del camino

**No hay que construir ni una pantalla nueva salvo la del saldo declarado.** Todo lo que
Luqui necesita ya existe; lo que falta es que algo lo lleve hasta ahí.

### Se reutilizan tal cual — son el `resolver()` de sus tareas

| Pantalla | Para qué tarea | Por qué sirve como está |
|---|---|---|
| **`/admin/carga-manual`** | Cargar los movimientos | **Carga el pago Y acredita los créditos en el mismo acto.** El Google Form no hace lo segundo: es la causa escrita de que un alumno pague y quede sin nada |
| **`/admin/libro?ver=salio`** | Cargar los gastos | El formulario ya existe, con 8 categorías. Luqui **ya tiene el permiso** |
| **`/admin/pagos-sin-asignar`** | Pagos sin dueño | Ya ordena por candidatos y **guarda el alias**, así el mes que viene se atribuye solo |
| **`/admin/sueldos`** | Sueldos | Ya calcula profes y equipo, y registra el egreso al marcar pagado |
| **`/admin/registro`** | Diferencias entre fuentes | Cruza las 4 tablas de plata y trae el instructivo paso a paso |

### Pasan a ser herramientas internas (fuera del escritorio, Ley 6)

| Pantalla | Por qué |
|---|---|
| **`/admin/libro`** (modo consulta) | Contesta "cómo venimos". Es lectura, no trabajo |
| **`/admin/finanzas`** | El tablero del negocio, con gráficos y dolarización. **Es de Facu**, no de Luqui |
| **`/admin/conciliacion`** | 11 chequeos contra MP en vivo. Son de sistema: precios de links, planes sin mapear, webhooks |
| **`/admin/revisar`** | Índice de problemas ajenos. Sus chequeos van pasando a tareas con dueño |
| **`/admin/auditoria-creditos`** | Es de José |

### Ninguna se borra

**[OPINIÓN] Y quiero ser explícito con esto**, porque en el documento de José sí propuse
borrar tres. Acá no hay nada que sobre: el problema de Luqui **nunca fue tener pantallas de
más, fue no tener ninguna que le dijera qué hacer.**

---

## 8. Lo que NO hay que construir

| | Por qué |
|---|---|
| **Un módulo de conciliación bancaria** | No hay datos de banco y no está claro que hagan falta. Es una pregunta abierta, no un pendiente |
| **Un dashboard financiero para Luqui** | Ley 6. El resumen del mes es de Facu y ya existe |
| **Re-importar la planilla** | La planilla no es la fuente: es el síntoma. Si se arregla la carga, deja de hacer falta |
| **Automatizar la carga de efectivo** | No hay de dónde. Alguien tiene que decir que entró |
| **Una pantalla de "verificar"** | Verificar no es una acción. Es el resultado de cargar y conciliar |
| **Un OCR de comprobantes / IA que lea transferencias** | Son ~3 movimientos por día. El cuello es que nadie los carga, no cuánto cuesta cargarlos |

---

## 9. En qué orden, y qué mueve plata

| # | Qué | ¿Mueve plata? | Por qué va ahí |
|---|---|---|---|
| **0** | **Tapar el hueco del 25 al 31/07** (a mano, una vez) | **No** — pero sin esto julio no cierra nunca | Es la única semana que no está en ninguna de las dos fuentes |
| **1** | Tarea de ritmo **"Cargar los movimientos de hoy"** → `/admin/carga-manual` | **SÍ.** Un alumno que pagó y no tiene créditos reclama o se va | Sin esto todo lo demás mide sobre datos incompletos |
| **2** | Tarea de ritmo **"Cargar los gastos de hoy"** → `/admin/libro` | **No directamente** — ver abajo | Es el 72% de lo que falta |
| **3** | **Matar el Google Form** | **SÍ.** El Form no acredita créditos; la app sí | Mientras haya dos lugares para cargar, la mitad va al equivocado |
| **4** | **Alarma: tres días sin cargar** | No | Es el chequeo que hubiera avisado el 27/07 |
| **5** | **Saldo declarado + tarea "Cerrar la caja"** | **SÍ.** Es lo único que puede encontrar plata que falta de verdad | Recién con 1 y 2 la diferencia va a ser chica y la tarjeta va a servir |
| **6** | Banco | ¿? | Depende de tu respuesta |

### La distinción que pediste, dicha de frente

**[OPINIÓN] Casi nada del trabajo de Luqui mueve plata directamente, y eso no lo hace menos
importante — lo hace distinto.**

- **Mueven plata hoy:** los pagos sin dueño (hay alguien que pagó y está esperando) y los
  sueldos (hay alguien de casa que no cobró).
- **No mueve plata, pero la decide:** cargar ingresos y gastos. **Es lo único que hace que
  las decisiones que sí mueven plata se tomen sobre números reales.** Con agosto mostrando
  +$921.410 falso, cualquier decisión de subir pauta, bajar precio o contratar a alguien se
  toma sobre un número inventado — y ésas sí mueven millones.

**El trabajo de José hace entrar plata. El de Luqui hace que sepamos si entró.** Sin el
segundo, el primero se mide mal.

---

## 10. Lo que necesito de vos antes de construir

1. **¿El banco entra o no?** Cambia si son 2 tareas o 4. Hoy no existe **nada** bancario.
2. **¿Luqui carga en la app o sigue con el Google Form?** Si sigue el Form, la tarea 1 no se
   puede cerrar nunca dentro del sistema y todo esto queda a medias.
3. **¿Quién tapa el hueco del 25 al 31 de julio?** Son once días sin fuente. Si no, su
   escritorio arranca con dos semanas de deuda encima.
4. **[OPINIÓN] Y una que no preguntaste:** ¿Luqui sabe que el corte fue el 1 de agosto? Si
   nadie se lo dijo, no dejó de cargar por desidia — cambió el lugar y no se enteró.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08 | v1 — la responsabilidad de Luqui y el concepto de tarea de ritmo | *"antes de diseñar, escribí cuál es su responsabilidad diaria"* |
| 04/08 | v1.1 — corregido: parte del hueco de julio es la convención de los sueldos | Me lo corrigió la memoria del 31/07 |
| 04/08 | v2 — recorrido completo del código y la base · el corte del 01/08 · las leyes reconciliadas en siete | Pedido de análisis exhaustivo antes de diseñar |
