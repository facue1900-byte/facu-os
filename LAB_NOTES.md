# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una entrada acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, se destila como nota en el vault.

### 2026-08-09 · FAIL ✓ · Le borré datos a Facu con mi propio verificador

Escribí dos verificadores de pantalla (`verificar-mesas`, `verificar-comisiones`) que
aprietan los botones de verdad: crean mesas, cargan pagos, arman categorías de RRPP y
después limpian. Bien pensados en todo menos en dónde: corrían sobre **la Previa de
Maceo Plex**, una fecha real, porque era la que estaba a mano cuando los escribí.

Facu estaba en esa misma pantalla cargando los escalones de comisión. Corrí el
verificador; su `limpiar()` hace `delete rrpp_categorias where event_id = <la Previa>`.
Le borró la categoría por debajo. El escalón siguiente que él cargó devolvió
`insert or update on table "rrpp_tramos" violates foreign key constraint
"rrpp_tramos_categ…"` —cortado a 90 caracteres— y me escribió: *"no me dejó cargar los
demás escalones"*. Desde su lado era un bug de la pantalla. Era yo.

**Causa raíz: no fue una carrera desafortunada, era inevitable.** Un script que borra
por `event_id` y una persona trabajando en ese `event_id` no pueden convivir. La
pregunta que no me hice al escribir el script no es "¿limpia bien?" sino **"¿de quién
son los datos sobre los que corre?"**.

Lo peor es que el script hacía todo lo demás bien: arrancaba de cero, limpiaba al final,
verificaba que no quedara nada. Toda esa prolijidad es exactamente lo que lo volvió
destructivo — un test descuidado que sólo inserta habría dejado basura, no un agujero.

**El fix:** cada verificador se crea su fecha descartable (`eventoDePrueba` en
`scripts/_pantalla.mjs`), la usa y la borra entera; nace en `draft` para que si queda
colgada no se vea en la web. Ya no hay un solo uuid de producción escrito en `scripts/`.
Regla nueva en el Playbook: *una prueba nunca escribe sobre datos reales*.

**Y el segundo error, que es de comunicación:** la pantalla mostró el error crudo de
Postgres cortado a la mitad. Aunque la causa hubiera sido otra, `violates foreign key
constraint "rrpp_tramos_categ…"` no le dice nada a nadie. Ahora `guardarTramo` chequea
que la categoría exista antes de insertar y explica que la borraron desde otro lado.

### 2026-08-10 · FAIL ✓ · Un rango válido puede pisar a otro rango válido

Facu mandó una captura de la escalera de comisiones de mesas con cuatro escalones
cargados: «0 a 2 al 10%», «3 a 5 al 12%», **«4 a 99999 al 20%»** y «6 a 8 al 14%».
Con 4 mesas vendidas hay dos escalones que dicen cosas distintas, y lo que se paga sale
del orden en que se recorren: `tramoDe` ordena por `desde` y devuelve el primero que
matchea, así que cobra 12%. **La comisión la decidía un `sort`, no un trato.**

**Causa raíz: la validación era completa por escalón y ciega al conjunto.**
`guardarTramo` chequeaba que el `hasta` fuera mayor que el `desde` y que el % estuviera
entre 0 y 100 —los dos chequeos correctos— y nunca leía los escalones que ya estaban. Un
rango bien formado puede solapar otro rango bien formado, y ninguna validación local lo
ve. Es el mismo modo de falla que un `check` de columna que no puede ver la tabla.

**El fix no fue validar el «desde»: fue dejar de preguntarlo.** La pantalla lo calcula
(`proximoDesde` = el número siguiente al último cargado) y lo muestra fijo, con la forma
de un dato y no de un input (`.hj-fijo`). Un campo que no se puede escribir mal no se
escribe mal. `validarEscalon` lo verifica igual del lado del servidor, porque un
`<input>` se edita con las herramientas del navegador. La regla, dicha por Facu: *"siempre
se debe respetar lo que se puso primero"* — así la escalera queda continua y sin huecos
por construcción.

**Lo ya cargado no se borra solo: se marca.** Los solapes que entraron antes se están
pagando, y borrarlos es una decisión de plata de Facu. `escalonesPisados` los detecta y la
fila sale en rojo con «se pisa con el de arriba». Y el `99999` que él usaba para decir
"infinito" ahora se nombra: `hasta` vacío es «de acá en adelante», y la nota lo dice.

**Efecto colateral que enseña algo:** con el «4 a 99999» cargado, `proximoDesde` propone
**100000**. El número absurdo delata el dato absurdo — es preferible a proponer 9 y
esconder que hay un escalón que llega a 99999.

Tests: `npm run test:comisiones` (bloques 6, 7 y 8, con el caso textual de la captura) y
`npm run verificar:comisiones` (bloque 5b, apretando los botones).

### 2026-08-10 · FAIL ✓ · Comunicar el resultado por la URL es lo que scrollea la pantalla

Facu, dos veces en el mismo mensaje: *"cuando aprieto guardar me manda de vuelta todo para
arriba y la información aparece abajo"* y *"no quiero que al apretar un botón de guardar me
mueva de lugar; quiero que se mantenga donde estoy"*.

El 09/08 esto se había "arreglado" agregando un `#ancla` al destino del `redirect()`. Mejoró
el aterrizaje y **no resolvió el problema**, porque el ancla igual reposiciona la pantalla.

**Causa raíz: las acciones comunicaban el resultado por la query string** (`&ok=tramo`,
`&e=<motivo>`). Eso obliga a `redirect()`, `redirect()` navega, y navegar mueve el scroll.
El scroll era el síntoma; el diseño del canal de vuelta era la causa. Las acciones que se
aprietan repetido —cargar escalones, asignar cupo de cortesías fila por fila— ahora
**devuelven** `{ok, msg}`, el `revalidatePath` refresca la tabla en el lugar y el mensaje lo
muestra un componente cliente con `useActionState`. Sin navegación, el navegador no mueve
nada. Las de crear/borrar categoría siguen redirigiendo a propósito: ahí sí cambia qué se
está mirando.

Aparte, el botón «Abrir» de una categoría era un `<Link>` sin `scroll={false}`: Next
scrollea al tope al navegar, y abrir una categoría dejaba la pantalla arriba con los
escalones fuera de la vista. Ese era el "me manda para arriba y la información aparece
abajo", literal.

**Lo que rompió y hay que recordar: el arnés de pruebas de pantalla sólo conocía un
protocolo de form.** Next tiene dos: `<form action={serverAction}>` manda un único
`$ACTION_ID_<hash>`, y `<form action={deUseActionState}>` manda `$ACTION_REF_n`,
`$ACTION_n:0` (id + bound), `$ACTION_n:1` (el estado previo) y `$ACTION_KEY`.
`apretar()` en `scripts/_pantalla.mjs` buscaba sólo el primero, así que el POST llegaba sin
la referencia, **la action no corría**, y el verificador reportaba "no se cargó el escalón"
con la pantalla andando bien. Ahora copia todos los hidden que arrancan con `$ACTION` y
des-escapa las entidades HTML del JSON — que es lo que hace el navegador, y funciona con
los dos protocolos sin saber cuál es cuál.

**Y un test que pasaba de casualidad:** la marca `name="pct"` identificaba "el formulario de
agregar escalón", pero hay dos —entradas y mesas— y `apretar` toma el primero. Todo el
bloque de mesas le pegaba al de entradas y daba verde. Ahora la marca es `value="mesas"`.
Un test que acierta por casualidad es peor que uno que falla.

### 2026-08-09 · FAIL ✓ · La tabla estaba cerrada y la vista era la puerta

Tercera vez que cae el mismo método, un mes después de la auditoría del 08/08. Iba a
construir la pantalla de mesas de Dominé; antes de escribirla probé la superficie de la
base, que es lo que aquella auditoría dejó como regla.

`mesas` estaba impecable: RLS prendida, sin policies, y con la anon key PostgREST
devolvía `[]`. Verificado así el día que se creó, y por eso la memoria decía "las cinco
tablas con RLS prendida y sin policies", en pasado y con razón. **La vista sobre esa
misma tabla, `mesas_estado`, devolvía la fila entera**: titular, teléfono, precio y
saldo.

**Causa raíz — dos defaults que se combinan y ninguno es un error de nadie:**

1. Una vista de Postgres corre con los permisos de su **dueño**, no con los del que
   consulta. La RLS de las tablas de abajo **no se aplica**. Es el default: hay que
   pedir `security_invoker = on` explícitamente, y el `.sql` que creó las mesas no lo
   pedía porque nadie sabe lo que no sabe.
2. Supabase trae un *default privilege* que le da `select` a `anon` sobre **cada tabla
   y vista nueva de `public`**. Así que la vista nace publicada como endpoint.

Juntas convierten toda vista en una API pública. Y la anon key viaja en el bundle del
navegador: no hacía falta ninguna cuenta.

**No era sólo mesas.** Las **ocho** vistas del proyecto estaban abiertas. Medido con
curl antes de tocar nada — contando filas, porque un `[]` de hoy es una fuga de mañana:

```
pagos_por_persona          40 filas   nombre y apellido + cuánto pagó cada alumno
payment_links_pendientes  397 filas   nombre en el concepto + monto de cada pago
ticket_batch_stats          8 filas   cupo y disponibles de cada tanda
evento_aportes              3 filas   quién puso plata en una fecha y cuánta
evento_resultado            2 filas   ingresos, egresos y resultado por fecha
mesas_estado                1 fila    titular, contacto, precio y saldo
domine_fijos / v_reprogramaciones_mes  vacías hoy — filtraban igual
```

