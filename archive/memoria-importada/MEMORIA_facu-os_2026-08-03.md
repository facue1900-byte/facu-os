# Memoria completa — facu-os

Volcado del 2026-08-03 de `~/.claude/projects/-Users-Facu-facu-os/memory/`.
61 memorias + el índice `MEMORY.md`.

---

# ÍNDICE (MEMORY.md)

## Cómo trabajar con Facu
- [No robarle la pantalla](no-robarle-la-pantalla.md) — todo headless y en segundo plano; avisar recién al final
- [Cada número con su negocio](cada-numero-con-su-negocio.md) — todo hallazgo de plata se etiqueta con su negocio; nunca listas mezcladas
- [Estética simétrica siempre](estetica-simetrica-siempre.md) — tamaños y colores parejos, medir en el navegador
- [Regla de las 20 filas](regla-20-filas.md) — toda lista larga arma su scroll sola; el tope va siempre puesto y no se cuentan filas
- [Avisar al 50% de contexto](aviso-contexto-sesiones.md) — cortar la sesión antes de que baje la calidad; ya automatizado
- [Cartera de inversiones personal](cartera-inversiones-personal.md) — brokerage en USD en `~/Desktop/INVERSIONES_Facu.md`; no está en el CLAUDE.md global

## 🔑 Palabras clave para retomar
- **«eje»** → [Retomar eje](retomar-eje.md) — **la más reciente** (31/07–1/08/2026): calendario público, logo 3D girando, performance, regla de las 20 filas y las rachas nuevas — todo en producción
- **«pauta»** → [Retomar pauta](retomar-pauta.md) — **la más reciente** (cierre 31/07/2026): landing y pixel en producción, tres productos corriendo en Meta con US$10/día cada uno, y el margen real de los últimos 10 meses
- **«podio»** → [Retomar podio](retomar-podio.md) — premios (30–31/07/2026): instructivo entregado, podio de julio el 1/8 solo, y **$184.800 commiteados sin pushear esperando el OK de Facu**
- **«medalla»** → [Retomar medalla](retomar-medalla.md) — premios, DJ Delivery, Luki y la mudanza del repo (cierre 29–30/07/2026)
- **«showcase»** → [Retomar showcase](retomar-showcase.md) — pauta, videos de Modo Profesional y los 190 GB de Eventos (cierre 29–30/07/2026)

## ▶ Lo primero cuando vuelvas, por orden de plata
0. **Google: pedir la indexación a mano** — Search Console → Inspección de URL → `https://astronomyofficial.com/` → "Solicitar indexación". El favicon ya está bien, falta que el buscador refresque: [Retomar eje](retomar-eje.md)
1. **Dar el OK al presupuesto del video de Modo Profesional** — campaña, conjunto y anuncio ya creados y EN PAUSA a US$5/día; no gasta hasta que Facu confirme: [Retomar pauta](retomar-pauta.md)
2. **Cargar los egresos de JULIO** en el Form de finanzas — hay 3 filas y una es un test de $10; sin eso el margen de julio es un espejismo: [Margen real](astronomy-margen-real.md)
3. **Paseo Nordelta: La Jaula da de alta en agosto**, $2M/mes — la próxima de la rampa: [Ctas Ctes del Paseo](paseo-ctas-ctes-import.md)
4. **Cerrar el corte de Luki y `/admin/libro`**: [Finanzas unificadas](finanzas-unificacion-sheets.md) · [Roles de José y Luki](roles-jose-luki.md)
5. **Las rachas nuevas ya están EN PRODUCCIÓN** (Facu aprobó 5 cr el 31/07). El cron va entregando el arrastre: $184.800 de una vez + ~$29.260/mes: [Retomar podio](retomar-podio.md)

## Trampas que ya me costaron caro
- [Calendly y el sistema propio son DOS tablas](academy-y-eventos-separados.md) — `studio_events` (Calendly, hasta el 17/07/26) y `slot_bookings` (el vivo). Toda pantalla de historial tiene que leer las dos o miente
- [Verificar desde esta Mac](verificar-en-mac.md) — `timeout` no existe en macOS y el dominio le da 403 a los scripts: pegarle a la URL del deploy
- [El cron que nunca falló](cron-que-nunca-fallo.md) — `succeeded` en pg_cron sólo dice que encoló; el resultado real está en `net._http_response`
- [Las medallas "estáticas" no son un bug](medallas-reduce-motion.md) — el iPhone de Facu tiene «Reducir movimiento» activado; preguntar eso ANTES de leer CSS
- [PostgREST corta en 1000 filas](postgrest-tope-1000.md) — `limit=100000` no la levanta; contar por cabecera `count=exact` o el número sale mal y no avisa
- [Deploy de astronomyofficial.com](vercel-deploy-astronomy.md) — el push a `main` deploya solo; el token del `.env` está bloqueado por SAML, sirve el del CLI
- [DJ Delivery: la plata entraba sin registrarse](djdelivery-facturacion.md) — cobra solo por MP desde 2024 y la app tiraba el cobro. Arreglado
- [Academy y Eventos son mundos separados](academy-y-eventos-separados.md) — bases, RRPPs y admins propios; hoy está todo mezclado

## Software existente (no construir lo que ya está)
- [Software por negocio + respaldos](software-existente-respaldos.md) — qué app tiene cada negocio, repos en GitHub, bundles en iCloud, ojo con los CSV de alumnos
- [Carpetas de Astronomy en el Desktop](astronomy-carpetas-desktop.md) — dónde va cada tipo de archivo; el árbol quedó cerrado el 30/07, no inventar carpetas
- [Sistema de membresías](membership-system-project.md) — astronomy-members: el build completo, MP en producción, Calendly, migración de alumnos
- [Calendario público `/horarios`](calendario-publico-horarios.md) — EN PRODUCCIÓN: horarios libres del estudio para mandarle a un lead; dos espacios, no cuatro filtros
- [Dónde aparece un pago](donde-aparece-un-pago.md) — la respuesta a Luki: `sales` → `/admin/libro`, y el historial de créditos en `/member` y en la ficha del alumno
- [Auditoría de la web de Astronomy](astronomy-web-revision.md) — sistema de diseño en producción; quedan 2 decisiones de estética
- [App de finanzas del Paseo](paseo-nordelta-app.md) — PWA local-first (cobros, banco, caja, impuestos)
- [Web del Paseo](paseo-nordelta-web.md) — rebuild propio de paseonordelta.com; dominio en GoDaddy (¿de quién es la cuenta?)
- [Export de Passline](passline-export-eventos.md) — cómo sacar quién ENTRÓ, no sólo quién compró, y los tres bugs del CSV
- [Plata de los eventos = libro compartido](eventos-libro-compartido.md) — estilo Splitwise, no porcentajes fijos; ticketera congelada

## Astronomy Academy — reglas de negocio
- [Cuentas internas](cuentas-internas-astronomy.md) — `profiles.es_interno` marca al equipo como no-alumnado; 9 cuentas, 49 alumnos reales
- [Margen real y dónde viven los egresos](astronomy-margen-real.md) — NO están en Supabase: planilla `Finanzas - Astronomy Academy`, hoja Base. 10 meses acumulados dan −3,0%
- [Catálogo y precios](astronomy-catalog-data.md) — Silver $143.520/250 cr · Gold $195.600/360 · Platinum $272.000/480 (web 09/07/2026)
- [Regla central de créditos](regla-creditos.md) — membresías ACUMULAN, Curso DJ RENUEVA; vencen a 2 meses del último pago
- [Clases y sueldo del profe](reglas-clases-sueldo.md) — cancelación ±24hs, anticipación 12hs, umbrales editables
- [Identidad de alumnos](identidad-alumnos.md) — la cuenta va a nombre del alumno con el mail de quien paga
- [Quién factura Astronomy](astronomy-quien-factura.md) — cobra la cuenta personal de Vladimir Nadinic, persona física, CUIT 20-41662712-7
- [Roles de José y Luki](roles-jose-luki.md) — qué hace cada uno y los paneles por rol que faltan
- [Cuenta annie = promo](annie-promo-account.md) — no tocarle membresía ni créditos en ninguna limpieza
- [Cuenta demo](demo-account.md) — demo.gold@astronomyofficial.com, Platinum

## Astronomy Academy — la plata
- [Atribución de pagos](atribucion-pagos.md) — NUNCA matchear pagos por parecido de nombre; `ledger_aliases` + `payment_links`
- [Corte: sólo pagos desde la web](atribucion-pagos-corte-web.md) — lo anterior al 14/07/2026 se archiva; atribuirlo acredita dos veces
- [Reconciliación de pagos](reconciliacion-pagos-sistema.md) — cron `sync-sheet`, `sales` = fuente única de la plata
- [Finanzas unificadas en un sheet](finanzas-unificacion-sheets.md) — las dos planillas, duplicados borrados, y el token de MP que hay que usar
- [Egresos](egresos-sistema.md) — /admin/finanzas, corte 2026-07-01, comisión de MP
- [Reporte financiero](astronomy-finance-report.md) — Apps Script live, merge de 2 planillas, +US$8.575 operativo en 26 meses
- [Sistema de premios](astronomy-premios.md) — se entrega SOLO: objetivos al cumplirse, podio el día 1. Nada que apretar
- [Premios: se reclaman](premios-reclamar.md) — créditos al abrir, arte por rareza, isotipo trazado del PNG
- [Features hechas y pendientes](astronomy-pending-features.md) — booking nativo COMPLETO, panel ops, campanita; falta OTP de teléfono

## Astronomy Academy — pauta
- [Cómo se carga el egreso de pauta](pauta-como-se-carga-el-egreso.md) — el extracto del BofA cierra 15-al-15 y desfasa el margen hasta 49%; el monto sale de la API, 1 al 1
- [Inventario de pauta y público](pauta-inventario-y-publico.md) — qué se pauta hoy, a quién, con qué copy y qué rinde cada formato
- [Meta Ads: la cuenta](meta-ads-astronomy.md) — `CP - Astronomy Academy`, US$1,94/lead, token de sistema que no vence; **techo de US$500/mes sólo Meta**
- [Carrusel de Modo Profesional](pauta-carrusel-modo-profesional.md) — fechas de nacimiento de cada anuncio; chequear ahí antes de decir "lleva N días"
- [Generador de flyers](flyers-academy-generador.md) — skill `flyers`: 75 placas, precios de Supabase, nunca `--user-data-dir` en Chrome

## Astronomy — marca y web
- [Marca Astronomy Academy](astronomy-brand.md) — manual OFICIAL: Aktiv Grotesk + Roboto Mono, blanco/negro/`#180040`. **No aplica a eventos**
- [Dirección de color de la app](app-color-direction.md) — violeta (chakra corona), fuera el dorado
- [Reglas UI de la app](app-aesthetic-rules.md) — alineación, botones parejos, Lenis, nada de diálogos nativos
- [Sin emojis en la web](estetica-sin-emojis.md) — rótulos mono en mayúsculas en su lugar
- [Visión del sitio público](public-site-vision.md) — home institucional, split Dominé/Academy, "trabajá con nosotros"
- [Contactos y links](astronomy-contacts-links.md) — redes oficiales, Calendly de cada profe, config unificada

## Paseo Nordelta
- [Ctas Ctes y cómo cobra cada local](paseo-ctas-ctes-import.md) — Bigg 50/50 con efectivo, La Jaula desde ago-26, expensas desde Expensas Predio

## Otros proyectos
- [Sin City](sin-city-proyecto-musical.md) — trío musical (Facu/Vlado/Lanfranconi); demos en inglés, workbook en Downloads
- [E-commerce dropshipping](ecommerce-dropshipping-project.md) — 3 productos elegidos, landings listas, mercado nacional

> **Nordelta Plaza (NDPL SAS) y Noreventos: revisar en un futuro con Facu.** Quedó viejo
> y hoy no ocupa memoria. La data cruda sigue en `~/Desktop/Nordelta Plaza/` y
> `~/Desktop/Noreventos/`. Es otro negocio que Paseo Nordelta: nunca sumar sus números.

---

# LAS MEMORIAS, UNA POR UNA

---

## 1. `academy-y-eventos-separados.md`

---
name: academy-y-eventos-separados
description: "REGLA — Astronomy Academy y Eventos/Ticketera (Dominé) son dos mundos separados; base de datos, RRPPs y admins propios de cada uno"
metadata: 
  node_type: memory
  type: project
  originSessionId: 18ad68d7-f0e0-45b0-8756-88b4b6243c8b
  modified: 2026-07-30T04:43:38.469Z
---

**Astronomy Academy y Eventos/Ticketera NO se mezclan.** Decisión de Facu del 28/07/2026,
textual: *"No quiero mezclar astronomy academy con eventos y ticketera. Son dos cosas
distintas. Cada uno tiene que tener sus bases de datos, rrpps, admins, son dos mundos
distintos."*

**Why:** son negocios distintos con socios distintos. La academia es Astronomy (Blado 35 /
Facu 35 / Benja 15 / Lanfral 15); los eventos van por Puzzle (50/25/25) y no siempre con
los mismos. Un admin de la academia no tiene por qué ver la plata de un evento, y un RRPP
de un evento no tiene nada que hacer en la base de alumnos. Es el mismo criterio de
[[cada-numero-con-su-negocio]]: cada caja con su etiqueta, nunca heredada del contexto.

**Cómo está HOY (todo mezclado — hay que separarlo):**
- Las tablas de la ticketera (`events`, `ticket_*`, `rrpps`) viven en el **mismo proyecto
  de Supabase** que la academia (`qeakrjnseboiulcojlcw`).
- `/admin` es **un solo panel** con dos secciones ("Astronomy Academy" y "Dominé · Eventos").
- Los permisos salen de **una sola tabla `staff`**: hoy el acceso a eventos se controla con
  `ctx.isMaster`, no con un rol propio de eventos.
- `SiteHeader` y el footer mezclan las dos marcas en la misma navegación.

**How to apply:** cuando se retome la ticketera (hoy congelada, ver
[[eventos-libro-compartido]]), la separación es parte del diseño, no un refactor posterior.
Antes de escribir una línea hay que definir con Facu si van **dos proyectos de Supabase
distintos** o un solo proyecto con esquemas separados (`academy.` / `eventos.`) y RLS por
rol. Nunca asumir que un dato de uno aplica al otro.

---

## 2. `annie-promo-account.md`

---
name: annie-promo-account
description: annie hoffer es cuenta de promo/diseño — NO tocar su membresía ni créditos
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-30T04:50:32.263Z
---

**annie hoffer** NO es una alumna que paga: es una **chica de diseño** a la que le dieron
créditos + Gold para que **suba videos a Instagram del proceso de la web**
(promoción/explicación en redes).

> **La membresía ya no está: Facu la dio de baja el 30/07/2026** (`subscriptions.status =
> cancelled`), junto con la de Felipe Floria. **Los 240 créditos quedaron intactos**, vigentes
> hasta el 17/10/2026 — la orden fue textual: *"desactivales la membresía, si tienen créditos
> dejáselos"*. Ninguna de las dos tenía preapproval real en Mercado Pago, así que no había
> cobro que cortar.

**Lo que sigue valiendo: los créditos no se le tocan.** No se los ajustes ni los pongas en
cero en ninguna limpieza o reconciliación — no son un saldo sin respaldo, son la promo. Lo
mismo para la cuenta de prueba de Facu (Facundo Estevez) — ver [[demo-account]].

**Why:** al reconciliar membresías en julio de 2026 su Gold aparecía "sin respaldo" (ni MP
ni transferencia) y era candidata a baja automática. Es promo, y ahora que la membresía está
cancelada el riesgo se invierte: lo que hay que proteger son los créditos.

---

## 3. `app-aesthetic-rules.md`

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

---

## 4. `app-color-direction.md`

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

---

## 5. `astronomy-brand.md`

---
name: astronomy-brand
description: "Identidad visual OFICIAL de Astronomy Academy — tipografías, paleta, isotipo; y por qué no aplica a eventos"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56f9b80b-f934-42d7-8616-baefea6d84fe
  modified: 2026-07-30T04:44:16.834Z
---

Manual oficial: **`AstronomyIDENTIDAD.pdf`**, propuesta final de **Lola Gallal y Annie
Hoffer**, julio 2025. PDF y las 10 páginas en PNG en
`~/Desktop/Productoras/Astronomy/Marca Astronomy/Branding/`. Versión escrita en
`facu-os/active/astronomy/BRANDING_ACADEMY.md`.

**Esto reemplaza lo que esta memoria decía antes**, que estaba deducido del sitio y de
Instagram, no de un manual.

- **Tipografía primaria: Aktiv Grotesk** (Light · Regular · Medium · Bold).
  **Secundaria: Roboto Mono**, para los rótulos técnicos entre corchetes.
  *No es Montserrat* — eso era una inferencia vieja.
- **Paleta de tres colores y nada más:** blanco `#FFFFFF`, negro `#000000`, azul marino
  `#180040`. Fondo por defecto negro puro; el azul marino es acento. *No hay dorado ni
  cyan en la identidad oficial* — eso vive en las fotos, no en el sistema.
- **Isotipo:** estrella de 4 puntas **asimétrica** (la punta inferior es la más larga)
  que también es una A.
- **Logotipo:** `ASTRONOMY` en caja alta, ancho, **con la A sin travesaño** (`Λ`). Ese
  detalle es lo primero que se pierde si alguien lo retipea a mano.
- Frases de marca: `WHERE THE UNKNOWN BEGINS` · `ETERNAL EXPANSION`.

**ES DE LA ACADEMIA, NO DE LOS EVENTOS** — ver [[academy-y-eventos-separados]]. Los
eventos tienen estética propia y además se producen fechas con marcas de terceros ajenas
a Astronomy. Dato que lo confirma: los flyers de eventos usan la tipografía script
**Amsterdam Four** ("Astronomy Dominé"), que no existe en el manual de la Academia. Hay
además una cuenta publicitaria `CP - Astronomy Dominé` separada de `CP - Astronomy
Academy`. La portada del PDF menciona "Dominé": pendiente confirmar si necesita identidad
propia.

**Aktiv Grotesk es de pago (Dalton Maag) y no está instalada**: se sustituye por
**Helvetica Neue**, que ya viene en la Mac y es su pariente más cercano — Aktiv Grotesk
nació como alternativa a Helvetica. El skill `flyers` usa esa pila en sus dos plantillas,
así que **las 75 placas están en marca** ([[flyers-academy-generador]]).

**Desviaciones abiertas:**
- La app usa un violeta claro ~`#a97fff` ([[app-color-direction]]), bastante más claro
  que el `#180040` oficial. Ver si es decisión deliberada de producto o deriva.
- La bio de Instagram tiene emojis, contra la regla de [[estetica-sin-emojis]].

**Assets reales** (siguen vigentes): `Logos : Flyer/Isotipo/PNG/Isotipo Blanco.png` ·
`Logos : Flyer/Logotipo/PNG/Logotipo Blanco.png` (4320px, transparente) · fotos en
`Academia/Contenido/Material para contenido` y `Eventos/` (ojo: muchas en `.HEIC`, hay que
convertir antes de usar en web).

**Contacto y redes:** WhatsApp `https://wa.me/message/JKQAETPAN6CNN1` · IG academia
`@astronomy.academy` (marca madre: `astronomy.oficial`) · YouTube `@AstronomyOfficial` ·
`studio@astronomyofficial.com`. Bio actual: *"Formamos DJs & productores desde cero ·
Cursos 100% prácticos en Nordelta · Comunidad real & sello propio."*

**Eventos reales** (en `Eventos/`): Dark Mansion, Mansion (Dominé), Dome, Private Boat
Party, Boiler Room (JET), Moonrise, Yacht Party. Sets de YouTube: "The Bunker".
Ver [[membership-system-project]].


## El favicon es un SVG ADAPTATIVO (31/07/2026)

`astronomy-members/app/icon.svg`, trazado del mismo path que usa la medalla. **Sin fondo**:
el color lo decide `prefers-color-scheme` — **negro sobre claro, blanco sobre oscuro**.

**El negro es el DEFAULT y el blanco va en la consulta oscura, no al revés.** Los resultados
de Google se dibujan sobre blanco y su renderer no siempre aplica `prefers-color-scheme`:
con el negro de base, el que la ignore igual ve el logo. Ese era el bug original — el
favicon era el isotipo BLANCO sobre TRANSPARENTE a 4320×4320, invisible en Google.

Chrome elige el SVG en los dos temas e ignora `favicon.ico` y `icon.png`, que quedan de
respaldo. **`apple-icon.png` conserva el fondo negro a propósito**: iOS compone el icono de
inicio sobre negro y no maneja bien la transparencia.

> Google refresca los favicons cuando vuelve a rastrear el sitio, no al instante. Si sigue
> saliendo el globito, es tiempo, no configuración.

---

## 6. `astronomy-carpetas-desktop.md`

---
name: astronomy-carpetas-desktop
description: "Dónde va cada tipo de archivo de Astronomy en el Desktop — el árbol quedó cerrado el 30/07/2026, no inventar carpetas nuevas"
metadata: 
  node_type: memory
  type: project
  originSessionId: b2edfa77-7fae-467e-9fd1-2db67a594cef
  modified: 2026-07-30T05:24:58.263Z
---

`~/Desktop/Productoras/Astronomy/` tiene tres ramas y **ya cubre todo**. Antes de crear una
carpeta nueva, usar la que corresponde:

| Va acá | Qué |
|---|---|
| `Academia/astronomy-members/` | El repo de la app. **Nada de assets suelos acá adentro.** |
| `Academia/Contenido/PDF cursos/` | Programas y PDFs de curso |
| `Academia/Contenido/Pauta Online/` | Videos para pauta (`VIDEO PAUTA1/2`, `CursoProf2.mp4`) |
| `Academia/Contenido/Imagenes para WEB/` · `Material para contenido/` | Fotos y piezas para web y redes |
| `Academia/Flyers Academy/` | Lo que genera el skill `flyers` + diseños de posteos |
| `Academia/Reporte financiero/` | El Apps Script y los exports de finanzas (`Finanzas - Astronomy Academy.xlsx`, `base_finanzas.csv`) |
| `Academia/Pauta/` | Exports del Administrador de anuncios de Meta (CSV) |
| `Academia/Comercial/` | Precios, membresías, presupuestos, servicios |
| `Academia/Capturas app/` | Screenshots de la app |
| `Academia/Fotos del estudio/` | Fotos y videos del estudio |
| `Eventos/<nombre del evento>/` | Una carpeta por evento, plana, con flyers/videos/planillas mezclados |
| `Eventos/_sin-evento-asignado/` | Piezas que no se pudo atribuir a un evento — **Facu decide, no adivinar** |
| `Marca Astronomy/Branding/` · `Logos/` · `Contratos y propuestas/` | Manual de marca, logos y contratos plantilla |
| `_duplicados-revisar/` | Copias byte a byte y temporales, para que Facu las tire. **No borrar por cuenta propia** |

**Ojo con dos nombres reales del disco:** `Eventos/Boiler Room (Futura:Big Fett) ` termina
**con un espacio**, y los screenshots de macOS traen un **espacio angosto U+202F** antes de
"AM" (por eso un glob funciona y un nombre tipeado a mano no).

**How to apply:** un archivo de Astronomy que aparezca en `~/Downloads` o en el Desktop va a
una de estas carpetas, nunca queda suelto. Si no se puede atribuir a un evento, va a
`_sin-evento-asignado` con el motivo, no a la carpeta que más se parezca. La data de
ticketera de eventos (miles de personas con DNI y mail) **no va acá**: va a
`~/facu-os/data/eventos/`, que está gitignoreado — ver [[passline-export-eventos]].

**Lo que quedó pendiente (30/07/2026):** `~/Downloads` bajó de 821 sueltos a **729** y no
quedó ni uno de Astronomy. Los 729 son otra cosa —85 facturas, 31 comprobantes, 16 de AFIP,
24 con "Nordelta", 61 mp3, ~70 fotos— y ordenarlos es un trabajo aparte, sin plata atada, así
que va después de lo que factura. Ojo con las 37 carpetas que siguen ahí: `Passline/`,
`POSTEOS/`, `Ad Astra IDs/`, `curso-astronomy/` son de Astronomy y podrían entrar, pero
`Claude Code Full Course/` la referencia el repo (`CATALOGO_SKILLS_CURSO.md`) — mover esa
rompe la referencia.

Relacionado: [[software-existente-respaldos]], [[astronomy-brand]],
[[flyers-academy-generador]], [[academy-y-eventos-separados]].

---

## 7. `astronomy-catalog-data.md`

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

---

## 8. `astronomy-contacts-links.md`

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

---

## 9. `astronomy-finance-report.md`

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

---

## 10. `astronomy-margen-real.md`

---
name: astronomy-margen-real
description: "Dónde viven de verdad los egresos de Astronomy Academy y cuál es el margen mes a mes — la planilla, no Supabase. Medido el 30/07/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: a66a4ae5-626e-4cf6-b596-f3c2c98c0e83
  modified: 2026-07-31T09:11:39.705Z
---

**Los egresos NO están en Supabase.** La tabla `expenses` tiene **0 filas** y siempre las
tuvo; `staff_payments` también 0 y `salary_payments` sólo 3. Buscar el margen ahí y
concluir "no se registran costos" es el error que cometí el 30/07 antes de que Facu me
corrigiera.

**Viven en Google Sheets**, cargados por un Google Form:

| | |
|---|---|
| Planilla | **`Finanzas - Astronomy Academy`** |
| ID | `19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs` |
| Hoja | **`Base`** (también hay `Responses`, `Variables`, `Cobros`) |
| Cobertura | 1.132 filas, **2024-01 → 2026-07** |
| Columnas | `Timestamp · Real Date · ARS_Ammount · USD_Ammount · Category · Sub Category · Descripción · Client Id · Is New Client` |
| Acceso | cuenta `facu` de `execution/google_auth.py` |

`Category` es **Ingreso** o **Egreso**. Ojo: hay **otras tres planillas con hoja "Base"**
(`Astronomy - Finanzas`, `Finanzas - VLADINIC`, `Finanzas - Astronomy Dominé`) y ninguna
llega a 2026-07 — `Astronomy - Finanzas` corta en 2025-04. **Es fácil leer la equivocada.**

## El margen real, mes a mes

| Mes | Ingresos ARS | Egresos ARS | Resultado | Margen |
|---|---|---|---|---|
| 2025-09 | 3.047.900 | 2.945.766 | 102.135 | 3,4% |
| 2025-10 | 6.275.237 | 4.797.176 | 1.478.061 | 23,6% |
| 2025-11 | 4.574.154 | 3.019.459 | 1.554.695 | 34,0% |
| 2025-12 | 2.490.181 | 5.811.557 | −3.321.376 | **−133,4%** |
| 2026-01 | 3.602.080 | 2.300.521 | 1.301.559 | 36,1% |
| 2026-02 | 2.234.667 | 3.585.049 | −1.350.383 | −60,4% |
| 2026-03 | 2.858.612 | 2.881.339 | −22.727 | −0,8% |
| 2026-04 | 3.305.647 | 4.753.619 | −1.447.972 | −43,8% |
| 2026-05 | 3.467.944 | 3.159.950 | 307.994 | 8,9% |
| 2026-06 | 3.394.608 | 3.038.286 | 356.322 | 10,5% |

**Acumulado sep-2025 → jun-2026: ingresos 35.251.032 · egresos 36.292.722 · resultado
−1.041.691, margen −3,0%.** Diez meses, y el negocio operativo da negativo.

## Dos cosas que hacen que ese número esté MEJOR de lo que es

1. **A junio y julio les falta la pauta.** La planilla tiene las categorías
   `Pauta Publicitaria` y `Gestión de Pauta` y se cargaron de enero a mayo, pero
   **junio y julio no**. El gasto real de Meta, de la API: enero US$214,81 · febrero
   US$249,45 · marzo US$414,05 · abril US$514,59 · mayo US$490,18 · **junio US$498,84** ·
   **julio US$497,67**. En mayo, pauta + gestión sumaron ARS 1.017.840. Si junio fue
   parecido, **junio se da vuelta a ≈ −661.518, o sea −19,5%**, y no queda ningún mes
   claramente rentable en 2026 salvo enero.
2. **Julio está casi vacío de egresos: 3 filas**, y una es un **test de ARS 10**
   (`Sueldos / Test`). Las otras dos: `Financiero/Balance` 116.520 y `Mantenimiento/Bot`
   76.000. Contra ~ARS 2,9 M de ingresos da 7% de egresos, que es imposible. **El 93,4%
   de margen de julio es un espejismo hasta que se carguen.**

## Dónde se va la plata: sueldos

Egresos de junio 2026, las 8 filas: Pastrana 732.000 · Josefina Meyrelles 372.286 ·
Annie + Lola (diseño) 350.000 · Otero 225.000 · Guini 209.000 · Lucas Álvarez Ochoa
200.000 · Valen Frando 90.000 · devolución de un reclamo de MP 860.000.

**Sueldos ≈ ARS 2.178.286 de los 3.038.286 = 72% de los egresos.** Ahí está la palanca
del margen, no en el costo por conversación de la pauta.

## La planilla está alineada al mes, no a cuándo se paga

Los sueldos se cargan **con fecha del último día del mes al que corresponden**: los de
"Junio 2026" tienen Real Date 30/06, los de mayo 30/05, los de abril 30/04. Así que el
margen mes a mes de arriba **compara ingresos y costos del mismo mes**, está bien.

**Julio no está sin cargar por descuido: se paga a principios de agosto**, y ahí se carga
con fecha de julio. Dicho por Facu el 31/07/2026. Consecuencia operativa: **el margen se
lee con un mes de retraso**, así que un cambio de pauta hecho en julio recién muestra su
efecto en el margen en la primera semana de septiembre. La pauta se ajusta cada dos
semanas mirando ventas; el margen se juzga una vez por mes.

Única excepción vista: los sueldos de diciembre 2025 quedaron con Real Date 14/01/2026.

**Los sueldos de profes son variables, por clase.** Pastrana: 99.000 en abril, 286.000 en
mayo, **732.000 en junio**. No es un fijo. Implica que **facturar más no mejora el % por sí
solo en la parte de enseñanza** — lo que se diluye al crecer es lo fijo (Josefina, Lucas,
Annie y Lola, suscripciones). **El margen mejora por producto y por precio, no por
volumen.**

## Filas de prueba en `Responses` que NO están en `Base`

El 20/05/2026 alguien probó el Form y quedaron 4 filas basura **sólo en `Responses`**
(alguien ya las filtró de `Base`, así que **no ensucian ningún número**):

| Fila | Qué dice |
|---|---|
| 756 | Ingreso ARS 143.520, DJ Course, "PRUEBA INACTIVE" |
| 762 | Egreso ARS 111.111, Gestión de Pauta, "Prueba" |
| 763 | Egreso ARS 11.111, Gestión de Pauta, "Prueba Descripcion" |
| 764 | Egreso ARS 111.111, Gestión de Pauta, "Prueba description" |

**Ojo al limpiar: "Clase de Prueba" es un producto real** (~ARS 37.000) y aparece decenas
de veces. Filtrar por la palabra "prueba" borra ventas de verdad.

**Borrado el 31/07/2026:** la fila de test de ARS 10 (`Egreso / Sueldos / Test`, cargada
el 16/07), que sí estaba en las dos hojas — `Base` 1124 y `Responses` 819. Respaldo del
contenido en `~/facu-os/archive/respaldo-filas-borradas-finanzas.json`.

## Cuidados al leer esta planilla

- **Mezcla bruto y neto.** Un mismo curso aparece a veces como 143.520 (bruto) y a veces
  como 134.980,56 (neto de la comisión de Mercado Pago, ~6%). Los totales de ingresos
  arrastran esa inconsistencia.
- **No cierra con Supabase.** Julio: la planilla dice ARS 2.920.287 y `sales` dice
  3.026.640 — 106.353 de diferencia (3,5%). Antes de dar un número a un tercero, decidir
  cuál es la fuente.
- El `Timestamp` viene en formato `M/D/YYYY`, a veces con hora y a veces sin ella.
- Leer con `valueRenderOption="UNFORMATTED_VALUE"`: formateado, los decimales vuelven
  como texto con punto de miles y cualquier parseo ingenuo multiplica por mil.

---

## 11. `astronomy-pending-features.md`

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

---

## 12. `astronomy-premios.md`

---
name: astronomy-premios
description: "Sistema de premios de Astronomy Academy — las decisiones de diseño y de plata. Estado y números vigentes en premios-reclamar y retomar-medalla."
metadata: 
  node_type: memory
  type: project
  originSessionId: 929b961b-e090-4d4e-a61f-bcb861328e43
  modified: 2026-07-30T05:33:42.781Z
---

Sistema de premios de la academia. Este archivo guarda **las decisiones de diseño y de
plata**; el estado del código y los números vigentes están en [[premios-reclamar]] y
[[retomar-medalla]]. Estado completo:
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/ESTADO_PREMIOS.md`

## En producción desde el 29/07/2026

Lo que acá figuraba como "mergeado a `main` (`372bbfc`) pero sin deployar a propósito"
**ya está deployado**. El freno era que la pantalla abría por defecto el mes anterior
—junio, $104.720, con el botón de otorgar al lado— y el 29/07, al quedar el repo conectado
a Vercel, cualquier push la publicaba. La protección pasó a código: `PRIMER_PERIODO =
"2026-07"`, chequeado también en la acción que otorga. Ver [[premios-reclamar]].

## Lo irreversible que ya se hizo (28/07/2026)

**La tabla `premios` está creada** en Supabase `qeakrjnseboiulcojlcw` (Astronomy Oficial).
Verificado: 0 filas · las 2 viejas respaldadas en `awards_respaldo_2026_07` · `awards`
vaciada. **No se otorgó ningún premio**: nadie recibió créditos ni avisos.

## Decisiones de Facu, ya implementadas

- **Se cierra sólo julio, a principios de agosto.** Junio no se toca.
- Podio de **5 puestos** (4° y 5° pagan 3 y 2 créditos).
- **Dos meses seguidos sí, tres no**: quien encabezó los dos anteriores cede la punta.
- **Un aviso por alumno por mes**, no uno por premio.
- Forma del podio: ganador arriba y solo, 2° y 3° a los costados, 4° y 5° chiquitos abajo.
- **Los costos son sólo del admin.** El salón público no muestra créditos ni pesos.

## El error de arte que costó rehacer todo

La primera versión eran medallas de **oro, plata y bronce**. Mal, y estaba escrito en dos
lugares: el manual de Academy son **tres colores** (blanco, negro, azul marino `#180040`) y
[[app-color-direction]] dice que **el dorado está afuera**. Lección: antes de elegir una
paleta, leer [[astronomy-brand]] y las memorias de color — no inventar una.

La versión buena distingue el puesto **por forma, no por color**: rayos y aro doble para el
1°, aro doble para el 2°, aro simple para el 3°, aro punteado para 4° y 5°. El violeta va
**sólo en el primer puesto**. La estrella es la asimétrica del manual, la que también es
una A.

## Lo que falta: NADA (rediseñado el 30/07/2026)

Ya no hay que otorgar nada a mano. Los **objetivos** (hitos y rachas) se entregan solos
apenas se cumplen, desde el cron horario, y el **podio** se publica solo el día 1 con el
mes cerrado. Julio entregó sus 46 objetivos el 30/07 (320 cr, 23 alumnos) y el podio sale
el 1/8 sin que nadie toque nada. Detalle en [[retomar-medalla]].

**El número vigente, medido el 30/07 con julio completo y el fix de doble conteo aplicado:
380 créditos = $234.080**, 52 premios (38 hitos · 5 podio · 9 rachas) entre 23 alumnos, a
$616 el crédito. (El 28/07 se había medido 360 cr / $221.760 con las clases hasta ese día:
no se contradicen, es otro corte. Detalle en [[retomar-medalla]].)

Es de **arranque, no de régimen**: los hitos se cobran una vez en la vida y hoy nadie cobró
ninguno, así que el primer cierre paga toda la historia junta. Del segundo mes en adelante
quedan casi sólo podio y rachas (~190 cr/mes). Y no es plata de la caja: son créditos para
usar el estudio.

## El sistema viejo ya no existe (28/07)

`/admin/metricas` tenía botones "Premiar" / "Publicar top 5" / "Despublicar" que escribían
en la tabla `awards` y mandaban mail con emoji. **Borrado entero**, junto con
`app/actions/metrics.ts`, `lib/badges.ts`, `PremioArt.tsx` y `BadgeArt.tsx`. Los rankings
quedan de sólo lectura. La tabla `awards` sigue vacía en Supabase y **ya no la lee nadie**:
se puede dropear cuando quieras.

**Tensión de marca abierta:** las medallas usan `#180040` de fondo (del manual) pero el
acento del 1° puesto es `#8b5cf6`, el violeta de la app, que no está en el manual. Sin
decidir.

Ver también [[astronomy-web-revision]].


## El giro 3D del isotipo — dos trampas que costaron caro (31/07/2026)

El giro de las medallas es un sprite del render 3D real, usado como **máscara** (su alfa es
la luminancia; el color lo pone el CSS, por eso una sola pieza sirve para las 5 rarezas).
Archivo: `public/premios/isotipo-giro.webp`. Vuelta = **3317 ms**, el período exacto del
video, medido cuadro contra cuadro.

1. **`steps(N)` sin `jump-none` desliza el logo de lado como un carrusel.** Con
   `mask-size: N × 100%`, la posición p% muestra el cuadro `p/100 × (N-1)`; `steps(N)`
   reparte p en k/N y esos valores caen SIEMPRE entre dos cuadros. `jump-none` reparte en
   k/(N-1) y da los enteros.
2. **Una tira de 8640 px no se ve en el celular.** Muchos GPU de teléfono no decodifican
   texturas de más de 4096 px: la máscara falla y el elemento queda enmascarado entero, sin
   error en consola. Va en **grilla 8×6 (1440×1080)** con dos animaciones — la X recorre
   una fila (`total/filas`), la Y baja de fila (`total`).

**How to apply:** un sprite CSS grande se prueba SIEMPRE en un teléfono real. Chrome
emulando móvil usa la GPU de la Mac y no reproduce el límite de textura.

## Podio: 20/10/5/5/0 desde agosto 2026

Facu pidió números redondos ("5/10/15/20…"). Eran 20/10/5/3/2. **El mes sigue costando 40
créditos** — el cambio ordena la escala, no mueve la plata. El 5° puesto se lleva la
medalla sin créditos, igual que "Primera vez en la cabina".

---

## 13. `astronomy-quien-factura.md`

---
name: astronomy-quien-factura
description: "Astronomy Academy cobra a la cuenta personal de Mercado Pago de Vladimir Nadinic — persona física, no sociedad. Razón social, CUIT y domicilio publicados."
metadata: 
  node_type: memory
  type: project
  originSessionId: 929b961b-e090-4d4e-a61f-bcb861328e43
  modified: 2026-07-28T18:22:10.726Z
---

La plata de Astronomy Academy entra a la **cuenta de Mercado Pago de Vladimir Nadinic**,
que es **persona física, no una sociedad**.

| Dato | Valor |
|---|---|
| Razón social | Vladimir Nadinic |
| CUIT | **20-41662712-7** (dígito verificador validado; prefijo 20 = persona física) |
| Domicilio comercial publicado | Avenida de los Colegios 160, Nordelta, Tigre, Bs. As. |
| Nombre de fantasía en MP | Astronomy |
| Cómo figura en el resumen de tarjeta | `ASTDOM` |
| Mail de la cuenta MP | vladonadinic@gmail.com |

**Origen (28/07/2026):** `GET api.mercadopago.com/users/me` con el token de la cuenta.
El domicilio lo dio Facu — **no** es el que figura en MP (Echeverría 1200, General
Pacheco), que es particular y no corresponde publicar en una web indexada.

**Por qué importa, más allá del dato:** si cobra una persona física, **el vendedor legal
es Vladimir**. Los términos y condiciones del sitio lo obligan a él, y un reclamo de
Defensa del Consumidor le cae a él, no a "Astronomy Academy" ni a los otros tres socios.
No se corresponde con el reparto societario 35/35/15/15 del CLAUDE.md global.

**How to apply:** vive en `lib/empresa.ts` del repo `astronomy-members`, en un solo lugar,
y de ahí lo toman el footer y las tres páginas legales. Si algún día se constituye una
sociedad y la cuenta de cobro cambia, se toca ese archivo y listo. Ver
[[astronomy-web-revision]] y [[membership-system-project]].

**Pendiente de Facu, no de código:** inscribir la base de datos de alumnos en el Registro
Nacional de Bases de Datos de la AAIP (Ley 25.326, art. 21), y que un abogado revise los
Términos —sobre todo el tratamiento de alumnos menores de edad—.

---

## 14. `astronomy-web-revision.md`

---
name: astronomy-web-revision
description: Auditoría completa de la web de Astronomy (27/07/2026) — dónde vive el informe y las 5 decisiones que Facu tiene pendientes
metadata: 
  node_type: memory
  type: project
  originSessionId: 18ad68d7-f0e0-45b0-8756-88b4b6243c8b
  modified: 2026-07-30T04:46:35.688Z
---

Revisión integral de `astronomy-members/` (sitio público, Academy, Dominé, membresías,
back office de admin y de profes) hecha el **27/07/2026**. Informe completo con números
medidos en:
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/REVISION_WEB_2026-07-27.md`

Hallazgos que mandan (medidos, no estimados): `/eventos` público no vende nada aunque la
ticketera está entera en el back office · checkout de entradas sin terminar · 2.618
estilos inline con 35 tamaños de fuente y 15 radios distintos (no hay sistema de diseño) ·
264 emojis contra la propia regla del repo · sin robots.txt ni sitemap.xml · home con
2,6 s de TTFB porque `proxy.ts` y `SiteHeader` llaman los dos a `auth.getUser()`.

**De las 5 decisiones que estaban pendientes, quedan 2** (las otras tres se cerraron el
28/07, están más abajo):

1. Modo Profesional: ¿sigue como isla de diseño o se sube TODA la marca a ese look (negro puro, tipografía grande, violeta solo de acento)?
2. `/eventos`: ¿la galería sigue linkeando a Instagram o pasa a `/eventos/[slug]`? (Hoy la ticketera está congelada, ver [[eventos-libro-compartido]].)

**How to apply:** antes de tocar estética de la web, leer el informe y resolver esas dos.
Ver también [[membership-system-project]], [[estetica-sin-emojis]],
[[app-aesthetic-rules]], [[estetica-simetrica-siempre]].

---

## Estado al 28/07/2026 — YA HECHO Y EN PRODUCCIÓN

Sistema de diseño construido y deployado a `astronomyofficial.com`:
`app/tokens.css` (medidas) + `app/ui.css` (primitivas) + `components/ui/Icon.tsx`
(51 íconos) + `components/ui/DataTable.tsx` (regla de las 20 filas, mobile = tarjetas).
Guía viva en **`/admin/estilo`**. **264 emojis → 0** en 78 archivos.
Migradas: `/admin/usuarios`, `/admin/revisar`, `/admin/cobros-mes`.

Handoff completo con lo que sigue y las preguntas abiertas:
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/ESTADO_28-07-2026.md`

**Git (al 30/07):** ya está todo en `main` y pusheado — y desde el 29/07 **el push a `main`
deploya solo** ([[vercel-deploy-astronomy]]). Lo que decía este archivo sobre la rama
`fix/auditoria-creditos` sin pushear quedó viejo.

**Decisiones cerradas:** **vencimiento = 2 meses** desde el último pago (gana el código,
no el `HANDOFF.md`; ver [[regla-creditos]]) · **el producto se llama "Modo Profesional"** y
el H1 del landing ya dice así, igual que el cobro de MP · **`/profesores` se linkea**, ya
está colgada de `/academy` · ticketera congelada y sin nada público
([[eventos-libro-compartido]]) · Academy y Eventos separados
([[academy-y-eventos-separados]]) · premios Magnitud 1/2/3 sin el slot de evento.

**Trampa aprendida:** nunca normalizar espacios con regex global sobre el repo — un
`re.sub(r'[ \t]{2,}...')` colapsó la indentación de 66 archivos y `tsc`/`next build`
dieron verde igual. El error solo se ve en `git diff --shortstat`.

---

## 3ª sesión (28/07) — el embudo público

Rama **`web/embudo-publico`** (3 commits), **sin pushear y sin deployar**: espera OK de Facu.

`/` y `/eventos` pasaron de dinámicas a **estáticas**. La palanca: `SiteHeader` llamaba a
`auth.getUser()` y eso solo vuelve dinámica a cualquier página. Se partió en `SiteHeader`
(server) + `PublicHeader` (cliente, pide `/api/header`), con la lógica única en
`lib/headerState.ts`. Además `proxy.ts` pasó a **lista positiva de rutas**.
También: `robots.txt`/`sitemap.xml` (daban 404), títulos con `template`, **canonical en cada
landing** (la pauta de Meta agrega `?fbclid=`), `/eventos` con `next/image` (1.372 KB → WebP
lazy), H1 del landing `CURSO PROFESIONAL DE DJ` → **`MODO PROFESIONAL`** (el cobro de MP ya
decía así), y `/profesores` por fin linkeada desde `/academy`.

**Lo que sigue:** `/academy` es la única landing que quedó dinámica y es la que más plata
mueve — la frenan `searchParams`, su propio `getUser()` y las consultas de precios/profes.
Y el sitio público **sigue lleno de `style={{}}` inline**: el sistema de diseño llegó a
`/member` y al back office, no a las páginas que ve la pauta.

---

## 4ª sesión (28/07) — legales y navegación · TODO DEPLOYADO

Dos deploys a producción; `main` al día. **`astronomyofficial.com/privacidad` da 200**, con
lo cual la app de Meta `astronomy-ads` (ID 2994790630727835) quedó destrabada.

Nuevas: **`/terminos`** y **`/arrepentimiento`** (Resolución 424/2020, la falta que más se
sanciona). Las tres legales salen de `<LegalShell />`. `/privacidad` suma la sección
anclada **`#eliminacion-de-datos`** — **ésa es la URL que hay que cargar en el panel de la
app de Meta**, que hoy apunta a `facebook.com`.

**Datos del proveedor: ya cargados y publicados** — ver [[astronomy-quien-factura]]. Salieron
de la API de Mercado Pago, no de memoria, y el vendedor resultó ser **persona física**
(Vladimir Nadinic), no una sociedad. Viven en `lib/empresa.ts`, en un solo lugar.

Queda pendiente **para Facu, no para código**: inscribir la base en el **Registro Nacional
de Bases de Datos de la AAIP** (Ley 25.326 art. 21), que es trámite; y que un abogado
revise los T&C.

**Navegación:** `/login`, `/registro`, `/recuperar` y `/nueva-contrasena` usaban el nav del
**back office** — le ofrecían "Mi panel" y "Mi cuenta" a alguien sin cuenta. Ahora usan
`<AuthNav />`. `<Volver href>` unificado, y los botones nombran su destino.

---

## 5ª sesión (28/07) — el sitio público entero sale del CDN · DEPLOYADO

**Ya no queda ninguna página pública dinámica.** `/`, `/academy`, `/eventos`,
`/profesores`, `/curso-profesional-dj` y las tres legales, todas `○` y en
**0,12–0,19 s** en producción. `/academy` venía de 0,47–1,05 s y `/profesores` de 0,35 s.

Lo que ataba a `/academy`: `searchParams` (`?curso=err`), el `getUser()` de los CTA y el
cliente de Supabase que lee cookies. Los tres se sacaron; quedó con `revalidate = 300`,
así un cambio de precio entra sin deployar.

**La pieza clave es `lib/sesionCliente.ts`:** memoiza la promesa **a nivel de módulo**, así
los cinco componentes que preguntan por la sesión comparten UNA petición a `/api/header`.
Verificado con el net-log de Chrome (`--log-net-log`), contando `URL_REQUEST` reales.

**El patrón que hace que no se note:** las dos variantes de un botón de compra dibujan el
mismo botón con el mismo texto y sólo cambia el destino → cero parpadeo. Donde el texto SÍ
cambiaría (el header, el "¿no tenés cuenta?"), no se dibuja nada hasta saber.

**Verificación que vale repetir:** screenshot de la página contra producción y diff de
píxeles. `/academy` dio **diferencia cero** — la prueba más fuerte de que un refactor de
renderizado no cambió nada visible.

**Dos trampas de CSS de este repo:** `globals.css` importa `ui.css` arriba de todo, así que
a igual especificidad **globals gana por orden de fuente** (se resuelve con doble clase,
`.section.legal`, nunca con `!important`). Y el `p` global va `text-align: justify`, que en
cualquier columna angosta abre huecos entre palabras.

**Trampa de CSS que costó un rato:** `.card` trae `margin-left/right:auto`; dentro de un
grid eso dimensiona el item a **fit-content**. Al pasar el `<img>` a `next/image` con `fill`
(que es `position:absolute`) la foto dejó de aportar ancho intrínseco y **cada card se
encogió al ancho de su título**. `next build` y `tsc` dan verde: se ve sólo mirando.
Corolario: un screenshot headless **sin `--virtual-time-budget`** sale a medio cargar —
compararlo contra uno que sí lo tenía inventa regresiones.

---

## 15. `atribucion-pagos-corte-web.md`

---
name: atribucion-pagos-corte-web
description: Los pagos sin dueño sólo se persiguen desde que la web salió a producción (14/07/2026); lo anterior se archiva sin tocar
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e442b324-11da-4e75-9d68-dabfd0f2cf2a
  modified: 2026-07-30T04:39:35.221Z
---

**Sólo se atribuyen los pagos posteriores a que la web salió a producción: 14/07/2026.**
Todo lo que quedó sin dueño de antes de esa fecha se archiva y no se toca. Pedido explícito
de Facu el 30/07/2026, mirando la cola de `unassigned_payments`: *"si es antes de junio
olvidate, poné en tu memoria que solo agarre desde que se creó la web que a fin de cuentas
son los que importan"*.

**Why:** los pagos anteriores son de la era Calendly + planilla. Sus créditos ya entraron
por dos caminos —la migración de alumnos del 14/07 y la reconciliación fina a mano del
21/07— así que atribuirlos hoy no corrige un saldo: lo **acredita dos veces**. Perseguirlos
es trabajo de bajo valor con riesgo de romper saldos que ya están bien.

**How to apply:**
- El corte es la fecha del pago, no la de la fila en la cola.
- Medido el 30/07/2026: los 28 pagos sin dueño (abril 1 · mayo 15 · junio 12, $4.210.440)
  son **todos** anteriores al corte. La cola queda vacía a efectos prácticos.
