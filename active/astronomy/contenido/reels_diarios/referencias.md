# Referencias que mandó Facu — PRIORIDAD sobre lo que encuentre el agente

Facu (29/10/2026): «acá te paso muchas ideas para plagiar y usar con nuestro contenido».
Se toma la estructura, el ritmo y el remate; el video, el audio y el texto son nuestros.
Cada vez que se usa una, anotarlo en `resumen.md` (cuál y cómo se adaptó) y, cuando haya
números, en `aprendizajes.md`. Una referencia que ya se usó 2 veces sin rendir, se deja.

## Lo que tienen en común casi todas (aprendido el 29/10)

- **Duran ~9 s.** Las nuestras del 28/10 duraban 17 s.
- **Un corte en cada golpe (o cada 2) del tema.** El golpe = 60 / bpm del tema (`temas.json`):
  a 128 bpm, 0,469 s; dos golpes, 0,9375 s. Usá `dur` múltiplos de eso.
- **El texto se arma palabra por palabra al ritmo**, grande y al centro → `carteles_beat` en el
  guion (ver el docstring de `armar_reel.py`).
- **Un remate simple** (juego de palabras, una orden, una sorpresa) y cierre con el producto.
- Varias van **sin voz**: el texto en el golpe ES el mensaje. Con este formato, la voz es opcional.

## Las referencias

| # | Link | Qué hace | Adaptación Astronomy | ¿Se puede hoy? |
|---|---|---|---|---|
| 1 | instagram.com/reel/Deyot_CAaeN (@yannikframes) | Arranca como un reel ajeno adentro de Instagram (interfaz a la vista), «sale» al selector de apps del iPhone, pasa por Safari y la calculadora, abre Fotos y la tarjeta se agranda al video real. Te hace creer que deslizaste vos. | Reel de un DJ que se equivoca → selector de apps → Safari «clases de DJ zona norte» → Fotos → The Bunker en el drop. | NO con el armador (hay que dibujar la interfaz del iPhone): lo arma el hilo principal aparte. |
| 2 | instagram.com/reel/DeW8LJXRiYH | «Heeee… Stop! Look at… this, this, this… aaand»: abre en un círculo chico, después un corte por palabra mostrando el espacio. | «Pará. Mirá… esto, esto, esto… y esto»: cabina, CDJs, monitores, neón, el set. | SÍ: `carteles_beat` + cortes de 1 golpe. |
| 3 | instagram.com/reel/De642CERisd (Sprinhaus) | «GIVE ME A SIGN» palabra por palabra sobre la vidriera, cortes de productos con signos, remate «GO BUY YOUR SIGN». | «DAME UNA SEÑAL» → cortes del estudio → «ESTA ES TU SEÑAL / VENÍ A MEZCLAR». | SÍ. |
| 4 | instagram.com/reel/DeSv-vwSuXY | Una notificación de Instagram («This can be a HOOK») y la persona juega con ella: la quema, la estira, la tira. | Notificación «Astronomy: tu clase de prueba te espera» y el profe la agarra y la tira a la consola. | NO: hay que filmar al profe actuando la interacción. Pedirlo. |
| 5 | instagram.com/reel/DewfNScOktt (joyería) | «MOVE YOUR THUMB to the beat» con un pulgar dibujado; cada producto entra en un golpe. | «MOVÉ EL PULGAR AL RITMO» → un detalle del estudio por golpe (jog, fader, pad, neón). | SÍ (sin el dibujo: el texto alcanza). |
| 6 | instagram.com/reel/De90x1LI9yD (open day) | Cartel escrito a mano que pasa por distintos lugares mientras se completa «PUT THAT PHONE DOWN AND COME TO OUR OPEN-DAY»; cierra con el flyer. | «DEJÁ EL CELULAR Y VENÍ A MEZCLAR». Ya probado con `carteles_beat` el 29/10: funciona. Mejor todavía con un cartel real filmado. | SÍ con carteles; el cartel real hay que filmarlo. |
| 7 | instagram.com/reel/DesgAIqJ_Ou (3 tendencias de carrusel) | (a) «Me da vergüenza pedirte… un Porsche. Pero [producto] sí me lo podés regalar» → se comparte como indirecta. (b) «Abrí la foto» estilo foto de WhatsApp de una sola vez → al deslizar, el producto. (c) «Se acaba el año y siento que no hice nada» → la mejor foto de cada mes. | (a) «Me da vergüenza pedirte un viaje a Ibiza… pero una membresía en Astronomy sí me la podés regalar» (cumpleaños, diciembre). (b) «Abrí la foto» → la cabina: «tu próximo set». (c) enero→octubre con fotos de clases y eventos. | (a) y (b) SÍ como reel (tomas fijas + `carteles_beat`). (c) cuando haya fotos de todo el año. |

## Para el próximo pedido de filmación (`pedir_filmacion.py`)

- Un **cartel escrito a mano** (cartulina blanca, marcador negro grueso) que alguien lleva por
  4–5 lugares del estudio: puerta, cabina, CDJs, sillón, neón. 2 s en cada lugar.
- El profe **haciendo como que agarra algo en el aire** frente a la cámara (para la notificación
  falsa, ref. 4): agarrarla, estirarla, tirarla. 3 tomas de 3 s.
- Material en Drive que mandó Facu el 29/10: `Material filmado/Clases/` y
  `Material filmado/Fer_astronomy/`: **clases reales**. Usar eso primero.
