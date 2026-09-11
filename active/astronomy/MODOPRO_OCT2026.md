# Modo Profesional — edición `oct-2026`

Decidido por Facu el **11/09/2026**. Esto reemplaza a `sep-2026` (arrancaba el 07/09, se
vendió 0 de 25). Lo que no se menciona acá **no cambia**: precio $449.999 único /
2×$247.500, 25 cupos, una reprogramación por curso, la clase 8 sigue siendo la grabación
del set.

Producto y arquitectura previa: memoria `modopro-producto`. Acá va sólo el delta.

---

## 1. Las fechas

**Arranca la primera semana de octubre y son 8 clases**, aunque eso termine en noviembre.
Facu descartó achicar el curso a 4 semanas para que entrara en octubre: el producto vale
$449.999 por las 8.

El feriado **corre la semana de ese día**, no la de todos. Por eso los 25 cupos **no
terminan juntos**:

| Día | 1ª clase | Última | Nota |
|---|---|---|---|
| Lunes | 05/10 | **30/11** | salta el 12/10 (feriado ya cargado en `studio_holidays`) |
| Martes | 06/10 | 24/11 | |
| Miércoles | 07/10 | 25/11 | |
| Jueves | 08/10 | 26/11 | |
| Viernes | 09/10 | 27/11 | el 20/11 el estudio ABRE (Facu, 11/09) |

✅ **El 20/11/2026 (Día de la Soberanía, viernes) SE TRABAJA.** Decisión de Facu del
11/09/2026: el estudio abre. **No se carga en `studio_holidays`**, y los viernes terminan el
**27/11**. Los cupos de viernes se pueden vender.

Así que **el único feriado del curso es el 12/10**, y sólo corre a los lunes: los otros
cuatro días terminan entre el 24 y el 27/11, y los lunes el 30/11.

> Los feriados se pasan en los **cuatro** lugares que calculan o muestran fechas (crear las
> clases, apartar la cabina, la grilla de compra, el panel). Si uno se olvida, la pantalla
> promete una fecha y la base guarda otra.

## 2. La franja: sigue siendo la misma

**Lunes a viernes, 17 a 22.** Cinco horarios de arranque — **17, 18, 19, 20 y 21** — por
cinco días = **los 25 cupos**. La última clase arranca 21:00 porque el estudio cierra 22.

Los 25 son 25 porque **la cabina es una sola**: no existe un cupo 26 salvo otra cabina. El
inventario **es** la grilla `pro_cohort_slots`, nunca un contador.

## 3. 🔄 La cabina ya NO se aparta al ofrecer el cupo

**Cambio de fondo respecto de `sep-2026`.** Antes, los 25 cupos apartaban la cabina desde
que se ofrecían: durante las 8 semanas ningún member podía agendar DJ después de las 17.

Ahora: **el horario se bloquea recién cuando alguien compra y elige.** Mientras el cupo
está a la venta, esas fechas siguen disponibles para members y para todo el que paga
membresía. Eso devuelve ~7,6 clases de cabina por semana a la franja 17–22.

⚠️ Esto invalida el punto 2 de *"las tres cosas que no se pueden tocar"* de
`modopro-producto`. **Lo reemplaza la regla del punto 4**, que cubre el mismo agujero por
otro lado. El candado del cupo (índice único `pro_enrollments_un_cupo_por_horario`) **sigue
intacto**: eso no se toca.

## 4. 🚨 Modo Profesional PISA al member. Siempre.

Consecuencia directa del punto 3: un member puede agendar el lunes 19:00 del 09/11, y
después alguien compra el cupo "lunes 19:00". Dos reservas válidas, una sola cabina.

**Decisión de Facu: gana Modo Profesional, sin excepción, porque es el más caro.**

Al vender un cupo se chequean **las 8 fechas**, no el cupo:

1. La venta **se completa igual**. Nunca se frena una compra de $449.999 por una clase de
   member.
2. La clase del member **se cancela** y se le devuelve el crédito.
3. Se abre una **tarea marcada, imposible de pasar por alto**, para que **José, Luki o el
   profe** llamen al member y le reagenden. No un mail automático: una llamada.

**La tarea tiene que gritar** — igual que "FALTA PROFE": alerta arriba del panel de admin,
la clase en rojo, campanita al staff. Un member al que le cancelaron una clase y **nadie
llamó** es exactamente la forma en que esto se rompe en silencio.

⚠️ No alcanza con crear la tarea: **hay que poder contar cuántas se cerraron.** Si el
contador no existe, no sabemos si alguien llamó. Ver `boton-cargar-cobros-no-escribe` y
`contar-filas-no-es-contar-hechos`.

## 5. Cuotas: se agendan 4, se apartan las otras 4