- Desde el 17/07 no cayó ni un pago nuevo sin atribuir: la atribución automática del cron
  `sync-sheet` está funcionando. Si aparece uno nuevo, **ese sí** se resuelve, y se resuelve
  agregando el alias para que no vuelva a fallar.
- La regla de NUNCA matchear por parecido de nombre sigue valiendo entera para los que sí
  se atribuyen: ver [[atribucion-pagos]].

Relacionado: [[reconciliacion-pagos-sistema]], [[membership-system-project]].

---

## 16. `atribucion-pagos.md`

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

---

## 17. `aviso-contexto-sesiones.md`

---
name: aviso-contexto-sesiones
description: Facu quiere que le avisen al 50% de contexto para cerrar la sesión y abrir una nueva; el aviso está automatizado en un hook
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2cbbb6c9-3ebc-45ea-8f08-1b2d8f768789
  modified: 2026-07-28T03:07:19.705Z
---

Facu pidió (27/07/2026) que se le avise **al llegar al 50% de la ventana de contexto**,
para cerrar la sesión y arrancar una nueva antes de que baje la calidad de las respuestas.

**Why:** trabaja sesiones largas sobre plata real y prefiere cortar temprano a que las
respuestas se degraden sin que él lo note. No quiere tener que mirar un indicador: quiere
que se lo digan.

**How to apply:** ya está automatizado, no hace falta acordarse.
- `~/.claude/scripts/statusline.sh` muestra el `ctx %` y a partir del 50% cambia el texto a
  un aviso explícito (antes estaba roto: buscaba `context.used_tokens` en vez de
  `context_window.used_percentage`, y nunca mostró nada).
- `~/.claude/scripts/aviso-contexto.sh` corre como hook `UserPromptSubmit` e **inyecta el
  aviso en el contexto**, una sola vez por umbral (50 / 65 / 80 / 90).

Cuando llegue el aviso: decírselo en una línea al final de la respuesta, y si hay trabajo a
medio hacer, ofrecerle un resumen de estado para pegar en la sesión nueva. El handoff se
escribe en el `ESTADO.md` del negocio que corresponda, no solo en el chat.

Relacionado: [[cada-numero-con-su-negocio]]

---

## 18. `cada-numero-con-su-negocio.md`

---
name: cada-numero-con-su-negocio
description: "Todo número o hallazgo se reporta con el negocio al que pertenece, explícito — nunca una lista de plata sin etiquetar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33ec0f09-121b-4802-a441-1b27de7b7267
  modified: 2026-07-30T04:43:35.643Z
---

**Cada número que le reporto a Facu lleva su negocio adelante, explícito.** El
27/07/2026 le listé hallazgos de plata de Paseo Nordelta a continuación de un tema
de Astronomy, sin etiquetarlos, y me corrigió: *"No mezcles paseo nordelta con
astronomy"*.

**Why:** Facu maneja tres negocios con sociedades, socios y bancos distintos (Astronomy,
Paseo Nordelta, campos), y cada uno tiene su propia caja. Un hallazgo sin etiqueta lo
obliga a adivinar de qué caja está hablando — y en plata, adivinar es exactamente lo que
no se hace. El mismo criterio separa las bases dentro de un negocio:
[[academy-y-eventos-separados]].

**How to apply:** en cualquier mensaje que toque más de un negocio, cada monto,
hallazgo o pendiente va precedido por el negocio ("Paseo: …", "Astronomy: …").
Nunca una lista de plata mezclada ni heredando el contexto del párrafo anterior.
Vale también para los ESTADO.md, los reportes y los mails que se preparen.

---

## 19. `calendario-publico-horarios.md`

---
name: calendario-publico-horarios
description: "/horarios — el calendario público de horarios libres del estudio para mandarle a un lead: qué muestra, por qué son dos espacios y no cuatro, y que falta pushear"
metadata: 
  node_type: memory
  type: project
  originSessionId: 781a50f0-fe21-4567-8aa2-246290fda571
  modified: 2026-07-31T18:10:07.552Z
---

**`/horarios`** en `astronomy-members`: vista previa pública de los horarios libres del
estudio, para mandarle el link a un lead por WhatsApp. Pedido de Facu el 31/07/2026.
**EN PRODUCCIÓN desde el 31/07/2026: https://astronomyofficial.com/horarios** (200
verificado). Linkeado desde `/academy`, abajo de la grilla de profes, donde antes estaba
el "ver todos los profes" que Facu mandó sacar.

Archivos: `app/horarios/page.tsx`, `components/HorariosPublicos.tsx`, bloque `hp-*` al
final de `app/ui.css`.

## Las decisiones que no son obvias

- **No reserva nada.** Sin login, sin botón. La única salida es WhatsApp, que es por
  donde hoy hablan todos los leads (ver [[roles-jose-luki]]).
- **Los cuatro filtros que pidió Facu son DOS.** Él pidió cabinas / estudio / DJ / PRO y
  después aclaró: *"clases de DJ y alquiler de cabina de DJ sería mismo horario de
  disponibilidad, y alquiler de estudio de producción y clase de producción ocupan el
  mismo"*. O sea: se filtra por **espacio** (cabina · estudio), no por producto. Repetir
  los cuatro sería mostrar la misma grilla dos veces con nombres distintos.
- **Sale de `getSlotsByProf()`**, la misma función que usa `/reservar`. De todo lo que
  devuelve se usan sólo las dos claves de ALQUILER: la disponibilidad de un alquiler ES
  la del espacio (hereda el horario del estudio y se bloquea con cualquier reserva que lo
  ocupe, clase o práctica). Si acá hubiera una consulta propia, se desincronizaría.
- **Semana fija de lunes a domingo** (Facu, 31/07). Sábado y domingo ocupan **la mitad de
  ancho**: la forma dice que el estudio abre de lunes a viernes sin tener que explicarlo.
  La grilla distingue por qué un día está vacío —CERRADO, YA PASÓ o COMPLETO— y para eso
  `studio_hours` viaja al cliente (`diasAbiertos`), en vez de deducirlo por ausencia.
  Si en lo que queda de la semana no hay nada, abre directo en la siguiente.
- **En celular cada día es una tarjeta**, no una columna: encabezado con el número grande,
  el día y cuántos horarios, y las horas en dos columnas parejas de 58px. Los días vacíos
  colapsan a una tira de una línea y los pasados no se muestran.
- **`noindex` pero crawleable.** Es una grilla que cambia cada hora. No va al sitemap.
  Ojo: NO ponerlo en `Disallow` del robots.txt — si Google no puede entrar, nunca lee el
  noindex.

## Medido en Chrome de verdad, no a ojo

Script reutilizable: `scratchpad/medir.mjs` (CDP con el WebSocket nativo de Node 24, sin
dependencias) — screenshot + `scrollWidth` + conteo de nodos. A 1280px y a 390px:
`bodyScrollWidth == clientWidth`, cero desbordes, 38 horarios en los próximos 7 días.
`captureBeyondViewport: true` **duplica los elementos fijos** en la captura y parece un
bug de layout que no existe.

## Regla del estudio que Facu confirmó

*"Hay que cumplir con el horario del estudio primero y después el de los profes."* Es lo
que ya hace el código. Consecuencia viva: **Mateo Pastrana tiene disponibilidad cargada
los 7 días pero `studio_hours` sólo abre lunes a viernes de 14 a 22**, así que sus turnos
de sábado y domingo no existen para nadie. Facu no pidió abrir el fin de semana.

Relacionado: [[astronomy-pending-features]], [[public-site-vision]], [[app-aesthetic-rules]].

---

## 20. `cartera-inversiones-personal.md`

---
name: cartera-inversiones-personal
description: "Facu tiene una cartera de brokerage personal en USD, un área que no figura en su CLAUDE.md de los tres negocios"
metadata: 
  node_type: memory
  type: project
  originSessionId: 076a8805-0da6-4767-a8d8-1e66bd91b295
  modified: 2026-07-27T15:55:11.860Z
---

Además de los tres negocios de su CLAUDE.md (Astronomy, Paseo Nordelta, campos), Facu maneja
una **cartera de brokerage personal en USD**. El seguimiento vive en
`~/Desktop/INVERSIONES_Facu.md` — ahí están posiciones, plan de compras, catalizadores y pendientes.

Insumo recurrente: recibe **reportes semanales de mercado de one618 Asset Management** (HTML, en
español). Los usa como tesis de referencia y valida su cartera contra ellos.

**Why:** es un área entera de su vida financiera que no está en el contexto global, así que sin
esto arranco una sesión sin saber que existe ni dónde está el doc.

**How to apply:** cuando pregunte sobre inversiones, leer primero `~/Desktop/INVERSIONES_Facu.md`
y actualizarlo después de cada operación (es él quien lo mantiene desfasado). Aplica de lleno su
regla de "plata real = cero improvisación": verificar precios reales del broker antes de recomendar,
nunca estimar. Si una búsqueda web falla o vuelve dudosa, decirlo explícitamente en vez de usar
el número igual.

---

## 21. `cron-que-nunca-fallo.md`

---
name: cron-que-nunca-fallo
description: "Un cron que siempre dice 'succeeded' puede no estar midiendo nada: pg_net corta a 5s y encolar no es completar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1c43742-0bd7-4763-abed-245cc4f34576
  modified: 2026-07-28T23:07:55.045Z
---

`sync-sheet` de Astronomy tenía 197 corridas `succeeded` en `cron.job_run_details` y
**las 197 respuestas HTTP habían muerto por timeout**. `pg_net` corta a los 5000 ms
(su default) y el endpoint tarda ~20 s.

`cron.job_run_details.status = 'succeeded'` sólo dice que el pedido se **encoló**.
El resultado real vive en otra tabla:

```sql
select id, status_code, error_msg, created
from net._http_response order by created desc limit 10;
-- 200 = terminó.  null + "Timeout" = se perdió la respuesta.
```

Funcionaba igual, de casualidad: Vercel sigue ejecutando la función después de que el
cliente se desconecta. Andaba sin que nadie pudiera distinguir una corrida sana de una
rota. Arreglo: `timeout_milliseconds := 120000` en el `net.http_get`.

**Why:** encaja con la regla del CLAUDE.md — *una verificación que nunca falló desde
que existe es sospechosa*. Acá el chequeo verde medía la cosa equivocada.

**How to apply:** ante cualquier tarea programada, antes de creerle al estado verde,
buscar dónde queda registrado el **resultado** y no el **despacho**. Y si no se
encuentra el scheduler donde se lo espera (`vercel.json`, launchd), eso no prueba que
no exista: puede estar en pg_cron de Supabase, en GitHub Actions o en otro lado.

Relacionado: [[finanzas-unificacion-sheets]].

---

## 22. `cuentas-internas-astronomy.md`

---
name: cuentas-internas-astronomy
description: "profiles.es_interno marca al equipo como no-alumnado en Astronomy — 9 cuentas, aplicado el 01/08/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: b8503d04-a79b-4350-b642-6dc953fcd9ab
  modified: 2026-08-01T10:50:58.929Z
---

**`profiles.es_interno` es la única fuente de verdad de "esta cuenta no es un alumno"**
en `astronomy-members` (base `qeakrjnseboiulcojlcw`). Aplicado el **01/08/2026** con OK
explícito de Facu; DDL en `supabase/internos.sql`, lógica en `lib/internos.ts`.

**Las 9 cuentas marcadas:** Facu (facue1900@) · Annie Hoffer · Lola Gallal · Vladimir
Nadinic · José Meyrelles · Luki · Mateo Guini · Mateo Pastrana · Valentino Frandolich.
Quedan **49 alumnos reales** de 58 cuentas. Sumar una es un `UPDATE`, no un deploy.

**Qué significa: "no es un alumno", nada más.**
- Los profes **siguen liquidando sueldo** — `/admin/sueldos` NO filtra por esto.
- La plata **sigue en el libro**, rotulada `INTERNO` y con un subtotal "sin internos" al
  lado del total, porque el libro tiene que cuadrar contra el extracto de Mercado Pago.
- En la base de usuarios **no se ocultan**: José necesita entrar a la ficha de un profe
  para darle permisos.
- `/admin/eventos-estudio` sí las oculta, **pero dice cuántas dejó afuera**.

**Reemplazó a dos listas de mails hardcodeadas** (`EXCLUIR_RECONCILE` en `lib/payments.ts`
y `EXCLUIR_PREMIOS` en `lib/premiosData.ts`) que sólo miraban la reconciliación, la
cobranza y los premios — y que además apuntaban a cuentas **ya borradas**
(`facu1900@`, `demo.gold@`, `facue1900+alumno@` no existen en `auth.users`).

**Impacto real medido, no estimado:** panel 58→49 usuarios y 8→7 alumnos activos (era
1 suscripción de Facu en `authorized`); 19 filas ocultas en el historial del estudio (17
de Facu), **todas canceladas**, así que las 1.592 concretadas no se movieron; métricas y
premios sin cambio —los bookings de Facu ya estaban todos cancelados— y **cero filas
internas en el libro**.

**Trampa para el próximo que agregue una columna:** pedirla dentro de un `select`
existente rompe la consulta ENTERA con `42703` mientras la migración no corrió, y el
resto de los campos vuelven vacíos. Va siempre en consulta aparte que degrade sola.

**La Management API de Supabase necesita `User-Agent`**: sin él Cloudflare responde 403
con `error code: 1010` antes de llegar a la API. Token en `~/facu-os/.env`
(`SUPABASE_ACCESS_TOKEN`), endpoint `POST /v1/projects/{ref}/database/query`.

Relacionado: [[postgrest-tope-1000]], [[astronomy-premios]], [[roles-jose-luki]],
[[annie-promo-account]], [[reconciliacion-pagos-sistema]].

---

## 23. `demo-account.md`

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

---

## 24. `djdelivery-facturacion.md`

---
name: djdelivery-facturacion
description: "DJ Delivery SÍ cobra solo por Mercado Pago desde 2024; lo que fallaba era que la app nunca registraba esos cobros en `sales`"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a510161-bc1d-481c-a0e4-40eb0e269423
  modified: 2026-07-29T13:43:27.886Z
---

**Corrige el pendiente que decía "pasar DJ Delivery a link de suscripción de MP".
Eso ya estaba hecho y no había nada que migrar.**

Verificado el 29/07/2026 contra la API de Mercado Pago con el token de producción.

## Lo que realmente pasa

Los suscriptores de DJ Delivery cobran solos desde un **plan de suscripción creado en el
panel de MP** (`preapproval_plan_id 2c9380849198d2b80191aff9001b070f`, el `plan_id` que
aparece en cada pago es `d57dbc6a4d304b8285a75eda443fe329`), no desde el checkout de la web.

| Estado en MP, 29/07/2026 | |
|---|---|
| Luca Nacucchio | `authorized` · $16.499 · próximo cobro 01/08 |
| Josefina Rawson | `authorized` · $16.499 · próximo cobro 01/08 |
| Tomás Papazián | **`paused`** · próximo cobro figuraba 07/08 · último cobro real 07/07 |
| Santi Pérez Dome | `cancelled` · último cobro 15/06 |

Tomás pagó con dos cuentas distintas (`tomaspapaziann@gmail.com` hasta ene-2026,
`tomas-papazian@hotmail.com` desde abr-2026): son la misma persona.

**42 cobros aprobados entre jul-2025 y jul-2026: $687.103,52 bruto / $642.615,05 neto**
(comisión de MP 6,47%). Ninguno figuraba en `sales`.

## El bug: dos guardas que lo tiraban antes de llegar a `sales`

En `lib/payments.ts`:

1. `creditPlan` cortaba con `if (!pl.monthly_credits) return` **antes** de llamar a
   `registrarVenta`. DJ Delivery da 0 créditos → salía por ahí siempre.
2. `registrarVenta` arrancaba con `if (!PLANES_CON_COMISION.includes(planId)) return`, y
   esa lista no incluye `djdelivery` (no comisiona al closer).

O sea: **no era que "DJ Delivery no pasa por MP"** —como decía `ESTADO_FINANZAS.md`—, sino
que la app tiraba el cobro. `lib/ingresos.ts` ya tenía la fuente "DJ Delivery" preparada
para leerla de `sales`: faltaba escribirla.

El puente no tenía la culpa: `mp_plan_map` ya mapea `d57dbc6a…` → `djdelivery`, y
`user_mp_payers` ya tiene los `payer_id` de los dos activos. Resolvía bien quién y qué.

## Al arreglarlo hay que cuidar tres cosas más

Meter DJ Delivery en `sales` toca a todos los que leen esa tabla:

- **Comisiones** (`lib/salaries.ts`): `computeTeamSalaries` y `ventasSueltas` comisionaban
  *toda* fila de `sales` sin mirar el plan → José habría cobrado comisión sobre DJ Delivery.
- **`payment_number` / `is_first`**: el contador define si el closer cobra el % de primer
  pago o el recurrente. Si DJ Delivery corre el contador, la primera membresía de ese
  alumno deja de ser "primer pago".
- **`nuevosDelMes`** (`lib/nuevos.ts`): suscriptores de 2024 aparecerían como "alumnos
  nuevos" del mes en que se arregló el registro.

Relacionado: [[finanzas-unificacion-sheets]], [[reconciliacion-pagos-sistema]],
[[egresos-sistema]], [[roles-jose-luki]].

---

## 25. `donde-aparece-un-pago.md`

---
name: donde-aparece-un-pago
description: "La pregunta de Luki: cuando se cobra una suscripción, en qué tablas y en qué pantallas aparece el pago, y dónde se ve el historial de créditos"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 781a50f0-fe21-4567-8aa2-246290fda571
  modified: 2026-07-31T18:10:25.050Z
---

Pregunta de Luki (31/07/2026): *"una vez que se cobra la suscripción de un miembro y
aparece el pago, ¿dónde debería aparecer? ¿En Libros? ¿Y los créditos, hay un historial?"*

**Sí a las dos.** Cuando Mercado Pago cobra, el webhook (`app/api/mp/webhook/route.ts`)
escribe en tres lugares, en una sola pasada:

| Tabla | Qué guarda | Pantalla |
|---|---|---|
| `payment_events` | El log crudo de MP, con `credited` true/false | `/admin/pagos-sin-asignar` (`/admin/pagos` redirige ahí) |
| `sales` | La venta = la facturación real | **`/admin/libro`**, columna "Entró" |
| `credit_lots` + `credit_transactions` | Los créditos y su vencimiento | Ver abajo |

**`/admin/libro` es la respuesta a "¿dónde aparece?"**: es la pantalla de toda la plata
con su signo, y reemplazó a `/admin/ingresos` y `/admin/egresos` justamente para que no
hubiera dos motores calculando el mismo mes.

Excepción: la **compra de créditos sueltos** (`buycredits`) no puede ir a `sales` (su
`plan_id` no existe en `plans`, que tiene FK) y se guarda en `manual_payments` con
`loaded_by_email = "Mercado Pago (automático)"`. Igual la lee el Libro.

## El historial de créditos existe y está en dos lados

- **El alumno**: `/member` → sección **"Movimientos de créditos"** (`CreditHistory.tsx`,
  últimos 50, muestra 4 y se expande).
- **Staff**: `/admin/alumnos/<id>` → **"◆ Movimientos de créditos"**, con la ficha entera.
- Para saber si los saldos CUADRAN, que es el problema recurrente de José:
  `/admin/auditoria-creditos`.

## Verificado con un caso real, no de memoria (31/07/2026)

Un pago de ese día se puede seguir entero: `payment_events` id `170502148365`, $36.960,
`credited: true` → `manual_payments` "Compra de 60 créditos sueltos", medio `mp` →
`credit_transactions` `+60 "Compra de 60 créditos"` a las 16:25 → a las 16:30 el mismo
alumno gastó `-40 "Alquiler de cabina"`. La cadena entera funciona sola.

Relacionado: [[finanzas-unificacion-sheets]], [[roles-jose-luki]], [[egresos-sistema]],
[[reconciliacion-pagos-sistema]], [[regla-creditos]].

---

## 26. `ecommerce-dropshipping-project.md`

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

---

## 27. `egresos-sistema.md`

---
name: egresos-sistema
description: "Sistema de egresos y finanzas unificadas de astronomy-members — /admin/egresos, /admin/finanzas, corte 2026-07-01"
metadata: 
  node_type: memory
  type: project
  originSessionId: 33ec0f09-121b-4802-a441-1b27de7b7267
  modified: 2026-07-27T23:31:23.837Z
---

La app `astronomy-members` registra **egresos** además de ingresos (desde 22/7/2026):
`/admin/egresos` (sueldos de profes y equipo, comisión real de MP, gastos a mano) y
el hub `/admin/finanzas` (solo el GrandMaster ve el resumen de plata; los admin con
`view_payments` ven solo lo operativo).

Claves que rompen si se olvidan:
- **CORTE = 2026-07-01** (`CUTOVER_ISO` en `lib/finanzas.ts`): antes → histórico
  JSON estático (sheet viejo dolarizado al blue del día); desde → sistema
  (sales/manual/expenses/sueldos/mp_fee). Junio está en ambos: el web se clampea
  al corte para no duplicar.
- `sales.amount` es lo que paga el alumno; la comisión MP va en `sales.mp_fee`/
  `mp_net` (las llena `syncMpFees()` en el cron horario).
- Los egresos cuentan cuando la plata SALIÓ, no lo devengado.
- Transferencias de sueldos NO se automatizan (decisión): "marcar como pagado"
  registra el egreso, la transferencia se hace a mano.
- Neto histórico total al 23/7/2026: **$9.085.440 / u$6.616**.

**How to apply:** detalle completo (pestañas del sheet, esquemas, decisiones) en
`~/facu-os/archive/memoria-importada/egresos-sistema.md`. Relacionado:
[[reconciliacion-pagos-sistema]], [[astronomy-finance-report]].

---

## 28. `estetica-simetrica-siempre.md`

---
name: estetica-simetrica-siempre
description: "Regla de Facu para toda interfaz — simetría, tamaños y colores consistentes, sin excepciones"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9d12a113-1306-41b8-960e-3cb20c41613d
  modified: 2026-07-30T04:43:45.556Z
---

**La estética tiene que ser simétrica siempre.** Facu lo pidió como regla permanente el
27/07/2026, después de que le entregara varias pantallas con asimetrías: tarjetas de
distinto ancho en la misma lista, un botón sólido al lado de un link subrayado, un
desplegable nativo blanco sobre un panel oscuro.

Aplica a **todo lo que construya para él**, no solo a lo que pida explícitamente:

- **Tamaños** — elementos del mismo nivel jerárquico miden lo mismo. Tarjetas de una
  lista: mismo ancho. Botones de un par: mismo alto y ancho. Nada de un elemento que se
  achica porque tiene menos texto.
- **Colores** — de los tokens del proyecto, nunca inventados. Si el contenedor define un
  tema (`.theme-admin` ámbar, `.theme-profe` teal), lo que se dibuje adentro tiene que
  heredarlo — ojo con los portales, que se cuelgan del `<body>` y pierden las variables.
- **Scroll — me lo pidió tres veces, no lo olvides.** Toda lista larga va con scroll propio
  y altura máxima, nunca estirando la página hasta el infinito. Regla concreta que dio:
  **más de ~20 filas → contenedor con scroll.** Barras finas y a tono, nunca las claras del
  navegador. Siempre `data-lenis-prevent` + `overscroll-behavior: contain`, porque Lenis
  (el scroll suave del sitio) se roba la rueda del mouse.
- **Minimizar y maximizar** — los bloques largos van plegables, y el estado se ve de un
  vistazo.
- **Bases de datos y tablas** — filtros siempre, y que se note cuál está activo.
- **Desplegables** — nunca el `<select>` nativo donde importe: abre la lista del sistema
  operativo y no se puede estilar. Usar `components/Select.tsx`.

**Why:** él mira las pantallas en uso y detecta la asimetría al instante, aunque no la
sepa nombrar. Cada vez que entrego algo desparejo pierde tiempo señalándolo y yo pierdo
un turno arreglándolo. Además su marca es de tipografía técnica y grilla estricta
([[astronomy-brand]]): lo desparejo se lee como descuido.

**How to apply:** antes de dar por terminada cualquier pantalla, **medir en el navegador**
—no mirar el código— que los elementos hermanos tengan el mismo ancho y alto. La causa
más común en este proyecto: `globals.css` tiene `.section > * { margin-left:auto;
margin-right:auto }` y `.card` también, así que dentro de un flex column cada tarjeta se
auto-centra y toma el ancho de su contenido en vez de estirarse. Se arregla con
`alignItems: "stretch"` + `width: "100%"` en las tarjetas.

Dónde vive cada proyecto: [[software-existente-respaldos]] y la tabla de paths del
`CLAUDE.md` de facu-os.

---

## 29. `estetica-sin-emojis.md`

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

---

## 30. `eventos-libro-compartido.md`

---
name: eventos-libro-compartido
description: "Cómo quiere Facu que se lleve la plata de un evento de Dominé — libro compartido estilo Splitwise, no porcentajes fijos"
metadata: 
  node_type: memory
  type: project
  originSessionId: 18ad68d7-f0e0-45b0-8756-88b4b6243c8b
  modified: 2026-07-28T02:53:46.705Z
---

Para la gestión de plata de un evento (Dominé / Puzzle), Facu quiere un **libro compartido
estilo Splitwise**, no un reparto con porcentajes fijos cargados de antemano:

