# Astronomy OS — auditoría, propuesta técnica y plan

`06/08/2026` · Todo lo que sigue está **medido contra el código y contra la base**, no
estimado. Cada número dice de dónde sale.

Proyecto Supabase auditado: `qeakrjnseboiulcojlcw` (Astronomy Oficial).
Repo: `~/Desktop/Productoras/Astronomy/Academia/astronomy-members`, rama `main`.

---

## Veredicto, arriba de todo

**Astronomy OS no hay que construirlo: ya existe, y el problema no es que le falten
módulos — es que casi nadie lo abre.**

Las cinco fases que pediste están construidas en promedio a más de la mitad. La Fase 1
completa —usuarios, roles, permisos, dashboards personalizados por persona— está en
producción desde el 17/07/2026. El CRM de leads existe con seis estados y un timeline que
junta ocho fuentes.

Y al mismo tiempo, medido hoy contra `audit_log` de los últimos 30 días:

| Persona | Acciones en el sistema, últimos 30 días |
|---|---|
| Facu | 161 |
| José | 54 |
| Mateo Pastrana (profe) | 10 |
| **Luqui** | **4** |
| **Vlado** | **0** |

Y las tres tablas donde se anota el trabajo humano:

| Tabla | Filas | Qué significa |
|---|---|---|
| `incidencia_eventos` | **0** | Nadie registró nunca un contacto ni una resolución desde el sistema |
| `ritmo_log` | **0** | Las tareas diarias de Luqui no se marcaron ni una vez |
| `expenses` | **0** | Nunca se cargó un egreso |
| `incidencias` | 8 | Las 8 las cargamos nosotros el 05/08, ninguna la abrió una persona del equipo |

**Construir las cinco fases encima de esto es agregarle funcionalidades a algo que nadie
usó.** Es literalmente el caso que la Ley 8 y la Ley 9 —tus propias leyes, en
`astronomy-members/CLAUDE.md`— existen para frenar, y el protocolo del 18/08/2026 ya tiene
escrito qué pasa si estos contadores dan cero: *Sprint 4 suspendido, no se escribe una
línea de código.*

**Recomiendo:** no arrancar las Fases 1 a 5. Hacer las dos mañanas de observación con José
y con Luqui (ya planificadas en `active/astronomy/OBSERVACION.md`), llegar al 18/08 con
datos, y de ahí sacar qué se construye. Lo único que sí tiene autorización de la Ley 8 hoy
—porque sabemos que obliga a salir del sistema— es la **carga manual de leads que no
vinieron de la web**. Está justificado abajo, en §3.

Esto no dice que Astronomy OS sea mala idea. Dice que el cuello de botella no es de
software, y que gastar el próximo mes programando es la forma más cara de no averiguarlo.

---

# 1 · AUDITORÍA DEL SISTEMA ACTUAL

## 1.1 Tamaño real

| Qué | Cuánto |
|---|---|
| Pantallas (`page.tsx`) | 87, de las cuales **48 bajo `/admin`** |
| Server actions | 44 archivos en `app/actions/` |
| Rutas de API | 10 (`app/api/`), 4 de ellas crons |
| Tablas en Supabase | **68** |
| Vistas | 4 · Funciones SQL | 13 · Crons activos | 2 |
| Tablas en cero | 13 |

No es un sitio con un panel. Es una aplicación de gestión completa.

## 1.2 Qué de tu pedido YA ESTÁ CONSTRUIDO

Esta es la tabla que evita rehacer trabajo. Cada fila dice dónde vive.