**El fix** (`supabase/vistas_no_se_publican.sql`, aplicado por la Management API):
`security_invoker = on` en las ocho, `revoke all … from anon, authenticated`, y
`alter default privileges … revoke all on tables from anon` para que la próxima vista
nazca cerrada. Las ocho se leen sólo del servidor con el service role —verificado
grepeando: cada `from("<vista>")` cuelga de `createAdminClient()`— así que no rompió
nada. Después: 401 con la anon key, y el service role sigue leyendo las 40 y las 397.

**Lo que queda para que no vuelva:** el chequeo `[8]` de `scripts/seguridad-valores.mjs`
le **pega** a cada vista con la anon key y exige 401 — un 200 con `[]` no alcanza. La
lista sale de los `create view` de `supabase/`, así que una vista nueva entra sola.
Probado rompiéndolo a propósito: con el `grant` puesto, falla.

**La lección de método, que es la que importa.** Las tres veces el código de la app
estaba bien y la superficie paralela estaba abierta: funciones RPC (08/08), columnas que
RLS no filtra (08/08), vistas (hoy). La pregunta "¿está protegida la tabla?" no cubre
"¿qué más publica PostgREST que apunte a esa tabla?". **Al crear un objeto nuevo en
`public` —tabla, vista o función— se le pega con la anon key y se cuenta lo que
devuelve.** Leer el `.sql` no sirve: los dos defaults que causaron esto no están
escritos en ningún archivo del repo.

De paso apareció un chequeo podrido: el de `beginSubscription` seguía exigiendo
`EN_VENTA.includes(planId)` cuando el código había pasado a `COMPRABLES` hace días. El
código estaba bien y el test viejo, y venía fallando sin que nadie lo mirara. Ahora
prueba la garantía —hay lista blanca, y `test` y `modopro` están afuera— y no el nombre
de la constante.

### 2026-08-08 · Auditar la aplicación no audita la base: la reja estaba bien y la pared no llegaba al techo

Auditoría de seguridad completa de `astronomy-members` (44k líneas, 12 APIs, 45 archivos de
acciones, 51 pantallas admin). El diagnóstico salió muy bien: RLS activo en las 71 tablas,
cero secretos en el bundle del navegador, ningún `.env` en la historia de git, el webhook de
MP validando HMAC y re-preguntándole a MP en vez de creerle al pedido, las 51 pantallas de
admin protegidas una por una. **Cero vulnerabilidades críticas.**

Y estaba mal. Lo crítico apareció después, remediando, cuando Facu preguntó una cosa que yo
no me había preguntado: **"¿puedo llamar directamente a las APIs sin pasar por la UI?"**

Sí se podía. PostgREST publica **cada función del esquema `public`** como
`/rest/v1/rpc/<nombre>`, y el default de Postgres es `EXECUTE` para PUBLIC. Las 15 funciones
del sistema son `SECURITY DEFINER`, o sea que corren por encima de RLS. Con la sola `anon key`
—la que viaja en el navegador— y **sin ninguna sesión**, comprobado contra producción:
`user_id_by_email` devolvía el uuid de cualquiera por su mail, `credit_balance` su saldo
(3390), `lista_de_puerta` la lista de asistentes con nombres, y `check_in_ticket` quemaba la
entrada de otro. Sin ejecutarlas porque movían plata real: `grant_credits(p_user, p_amount…)`
y `pay_ticket_order(...)` estaban a un POST de regalar créditos y entradas.

**La causa raíz no fue una reja mal escrita.** `app/actions/puerta.ts` verifica cuenta,
permiso `validate_tickets` y una cookie firmada con HMAC timing-safe antes de llamar a
`check_in_ticket`. Está bien hecho. El problema es que auditar las server actions **muestra
las puertas y no muestra que la pared de al lado no llega al techo**: hay una superficie
paralela —PostgREST— que el código de la app no menciona en ningún lado.

El mismo error de método, dos veces más:

- **RLS filtra filas, no columnas.** `profiles` tenía la política correcta y el `GRANT` de
  UPDATE sobre las 7 columnas: un alumno se sacaba la suspensión y se marcaba `es_interno`
  —o sea se borraba de la cobranza y de las métricas— desde la consola, sin dejar rastro.
  Leer la política y darla por buena no alcanza: hay que leer el `GRANT`.
- **Un permiso que se verifica pero no está en el catálogo no es un agujero: es peor.**
  `validate_tickets` se exigía y no se podía otorgar, así que el 16/10 con cola en la puerta
  la salida iba a ser repartir `is_master`. Una verificación que nadie puede satisfacer
  fabrica la escalada que quería evitar.

**Lecciones, en orden de valor:**

1. **Preguntar por la superficie DIRECTA de cada cosa que se da por protegida.** No "¿quién
   llama a esto?" sino "¿qué pasa si le pegan sin pasar por acá?". Las tres las encontré
   atacando de verdad con `curl`, no leyendo código — y el código lo había leído entero.
2. **Una auditoría de aplicación y una de plataforma son dos trabajos.** Los GRANTs de
   EXECUTE, los de columna y los defaults del motor no aparecen en ningún `grep`.
3. **La falta de configuración tiene que CERRAR.** Apareció tres veces: `if (secret)` en los
   4 crons, `|| ""` en la firma de la cookie de la puerta, `sin-secreto` en el webhook. Un
   error de configuración no rompía nada visible, sólo sacaba la reja.
4. **Contar filas no es contar hechos.** `webhook_hits` guarda un golpe por notificación y MP
   reintenta: leí "7 pagos fallidos" donde había **un pago de prueba reintentado 7 veces**, y
   "13 rechazados" donde había **4**. Se lo reporté a Facu antes de verificarlo. Es la regla 2
   de la Constitución al revés — un resultado *grande* también es un error hasta que se
   demuestre lo contrario, cuando la unidad de la fila no es la unidad del hecho.

**Fixes**, todos verificados atacando antes y después: `revoke execute` en las 15 funciones ·
`revoke update/insert` en `profiles` · `lib/cronAuth.ts` fail-closed en los 4 crons ·
`validate_tickets` al catálogo y a `PERMISOS_ACOTADOS` · `check_in_ticket` distingue las
entradas de prueba (y `lista_de_puerta` también, o el modo offline lo salteaba). Los chequeos
que impiden la regresión están en `scripts/seguridad-valores.mjs`, y la regla quedó en el
`CLAUDE.md` del repo.

**Lo que quedó abierto a propósito:** los `merchant_order` se rechazan por firma 4 de 4 —no
se pierde plata porque el `payment` gemelo acredita, pero es un mecanismo de seguridad
rechazando tráfico legítimo, y no se toca hasta poder reproducirlo— y el panel cuenta
webhooks en vez de pagos.

### 2026-08-08 · La puerta rechazaba a quien pagó, y el escáner se moría con una raya

Segunda tanda del mismo día, en `/puerta`. Salí a verificar qué le hacía a la puerta el
`revoke execute` que otra sesión aplicó a las funciones `SECURITY DEFINER`. El revoke está
bien —lo verifiqué contra la base, no contra el código: `service_role` conserva `EXECUTE` en
las 5 funciones de la ticketera y `anon`/`authenticated` la perdieron— pero mirando ese
camino aparecieron **tres agujeros propios**, los tres invisibles hasta la noche del 16/10.

**1. El escáner se moría con una raya de señal.** `navigator.onLine` dice que hay RED, no que
haya INTERNET. Con señal débil la server action rechaza, `resolver()` tiraba, el veredicto
nunca aparecía — y como la pausa del escáner **se suelta tocando el cartel del veredicto**,
sin cartel no había forma de soltarla: la cámara seguía prendida y no leía nada más, hasta
recargar. El escenario exacto de Native Beach Club.

**2. "NO EXISTE" en rojo para gente que pagó.** `if (error) return { result: "invalido" }`
metía en el mismo cartel tres cosas del *teléfono* —sesión vencida, cookie vencida, error de
la base— disfrazadas de veredicto sobre *la entrada*. Si el revoke de la otra sesión hubiera
errado un grant, **todas** las entradas válidas decían NO EXISTE sin un solo error a la
vista. Detalle completo en la memoria `un-error-no-es-un-veredicto`.

**3. El cartel se salía de la pantalla, y venía así desde antes.** Medí en el navegador con
la Montserrat de producción: a `13vw` en 393px entran 329px, o sea **9 caracteres**.
`OTRA FECHA` (10) y `FUERA DE HORA` (13) estaban cortadas desde siempre y nadie las había
visto **porque son los dos casos que todavía no pasaron en una fecha real** — el 16/10, con
una tanda que corta a las 20:00, `FUERA DE HORA` va a aparecer un montón.

Y acá me comí dos veces la misma trampa de medición. Primero le reporté a la otra sesión que
`ENTRADA DE PRUEBA` desbordaba (era cierto). Después "vi" desbordar dos textos que en
realidad entraban: **Chrome headless maqueta a 500px aunque `--window-size` diga 393 y la
captura salga de 393**, así que `13vw` se calculaba sobre 500 y todo se veía cortado. Lo
resolví midiendo con canvas y la fuente real, y renderizando **dentro de un iframe de 393px**,
que es lo único que hace que `vw` valga lo que vale en el teléfono. Lección: una medición en
el navegador vale por el **viewport que el navegador realmente usó**, no por el que le pediste
— hay que imprimir `document.documentElement.clientWidth` en la propia captura.

El arreglo de fondo no es el umbral de 9 caracteres: es `overflow-wrap: anywhere` en el
cartel, que hace imposible que un texto futuro se corte sin que nadie mida nada.

### 2026-08-08 · Un chequeo de "esto no se toca" que pasaba porque nada lo tocaba

La puerta de la ticketera (`/puerta`) tenía modo offline pero **no service worker**: si el
de la puerta recargaba sin señal, no abría nada. Lo construí (`public/puerta-sw.js`) con un
verificador que lo carga con caché y red de mentira (`npm run verificar:puerta`, 25
chequeos). El primero de todos era el más importante: **un service worker jamás puede
tocar un POST**, porque las server actions de Next —validar un código, abrir la fecha— son
POST a la misma URL. Si las intercepta, la puerta deja de validar CON señal, que es el
caso normal.