- Los **costos se cargan a mano** — varían muchísimo de un evento a otro.
- Si alguien **pone plata**, se anota quién y cuánto.
- Si alguien **recauda**, también se anota.
- **Cualquiera puede anotar lo que recaudó otro.** Ejemplo textual de Facu: *"si Benja
  recaudó un millón de pesos de una mesa, que Facu pueda anotar ese ingreso para Benja"* —
  o sea que el movimiento tiene dos personas: el **sujeto** y **quién lo cargó**.
- Al cierre se **netea todo al valor del día de hoy** → cierre de caja automático y
  **el porcentaje que le toca a cada uno sale de lo que aportó y recaudó**, no de una tabla
  fija de socios.

**Why:** es cómo trabajan de verdad. Un 50/25/25 fijo (la regla de Puzzle) no refleja que
en un evento puntual uno puso la plata del venue y otro recaudó las mesas.

**How to apply:** una sola tabla `event_ledger` con `tipo` (aporte | recaudacion | gasto),
`persona` (el sujeto) y `cargado_por` (quién lo anotó) contesta las tres preguntas. El
neteo usa la serie del blue que ya existe en `lib/finanzas.ts` (`rateAt` / `getBlueHoy`) —
hay que fijar con Facu con qué cotización se netea. Relacionado: [[astronomy-web-revision]].

**Estado 27/07/2026: la ticketera está congelada por decisión de Facu.** No es prioridad y
no quiere nada público. Verificado ese día: 1 evento en la base, en `draft`, correctamente
oculto (404 para quien no sea GrandMaster). El rumbo cuando se retome sí está decidido:
checkout por Mercado Pago con página pública por evento.

---

## 31. `finanzas-unificacion-sheets.md`

---
name: finanzas-unificacion-sheets
description: "Las DOS planillas de finanzas de Astronomy, el doble conteo de $861.120 en `sales`, y por qué el diagnóstico de que el sync no corría era falso"
metadata: 
  node_type: memory
  type: project
  modified: 2026-07-30T04:46:07.367Z
  originSessionId: e1c43742-0bd7-4763-abed-245cc4f34576
---

Plan completo y verificado en
`~/Desktop/Productoras/Astronomy/Academia/astronomy-members/ESTADO_FINANZAS.md`.

## Corrección al diagnóstico del 28/07 (mañana)

Se creía que **`sync-sheet` no lo disparaba nadie**. **Es falso.** Está en **pg_cron
de Supabase**, no en `vercel.json`: `active`, cada hora, 197 corridas desde el
20/07/2026, y el historial de revisiones de la planilla muestra 37 de 38 escrituras
en el minuto 0 de cada hora. La planilla Base de Clientes está al día.

Lección: buscar el scheduler en `vercel.json` y no encontrarlo **no prueba** que no
haya scheduler. Ver [[cron-que-nunca-fallo]].

## Las dos planillas — no confundirlas

| Planilla | Rol |
|---|---|
| **Finanzas - Astronomy Academy** (`19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs`) | Donde **Luki carga** por Google Form. La app **sólo la lee**. |
| **Base de Clientes** (`1gj2JHtPqS8CGh2IdNa5vijCM3Zez9rNdFOudcRwFDKs`) | Donde `sync-sheet` **escribe**, 7 pestañas, cada hora. |

Decisión de Facu: todo se consolida en Base de Clientes. A la de Luki **no se le
escribe nunca**.

## El problema de plata real (28/07)

**`sales` cuenta 6 cobros dos veces: $861.120.** Mezcla dos orígenes sin deduplicar —
14 filas del webhook de MP (`mp_payment_id` numérico) y 34 importadas de la planilla
(`mp_payment_id` = `sheet:AAAAMMDD:NN`).

- Reporta $7.382.000 · **real $6.520.880** · inflada 13,2%.
- **Créditos NO duplicados** (verificado en `credit_transactions`).
- Script preparado y frenado: `supabase/limpiar_duplicados_sales.sql`.
- A revisar a mano: Fernando Lopez Peña, dos filas `sheet:` de $143.520 a 2 días.

## Luki: qué puede dejar de cargar y qué NO

De 49 ingresos suyos desde el 02/06, **42 ya los tenía la web sola**. Pero los otros
7 la web **no los captura**: 4 DJ Delivery, 1 Clase de Prueba, 1 fila en $0. Más
**11 egresos por $3.230.816** que la web no tiene.

> El corte es sólo para los cobros de Mercado Pago. Egresos, DJ Delivery y Clases de
> Prueba los sigue cargando él.

**Luki anota el NETO, la web el BRUTO** (35 de 42): $6.200.308 vs $6.520.880, la
diferencia es la comisión de MP ($320.572, 4,92%). El modelo de la web es el correcto.

## Estado al cierre del 28/07 (noche)

**Hecho y verificado:** 6 duplicados borrados de `sales` ($6.520.880 queda como
facturación real) · pg_net con timeout de 120 s · `/admin/registro` en producción
(commit `88959b6`) · tabla `incidencias` creada · fila falsa de suscripción de
Inchausty (`sheet:2007juanmai@gmail.com`) borrada.

## Cierre del 28/07 — puntos 2, 3 y 4 hechos (commit `41af05f`, **en producción desde el 29/07**)

- **Títulos por consecuencia.** "Martin Cañeque pagó $143.520 el 01/07 y no se le
  acreditó ningún crédito — en el Libro figura como «Martin Bernardo»". El nombre
  crudo del Libro va **al final**: es lo que se busca en la planilla, no el titular.
  La variante "no se le acreditó nada" sólo sale si la fila del Libro tiene
  `credits = null`; DJ Delivery da 0 por diseño y lleva la redacción de hueco de
  facturación.
- **Un pago, un problema.** Sin dueño + sin facturar era el mismo cobro con dos
  carteles. Gana sin dueño (es lo que destraba) y su instructivo llega hasta el final.
- **Un problema, un lugar.** `/admin/revisar` **cuenta y linkea**; `/admin/registro`
  **describe y resuelve**, filtrado por `?tipo=`. Fuera la prosa con nombres propios.
  De paso: el chequeo decía "Cobró en Mercado Pago" y los nueve casos venían del Libro.
- **Mobile**: `/admin/registro` pasó a `DataTable` (tarjetas bajo 720px). Medido a
  390px de viewport real con el truco del iframe de la lab note: `scrollWidth` 390,
  cero desbordes.

**El token de MP: usar SIEMPRE el de producción.** Está en
`astronomy-members/mp-prod.env` (prefijo `APP_USR-`) y responde bien contra
`api.mercadopago.com` desde la Mac. El de `.env.local` es `TEST-`: devuelve el preapproval
pero **0 pagos**, así que parece que anda y miente. Cualquier consulta de plata contra MP
va con el de `mp-prod.env`.

**Lo próximo, en orden:**

1. Fernando Lopez Peña contra el extracto (dos filas `sheet:` de $143.520 a 2 días).
2. **El corte de Luki**: mandarle `INSTRUCTIVO_LUKI.md`, que ya está escrito. Deja de
   cargar los cobros de MP **y DJ Delivery**; sigue cargando efectivo/transferencia,
   clases de prueba y todos los egresos.
3. `/admin/libro` con las dos fuentes.

**Tres pendientes que estaban acá ya se cerraron** (30/07) — no volver a abrirlos:

- ~~Inchausty sin próxima fecha de cobro~~ → **no tiene suscripción**: transfirió 8 clases
  de una. Las suscripciones sin fecha son 2, no 3, y las dos están bien (Floria a $1 y
  annie, cuenta promo). No hay plata perdida. Ver [[retomar-medalla]].
- ~~Los 51 pagos sin dueño de 2026~~ → **ya no se persiguen.** Son 28 y todos son
  anteriores a que la web saliera a producción; atribuirlos acredita dos veces. Regla en
  [[atribucion-pagos-corte-web]].
- ~~DJ Delivery a link de suscripción de MP~~ → estaba mal planteado: ya cobraban solos
  por MP desde 2024, el agujero era que la app no registraba esos cobros. **Arreglado y
  en producción.** Ver [[djdelivery-facturacion]].

Relacionado: [[astronomy-finance-report]], [[reconciliacion-pagos-sistema]],
[[egresos-sistema]], [[atribucion-pagos]], [[roles-jose-luki]], [[cron-que-nunca-fallo]].

---

## 32. `flyers-academy-generador.md`

---
name: flyers-academy-generador
description: "Skill `flyers` de facu-os — genera 75 placas de Astronomy Academy con precios sincronizados desde Supabase; qué NO volver a tocar"
metadata: 
  node_type: memory
  type: project
  originSessionId: 94994e33-93cd-4ea7-98ae-578879c7e059
  modified: 2026-07-30T04:44:11.664Z
---

Creado el 28/07/2026. Skill `flyers` en `~/facu-os/.claude/skills/flyers/`: genera
75 placas PNG de Astronomy Academy (5 productos × 5 ángulos × 3 formatos) y las deja
en `~/Desktop/Productoras/Astronomy/Academia/Flyers Academy/`, con hoja de contacto.

Productos: `curso-dj`, `produccion`, `produccion-online`, `membresias`,
`modo-profesional`. Ángulos: `precio`, `beneficios`, `profe`, `como-funciona`, `cta`.

**Lo no obvio, que se pierde si no queda escrito:**

- **Las piezas NO llevan precio en pesos** (decisión de Facu, 28/07/2026): con la
  inflación argentina un flyer publicado con un número queda viejo en semanas y
  obliga a rehacer la tanda. Solo sale lo que no se desactualiza —créditos, clases,
  módulos— y el valor del mes se pide por DM (`[ ESCRIBINOS POR DM ]`). El guard
  está en el código: `bloque_editorial()` revienta ante un bloque de tipo `precio`,
  así no alcanza con editar el JSON para que vuelva a salir un número.
- Los créditos tampoco se escriben a mano: `sync_precios.py` los baja de la tabla
  `plans` de Supabase (`monthly_credits`). Ver [[astronomy-catalog-data]].
- `produccion` y `produccion-online` no tienen SKU propio — se venden vía membresía
  (60 créditos la clase).
- El render usa el Chrome de `/Applications` en headless. **Nunca agregarle
  `--user-data-dir`**: cuelga el proceso indefinidamente en macOS.
- **La estética de @astronomy.academy NO es la de la app ni la de la marca madre.**
  Es un sistema editorial monocromo: negro puro o foto muy desaturada, Helvetica
  Neue en MAYÚSCULAS alineada a la IZQUIERDA y anclada abajo, micro-rótulos mono en
  las esquinas (`COMMUNITY-DRIVEN / EDUCATION`, `BUILT BY DJS / FOR DJS`,
  `WHERE MUSIC / CONNECTS US`…), cruces de registro, logo de **dos círculos**, y el
  llamado a la acción como etiqueta entre corchetes — **cero botones, cero violeta,
  cero firma cursiva**. El énfasis se hace con peso tipográfico, no con color.
  Estilo `editorial`, que es el default. Verificado contra capturas de la grilla
  el 28/07/2026. Contradice [[app-color-direction]] y [[astronomy-brand]]: esos
  valen para la app y el sitio, no para la cuenta de Academy.
- **Una foto distinta por ángulo, y el generador lo verifica** (29/07/2026). `foto`
  es campo del ÁNGULO, no del producto; `chequear_fotos()` corta la corrida si una
  se repite dentro de un mismo producto. Salió de un anuncio real: el carrusel de
  Modo Profesional salió con cuatro de cinco tarjetas con la misma foto y la quinta
  100% negra. Tampoco van tarjetas negras: las densas (bullets, planes) sobre foto
  muy oscura. Hay 14 fotos en `assets/fotos/`.
- **Para elegir foto se mide, no se mira**: luminancia media de la esquina inferior
  izquierda (donde el sistema ancla el titular) con el mismo grayscale/brightness
  del CSS. Arriba de ~60 no aguanta texto blanco.
- El logo de dos círculos está dibujado en SVG dentro del template — no existe el
  asset oficial en el repo. Si aparece, reemplazarlo.
- **El handle de Academy es `@astronomy.academy`**, distinto del de la productora
  (`@astronomy.oficial`, el que figura en [[astronomy-contacts-links]]).

Falta decidir: si la landing de producción online merece producto propio con precio
propio, hoy solo se vende adentro de la membresía.

---

## 33. `identidad-alumnos.md`

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

---

## 34. `medallas-reduce-motion.md`

---
name: medallas-reduce-motion
description: El iPhone de Facu tiene «Reducir movimiento» ACTIVADO — por eso las medallas se ven estáticas y no es un bug de CSS
metadata: 
  node_type: memory
  type: project
  originSessionId: b8503d04-a79b-4350-b642-6dc953fcd9ab
  modified: 2026-08-01T10:05:22.265Z
---

**El iPhone de Facu tiene «Reducir movimiento» activado** (Ajustes → Accesibilidad →
Movimiento). Confirmado por él el 1/08/2026.

**Why:** el CSS de `astronomy-members` apaga el giro a propósito cuando el sistema lo
pide (`app/ui.css`, bloque `@media (prefers-reduced-motion: reduce)`, con
`animation: none !important` sobre `.md-giro-tira` y `.md-giro-fila`). Así que en SU
teléfono la medalla queda congelada en el cuadro 0 — que se ve bien, es el isotipo de
frente, pero no gira. **Eso no es un bug y no se arregla tocando el sprite.**

El 31/07 se quemó media sesión persiguiendo tres bugs reales de sprite en iOS
(ver [[astronomy-premios]]) y quedó la sensación de que el giro seguía roto. No seguía
roto: era esta preferencia.

**How to apply:** cuando Facu diga que algo "no se anima" en el teléfono, **preguntar
primero si tiene Reducir movimiento activado** — antes de leer una línea de CSS. Y si
alguna vez se decide que el giro corra igual, es una decisión suya a tomar explícita:
sacar el respeto a `prefers-reduced-motion` empeora la app para quien lo activó por
mareo o migraña.

## Lo que se hizo el 1/08/2026 (en producción)

1. **Switch de movimiento en `/cuenta`** (`c73d25a`). La preferencia del sistema sigue
   siendo el default, pero se puede pisar **sólo para este sitio** con
   `data-motion="full"` sobre `<html>`, guardado en el dispositivo. Los cuatro bloques
   `@media (prefers-reduced-motion: reduce)` (tokens.css, ui.css ×2, globals.css)
   escapan por `:root:not([data-motion="full"])`. Lógica en `lib/motion.ts`, UI en
   `components/MotionToggle.tsx`. **El switch sólo se dibuja si el sistema está pidiendo
   menos movimiento.**
2. **La grilla ahora también gira** (`abb988b`). Antes el giro existía en un solo lugar
   —la ficha del premio abierto—; ahora `GaleriaPremios` pasa `volumen` en las dos.
   Para que no se pague caro: `will-change` quedó sólo en `.pr-medalla` (en la grilla
   eran 98 capas de GPU) y la grilla gira a la mitad de ritmo.

**Trampa que dejó ese cambio:** `.pr-cerrado .pr-art > svg` dejó de alcanzar a la
medalla cuando pasó a venir envuelta en `<div class="md-3d">`, y las medallas sin abrir
se veían nítidas. Se arregló sumando `> .md-3d`. **Cualquier selector con `>` sobre la
medalla hay que revisarlo si cambia `volumen`.**

Relacionado: [[astronomy-premios]], [[premios-reclamar]], [[retomar-eje]],
[[verificar-en-mac]].

---

## 35. `membership-system-project.md`

---
name: membership-system-project
description: "Astronomy Academy membership + credits system — scope, decisions, and demo status"
metadata: 
  node_type: memory
  type: project
  originSessionId: a22b1c54-e514-4f65-9904-35b311b90df5
  modified: 2026-07-30T04:44:22.034Z
---

Building a **membership + credits system** for Astronomy Academy (music school: DJ & production). Students pick a monthly membership, pay via Mercado Pago, credits accrue automatically, they book classes with a chosen professor, and credits are deducted automatically. See [[astronomy-brand]] and [[astronomy-catalog-data]].

**Decisions made (2026-07-09):**
- Approach: **demo visual first**, then wire the real backend.
- Payment: **Mercado Pago subscription** (automatic monthly rebill), not one-time.
- Credits: **accumulate but expire 3 months** after being credited.
- Scheduling: professor availability + **Google Calendar** integration (event created for student & professor on booking).

**Status:** Phase-1 interactive demo done. Demo simulates the whole flow client-side (localStorage), no real backend yet.

**Demo HTML — ya OBSOLETO, no es fuente de verdad de nada.** La app real está en producción; el demo era el paso previo. Al 30/07/2026 su única copia en disco quedó en `Productoras/Astronomy/_duplicados-revisar/Astronomy - Demo Membresias.html` (7 MB), una carpeta que existe para que Facu la vacíe: si la borra, el demo se va con ella y **está bien que se vaya**. Espejo viejo en el artifact `35e084c1-ed2c-44b3-b08e-b229acc4af33`.

**Etapa 2 progress (real build):**
- App lives in `/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members/` — **Next.js 16.2** (App Router, TS, Turbopack, React 19). Node installed via **nvm** (v24 LTS); load with `. "$HOME/.nvm/nvm.sh"` before npm/node. Next 16 note: middleware→**proxy.ts**, `cookies()`/`params`/`searchParams` are async. Read local docs at `node_modules/next/dist/docs/` — Next 16 differs from training.
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

---

## 36. `meta-ads-astronomy.md`

---
name: meta-ads-astronomy
description: "Las dos cuentas de Meta Ads, el costo real por lead de Academy, y por qué la app de WhatsApp no sirve para la API de pauta"
metadata: 
  node_type: memory
  type: project
  originSessionId: 56f9b80b-f934-42d7-8616-baefea6d84fe
  modified: 2026-07-31T21:41:35.308Z
---

Relevado el 28/07/2026 desde el export del Administrador de anuncios. Los CSV se
archivaron el 30/07 en `~/Desktop/Productoras/Astronomy/Academia/Pauta/`
(`CP---Astronomy-Academy-*.csv`; los `Facu-Estevez-*.csv` son de la cuenta vieja que no
se usa).

**La cuenta de pauta de Astronomy es `CP - Astronomy Academy`, en USD.** US$7.071
gastados entre ago-2023 y jul-2026 según el CSV del 28/07 (por API, al 30/07, US$7.111 —
la diferencia son los días de por medio, no un descuadre).

> En el mismo Business Manager aparece una cuenta `Facu Estevez` (ARS) con campañas
> `NP-*`. **Es vieja, ya no se usa, y Facu pidió expresamente ignorarla.** No
> analizarla ni mencionarla.

**El número clave: US$1,94 por conversación de WhatsApp nueva** (3.639 contactos
nuevos). Contra un CAC objetivo de US$57, la pauta cierra si se cierra 1 de cada 29
conversaciones (3,4%). Ver [[flyers-academy-generador]] para los creativos.

Las "5 compras" que reporta Meta **no son ventas**: la venta se cierra por WhatsApp y
Mercado Pago, fuera de todo píxel. Es un agujero de medición.

**Los nombres de los conjuntos mienten — leer siempre el `targeting` por API.** Ningún
conjunto de la cuenta usa públicos personalizados, ni los llamados "Interactors" ni
"Revinculado": nunca hubo remarketing. Todos usan edad 18-65 con Advantage+, así que eso
no explica diferencias. **La variable que sí separa buenos de malos es la geografía**:
históricamente, los conjuntos atados a un radio de 18 km gastaron 1.067–1.564 impresiones
por conversación; los de alcance país, 387–680. Pileta chica = saturación.

> Lo que corre HOY (un solo conjunto, radio de 35 km sobre Nordelta, sin intereses ni
> exclusiones) está inventariado anuncio por anuncio en [[pauta-inventario-y-publico]] —
> ése es el estado vigente; esta memoria es el análisis histórico de la cuenta.

**Gasto real: US$442/mes promedio** (no US$157). El archivo de finanzas registra
US$4.063 contra US$5.748 reales en 13 meses; hay 5 meses (ago/nov/dic-2025, jun/jul-2026)
sin una sola fila de pauta. "Pauta Publicitaria" tiene 5 filas en toda su historia — antes
de feb-2026 el medio iba mezclado dentro de "Gestión de Pauta".

> **TECHO DE US$500/MES — Facu, 31/07/2026.** Textual: *"quiero que te mantengas en un
> margen de presupuesto de 500usd por mes, si te pasas de eso tiene que ser por una razón
> que valga la pena invertir más dinero"*. **Esto reemplaza** lo que decía acá antes
> (*"pauta varía mes a mes, no pongamos un fijo"*, 30/07) — un día después puso el fijo.
>
> El techo es realista, no un recorte: el promedio real de los últimos 12 meses es
> **US$458/mes**. Detalle mes a mes y el plan de dos fases en [[retomar-pauta]].
>
> **La única razón válida para pasarse es un número medido**, no una corazonada: que esté
> cruzado que un dólar más de pauta trae más de un dólar de margen (códigos de WhatsApp
> contra `sales`). Sin ese cruce hecho, el techo es techo. Los presupuestos fijos escritos
> en `PLAN_PAUTA.md` son anteriores a esto.

**El token de API YA EXISTE** (resuelto el 29/07/2026, esto corrige lo que decía antes):
usuario del sistema `facu-os` sobre la app **`astronomy-ads`**, `expires_at: 0` — no vence
y no se cae si Facu cambia la contraseña de Facebook, que es lo que rompió al anterior.
Detalle y trampas de la API en [[pauta-carrusel-modo-profesional]]. El lector es
`active/astronomy/pauta/leer_meta.py` (descubre solo la cuenta, no hace falta el `act_`).

> Lo que quedó descartado: la app `Astronomy Message Sender` (ID 1005153115125458) es de
> WhatsApp, con *Productos disponibles* vacío, y **nunca** va a ofrecer `ads_read` /
> `ads_management`. No insistir con esa.

---

## 37. `no-robarle-la-pantalla.md`

---
name: no-robarle-la-pantalla
description: Nunca abrir ventanas visibles en la Mac de Facu — trabajar en segundo plano y avisar al final
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9d12a113-1306-41b8-960e-3cb20c41613d
  modified: 2026-07-27T20:13:10.063Z
---

**Trabajar siempre en segundo plano, sin abrir ventanas.** Facu lo pidió el 27/07/2026:
*"cada vez que usás mi compu, abrís Chrome o lo que sea, no me lo muestres porque a veces
estoy haciendo otras cosas y me sacás de mi pantalla"*.

Aplica a todo lo que corra en su máquina:

- **Chrome / Puppeteer** — `headless: "new"`, nunca una ventana visible. Si hace falta su
  sesión iniciada, se levanta headless apuntando al mismo `--user-data-dir`
  (`~/.claude-chrome-profile`): las cookies siguen ahí y no aparece nada en pantalla.
- **Nada de `open`, `osascript` ni abrir archivos** — ni un PDF, ni una imagen, ni el
  navegador. Si quiero mostrarle algo, se lo describo o le paso la ruta y lo abre él.
- **Servidores de desarrollo** en background, sin abrir el navegador.

**Why:** cada ventana que aparece le roba el foco y lo saca de lo que está haciendo. Trabaja
en tres negocios a la vez y su cuello de botella es el tiempo — una interrupción le cuesta
más que esperar el resultado.

**How to apply:** hacer todo el trabajo completo y **avisarle recién al final**, con el
resultado listo. Él lo mira cuando puede. Si necesito que haga algo (loguearse, apretar un
botón), se lo digo en el mensaje y espero — no le abro la ventana de sorpresa.

Va de la mano con [[estetica-simetrica-siempre]]: verificar midiendo en headless, no
mostrándole la pantalla.

---

## 38. `paseo-ctas-ctes-import.md`

---
name: paseo-ctas-ctes-import
description: Cuentas corrientes Paseo Nordelta — cómo se cobra cada local y qué falta para automatizar los cargos
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b70977d-f5a4-4025-981c-7a2f8c912611
  modified: 2026-07-28T15:26:57.158Z
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
  ("Diferencia Alquiler"), y **paga adelantado** (el cargo del mes se paga ese mes).
  Corregido el 28/07/2026: lo de "jun-26 tiene dos diferencias porque recuperó la de
  mayo" **era falso** — la fila estaba mal etiquetada. Ver la regla de abajo.
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

---

## 39. `paseo-nordelta-app.md`

---
name: paseo-nordelta-app
description: "App PWA de finanzas de Paseo Nordelta (local-first, Dexie) — qué es, dónde vive, y dónde está el detalle completo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 33ec0f09-121b-4802-a441-1b27de7b7267
  modified: 2026-07-27T23:31:15.775Z
---

Existe una **PWA de finanzas de Paseo Nordelta** (cobros, banco, caja, impuestos,
rentabilidad), base propia local-first. Vive en
`~/Desktop/Paseo Nordelta/Paseo Nordelta - CLAUDE/App Paseo Nordelta/`
(Vite + React + TS + Tailwind v4 + Dexie; `npm run dev` → localhost:5173).
Deploys por rol en Netlify: `lucent-buttercream` = Mati · `whimsical-alfajores` =
Inversores · `dancing-elf` = Admin.

Datos clave que ya tiene cargados y verificados:
- Junio 2026 reconciliado al peso (saldo cierre $4.119.498,46, neto +$5.428.379).
- **Fabric** (SUSHINOR): total a facturar $10.999.329/mes. **Bigg** (RODOLFO SRL):
  $5.158.624/mes, con alquiler 50% facturado con IVA y 50% "diferencia" sin IVA.