| Lo que pediste | Estado | Dónde vive |
|---|---|---|
| Sistema de roles y permisos real | **Construido.** 16 permisos granulares, `is_master`, y `permissions[]` por persona | `lib/staff.ts` · tabla `staff` (7 filas) |
| Administrador asigna permisos desde la web | **Construido.** Sólo el maestro, con selector de rol y checklist de permisos | `/admin/alumnos/[id]/rol` |
| Cada uno ve sólo lo suyo | **Construido, y con dos capas.** El permiso dice quién *puede* entrar; el **dueño** dice de quién *es* el trabajo | `lib/staff.ts` + `lib/duenos.ts` |
| Roles Dirección / Academy Ops / Academy Finance | **Construido como concepto**, con otros nombres: `facu` / `jose` / `luqui` | `lib/duenos.ts` |
| Dashboard "qué tengo que hacer hoy" | **Construido.** `/admin` es una sola lista de trabajo, filtrada por dueño y permiso | `app/admin/page.tsx` + `lib/workflows.ts` (968 líneas) |
| Dashboard José: leads, seguimientos, pagos con problema, alumnos que requieren acción | **Construido.** Son tareas con dueño `jose` | `lib/workflows.ts` |
| Dashboard Luqui: pagos pendientes, errores, Mercado Pago, ingresos | **Construido.** Tareas con dueño `luqui` | `lib/workflows.ts` |
| CRM de leads con estados | **Construido al 70%.** Seis estados, motivos de cierre cerrados, timeline de 8 fuentes | `lib/casos.ts` · `lib/leads.ts` (751 líneas) · `/admin/leads` |
| Escalamiento y "qué pasa después" | **Construido.** 18 detectores, consulta/respuesta entre personas, vencimientos | `lib/problemas/` · `/admin/problemas` |
| Panel de profesores intacto | **Construido y en producción.** Calendario, alumnos, horarios, sueldo | `/profe/*` |
| Lanfran, sólo lectura del estudio | **Construido y en producción desde hoy, 06/08.** Permiso `view_calendar`: ve, no toca | `lib/staff.ts` |
| Label: demos con estado de revisión | **Construido.** `label_demos` con estados y bandeja | `/admin/label` |
| Label: lanzamientos con fechas y planificación | **Construido.** Cargar y publicar separados a propósito | `/admin/label/releases` |
| Sin emojis, estética de software empresarial | **Ya es la regla del repo** | `astronomy-members/CLAUDE.md` |
| Astronomy es la fuente de verdad, no WhatsApp | **Ya es la Ley 1 del repo** | `astronomy-members/CLAUDE.md` |

**Traducción: tu Fase 1 está hecha al 85%, tu Fase 2 al 70%, tu Fase 4 al 40%.**

## 1.3 Qué NO existe (trabajo genuinamente nuevo)

| Lo que pediste | Qué falta exactamente |
|---|---|
| **Leads de fuentes externas** | Hoy un lead **sólo existe si tocó la web**: sale de `lead_events`, `auth.users` y `subscriptions`. Alguien que escribió por Instagram o por WhatsApp **no tiene fila en ningún lado**. No hay alta manual, ni campo `fuente`. Éste es el agujero real del CRM |
| **Roles con nombre** | Hay permisos, no hay roles. Dar de alta a alguien es tildar hasta 16 casillas de memoria. No existe "es Academy Finance" como cosa asignable |
| **Módulo Dominé** | Prácticamente inexistente. `events` tiene **1 fila**; la ticketera (`tickets`, `ticket_orders`, `ticket_scans`) está en **0 y congelada**. No hay tareas de producción, ni proveedores, ni presupuesto, ni gastos por evento |
| **Splitwise interno entre socios** | **No existe nada.** Ni tabla, ni pantalla, ni concepto |
| **Label: tracks, versiones, metadata** | No existe. Hay demos (bandeja) y releases (publicación), no hay gestión de archivos ni versionado |
| **Transparencia societaria de Dominé** | No existe. Los porcentajes (35/35/15/15) no están en ningún lado del sistema |
| **Dashboard de Dirección** | No existe una vista global de los tres negocios |

## 1.4 Qué está incompleto o mintiendo

**a) Las 13 tablas en cero.** `awards`, `booking_reschedule_requests`, `checkout_intents`,
`contact_log`, `expenses`, `incidencia_eventos`, `label_demo_events`, `label_demos`,
`ritmo_log`, `slot_group_invites`, `ticket_orders`, `ticket_scans`, `tickets`.

Algunas son normales (el sello salió ayer). Otras son la evidencia del párrafo de arriba.

**b) `contact_log` está jubilada y el protocolo del 18/08 todavía la cuenta.**
El 05/08 el historial humano se unificó en `incidencia_eventos`. **Ningún archivo de la
app escribe ya en `contact_log`** — lo verifiqué grepeando: la única referencia que queda
es el script que la cuenta. Pero el *Protocolo del 18/08* en `astronomy-members/CLAUDE.md`
dice contar `contact_log` / `ritmo_log` / `expenses`.