Verde. Después, por costumbre, saqué el filtro por método a propósito para ver si el
chequeo lo agarraba: **seguía verde.** El POST no pasaba derecho por estar protegido, sino
porque ninguna de las tres ramas del `fetch` lo agarraba: no era navegación, no era
`/_next/static/`, y `/puerta` no termina en `.js`. **El chequeo probaba una coincidencia,
no una protección.**

Y buscando el POST que sí caería en una rama apareció un caso real que no había pensado:
un `<form>` con server action tocado **antes de que la página hidrate** —3G en la puerta,
pasa— se manda como POST de **navegación**, y eso sí cae en la rama de la página. Con señal
se habría comido la respuesta de la acción; sin señal habría contestado el escáner guardado
como si la fecha se hubiera abierto. Mismo agujero para `/api/qr/E-000043.png` (termina en
`.png`: cae en la rama de archivos) y para las tapas `.jpg` de Supabase (otro dominio).

Causa raíz: **un chequeo de que algo NO pasa no vale nada si el caso de prueba no tiene la
forma exacta que caería en la trampa.** Verde por ausencia de coincidencia se lee igual que
verde por protección.

Los 6 mutantes que probé después caen todos: sin filtro de método, sin filtro de `/api`,
sin filtro de origen, guardando cualquier HTML, sin borrar lo guardado al cerrar la fecha,
y caché-primero en vez de red-primero. Quedó como método fijo en el Playbook §4.

### 2026-08-07 · El archivo que lleva el nombre de la función no tiene su última versión

Carrito de la ticketera: `create_ticket_order` pasaba de vender un nivel a vender varios.
Abrí `supabase/ticketera_checkout.sql` —el archivo que la crea, el que se llama como el
tema— y reescribí la función a partir de esa versión. Compiló, se aplicó, devolvió `[]`.

**Tres features desaparecieron sin que nada fallara.** `ticketera_visibilidad.sql`, una
migración posterior, había hecho su propio `create or replace` de la MISMA función y le
había agregado las guardas de tandas `hidden`/`rrpp_only` y el modo prueba entero. Mi
versión, escrita sobre la vieja, las borró: una tanda escondida pasaba a venderse sola por
la web, y **el modo prueba habría cobrado $50.000 reales en vez de $1**. La ticketera
seguía vendiendo perfecto — sólo que tres reglas ya no existían.

Lo agarró `verificar:ticketera` con 6 chequeos en rojo, antes de tocar producción.

Y adentro del mismo cambio, la misma clase de silencio otra vez: el `drop function if
exists` llevaba 14 tipos y la función vieja tiene 15. **Un drop que no matchea no borra
nada y no avisa** — quedaron las dos versiones vivas al mismo tiempo, que es exactamente
el "function is not unique" contra el que advertía el archivo original. El `[]` de la
Management API decía que el SQL corrió, no que hubiera hecho algo.

Causa raíz: **en un directorio de migraciones, el nombre del archivo dice cuándo NACIÓ una
función, no dónde está su última versión.** Con 90 archivos en `supabase/`, la que manda es
la última que la reemplazó, y no hay nada en el nombre que lo diga.

Lo que se lleva, y va como chequeo fijo: antes de reescribir un `create or replace`,
**`grep -l "function public.<nombre>" supabase/`** y partir del último, no del primero. Y
después de aplicar un `drop`+`create`, **contar cuántas quedan** en `pg_proc` — la firma
del drop se escribe contando los tipos, uno por uno.

### 2026-08-07 · El chequeo que falló tenía razón dos veces, por causas opuestas

Se construyó el **Design Engine** de la ticketera (`astronomy-members`, `618fbac`): saca la
paleta de cada fecha del flyer y la refina. Al correr el verificador por primera vez, 2 de
23 chequeos en rojo, los dos por milésimas. La tentación obvia —y equivocada— era la misma
para los dos: subirle el umbral al chequeo y seguir.

Eran **dos causas distintas**, y sólo una era del código.

1. *"Ningún acento pasa el techo de saturación"* falló con `.1460` contra un techo de
   `.145`. Ahí el **chequeo estaba mal**: el motor calcula en flotante pero la pantalla
   tiene 256 escalones por canal, así que el color que realmente se pinta nunca es
   exactamente el pedido. Medir el hex redondeado contra el ideal es medir el redondeo.
2. *"Los fondos siguen siendo neutros"* falló con croma `.0124`. Ahí el **código estaba
   mal**: yo había puesto el croma de las superficies **constante**, y el mismo croma se ve
   más fuerte cuanto más clara es la superficie — o sea que el teñido crecía justo en las
   áreas más grandes de la pantalla. Se bajó la constante.

Y hubo una tercera trampa dentro de la misma medición: en un fondo casi negro **el croma de
OKLCh es puro ruido de cuantización** (`#070403` y `#050505` están a 2 unidades de canal y
dan `.0124` vs `.0000`). Medir "esto sigue siendo neutro" por croma ahí hace fallar al motor
por algo que ningún ojo ve. Se cambió por la **separación entre canales R/G/B**, que es la
definición operativa de "esto es un gris" y no se descompone cerca del negro.

Lo mismo pasó con la primera captura de pantalla: mostraba el contenido cortado a la
derecha. Podría haberse "arreglado" el CSS. Medido en el navegador, el desborde real a 390px
era **0**: headless sin emular cae a un viewport de 980 y recorta la imagen a la ventana. El
bug era del instrumento.

Lo que se lleva: **la regla 3 —no parchear alrededor de un chequeo que falla— no dice que el
chequeo siempre tenga razón. Dice que hay que averiguar cuál de los dos está mal.** Tres
veces en la misma sesión el rojo vino del instrumento y no del sistema, y las tres veces la
única forma de saberlo fue entender qué se estaba midiendo. Un umbral que se mueve para que
el test pase es un test que se apagó; un umbral que se mueve **porque medía la cosa
equivocada** es un test que recién ahora sirve — y la diferencia sólo se ve escribiendo por
qué.

### 2026-08-06 · Cambié una regla en un script y otros dos siguieron diciendo lo viejo

Facu fijó cuatro reglas de cobro nuevas del Paseo: «Escuelita» eran dos cobradores (Beto y
Meta), La Jaula pasa a cobrarse $372.644 en agosto, y de septiembre en adelante sale del
precio semestral de `Futbol!AR`. Se aplicaron en `deuda_efectivo.py`, se verificó la tarjeta
de Mati contra el bundle en vivo y se dio por cerrado.

**Estaba a medias y nada falló.** Las mismas reglas estaban copiadas y pegadas en
`radar_deudores.py` y en `exportar_ctas_ctes.py`. Media hora después, corriendo el radar por
otra cosa, apareció el resultado real: la tarjeta de Mati decía **$372.644** y el radar, en
la misma máquina y sobre la misma planilla, seguía diciendo *«La Jaula: se le cobra recién
desde agosto 2026 (tenía saldo a favor)»* — sin monto. Y `exportar_ctas_ctes.py`, que
alimenta la pestaña **Deuda** de la app, lo mismo. Ninguno de los tres tiró un error: cada
uno era internamente coherente con su propia copia.

Causa raíz: **un `dict` de reglas de negocio duplicado en tres archivos.** No hay chequeo
posible que lo agarre, porque no hay nada roto que testear — hay tres verdades. Fix:
`scripts/reglas_locales.py` con `REGLAS`, `PAGAN_POR_BANCO`, `PAGAN_ADELANTADO`,
`SIN_PESTANA` y `JAULA_AGOSTO`, importado por los tres. Verificado que el refactor no mueve
ningún número: `deuda_efectivo` sigue dando $6.659.073,11 y el export, exigible
$2.302.497,48 sobre 8 locales.

Lo que se lleva: **la regla 12 no se cumple sola por escribirla.** Antes de tocar una
constante de negocio, `grep` del nombre en todo el skill — si aparece en más de un archivo,
el trabajo no es cambiarla, es unificarla. Y el descubrimiento no vino de una revisión, vino
de correr *otro* comando y leer el output completo: si el radar no se hubiera corrido ese
día, la app y el reporte iban a contradecirse durante semanas.

### 2026-08-06 · La hipótesis anotada era falsa, y el arreglo escrito no hacía nada

Dos bugs de `/label` en `astronomy-members`, distintos, con la misma moraleja: **lo que está
escrito en el código no es lo que el navegador ejecuta, y la única forma de saberlo es
medirlo.**

**1 · El hero que se iba solo al pie.** El 05/08 se revirtió `components/label/HeroCta.tsx`
porque en el teléfono de Facu la página *"de la nada se va todo para abajo"*. Quedó anotada
una hipótesis: el `history.replaceState` dejando `#demos` en la URL y algún re-render
volviendo a saltar al ancla. **Era falsa** — 16 s de página quieta en producción con el hash
puesto, cero saltos.

La causa real: `app/globals.css` tiene `html{scroll-behavior:smooth}`, y **la forma de dos
argumentos `window.scrollTo(0, y)` hereda esa curva**. El bucle de `requestAnimationFrame`
no fijaba la posición: disparaba una animación suave nueva por frame, que se pisaban entre
sí. Medido en emulación de iPhone: durante el segundo entero la página avanzaba 10 px por
frame y quedaba en **339 de 1806 px**; recién cuando el bucle terminaba, la última animación
—ya sin nadie que la interrumpiera— la mandaba al pie en 570 ms. El movimiento llegaba
cuando Facu ya había soltado el dedo. Fix: `behavior: "instant"`, lo único que ignora el
CSS, más cancelación por `touchstart`/`wheel`/`pointerdown`/`keydown` y un solo bucle a la
vez.

