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
3. **Dónde está y cuánto sale** — la aérea con el pin del local (los pines salen
   del mapa de 12 sectores del deck, que Facu corrigió a mano el 25/08/2026),
   las condiciones y el contacto.

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
| Pines del mapa | `data/presentacion-paseo/deck.template.html`, lámina 05 |
| Contacto | `paseonordelta@gmail.com` · @paseonordelta · Av. de los Colegios 160 |

## Abierto

- **La expensa del local chico de la pizzería no existe en ninguna fuente.** Las
  tres que hay son de otros locales. Hasta que Facu la cierre, la ficha dice
  "Según liquidación".
- **Frente de la pizzería: 7,60 m o 6,60 m.** El dibujo validado mide 7,60 y con
  ese número el área cierra en ~49 m²; la nota vieja del deck dice 6,60 para los
  tres locales y con ese número no cierra. Las fichas van con **7,60**.
- **La tipografía real es Neue Haas Display** y vive en el Desktop, que este
  proceso no puede leer (TCC de macOS). Se renderiza con Helvetica Neue, su
  pariente directo. Si algún día se puede leer la carpeta, se embebe y listo.
