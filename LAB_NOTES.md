# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una entrada acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, se destila como nota en el vault.

### 2026-08-04 · Dos sesiones sobre el mismo repo, y un `git add -A` que se llevó puesto trabajo ajeno

Construyendo el Centro de Problemas en `astronomy-members`, otra sesión de Claude estaba
trabajando el mismo repo al mismo tiempo. Se notó tarde y por un síntoma raro: `npx tsc
--noEmit` había pasado limpio, y diez minutos después fallaba en `lib/leads.ts`, un archivo
que no había tocado. El número de línea del error incluso se movió entre dos corridas
seguidas — alguien estaba escribiendo mientras yo compilaba.

**Causa raíz: en un repo compartido, `git add -A` no commitea "mis cambios", commitea el
estado del disco.** El commit `7c63d8d` de la otra sesión ("Las cards de una lista median
distinto y el scroll de leads no andaba") se llevó dos archivos míos a mitad de camino
(`app/actions/conciliacion.ts` y `app/actions/auditoriaCreditos.ts`), que quedaron en la
historia bajo un mensaje que no los describe. No rompió nada —los cambios estaban completos
y compilaban— pero el rastro quedó mintiendo: buscar cuándo se refactorizó la corrección de
saldos lleva a un commit sobre el scroll de una lista.

**Lo que se hizo:**

1. Stagear **por nombre**, nunca `git add -A`, en cuanto `git status` muestra archivos que
   no toqué.
2. Antes de pushear, verificar en un árbol que tenga **sólo lo commiteado**:
   `git worktree add <tmp> HEAD` + `tsc` + `build` ahí adentro. Es la única forma de saber
   si lo que se va a deployar compila, cuando el árbol de trabajo tiene trabajo ajeno sucio.
3. Recién con eso en verde, `git push` — que en este repo **deploya solo a producción**.

**La trampa técnica del paso 2:** symlinkear `node_modules` al del repo real no sirve.
Turbopack corta con `Symlink [project]/node_modules is invalid, it points out of the
filesystem root` y el build muere. Hay que copiarlo: 437 MB, unos 20 segundos. `tsc` sí
anda con el symlink; el que no lo tolera es el build.

**Lo que queda abierto:** no hay forma de enterarse de que otra sesión está trabajando el
mismo repo salvo mirando `git status`. Vale la pena hacerlo **antes de empezar**, no al
final: si hubiera mirado al arrancar, habría stageado por nombre desde el principio y los
dos archivos no habrían terminado en el commit equivocado.

### 2026-08-04 · FAIL ✓ — Reprogramar una clase era una cancelación gratis

Facu pidió auditar si `astronomy-members` cobraba las reprogramaciones hechas con menos de
12hs. **La regla no existía.** No había ni una línea que comparara el momento de la
reprogramación contra el horario original de la clase.

**Causa raíz: `rescheduleSlot` (`app/actions/availability.ts`) sólo miraba el horario
DESTINO.** Validaba que el nuevo horario respetara las 12hs de anticipación y después hacía
`update({ starts_at })`. El horario original —el que el profe tenía bloqueado— no se leía
para decidir nada, sólo para armar el mail.

Eso convertía la regla de cancelación de 24hs en **opcional**, en dos clics:

1. Clase mañana 10:00, ahora son las 21:00 → faltan 13hs, adentro de la ventana de 24hs.
   Cancelar ahí cuesta los créditos y el profe cobra.
2. En vez de cancelar, **reprogramar a +3 días**: pasa el chequeo del destino, gratis.
3. Ahora faltan 72hs → **cancelar** → `refunded = true` → créditos devueltos y `devenga()`
   deja al profe en cero.

El alumno recuperaba todo y el profe perdía la hora que ya había bloqueado sin poder
agendar otra cosa. **Y no se podía ni medir**: `starts_at` se pisaba in-place, sin columna
de rastro, así que no existía forma de saber cuántas veces había pasado.

**El patrón, que es lo que se transfiere:** una regla de negocio implementada en tres server
actions distintas —reservar, cancelar, reprogramar— donde cada una chequeaba *una parte*.
Ninguna estaba mal por sí sola; el agujero estaba en el hueco entre las tres. Una regla
repartida entre N funciones no es una regla, es N reglas parecidas que van a divergir.

**Fix:** las dos reglas se mudaron a `lib/reglasClase.ts`, puras y sin acceso a base — que es
lo que permitió escribirles 22 tests que corren sin red (`npm run test:reglas`). Una
reprogramación tardía ahora **cierra la reserva vieja cobrada** (`refunded = false`, que es
justo lo que `devenga()` ya leía para pagarle al profe) **y abre una nueva que se cobra
aparte**. Se agregaron `original_starts_at`, `rescheduled_at`, `reschedule_count` y
`rescheduled_from` a `slot_bookings`, más la vista `v_reprogramaciones_mes` — porque una
regla que no se puede contar no se puede verificar (Ley 9).

**Lo que faltó y quedó anotado:** `bookSlot` toma el **precio** de un `<input type="hidden">`
del formulario y se lo pasa a `spend_credits` sin validarlo contra el catálogo. Un POST con
`cost=0` reserva una clase sin gastar créditos. Se detectó siguiendo este flujo, no se tocó
(fuera del alcance pedido), y está sin arreglar.

### 2026-08-04 · FAIL ✓ — El timeline de leads mostraba las 16:24 como "04:24"

Primera corrida del monitoreo de `lead_events` (`scripts/verificar-leads.mjs`), el mismo día
que se instrumentó el Tracker. El log decía que el último evento había entrado a las
**04:24:37**. En la base estaba guardado como `19:24:37Z` — o sea las **16:24** de acá.

**Causa raíz: el locale `es-AR` devuelve formato de 12 horas.** Y `toLocaleString("es-AR")`
sin opciones **ni siquiera agrega el meridiano**:

```js
new Date("2026-08-04T19:24:37Z").toLocaleString("es-AR")
// "4/8/2026, 04:24:37"        ← ambiguo: ¿4 de la mañana o 4 de la tarde?
new Date(...).toLocaleString("es-AR", { hour12: false })
// "4/8/2026, 16:24:37"        ← lo que hay que escribir
```

Dónde pegaba, de peor a mejor:

| Dónde | Mostraba | Por qué importa |
|---|---|---|
| Log del verificador | `04:24:37` | **Dato falso.** Un monitoreo que miente en la hora no sirve para nada |
| Pie de `/admin/growth` | `04:24 p. m. hs` | La palabra "hs" promete 24 h y el valor es de 12. Venía de antes |
| Timeline de `/admin/leads` | `04:24 p. m.` | La columna está dimensionada para `16:24`. En una lista cuyo sentido es leer la secuencia de horas de un vistazo, el meridiano en cada línea es el ruido que la vuelve ilegible |

**Lo que lo hace fácil de repetir:** escribir `hour: "2-digit"` se siente completo. Nadie
agrega `hour12: false` porque en castellano uno *asume* 24 horas — y el asumido es
justamente el que no se cumple. En este repo hay **~17 lugares más** con el mismo patrón
(agenda, reservas, recordatorios); ahí el meridiano al menos se muestra, así que son feos
pero no ambiguos. **El peligroso es `toLocaleString` sin opciones de hora**, que se come el
meridiano.

**La lección que se lleva:** una hora sin `hour12` explícito es un bug esperando el turno.
Si el texto de al lado dice "hs", ya es un bug.

**Y el meta-aprendizaje, que vale más:** esto no lo encontró una revisión de código ni un
test. Lo encontró **la primera corrida de un verificador mirando datos reales**. La primera
corrida de cualquier monitoreo es la más valiosa que va a tener — es la única que compara el
sistema contra la realidad sin que nadie haya ajustado nada todavía.

### 2026-08-04 · FAIL ✓ — Cada evento de navegación entraba a la base y devolvía un 500

Instrumentando el rastro de navegación de `astronomy-members` (tabla `lead_events`,
`app/api/track/route.ts`), el endpoint de ingesta escribía la fila **perfecta** y devolvía
**HTTP 500**. Las dos cosas a la vez, en todos los casos: los válidos, los rechazados y los
inválidos.

**Causa raíz: `NextResponse.json(null, { status: 204 })`.** Un 204 significa "recibido, no
hay nada que devolver" y **no puede llevar cuerpo**; `json()` siempre arma uno. El
constructor de `Response` tira `TypeError: Invalid response status code 204`, y como el
`return` estaba adentro del `try`, el error caía en el `catch`… que devolvía **el mismo 204
imposible**. El catch reproducía el bug que intentaba contener.

```ts
return NextResponse.json(null, { status: 204 });   // ✗ TypeError → 500
const sinContenido = () => new NextResponse(null, { status: 204 });  // ✓
```

**Por qué se iba a descubrir tarde, o nunca:** el cliente que manda estos eventos ignora la
respuesta a propósito (un error de tracking no puede romperle la navegación a alguien que
está por comprar). Los datos llegaban bien, la pantalla mostraba todo, y lo único roto era
un 500 por visita en los logs de Vercel — el lugar exacto donde nadie mira hasta que hay
otro incendio.

**Lo que lo hizo visible: probar el endpoint mirando el código de estado, no el resultado.**
La verificación "¿se guardó la fila?" daba verde. Sólo mirar los dos —`204` **y** la fila—
mostró la contradicción.

**La lección, que ya estaba escrita en este mismo repo:** `app/api/header/route.ts` tiene el
comentario *"un 204 no puede llevar cuerpo y el cliente espera JSON"*, de una sesión
anterior. **El conocimiento existía a dos carpetas de distancia y se volvió a pagar igual.**
Un archivo nuevo no hereda los comentarios del viejo: si la restricción vale para todas las
rutas, va en un helper compartido, no en un comentario.

### 2026-08-04 · FAIL ✓ — Las alarmas de `astronomy-members` nunca le llegaron a Facu

Construyendo la alarma de "hace días que nadie carga plata" apareció esto: **la cuenta de
Facu (`facue1900@gmail.com`) no tiene fila en la tabla `staff`.** Es maestro por la variable
de entorno `ADMIN_EMAILS` (`lib/staff.ts` → `isMasterByEnv`): entra al panel con todos los
permisos y **no existe como registro**.

Las cinco alarmas del cron armaban su lista de destinatarios así:

```ts
const { data: staff } = await admin.from("staff").select("user_id, permissions, is_master");
for (const st of staff) { if (st.is_master || st.permissions.includes("view_payments")) notify(...) }
```

**Causa raíz: el código asume que todo maestro tiene fila en `staff`, y uno no la tiene.**
Las campanitas de *"Mercado Pago cobró y no nos avisó"* y *"el puente acreditó"* le llegaban
a `vladimir.nadinic@gmail.com` (maestro con fila) y a quien tuviera `view_payments` — nunca
a la cuenta personal de Facu.

**Lo que lo hace peor que un bug suelto: el arreglo ya existía.** `notifyVencidos()` resolvía
los mails de `ADMIN_EMAILS` con el RPC `user_id_by_email` y agregaba los uuid a mano. Estaba
escrito ahí adentro, y **ninguna de las otras cuatro funciones se enteró**. Es el costo exacto
de tener la misma respuesta escrita cinco veces (regla 12): se arregla en una y las otras
cuatro siguen mintiendo, sin que nada las contradiga.

**Fix:** `lib/destinatarios.ts` → `destinatariosDeAviso(admin)`, único lugar que contesta "¿a
quién le avisamos?". Devuelve las filas de `staff` más los maestros por env resueltos a uuid.
Los cinco bucles la usan; ya no queda ningún `from("staff")` a mano en `lib/payments.ts`.
Verificado contra la base: **7 destinatarios, y `facue1900@gmail.com` aparece con su uuid.
Antes eran 6 y él no estaba.**

**La lección, y es la regla final de la Constitución:** un aviso que no llega no se distingue
de "no pasó nada". Al escribir cualquier alerta nueva, la pregunta no es "¿avisa?" sino
**"¿a quién, y esa lista incluye a la persona que puede hacer algo?"**. Y una alarma se
prueba mirando a quién le llegó, no viendo que la función no tiró error.

**Bonus del mismo día, misma clase de falla:** la racha de la alarma nueva contaba huecos
viejos sin preguntar si hoy ya estaba cubierto, así que reportaba *"hace más de 60 días que
no se carga nada"* de los ingresos que Luqui había cargado **esa misma mañana**. Sólo se vio
corriéndola de verdad contra la base — `tsc` y `build` estaban limpios.

### 2026-08-04 · FAIL ✓ — La auditoría de créditos acusaba de deudores a los que habían pagado

El panel `/admin/auditoria-creditos` listaba tres alumnos bajo *"Reservaron más de lo que
pagaron"* —Fernando Lopez Peña, Guadalupe Merke, Maximiliano Aguirre— y en la **misma
fila** la columna Dif. decía `✓`. Las dos cosas no pueden ser ciertas a la vez, y ésa fue
la pista.

**Causa raíz: el chequeo comparaba las clases del ciclo contra `otorga` a secas**, o sea
los créditos que da el plan del último cobro y nada más. Todo lo que entró por otra puerta
quedaba afuera del denominador: compras sueltas de créditos, premios, reintegros por
cancelación y el saldo arrastrado del ciclo anterior. Fernando había **comprado 60
créditos** el 31/07; Guadalupe, **240 comprados más 60 de premios**. Eran clientes al día,
y el sistema los mandaba a la lista de los que hay que llamar.

**Lo que lo vuelve estructural y no un off-by-one:** reservar una clase DESCUENTA créditos,
y `spend_credits` rechaza la reserva si el saldo no alcanza (verificado en los cuatro
caminos de reserva, incluida la carga manual del admin, que además revierte). **Una clase
agendada sin créditos atrás no puede existir.** El chequeo, tal como estaba escrito, sólo
podía producir falsos positivos — nueve el primer día que se midió.

**El costo real de un chequeo que grita de más:** deja de mirarse. Y mientras tanto tapa el
caso inverso, que sí importa — un alumno con premios al que ADEMÁS le faltan créditos del
plan: las dos diferencias se cancelan y queda invisible.

**El fix:** el denominador pasó a ser todo lo que el alumno recibió y podía gastar en la
ventana del ciclo, contado por `amount_granted` de los lotes (no por lo que le queda: un
lote gastado entero está en 0 justamente porque se usó en las clases que estamos contando).
Los cuatro casos que había pasaron a 0. Lo que antes salía en rojo como deuda ahora sale en
gris como dato: *"usó 40 créditos de fuera del plan"*. Y el bloque se renombró a **"Clases
sin créditos que las cubran"**, con el texto diciendo que si aparece alguien ahí es una
anomalía real y hay que ir a mirar su historial, no corregirle el saldo.

**La lección transferible:** cuando una pantalla afirma dos cosas contradictorias sobre la
misma fila, el bug no está en la que se ve mal — está en que dos cálculos distintos usan
denominadores distintos para la misma pregunta.

### 2026-07-29 · FAIL ✓ — Un token vencido borró el manifiesto de creativos, porque el script escribía pase lo que pase

Facu dio el OK para subir las 75 placas nuevas a Meta. `subir_creativos.py` intentó las 75,
las 75 fallaron con `OAuthException code 190, subcode 460` —"the session has been
invalidated because the user changed their password"— y al terminar **escribió el
manifiesto igual**, dejando `data/pauta/creativos.json` en `{}`. Los hashes de los
creativos que estaban corriendo se perdieron. `data/` está gitignoreado: no hay historia
de dónde recuperarlos.

**Causa raíz: el script trataba "no subí nada" como un resultado válido.** Construía
`manifiesto = {}`, lo llenaba con lo que salía bien, y escribía el diccionario al final
sin preguntarse si tenía algo adentro. Es el modo de falla del global —*un resultado vacío
es un error hasta que se demuestre lo contrario*— pero del lado de la escritura, que es
donde duele: no reportó un total falso, destruyó el dato bueno.

Segundo error, más barato: reintentó 74 veces un error de autenticación. Un token vencido
no mejora en el intento 75.

**Arreglos:**

- El manifiesto **se mezcla** con el que ya está en disco, no lo reemplaza.
- Si `manifiesto == previo` (no subió nada nuevo), sale con error y **no escribe**.
- Un `code == 190` corta la corrida en la primera pieza, con el mensaje de qué hacer.
- `--send`, apagado por defecto, como manda la regla del repo. No lo tenía y escribía en
  la cuenta de Meta igual.

**Costo real: cero.** Los hashes viejos apuntaban a las placas viejas, que justamente
íbamos a reemplazar. Y son recuperables: las imágenes siguen en la biblioteca de la cuenta
y el anuncio que corre guarda su creativo del lado de Meta —nuestro JSON es solo un índice
local—, así que con un token válido salen de
`GET /{ad_id}?fields=creative{object_story_spec}`. El anuncio en producción no se tocó.

**Pendiente de Facu:** generar un `META_ACCESS_TOKEN` nuevo (cambió la contraseña de
Facebook) y ponerlo en el `.env`. Hasta entonces no se puede subir nada ni crear el
carrusel.

### 2026-07-29 · FAIL ✓ — El carrusel que pagamos tenía la misma foto cuatro veces, y el gancho no estaba en la imagen

Facu vio el anuncio de Modo Profesional corriendo en su propio Instagram, le sacó cinco
capturas y dijo: la primera no tiene texto que capte la atención, y la foto de fondo se
repite mucho. Las dos cosas eran ciertas y las dos venían del generador, no del diseño.

**Causa raíz 1: `foto` era un campo del PRODUCTO, no del ángulo.** En `academy.json` cada
producto declaraba una sola foto y los cinco ángulos la heredaban. Sobre la grilla de
Instagram no molesta —las piezas se publican de a una, con semanas de por medio— pero un
carrusel muestra las cinco juntas y ahí cuatro tarjetas idénticas se leen como que la app
no cargó bien la imagen. El quinto ángulo (`beneficios`, el de bullets) tenía
`fondo: "negro"`, y como el texto va anclado abajo, quedaba con el 45% superior del cuadro
vacío. O sea: de cinco tarjetas, cuatro repetidas y una vacía.

**Causa raíz 2: el mejor gancho estaba escrito, pero en el lugar donde nadie lo lee.** El
texto del anuncio abría con "Mezclás hace dos años. Nunca tocaste para nadie." — una línea
que funciona. La tarjeta 1 decía "DE TU DIAGNÓSTICO ARTÍSTICO A TU SHOWCASE": jerga
interna, seis palabras antes de que signifique algo, y en cuerpo chico sobre una foto
oscura. En un carrusel la tarjeta 1 es lo único que decide si alguien desliza. El gancho
estaba en el pie de foto y la jerga en la imagen: al revés.

**Causa raíz 3 (la que no se veía hasta arreglar las otras dos):** el velo era un solo
gradiente vertical. `dj-bw.jpg` tiene un saco beige claro justo en el tercio inferior
izquierdo, que es exactamente donde el sistema ancla el titular. "EL CURSO PARA / EL QUE
YA" caía encima del saco y se perdía.

**Los arreglos, todos en el generador y no a mano sobre los PNG:**

- `foto` ahora es por ángulo (`foto_del_angulo()`), con el del producto como fallback.
- **`chequear_fotos()` revienta la corrida si una foto se repite dentro de un producto.**
  Es el chequeo que faltaba: a ojo ya se pasó una vez, y una tanda son 75 piezas.
- Se importaron 9 fotos nuevas de `Fotos nuevas (Drive)`, elegidas midiendo la luminancia
  media de la zona donde cae el titular (esquina inferior izquierda, con el mismo
  `grayscale/brightness` que aplica el CSS). Sirve para descartar antes de renderizar:
  las cuatro fotos diurnas del exterior daban L=80–120 y no aguantan texto blanco.
- El velo pasó a dos capas: la horizontal oscurece la columna izquierda y deja limpio el
  lado derecho de la foto. Más `text-shadow` sobre negro como seguro — no se ve, pero
  salva el titular cuando abajo pasa un reflejo.
- `escala: "xl"` para el titular de apertura (7.2rem, 11ch, sin bloque).
- Ninguna tarjeta queda 100% negra: las densas van sobre foto muy oscura (L≤25).
- En `crear_carrusel.py`, `titulares` pasó de lista posicional a diccionario por ángulo.
  Con la lista, cambiar `ORDEN` dejaba cada titular sobre la imagen equivocada **sin que
  nada fallara** — el bug perfecto: silencioso y pago.
- `ORDEN` nuevo: gancho → cómo funciona → qué incluye → quién enseña → contacto. Los
  bullets pasaron de la posición 2 a la 3: la tarjeta 2 todavía tiene que hacer que el
  otro siga deslizando, y una lista no hace eso.

75/75 piezas OK, los estilos `foto` y `plano` intactos, 24 tests verdes.

**La lección transferible:** un chequeo que solo mira una pieza por vez no ve los defectos
que aparecen cuando las piezas se muestran juntas. El verificador del skill revisaba
dimensiones, peso y desborde de cada PNG por separado — y las 75 pasaban. El defecto vivía
en la *relación* entre cinco de ellas. Cuando el entregable es un conjunto, hay que
verificar el conjunto.

**Lo que queda abierto:** las placas nuevas están en disco pero **el anuncio que corre
sigue con los hashes viejos**. Hay que volver a subirlas con `subir_creativos.py` y crear
el carrusel nuevo. Y `subir_creativos.py` **no tiene flag `--send`** aunque escribe en la
cuenta de Meta, contra la regla del repo.

### 2026-07-29 · FAIL ✓ — Pushear a `main` nunca deployó astronomyofficial.com, y verifiqué con un hash que cambia solo

Terminé tres arreglos de `/admin/registro`, commiteé, Facu dijo "dale pushea", pusheé. Y me
quedé mirando producción esperando el deploy que nunca llegó.

**Dos errores encadenados, uno mío y uno del proyecto.**

**El error del proyecto (la causa real):** el proyecto `astronomy` de Vercel tiene
**`link: null`** — ningún repositorio de GitHub conectado. Pushear a `main` no deploya nada,
ni hoy ni nunca. Lo que confundía era el dashboard: los deploys aparecen con hash de commit y
rama `main`, idénticos a un deploy por push. **No lo eran.** Cuando corrés `vercel` desde una
carpeta con git, el CLI le adjunta los metadatos del commit local al deployment. Todos los
deploys de este proyecto salieron del CLI y ninguno de un push. Se ve así:

```bash
curl -s -H "Authorization: Bearer $T" \
  "https://api.vercel.com/v9/projects/$PID?teamId=$TID" | jq .link
# null  →  no hay git conectado, pushear no deploya
```

**El error mío (peor, porque es de método):** para chequear si el build nuevo estaba vivo,
busqué el chunk de JS que sólo existía con mi código (`grep -rl "No hay pagos que coincidan"
.next/static/chunks/`) y lo pedí contra producción. Daba 404, y lo reporté como prueba de que
el deploy no había salido. **Los nombres de chunk de Turbopack no son deterministas.** Borré
`.next`, recompilé el mismo código sin tocar una coma, y el chunk pasó de `1e3yovzzwil0u.js` a
`2uf5e7mogwn_6.js`. El 404 no probaba nada: probaba que dos builds distintos nombran distinto.

Sobre esa sonda inventé una hipótesis entera ("el webhook de GitHub no llega"), pusheé un
commit vacío para forzarlo, y esperé otros seis minutos a que pasara algo que no podía pasar.
Ese commit quedó en el historial con un mensaje que hoy sabemos falso.

Lo que sí valía era la evidencia del lado del servidor: `vercel ls` no mostraba **ningún
deployment nuevo** después de los dos pushes. Eso no dependía de ningún hash mío.

**El fix:** `npx vercel --prod` desde la carpeta. Y la verificación buena es preguntarle a
Vercel **a qué deployment resuelve el dominio**, no adivinarlo desde afuera:

```bash
curl -s -H "Authorization: Bearer $T" \
  "https://api.vercel.com/v13/deployments/astronomyofficial.com?teamId=$TID" | jq '.url, .meta.githubCommitSha'
```

**Cerrado el mismo día:** conectar el repo requería primero una **Login Connection con GitHub**
en la cuenta de Vercel — Facu había entrado con mail, así que la API devolvía
`You need to add a Login Connection to your GitHub account first`. Lo conectó, linkeé el repo
por API, y lo probé con un push de prueba: `BUILDING` a los segundos, `READY` en ~60s, dominio
resolviendo al deployment nuevo. **Ahora pushear a `main` sí deploya.**

El campo que distingue un deploy por push de uno del CLI es `meta.githubDeployment` en la API:
`1` = vino de un push, ausente = lo corrió alguien a mano. Es el único lugar donde se ven
distintos; en el dashboard son idénticos.

**La próxima:** verificar contra algo que el sistema **promete** que es estable —un id de
deployment, un commit sha, una respuesta de la API del proveedor— y nunca contra un artefacto
del build. Un hash de compilación no es una identidad: es una consecuencia. Y el corolario que
ya me mordió dos veces en dos días (ver la nota de Chrome headless a 500px): **antes de
construir una hipótesis sobre una medición, verificar que la medición mida lo que creo.**

### 2026-07-28 · FAIL ✓ — El cron que llevaba 197 corridas "exitosas" sin completar una sola respuesta

Arrancamos la sesión con un diagnóstico heredado: *"`sync-sheet` existe pero no lo dispara
nadie"*. La evidencia parecía sólida — `vercel.json` sólo programa `expire-group-invites` y
`send-reminders`, no hay GitHub Actions, no hay launchd. De ahí salía la conclusión de que por
eso Luki seguía cargando pagos a mano.

**Era falso, y las dos mitades estaban mal.**

**Primero:** el scheduler existía, en el único lugar donde no se había mirado — **pg_cron de
Supabase**, configurado por `supabase/pg_cron.local.sql` (gitignoreado, por eso no aparecía en
ninguna búsqueda del repo). `active = true`, `0 * * * *`, 197 corridas desde el 20/07. No
encontrar el scheduler donde uno lo espera no prueba que no haya scheduler.

**Segundo, y peor:** las 197 corridas figuraban como `succeeded` en `cron.job_run_details` y
**las 197 respuestas HTTP habían muerto por timeout**. `pg_net` corta a los 5000 ms por defecto
y el endpoint tarda ~20 s. `succeeded` ahí sólo significa que el pedido se **encoló**; el
resultado real vive en `net._http_response`, donde había 6 filas de `status_code = null` con
`error_msg = "Timeout of 5000 ms reached"` alternadas con los 200 del otro job.

Y sin embargo la planilla estaba al día. **Andaba de casualidad:** Vercel sigue ejecutando la
función después de que el cliente se desconecta. El trabajo se hacía, la respuesta se perdía, y
nadie podía distinguir una corrida sana de una rota.

**Lo que lo cerró** fue una fuente que no era ninguna de las dos: el **historial de revisiones
de Google Drive** de la planilla. 37 de 38 escrituras en el minuto 0 de cada hora, firmadas por
la service account. Eso probó que sí completaba, cosa que ni los logs de Vercel ni pg_cron
podían decir.

**Fix:** `timeout_milliseconds := 120000` en los dos `net.http_get`. Verificado disparando el
pedido de verdad — `net._http_response` id 494 volvió `200` con el cuerpo entero. Ojo con un
detalle que cuesta media hora: **pg_net encola y sólo despacha cuando commitea la transacción**,
así que un `pg_sleep()` en la misma query nunca ve su propia respuesta. Hay que disparar en una
transacción y consultar en otra.

**El hallazgo de plata que apareció en el camino:** `sales` mezcla dos orígenes sin deduplicar
—14 filas del webhook de MP y 34 importadas de la planilla con `mp_payment_id` = `sheet:…`— y
**6 cobros están contados dos veces: $861.120, un 13,2% de facturación inflada**. Se validó por
dos caminos independientes que dieron el mismo número: cruzar la planilla de Luki contra `sales`,
y buscar pares dentro de `sales`. Los créditos no se duplicaron.

**La próxima:** antes de creerle al estado verde de una tarea programada, buscar dónde queda
registrado el **resultado** y no el **despacho**. Y cuando dos análisis distintos tienen que dar
el mismo número, correr los dos: acá el acuerdo exacto en $861.120 fue lo que convirtió una
sospecha en un dato.

### 2026-07-28 · FAIL ✓ — Chrome headless renderiza mínimo a 500px y después recorta: inventé un bug de mobile que no existía

Sacando la vista previa del salón de premios, la captura a `--window-size=390,1500` mostraba
todo cortado a la derecha: nombres partidos, el texto de la nota tajeado. Diagnostiqué
desborde horizontal, encontré una causa plausible —la trampa ya documentada de `min-width:auto`
en items de grid— y **edité `ui.css` para arreglarlo**. La captura de después seguía cortada.

**La causa real:** Chrome headless tiene un **ancho de ventana mínimo de ~500px**. Pide 390 y
lo que hace es maquetar a 500 y **recortar la imagen** a 390. Todo lo que caía entre 390 y 500
desaparecía de la foto sin desaparecer del layout. El `--window-size` no controla el viewport
CSS por debajo de ese piso, sólo el encuadre.

Lo delató inyectar un script que imprimiera `document.documentElement.clientWidth`: decía
**500**, no 390. Y `DESBORDAN=0`. Después revertí `ui.css` y medí de nuevo: también 0. **No
había bug.** El parche llevaba 20 minutos de trabajo sobre un fantasma.

`--headless=new` no lo arregla: la imagen sale de 780px (390×2) pero el layout se sigue
haciendo a 500. `--dump-dom` es peor todavía, ignora el `--window-size` por completo.

**La próxima:** Para medir anchos de teléfono de verdad, **embeber la página en un `<iframe>`
del ancho buscado**, servido desde el mismo origen (un HTML en `public/`). El iframe crea su
propio viewport, las media queries responden al ancho real y desde el padre se puede leer el
`clientWidth` y el `scrollWidth` del hijo. Y la regla de fondo: **antes de arreglar algo que
viste en un screenshot, verificá que el screenshot mida lo que creés.** Un artefacto de
captura se parece muchísimo a una regresión.

### 2026-07-27 · FAIL ✓ — El conector de Drive (read_file_content) devolvió la pestaña…

El conector de Drive (`read_file_content`) devolvió la pestaña Movimientos del Master Plan cortada en 206 de 455 filas, **sin error ni aviso**. Los totales daban más chicos y plausibles.

**La próxima:** Bajar siempre el export `.xlsx` completo. Un resultado uniformemente vacío o corto es un error hasta que se demuestre lo contrario: contar las filas antes de confiar en un total.

### 2026-07-27 · FAIL ✓ — radar_rampa.py calculaba piso = SOLO_EXPENSAS.get(local, 0) if desde…

`radar_rampa.py` calculaba `piso = SOLO_EXPENSAS.get(local, 0) if desde > hoy else 0` dentro de la rama donde `desde <= hoy`: la condición estaba muerta y el piso daba **0 fijo**. Un local que pagaba solo expensas (Peak One, $1,71M) podía cruzar el umbral de medio alquiler y figurar "al día" sin haber pagado un peso de alquiler.

**La próxima:** Fix: descontar las expensas siempre — el local las paga *además* del alquiler. Toda condición que compara con la variable que ya filtró el `continue` de arriba es sospechosa.

### 2026-07-27 · LEARN — Los cargos bancarios chicos del Macro (SIRCREB, Ley 25.413,…

Los cargos bancarios chicos del Macro (SIRCREB, Ley 25.413, comisiones) cargados uno por uno hacían ruido en Movimientos. Agrupados en una línea mensual cada uno, junio 2026 concilió al centavo.

**La próxima:** El criterio de agrupado está verificado contra un mes que cerró exacto. El neto se controla contra el extracto **crudo**, nunca contra el agrupado.

### 2026-07-27 · LEARN — El extracto del Macro no separa débito de crédito por columna de…

El extracto del Macro no separa débito de crédito por columna de forma confiable.

**La próxima:** Deducir el signo de cómo se movió el saldo línea a línea, arrancando de "SALDO ULTIMO EXTRACTO".

### 2026-07-27 · LEARN — El Dashboard Mensual matchea ingresos por Local y egresos por…

El Dashboard Mensual matchea ingresos por **Local** y egresos por **Categoría**, con SUMIFS sensible a acentos y espacios. Un local mal escrito no tira error: suma cero y el mes queda desfasado en silencio.

**La próxima:** Chequeo de categorías huérfanas en todo cierre. "Apex" → "Peak One" fue exactamente esto.

### 2026-07-27 · FAIL ✓ — Traté a Nordelta Plaza como si fuera una unidad de Paseo Nordelta y…

Traté a **Nordelta Plaza** como si fuera una unidad de **Paseo Nordelta** y le atribuí la sociedad NDPL SAS al Paseo. Son dos negocios distintos: otra sociedad, otros socios (Jero Gallo, Tino/Noreventos, Las Carolas), otro banco (BBVA vs Macro). Facu lo corrigió.

**La próxima:** Que compartan la palabra "Nordelta" y estén en carpetas vecinas del Desktop no los hace el mismo negocio. Antes de fusionar dos fuentes, verificar CUIT/sociedad/banco. Separados en `active/paseo-nordelta/` y `active/nordelta-plaza/`.

### 2026-07-27 · FAIL — Las dos "tareas automáticas" que el MEMORIA de Paseo daba por…

Las dos "tareas automáticas" que el MEMORIA de Paseo daba por creadas (conciliación día 10 9am, sync aportes diaria 7am) **no existen**: `RemoteTrigger list` devolvió cero routines. Estuvieron meses documentadas como activas sin correr nunca.

**La próxima:** Persist-or-it-didn't-happen: una automatización que no deja archivo ni corrida verificable no existe. Nunca anotar una tarea como "creada" sin listarla después.

### 2026-07-27 · LEARN — No hay node, npm, brew ni CLI claude en la Mac, y Python es el 3.9…

No hay `node`, `npm`, `brew` ni CLI `claude` en la Mac, y Python es el 3.9 del sistema sin `requests`. Toda la automatización local (launchd + claude headless) está bloqueada hoy.

**La próxima:** Las routines cloud son la única vía automática disponible, y **no ven el Desktop**. Lo que necesite archivos locales tiene que subir a Drive primero.

### 2026-07-27 · FAIL ✓ — claude no arrancaba desde la terminal ("no está instalado")

`claude` no arrancaba desde la terminal ("no está instalado"). Estaba instalado y funcionando (v2.1.220 en `~/.local/node/bin/claude`): el `export PATH` se había escrito **solo en `~/.zshrc`**, pero el shell de login de la Mac es `/bin/bash`, que nunca lo lee. Nada fallaba con error — el comando simplemente no existía.

**La próxima:** Fix: PATH y alias movidos a `~/.profile`, con `~/.bashrc` sourceándolo para shells no-login (terminal de VSCode). Antes de escribir en un rc, chequear el shell real con `dscl . -read ~ UserShell` — no asumir zsh porque es el default de macOS. Verificar con `env -i HOME=$HOME /bin/bash -lc 'which X'`, no en la shell que ya tenés abierta.

### 2026-07-27 · LEARN — Las cuatro copias de MEMORIA - Paseo Nordelta en el Desktop…

Las cuatro copias de `MEMORIA - Paseo Nordelta` en el Desktop divergieron entre sí; ninguna decía cuál era la buena.

**La próxima:** Una sola fuente por tema. El estado vive en la memoria de Claude Code y en `active/`, no en copias sueltas con `copy` en el nombre.

### 2026-07-27 · FAIL ✓ — gemini.py devolvía un genai.Client nuevo en cada llamada

`gemini.py` devolvía un `genai.Client` nuevo en cada llamada. Como `models.list()` es un pager perezoso, el cliente temporal se recolectaba antes de que saliera el request y httpx tiraba `RuntimeError: Cannot send a request, as the client has been closed` — un error que no menciona ni la key, ni la red, ni el modelo, y manda a debuggear para el lado equivocado.

**La próxima:** Fix: `_CLIENTE` singleton de módulo. Un cliente HTTP creado inline y usado con una API perezosa se muere antes del request. Además `.strip()` en la key: un espacio pegado al `=` del `.env` viaja hasta el header de auth.

### 2026-07-27 · FAIL ✓ — GEMINI_MODEL=gemini-2.5-flash daba 404 "no longer available to new…

`GEMINI_MODEL=gemini-2.5-flash` daba 404 `"no longer available to new users"` **aunque el modelo figura en `--modelos`**. La lista de la API incluye modelos que la key no puede invocar. También, en el free tier, `gemini-2.0-*` y `gemini-2.5-pro` dan 429 por cuota.

**La próxima:** `models.list()` no es prueba de que un modelo sirva: probarlo con un `generate_content` real antes de fijarlo. Sondeados 7 candidatos, andan `gemini-flash-latest` y `gemini-flash-lite-latest`. Quedó `gemini-flash-latest`.

### 2026-07-27 · FAIL ✓ — El chequeo "cero modelos es error" de listar_modelos() medía antes…

El chequeo "cero modelos es error" de `listar_modelos()` medía **antes** del filtro de `generateContent`: si la API devolvía modelos pero ninguno servía para generar, el script imprimía cero líneas y salía con código 0. Un chequeo escrito para cazar el silencio que dejaba pasar el silencio. Lo encontró `code-reviewer`, no yo — yo escribí el chequeo y lo di por bueno.

**La próxima:** Contar lo que se **imprime**, no lo que devuelve la fuente. La regla del resultado vacío se aplica al final del pipeline, no al principio. Y el workflow de correr `code-reviewer` sobre código propio se paga solo: el que lo escribió no ve este tipo de error.

### 2026-07-27 · LEARN — Tres fixes más de la misma revisión de gemini.py

Tres fixes más de la misma revisión de `gemini.py`: (1) `except Exception` convertía un typo del script en "la API contestó" — acotado a `genai_errors.APIError` y `httpx.HTTPError`, verificado que toda la jerarquía real de errores de API y red cae ahí; (2) `r.text` puede venir `None` sin error (filtro de safety, respuesta cortada) y `leer_imagen()` lo devolvía tal cual, así que un skill podía guardar `None` como el dato extraído de una guía de SENASA — ahora `_texto()` revienta con el `finish_reason`; (3) `modelo()` no tenía el `.strip()` que sí tenía la key.

**La próxima:** Cuando se arregla un patrón (un `.strip()`, un chequeo de vacío), buscar el mismo patrón en todo el archivo. Arreglarlo en un solo lugar deja el bug vivo al lado.

### 2026-07-27 · LEARN — Los tests de gemini.py vivían en el scratchpad de la sesión, que se…

Los tests de `gemini.py` vivían en el scratchpad de la sesión, que se borra. Reportar "13 tests en verde" con los tests a punto de evaporarse es la misma trampa que las routines fantasma.

**La próxima:** Movidos a `execution/tests/`, con el path del repo calculado desde `__file__` en vez de hardcodeado. Un test que no está en el repo no existe.

### 2026-07-27 · FAIL ✓ — Al autorizar la SEGUNDA cuenta de Google, el flujo guardó…

Al autorizar la SEGUNDA cuenta de Google, el flujo guardó `token-facu.json` con las credenciales de **studio@astronomyofficial.com**. `run_local_server()` no pide `prompt`, así que Google reusó la sesión abierta y ni mostró el selector. No hubo ningún error: el token se guardó "bien", con el nombre de otra cuenta. Un `triage-inbox` pidiendo la cuenta `facu` habría ordenado el inbox equivocado y reportado éxito.

**La próxima:** Fix en dos partes: (1) `prompt="select_account"` fuerza el selector; (2) antes de guardar, `_cuenta_con_email()` chequea si ese mail ya está bajo otro nombre y **corta sin guardar**. Todo login que reusa sesión puede autenticar a quien no querés: el token no se da por bueno hasta preguntarle a la API **con qué identidad** quedó.

### 2026-07-27 · FAIL ✓ — Mi propio script de comparación reportó que studio NO llegaba al…

Mi propio script de comparación reportó que `studio` NO llegaba al Master Plan, contradiciendo una verificación mía de veinte minutos antes. La causa era el script, no los permisos: clasificaba las excepciones a mano (`"403" if "403" in str(e) else ... else "no"`) y el cajón "no" se tragaba el motivo real. Reportar esa tabla habría hecho configurar los skills con la cuenta equivocada.

**La próxima:** Cuando un resultado nuevo contradice uno ya verificado, el sospechoso es el medidor. Imprimir la excepción CRUDA antes de clasificarla; un `else` que resume errores desconocidos en una etiqueta corta es un lugar donde se pierde información.

### 2026-07-27 · FAIL ✓ — Obsidian "no estaba instalado" (/Applications/Obsidian.app no…

Obsidian "no estaba instalado" (`/Applications/Obsidian.app` no existía) pero estaba **corriendo**: se había abierto directo desde el `.dmg` de Downloads, y macOS lo ejecutaba translocado desde `/private/var/.../AppTranslocation/` — copia de solo lectura, sin updates y con config que no persiste. Nunca había registrado el vault (`obsidian.json` no existía).

**La próxima:** Instalado de verdad en `/Applications` y vault registrado con ID determinístico (`sha256(path)[:16]`) para que re-correr no duplique la entrada. Una app que corre desde `AppTranslocation` está a medio instalar: `pgrep -fl <app>` lo delata. Mismo patrón que el PATH: el síntoma decía "no existe", la causa era "existe pero mal ubicado".

### 2026-07-27 · LEARN — Revisión de las 27 skills de ~/Downloads/Claude Code Full Course/All…

Revisión de las 27 skills de `~/Downloads/Claude Code Full Course/All Of My Claude Skills/`. Son de una agencia de cold email: 18 dependen de servicios que Facu no tiene (Apify, PandaDoc, Instantly, Anymailfinder, Auphonic, TubeLab, Pinecone) o de negocios ajenos (Skool, Upwork, thumbnails de YouTube). Copiarlas todas habría metido 27 descripciones al auto-descubrimiento de skills para disparar dos.

**La próxima:** Se portaron dos: `triage-inbox` (de `gmail-label` + `gmail-inbox`) y `prospectar-gmaps` (de `gmaps-leads`, solo el scraper). Portar, no copiar: auth propia (`execution/google_auth.py` en vez del registry multi-cuenta), categorías por negocio de Facu, y `--send` apagado donde el original escribía directo. Un skill importado tal cual es deuda con nombre lindo.

### 2026-07-27 · FAIL ✓ — El gmail_label_merge.py original juntaba lo que clasificaba cada…

El `gmail_label_merge.py` original juntaba lo que clasificaba cada subagente **sin chequear cobertura**: si un subagente moría, sus mails quedaban sin etiquetar y el resumen igual decía "listo". El mismo modo de falla que el Drive truncado.

**La próxima:** `merge_labels.py` compara los IDs clasificados contra el `emails.json` original y **corta** si falta uno. Probado a propósito con un chunk faltante antes de darlo por bueno. Todo fan-out a subagentes necesita un chequeo de cobertura del lado del que junta.

### 2026-07-27 · LEARN — El pipeline de gmaps-leads (571 líneas) le pedía a Claude Haiku que…

El pipeline de `gmaps-leads` (571 líneas) le pedía a Claude Haiku que sacara "el email del dueño" scrapeando webs. Eso inventa datos con cara de dato verificado.

**La próxima:** En `prospectar-gmaps` sale solo lo que Google Maps publica (nombre, dirección, teléfono, web, rating) y nada más. Si un dato hay que adivinarlo, no es un dato.

### 2026-07-27 · FAIL ✓ — El subagente research tenía en su cuerpo la instrucción "escribí el…

El subagente `research` tenía en su cuerpo la instrucción "escribí el resultado en la ruta que te den", pero su frontmatter declaraba `tools: Read, Glob, Grep, WebSearch, WebFetch` — **sin `Write`**. Venía así del template del curso. Nunca había fallado ruidosamente: el agente investiga igual y devuelve texto, así que el hueco solo se nota cuando alguien espera el archivo y no está.

**La próxima:** Fix: `Write` agregado. Auditar los agentes es leer el frontmatter contra el cuerpo: si el cuerpo pide una herramienta que el frontmatter no da, el agente hace algo distinto de lo que dice hacer, y en silencio.

### 2026-07-27 · LEARN — Auditoría de los 6 subagentes del OS

Auditoría de los 6 subagentes del OS. `code-reviewer`, `qa` y `research` seguían en inglés y con el formato de salida del curso (PASS / NEEDS CHANGES): son justo los tres que el workflow de cambios no triviales manda correr, así que sus reportes volvían en otro idioma que el resto del OS. `clasificador-mails` corría en Sonnet para una tarea de clasificación pura, contra la regla del `CLAUDE.md` de mandar eso a Haiku.

**La próxima:** Los tres reescritos en español, con secciones obligatorias de "lo que no pude verificar/probar". `clasificador-mails` bajado a Haiku (con nota de cómo volver a Sonnet si confunde ámbitos). Un agente heredado de un template arrastra el idioma, el formato y el modelo de otro proyecto.

### 2026-07-27 · LEARN — Los skills nuevos arrancaron clavados a los cuatro negocios

Los skills nuevos arrancaron clavados a los cuatro negocios: las reglas de ámbito vivían dentro del agente `clasificador-mails`. Facu pidió que fueran generales.

**La próxima:** Los ámbitos se movieron a `.claude/skills/triage-inbox/contextos.json`, con `senales` y `no_confundir` por ámbito, y el merge **valida** contra ese archivo: un ámbito no declarado corta la corrida. Regla que queda: lo genérico va en el skill, lo específico en un JSON al lado. Un skill clavado a un negocio sirve para uno; parametrizado sirve para los cuatro.

### 2026-07-27 · LEARN — grabacion-a-tareas se probó end-to-end de verdad

`grabacion-a-tareas` se probó end-to-end de verdad: audio generado con `say` de macOS → Files API de Gemini → extracción. Sacó las 2 tareas con responsable y plazo, la decisión, el tema abierto y el monto, cada uno con su cita textual.

**La próxima:** Un extractor validado solo con JSON de mentira no está validado. `say -o x.aiff "..."` alcanza para fabricar un caso de prueba real sin depender de que aparezca una grabación. Los montos dichos en una grabación van a una tabla aparte marcada como **no verificados**: lo que alguien dice en una reunión no es un dato contable.

### 2026-07-27 · FAIL ✓ — La línea de estado nunca mostró el contexto usado

La línea de estado **nunca mostró el contexto usado**. Buscaba `context.used_tokens` / `context.percent_used`; el campo real que manda Claude Code (v2.1.220) es `context_window.used_percentage`. Como ninguna ruta matcheaba, caía en un `else` silencioso y la barra mostraba solo `proyecto \| modelo`. Un chequeo que no falló nunca desde que existe porque nunca corrió.

**La próxima:** Fix contra el payload real, que la propia statusline guarda en `/tmp/claude-statusline-payload.json`. Regla: un script que "prueba varias rutas antes de rendirse" necesita **fallar ruidosamente cuando ninguna pega**, o el fallback tapa el bug para siempre. Antes de escribir rutas defensivas, mirar un payload de verdad.

### 2026-07-27 · FAIL ✓ — El hook aviso-contexto.sh no imprimía nada

El hook `aviso-contexto.sh` no imprimía nada: usaba `python3 - <<'PY'` y leía el payload con `json.load(sys.stdin)` — pero el heredoc **ya ocupa stdin**, así que Python parseaba su propio código fuente como JSON. Con `2>/dev/null` encima, el error era invisible; y los casos de prueba "no debe imprimir nada" pasaban en verde por la razón equivocada.

**La próxima:** Fix: `payload=$(cat)` y pasarlo por `argv`, igual que `statusline.sh`. Un test cuyo criterio de éxito es "salida vacía" no distingue funciona-y-calla de está-roto: cada suite necesita al menos un caso que **exija** output.

### 2026-07-27 · FAIL ✓ — cierre-mes invocaba el python3 del sistema

Los pasos 1 y 2 de `cierre-mes-nordelta/SKILL.md` invocaban `python3` pelado (3.9, sin PyMuPDF ni openpyxl) → `ModuleNotFoundError` garantizado en el cierre. Era el único skill con el bug; el paso 2-bis del mismo archivo ya lo hacía bien. Además `triage-inbox` referenciaba un `token.json` que ya no existe (multi-cuenta lo partió en `token-facu.json`/`token-studio.json`) y `consenso` hacía `cd` a un directorio que nunca se creaba.

**La próxima:** cuando cambia una convención (venv, nombres de token, directorios), grepear TODOS los SKILL.md y scripts por la convención vieja en el mismo commit. Una referencia rota en un skill es un skill que falla recién cuando se lo necesita.

### 2026-07-27 · FAIL ✓ — conciliar.py v1: chequeo más permisivo que el sistema que replica

La primera versión de `conciliar.py` normalizaba categorías sacando tildes y colapsando espacios. El SUMIFS real del Dashboard es sensible a acentos y espacios: una categoría con tilde distinta queda FUERA del Dashboard en la vida real, y el chequeo la daba por buena → falso CIERRA sobre plata. Lo agarró el code-reviewer antes del primer uso real.

**La próxima:** un chequeo que replica el comportamiento de otro sistema (un SUMIFS, un matcher, un parser ajeno) tiene que ser EXACTAMENTE igual de estricto. Cada normalización "por las dudas" que el sistema real no hace es una clase de error que el chequeo deja de ver.

### 2026-07-27 · LEARN — Saldo Actual es histórico: descomponer antes de culpar al mes

`conciliar.py` encontró $0,69 de diferencia entre el extracto de junio y Saldo Actual. El agente `numeros` recalculó los 6 meses contra sus PDFs: junio cierra al centavo — la diferencia es de MARZO (fila 95 de Movimientos, "Tubomarket galeria" cargada $391.325,00 cuando el banco movió $391.324,31). Saldo Actual es un SUMIFS sobre todo el historial, así que arrastra errores viejos al presente. El script ahora descompone: cuánto viene arrastrado y cuánto es del mes.

**La próxima:** cuando un acumulado histórico no cierra, bisectar por período contra las fuentes antes de tocar nada del mes corriente. Y auditar con un agente independiente un script nuevo de plata ANTES del primer uso real: acá el auditor encontró además gastos VISA sin registrar ($4.887) y aportes de capital mezclados como ingresos en el Dashboard ($10,4M en junio).

### 2026-07-27 · FAIL ✓ — La memoria quedaba en el proyecto equivocado

La memoria de Claude Code se guarda según la carpeta desde donde se abre la sesión: 224 KB de memoria de los negocios (35 archivos, incluidas las reglas de membresías que el CLAUDE.md listaba como "hueco por completar") estaban repartidos entre el proyecto del Curso y el de Astronomy, y la memoria de facu-os estaba VACÍA. Unificada el 27/07/2026: 27 memorias + MEMORY.md en facu-os, crudos grandes en `archive/memoria-importada/`, orígenes vaciados tras verificar byte a byte.

**La próxima:** las sesiones de los negocios se abren SIEMPRE desde `~/facu-os` — es lo que decide dónde vive la memoria. Si una sesión se abrió desde otra carpeta y guardó memoria valiosa, migrarla en el momento.

### 2026-07-27 · LEARN — La política de modelos no rutea nada si no hay a quién delegar

El global declaraba "Haiku clasifica · Sonnet genera · Opus para plata" desde siempre, pero el hilo principal corre en Opus y **un skill no puede bajarse el modelo: no existe esa palanca en el frontmatter de `SKILL.md`**. El único ruteo real es delegar a un subagente con `model:` clavado. Resultado: los 6 subagentes estaban bien ruteados, pero todo el trabajo mecánico (leer archivos, extraer campos, escribir borradores) se lo comía Opus 1M porque no había ningún agente genérico a quien mandárselo — `clasificador-mails` estaba clavado a mails.

**El fix:** agentes `mecanico` (Haiku, trabajo de dedos) y `redactor` (Sonnet, texto para terceros), más la tabla de ruteo en `.claude/CLAUDE.md`. Regla que los sostiene: **lo que decide no se delega** — el `mecanico` trae datos, el hilo principal saca la conclusión.

**La próxima:** Una política sin mecanismo es un comentario. Antes de escribir una regla en un CLAUDE.md, preguntarse qué la ejecuta.

### 2026-07-27 · LEARN — Los subagentes nuevos no existen hasta reiniciar la sesión

Recién creado `.claude/agents/mecanico.md`, invocarlo devolvió `Agent type 'mecanico' not found`. El registro de agentes se arma **al arrancar la sesión**; escribir el archivo no lo registra en caliente.

**La próxima:** Un agente nuevo se prueba en la sesión siguiente, no en la que lo creó. El frontmatter sí se puede validar en el momento (`name` == nombre del archivo, `model` en haiku/sonnet/opus).

### 2026-07-28 · LEARN — Skill `flyers`: `--user-data-dir` cuelga al Chrome headless de macOS

Armando el generador de flyers de Academy, los 75 renders se colgaban a los 120s sin
escribir el PNG ni tirar error. Aislando flag por flag, el culpable era
`--user-data-dir` apuntando a un perfil nuevo en `/tmp`: se queda esperando para
siempre, ni siquiera con `--no-first-run --no-default-browser-check --disable-sync`.
Sin el flag anda, y cinco corridas en paralelo producen PNGs **byte a byte idénticos**
— o sea que compartir el perfil por defecto no genera contención.

De paso: **`timeout` no existe en macOS**, así que el primer intento de acotar el
render "colgado" no corrió Chrome en absoluto y dio un falso negativo. El corte tiene
que ir en el `subprocess.run(timeout=...)` de Python.

**La próxima:** cuando un subproceso se cuelga, bisectar los flags antes de tocar el
código. Y desconfiar de un test que "falla rápido": verificar que la herramienta que
usás para acotarlo exista (`command -v timeout`) — un 127 se lee igual que un fallo
real si no mirás el stderr.

### 2026-07-28 · LEARN — Un flyer con precio a mano es un precio que se desactualiza

Los precios de los flyers de Academy no se escriben en el JSON de contenido: los pisa
`sync_precios.py` leyendo la tabla `plans` de Supabase, la misma que lee el checkout.
Un flyer publicado con precio viejo lo compara el alumno contra Mercado Pago y no
coincide. Además el generador **revienta** si un ángulo de tipo `precio` se encuentra
con `precio_ars: null`, en vez de dibujar el precio en blanco.

Excepción registrada: `modo-profesional` tiene el precio hardcodeado en
`app/actions/buyCursoPro.ts` (`PRECIO_UNICO` $440.000 / `PRECIO_CUOTA` $250.000), no
en la base. Si cambia allá, hay que actualizarlo a mano en `contenido/academy.json`.

**La próxima:** todo número que sale a un tercero se sincroniza desde su fuente o el
script no corre. "Lo actualizo cuando cambie" es cómo se publica un precio viejo.

### 2026-07-28 · LEARN — La convención de pago de cada local cambia la deuda

El radar de deudores mostraba a Bigg debiendo $2,2M. Facu aclaró que Bigg **paga por adelantado** (el cargo del mes se paga en el mismo mes) y que dic'25 se pagó fuera del registro 2026 → deuda real: cero. Lo mismo con el Salón: un pago de $5M que parecía adelanto de expensas era la **penalidad de una inquilina saliente**. Los números estaban bien calculados; la interpretación estaba mal porque cada local tiene su convención (vencido/adelantado, efectivo/banco, redondeos).

**La próxima:** antes de reportar deuda de un local, confirmar su convención de pago con Facu. Las convenciones viven en `radar_deudores.py` (`REGLAS`, `PAGAN_ADELANTADO`, `PAGAN_POR_BANCO`) — un local nuevo se agrega ahí el día uno.

### 2026-07-28 · FAIL ✓ — CUENTA CORRIENTE solo suma conceptos que matchean sus SUMIFS

Cargué un cargo "Penalidad rescisión" en CARGOS y la CUENTA CORRIENTE lo ignoró en silencio: sus columnas suman por concepto con SUMIFS (`"Alquiler*"`, `"Servicios comunes"`, `"Recupero*"`) y un concepto nuevo no matchea ninguno. El saldo quedó $5M mal hasta que el radar lo delató. Fix: renombrar a "Alquiler - Penalidad rescisión" para entrar por el comodín.

**La próxima:** antes de inventar un concepto nuevo en una tabla que otra hoja consume por SUMIFS, leer las fórmulas del consumidor y usar un nombre que matchee. Y después de cada escritura al sheet, re-bajar y re-correr el reporte que lo lee: esa verificación fue la que agarró el error.

### 2026-07-28 · FAIL ✓ — Diseñé dos tandas contra la estética equivocada

Para los flyers de Academy inferí la estética de dos fuentes indirectas: los tokens
de la app (`--violet:#8b5cf6`, Montserrat, centrado) y el material viejo del Desktop
(PDFs de curso de 2023, portadas de The Bunker). Salieron 150 piezas. Ninguna se
parecía a la cuenta.

La grilla real de **@astronomy.academy** es un sistema editorial monocromo: negro
puro o foto muy desaturada, Helvetica Neue en MAYÚSCULAS **alineada a la izquierda
y anclada abajo**, micro-rótulos mono en las cuatro esquinas, cruces de registro,
logo de dos círculos, y el CTA como etiqueta entre corchetes. **Cero violeta, cero
botones, cero centrado.** El énfasis dentro de un titular se hace con peso, no con
color.

El `WebFetch` a instagram.com no sirvió: pega contra el muro de login y el modelo
chico que resume la página devolvió una descripción inventada ("rojos, naranjas y
azules") que contradecía todos los assets reales. Se descartó a tiempo por eso mismo
— por contradecir la fuente— pero el costo ya estaba pagado en las dos tandas.

**La próxima:** la estética de una cuenta se ve o no se diseña. Antes de generar la
primera pieza, pedir capturas de la grilla. Inferir una identidad visual desde el
sistema de diseño de otro producto de la misma empresa es exactamente el error:
Academy y la app comparten dueño, no lenguaje. Y una descripción de imagen que
contradice los archivos que sí podés abrir es un dato falso, no una segunda opinión.

### 2026-07-28 · LEARN — En Argentina, un precio impreso es deuda técnica

Facu bajó los precios de las 75 piezas de Academy: con la inflación, un flyer
publicado con un número queda viejo en semanas y obliga a rehacer la tanda entera.
Las piezas ahora muestran solo lo que **no se desactualiza** —créditos por mes,
cantidad de clases, cantidad de módulos— y el valor del mes se pide por DM.

El guard quedó en el código, no en el contenido: `bloque_editorial()` revienta si le
llega un bloque de tipo `precio`. Puesto solo en el JSON, alcanzaba con editar el
contenido para que volviera a salir un número.

Efecto secundario que importa: la tanda pasó de tener una fecha de vencimiento a no
tener ninguna. Antes había que regenerar con cada lista de precios; ahora solo si
cambia el catálogo.

**La próxima:** en cualquier pieza que se publica y queda dando vueltas —flyer, PDF,
landing— preguntarse qué dato tiene fecha de vencimiento y sacarlo. Un número que
obliga a rehacer el material es peor que un número ausente.

### 2026-07-28 · FAIL ✓ — Una tanda que se cae a la mitad deja mezcla, no vacío

Regenerando los 75 flyers sobre la carpeta ya poblada, un Chrome se colgó a los 120s
y el script murió. En disco quedaron 75 PNGs —el conteo daba bien— pero eran una
mezcla de la corrida nueva y la vieja. El chequeo de cantidad no lo veía: los
archivos viejos existen, pesan bien y miden bien.

**El fix:** `render()` reintenta 3 veces antes de darse por vencido (el cuelgue es de
Chrome bajo carga, no del contenido: la misma pieza sale bien al segundo intento), y
una regeneración total borra la carpeta primero.

**La próxima:** un contador de archivos no verifica una regeneración; verifica que
haya archivos. Si el proceso escribe sobre lo que ya estaba, o se borra el destino
antes, o se compara algo que distinga la corrida (fecha, hash, versión).

### 2026-07-28 · FAIL ✓ — El agente `numeros` frenó dos errores en la estrategia de pauta

Primer borrador de `active/astronomy/PAUTA_ACADEMY.md`: los 8 cálculos centrales
reprodujeron exactos (retención de cohorte al segundo decimal, CAC, márgenes). Pero
el auditor encontró dos cosas que sí importaban:

1. **El margen −7% descansaba casi entero en un solo mes con problema de carga.**
   Dic-2025 tiene CERO filas de Membership (el resto de los meses tienen entre 5 y 20)
   y ene-2026 tiene 20, el máximo de la serie: las membresías de diciembre se cargaron
   en enero. Dic-2025 cierra en −US$3.145 y **los otros once meses suman +US$1.103**.
   El total anual no cambia, pero "el negocio pierde plata" era una lectura falsa:
   está en el cero. Iba a un documento que decide presupuesto.
2. **Un escenario alternativo mal derivado.** "Si Sueldos es fijo, la contribución
   sube a ~75% y el CAC a US$68" — la cuenta real da 81% y US$74. Aparecía dos veces.

Y varias menores reales: un subtotal de US$549 que era US$753 (la planilla tiene la
misma subcategoría con dos grafías — `Clase de Prueba` / `Clase de prueba` — y el
conteo tomó una sola), "1,2x más" leído como 120% cuando es 21%, seis filas con tipo
de cambio implícito imposible (una de 9.546 ARS/USD) que mueven el resultado US$269,
y `Sueldos Fijos` —la línea de egreso más grande, US$6.904— sin mencionar en ningún
lado del análisis de costos.

**La próxima:** dos cosas. Una, antes de promediar una serie mensual, mirar si algún
mes tiene cero de una categoría que todos los demás tienen: es carga corrida, no
negocio, y contamina cualquier conclusión de tendencia. Dos, agrupar por una columna
de texto libre sin normalizar mayúsculas parte la categoría en dos y el subtotal
queda corto en silencio.

**Lo que salió bien:** el auditor corrió ANTES de que el documento se usara, y su
propio reporte se autolimitó donde correspondía — reconstruyó la retención real
matcheando Client Id faltantes por nombre, dio el número (2,94 en vez de 2,81), y
aclaró que no lo tomaba como bueno porque matchear por nombre es exactamente lo que
la regla de atribución prohíbe. Lo reportó como cota del sesgo, no como dato.

---

## 2026-07-28 — Bigg: una etiqueta de mes movió $1,9M de lugar

**Qué pasó.** Revisando cuentas corrientes, junio de Bigg aparecía con el alquiler
cargado **tres veces** ($5.731.160,59 cuando el contrato 50/50 da $3.820.773,73) y
mayo con una sola mitad. Ni uno ni otro eran errores de plata: los pagos estaban
perfectos. Era una etiqueta de mes mal puesta en la pestaña del local.

**La causa.** En las pestañas de Ctas Ctes, el alquiler de un mes se carga en dos
filas: `Alquiler` (mitad facturada, con IVA) y `Diferencia Alquiler (sin iva)` (la
mitad en efectivo). En los bloques viejos la Diferencia llevaba **el mes anterior**
al que corresponde. Mientras las dos mitades valieron lo mismo ($1.750.000) el
desfase fue invisible; cuando el ajuste por IPC las movió a $1.910.386,86, un mes
quedó con tres mitades y otro con una.

**La regla que faltaba escrita:** en una pestaña de local, **cada fila pertenece al
mes del bloque donde se paga, no al mes que dice la etiqueta**. El bloque es
"expensas del mes anterior + alquiler del mes corriente", y cierra contra el pago
de ese mes. Verificarlo así es lo que permitió fechar el ajuste de IPC sin
adivinar: el pago de mayo usa la tarifa vieja y el de junio la nueva, los dos al
centavo.

**La próxima:** cuando un local paga en dos canales (banco / efectivo), reconstruir
el pago esperado por canal y compararlo contra lo pagado. Banco = mitad facturada +
IVA + expensas del mes anterior; efectivo = mitad sin IVA. Si los dos cierran al
peso, los movimientos están bien y el problema está en los cargos. Eso convierte
"algo no cuadra" en "esta celda está mal" en cinco minutos.

**Dos errores míos, para no repetirlos:**

1. **Calculé el saldo contra CARGOS en vez de contra la pestaña del local.** La
   pestaña es la contabilidad viva: su saldo corre secuencialmente y no le importa
   la etiqueta de mes, así que estaba bien mientras CARGOS estaba mal. Le pasé a
   Facu $1.171.137,46 cuando el número correcto —el suyo— era **$961.345**. Antes
   de dar un saldo, mirar la pestaña del local, no la tabla derivada.
2. **Prometí que dos celdas iban a arreglar el radar y no lo arreglaron.** Corregí
   junio, dije "con esto el radar deja de mentir", y el radar siguió marcando a Bigg
   al día. Faltaban el desfase de las otras tres etiquetas, el crédito por error de
   expensas y un pago en tránsito. **No anunciar el efecto de un fix antes de
   correrlo:** aplicar, correr, y recién ahí decir qué cambió.

**Lo que quedó construido.** `exportar_ctas_ctes.py` (radar → JSON) y la pestaña
**Deuda** en la app del Paseo, con un bloque `PENDIENTES_DE_CARGA` que muestra la
plata ya cobrada que todavía no entró al sheet **sin sumarla al saldo** — el saldo
sigue saliendo de la fuente, y el aviso evita reclamar algo ya pagado.

---

## 28/07/2026 · Astronomy web — el header era lo que impedía que las landings fueran estáticas

**El síntoma.** La pauta de Academy cae en `/` y `/academy`, y esas páginas tardaban
0,30 s en caliente y **1,83 s en frío**. `/curso-profesional-dj` tardaba 0,18 s. La única
diferencia entre ellas: `curso-profesional-dj` no usaba `SiteHeader`.

**La causa.** `SiteHeader` es un componente de servidor que llama a `auth.getUser()`. Basta
con eso —una sola lectura de cookie— para que Next marque **toda la página** como dinámica y
la renderice en cada visita en vez de servirla del CDN. El header, que es lo mismo en las 9
páginas, obligaba a re-renderizar las 9.

**El arreglo.** Partirlo en dos: `SiteHeader` (server, para las páginas con sesión, donde el
alumno no puede ver un header vacío) y `PublicHeader` (cliente, pide `/api/header` al
montar). La lógica queda en un solo archivo, `lib/headerState.ts`, o las dos vías se
desincronizan y el header miente en una de las dos. Mientras no sabe si hay sesión, el
bloque de cuenta **no se dibuja**: mostrar "Ingresar" y darlo vuelta 150 ms después se ve
peor que que aparezca una vez y bien.

**La generalizable.** Cualquier cosa que lea cookies o headers —aunque sea un componente
compartido y chiquito— le saca lo estático a la página entera. Antes de optimizar consultas,
buscar quién toca la sesión.

**El error de método, que fue el que más tiempo comió.** Saqué un screenshot de producción
con `--virtual-time-budget=8000` y el local **sin** el flag. El local salió a medio cargar,
lo comparé contra el otro y di por rota una grilla que estaba bien. Recién al repetir la
medición en igualdad de condiciones apareció la regresión **de verdad**, que era otra:

> `.card` trae `margin-left/right:auto`. Dentro de un grid, un margen automático dimensiona
> el item a **fit-content**, no a la columna. Mientras hubo un `<img>` normal adentro no se
> notaba, porque la imagen aportaba su ancho intrínseco. Al pasarlo a `next/image` con
> `fill` —que es `position:absolute`— la foto dejó de aportar y **cada card se encogió al
> ancho de su propio título**. `next build` y `tsc` dieron verde.

**Las dos reglas que dejo escritas:**

1. **Comparar siempre con el mismo instrumento.** Un screenshot contra otro tomado con otros
   flags no es una comparación, es ruido que se disfraza de hallazgo.
2. **Cambiar un `<img>` a `next/image` con `fill` cambia el layout aunque el CSS no se
   toque**, porque la imagen deja de aportar tamaño intrínseco al padre. Si el contenedor
   depende de eso —`fit-content`, `margin:auto` en grid o flex, `width` sin declarar—, se
   rompe en silencio. Verlo requiere abrir la página; ningún chequeo automático lo agarra.

---

## 28/07/2026 · Astronomy web — legales, y dos veces la misma trampa de CSS

**Lo que destrabó plata.** La app de Meta `astronomy-ads` no se podía publicar sin una URL
de política de privacidad alcanzable, y con eso los anuncios por API quedaban bloqueados.
`/privacidad` ya estaba escrita pero sin deployar: el primer deploy la puso online y
destrabó la pauta. Después se completó el resto —`/terminos`, `/arrepentimiento` (que es
obligatorio por la Resolución 424/2020 y es la falta que más se sanciona), datos del
proveedor y link a Defensa del Consumidor en el footer—.

**La decisión que vale repetir.** Los datos que faltaban —razón social, CUIT, domicilio—
se centralizaron en un `lib/empresa.ts` con los campos en `null`, y **el sitio no dibuja
esa línea mientras estén vacíos**. La alternativa habitual, un placeholder tipo
`XX-XXXXXXXX-X`, es peor: parece un dato real, nadie lo nota, y termina publicado. Cuando
lleguen los datos se cambia un archivo y aparecen en las cuatro páginas a la vez.

**La trampa, que apareció dos veces en la misma sesión.** `globals.css` importa `ui.css`
en la primera línea. Los `@import` van primeros por regla de CSS, así que **todo lo que
está en globals se aplica después** y, a igual especificidad, gana por orden de fuente. Mi
`.legal { max-width: 760px }` perdía contra `.wrap`, y mi `.legal { text-align: left }`
perdía contra `.section { text-align: center }`. En las dos el síntoma era el mismo: la
regla existía, el navegador la mostraba tachada, y parecía que el archivo no se había
recargado.

Se resuelve subiendo la especificidad con doble clase —`.section.legal` mide (0,2,0) y le
gana a (0,1,0)—, nunca con `!important`, que arregla un caso y arruina el siguiente.

**La regla general:** en un proyecto con dos hojas y una importando a la otra, **la capa
importada es la más débil, no la más fuerte**. Si el sistema de diseño vive en la hoja
importada, cualquier regla de la hoja principal lo pisa gratis. Antes de escribir un
override, mirar quién importa a quién.

**La otra, chica pero repetida:** el `p` global de este sitio va `text-align: justify`.
Está bien para una landing ancha y mal para cualquier columna angosta —footer, texto
legal—, donde abre huecos de espacio entre palabras. Toda columna angosta nueva tiene que
volver a poner `text-align: left` explícito.

**Cómo se verificó**, además del build y `tsc`: screenshots de cada página nueva, y un
crawl de los 138 links internos de las 11 páginas públicas para confirmar que ninguno
quedó roto. Un link roto en un footer nuevo no lo detecta ningún compilador.

---

## 28/07/2026 · Astronomy web — sacar una página del servidor sin que se note

**El resultado.** Las seis páginas públicas pasaron de renderizarse en el servidor en cada
visita a servirse del CDN. `/academy`, que es donde cae la pauta, bajó de **0,47–1,05 s a
0,12 s** de TTFB.

**Qué las ataba.** Casi nunca es la consulta pesada que uno imagina. Eran tres cosas
chiquitas, y cualquiera de las tres sola alcanzaba para volver dinámica la página entera:
leer un `searchParam` para mostrar un cartel de error, un `getUser()` que sólo decidía el
texto de un botón, y usar el cliente de Supabase que lee cookies para traer datos que son
**públicos**. Ese último es el más fácil de pasar por alto: la consulta no necesitaba
sesión, sólo se había escrito con el cliente que estaba a mano.

**La regla:** antes de optimizar consultas, buscar quién toca cookies, headers o
searchParams. Una sola línea condicional cuesta la página completa.

**El patrón para que el usuario no vea el cambio.** Cuando la sesión se resuelve en el
navegador hay un momento en que no se sabe quién entró. La solución no es única, depende
de si las dos variantes se ven distinto:

- **Se ven igual** (un botón "Suscribirme" que cambia de destino pero no de texto):
  dibujar la variante anónima y listo. No hay parpadeo posible porque el pixel es el mismo.
- **Se ven distinto** (el header con créditos, un "¿todavía no tenés cuenta?"): **no
  dibujar nada** hasta saber. Mostrar el estado equivocado y darlo vuelta 150 ms después se
  ve peor que que aparezca una vez, bien.

Y siempre hay que cubrir el borde: alguien que toca el botón *antes* de que resuelva. Acá
eso mandaba a un usuario logueado a `/registro?plan=gold`, donde el proxy lo redirigía al
panel **perdiéndole el plan que había elegido**. Se arregló en el proxy, no en el botón.

**Una petición, no cinco.** En `/academy` hay cinco componentes que preguntan lo mismo. La
promesa del `fetch` se guarda **a nivel de módulo**, así todos esperan la misma respuesta:

```ts
let promesa = null;
export function pedirSesion() {
  if (!promesa) promesa = fetch("/api/header").then(...).catch(() => ANONIMO);
  return promesa;
}
```

Sin contexto, sin provider, sin envolver el árbol. Y se verifica de verdad, no de palabra:
`chrome --headless --log-net-log=net.json`, y después contar en el JSON las fuentes de
tipo `URL_REQUEST` (type 1) que mencionan la URL — los otros ids que aparecen son jobs y
sockets subordinados del mismo pedido, así que contar coincidencias de texto da de más.

**La verificación que más tranquilidad da:** screenshot de la página vieja y de la nueva al
mismo tamaño, y `ImageChops.difference(...).getbbox()`. Si devuelve `None`, el refactor no
cambió **un solo pixel**. En `/academy` dio `None`. Cuando después toqué la tipografía, el
mismo diff me dijo exactamente qué se había movido y pude mirar sólo eso.

---

## Meta Marketing API: el `creative_id` es un objeto compartido, no una copia

*28/07/2026 · Astronomy Academy · costó una hora de entrega del anuncio que más gastaba*

Para armar un test A/B necesitaba un anuncio nuevo con la misma imagen que uno existente.
Reutilicé su `creative_id` — parecía lo obvio y lo barato:

```python
post(f"{CUENTA}/ads", name=..., adset_id=NUEVO,
     creative=json.dumps({"creative_id": "1514918636967589"}))  # el del anuncio que ya corría
```

Un `creative` en Meta **no es un archivo, es un objeto vivo compartido entre todos los
anuncios que lo referencian.** El conjunto nuevo pertenecía a una app que en ese momento
estaba en modo Desarrollo, así que Meta marcó el creativo, y **el anuncio original —que
no toqué— heredó el problema y se autopausó.** Se llevaba el 76% de la entrega del
conjunto.

Reactivarlo no alcanza: Meta vuelve a marcarlo. La marca queda en el objeto.

**La regla:** para un anuncio nuevo, siempre un creativo nuevo, aunque apunte a la misma
imagen. Cuesta una llamada más y aísla el riesgo.

Al reconstruirlo aparecieron dos trampas más:

- **`/copies` falla** si el creativo original usa `asset_feed_spec` con recortes
  discontinuados (`191x100`). El error no menciona el recorte hasta que se lee
  `error_user_msg`, no `message`.
- **Crear un `adcreative` desde `object_story_id`** de una publicación dinámica devuelve
  `Invalid parameter` a secas; el motivo real (*"falta el identificador del conjunto de
  productos"*) sólo aparece en `error_user_msg`.

**En esta API, `error["message"]` casi nunca alcanza. Siempre loguear también
`error_user_msg` y `error_subcode`** — ahí está el diagnóstico.

Lo que sí se puede reutilizar sin riesgo es el **`image_hash`**: son inmutables y
compartirlos entre creativos no propaga nada.

**Y un borde de reporte:** `issues_info` a nivel cuenta devuelve el ruido histórico de
años de campañas pausadas. Filtrar por anuncios que pertenezcan a conjuntos con
`effective_status == ACTIVE`, o el informe grita todas las semanas por anuncios de 2024.

### 2026-07-30 · FAIL ✓ — La tabla de `leer_meta.py` escondía la decisión que había que tomar

Al retomar la decisión abierta de pauta (¿pausar `3IntW2`?), la primera corrida de
`leer_meta.py --nivel ad` salió con la columna NOMBRE **entera en `?`** y con el costo por
conversación redondeado a `1` y `2`. Con esa tabla la decisión era imposible de tomar, y
peor: la lectura del 29/07 que quedó en memoria estaba **mal** por culpa de esto.

**Tres causas raíz distintas, las tres en el mismo lugar:**

1. **`CAMPOS_INSIGHTS` no pedía `<nivel>_id` ni `<nivel>_name`.** La Graph API no los
   devuelve por defecto en `/insights`, así que las filas venían sin identificador y el
   cruce contra las entidades (`por_id`) fallaba en el 100% de los casos. La fila mostraba
   `?` en vez de gritar. `reporte_pauta.py` sí los pedía —ahí estaba la pista de que el
   campo era obligatorio, no opcional. Fix: `campos_insights(nivel)`.
2. **El formato `,.0f` en gasto, CPM y `$/CONV`.** Un costo de US$0,89 y otro de US$2,38
   se imprimen los dos como un entero de una cifra y **el 3x desaparece**. Es justamente
   el número por el que se mueve presupuesto. Fix: dos decimales.
3. **Homónimos indistinguibles.** Hay **dos anuncios llamados `2IntW2 Curso de DJ`**: el
   viejo (`…260448`, borrado el 28/07, corría a US$2,29 y se llevó US$382,97 en 30 días) y
   el nuevo (`…530448`, creado el 28/07, US$0,89). Es el mismo defecto de nombres que ya
   documentamos para los carruseles, pero acá no había versión que los separara. Encima el
   viejo **no aparece en `/{cuenta}/ads`** —el listado esconde los borrados— así que su
   fila quedaba sin entidad y sin estado. Fix: cuando el nombre se repite se le cuelga el
   final del id, y una fila sin entidad se marca `BORRADO` en vez de dejar el estado vacío.

Y al arreglar los tres apareció un cuarto: **la tabla no cerraba contra sí misma.** La
fila del conjunto decía US$2,20 por conversación y el TOTAL US$2,00 sobre exactamente el
mismo gasto, porque `conversaciones()` tomaba el **máximo** de las dos variantes de la
acción de mensajes para la cantidad (255) y el `cost_per_action_type` que Meta reporta para
**la otra** variante (232 conversaciones). Dos métricas distintas mezcladas en una fila.
Fix: se elige una sola variante por fila, en orden de preferencia, y el costo se divide
acá (`gasto / cantidad`) en vez de leerlo de la API — así cada fila cierra y el total
cierra con las filas.

**La lección transferible: una fila de reporte que no puede identificar a qué se refiere
no es un dato, es un error.** Un `?` en la columna que da identidad tiene que romper la
corrida, no imprimirse. Y un anuncio borrado sigue teniendo gasto histórico: el listado de
entidades vivas nunca es suficiente para explicar de dónde salió la plata.

**Y el resultado real, que era lo que se buscaba:** medido por día, `3IntW2` ya lo
desfinanció Meta solo (US$2,10 en 7 días, 1,4% del conjunto). Pausarlo no mueve plata. Lo
que la mueve es que el carrusel de Modo Profesional lleva 30 días con **US$0,60 y cero
conversaciones** porque comparte el **único conjunto activo** de la cuenta con un anuncio
de Curso de DJ que gana: un solo presupuesto, y Meta se lo da todo al ganador.

### 2026-07-30 · FAIL ✓ — Un lifetime de Meta sin paginar dio 4 veces menos gasto del real, sin ningún error

Chequeando fechas de anuncios usé un helper propio de una línea que no seguía la
paginación. Para el anuncio `2IntW2` borrado devolvió **US$127,40 de gasto de por vida**.
El real, paginando, es **US$529,54**. Cuatro veces más. La API no avisó nada: devolvió una
primera página de 25 días perfectamente válida y un `paging.next` que nadie miró.

Peor: el mismo dato ya lo había traído bien un rato antes en otra corrida —US$382,97 en 30
días— así que **el lifetime era menor que la ventana de 30 días y eso solo ya era
imposible.** No lo vi hasta comparar los dos números.

`leer_meta.py` sí pagina (`pedir()` sigue `paging.next` hasta el final). El bug fue mío por
escribir un helper descartable al lado del que ya estaba resuelto.

**Dos reglas:**

- **Ningún total de Meta se reporta desde un helper que no pagine.** Si es de una sola
  corrida, se usa `pedir()` de `leer_meta.py`, no un `httpx.get` suelto.
- **Todo lifetime lleva un control de suma.** El que sirve acá: la suma del gasto de los
  175 anuncios tiene que dar el `amount_spent` de la cuenta. Dio US$7.111,24 contra
  US$7.110,61 declarado — 0,009%. Sin ese control, un total truncado se reporta como dato.

**Y el error de lectura que esto casi dejó pasar:** dije que el carrusel de Modo Profesional
"lleva 30 días con US$0,60 y cero conversaciones". Falso. El carrusel **nació el 29/07 a las
11:06** — tenía **un día**. Lo que tenía 30 días era la ventana del reporte (`--dias 30`),
no el anuncio. Facu lo cazó al toque porque se acordaba de haberlo hecho el día anterior.
**`created_time` no es opcional en un reporte de pauta: sin él, "lleva N días" es una
invención con formato de dato.**

---

## 30/07/2026 — El 89% de los premios no era del mes, y esperaba un botón

El sistema de premios de la academia tenía **un solo botón**: "cerrar el mes". Adentro de
ese botón convivían dos cosas de naturaleza distinta, y sólo una era mensual.

Julio 2026, contra la base: **52 premios, 380 créditos**. De esos, **47 premios y 340
créditos eran hitos y rachas** — metas individuales, sin competencia, cumplidas hacía
semanas. El podio, lo único donde se compite de verdad, eran **5 premios y 40 créditos**.

Lo delator estaba en el propio código: la clave de un hito es `hito:10:alumno`, **sin
período**. El mes nunca formó parte de la identidad de un objetivo; sólo lo retenía.

**Lo que se rompió por eso:** el mes en curso no se podía cerrar sin congelar mal el podio,
así que el 89% de los premios quedaba rehén de un mes que todavía no había terminado. Y la
"protección" era acordarse de apretar el día correcto.

**El arreglo** (idea de Facu: *"si los premios son más objetivos que premios..."*):
objetivos entregados por el cron horario apenas se cumplen; podio publicado solo el día 1.

Tres cosas que dejó el camino:

1. **Un desempate puede ser un bug con cara de orden.** El podio ordenaba los empates con
   `a[0].localeCompare(b[0])` — el **UUID**. Dos alumnos con las mismas clases cobraban 3 y
   2 créditos según el azar de un identificador interno. Ahora comparten puesto. Si un
   criterio de orden no se puede explicar en una frase del negocio, no es un criterio.
2. **Una condición de fecha adentro de una función que escribe no se puede probar.** El
   guardarraíl salió a `motivoParaNoPublicar(periodo, hoy)`, puro y con `hoy` inyectable.
   Recién ahí se pudo verificar en verde que julio no se publica el 30 y sí el 1/8.
3. **Me equivoqué al describir el daño.** Dije que otorgar antes de tiempo dejaría "dos 4°
   puestos y medallas duplicadas". Falso: la clave del podio es `podio:mes:alumno` **sin el
   puesto**, justamente para eso. El daño real era otro —el podio se congelaba al revés—
   y seguía justificando frenar, pero **afirmé un mecanismo sin haber leído `claveDe`**.
   Cuando el argumento para frenar algo es técnico, el mecanismo hay que leerlo, no
   deducirlo.

Verificado en producción: 46 objetivos entregados, 320 créditos, 23 alumnos avisados (un
aviso por alumno, no uno por premio), 0 podios. Segunda corrida: 0 — es idempotente.

### 2026-07-30 · FAIL ✓ — Chrome headless con ventana alta deforma los `vh` y el recorte cae en otra sección

Para verificar el bloque de precio del landing de Modo Profesional saqué una captura de
página completa con `--window-size=1440,12000` y recorté por coordenadas. El recorte cayó
en **"Qué vas a lograr"**, tres secciones antes.

**Causa raíz: el viewport define el `vh`.** Con una ventana de 12000px de alto, el
`minHeight: 88vh` del hero pasa a medir **10.560px** y se come la página entera. No es que
el recorte esté mal calculado: es que el layout que se fotografió no existe en ningún
teléfono ni monitor.

**El fix es fijar el viewport y capturar más allá de él**, que solo se puede por CDP:
`Emulation.setDeviceMetricsOverride` con un tamaño realista (1440×900, 390×844) y
`Page.captureScreenshot` con `captureBeyondViewport: true` y el `clip` del
`getBoundingClientRect()` del elemento. Quedó en `shot.py` (scratchpad de la sesión; si se
vuelve a usar, graduarlo a `execution/`). El venv ya tiene `websockets`.

Tres bordes más, todos costaron corridas:

- **`--screenshot` no scrollea por el `#hash`.** La captura sale del tope de la página
  aunque la URL tenga ancla. Hay que scrollear con `Runtime.evaluate` antes de capturar.
- **`IntersectionObserver` no dispara en headless.** Depende de que el navegador produzca
  frames. Una barra fija que aparecía por IO nunca se activó, y `getComputedStyle` mostró
  la clase sin aplicar. **Un elemento que solo se puede verificar con frames no se puede
  verificar así**: la barra se sacó antes de pushear en vez de mandarla sin probar.
- **Los procesos se acumulan.** `proc.terminate()` mata al padre y deja los hijos: llegué
  a **49 procesos de Chrome** y a partir de ahí cada lanzamiento nuevo se colgaba o
  devolvía `Not attached to an active page`. Hay que matar por patrón entre corridas — y
  eso también se lleva el Chrome interactivo del usuario, así que se avisa.

**La lección: una captura headless no es prueba de nada hasta saber a qué viewport
corresponde.** El tamaño de ventana no es un parámetro de encuadre, es parte del layout.

### 2026-07-30 · Grepear el HTML no prueba que un pixel funcione

Al poner el pixel de Meta en `astronomy-members`, la verificación obvia —bajar la página
con `curl` y buscar el ID— dio **cero** en producción, en el deploy directo y hasta en el
build local servido con `next start`. Parecía un deploy roto. No lo era.

**`next/script` con `strategy="afterInteractive"` no deja el snippet en el HTML servido**:
lo inyecta el bundle del cliente después de hidratar. El HTML prerenderizado en
`.next/server/app/*.html` sí lo tiene, y el servido no — por eso el primer grep dio
positivo y el segundo negativo, que fue lo más confuso de todo.

**Cómo se verifica de verdad, en orden de qué tan concluyente es:**

1. **`last_fired_time` del pixel en la Graph API.** Es el único que prueba que Meta
   *recibió* el evento, no que el navegador lo mandó. Pasó de `2025-07-20` a la hora de la
   prueba. Cierra el circuito de punta a punta.
2. **Los pedidos de red del navegador** (`Network.requestWillBeSent` por CDP), mirando
   `connect.facebook.net/signals/config/<pixel_id>` y los beacons a `facebook.com/tr`.
   Quedó en `pixel_check.py`.
3. **El estado de `window.fbq`** (`loaded: true`, `queue: 0`, `version`). Prueba que el
   snippet corrió, no que salió el evento.

**Un borde de headless:** el `config` del pixel volvió 200 y `fbq` quedó cargado con la
cola vacía —o sea, `init` y `track` se procesaron— pero **no se vio ningún beacon a
`/tr`**. Meta detecta automatización. En headless, la ausencia del beacon **no** es
prueba de que el pixel esté roto; para eso está el punto 1.

**Y una trampa de verificación aparte:** pegarle 40 veces seguidas a
`astronomyofficial.com` hace que Vercel devuelva un challenge anti-bot
(`x-vercel-mitigated: challenge`), y ahí el HTML deja de tener el contenido del sitio. Se
lee como "el deploy borró todo". Hay que pegarle a la URL del deployment, como ya decía
la memoria `verificar-en-mac`.

### 2026-08-03 · Una fila `pendiente` creada antes de pagar bloquea la venta para siempre

El checkout de Modo Profesional ($440.000) estaba muerto para cualquiera que hubiera
intentado comprar una vez sin pagar. `buyModoPro` crea la inscripción en `pendiente`
**antes** de mandar a Mercado Pago —correcto: si el webhook llega antes que el usuario,
tiene que haber una fila que activar— pero después chequeaba `inscripcionViva`, que
cuenta `pendiente` como viva, y bloqueaba. El que abandonaba el checkout quedaba
encerrado, **y nada lo destrababa**: no hay cron que venza las pendientes (a propósito,
porque un cron que no corre falla en silencio).

Síntoma que reportó Facu: los dos botones de compra "no redirigen a ningún lado". Era
verdad — redirigían a la misma pantalla, siempre.

**El patrón, que vale para cualquier checkout:** una fila creada *en espera del pago* es
un borrador, no un compromiso. Tiene que poder **reusarse**, no bloquear. Y la pregunta
de diseño que hay que hacerse al escribirla es: *¿qué la borra si el usuario nunca
vuelve?* Si la respuesta es "nada", ya está el bug.

**Reusar la misma fila es mejor que cancelar y crear otra.** El `external_reference` de
Mercado Pago lleva el id adentro, así que reusando, un link viejo y uno nuevo apuntan al
mismo lugar y ningún pago queda huérfano. Cancelando y recreando, un pago sobre el link
viejo activa una fila muerta y quedan dos activas — que el índice único parcial rechaza
**en silencio**, porque el `UPDATE` del webhook no mira el error.

**Y el corolario que muerde:** si la fila se reusa, sus datos pueden haber cambiado entre
un checkout y el otro. Acá el `modo`: la fila decía `cuotas` y podía entrar el pago de un
link de pago único anterior → 4 clases habilitadas por $440.000. La verdad de un pago
está en **el pago**, no en la fila; por eso el `modo` viaja en el `external_reference` y
manda mientras la inscripción esté pendiente.

**Aparte, un modo de falla de UX barato de cometer: reciclar un código de error entre dos
dominios.** El bloqueo redirigía con `e=yatenes`, que en la misma tabla de textos
significa "ya tenés otra clase reservada en ese mismo horario". Al que quería *comprar*
le aparecía un error de *agendar*, hablándole de una reserva que nunca hizo. Un
diccionario de errores compartido entre dos flujos necesita claves con el flujo en el
nombre, o termina mintiendo con total confianza.

**Lo encontró el Análisis 360° del Playbook** (sección 7), grepeando dónde más aparecía
lo mismo: la landing prometía un "showcase final de 60 minutos frente a público" que no
existe —la clase 8 es la grabación del set— y **su propia lista de reglas dos bloques más
abajo ya decía "grabación"**. La página se contradecía a sí misma y la versión que vendía
era la que prometía de más. El mismo grep encontró "los 60 créditos de cada una no
vencen" y "Créditos que no vencen": promesas del curso viejo, sobre un producto que no
usa créditos y vence a los 4 meses.

**La lección de contenido: cuando un producto reemplaza a otro, el texto viejo no se
borra solo.** Sobrevive en la metadata, en el open graph y en la página de al lado — que
es exactamente donde nadie mira. Y una promesa de más en una página de venta no es un
typo: es lo que el alumno va a reclamar después de pagar.

### 2026-08-03 · Auditar un módulo de cobros: lo que sólo se ve mirando los datos

Cuatro rondas sobre el módulo de pagos de `astronomy-members`. Ninguno de los hallazgos
graves salió de leer código: todos salieron de **cruzar la base contra la API del
proveedor**. Vale para cualquier integración de plata.

**El más caro fue una puerta abierta, no un bug.** La ruta `/prueba` vendía **1000
créditos por $15** —a precio de Platinum, unos $566.000— y sólo pedía estar logueado. El
plan estaba oculto de las pantallas por una lista `HIDDEN_PLANS`, y eso da una falsa
sensación de cierre: **esconder el precio no cierra la puerta**. La guarda tiene que estar
en la server action, no en la página, porque una action se invoca directo. No la usó nadie
(0 pagos), pero llevaba meses ahí.

**Un proveedor puede usar DOS ids para la misma cosa.** Mercado Pago identifica un plan con
un id en la suscripción y con otro en el pago. Una Silver vieja tiene `2c938084…` en una
punta y `52c8c6d7…` en la otra. Cualquier cruce contra "el id del proveedor" anda para unos
casos y falla en silencio para otros. **Se cruza por el id NUESTRO**, y la traducción se
hace en un solo lugar.

**Tres relojes.** Una ventana de tiempo con borde superior estricto (`created_at <=
fecha_del_pago`) descartaba un registro recién creado, porque Postgres iba **1,4 segundos
adelante** del otro reloj. En producción los relojes son tres: el del proveedor, el de la
base y el del server. Toda ventana que cruce sistemas necesita **tolerancia**, y el test de
punta a punta fue lo que lo encontró — el typecheck no ve esto.

**Los links de pago del proveedor no caducan.** Quedaban 10 vivos, cada uno atado al mail
con el que se generó. De ahí salía un error que parecía del sitio ("tu e-mail no coincide
con el de la suscripción"). Si se cancela un intento, hay que cancelarlo **de los dos
lados**, y primero en el proveedor: si eso falla, la fila propia NO se toca. Una base que
dice "cancelado" mientras el proveedor sigue cobrando es lo peor de los dos mundos.

**Y la contracara: cancelar con demasiada prisa.** Al empezar a cancelar en el proveedor
introduje una regresión — alguien con el checkout abierto en otra pestaña se quedaba sin
link. Toda cancelación automática necesita **gracia**.

**Rechazar una firma inválida no es paranoia, es cuota.** El webhook procesaba igual
porque "el crédito se valida contra la API". Cierto, pero cada POST falso costaba una
consulta al proveedor con nuestro token: si nos limitan, los webhooks **reales** dejan de
acreditar. Se corta antes de hablar con el proveedor. Lo que hace seguro cortar es que hay
un puente horario que acredita igual: el peor caso es "una hora más tarde", no "nunca".
De paso, `timingSafeEqual` **tira excepción si los largos difieren** — cualquiera podía
hacernos devolver 500 mandando una firma corta.

**La conclusión que vale para el OS: una auditoría que se corre a mano se corre una vez.**
Los once chequeos quedaron en `/admin/conciliacion`. Y la regla al construirlo: **un panel
que avisa en falso el primer día deja de mirarse**. El primer borrador marcaba 3 planes
como huérfanos por el problema de los dos ids; encontrarlo antes de mostrarlo fue tan
importante como el panel.

### 2026-08-04 · FAIL ✓ — Arreglar un camino de cobro y dejar los otros tres con el mismo bug

El 03/08 hicimos transaccional la acreditación de un pago (`creditPlan`). La sesión cerró
con el pendiente bien anotado: "el mismo patrón vive en otros dos caminos". Al ir a
portarlos aparecieron **cuatro**, y el peor no estaba en la lista de nadie.

**El que no estaba anotado.** El puente horario (`syncPayments`, que rescata lo que el
webhook no pudo) mandaba los pagos de Modo Profesional a `creditPlan`, como a cualquier
plan. Y **eso no fallaba**: `modopro` existe en la tabla `plans` con 0 créditos, así que
la función tomaba el candado de idempotencia, registraba la venta, devolvía OK... y no
habilitaba una sola clase. Con el candado puesto, el webhook que llegara después rebotaba
con "ya procesado" y el curso no se activaba nunca. El alumno paga $440.000, la venta
figura cobrada en el libro, y él no puede agendar nada. **Ni un log lo decía.** El mismo
agujero estaba en el desplegable de asignación manual, que ofrece "Modo Profesional" entre
los planes.

**Causa raíz — no es "faltó un caso", es que el ruteo se derivó de la tabla equivocada.**
El código preguntaba "¿existe este plan?" cuando la pregunta era "¿qué hay que HACER
cuando entra plata de este plan?". Modo Profesional está en `plans` porque tiene precio,
no porque se acredite como los demás. Una lista de planes sirve para cobrar; no sirve para
decidir qué se entrega.

**La regla que queda: cuando un producto se acredita distinto, el ruteo se escribe UNA vez
y todos los caminos de cobro pasan por ahí.** Acá los caminos eran cuatro —webhook, puente
horario, asignación manual, carga manual— y sólo uno conocía la excepción. Al agregar un
producto que no encaja en el molde, la pregunta no es "¿anduvo?" sino **"¿por dónde más
puede entrar esta misma plata?"**. Se contesta grepeando el id del producto: aparece en
todos los lugares que hay que tocar.

**Segundo hallazgo: un contador en memoria no es idempotente.** `cuotas_pagadas + 1` se
calculaba leyendo la fila y escribiendo el resultado. Dos cobros entrando juntos leían el
mismo valor y escribían el mismo: el alumno pagaba las dos cuotas y le quedaban 4 clases
de 8. Se arregla con `for update` sobre la inscripción dentro de la transacción, no con un
reintento. **Todo contador que representa algo que se entrega necesita el lock, no el
optimismo.**

**Tercero, el más silencioso: un try/catch que no atrapa nada.** El registro del ingreso
por compra suelta de créditos estaba envuelto en `try { await supabase.insert(...) }
catch`. El cliente de Supabase **devuelve** el error, no lo tira: ese catch nunca se
ejecutó ni una vez. Si el insert fallaba, el alumno se quedaba con los créditos y la plata
desaparecía de Finanzas sin dejar rastro. Un `catch` alrededor de un cliente que devuelve
errores es una red de seguridad **pintada en el piso**.

**Cuarto: contestar 200 pase lo que pase pierde la plata que no se pudo acreditar.** El
webhook devolvía éxito siempre, así que un fallo se perdía ahí mismo: Mercado Pago daba la
notificación por entregada y no volvía a llamar. Y el puente sólo rescata los cobros que
tienen suscripción — deja afuera justo a los pagos únicos. Ahora un fallo reintentable
contesta 500 (MP reintenta) y queda en `audit_log`, visible en `/admin`. **Devolver éxito
a quien te avisó que entró plata, cuando no la pudiste acreditar, es mentirle al único que
puede volver a intentarlo.**

**Y una del método, que costó un susto:** el test de la acreditación creaba una inscripción
de prueba y caía, por diseño, en "la inscripción viva del alumno" cuando no encontraba la
indicada. La cuenta que elegí para probar tenía una inscripción real: el test le activó el
curso a una persona con un pago que no existía. Se detectó y se revirtió en el momento.
El script ahora **aborta si la cuenta de prueba tiene una inscripción viva**. Un test que
escribe en la base de producción necesita su propia precondición verificada, no una cuenta
"que seguro no tiene nada".

### 2026-08-04 · FAIL ✓ — Mercado Pago descarta el `notification_url` de las suscripciones, y un puente horario lo tapó durante semanas

Un alumno pagó el Curso de DJ a las 9:18. Mercado Pago lo aprobó y le cobró $143.520. La
web le siguió diciendo **"Pendiente de pago"** con 0 créditos. José, para destrabarlo, le
dio 240 créditos a mano a las 9:46. A las 10:00 pasó el puente horario y le acreditó los
240 del pago real: **480 créditos por un solo pago**. A las 10:38 el alumno agendó cuatro
clases. Con los 480 se habría llevado ocho por un pago de una.

**La causa raíz no es un error: es un campo que se ignora en silencio.** Mandamos
`notification_url` en el `POST /preapproval` y Mercado Pago lo guarda como `null` — el
`back_url` del mismo request sí queda. En una Preference (pago único) el mismo campo
funciona. O sea que **ningún cobro de suscripción notificó nunca a nuestra URL**: ni Curso
de DJ, ni Silver, Gold o Platinum. `payment_events` tenía 3 filas desde que existe, y las
3 eran pagos únicos.

**Lo que hizo que no se descubriera antes fue la red de seguridad.** El puente horario
(`syncPayments`, cron cada hora) acreditaba todo igual leyendo la API de MP. La plata
entraba, el libro cerraba, los créditos llegaban. Sólo que hasta 60 minutos tarde, y en
esos 60 minutos el alumno ve que pagó y no tiene nada. **Un rescate que funciona en
silencio no arregla la falla: la esconde, y te enterás por WhatsApp.**

Y había una segunda capa: aunque mañana se configure el webhook en el panel de MP, no
habría alcanzado. Los cobros de suscripción llegan con el topic
`subscription_authorized_payment` —cuyo `data.id` es el del *authorized payment*, no el del
pago— y ese topic no estaba manejado: llegaba, se contestaba 200 y no pasaba nada.

**El diagnóstico que sirvió, y el que no.** Los logs de Vercel duran ~2 minutos de tráfico:
inútiles para un pago de hace una hora. `payment_events` se escribe *después* de acreditar,
así que un webhook que nunca llegó y uno que llegó y falló se ven exactamente igual: nada.
Lo que cerró el caso fue leer el recurso en la API de MP y comparar dos pagos —uno de
suscripción y uno de Preference— por el mismo campo. **Cuando la pregunta es "¿me están
avisando?", la respuesta no está en tus logs sino en lo que el otro sistema guardó.**

Arreglado: tabla `webhook_hits` (todo golpe queda escrito **antes** de procesarlo), la rama
del topic que faltaba, rescate al volver del checkout (`lib/rescate.ts`, llama al mismo
puente idempotente sobre una ventana de 2 hs) y un chequeo en `/admin/conciliacion` que
lista los cobros que entraron sin su webhook. Verificado en producción con una notificación
firmada real: rebotó por idempotencia, sin doble acreditación.

**Queda de Facu, y es la causa raíz de verdad:** panel de MP → Tus integraciones → la
aplicación → Webhooks → URL `https://astronomyofficial.com/api/mp/webhook` con los eventos
de pagos **y de suscripciones** tildados. Es la única vía que existe para suscripciones.

### 2026-08-04 (bis) · Corrección a la entrada de arriba — eran DOS canales cerrados, y la doc de MP dice lo contrario

Facu marcó, con razón, que *"Mercado Pago descarta el `notification_url`"* era generalizar
desde **una sola** suscripción. Al medirlo en serio apareció algo mejor y algo peor.

**Mejor: la observación se sostiene, y más fuerte.** La respuesta del **propio POST**
`/preapproval` ya devuelve `notification_url: null`, con el `back_url` del mismo request
presente — o sea que el campo se pierde en la creación, no en la lectura. Un `PUT` para
setearlo tampoco persiste. De 100 suscripciones de la cuenta, **0** lo tienen. En una
Preference (pago único) el mismo campo sí queda.

**Peor: el segundo canal también estaba cerrado, y eso no lo había mirado.** El webhook a
nivel aplicación —lo que yo le había dicho a Facu que configurara— estaba **vacío**, y se
lee por API sin entrar al panel:

```
GET https://api.mercadopago.com/applications/<app_id>
notifications_callback_url: ""      notifications_topics: []
```

Con los dos canales cerrados no había ningún bug que buscar: **no había a dónde avisar.**

**Y la contradicción que hay que dejar anotada:** la documentación oficial de MP dice que
para Suscripciones la configuración desde "Tus integraciones" **no está disponible**, y que
hay que usar el `notification_url` de la creación — justo el que no persiste. Doc y
comportamiento real no coinciden.

**La lección del método, que es la que vale:** yo había verificado una cosa y afirmado
tres. Un caso confirma que algo *puede* pasar; no confirma la regla, ni el alcance, ni la
causa. La duda de Facu costó veinte minutos de mediciones y cambió la recomendación
concreta — de *"configurá el panel y listo"* a *"los dos caminos están cerrados y la doc
miente en uno"*. **Cuando una sola muestra alcanza para el diagnóstico, no alcanza para la
afirmación.**

### 2026-08-04 (ter) · RESUELTO — el canal que servía era el que estaba vacío, y ahora hay alarma

Facu configuró el webhook a nivel aplicación desde el panel (**por API no se puede**: `PUT`
y `POST` sobre `/applications/{id}` dan 403 en cinco variantes) y quedó verificado con un
cobro real de **$15**: MP aprobó a las 11:41:28, el golpe llegó 1,6 s después y los créditos
y la venta quedaron escritos a los **1,9 s**. El cron corre en punto y esto pasó al minuto
41: no fue el cron. **El puente pasó de mecanismo a respaldo.**

Dos trampas nuevas, las dos del mismo tipo — herramientas de diagnóstico que mentían:

- **`notifications_topics` de la API queda `[]` aunque los tres eventos estén tildados y
  llegando.** Es legacy. Casi le digo a Facu que se había olvidado de tildarlos. Un chequeo
  apoyado en ese campo avisaría "falta configurar" para siempre, y **un chequeo que siempre
  falla se ignora igual que uno que nunca falla.** Ahora se mira qué topics llegaron de
  verdad, que además prueba algo más fuerte que una casilla tildada: que MP entrega.
- **`preapproval/search` ignora el filtro `external_reference`** y devuelve la cuenta
  entera. Mi script de limpieza filtraba sobre esa lista creyéndola acotada, no encontró
  nada, imprimió *"0 suscripciones vivas"* y **dejó la suscripción de prueba cobrando $15
  por mes**. Un limpiador que no limpia y encima dice que sí es peor que no tener ninguno.

Y el veredicto del propio verificador cruzaba registros de **dos pagos distintos**: informó
2709 segundos de demora sobre un caso que había tardado 2. Ahora el par se arma por
`payment_id` y se mide contra el `date_approved` de MP — **medirse contra el propio registro
no prueba nada**.

Sobre pedido de Facu quedó la alarma: `alertarPagosSinWebhook()` en el cron horario avisa si
hay plata aprobada en MP sin webhook a los 5 minutos. Y **reporta que corrió** en la
respuesta (`webhook_mudo: {revisados, mudos}`): *"cero pagos mudos"* y *"el chequeo ni
corrió"* son los dos silencio, y esa indistinguibilidad es exactamente cómo este incidente
se escondió durante semanas.

**Los $15 del ensayo quedan en el libro.** Criterio de Facu, y es el correcto: la plata
entró de verdad, MP procesó el cobro, y borrarla sería falsear la caja. Los créditos de
prueba sí se revirtieron.

---

## 04/08/2026 — Un producto puede estar construido y no existir

Modo Profesional estaba **terminado y en producción** desde el 03/08: landing propia,
checkout, agenda, panel de admin, tests. Y aun así, la app entera lo trataba como si no
existiera. La razón es que se lo construyó como **producto** y no como **categoría**.

La app enumera sus categorías en muchísimos lugares —filtros, badges, audiencias de avisos,
conteos, exports, la cola de trabajo— y en cada uno de esos lugares hay una lista escrita a
mano: `["silver", "gold", "platinum", "djdelivery", "cursodj"]`. Un producto nuevo no rompe
ninguna: **sigue funcionando, sólo que sin él**. No hay error, no hay test en rojo, no hay
nada que avise. Se descubre cuando alguien pregunta "¿y este alumno por qué figura
inactivo?" — que fue exactamente lo que pasó: el que pagó **$449.999** aparecía **inactivo**
en la base de usuarios, porque "activo" se definía como *tiene membresía o tiene créditos*,
y el curso no usa ninguna de las dos.

Lo mismo, doce veces: no contaba como alta de alumno nuevo, no recibía los accesos
compartidos que el pack promete, no entraba en la cola de trabajo (podía pagar, dar dos
clases y desaparecer cuatro meses sin que nadie se enterara), y se le reclamaba una cuota
mensual que no existe.

**El patrón, para la próxima:** cuando nace un producto que no encaja en la tabla donde
viven los demás (`modopro` vive en `pro_enrollments`, no en `subscriptions`), la pregunta no
es *"¿anda?"* sino **"¿en cuántas listas de categorías falta?"**. Se busca por una de las
categorías viejas —`grep -rn '"djdelivery"'`— y se recorre cada resultado. Son diez minutos
y encuentran lo que ningún test encuentra, porque el bug es una **ausencia**, y una ausencia
no tiene stack trace.

Dos cosas más que salieron de ahí y valen aparte:

- **Un filtro que se arma con el texto que se muestra no filtra.** La columna del curso
  mostraba "Activo 3/8", así que el desplegable ofrecía una opción por cada contador
  posible y ninguna que dijera "todos los del curso". El estado y el detalle tienen que ser
  **dos datos distintos**: uno para filtrar, otro para leer.
- **El precio vivía en dos lados** (la tabla `plans` y strings en la landing), y el segundo
  no se actualizaba solo. Es la regla 12 en su forma más cara: la página podía prometer un
  número y Mercado Pago cobrar otro. Ahora la landing lee la misma fila con la que se arma
  el cobro, en cada visita.

---

## 04/08/2026 (II) — Lo que sigue contestando "ok" es lo que hay que revisar

Segunda vuelta sobre lo mismo del Lab Note anterior, después de que Facu preguntara lo
correcto: *"¿y que no quede hardcodeado otra vez? ¿y los reportes?"*. La respuesta al
primero fue un catálogo único (`lib/productos.ts`) del que se derivan las catorce listas
que estaban escritas a mano. La respuesta al segundo fue correr todos los reportes contra
la base real, y ahí apareció algo peor que lo que buscaba.

**El cron de recordatorios de clase no le avisaba a nadie desde la migración.** Lee
`bookings` —la tabla de Calendly— que tiene 37 filas y **cero clases futuras**. Las clases
están en `slot_bookings`: 16 futuras, 5 dentro de su ventana. Corría todos los días, sin
error, contestando `{ok: true, candidates: 0, sent: 0}`.

Ese `candidates: 0` es todo el problema. **"No hay clases mañana" y "estoy mirando la tabla
equivocada" producen exactamente la misma salida.** Un endpoint que devuelve un número que
puede ser cero por dos motivos opuestos no está reportando: está tapando. Por eso ahora
devuelve `porTabla: {slot_bookings, bookings}` — dos contadores, y uno en cero al lado de
otro que no lo está es una pregunta que alguien se hace.

Es la tercera vez que el mismo patrón nos muerde: [[cron-que-nunca-fallo]] (pg_cron decía
`succeeded` porque encoló), el webhook de suscripciones (MP descartaba el `notification_url`
y todo lo acreditaba el puente una hora tarde), y ahora esto. **Los tres se veían bien desde
afuera.** Ninguno rompió nunca.

De ahí sale la regla que vale la pena escribir: **una migración de tabla no termina cuando
la nueva funciona, termina cuando se grepeó `from("<tabla vieja>")` en todo el repo.** Los
que quedan apuntando a la vieja no son los que explotan — son los que siguen diciendo que
sí con las manos vacías.

Lo demás que apareció mirando reportes, todo del mismo tipo (funciona, pero sin la
categoría nueva): con el Curso de DJ se podían reservar beneficios de member —el chequeo
del server preguntaba por *cualquier* suscripción y contradecía a su propio comentario—, el
curso más caro no aparecía en el embudo ni en leads, nadie avisaba que un curso pago se
vencía con clases sin usar, y el buscador del admin no encontraba por categoría: ni
"Gold". Ninguno de esos daba error tampoco.

Y una nota de método, porque va a volver a pasar: **había otra sesión de Claude editando el
mismo repo al mismo tiempo.** Se detectó por un `git diff` con 210 líneas que yo no había
escrito. El reflejo de `git add -A` habría commiteado su trabajo a medio hacer, incluyendo
imports a archivos que ella todavía no había commiteado — build roto para todos. Se
commiteó archivo por archivo y se dejó el compartido afuera. **Antes de `git add -A`,
mirar si el diff dice algo que uno no escribió.**

---

## 05/08/2026 — Dos tablas de historial son una que miente, y las dos estaban en cero

Se cerró el circuito de ejecución de Incidencias: acciones rápidas, asignación con próximo
paso y fecha límite, y el reporte ampliado. El diseño venía escrito del 04/08
(`HANDOFF_INCIDENCIAS.md`), así que la sesión arrancó codeando. **Y el handoff estaba
incompleto en un punto que habría dolido.**

Decía: "`contact_log` tiene dos ESCRITORES, redirigilos a `incidencia_eventos`". Un grep de
30 segundos mostró que también tiene **dos lectores**, y no cualquiera: `historial()` en
`lib/workflows.ts` es la función que decide **a quién NO mostrarle en la cola de trabajo
porque ya se le escribió**. Si se redirigían sólo los escritores, el resultado no habría
sido un error: la cola habría empezado a mostrar todos los días a gente ya contactada, y
José le habría mandado el mismo WhatsApp dos y tres veces a clientes reales. Nada habría
fallado. **Cuando un handoff dice "redirigí los escritores", la pregunta que falta siempre
es quién lee.**

Dos hallazgos más, del mismo tipo:

- **El tope de 1000 filas de PostgREST volvió a aparecer, ahora en el peor lugar.** Al
  quedar UNA sola tabla de historial, la consulta de la cola pasó a leer también los
  contactos. Cortada en mil, lo que se pierde es **lo más viejo** — o sea las decisiones de
  "ya no aplica", que son justo las que impiden que alguien vuelva a la lista. No da error:
  da una lista más larga que parece correcta. Se paginó de verdad ([[postgrest-tope-1000]]).
- **La verificación escribió en producción y tuvo que dejar la base como estaba.** Las tres
  tablas están en cero, y ese cero es el dato que Facu va a mirar el 18/08 para decidir si
  el problema es de software o de adopción (Ley 9). Un script de prueba que deja cuatro
  filas adentro no rompe nada — **corrompe la medición**. `verificar-circuito.mjs` escribe,
  lee, borra, y **falla si el conteo no volvió al de partida**.

Y una decisión que vale escribir: **las 9 acciones rápidas no cierran casos.** Ninguna, ni
siquiera "pago verificado". Cerrar tiene una sola puerta y esa puerta vuelve a mirar la
base antes de dejar pasar. Dos caminos y uno sin verificación es lo mismo que ninguno
(Regla 3). Las tres acciones que casi siempre terminan en cierre **abren** el formulario
con el motivo puesto — un clic más, y ese clic sí verifica.

**Lo que no cambió, y es lo que importa:** las tablas siguen en CERO filas. El circuito
está construido, verificado y en producción, y eso no es lo mismo que usado. Se le dijo a
Facu antes de empezar y se le repite acá: **si el 18/08 `incidencias` e `incidencia_eventos`
siguen en cero, el problema es de adopción y no se escribe una línea más.**

---

## 05/08/2026 — Ctas Ctes: lo que se escribe dos veces no lo dice el saldo

Armar las cuentas corrientes del Paseo eran ~50 filas tipeadas a mano por mes en 8
pestañas. Se automatizó (`cargos_del_mes.py`) y se escribieron los alquileres de
agosto. **Escribiendo de verdad aparecieron dos bugs que en dry-run no existían**, los
dos del tipo que no avisa:

**El dedupe estaba en una punta y no en la otra.** La escritura en CARGOS chequeaba si
el cargo ya existía; la escritura en la pestaña del local, no. Correr el script dos
veces escribió agosto dos veces en Fabric, Bigg, Boss y Volta. Y acá está lo peligroso:
**el saldo de una pestaña es una cadena de fórmulas** (`=G51+E52-F52`), así que el
bloque duplicado se sumó solo al saldo del local y quedó un número perfectamente
formado, sin un error, sin una celda roja. Lo que lo detectó fue correrlo dos veces a
propósito. **Todo script que escribe tiene que ser idempotente en TODAS las tablas que
toca, no en la principal.**

**Leer el valor formateado se come los centavos.** La celda de Volta muestra `732,672`
y vale `732671,57`. `FORMATTED_VALUE` devuelve lo que se ve, no lo que hay: el alquiler
se escribió redondeado y, peor, la verificación posterior comparaba lo escrito contra
lo mostrado y daba **falso negativo en todo importe con decimales**. La primera corrida
marcó ⚠ en Fabric y Bigg cuando en realidad estaban bien. Un chequeo que grita donde no
hay problema entrena a ignorarlo (Regla 3). `UNFORMATTED_VALUE` en las dos puntas.

**Dos hallazgos del negocio, del mismo día:**

- **El reparto de expensas no es margen: es el agujero de los locales vacíos.**
  `Expensas Predio` prorratea entre los **23** locales pero sólo pagan **6**, así que el
  total repartido ($14,03M) parece superar el gasto ($12,12M). Leído rápido parece
  ganancia. Medido: se gastan $12.125.351, entran $7.081.223, y **Facu pone $5.044.128
  por mes**. Cada alta de la rampa achica esa sangría — La Jaula aporta $594.855/mes.
- **`Expensas Predio!P4` está clavado a `"mayo 2026"` literal** mientras sus nueve
  hermanas usan `A3`. Cambiés el mes que cambiés, el retiro de basura reparte mayo÷3.
  El generador lo avisa en cada corrida hasta que se arregle.

**Y un criterio que ya estaba escrito y nadie había anotado:** las liquidaciones de AVN
se cargan por **mes de pago, no por su período** — las de la carpeta "Junio 2026" dicen
período 05-2026 y suman exactamente los $2.599.309,30 cargados como junio. Cierra al
centavo, así que el criterio es ese. Igual con el ABL: de la liquidación de Tigre sólo
van a expensas la Tasa por Servicios Municipales y la Contribución Hospital; los
DERECHOS DE CONSTRUCCIÓN y el PLAN DE PAGOS FONDO Y ÁRIDOS ($25.975.011,50 en agosto)
son obra y van a Inversiones. La fórmula `D4` (`=935644+44087`) ya lo decía sola.
