# MEMORIA COMPLETA — Facu (export para Antigravity)
Generado: 2026-07-13 · Fuente: Claude Code memory + CLAUDE.md global
Este archivo consolida TODA la memoria persistente para sincronizar con otra herramienta.

---

## INDICE

- [Membership system project](membership-system-project.md) — Astronomy credits/membership app: scope, decisions, demo status, Phase-2 needs
- [Astronomy brand](astronomy-brand.md) — palette (black/white/gold + cyan), 4-point star logo, aesthetic, photo library
- [Astronomy catalog data](astronomy-catalog-data.md) — exact memberships, prices, credits, professors
- [Public site vision](public-site-vision.md) — Etapa 3: new astronomyofficial.com (company home + Dominé/Academy split, footer, jobs form)
- [Finance report](astronomy-finance-report.md) — monthly financial report: data source, FX method, key figures (+US$8.575, rentable), artifact link
- [Contacts & links](astronomy-contacts-links.md) — official WhatsApp/IG/YouTube/SoundCloud/mail + per-professor Calendly links & credit costs
- [App color direction](app-color-direction.md) — violet (crown chakra), kill gold/yellow, white text; where to change it
- [Demo account](demo-account.md) — demo.gold@astronomyofficial.com login to showcase the members app
- [Pending features](astronomy-pending-features.md) — next-up: profes, ops panel, notifications (+ phone-OTP note)
- [App aesthetic rules](app-aesthetic-rules.md) — STANDING: left-align text in cards, uniform button/card sizes, no dup nav
- [Identidad de alumnos](identidad-alumnos.md) — la cuenta va a nombre del alumno con el mail del que paga (padres, empresas, typos)
- [Paseo Nordelta web](paseo-nordelta-web.md) — rebuild de paseonordelta.com para control total sin el hermano; proyecto en Desktop, dominio en GoDaddy
- [Paseo Nordelta app](paseo-nordelta-app.md) — PWA de finanzas (cobros/banco/impuestos/rentabilidad), base propia local-first, v1 con datos reales de junio 2026
- [Sin City proyecto musical](sin-city-proyecto-musical.md) — trío de electrónica (Vlado, Lanfran, Facu); kit de crecimiento House/Melodic + plan 90 días
- [E-commerce dropshipping](ecommerce-dropshipping-project.md) — proyecto nuevo aparte de Astronomy: mercado AR nacional, 3 productos elegidos, ~$500k pauta, landings creadas
- [Annie promo account](annie-promo-account.md) — annie hoffer = cuenta de diseño/promo, no tocar su membresía ni créditos
- [Reconciliación pagos (sistema)](reconciliacion-pagos-sistema.md) — cron: pull MP + reconcile subs + espejo unificado 4 pestañas; closer/comisión
- [Reglas clases/sueldo](reglas-clases-sueldo.md) — cancelación -24/+24hs → sueldo del profe; anticipación mínima 12hs para agendar
- [Ctas ctes import pendiente](paseo-ctas-ctes-import.md) — DIC'25/ENE'26 a importar, solapamientos y columnas por hoja ya verificados
- [Egresos sistema](egresos-sistema.md) — sección /admin/egresos + pestaña Egresos del sheet: sueldos, comisión MP real, gastos a mano
- [Atribución de pagos](atribucion-pagos.md) — REGLA: nunca matchear pagos por nombre parecido; usar ledger_aliases + payment_links
- [Regla de créditos](regla-creditos.md) — CENTRAL: membresías ACUMULAN, Curso de DJ RENUEVA; recalcular solo activos desde su primer pago
- [Estética sin emojis](estetica-sin-emojis.md) — STANDING: nada de emojis en la web; usar tipografía técnica (mono/mayúsculas/tracking) del Instagram


---

# CONTEXTO GLOBAL (CLAUDE.md)

# Contexto global — Facu

Esto se carga en todas mis sesiones. Es quién soy y cómo quiero que trabajes conmigo.

## Idioma

Hablame en **español rioplatense**, con voseo. Código, nombres de archivo, commits e
identificadores en inglés.

## Cómo trabajo

Manejo tres negocios en paralelo y mi cuello de botella es el tiempo, no las ideas.

- **Ideas concretas, no menús.** Si hay que elegir, recomendá una y bancala. No me tires
  cinco opciones para que decida yo.
- **Priorizá por plata.** Ante dos tareas, va primero la que mueve ingresos o evita una
  pérdida. Decímelo si creés que lo que te pedí no es lo que más mueve la aguja — pero
  hacé igual lo que te pedí.
- **Nada de trabajo de bajo valor.** Si algo se puede automatizar, automatizalo en vez de
  enseñarme a hacerlo a mano. Anotar pagos en un Excel es exactamente lo que no quiero
  estar haciendo.
- **Números en pesos y dólares.** Argentina: inflación y tipo de cambio importan. Si un
  cálculo cruza monedas o meses, decime qué tipo de cambio usaste y de cuándo.
- **Plata real = cero improvisación.** En cualquier cosa que toque plata (Paseo Nordelta,
  ventas de hacienda, reparto de ganancias) no estimes ni redondees sin avisar. Si te falta
  un dato para que el número cierre, pedímelo. Un número inventado ahí me cuesta caro.

---

# Los tres negocios

## 1. Astronomy

Tres ramas: **eventos**, **academia** y **música**. Es el negocio más complejo de los tres.

### Participaciones

**Astronomy** (toda la empresa):

| Socio | % |
|---|---|
| Blado | 35% |
| Facu (yo) | 35% |
| Benja | 15% |
| Lanfral | 15% |

**Puzzle** — solo para la rama de eventos, no aplica al resto de Astronomy:

| Parte | % |
|---|---|
| Astronomy | 50% |
| Lanfral | 25% |
| Benja | 25% |

En la práctica esto deja a los cuatro con 25% real en Puzzle.

> Cuando calcules reparto de ganancias, aclará siempre **sobre qué base** estás repartiendo
> (Astronomy entero vs. solo eventos vs. Puzzle). Confundir las bases da números mal.

### Eventos

Producimos eventos de **música electrónica**. Cada tanto nos asociamos con **Puzzle**, que
hace eventos de cachengue.

Mi día a día acá: hablar con productoras, buscar venues nuevos, DJs nuevos, oportunidades
de negocio, e invitar gente.

**Donde más me duele:** las invitaciones. Quiero mejorar tres cosas:
1. Tasa de conversión de invitado → asistente.
2. Generar FOMO real para que la gente quiera ir.
3. Conseguir gente de estatus alto (influencers) a bajo costo, con propuestas que les
   resulten tentadoras.

### Academia (Astronomy Academy)

**Membresías mensuales** donde los alumnos juntan **créditos**. Cada tipo de membresía tiene
sus propias reglas. Los créditos se canjean por:

- Agendar una clase de producción o DJ (individual, grupal u online).
- Alquilar el estudio de DJ o el estudio de producción (se pueden hacer ambos).

**Profesores:**
- Mateo Iní — producción y DJ
- Mateo Pastrana — producción y DJ
- Valen Frando — producción, **solo online**

**Soporte y diseño:**
- José Alugi — administración
- Annie — diseño
- Lola — diseño
- Equipo de pauta — *(nombre pendiente)*

### Música

Objetivo: producir canciones, armar sellos y armar EPs para ser reconocidos mundialmente.
Es la rama más de largo plazo de las tres.

---

## 2. Paseo Nordelta

Paseo comercial en Nordelta. Algunos locales operativos, otros en obra.

**Obra y gestión:** trámites municipales, permisos, autorizaciones, arquitectos. Demolición
de locales, y rearmado de todo — caminos, cables, proveedores, toldos, cemento,
constructoras.

**Operación y finanzas:**
- Cobro de alquileres y expensas
- Inversiones e inversionistas
- Recupero, plan de financiación, estimaciones de recupero de la inversión
- Seguimiento diario de la plata: efectivo, transferencia y banco — en pesos y dólares,
  incluyendo compra y venta de dólares

**Este es el negocio donde más miedo tengo de pifiarla.** Tratá los números de acá con el
cuidado que eso implica: sin estimaciones silenciosas, sin redondeos sin avisar, y
mostrando el cálculo cuando el resultado importa. La pregunta de fondo que quiero poder
responder siempre es si el negocio operativo cierra o no cierra.

---

## 3. Campos familiares — Chaco y Pergamino

Campos de la familia. Hoy trabajo casi todo sobre **Chaco**, en la parte operativa.

**Lo que hago:**
- Papeleo de **SENASA** para traslado de jaulas de animales
- Venta de vacas y novillos a frigoríficos
- Autorizaciones de venta, pases de provincia

**Lo que quiero:** eficientizar el tiempo de mi viejo, principalmente. Un plan de
automatizaciones alrededor de:

1. Conteos y negociaciones.
2. Precio de la carne del día: cuándo vender, a cuánto el kilo, qué porcentaje de desbaste,
   y qué conviene según todo eso junto.
3. Cuándo conviene vender una jaula de 32 novillos o 32 vacas.

**Restricción del contexto:** Chaco es una zona muy pobre. Cualquier solución tiene que
asumir conectividad mala, poca tecnología disponible en el campo, y gente que no va a usar
una app complicada. Priorizá WhatsApp, papel y planillas simples por sobre cualquier
sistema que requiera entrenamiento.

---

# Objetivos: próximos 3 a 6 meses

**Hacer la mayor cantidad de plata posible, mes a mes.** Y sacarme de encima las tareas de
bajo valor para poder usar el tiempo pensando en cómo hacer más plata.

Traducido a cómo me ayudás:
- Si algo genera ingresos este mes, va primero.
- Si algo me ahorra horas repetitivas, va segundo.
- Si algo es interesante pero no mueve ninguna de las dos, decímelo y dejalo anotado, no lo
  construyas todavía.

---

# Huecos por completar

Cosas que todavía no te conté y que van a hacer falta cuando lleguemos ahí:

- Reglas concretas de cada membresía de la academia (precios, créditos que otorga, vencimiento,
  costo en créditos de cada clase y de cada hora de estudio)
- Nombre del equipo de pauta
- Números reales de Paseo Nordelta: locales, alquileres, expensas, monto invertido
- Volumen de hacienda en Chaco y con qué frigoríficos operamos
- Cómo se gestiona hoy la academia (planilla, plataforma, papel) y cómo se cobran las membresías
- Situación de Pergamino, que hoy casi no toco


---

# MEMORIAS INDIVIDUALES



============================================================
## FILE: annie-promo-account.md
============================================================

---
name: annie-promo-account
description: annie hoffer es cuenta de promo/diseño — NO tocar su membresía ni créditos
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
---

**annie hoffer** (cuenta Gold en el app, con ~240 créditos) NO es una alumna que paga: es una **chica de diseño** a la que le dieron créditos + Gold para que **suba videos a Instagram del proceso de la web** (promoción/explicación en redes).

**Por qué:** al reconciliar membresías (julio 2026) su Gold aparecía "sin respaldo" (ni MP ni transferencia) y era candidata a baja. Facu aclaró que es promo.

**How to apply:** NO le saques la membresía ni le ajustes los créditos en ninguna limpieza/reconciliación. Excluila siempre. Igual que la cuenta de prueba de Facu (Facundo Estevez, platinum) — ver [[demo-account]].


============================================================
## FILE: app-aesthetic-rules.md
============================================================

---
name: app-aesthetic-rules
description: Standing UI/aesthetic rules for the astronomy-members app — apply to EVERY change
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a9298c9d-3a4c-464b-b6d1-d67668bf2896
  modified: 2026-07-22T16:16:26.667Z
---

Facu repeatedly corrects the same aesthetic issues. Apply these to EVERY UI change without being asked:

- **Typography alignment**: inside cards/forms, text must be LEFT-aligned. The global `.section` rule
  centers text (`text-align:center`), so form labels/checkbox rows inherit centering and look ragged.
  Always set `textAlign:"left"` on card/form containers (or the label wrapper) so checkbox + title + desc
  line up in a clean left column. This has been flagged on: notification prefs, rol editor, etc.
- **Buttons**: same width AND height across a group — pick the nicest-looking size and apply it to ALL
  (give them a fixed `minWidth`/`width` so different label lengths don't make them different widths, e.g.
  "Reprogramar" vs "Cancelar"). Consistent padding, consistent font-size. No mix of tall/short or
  wide/narrow buttons in the same row. This gets flagged repeatedly — CHECK IT on every button group.
- **Cards in a list** (stacked): force `width:"100%"` so they don't size-to-content and end up different
  widths (the global `.card{margin:auto}` + flex causes ragged widths otherwise).
- **Cards/tiles in a group**: equal size (use fixed width/minHeight or a grid that stretches), even if some
  end with empty space. Flagged many times (stats, cost cards, shared accesses).
- **No duplicate navigation**: never two buttons that go to the same place; each action → its own single page.
- **Nunca cortar palabras con guión**: `app/globals.css` tenía `p{hyphens:auto}`, que partía palabras
  en cualquier ancho ("acotada"→"acota-da", "eventos"→"even-tos"). Se arregló en la raíz (`hyphens:none`
  el 21/7/2026); antes estaba parchado solo para el footer. Si aparece un corte raro, mirar ahí.
- **Inputs y selects de un mismo formulario = mismo ancho**, con la unidad afuera como texto ("60 |min",
  "12 |hs") para que los bordes derechos alineen. Un `<select>` sin ancho fijo mide distinto que un
  `<input>` y queda escalonado (pasó en Horarios del estudio).
- **Match the existing style**: violet accent (members), teal (profe theme), amber (admin theme). Reuse
  existing classes (.btn, .card, .coord, .mono). Dark theme; keep contrast.
- **Notification badges clear once opened**: any count badge (the yellow/violet "N" next to a nav item —
  Postulaciones, Pagos, etc.) must DISAPPEAR after the user opens/views that section. Track a "seen" marker
  (e.g. a `seen` column marked on page view, or a last-seen timestamp) and count only UNSEEN items. Facu
  finds a badge that stays after opening annoying. Apply to every badge.
- **Collapsible histories/lists + regla de los 5 renglones**: CUALQUIER bloque que pase de ~5 renglones
  (historiales, listas largas, cards con párrafos + bullets, secciones de instrucciones) tiene que ser
  minimizable/maximizable (`<details>` con summary), para que no tape la pantalla. Facu lo pone a prueba:
  revisa TODO en cada pantalla, no solo lo que se pidió. Criterio de cuándo va abierto o cerrado:
  · **Bloque secundario** dentro de una pantalla con varias secciones (lo que ya no pide acción, config
    que casi no se toca, explicaciones) → **colapsado por defecto**. Ej: "Pagaron este mes", "Tarifas de
    profesores", "Cómo funciona", "Alquileres que cubriste".
  · **Contenido principal de una página dedicada** (un historial que ES la página) → `<details open={n <= 10}>`:
    abierto si es corto, colapsado si es largo. Ej: créditos a mano, bajas, postulaciones, detalle de métricas.
  · **Lo accionable NUNCA se colapsa** (ej. "Falta cobrar", pagos sin asignar): eso va siempre a la vista.
  · Explicaciones largas → párrafo corto visible + `<details><summary>Cómo funciona ▾</summary>` con el resto.
- **Colores del calendario (ClassCalendar)**: cada profe/recurso un color DISTINTO y fijo (PROFE_COLORS en
  lib/profes.ts). NINGÚN color puede ser `#ff6b81` — ese tono (var(--bad)) está reservado para FERIADOS, que
  además deben aparecer en la leyenda ("Feriado" rojo). Los alquileres de cabina/estudio se ven SIEMPRE
  ("de base") con su color; el toggle "Ver otros profes" muestra SOLO las clases de otros (no las mías).
- **NUNCA usar diálogos nativos del browser** (`window.confirm`, `alert`, `prompt` → el cartel feo
  "astronomyofficial.com says"). SIEMPRE un modal propio con la estética de la web (card oscura, botón
  violeta, botón cancelar). Vale para toda confirmación: cambiar de plan, comprar curso, borrar algo, etc.
  Facu lo flageó explícitamente — que no vuelva a pasar en ningún botón.
- **Cambios de suscripción = pagar primero, dar de baja después**: al cambiar de plan NUNCA cancelar la
  suscripción actual antes de que se confirme el pago del nuevo plan. Si el alumno no paga, tiene que
  quedarse con su plan actual. La baja del viejo se hace en el webhook, cuando el nuevo preapproval queda
  authorized. (Facu perdió su membresía probando porque se cancelaba antes de pagar.)
- **Acciones destructivas SIEMPRE con doble confirmación** (modal propio): salir de la sesión, borrar,
  dar de baja. El "Salir" del header está pegado a otros botones y se toca sin querer — usar
  `components/LogoutButton.tsx` (está en las 26 pantallas), nunca un `<form action={logout}>` suelto.
- **Scroll interno + Lenis**: la app usa **Lenis** (scroll suave) y se queda con la rueda del mouse a
  nivel de página. CUALQUIER contenedor con scroll VERTICAL propio (`overflowY:auto` + `maxHeight`:
  desplegables, listas, modales) necesita `data-lenis-prevent` + `overscrollBehavior:"contain"`, si no
  **no scrollea** y encima arrastra la página. Los `overflowX` (tablas) NO se ven afectados. Ya mordió
  en: PersonPicker, NotificationBell (campanita) y ProfeMessage. Chequear esto al crear cualquier
  desplegable nuevo.
- **Chrome ignora `autocomplete="off"` en campos llamados `email`** y les encaja su autocompletado
  encima. Si es un buscador propio (no un login real), el input visible tiene que llamarse distinto
  (ej. `buscar_email`) y el valor real va en un `<input type="hidden" name="email">`. Ver PersonPicker.
- **`.cal2-card` (card BLANCA) es SOLO para el flujo del alumno** (`/reservar`, SlotPicker,
  NativeAgenda), donde funciona como "ticket" claro sobre fondo oscuro. **Nunca usarla en /admin
  ni /profe**: choca con el tema oscuro y, como los estilos inline usan `var(--ink)` (casi blanco),
  el texto queda invisible sobre el fondo claro. En admin/profe va `.card` (oscura) de toda la vida.
  Pasó en CargaManualForm y AgendaManualForm — Facu lo flageó como "feo y no se ve".
- **Estado "seleccionado" NUNCA con `color-mix(..., transparent)`**: sobre las cards claras
  (`.cal2-card`) el tinte transparente deja ver el fondo claro y, como el texto es `var(--ink)`
  (casi blanco), la opción elegida queda INVISIBLE. Mezclar siempre contra el fondo oscuro:
  `color-mix(in srgb, var(--violet) 26%, var(--space-2))`. Pasó en CargaManualForm y AgendaManualForm.
- **Prefer step-by-step forms**: admin data-entry forms (carga manual, agendar a mano) should be clean,
  card-based and step-by-step (like the member booking flow / AgendaManualForm), NOT a dense grid of
  selects. Violet cards, one decision at a time. Facu flags dense forms as "feas".

**Why:** consistency is the #1 recurring complaint. **How to apply:** before finishing any UI edit,
re-check alignment (left inside cards), button sizing (uniform), and card sizing (equal). See [[membership-system-project]].


============================================================
## FILE: app-color-direction.md
============================================================

---
name: app-color-direction
description: "Facu's color direction for the members app: violet (crown chakra), no gold/yellow, white text"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

Para la app `astronomy-members` (y probablemente el rebrand general), Facu definió el 2026-07-13:

- **Fuera el amarillo/dorado** — "no nos representa". Antes el acento era `--gold #f2c14e`.
- **Acento = violeta potente, séptimo chakra (corona)**. Implementado: `--violet #8b5cf6` (texto/bordes, legible) + `--violet-strong #7c3aed` (fondos de botón). Usar violeta **solo en lo CLAVE** (CTAs, montos de créditos, precios, links) — el resto neutro. Buscar minimalismo.
- **Texto blanco** sobre el fondo oscuro (antes había negro ilegible). Body ya usa `--ink #eef1f8`.

**Cómo aplicarlo:** el sistema de color vive en `app/globals.css` (variables en `:root`). `--gold` quedó **aliaseado a violeta** para no tocar cada archivo; idealmente renombrar a `--violet` en una limpieza futura. Labels `.coord` pasaron a `--muted` por minimalismo.

**Pendiente:** el isotipo/logotipo (`public/brand/*.png`) es raster — si es dorado, hay que editar el asset para pasarlo a violeta/blanco (no se puede por CSS). Contradice parcialmente [[astronomy-brand]] (que lista gold+cyan) — este es el nuevo rumbo del app; confirmar si el rebrand aplica a toda la marca. La estética final completa (matchear el demo aprobado) sigue pendiente para el cierre.