De paso apareció otro: `stopPropagation()` **no** saca del medio al listener de
`components/SmoothScroll.tsx`, porque React delega los eventos en `document`, que es el
mismo nodo donde ese listener vive. Eran dos `lenis.scrollTo` por un solo clic — medido
espiando el método. Se resolvió con una marca en el elemento (`data-scroll-propio`).

**2 · El ES/EN que el eclipse tapaba en la vista de compu.** `.lb-bar` tenía
`z-index: 2` **escrito, comentado y sin efecto**: la regla genérica
`.theme-label > *:not(.lb-atmos)` pesa (0,2,0) —`:not()` suma la especificidad de su
argumento— y le ganaba a la clase pelada de (0,1,0). La franja quedaba en el z-index base,
el mismo que el hero, y a igual altura pinta último el que viene después en el DOM. El
computado daba `1`. Fix: `.theme-label > .lb-bar { z-index: 2 }`, que empata el peso, en vez
de un `!important` que habría tapado el agujero sin dejarlo a la vista (regla 3).

**Trampa de método que costó un rato:** `elementFromPoint` decía "no está tapado" porque el
eclipse es `pointer-events: none`. Tapado *para el clic* y tapado *para el ojo* son dos
preguntas distintas; la segunda se contesta con el `zIndex` computado o con una captura.

**Lo que queda para la próxima.** Reproducir antes de arreglar valió exactamente lo que
costó: la hipótesis anotada era plausible y estaba equivocada, y arreglarla no habría movido
nada. Se manejó Chrome headless por CDP sin instalar dependencias (Node 24 ya trae
`WebSocket`), envolviendo `window.scrollTo` para registrar *qué se pidió* contra *qué pasó*
— ahí se vio el desfasaje de un saque. **Falta la verificación que desde esta Mac no se
puede hacer: abrirlo en el iPhone de verdad**, que es justo donde el bug pasó desapercibido
la primera vez.

Commit `14cffa7`. Detalle en la memoria: «scroll».

### 2026-08-05 · Un cron le iba a vaciar la cola a José a las 9 de la mañana

Se agregó a `astronomy-members` el detector de **checkouts trabados**: 5 alumnos que
abrieron el checkout y Mercado Pago frenó en SU pantalla, $846.080/mes que no aparecían en
ninguna de las 36 pantallas del panel. La fuente natural es `subscriptions.status =
'pending'` — la fila la escribe nuestro propio checkout justo antes de mandar a MP.

**Lo que casi pasa:** el mismo día se había puesto en producción `cerrarCheckoutsZombie`,
un barrido que corre con el cron diario de las 09:00 ART y **cancela los checkouts
abandonados de más de 7 días**, pasando la fila a `cancelled`. Cuatro de los cinco casos
tenían más de 7 días encima. A la mañana siguiente el detector iba a mostrar 1 en vez de 5,
**$574.080 desaparecidos**, y el panel lo iba a presentar como *"se apagó solo"*.

**Causa raíz: un detector no puede colgarse de un campo de estado que otro proceso pisa.**
Un problema que se apaga porque el dato de fondo se arregló no puede mentir; uno que se
apaga porque un cron cambió el campo que el detector mira, miente siempre. Y acá el caso ni
siquiera se cierra cuando muere el link: **empeora**, porque desde ahí la persona no puede
pagar ni queriendo.

**Fix:** el barrido deja el intento escrito en `audit_log` (`checkout_abandonado`, historia
inmutable) y el detector lee las **dos puntas** —la fila viva y el renglón del log— armando
**la misma clave** (`alumno:producto:día del intento`). Si la clave cambiara, el caso
resucitaría con otra identidad y perdería lo que alguien ya decidió sobre él.

**Dos cosas que salieron de probarlo.** Probarlo de verdad exigía cancelar links reales en
Mercado Pago (regla 10), así que se hizo con un cliente de mentira —
`npm run verificar:trabados`. Ese chequeo encontró un **error real que la revisión a ojo no
vio**: la ventana se medía desde el renglón del log y no desde el intento, así que un
checkout de hace tres meses cerrado ayer entraba a la cola como si fuera nuevo.

**Lo transferible, en una pregunta:** *antes de que un detector lea un campo de estado,
¿quién más escribe ese campo y cuándo?* Es la misma familia que el detector que leía lo que
escribía su propia acción (04/08) — ahí se pisaba a sí mismo, acá lo pisa un cron.

### 2026-08-05 · El bug sobrevivió porque la parte que fallaba no era nuestra

José reportó un lead que al ir a pagar recibe *"tu e-mail no coincide"* y termina
preguntando si puede transferir. Facu lo leyó como un error de la web y propuso la
solución que suena obvia: dejar de usar el mail como identificador de pago y manejar un
ID único por usuario.

**Ese ID ya existía y ya era el identificador de pago.** `external_reference =
"<userId>:<planId>"` viaja en cada preapproval y el webhook atribuye por ahí
(`resolveUser`, prioridad 1), nunca por mail. `user_emails` ya permitía varios mails por
persona. O sea: la mitad del sistema que Facu quería construir estaba construida, andando,
y **no tenía nada que ver con el error**.

**Causa raíz: `payer_email` es obligatorio en `POST /preapproval` y Mercado Pago ATA la
suscripción a la cuenta de ese mail.** El que abre el checkout logueado en MP con otra
cuenta es rechazado por MP. El chequeo corre en el servidor de Mercado Pago: ningún
identificador nuestro lo puede pisar. Nosotros mandábamos siempre el mail del registro, y
el Mercado Pago del alumno suele estar a nombre del padre, de la madre o de una empresa —
que es la convención de identidad que ya teníamos escrita desde julio y nadie conectó con
el cobro.

**Lo que dejó pasar el diagnóstico equivocado: NO HABÍA ERROR QUE MIRAR.** Un
`checkout_error` sólo se escribe si MP nos rechaza a NOSOTROS al crear el preapproval. Acá
el preapproval se crea perfecto (HTTP 201, con `init_point`), y el rechazo pasa después,
en la pantalla de MP, donde no tenemos telemetría. Medido: **8 checkouts `pending` sin
completar y CERO `checkout_error`.** Cinco de personas reales, $846.080/mes de cuotas que
nunca aparecieron en ningún tablero. La única evidencia de que alguien quiso comprar y no
pudo era una fila `pending` que había escrito nuestro propio checkout treinta segundos
antes — el dato estaba, nadie lo leía.

**La lección transferible: cuando el síntoma es "el usuario no puede", preguntar quién
ejecuta el chequeo que falla.** Si lo corre un tercero, rediseñar nuestro modelo de datos
no lo toca. Lo que hay que cambiar es **qué le mandamos** a ese tercero.

**Y la segunda: un embudo sin telemetría en el último tramo miente por omisión.** El panel
decía que todo andaba porque sólo sabía contar lo que había fallado de este lado. La
pregunta que lo destapa no es *"¿hay errores?"* sino *"¿hay intentos que no terminaron?"*.

**Lo que se hizo** (commit `92645a6` de `astronomy-members`, en producción):

1. `profiles.mp_email` — el alumno declara con qué mail entra a Mercado Pago en
   `/pagar/mail`, y el checkout se reabre con ése. Lo usan los tres `preapproval`:
   membresías, Curso de DJ y Modo Profesional en cuotas.
2. **Ese mail NO atribuye pagos.** No se guarda en `user_emails`, que sí atribuye
   (prioridad 2 de `resolveUser`): si el alumno pudiera escribir esa tabla, cargar el mail
   de otra persona alcanzaría para quedarse con sus cobros. La atribución sigue colgando de
   `external_reference`, que lo escribe el servidor.
3. `lib/checkoutTrabado.ts` — la fila `pending` con más de 20 minutos es la evidencia, y el
   panel del alumno le ofrece la salida. Se calla si ya pagó, y **no** se calla porque
   tenga otra suscripción viva: el que ya es Silver y se traba subiendo a Platinum está
   igual de trabado y es el que más plata deja sobre la mesa.
4. `lib/checkoutsZombie.ts` — un preapproval `pending` es un link que **no caduca nunca** y
   queda atado a un mail; de ahí sale la otra mitad de los *"no coincide"*, cuando alguien
   reabre un link viejo o reenviado. Se cierran a los 7 días desde el cron diario, primero
   en MP y sólo después la fila nuestra. La ventana está acoplada a propósito a la del
   cartel: barrer antes sería sacarle la salida al que la está viendo.

**Una trampa de verificación, de regalo.** El verificador falló en su primera corrida con
HTTP 500 al crear un preapproval, y la hipótesis inmediata —"es el dominio inventado del
mail de prueba"— era **falsa**: la corrida siguiente aceptó ese mismo dominio con 201. Es
la falla por casilla de MP, intermitente, ya documentada desde el 01/08. Quedó escrito en
el script para que un 500 ahí no se lea nunca más como "el arreglo no sirve" — las ramas
que prueban el fix no dependen de MP. `npm run verificar:mail-de-pago`.

**CIERRE (05/08/2026, mismo día).** Se probó con plata real dos veces y quedó prendido en
producción (`MP_LINK_PERSONAL=1`). La primera prueba pasó la atribución —Facu pagó desde
`facue1900@gmail.com` un link que pertenecía a otra cuenta y el pago cayó donde debía— pero
**imprimió `suscripción: ninguna` como un simple mensaje en pantalla, no como un chequeo.**
Ese renglón era el bloqueante: sin la fila de `subscriptions`, un cambio de plan no da de
baja el plan anterior y el alumno paga DOS suscripciones. Se vio de casualidad.