Eso significa que **el 18/08, aunque José hubiera usado el sistema todos los días, uno de
los tres contadores iba a dar cero igual — y el contador que sí tiene la evidencia
(`incidencia_eventos`) no está en la lista.** Hoy los cuatro están en cero, así que el
veredicto no cambia; pero el instrumento que decide si se construye Astronomy OS estaba
roto y se iba a romper en silencio. *(Corregido — ver §4.)*

**c) Facu no tiene fila en `staff`.** Entrás como maestro por la variable de entorno
`ADMIN_EMAILS`, no por la base. Ya nos costó una vez: las alarmas no te llegaban. Cualquier
cosa que arme el organigrama leyendo `staff` te va a dejar afuera.

**d) Vlado es maestro y nunca usó el sistema.** `is_master: true` desde el 17/07, cero
acciones en 30 días. Pedís que Dirección sean vos y él: hoy Dirección es una sola persona.

**e) El módulo de pagos está congelado** por decisión previa (`CLAUDE.md`). Cualquier cosa
que toque cobros arranca chocando con ese congelamiento.

**f) Las clases viven en dos tablas.** `studio_events` (2178 filas, de Calendly hasta el
17/07) y `slot_bookings` (210, sistema propio). Leer una sola no da error: da una lista más
corta que parece correcta.

## 1.5 Riesgos

| Riesgo | Gravedad | Por qué |
|---|---|---|
| **Construir sobre adopción cero** | **Alta** | El riesgo principal, y no es técnico. Cinco fases nuevas encima de tres tablas vacías |
| Duplicar el CRM | Alta | El modelo de casos ya existe con seis estados. Tu embudo de siete estados mide otro eje (dónde está la persona) sobre el mismo objeto. Dos modelos de estado sobre la misma entidad se contradicen solos |
| Romper pagos / Mercado Pago | Alta | Módulo congelado, 58 ventas, 616 `payment_links`, webhook en producción |
| Duplicar la identidad de personas | Alta | `profiles` (66), `staff` (7), `auth.users`, `user_emails`, `ledger_aliases`, `client_closers`. Un lead manual mal modelado agrega un séptimo lugar donde vive "una persona" |
| Dos tablas de clases | Media | Ya nos mordió |
| RLS despareja | Media | De 68 tablas, muchas con RLS activo y **cero políticas**. Hoy funciona porque todo pasa por el service role en el server; una pantalla nueva que consulte desde el navegador se cae o filtra |
| `staff` como organigrama | Media | Le falta Facu, y `permissions[]` es un array sin catálogo en la base: el catálogo está en TypeScript |

---

# 2 · PROPUESTA TÉCNICA

Escrita para cuando se descongele. **Nada de esto se ejecuta antes del 18/08.**

## 2.1 Principio rector

**Astronomy OS no es un módulo nuevo: es terminar de nombrar lo que ya existe.** Casi todo
lo que pedís se consigue agregando una capa fina de nombres y tres tablas, no reescribiendo.

## 2.2 Roles con nombre, sobre los permisos que ya existen

No hace falta tabla nueva ni migración. Los roles se declaran en código como paquetes de
los permisos que ya existen, igual que `PERMISOS_ACOTADOS` en `lib/staff.ts`:

```
DIRECCION        → is_master
ACADEMY_OPS      → view_students, view_payments, add_credits, assign_payments,
                   manage_djdelivery, manage_studio, manage_calendar,
                   manage_announcements          (= lo que José ya tiene)
ACADEMY_FINANCE  → view_students, view_payments, view_metrics, view_salaries,
                   add_credits, assign_payments, manage_announcements
                                                 (= lo que Luqui ya tiene)
PROFESOR         → professor_name + su set
ESTUDIO_LECTURA  → view_calendar                 (= Lanfran, ya en producción)
LABEL            → manage_label, manage_releases, view_shared_access
```

Los paquetes que puse arriba **son exactamente los permisos que esas personas ya tienen
hoy en la base**: aplicar los roles no cambia el acceso de nadie. Es el cambio más seguro
posible y convierte "tildar 16 casillas" en "elegir un rol".

