# Academy: los cambios de octubre 2026

Arrancado el **14/09/2026**. Sale de "Astronomy Concepts", el PDF que armaron Facu y
Mateo Pastrana. **Esto es para definir: todavía no se construyó nada fuera de la previa**
(`astronomyofficial.com/academy/preview`, con noindex).

## Lo que ya está decidido

- **Vidriera de `/academy`: tres puertas.** DJ (membresías) · Producción Online ·
  Profesional. El Curso de DJ mensual deja de venderse.
- **Membresías nuevas**, según el PDF:
  - **Silver**: 240 cr · clases de DJ · DJ Delivery. Sin producción, sin alquiler y
    sin acumular.
  - **Gold**: 360 cr · DJ · producción en Ableton · alquiler de cabina y estudio · DJ
    Delivery · grabación de live sets · **acumula**.
  - **Platinum**: 480 cr · todo lo de Gold · grupales · live sets con cámaras · mixing
    y mastering · comunidad y tracks inéditos · **acumula**.
- **Profesional**: 8 semanas, una clase de una hora por semana en tu día y horario fijo.
  Incluye presskit, set final de 60 minutos grabado con cámara, DJ Delivery y unreleased
  tracks de Astronomy Members. Es para el que ya mezcla.
- **Producción Online**: Ableton Live, con Valen Frando (Owners of Time). Temario
  adaptado por encuesta previa.
- **Cuándo** (Facu, 14/09): los cambios salen **a principio de octubre**. La migración de
  los alumnos actuales va **con un mes de aviso como mínimo**.

## El dato que ordena la migración

En la base (`plans`, 14/09): **el Curso de DJ ya es 240 cr a $143.520**, o sea el Silver
nuevo exacto. Los **14** alumnos activos del Curso de DJ pasan a Silver sin perder nada, y
suman DJ Delivery. Los que **pierden** son los **9** Silver actuales: producción,
alquiler, acumulación y 10 créditos. Son $1.291.680/mes (9 × $143.520).

## Respuestas de Mateo Pastrana (14/09/2026, pasadas por Facu)

| # | Tema | Decisión |
|---|---|---|
| 1 | Precio de Profesional | **Se mantiene** ($449.999 único o 2×$247.500), pero **no se muestra en la web**. Primero la encuesta, y el vendedor pasa el precio según la respuesta |
| 2 | Producción Online | Igual: encuesta, y **precio según la experiencia del prospecto**: Inicial **$200.000** · Avanzado **$250.000** · Profesional **$280.000**. La encuesta está para que el vendedor sepa qué venderle a cada uno |
| 3 | Clase de prueba | **Se borra.** La encuesta es la primera interacción |
| 4 | Profesional: ¿ediciones o cualquier semana? | **Se vende y se arranca**: cuando paga, se agendan sus 8 clases fijas. No puede chocar con las clases de las membresías |
| 5 | Silver actuales | Aviso con un mes, más oferta para pasar a Gold |
| 6 | Créditos acumulados del Silver | Se respetan hasta su vencimiento |
| 7 | Clases grupales | **Sólo Platinum** |
| 8 | Vidriera | DJ (con las membresías adentro) · Producción Online · **Carrera Profesional** o Profesional |
| 9 | Tracks de producción | Tracks del profe, de Vlado, de referencia y de alumnos que pasaron por Astronomy |

## Lo que queda abierto

| # | Pregunta | Recomendación |
|---|---|---|
| A | Los $200.000/$250.000/$280.000 de producción: ¿son por mes o por curso? ¿Cuántas clases incluyen? | Falta el dato: no se escribe un precio sin eso |
| B | Nombre: ¿"Carrera Profesional" o "Profesional"? | **Carrera Profesional**. "Profesional" ya es un nivel del precio de producción, y el cruce confunde al vendedor y al prospecto |
| C | ¿Adónde va la encuesta cuando alguien la termina? | Se guarda como lead en `/admin/leads` (ya existe, con estado y responsable) **y** abre WhatsApp con las respuestas ya escritas, así la charla arranca en el momento. 232 conversaciones/mes dan 1,3% de conversión: si el vendedor tarda horas, el lead se enfría |
| D | ¿Quién contesta los leads de la encuesta, y en cuánto tiempo? | Falta definir: José o Luqui |
| E | Profesional sin chocar con las membresías | Al comprar, la grilla **ofrece sólo horarios con las 8 semanas libres**. Así ningún member pierde una clase y no hay que llamar a nadie. Después de la compra, la cabina queda ocupada y los members no pueden reservar ahí: eso **ya lo hace** `lib/slots.ts`. Si hay mucha demanda, franjas exclusivas para el curso |
| F | Membresías: ¿el precio queda visible y se pagan solas por MP? | Sí: son el producto de autoservicio. La encuesta sólo va en los dos cursos |
| G | Tracks de referencia | Embebidos (SoundCloud/YouTube) y rotulados como **referencia**: que no parezcan hechos en Astronomy |

## Calendario propuesto

| Cuándo | Qué |
|---|---|
| hasta el 25/09 | Cerrar las preguntas A a G |
| 26/09 al 30/09 | Construir: planes y créditos por plan en la base, acumulación por plan, la web real y la landing de producción |
| **01/10** | Web nueva, encuesta y productos nuevos **sólo para altas nuevas**. Cambiar la pauta que apunta a `/curso-profesional-dj` |
| **01/10** | Aviso a los alumnos actuales. Se prepara entero y **lo manda Facu** (regla 10) |
| **01/11** | Migración efectiva de Silver y Curso de DJ, al mes del aviso |

⚠️ **`sep-2026` sigue `abierta` en `pro_cohorts`** (14/09) aunque arrancó el 07/09. Ver
`MODOPRO_OCT2026.md`: se cierra antes de abrir la próxima.
