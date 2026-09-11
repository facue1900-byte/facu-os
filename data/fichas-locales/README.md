# Fichas de locales — Paseo Nordelta

Una ficha comercial por local vacío. Un JSON por local, dos piezas de salida:

| Pieza | Qué es | Para qué |
|---|---|---|
| `salida/<slug>.pdf` | 3 hojas A4 verticales | mandar por WhatsApp a un candidato |
| `salida/<slug>-story.png` | 1080 × 1920 | historia de Instagram, con o sin pauta |

```bash
/Users/Facu/facu-os/.venv/bin/python \
  /Users/Facu/facu-os/data/fichas-locales/build.py cafe pizzeria
```

Sin argumentos hace los dos. Para un local nuevo: copiar un JSON, cambiarle los
datos y correrlo con el slug nuevo. **No hay que tocar el HTML ni el CSS** salvo
que cambie el diseño.

## Las tres hojas

1. **Portada** — render a sangre, logo, el chip de disponibilidad, el título y
   tres datos de cabecera.
2. **El local** — los m² como números grandes, el plano, y seis puntos de lo que
   tiene.
3. **Dónde está y cuánto sale** — a la izquierda el plano general de Max con
   este local encendido, a la derecha las condiciones, y abajo el contacto.

## El ubicador

`plano_ubicador.py` toma `plano-general.pdf` (el `reunion facu-PLANTAS.pdf` del
arquitecto) y **lo copia tal cual**: no redibuja nada, sólo cambia el color.
Todo el predio baja a un trazo apagado sobre el negro del paseo, y el
rectángulo del local queda a full en Corten, con halo y marco.

Escupe dos versiones y `ubicadores.json` con dónde quedó el centro de cada
local en %, que es lo que usa la ficha para colgar la etiqueta:

| Archivo | Dónde se usa | Por qué |
|---|---|---|
| `img/ubicador-<slug>.png` | la historia 2 | el plano entero, que en 1080×1920 se lee |
| `img/ubicador-<slug>-zoom.png` | la hoja 3 del PDF | a 85 mm el plano entero no se lee: el local queda del tamaño de una uña |

**El rectángulo de cada local está a mano en `LOCALES`, y se verifica mirando
el recorte** (`page.get_pixmap(clip=rect)`) antes de darlo por bueno. Tiene que
entrar el local entero y nada del vecino. El plano numera **ambientes**, no
locales comerciales: el `LOCAL 9` del plano no es el "sector 9" del deck.

Qué es cada letra del plano, dicho por Facu el 11/09/2026:

| | | | |
|---|---|---|---|
| Cafetería | SALON 28 + OFICINA 29/30 + GALERIA + deck | Pizzería | LOCAL 13 + COCINA 14 |
| Futuro Fabric | LOCAL 11 + COCINA 12 | Heladería Shock BA | LOCAL 9 + COCINA 10 |
| BIGG | SALON 16/17 + COCINA 18 (el gris al costado es el Fabric de hoy, futura parrilla) | Wellness | GIMNASIO 3 |
| Market | SUPERMERCADO 1 | Los 7 de servicios | la tira de LOCAL 2 |
| Salón multiespacios | SALON 32 | Oficinas | OFICINA 31 |
| Hamburguesería | LOCAL 8 + COCINA 15 | Astronomy | LOCAL 8 (centro-derecha) |
| Sin dueño | los dos LOCAL 8 del centro (contenedores) | Futuro lavadero | LOCAL 8 de arriba |

## Lo que el script NO hace

**No calcula plata.** Alquiler y expensas salen tal cual del JSON. Si un monto
no está confirmado, va la palabra en vez del número — como en la pizzería, que
dice "Según liquidación" porque nadie tiene cargada su expensa. Constitución,
regla 6.

## Chequeos

Antes de dar una pieza por buena, `verificar()` abre los archivos: el PDF tiene
que traer **3 hojas A4 verticales con texto adentro**, y el PNG tiene que medir
**1080×1920 exactos** y no ser una placa lisa. Los dos chequeos se probaron
rompiéndolos a propósito (una hoja de más, un `--window-size` cambiado) y los
dos cortaron con el mensaje correcto.

## Trampas ya pagadas

- **Nunca `--user-data-dir` en el Chrome headless**: cuelga el proceso para
  siempre en esta Mac. Es la misma trampa del skill `flyers`.
- **El punto de una lista no va como celda de grilla.** Con
  `display:grid` en el `<li>`, el texto suelto que sigue al `<b>` se vuelve un
  ítem anónimo, cae en la columna de 5 px y baja **una palabra por renglón**. El
  PDF salía ilegible y el chequeo de "hay texto" daba verde igual.
- **El plano lleva techo de alto.** Si crece libre empuja la lista fuera de la
  hoja y `overflow:hidden` se la come sin avisar.
- **El mapa se achica por el ancho, no recortándolo.** Los pines están en % del
  contenedor: un `object-fit:cover` los corre de lugar y el local queda señalado
  en el edificio equivocado.

## La fuente de cada dato

| Dato | De dónde salió |
|---|---|
| Café: 130 / 52 / 39 m², cotas | plano preliminar del Arq. Max Elewaut (`SECTOR CAFE - PLANTA`) |
| Café: $3.500.000 + $1.050.000 | tabla de precios de Facu, 11/09/2026 |
| Pizzería: 47,9 m², cotas 2,00 / 10,95 / 7,60 | proyecto validado, medido en `propuesta 16-07.pdf` |
| Pizzería: $2.250.000 | Facu, 11/09/2026 |
| Qué local es cada ambiente del plano | Facu, 11/09/2026 |
| La cafetería es el bloque de SALON 28 | el plano trae `9,60`, `3,45`, `5,95`, `GALERIA 13,00` y `Deck madera descubierto` — las mismas cotas que el plano del café de Max |
| Contacto | `paseonordelta@gmail.com` · @paseonordelta · Av. de los Colegios 160 |

## Abierto

- **La expensa del local chico de la pizzería no existe en ninguna fuente.** Las
  tres que hay son de otros locales. Hasta que Facu la cierre, la ficha dice
  "Según liquidación".
- 🚨 **Los m² de la pizzería no cierran entre dos planos del mismo arquitecto.**
  El plano general acota el bloque LOCAL 13 + COCINA 14 en 2,00 arriba, 7,13
  abajo y 7,30 de alto: **33,3 m²**, o ~40 m² sumando el semicubierto de 1,00 m.
  La ficha publica **47,9 m²**, medido sobre `propuesta 16-07.pdf`. Los otros dos
  dan 65,7 y 96,4 contra 88,3 y 123,7 — la misma proporción, distinto tamaño, así
  que **son dos plantas distintas, no un error de medición**. Hasta que Facu diga
  cuál rige, el número que sale a un tercero no está confirmado.
- **Frente de la pizzería: 7,60 · 7,30 · 6,60.** El dibujo validado mide 7,60; el
  plano general acota 7,30; la nota vieja del deck decía 6,60. Las fichas van con
  **7,60**, que es con el que cierra el área publicada.
- **La tipografía real es Neue Haas Display** y vive en el Desktop, que este
  proceso no puede leer (TCC de macOS). Se renderiza con Helvetica Neue, su
  pariente directo. Si algún día se puede leer la carpeta, se embebe y listo.
