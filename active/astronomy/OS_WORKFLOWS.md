# OS de Workflows — Astronomy

`v1 · 04/08/2026` · Respuesta a la propuesta de Facu: *"no construyas un Home para José,
construí un motor de workflows"* + *"diseñá el sistema operativo de Luqui"*.

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra el código o la base el 04/08/2026. Reproducible. |
| **[INFERENCIA]** | Calculado desde hechos. Los supuestos van escritos. |
| **[OPINIÓN]** | Mi juicio. Discutible. |

---

## Veredicto en tres líneas

1. **La arquitectura que proponés es la correcta y ya está construida — tres veces, con tres
   nombres distintos.** No hay que inventar un motor: hay que fusionar `Tarea`, `Chequeo` y
   `Chequeo` (sí, dos tipos distintos con el mismo nombre) en uno solo. Es un refactor, no un
   proyecto.
2. **Le cambiaría una cosa a tu diseño, y es la más importante:** el ítem de un workflow **no
   puede ser una persona**. La mitad del trabajo de Luqui no opera sobre gente, opera sobre
   movimientos de plata. Si el motor nace con `getPendientes(): Persona[]`, Luqui no entra.
3. **El OS financiero de Luqui no se puede construir hoy**, y no por diseño: **la plata que él
   maneja no está en la app.** `expenses` tiene **0 filas**. Un inbox financiero sobre una tabla
   vacía es una pantalla que dice "todo en orden" mintiendo.

---

## 1. El motor ya existe. Tres veces.

**[HECHO]** Hoy en `astronomy-members` hay tres tipos que describen exactamente el mismo
concepto — *un trabajo pendiente, con título, gravedad, cantidad y una acción* — y ninguno se
conoce con los otros:

| Dónde | Tipo | Campos |
|---|---|---|
| `lib/tareasHoy.ts` | `Tarea` | `id · urgencia · titulo · objetivo · porque · plata · minutos · cta · href · personas[]` |
| `lib/conciliacion.ts` | `Chequeo` | `clave · titulo · descripcion · severidad · cantidad · filas[] · accion` |
| `app/admin/revisar/page.tsx` | `Chequeo` (local) | `titulo · detalle · n · href · grave` |

Sumados detectan **25 problemas distintos**: 3 en `tareasHoy`, 11 en `conciliacion`, 11 en
`revisar`. Cada uno ya sabe su título, su gravedad, cuántos hay y a dónde se va a resolver.

**Eso es el motor de workflows.** Lo único que le falta a esa unión son tres campos:
`dueño`, `minutos` y `plata` — y `tareasHoy` ya tiene los tres.

> **[OPINIÓN]** Ésta es la parte importante del mensaje. No estás pidiendo una arquitectura
> nueva: estás pidiendo que se deje de escribir la misma por cuarta vez. El costo de la
> unificación es de un día; el de "construir el motor de workflows" desde cero es de dos
> semanas y produce lo mismo.

### La duplicación ya está haciendo daño

**[HECHO]** El mismo problema tiene hoy tres nombres y tres pantallas:

| El problema | Se llama… | En… |
|---|---|---|
| Cobros de MP que no se pudieron atribuir | "Pagos sin asignar" | `/admin/conciliacion` |
| ídem | "Cobros de Mercado Pago a identificar" | `/admin/revisar` |
| ídem | "N pagos sin asignar" | `/admin` (tarjeta violeta) |

Y los cobros duplicados los detectan **dos motores distintos** que no dan lo mismo:
`conciliacion.ts` mira `sales` de 60 días agrupando por plan; `registroIngresos.ts` cruza las
cuatro tablas de plata con tolerancia de bruto-vs-neto. Si algún día discrepan, no hay forma
de saber cuál miente.

**Un problema, un detector, un dueño.** Eso es lo que compra el motor.

---

## 2. Los cuatro cambios que sí haría sobre tu diseño

### 2.1 El ítem no es una persona — es un ítem

Tu contrato es `getPendientes()` + `resolver()`. De acuerdo. Pero en tu ejemplo los pendientes
son Clemente, Pedro y Felipe. Los de Luqui son *"$36.960 del 12/08 sin dueño"* y *"el gasto de
Splice de julio sin categoría"*. No son personas y no tienen teléfono.

```
Workflow = {
  id, dueño, titulo, objetivo, porque, urgencia,
  plata, minutos,
  items: Item[],            // ← genérico
  resultados: Resultado[],  // ← qué botones cierran un ítem, y qué escribe cada uno
}

Item = { clave, titulo, detalle, plata, contexto }
```