**La lección concreta: un dato cuyo modo de falla cuesta plata no puede ser decorado.** Pasó
a ser cuatro aserciones, y la segunda prueba las pasó todas. Es la misma forma del error que
esta Lab Note describe arriba —el sistema contestando "ok" mientras algo faltaba— y reapareció
dentro de la propia herramienta escrita para detectarlo.

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

---

## 05/08/2026 — Las expensas entraban a CARGOS y nunca a la pestaña del local

**Lo que estaba roto.** `filas_para_pestania()` armaba el bloque de la pestaña con una
sola línea de filtro: `per == f"{anio}-{mes:02d}"`. Pero un bloque de cobro son **dos
períodos** — las expensas del mes M más el alquiler del mes M+1. Filtrando por el mes
del alquiler, las expensas quedaban afuera: entraban a `CARGOS` (esa función no filtra)
y **nunca llegaban a la pestaña del local**.

Y el saldo del locatario sale de la pestaña, no de CARGOS: es la cadena
`=G{n-1}+E{n}-F{n}`. O sea que **la expensa no se le reclamaba a nadie**. Pasó en los
bloques `JUL'26` y `AGO'26` de Fabric, Bigg, Boss y Volta: sólo tenían alquiler, mientras
`JUN'26` tenía alquiler + Recupero + Servicios Comunes + IVA. Dos meses de expensas sin
reclamar.

**Por qué no avisó — el patrón que hay que reconocer.** El script decía
`✅ verificado: las filas están en CARGOS` y después
`· Fabric: AGO'26 ya estaba en su pestaña — no escribo nada`. Las dos frases eran
ciertas. La verificación miraba la tabla donde el dato **sí** había entrado, y el dedupe
confirmaba que el bloque existía sin preguntarse si estaba **completo**. Un chequeo que
sólo mira la tabla principal no protege a la secundaria — es la misma lección del bloque
duplicado, del otro lado: aquella vez sobró, esta vez faltó.

**El IVA ya estaba calculado y se tiraba.** La propuesta es
`(local, período, concepto, monto, iva)` y la función lo desempacaba como `_iva` para
descartarlo, recalculando después sólo el de Alquiler. Por eso tampoco salía la fila
`IVA Servicios Comunes`. Ahora sale de la propuesta: el que ya resolvió qué lleva IVA
es quien tiene que decirlo.

