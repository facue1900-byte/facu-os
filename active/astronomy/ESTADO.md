# Astronomy — estado

Última actualización: 2026-08-09

Participaciones, ramas, equipo y objetivos: en el CLAUDE.md global. Acá va solo lo
operativo y lo que cambió.

## Dónde está todo

`~/Desktop/Productoras/Astronomy/` y `~/Desktop/Productoras/Puzzle/`

**La academia se gestiona con app propia**: `astronomy-members` (Next.js + Supabase +
Mercado Pago), **en producción en astronomyofficial.com**. Código en
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/`. El detalle vive en la memoria
(`membership-system-project`, `reconciliacion-pagos-sistema`, `egresos-sistema`).

## Datos que ya no son hueco (migrados a la memoria el 27/07/2026)

Fuente: la web y la app en producción (verificado 09-24/07/2026).

- **Membresías** (mensuales, ARS): Silver $143.520 / 250 créditos · Gold $195.600 / 360 ·
  Platinum $272.000 / 480 · Bronze $1 (secreta, para amigos, a mano).
- **Costos en créditos**: clase individual (DJ o producción) 60 · alquiler cabina/estudio 50 ·
  clase grupal 50 por alumno.
- **Regla central de créditos**: las membresías **acumulan** mes a mes; el Curso de DJ
  **renueva** (cada pago resetea a 240 = 4 clases). Los créditos vencen a los 3 meses.
- **Clases**: cancelación con menos de 24 hs no devuelve créditos y el profe cobra igual;
  con más de 24 hs devuelve y el profe no cobra. Anticipación mínima para agendar: 12 hs.
  Los dos umbrales son editables desde la app (`studio_config`).
- **Cobros**: suscripción por Mercado Pago + cargas manuales. `sales` es la fuente única
  de verdad de la plata; la comisión de José (closer) sale de ahí.

## Frentes abiertos

- **Dominé: el back office de una fecha quedó completo (09/08/2026).** Todo dentro de
  `/admin/eventos/<id>`, una hoja por pregunta. Mesas con sectores, comisiones
  escalonadas por RRPP, base de ventas filtrable, cortesías masivas pegando dos columnas
  del Excel, y las fechas que se apagan solas cuando pasan. Detalle y decisiones
  pendientes en la memoria (`retomar-mesas`).

  ⚠️ **Antes de pagarle una comisión a alguien, Facu tiene que confirmar cómo sube la
  escalera** (`alcanzado` vs `marginal`): con los mismos tramos y las mismas ventas dan
  números distintos.

  ⚠️ **Ley 9: nadie lo usó todavía.** El 18/08 se cuentan mesas cargadas y cortesías
  emitidas desde ahí. Si dan cero, el problema es adopción y no software.

- **Eventos** — lo que más duele: invitaciones. 1) conversión invitado → asistente,
  2) FOMO real, 3) influencers a bajo costo.

  **Puzzle: dos fechas analizadas end-to-end (27/07/2026).** Datos en
  `data/eventos/puzzle/` (gitignoreado: ~1.500 personas con mail, teléfono y DNI).
  Todo verificado contra el panel de Passline y contra los totales de la planilla.

  | | Abril (490638) | Junio (514816) |
  |---|---|---|
  | Entradas | 823 pers · $19.030.000 | 727 pers · $14.460.000 |
  | Mesas | 470 pers · $20.662.500 | 436 pers · $21.580.000 |
  | **Total** | **1.293 pers · $39.692.500** | **1.163 pers · $36.040.000** |
  | Ocupación (aforo 2.000) | 64,6% | 58,1% |

  Hallazgos accionables:
  - **La mesa vale 1,9x–2,5x la entrada** por persona ($43.963 y $49.495 vs $23.123 y
    $19.890). Las mesas son el 52% y el 60% del ingreso con ~37% de la gente.
  - **Cortesías curadas convierten 7,6x mejor**: en junio, las 391 que estaban en las
    planillas del Desktop entraron al 55,8%; las 262 sueltas, al 7,3%.
  - **Techo de precio de entrada: $25.000–$30.000.** Todo tier de $25k para abajo se
    agotó; de $30k para arriba quedó stock con días por delante. Idéntico en las dos fechas.
  - **El 74% entra entre las 2 y las 3 AM**, en una sola hora.
  - **Retención 22%**: de 633 que entraron en abril, 140 volvieron en junio. Esa lista de
    140 vale más que cualquier lista de RRPP y hoy no existe como activo.
  - **Vladimir Nadinic: 90 cortesías en las dos fechas, 0 validadas.** Cero es demasiado
    limpio para ser "convierte mal" — algo está roto (no se enviaron, link caído, o
    cargadas a un nombre que no las repartió). **Preguntarle antes de concluir.**
  - Junio colocó 37 de 46 mesas (80%) vs abril 43 de 45 (96%). Las 9 sin colocar no son
    plata por cobrar (Facu confirmó: no se vendieron o se regalaron), pero ahí hay más
    plata que en optimizar las cortesías.

  **Dónde vive el dato de mesas**: Drive de la cuenta `facu` (no `studio`), planillas
  `RompeCabezas - Master Plan` y `RompeCabezas 2.0 - Master Plan`, pestaña
  **`Ingresos/Mesas`, la tabla de abajo** (fila ~29 en adelante). El resumen de arriba y la
  pestaña del plano de mesas **no cierran** con el ingreso — no usar esas.

  Pendiente: escribir `wiki/eventos/`, que sigue vacía.

  **Backlog de la puerta (pedido por Facu el 08/08/2026, NO construido).** Lo pidió después
  de escanear de verdad con `/puerta` en modo avión. Va acá y no al código porque todavía no
  hay una fecha real que lo necesite — el 16/10 se valida con lo que ya está. Cuando se
  construya, arranca por lo de abajo, que es lo único que hoy le cuesta plata:

  - 🥇 **La mesa en la pantalla del escáner.** Es lo que más pesa: la mesa es el **52%–60%
    del ingreso** de una fecha de Puzzle y **el de la puerta hoy no sabe quién tiene mesa ni
    cuál** — se resuelve preguntando por radio o mandando a la persona a averiguar adentro.
    Número de mesa y sector al escanear elimina ese ida y vuelta, que es trabajo real de una
    persona, en la fila, con cola atrás.
  - 🥈 **Cortesías con color por tipo de invitado** (el caso concreto de Facu: rosa mujeres,
    azul varones para los ingresos de cortesía). Sirve para dos cosas distintas y conviene no
    mezclarlas: el **color del QR** en el flyer/mensaje, y el **color del veredicto** al
    escanear. La segunda es la que hace el trabajo en la puerta.
  - 🥉 **Color por tipo de entrada** (VIP dorado, etc.). Hoy el nivel ya sale grande y de
    texto; el color es el paso siguiente, para leerlo sin leerlo.
  - **Ver de un golpe si un QR está usado o no y de qué sector es** — parte está: el escáner
    ya dice YA ENTRÓ. Lo que falta es el sector.

  Ojo con el orden: los tres primeros suenan a diseño de QR y en realidad **el trabajo está
  del lado del escáner**, no del lado de la imagen. Un QR rosa no le sirve a nadie si el
  cartel del veredicto no dice "MESA 14 · SECTOR B".

  **El plano del salón al lado de las mesas (pedido por Facu el 10/08/2026, NO construido).**
  Textual: *"estaría bueno que te dé la opción de agregar una foto al lado de la enumeración
  de mesas… para tener a mano el mapa de las mesas del boliche, que siempre cambia dependiendo
  del lugar, y poder enumerarlas en base al número real de la foto"*.

  El trabajo que elimina está nombrado y es real: **hoy el número de mesa del sistema y el
  número de la mesa en el salón se hacen coincidir de memoria o mirando un plano en otra
  ventana.** Cada venue tiene su plano y cambia. Con la imagen al costado, numerar y asignar
  dueño se hace mirando una sola pantalla.

  Cuando se construya, tres decisiones ya tomadas por cómo está el modelo:
  - **La imagen es del EVENTO, no del sector ni de la mesa.** Un plano por fecha, porque el
    venue cambia por fecha. Va como `events.plano_url` o similar, al lado de `flyer_url`.
  - Sube al mismo storage que el flyer y se muestra **al costado de la tabla**, fija mientras
    se scrollea la lista (es una referencia, no contenido).
  - **No se intenta mapear coordenadas sobre la foto.** Eso es otro producto: acá el trabajo
    es *ver el plano mientras se numera*, no dibujar el plano.

- **La ticketera como producto propio, separada de la Academia (pedido por Facu el
  10/08/2026, NADA construido).** Es un **negocio nuevo**, no una función más: vender la
  ticketera a otras productoras. Pidió base de datos nueva, panel de comprador y panel de
  productora, y armarlo *"como si fuese algo nuevo con el mismo link"*.

  Flujo que pidió, textual y en su orden: (a) la productora se crea cuenta, (b) al crear el
  evento se genera **un ID y una contraseña únicos para los validadores de ESE evento**,
  (c) se sincroniza **una cuenta de Mercado Pago propia** para recibir los pagos, (d) un
  camino de datos para nombres, fechas, fotos, (e) recién ahí se crea el evento y después se
  cargan los públicos.

  **Método que pidió, y manda sobre cualquier plan:** *"vamos de a poco y vamos haciéndolo
  juntos, paso a paso, botón por botón… vos siempre preguntame después por un botón que
  quiero que aparezca y lo vamos armando juntos"*. **No se construye de corrido.**

  Lo que ya existe y no se reescribe (Ley 8): ticketera vendiendo desde el 07/08, carrito,
  design engine que saca la piel del flyer, QR, validador `/puerta` con modo offline, mesas
  con sectores, comisiones escalonadas, cortesías masivas, panel de RRPP por link privado.
  Todo eso es **de una sola productora**: lo que falta es el eje de *quién es el dueño de
  cada dato*.

  ⚠️ **Las tres decisiones que ordenan todo lo demás, sin resolver:**
  1. **Qué pasa con la Previa del 16/10**, que ya vende y tiene QR en la calle. Recomendación:
     no se toca, termina en la base actual; la nueva arranca vacía con la fecha siguiente.
  2. **Base nueva = proyecto Supabase nuevo** (sería el tercero, un negocio una base) o
     esquema aparte. Facu dijo "base de datos nueva".
  3. **Cómo cobra cada productora**: MP propio por productora (OAuth) vs Marketplace con
     split. Define si Astronomy se queda una comisión automática o factura aparte. **Es la
     decisión de plata del producto y todavía no está tomada.**

  ⚠️ **Y el conflicto con la Ley 9, dicho de frente:** Astronomy está congelado hasta el
  18/08 esperando el conteo de adopción. Esta obra no genera un peso de la Previa —genera
  plata sólo si hay **otra productora** que la quiera usar—. Antes de escribir la primera
  tabla: **¿quién es esa productora y cuándo es su fecha?** Sin nombre y sin fecha, es la
  idea más caras de las que hay anotadas.
- **Academia** — la app está productiva. Queda: pase de estética final (contra el demo
  aprobado), sitio público etapa 3, y decidir si se reemplaza Calendly por el booking
  nativo (ya está completo y listo).
- **Música** — Sin City: trío de Facu (@thefacu__), Vlado (@vladinicc) y Lucas
  Lanfranconi. Ver memoria `sin-city-proyecto-musical`.

## Pendiente de dato

- Nombre del equipo de pauta.

(Resuelto 27/07/2026: "Mateo Iní" y "Mateo Guini" eran la misma persona — confirmado
por Facu. El nombre correcto es **Mateo Guini**; ya está unificado en todos lados.)

## Pauta de Meta — abierto desde el 28/07/2026

**Acceso por API funcionando.** App `astronomy-ads` (ID 2994790630727835, tipo Negocios,
con API de marketing). Cuenta: `act_628045479472592` (`CP - Astronomy Academy`, USD).

**El token ahora es de usuario del sistema y no vence** (29/07/2026). El anterior era de
usuario, de 60 días, y se murió antes de tiempo: Facebook lo invalidó cuando Facu cambió
la contraseña (`OAuthException 190, subcode 460`). El nuevo sale del usuario del sistema
`facu-os` en el Business Manager, con `expires_at: 0` — no vence y no le afecta un cambio
de contraseña. Tiene asignados la página, las dos cuentas publicitarias, la app
`astronomy-ads` y la cuenta de Instagram.

> **Ojo con el rate limit** (`code 17`): subir las 75 placas de una deja la cuenta
> limitada varios minutos, y en ese estado la API devuelve **listas vacías sin error
> visible** si no se mira el campo `error`. Un conjunto con cero anuncios es un rate
> limit hasta que se demuestre lo contrario.

**Lo que se descubrió y contradice supuestos previos:**

- **El gasto real es US$442/mes**, no los US$157 que decía el archivo de finanzas. Faltan
  US$1.685 sin registrar en 13 meses, concentrados en 5 meses sin ninguna fila de pauta
  (ago/nov/dic-2025, jun/jul-2026).
- **La cuenta se degradó 5x en siete meses**: de 375 impresiones por conversación en enero
  a 1.995 en julio, con el CPM *bajando*. No son medios más caros: la audiencia dejó de
  responder.
- **La variable que separa buenos de malos conjuntos es la geografía**, no prospección vs
  remarketing. Los nombres de los conjuntos mienten: ninguno usa públicos personalizados.

**Cambios aplicados (mismo presupuesto, US$19,56/día):** radio 18→35 km · carrusel de
Modo Profesional (formato nunca probado en 35 meses) · variante de copy con gancho de
dolor · anuncio de búsqueda de profesores sacado del conjunto que vende cursos.

**Corriendo desde el 29/07/2026:** `modo-profesional | carrusel | square | dolor | v2 | jul-26`
(`120248150444820448`), con las 75 placas rehechas — una foto distinta por tarjeta y el
gancho en la primera. Los dos carruseles viejos, los de las fotos repetidas, quedaron en
pausa. Detalle del defecto y de los arreglos al generador: `LAB_NOTES.md`, 29/07/2026.

**La decisión de plata que quedó abierta, con fecha:** `3IntW2 Flyer Curso de DJ`
(`120245002157250448`) se lleva **el 72% del gasto del conjunto a US$2,58 por
conversación**, mientras `2IntW2 Curso de DJ` (`120248128929530448`) trae a **US$0,83**.
Mover esos ~US$90/mes compraría ~108 conversaciones en vez de 35. **No se pausó** porque
`2IntW2` tenía 18 conversaciones de historia, debajo del umbral de 20 de la regla
operativa: sería apostar US$90/mes a que un número chico aguanta al sextuplicar la
inversión. **Revisar cuando `2IntW2` pase de 30 conversaciones.**

**Reporte automático:** launchd `com.facu.reporte-pauta`, lunes 10:00 → `~/Desktop/REPORTE_PAUTA.txt`.

**Documentos:** `pauta/PLAN_PAUTA.md` (plan por producto) · `pauta/CAMBIOS_META.md` ·
`pauta/PLAN_CREATIVOS.md` · `pauta/GANCHOS_Y_CONTENIDO.md` (10 ganchos, 3 guiones, 10 CTAs).

### Pendientes de dato

- **Qué plataforma es el chatbot de WhatsApp.** Es lo único que falta para calcular la
  tasa de cierre sola (teléfono → `profiles.phone` → `sales.is_first`) y no depender de que
  nadie cargue nada a mano. Sin ese número, ninguna decisión de presupuesto tiene base.
- **Resultados reales de alumnos** para la prueba social. La sección quedó vacía a propósito.
- **Los videos de Modo Profesional.** Facu los va a pasar (29/07/2026). Van como creativo
  principal de ese producto: el video es el formato que la cuenta menos exploró en 35 meses
  y el que mejor le rinde a este público. Las placas quedan de banco de rotación.
- **Quién dicta Modo Profesional.** La tarjeta 4 del carrusel dice "te enseñan DJs que están
  tocando", genérico, porque no hay fuente. Las placas de `curso-dj` sí nombran a Pastrana y
  Guini. Con los nombres confirmados, esa tarjeta convierte mejor.
- **Si el manual de identidad era para Dominé** y no para la Academia (lo dice la portada).
- Presupuestos de `PLAN_PAUTA.md` escritos sobre US$157/mes: hay que rehacerlos sobre US$442.