============================================================
## FILE: astronomy-brand.md
============================================================

---
name: astronomy-brand
description: "Astronomy Academy visual branding — palette, logo, aesthetic for web work"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

Branding pulled from their site + Instagram (@astronomy.academy) on 2026-07-09.

- **Logo/isotipo:** a sharp **4-point star** (elongated points). Real asset: `Logos : Flyer/Isotipo/PNG/Isotipo Blanco.png` (white). Use this as the brand mark, not a generic dot.
- **Logotipo (wordmark):** "ASTRONOMY" in a geometric uppercase sans. Real asset: `Logos : Flyer/Logotipo/PNG/Logotipo Blanco.png` (white, huge 4320px, transparent). Use the PNG directly for the wordmark.
- **Typography:** their wordmark/IG font is a geometric sans → matched with **Montserrat** (embedded as woff2 data-URI in the demo, since Artifact CSP blocks font CDNs). If Facu says it's off, likely alternative is Poppins. They also own the **Amsterdam Four** script font (`Logos : Flyer/LogouOLD/Amsterdam_...`, .ttf, free-for-personal-use) used for the cursive neon/"Dominé" — available for script accents.
- **Base:** black background, white/minimal typography. Dark, cinematic, nightlife/club aesthetic.
- **Web/digital identity (Facu's preference, 2026-07-10):** black + white **minimalist**, accent **violet** ~`#a97fff`, used sparingly (eyebrows/labels in muted grey, not colored). This replaced an earlier gold-accent version. **Gold lives only inside the photos** (neon, mixers), NOT in the UI. Cyan/teal ~`#5ad7d0` is their graphic accent on IG (low-poly net) — secondary. Apply this violet-minimal palette to the real app's design pass too.
- Gold ~`#f2c14e` = physical brand (neon sign, gold Pioneer mixer). Violet ~`#b98cff` also a brand variant (violet isotipo, purple studio lighting).
- **Membership tier color-coding** (from their console images): Silver = platinum grey, Gold = gold, Platinum = black/chrome (violet accent in demo).
- IG bio tagline: *"Formamos DJs & productores desde cero · Cursos 100% prácticos en Nordelta · Comunidad real & sello propio."*

**Contact / social links (from their site):** WhatsApp `https://wa.me/message/JKQAETPAN6CNN1` · Instagram (academy) `https://www.instagram.com/astronomy.academy/` (main brand: `astronomy.oficial`) · YouTube `https://www.youtube.com/@AstronomyOfficial` · SoundCloud `https://on.soundcloud.com/mueVQ73X7hPadg9eA` · email `studio@astronomyofficial.com`.

**Events (real, in `Eventos/`):** Dark Mansion, Mansion (Dominé), Dome, Private Boat Party, Boiler Room (JET), Moonrise, Yacht Party. YouTube sets: "The Bunker" sessions (GUEVA, Natcheo) in `Astronomy Academy/The Bunker/`. Flyers use the Amsterdam script ("Astronomy Dominé").

Real photo library lives in the working dir: `Astronomy Academy/Material para contenido` (studio/CDJ/neon shots, incl. `Studio + CDJs Horizontal.JPG`, `Astronomy Studio + NEON.JPG`), plus `Eventos/` (event photos). Professor & membership photos are on the Squarespace site (Squarespace CDN). Note: many local files are `.HEIC` (convert before web use). See [[membership-system-project]].


============================================================
## FILE: astronomy-catalog-data.md
============================================================

---
name: astronomy-catalog-data
description: "Astronomy Academy exact memberships, prices, credits and professors"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

Exact data from astronomyofficial.com (as of 2026-07-09). Used in [[membership-system-project]].

**Memberships (monthly, ARS):**
- Silver — $143.520 — 250 créditos — DJ Delivery ilimitado.
- Gold — $195.600 — 360 créditos — DJ Delivery + acceso a tracks de otros miembros.
- Platinum — $272.000 — 480 créditos — DJ Delivery + tracks inéditos + oportunidad de tocar en eventos Astronomy.

**Credits redeem for:** clases DJ/producción (60 créditos/clase), alquiler de estudio/cabina, grabación de live sets, mezcla/mastering, Astronomy Starter Pack, DJ Delivery.

**Professors (60 créditos/clase each):**
- Mateo Pastrana — DJ & Producción, 22 — Progressive House & Melodic Techno — "versátil, experimental y teórico" — todos los días.
- Mateo Guini — DJ & Producción, 23 — House/Melodic/Progressive — "dinámico, groovy y atmosférico" — martes y viernes.
- Owners Of Time — Producción (online), 22 — Melodic House & Techno — "una CDJ más" — online, todos los días.

Membership card images on the site are Pioneer DJ consoles: Silver=silver controller, Gold=gold mixer, Platinum=black 4-CDJ setup.


============================================================
## FILE: astronomy-contacts-links.md
============================================================

---
name: astronomy-contacts-links
description: Astronomy Academy official contact links + professor Calendly links (from astronomyofficial.com/profesores)
metadata: 
  node_type: memory
  type: reference
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

Enlaces oficiales de Astronomy (sacados de `astronomyofficial.com/profesores`, 2026-07-13). Útiles para el footer del sitio nuevo ([[public-site-vision]]) y para la agenda ([[membership-system-project]]).

**Contacto / redes:**
- WhatsApp: https://wa.me/message/JKQAETPAN6CNN1
- Instagram: https://www.instagram.com/astronomy.oficial/
- YouTube: https://www.youtube.com/@AstronomyOfficial (canal tiene 3 live sets "The Bunker": `2PCthxoiSh8` Moncho Amaral AA004, `3mC0VKMk9j8` DØME AA003, `ePzC4q6O_zI` Free for All Ep1 — usados en el carrusel de `components/LiveSets.tsx` de Academy)
- SoundCloud: https://on.soundcloud.com/mueVQ73X7hPadg9eA
- Mail: studio@astronomyofficial.com

**Profes que se muestran en la agenda de la app (foto real bajada a `public/profes/*.webp`):**
- **Mateo Pastrana** — DJ: `calendly.com/d/cxxg-xc8-5cs/curso-de-dj-con-mateo-pastrana` · Producción presencial: `calendly.com/astronomy-academy/produccion-musical-presencial-con-mateo-pastrana`
- **Mateo Guini** — DJ: `calendly.com/astronomy-academy/curso-de-dj-con-mateo-guini` · Producción presencial: `calendly.com/astronomy-academy/produccion-musical-presencial-con-mateo-guini`
- **Owners Of Time (Valen Frando)** — SOLO Producción online: `calendly.com/d/cr39-d2h-r5y/produccion-musical-online`

Costos en créditos (por hora / reserva de 60 min): clase DJ o Producción = **60**; alquiler de cabina/estudio = **50**; clase grupal = **50** por alumno. El webhook los detecta por el nombre del tipo de reunión ("alquiler"/"grupal" → 50, resto → 60).

**Config de Calendly unificada (2026-07-13, vía navegador):** los 5 event types que usa la app (Curso DJ y Producción de Pastrana y Guini + Producción Musical Online de Owners of Time) quedaron todos con: **teléfono obligatorio**, **casilla "He leído y acepto los Términos y Condiciones de Astronomy" obligatoria**, y **sin redirect** (muestran la página de confirmación de Calendly, no astronomyofficial.com). Esto último es lo que permite que el "bonus" (cartel de confirmación in-app + descuento) se vea. Nota: la API de Calendly es de solo lectura para esta config → se editó a mano en el panel. Si se crean event types nuevos, hay que replicar estos 3 ajustes.


============================================================
## FILE: astronomy-finance-report.md
============================================================

---
name: astronomy-finance-report
description: "Astronomy Academy monthly financial report — data source, method, key figures, artifact"
metadata: 
  node_type: memory
  type: project
  originSessionId: c15b25e4-9e21-4d34-881c-2b29de259968
---

Facu pidió (2026-07-13) un **reporte financiero mensual** de Astronomy Academy. Ver [[membership-system-project]].

**Fuente de datos:** Google Sheet **"Finanzas - Astronomy Academy"** id `19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs`, owner `it@astronomyofficial.com`. Compartida como Lector con `facue1900@gmail.com` (la cuenta del conector de Drive MCP `41d4bf1c…`). NO es pública (CSV export da 401) → leer vía connector `download_file_content` con `exportMimeType text/csv` (devuelve **base64**, hay que decodificar). La hoja "base" son 810 movimientos (ene 2024 – jul 2026). Columnas: Timestamp, Amount, Select Currency (ARS/USD), Academy - Transaction Category (Ingreso/Egreso), Income Category, Expense Category, Descripción, etc.

**Método FX:** convertir cada movimiento a USD con el **dólar blue** (promedio compra/venta) del día de la transacción. Serie histórica de `https://api.bluelytics.com.ar/v2/evolution.csv` (curl funciona, 2011→hoy; blue 13/07/2026 ≈ $1.510). USD nativos → ARS con el mismo criterio. **Resultado operativo** excluye "Aporte de Capital" (financiamiento dueños) y "Retiro de Ganancia" (distribuciones), que van aparte.

**Cifras clave (ene 2024 – jul 2026, ~26 meses):**
- Ingresos operativos: **US$ 39.051 / $52,1M** · Egresos operativos: **US$ 30.476 / $40,7M**
- **Resultado operativo: +US$ 8.575 / +$11,4M (margen 22%) → RENTABLE**
- Capital aportado: US$ 3.665 / $4,7M · Retiros de ganancia: US$ 6.784 / $8,8M (ya recuperaron la inversión + US$ 3.119)
- Ingresos: Venta de Servicio, Venta de Curso, Membership = ~90%. Egresos: Sueldos ~46%, Otros, Suscripciones (US$4.850, en USD), Diseño Audiovisual, Pauta.
- Pico de acumulado oct-2025 (US$9.125), luego amesetó; varios meses en rojo en 2025-2026.

**Entregable v1:** Artifact estático (SVG a mano). Generador `scratchpad/gen_report.py`.

**Entregable v2 — LIVE (2026-07-13):** Google Apps Script web app (vive en el Google de Facu, lee los sheets en vivo, filtros por año, público). Archivos en `Astronomy/reporte-apps-script/` (`Codigo.gs` + `Index.html`, con copias `.txt` para pegar fácil). Deployado por Facu como web app (autoriza como facue1900@gmail.com; pantalla "Google hasn't verified" → Advanced → continuar → Allow). Para actualizar el código: repegar los 2 archivos y **Administrar implementaciones → ✏️ → Nueva versión** (mantiene la MISMA URL).

**Sync Mercado Pago → planilla (2026-07-14):** `reporte-apps-script/MercadoPago.gs` — Apps Script que trae los cobros aprobados de MP (`/v1/payments/search`) y los agrega a la hoja Finanzas como "Ingreso MP" (medio "Mercado Pago"), con la descripción etiquetada `MP:<id>` para dedup. Trigger diario (`crearDisparadorDiario`). Token va en Script Properties `MP_ACCESS_TOKEN` (producción, NUNCA en chat). `MP_SYNC_START` opcional (default = hoy, para no duplicar lo ya cargado a mano). **Requisitos:** la cuenta que ejecuta necesita EDITOR sobre la planilla (hoy facue1900 es Lector → hay que cambiarlo o correrlo desde it@). **Caveats reales:** MP solo tiene lo que pasó por MP (efectivo, subs USD, equipos, transferencias, retiros = manuales); y si el sync auto-carga ingresos, Facu NO debe seguir cargándolos a mano (doble conteo). Clasificación default "Ingreso MP" (configurable en `MP_INCOME_CATEGORY`).

**MERGE de 2 planillas (v2):** además de Finanzas, ahora lee **"Inversiones - Astronomy"** id `1-WquwJQgvsl0mXwdv1Hwz6LJaYMq2rH9S6d9kfR3PTI` (owner studio@astronomyofficial.com, compartida c/ facue1900) — historial **2023→2024** con la inversión inicial (equipos + obra del container). Estructura distinta: cols Person, Business Unit, Category(Ingreso/Egreso), Sub Category, Moneda, USD_Ammount, ARS_Ammount. Reglas del merge (decidido con Facu): **mergear todo + solo Academy** (filtra Business Unit=='Astronomy Academy', excluye Dominé/eventos y Retiro de Socios). Dedup por (fecha+moneda+monto) — Finanzas es la fuente primaria, Inversiones no duplica. **Clasificación en 4 buckets:** operativo, **inversión (Equipos/Acondicionamiento/Muebles/MIDI/Mejoras)**, aportes de capital, retiros de ganancia. El reporte separa la inversión del resultado operativo → panel "¿rentable a pesar de la inversión?" compara ganancia op acumulada vs inversión (equipos+obra). Filtros ahora: Todo/2023/2024/2025/2026. Charts: nombres de mes ("Ene 2024"), barras gruesas, todos los meses aunque vacíos, scroll horizontal.


============================================================
## FILE: astronomy-pending-features.md
============================================================

---
name: astronomy-pending-features
description: "Big features Facu asked for next on the members app (profes, ops panel, notifications) + specs"
metadata: 
  node_type: memory
  type: project
  originSessionId: a9298c9d-3a4c-464b-b6d1-d67668bf2896
  modified: 2026-07-23T04:17:27.460Z
---

Status of the 3 big features for `astronomy-members`:

1. **Perfil de profesores** — ✅ DONE (2026-07-15). `staff.professor_name` links a profe to their classes
   (matched via `bookings.professor`/`event_name` ILIKE). Set from the student profile role editor (master).
   `/profe` dashboard: agenda grouped by day + "mandá un aviso" (to their students via notify, or to all via
   announcement). Header shows "🎧 Mi agenda" for profes; profes w/o admin perms redirect /admin→/profe.
   class_booked notification fires from Calendly webhook. `hasAdminAccess()` gates real admin vs profe-only.
   Calendar: ClassCalendar (Lista/Semana/Mes, color-coded, "ver otros profes"). Admin generic calendar at
   /admin/calendario. Role separation done: login routes admin→/admin, profe→/profe, member→/member;
   header hides credits/Agendar for admin+profe; /member shows "vista previa" banner for non-members.

**Native booking system — COMPLETE (2026-07-15).** Individual + rentals (studio hours) + online
(Owners of Time/Valen, Discord link, not studio-bound, seeded Lun-Vie 14-19) + group invites
(slot_group_invites: invite partner → confirm → charge both) + cancel + reschedule (both individual and
confirmed group) + emails on book/cancel/reschedule/group + studio hours + auto AR holidays (cascade) +
per-profe colors. Admin: audit_log (staff activity ficha), users/alumnos merged into one Usuarios base with
⋮ menu (credits, block X days, warn, activate-membership-with-plan-picker, delete). Ready to replace Calendly
if Facu decides. Minor optional still pending:
phone-change SMS OTP (needs provider), profe self-service color picker (defaults exist), Etapa 3 public site.

(Old note, kept for context) Native booking BETA tables:
`availability` (weekly rules per professor_name), `availability_blocks` (blocked days), `slot_bookings`
(unique(professor_name,starts_at) prevents double-book). Profe sets availability at /profe/horarios;
students book at /reservar (beta, discreet link in /member). Slots via lib/availability.ts generateSlots
(Argentina UTC-3 fixed). bookSlot action: check balance → reserve slot → spend_credits → notify profe.
Native bookings merged into profe agenda + admin calendar. COST=60 fixed. Calendly stays the main flow
(Option 1) per Facu; this is Option 2 for future migration. Needs SQL: native_booking_schema.sql.

**Resource-based conflict model — DONE (2026-07-15).** Studio grew: DJ + Producción CAN run at the same time
IF different profe AND different space. Rules: a profe can't have 2 classes at once; no two DJ (one cabina)
nor two Producción (one estudio) at once; online (Valen) doesn't occupy space. Each `slot_bookings` row now
has a `resource` col (cabina|estudio|online). `lib/profes.ts`: classResource/RENTAL_RESOURCE/slotKey/
profeResources/resolveResource. `lib/slots.ts` generates slots per (provider × resource), keyed
`slotKey(name,res)` = `${name}||${resource}`. Enforced by partial unique indexes (SQL: slot_resource.sql):
`(professor_name,starts_at)` and `(resource,starts_at) where resource<>'online'`, both `where status in
('active','pending')` — which ALSO fixed the latent bug where a canceled row blocked re-booking.

**Base de métricas + premios — DONE (2026-07-15).** `/admin/metricas` (new permission `view_metrics`,
master auto). Source = slot_bookings (single source: individual, grupal, alquileres). `lib/metrics.ts`:
fetchMovements(filters: from/to/professor/type/resource/status) + computeStats (by type/profe/space/weekday,
credits) + computeRankings (streak/mostActive/explorer/ambassador/topProfessor, top 5) + movementsToCsv.
CSV download at `/admin/metricas/export` route; printable PDF report (light theme, window.print) at
`/admin/metricas/reporte` (components/PrintButton). **Premios/badges:** hidden by default; admin grants from
ranking rows ("Premiar" per student, or "Publicar top 5" per ranking) — on grant: upsert `awards` row
(visible=true) + notify (campanita) + email (brandEmail). Student sees badges on /member ("Tus premios").
Actions in app/actions/metrics.ts (awardStudent/publishRankingTop/hideAward); catalog lib/badges.ts.
SQL needed: awards_schema.sql. topProfessor rows have no user_id → shown but no premio button (could wire
staff user lookup later).

2. **Panel de problemas (ops)** — ✅ DONE (2026-07-15). `/admin/problemas` (gated view_payments):
   failed payments (payment_events.credited=false), negative balances, stuck group invites. Links to profiles.

3. **Sistema de notificaciones (campanita)** — ✅ DONE (2026-07-15). Tables `notifications` +
   `notification_prefs`. Bell in header (NotificationBell), prefs at `/cuenta/notificaciones`.
   Live triggers: payment_failed (MP webhook), group_confirm (Calendly webhook), class_reminder
   (send-reminders cron). class_booked type exists but fires only once profes are wired.

**Phone OTP note:** email change already uses Supabase's built-in confirmation link (secure). Phone-number
change confirmation via SMS code needs an SMS provider (Twilio etc.) — NOT set up. Interim: phone edits are
direct, or confirm via an email code. Decide provider before building phone OTP.

**Teléfonos de alumnos (2026-07-22, RESUELTO):** Teléfono clickeable → WhatsApp WEB (`web.whatsapp.com/send`, helper `waWebLink` en lib/links.ts) al lado de cada alumno en `/admin/cobros-mes`. (a) Se agregó campo teléfono OBLIGATORIO al registro (`app/registro` + `register()` en auth.ts, upsert a profiles.phone con service_role). (b) Se importaron 35 números desde la pestaña **"Clientes Julio"** de la Base de Clientes (col 3=email, col 4=tel) → matcheados por email a profiles. Pasó de 2/49 a 37/50 con teléfono. Los que faltan son members recientes que no están en esa planilla; el registro los captura de ahora en más. Facu quiere WhatsApp web, NO la app de escritorio.

**Ingresos — hueco cerrado (2026-07-22):** la compra de créditos sueltos por MP (`buycredits`) acreditaba pero NO se registraba como ingreso (su plan_id no existe en `plans`, que tiene FK). Ahora el webhook la guarda en `manual_payments` (kind unico, medio MP) para que aparezca en Finanzas. Nunca había pasado ninguna (0 casos), así que no hubo backfill. El resto de ingresos SÍ estaban OK: MP subs/membresías → sales; cargas manuales (efectivo/transferencia/curso/membresía/prueba) → manual_payments; ambos los lee la pestaña Finanzas.

**Bug arreglado (2026-07-22):** "Dar de baja" en Cobros del mes no pegaba — `reconcileSubscriptions` (cron horario) reactivaba a `authorized` a cualquiera con venta en 50 días. Ahora respeta la baja administrativa: solo reactiva si hay un pago POSTERIOR a la baja. Ver [[egresos-sistema]].

See [[membership-system-project]].


============================================================
## FILE: atribucion-pagos.md
============================================================

---
name: atribucion-pagos
description: NUNCA matchear pagos con alumnos por parecido de nombre — usar las tablas ledger_aliases y payment_links
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-24T16:21:18.791Z
---

Para saber de quién es un pago, leer `payment_links` (Supabase). NUNCA re-derivar el dueño de un pago comparando el nombre del concepto de la planilla con `profiles.full_name`.

**Why:** la plata histórica vive en la planilla con la persona escrita a mano y en formatos que cambian ("Segundo Pinto - Silver Member - Enero 2025", "Pago de Silver Member por Segundo Pinto", "Sofi (Caro Caruso/Alejandro Stojadinovic)", "Martin Bernardo" = Martin Cañeque, "Ary Juarez" = Aracely). El matching por parecido falla en las dos direcciones: pierde pagos que sí son de la persona y se cuela pagos que no — un "Comisión Brocca $3.750" entró como si fuera de Segundo Pinto porque comparten letras. Facu lo marcó explícitamente el 24/07/2026: "estamos dando vueltas con los cobros, tenés que grabarte la memoria de qué pago le pertenece a quién".

**How to apply:**
- `ledger_aliases` (alias_norm único → user_id) es la única fuente de cómo se escribe una persona en los registros de plata. El match es EXACTO contra esa tabla, nunca por substring ni fuzzy.
- `payment_links` guarda cada pago ya resuelto, con `fingerprint` = sha256(fecha|concepto|monto) para que una edición en la planilla entre como fila nueva en vez de tapar la vieja.
- Lo que no matchea queda con `user_id` null y aparece en la vista `payment_links_pendientes`. No inventar: se resuelve a mano y eso agrega un alias, así no vuelve a fallar.
- Vista `pagos_por_persona` para el total real de cada uno.
- Schema en `supabase/atribucion_pagos.sql`. Relacionado: [[identidad-alumnos]], [[reconciliacion-pagos-sistema]].


============================================================
## FILE: demo-account.md
============================================================

---
name: demo-account
description: Demo/showcase login for the Astronomy members app (email + password)
metadata: 
  node_type: memory
  type: project
  originSessionId: a9298c9d-3a4c-464b-b6d1-d67668bf2896
---

Demo account to show the members app without using the master/admin account:
`demo.gold@astronomyofficial.com` · password `Demo2026`.

Created during the membership build; not an admin (no back-office access). As of 2026-07-14
Facu asked to move it to **Platinum** (was Gold). See [[membership-system-project]] and
[[astronomy-catalog-data]] for plan credits (Platinum = 480 cr/mes, $272.000 ARS).


============================================================
## FILE: ecommerce-dropshipping-project.md
============================================================

---
name: ecommerce-dropshipping-project
description: "Nuevo proyecto de e-commerce/dropshipping de Facu (aparte de Astronomy): mercado, productos, presupuesto y assets ya creados"
metadata: 
  node_type: memory
  type: project
  originSessionId: 090bbe31-5ee1-4890-9b83-2deef1b17864
---

Proyecto nuevo de Facu (julio 2026), separado de Astronomy. Dropshipping. Carpeta: `/Users/Facu/Desktop/Facu/E-COMMERCE $$$/`.

**Decisiones tomadas:**
- Mercado: **nacional argentino** (proveedores locales / MercadoLibre / Tiendanube; sin aduana, en pesos, envío 2–5 días). Se descartó importar de China a AR y, por ahora, EE.UU. (queda para escalar).
- Presupuesto de pauta de prueba: **~$500k ARS (US$300–500)** para 2–4 semanas.
- Filosofía acordada: validar con lo mínimo → matar rápido lo que no da → escalar el ganador. Markup **3×** con el CAC (costo de ads) adentro; ROAS de equilibrio ≈ 1,6, objetivo 2,5–3. El +20% del plan original estaba roto.

**3 productos elegidos (yo se los elegí):**
1. Mini licuadora portátil — venta $29.900
2. Proyector galaxia/astronauta — venta $24.900
3. Masajeador cervical eléctrico — venta $44.900

**Assets ya creados por mí:**
- 3 landings HTML listas para hostear en `E-COMMERCE $$$/landings/` (1-licuadora-freshmix, 2-proyector-galaxia-nebula, 3-masajeador-aliviomax). Tienen slots marcados `⚠️ REEMPLAZAR` para reseñas reales.
- Artifacts: plan corregido, plan productos+marketing+pauta, guía de videos con IA.

**Límite importante:** NO puedo producir archivos de video (soy texto/código). Facu los hace con celular + CapCut + ElevenLabs (US$0) y opcional Arcads (~US$30). Yo hago todo lo textual: guiones, hooks, prompts.

**Riesgo que le marqué:** reseñas/stock inventados en landings = ilegal (FTC en US desde 2024, Defensa del Consumidor AR) + más contracargos + baneo de ads. Usar reseñas reales de primeros clientes.

**Pendiente:** confirmar proveedores/costos reales de los 3 productos (pedir muestra y probar los electrónicos), montar tienda (Tiendanube) + Mercado Pago, y producir los 9 videos (3 ángulos × 3 productos). Relacionado con [[identidad-alumnos]] no; es proyecto aparte.


============================================================
## FILE: egresos-sistema.md
============================================================

---
name: egresos-sistema
description: Sección de Egresos en la app + pestaña Egresos del sheet — registro de toda la plata que sale
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-23T19:41:56.832Z
---

Creado 22/7/2026. Antes el sistema sólo registraba ingresos; la pestaña Finanzas del sheet sumaba cobros y nada más, así que nunca se sabía cuánto quedaba de verdad.

**Qué hay ahora** (`/admin/egresos`, permiso `view_salaries`):
- Resumen del mes: Ingresos − Egresos = Resultado, + desglose "En qué se va" por rubro.
- Detalle con 4 fuentes: sueldos de profes pagados (`salary_payments`), sueldos de equipo (`staff_payments`), **comisión real de Mercado Pago**, y gastos cargados a mano (`expenses`: alquiler/servicios/publicidad/equipos/impuestos).
- Los egresos cuentan cuando la plata SALIÓ, no lo devengado.

**Comisión de MP**: `sales.amount` guarda lo que paga el alumno (`transaction_amount`), no lo que entra. Se agregaron `sales.mp_fee` y `sales.mp_net`; `syncMpFees()` en [[reconciliacion-pagos-sistema]] las rellena (corre en el cron horario sync-sheet). El fee es el egreso más grande después de sueldos.

**Sheet (Base de Clientes, id 1gj2JHtPqS8CGh2IdNa5vijCM3Zez9rNdFOudcRwFDKs)**: la web escribe estas pestañas de finanzas:
- "Finanzas" — ingresos (mirror). "Egresos" — egresos (12 meses).
- **"Finanzas WEB"** — ingresos + egresos de la web UNIFICADOS (auto, cada sync). Esquema: Fecha, Tipo (Ingreso/Egreso), Categoría, Concepto, Medio, Monto (egresos en negativo), Moneda, Nota.
- **"Finanzas (histórico)"** — volcado ÚNICO (no se re-genera) del sheet viejo "Finanzas - Astronomy Academy" (id 19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs), MISMO esquema. 821 filas (512 ing + 309 egr). Se cargó a mano leyendo el CSV del sheet viejo (via connector Drive) y escribiendo con la SA. Si el sheet viejo cambia, re-correr ese backfill.

Ambas hojas (histórico + WEB) comparten esquema para compararlas/mergearlas en el reporte. Facu decidió (2026-07-23, opción B) esto en vez de tocar el sheet del reporte directamente. Ver [[astronomy-finance-report]].

**Pagar sueldos desde la web / transferir por MP**: se decidió NO automatizar la transferencia. La API money-out de MP existe pero necesita aprobación especial y es compleja; no vale la pena. El flujo es "marcar como pagado" (registra el egreso) y la transferencia real se hace a mano.

Archivos: `lib/egresos.ts`, `app/actions/egresos.ts`, `components/EgresoForm.tsx`, `app/admin/egresos/page.tsx`, `supabase/egresos.sql`.

**Hub Finanzas (2026-07-23):** `/admin/finanzas` (`lib/ingresos.ts` + `lib/egresos.ts`). Split de permisos: el **RESUMEN de plata** (Ingresos/Egresos/Resultado neto + desglose por fuente/rubro + **listas minimizables de TODOS los movimientos** de ingresos y egresos) lo ve SOLO el GrandMaster (`ctx.isMaster`); la **parte operativa** ("¿está todo en orden?": nadie debe, nada sin identificar, egresos cargados + accesos) la ven todos los admin con `view_payments`. **Selector de período:** 12 meses + "Todo AÑO" + "Todo (histórico del sistema)". Motores refactorizados a rango: `resumenIngresosRango(admin,from,to)` y `egresosEnRango(admin,from,to,label)`. Nav: "Finanzas (resumen/estado)" arriba de "Plata que entra". **Renombre:** "Pagos" → **"Pagos a identificar"** (bandeja MP sin dueño) vs "Cobros del mes" (cuota mensual).

**Ingresos/egresos manuales ampliados (2026-07-23):** el form de `/admin/egresos` ahora tiene toggle **Egreso/Ingreso**. Categorías egreso nuevas: **Inversiones y mejoras**, **Retiro de ganancias** (además de alquiler/servicios/publicidad/equipos/impuestos/otro). Categorías ingreso: **Aporte de capital**, Otro ingreso. Todo va a la tabla `expenses` con su `category`; `esCategoriaIngreso(cat)` (aporte/otro_ingreso) decide si se lee como ingreso (lib/ingresos) o egreso (lib/egresos los excluye). NO hizo falta tocar la DB. El sync-sheet también suma los aportes al lado de los ingresos.

**Tablero unificado + dolarización (2026-07-23):** Facu pidió integrar TODO el histórico y ver el negocio dolarizado. Implementado:
- **`lib/fxBlue.json`** — serie del dólar blue (promedio compra/venta) por día desde 2023-06 (fuente bluelytics evolution.csv). `rateAt(iso)` en `lib/finanzas.ts` busca el día o el hábil anterior.
- **`lib/historicalMovements.json`** — 802 movimientos del sheet viejo "Finanzas - Astronomy Academy" ANTERIORES al corte, ya dolarizados (ARS↔USD con el blue del día). Es data ESTÁTICA en el repo (no tabla DB — el intento de crear tablas falló por la pestaña Supabase congelada, y además el histórico no cambia).
- **CORTE = 2026-07-01** (`CUTOVER_ISO` en lib/finanzas): antes → histórico (sheet viejo, 2024-01→2026-06); desde → sistema (sales/manual/expenses/sueldos/mp_fee). Junio 2026 está en ambos → el web se clampea a >= corte para NO duplicar.
- **`lib/finanzas.ts`** — motor unificado: `movimientos(admin,from,to)` (histórico JSON + web dolarizado), `serieMensual`, `totales` (ARS+USD), `porCategoria`, `rangoDe(sel)`. La comisión MP se atribuye POR MES (antes egresosEnRango la agregaba en 1 fila al final del rango → descuadraba el neto y el gráfico).
- **`/admin/finanzas`** (solo master ve plata): selector Todo/Año/Mes (desde 2024); 4 tarjetas (Ingresos, Egresos, Resultado neto, Neto de toda la historia) en ARS+USD; **gráfico de barras mes a mes** (`components/MonthlyChart.tsx`, SVG puro, verde/rojo, período resaltado); desglose por categoría; drill-downs "Ver todos los ingresos/egresos" con lista completa. Cifra clave: **neto histórico total = $9.085.440 / u$6.616**.
- **Criterio contable (respondido a Facu):** resultado por FECHA DE TRANSACCIÓN (cuando se cobró/generó), no cuando MP libera. El desfasaje de 35 días es tema de caja, se puede mostrar aparte como "por liquidar" (pendiente).
- **Sheets dolarizados:** "Finanzas (histórico)" (803 filas, one-time) y "Finanzas WEB" (auto en el sync, con Monto ARS + Monto USD) — egresos en negativo, mismo esquema, comparables.
**Ampliación tablero (2026-07-23 b):**
- **Inversiones - Astronomy** (id 1-WquwJQgvsl0mXwdv1Hwz6LJaYMq2rH9S6d9kfR3PTI) IMPORTADA: filtró Business Unit=="Astronomy Academy", fecha < 2024-05 (corte pre-Finanzas, sin duplicar), usa su USD/ARS propio. Sumó 183 mov (equipos Allen Heath/monitores/JBL + acondicionamiento container + muebles + MIDI ≈ inversión inicial). `historicalMovements.json` ahora = 985 mov (jun 2023 → jun 2026). Base64 en scratchpad/inv.b64.
- **Resultado OPERATIVO vs neto total:** `totalesOperativo()` en lib/finanzas saca aportes de capital, retiros de ganancia e inversión (equipos/obra/muebles/midi) → el número de "cómo va el negocio". Cifras "todo": operativo **+$13.740.648 / +u$10.248** (rentable), neto con TODO **+$4.219.321 / −u$1.658** (arrastrado por inversión+retiros). Se muestran las 4 tarjetas: Ingresos, Egresos, Resultado operativo, Resultado neto (con todo).
- **Panel "Inversión vs recuperado"** (`capital()` en lib/finanzas, matchers esInversion/esAporte/esRetiro): Se invirtió u$12.453 (equipos+obra u$8.788 + aportes u$3.665) · Se retiró u$6.784 · **Falta recuperar u$5.669**.
- **Desgloses:** top-6 categorías + `<details>` "＋ ver N más" (antes eran listas larguísimas).
- **Criterio contable confirmado:** por fecha de transacción. El "por liquidar" de MP se descartó (Facu se confundió, no va).
- "Finanzas (histórico)" sheet = 986 filas dolarizadas (con inversión inicial).

**Rediseño tablero (2026-07-23 c):** USD primario, pesos secundarios (chicos). Layout:
- Arriba de todo las **2 cajas clave**: (1) **Caja real hoy** = plata líquida = Σ ingresos − Σ egresos nominal en pesos ($4.219.321), en USD al blue de HOY (u$2.742, NO la suma de mov dolarizados). (2) **Inversión vs recuperado** (capital(): invertido u$12.453, recuperado u$6.784, falta u$5.669).
- Headline: resultado del negocio operativo histórico u$10.248 (+con-todo −u$1.658).
- **Filtro por año con flechas ‹ › + chips** (2023-2026) — reemplazó el `<select>` gigante que scrolleaba mal.
- **Resultado neto del filtro activo** (año o mes, aclarado).
- **Gráfico mes a mes (ene→dic del año)**: barras apiladas con las 4 patas — ingresos (verde, arriba) + egresos (naranja) + inversiones (azul) + retiro de ganancias (dorado) abajo. `serieAno`/`desglose4` en lib/finanzas. `components/MonthlyChart.tsx` reescrito: clickeable (link `?y=&mes=`), en USD.
- **Click en un mes → abre su detalle** (breakdowns top-6 + listas de movimientos), con "✕ cerrar el mes".
- Totales del año abajo del chart (ingresos/egresos/inversiones/retiros/neto).
- PENDIENTE que Facu quería "pensar juntos": la mejor forma del "resultado real del negocio". Hoy: caja real + invertido/recuperado + operativo. Abierto a iterar.

**Ajustes (2026-07-23 d):**
- **CAJA CORREGIDA:** daba $4,2M pero la real es ~$1,5M. NO había duplicados. Causa: el hub sumaba el MES EN CURSO (julio 2026), que tiene ingresos cargados pero egresos/retiros no, y encima MP retiene los cobros ~35 días. Fix: **caja = Σ movimientos AL CIERRE DEL ÚLTIMO MES COMPLETO** (excluye el mes actual) = $1.391.909 ≈ real. La tarjeta aclara "al cierre de {mes} {año}" + muestra el mes en curso como provisional. (Acumulado nominal por año verificado: 2023 −$3,98M · 2024 −$0,44M · 2025 +$6,67M · hasta jun-2026 = +$1,39M.)
- **CHART rediseñado (`components/MonthlyChart.tsx`):** full width (viewBox 0 0 1000 250, width 100%, preserveAspectRatio none, min-width 680, overflow-x auto) y las 4 patas como barras **una al lado de la otra** hacia arriba (no ingresos-arriba/egresos-abajo). Cada mes clickeable. Verificado: 12 meses × 4 series con sus colores.

**Base real + corte agosto (2026-07-23 e):**
- **FUENTE ÚNICA DEL HISTÓRICO = pestaña "Base" del sheet 19N6 (gid=1400774963)** — la SA ya tiene acceso. Es la base reconciliada de Jose (cols: Timestamp, Real Date, ARS_Ammount, USD_Ammount, Category Ingreso/Egreso, Sub Category, Descripción...). 1129 mov, 2024-01 → 2026-07. Acumulado ARS = **$1.697.328 ≈ caja real** (antes daba $4,2M por sumar el mes en curso web). `historicalMovements.json` regenerado desde esta base (USD viene del sheet). OJO: empieza 2024, así que NO tiene la inversión 2023 en equipos → "invertido" ahora es solo aportes de capital (equipos+obra u$0). Si Facu quiere los equipos, agregarlos a la Base.
- **CORTE_ISO → 2026-08-01** (`lib/finanzas`). El web toma la posta en AGOSTO. Caja = cumulative completo (se sacó el truco de "excluir mes en curso" y la mención de los 35 días — Facu dijo que NO retienen 35 días).
- **"Finanzas (histórico)" sheet = réplica EXACTA de la pestaña Base** (1130 filas, script vía SA, one-time). **"Finanzas WEB" arranca agosto** (sync filtra `CORTE_WEB=2026-08-01`; se limpió a mano).
- Bugs UI: scroll de detalle (data-lenis-prevent + overscroll contain) y toggle "ver más/ver menos" (CSS `.fin-det[open]`).
- **Reconciliación jun/jul:** Olivia Sanchez Dubini dada de baja (import no en la base). Aracely (=Ary Juarez, sí está) y Sofía (MP real) se dejaron.

**HISTÓRICO VIVO + inversión 2023 (2026-07-23 f):**
- **`lib/historico.ts` — el histórico ahora se lee EN VIVO** de la pestaña "Base" del 19N6 (gid=1400774963) con la SA (`readSheetValues` en gsheets.ts), cacheado 5 min (`unstable_cache`). Si Jose edita la base, el tablero se actualiza solo. Se eliminó `historicalMovements.json` estático. `lib/finanzas` refactorizado: `histMovs` es async.
- **CAJA = base "base" SOLA** = $1.697.328 ≈ real. NO se le suma el 2023: sumar todos los movimientos 2023 dejaba la caja en −$2,4M (la inversión inicial ya está hundida; la base "base" de 2024→ ya refleja la plata real).
- **Inversión 2023 (equipos+obra, u$7.772) = `lib/inversion2023.json`** (estático, del sheet Inversiones 1-WquwJQ que la SA NO puede leer; el 2023 no cambia). Se suma SOLO al panel "invertido vs recuperado" (const `INVERSION_2023` sumada en `capital()`), no a la caja/totales. Invertido total ahora = u$11.372.
- **"Finanzas (histórico)" sheet ahora se re-sincroniza HORARIO** desde el histórico vivo (se agregó TAB_HISTORICO al cron sync-sheet, 7 pestañas). "Finanzas WEB" arranca agosto.
- Selector de años: 2023→actual (rangoDisponible fijo, ya no depende del array).

**Moneda: PESOS primario (2026-07-23 g):** Facu se arrepintió del USD primario. Ahora **pesos grande + dólar al lado en violeta**, EXCEPTO el panel "inversión vs recuperado" (USD primario, pesos = USD×blue hoy). Caja/operativo/resultado neto/totales año/desglose/movimientos/chart → pesos. Chart usa ingArs/egrArs/invArs/retArs. Helpers `arsHoy(usd)=usd×blueHoy` y `usdHoy(ars)=ars/blueHoy`. Los pesos de montos que cruzan años (invertido, operativo, caja) van a valor de HOY (no suma nominal, que mezclaba pesos de años distintos = daban mal). Para los NETOS de un período, el dólar secundario = `usdHoy(netArs)` así peso y dólar coinciden en signo (antes 2025 daba −$397k / +u$44).
- **Aporte de capital = inversión en el estudio (aclaración de Facu):** son lo mismo, plata que pusieron los dueños. El panel "invertido" ya los suma (equipos+obra u$7.772 + aportes u$3.600 = u$11.372 = total que pusieron los dueños). Se SACÓ el "flujo" operativo que había puesto (mezclaba aportes con la operación, mal planteado). El resultado operativo (u$3.822) es la rentabilidad pura del negocio, APARTE de la plata de los dueños.
- **Waterfall (`components/WaterfallChart.tsx`):** cascada en el panel de inversión: Invirtieron u$11.372 → Recuperaron u$5.478 → Falta recuperar u$5.894. En dólares. (H achicado a 150.)
- **Operativo "sin sentido" — RESUELTO (2026-07-23 h):** mostraba $5,88M porque hacía doble conversión (dolarizado-al-momento × blue hoy). El número REAL de la base = **$3.925.613** (ingresos operativos $65.863.093 − egresos $61.937.480 / u$3.822 dolarizado). Fix: mostrar el NOMINAL de la base + la cuenta a la vista, así Facu lo verifica.
- **REGLA de moneda definitiva:** pesos = NOMINAL (lo que dice la base), dólar secundario = `usdHoy(pesos)` = pesos/blue hoy (mismo signo siempre, valor de hoy). En TODOS lados (caja, operativo, neto período, totales año). EXCEPCIÓN: panel inversión/waterfall = USD dolarizado-al-momento (u$11.372, necesario porque el 2023 tiene inflación extrema), pesos = USD×blue hoy. NO usar dolarizado-al-momento en el resto (confunde).
- **Criterio de moneda DEFINITIVO por Facu (2026-07-23 j):** son DOS criterios distintos a propósito:
  - **Inversión vs recuperado + waterfall → DÓLARES** (dolarizado al día de cada transacción): invirtieron u$11.372 (equipos u$7.772 + aportes u$3.600), recuperaron u$5.478, falta **u$5.894**. La FALTA se muestra en dólares porque hay que recuperarla en dólares sí o sí; su peso va al **blue de HOY EN VIVO**. Pesos secundarios = USD × blue hoy. FilaCap y WaterfallChart → USD-primero. (Se revirtió el intento de ponerlo en pesos nominales.)
  - **Operativo + puente + caja + períodos → PESOS** (nominal del momento): operativo = ingresos−egresos $3.925.613; puente = operativo + aportes $4.631.116 − retiros $6.859.401 = caja $1.697.328. Los retiros dan distinto en el panel USD (u$5.478) vs el puente (pesos $6.859.401) A PROPÓSITO — distinto criterio para distinto fin.
- **Blue EN VIVO (`getBlueHoy` en lib/finanzas):** fetch a bluelytics `/v2/latest`, cacheado 1h (unstable_cache), fallback a la serie fija. El tablero usa este para las conversiones "a hoy" (arsHoy/usdHoy), así la falta-recuperar en pesos está activa 24/7.
- **BridgeChart = fila de números (2026-07-23 k):** Facu odió las barras (anchas, pixeladas por el preserveAspectRatio="none"). Ahora NO es SVG: es una fila HTML limpia — nombre arriba + monto grande abajo por paso, con operadores +/−/= entre medio, caja resaltada. "OPERATIVO $3.925.613 + APORTES $4.631.116 − RETIROS $6.859.401 = CAJA $1.697.328". (El WaterfallChart de inversión SÍ sigue siendo barras SVG, ese no lo criticó.)
- **Puente operativo→caja (`components/BridgeChart.tsx`):** mini-waterfall abajo del resultado operativo: **Operativo +$3.925.613 → +Aportes +$4.631.116 → −Retiros −$6.859.401 → =Caja $1.697.328**. Explica que la CAJA (todos los ingresos−egresos = $1.697.328) ≠ el OPERATIVO (solo operativos = $3.925.613); la diferencia son aportes(+) y retiros(−). Componente genérico de waterfall bridge (steps con delta + total).


============================================================
## FILE: estetica-sin-emojis.md
============================================================

---
name: estetica-sin-emojis
description: "STANDING — nada de emojis en la web de Astronomy; estética técnica del Instagram (mono, mayúsculas, tracking ancho)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-24T18:55:36.114Z
---

No usar emojis en ninguna parte de la web de Astronomy (headers, botones, títulos, cards). Se leen poco profesionales.

**Why:** Facu lo pidió el 24/07/2026: *"no usemos emojis tampoco, es poco profesional"*. La marca tiene una estética muy cuidada en Instagram y la web tiene que estar a la altura.

**How to apply:**
- En vez de un emoji, usar tipografía: rótulos en **mayúsculas, monoespaciada (`--mono`), con tracking ancho** (letter-spacing .14–.22em), como los rótulos del Instagram ("COMMUNITY-DRIVEN EDUCATION", "BUILT BY ARTISTS / FOR ARTISTS"). La clase `.coord` y `.nav-group-title` ya son ese estilo.
- Los símbolos geométricos de UI puros (☰, ✕, flechas →) están OK; los emojis a color (👋 🎧 ⭐ 👀 💬 ◆ como adorno) no.
- Al tocar cualquier pantalla, aprovechar para sacar los emojis que tenga.
- Relacionado: [[astronomy-brand]], [[app-aesthetic-rules]].


============================================================
## FILE: identidad-alumnos.md
============================================================

---
name: identidad-alumnos
description: "Convención para armar cuentas de alumnos cuando el mail no es del alumno (padres, empresas, typos)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
---

En Astronomy el mail con el que se reserva o se paga **muy seguido no es del alumno**: los padres reservan por sus hijos y algunos usan el mail de la empresa. Casos reales: Azul Haupt reserva con `corina@brandology.com.ar`, Sofia Caruso con `caruso.caro@gmail.com`, Ignacio Kertzman con `lv@mtgroup.com.ar`.

**Convención (definida por Facu, 16/7/2026): la cuenta va a nombre del ALUMNO, con el mail de quien reserva/paga.** Los mails alternativos se vinculan en `user_emails` y el `payer_id` de Mercado Pago en `user_mp_payers`; con eso los pagos futuros se reconocen solos.

**Why:** el mail es de quien maneja la plata, pero la ficha, los créditos y las clases son del alumno. Si se arma al revés, el alumno no existe en el sistema y sus clases quedan huérfanas.

**How to apply:** al migrar clientes o resolver un pago sin asignar, mirar el `student_name` de la reserva, no el mail. Ojo con los typos de Calendly (`caruso.caro@gmail.co` / `.cl`, `lairaemartinwz5`): son alias, no personas nuevas. Los inactivos se dan por perdidos y no se les arma cuenta. Ver [[astronomy-pending-features]] y [[membership-system-project]].


============================================================
## FILE: membership-system-project.md
============================================================

---
name: membership-system-project
description: "Astronomy Academy membership + credits system — scope, decisions, and demo status"
metadata: 
  node_type: memory
  type: project
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

Building a **membership + credits system** for Astronomy Academy (music school: DJ & production). Students pick a monthly membership, pay via Mercado Pago, credits accrue automatically, they book classes with a chosen professor, and credits are deducted automatically. See [[astronomy-brand]] and [[astronomy-catalog-data]].

**Decisions made (2026-07-09):**
- Approach: **demo visual first**, then wire the real backend.
- Payment: **Mercado Pago subscription** (automatic monthly rebill), not one-time.
- Credits: **accumulate but expire 3 months** after being credited.
- Scheduling: professor availability + **Google Calendar** integration (event created for student & professor on booking).

**Status:** Phase-1 interactive demo done. Demo simulates the whole flow client-side (localStorage), no real backend yet.

**Working file (source of truth Facu chose):** `/Users/Facu/Desktop/Productoras/Astronomy/Astronomy - Demo Membresias.html` — a self-contained HTML with all images/fonts embedded as data URIs. Edit THIS file directly for demo changes. Also mirrored to artifact `35e084c1-ed2c-44b3-b08e-b229acc4af33` (re-publish same URL to share a link). Note: the artifact viewer was flaky with the ~950KB inline page; the local file opens reliably by double-click.

**Etapa 2 progress (real build):**
- App lives in `/Users/Facu/Desktop/Productoras/Astronomy/astronomy-members/` — **Next.js 16.2** (App Router, TS, Turbopack, React 19). Node installed via **nvm** (v24 LTS); load with `. "$HOME/.nvm/nvm.sh"` before npm/node. Next 16 note: middleware→**proxy.ts**, `cookies()`/`params`/`searchParams` are async. Read local docs at `node_modules/next/dist/docs/` — Next 16 differs from training.
- **Supabase** connected (DB + auth). Uses NEW API key format (`sb_publishable_` / `sb_secret_`). Schema in `supabase/schema.sql` (profiles, plans seeded w/ real prices, subscriptions, credit_lots+credit_transactions, RPCs: credit_balance/grant_credits/spend_credits — grants expire 3 months). "Confirm email" disabled in Supabase for dev.
- **DONE:** registro/login/logout + dashboard showing real credit balance + plans. Runs on `npm run dev` (localhost:3000). Auth verified working.
- **Mercado Pago — BUILT & verified (2026-07-13):** `lib/mercadopago.ts`, `app/actions/subscribe.ts` (creates a **direct preapproval** — NOT preapproval_plan, which needs card_token — with `external_reference=userId:planId` + `notification_url`; returns MP init_point), `app/api/mp/webhook/route.ts` (grants credits on approved payment via `grant_credits` RPC, idempotent via `processed_payments` table — schema in `supabase/mp_schema.sql`), dashboard plan buttons wired to `subscribe`. MP TEST access token in `.env.local`. Account already had 157 historical subscriptions ("Silver Membership"). Verified: preapproval creation works + external_reference attaches to the payment (saw `e73…:silver` in MP) + webhook reachable + credit engine works (granted 250 via RPC). **Sandbox gotcha:** direct preapproval 500s with fake `@testuser.com` emails (use real-looking email); and "Both payer and collector must be real or test users" if you register the app account with a test-buyer email — can't fully approve a sandbox subscription payment with the real account's TEST creds. Final payment verification = small real charge at launch (or full test-seller+test-buyer sandbox setup).
- **Testing infra:** for local webhook testing, run dev server + **cloudflared** quick tunnel (`scratchpad/bin/cloudflared tunnel --url http://localhost:3000`) and set `NEXT_PUBLIC_SITE_URL` to the tunnel URL. Tunnel URL changes on restart.
- **Calendly / Agenda — BUILT (2026-07-13):** Facu ya tiene Calendly (plan pago) con 24 event types (servicios × profes). Token en `.env.local` (`CALENDLY_TOKEN`) — user URI `22def2ea-…`, org `909f21d2-…`. **NO se muestra el Calendly crudo.** Flujo guiado en `components/AgendaSelector.tsx` (client): paso 1 elegir profe → paso 2 DJ/Producción → paso 3 aparece SOLO el Calendly de ese event-type exacto (`CalendlyEmbed.tsx` usa `initInlineWidget`, se re-inicializa al cambiar url, prefill name+email del alumno). Profes en la app: **Mateo Pastrana** (DJ+Prod), **Mateo Guini** (DJ+Prod), **Owners Of Time = Valen Frando** (sólo Producción online). Fotos + links CONFIRMADOS sacados de `astronomyofficial.com/profesores` (fotos reales bajadas a `public/profes/*.webp`; links en [[astronomy-contacts-links]]). **Costos de crédito:** clases individuales 60, alquiler cabina/estudio 50, grupales 50 (detectado por nombre en el webhook). `app/api/calendly/webhook/route.ts`: `invitee.created`→`spend_credits` (idempotente por `calendly_invitee_uri`, marca `paid=false` si no alcanza en vez de romper); `invitee.canceled`→reintegra vía `grant_credits`. Tabla `bookings` + RPC `user_id_by_email` en `supabase/calendly_schema.sql` (Facu debe correrlo en SQL Editor). Firma opcional `CALENDLY_WEBHOOK_SIGNING_KEY`. Para activar en vivo: app con URL pública + `node scripts/calendly-webhook.mjs create` (crea la suscripción del webhook).
- **Baja de membresía — BUILT:** `app/cuenta/page.tsx` (Mi cuenta) con la baja escondida al fondo en DOS `<details>` anidados + confirmación; `app/actions/cancel.ts` cancela el preapproval en MP (status cancelled) y actualiza `subscriptions`. Nav ahora: Inicio · Agendar · Mi cuenta (`components/Nav.tsx`).
- **Migración de alumnos — EN CURSO:** planilla Google Sheet (gid 1245481228) leída por CSV export. 210 filas; **26 con créditos positivos** (los activos, total 18.572), 12 con créditos NEGATIVOS (Facu los revisa aparte), 207 con email. Detectado 1 duplicado (Maximiliano Aguirre 240+120→360) y 1 sin email (Rochi Mounier, queda afuera) → 24 cuentas a crear. `scripts/migrate.mjs`: modo `--test` (crea 1 cuenta con password temporal) ya corrido → alumno de prueba `facue1900+alumno@gmail.com` / `AstronomyPrueba2026`, 240 créditos. Modo `--all` (con email de invitación "creá tu contraseña") NO ejecutado — Facu quiere aviso antes de mandar mails. Para el envío masivo conviene SMTP propio (Resend). Créditos migrados también vencen a 3 meses.
- **DEPLOY A PRODUCCIÓN — HECHO (2026-07-13):** app publicada en **Vercel** (hobby, cuenta `facue1900-9658`, team `astronomyofficial`, proyecto `astronomy`). **URL 24/7: https://astronomy-eight.vercel.app** (alias estable). Deploy vía CLI con un **Vercel token** en `astronomy-members/.vercel-token` (gitignoreado en `.vercelignore` junto a `.env*`). Env vars en Vercel producción: Supabase url/anon/service, MP_ACCESS_TOKEN, CALENDLY_TOKEN, ADMIN_EMAILS, NEXT_PUBLIC_SITE_URL=la de Vercel. **Vercel Authentication desactivada** vía API (`PATCH /v9/projects/astronomy ssoProtection:null`). **Calendly webhook re-registrado** a `https://astronomy-eight.vercel.app/api/calendly/webhook` (el del túnel borrado) → créditos descuentan 24/7 sin túnel. Redeploy: `cd astronomy-members && TOKEN=$(cat .vercel-token) && npx vercel deploy --prod --token=$TOKEN --yes`.
- **NEXT:** confirmar fechas reales de eventos (orden /eventos tentativo); migración real de los 24; **MP producción** (hoy TEST, no cobra de verdad); apuntar `astronomyofficial.com` a Vercel (DNS en Squarespace); AESTHETICS pass; opcional conectar Vercel a repo git para auto-deploy.
- **Cancel/unsubscribe (Facu request):** the real app MUST allow cancelling the MP subscription, but keep the cancel button **hard to find** — tucked inside an "Mi cuenta" subpage, small, with a confirmation step. Deliberately not prominent so it's not too easy to unsubscribe.
- **AESTHETICS:** Facu wants a full design pass at the END (after all programming) to match the approved demo look — current app UI is intentionally basic. Don't polish until functionality is complete.

**2026-07-14 — big update (all live on astronomyofficial.com, custom domain now serves the Vercel app):**
- **MP PRODUCTION LIVE:** `MP_ACCESS_TOKEN` on Vercel now = production token (`APP_USR-…`, account nickname VLADIMIRNADINIC, MLA/AR). `NEXT_PUBLIC_SITE_URL` on Vercel updated to `https://astronomyofficial.com`. Real charges happen now. Production token also stored locally in gitignored `astronomy-members/mp-prod.env` (kept as backup; local `.env.local` still has TEST token so local dev doesn't charge). **PENDING:** `MP_WEBHOOK_SECRET` not set (webhook signature unvalidated) — LOW risk because the webhook re-fetches the payment from MP API and only credits if MP itself says approved; still, set it once Facu configures the webhook in the MP production dashboard. Recommended launch test: subscribe to the **secret Bronze $1 plan** to verify real charge → auto-credit → shows in /admin/pagos.
- **Payments visibility + auto-credit + failure alerts:** `payment_events` table (`supabase/payments_schema.sql`, RAN), webhook logs every payment (credited true/false), `/admin/pagos` view (green acreditado / red sin acreditar + filters), student hub shows next-charge date + credit expiry + red banner if last payment failed.
- **Plan change fixed:** `subscribe.ts` cancels the old MP preapproval before creating the new one (skips MP call for migrated `sheet:`/`demo` ids).
- **Bookings additions:** in-app cancel (Calendly API, refunds in the act) + embedded reschedule (no redirect); rentals (cabina/estudio) + group DJ classes added to `AgendaSelector`; "Tus reservas" mini-calendar + credit-movements history in hub; admin alumnos status now activo/**baja**/inactivo.
- **Group class invite flow (full):** A books grupal in Calendly + required question "email del compañero"; `group_class_invites` table (`supabase/group_schema.sql` — Facu must RUN) + `bookings.group_ref`; A pending until B confirms in-app (Confirmar/Rechazar in `GroupInvites.tsx`), charges 50 to BOTH only on confirm, cancels Calendly on reject. Expiry at **12h before class** (min-notice) via daily Vercel cron (`vercel.json`, hobby=daily) + expire-on-read in hub. **Penalty:** unconfirmed-at-expiry charges A 50 (blocked slot); **1st offense per student forgiven** with warning, then charged; both notified in hub. Calendly setup Facu must do: min scheduling notice = 12h on all event types; required "email compañero" question + keep grupal 1-on-1 on the 2 grupal event types.
- **Migration DONE:** 24 alumnos migrated (accounts already existed w/ random pw). Memberships assigned per new Google Sheet (gid 1434996738 "Active Clients"): Curso DJ→silver, plus Gold/Platinum per sheet. **Onboarding chosen: temp passwords via WhatsApp (Facu sends).** `scripts/set-temp-passwords.mjs` set temp passwords for the 24 never-logged-in students → list in gitignored `claves-temporales.csv`. Added "Cambiar contraseña" in `/cuenta` (`updatePassword` action). App still has NO forgot-password email flow (would need Resend/SMTP).
- **12 alumnos con crédito negativo** (from original sheet, all mostly "Curso DJ", multiples of −60): Flores, Rawson, Papazian, Brandan (−180); Ozores, Ibero (−170); Taborda, Nacucchio, Haupt (−120); Lopez Aufranc, Caneque, Juarez (−60). Facu investigating; decide if they start at 0 or keep the debt.
- **Bronze = SECRET membership** ($1, hidden from all public plan lists via `p.id!=="bronze"` filter, has `.tier-bronze` badge). `supabase/bronze_schema.sql`. Assign to friends manually by request.
- **App palette:** violet (crown chakra), gold/yellow killed — see [[app-color-direction]].

**Phase 2 (real build) — still needs from Facu:**
- Mercado Pago account + API credentials (never have him paste them in chat).
- Hosting decision. Current site `astronomyofficial.com` is **Squarespace**; membership app will likely be a standalone app linked from the site.
- Real system needs: auth per student, DB, MP webhook → credit wallet, Google Calendar API.

**Prices/credits are exact from their live site** — see [[astronomy-catalog-data]].


============================================================
## FILE: paseo-ctas-ctes-import.md
============================================================

---
name: paseo-ctas-ctes-import
description: Cuentas corrientes Paseo Nordelta — cómo se cobra cada local y qué falta para automatizar los cargos
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b70977d-f5a4-4025-981c-7a2f8c912611
  modified: 2026-07-22T15:37:06.999Z
---

Sistema de cuentas corrientes en **Ctas Ctes Paseo Nordelta - 2026**
(`10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`): hojas CONTRATOS + CARGOS +
CUENTA CORRIENTE, generadas por el Apps Script
`1gbqCLmRMBY-uA0Q61-Yce-bOc0NHPROQqxkTvqUyt7XVDZA2sSfkxjCD`. Todo se dispara desde
el menú **Ctas Ctes** de la planilla (el desplegable de funciones del editor no
responde; el menú sí).

**Import histórico: HECHO y verificado.** Dic-25/ene-26 (y feb-26 de Volta) traídos
del archivo 2025 `1UgoRtbM-LM-woGbI95f4zO206nm_LgHkdVNYCzPn0yo`. Deltas exactos.
Volta MAR'26 está en los dos archivos — no importarlo dos veces.

## Cómo cobra cada local (dicho por Facu, 22/7/2026)

- **Expensas y recupero varían todos los meses** y salen de la hoja
  **"Expensas Predio" del Master Plan** (`1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs`).
  Verificado: el total de la fila Peak One ($1.205.581) es exactamente su
  "Recupero de gastos" de JUN'26. La hoja **recalcula según la fecha que le pongas
  arriba**, así que el historial se puede reconstruir cambiando esa fecha (ojo: es
  una planilla viva y compartida, dejarla como estaba).
- **PERO el número calculado es una propuesta, no una decisión**: cuando viene una
  expensa de mejoras muy alta, Facu la parte en 2 o 3 cuotas. El generador propone,
  su edición manda. Conviene anotar "1 de 3 cuotas" en la columna Nota.
- **Bigg**: el alquiler va **mitad facturada con IVA y mitad en efectivo sin IVA**
  ("Diferencia Alquiler"). En jun-26 hay dos diferencias porque recuperó la de mayo.
  **Falta cargar la mitad en efectivo de julio** (~$1.910.387). Bigg es el único que
  debe efectivo hoy.
- **La Jaula**: tenían saldo a favor, recién se les cobra **desde agosto-26**. Los
  ~$12,6M cargados ene–jul son un estimado inventado y hay que borrarlos.
  NO usar la pestaña "Astor + La Jaula" del archivo 2025: es una pizzería vieja.
- **Salón (Alto)**: hoy **solo paga expensas**, sin alquiler.
- **Escuelita**: es un **% de facturación**, no lleva cargo generado; el ingreso
  entra solo por Movimientos.
- **Peak One**: sin alquiler propio, solo recupero + servicios de la hoja de expensas.
- Todos pagan **el mes siguiente** al que se les cobra, así que siempre hay ~1 mes
  en la calle. Eso no es deuda vencida.

## Pendiente (spec listo para ejecutar)

1. `generarCargosDelMes` debe leer **Expensas Predio** para recupero/servicios
   (mapeando nombres entre hojas) y la tabla de IPC de cada local para alquiler.
   Hoy lee CONTRATOS, que tiene valores fijos y desactualizados.
2. CONTRATOS necesita **dos líneas de alquiler para Bigg** (facturado + efectivo).
3. Corregir fichas: La Jaula desde ago-26 · Salón sin alquiler · Escuelita sin cargo.
4. Recién ahí correr **"Activar generación automática (día 1)"** del menú.

Ojo con `normPer_`: Sheets interpreta "2026-07" como fecha, por eso el dedupe del
generador compara períodos normalizados. Ver [[paseo-nordelta-app]].


============================================================
## FILE: paseo-nordelta-app.md
============================================================

---
name: paseo-nordelta-app
description: "App PWA de finanzas de Paseo Nordelta (cobros, banco, impuestos, rentabilidad) — base propia local-first"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b70977d-f5a4-4025-981c-7a2f8c912611
  modified: 2026-07-22T01:36:45.601Z
---

Facu pidió una **app para el teléfono que unifique todo lo financiero** de Paseo Nordelta (sheets, forms, facturas, banco, caja, inversiones, reportes, impuestos, IVA, rentabilidad). Relacionado con [[paseo-nordelta-web]] (mismo complejo) y con su hábito de construir apps ([[membership-system-project]]).

**Decisiones (jul 2026, vía AskUserQuestion):**
- **Base propia** (la app es el nuevo centro), no encima de los Google Sheets. Después se le suma sync/espejo a los sheets del contador.
- **v1 = Cobros + Reportes/Rentabilidad.**
- **PWA instalable** (no nativa).

**Ubicación:** `/Users/Facu/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/App Paseo Nordelta/`. Stack: Vite + React + TS + Tailwind v4 + Dexie (IndexedDB, local-first) + vite-plugin-pwa. Correr: `npm run dev` (localhost:5173). Publicar: `npm run build` → Netlify Drop / Cloudflare Pages (estático). Paleta de marca: negro cálido #171614 + off-white #f2ece1 + Corten #c4622d.

**v1 construido (4 pantallas, nav inferior):** Inicio (resultado del mes ARS+USD, margen, saldo banco), Cobros (facturado/cobrado/pendiente por local + detalle editable), Banco & Caja (libro con filtros), Impuestos & IVA (posición IVA, IIBB SIRCREB, Ley 25.413, AFIP).

**Seed de datos reales:** los 69 movimientos de **junio 2026** parseados del extracto Banco Macro cta 4-452-0960512147-9 (dirección ingreso/egreso deducida del delta de saldo). Reconcilia al peso: saldo cierre $4.119.498,46, ingresos $18.016.326, egresos operativos $12.587.947, neto +$5.428.379, impuestos banco $1.349.182 (IIBB 540.489 + Ley25413 191.477 + AFIP 617.216).

**Fabric y Bigg con valores REALES de factura** (leídas de los PDFs en `Facturas de Venta/2026/Mayo 2026/`, may/abr-26):
- Fabric (SUSHINOR, CUIT 30716663279): alquiler neto 7.500.000 (+IVA), gastos comunes 990.375 (+IVA), recupero 725.975 (NO gravado). Total a facturar $10.999.329/mes.
- Bigg (RODOLFO SRL, CUIT 30716281457): alquiler 50/50 → 1.750.000 con IVA + 1.750.000 diferencia sin IVA; gastos comunes 723.210 (+IVA); recupero 416.040 (sin IVA). Total $5.158.624/mes.
- **Clave fiscal:** el RECUPERO de gastos se factura como Nota de Débito NO GRAVADA (sin IVA); solo alquiler + gastos comunes llevan 21%. IVA débito mensual Fabric+Bigg = $2.302.353.
Modelo de Local ajustado a: alquiler, alquilerNoGravado, gastosComunes, recupero, cobraIva. El resto de los locales (Boss, Volta, Apex, Salón) siguen con **expensas ESTIMADAS** (flag `expensasEstimadas`, editables tocando el número) hasta tener sus facturas / la cta cte.

**Módulo CAJA / Efectivo (construido):** 5ª pestaña. Carga de efectivo por **lenguaje natural** en español rioplatense (`src/lib/parseCaja.ts`): "pagué 80mil al jardinero" → Egreso $80.000 Jardinería; "cobré 500mil escuelita" → Ingreso loc=escuelita. Parsea montos (80mil/500k/1,5M/"2 palos"/120.000), detecta ingreso/egreso por verbo, categoriza egresos por keyword y matchea locales en ingresos; lo dudoso lo marca "revisar". Botón **"Pegar de WhatsApp"** importa el chat entero (soporta formatos iOS `[12/6/26, 20:03] Nombre:`, iOS sin hora `[20/6/26]`, Android `12/6/2026 8:15 - Nombre:`, y fecha suelta `16/6`; sin fecha usa hoy). Saldo de caja = base editable ($4.370.000, cierre jun-26 s/memoria) + movimientos. Verificado end-to-end. Bug corregido: el `\b` tras vocal acentuada rompía la detección de verbos (regex sin flag `u`).

**Contexto financiero incorporado (memoria MEMORIA_Paseo_Nordelta.md que cargó jul-2026):**
- Master sheet ACTUAL = "Paseo Nordelta 2026 - Master Plan" `fileId 1ATiNBHCukPYPn9-poP1HO4SlfsDu5pGXsLz-JvW-IQs` (Movimientos gid 478887315, +col J=Resultado; pestaña Configuración col A=locales/col C=categorías es la lista maestra; dólar oficial F2). El fileId viejo `15SKKvr8…` quedó obsoleto.
- **Apex → renombrado "Peak One"** en el sheet. Locales: Fabric, Bigg, Heladeria, Hamburgueseria, Salon Multiespacios, Peak One, Beto/Meta Escuelita, Parrilla, Alquiler Cancha/Cumpleaños.
- **INVERSIÓN vs NEGOCIO:** aportes de capital (ingresos Local "Aporte de Capital" = Richi/Facu) y egresos categoría "Inversiones" NO son del negocio. Resultado del negocio jun-26 = +$5,4M (coincide con la app). Capital: Richi ~$150-161M, Facu ~$23M, invertido en obra ~$166M (obra financiada ~100% por socios).
- Tareas automáticas que ya tiene: conciliación día 10 (manda PDF branded a inversores re1900@gmail.com y facue1900@gmail.com) y sync-aportes-capital diario 7am. Reporte inversores en USD.
- Las transferencias salientes de jun ($11,2M "a categorizar") incluyen: TOSDE $1.149.538, NOREVENTOS $572.964, herrero $400.000, cuota VISA luces (~$306k → Inversiones), durlock/materiales, etc. Casi todo obra/proveedores/inversión.

**Caja real cargada + reconciliación (jul-2026):** Leí la pestaña Movimientos del Master Plan con el conector de Drive (`download_file_content` exportMimeType text/csv → base64; 409 filas, 288 de caja). Caja ARS neta acumulada desde ene-2026 = **$4.372.198** (= Saldo Actual del sheet; USD 0). Junio cerró la caja física en **−$173.814** (coincide con el inicio de julio del WhatsApp de Facu; el sheet daba −$172.716, dif $1.098 redondeo).
- **HALLAZGO: Facu le debe a Paseo $3.024.987.** Son aportes de Richi (8/7: 9M+6M+14M = $29.000.000) menos las cuotas de obra pagadas (1/3 derechos construcción $10.284.052 + 1/6 plan de pagos fondo $15.690.961 = $25.975.013). Ese sobrante entró en el banco PERSONAL de Facu (no MercadoPago) y es lo que le debe a Paseo.
- El sheet mete en "Caja" (medio) tanto el efectivo físico como los aportes de capital + pagos de obra (financiación de inversión que NO toca la caja física). Por eso el sheet-caja ($4,37M) ≠ caja física del WhatsApp de Mati. Regla de Facu: "todo lo que no sea por Banco Macro de la empresa cuenta como efectivo" (incluye MercadoPago).
- **Cargué el WhatsApp de julio como la caja física real** en la app (`src/data/caja-julio-2026.json`, 31 movs, base saldoCajaBase = −173.814). Saldo app = **$376.995** (corregido; vs WhatsApp corregido de Facu ~$377.596, dif $601 = redondeos en las corridas de Mati). El sheet tiene la caja cargada solo hasta el 8/7; el WhatsApp llega al 17/7.
- Correcciones que confirmó Facu: (1) el "faltante" de $300.000 del 10/7 era **error de anotación de Mati** — el WhatsApp está $300k bajo del 10/7 en adelante; se quitó el ajuste (por eso el saldo subió de $76.995 a $376.995). (2) **"Recibí de Richard" $1.710.000 = Peak One** (cobro del inquilino). **Apex fue renombrado a "Peak One"** también en el seed de la app (id sigue siendo "apex").

**Efectivo julio 10-17/7 cargado al Master Plan (jul-2026):** Facu eligió cargar el efectivo faltante directo al final del Sheet con fecha real. Se cargaron las 11 filas (10-17/7) al final de la pestaña Movimientos (fileId 1ATiNBHC…, gid 478887315) y se borró la fila suelta que había metido el Form. Estado final verificado: 421 filas de datos, "Sanitarios 10/7" una sola vez, sin fecha 18/7, col Mes autocompletada. Total caja física julio en la app = $376.995 (WhatsApp de Facu ~$377.596, dif $601 redondeo de Mati).

**Técnica para escribir/leer el Sheet vía Claude in Chrome (importante):**
- LEER en vivo (autoritativo): desde el navegador logueado, `fetch('https://docs.google.com/spreadsheets/d/<id>/gviz/tq?tqx=out:csv&gid=<gid>&t='+Date.now(), {credentials:'include'})`. El conector de Drive (`download_file_content` CSV) trae copia CACHEADA/vieja — no confiar para verificar escrituras.
- ESCRIBIR en masa: Name Box → primera fila vacía; `navigator.clipboard.writeText(tsv)` (TSV con \t y \n, columnas A-H, NO tocar col I ArrayFormula) + Cmd+V. Fiable. La col I (Mes) se autocompleta sola.
- El **Google Form** ("Paseo Nordelta", fileId 1ilw3XodJXkswLaqgAjmbFhN-Kf_KHNdNLmFDjtIigEk; response id 1FAIpQLSeON6Y8dfHddRx1g0dJRA3uXiyCg98G5JLI-ffzEPjkl1mABQ) es de 4 páginas (Tipo/Medio → Local o Categoria → Monto/Moneda/Obs; sin campo fecha, usa timestamp). POST directo al formResponse: Google devuelve 200 pero NO registra (anti-automatización de forms con login) — hay que llenarlo por UI. Y OJO: el Form **inserta la fila en el medio** (donde termina el bloque de respuestas), NO abajo de todo, porque las filas recientes se cargaron a mano debajo. Por eso conviene escribir directo al Sheet, no el Form.

**DECISIÓN GRANDE (jul-2026): la app pasa a ser la fuente de verdad con backend (Supabase).** Facu aprobó: la app es el único lugar de carga y sincroniza sola y prolija al Sheet (fila al final, fecha real, categoría exacta, sin romper fórmulas). Arquitectura: **una sola app responsive (teléfono + compu), con 3 roles** — (1) Facu "el TODO" (admin, ve todo), (2) Mati (solo carga de efectivo, pantalla bloqueada, reemplaza el WhatsApp), (3) Inversores (solo lectura + PDF mensual, puede vivir en link privado de la web). Fuentes que ingiere: efectivo, extractos Macro (PDF→concilia), facturas compra/venta (foto/PDF→OCR→IVA crédito), ARCA/VEPs, balances; y facturación de expensas por local. **Necesita de Facu:** cuenta Supabase, cuenta de servicio de Google (escritura al Sheet), API key de Claude (OCR). Diagrama de la visión mostrado con visualize.

**Backend Supabase (jul-2026):** proyecto creado por Facu, ref `wujutradczplokjrgmdo`, URL `https://wujutradczplokjrgmdo.supabase.co`. Corrió `supabase/schema.sql` (tablas profiles/locales/movimientos/facturas/config + RLS por rol + vista reporte_inversores + función mi_rol()). App conectada: `.env.local` (VITE_SUPABASE_URL + anon key eyJ…, claves públicas OK), `src/lib/supabase.ts` (@supabase/supabase-js instalado). Falta que Facu corra `supabase/seed.sql`. Bootstrap de usuarios: trigger `on_auth_user_created` crea profile (default inversor); Facu se hace admin con `update profiles set rol='facu' where email='facue1900@gmail.com'`. Pendiente: pantalla login + 3 vistas por rol + swap del data layer Dexie→Supabase + migrar los 421 movimientos del Sheet a Supabase.

**Diseño ciclo de vida de LOCALES (decisión jul-2026):** los locales NUNCA se borran (rompe el histórico de movimientos que los referencian); cambian de `estado` (activo / solo-expensas / saliente / cerrado / futuro). Todo editable desde la app por Facu, sin SQL. Casos: local nuevo → 'futuro' hasta abrir; se va → 'saliente'→'cerrado' (histórico intacto); cambio de inquilino en mismo lugar → local nuevo + viejo cerrado; renombrar → cambia nombre, id queda igual (por eso Apex→Peak One mantuvo id 'apex'); cambio de valor → editar vigente, el pasado ya quedó en movimientos. El sync (fase 2) debe reflejar altas/renombres en la lista Configuración del Sheet y el Form para no romper el Dashboard SUMIFS. Se agregaron campos `fecha_desde`, `fecha_baja`, `orden`. El `seed.sql` ahora incluye los 7 actuales + los futuros del rent roll (La Jaula, Cafetería, Fabric nuevo, parrilla, Shock Ba, Canchera, Comercio 1-6, Market) como 'futuro' con valores ESTIMADOS a verificar.

**App migrada a Supabase + login + roles (jul-2026, verificado):** La app dejó de usar Dexie (base local) y ahora lee/escribe en Supabase. Nuevos: `src/state/auth.tsx` (AuthProvider: session, rol, signIn/signUp/signOut), `src/state/data.tsx` (DataProvider: carga locales/config/movimientos de Supabase con realtime + funciones addMovimiento/addMovimientos/deleteMovimiento/updateLocal/setConfig, mapea snake↔camel), `src/pages/Login.tsx`, `src/pages/Inversores.tsx`. `main.tsx` = gate (sin sesión → Login; con sesión → DataProvider → app). `App.tsx` = nav por rol (facu: todas las tabs; mati: solo Caja; inversor: solo Reporte) + guardia que redirige. Todas las páginas (Dashboard/Cobros/Caja/Movimientos/Impuestos/LocalDetalle) usan `useData()`. `db/db.ts` y `data/seed.ts` quedaron como código muerto (no importados). Typecheck limpio, login renderiza sin errores en localhost:5173. Falta: correr `movimientos-seed.sql` (100 movs junio+julio) en Supabase; que Facu se registre en la app y corra `update profiles set rol='facu'...`; apagar "Confirm email" en Supabase para que el signup sea inmediato. Pendiente aún: migrar los 421 movs completos del Sheet (por ahora solo jun+jul), Mati/inversor usuarios, deploy, sync-al-Sheet (punto 2), OCR (punto 3). Endurecer: la vista reporte_inversores hoy es legible por anon — restringir a authenticated.

**App ANDANDO end-to-end (jul-2026, confirmado por Facu con screenshot):** login → Supabase → dashboard con datos reales. Los 100 movimientos (jun banco + jul caja) se cargaron a Supabase vía Claude in Chrome (Monaco `window.monaco.editor.getModels()[0].setValue(sql)` + Run; el clipboard writeText se colgaba por foco). Verificado: 100 movs, ingresos $31.891.826, egresos $27.718.693. Junio muestra Ingresos $18M/Egresos $12,6M/Neto $5,4M ✓. Facu es admin (corrió `update profiles set rol='facu'`). Nota: entró con contraseña pero le da fiaca — quedó pendiente ofrecer login passwordless (código por mail) + link privado para inversores. Realtime NO activado (hay que `alter publication supabase_realtime add table movimientos, locales, config;`) — por eso hoy hay que refrescar para ver cambios. App corre en localhost:5173 (dev), falta deploy para usarla desde el celular.

**Punto 2 — sync app→Sheet (jul-2026, en progreso):** Se descartó la cuenta de servicio de Google (pesada) por un **Apps Script web app** dentro del propio Sheet (`supabase/apps-script-sync.gs`): `doPost` recibe el movimiento y hace `appendRow` en Movimientos, mapeando local_id→nombre del Sheet (LOCAL_MAP). Facu lo deployó como Web App (Ejecutar como: él, Acceso: Cualquiera), URL `https://script.google.com/macros/s/AKfycbzkHrs9PsaTLfHt4bO-jOHuTaVEf-O9qTSBsZuoaIoh21ESa-BAhzpuJATBQgc9Uvem/exec`, token `pn-sync-7k2x9`. En vez de webhook de Supabase, se cablea **desde la app**: `.env.local` VITE_SYNC_URL + `syncSheet()` en `src/state/data.tsx` (fetch no-cors fire-and-forget en addMovimiento/addMovimientos). PENDIENTE VERIFICAR: al probar con curl las filas aparecían en gviz pero no persistían en la vista (Movimientos está **linkeada a un Google Form** → posible que appendRow no persista; también hubo mucho cache confundiendo). Falta que Facu cargue un movimiento real y confirme si aparece al fondo de su Movimientos; si NO, el arreglo es desvincular el Form o usar una pestaña propia. El editor de Apps Script se colgaba para la automatización (no dejaba seleccionar función en el dropdown).

**Feedback de Facu incorporado (jul-2026):** (1) las líneas de seguimiento del WhatsApp ("queda $X", "quedan", "inicio de caja", saldos pelados "-$253.414") se tomaban como gasto → arreglado en `parseCaja.ts` (se filtran; probado con su chat real). (2) doble-carga al apretar Cargar dos veces → guard `if(busy)return` + estado `busy`. (3) botón muestra "Cargando…" y queda deshabilitado mientras procesa. La carga por WhatsApp (copy-paste) le gustó mucho. Ambigüedad conocida sin resolver: "Pago beto escuelita" lo toma como Egreso (por la palabra "Pago") cuando es un cobro (Ingreso).

**Punto 2 CONFIRMADO ANDANDO + CRUD (jul-2026):** El sync de inserción SÍ funciona — se vieron en el Sheet (filas 425+) las cargas de la app (Bigg, Jardinero, Plomero, Osecac). La "desaparición" anterior era 100% cache de gviz/UI, NO el form-linkage. Se amplió a **agregar/editar/borrar**: cada fila lleva su ID de la app en la **columna K** del Sheet; el Apps Script (`supabase/apps-script-sync.gs` reescrito) maneja action insert/update/delete buscando por ID (`buscarFila`). App (`src/state/data.tsx`): addMovimiento/addMovimientos insertan con `.select("id")` y sincronizan con el id; deleteMovimiento sincroniza 'delete'; nuevo `updateMovimiento` sincroniza 'update'. Caja: tocar un movimiento lo edita (monto/categoría/flip tipo, prompts) y borrar pide confirmación. FALTA: Facu tiene que **redeployar el Apps Script nuevo** (Gestionar implementaciones → editar → Versión nueva; la URL no cambia). Ojo: las filas ya sincronizadas con el código viejo NO tienen ID en col K → el delete/edit solo aplica a lo cargado DESPUÉS del redeploy. Las entradas de prueba de hoy (Plomero/Jardinero/Bigg/Osecac, duplicadas por la doble-carga) están en el Sheet filas 422-429 (mis "test sync"/"PING" ya los borré) — confirmar con Facu si eran pruebas para limpiar ambos lados.

**Punto 2 CRUD sync FUNCIONANDO (jul-2026, verificado):** El bug de "editar duplica / borrar no borra" era el clásico de Apps Script: el web app corría la **Versión 1** (código viejo) aunque el editor tenía el código nuevo. Se redeployó la **Versión 2** (Deploy → Manage deployments → lápiz → Version: New version → Deploy; la URL /exec NO cambia). Probado con curl: insert con ID escribe en col K; delete por ID borra la fila exacta (buscarFila). El editor de movimientos en Caja ahora es un **modal propio in-app** (toggle Ingreso/Egreso, monto, categoría, nota, Guardar/Cancelar/Borrar) — se sacaron los `window.prompt/confirm` que a Facu le parecían engañosos, y la ✕ de la lista. Toda edición/borrado sincroniza al Sheet. IMPORTANTE si hay que redeployar el Apps Script de nuevo: SIEMPRE "Version: New version" o el web app sigue con el código viejo.

**Ajustes UX (jul-2026):** (1) La app abre en el **mes actual** (`period.tsx` default = new Date() → yyyy-mm) en vez de fijo "2026-06"; el selector (`App.tsx`) siempre incluye el mes actual aunque no tenga datos. (2) En **Caja** se separan los **aportes de capital** del día a día: `esAporte` = categoría empieza con "Aporte de Capital"; la lista y stats del mes son solo operativos (sin aportes); hay una sección "Aportes de capital · Privado" aparte que solo ve rol facu (Mati no la ve, y Mati solo tiene acceso a Caja). El saldo "Efectivo en caja" sigue incluyendo TODO (plata física real). El editor de movimientos (modal in-app) aplica también a los aportes. Los inversores ya tienen la vista "Reporte" (rol facu/inversor, Mati no accede).

**Migración histórico completo + página Análisis (jul-2026):** Se generó `supabase/migracion-2026.sql` (420 movimientos ene→jul 2026, `delete from movimientos;` + insert, origen 'sheet') con un script node que revierte los NOMBRES de local del Sheet a local_ids de la app (Fabric→fabric, Bigg→bigg, Hamburgueseria→boss, Heladeria→volta, Peak One→apex, Beto/Meta Escuelita→escuelita, Salon Multiespacios→salon, Parrilla→parrilla, Alquiler Cancha→lajaula, Cafeteria→cafeteria; "Aporte de Capital *" → categoria intacta, local_id null). 420 filas (Banco 121 + Caja 299, ARS 418 + USD 2). **Enviado a Facu para correr en Supabase** — la página Análisis depende de que esté cargado. Clasificador `claseMov()` en `src/lib/calc.ts`: Ingreso categoría "Aporte de Capital…" → 'aporte'; Egreso categoría "Inversiones" → 'inversion'; resto → 'negocio'. Nueva página **`src/pages/Analisis.tsx`** (ruta `/analisis`, link desde Inicio "Análisis mes a mes →", solo rol facu, no está en tabbar): 3 lentes (Negocio acumulado, Invertido en obra, Neto con inversión), lista mes a mes con acumulado corrido, y detalle filtrable por mes (ene→jul, tocá un mes de la lista o los chips) / medio (Banco/Caja) / clase (Negocio/Aportes/Inversión). Solo ARS (los 2 USD se excluyen). Typecheck limpio, compila sin errores (login renderiza). NOTA: `.claude/launch.json` de la app apunta al puerto 5173 pero `preview_start` lee el launch.json del cwd primario (Astronomy) — para previsualizar Paseo hay que `npm run dev` a mano y navegar a localhost:5173.

**migracion-2026.sql CORRIDA en Supabase (jul-2026, verificado):** Facu no podía correrla, la ejecuté yo vía Claude in Chrome (su sesión logueada en el SQL Editor de Supabase, proyecto wujutradczplokjrgmdo). Resultado verificado con query de control: **420 filas, Banco 121 + Caja 299, USD 2, desde 2026-01-12 hasta 2026-07-17, 7 meses** ✓. Ahora la app tiene el histórico completo ene→jul 2026 y la página Análisis funciona con todo. TÉCNICA que funcionó para cargar SQL grande (51KB) en el editor Monaco de Supabase: `navigator.clipboard.readText()` CONGELA el renderer (45s timeout) — NO usar. El `fetch` a un server local con CORS lo bloquea el CSP de Supabase (connect-src) — NO sirve. El Cmd+A/Cmd+V por teclado NO reemplaza el contenido (el paste no entra). LO QUE SÍ: partir el SQL en tramos (~140 líneas c/u), inyectar cada tramo como template literal (backticks) concatenando en `window.__s += \`...\``  (el SQL no tiene backticks ni backslashes ni ${), y al final `window.monaco.editor.getModels()[0].setValue(window.__s)` + click en Run. Supabase muestra un warning "Potential issue detected / destructive operations" por el `delete from movimientos;` — hay que clickear "Run query" para confirmar (es esperado, la migración borra y recarga todo).

**Vistas inversores + Mati/Caja mejoradas (jul-2026, verificado en Chrome):** (1) `src/pages/Inversores.tsx` reescrita — ya NO usa la vista `reporte_inversores` de la base (podía no coincidir con `claseMov`); ahora calcula directo de `movimientos` + `claseMov` (misma regla que Análisis, consistente). Muestra: Capital aportado ($173,4M / US$113.708), Invertido en obra ($166,9M / US$109.424), "obra financiada 96% con aportes", Resultado operativo acumulado (+$989.471 / US$649), y mes a mes con acumulado corrido + equivalente USD por mes. Todo en pesos con dólar de config. (2) `src/pages/Caja.tsx` ahora **agrupa los movimientos por día** (encabezado con fecha + neto del día), se lee como registro corrido — ideal para Mati; + resumen de "Hoy" en la tarjeta de saldo cuando hay movimientos del día. (3) Regla confirmada por Facu: egresos categoría "Inversiones" → inversión en obra; "Mejoras" y todo lo demás → negocio (ya era el comportamiento de `claseMov`, no hubo cambios). (4) Facu (admin) ahora puede **previsualizar** la vista de inversores: guard en `App.tsx` habilita `/inversores` para rol facu, y hay link "Vista de inversores →" en Inicio (Dashboard) junto al de Análisis. Typecheck limpio, las 3 páginas verificadas en localhost:5173 con datos reales.

**AUDITORÍA DE BANCO — reconciliado al peso contra extractos Macro (jul-2026):** Facu pidió rechequear todos los movimientos de banco porque le parecía raro ver meses en -18M (un banco no te deja saldo negativo). Se leyeron los 7 extractos reales de Banco Macro (`/Users/Facu/Desktop/Paseo Nordelta/Principio de mes/Resumen de Banco Paseo Nordelta/` — dic 2025 + ene-jun 2026 PDFs) con pypdf (NO hay poppler, el Read de PDF falla; usar `python3` + `from pypdf import PdfReader`). **RESULTADO: los datos de banco están PERFECTOS.** La cuenta operativa es **4-452-0960512147-9** (Cta Cte Especial en Pesos); abrió enero en **$0,00** y cada cierre de mes coincide EXACTO con la app: ene 8.735.090,49 → feb 131.413,71 → mar 3.951.045,25 → abr 7.744.498,97 → may 497.174,28 → jun 4.119.498,46. La cuenta operativa **NUNCA estuvo en negativo** (mínimos: may $32.815 el 18/5, jun $128.194 el 4/6). El "−18M" que veía Facu NO es un saldo — era el resultado/flujo mensual mezclado (o el neto del viejo dashboard que sumaba aportes+obra). Hay una 2da cuenta en pesos (3-452-0942483045-1, ~$5k, NO la seguimos) que sí tocó −306.055 unas horas el 2/6 por un pago de tarjeta Visa y se cubrió sola con transfer interna el mismo día (ese es el egreso "Transf interna SDO MISMO TIT 306.055 cubre VISA luces" del 2/6). El saldo real al 1/1/2026 era ~$5.158 (casi cero, en la cuenta 3-452 que no seguimos) → **el arranque de banco correcto es $0**.

**Dashboard/Inicio rehecho + arranques a 0 (jul-2026, verificado):** (1) `saldoCajaBase` en config Supabase puesto en **0** (antes -173.814 que era arranque de julio, mal con histórico completo). (2) SALDO_INICIAL de banco eliminado: era 497.174 (saldo 29/5) y con el histórico desde enero double-conteaba → ahora banco arranca en **$0** (`flujoHasta`). (3) `Dashboard.tsx` reescrito: sección "Plata disponible" con **Total (mix) / En banco / En caja** por separado (USD c/u); "Resultado del negocio · mes" usa el criterio negocio de `claseMov` (sin aportes ni obra, consistente con Análisis/Inversores); card "Movimiento del mes por cuenta" (Banco vs Caja net, separados). `mesActual()` ahora exportado en `period.tsx`. Typecheck limpio, verificado en Chrome: Total $7,5M / Banco $4,1M (=cierre junio, sin extracto julio aún) / Caja $3,4M. **OJO CAJA:** la "Caja" (medio) NO es la caja chica física — incluye aportes de capital en efectivo (Richi $29M el 8/7) y pagos de obra en efectivo (municipal $5,5M, cuotas derechos/plan $10,28M+$15,69M). Por eso da $3,4M y no ~$377K. La etiqueta del Inicio ya lo aclara. La caja-medio acumulada ene-jun = -172.716 (≈ el viejo arranque de julio -173.814, dif $1.098 redondeo) → confirma consistencia. **Facu confirmó (jul-2026) que el saldo de caja $3,4M ESTÁ BIEN, no hay que tocarlo ni separar caja-chica.** La diferencia es plata que Facu se quedó (la parte del aporte de Richi que entró a su banco PERSONAL) → figura en la caja de Paseo como lo que Facu le debe para dejarla al día. Es el mismo ~$3M del hallazgo "Facu le debe a Paseo $3.024.987" (ver más arriba). O sea: el número de caja es correcto, incluye ese préstamo pendiente de Facu; NO es un error.

**~~OJO — base de caja a reajustar~~ RESUELTO (jul-2026):** Facu decidió arranque = **$0**. Ya está puesto en 0 en config. (Ver bloque "Dashboard/Inicio rehecho + arranques a 0" arriba.)

**Hoja Banco rehecha (jul-2026, verificado):** `src/pages/Movimientos.tsx` mostraba TODOS los movimientos (banco+caja) mal etiquetados como "Banco Macro" — en julio se veían puros movimientos de caja porque no hay extracto de banco de julio cargado. Reescrita: **solo `medio==="Banco"` ARS**. Estructura estilo Caja: tarjeta "Saldo en banco" arriba (arrastrado desde $0, con USD y +/− del mes), sección "Mes a mes" con cada mes tocable (muestra neto + saldo al cierre; tocar setea el `periodo` global), y detalle del mes seleccionado agrupado por día. Título del header cambiado de "Banco & Caja" a "Banco" (`App.tsx` TITULOS). Verificado: saldos al cierre coinciden con extractos (ene $8,7M, feb $131K, mar $4M, abr $7,7M, may $497K, jun $4,1M); tocar Junio muestra solo cobros Fabric + impuestos del extracto, cero caja. Read-only (la carga de banco será por import de extracto, fase 2). Typecheck limpio.

**Preview "Ver como Mati" para Facu (jul-2026, verificado):** Facu preguntó si faltaba la página de Mati — NO falta, es la solapa Caja lockeada. Se agregó que Facu (admin) pueda espiar la vista de Mati sin desloguearse: `Caja` acepta prop `vistaMati` (fuerza `esMati` → oculta la sección "Aportes de capital · Privado"); nueva página `ComoMati.tsx` (banner "Estás viendo lo que ve Mati" + `<Caja vistaMati/>`), ruta `/como-mati` (facu-only en guard), link "Ver como Mati →" en Inicio (Dashboard) junto a Análisis/Inversores. Verificado en Chrome: muestra la Caja (efectivo $3.403.080, cargar, WhatsApp, registro por día) SIN aportes. NOTA: los egresos de "Inversiones" (obra en efectivo, ej. cuota $15.690.961) SÍ se ven en la Caja de Mati (son plata física que salió); si Facu quiere ocultarle también esos grandes pagos de obra, habría que filtrarlos aparte (hoy solo se separan los aportes de ingreso, no las inversiones de egreso).

**Usuario de Mati CREADO (jul-2026):** cuenta auth creada en Supabase (Authentication → Add user → Create new user, Auto confirm tildado). **mati@paseonordelta.com / clave temporal MatiCaja2026** (id 5f77f29e-5e9f-4616-b7e2-836f7062ba28). Perfil seteado con `rol='mati'`, nombre 'Mati' (upsert desde auth.users vía SQL editor). Verificado: rol=mati. Con ese rol solo ve la solapa Caja (navFor + guard en App.tsx). Facu tiene que pasarle las credenciales a Mati para que cambie la clave. NOTA: el SQL editor de Supabase estuvo MUY flaky esta sesión (páginas en blanco, Monaco no cargaba); funcionó abriendo una query existente (`/sql/<id>`) y reintentando setValue. NO extraer tokens de sesión de localStorage (el classifier lo bloquea, y está bien).

**PRÓXIMA FASE pedida por Facu (jul-2026):** ~~(1) Usuario de Mati~~ HECHO. (2) **Escaneo/OCR** de facturas, PDFs, fotos de tickets, extractos bancarios y PDFs de ARCA para **rechequear que IVA e Ingresos Brutos den igual que el extracto/ARCA**, distinguiendo factura A/B/C. Necesita: API key de Claude (visión/OCR), flujo de subida en la PWA, Supabase Storage, y lógica de parsing + validación contra los números ya cargados. Hay muchos PDFs ya en el proyecto (`Principio de mes/Facturas de Compra/`, `Impuestos del mes/`, `Resumen de Banco/`, `Recibos de Sueldo/`) para probar.

**CROSS-CHECK DE IMPUESTOS junio + página Impuestos arreglada (jul-2026, verificado):** Facu no puede pagar la API de Claude todavía → avanzamos el OCR sin key. Leí yo los PDFs de ARCA de junio con pypdf (`Principio de mes/Impuestos del mes/2026/Junio 2026/`): el **F.2083 Libro IVA Digital** (usar `extract_text(extraction_mode='layout')` para tabla limpia) da junio: VENTAS neto gravado $11.319.589 → **débito fiscal $2.377.113,69**; COMPRAS neto $8.834.719 → **crédito fiscal $1.850.407,58** (−NC $1.700,83 = $1.848.706,75). Posición IVA real ≈ **$528.407 a pagar**. El **CM (IIBB Convenio Multilateral CM03)** da determinado $939.730,57 (CABA $222.762 + BsAs $716.968), **a pagar $0** (cubierto por saldo a favor $434.135 + retenciones SIRCREB). HALLAZGO: la app mostraba IVA crédito=$0 (no cargaba compras) → sobre-estimaba el IVA. ARREGLADO: (1) `facturas` ahora se carga en DataProvider (`toFactura`, expone `facturas` + `addFactura`/`deleteFactura`, realtime). (2) `Impuestos.tsx` calcula IVA débito de facturas clase='venta' (si no hay, estimado rent roll) y crédito de clase='compra'; muestra posición real + flag "faltan compras" cuando no hay. (3) `sumaMatch` matchea categoría Y observación (los impuestos vienen como "Gastos bancarios" con detalle en obs) → ahora Ley 25.413 ($191.477), AFIP/cargas ($617.216), comisiones ($847) se desglosan bien. Total impuestos banco junio = **$1.349.182** ✓ (coincide extracto). Cargué en `facturas` 2 filas agregadas del Libro IVA de junio (contraparte '...(Libro IVA ARCA)') vía `window.supabase` (hook dev agregado en `supabase.ts`, guardado con `import.meta.env.DEV`, porque el SQL editor de Supabase estuvo imposible de cargar). OJO: esas 2 filas son AGREGADOS del Libro IVA — si después se escanean las compras individuales de junio hay que borrarlas para no duplicar (están tagueadas). Verificado en Chrome: junio muestra IVA a pagar $528.407 "coincide con DDJJ F.2083".

**Archivos de impuestos + recibos ORDENADOS por mes + IVA de todos los meses cargado (jul-2026):** Facu tiró ~44 PDFs sueltos en `Principio de mes/Impuestos del mes/2026/` y 5 recibos en `Recibos de Sueldo/` (dio permiso a mover). Ordenados con script python por patrón del nombre (`2026MM`, `MM 2026`, `MM2026`): Impuestos → 2026/{Enero..Junio} 2026 (Ene 2, Feb 3, Mar 10, Abr 17, May 9, Jun 3) + `2025/Noviembre 2025` (LID 202511) + `2025/Bienes Personales 2025 (anual)` (DJ BBPP + su VEP $150.000). Se corrigió carpeta mal nombrada "Abril 2025"→borrada, archivos a "Abril 2026". Recibos → `Recibos de Sueldo/2026/{Marzo,Abril,Mayo,Junio} 2026`. **IVA de los 6 meses extraído del F.2083 (pypdf layout, OJO el F.2083 usa PUNTO decimal, no formato AR)** y cargado en `facturas` (reemplazó los agregados de junio; 12 filas venta+compra tag '(Libro IVA ARCA)'). Posiciones mensuales: ene débito $0/créd $6.315.752 (a favor), feb $0/$3.825.652 (a favor), mar $2.094.401/$2.365.150 (a favor $270.749), abr $2.256.503/$2.325.974 (a favor $69.471), may $2.302.353/$2.547.482 (a favor $245.129), jun $2.377.114/$1.848.707 (**a pagar $528.407**). **HALLAZGO CLAVE: MAHNI tiene ~$10.726.753 de IVA a FAVOR acumulado a mayo** (compras de obra con mucho crédito, sin ventas facturadas ene/feb) → no paga IVA real, se absorbe con ese saldo. Se agregó a `Impuestos.tsx` la tarjeta "Saldo de IVA a favor (acumulado)" (suma débito−crédito de todos los períodos ≤ el actual). Verificado en Chrome (mayo: a favor mes $245.129, acumulado $10.726.753). Datos preliminares NO cargados aún (parseo regex dudoso, mejor con OCR visión): F931 cargas sociales SUSS (~$156k-$207k/mes), OSECAC (obra social), FAECYS (sindicato), CM/IIBB determinado (jun $939.730 a pagar $0; may ~$973.484 a pagar $0). Recibos de sueldo (MB = Matias Barbagrigia + SUELDOS/SAC junio) sin extraer aún.

**Escaneo/OCR — estado (jul-2026):** capa de datos lista (`facturas` en DataProvider + `addFactura`). FALTA (necesita API key de Claude que Facu no pudo pagar aún — el pago le da error): pantalla de subir foto/PDF, Supabase Storage, y una Edge Function que llame a Claude visión con la key (backend, NUNCA en el cliente) para auto-completar la factura (tipo A/B/C, CUIT, neto, IVA, total) y cruzar contra extracto/ARCA. Hay PDFs reales para probar en `Principio de mes/Facturas de Compra` (123), `Facturas de Venta` (19), `Resumen de Banco`, `Impuestos del mes`.

**Paginado "Ver 5 más / Minimizar" (jul-2026, verificado):** Caja y Banco (Movimientos) muestran los movimientos del mes de a 5 (estado `tope`, default 5). Botón "Ver 5 más (N restantes)" suma +5; "Minimizar" vuelve a 5. Header muestra "X de Y". El slice se hace sobre la lista plana ordenada y se reagrupa por día. Typecheck limpio, verificado en Chrome (Caja julio: 5→10 con botón).

**ACCESO PÚBLICO SIN LOGIN = auto-login como Mati (jul-2026, verificado):** Facu pidió sacar la pantalla de login y que el link sea público (para Mati). Implementado en `auth.tsx`: constante `MATI_PUBLIC = {mati@paseonordelta.com / MatiCaja2026}`; en el mount, si NO hay sesión → `signInWithPassword(MATI_PUBLIC)` automático → entra directo a la Caja sin login. Si la URL tiene `?admin` → cierra la sesión pública y muestra el Login (puerta de Facu para entrar como admin). Botón "Salir" oculto para rol mati (`App.tsx`, para que no se deslogue). Verificado en localhost: signOut+reload → entra solo como Mati (header "MAHNI · MATI", Caja, sin Salir, con filtro de meses); `?admin` → login. SEGURIDAD (clave): RLS protege — Mati solo lee/inserta movimientos `medio='Caja'` (banco, impuestos, facturas, inversores NO accesibles por el link público). PERO OJO: (1) los aportes de capital son medio='Caja' → un curioso que abra devtools en el link público PODRÍA ver los montos de aportes (Richi $29M etc.) aunque la UI los oculta; (2) la password de Mati queda embebida en el JS del cliente (extraíble); (3) cualquiera con el link puede AGREGAR movimientos de caja (insert). Blast radius limitado a la Caja. Si Facu quiere blindar los aportes del link público, hay que endurecer la RLS de Mati (pero rompe el saldo de caja que los incluye) — pendiente si lo pide. Requiere REDEPLOY del dist nuevo a Netlify para que el sitio live (lucent-buttercream-8ac45a.netlify.app) tenga el auto-login.

**Filtro de meses dentro de la Caja (jul-2026, verificado):** Mati no tiene el selector de mes del header (`mostrarPeriodo = rol!=="mati"`), así que se agregó una fila de chips de meses DENTRO de `Caja.tsx` (arriba, después de la tarjeta de saldo): `mesesCaja` = meses con actividad de caja + mes actual, desc; `elegirMes(p)` hace `setPeriodo(p)` + `setTope(5)`. Sirve para Mati y para Facu. Verificado en /como-mati: tocar jun-2026 cambia la lista a junio (5 de 48, saldo sub-línea del mes). Se actualizó el banner de `ComoMati.tsx` (ya NO dice "no ve el selector de mes", ahora Mati sí filtra por mes con los chips). `Caja` acepta prop `vistaMati`; `esMati=vistaMati||rol==='mati'` oculta aportes.

**DEPLOY / link para Mati (jul-2026):** la app corre en localhost:5173 (dev) — NO hay link público. Se compiló OK (`npm run build`, 491KB js / 141KB gzip, incluye SW PWA; hash router → anda en cualquier host estático sin config de redirects; las 3 claves VITE_ se hornean del `.env.local`, anon key pública OK). Se armó `paseo-nordelta-app.zip` (150KB) del `dist/` y se envió a Facu para publicarlo. NO se puede deployar por Claude sin crear cuenta (prohibido) → Facu tiene que hacer el paso de la cuenta: **arrastrar el zip/carpeta dist a app.netlify.com/drop** (2 min, da URL tipo x.netlify.app con HTTPS). Login de Mati: mati@paseonordelta.com / MatiCaja2026. Pendiente real: deploy formal (Netlify/Cloudflare/Vercel) + apuntar subdominio de paseonordelta.com (GoDaddy). Alternativa para probar YA en el cel de Facu en la misma WiFi: `npm run dev -- --host` → http://192.168.1.x:5173.

**PLAN 3 LINKS PÚBLICOS SEPARADOS POR ROL (jul-2026, pedido por Facu) — en construcción:** Facu quiere 3 apps/links distintos, cada uno único SIN contraseña (eligió la opción de apps separadas para aislar credenciales). Requisitos por rol:
- **Link MATI** (único, sin clave): Caja. NO mostrar en NINGÚN lado aportes de capital NI inversiones (ni en lista, ni en suma/saldo, ni totales) — solo lo operacional. Saldo de caja = cómo CERRÓ ese mes (al cierre del período); si es el mes actual, muestra cómo está hoy. Filtro por meses, min/max.
- **Link INVERSORES** (distinto al de Mati y admin, sin clave): SOLO LECTURA — poder indagar/revisar todos los movimientos pero NO modificar. Súper claro, filtrar por meses, minimizar/maximizar, y que se vea bien también en COMPUTADORA (no solo teléfono).
- **Link ADMIN** (distinto a los otros dos, sin clave): editar, cargar ingresos/egresos, movimientos de caja, filtrar por meses, min/max, subir fotos de facturas/PDFs/archivos múltiples, aprobar cargas, extractos bancarios. Vista previa muy ordenada para compu. TODO lo que hace el admin se automatiza a los sheets: cuentas corrientes de cada local, Paseo Nordelta Master Plan, expensas de cada local, todo.
- General a los previews de mes: el saldo/caja mostrado = cómo cerró ESE mes; el mes actual = cómo está hoy.
Arquitectura: build por rol con `VITE_AUTO_EMAIL`/`VITE_AUTO_PASSWORD` embebidos (cada deploy solo tiene su propia credencial → aislado). Implementado en `auth.tsx` (`HAY_AUTO`: si hay env auto-login, si no muestra login; `?admin` fuerza login).
**CUENTAS CREADAS + roles OK (jul-2026):** mati@paseonordelta.com / MatiCaja2026 (rol mati) · inversores@paseonordelta.com / InvPaseo2026 (rol inversor) · admin@paseonordelta.com / AdminPaseo2026 (rol facu). Roles seteados vía SQL (verificado, 3 rows). El facue1900@gmail.com sigue siendo facu también (login manual).
**3 BUILDS HECHOS + aislación verificada (jul-2026):** script en Bash con `.env.production.local` temporal por rol → `dist-mati`/`dist-inversores`/`dist-admin` + `paseo-mati.zip`/`paseo-inversores.zip`/`paseo-admin.zip` (~150KB c/u, en la raíz del proyecto). Grep confirmó: cada JS tiene SOLO su propio email/pass (el de Mati NO contiene admin@ ni AdminPaseo2026). El `window.supabase` dev-hook NO va en prod (guardado con import.meta.env.DEV).
**HECHO del refactor Caja (jul-2026, typecheck OK):** saldo "al cierre del mes / hoy si es el actual" (period-based, como Banco); Mati (esMati) excluye aportes de capital Y inversiones de TODO (lista, saldo, totales); "ajustar base" oculto para Mati.
**INVERSORES EXPLORER HECHO + fix RLS + Mati inversiones (jul-2026, verificado):** (1) BUG inversores vacío ($0) = el rol inversor NO tenía policy para leer movimientos (solo locales). ARREGLADO: se corrieron `create policy "inv ve mov/fact/cfg" ... using (mi_rol()='inversor')` (SQL, ok). (2) `Inversores.tsx` reescrito como EXPLORER de lectura estilo la foto 3 de Facu: hero resultado del negocio del mes, "El negocio mes a mes" con BARRAS proporcionales, cada mes se ABRE (click ▸/▾) para ver sus movimientos read-only con paginado "Ver 10 más / Minimizar", acumulado del año, caja "El negocio se sostiene solo", Saldos al cierre (Efectivo/Dólares/Banco + total), Capital y obra (Aporte Richi/Facu/total/obra + % financiado). Filtro por mes = selector del header (inversor lo tiene). Verificado en localhost (auto-login inversor temporal): datos reales, saldos Efectivo $3,4M/Dólares US$0/Banco $4,1M, capital Richi $150M/Facu $23,3M/total $173,4M/obra $166,9M (coincide foto 3). (3) DESKTOP: `App.tsx` main+header ahora `max-w-md lg:max-w-4xl` para no-mati (Mati queda angosta). (4) "Salir" ahora solo visible para rol facu (Mati e Inversores son kioscos públicos, no se deslogean). (5) Mati: la exclusión de inversiones YA está en el código (`esInversion`), lo que veía Facu era el build viejo deployado → se rebuildearon las 3 variantes (mati/inversores/admin) con todo, aislación verificada. Facu tiene que REDEPLOYAR dist-mati y dist-inversores (y dist-admin).

**3 SITIOS NETLIFY YA ASIGNADOS BIEN (jul-2026, verificado en Chrome):** Facu creyó que se mezclaron los builds pero NO — cada sitio auto-loguea con su rol correcto: **lucent-buttercream-8ac45a → Mati**, **whimsical-alfajores-91122a → Inversores**, **dancing-elf-c4ed3f → Admin** (todos Netlify Drop, team Astronomy/facue1900). (dapper-cajeta-537756 es de Astronomy, ignorar). Tenían builds viejos. SÍ SE PUDO DEPLOYAR VÍA NETLIFY CLI (jul-2026): `file_upload` del navegador NO sirve (solo acepta archivos que el user compartió; rechaza los que genero yo). PERO el **Netlify CLI SÍ**: `npx --yes netlify-cli@latest login` → imprime URL `app.netlify.com/authorize?...ticket=X` → navegué el Chrome de Facu ahí (mostró "Error during authorization" pero IGUAL el CLI quedó logueado, token en `~/Library/Preferences/netlify/config.json`) → `npx netlify-cli deploy --prod --dir=dist-<rol> --site=<ID>`. **Site IDs:** Mati lucent-buttercream=c8e5aed4-4a4b-4cac-9cd1-ad2f27f61e21 · Inversores whimsical-alfajores=57853b83-a64f-4a73-bd3f-542e056fb184 · Admin dancing-elf=619be610-5e8e-4739-b86d-d2d5d52959ce. Los 3 desplegados y verificados en vivo (Mati $3.403.080 real / Inversores explorer con barras / Admin). OJO: la PWA cachea con service worker → tras un deploy hay que limpiar SW+caches para ver lo nuevo (`navigator.serviceWorker.getRegistrations()` unregister + `caches.delete`); los usuarios reales lo ven tras 1-2 recargas (autoUpdate). Para futuros deploys: rebuild 3 variantes + los 3 comandos `netlify deploy` (ya logueado).
**BUG CORREGIDO saldo Mati (jul-2026):** al excluir aportes+inversiones también del SALDO, la caja de Mati daba −$11.388.954 (negativo, imposible). Fix: el saldo "Efectivo en caja" ahora es SIEMPRE el efectivo físico real (base + TODO lo de caja, incl aportes/inversiones) ≈ $3,4M; solo la LISTA le oculta a Mati los ítems de aporte/inversión. Rebuildeados los 3 zips con este fix + el explorer de inversores.

**INVERSORES top rediseñado (jul-2026, verificado + deployado):** Facu pidió cambiar el encabezado. AHORA: sección "El negocio, al día de hoy" con 3 cards: (1) **Plata del negocio** = caja+banco HOY ($7.522.578), abajo chico "Caja $3,4M · Banco $4,1M" + USD; (2) **Invertido en el negocio** = obra total ($166,9M); (3) **Recuperado hasta hoy** = ingresos/cobros del negocio acumulados ($114M). Luego hero **"Resultado del negocio total"** = acumulado de TODOS los meses (+$989K, "Ingresos totales − gastos operativos", sin aportes ni obra) — ya NO es el resultado de julio (julio está en las barras; detalle tocando el mes). Se sacó la sección "Saldos al cierre" (quedó en el top). OJO A CONFIRMAR CON FACU: "Recuperado" hoy = ingresos brutos del negocio ($114M, = mismo nº que "ingresos totales" del hero) — puede querer otra cosa (resultado neto, plata disponible, o el "recupero de gastos" facturado). Todo calculado sobre TODO (no depende del selector de mes).

**RECUPERADO corregido + PLANILLA "GASTOS OBRA" a integrar (jul-2026):** Facu corrigió: "recuperado" NO son los cobros brutos — es **literalmente la ganancia NETA acumulada del negocio** (si el negocio no deja plata mes a mes, no se recuperó nada de lo invertido). Ya cambiado: `recuperado = negocioTotal` (+$989K) y el sub muestra "% de lo invertido". Deployado.
**Nueva fuente de verdad de inversores = planilla "Gastos Obra - PASEO NORDELTA 2026"** `1wxaXia5lvoYk9lPZ_2Ie9imhxexUqmaU0wFqryNjIDY` (Hoja 1). Estructura: A-F Fecha/Persona/Descripción/Monto/Moneda/Fx; H-I Monto ARS/USD; **L-N = Acumulado por inversor** (fila 5+: nombre, ARS, USD, hasta fila "Total"); T-V un acumulado agrupado alternativo; Q1 "Facu debe a Richi US$12.116". DATOS REALES leídos: Facundo $77.590.282/US$52.221 · Richi $109.442.000/US$76.453 · **Mariana —/US$180.380** · Paseo Nordelta $22.141.629/US$15.483 · **Soledad —/US$91.530** · Tomas US$0 · **TOTAL $209.173.911 / US$416.067**. OJO: el total REAL es el de USD (Mariana y Soledad no tienen ARS porque pagaron obra por fuera de las cuentas de Paseo) — muy distinto al $166,9M que la app calculaba de movimientos. Se creó `supabase/apps-script-inversores.gs` (doGet → JSON con inversores+total, deploy como Web App "Cualquier persona"). `Inversores.tsx` ya lo consume vía `VITE_INVERSORES_URL` con FALLBACK a lo calculado: si hay planilla, "Invertido en el negocio" muestra el total USD y la sección pasa a llamarse "Quién puso la plata" listando cada inversor. **✅ HECHO — Apps Script deployado y app conectada (jul-2026, verificado en vivo).** URL del web app: `https://script.google.com/macros/s/AKfycbxdPLM7dLULqUIwh92ycgA_dF0E-_wmhMABsTNubE7NNWcusIFbfCg6HaSsXEOMniRkvQ/exec` (Version 2, Ejecutar como Facu, Acceso: Cualquiera). Guardada en `.env.local` y horneada en el build de inversores como `VITE_INVERSORES_URL`. CORS VERIFICADO: fetch desde whimsical-alfajores.netlify.app → 200 OK. La vista de inversores ya muestra "Invertido en el negocio US$416.067" (de la planilla) y "Quién puso la plata" con los 6 (Facundo/Richi/Mariana/Paseo Nordelta/Soledad/Tomas). **Cada edición de la planilla se refleja al recargar la app — sin copiar nada.** NOTA sobre el deploy de Apps Script: yo puedo hacer TODO (pegar código con `window.monaco...setValue`, guardar Cmd+S, Deploy → New deployment → Web app → Anyone) MENOS el popup de consentimiento OAuth de Google, que abre en una VENTANA APARTE fuera del tab group y no puedo tocar — eso lo tiene que clickear Facu (elegir cuenta → Configuración avanzada → Ir a … (no seguro) → Permitir). Después de que él autoriza, relanzar Deploy → New deployment y sale directo. Técnica para leer la planilla desde el Chrome logueado: `fetch(gviz/tq?tqx=out:csv&gid=0, {credentials:'include'})` + parser CSV propio.

**PROYECCIÓN DE RECUPERO en vista Inversores (jul-2026, deployada):** Facu pidió un estimado de recupero según cómo viene el negocio + la proyección de los locales nuevos (mencionó "eso que armamos" — NO había registro mío, se lo dije y lo armé de cero con los datos que sí había). Fuente: el **rent roll ya cargado en `locales`** con `estado='futuro'` y `fecha_desde` (La Jaula ago-26, Cafetería sep-26, Peak One y Salón ene-27, Fabric-nuevo nov-27, Parrilla y Shock Ba dic-27, Comercios 1-6 + Market fin-27). Cálculo: `ingresoNeto(local) = alquiler + alquilerNoGravado + gastosComunes + recupero` (SIN IVA, no es plata del negocio); `gastoProm` = promedio real de egresos-negocio de los meses ya cerrados; simula mes a mes sumando cada local cuando llega su `fechaDesde` hasta cubrir lo invertido. Muestra 3 KPIs (Resultado mensual hoy $534K · Con todo el rent roll $50,9M · Recupero estimado **2.2 años, sep-28**) + lista "Próximas aperturas" con cuánto suma cada uno. **BUG CORREGIDO:** al principio daba 1.5 años porque usaba `obra.total.ars` ($209,2M) como lo invertido — esa columna de la planilla está INCOMPLETA (Mariana y Soledad aportaron en USD y no tienen ARS). Ahora usa `obra.total.usd * dolar` = US$416.067 ≈ $634,5M, que es el invertido real. Texto al pie aclara que es estimación, sin ajuste por inflación ni dólar.
**Colchón de vacancia + capex de comercios agregados (jul-2026, deployado):** Facu avisó que varios locales no tienen alquiler ni obra 100% confirmados, y que **los 6 comercios pueden costar US$200.000 más de obra**, que piensan reinvertir con plata del negocio. Implementado en `Inversores.tsx`: `VACANCIA = 0.15` (se aplica a `ingresoConColchon()` solo sobre locales `estado==='futuro'`, los ya activos van a valor pleno) y `CAPEX_COMERCIOS_USD = 200000` que se RESTA del acumulado en el mes en que abren los comercios (`mesComercios`, dic-27) porque se reinvierte y retrasa el recupero de los socios. Resultado: "Con todo el rent roll" bajó de $50,9M → **$43,7M/mes** y el recupero pasó de 2.2 → **2.9 años (jun-29)**. Se agregó card "Supuestos de la proyección" listando los 4 supuestos (vacancia 15%, US$200k capex ≈$305M en dic-27, gasto operativo real $16,6M/mes, sin ajuste por inflación/dólar). NOTA: la lista "Próximas aperturas" muestra el valor bruto del rent roll (sin el 15%), el colchón se aplica en el cálculo — está aclarado en los supuestos.

**ADMIN — OVERHAUL GRANDE pendiente (pedido jul-2026, NO empezado):** Facu quiere para el link admin: ✅ (b) AGREGAR/EDITAR LOCALES — HECHO (jul-2026, verificado en admin, deployado a dancing-elf): `data.tsx` tiene `addLocal` (genera id slug del nombre, único, orden=max+1) y `updateLocal` ampliado (mapea todos los campos vía `localCols`). `Cobros.tsx` reescrito: botón "+ Agregar local", botón "editar" en cada card, modal con nombre/unidad/rubro/estado(select)/alquiler/alquiler-sin-IVA/gastos-comunes/recupero/cobra-IVA(check), grid 2 columnas en compu (lg:grid-cols-2). Verificado: editar Fabric carga bien todos los valores, Guardar funciona. FALTA aún: sync del alta/edición de local al sheet Configuración + crear su cta cte/dashboard automáticamente (punto f, va con la automatización de sheets).
✅ (c) CUENTA CORRIENTE POR LOCAL — HECHO (jul-2026, deployada a dancing-elf): `LocalDetalle.tsx` (`/cobros/:localId`) reescrita. Muestra **Saldo de cuenta corriente** arriba + libro mes a mes (Mes · Se le facturó · Pagó · Saldo acumulado), cada mes se abre y lista los pagos reales (de `movimientos` ingresos de ese local). El CARGO de cada mes sale de `facturas` (clase='venta', local_id=X, periodo=P) si existe → **real**; si no, estima con `facturacionMensual(local).total` de HOY y lo marca "est.". Botón por mes **"Dejar fijo el cargo de {mes}"** que crea la factura (via `addFactura`) para que el saldo sea exacto de ahí en más. Arranca en `min(fechaDesde, primer movimiento)`. IMPORTANTE/HONESTIDAD: cuando hay meses estimados el título dice "(estimado)" y avisa en rojo que el saldo puede estar INFLADO porque aplica el alquiler de hoy a meses viejos (ej. Fabric daba $24,2M de deuda usando $11M/mes cuando en enero facturaba ~$4,2M). ANTI-DOBLE-CONTEO: `Impuestos.tsx` ahora filtra `!f.localId` en `facMes` y `facHasta` — el IVA sale SOLO de los agregados del Libro IVA ARCA (local_id null); las facturas por local son cargos de cta cte y ya están dentro de esos totales.
PENDIENTE resto admin: (a) simplificar el Inicio; (b) en Cobros: agregar/editar locales; (c) por cada local ver movimientos, cuándo/cuánto pagó, cuánto debe de alquiler y expensas, sincronizado con CUENTAS CORRIENTES; (d) los pagos → sincronizados con ingresos y que entren automático a la cta cte del sheet del local ni bien entra un ingreso; (e) actualizar ctas ctes automáticamente a principio de mes (cuánto cobrar de alquiler+expensas a c/u), mes a mes en la app admin; (f) al agregar local nuevo → crear su cta cte + dashboard mensual + movimientos/forms (todo al día); (g) simplificar y unir el dashboard de expensas (muy complejo hoy); (h) vista compu bien armada (admin es la más grande/compleja). El OCR de facturas necesita API key (Facu no pudo pagar aún). Es un proyecto multi-etapa. DEPLOY: 3 sitios Netlify (Mati puede reusar lucent-buttercream).

**Pendiente / Fase 2:** escaneo de facturas (OCR → IVA crédito automático); cruzar las transferencias de $11,2M con Configuración/categorías reales; separar Inversión vs Negocio en el dashboard; cargas sociales (recibos MB); Ganancias estimado; reporte inversores ARS+USD; sync a los Google Sheets; importar extractos PDF desde la app. Falta expensas reales de Boss/Volta/Peak/Salón (Fabric y Bigg ya reales).


============================================================
## FILE: paseo-nordelta-web.md
============================================================

---
name: paseo-nordelta-web
description: Paseo Nordelta website rebuild — Facu wants full control of paseonordelta.com without his brother
metadata: 
  node_type: memory
  type: project
  originSessionId: fdd90af5-3b50-4ee8-b234-50e37648a370
---

Facu pidió tener **control total** de la web paseonordelta.com (landing del paseo comercial en Nordelta). La original la armó su hermano en Manus (AI builder, hosteada ahí + CDN cloudfront), y Facu no quiere depender más de él para arreglos.

**Decisión:** rebuild limpio en vez de pedir handover. Reconstruí el sitio de cero, fiel al original pero mejorado (hero de 7 MB → 941 KB, formulario que compone email, responsive, accesible).

**Ubicación del proyecto:** `/Users/Facu/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/Web Paseo Nordelta/` (Facu lo movió acá y renombró la carpeta a "Web Paseo Nordelta" para diferenciar el sitio del resto de sus archivos del workspace). Requiere `request_directory` a `/Users/Facu/Desktop/Paseo Nordelta` para editarlo. HTML/CSS/JS estático sin build. Imágenes y tipografía (Neue Haas Display) descargadas dentro de `assets/` (antes vivían en el CDN de Manus del hermano → riesgo de que desaparezcan).

**Diseño:** negro cálido `#171614` + off-white `#f2ece1` + acento Corten `#c4622d`. Font Neue Haas Display.

**Interacción:** scroll suave con inercia (Lenis, vendorizado en `assets/js/lenis.min.js`) + animaciones de aparición al scrollear (reveal vía IntersectionObserver en main.js). Respeta prefers-reduced-motion. Facu valoró mucho este "flow" (le gustaba el de la web original del hermano). NOTA: el navegador interno del preview de Claude Code tiene el scroll roto en este proyecto — verificar cambios de scroll en Chrome real (claude-in-chrome), no en el preview pane.

**Dominio:** `paseonordelta.com` registrado en **GoDaddy** (creado 1-abr-2026, DNS en GoDaddy, titular con privacidad). Pendiente confirmar si la cuenta GoDaddy es de Facu o del hermano — ese es el único paso que necesita cooperación/acceso.

**Contacto oficial del paseo:** paseonordelta@gmail.com · IG @paseonordelta · Av. de los Colegios 160, Nordelta, Tigre. NOTA: "Astronomy Eventos" figura como uno de los locales del paseo (vínculo con [[membership-system-project]]).

**Próximo paso:** publicar (Netlify Drop / Cloudflare Pages) y apuntar el dominio desde GoDaddy.


============================================================
## FILE: public-site-vision.md
============================================================

---
name: public-site-vision
description: Etapa 3 — the new public astronomyofficial.com site vision (company presentation + Dominé/Academy split)
metadata: 
  node_type: memory
  type: project
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
---

**Etapa 3 (después de lo funcional):** rehacer el sitio público en el MISMO dominio `astronomyofficial.com`. Facu lo pidió el 2026-07-13. Ver [[membership-system-project]] y [[astronomy-brand]].

Estructura deseada:
- **Home = presentación de la empresa** (más institucional, no directo a membresías).
- Dos accesos principales desde el home:
  - **"Dominé"** → página de **eventos pasados** (Dominé es la marca de eventos). 
  - **"Academy"** → página de **membresías** (la academia / lo que hoy es el demo de membresías).
- **Footer (abajo de todo):** botones de **YouTube, WhatsApp, mail, "Contactanos"**.
- **Sección "Trabajá con nosotros":** formulario básico (nombre, contacto) para que la gente deje sus datos y Astronomy los contacte; con opción de elegir si quiere trabajar en **Eventos** o en la **Academia**.

Facu: "hay muchas cosas a mejorar". La estética de la app real (astronomy-members) hoy es básica a propósito — falta cargar muchas fotos; el pase de estética va al final, tomando como base el demo aprobado (`Astronomy - Demo Membresias.html`).

**BUILT — v1 (2026-07-13):** decidido con Facu: **(A) integrado en la misma app Next.js** (no sitio aparte) + **mobile-first**. Hecho:
- `app/page.tsx` = **Home pública** (antes redirigía a /dashboard; ahora es el landing): hero + split Dominé/Academy + "quiénes somos" + form "Trabajá con nosotros" + footer.
- `app/eventos/page.tsx` = **Dominé** (grid de flyers en `public/eventos/*.jpg`, 7 eventos curados de la carpeta Eventos).
- `app/academy/page.tsx` = **Academy** (profes con foto + membresías reales con foto `public/planes/*.webp` + badge metálico por tier + CTA a /registro).
- `components/SiteHeader.tsx` (logo + Dominé/Academy + botón Ingresar→/login), `components/SiteFooter.tsx` (WhatsApp/IG/YouTube/SoundCloud/mail, links en `lib/links.ts`).
- `components/JobForm.tsx` + `app/actions/apply.ts` → guarda en tabla `job_applications` (SQL en `supabase/jobs_schema.sql`, Facu debe correrlo). Campos: nombre, contacto, área (eventos/academia), mensaje.
- Estilos del sitio en `app/globals.css` (.site-nav, .hero, .split, .footer). El proxy NO protege /, /academy, /eventos (públicas).
- Badges metálicos de plan (.tier-silver/gold/platinum) también usados en el dashboard del alumno (`components/PlanSection.tsx`) — con foto del plan; cuando el alumno ya tiene plan activo se oculta "Elegí tu plan" y aparece el badge + "Cambiar plan".
- **Pendiente:** que Facu corra `jobs_schema.sql`; sumar las postulaciones al panel /admin; iterar estética; después apuntar `astronomyofficial.com` a esta app al hacer deploy.


============================================================
## FILE: reconciliacion-pagos-sistema.md
============================================================

---
name: reconciliacion-pagos-sistema
description: Cómo funciona el pull automático de MP + reconciliación de suscripciones + espejo unificado en la Base de Clientes
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-22T13:48:44.255Z
---

Sistema de pagos/suscripciones auto-mantenido (armado 2026-07-21). Todo cuelga del cron
`app/api/cron/sync-sheet` (horario + disparado al instante desde webhook MP, carga manual,
reserva, baja y asignación de pago vía `lib/syncSheet.ts` `syncSheetSoon()` con `after()`).

**Cada corrida hace, en orden:**
1. `syncPayments(últimos 45 días)` — trae pagos de MP, **acredita solo** a payers conocidos
   (alias en `user_mp_payers` / `user_emails`; `resolveUser` en `lib/payments.ts`) y **encola**
   los desconocidos en `unassigned_payments` para linkear 1 vez en "Pagos" (admin). El token de
   MP prod está SOLO en Vercel; el `.env.local` tiene el TEST (por eso local ve 0 pagos).
2. `reconcileSubscriptions()` — deja `subscriptions.status='authorized'` + plan + `next_charge_date`
   (estimada = último pago + 31d, salvo preapproval real de la web que lo maneja MP) para quien pagó
   una MEMBRESÍA hace <50d. Los que pagan el producto viejo "Curso Astronomy Suscripción" (mapeado a
   `cursodj`) PERO ya tienen registro de sub = members legacy → Silver (o su plan). Excluye
   facue1900/facu1900/annie. NO toca a los que no pagaron.
3. Escribe 4 pestañas en la **Base de Clientes** (`GOOGLE_SHEETS_ID` = `1gj2JHtPqS8CGh2IdNa5vijCM3Zez9rNdFOudcRwFDKs`,
   compartida con el SA `astronomy-calendar@astronomy-app-502618.iam.gserviceaccount.com`):
   **Web (espejo)** (alumnos+créditos+plan+estado), **Eventos (web)** (slot_bookings), **Finanzas**
   (sales atribuidas + unassigned + manual_payments), **Bajas de membresías** (cancellations).
   Encabezados violeta/negrita/congelados vía `styleHeaders`. Pestaña estática aparte **Finanzas
   (histórico)** = 652 ingresos importados de la planilla externa de finanzas (id `19N6pPrE6rEM8...`).

**Closer/comisión** (para sueldo de Jose): la comisión sigue al ALUMNO (`client_closers`), no al pago:
quien lo trae cobra TODOS sus pagos. `first_pct` en el 1er pago, `recurring_pct` en renovaciones
(en `staff_rates`). Solo comisionan membresías + Curso DJ. Sueldo = fijo + comisiones. Ver [[astronomy-pending-features]].

**Limpieza del 21/7/2026:** se dieron de baja 8 suscripciones que la migración del sheet había
marcado `authorized` sin ningún pago real detrás (verificado contra la pestaña "Finanzas (histórico)",
formato de fecha **M/D/YYYY**): Carlos Ortiz, Felipe Floria, Felipe Taborda, Francisco Agüero, Grego
Pedriel, Juani Gastaldi, Martin Serebrinsky, Pablo Castro — ninguno pagaba desde marzo/mayo 2026.
Quedó registro en `cancellations` con motivo "Baja administrativa (sin pagos)" y el último pago real.
**Sus créditos NO se tocaron.** Si alguno vuelve a pagar, `reconcileSubscriptions` lo reactiva solo.
Resultado: authorized 30→22, "Falta cobrar" 18/$2.542.278 → 3/$482.640, esperado del mes $4.870.998.
Ojo: `manual_payments` está VACÍA — el botón "Cargar un pago a mano" nunca se usó, así que los pagos
por transferencia/efectivo hoy no quedan registrados en la app.

**`sales` es la fuente ÚNICA de verdad de la plata**: de ahí salen "Cobros del mes", la comisión del
closer (sueldo de Jose), `reconcileSubscriptions` y la pestaña Finanzas. Todo pago que entre por
cualquier vía TIENE que registrarse ahí o desaparece de los 4 lugares. `mp_payment_id` es **text**
(los pagos manuales usan `manual:<userId>:<timestamp>`). Bug arreglado 21/7/2026: `registrarPagoManual`
insertaba solo en `manual_payments` → el alumno seguía figurando como que no pagó y la comisión se
perdía. Ahora, si es cuota de suscripción, también registra la venta (vía `registrarVenta` si el plan
comisiona, o insert directo para DJ Delivery que no comisiona). Ojo: `registrarVenta` **ignora errores
en silencio** (`if (error) return`), así que cualquier cambio ahí hay que probarlo de verdad.

**`ventas@bedonnad.com` = CHRISTINE BELL** (confirmado por Luqui, 22/7/2026). Es el mail con el que
paga su Curso de DJ. Ya quedó vinculado: `user_mp_payers` (payer MP 251693157) + `user_emails`, así
sus pagos futuros se atribuyen solos. El pago de $143.520 del 22/6 (MP 164509583241) se vinculó **sin
re-acreditar créditos** (ya estaban en su saldo migrado) pero **sí** se registró la venta, para que la
comisión se pague. Su closer ya está asignado (Jose).

**Reconciliación fina de créditos — HECHA 21/7/2026** (aprobada por Facu). Total 21.672 → **19.132**:
· Los 8 dados de baja (dejaron de pagar) → 0: Agüero 340, Floria 270, Gastaldi 250, Pedriel 240,
  Serebrinsky 240, Castro 240, Taborda 240, Ortiz 240 = 2.060.
· Curso de DJ vencido (no acumula, +31 días sin pagar) → 0: Constantino Aldazabal 240, Simon
  Garimberti 240 = 480.
Método: se pone `credit_lots.amount_remaining = 0` en los lotes vigentes + fila en
`credit_transactions` (`type:"spend"`, delta negativo) con el motivo → auditable y reversible.
**NO se tocó** a los 4 de saldo alto (Toninelli 5.932, Marciano 4.110, Pacino 2.590, Álvarez/Patuel
1.750), annie (240) ni la cuenta de prueba de Facu (1.390). El resto quedó como está (todos pagaron
hace <31 días). Los historiales por alumno están en Desktop/Historiales-Alumnos/.

**Venta faltante detectada:** el pago MP `169142692378` de Santiago Romero (16/7, $143.520, cursodj)
se le había acreditado a mano pero NUNCA se registró en `sales` → Jose perdía la comisión y julio
quedaba subfacturado. Se registró como pago #2.

**OJO — error mío a no repetir (22/7/2026):** reporté que `client_closers` estaba vacía y que la
comisión de Jose era $0. **FALSO**: tiene 29 filas (Jose 22, Luqui 3, "ninguno" 4) y la comisión de
Jose en julio es **$236.258** por 19 pagos. La causa fue un helper de consulta que hacía
`return r.ok ? r.json() : []` — al fallar la request devolvía lista vacía **en silencio** y yo lo leí
como "no hay datos". **Nunca usar ese patrón para sacar conclusiones**: el helper tiene que tirar error
(`if (!r.ok) throw`). Antes de afirmar "no hay X", confirmar que la query realmente respondió 200.


============================================================
## FILE: regla-creditos.md
============================================================

---
name: regla-creditos
description: "REGLA CENTRAL — las membresías acumulan créditos, el Curso de DJ los renueva (no acumula)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-24T17:50:58.280Z
---

Los créditos NO se comportan igual en todos los planes:

- **Membresías (Silver, Gold, Platinum, Bronze): SE ACUMULAN.** Cada mes que el alumno paga, los créditos del plan se SUMAN a los que ya tenía. Si viene pagando hace un año y usó menos de lo que pagó, tiene el excedente acumulado.
- **Curso de DJ: SE RENUEVAN, no se acumulan.** Cada pago RESETEA el saldo a los créditos del plan (240 = 4 clases). Lo que no usó ese mes se pierde.

**Why:** Facu lo marcó explícitamente el 24/07/2026 después de ver que una reconciliación mía había bajado los saldos de gente que venía acumulando legítimamente: *"La regla es simple y grábatela. Si viene pagando todos los meses una membresía, se le suman los créditos, se acumulan. Si venía pagando curso de DJ, cada vez que pagabas se le renovaban los créditos, no se acumulan."* Antes yo había asumido que no se acumulaba para nadie — eso está MAL y le rompió saldos reales.

**How to apply:**
- El saldo de hoy de un alumno activo se reconstruye desde su PRIMER pago: todos los pagos (acumulando o renovando según el plan) menos todas las clases, incluidas las **agendadas a futuro** (la reserva ya toma el crédito).
- Sólo se recalculan los **alumnos activos** (los que pagan hoy). Los inactivos no se tocan.
- Las clases se buscan por nombre, mail o el nombre del hijo/pagador — ver [[identidad-alumnos]] y [[atribucion-pagos]].
- **Si alguien dejó de pagar** (venía pagando y no pagó en junio/julio): entender por qué se fue. Si era Curso de DJ → se le sacan los créditos. Si era membresía → los créditos que le sobraron llevan fecha de vencimiento, y hay que revisar si tiene clases agendadas.
- Relacionado: [[astronomy-catalog-data]] (créditos por plan), [[reglas-clases-sueldo]].


============================================================
## FILE: reglas-clases-sueldo.md
============================================================

---
name: reglas-clases-sueldo
description: "Reglas de cancelación, liquidación del profe y anticipación mínima para agendar"
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-22T16:52:11.236Z
---

Reglas de negocio de clases (definidas por Facu, 2026-07-21):

- **Cancelación con -24hs**: NO se devuelven los créditos al alumno y el profe **cobra igual**
  (ya se había organizado, perdió la hora).
- **Cancelación con +24hs**: se devuelven los créditos → el profe **NO cobra**.
- Por eso la liquidación del profe sale sola de esto (`devenga()` en `lib/salaries.ts`): cobra si la
  clase ya pasó y (está `active`) o (se canceló con `refunded === false`). NO hay marcado manual de
  "clase dada" — se **eliminó** esa feature (columna `given` quedó sin uso en la DB, inofensiva).
- **Anticipación mínima para que un alumno agende SOLO = 12hs** (default). Clases con profe a menos de
  ese plazo no se ofrecen en el slot picker (`lib/slots.ts` pasa `leadMs`) y el server las rechaza
  (`bookSlot` y `rescheduleSlot` → `e=antic`/`slot=antic`). Motivo: con tan poco tiempo a veces el profe
  no puede, hay que coordinarlo antes. Los **alquileres** (cabina/estudio, sin profe) NO tienen ese
  límite. El admin igual puede cargar a mano (agenda-manual) sin la restricción.
- **Los dos umbrales son EDITABLES** desde Admin → Horarios del estudio ("Reglas del estudio"):
  columnas `studio_config.min_lead_hours` (12) y `cancel_hours` (24). Se leen con `getStudioRules()`
  de `lib/studioRules.ts` — usarlo SIEMPRE, nunca hardcodear 12/24 (ni en la copy al usuario: los
  textos de member/reservar/sueldos y los componentes BookingCard/NativeBookings/SlotGroupInvites
  reciben `cancelHours` por prop).

**Alta de alumnos y contraseñas (decidido 22/7/2026):** las cuentas creadas desde "Cargar un pago a
mano" usan una contraseña aleatoria que NADIE ve; el alumno entra por el mail de "poné tu contraseña"
(`resetPasswordForEmail`) y queda marcado `must_change_password`. **Nunca contraseñas con patrón
adivinable tipo `nombre123`**: con el nombre de cualquier alumno se entraría a su cuenta y quedarían
expuestos su mail, teléfono, pagos y créditos (y el mail suele ser el del padre/madre que paga).
Facu evaluó alternativas (clave temporal en pantalla / magic link) y decidió **quedarse con el mail**.

Ver [[app-aesthetic-rules]] y [[astronomy-pending-features]].


============================================================
## FILE: sin-city-proyecto-musical.md
============================================================

---
name: sin-city-proyecto-musical
description: Sin City — proyecto de música electrónica de Facu (trío con Vlado y Lanfran); género y kit de crecimiento
metadata: 
  node_type: memory
  type: project
  originSessionId: 486b936f-ffab-498c-aea1-6b2225d0967e
---

Facu produce música electrónica bajo el nombre artístico **Sin City**, que NO es solista: es un **trío** con dos socios. Los tres integrantes son **Vlado, Lanfran y Facu**. (Confirmar si "Vlado Lanfran" es una persona o dos — Facu escribió "vlado lanfran y facu" pero dijo "somos 3".)

Género: House / Tech House + Melodic / Progressive.

Tiene un kit de estrategia de crecimiento musical en `/Users/Facu/Downloads/Sistema_Crecimiento_Musical_Facu.md` (v1.0, julio 2026): estrategia real de la industria, directorio de canales oficiales de demos (LabelRadar, Defected, Toolroom, Anjunadeep, etc.), 12 prompts reutilizables (research de sellos, demo submission, bio, EPK, contenido, pitch Spotify, promo a DJs, CRM, rollout, análisis, booking) y un plan de 90 días.

**Ojo:** el kit fue escrito para un artista solista llamado "Facu". Toda salida (bios, EPK, demos, prompts) hay que adaptarla al trío Sin City y a tercera persona plural.

**Segundo doc** en `/Users/Facu/Downloads/Objetivos_y_Oportunidades_Facu.md` (complemento): añade sellos objetivo (Pangea Recordings — abierto todo el año, mejor primer objetivo melódico, `pangea@pangearecordings.com`; Relief; Selador; Sudbeat de Hernán Cattáneo; Bedrock; mau5trap) y oportunidades poco usadas (remix/stem contests como atajo a release en sello grande; canales de YouTube que hacen premieres — Selected, MangoMusic, When We Dip; Groover/SubmitHub; promo pools; sync; Bandcamp; Beatport Hype).

**Ventaja de marca clave:** son argentinos (Buenos Aires) haciendo progressive/melódico — BA es meca mundial del progressive (Cattáneo/Sudbeat es local). Ángulo de identidad fuerte y networking local real.

**Integrantes confirmados (3):** Facu (@thefacu__), Vlado (@vladinicc), Lucas Lanfranconi (@lucaslanfranconi). Proyecto: @thesincitysound. SoundCloud: sin-city-331265813. Tracks: "Space Miami", "Go Back", "Bitch We're Not the Same".

**Preferencia:** todo lo que mira la industria (demos, materiales) va en **inglés** (idioma internacional). El chat de trabajo sigue en español rioplatense.

**Entregado (jul 2026):**
- **Workbook maestro** en `/Users/Facu/Downloads/Sin_City_Demos_y_Sellos.xlsx` — 8 hojas: Sellos objetivo, Tracker de demos (CRM), Oportunidades, Escena BA, Contenido 30 días, Remix contests, YouTube premieres, Rollout. Estilo noir/neón. Regenerable con el script en scratchpad `build_xlsx.py`.
- **4 mensajes de demo** (en el chat, en inglés, 2 versiones c/u): Pangea, Sola, Colorize, Repopulate Mars — con `[corchetes]` a completar (link privado, BPM, release de referencia, credenciales).

**Pendiente:** Facu arma la **bio** él mismo. Falta que describa el sonido en una frase. EPK y credenciales quedan para cuando tenga bio + números.

Facu también maneja [[membership-system-project]] (Astronomy) y [[paseo-nordelta-web]].
