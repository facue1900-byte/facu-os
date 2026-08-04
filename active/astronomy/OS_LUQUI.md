# El Sistema Operativo de Luqui

`v1 · 04/08/2026` · **La responsabilidad, antes que las pantallas.** Este documento no
diseña nada: escribe cuál es el trabajo de Luqui y qué parte de ese trabajo el sistema
puede ver hoy. Las tareas salen de acá, igual que salieron las de José.

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra la base o la planilla el 04/08/2026. Reproducible. |
| **[INFERENCIA]** | Calculado desde hechos. Los supuestos van escritos. |
| **[OPINIÓN]** | Mi juicio. Discutible. |

Las cinco leyes y el manifiesto están en `OS_JOSE.md` y en el `CLAUDE.md` del repo. **No se
diseña "la pantalla de Luqui": se le agregan escritorios al mismo sistema operativo.**

---

## 1. La medición que decide todo lo demás

**[HECHO] La planilla de finanzas no tiene una sola fila desde el 24/07/2026.** Once días.
Leída hoy con la service account: 1.133 filas, la última es *"Matilda Goldy - Silver Member
- Agosto 2026"* del 24/07.

**No es el sync: es que dejó de cargarse.** El cron corre cada hora y `payment_links` no
tiene **ni una** fila escrita por él — sus 613 filas son la importación del 24/07. No hay
nada nuevo que traer.

**[HECHO] Y los egresos se cortaron antes: el último es del 16/07.**

| Mes | Ingresos | n | Egresos | n | Resultado que muestra |
|---|---|---|---|---|---|
| enero | $2.125.844 | 20 | $1.228.071 | 12 | +$897.773 |
| febrero | $2.279.664 | 21 | $2.643.539 | 12 | −$363.875 |
| marzo | $2.498.669 | 24 | $2.881.339 | 12 | −$382.670 |
| abril | $3.654.694 | 32 | $4.753.619 | 15 | −$1.098.925 |
| mayo | $3.118.912 | 25 | $3.159.950 | 13 | −$41.038 |
| junio | $3.259.634 | 26 | $3.038.286 | 8 | +$221.348 |
| **julio** | **$3.055.273** | 23 | **$192.520** | **2** | **+$2.862.753** |
| **agosto** | **$143.520** | **1** | **$0** | **0** | **+$143.520** |

**[INFERENCIA] El resultado de julio no es +$2.862.753.** El promedio de egresos de enero a
junio es **$2.950.801/mes** (17.704.804 ÷ 6). Con ese promedio, julio real ronda **+$105.000
— unas 27 veces menos.** El supuesto es que julio gastó como el promedio del semestre; el
número exacto sólo sale de cargar los egresos de verdad.

> **La asimetría que produce esto es la clave de todo el escritorio de Luqui: los ingresos
> entran solos porque Mercado Pago avisa; los egresos los carga una persona.** Cuando esa
> persona deja de cargar, el sistema no se rompe — **empieza a mostrar ganancias que no
> existen, y no avisa.** Es exactamente la falla que la regla final de la Constitución
> prohíbe: algo que puede romperse en silencio.

**[HECHO] Y agosto ya está roto:** la app tiene 8 ventas de Mercado Pago del mes; la
planilla, 1 ingreso y 0 egresos.

---

## 2. La responsabilidad de Luqui, escrita

Tomo tu lista de siete y le hago **una sola corrección**: *"verificar que todo el dinero que
entró esté registrado"* y *"verificar que todo el dinero registrado exista"* no son dos
responsabilidades, son **las dos direcciones de la misma** — y ninguna de las dos es trabajo
diario: son **el resultado** de cargar y conciliar. Ponerlas como tareas propias haría que
Luqui abra una pantalla a "verificar" sin nada concreto que hacer.

Con eso, queda esto:

### Todos los días
1. **Cargar la plata que no pasa por Mercado Pago** — efectivo, transferencias, clases de
   prueba. Es lo único que nadie más va a registrar.
2. **Cargar los egresos del día** — sueldos ya pagados, alquiler, Splice, pauta, insumos.
3. **Darle dueño a la plata que entró sin nombre.**

### Todas las semanas
4. **Que el saldo real coincida con el del sistema.** Mercado Pago y el efectivo en mano.
   Una sola pregunta: *¿la plata que hay es la que decimos que hay?*

### Todos los meses
5. **Liquidar y pagar los sueldos**, del 1 al 5.
6. **Cerrar el mes**: que el resultado que ve Facu sea el real, no el que sale de tener los
   ingresos completos y los egresos a medias.

> **[OPINIÓN] Saqué "banco" de la responsabilidad 4, y quiero que sea una decisión tuya y no
> un olvido mío.** [HECHO] En el sistema no existe absolutamente nada bancario: ni saldo, ni
> movimientos, ni cuenta. Meterlo ahora es abrir un frente entero. Si el banco importa para
> el día a día de Luqui, decímelo y lo diseño; si el banco es sólo el destino de las
> transferencias que él ya carga a mano, con la 1 alcanza.

---

## 3. De la responsabilidad a las tareas — y qué puede ver el sistema hoy

