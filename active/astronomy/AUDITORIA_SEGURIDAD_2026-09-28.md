# Auditoría de seguridad — astronomyofficial.com (astronomy-members)

**28/09/2026.** Hecha con los 20 puntos del reel de Alejo Sant'Anna (transcripto con Whisper local).
Cuatro auditores en paralelo: base de datos, login/permisos, plata, código/secretos. Todo solo lectura:
nada se escribió en la base ni se atacó producción.

## Estado de los arreglos (28/09)

**Tarde, 28/09:** Facu corrió `aplicar-seguridad.mjs` → verificado: Facu `is_master=true` en staff y `extender_vencimientos_por_pago` da 401 a anon. Commit `7807afd` (Ready): el maestro sale sólo de `staff.is_master`. **C1 y C2 CERRADOS; A3 cerrado (candado en `spend_credits`).**

Commit `82a513b` en astronomy-members, Vercel Ready:

- ✅ **En producción:** C3 (Next 16.3.6) · A1/A2 cancelaciones con guarda (también el cruce alumno+staff en grupales) · A3 parcial (grupal mira el cobro) · A4 (plan B va último) · A5 open redirect (verificado con curl en prod) · A6 parcial (2 pendientes por mail, reserva 15 min) · testpay sólo maestro · helpers fuera de `"use server"` (verificado en el manifest).
- ⏳ **SQL escrito, lo corre Facu** (el clasificador de permisos no me deja tocar grants): `supabase/seguridad_2026_09_28.sql` (C2 revoke, `spend_credits` con candado = resto de A3, CHECK, índice de reintegros) y `supabase/staff_maestro_facu.sql`. Antes de correrlo, re-chequear 0 lotes negativos y 0 `refund:slot:` duplicados.
- ⏳ **C1:** después de la fila de maestro de Facu, sacar `ADMIN_EMAILS` de `lib/staff.ts`, `lib/destinatarios.ts`, `lib/adminData.ts`, `app/actions/auth.ts`. Mirar `ADMIN_EMAILS` en Vercel (no se lee por CLI: `[SENSITIVE]`).
- ⏳ **Sin hacer:** límite por IP (firewall de Vercel) para entradas, login y `/recuperar` · captcha · 2FA · apagar autoconfirm (cambia el registro: decisión de Facu) · medios y bajos · arreglar `test:seguridad`.
- Riesgo nuevo anotado por la revisión: si `confirmSlotGroup` se corta entre tomar el invite y cobrar, el invite queda `confirmed` sin salida (hay que destrabarlo a mano).

PROBADO = se verificó contra producción o la base. INFERIDO = leído del código, sin explotar.

## CRÍTICO

| # | Qué | Estado | Arreglo |
|---|---|---|---|
| C1 | **Cualquiera puede volverse maestro.** `lib/staff.ts:83` da maestro a todo mail de `ADMIN_EMAILS`, y Supabase tiene `mailer_autoconfirm: true` + registro abierto (PROBADO). En `.env.local` hay 2 mails y **uno no tiene cuenta** (PROBADO): quien se registre con ese mail entra como maestro (sueldos, finanzas, créditos). El valor de Vercel prod no se puede leer desde la CLI (sensible). | Depende de prod | Mirar `ADMIN_EMAILS` en Vercel YA. De fondo: maestro sólo por `staff.is_master` + apagar autoconfirm |
| C2 | **`extender_vencimientos_por_pago` la puede llamar cualquiera sin login.** PROBADO: con la anon key se ejecutó (devolvió 0 sobre un uuid inexistente). Un alumno se extiende los créditos 2 meses por llamada, sin límite. Se creó el 01/09, después del cierre de RPCs del 08/08. | PROBADO | `revoke execute ... from public, anon, authenticated` |
| C3 | **Next 16.2.10 con CVEs** (1 crítico, 3 altos: bypass del proxy, DoS de server actions, exposición de server functions, cache confusion). PROBADO con `npm audit`. | PROBADO | Subir a `next@16.3.6` |