| Pagó | Se agenda |
|---|---|
| **Curso completo** ($449.999) | las **8** clases, de una |
| **1ª cuota** ($247.500) | las **4** primeras |
| **2ª cuota** | se agendan solas las 4 que faltaban |
| **No paga la 2ª** | no se agenda nada más, y las semanas 5-8 se liberan |

🔒 **Las semanas 5-8 quedan APARTADAS a su nombre desde la 1ª cuota.** No son clases: no se
le liquidan al profe, no le aparecen al alumno en el panel. Pero **ningún member las puede
tomar.**

Sin eso, el punto 3 se come su propio producto: agenda 4 semanas, la cabina de las semanas
5-8 queda libre, un member la toma, y cuando paga la 2ª cuota el 05/11 **su horario fijo ya
no existe**. Le vendimos "todos los lunes a las 19" y lo perdió pagando.

Si no paga la 2ª cuota, el apartado se libera solo.

## 6. El 21:00 no frena la venta

Hoy **nadie puede dar una clase que arranque 21:00**: Pastrana llega hasta las 20:00 y
Guini hasta las 21:00, y sólo martes y viernes. Son 8 de los 25 cupos sin profe posible.

**Decisión de Facu, textual:** *"En principio la prioridad es que paguen. Una vez que
paguen, resolvemos."* Se venden igual. Si alguien compra un 21:00, se habla con Pastrana o
Guini y se le **extiende la disponibilidad** en Admin → Horarios — sin eso el profe no
puede dar la clase aunque se lo asignen.

El estado "todavía no sé quién lo da" ya existe en el sistema y funciona: las 8 clases
quedan **en espera**, se crean solas al asignar el profe, y mientras tanto gritan.

## 7. El orden de trabajo

**Facu:** *"Primero hacer los cambios en la web para el que quiera pagar, que el paso a
paso de pagar y elegir las semanas esté actualizado y funcionando, y después resolvemos el
tema de los horarios internamente."*

1. Crear la edición `oct-2026` con sus 25 cupos y las fechas del punto 1.
2. `clasesDelCupo` / `semanasPagas`: 4 u 8 según la cuota (punto 5).
3. Sacar el apartado de cabina al ofrecer; agregar el apartado de semanas 5-8 (puntos 3 y 5).
4. El chequeo de las 8 fechas al vender + la tarea de llamada (punto 4).
5. Landing `/curso-profesional-dj` y grilla `/modo-profesional`: fechas nuevas.
6. `npm run test:cohorte` tiene que quedar en verde, con casos nuevos para 4 y 5.
7. Recién ahí, los profes del 20:00 y 21:00.

⚠️ **Cerrar `sep-2026` antes de abrir `oct-2026`.** La pantalla pública lista las
`abierta`: si quedan las dos, se ven 50 cupos.

🔴 **`RESEND_API_KEY` en producción sigue sin verificar.** Si falta, el alumno paga
$449.999 y **no recibe el mail con sus 8 fechas**, que es su único comprobante. Verificar
antes de abrir la venta, no después.

---

## Estado: ESCRITO, NO CONSTRUIDO

Al 11/09/2026 **no se tocó una línea de código.** El repo `astronomy-members` vive en
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/` y la sesión no lo pudo leer.

**El diagnóstico, para no repetir el camino largo:**

- ❌ **No era el Acceso a disco completo.** Antigravity IDE ya lo tenía prendido, y TCC
  tiene el Escritorio en `auth 2` para `com.google.antigravity-ide` **y** para el node que
  corre Claude (`/Users/Facu/.local/node/bin/node`). Se lee en
  `~/Library/Application Support/com.apple.TCC/TCC.db`, tabla `access`, servicio
  `kTCCServiceSystemPolicyDesktopFolder`.
- ✅ **Parte era el clasificador de `autoMode`**, que denegaba con motivo
  `[Auto-Mode Bypass]`. Se resolvió agregando a `autoMode.allow` de
  `~/.claude/settings.json` una regla acotada a **ese repo** (no a todo el Escritorio).
  ⚠️ Ese archivo **Claude no lo puede editar solo**: el clasificador lo bloquea con motivo
  `[Self-Modification]`. Lo tiene que pegar Facu.
- ⏳ **Lo que quedó**: `readdir` sobre `~/Desktop` seguía dando `EPERM` mientras `stat`
  sobre la misma carpeta andaba, y `~/Downloads`, `~/Documents`, `~/Movies` y `~/Pictures`
  se leían bien. Es TCC negándole en caliente a un proceso que arrancó con otro estado
  cacheado. **Se destraba reiniciando Antigravity IDE con ⌘Q** (que salga el proceso, no
  la ventana).

**Para retomar**, con el IDE ya reiniciado:

```
cd ~/Desktop/Productoras/Astronomy/Academia/astronomy-members && claude --continue
```

Lo primero: confirmar que se lee `lib/modoproCohorte.ts`, y verificar `RESEND_API_KEY`.
