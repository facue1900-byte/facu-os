# Observación — dos mañanas, y de ahí sale el próximo workflow

`04/08/2026` · **congelado hasta el 18/08/2026**

El sprint terminó: José tiene escritorio, Luqui tiene escritorio. **El próximo trabajo no es
código, es mirar.** Este documento es la herramienta de esas dos mañanas.

> **LEY 8** (`astronomy-members/CLAUDE.md`): el software crece únicamente cuando aparece
> **trabajo** nuevo, nunca cuando aparece una **idea** nueva. La pregunta que autoriza a
> escribir una línea de código es una sola:
>
> ### ¿Esta persona necesitó SALIR del sistema para hacer su trabajo?
>
> Sí → falta una tarea. No → **no se construye nada.**

---

## Las reglas del que mira

Son cuatro y las cuatro cuestan, por eso están escritas.

1. **No ayudar.** Si José se traba y vos le decís dónde está el botón, acabás de borrar la
   evidencia. El trabarse **es** el dato.
2. **No explicar por qué está diseñado así.** Explicarlo convierte un problema de diseño en
   un problema de memoria de él, que es justo el error que se quiere evitar.
3. **No arreglar nada en el momento.** Anotar y seguir. Si algo está tan roto que le impide
   trabajar, se anota y recién ahí se interrumpe.
4. **Anotar la frase textual.** *"¿Y esto de dónde salió?"* vale mil veces más que
   *"parecía confundido"*. Las categorías útiles salen de leer veinte citas, no de
   inventarlas antes de tener una.

**Duración: una mañana entera de trabajo real, no una demo.** Si arranca a las 9 y a las
9:20 ya está hecho el escritorio, quedarse igual: lo que hace de 9:20 a 13:00 es
exactamente el trabajo que el sistema todavía no conoce.

---

## La planilla

Una fila por cada vez que pasa **cualquiera** de estas nueve cosas. Sin filtrar, sin juzgar
si "es importante". El filtro viene después.

| # | Hora | Qué estaba tratando de hacer | Qué hizo en vez de eso | Disparador | ¿Salió del sistema? | Frase textual |
|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |

**Los nueve disparadores** (poner el código en la columna *Disparador*):

| Código | Qué es | Por qué importa |
|---|---|---|
| **DUDA** | Se quedó pensando antes de tocar algo | La pantalla no dice lo que hace falta saber |
| **PREG** | Te preguntó a vos | Igual que arriba, pero peor: no lo pudo resolver solo |
| **ATRÁS** | Volvió a una pantalla anterior | Le faltaba un dato que ya había pasado |
| **FUERA** | Salió del sistema por cualquier motivo | **El disparador principal. Es lo que la Ley 8 pide encontrar** |
| **WA** | Abrió WhatsApp a mano | ¿El sistema no le dio el link, o no le dio el mensaje? |
| **PLAN** | Abrió una planilla | Hay un dato que vive afuera. **Ese dato es un workflow** |
| **MP** | Abrió Mercado Pago | Fue a buscar algo que el sistema no le muestra. ¿Qué? |
| **BCO** | Abrió el banco | Idem, y define si el banco entra al sistema o no |
| **PAPEL** | Anotó algo en papel | Lo más caro de todos: ese dato no existe para nadie más |

---

## La pregunta del final de la mañana

Una sola, y se contesta antes de levantarse de la silla:

> **¿Hubo algún momento en que esta persona supo qué hacer y el sistema no la ayudó a
> hacerlo?**

- **No** → el escritorio está bien. **No se construye nada.** Se vuelve a mirar en dos semanas.
- **Sí** → por cada momento, se nombra el trabajo. Si no se puede nombrar, no era un trabajo.

---

## De una observación a una tarea

Una fila de la planilla **no** es un workflow. Se convierte en uno sólo si pasa las cuatro
preguntas — y las cuatro ya son las leyes del motor:

| | Pregunta | Ley |
|---|---|---|
| 1 | ¿De **quién** es este trabajo? José / Luqui / Facu. Uno solo | Ley 1 |
| 2 | ¿**Por qué aparecería**? El disparador, con el dato que lo activa | Ley 2 |
| 3 | ¿**Cuándo termina**? La condición de salida, no una intención | Ley 2 |
| 4 | ¿Qué pasa si **no se hace**? Si la respuesta es "nada", **es una estadística** | Ley 2 |

Y una quinta, que es la de la Ley 8: **¿esto elimina trabajo manual, evita un error, o
reemplaza una herramienta externa?** Si no hace ninguna de las tres, se anota y no se
construye.

---

## Antes de sentarse: qué dice la base

Esto se corre **el mismo día** de cada observación, para saber si el escritorio se está
usando o si sigue siendo decoración. Son los tres contadores que ya existen:

```bash
cd "/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members"
npm run ver:workflows          # qué ve cada uno HOY, corriendo el motor real
```

| Tabla | Qué prueba | Al 04/08/2026 |
|---|---|---|
| `contact_log` | José usó la cola de contacto | **0 filas** |
| `ritmo_log` | Luqui declaró algún día vacío | **0 filas** |
| `expenses` | Alguien cargó un gasto en la app | **0 filas de por vida** |

> **Si el 18/08 los tres siguen en cero, el hallazgo no es "faltan tareas": es que nadie
> usa esto**, y ninguna tarea nueva lo va a arreglar. Ése sería el resultado más importante
> de las dos mañanas, y hay que estar dispuesto a escribirlo.

---

## Las dos sesiones

### Mañana con José

Su escritorio son 5 tareas · 10 casos. Lo que hay que mirar sin preguntar:

- Cuando termina un WhatsApp, **¿aprieta uno de los cuatro botones de resultado?** Si no lo
  hace, `contact_log` queda en cero y la cola le repite la misma persona mañana.
- **¿Usa el mensaje sugerido o lo reescribe?** Si lo reescribe siempre, el mensaje está mal.
- Con *"Corregir los créditos"*, **¿entiende qué tiene que corregir** o abre la ficha y sale?
- ¿Qué hace **entre** tarea y tarea? Ese hueco es el trabajo que el sistema no conoce.

### Mañana con Luqui

Su escritorio son 2 tareas, y las dos son nuevas de hoy. Lo que hay que mirar:

- **¿Carga o declara?** Si declara *"hoy no hubo nada"* todos los días, la declaración se
  volvió el camino corto y hay que hacerla costar más.
- **¿Abre Mercado Pago?** Casi seguro que sí — el saldo no se puede leer por API (403). Eso
  ya está diagnosticado y es el punto 4 del `OS_LUQUI.md`. **Confirmarlo mirando, no
  asumirlo.**
- **¿Sigue cargando en el Google Form?** Si carga en los dos lados, mirar que la **fecha sea
  la misma**: distinta fecha en cada lado hace que un pago se cuente dos veces o ninguna.
- ¿Cuánto tarda en encontrar la pantalla de cargar un gasto?

---

## Lo que NO se hace en estas dos semanas

- Ningún workflow nuevo. Ninguno.
- Ninguna pantalla nueva, incluida la del **saldo declarado** — está diseñada y aprobada, y
  **espera igual**: va después de ver dos semanas de carga real, si no la diferencia va a
  ser de millones todos los días y la tarjeta se deja de mirar en una semana.
- No investigar la diferencia de **$17.258** en el sueldo de julio de José. Guardada, no
  perdida: [[sueldo-jose-diferencia-luqui]].

---

## Registro

| Fecha | Con quién | Filas anotadas | ¿Salió del sistema? | Qué salió |
|---|---|---|---|---|
| | José | | | |
| | Luqui | | | |