## ALTO — créditos o plata gratis

| # | Qué | Dónde | Arreglo |
|---|---|---|---|
| A1 | Cancelar la misma clase 10 veces en paralelo devuelve 10 veces los créditos (60 cr ≈ $35.880 c/u). Hoy 0 duplicados (PROBADO). | `app/actions/availability.ts:307-342` | update con `.eq("status","active")` + reintegrar sólo si tocó 1 fila; índice único en `credit_lots.source` para `refund:%` |
| A2 | Lo mismo en la grupal, y paga a los dos alumnos. | `availability.ts:727-747` | ídem |
| A3 | `spend_credits` sin lock: con 60 créditos se reservan N clases en paralelo; saldo puede quedar negativo. Hoy 0 negativos (PROBADO). | `supabase/schema.sql:114-140` | `pg_advisory_xact_lock` por usuario + `for update` + `CHECK (amount_remaining >= 0)` |
| A4 | Un alumno logueado se queda con el cobro de otro que paga por link viejo de MP: entra a `/pagar/alternativa?plan=platinum` sin pagar, y el próximo Platinum sin referencia en 48 hs se le acredita a él. `checkout_intents` hoy en 0. | `app/pagar/alternativa/route.ts`, `lib/payments.ts:236-270`, `lib/checkoutFallback.ts` | intención después de payer_id/mail; sólo si hubo `checkout_error` reciente; una por usuario |
| A5 | Open redirect: `/login?next=//sitio.com` manda afuera después del login (PROBADO que el `next` se acepta). Phishing con el dominio real. | `auth.ts:47,132,143,151`, `login/page.tsx:18`, `registro/page.tsx:20`, `auth/confirm/route.ts` | una función `destinoSeguro()` |
| A6 | Se puede agotar una tanda de entradas sin pagar: compra anónima, 10 por pedido, retiene 30 min, sin límite ni captcha. Riesgo concreto para Obsession/Dominé. | `app/actions/comprarEntradas.ts:39,131` | Turnstile + tope de pendientes por mail/IP + retención 10-15 min |

## MEDIO

- **Registro con mail ajeno** (autoconfirm): si alguien registra primero el mail de un futuro alumno o staff, José le acredita el pago o Facu le da permisos a él. Afecta `saveStaff`, `acreditarAAlumno`, `asignarPago`, `registrarPagoManual`, el puente por `user_id_by_email`.
- **Login sin rate limit, sin 2FA, clave mínima 6.** Supabase ve la IP de Vercel, no la del atacante. No se registran logins fallidos.
- **Bombardeo de mails de recuperación:** `requestPasswordReset` usa `generateLink` + Resend sin tope → quema la cuota y dejan de salir QR de entradas y resets.
- **Nombres de alumnos extraíbles desde el registro:** `auth.ts:67` usa `ilike` con el nombre sin escapar `%`/`_`.
- **HTML inyectable en mails oficiales:** `lib/email.ts` no escapa `full_name` ni `buyer_name` → link de phishing en un mail de Astronomy a profes/staff.
- **Fórmulas en CSV exportados:** `lib/adminData.ts:331`, `lib/metrics.ts:224` no neutralizan `= + - @`.
- **Contracargos y devoluciones de MP no sacan nada:** el que hace contracargo se queda con créditos/entradas.
- **Grupal confirmada aunque el cobro falle:** `confirmSlotGroup` ignora el resultado de `spend_credits`.
- **Cualquier staff (profes, Annie, Lola) se compra 1000 créditos por $15:** `app/actions/testpay.ts:24` → exigir maestro.
- **La suspensión sólo se aplica en `/member`:** un suspendido reserva igual desde `/reservar`.
- **`contact_log`:** la policy le abre la tabla entera a cualquier fila de `staff` vía PostgREST.
- **La batería `test:seguridad` está rota** (exit 1: chequeo de Bronze viejo + `lib/equipo.ts` borrado) y no controla funciones → por eso C2 entró sin aviso.
- **Helpers exportados desde `"use server"`:** `syncCalendarOnBook` y `profeEmailFor` (`availability.ts:247,296`) quedan como endpoints públicos; el primero crea eventos en el calendario del estudio con invitación a cualquier mail.
- **Faltan headers:** sin CSP, X-Frame-Options, nosniff, Referrer-Policy; `x-powered-by: Next.js` (PROBADO).
- **`/api/track`** acepta escrituras sin límite → ensucia embudo y UTM.