- Regla fiscal: el RECUPERO de gastos va como Nota de Débito NO GRAVADA; solo
  alquiler + gastos comunes llevan 21%.
- Carga de caja por lenguaje natural ("pagué 80mil al jardinero") + import de chat
  de WhatsApp.

**Why:** es el sistema operativo financiero del Paseo; sin saber que existe se
propone construir lo que ya está construido.

**How to apply:** el detalle completo (52 KB: módulos, bugs resueltos, decisiones)
está en `~/facu-os/archive/memoria-importada/paseo-nordelta-app.md` — leerlo antes
de tocar la app. Relacionado: [[paseo-ctas-ctes-import]], [[paseo-nordelta-web]].

---

## 40. `paseo-nordelta-web.md`

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

---

## 41. `passline-export-eventos.md`

---
name: passline-export-eventos
description: Cómo sacar y leer el export de Passline de un evento — qué columnas importan y los tres bugs del CSV
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2cbbb6c9-3ebc-45ea-8f08-1b2d8f768789
  modified: 2026-07-28T03:07:34.913Z
---

La ticketera de Puzzle (y de los eventos) es **Passline**. El export de ventas sí trae el
dato de asistencia, aunque la documentación pública no lo diga.

**Dónde:** panel de productor → Mis Eventos → Ventas / Reportes → descarga CSV
(`tickets_comprados_<idEvento>-<fecha>.csv`). Separador `;`, encoding utf-8-sig.

**Columnas que importan** (por índice, porque los nombres se repiten):
`0 Nombre · 1 Email · 3 DNI · 8 Tipo · 10 Cortesia (SI/NO) · 11 RRPP · 12 Total ·
14 Estado del eticket · 20 Nombre RRPP · 34 Fecha/Hora Validación`

`Estado del eticket` = **Validada** significa que la persona entró. Es *el* dato: sin él
solo se sabe quién compró, no quién fue.

**Tres trampas del archivo:**
1. Hay **dos columnas llamadas "Fecha/Hora Validación"**. La 34 es la fecha real; la 35 es
   el dispositivo que escaneó (`bali1234`, `control1`). `Código Activación` viene toda
   `31-12-1969` — epoch nulo, basura.
2. Las filas `Anulada` **no las cuenta el panel**. Hay que excluirlas o el total de
   cortesías da uno de más.
3. El header tiene 38 campos y las filas 39: hay un corrimiento al final. No afecta a
   ninguna columna útil, pero no confiar en los índices altos sin verificar.

**Siempre cruzar contra el panel antes de reportar**: capturar la pantalla de eTickets
(comprados / cortesías / validadas / total por tipo de entrada) y verificar que el parseo dé
igual. Ya salvó dos veces de reportar números mal.

Los datos de eventos van a `~/facu-os/data/eventos/` (gitignoreado): son miles de personas
con mail, teléfono y DNI. **Nunca al vault**, que se sincroniza.

Relacionado: [[eventos-libro-compartido]] · [[cada-numero-con-su-negocio]]

---

## 42. `pauta-carrusel-modo-profesional.md`

---
name: pauta-carrusel-modo-profesional
description: "Estado de la pauta de Astronomy Academy al 29/07/2026 — carrusel nuevo activo, y la decisión pendiente sobre el anuncio que se come el 72% del gasto"
metadata: 
  node_type: memory
  type: project
  originSessionId: a6298426-cff6-4848-ac49-0036e2e35bd6
  modified: 2026-07-30T04:35:21.612Z
---

**29/07/2026.** Facu vio el carrusel de Modo Profesional corriendo en su Instagram y
detectó dos defectos reales: la tarjeta 1 sin gancho y la foto de fondo repetida. Los
dos venían del generador — ver [[flyers-academy-generador]] y `LAB_NOTES.md`.

**Qué quedó en la cuenta `CP - Astronomy Academy`** (conjunto `IntWpp1 PresCurso
Nordelta`, id `120245002157210448`):

- **ACTIVO** `modo-profesional | carrusel | square | dolor | v2 | jul-26`
  (`120248150444820448`), con las 5 placas nuevas — verificado hash por hash contra
  `data/pauta/creativos.json`.
- **PAUSADOS** los dos carruseles viejos, los de las fotos repetidas:
  `modo-profesional | carrusel | square | dolor` (`120248128874040448`) y
  `modo-profesional | carrusel | square | v1` (`120248128330160448`). Entre los dos,
  US$0,38 y cero conversaciones.
- Siguen activos los cuatro anuncios `IntW2` de Curso de DJ.

**Cómo se nombran los anuncios** (y por qué importa): el nuevo nació con el nombre
**idéntico** al viejo que reemplazaba, porque salía de producto+formato+variante y la
variante no cambió. Se distinguían solo por el estado — un click de pausar el que no
era. La convención quedó en:

```
<producto> | <angulo|carrusel> | <formato> | <variante> | v<n> | <mes-año>
```

y **el `v<n>` no se escribe a mano**: `nombrar()` en `crear_carrusel.py` lee los
anuncios del conjunto, busca el número más alto de esa combinación y usa el
siguiente (arranca en `v2`; `v1` es el nombre viejo sin versión). Verificado: la
próxima corrida ya calcula `v3`.

## Fechas de nacimiento de cada anuncio — chequear ACÁ antes de decir "lleva N días"

Facu pidió el 30/07 que estas fechas queden guardadas, porque es fácil confundir **la
ventana del reporte** (`--dias 30`) con **la vida del anuncio**. Traídas de
`created_time` de la Graph API el 30/07/2026:

| Anuncio | id | Creado | Estado al 30/07 |
|---|---|---|---|
| `modo-profesional \| carrusel \| square \| dolor \| v2 \| jul-26` | `120248150444820448` | **29/07/2026 11:06** | ACTIVE |
| `modo-profesional \| carrusel \| square \| dolor` | `120248128874040448` | 28/07/2026 16:05 | PAUSED |
| `modo-profesional \| carrusel \| square \| v1` | `120248128330160448` | 28/07/2026 15:32 | PAUSED |
| `2IntW2 Curso de DJ` **(nuevo)** | `120248128929530448` | 28/07/2026 16:06 | ACTIVE |
| `2IntW2 Curso de DJ` **(viejo, homónimo)** | `120245002157260448` | 27/05/2026 12:44 | **DELETED** el 28/07 |
| `3IntW2 Flyer Curso de DJ` | `120245002157250448` | 27/05/2026 12:44 | ACTIVE |

**Toda la línea de Modo Profesional nació el 28 y 29 de julio de 2026.** No existe
ningún dato de ese producto anterior al 28/07.

**CORREGIDO el 30/07/2026 — la lectura del 29/07 estaba contaminada por un homónimo.**
Los US$0,83 eran del `2IntW2` **nuevo** con un día de historia; el homónimo viejo
corría a US$2,12 de por vida y se llevó US$382,97 de los últimos 30 días.

Números de por vida al 30/07 (con paginación completa — ver la trampa abajo):

| Anuncio | Vida | Gasto | Conv | US$/conv |
|---|---|---|---|---|
| `2IntW2` viejo (borrado) | 27/05 → 29/07, 59 días con entrega | 529,54 | 250 | **2,12** |
| `3IntW2 Flyer` | 27/05 → 28/07, 48 días con entrega | 378,19 | 159 | **2,38** |
| `2IntW2` nuevo | 28/07 → 30/07, 3 días | 34,84 | 39 | **0,89** |
| `MP carrusel v2` | **29/07 → 30/07, 2 días** | 0,60 | **0** | — |

Control: la suma de los 175 anuncios da US$7.111,24 contra el `amount_spent` que
declara Meta, US$7.110,61 — 0,009% de diferencia.

Estado real al 30/07:

- **`3IntW2` ya está desfinanciado por Meta solo.** Últimos 7 días: **US$2,10 (1,4%
  del conjunto)**; desde el 16/07 gasta centavos. El "72% del gasto" fue cierto antes
  del 16/07, no ahora. Pausarlo es prolijidad, no plata: ~US$0,30/día.
- **El nuevo `2IntW2` es el ganador y ya se lleva el 80% del presupuesto**: 39
  conversaciones a **US$0,89** en sus dos primeros días (28 y 29/07), 21k impresiones
  diarias.
- **El carrusel de Modo Profesional no tiene entrega, y con 2 días NO se puede
  concluir nada del creativo.** Lo que sí se puede comparar es el debut contra debut,
  porque los dos son nuevos y salieron con un día de diferencia del **mismo conjunto**:
  el anuncio de Curso de DJ hizo **22.218 impresiones su primer día**, el carrusel
  **277**. Ochenta veces menos, y no es fase de aprendizaje porque los dos arrancaron
  de cero.
- **La causa es estructural, no temporal:** la cuenta tiene **un solo conjunto activo**
  (`IntWpp1 PresCurso Nordelta Revinculado`, `120245002157210448`, US$19,56/día) y ahí
  adentro compiten Modo Profesional y Curso de DJ por el mismo presupuesto. Meta se lo
  da al ganador. **Modo Profesional no va a tener una prueba justa mientras viva en ese
  conjunto** — no es que fracasó, es que nunca se midió.

**El token de Meta ahora es de usuario del sistema** (`facu-os`, app `astronomy-ads`,
`expires_at: 0`): no vence y no se muere si Facu cambia la contraseña de Facebook —
que es exactamente lo que rompió el anterior. Tiene asignados la página, las dos
cuentas publicitarias, la app y la cuenta de Instagram.

Ojo con el **rate limit** (`code 17`): subir las 75 placas de una deja la cuenta
limitada varios minutos, y la API devuelve **listas vacías sin error visible** si no se
mira el campo `error`. Un conjunto con cero anuncios es un rate limit hasta que se
demuestre lo contrario.

---

## 43. `pauta-como-se-carga-el-egreso.md`

---
name: pauta-como-se-carga-el-egreso
description: "Cómo entra el gasto de pauta en la planilla de finanzas, por qué el extracto del Bank of America desfasa el margen mes a mes, y qué es cada subcategoría — medido el 31/07/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6cee032c-eb5a-4d15-803e-3002e64f1f53
  modified: 2026-07-31T22:08:19.883Z
---

Explicado por Facu el 31/07/2026 y medido contra la fuente ese día. Es la respuesta a
"¿de dónde sale el número de pauta que va al Form?".

## El método viejo y por qué desfasa

El monto se sacaba **del extracto del Bank of America** — lo que Facebook efectivamente
cobró. El problema: **el extracto cierra del 15 al 15 y Meta factura del 1 al 1**, así que
el monto cargado nunca es el del mes calendario.

**Medido: no falta ni sobra plata, está en el mes equivocado.** Las 5 filas de
`Pauta Publicitaria` de 2026 contra el gasto real de la API de Meta:

| Fila | USD cargado | USD real Meta | Dif |
|---|---|---|---|
| Facebook Ads - Enero 2026 | 297,35 | 214,81 | **+82,54** |
| Pauta Febrero | 220,46 | 249,45 | −28,99 |
| Pauta Marzo | 209,91 | 414,05 | **−204,14** |
| Pauta Publicitaria Abril | 613,71 | 514,59 | +99,12 |
| Pauta Mayo | 547,00 | 490,18 | +56,82 |
| **Total** | **1.888,43** | **1.883,08** | **+5,35 = +0,3%** |

Mes a mes se desvía hasta **49%**; en cinco meses cierra al **0,3%**. Marzo cargó US$204
de menos (≈ARS 288.000, **10 puntos de margen** sobre 2,86 M facturados) y abril US$99 de
más — o sea que el desfase mueve el margen mensual más que muchas decisiones de negocio.
Ver [[astronomy-margen-real]].

## El método correcto

**El monto de Meta sale de la API, del 1 al 1. El extracto del BofA se usa para conciliar,
no para determinar el monto.** `Real Date` = último día del mes.

Por qué, en orden de peso:

1. **La planilla ya es devengada, no de caja.** Los sueldos se cargan con `Real Date` del
   último día del mes al que corresponden aunque se paguen después. La pauta por fecha de
   débito sería el único rubro que rompe la convención — por eso es el único que zigzaguea.
2. **El ingreso está en mes calendario** (`sales` es 1 al 1). Egreso 15-al-15 contra
   ingreso 1-al-1 da un margen que se mueve por almanaque.
3. **No se pierde plata al cambiar**: 0,3% en cinco meses.

El extracto sigue haciendo falta para confirmar que el cargo salió y para cargar el resto
de lo que aparece ahí (Squarespace, Calendly, DJ Delivery y otros), que hoy cae en
`Suscripciones` — **86 filas, la subcategoría de egresos más grande**. Para ésas el
desfase 15-al-15 casi no molesta: son montos fijos, mes bancario ≈ mes calendario.

## Las dos subcategorías son cosas distintas — y una cambió de significado

| Subcategoría | Qué es HOY | Cuánto |
|---|---|---|
| `Pauta Publicitaria` | lo que se le paga a **Meta** | el techo, ver abajo |
| `Gestión de Pauta` | **una persona que ayuda con la pauta** | ~US$150/mes en 2026 |

**Ojo al leer el histórico: `Gestión de Pauta` significaba otra cosa antes.** Hasta
jul-2025 ahí se cargaba **el medio** — pagos a Facebook Ads y Google Ads, más el IVA del
21% en filas aparte. Desde sep-2025 pasa a ser el pago mensual al tercero, y en 2026 nace
`Pauta Publicitaria` para el medio. **Sumar toda la historia de `Gestión de Pauta` como si
fuera un solo concepto da un número sin sentido.**

En las filas de sep/oct-2025 el pago aparece como **"Ventas Claras" / "Cuentas Claras"**.
Facu confirmó que es **una persona**, pero **no confirmó el nombre** — el equipo de pauta
sigue como *"nombre pendiente"* en el CLAUDE.md global.

## El techo: US$500/mes son SOLO de Meta

Facu, 31/07/2026, textual: *"el techo de meta es 500 y los 150 son aparte para una persona
que nos está ayudando con la pauta"*. O sea el costo total de pauta ronda **US$650/mes**.
Ver [[meta-ads-astronomy]] y [[retomar-pauta]].

## Hipótesis sin verificar: el BofA ahorra el 51%

El IVA del 21% aparece en todas las filas de pauta de 2025 y **en ninguna de 2026**, que
es justo cuando empiezan a pagar con el **Bank of America** (cuenta en EE.UU., paga a Meta
en USD). Si la causa es ésa, pagar desde el BofA evita el 21% de IVA **más** el 30% de
percepción de RG 5617/24 — y **responde que NO conviene pasar a pagar Meta en pesos**, que
era un pendiente abierto. **Falta ver el extracto para confirmarlo.**

## Datos de la planilla

`Finanzas - Astronomy Academy`, ID `19N6pPrE6rEM8-ohkYIjwzi4ChZ1I91mfSjTrgaChiJs`, hoja
`Base`. Tiene columnas **`ARS_Ammount` y `USD_Ammount`**, así que el gasto de Meta se puede
cargar en su moneda nativa.

## El tipo de cambio se toma del DÍA EN QUE SE PAGÓ

Dicho por Facu el 31/07/2026. **No es el TC del cierre del mes ni el del día que se carga:
es el del día del pago.** Los TC implícitos de 2026 son entonces la cotización de esa
fecha: **1.440 (ene) · 1.395 (feb) · 1.410 (mar) · 1.420 (abr) · 1.470 (may)**.

Esto **no choca** con el criterio devengado: el **monto en USD** es el gasto devengado del
mes (1 al 1, de la API) y el **TC** es el del día en que esa plata se pagó. Igual que los
sueldos, que se devengan en un mes y se pagan al principio del siguiente.

**Nunca inventar el TC de un mes nuevo: hay que saber la fecha de pago.**

## Lo que falta cargar — retomar el 1/08/2026

**Junio y julio 2026 no tienen ninguno de los dos rubros** — ni `Pauta Publicitaria` ni
`Gestión de Pauta`. Meta: junio **US$498,84**, julio **US$528,84 y subiendo** (el 31/07 no
había cerrado; el definitivo se lee el 1/08).

**Lo que hay que averiguar antes de cargar nada** (Facu lo dejó para el 1/08, no se
acordaba):

1. **Cuándo se pagó junio** — de ahí sale el TC.
2. **Si ese pago fue en pesos o en dólares.**
3. **Cuánto se le pagó a la persona de gestión** en junio y julio.

**Julio todavía NO se le pagó** al 31/07 (dicho por Facu), así que esa fila no tiene TC
todavía y se carga cuando se pague — con `Real Date` de julio y el TC del día de pago.

---

## 44. `pauta-inventario-y-publico.md`

---
name: pauta-inventario-y-publico
description: "Inventario completo de lo que Astronomy Academy tiene pautado en Meta, con el copy de cada anuncio, el público exacto y el rendimiento histórico por formato — verificado el 30/07/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: a66a4ae5-626e-4cf6-b596-f3c2c98c0e83
  modified: 2026-07-30T05:08:20.784Z
---

Pedido de Facu el 30/07/2026: tener escrito **qué estamos pautando, a qué público y con
qué resultado**, para poder armar estrategia en vez de decidir anuncio por anuncio.
Todo verificado contra la Graph API ese día. Fechas de nacimiento de cada anuncio en
[[pauta-carrusel-modo-profesional]] — **chequear ahí antes de decir "lleva N días"**.

## La cuenta entera cabe en un solo conjunto

Cuenta `CP - Astronomy Academy` (`act_628045479472592`), moneda **USD**, gasto histórico
**US$7.111** en 24 campañas y 175 anuncios. Al 30/07 hay **un único conjunto activo**:

| | |
|---|---|
| Campaña | `Interaccion` · objetivo `OUTCOME_ENGAGEMENT` |
| Conjunto | `IntWpp1 PresCurso Nordelta Revinculado` (`120245002157210448`), desde 27/05/2026 |
| Presupuesto | **US$19,56/día** (~US$590/mes) |
| Optimiza | `CONVERSATIONS` · cobra por impresión · destino **WhatsApp** |

## El público es una sola cosa: 35 km alrededor de Nordelta

**No hay intereses, no hay públicos personalizados, no hay exclusiones, no hay idioma ni
ubicaciones elegidas.** El targeting completo es:

- **Geografía:** ubicación custom, radio de **35 km** sobre lat `-34.414559`, long
  `-58.645394` (Nordelta), `country: AR`.
- **Edad 18-65, todos los géneros.**

Esto confirma lo de [[meta-ads-astronomy]]: **la geografía es la única variable y los
nombres de los conjuntos mienten.** Un conjunto que se llama "Intereses 3" puede no
tener ningún interés cargado.

## Los 5 anuncios activos y qué dice cada uno

Cuatro son de **Curso de DJ** y comparten el mismo copy; uno es de **Modo Profesional**.

| Anuncio | Formato | Copy / contenido |
|---|---|---|
| `2IntW2 Curso de DJ` (`120248128929530448`) | imagen | "¿Querés aprender a mezclar como un profesional? / Clases presenciales en Nordelta, adaptadas a tu nivel y tu interés. / Música electrónica, horarios flexibles y práctica con equipos." |
| `4IntW2 Curso de DJ` (`120245002157230448`) | **video** (`1412436164237058`) | mismo copy |
| `1IntW2 Reel subtitulos` (`120245002157240448`) | **video** (`1708774983461378`) | mismo copy |
| `3IntW2 Flyer Curso de DJ` (`120245002157250448`) | imagen | **sin copy** (`message: None`) — el flyer solo |
| `modo-profesional \| carrusel \| square \| dolor \| v2 \| jul-26` (`120248150444820448`) | carrusel de **5 tarjetas** | "Mezclás hace dos años. Nunca tocaste para nadie. / No es que te falte talento. Es que nadie te dijo qué sigue después de aprender a mezclar… / Mandanos un tema tuyo y te decimos qué le falta." |

Tres anuncios de Curso de DJ con **el mismo copy** compiten entre sí en el mismo
conjunto. Y **el 100% del presupuesto activo apunta al Curso de DJ**, el producto más
barato del catálogo ([[astronomy-catalog-data]]).

## El video NO es el formato inexplorado — es el más probado

**Corrige lo que decía [[retomar-showcase]].** Medido sobre los 175 anuncios:

| Formato | Gasto histórico | Conv | US$/conv |
|---|---|---|---|
| **Video** | **US$3.356 (47,2% de la historia)** | 2.158 | **1,56** |
| Resto | US$3.755 | — | — |

El mejor anuncio de la historia de la cuenta es un **video**: `Astronomy 1`, US$535 a
**US$1,16/conv** con 460 conversaciones. El video está probado y rinde mejor que el
promedio de la cuenta (US$1,83).

**Lo que sí es cierto: los dos videos que corren HOY son malos.** No por el formato, por
la retención:

| Video | Gasto | US$/conv | Llegó al 25% | Lo vio completo |
|---|---|---|---|---|
| `4IntW2` | 31,65 | 2,43 | 11,1% | **1,5%** |
| `1IntW2 Reel subtitulos` | 21,59 | 4,32 | 4,8% | **0,7%** |

Un video nuevo bien hecho es la apuesta con mejor respaldo histórico de la cuenta.

## Los mejores anuncios de la historia (20+ conversaciones)

| US$/conv | Conv | Anuncio |
|---|---|---|
| 0,25 | 81 | Campaña de mensajes personalizada 29/05 |
| 0,35 | 42 | Anuncio de Búsqueda de Profesores |
| 0,56 | 49 | `1Int Busqueda de Profesores` |
| **0,67** | **120** | **`Curso DJ 2`** ← el mejor con volumen real |
| 0,76 | 108 | `Curso DJ 2` (otro conjunto) |
| 0,76 | 91 | `RAW Container` |
| 0,88 | 74 | `RAW Mansion Original` |
| 0,89 | 39 | `2IntW2 Curso de DJ` (el nuevo, 3 días) |

`Curso DJ 2` hizo 228 conversaciones a US$0,67-0,76 entre dos conjuntos. **Nadie miró
por qué ese creativo funcionaba tan bien** — es la pregunta más barata de responder que
tiene la cuenta.

## El agujero real: nadie mide conversación → alumno que paga

Meta cuenta **conversaciones de WhatsApp**, no plata. Lo que sabe la app
(`sales` en Supabase `qeakrjnseboiulcojlcw`, **solo tiene junio y julio 2026**, 42 pagos):

| Mes | Pagos | Primeros pagos | ARS |
|---|---|---|---|
| 2026-06 | 22 | 20 | 3.494.240 |
| 2026-07 | 20 | **3** | 3.026.640 |

Los 20 "primeros pagos" de junio son **artefacto de la migración** de alumnos, no
altas reales. En julio hubo **3 primeros pagos** contra **232 conversaciones** de Meta
y US$510 de gasto. Eso da ~1,3% de conversión y un costo de adquisición de ~US$170 por
alumno — **pero el número no está verificado**: falta saber cuántas de esas
conversaciones eran de Curso de DJ, y `is_first` no distingue migrado de nuevo.

**Hasta que ese número esté medido, cualquier decisión de escalar presupuesto es a
ciegas.** Optimizar US$0,89 por conversación no sirve si la conversación no se convierte.
Ver [[reconciliacion-pagos-sistema]] y [[astronomy-finance-report]].

## Decisiones de Facu del 30/07/2026

- **El video de Modo Profesional manda a la web, no a WhatsApp**: al landing
  `astronomyofficial.com/curso-profesional-dj`. El archivo es
  `~/Downloads/CursoProf2.mp4` — 1080×1920 (vertical 9:16), 39,6 s, H.264.
- **Producción online se vende en toda la provincia de Buenos Aires para empezar**, y
  se evalúa todo el país después. **Mateo Guini queda disponible como profe de
  producción online si Valen Frando se saturea** — hasta hoy la memoria decía que
  Valen era el único (ver el CLAUDE.md global).
- **Pendiente averiguado a medias: pagar Meta en pesos.** Hoy la cuenta es **USD** con
  **VISA \*9478** (verificado por API: `currency: USD`, `business_country_code: AR`,
  `funding_source_details.type: 1`). Se paga en USD justamente por los impuestos.

## Bloqueante para mandar pauta a la web: no hay pixel

**El sitio no tiene ningún pixel de Meta ni analytics** — grepeado `fbq`,
`connect.facebook.net`, `gtag` en todo `app/`, `components/` y `lib/` de
`astronomy-members`: cero resultados. Consecuencias, las dos duras:

1. Meta **no puede optimizar por compra**: sin señal de conversión, un anuncio a la web
   optimiza clicks, que es la métrica que peor correlaciona con plata.
2. **No se puede atribuir**: no hay forma de saber qué anuncio trajo al que pagó.

Y hay un tema de estructura: el conjunto activo es `OUTCOME_ENGAGEMENT` con destino
`WHATSAPP`. **Un anuncio que manda a la web no entra ahí** — necesita campaña nueva con
objetivo de tráfico o de ventas. No es cambiarle el link al anuncio.

El landing ya tiene ancla `#precio` para poder linkear directo al bloque de pago.

---

## 45. `postgrest-tope-1000.md`

---
name: postgrest-tope-1000
description: La REST de Supabase corta en 1000 filas aunque pidas limit=100000 — un conteo sobre esa respuesta da un número mal y no avisa
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b8503d04-a79b-4350-b642-6dc953fcd9ab
  modified: 2026-08-01T10:40:36.552Z
---

**La API REST de Supabase (PostgREST) devuelve como mucho 1000 filas por respuesta, y
`?limit=100000` NO lo levanta.** Devuelve 200 y mil filas, sin error y sin señal de que
hay más.