`Persona` pasa a ser **un caso de `Item`**, no la base. La cola de `/admin/hacer/[id]` renderiza
`Item` y, si el contexto trae teléfono y mensaje, muestra además el botón de WhatsApp. Un
workflow financiero usa la misma cola sin tocar una línea.

### 2.2 El dueño es explícito, no se deriva de los permisos

**[HECHO]** Hoy José y Luqui **comparten** `view_payments`, `add_credits` y `assign_payments`.
Si el Home filtra por permiso, los dos ven los mismos workflows y no se resuelve nada de lo que
buscás. El permiso dice *qué puede hacer*; el dueño dice *quién lo tiene que hacer*. Son dos
cosas y hoy hay una sola.

`workflow.dueño` sale de una tabla chiquita (`workflow_owner`: workflow_id → user_id, activo),
editable por vos. El permiso sigue mandando para el acceso; el dueño manda para el Home.

### 2.3 El log se generaliza — es la pieza más valiosa de lo que ya está

**[HECHO]** `contact_log` guarda qué pasó con cada persona, y `tareasHoy.ts` implementa encima
**la regla que hace que esto funcione**: *ninguna tarea desaparece porque pasó el tiempo.* Sale
sólo por una decisión registrada (`agendó`, `no le interesa`, `pospuesto + fecha`); con
`leyó`/`no leyó`/`contestó` vuelve a las 48 horas.

Esa regla es lo que separa este sistema de una lista de alertas que se ignora. **Tiene que vivir
en el motor, no en un workflow.** `contact_log` → `workflow_log (workflow_id, item_key,
resultado, volver_el, nota, actor, created_at)` y la regla se aplica sola a los 25 workflows.

Sin esto, el workflow financiero de Luqui hereda el problema que ya tuvimos: una alerta que se
vence sola. **[HECHO]** Pasó literalmente: la de sueldos sólo existía si el día del mes era ≤5,
así que si nadie entraba entre el 1 y el 5, nadie cobraba.

### 2.4 `/admin/workflows` sí — pero de sólo lectura

Acá te discuto. Escribiste que cada workflow define *"cuándo aparece, cuándo desaparece, quién
lo ejecuta, qué flujo sigue, qué estados puede tener, qué resultado lo cierra"*. Eso, en una
pantalla, es un **constructor de workflows sin código**. Es el proyecto donde mueren estos
sistemas: se pasa un mes construyendo el editor y ninguno de los dos workflows que importaban
se escribe nunca.

**[OPINIÓN]** La definición va **en código** — un archivo por workflow, ~40 líneas, que es menos
de lo que ocupa configurarlo en una UI. `/admin/workflows` existe pero es un **catálogo**:

| Workflow | Dueño | Pendientes | Plata | Última vez | Estado |
|---|---|---|---|---|---|
| Recuperar clases por vencer | José | 3 | $344.448 | hoy | ● activo |
| Cargar egresos del mes | Luqui | 1 | — | nunca | ● activo |
| Links con precio distinto | Facu | 0 | — | 04/08 | ○ apagado |

Con dos controles: **cambiar el dueño** y **apagarlo**. Definición en código, asignación y
encendido en la base. Eso te da el 95% de lo que querés al 10% del costo — y "agregar un
workflow nuevo aparece solo" sigue siendo cierto, porque el registro es un array.

---

## 3. La medición incómoda: la plata de Luqui no está en la app

**[HECHO]** Contado contra la base el 04/08/2026:

| Tabla | Filas |
|---|---|
| `expenses` (egresos) | **0** |
| `manual_payments` (cargas a mano) | **2** |
| `incidencias` (problemas de plata marcados) | **0** |
| `contact_log` (uso de la cola de tareas) | **0** |
| `unassigned_payments` pendientes | **0** |
| `payment_links` sin dueño y sin confirmar | **1** |
| `salary_payments` de 2026-07 | **0** |
| `staff_payments` de 2026-07 | **0** |

**[INFERENCIA] Si hoy le abrís a Luqui el inbox financiero que diseñaste, ve dos tarjetas:**
"Pagar los sueldos de julio" y "1 nombre del Libro sin resolver". Nada más. No porque esté todo
en orden — **porque los datos están en otro lado**: los egresos, el efectivo, las transferencias
y las clases de prueba viven en el Google Form → planilla *Finanzas - Astronomy Academy*, que la
app **sólo lee**.

Todo lo que pediste que el inbox muestre —*"hay ingresos en efectivo sin registrar"*, *"hay un
gasto sin categoría"*, *"Mercado Pago tiene diferencias con la caja"*— **no se puede calcular**
contra lo que la app tiene hoy.