## BAJO

Grants de más a `anon`/`authenticated` (hoy lo frena RLS) · `notifications` editables por su dueño ·
webhook de MP abre si falta el secreto (en prod está: 327 avisos firmados) y no valida `ts` ·
`expire_ticket_orders`/`mark_ticket_email_sent` ejecutables por anon · cookie de la puerta cae a clave vacía ·
`lib/supabase/admin.ts` sin `import "server-only"` · tipo de imagen subida por `file.type` ·
`.gitignore` sin patrones genéricos (`*.env`, `claves-*`, `*-sa.json`) · **contraseñas en texto plano en
la carpeta del repo** (`claves-admins.txt`, `claves-alumnos.txt` 164 líneas, `clave-fer.txt`,
`claves-temporales.csv`: no están en git, pero conviene borrarlas) · monto cobrado no se compara contra el
precio (hoy no explotable) · entrada pagada dos veces no avisa · devolución cargable dos veces (sólo staff) ·
token de RRPP no vence · `/api/calendario` muestra reservas de todos los profes a cada profe.

## Lo que está bien (probado)

- Las 97 tablas con RLS activo; con la anon key sólo se ven `plans`, anuncios activos y perfiles de profes (a propósito). Un alumno no puede leer filas de otro. Sin IDOR.
- Las 15 RPC de plata del 08/08 siguen cerradas. Webhook de MP con firma HMAC en tiempo constante; pagos idempotentes; precios calculados en el servidor.
- ~150 server actions revisadas: todas chequean permiso adentro. Páginas `/admin` chequean en el servidor. Crons con secreto y `timingSafeEqual` (401 sin él, PROBADO).
- Ningún secreto en git (historial completo revisado). La service key no llega al navegador. Sin source maps, `.env` y `.git` dan 404.
- Sin SQL injection, sin XSS por `dangerouslySetInnerHTML`, sin SSRF. Storage no listable ni escribible por anon.

## Los 20 puntos del video

| Punto | Estado |
|---|---|
| Revisar permisos | ⚠️ C1, testpay, contact_log |
| Proteger panel admin | ✅ chequeo server-side en todas las páginas · ⚠️ C1 |
| Separar datos entre clientes | ✅ RLS por `auth.uid()` |
| Blindar la base | ⚠️ C2, grants de más |
| Ocultar claves privadas | ✅ en git y bundle · ⚠️ claves en texto plano en disco |
| Asegurar inicio de sesión | ⚠️ autoconfirm, open redirect, clave de 6 |
| Cerrar sesiones | ✅ `getUser()`, logout por POST |
| Doble factor | ❌ no existe para staff |
| Inyección SQL | ✅ · ⚠️ `ilike` sin escapar en registro |
| Código malicioso (XSS) | ✅ en la web · ⚠️ HTML en mails, CSV |
| Acciones sensibles | ✅ en general · ⚠️ carreras A1-A3 |
| Validar archivos subidos | ✅ sólo staff, sin SVG · ⚠️ tipo por `file.type` |
| Bloquear accesos internos (SSRF) | ✅ |
| Verificar webhooks | ✅ firma HMAC · ⚠️ sin `ts` |
| Evitar pagos duplicados | ✅ idempotente · ⚠️ A4, contracargos |
| Limitar solicitudes | ❌ no hay rate limit en ningún lado |
| Dependencias vulnerables | ❌ C3 |
| Paneles expuestos | ✅ · ⚠️ helpers `"use server"` |
| Detectar accesos sospechosos | ❌ no se registran logins fallidos |
| Probar hasta romper | ⚠️ `test:seguridad` roto |