**Why:** el 01/08/2026 conté cuántos eventos de cuentas internas había en
`studio_events` con un `select ... &limit=100000`, me llevé 1000 filas de las 2178
reales y le reporté a Facu **5 filas** cuando eran **19**. Él lo detectó mirando la
pantalla: se veían 6 suyas en un solo día. Un resultado corto que se reporta como dato
es exactamente el modo de falla que ya estaba anotado en el CLAUDE.md global.

**How to apply:** para CONTAR, nunca contar el largo del array. Pedir el conteo exacto
por cabecera, que es inmune al tope:

```python
H = {..., "Prefer": "count=exact"}
req = urllib.request.Request(f"{URL}/rest/v1/{tabla}?select={una_columna}",
                             headers={**H, "Range": "0-0"})
total = resp.headers["Content-Range"].split("/")[-1]   # "2178"
```

Para TRAER todo, paginar con `Range: desde-hasta` hasta que el lote venga corto (es lo
que hace `app/admin/eventos-estudio/page.tsx`, que ya paginaba de a 1000 — el código de
la app estaba bien; el mío de análisis, no).

Ojo con `select=id`: hay tablas sin esa columna (`sales`, `studio_events`) y el pedido
falla con 400. Usar una columna que exista.

Relacionado: [[cada-numero-con-su-negocio]], [[cuentas-internas-astronomy]].

---

## 46. `premios-reclamar.md`

---
name: premios-reclamar
description: "Los premios se RECLAMAN (créditos al abrir, no al otorgar), el arte sale de la rareza, y junio quedó bloqueado por código"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a510161-bc1d-481c-a0e4-40eb0e269423
  modified: 2026-07-30T05:33:18.100Z
---

Rediseño del 29/07/2026, sobre [[astronomy-premios]]. **En producción** (`8af0643`),
con `premios_v3_reclamar.sql` ya aplicado y verificado en Supabase.

> **La Management API de Supabase se corta con el User-Agent de urllib**: devuelve
> `403 error code: 1010`, que es el WAF de Cloudflare y parece un problema de permisos.
> Con `curl` (o mandando un UA normal) el mismo token anda. El endpoint que corre DDL es
> `POST /v1/projects/<ref>/database/query`.

## Lo que cambió

- **Sólo se ve lo ganado.** Se fue `ProgresoHitos` y los huecos de la tira. Decisión de
  Facu: que los premios que faltan sean un misterio.
- **El arte sale de UN número: la rareza (0 a 4)**, en `rarezaDe()`. De ahí salen fondo,
  aro, halo, rayos, facetas y tamaño. Antes las trece medallas eran el mismo dibujo con
  otro número grabado.
- **El premio se reclama.** `otorgarPremios` ya NO acredita; los créditos los cobra el
  alumno al abrir la medalla (`reclamarPremio`), con animación que dura más cuanto más
  raro es. La barrera contra cobrar dos veces es el `update ... is null` + `eq(user_id)`
  en un solo statement, no un chequeo previo.
- **Símil coleccionable sin cripto**: número de serie y código público por medalla. Facu
  descartó NFT de verdad ("total la gente no entiende").

## El triángulo del isotipo tiene que ir GRANDE

La estrella con el triángulo chico se lee como una estrella cualquiera. A 64px unos pocos
píxeles de calado no se ven. Va como subpath con `fill-rule: evenodd` —no como triángulo
pintado del color del fondo—, si no sobre fondo violeta se ve el parche.

## El isotipo NO se dibuja a ojo

Se probaron dos estrellas inventadas y las dos fallaron. El path bueno está **trazado del
alfa de `public/brand/isotipo.png`** (seguimiento de contorno + simplificación, 39 puntos)
y vive en `components/Medalla.tsx`. Dos cosas que a ojo nunca salen:

- **Mide 48,57 × 100**: es el doble de alto que de ancho. Dibujado casi cuadrado deja de
  ser el logo.
- **Le falta el lóbulo de abajo a la derecha**, y es parte de la estética de la marca.
  Después del brazo derecho el contorno vuelve al centro en vez de bajar. Simetrizarlo lo
  rompe.

El volumen es una **extrusión** (la misma silueta corrida en diagonal y oscurecida), no
partirlo al medio: el logo ya viene cortado y sumarle otro corte lo ensucia.

Al abrir un premio gira **el isotipo, no el disco**. Y van **dos `<g>` anidados**: el de
afuera ubica con el atributo `transform`, el de adentro gira por CSS. Juntos no —
`transform-box: fill-box` le cambia el punto de referencia también al transform de
posición y manda el isotipo a un costado del círculo.

**Sin cinta ni número grabado.** Había una chapita con "50" / "1°" / "8s": no se entendía
qué era y le comía el centro al isotipo. El dato lo dice el título de al lado.

## Ya no queda nada que apretar (30/07/2026)

Se rediseñó de nuevo: los **objetivos** (hitos y rachas) se entregan solos apenas se
cumplen, y el **podio** se publica solo el día 1. Nadie tiene que otorgar nada. Julio ya
entregó sus 46 objetivos (320 cr, 23 alumnos) y el podio sale el 1/8. Detalle completo en
[[retomar-medalla]].

La tira del alumno tampoco dice ya cuántas medallas hay en total: sólo "N medallas".

## Junio: la protección era el deploy, y se cayó sola

`/admin/premios` sin `?periodo=` abría **junio** —un mes que no se premia, $104.720— con
el botón de otorgar al lado. Lo único que lo frenaba era que la pantalla no estuviera
deployada… y el 29/07, al quedar el repo conectado a Vercel, cualquier push la deployó.

Ahora existe `PRIMER_PERIODO = "2026-07"` en `lib/premios.ts`, y lo chequea **también la
acción** que otorga, no sólo el default de la pantalla: un `?periodo=2026-06` escrito a
mano llega igual al form.

**Why:** una decisión de plata no puede depender de que un deploy no haya salido.

**How to apply:** cuando algo esté "protegido porque no está deployado", eso no es una
protección — es una carrera contra el próximo push. Ponerlo en código.

Relacionado: [[astronomy-premios]], [[astronomy-brand]], [[app-color-direction]],
[[vercel-deploy-astronomy]].

---

## 47. `public-site-vision.md`

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

---

## 48. `reconciliacion-pagos-sistema.md`

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

---

## 49. `regla-20-filas.md`

---
name: regla-20-filas
description: "REGLA DE LA CASA — toda lista de más de 20 filas arma su scroll sola; cómo está implementada y por qué no hace falta contar filas"
metadata:
  type: feedback
---

**Facu, 31/07/2026:** *"todo lo que se pase de más de 20 renglones tiene que tener el
scroll down funcionando sí o sí, y en todas las bases de datos aplicar esa regla; una vez
que se pasa de 20 renglones que se active el scroll de manera automática también."*
(Ya lo había dicho el 27/07 — ver [[estetica-simetrica-siempre]].)

**Why:** una lista de 200 filas estira la página al infinito y para encontrar algo hay que
leerla entera. Y si la regla es opt-in, no se cumple: `DataTable` la implementaba desde el
27/07 y sólo la usaban 5 pantallas de diecinueve.

**How to apply — no se cuentan filas.** `max-height` **no recorta nada hasta que el
contenido lo supera**, así que el tope va SIEMPRE en el contenedor y la regla se activa
sola. Una tabla de 3 filas queda idéntica (verificado: mismo alto, sin barra); una de 200
arma su scroll.

En `astronomy-members`:

| Clase | Para qué |
|---|---|
| `.tbl-wrap` | Contenedor completo (borde, fondo, radio) + tope de 62vh. `.corta` baja a 44vh, `.sin-tope` lo saca. |
| `.scroll-20` | Sólo scroll + encabezado fijo. Para las tablas escritas a mano: no toca bordes ni tipografía, así que se agrega sin cambiar cómo se ve la pantalla. |
| `DataTable` | Además buscador, filtros por columna y tarjetas abajo de 720px. |

Tres cosas que no son obvias:

- **62vh, no 100%.** Tiene que verse que la lista sigue abajo del borde; con la altura
  completa el corte queda fuera de pantalla y parece que ahí terminó.
- **El encabezado fijo necesita fondo opaco** (`--space-2`, que cambia con el tema). Sin
  él las filas se ven pasar por detrás del título justo cuando la regla empieza a servir.
- **`data-lenis-prevent` en cada contenedor.** Lenis se queda con la rueda: sin eso la
  lista tiene barra y no se mueve. Es el error que hace parecer que "el scroll no anda".

Tamaños reales que justifican todo esto (medidos el 31/07): `payment_links` 613 filas ·
`credit_transactions` 246 · `slot_bookings` 190 · `profiles` 57 · `subscriptions` 54 ·
`premios` 49 · `bookings` 37 · `cancellations` 27.

---

## 50. `regla-creditos.md`

---
name: regla-creditos
description: "REGLA CENTRAL — las membresías acumulan créditos, el Curso de DJ los renueva (no acumula)"
metadata: 
  node_type: memory
  type: project
  originSessionId: c2d2783b-f7d8-4f9b-9336-c669948a8c9e
  modified: 2026-07-28T02:34:14.341Z
---

**Vencimiento: 2 meses desde el ÚLTIMO PAGO** (confirmado por Facu el 27/07/2026). El reloj
no corre por lote acreditado sino desde el último pago, así que al alumno que sigue pagando
no se le vence nada nunca. Si deja de pagar, tiene 2 meses para usar lo que le quedó.
Cualquier doc que diga "3 meses" está desactualizada.

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

---

## 51. `reglas-clases-sueldo.md`

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

---

## 52. `retomar-eje.md`

---
name: retomar-eje
description: "PALABRA CLAVE «eje» — cierre del 31/07 al 1/08/2026: calendario público, logo 3D girando, performance, regla de las 20 filas y las rachas nuevas en producción"
metadata: 
  node_type: memory
  type: project
  originSessionId: 781a50f0-fe21-4567-8aa2-246290fda571
  modified: 2026-07-31T23:43:37.967Z
---

**Si Facu dice «eje», empezá acá.** Sesión larga del 31/07 al 1/08/2026, sobre
`astronomy-members`. **Todo lo de abajo está en producción y verificado.**

## ▶ Lo primero al retomar

1. **Google todavía muestra el globito genérico** en los resultados. Facu lo dejó para esta
   sesión: *"lo de google no sé qué hacer, sigue sin funcionar"*. Ver abajo por qué **no es
   un problema de código** y qué es lo único que falta.
2. **`/admin/eventos-estudio` conviene mirarlo con José**: se arregló dos veces esta noche
   y es su pantalla.
3. El **instructivo de premios** sigue vigente:
   https://claude.ai/code/artifact/abcb9bea-cab2-4014-be60-f9f9abfd2a71

## Google: ya tiene el favicon, falta que refresque el buscador

`google.com/s2/favicons?domain=astronomyofficial.com` **devuelve el isotipo negro**: Google
ya rastreó el ícono nuevo. Lo que se ve en los resultados es el caché del SERP, que se
refresca aparte y más lento.

Todo lo verificable está bien: robots.txt permite los íconos, `/favicon.ico` y `/icon.svg`
dan 200 a Googlebot, la home tiene los cuatro `<link rel="icon">`, y el `.ico` pasó a
48/96/144/192 (múltiplos de 48, como pide Google — declaraba 256).

**Lo único que queda es que Facu entre a Search Console → Inspección de URL → pegue
`https://astronomyofficial.com/` → "Solicitar indexación".** No lo puedo hacer yo: las
credenciales de Google del OS no tienen el scope de Search Console, y agregarlo **invalida
los tokens** que usan `triage-inbox` y `cierre-mes` (ver [[astronomy-brand]]).

## Lo que se hizo, todo en producción

| | |
|---|---|
| **`/horarios`** | Calendario público para mandarle a un lead. Ver [[calendario-publico-horarios]] |
| **Favicon adaptativo** | SVG sin fondo, negro sobre claro / blanco sobre oscuro. Ver [[astronomy-brand]] |
| **Logo 3D en las medallas** | El render real de Facu, girando. Ver [[astronomy-premios]] |
| **Performance** | Imágenes de 4.561 → 2.010 KB (−55%), lazy loading, dos fugas tapadas |
| **Regla de las 20 filas** | Aplicada en las 14 pantallas que faltaban. Ver [[regla-20-filas]] |
| **Rachas + objetivo mensual** | Reglas nuevas, 5 cr. Ver [[retomar-podio]] |
| **Podio 20/10/5/5/0** | Números redondos; el mes sigue costando 40 cr |

### El giro del logo: tres bugs encadenados, y los tres son transferibles

Costó tres iteraciones y cada una enseñó algo (detalle en [[astronomy-premios]]):

1. **`steps(N)` sin `jump-none`** → el logo se desliza de lado como un carrusel. Los pasos
   caen SIEMPRE entre dos cuadros.
2. **Tira de 8640 px** → en el celular **no se ve nada**. Muchos GPU de teléfono no
   decodifican texturas de más de 4096 px y la máscara falla sin error en consola. Va en
   grilla 8×6 (1440×1080).
3. **`mask-position-x/-y` no se anima en iOS** → se veía pero quedaba clavado. Ahora se
   anima `transform`… y ojo: **dos animaciones sobre `transform` se pisan** (no se suman),
   así que son tres capas — el padre recorta, una capa se mueve en Y y otra en X.

> **How to apply:** un sprite CSS se prueba en un teléfono REAL. Chrome emulando móvil usa
> la GPU de la Mac y no reproduce ninguno de estos tres.

### `/admin/eventos-estudio` — dos arreglos seguidos

- Leía **una sola fuente** (`studio_events` = Calendly) y la última clase concretada era el
  17/07/26: Calendly se reemplazó entre el 13 y el 17/07 y todo lo real vive en
  `slot_bookings`. Ahora lee las dos y deduplica por (mail, instante).
- Y después **contaba el futuro como concretado**: entraban las clases agendadas hasta
  agosto con el tilde verde. Ahora sólo `starts_at <= ahora`.

## Dos errores míos de esta sesión, para no repetirlos

- **Le dije a Facu que el cambio de rachas estaba sin pushear y ya estaba deployado.**
  Lo había commiteado antes y `git push` manda la rama entera. **Si algo se frena por ser
  plata, no alcanza con no pushearlo en ese momento: hay que no commitearlo, o avisar que
  el próximo push lo arrastra.**
- **Pusheé un build roto.** Encadené `npm run build | grep ... && git commit` y el grep
  devolvió 0 al encontrar la palabra "error", así que la cadena siguió. **El build se
  verifica mirando el resultado, no encadenando un grep.**

## Lo que quedó anotado y no se hizo

- **0 de 49 medallas reclamadas.** Si sigue en cero la semana del 4/8, el aviso no funciona.
- **El fin de semana del estudio**: Pastrana tiene disponibilidad cargada sábado y domingo
  pero `studio_hours` abre lunes a viernes, así que esos turnos no existen. Facu decidió
  que manda el horario del estudio; quedan 16 horas de cabina por finde sin ofrecer.
- **Los alquileres en `/reservar` no aplican la anticipación de 12 hs** (sí `/horarios`).

Relacionado: [[retomar-podio]], [[calendario-publico-horarios]], [[regla-20-filas]],
[[astronomy-premios]], [[donde-aparece-un-pago]], [[vercel-deploy-astronomy]].

---

## 53. `retomar-medalla.md`

---
name: retomar-medalla
description: "PALABRA CLAVE «medalla» — qué quedó abierto de la sesión del 29/07/2026: premios, DJ Delivery, Luki y la mudanza del repo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a510161-bc1d-481c-a0e4-40eb0e269423
  modified: 2026-07-30T05:33:10.378Z
---

**Si Facu dice «medalla», empezá acá.** Cierre de la sesión del 29/07/2026.

## Lo que quedó EN PRODUCCIÓN esa sesión

Cinco deploys, todos `Ready` y verificados:

1. **DJ Delivery entra al libro** — cobraba solo por MP desde 2024 y la app tiraba el
   cobro antes de `sales`. Ver [[djdelivery-facturacion]].
2. **Premios se reclaman**, arte por rareza, isotipo real trazado del PNG, sin cinta.
   Ver [[premios-reclamar]].
3. **`PRIMER_PERIODO = "2026-07"`** — junio ya no se puede otorgar ni forzando la URL.
4. **Carga manual** ya no cuenta dos veces una cuota de suscripción.
5. **Las cuentas de prueba no compiten** por premios (ni las borradas de `auth.users`,
   cuyas reservas seguían corriendo el podio).

## Lo primero cuando vuelvas, por orden de plata

1. **Paseo Nordelta**: La Jaula da de alta en agosto, $2M/mes. Es la próxima de la rampa.

> **Julio de premios ya no requiere que hagas nada.** El 30/07 se rediseñó el sistema: los
> objetivos se entregan solos y el podio se publica solo el 1/8. Ver abajo.

## Cerrado el 30/07/2026

- **Tomás Papazián se dio de baja.** No se toca. Los $16.499/mes no vuelven.
- **Suscripciones sin fecha de próximo cobro: eran 2 (Felipe Floria en `bronze` y annie), y
  Facu las dio de baja el 30/07.** Hecho y verificado: las dos en `status = cancelled`, con
  fila en `cancellations`, y **los créditos intactos** (annie 240 hasta el 17/10; Floria ya
  tenía 0 desde la reconciliación del 21/07). Ninguna tenía preapproval real en MP, así que
  no hubo nada que cancelar allá. Quedan **24 authorized, todas con fecha**.
  **Inchausty no tiene suscripción**: transfirió 8 clases de una. No había plata perdida acá.
- **Los pagos sin dueño ya no se persiguen.** Son 28 (no 51): abril 1 · mayo 15 · junio 12,
  $4.210.440 — **todos anteriores a la web**. Regla nueva de Facu en
  [[atribucion-pagos-corte-web]]. Desde el 17/07 no cayó ninguno nuevo: la atribución
  automática anda.
- **Pauta: no fijar presupuesto mensual**, varía mes a mes. Ver [[meta-ads-astronomy]].
- **El doble conteo de clases era real y está arreglado** (ver abajo).

## El bug de `rescheduled`: confirmado, medido y arreglado

Estaba anotado como sospecha; el 30/07 se verificó contra la base y **eran dos bugs**, que
juntos inflaban julio en **8 clases sobre 151**:

1. `status = "rescheduled"` en `bookings` es la fila **vieja** de una clase que se movió.
   En `slot_bookings` reprogramar es un `update` de `starts_at` sobre la misma fila, así que
   la clase real ya estaba contada — la vieja entraba de nuevo, y con el horario viejo.
2. La migración de Calendly (13–17/07/2026) copió clases a `slot_bookings` **sin borrar el
   original**: 5 clases vivían enteras en las dos tablas.

Fix en `lib/premiosData.ts` (`clasesTomadas`): descarta `rescheduled` y dedupea por
`user_id` + instante exacto, ganando `slot_bookings`. Efecto: no cambia el costo total
($234.080 igual), **cambia el podio** — se dan vuelta el 4° y el 5° puesto (Guadalupe M.
pasa a 4°, Felipe B. a 5°).

**How to apply:** las dos tablas de reservas se solapan. Contar clases sumando
`bookings` + `slot_bookings` sin deduplicar por (alumno, instante) da de más, igual que
contar sin mirar `status`.

## Los premios se entregan solos (rediseño del 30/07, EN PRODUCCIÓN)

Idea de Facu: *"los premios son más objetivos que premios"*. Se partió en dos, porque eran
dos cosas distintas metidas en un mismo botón de "cerrar el mes":

| | Qué es | Cuándo se entrega |
|---|---|---|
| **Objetivos** (hitos + rachas) | Metas individuales, no compiten con nadie | **Solos, apenas se cumplen**, desde el cron horario |
| **Podio** (5 puestos) | Lo único que se compite | **Solo el día 1**, con el mes cerrado |

Eran **47 de 52 premios (89% de los créditos)** cumplidos hacía semanas, esperando un botón.

**Ya entregado y verificado en producción el 30/07:** 46 objetivos · 320 créditos · 23
alumnos avisados (un aviso por alumno, no uno por premio) · 0 podios, que es lo correcto
porque julio no había terminado. Segunda corrida devolvió 0: es idempotente.

**Lo que falta sale solo:** el hito de 10 clases de Guadalupe cuando tome la clase del 31,
y el podio de julio el 1/8 (40 cr). Total del mes: 380 cr / $234.080, igual a lo medido.

**Empates:** comparten puesto y créditos, y se muestran los dos. Antes el orden entre dos
alumnos con las mismas clases **lo decidía el UUID** (`localeCompare` sobre el id): 3
créditos para uno y 2 para el otro por azar. Los puestos tapados se saltean (1, 2, 2, 4) y
el podio puede tener más de cinco personas — el tope son cinco PUESTOS.

Código: `lib/premiosOtorgar.ts` (motor), `calcularObjetivos` / `calcularPodio` /
`motivoParaNoPublicar` en `lib/premios.ts`, enganchado al cron `sync-sheet`.

**El alumno no sabe cuántas medallas hay.** La tira decía "5 medallas de 13"; ahora dice
"5 medallas". Se borró `TOTAL_MEDALLAS` para que el número no quede a mano de nadie. Es la
misma decisión que sacó los huecos de la tira: que la que falta sea una sorpresa.

## Una cosa que dejé anotada y no toqué

- **El instructivo de Luki** está en `astronomy-members/INSTRUCTIVO_LUKI.md`, listo para
  mandarle. El corte es: deja de cargar los cobros de Mercado Pago **y DJ Delivery**;
  sigue cargando efectivo/transferencia, clases de prueba y todos los egresos.

## OJO: el repo se movió

`astronomy-members` pasó a **`~/Desktop/Productoras/Astronomy/Academia/astronomy-members`**
(antes colgaba de `Astronomy/` directo). Facu reorganizó el Desktop el 29/07 y también
apareció `Astronomy/Marca Astronomy/`. **Quedan scripts y notas apuntando al path viejo**
— revisar antes de correr nada por path absoluto.

## Un error mío, para que no se repita

Reporté que la cuenta de prueba de Facu iba a salir segunda en el podio de julio. **Falso:**
conté las reservas sin filtrar por estado y 11 de 15 estaban canceladas. El código real
siempre filtró las canceladas.

**How to apply:** en cualquier tabla de reservas de esta app, `status` no es opcional —
`bookings` y `slot_bookings` guardan canceladas, reprogramadas y activas en la misma tabla,
con las dos grafías (`canceled` y `cancelled`). Contar filas sin mirar el estado da de más.

Relacionado: [[premios-reclamar]], [[djdelivery-facturacion]],
[[finanzas-unificacion-sheets]], [[roles-jose-luki]].

---

## 54. `retomar-pauta.md`

---
name: retomar-pauta
description: "PALABRA CLAVE «pauta» — cierre 30-31/07/2026: landing y pixel en producción, tres productos corriendo con la misma plata en Meta, y el margen real de los últimos 10 meses"
metadata: 
  node_type: memory
  type: project
  originSessionId: a66a4ae5-626e-4cf6-b596-f3c2c98c0e83
  modified: 2026-07-31T22:00:52.367Z
---

**Si Facu dice «pauta», empezá por acá.** Palabra clave acordada el 30/07/2026, sesión
cerrada el 31/07. Es la continuación de [[retomar-showcase]].

## TECHO DE PAUTA: US$500/mes, SOLO META (Facu, 31/07/2026)

Instrucción nueva, **posterior** a la de "no pongamos un fijo" del 30/07 — ver
[[meta-ads-astronomy]]. Pasarse sólo con un número medido que lo justifique.

**El techo es sólo lo que se le paga a Meta.** Los ~US$150/mes de `Gestión de Pauta` van
aparte: es una persona que ayuda con la pauta, no el medio. Costo total de pauta ≈
US$650/mes. Textual de Facu: *"el techo de meta es 500 y los 150 son aparte para una
persona que nos está ayudando con la pauta"*. Detalle en
[[pauta-como-se-carga-el-egreso]].

**Gasto mensual real, leído de la API el 31/07/2026:**

| Mes | USD | | Mes | USD |
|---|---|---|---|---|
| ago-25 | 442,96 | | feb-26 | 249,45 |
| sep-25 | 600,10 | | mar-26 | 414,05 |
| oct-25 | 777,81 | | abr-26 | 514,59 |
| nov-25 | 510,88 | | may-26 | 490,18 |
| dic-25 | 253,84 | | jun-26 | **498,84** |
| ene-26 | 214,81 | | jul-26 | **528,60** ← sin cerrar el día |

Promedio 12 meses: **US$458**. El techo no es un recorte, es el ritmo actual.

**Ejecutado el 31/07:** los tres conjuntos bajaron de US$10 a **US$7/día** (US$21/día
total), verificado releyendo de Meta. A US$30/día agosto salía **US$930**.

**Plan de dos fases para que agosto cierre en 500:**

| Fase | Días | Qué corre | US$/día | Total |
|---|---|---|---|---|
| 1 — comparar | 1 al 14/08 | los tres productos, misma plata | 21 | 294 |
| 2 — concentrar | 15 al 31/08 | sólo el ganador | 12 | 206 |

~US$98 por producto en la fase 1 = 50-100 conversaciones cada uno, suficiente para
comparar. **Si nadie apaga nada el 15/08, agosto termina en US$651.** Quedó ofrecido un
chequeo diario que avise por dónde va el mes (recomendado sobre un `spend_cap` duro, que
cortaría la pauta a fin de mes y perdería ventas). **Facu no lo aprobó todavía.**

