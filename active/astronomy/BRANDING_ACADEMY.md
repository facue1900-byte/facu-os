# Identidad visual — Astronomy Academy

Fuente: **`AstronomyIDENTIDAD.pdf`**, propuesta final de **Lola Gallal y Annie Hoffer**,
julio 2025. Copia permanente en `~/Desktop/Productoras/Astronomy/Marca Astronomy/Branding/`, con las 10
páginas renderizadas en `paginas-png/`.

> **ESTA IDENTIDAD ES DE LA ACADEMIA. NO SE USA PARA EVENTOS.**
>
> Astronomy Academy y los eventos son mundos separados. Los eventos tienen su propia
> estética —parecida pero no igual— y además se producen fechas con marcas de terceros
> que no tienen ninguna relación con Astronomy. Nunca aplicar esta identidad a una pieza
> de evento sin que Facu lo confirme explícitamente.
>
> **Pendiente de confirmar:** la portada del PDF dice *"Astronomy Dominé"*. Existe además
> una cuenta publicitaria `CP - Astronomy Dominé` separada de `CP - Astronomy Academy`.
> Facu indicó que este manual es de la Academia; la mención a Dominé en la portada queda
> anotada por si hay que separar las dos identidades más adelante.

---

## Isotipo

Una **estrella de cuatro puntas que es, a la vez, una A**. El vértice de la A forma la
punta superior, el travesaño es el eje horizontal, y la pata se estira hacia abajo en la
punta más larga.

**No es simétrica y ahí está su carácter:** el eje vertical es mucho más largo que el
horizontal, y la punta inferior es la más larga de las cuatro. Las puntas nacen anchas y
terminan en filo.

Usos vistos en el manual: avatar de Instagram sobre negro, bordado tono sobre tono en
remeras negras, y marca de agua a gran escala.

## Logotipo

**ASTRONOMY** en caja alta, grotesca ancha, con mucho espaciado entre letras.

**El detalle que lo hace propio: la A no tiene travesaño.** Es una `Λ`. Eso lo conecta
con el isotipo y es lo primero que se pierde si alguien lo retipea a mano.

## Tipografías

| Rol | Tipografía | Pesos |
|---|---|---|
| **Primaria** | **Aktiv Grotesk** | Light · Regular · Medium · Bold |
| **Secundaria** | **Roboto Mono** | Light · Regular · Medium · Bold |

La mono no es decorativa: es la que sostiene los rótulos técnicos —coordenadas, marcas de
tiempo, etiquetas entre corchetes— que le dan el aire de instrumental astronómico a todo
el sistema.

> ### Cómo se resuelve Aktiv Grotesk en la práctica
>
> Aktiv Grotesk es de pago (Dalton Maag) y no está instalada. El sustituto es **Helvetica
> Neue**, que ya viene en la Mac: las dos son neogrotescas y se parecen mucho. Aktiv
> Grotesk nació justamente como alternativa a Helvetica, así que la sustitución es de las
> más fieles posibles.
>
> **Las 75 placas ya generadas usan Helvetica Neue + Roboto Mono, o sea que están en
> marca.** La plantilla `editorial.html` —la que se usa por defecto y la que las generó—
> siempre tuvo esa pila.
>
> *(Corregido el 28/07/2026: antes acá decía que las placas usaban Montserrat. Era falso.
> Montserrat estaba solo en `flyer.html`, la plantilla vieja de los estilos `foto` y
> `plano`, que no generó ninguna de las 75. Igual se cambió a Helvetica Neue para que las
> dos plantillas coincidan.)*
>
> Si algún día se compra Aktiv Grotesk, se cambia en un solo lugar: la variable `--grot`
> de cada plantilla.

## Paleta

| Color | HEX | RGB |
|---|---|---|
| Blanco | `#FFFFFF` | 255 · 255 · 255 |
| Negro | `#000000` | 0 · 0 · 0 |
| **Azul marino** | **`#180040`** | 24 · 0 · 64 |

Son **tres colores y nada más**. El azul marino es un violeta-azul muy oscuro y funciona
como acento, no como fondo general: el fondo por defecto es negro puro.

> **Corrección a lo que veníamos usando:** la memoria decía "negro/blanco + violeta" y la
> app viene usando un violeta bastante más claro y saturado. El violeta oficial de la
> Academia es **`#180040`**, mucho más oscuro. Antes de repintar la app conviene mirar si
> el violeta de producto es una decisión propia y deliberada o una deriva.

## Cómo se ve en Instagram (@astronomy.academy)

De la página 9 del manual, que muestra la grilla aplicada:

- **Fondo negro dominante.** La grilla se lee como un bloque oscuro continuo.
- **Fotografía de personas**, desaturada y de alto contraste. DJs, alumnos, el estudio.
  Gente real, no stock.
- **Titulares en caja alta**, grandes, ocupando el ancho: `BEHIND THE DECKS`,
  `UN DÍA EN ASTRONOMY ACADEMY`, `ASTRONOMY TRACKLIST`.
- **Rótulos mono chiquitos** en las esquinas, con datos tipo instrumento.
- El isotipo como avatar, blanco sobre negro.

**Frases de marca** que aparecen en el manual:
`WHERE THE UNKNOWN BEGINS` · `ETERNAL EXPANSION`

## Reglas heredadas que siguen valiendo

- **Sin emojis en piezas de marca.** En su lugar, rótulos mono en mayúsculas.
  *(Nota: la bio actual de Instagram sí tiene emojis — es una inconsistencia con el manual.)*
- Las piezas **no llevan precio en pesos**: con la inflación argentina un flyer con precio
  queda viejo en semanas.

---

## Para eventos, esto no aplica

Cuando toque trabajar la estética de eventos hay que partir de cero y con su propio
material. Lo único que se comparte con la Academia es que **ambas son de Astronomy**;
todo lo demás —paleta, tipografía, tono— puede y suele ser distinto. Y las fechas con
marcas de terceros no llevan nada de Astronomy.