### Y no hay caja

**[HECHO]** No existe en el sistema ningún saldo: ni de Mercado Pago, ni bancario, ni de
efectivo en mano. `sales` dice *qué se cobró*, no *cuánta plata hay*. La tarjeta "✅ Caja
conciliada" que pediste **no es computable**: conciliar es comparar lo que el sistema dice
contra lo que hay, y la segunda mitad de esa resta no existe en ningún lado.

Para que exista hace falta **una sola cosa nueva y chica**: un **saldo declarado** —
Luqui abre la app de MP, mira el número, lo escribe; hace lo mismo con el efectivo del cajón.
Con eso, y sólo con eso, el sistema puede decir *"faltan $12.500"* en vez de mostrar una tabla.

**[OPINIÓN]** Es el único componente verdaderamente nuevo de todo este documento, y es una
pantalla de dos campos.

---

## 4. El OS de Luqui, con la secuencia que sí funciona

El orden importa más que el diseño. Cada workflow de abajo depende de que el anterior exista.

### Workflow 0 — Cargar la plata que no pasa por Mercado Pago
**Sin esto, todo lo demás lee de una tabla vacía.**

Hoy Luqui abre un Google Form. **[HECHO]** El Form **no acredita créditos** — es la causa
escrita en el instructivo de `/admin/registro` de que un alumno pague y quede sin nada. Y
`/admin/carga-manual`, que sí acredita, ya existe y ya funciona.

El workflow no es una pantalla nueva: es **matar el Form** y que la carga sea la pantalla que
ya está. Un ítem = un movimiento por cargar. Se cierra cuando el mes no tiene huecos.

> Qué se carga a mano y qué no, ya está decidido y verificado: MP y DJ Delivery los toma la web
> sola; **efectivo, transferencia, clases de prueba y todos los egresos los sigue cargando él.**

### Workflow 1 — Pagar sueldos del mes
**[HECHO]** Está vivo ahora mismo: `salary_payments` y `staff_payments` de 2026-07 están en cero
y hoy es 4 de agosto. Ya existe `/admin/sueldos` y ya calcula todo. Sólo le falta ser un ítem
del inbox en vez de una tarjeta que aparece en el panel de José, que no paga sueldos.

### Workflow 2 — Este pago no sabemos de quién es
Ya existe entero: `/admin/pagos-sin-asignar` (MP) y `/admin/pagos-sin-atribuir` (Libro), y ya
ordena por probabilidad agrupando por persona. Es exactamente el flujo que describiste —
*mostrar primero las coincidencias más probables, nunca una lista enorme*— y ya está escrito.
**No se toca. Se enchufa.**

> La regla que nunca se rompe, y que el workflow tiene que seguir respetando: **jamás se atribuye
> un pago por parecido de nombre.** Se resuelve una vez por persona y queda en `ledger_aliases`.

### Workflow 3 — Esta plata entró y no está en la facturación
Ya existe: `/admin/registro` con el instructivo paso a paso escrito. Es la mejor pantalla de
resolución que tiene el sistema hoy.

### Workflow 4 — La caja no cuadra
**El único que hay que construir.** Luqui declara el saldo de MP y el efectivo; el sistema
compara contra lo cobrado del período y dice qué falta. Va **después** del Workflow 0: sin los
movimientos cargados, la diferencia va a ser siempre enorme y la tarjeta se vuelve ruido.

### Workflow 5 — Un gasto sin categoría
Va último y **[OPINIÓN]** vale poco: son 0 filas hoy y ninguna decisión cambia por la categoría
de un gasto. Se anota, no se construye.

### El Home de Luqui

No es una pantalla nueva: **es `/admin` filtrado por dueño**. Mismo componente, mismo motor.

```
Buenos días, Luqui.
Hoy tenés 3 cosas · ≈25 min

● Pagar los sueldos de julio          $1.2M por salir · 10 min   [Empezar →]
● Cargar 4 movimientos de agosto      sin esto el mes miente · 10 min
○ 1 nombre del Libro sin resolver     $143.520 sin dueño · 5 min
```

Y al terminar, la misma pantalla de "Tarea terminada" que ya existe.

---

## 5. Pantalla por pantalla — qué sobra, qué se reutiliza, qué desaparece

**[HECHO]** Las 14 pantallas de plata del admin, auditadas contra el código.