## Lo primero cuando vuelvas

1. **No leer los números de la pauta antes del lunes 3/08.** Los tres conjuntos entraron
   en aprendizaje el 30-31/07, y el 31/07 se les tocó el presupuesto.
2. **Cargar la pauta de junio y julio** — falta en los **dos** rubros (`Pauta Publicitaria`
   y `Gestión de Pauta`). Meta: junio **US$498,84**, julio **US$528,84 y subiendo** (el
   definitivo se lee el 1/08; el US$497,67 que tenía anotado era una lectura del 30/07 y
   quedó viejo). **Falta el tipo de cambio de esos meses y el monto de la gestión — no
   inventarlos.** El método de carga, medido y explicado, en
   [[pauta-como-se-carga-el-egreso]]: el monto sale de la API del 1 al 1, no del extracto
   del Bank of America, que cierra 15-al-15 y desfasa el margen hasta 49% en un mes. Sin
   esto junio queda con un 10,5% de margen que no es real: [[astronomy-margen-real]].
3. **A las 2-3 semanas, prender la campaña web de Modo Profesional** (`120248181489120448`)
   como cuarto brazo y **también a US$10/día**, para no romper la comparación. Facu la
   quiere prendida; se difirió para no darle el doble de plata a un producto.
4. **Leer el resultado cruzando los códigos de WhatsApp contra los pagos**, no el costo
   por conversación.

## Lo que quedó cerrado y verificado

**El landing de Modo Profesional está en producción** — commit `0de82e4`, pusheado y
confirmado contra `https://astronomyofficial.com/curso-profesional-dj` (aparece "Sumate",
dos `href="#precio"`, el `id="precio"`, y "Inversión" ya no está):

- La sección de precio se llama **"Sumate"**, no "Inversión". Facu dio como referencias
  unite / sumate / subite / arrancá YA / empezá hoy / quiero — "Sumate" salió de ahí y
  además es lo que dice el botón.
- **Dos botones que bajan directo al cobro**, uno en el hero y uno en el cierre, los dos
  al ancla **`#precio`** — que sirve también para que un anuncio linkee directo al pago:
  `astronomyofficial.com/curso-profesional-dj#precio`.
- El bloque de pago es el cierre visual: centrado, más grande, con el azul marino
  `#180040` detrás del número, qué incluye al lado del precio, y **$55.000 por clase**
  (440.000 ÷ 8). En 2 cuotas dice el **total $500.000**: financiado sale $60.000 más y se
  declara.
- Corregidos midiendo en el navegador: el resplandor tapaba el selector y deslavaba el
  botón activo; en móvil la bajada quedaba a la izquierda mientras el título se centraba.

**Se quitó una barra fija de móvil** que yo había agregado (precio + botón siempre a la
vista). No se pudo verificar en Chrome headless y se sacó antes de pushear en vez de
mandar a producción algo sin probar. **Si se quiere, se rehace y se prueba en un celular
de verdad** — el botón que Facu pidió no depende de eso y sí está verificado.

## El pixel ya está vivo (30/07/2026)

**Pixel `6508137999303373`** — el único de los cuatro del business que está **asignado a
la cuenta publicitaria**; los otros tres nunca dispararon y no sirven para optimizar ni
atribuir. En producción desde el commit `1f80cd8`.

**Verificado contra Meta, no contra el propio HTML:** el `last_fired_time` del pixel pasó
de `2025-07-20` a **`2026-07-30T17:45:31Z`**. Está recibiendo eventos.

Tres eventos: `PageView` (en el layout y en cada cambio de ruta, porque Next no recarga la
página al navegar), `InitiateCheckout` (al apretar el botón de pago de Modo Profesional) y
`Purchase` (cuando Mercado Pago devuelve a `/member?curso=ok`, con el monto en la URL).

**Trampa que costó tiempo: grepear el HTML NO sirve para verificar un pixel.**
`next/script` con `afterInteractive` no deja el snippet en el HTML servido, lo inyecta el
bundle después de hidratar. La prueba es mirar los pedidos del navegador o el
`last_fired_time` de la API. Quedó `pixel_check.py` en el scratchpad.

**Límite conocido de `Purchase`:** sólo cuenta al que vuelve al sitio. Si cierra la
pestaña de Mercado Pago, el pago entra igual por el webhook pero el evento no sale. La
fuente de verdad de la plata sigue siendo `sales`. **Cerrarlo del todo es mandar el evento
desde el webhook con la Conversions API** — es el paso siguiente.

## El anuncio del video está armado y EN PAUSA

Creado y verificado leyéndolo de vuelta de la API el 30/07. **Nada gasta hasta que Facu
confirme el presupuesto** — los US$5/día son mi recomendación, nunca confirmada.

| Qué | ID | Estado |
|---|---|---|
| Campaña `Modo Profesional \| web \| jul-26` (`OUTCOME_SALES`) | `120248181489120448` | **PAUSED** |
| Conjunto `MP web \| Nordelta 35km \| InitiatedCheckout` | `120248181491980448` | **PAUSED** · US$5/día |
| Anuncio `modo-profesional \| video \| 9x16 \| web \| v1 \| jul-26` | `120248181499500448` | en revisión |
| Video subido (39,6 s, 1080×1920) | `987433777631449` | listo |

- Optimiza **`OFFSITE_CONVERSIONS` → `INITIATED_CHECKOUT`**, no compras: el pixel está
  frío y con US$5/día una optimización por compra no sale nunca de aprendizaje. Se pasa a
  `PURCHASE` cuando haya volumen. **No se usó objetivo de tráfico a propósito**: optimizar
  clics es la métrica que peor correlaciona con plata.
- Público: **mismo que el que ya funciona**, 35 km alrededor de Nordelta, 18-65. El curso
  es presencial, la geo no se puede abrir.
- CTA → `https://astronomyofficial.com/curso-profesional-dj`.
- El archivo lo movió Facu a
  `~/Desktop/Productoras/Astronomy/Academia/Contenido/Pauta Online/CursoProf2.mp4`.
- **Ojo con la API**: `custom_event_type` es `INITIATED_CHECKOUT` (no `INITIATE_`), la
  campaña exige `is_adset_budget_sharing_enabled` si no usa presupuesto de campaña (va en
  **false**, o el conjunto comparte su plata y se pierde el sentido de aislarlo), y
  `degrees_of_freedom_spec.standard_enhancements` quedó **deprecado**.

## El hallazgo que cambió la estrategia: la geografía vale 5x

Buscando por qué `Curso DJ 2` fue el mejor anuncio con volumen de la cuenta, apareció un
**experimento natural que ya había corrido**: el mismo creativo, el mismo copy, dos
conjuntos a la vez.

| Conjunto | Geo | Gasto | Conv | US$/conv | Días |
|---|---|---|---|---|---|
| `Intereses 3 (Nuevo) - IG` | **PAÍS AR** | 80,72 | 120 | **0,67** | 12 |
| `Intereses 3 (Nuevo)` | **Nordelta** | 35,13 | 10 | **3,51** | 44 |

Y ese copy es **idéntico** al que corre hoy. **No hay un creativo mágico: hay una
geografía cara.**

**El mejor anuncio de la historia, `Astronomy 1`** (US$1,16/conv, 460 conversaciones,
**89 días sin decaer**), vendía **producción musical ONLINE a todo el país** — no el curso
de DJ. Su retención era malísima: **3,3% llegó al 25% y 0,6% lo vio completo**, peor que
los videos de hoy. **Ganó por producto y geografía, no por creativo.**

Los conjuntos locales se saturan: el histórico de Nordelta llegó a **frecuencia 2,92** y
el mismo anuncio pasó de US$0,76 (12 días) a US$3,51 (44 días). Los nacionales aguantaron
89 y 136 días. **En 35 km, un anuncio dura unas dos semanas.**

**El video proven sigue disponible en la cuenta: `3389915887829399`** (40 s, listo).

## Los tres conjuntos separados, CORRIENDO desde el 30/07/2026

**Facu dio el OK y están los tres prendidos desde el 30/07/2026, US$30/día en total.**

Facu pidió correr Curso de DJ y Modo Profesional en paralelo para ver cuál rinde. Se
sumó Membresía online, que es el único con techo geográfico alto. **Los tres a WhatsApp
a propósito**: si uno fuera a la web, la comparación mediría el destino y no el producto.

**Presupuesto igual para los tres, por pedido de Facu (30/07):** "si le metemos la misma
plata a todos, nos vamos a dar cuenta de qué es lo que más vende". Tiene razón — con
presupuestos distintos la comparación no dice nada.

| Conjunto | Producto | Geo | Presupuesto | IDs |
|---|---|---|---|---|
| `IntWpp1 PresCurso Nordelta Revinculado` | Curso de DJ | **20 km** Nordelta | US$10/día | `120245002157210448` |
| `MP \| Nordelta 20km \| wpp` | Modo Profesional | **20 km** Nordelta | US$10/día | conjunto `120248181844100448` · anuncio `120248181858940448` |
| `Membresia online \| Prov Bs As + CABA \| wpp` | Membresía | Provincia 97 + CABA 103 | US$10/día | conjunto `120248181844670448` · anuncio `120248181861420448` |

**El radio bajó de 35 a 20 km** porque Facu marcó que viajar más de 30 km a un curso
presencial no lo hace nadie. El número que lo decidió, del `reachestimate`:

| Radio | Público |
|---|---|
| 10 km | 1,1 M |
| 15 km | 2,2 M |
| **20 km** | **3,7 M** |
| 25 km | **7,4 M** ← se duplica |
| 35 km | 10,6 M |

Entre 20 y 25 km el público se duplica: ahí el radio se come CABA y el conurbano oeste.
A 35 km, **7 de cada 10 personas alcanzadas vivían a más de 20 km del estudio**. Por
debajo de 15 km el público es tan chico que se satura en semanas.

Alcance final: Curso de DJ y Modo Profesional **3,7-4,3 M cada uno** (idéntico, que es lo
que hace válida la comparación), Membresía **20,3-23,9 M**.

**El conjunto del Curso de DJ volvió a fase de aprendizaje** al cambiarle geo y
presupuesto de una sola vez (una sola perturbación en vez de dos). **Los primeros 3 a 5
días de sus números no se leen.**

**Se pausó el carrusel de Modo Profesional que vivía adentro del conjunto del Curso de
DJ**: contaminaba justo el producto que se está midiendo. Cada conjunto mide uno solo.

**Cómo se lee el resultado dentro de 2-3 semanas:** no gana el que trae la conversación
más barata, gana el que trae plata. Una venta de Modo Profesional (ARS 440.000) equivale
a tres del Curso de DJ (ARS 143.520). Si Modo Profesional trae conversaciones al triple
de precio pero convierte igual, empata; si convierte mejor, gana. **Cruzar los códigos
`[MP-VID]` y `[MEM-ONL]` de WhatsApp contra `sales`, no mirar el costo por conversación.**

**Sigue en pausa a propósito** la campaña web `Modo Profesional | web | jul-26`
(`120248181489120448`), esperando que el pixel junte datos.

Campaña nueva `Astronomy | productos separados | jul-26` (`120248181843670448`),
**`is_adset_budget_sharing_enabled: false`** — la campaña vieja `Interaccion` lo tiene en
**true**, así que colgar los conjuntos nuevos ahí habría dejado que Meta les moviera la
plata al ganador, que es justo el problema que se está tratando de resolver.

**Atribución por el mensaje que manda el lead** (el `ref` de WhatsApp es el texto
autocompletado, `page_welcome_message.autofill_message.content` — no hay query param que
sobreviva al salto a la app):

| Llega diciendo | Es de |
|---|---|
| `[MP-VID]` | Modo Profesional |
| `[MEM-ONL]` | Membresía online |
| "Hola! Quiero más info de las clases presenciales." | los 3 anuncios viejos de Curso de DJ |
| texto libre, sin nada | `2IntW2 Curso de DJ`, el ganador actual |

**Al ganador NO se le tocó el creativo a propósito**: cambiarlo le resetea la fase de
aprendizaje y hoy trae a US$0,89. Se distingue por descarte.

## Formatos que pidió el equipo (30/07/2026)

Regla que le pasaron a Facu, **vale para toda publicación**:

| Ubicación | Relación |
|---|---|
| Feed, si es carrusel | **5:5** (cuadrado) |
| Feed, si no | **4:5** |
| Story | **9:16** |

`CursoProf2.mp4` es **9:16**, así que nace para Story/Reels. **Para feed falta una versión
4:5** y en esta Mac **no hay ffmpeg**, así que no se pudo generar. Afecta también al skill
`flyers` ([[flyers-academy-generador]]), que hoy produce feed, story y cuadrado.

## El objetivo que puso Facu (30/07/2026)

**Facturar ARS 5.000.000 o más por mes, y subir el % de ganancia mes a mes.** Textual:
si factura 3M con 2% de ganancia y después 5M con 10% aunque el costo sea mayor, mejor —
**lo que importa es más ganancia, y que el % suba.**

Julio 2026, medido contra Supabase el 30/07:

| | |
|---|---|
| Facturado | **ARS 3.026.640** en 20 pagos |
| Mezcla | Curso de DJ 14 pagos (ARS 2.009.280, **66%**) · Gold 3 (586.800) · Silver 3 (430.560) · **Platinum 0** |
| Comisión de Mercado Pago | **8% a 11%** del bruto donde está registrada |

Para llegar a 5M con el ticket actual hacen falta **~35 pagos por mes contra los 20 de
julio**. O mover la mezcla: hoy **el 100% del presupuesto de pauta apunta al Curso de DJ,
que es el producto más barato del catálogo**, y Platinum (ARS 272.000) no vendió nada.

## El % de ganancia SÍ se puede calcular — está en una planilla, no en Supabase

**CORREGIDO el 31/07/2026 por Facu.** Yo había concluido "no se registran costos" porque
`expenses` en Supabase tiene **0 filas** (igual que `staff_payments`; `salary_payments`
sólo 3). **Esa conclusión estaba mal.** Los egresos se cargan por un Google Form a la
planilla **`Finanzas - Astronomy Academy`, hoja `Base`** — 1.131 filas, de 2024-01 a
2026-07.

**El margen real, mes a mes, y por qué los últimos 10 meses dan −3,0%, en
[[astronomy-margen-real]].** Ahí está también qué falta cargar y cómo leer la planilla
sin equivocarse.

Lo único cierto de lo que había escrito antes: `mp_fee`/`mp_net` en `sales` están
cargados en **14 de 42 pagos**, así que dentro de Supabase el único número de facturación
confiable sigue siendo `amount`. Y la planilla y `sales` **no cierran entre sí**: julio da
ARS 2.920.287 contra 3.026.640, 3,5% de diferencia. Ver [[egresos-sistema]] y
[[astronomy-finance-report]].

## Producción online: decisión tomada

Se vende en **toda la provincia de Buenos Aires** para empezar, y se evalúa el país
después. **Mateo Guini queda como profe de producción online si Valen Frando se saturea**
— hasta ahora Valen figuraba como el único que daba online.

## Pagar Meta en pesos: falta el dato que decide

La cuenta es **USD** con **VISA \*9478** (verificado por API). Las fuentes que encontré
son blogs de agencias y estudios contables, **no Meta ni ARCA**: con tarjeta van 21% de
IVA más 30% de percepción (RG 5617/24), el Impuesto PAÍS se dejó de cobrar el 23/12/2024,
y existiría un pago local en pesos con solo el 21%.

**No hay recomendación posible sin saber si Vladimir Nadinic es monotributista o
responsable inscripto** ([[astronomy-quien-factura]]): el 30% es pago a cuenta y se
recupera solo si se puede computar. Es pregunta para el contador. Y ojo: **la moneda de
una cuenta publicitaria no se cambia** — habría que crear una nueva y perder los
US$7.111 de historia de aprendizaje de Meta.

## Herramienta que quedó en el scratchpad (efímera)

`shot.py` — captura un elemento de una página real por CDP con `websockets`. Sirve para
verificar diseño headless y **resuelve la trampa de los `vh`** (ver `LAB_NOTES.md`). Si se
va a usar de nuevo, conviene graduarlo a `execution/`; el scratchpad se borra.

**Aviso:** para desbloquear Chrome tuve que hacer `pkill -9` sobre todos sus procesos
(se habían acumulado 49). Si Facu tenía ventanas abiertas, se le cerraron.


## Estado al cerrar (31/07/2026)

**En producción:** landing de Modo Profesional (`0de82e4`) y pixel de Meta (`1f80cd8`),
los dos verificados contra la fuente real, no contra el HTML propio.

**Corriendo en Meta, US$30/día:** tres conjuntos con **US$10/día cada uno** — Curso de DJ
y Modo Profesional a 20 km de Nordelta, Membresía online a provincia + CABA. Los tres a
WhatsApp, cada uno con un código en el mensaje del lead.

**Cerrado en esta sesión:** Bronze **no se vende** (es sólo para conocidos, así que Silver
a ARS 143.520 es la puerta de entrada); se borró la fila de test de ARS 10 de las dos
hojas de la planilla de finanzas, con respaldo en
`~/facu-os/archive/respaldo-filas-borradas-finanzas.json`.

**Abierto, además de los 4 puntos de arriba:**

- **Versión 4:5 del video** para feed — el equipo pidió 5:5 carrusel / 4:5 feed / 9:16
  story, y `CursoProf2` es 9:16. **No hay ffmpeg en la Mac**, hay que instalarlo.
- **Conversions API** desde el webhook de Mercado Pago, para que `Purchase` no dependa de
  que el alumno vuelva al sitio.
- **Pagar Meta en pesos**: depende de si Vladimir es monotributista o responsable
  inscripto. Es pregunta para el contador.
- **Las 4 filas de prueba del 20/05 en `Responses`** (111.111 y 11.111 de Gestión de
  Pauta, y una venta "PRUEBA INACTIVE"). No están en `Base`, así que no ensucian ningún
  número. Facu no pidió borrarlas.

---

## 55. `retomar-podio.md`

---
name: retomar-podio
description: "PALABRA CLAVE «podio» — cierre del 30/07/2026 de madrugada: los premios se entregan solos, y lo único que queda pasa el 1/8 sin que nadie lo toque"
metadata: 
  node_type: memory
  type: project
  originSessionId: e442b324-11da-4e75-9d68-dabfd0f2cf2a
  modified: 2026-07-31T22:08:57.128Z
---

**Si Facu dice «podio», empezá acá.** Sesiones del 30 y 31/07/2026.

> **El instructivo YA SE ENTREGÓ** (31/07/2026):
> https://claude.ai/code/artifact/abcb9bea-cab2-4014-be60-f9f9abfd2a71 — reglas sacadas
> del código, estado medido y las tres decisiones abiertas. Nada del podio por tokens se
> toca hasta que Facu conteste las dos primeras.

## Lo que pasa solo, sin que nadie haga nada

| Cuándo | Qué |
|---|---|
| ~~31/07~~ | ✔ El hito de 10 clases de Guadalupe salió solo el 30/07 a las 21:00 |
| **1/08** | Se publica el **podio de julio**: 5 premios, 40 cr, $24.640 |

Al cierre del 31/07 la base tiene **47 premios · 340 créditos · 23 alumnos**, y el cron
sigue devolviendo 200 cada hora en punto. Con el podio de mañana, julio cierra en los
**380 cr / $234.080** medidos.

Después de eso julio cierra en **380 créditos = $234.080**, el número medido. **No hay
ningún botón que apretar.**

**El cron ya se verificó corriendo con el código nuevo** (30/07, 14:30). No alcanza con el
`succeeded` de pg_cron —eso sólo dice que encoló, ver [[cron-que-nunca-fallo]]—, así que se
miró `net._http_response`: 200 cada hora en punto, y el campo `premios` aparece en la
respuesta con `{"objetivos":{"otorgados":0},"podios":[]}`. Entrega 0 porque todavía no hay
nada nuevo, que es lo correcto. **La query que lo prueba:**

```sql
select created, content::json->>'premios' as premios from net._http_response
where content like '%stamp%' order by created desc limit 5
```

