---
name: flyers
description: Genera tandas de flyers en PNG listos para Instagram (feed, story y cuadrado) para los productos de Astronomy Academy — Curso de DJ, producción presencial, producción online, membresías y Modo Profesional. Usar cuando Facu pida "flyers", "placas", "creativos para pauta", "algo para postear del curso/las membresías", o cuando cambie el catálogo y haya que rehacer las piezas.
---

# flyers

Un producto × N ángulos de venta × M formatos, generados de una. El copy vive en
`contenido/academy.json` y los créditos salen de la base de la app. **Las piezas no
llevan precio en pesos** — ver más abajo.

## La placa de DISPONIBILIDAD (Modo Profesional)

Va aparte porque no es un flyer de producto: es **el inventario del curso, dibujado**.
La grilla de 5 días × 5 horas con los bloques vendidos tachados.

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/flyers/scripts/disponibilidad.py"
# --formatos story,feed,square   · --cohorte sep-2026   · --sin-foto
```

Sale a `~/Desktop/Productoras/Astronomy/Academia/Flyers Academy/disponibilidad/`.

**Los bloques se tachan solos.** La grilla se lee de las mismas tablas con las que la web
cobra (`pro_cohort_slots` + `pro_enrollments`), con el mismo criterio de "tomado" que usa
la app —una `pendiente` con el hold vencido no ocupa—. Por eso la placa y el checkout no se
pueden separar: si un casillero está tachado, ese lugar está vendido de verdad.

Se regenera **cada vez que se vende un lugar**, antes de postear. Tachar a mano es
exactamente el trabajo que esto vino a sacar: vuelve con cada venta, y el día que alguien
se olvida la story ofrece un horario que ya no existe.

| Casillero | Qué significa |
|---|---|
| Vacío | Libre. Un cupo sin profe asignado se muestra libre: el alumno compra el día y la hora |
| Cruz blanca | Vendido |
| Cruz apagada | Fuera de venta en esta edición |

Si la consulta vuelve vacía, el script **corta**: una grilla sin filas daría una placa con
los 25 bloques libres, que es la mentira más cara de publicar.

## Correr

Siempre en dos pasos, y en este orden:

```bash
# 1. Refrescar créditos/planes contra la fuente de verdad (tabla `plans` de Supabase)
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/flyers/scripts/sync_precios.py"