| Pantalla | Qué resuelve | Veredicto |
|---|---|---|
| `/admin/libro` | Toda la plata con su signo. Un motor por lado. | **Se queda intacta.** Es la única pantalla de consulta que vale: contesta "cómo venimos" y no genera trabajo. |
| `/admin/registro` | Un renglón por pago real; describe y resuelve cada problema. | **Se queda.** Es la pantalla de resolución de los workflows 2 y 3. |
| `/admin/pagos-sin-asignar` | Cobros de MP sin dueño, con candidatos. | **Se queda.** Es el `resolver()` del workflow 2. |
| `/admin/pagos-sin-atribuir` | Nombres del Libro sin dueño, agrupados por persona. | **Se queda.** |
| `/admin/carga-manual` | Carga un pago Y acredita créditos. | **Se queda y sube de rango:** es el reemplazo del Google Form. |
| `/admin/sueldos` | Liquidación de profes y equipo. | **Se queda.** Es el `resolver()` del workflow 1. |
| `/admin/cobros-mes` | Quién pagó este mes y quién no. | **Se queda.** *(Es el mejor diseño del panel: estado con punto de color, WhatsApp, botón de recordar. Cuando haya que diseñar algo, copiar de ahí.)* |
| `/admin/auditoria-creditos` | ¿Los saldos cuadran? | **Se queda**, pero es de José, no de Luqui. |
| `/admin/revisar` | 11 contadores de "qué está roto". | **Desaparece como pantalla.** Sus 11 chequeos se convierten en 11 workflows con dueño. Hoy es un índice de problemas ajenos: nadie es responsable de ninguno. |
| `/admin/conciliacion` | 11 chequeos contra Mercado Pago en vivo. | **Desaparece como pantalla**, misma razón. Sus chequeos son casi todos **de Facu**, no de Luqui: precios de links, planes sin mapear, webhooks. |
| `/admin/finanzas` | Resumen histórico + gráficos. | **Se queda, sólo para Facu.** No es trabajo, es lectura. Fuera del inbox de todos. |
| `/admin/ingresos`, `/admin/egresos` | — | Ya son redirecciones al Libro. Nada que hacer. |
| `/admin/creditos-manuales` | Créditos dados a mano. | **Se queda.** Auditoría, no trabajo. |
| `/admin/growth` | Embudo + a quién llamar. | **Se solapa con el Home de José.** Cuando el motor esté, su lista de llamados es un workflow y el resto del embudo es lectura. Revisar en Sprint 4. |

**El patrón:** de 14 pantallas, **ninguna hay que borrarla y sólo dos dejan de ser pantallas**
(`revisar` y `conciliacion`, que pasan a ser fuentes de workflows). Todo lo demás ya está bien
hecho — el problema nunca fue que faltaran herramientas, fue que **nadie era dueño de ninguna**.

---

## 6. El riesgo real, dicho de frente

**[HECHO] `contact_log` tiene 0 filas.** La cola de tareas de José se puso en producción el
04/08 y **todavía no la usó nadie una sola vez.**

**[HECHO]** El `OS_CRECIMIENTO.md` v2, escrito hoy, dice: *"Restricción vigente: está prohibido
escribir código. Se levanta sólo si (a) el proceso manual funcionó 2 semanas, (b) el cuello pasó
a ser operativo y (c) automatizar rinde más que seguir a mano."*

**[OPINIÓN]** Generalizar a motor un sistema que no se usó ni una vez es exactamente lo que esa
regla prohíbe. La abstracción correcta no se deduce de un diseño, se descubre usando el caso
concreto: hoy no sabemos si José va a apretar "pospuesto" o si va a ignorar la cola entera.

Por eso la recomendación no es "sí" ni "no", es **esto sí y esto todavía no**:

| Ahora (≈1 día, dentro de la restricción: no agrega features, saca duplicación) | Sprint 4 (15–28 sep) |
|---|---|
| Unificar los tres tipos en `Workflow` | La pantalla `/admin/workflows` |
| `contact_log` → `workflow_log`, con la regla de reaparición en el motor | Los workflows financieros 2 a 5 |
| `dueño` explícito + Home filtrado por dueño | El saldo declarado y la caja |
| Enchufar los 3 workflows que ya están vivos: sueldos, pago sin dueño, egresos sin cargar | |

Y **antes de todo eso**, lo que rinde de verdad esta semana y no requiere una línea de código:
**[HECHO]** a Clemente Trejo Benayas, Pedro Fraguas y Felipe Brandan **se les vencen las clases
el 13/08** — 240, 240 y 120 créditos. Eso son 14 días. El motor de workflows no.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08 | v1 — respuesta a la propuesta de motor de workflows + OS de Luqui | — |