**El error propio, y cómo se encontró.** El primer arreglo escribió las expensas de
julio bajo la etiqueta `AGO'26` — razonando desde el docstring ("bloque = expensas de M
+ alquiler de M+1") en vez de desde la planilla. Mirando `JUN'26` de Fabric se ve que
tiene el recupero de **junio** (período 2026-06 en CARGOS, $846.539,07): la columna se
llama **"Mes Origen"** y lleva el período del cargo, no el del bloque. Cada fila viaja
ahora con su propia etiqueta, y el dedupe pasó a ser por el par **(mes, concepto)** —
porque un bloque trae dos meses y "Servicios comunes" aparece legítimamente en los dos.
Las 13 filas mal etiquetadas se corrigieron verificando detalle y etiqueta antes de
tocar cada una. **La convención de una planilla se lee en la planilla, no en el
comentario del código que la escribe.**

**`--avn`, para no esperar al extracto.** `B4` es un `SUMIFS` contra Movimientos, así
que sin el extracto del Macro importado da $0 y el generador corta — correcto, pero
dejaba el cobro entero bloqueado. El flag escribe el total de las 4 liquidaciones y
**restaura la fórmula** igual que el resto. No carga una fila falsa en Movimientos: el
gasto entra una sola vez, cuando entre el extracto. El mes congelado queda marcado en
`EXPENSAS HISTORICO` con la nota de que la AVN se puso a mano — sin eso, un valor
provisorio queda indistinguible de uno definitivo y nadie lo revisa.

**El `finally` que protegía era el que podía perder.** Las dos restauraciones estaban
encadenadas: si la primera fallaba (timeout, 429, red), la segunda no corría y la
fórmula de `B4` quedaba pisada por un número, para siempre. Peor: la corrida siguiente
leía ese número como "el original" y lo volvía a restaurar, **confirmando la corrupción
mes a mes**. Ahora cada restauración va en su propio `try`, si algo falla se imprime el
backup en pantalla, y al arrancar se corta si `B4` no empieza con `=`. Lo encontró el
`code-reviewer`, no yo.

**Y `congelar_expensas` leía formateado.** `A3:R30` sin `render` — de ahí salen el
recupero y los servicios comunes de los 8 locales. La lección de los centavos ya estaba
escrita en este mismo archivo y aplicada a las pestañas, pero no en el lugar donde
**nace** el número. Arreglar un bug donde se ve no lo arregla donde se origina.

## 05/08/2026 — Un pago sin volcar no es plata reclamada de más

La sesión anterior dejó escrito, en rojo, que faltaban **$20.298.678,78 de pagos** en
las cuentas corrientes del Paseo y que por eso **"las cuentas reclaman plata que el
locatario ya pagó"**. Con esa frase adentro no se le podía mandar la cuenta a nadie.
Era falso, y la forma de medirlo era el error.

**Cómo se midió mal.** Por local: total de la columna de cobros automáticos (Q/R/S, que
baja de Movimientos) contra total de la columna Ingreso de la cuenta. La resta da un
número grande y aterrador. Pero las pestañas **no arrancan en el origen del contrato**:
la de Fabric empieza en `FEB'26`, la de Volta en `MAR'26`. Todo cobro anterior a esa
primera fila aparece como "sin volcar" — y su **cargo tampoco está**. Cruzando los
pagos faltantes contra los cargos que el auditor reporta como no reclamados, en el
mismo local y el mismo período:

| Local | Pagos sin volcar | Cargos sin reclamar | Neto |
|---|---|---|---|
| Fabric | $8.376.000,00 | $8.375.950,11 | $49,89 |
| Bigg | $6.243.895,00 | $6.243.895,00 | $0,00 |
| Volta | $4.730.000,00 | $4.729.228,51 | $771,49 |
| | **$19.349.895,00** | **$19.349.073,62** | **$821,38** |

Falta el **bloque entero**, no el pago. El saldo nunca estuvo inflado. **La comparación
válida es por bloque, no total contra total**: un total contra otro total sólo dice
"algo no coincide", y en una cuenta que arranca a mitad de camino eso es lo esperable.
Lo único que quedó para preguntar fueron $210.000 de Volta del 29/05 — una fila, no
veinte millones — y Facu confirmó el mismo día que la conciliación de junio ya los
había absorbido: volcarlos habría sido acreditarlos dos veces. **De los veinte millones
no sobrevivió un peso.**

**El chequeo que sí sirve, y es gratis.** Cada bloque de cobro tiene su total, y el
locatario paga contra ese total. Los cinco pagos de Fabric de julio suman
$11.930.491,11 contra un bloque de $11.930.490,91; Boss pagó $1.963.000 contra
$1.962.514,54; Volta $1.880.000 contra $1.883.189,31; Bigg quedó en $1.344,90. **Que
un pago caiga a centavos sobre el total de un bloque es la verificación de que está
bien atribuido** — y si no cae sobre ninguno, está mal atribuido y hay que preguntar,
no acomodar.

**Dos trampas de Sheets al insertar filas en el medio de una cuenta.**

1. `insertDimension` inserta la fila **entera**. En estas pestañas la columna N tiene la
   escalera de alquiler por IPC (`=N49*(1+O48)`), viva hasta 2029: una fila entera le
   mete un blanco en el medio y la cadena se corta. Va `insertRange` acotado a **A:H**,
   que además deja quieto el derrame del `QUERY` de Q/R/S.
2. **La fila de abajo sigue colgando del saldo viejo.** Sheets ajusta una referencia
   cuando la celda referenciada se mueve; `G49` no se movió, así que la fórmula que
   estaba en `G50` viaja a `G55` y sigue diciendo `=+G49+E55-F55`. Se saltea los cinco
   pagos recién insertados y **el saldo queda perfectamente formado y equivocado** —
   exactamente el modo de falla que el auditor de la cadena existe para atrapar. Hay
   que re-encadenar esa fila a mano, y volver a leer los saldos después de escribir.

## 05/08/2026 (II) — La captura que le mando al locatario sale de una hoja de un solo mes

Facu le manda a cada locatario una captura del bloque de las filas 40-58 de
`Expensas Predio` con el detalle de sus expensas, y pidió que eso coincida con la
cuenta corriente. **No coincidía**, y el motivo es estructural: ese bloque son dos
fórmulas `TRANSPOSE` sobre la tabla viva de arriba, que **es de un solo mes** —
todo se recalcula contra la fecha de `A3`. Al generar los cargos, `A3` se pone en
el mes nuevo y **vuelve al anterior**, así que la captura sacada después muestra el
mes viejo. Con `A3` en junio, para julio la hoja mostraba a Fabric **$989.867,29**
de servicios comunes donde su cuenta dice **$821.057,09**: $168.810 de más en un
número que sale a un tercero.

**Un mirror de una hoja viva no es un registro.** El bloque parecía un archivo
—tiene el mes escrito arriba— y era una vista. La diferencia sólo se nota cuando
alguien lo mira un mes después, que es exactamente cuando se manda. Ahora hay un
bloque **literal, sin fórmulas**, por mes, escrito por
`congelar_detalle_expensas.py` con el mismo formato del vivo, y que **se niega a
escribir** si el detalle no coincide contra `EXPENSAS HISTORICO` **y** contra la
fila del mes en la pestaña de cada local. Dos fuentes, no una.

**Congelar dos totales no alcanza para reconstruir un mes.**
`--congelar-expensas` guardaba sólo recupero y servicios por local. Julio se pudo
recuperar igual, pero de casualidad: los servicios se recalculan corriendo los
`SUMIFS` contra Movimientos, y la AVN —que se había puesto **a mano**, porque el
extracto del Macro no estaba— se **despeja** del recupero congelado de un local y
se valida contra los otros 16. Despejada desde Fabric y desde Peak One por
separado dio el mismo número, $2.650.057,36. De paso: la nota que el propio
generador dejó escrita dice **$2.651.057,36** — está mal por $1.000. Un valor que
se anota en prosa y no se vuelve a chequear miente sin que nadie se entere.

**`Movimientos!I` es TEXTO y Sheets lo lee como fecha.** La columna guarda
`"julio 2026"` y el criterio del `SUMIFS` es `A3`, una fecha. Sheets parsea el
texto y matchea; Python comparando literal da **$0 en todos los conceptos**, que se
lee igualito a "no hay datos cargados". Estuve a un paso de reportar que el
detalle de julio era irrecuperable. **Cuando una réplica en código da todo cero,
el sospechoso es la réplica, no el dato** — el control que lo destrabó fue correr
el modelo contra la hoja viva primero: si no reproduce lo que ya está a la vista,
el modelo está mal y no hay nada que concluir del mes viejo.

**Lo que apareció al reconstruir.** `Sueldo Mantenimiento Gastronomia` de julio no
está en Movimientos (junio: $1.936.000, julio: $0), y de ahí salen *Limpieza Baños*
(`I4 = sueldo/2`) y *Limpieza Predio* (`K4 = I4`). **Julio se facturó con los dos
en $0** para todos los locales: con el valor de junio serían ~$939.928 más entre
los 6 que hoy pagan. Un input que falta no rompe nada — reparte cero y sigue.

## 05/08/2026 (III) — Un input que falta no rompe nada: reparte cero y sigue

Reconstruyendo julio para congelar el detalle de expensas apareció que
`Sueldo Mantenimiento Gastronomia` no estaba en Movimientos para ese mes (junio:
$1.936.000, julio: $0). De ahí salen dos conceptos —*Limpieza Baños* (`I4 =
sueldo/2`) y *Limpieza Predio* (`K4 = I4`)— así que **julio se facturó con los dos
en $0 para todos los locales**. Nada falló: el `SUMIFS` devolvió cero, los
porcentajes repartieron cero, cada fórmula dio un número perfectamente formado y
las expensas salieron **$875.691,52 más baratas** de lo que correspondía. Facu
confirmó que ese sueldo **repite el del mes anterior**, así que nunca debió quedar
en cero.

**Un cero calculado y un cero real se escriben igual.** Un dato que falta se nota
cuando algo se rompe; acá el input faltante entra en una multiplicación y sale por
el otro lado como una expensa más barata. La única razón por la que se descubrió es
que el bloque congelado muestra el **detalle concepto por concepto**: con dos
renglones en `$0` al lado de diez con números, salta a la vista. El total solo no
lo habría mostrado nunca.

**La corrección hay que hacerla en las cuatro capas, en orden.** El número vive en
`EXPENSAS HISTORICO` (lo congelado), en `CARGOS` (lo que consume CUENTA CORRIENTE),
en la fila `JUL'26` de la pestaña de cada local (lo que ve el locatario) y en el
bloque congelado de `Expensas Predio` (lo que se manda por captura). Se corrigieron
las tres primeras y recién después se rehizo la cuarta, que **valida contra la
primera y la tercera** y se habría negado a escribir si alguna no cerraba.

**Y casi duplico un cargo.** `CARGOS` tiene filas placeholder **vacías** con el
mismo período, local y concepto que la fila buena (f96 Boss y f97 Peak One conviven
con f150 y f151). El primer `batchUpdate` iba a escribirle el monto a las cuatro:
CUENTA CORRIENTE las suma solas y a Boss y Peak One les habría aparecido el cargo
dos veces. Lo delató contar: "7 filas en CARGOS" para 5 locales. **Cuando un
contador no da redondo contra la cantidad de entidades, hay que mirar antes de
escribir** — la regla quedó en el script: se toca sólo la fila que ya tiene valor, y
si hay más de una con monto, corta.

**La palanca correcta es `--sueldo`, no una fila en Movimientos.** Mismo criterio
que el `--avn` que ya existía: el dato se pone a mano para calcular, pero el egreso
entra una sola vez, cuando entre el extracto. Cargarlo ahora en Movimientos para
"que dé bien" lo duplicaría en julio.

## 05/08/2026 (IV) — "Sueldo Mantenimiento Gastronomia" no es un sueldo

Facu puso la regla: en las expensas del Paseo **todo tiene que estar facturado; si
no está la factura, el concepto no se anota y se cobra el mes vencido**. Aplicarla
obligó a preguntar algo que nadie se había preguntado: *¿de qué comprobante sale
cada renglón?*

**Dos de los tres nombres de la planilla mentían sobre qué son.**
`Sueldo Mantenimiento Gastronomia` no es un sueldo: es **RHINO** —Sánchez Yanina
Betsabé, CUIT 27373389973— que factura *Limpieza y mantenimiento* por $1.600.000 +
IVA = $1.936.000 todos los meses. De ahí salen *Limpieza Baños* (`I4 = monto/2`) y
*Limpieza Predio*. Buscar el respaldo en `Recibos de Sueldo/` era buscar en el
cajón equivocado: el recibo de julio que había ahí es de un administrativo y **no
toca las expensas**. Y `Expensas AVN` no es una factura sino **cuatro
liquidaciones** distintas de la Asociación Civil. Un nombre de categoría heredado
manda a buscar el comprobante donde no está.

**El mes de la carpeta es el mes de PAGO, no el período de la factura.** Se
verificó leyendo las liquidaciones: carpeta *Junio* = período 05-2026, *Julio* =
06-2026, *Agosto* = 07-2026. Y así las consume el cálculo. Archivarlas "por
período" hubiera sido más intuitivo y habría roto el cruce.

**El error que la regla encontró en el primer intento.** Las cuatro liquidaciones
de julio suman **$2.651.057,36** y en el cálculo estaba **$2.650.057,36**: $1.000
de menos. Peor: unas horas antes yo había despejado ese valor desde dos locales
independientes, visto que la nota del generador decía otra cosa, y concluido que
**la nota estaba mal**. Estaba al revés — la nota tenía el número de la factura y
el valor cargado era el equivocado. **Dos reconstrucciones que coinciden entre sí
prueban qué número se usó, no que ese número esté bien.** Contra un comprobante
manda el comprobante, no la coherencia interna.

**Y la regla salvó al renglón que iba a borrar.** Con Rhino sin factura de julio a
la vista, lo que correspondía era sacar los $1.936.000 y pasarlos a agosto. Antes
de tocar nada aparecieron en Downloads las facturas **00000011** (01/07) y
**00000012** (01/08): el renglón de julio estaba bien y el de agosto ya tiene
respaldo. Buscar el comprobante antes de revertir costó diez minutos y evitó
mover $875.691,52 al mes equivocado.

**El hueco que la regla todavía tiene.** "No se anota" sólo funciona si lo
diferido deja rastro. Un concepto que se saltea en julio y que nadie registra no
se cobra nunca — es el mismo agujero de siempre con otra causa. Falta la lista de
diferidos; sin eso la regla es media regla.

## 05/08/2026 (V) — Un cero deliberado y un cero que es un error se escriben igual

Facu pidió que cuando un concepto va en $0 quede aclarado, *"para que el cliente
note lo que se está ahorrando y no se me queje después con otras cosas"*. Había
**26 filas de cargo en $0** en las cinco cuentas y **una sola** decía por qué
(«Mes de gracia», escrita a mano por él). Las otras 25 se leen como un olvido.

**Aclarar un cero exige clasificarlo primero, y ahí está el riesgo.** Escribir
"Sin IVA" al lado de un cero convierte una omisión en una decisión — y si el cero
era un error, lo tapa para siempre con cara de intencional. De las 26 filas, dos
NO son bonificaciones y quedaron sin tocar a propósito: **Bigg FEB'26 «IVA
Servicios Comunes» en $0**, cuando Bigg sí factura (faltan $97.860), y **Volta
MAR'26 «Dif alq»**, una fila que sobra por haber copiado la plantilla de Bigg a un
local sin alquiler partido. El script las lista aparte en vez de anotarlas: **una
regla que clasifica tiene que tener una salida para "no sé", o clasifica todo mal
con confianza.**

**Si la fila no existe, no hay nada que ver.** Al bloque de agosto le faltaban 7
renglones en $0 que los bloques anteriores sí tenían — el IVA de Boss y Volta, y
el alquiler de Peak One, que es justo el caso que Facu quería mostrar. La
aclaración no servía de nada sin agregarlos primero.

**Cada insert necesita su propio re-encadenado, no sólo el último.** Esta misma
sesión ya había dejado escrito que al insertar filas la de abajo sigue colgando
del saldo viejo. Con dos inserts en la misma pestaña lo apliqué **una sola vez**,
al último: la cadena quedó cortada en Boss (`G33` arrastraba de la 31, salteando
la 32) y en Volta (`F40`, de la 38). **Y los cinco saldos verificaron OK**, porque
las filas nuevas valen $0 — la verificación que había elegido no podía ver este
error. Lo agarró `auditar_ctas_ctes.py`, que chequea la cadena celda por celda en
vez de mirar el número final. Una lección escrita no se aplica sola cuando el caso
cambia de forma: **saber la trampa no es lo mismo que tener el chequeo**.

**Y los inserts iban de abajo hacia arriba.** Los hice en orden inverso para que
el segundo no corriera al primero — pero las posiciones estaban calculadas sobre
la numeración *post* primer insert, así que la fila de abajo cayó una más abajo,
fuera del bloque y debajo del total. En una tabla donde el orden es semántico, el
orden de los inserts y el sistema de coordenadas de las posiciones tienen que
decidirse juntos, no por separado.

## 06/08/2026 — El permiso más chico que existía abría la base entera de alumnos

Lanfran necesitaba entrar al back office de Astronomy para tres cosas: las demos
del sello, el catálogo de lanzamientos, el calendario y el usuario/clave de DJ
Delivery. Nada de la academia. El sistema de permisos ya existía y tenía trece
llaves, y aun así **no había forma de darle eso sin darle de más**.

**Un permiso que sirve para dos trabajos distintos no es un permiso, son dos.**
El calendario colgaba de `view_students`, que además abre la base de alumnos, las
fichas, los créditos y las bajas. Y para *leer* el usuario y la contraseña de DJ
Delivery había que tener `manage_djdelivery`, o sea el botón de *cambiarlos* — en
una clave que es una sola y la comparten todos los alumnos a la vez. En los dos
casos el permiso mezclaba "mirar" con "tocar", y la única forma de dar lo primero
era regalar lo segundo. Se partieron: `view_calendar` y `view_shared_access`.

**El escritorio le decía "hoy no hay nada para hacer" a alguien que sí tiene
trabajo.** `/admin` es una cola que sale de `lib/workflows.ts`, y ninguno de esos
workflows es del sello. Para un perfil que entra a cuatro pantallas, esa pantalla
está vacía todos los días, para siempre. El corte quedó **declarativo** —"si todo
lo que puede hacer entra en esta lista, mostrale sus herramientas"— y no "si es
Lanfran": el día que se le dé un permiso de administración, sale del panel simple
solo, sin que nadie se acuerde de venir a tocarlo.

**El `decodeURIComponent` que rompía justo el caso real.** El alta de un
lanzamiento resuelve el reproductor sola, pegándole al oEmbed de la plataforma, y
para SoundCloud saca el id numérico y el `secret_token` del html que devuelve.
Decodificaba ese html antes de buscar — y `decodeURIComponent` tira `URI
malformed` con un `%` suelto, que el html de SoundCloud trae de sobra. Explotaba
con el primer link que se probó, uno de los de Sin City. Lo peor no era el error:
estaba adentro de un `try/catch` que contesta *"no se pudo hablar con
SoundCloud"*, así que el lanzamiento se habría guardado sin reproductor
**culpando a una plataforma que había contestado perfecto**. Decodificar nunca
hizo falta: los patrones ya aceptaban `%2F` y `/`. Verificado contra los cuatro
links reales, y los `trackId` que devuelve coinciden con los que estaban
hardcodeados desde el 05/08 — o sea que el resolvedor reproduce a mano lo que se
había cargado mirando.

**Esconder el botón no es el permiso.** Publicar un lanzamiento es lo único de
este perfil que escribe en astronomyofficial.com, así que quedó sólo para la
cuenta maestra. Se verificó armando el POST a mano con la cookie del perfil
acotado y el id de la server action sacado del `server-reference-manifest.json`:
303 a `/admin?denied=1` y `published` siguió en `false`. Sin esa prueba, lo único
que se sabía era que el botón no se dibujaba.

**La vista previa tiene que recortar de verdad.** Facu pidió ver el panel de
Lanfran desde su admin. Una maqueta —dibujar esa pantalla con los permisos del que
mira— muestra botones que el otro no tiene, que es exactamente el error que uno
está tratando de encontrar al mirar. La cookie hace que `getStaffContext()`
devuelva los permisos de la otra persona: adentro de la vista previa el maestro
tampoco entra a los sueldos. Por eso salir **no puede pedir** el permiso que la
cookie acaba de sacar, y por eso entrar pregunta por `esMaestroReal()`, que ignora
la cookie — si no, se queda encerrado en la vista previa del primero que eligió.

**Un POST a mano no prueba un server action.** El primer intento mandó
`Next-Action` como cabecera y Next contestó *"Connection closed"*: parecía un bug
de la app y era el arnés. La forma que sí funciona es la de un formulario sin
JavaScript — el `$ACTION_ID_…` como **campo** del multipart, no como header.
Sirve para probar cualquier server action de este repo por curl.

## 06/08/2026 — La deuda en efectivo no es el saldo, y el deploy que da Forbidden

Mati sale a cobrar en mano, así que necesita **cuánto debe en efectivo cada
local**. El saldo de la cuenta corriente no sirve para eso, por dos razones que
mueven mucha plata: **mezcla banco con efectivo** (Fabric tiene $11,6M de saldo y
no debe un peso en efectivo; Bigg tiene $5,4M pero sólo $1,1M es en mano) y
**cuenta como deuda un bloque que todavía no venció** (todos pagan el mes
siguiente). Separar las dos cosas convierte un número inservible en uno accionable.

**El corte de "vencido" se puede leer de la planilla en vez de calcularlo.** El
bloque que se está cobrando es todo lo que hay **debajo de la última fila de
pago**. No hay que hardcodear filas ni fechas ni saber en qué día del mes estamos:
la estructura del documento ya dice dónde termina lo cobrado. Hoy da que casi nada
está vencido — Boss −$485, Peak One $579, Volta $3.189.

**El invariante que valida todo el cálculo.** En los locales que cobran 100% en
efectivo, la deuda en efectivo tiene que dar **exactamente** el saldo de la
pestaña. Ese chequeo destapó el bug: yo salteaba las filas sin detalle, y **muchos
pagos tienen el detalle vacío** porque el medio va en la columna B. Daba $4,1M
donde el saldo era $1,7M. Sin un invariante, ese número se veía perfectamente
plausible.

**Lo que no está verificado no se muestra como cobrable.** La Jaula da $668.824,
pero su alias en `Cobros` mezcla alquileres sueltos de cancha con el contrato. El
JSON lleva un campo `confiable` y la tarjeta muestra **"a confirmar"** en vez del
monto. Mandar a alguien a cobrar un número que no se puede defender es peor que no
mostrarlo.

**El deploy: `--prod` da `Forbidden`, el draft no.** Mismas credenciales, mismo
sitio, mismo bundle. El sitio no está locked y la cuenta es la dueña. Lo que sí
funciona es deployar en draft y **publicar ese deploy por API** con
`restoreSiteDeploy`. Diagnosticarlo fue posible porque el draft deploy **no toca
el sitio en vivo**: se puede usar como sonda sin riesgo. Ante un error opaco en
una herramienta de deploy, buscar primero la variante inocua que aísla si el
problema es de credenciales, de destino o de la acción concreta.

## 06/08/2026 (II) — El calendario mostraba 21 de 175 clases y parecía un borrado

Lanfran, el día después de estrenar su perfil: *"¿por qué se borran del calendario
los eventos que ya sucedieron?"*.

**No se borraban: nunca se consultaban.** La consulta pedía `starts_at >= ahora`.
De las 175 clases activas que había, el calendario mostraba **21** — el 88% del
historial del estudio era invisible. Y esto es lo que hay que quedarse: **nadie
lo había reportado en dos meses**, ni José, ni Luqui, ni los profes, ni Facu.
Hizo falta alguien que entrara por primera vez, sin la costumbre de que "el
calendario es lo que viene", para que la pregunta apareciera.

**Una ausencia no se ve.** Un dato mal calculado grita: el número no cierra,
alguien lo cruza contra otra cosa y salta. Un dato que directamente no está no
tiene contra qué chocar — la pantalla se ve completa, ordenada y correcta.
`gte("starts_at", ahora)` no es un bug que se pueda encontrar mirando la
pantalla: sólo se encuentra contando las filas de la base y comparándolas con
las que se dibujan. Es el mismo mecanismo de la regla 2 (*"un resultado vacío o
corto es un error hasta que se demuestre lo contrario"*) pero un escalón más
arriba: acá el resultado no era vacío, era **plausible**.

**El filtro estaba en tres pantallas y sólo se arregló una.** `/member` y
`/profe` tienen exactamente el mismo `gte("starts_at", nowIso)`: Pastrana no ve
las 88 clases que dio, Guini no ve 29, y 48 alumnos no ven su historial. Se
arregló sólo el back office —que es donde se reportó— y las otras dos quedaron
anotadas para que las decida Facu, porque cambian la pantalla principal del
alumno. **Escribirlo importa más que arreglarlo rápido**: la próxima sesión que
abra `/member` tiene que encontrarse con que esto ya se sabe.

**La ventana es de 90 días y no "todo", a propósito.** Hoy el historial completo
entra (la app arrancó en junio) y traerlo entero funcionaría igual. Pero en un
año son miles de filas y **PostgREST corta en 1000 sin avisar**: el calendario
empezaría a perder días viejos en silencio, justo cuando ya nadie se acuerde de
que esta consulta no tenía tope propio. Un límite que uno elige se puede
explicar; uno que aparece solo, no. Ver [[postgrest-tope-1000]].

**`pasado` lo decide el servidor.** Calcularlo en el componente era una línea
menos, pero entonces el reloj y la zona horaria del teléfono de cada uno
definirían qué clase "ya sucedió". Un solo reloj, el del servidor.

**Y una clase pasada nunca trae acciones, tenga quien mire el permiso que
tenga.** Reprogramar, cancelar o reasignar algo que ya pasó no significa nada, y
los tres botones mueven créditos. El corte va en el componente **y** en el
servidor: los horarios libres y los datos del alumno ni siquiera viajan al
navegador para una clase con la que no se puede hacer nada.

**Además del gris, dice "ya pasó".** El apagado solo es ambiguo: se lee igual
que "cancelada", que "no confirmada" o que un bug de contraste. Y los **días**
pasados se apagan comparando contra la medianoche de hoy, así que hoy nunca se
apaga aunque ya haya terminado la última clase.

### Lo que se llevó de arrastre

Un `FATAL` de Turbopack sobre `/preview-medallas/page` —una ruta que no existe en
el árbol— hizo aparecer "2 Issues" en el overlay del dev server y mandó a buscar
un bug propio que no había. Era otra sesión creando y borrando archivos en el
mismo repo mientras el HMR corría. **El overlay de `next dev` no distingue un
error del código de un error del compilador con archivos que se movieron abajo
suyo:** cuando aparece un issue raro y hay otra sesión trabajando, la
verificación honesta es un `npm run build` en frío. Ver
[[dos-sesiones-mismo-repo]].

## 06/08/2026 — El cero ya era la aclaración

Facu había pedido que cuando un concepto va en $0 "quede aclarado, para que el
cliente note lo que se está ahorrando". Lo implementé escribiendo notas —«Sin
IVA», «Sin alquiler hasta dic-26»— en la columna B de Volta y Peak One y en la D
de Boss. **Estaba mal, y él lo corrigió: se ve feo y la B no es para eso.**

Lo que quería es más simple y ya existía en la estructura: **cada bloque lleva
siempre los cinco conceptos** —Recupero, Servicios comunes, IVA servicios,
Alquiler, IVA alquiler— y en la columna de egreso va el monto de cada uno.
**Si el IVA es 0, se escribe `0`.** El renglón con su cero al lado ya dice que no
se cobra. La aclaración no era texto nuevo: era **completar la tabla**.

**Dónde me desvié.** Tenía la pieza correcta —"si la fila no existe, no hay nada
que ver", y agregué los 7 renglones que faltaban— y encima le sumé una capa de
prosa que no hacía falta. Habiendo entendido que el problema era una tabla
incompleta, seguí adelante y también inventé un vocabulario de notas, un lugar
donde ponerlas y una regla distinta por pestaña según qué columna estuviera libre.
**Que la columna esté vacía no significa que sea para eso**: la B tiene un
significado —el medio de un INGRESO— que yo mismo había dejado escrito en la
memoria dos horas antes, y lo pisé igual.

**Y quedaban 17 celdas en blanco donde iba un cero.** Vacío y `0` se ven casi
igual en la pantalla pero no dicen lo mismo: el vacío se lee como olvido. Pasarlas
a `0` no mueve ningún saldo — se verificó — y es exactamente lo que hace visible
que ese concepto no se cobra. La aclaración que hacía falta costaba 17 celdas, no
29 notas.

## 06/08/2026 (III) — La cuenta con la que probás que "la página abre" es la que no rompe

Buscando dónde mostrar el historial de clases apareció otra cosa: **`/member`
tiraba 500 en producción para todo alumno con una clase agendada.** El panel del
alumno, la pantalla más visible del negocio, caída.

`editBookings` usa `minLeadMs` y `cancelMs` adentro de un `.map`, y las dos se
declaraban veinte líneas más abajo. TDZ de manual. Estaba en `main` desde antes
de esta sesión.

**Por qué sobrevivió: el callback de un `.map` sobre una lista vacía no se
ejecuta.** Un alumno sin clases entraba perfecto. Y ésa es exactamente la cuenta
con la que uno prueba que una página abre — la recién creada, la de prueba, la
que no tiene datos. Medido contra producción: cuenta sin clases → 200, cuenta con
una clase → 500. **Estaba roto para todos los que tienen algo que ver ahí, y sano
para el único caso que se testea.**

De acá sale un chequeo, no una anécdota: **una pantalla se prueba con una cuenta
que tenga datos, no con una recién creada.** La cuenta vacía verifica que la ruta
resuelve; no verifica la pantalla.

**Y me equivoqué en el medio, dos veces, por el mismo motivo.** Al ver el 500
stasheé mis cambios, seguí viendo 500 y concluí "no es mío". Después lo probé en
un worktree en un commit viejo, 500 otra vez, y concluí "es preexistente y lo
rompió otra sesión" — estuve a punto de reportarle a Facu un incendio ajeno. Las
dos veces estaba leyendo el mismo error **minificado** (`Cannot access 'aQ'…`),
que no dice nada, y lo atribuí por contexto. La respuesta apareció en un minuto
cuando lo corrí en `next dev`, que da el nombre real: `minLeadMs`, y el archivo y
la línea. **Un error minificado no se diagnostica, se reproduce en dev.** Bisecar
con un símbolo ilegible es adivinar con pasos intermedios.

### Y de paso, lo que sí se vino a hacer

**El calendario guarda todo y se navega sin límite.** Facu, después del reporte de
Lanfran: *"que quede todo guardado, desde la primera clase que tomaron, que puedan
volver el calendario para atrás año por año"*. La ventana fija de 90 días que se
había puesto a la mañana era el mismo bug corrido de lugar: al salirse de la
ventana, los días aparecen vacíos aunque haya clases. Ahora el servidor pinta una
ventana inicial y el componente pide los meses que faltan a `/api/calendario`.

**El ámbito lo decide el endpoint, no quien pregunta.** No hay ningún parámetro
que diga de quién son las clases: entran dos fechas y nada más. Facu fue
explícito —*"no está bien que un alumno vea las clases de otro, se mezcla mucho;
con alquileres de cabina lo mismo"*— y se verificó atacándolo: pidiéndole el
`user_id` de otro alumno y un `ambito=todos`, devuelve las suyas igual.

**Un registro de "esto ya lo pedí" no va en `useState`.** La primera versión
guardaba los meses ya traídos en estado: es dependencia del efecto **y** lo
escribe el propio efecto. Marcar un mes dispara el efecto otra vez. Medido en el
log del server: **40 pedidos del mismo rango en una visita**. Con `useRef`, uno.
Y no se descubrió mirando el código —se veía razonable— sino contando las líneas
del log.

**Cambiar el significado de una variable rompe a los que la leen.**
`nativeBookings` y `nativo` dejaron de ser "sólo futuras", y había **cinco**
lugares que dependían de que lo fueran: reasignar una clase, a quién avisarle,
pedir los horarios libres, mover y cancelar. Sin el corte, el profe le escribe a
un alumno por una clase que ya tomó. Se nombró `futuras` una vez por archivo en
vez de repetir el filtro en cinco lados y perderse el sexto.

**El dev server no sirve para medir cuando hay otra sesión editando.** Cada
guardado ajeno provoca un full reload: 22 cargas de la misma página en una
corrida, que además parecían un loop mío. La medición limpia salió con
`npm run build && next start`. Ver [[dos-sesiones-mismo-repo]].

## 07/08/2026 — Tres emisiones fiscales fallidas por un sufijo, y una app que confirma y no hace nada

Automatizar la facturación de Paseo Nordelta en **Bejerman Web** (MAHNI MANAGEMENT, punto
de venta 0002). Seis comprobantes por mes: alquiler del mes corriente, y recupero de gastos
y servicios comunes del mes anterior, para Fabric y Bigg.

**Cuatro Facturas A salieron bien. La Nota de Débito de Bigg falló tres veces seguidas**,
siempre con el mismo mensaje: *"Debe ingresar la Fecha Desde Período o seleccionar un
comprobante asociado desde Datos Adicionales"*. El robot abría Datos Adicionales, escribía
las fechas, **releía los campos para confirmar que habían quedado escritas**, aceptaba el
modal — y la emisión fallaba igual.

Causa raíz: **el modal de Datos Adicionales de una Nota de Débito tiene dos pares de fechas
distintos.** `DatosAdic_Dscv_FECHADESDE` es *Fecha Desde **Servicio***; el que ARCA valida
es `DatosAdic_Dscv_FECHADESDE**PERIODO***. El robot llenaba el primero. La verificación de
"quedó escrito" pasaba perfecto porque el campo existía y aceptaba el valor — sólo que era
el campo equivocado. Las Facturas no piden período, por eso las cuatro pasaron.

**Cómo se encontró: grabando a Facu hacerlo a mano.** Se le inyectó un listener de `click`
y `change` en todos los frames vía CDP, y el log escupió el id real. Ninguna cantidad de
lectura del DOM lo hubiera dado, porque los dos campos se ven iguales y el error nombra una
etiqueta ("Fecha Desde Período") que no coincide con el id que uno prueba primero.

**El segundo hallazgo, más caro que el primero:** en la primera pasada el robot reportó
`CONFIRMADO` en la ND —había clickeado el "Sí" del modal *"¿Confirma la emisión?"*— y **no
se creó ningún comprobante**. La app confirma y después falla, dejando un cartel de error
que nadie mira. Si la verificación hubiera sido "clickeé Sí, listo", habría reportado seis
facturas emitidas con cinco existiendo. El chequeo bueno resultó ser **bajar el PDF con la
sesión del navegador**: `PROWEB/facturas/101838/0073/<TIPO> A0002-<NRO>.pdf`, donde 404
significa que no existe. Sirve en los dos sentidos: también confirma, antes de reintentar
una emisión fallida, que no quedó nada duplicado.

Otras cuatro trampas de la misma app, todas en el README del robot: tipear "FC" y soltar
elige sola la **Factura de Crédito MiPyME (201)** en vez de la Factura A; **dos botones
distintos comparten el id `sales-crud-add-button`**; **"Agregar" registra pero no emite**
(deja el comprobante sin CAE, que no es una factura válida); y el buscador de conceptos
**devuelve resultados desfasados una consulta**.

Fix: `.claude/skills/cierre-mes-nordelta/scripts/bejerman/` — `emitir.js` (verifica el
total en pantalla contra el esperado **antes** de emitir, y frena si un peso no coincide),
`grabar.js` (el grabador de clicks, que es lo que destrabó esto) y el README con las siete
trampas. Las seis de agosto quedaron emitidas, con CAE verificado contra el PDF, y
archivadas en `Facturas de Venta/2026/Agosto 2026/`. Total $15.199.684,81.

**La lección transferible: una verificación que sólo comprueba que *escribiste* algo no
verifica nada.** Hay que comprobar que el sistema *aceptó* lo que escribiste — y para algo
irreversible, comprobarlo contra una fuente que el propio sistema no controle.