Cambio de UI: en `/admin/alumnos/[id]/rol`, elegir rol pre-tilda el paquete, y las casillas
quedan para la excepción. **Los permisos siguen siendo la única reja** — el rol es una
etiqueta que los agrupa, nunca una segunda fuente de verdad.

Coste estimado: **1 día**. Migraciones: **ninguna**.

## 2.3 Tablas nuevas — las mínimas

Sólo tres áreas necesitan tablas. Todo lo demás se reutiliza.

**A · Leads que no vinieron de la web** (Fase 2, el único candidato de hoy)

```sql
create table lead_manual (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  contacto text not null,              -- teléfono, @ de Instagram, mail
  fuente text not null,                -- whatsapp | instagram | referido | ads | otro
  detalle_fuente text,                 -- quién lo refirió, qué campaña
  interes text,                        -- qué producto
  user_id uuid references auth.users,  -- se llena SOLO cuando crea cuenta
  cargado_por uuid, cargado_email text,
  created_at timestamptz default now()
);
```

La clave de diseño: **`user_id` empieza nulo y se llena cuando la persona se registra.** A
partir de ese momento el lead deja de vivir acá y pasa a ser el caso que el sistema ya
detecta solo contra la base. Así el embudo que pediste no es una máquina de estados nueva:

| Tu estado | De dónde sale, sin inventar nada |
|---|---|
| Nuevo | fila en `lead_manual` sin contacto registrado |
| Contactado | hay un `incidencia_eventos` de contacto |
| Interesado | resultado del contacto lo dice |
| Cuenta creada | `lead_manual.user_id` dejó de ser nulo |
| Pago pendiente | `subscriptions.status = 'pending'` — ya se detecta |
| Alumno | fila en `sales` — ya se detecta |
| Cerrado | estado de cierre en el modelo de casos que ya existe |

**Cinco de los siete estados ya se calculan solos hoy.** Sólo los dos primeros necesitan
tabla. Eso mantiene la regla que sostiene el sistema: *el caso se detecta contra la base;
sólo se guarda lo que decidió una persona.*

**B · Dominé** (Fase 3)

```sql
evento_tareas       (evento_id, titulo, responsable_id, vence_el, estado)
evento_proveedores  (evento_id, nombre, rubro, contacto, monto_acordado, estado_pago)
evento_movimientos  (evento_id, fecha, concepto, pago_por, monto, tipo)  -- gasto|ingreso
evento_reparto      (movimiento_id, socio_id, porcentaje)                -- el Splitwise
```

Colgadas de la tabla `events` que ya existe. Los porcentajes societarios van en config, no
en la base: cambian por acuerdo, no por transacción.

**C · Label** (Fase 4)

```sql
label_tracks    (release_id, titulo, version, archivo_url, duracion, bpm, key, isrc)
label_versiones (track_id, n, archivo_url, nota, subido_por, created_at)
```

`label_demos` y `label_releases` ya existen y no se tocan.

## 2.4 Lo que NO hay que hacer

- **No crear una tabla `users` ni `roles` ni `permissions`.** Ya hay seis lugares donde
  vive una persona. El séptimo rompe la Regla 12.
- **No crear un embudo de leads con máquina de estados propia.** Se contradice con
  `lib/casos.ts`.
- **No crear `/os` ni una app aparte.** Todo entra en `/admin`, que ya tiene la reja.
- **No tocar pagos, créditos ni el webhook de Mercado Pago.**
- **No reemplazar `contact_log`**: ya está reemplazada, sólo hay que dejar de nombrarla.

## 2.5 Migraciones

Se aplican solas con el token de facu-os por la Management API, sin intervención tuya.
Ninguna de las tablas propuestas toca una tabla existente: son todas nuevas o cuelgan por
foreign key. **Ninguna migración destructiva, ninguna columna eliminada.**

---

# 3 · PLAN DE IMPLEMENTACIÓN

## Fase 0 — Hasta el 18/08/2026: no se construye

1. **Una mañana con José y una con Luqui.** Guion en `active/astronomy/OBSERVACION.md`.
   Sin ayudar, sin explicar, sin arreglar en el momento, anotando la frase textual.