# 2. Generar
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/flyers/scripts/generar_flyers.py"
```

Sale todo a `~/Desktop/Productoras/Astronomy/Academia/Flyers Academy/<estilo>/<producto>/<angulo>__<formato>.png`,
más una `_hoja-de-contacto.jpg` por estilo para revisar las piezas de un vistazo.

Filtros útiles cuando cambia una sola cosa:

```bash
--estilo editorial|foto|plano       # default: editorial
--productos membresias,curso-dj     # solo esos productos
--angulos que-es                    # solo el ángulo "qué es"
--formatos story                    # solo 1080x1920
```

## Los tres estilos

| Estilo | Qué es | Cuándo |
|---|---|---|
| `editorial` (default) | El sistema real de la cuenta. Negro puro o foto desaturada, **monocromo**, Helvetica Neue en MAYÚSCULAS **alineada a la izquierda y anclada abajo**, micro-rótulos mono en las esquinas, cruces de registro, logo de dos círculos. | **Instagram (@astronomy.academy).** Es el único que matchea la grilla. |
| `foto` | Foto del estudio + velo violeta + firma cursiva. | Descartado como referencia de IG — quedó como variante. |
| `plano` | Degradado violeta sobre negro + isotipo estrella. | La app y el sitio (astronomyofficial.com). |

### El sistema editorial, leído de la grilla (capturas del 28/07/2026)

- **Monocromo, sin acento de color.** Nada de violeta. El énfasis dentro de un
  titular se hace con **peso** (`<em>` = bold), no con color.
- **Alineado a la izquierda, anclado abajo.** Nada centrado.
- **Mayúsculas** vía CSS: el JSON queda legible en minúscula.
- **Micro-rótulos mono** en las esquinas — textuales de sus posts:
  `COMMUNITY-DRIVEN / EDUCATION`, `BUILT BY ARTISTS / FOR ARTISTS`,
  `BUILT BY DJS / FOR DJS`, `WHERE MUSIC / CONNECTS US`, `JOIN THE FREQUENCY`,
  `FROM BEDROOM / TO BOOTH`, `REAL TRACKS / REAL SCENE`,
  `TRAINED BY CLUBS / SHAPED BY SOUND`, `ZERO NOISE / ALL IMPACT`.
  Se configuran en `marca.rotulos` con override por producto.
- **Nada de botones.** El llamado a la acción es una etiqueta entre corchetes
  (`[ INSCRIPCIONES ABIERTAS ]`), como en la cuenta. En toda la grilla no hay un
  solo botón redondeado.
- **Los asides van entre paréntesis** — `(CURSO DE DJ)`, `(HERNAN CATTANEO)`.
- **Las cruces de registro** van a inset fijo de 1.5rem, **menor** que el padding
  del contenido: son marcas de margen. Ancladas al mismo padding que el texto, se
  le montan encima al rótulo y al logo.
- **Alternancia de fondo:** las piezas con mucho texto (bullets, planes) van sobre
  negro puro; las de titular corto, sobre foto. Es la cadencia de la grilla.
- **Foto muy desaturada** (`grayscale(.72)`): con poca desaturación el neón amarillo
  del estudio le grita al blanco del titular.

**Tipografía:** Helvetica Neue, que ya está en macOS (`/System/Library/Fonts/HelveticaNeue.ttc`)
— no se descarga nada. Los micro-rótulos usan Roboto Mono, embebida en `assets/fonts/`.

**Pendiente:** el logo de dos círculos está **dibujado en SVG dentro del template**,
no es el archivo oficial (no hay asset de ese símbolo en el repo). Si aparece el
original, reemplazarlo.

### Una foto por ángulo, y el generador lo verifica

Las fotos viven en `assets/fotos/` (14) y se asignan **en cada ángulo** de
`academy.json` (campo `foto`). El `foto` a nivel producto quedó como red de
seguridad para un ángulo nuevo, pero ya no es lo que se dibuja.

**Ninguna foto puede repetirse dentro de un mismo producto.** `chequear_fotos()`
corta la corrida si pasa. Los cinco ángulos de un producto se ven juntos —como
tarjetas del carrusel de Meta o como fila de la grilla— y ahí la repetición se lee
como un error de carga, no como una pieza. Reusar la misma foto entre productos
distintos está bien: nunca se ven juntos.

**Tampoco hay tarjetas 100% negras.** El negro puro con el texto anclado abajo
funciona en la grilla de Instagram (aire deliberado), pero entre cuatro fotos a
sangre en un carrusel deja medio cuadro vacío. Las piezas densas (bullets, planes)
van sobre foto **muy oscura**: misma cadencia, sin el hueco. `fondo: "negro"` sigue
soportado por si alguna vez conviene.

**`escala: "xl"`** en un ángulo hace el titular grande y angosto (11ch). Es para la
tarjeta que abre un carrusel: titular corto, sin bloque abajo, porque es lo único
que frena el scroll.

Las fotos vinieron de `~/Desktop/Productoras/Astronomy/Academia/Contenido/Material para contenido/`
y de `~/Desktop/Productoras/Astronomy/Academia/Fotos del estudio/Fotos/`, reescaladas a
1800px de lado largo.

**El velo son dos gradientes, no uno.** El vertical solo no alcanza cuando la foto
tiene una masa clara justo donde cae el texto: el saco beige del DJ en `dj-bw.jpg`
se comía "EL CURSO PARA / EL QUE YA". El horizontal oscurece la columna izquierda
—donde el sistema ancla todo el texto— y deja intacto el lado derecho de la imagen.

## Qué hay adentro

| Archivo | Qué es |
|---|---|
| `contenido/academy.json` | Productos, ángulos y copy. **Es lo único que se edita para cambiar textos.** |
| `contenido/precios.json` | Snapshot de la tabla `plans`, con fecha. Lo escribe `sync_precios.py`. |
| `templates/editorial.html` | **La estética que va a Instagram.** Sistema de la cuenta. |
| `templates/flyer.html` | Los estilos `foto` y `plano`. Tokens de `app/globals.css`. |
| `assets/marca/` | Isotipo, logotipo y **firma cursiva** (`academy-blanco.png`, la del neón del estudio). |
| `assets/fotos/` | Fotos del estudio para el estilo `foto`. |
| `assets/fonts/` | Helvetica Neue sale del sistema; acá viven Roboto Mono (rótulos) y Montserrat (estilos viejos). |

**Productos** (5): `curso-dj`, `produccion`, `produccion-online`, `membresias`,
`modo-profesional`.
**Ángulos** (5 por producto): `que-es`, `beneficios`, `profe`, `como-funciona`,
`contacto`.
**Formatos** (3): `feed` 1080×1350 · `story` 1080×1920 · `square` 1080×1080.

Total por tanda completa: **75 piezas**.

## Las piezas NO llevan precio en pesos

Decisión de Facu del 28/07/2026. Con la inflación argentina, un flyer publicado con
un número queda viejo en semanas y obliga a rehacer la tanda entera. Lo único
numérico que sale es lo que **no se desactualiza**: créditos, cantidad de clases,
cantidad de módulos. El que quiere el valor del mes, escribe por DM — por eso la
etiqueta de casi todas las piezas es `[ ESCRIBINOS POR DM ]`.

**El guard está en el código, no en el JSON**: `bloque_editorial()` revienta si le
llega un bloque de tipo `precio`. Así no alcanza con editar el contenido para que
vuelva a salir un número en pesos.

`sync_precios.py` se sigue corriendo: de ahí salen los **créditos** por plan
(`monthly_credits`), que tampoco se escriben a mano. Los `precio_ars` que quedan en
`academy.json` no se dibujan en ninguna pieza — están para no perder la trazabilidad
contra la base.

## Verificación

Ninguna pieza se da por buena porque Chrome no tiró error. De cada PNG se chequea:

- que las dimensiones sean exactamente las del formato;
- que pese más de 40 KB (menos que eso es una placa vacía: el render se colgó antes
  de pintar el texto);
- que el texto **no haya desbordado**. El template mide el alto real y achica la
  tipografía hasta que entra; deja el veredicto en el `<title>` y el script lo lee
  del DOM en la misma corrida de Chrome. Si ni al 62% entra, la pieza se reprueba y
  el script sale con error.

Una tanda con aunque sea una pieza mala termina en exit 1. No exporta 74 buenas y
una rota en silencio.

## Lecciones

- **`--user-data-dir` cuelga al Chrome de macOS.** Con un perfil nuevo en `/tmp` el
  proceso se queda esperando para siempre, sin escribir el PNG ni tirar error — ni
  agregando `--no-first-run --no-default-browser-check --disable-sync`. Sin el flag
  anda, y cinco corridas en paralelo dan PNGs byte a byte idénticos. No volver a
  agregarlo "por prolijidad".
- **`timeout` no existe en macOS**, así que no sirve para acotar un render colgado.
  El corte va en el `subprocess.run(timeout=...)` de Python.
- **Chrome se cuelga cada tanto con 5 instancias en paralelo.** No es el contenido:
  la misma pieza renderiza bien al segundo intento. `render()` reintenta 3 veces y
  recién ahí revienta. Sin el reintento, la tanda se caía a mitad de camino y dejaba
  en disco una mezcla de piezas nuevas y viejas — que es peor que fallar del todo,
  porque parece completa. Por eso también conviene borrar la carpeta antes de una
  regeneración total.
- El auto-ajuste del template es la razón por la que se puede escribir copy sin
  contar caracteres. Si una pieza sale con la tipografía notoriamente más chica que
  sus hermanas, el copy es demasiado largo — acortarlo en vez de subir el piso
  del 62%.
