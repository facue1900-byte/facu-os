# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una entrada acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, va a memoria en `indice-trampas.md`.

### 2026-10-09 · FAIL · La tarea «Aprobar comentarios» no tenía ningún botón

**Dónde:** `astronomy-members`: `app/admin/hacer/[id]/page.tsx`, `lib/workflows.ts`.

**Qué pasó:** José (08/10): «no sé dónde poner publicar». El caso declaraba el botón
«Publicar en la web», pero la cola sólo dibuja `botones` adentro de casos con `resolverEn`;
éste no tenía, así que no se veía nada. «Descartar» tampoco andaba: anotaba el id del
COMENTARIO en `incidencia_eventos.persona_id` (FK a `auth.users`) y fallaba siempre.

**Causa raíz:** un caso nuevo con una forma que la pantalla no contemplaba (botones sin
pantalla de destino), y nadie lo abrió en la cola real antes de darlo por hecho (06/10).

**Fix:** commits `a1f4461` + `d189adf`: la cola dibuja botones sin `resolverEn`; Publicar /
No publicar escriben en `encuesta_profes` (`comentario_descartado_at`, columna nueva, no
se borra nada); Deshacer 15 min; `noEsPersona` saca Posponer/Ya no aplica de casos cuya
clave es un uuid que no es persona. Push frenado hasta aplicar la columna.

**Lección:** una tarea nueva de la cola se da por hecha recién abriéndola en
`/admin/hacer/<id>` y apretando cada botón. Que el caso traiga el botón no prueba que se vea.

### 2026-10-07 · FAIL ✓ · Cada tarea programada se cuidaba sola, y dos se cayeron

**Dónde:** `execution/launchd/*.plist`, `execution/reporte_equipo.py`, `cierre_mensual.sh`.

**Qué pasó:** el reporte del equipo del viernes 02/10 no salió ("JWT issued at future": la
Mac recién despierta, una sola vez; corrido de nuevo anduvo). Ese sí mandó mail de error.
El cierre del Paseo del 16/09 falló sin red y no avisó a nadie: `cierre_mensual.sh` no
tenía aviso. Y `alerta-rampa` llevaba dos meses sin cargar en launchd (sí documentado).

**Causa raíz:** no había una forma única de correr una tarea. Cada plist resolvía red,
reintento y aviso a su manera: `efectivo-diario` esperaba la red y mandaba mail,
`reporte-pauta` y `verificar-leads` tenían reintento y notificación pegados en el plist,
los otros nada. Y ninguna tarea puede avisar que NO corrió.

**Fix:** `execution/launchd/correr.sh` envuelve las 7 (espera red, registra en
`data/logs/tareas.jsonl`, avisa si falla); el radar calcula contra ese registro qué falló,
qué no corrió y qué no está cargado (`chequeo_tareas`, con test que le fabrica las tres
fallas). `juntar()` del reporte del equipo reintenta 3 veces: sólo lee.

**Lección:** una tarea programada no puede ser la única que vigila si corrió. El registro
lo escribe el wrapper y lo lee otro (el radar). No se reintenta una tarea que escribe o
manda: se reintenta el paso que lee.

### 2026-09-23 · FAIL ✓ · "Ya está cargado" sin decir qué: $1,14M de gastos que no existen

**Dónde:** `astronomy-members`, espejo de MP (`app/actions/espejoMp.ts`) y tareas de Luqui (`lib/workflows.ts`), commit `63558de`.

**Qué pasó:** el retiro de MP del 08/09 ($2.115.838,57 = pauta + suscripciones jul-ago) se cerró con "ya cargado" y un texto. En el Libro había sólo agosto ($974.491): ≈$1.141.348 de gastos en ningún lado, con el movimiento dado por resuelto. Y una cuota de Inchausty se cargó dos veces (31/07 y 04/08) porque cada carga era válida por separado.