**Podio esperado, recalculado contra la base el 31/07** (después del fix de "la clase
premia cuando terminó"): 1° Segundo P. (17 clases, 20 cr) · 2° Fernando L. (9, 10 cr) ·
3° Juan M. (8, 5 cr) · 4° Guadalupe M. (6, 3 cr) · 5° Felipe B. (5, 2 cr) = **40 cr,
$24.640**.

> Eso asume que **Guadalupe toma su clase del 31/07 a las 21:00**. Si la cancela queda en
> 5 y **empata con Felipe en el 4°**: los dos cobran 3, el 5° se saltea, y el mes sale
> **41 cr ($25.256)**. La regla del empate hace que cancelar una clase salga más caro que
> tomarla — es correcto, pero conviene tenerlo visto.

## Lo que se hizo esa noche, todo en producción y verificado

1. **Doble conteo de clases, arreglado** (`2e52e47`). Julio contaba 151 clases donde hay
   143: `rescheduled` en `bookings` es la fila vieja de una clase movida, y la migración de
   Calendly dejó 5 clases duplicadas en las dos tablas.
2. **Los premios se entregan solos** (`7571487`). Objetivos al cumplirse, podio el día 1.
   Ya entregó: 46 objetivos · 320 cr · 23 alumnos avisados. Detalle en [[retomar-medalla]].
3. **La tira no dice el total** (`daaf28a`). Decía "5 medallas de 13"; ahora "5 medallas".
   Vista antes/después: https://claude.ai/code/artifact/84437372-2fa2-4475-83d0-dea58968ee5e
4. **Floria y annie**: membresías dadas de baja, créditos intactos (annie 240 hasta el
   17/10). Quedan 24 suscripciones activas, todas con fecha.
5. **Papazián se dio de baja** — cerrado, no se toca.
6. **Los pagos sin dueño no se persiguen más**: son 28, todos anteriores a la web. Regla
   nueva en [[atribucion-pagos-corte-web]].

## Las notificaciones de "Cobro vencido" NO las ve ningún alumno (verificado 30/07)

Facu preguntó al ver la campanita en la vista previa de alumno. Verificado por dos vías
independientes contra producción:

- **A quién se le mandaron**, consultando la base: sólo 4 cuentas — Facu (por
  `ADMIN_EMAILS`, no está en `staff`), **José**, **Luki** y **Vlado** (master). Ningún
  alumno, ningún profe.
- **RLS activo** en `notifications` (`relrowsecurity = true`) con la política
  `auth.uid() = user_id`: aunque se mandara mal, un alumno no puede leer las ajenas.

`notifyVencidos` (en `lib/payments.ts`) sólo elige staff con `is_master` o permiso
`view_payments`. **Los profes están en `staff` pero no tienen ese permiso**: Mateo Pastrana
tiene `manage_bookings`/`manage_studio`, y Mateo Guini y Valen tienen `permissions: []`.

> La campanita se ve en la vista previa de alumno porque **es la sesión de Facu**: la vista
> previa cambia el panel, no quién está logueado.

## La medalla abierta gira para siempre (30/07, en producción)

Pedido de Facu. Al terminar de abrirse el isotipo quedaba quieto y la ficha parecía una
captura. Ahora sigue girando mientras la ficha esté abierta — tanto al reclamarla como al
volver a mirar una vieja. `.pr-fase-listo .md-estrella` en `app/ui.css`, commit `60de112`.

La velocidad sale de la **rareza**, como el resto del arte: común 6s por vuelta, rara 4s,
legendaria 3s (`calc(12s / (--vueltas + 1))`).

**Verificado en Chrome con `getAnimations()`**, no a ojo: duración 6000/4000/3000 ms según
rareza, `iterations: Infinity`, `playState: running`. Con `--force-prefers-reduced-motion`
devuelve `SIN-ANIMACION`, o sea el bloque de movimiento reducido que ya cubría
`.md-estrella` la apaga sola.

## `/djcourse` daba 404 a quien venía de Google (arreglado 30/07)

Lo reportó **José**: buscando "astronomy academy" o "curso dj nordelta", Google muestra
**DJ Course** como sitelink y el link caía en un 404. Era la URL del sitio viejo de
Squarespace, en inglés; al migrar a esta app las rutas pasaron a español y nadie redirigió.
Era tráfico de gente a punto de comprar, cayendo en una pantalla de error.

**Arreglado** con `redirects()` en `next.config.ts` (commit `782f9a9`): `/djcourse` y
`/dj-course` → `/academy`, con `permanent: true` (308, que para Google vale como 301 y
traslada el posicionamiento; un 302 dejaría el ranking en la URL vieja para siempre).

Verificado en producción: `astronomyofficial.com/djcourse → 308 → /academy → 200`.

**Lo que Google tiene indexado hoy** (verificado por búsqueda, no adivinado): `/`,
`/academy` y `/djcourse`. Las dos primeras andaban bien. **Si aparecen más 404, están
listados en Search Console → "Páginas · 404"** — Facu tiene el acceso. No agregar redirects
inventados: probé 20 rutas candidatas del sitio viejo y todas dan 404, pero eso no prueba
que nadie las visite ni que Google las tenga.

## El isotipo tiene espesor real (30/07, `fee8ca0`)

Facu: *"así finito cuando gira queda feo"*. Tenía razón y era peor de lo que se veía: el
"volumen" del logo eran **tres copias del path corridas en diagonal**, que engañan de
frente pero no tienen canto. Girando, el logo se afinaba hasta una aguja y **a 90° exactos
desaparecía del todo** — el disco quedaba vacío.

Ahora son **24 láminas del mismo path separadas en Z** (`transform-style: preserve-3d` en
`.md-iso3d`, `perspective: 620px` en `.md-3d`), con el color interpolado lámina a lámina.

Tres cosas que costaron y no son obvias:

- **`preserve-3d` no se propaga a los hijos de un `<svg>`.** Las láminas tienen que ser
  HTML; adentro del SVG colapsan todas al mismo plano.
- **Sin `perspective` en el padre no hay 3D**: el giro vuelve a ser un aplastamiento, con
  láminas y todo.
- **Apilar planos no hace un sólido.** A 90° exactos todos tienen área cero y el logo se
  esfuma. Por eso existe `.md-canto`: una barra del ancho del espesor **girada 90° respecto
  de las láminas**, que está de perfil cuando ellas están de frente y aparece justo cuando
  ellas se desvanecen. Con 12 láminas además se contaban las rayas; con 24 no.

**Cuesta 24 SVG en vez de uno**, así que la prop `volumen` se pide SÓLO en la ficha del
premio abierto (`GaleriaPremios`, size 190), que es la única medalla que gira grande y sin
parar. En la tira y en las tarjetas de la galería sigue la versión plana, y se ve igual.

**El bloque es TODO BLANCO** (`8283ec5`). La primera versión oscurecía las láminas de atrás
para simular sombra y al girar el logo quedaba mitad blanco y mitad violeta: se leía como
dos piezas pegadas. Facu: *"si la parte de adelante es blanca, que la parte de atrás sea
blanca también"*. El volumen lo dice la silueta, no hace falta oscurecerlo.

## Una clase premia cuando TERMINÓ (fix del 31/07, `e6e656e`)

El corte era la FECHA: apenas cambiaba el día, todas las clases de esa jornada ya
premiaban. Mientras los premios los otorgaba una persona al cierre del mes era inofensivo
—para cuando apretaba el botón la clase ya había pasado—, pero **al entregarlos solos cada
hora el desfase se volvió real**: el 30/07 a las 21:00 salió el hito de diez clases de
Guadalupe, cuya décima clase era el 31 a las 21:00. Un premio pagado por una clase que
todavía podía cancelarse.

Ahora el corte es `starts_at + duration_min`. `bookings` no guarda duración (tabla vieja de
Calendly) y ahí se asume la hora de clase (`DURACION_POR_DEFECTO_MIN = 60`).

Verificado contra la base: 140 clases contadas contra las 143 de antes, y la clase de hoy
de Guadalupe deja de contar hasta que termine. **El hito ya otorgado no se revirtió**: la
clase iba a suceder igual.

**How to apply:** automatizar algo cambia qué defectos importan. Este bug existía hace
meses y era inocuo porque una persona lo tapaba con su timing; al sacar a la persona,
apareció. Cuando se automatice una tarea manual, revisar qué supuestos sostenía el humano
sin que nadie los hubiera escrito.

## El premio aparece al abrir el panel (31/07, `ca9fded`)

El cron horario entrega todo, pero entre que termina la clase y corre pueden pasar **59
minutos**: el alumno salía de su quinta clase, abría la app y no había nada. Ahora
`/member` llama a `entregarObjetivosDe(user.id)` **antes** de leer los premios, así nunca
puede entrar y no ver la medalla que se ganó.

Corre sólo para ese alumno (a los demás los sigue agarrando el cron, con su aviso), es
idempotente por la clave única, va en `try/catch` para que un problema de premios no deje
al alumno sin panel, y no corre en la vista previa de admin.

## ▶ El instructivo de reglas — ENTREGADO el 31/07/2026

Artifact: https://claude.ai/code/artifact/abcb9bea-cab2-4014-be60-f9f9abfd2a71
Reglas leídas de `lib/premios.ts`, `lib/premiosData.ts` y `lib/premiosOtorgar.ts`; números
medidos contra Supabase. Los datos duros:

| | |
|---|---|
| Hitos | 1 cl → 0 cr · 5 → 10 · 10 → 20 · 25 → 40 · 50 → 80 |
| Rachas | 4 semanas → 10 cr · 8 → 20 · 12 → 30 |
| Podio | 1° 20 cr · 2° 10 · 3° 5 · 4° 3 · 5° 2 |
| Crédito | $616 · los de premio **vencen a los 2 meses** de reclamarlos (`grant_credits` default `p_months = 2`) |
| Rareza | hito por escalón (50→legendaria); racha 12→épica; podio: el puesto ES la dificultad |

## ▶ LO PRIMERO: $184.800 esperando el OK de Facu (31/07, commit `47e0a19` SIN PUSHEAR)

Facu definió dos cambios y el código está escrito, con build limpio, **commiteado y sin
deployar a propósito**. En cuanto se pushee, el cron entrega todo de una.

1. **Las rachas dejan de ser semanas consecutivas** → clases dentro de una ventana de
   meses: **4 en 1 mes · 8 en 2 · 12 en 3**. Su caso: *"algunos hacen 2 clases en una
   semana, después 2 en la próxima, y esperan al mes siguiente porque tienen un viaje o
   exámenes"*. El nivel pasa de semanas a clases y los números coinciden (4/8/12), así que
   las 9 rachas ya otorgadas conservan su clave y **no se re-pagan** (verificado: 0 claves
   repetidas).
2. **Objetivo mensual repetible** — "Mes cumplido", 4 clases en el mes, **5 cr**, se gana
   de nuevo cada mes. Clave `mensual:<periodo>:<alumno>`. Va aparte de las medallas
   permanentes para no tener que revocar una ya reclamada, que no tiene salida limpia.

**Costo, simulado con el código real contra producción** (`scratchpad/simular-premios.ts`,
corre con `node --experimental-strip-types` e importa `lib/premios.ts` de verdad):

| | |
|---|---|
| De una sola vez al activarlo | **23 premios · 300 cr · $184.800** — arrastre de gente que ya califica |
| Recurrente | 9–10 alumnos/mes · ~48 cr · **$29.260/mes** |
| Costo total de premios | pasa del 3,1% al **~3,9%** de la facturación |

> Facu aprobó el mensual a 5 cr **cuando el número era $12.320–$15.400/mes**, medido con la
> regla vieja de semanas consecutivas (4–5 alumnos). Con la definición nueva son 9–10
> alumnos y el costo se duplica. **Eso todavía no lo vio.** La palanca es `MENSUAL.creditos`
> en `lib/premios.ts`: a 3 cr son $17.556/mes.

Los premios son plata **comprometida, no salida**: el crédito sale cuando el alumno abre la
medalla, y van 0 de 47.

## Las tres definiciones de Facu del 31/07, para no volver a confundirlas

1. **Los premios pagan CRÉDITOS.** Confirmado, ya es así.
2. **Las medallas son las de la tira**, abajo del nombre en el perfil. Ya es así.
3. **"Acumulables mes a mes, hasta que alguna no cumpla con su requisito"** — ESTO ES
   NUEVO Y NO ESTÁ DEFINIDO. Hoy una medalla ganada es **para siempre**. Facu parece querer
   que se pueda **perder** si el alumno deja de cumplir el requisito (¿la racha de 4
   semanas se pierde al faltar una?). **Preguntarlo explícitamente antes de tocar nada:**
   revocar una medalla ya reclamada implica además decidir qué pasa con los créditos que
   el alumno ya cobró.

## El podio por tokens: medido, y por qué frené

Facu quiere que el podio ordene por **cantidad de premios/tokens**, no por clases del mes.
Medido contra la base el 31/07, **el catálogo se agota y el podio se da vuelta**:

- Son **8 objetivos en toda la vida** (5 hitos + 3 rachas). No hay más.
- Segundo P. y Fernando L. ya tienen **5 de 8 en un solo mes**.
- Segundo hace 17 clases/mes: llega a 25 clases en agosto y a 50 en octubre. **Después no
  puede ganar una sola medalla más.**
- → El podio terminaría premiando al alumno NUEVO (que desbloquea "primera clase" y "cinco
  clases") y dejando afuera al que sostiene hace un año. Lo contrario de para qué existe.
- Además: en julio ya habría **2 empatados en el 1°** (Segundo y Fernando, 5 medallas), y
  como el podio otorga medallas hay que excluirlo del conteo o se retroalimenta.

**Mi recomendación, sin respuesta todavía:** agregar **objetivos mensuales repetibles**
("4 clases este mes", "8 este mes", "12 este mes") que se puedan ganar de nuevo cada mes.
Con eso el podio por tokens mide lo que Facu quiere y no se vacía; los 8 hitos de toda la
vida quedan como la colección rara. Los escalones y sus créditos **se proponen y se
confirman con Facu antes de tocar nada** — es plata.

## Lo que quedó anotado y NO se hizo

- **Nadie reclamó su medalla**: 0 de 47 al 31/07, con 23 alumnos avisados hace un día.
  Facu no lo ve como problema todavía. **Si sigue en cero la semana del 4/8, el aviso no
  funciona y hay que repensarlo.** Ojo: los 47 ya son reclamables hoy, no esperan a agosto.
- **La lista de 404 de Search Console**: la propiedad ya está verificada a nombre de Facu,
  pero el informe **no sale por API** (sólo Search Analytics, sitemaps e inspección de una
  URL por vez). Hay que exportarlo a mano: Search Console → Indexación · Páginas → "No
  encontrada (404)" → Exportar. Facu lo pospuso el 31/07: no es prioridad.
  · Automatizarlo requiere agregar el scope `webmasters.readonly`, y eso **invalida los
    tokens OAuth actuales** (se caen triage-inbox y cierre-mes hasta re-autorizar). Si se
    hace, va con credenciales aparte.

## Lo que sigue abierto

1. **Paseo Nordelta: La Jaula da de alta en agosto**, $2M/mes. Es la próxima de la rampa y
   es lo que más plata mueve de todo lo que quedó.
2. **Conjunto propio para Modo Profesional** en Meta — hoy no se mide porque comparte
   presupuesto. Ver [[pauta-carrusel-modo-profesional]]. Sin presupuesto fijo:
   [[meta-ads-astronomy]].
3. **El instructivo de Luki** (`astronomy-members/INSTRUCTIVO_LUKI.md`) sigue escrito y sin
   mandar. Ver [[roles-jose-luki]].
4. **Floria, detalle de $1**: figura a la vez en `cancellations` (22/07) y con Bronze
   asignado el mismo día. Preguntarle a Facu si fue a propósito.

## Trabajamos los dos sobre el mismo repo esa noche

Facu editaba `components/CursoProDJ.tsx` (la sección de precio de Modo Profesional) al
mismo tiempo que yo tocaba premios. Apareció como modificado en mi `git status` y lo dejé
afuera de mis commits; después él lo commiteó solo, en `0de82e4`. Todo pusheado.

**How to apply:** en `astronomy-members` el working tree puede tener cambios de Facu en
vivo. Nunca `git add -A` a ciegas — mirar qué archivos son y commitear sólo los propios.

## Un error mío, para que no se repita

Le dije a Facu que otorgar el podio antes de tiempo dejaría "dos 4° puestos y medallas
duplicadas". **Falso:** la clave del podio es `podio:mes:alumno`, **sin el puesto**,
justamente para impedir eso. El daño real era otro —el podio quedaba congelado al revés— y
seguía justificando frenar, pero afirmé un mecanismo sin haberlo leído.

**How to apply:** cuando el argumento para frenar algo es técnico, el mecanismo se lee, no
se deduce. En este repo eso significa abrir `claveDe` antes de hablar de duplicados.

Relacionado: [[retomar-medalla]], [[astronomy-premios]], [[premios-reclamar]].

---

## 56. `retomar-showcase.md`

---
name: retomar-showcase
description: "PALABRA CLAVE «showcase» — qué quedó abierto de la sesión del 29/07/2026: carrusel de Modo Profesional, pauta y carpetas de Astronomy"
metadata: 
  node_type: memory
  type: project
  originSessionId: a6298426-cff6-4848-ac49-0036e2e35bd6
  modified: 2026-07-30T05:08:24.618Z
---

**Si Facu dice «showcase», empezá por acá.** Es la palabra clave que acordamos el
29/07/2026 para retomar esta línea de trabajo.

## Lo que quedó cerrado ese día

- Carrusel nuevo de Modo Profesional **activo** en Meta con las placas rehechas —
  detalle en [[pauta-carrusel-modo-profesional]].
- Skill `flyers` arreglado de raíz: una foto por ángulo con chequeo que corta la
  corrida, gancho en la tarjeta de apertura, cero tarjetas negras. Ver
  [[flyers-academy-generador]].
- Carpetas de Astronomy reorganizadas en **Academia / Eventos / Marca Astronomy**,
  con las 9 referencias de path absoluto actualizadas y verificadas corriendo los
  scripts. Commits `dd37dcc` y `c8c8e61`, pusheados.
- Token de Meta ahora es de usuario del sistema: **no vence**.

## Lo que quedó abierto, en orden de plata

1. **Darle conjunto propio a Modo Profesional.** Es lo que más mueve: hoy comparte el
   único conjunto activo con el ganador de Curso de DJ, Meta le da el presupuesto al
   ganador, y por eso el carrusel lleva días con US$0,60 y cero conversaciones. **No
   fracasó — nunca se midió.** Detalle en [[pauta-carrusel-modo-profesional]].
2. **Los videos de Modo Profesional.** **El primer video YA ESTÁ**: `CursoProf2.mp4`
   (71 MB, 40 s, editado en Adobe, apareció el 30/07) quedó archivado en
   `Academia/Contenido/Pauta Online/`. Falta mirarlo y subirlo como creativo principal
   del producto; las placas quedan de banco de rotación. El video es el
   formato **más probado** de la cuenta (47,2% del gasto histórico a US$1,56/conv, y el
   mejor anuncio de la historia es uno) — ver [[pauta-inventario-y-publico]].
3. **Quién dicta Modo Profesional.** La tarjeta 4 del carrusel dice "te enseñan DJs
   que están tocando", genérico, porque no hay fuente. Las placas de `curso-dj` sí
   nombran a Pastrana y Guini. Con los nombres confirmados esa tarjeta convierte
   mejor.
4. **Los 190 GB de `Eventos/`.** Es el 98% de la carpeta Astronomy y el disco tiene
   164 GB libres de 926. No hay duplicados —se escanearon los 2.091 archivos por
   hash, apareció uno solo de 3,1 MB— y el 87% del peso es video, todo único. **La
   única palanca es sacarlo del disco**: recomendación de un SSD externo de 2 TB.
   `Eventos/Marcadas por Facu/` (las 158 etiquetadas por Facu, clones de APFS) es lo
   que conviene dejar en la Mac.
5. **`Astronomy/_duplicados-revisar/`** — archivos puestos ahí para que Facu los tire
   (eran 5; el 30/07 se sumaron 4 duplicados exactos que estaban en Downloads). No
   borrar por cuenta propia. Ojo: uno es el demo viejo de membresías, cuya única copia
   en disco quedó ahí ([[membership-system-project]]) — está obsoleto, así que si se va
   con la carpeta, está bien.

**Pausar `3IntW2` ya NO es prioridad** (era el punto 2 de esta lista): Meta lo
desfinanció solo, US$2,10 en 7 días. Pausarlo es prolijidad, ~US$0,30/día.

**Los dos PDFs de Nordelta Plaza salieron de Astronomy** (30/07): estaban en `Marca
Astronomy/Contratos y propuestas/` y se mudaron a `~/Desktop/Nordelta Plaza/`, que es su
negocio. Plaza se revisa con Facu en un futuro, no hoy.

## Sin commitear en el repo (de sesiones anteriores, no de esta)

`.gitignore`, `active/paseo-nordelta/ESTADO.md`, el plist de launchd y
`archive/base-clientes-antes-del-sync-2026-07-28/`. **Ese archive tiene la base de
clientes con datos personales de alumnos** — no meterlo en git sin preguntar.

---

## 57. `roles-jose-luki.md`

---
name: roles-jose-luki
description: "Qué hace José y qué hace Luki en Astronomy Academy, y por qué se perdieron cuando se automatizó todo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 771bfdd6-5e9e-442d-9c71-8efc80d0a473
  modified: 2026-07-28T22:40:48.088Z
---

Las dos personas que operan Astronomy Academy todos los días.

**José** (ella) — atención al cliente y que todo esté al día:
- Responde las dudas de los leads. **Hoy los leads hablan todos por WhatsApp.**
- Su problema recurrente: **los créditos no dan** — el alumno tiene menos créditos de
  los que pagó. Ella se fija si pagó y lo corrige a mano.
- Chequea que las clases estén agendadas.

**Luki** — el registro de la plata:
- Carga ingresos y egresos en un **Google Form** que cae en la planilla
  *Finanzas - Astronomy Academy* (ver [[finanzas-unificacion-sheets]]).
- **Está cargando a mano los pagos de Mercado Pago que la web ya registra sola.**
  Eso es lo que hay que cortar.

## Por qué se perdieron

Se automatizaron muchas cosas y **no quedó nada que dijera qué mirar**. Mientras el
trabajo se hacía a mano, el acto de hacerlo era el recordatorio; al automatizarlo
desapareció el acto y no lo reemplazó nada.

El panel `/admin` lista **26 pantallas como herramientas, no como tareas**:
`auditoria-creditos` pesa lo mismo que `estilo`. Nadie sabe cuál abrir para saber si
algo está roto.

## Lo que hay que construir (pedido de Facu, después de finanzas)

**Un panel por rol**, que no liste herramientas sino pendientes: *"3 pagos sin
atribuir · 2 alumnos con créditos que no cuadran"*, con tilde verde cuando no hay
nada. Que se abra del teléfono y en cinco segundos se sepa si hay algo roto.

- **Panel de José**: pagos sin atribuir (es la causa de que los créditos no den),
  créditos que no cuadran, clases sin agendar. Facu pidió **ver una vista previa
  antes** de que se construya.
- **Panel de Luki**: qué falta cargar, y las alarmas de pago duplicado / faltante.

**Hueco real: los leads de WhatsApp no tienen NADA en el sistema.** Es lo único que
hay que construir de cero, y va último porque depende de dónde estén hoy.

Los 12 permisos de `lib/staff.ts` están bien pensados y alcanzan: `view_students`,
`view_payments`, `add_credits`, `assign_payments`, `manage_calendar`, etc.

---

## 58. `sin-city-proyecto-musical.md`

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

---

## 59. `software-existente-respaldos.md`

---
name: software-existente-respaldos
description: Facu ya tiene software en producción por negocio (no construir lo que existe) + cómo están respaldados los repos
metadata: 
  node_type: memory
  type: project
  originSessionId: 33ec0f09-121b-4802-a441-1b27de7b7267
  modified: 2026-07-27T23:31:32.482Z
---

Facu **ya tiene software real construido** por negocio — antes de proponer construir
algo, mirar qué hay en la carpeta correspondiente:

| Negocio | Carpeta | Qué hay |
|---|---|---|
| Paseo Nordelta | `~/Desktop/Paseo Nordelta/` | PWA de finanzas ([[paseo-nordelta-app]]), web estática ([[paseo-nordelta-web]]), 2 tareas programadas |
| Astronomy Academy | `~/Desktop/Productoras/Astronomy/Academia/astronomy-members/` | Next.js 16 + Supabase + MP en producción (astronomyofficial.com) — [[membership-system-project]] |
| Astronomy Eventos | `~/Desktop/Productoras/Astronomy/Eventos/` | Negocio/ops, no código. La ticketera vive en el repo de Academy |
| Campos | `~/Desktop/Chaco/` | 650 PDFs de SENASA con patrón de nombre parseable |

**Respaldos** (GitHub `facue1900-byte`, auth por SSH `~/.ssh/id_ed25519`):
`astronomy-members` y `app-paseo-nordelta-` (**el guion final es parte del nombre**),
ambos privados, más `facu-os`. Bundles en iCloud:
`bash ~/Claude-Workspace/backup-repos.sh` (rota, conserva 5 por repo).

**Ojo con datos personales:** los CSV de `Historiales-Alumnos/` (datos de ~40
alumnos con email) se sacaron del historial de git y quedaron solo en disco,
gitignoreados. No volver a commitearlos.

**How to apply:** el `HANDOFF.md` de astronomy-members y el CLAUDE.md de cada
carpeta son la fuente de verdad de cada proyecto.

---

## 60. `vercel-deploy-astronomy.md`

---
name: vercel-deploy-astronomy
description: "astronomyofficial.com NO deploya por git push: el proyecto de Vercel no tiene repo conectado. Se deploya con `vercel --prod` a mano"
metadata: 
  node_type: memory
  type: project
  originSessionId: d8ac2c5b-e25e-493f-8410-743b29f9021f
  modified: 2026-07-29T11:06:50.974Z
---

**Desde el 29/07/2026 el push a `main` deploya solo.** El repo
`facue1900-byte/astronomy-members` quedó conectado al proyecto `astronomy`
(`prj_dap1DAp92rx2pWrs687Y43zMnSFO`, team `team_6UEQkSTshVWvbqxLal4yDYu1`), rama de
producción `main`. Verificado con un push de prueba: `BUILDING` en segundos, `READY` en ~60s.

Deploy manual, si hace falta saltear el push:

```bash
npx vercel --prod --yes --scope astronomyofficial
```

**Hasta el 29/07 el proyecto tenía `link: null` y pushear no deployaba nada.** Lo que lo
tapaba: en el dashboard los deploys del CLI figuran con hash de commit y rama `main`, idénticos
a un deploy por push — el CLI adjunta los metadatos del git local. Para distinguirlos está
`meta.githubDeployment` en la API: `1` = salió de un push, ausente = salió del CLI.

**Cómo se verifica que un deploy está vivo** (preguntándole a Vercel a qué deployment
resuelve el dominio, no adivinando desde afuera):

```bash
curl -s -H "Authorization: Bearer $T" \
  "https://api.vercel.com/v13/deployments/astronomyofficial.com?teamId=$TID" \
  | jq '.url, .meta.githubCommitSha'
```

**Nunca verificar con un nombre de chunk de `.next/static/chunks/`**: Turbopack no los genera
determinísticamente. El mismo código recompilado cambia el nombre solo. Ver la Lab Note del
29/07/2026 en `~/facu-os/LAB_NOTES.md`.

**Las cuentas, que se confunden:** Vercel es `facue1900-9658` / **facue1900@gmail.com** (no
studio@), y GitHub es **`facue1900-byte`** — comprobable con `ssh -T git@github.com`. Para
linkear el repo hizo falta primero una **Login Connection con GitHub** en la cuenta de Vercel
(https://vercel.com/account/login-connections); sin eso la API responde
`You need to add a Login Connection to your GitHub account first`. Ya está hecha.

El `VERCEL_TOKEN` del `.env` de facu-os **está bloqueado por SAML** para el scope
`astronomyofficial`. El que sirve es el del CLI, en
`~/Library/Application Support/com.vercel.cli/auth.json` (o `~/.local/share/com.vercel.cli/`),
que se renueva con `npx vercel login`.

Relacionado: [[software-existente-respaldos]], [[membership-system-project]],
[[finanzas-unificacion-sheets]].

---

## 61. `verificar-en-mac.md`

---
name: verificar-en-mac
description: "Trampas al verificar cosas desde esta Mac: `timeout` no existe, y astronomyofficial.com le contesta 403 a los scripts"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e442b324-11da-4e75-9d68-dabfd0f2cf2a
  modified: 2026-07-30T17:46:27.365Z
---

Dos cosas que hacen que una verificación **parezca fallar cuando en realidad no corrió**,
las dos encontradas el 30/07/2026.

## `timeout` no existe en macOS

`timeout 90 comando` devuelve `exit 127: command not found`. En un pipe eso da salida
vacía, que se lee como "el comando no encontró nada" en vez de "el comando no existe".
Costó tres intentos fallidos creyendo que Chrome no renderizaba.

**Qué usar:** el parámetro `timeout` de la herramienta Bash, que ya existe. Si hace falta
en el shell, `gtimeout` (coreutils) — pero casi nunca hace falta.

## `curl` a astronomyofficial.com devuelve 403

El dominio contesta **"Vercel Security Checkpoint"** a curl y también a Chrome headless.
**No es el sitio caído ni una config rota:** es la mitigación automática de Vercel
reaccionando a requests automatizados repetidos. Verificado el 30/07: no hay Attack
Challenge Mode activado, `ssoProtection: null`, y las URLs de deploy directas
(`astronomy-<hash>-astronomyofficial.vercel.app`, `astronomy-eight.vercel.app`) devuelven
**200 con el mismo contenido**.

**Qué hacer:** para verificar que algo llegó a producción, pegarle a la **URL del deploy**,
no al dominio. Ejemplo, confirmar que una regla CSS salió:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0.0.0"
u="https://astronomy-<hash>-astronomyofficial.vercel.app"
curl -s -A "$UA" "$u" -o /tmp/d.html
css=$(grep -oE '_next/static/[^"]+\.css' /tmp/d.html | sort -u | head -1)
curl -s -A "$UA" "$u/$css" | grep -o "mi-regla{[^}]*}"
```

**Ojo:** un 403 del dominio **no** es evidencia de que el sitio esté caído para los
alumnos. Antes de alarmar a Facu, probar la URL de deploy.

Relacionado: [[vercel-deploy-astronomy]], [[flyers-academy-generador]].