2. **07 y 08/08: vencen las 8 preguntas** de Luqui y José. Ése es el primer dato real y
   llega antes que el 18.
3. **18/08: correr los contadores** —con la lista corregida— y aplicar el protocolo que ya
   está escrito. Sin excepciones.

## Lo único que la Ley 8 autoriza hoy

**Carga manual de leads.** Pasa el test que vos mismo escribiste: *¿esta persona necesita
salir del sistema para hacer su trabajo?* Sí — un lead que llega por Instagram o por
WhatsApp hoy no tiene dónde anotarse, y termina viviendo en la cabeza de José o en un chat.
Es un trabajo real que ocurre afuera, no una idea.

Alcance mínimo: la tabla `lead_manual`, un formulario de alta en `/admin/leads`, y que esos
leads entren a la misma cola de trabajo que los demás. **Nada más.** Sin embudo nuevo, sin
pantalla nueva, sin reportes.

Coste: 1 a 2 días. **Y aun así, mi recomendación es hacerlo después de la mañana con José,
no antes** — porque esa mañana puede mostrar que el lead de Instagram no es el que se
pierde, y entonces esto también sería una idea disfrazada de trabajo.

## Después del 18/08, si los contadores dan filas

Orden distinto al que propusiste, y ésta es la razón: tu Fase 1 casi no existe como trabajo
(1 día), y tu Fase 3 es la más grande de todas pero es la que menos evidencia de uso tiene.

| Orden | Qué | Días | Por qué acá |
|---|---|---|---|
| 1 | Roles con nombre + fila de `staff` para Facu | 1 | Sin migración, sin riesgo, arregla el alta de personas |
| 2 | Leads manuales + fuente | 2 | Es donde está la plata: leads que hoy se pierden |
| 3 | Dashboard de Dirección | 3 | Se arma leyendo lo que ya existe. Y es la única forma de que Vlado tenga motivo para entrar |
| 4 | Label: tracks y versiones | 3 | El sello ya está en producción y va a necesitar dónde poner los archivos |
| 5 | Dominé: evento como unidad + gastos | 5 | Grande y sin evidencia de uso todavía |
| 6 | Splitwise entre socios | 3 | Depende de 5 |

**Fase 5 (Dirección) sube al puesto 3 a propósito.** Es barata, no toca nada crítico, y
ataca el número más preocupante de toda esta auditoría: el socio que es maestro del sistema
y nunca lo abrió.

## Reglas de ejecución, para cada una

1. Cada fase arranca declarando **qué trabajo humano elimina** y **quién lo ejecuta hoy sin
   el sistema**. Si no se puede nombrar la persona, no se construye.
2. Cada fase termina con un contador, no con un deploy. Dos semanas de uso sin
   instrucciones, o no está terminada.
3. Nada que toque pagos, créditos, clases o accesos actuales entra en el mismo commit que
   una función nueva.
4. `code-reviewer` y `qa` en paralelo antes de usar nada.

---

# 4 · LO QUE YA CORREGÍ

Una sola cosa, y no es código: la línea del **Protocolo del 18/08** en
`astronomy-members/CLAUDE.md` nombraba `contact_log`, que está jubilada desde el 05/08 y no
tiene escritores. Quedó apuntando a `incidencia_eventos`, que es donde hoy se escribe el
trabajo humano.

Sin ese cambio, el 18/08 la medición que decide si Astronomy OS se construye o no iba a dar
un cero falso, y nadie se iba a enterar.

---

# 5 · LO QUE NECESITO DE VOS

1. **Confirmar el freno**, o decirme que lo levantás igual. Si lo levantás, lo hago y no lo
   discuto más: es tu empresa y tu plata. Sólo quería que la decisión estuviera tomada con
   los contadores a la vista.
2. **Vlado.** ¿Va a operar el sistema o alcanza con que lea? Cambia si Dirección son dos
   perfiles o uno con un tablero de lectura.
3. **Dominé.** ¿Hay un evento concreto en los próximos 60 días? Si no lo hay, la Fase 3 no
   tiene contra qué probarse.
4. **Label.** ¿Los tracks van a vivir en Drive o adentro del sistema? Cambia si hay que
   subir archivos pesados o sólo guardar links.