**Causa raíz:** una decisión que dice "esto ya está en otro lado" sin apuntar a QUÉ no se puede verificar, y ninguna pantalla preguntaba "¿esto ya existe?" antes de escribir plata (salvo para sueldos).

**Fix:** el gasto queda atado al movimiento (`expenses.mp_mov_id`); cerrar una salida exige tildar gastos que sumen igual; un gasto suelto del mismo monto frena la carga; un gasto borrado reabre el movimiento; la carga manual frena una cuota del mismo plan a ±20 días. Además las tareas diarias de ritmo de Luqui (0 usos en 7 semanas) se reemplazaron por evidencia: transferencias vencidas, resumen mensual de tarjeta, sueldos por persona después del 5.

**Lección:** toda decisión que cierra un movimiento de plata apunta a la fila que lo explica. Un texto libre como prueba es un chequeo que nunca falla.

### 2026-09-23 · FAIL ✓ · La cola de José: 0 de 15 casos de créditos eran corregibles, y un filtro que no filtraba nada

**Dónde:** `astronomy-members`, `lib/workflows.ts` y `lib/auditoriaCreditos.ts` (commit `2dee6cc`).
Disparador: Facu pidió auditar las tareas de José "asumiendo que está todo mal hecho".

**Lo que estaba mal, por causa raíz:**
- **`'cancelled'` vs `'canceled'`.** La base escribe `canceled` con una L; el motor comparaba con
  dos. 49 clases canceladas de la web y 290 de Calendly contaban como "vino" o "tiene clase
  futura". Pasó `tsc` y nunca falló nada: un filtro que no filtra no da error.