| # | Responsabilidad | ¿El sistema puede saber que falta? | Estado |
|---|---|---|---|
| 1 | Cargar la plata que no pasa por MP | **No.** Nadie le avisa al sistema de un efectivo que entró | **Hay que construirla** |
| 2 | Cargar los egresos | **No.** Mismo caso, y `expenses` tiene **0 filas** | **Hay que construirla** |
| 3 | Pagos sin dueño | **Sí.** `unassigned_payments` con estado `pending` | **Ya existe** — es tarea de Luqui desde hoy |
| 4 | Que el saldo real coincida | **No.** No existe ningún saldo declarado contra el cual comparar | **Falta la pieza** |
| 5 | Sueldos | **Sí.** `salary_payments` / `staff_payments` del período | **Ya existe** — está viva ahora |
| 6 | Cerrar el mes | Se deriva de 1 y 2 | **Sale sola** cuando las dos existan |

### Acá aparece un tipo de tarea que José no tiene

Todas las tareas de José nacen de **evidencia**: el sistema ve un dato y arma el caso —
tres alumnos vencidos, un pago sin dueño. Las tareas 1, 2 y 4 de Luqui **no pueden nacer
así**, porque su disparador es algo que ocurrió *fuera* del sistema: un billete, una
transferencia, un gasto. Nadie se lo va a contar.

**[OPINIÓN] Entonces nacen de un ritmo, no de un dato**, y hay que llamarlas por su nombre
en vez de disfrazarlas de evidencia:

| | Tarea de evidencia | Tarea de ritmo |
|---|---|---|
| Aparece porque | el sistema encontró algo | pasó el tiempo |
| Se cierra porque | el dato cambió | **una persona declaró** que no hay nada |
| Puede mentir | no | **sí** — y hay que asumirlo |
| Ejemplos | los 5 trabajos de José, sueldos, pagos sin dueño | cargar los movimientos del día, cerrar la caja |

Una tarea de ritmo **rompe la propiedad más linda del motor**: que un caso desaparezca sólo
cuando el problema se arregló de verdad. Acá, "no hubo movimientos hoy" lo dice Luqui, y
puede equivocarse.

**No conozco forma de evitarlo**, y prefiero decirlo antes que fingir que el sistema puede
saber lo que no puede. Lo que sí se puede hacer es que **mentir cueste**: la tarea pide
declarar *"no hubo"* explícitamente, queda registrado con nombre y fecha, y **si pasan tres
días seguidos sin una sola carga, eso vuelve como problema** — que es exactamente lo que
falló el 24/07 y nadie notó en once días.

Cumple la Ley 2 sin problemas:

> **Por qué apareció:** hoy todavía no cargaste los movimientos.
> **Termina cuando:** cargaste lo que hubo, o dijiste que no hubo nada.
> **Si no hago nada:** el resultado del mes queda inflado. En julio mostró +$2.862.753
> cuando el promedio de egresos del semestre es $2.950.801.

---

## 4. Qué construir, en orden

| # | Qué | Por qué va ahí | Tamaño |
|---|---|---|---|
| 1 | **Tarea de ritmo "Cargar los movimientos de hoy"** → resuelve en `/admin/carga-manual`, que ya existe y **ya acredita créditos** (el Google Form no) | Sin esto todo lo demás mide sobre datos incompletos | Chico: la tarea + el botón de "no hubo nada" |
| 2 | **Egresos dentro de la app** | `expenses` está vacía y la pantalla ya existe (`/admin/libro` los muestra). Falta que alguien los cargue ahí en vez de en el Form | Chico |
| 3 | **Matar el Google Form** | Mientras existan dos lugares para cargar, la mitad va a ir al equivocado. Y el Form **no acredita créditos**: es la causa escrita de que un alumno pague y quede sin nada | Es una decisión, no código |
| 4 | **Saldo declarado + tarea "Cerrar la caja"** | Recién con 1 y 2 la diferencia va a ser chica y la tarjeta va a servir. Antes sería ruido gigante todos los días | Dos campos y una comparación |
| 5 | **Alarma: tres días sin cargar** | Es el chequeo que hubiera avisado el 27/07 en vez del 04/08 | Muy chico |

**[OPINIÓN] El orden importa más que el diseño.** Construir la caja (4) antes que la carga
(1 y 2) da una pantalla que dice "faltan $3.000.000" todos los días y se deja de mirar en
una semana.

## 5. Lo que NO haría

- **Un módulo de conciliación bancaria.** No hay datos de banco y no está claro que hagan
  falta. Ver la pregunta abierta.
- **Importar la planilla de vuelta.** La planilla no es la fuente: es el síntoma. Si se
  arregla la carga, la planilla deja de hacer falta.
- **Un dashboard financiero para Luqui.** Ley 3. El resumen del mes es de Facu y ya vive en
  `/admin/finanzas`.
- **Automatizar la carga de efectivo.** No hay de dónde: alguien tiene que decir que entró.

---

## 6. Lo que necesito de vos antes de construir

1. **¿El banco entra o no?** (ver arriba). Cambia si son 2 tareas o 4.
2. **¿Luqui carga en la app o seguimos con el Form?** Si sigue el Form, la tarea 1 no se
   puede cerrar nunca dentro del sistema y todo esto queda a medias.
3. **[HECHO] Hay 11 días sin cargar y 19 sin un egreso.** Antes de que el escritorio exista,
   eso hay que ponerlo al día a mano o el primer día va a arrancar con una deuda de dos
   semanas encima.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08 | v1 — la responsabilidad de Luqui, la planilla muerta desde el 24/07 y el concepto de tarea de ritmo | *"antes de diseñar Luqui, escribí cuál es exactamente su responsabilidad diaria"* |