- **El esperado de créditos tenía cinco sesgos más**: no leía devoluciones (Basso "le faltan 240"
  sobre un cobro devuelto), asignaba clases por fecha de clase y no de reserva (se paga al
  reservar), ignoraba lo reservado pasado el vencimiento y las cancelaciones cobradas (−24 hs),
  y valuaba los pagos viejos con los créditos del plan de hoy (Silver 250→240 el 22/09 = "+10 por
  mes" a todo Silver viejo). Y para quien tiene saldos puestos a mano en julio no es calculable.
- **El freno de premios sólo miraba `dif > 0`**: del lado de "le faltan", el botón regalaba.
- **La cola mandaba a José a apretar "Está bien así" en filas donde ese botón estaba oculto.**
- **`contactar.ts` tiene una lista cerrada de resultados**: un botón nuevo sin sumarse ahí vuelve
  a la cola sin anotar nada. Lo agarré antes de publicar.

**Fix:** una sola función `porQueNoSeCorrige` para botón, pantalla y cola; los cinco términos del
esperado corregidos; los no calculables frenados con su motivo (15 → 9, 0 con botón). La cola de
José pasó a ser sólo de contacto (pagos que no entraron, cuentas sin compra, paga a mano,
inactivos), una persona por tarea. La revisión independiente encontró 3 bugs míos antes del push
(suscripciones `pending` contadas como compra, "agendó y canceló" tratado como "nunca agendó",
`profiles` sin paginar).

**Lección:** comparar contra un literal de estado sin verificar qué valores existen en la base es
un chequeo que nunca falla — regla 3 de la Constitución. Antes de filtrar por `status`, contar los
valores reales (`select status` + agrupar).

### 2026-09-18 · FAIL ✓ · Una diferencia de créditos que era el neto de cuatro errores

**Dónde:** `astronomy-members`, `lib/auditoriaCreditos.ts` y `/api/admin/export`.
Disparador: dos mensajes de José por WhatsApp a la mañana.

**Lo primero era simple.** "Descargar CSV" en `/admin/usuarios` le abría una pestaña en
blanco con **No autorizado**. La pantalla entra con `view_students`, que él tiene; la ruta
`/api/admin/export` autorizaba contra `ADMIN_EMAILS`, una variable de entorno con un solo
mail. Lo que lo hacía indiagnosticable: **lo que faltaba no era un permiso**, así que mirar
`staff.permissions` —que es el reflejo correcto— no alcanzaba, y `/admin/accesos` no podía
arreglarlo. Fix: las dos rutas de export autorizan con `view_students`, y
`verificar:permisos` recorre `app/api/admin/**/route.ts` y falla si alguna vuelve a gatear
por lista de mails **o si pide `getStaffContext()` sin chequear nada con él** — el segundo
chequeo salió de la revisión, porque sin él una ruta sin reja pasaba en verde.

**Lo segundo es la lección.** La cola *Corregir créditos* le mostraba a José "Juan Manuel
Inchausty tiene 60 créditos de más" con un botón que se los sacaba.

Encontré que `esperado` suma los créditos de premios y compras sueltas por lo que **queda**
del lote, pero resta **todas** las clases: un premio gastado vale 0 en el saldo y la clase
que pagó se sigue restando. Inchausty tenía 70 de premio, le quedaban 10 → gastó 60. Su
`dif` era **+60**. Cerraba perfecto, y lo escribí como causa verificada.

**No era la causa.** El auditor de números levantó la identidad real:

```
dif = extraGastado − (clases canceladas que igual se cobraron) + (lotes del plan − otorgadoTotal del Libro)
+60 = 60 − 120 + 180 − 60
```

Los 180 de refunds gastados y los −120 de cancelaciones son **más grandes** que el término
que yo había medido. El +60 coincidía con los premios por casualidad aritmética.

**Causa raíz del error mío:** un número que cierra exacto con una hipótesis se siente como
una demostración, y no lo es cuando el resultado es un **neto de varios términos con signo**.
Un solo caso no distingue "esto lo explica" de "esto suma lo mismo que el resto neteado".

**Lo que quedó, y por qué frena en vez de corregir.** El freno no afirma una causa: afirma
lo único verificable —*si hay premios gastados, el esperado no es confiable*— y se niega a
escribir. Dos cosas más que salieron de la revisión y valen por sí solas:

- El caso **no se filtra de la cola**. La primera versión lo hacía, y un caso que desaparece
  sin que nadie lo haya resuelto no deja dueño ni rastro (Ley 1). Se queda, diciendo por qué
  no se corrige y apuntando a la cuenta en vez de al botón.
- `corregirSaldo` **descartaba el resultado** y redirigía igual: un "no se pudo" se veía
  idéntico a un "listo". Regla final de la Constitución, en una acción que mueve plata.

**Abierto, y es decisión de Facu:** reescribir `esperado` para contar los cuatro términos;
las cancelaciones sin reintegro (Segundo Pinto 920 cr y 0 reintegrados, y siete más); y
sobre todo que **1.190 de 1.547 `studio_events` activos no tienen `user_id` (77%)** — el
`consumido` de Santiago Pacino son 7 clases de ~60, así que su "+60" está armado sobre un
octavo de sus clases. Es el único que quedó con botón vivo y **no hay que apretarlo**.

### 2026-09-11 · FAIL ✓ · El historial de las demos sólo registraba al primero que abría

**Dónde:** `astronomy-members`, bandeja de Astronomy Records (`/admin/label`).

Facu pidió ver en cada demo quién la abrió, quién la tickeó y quién puso el veredicto, con
un círculo de iniciales y un color por persona. Al construir la columna apareció el bug de
abajo — no se estaba buscando: **el dato que la columna iba a mostrar no existía**.

**El síntoma fue un número demasiado prolijo.** La tabla `label_demo_events` tenía 30
eventos `kind = "vista"` para 30 demos. Uno por demo, ni uno de más, con cuatro personas
entrando a la bandeja desde agosto.

**Causa raíz:** el `anotarEvento({ kind: "vista" })` estaba escrito adentro del `if` que
gana el candado de la primera apertura (`update … .is("first_seen_at", null)`). O sea que
sólo se anotaba la vista **del primero que entraba**; el segundo y el tercero no dejaban
rastro. Son dos preguntas distintas metidas en un mismo `if`: *¿quién fue el primero?* se
contesta una vez, *¿quién la abrió?* se contesta una vez **por persona**. Con dos personas
en el equipo las dos respuestas coinciden y el bug no existe; con seis —Facu autorizó a los
tres profes el mismo día— la pregunta que importa se queda sin respuesta.

**Fix:** la regla salió de la página y se fue a `registrarApertura()` en
`lib/label/demos.ts`, que pregunta por `(demo, persona)` antes de anotar. La ficha la llama
y **el verificador corre exactamente esa función**, como ya se hacía con `aplicarVeredicto`.
El candado de `first_seen_at` no se tocó: sigue diciendo quién llegó primero y sigue siendo
el que dispara New → Listening (verificado: dos aperturas, un solo pase de estado).

**Lo que evita que vuelva:** dos verificadores nuevos. `npm run verificar:firmas` prueba la
regla contra Postgres con una demo descartable, y `npm run verificar:firmas-pantalla` abre
**la misma ficha con dos sesiones distintas** por magic link y cuenta los círculos de la
fila. El segundo es el que importa: la regla puede estar perfecta y la columna mostrar una
sola cara igual. Los dos se probaron en rojo —se reintrodujo el bug a mano y fallaron 4
chequeos— antes de darlos por buenos ([[chequeo-verde-con-el-codigo-roto]]).

**Lo que se aprendió, transferible:** una línea de auditoría hay que preguntarse de qué es
única, si del hecho o de la persona. Y un chequeo que cuenta filas no protege esto: "hay 30
eventos" da verde con el bug puesto. Hay que contar caras.

**De paso:** el directorio de personas sale de `destinatariosDeAviso()` y no de un
`from("staff")`, por el agujero ya documentado — Facu es maestro por `ADMIN_EMAILS`, no
tiene fila en `staff`, y es quien más demos abrió: recorriendo la tabla se quedaba sin cara
justo él.

### 2026-09-01 · FAIL ✓ · Tres preguntas de Luqui, tres bugs distintos y uno que no existía

**Dónde:** `astronomy-members`. Commits `675bc50` (espejo de MP) y `ae2b82e` (sueldos fijos).

Luqui, a las 8:18 de la mañana, arrancando la liquidación: (1) a una alumna le
descontaron créditos «con fecha de hoy pero con horario 10am, y acá son las 8»; (2) desde
`/admin/mp` no puede sumar créditos, así que carga cada pago dos veces; (3) en los egresos
de agosto no figuran los sueldos.

**Lo importante: sólo dos de los tres eran bugs, y el tercero no era ninguno.**

**1. Los créditos: no había bug, había un reloj mintiendo.** Verificado contra la base: las
5 reservas de Christine Bell se crearon el 01/09 entre las **07:37 y las 07:40** hora
argentina, y los 5 débitos tienen esa misma hora al minuto. El descuento es sincrónico al
agendar y no existe ningún cron que toque créditos. Lo que estaba mal era **la hora que
mostraba la ficha**: `toLocaleString("es-AR", …)` **sin `timeZone`** se renderiza en el huso
del servidor, y en Vercel eso es UTC → **3 horas adelantada**. Reproducido: el mismo instante
daba `10:40` con el código viejo y `07:40` con el nuevo. Estaban mal **12 pantallas**, y las
otras sí declaraban el huso: convivían dos horas distintas del mismo hecho. Ahora sale de
`lib/hora.ts`, un solo lugar.

**La primera explicación fue equivocada, y vale anotarla:** supuse que Luqui estaba en otro
huso y que la hora era correcta. Facu lo corrigió (*«mandó el mensaje a las 8:18 ARG»*) y
recién ahí apareció el bug real. **Una explicación que cierra no es una explicación
verificada.**

**2. El doble trabajo en MP era una herramienta que faltaba, no un descuido.** Un cobro sin
identificar tenía una sola salida de carga —escribir un renglón suelto en `expenses`, sin
alumno y sin créditos— así que Luqui lo cargaba en `/admin/carga-manual` y dejaba el
movimiento intacto, porque cerrarlo se lo duplicaba. **La opción honesta no existía**: por eso
`mp_decisiones` estaba literalmente vacía y había 89 movimientos colgados.

**3. Los sueldos de agosto sí estaban cargados; el problema era de MES.** Se imputan al mes
**devengado**, `/admin/sueldos` abre en el mes **anterior** y `/admin/libro` en el **actual**.
Luqui liquidó julio, fue al Libro, vio agosto y no encontró nada. Nada falló. Ahora la
pantalla dice a qué mes va lo que marcás, con el link a **ese** mes.

**Lo que casi se rompe en silencio, y lo agarró la auditoría, no el código:**

| | |
|---|---|
| Sin `source_id` se acreditaba con un id interno del espejo | el webhook acreditaba **el mismo pago de nuevo** más tarde: créditos duplicados, sin error |
| El fijo con `valid_from` el día 1 se colaba en el mes anterior | junio de Pastrana daba **$774.000** sobre $484.000 pagados |
| `expenses` y `salary_payments` se suman sin cruzarse | marcar pagados los sueldos de diseño **inflaba el mes $926.500** |
| `ORIGEN_SENSIBLE` copiado a mano en dos archivos | un origen nuevo **no falla: filtra**. El sueldo de diseño quedaba a la vista de cualquiera |

**Las tres lecciones que quedan:**

1. **Un reporte de usuario suele traer más de un bug, y alguno no es bug.** «No figuran los
   sueldos» era una pantalla mirando otro mes; «10am» era un huso; el doble trabajo era una
   funcionalidad que faltaba. Tratarlos como uno solo lleva a arreglar el que no era.
2. **Un pago de más recurrente es un trato que el sistema no conoce.** Los $290.000 de
   Pastrana estuvieron anotados un mes como error de Luqui y eran su sueldo fijo. **Sigue
   abierto el mismo patrón con Owners of Time: $15.000 de más en julio, sin explicar.**
3. **Una constante copiada en dos archivos no falla cuando se agrega un caso: filtra.** Es
   peor que un error, porque no avisa.

**Chequeo nuevo:** `npm run test:sueldo-fijo`. Verificado que **falla** con las dos versiones
rotas del cálculo de vigencia — no alcanza con que dé verde.

**Restricción del entorno que costó tiempo:** la Management API de Supabase está detrás de
Cloudflare y rechaza el `User-Agent` de `urllib` con un **403 «error code: 1010»**, un error
que no dice nada del token y manda a buscar el problema donde no está. `execution/supabase_sql.py`
manda uno propio.

---

**Julio y agosto 2026** (133 entradas, movidas el 07/10/2026): en
[`archive/lab-notes/LAB_NOTES-2026-07-y-08.md`](archive/lab-notes/LAB_NOTES-2026-07-y-08.md),
con índice arriba. Cuando este archivo vuelva a pasar los ~60 KB, se mueve igual el
trimestre más viejo: buscar ahí con `grep -rn "<tema>" LAB_NOTES.md archive/lab-notes/`.

## 2026-10-07 — La nube de Claude Code bloquea dominios que no están en su lista

**Qué pasó:** la rutina de la carpeta cripto (`trig_01DjiQf8wctTrs8xAgXjaNR1`) corrió en la nube y
`data-api.binance.vision` devolvió `Tunnel connection failed: 403 Forbidden`. El entorno Default
de claude.ai/code tiene acceso de red restringido: sólo deja salir a una lista de dominios.
El script falló bien (no operó sin precio) y la rutina avisó con `CARTERA_FALLA`.

**Lección:** antes de mudar a una rutina en la nube algo que llama a una API externa, probar
ese dominio desde la nube (una corrida con `curl`), no desde la Mac. Se arregla habilitando el
dominio en Network access del entorno. Además, `api.binance.com` da 451 desde IPs de EE.UU.:
para datos públicos usar el espejo `data-api.binance.vision`.
