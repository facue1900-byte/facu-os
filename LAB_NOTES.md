# Lab Notes

Cada vez que algo falla, sale bien de forma no obvia, o revela una restricción escondida,
va una entrada acá. **Nunca se borra una entrada** — es registro histórico. Cuando algo se
arregla, se marca `FAIL ✓` y se anota el fix.

Reglas: documentar la **causa raíz**, no el síntoma. Nombrar el script / la API / el skill.
El postmortem completo va acá; la lección corta (dos oraciones) va al `SKILL.md` del skill
afectado. Si es un patrón transferible, va a memoria en `indice-trampas.md`.

### 2026-11-12 · FAIL ✓ · Paseo: el brief decía «nadie debe nada vencido» y Bigg debía la ND 11

**Síntoma:** el panel de Jarvis (12/11 07:50) mostraba exigible $0 y a Bigg entero como
«BANCO» ($5.527.601). Recalculado a mano desde la pestaña: Bigg debe **$471.465,66 vencidos
por banco** (ND 11, recupero de sep, vto 11/10 — ya identificada el 05/11) y del bloque de
noviembre $1.229.303,58 en efectivo + $3.826.831,42 por banco.

**Causa raíz:** `radar_deudores.clasificar` neteaba todos los pagos contra todos los cargos
sin mirar el medio. Los $800.000 que Bigg pagó **en mano** el 06/11 (contra la Diferencia
Alquiler de nov) «cancelaban» la ND 11 de banco, y lo vencido daba negativo → $0. El brief
además marcaba el medio con un booleano por local (`n in PAGAN_POR_BANCO`), así que Bigg
salía 100% banco. La tarjeta de Mati (`deuda_efectivo.py`) ya separaba medios; el radar no.

**Fix:** `medio_del_cargo` / `medio_del_pago` se mudaron a `reglas_locales.py` (una sola
regla para Mati y para el radar). El radar etiqueta cada movimiento con su medio y, en el
local partido, camina en orden: el efectivo cancela efectivo y sólo el excedente se derrama
a banco (como los cartuchos de Facu). Cada local trae `medios` y el brief publica
`efectivo` / `banco` por renglón. Verificado: efectivo de Bigg = el de la tarjeta de Mati al
centavo, y efectivo + banco = saldo de la pestaña. Tests en `test_jarvis.py`.

**Lección:** en un local que paga por dos medios, «al día» se calcula **por medio**. Un
neto único deja que un pago en mano tape una deuda de banco y el cero parece verdad.

### 2026-11-11 · FAIL ✓ · El brief de Jarvis mostraba la deuda del Paseo de JULIO

**Síntoma:** el panel del Paseo decía Fabric $2.033.664 exigible; la pestaña Fabric ya
tenía cargos hasta NOV'26 y pagos por banco al 26/10.

**Causa raíz:** `radar_deudores.py` (y el brief, que lo usa) leía la pestaña consolidada
**CUENTA CORRIENTE** de Ctas Ctes. No es una tabla que crece: es una grilla de **filas
fijas** período × local (64 filas: 8 locales × dic-25…jul-26) con `SUMIFS` contra CARGOS
y Cobros. Nadie la extendió desde julio y nada lo hacía — `cargos_del_mes.py` agrega a
CARGOS y a cada pestaña, nunca a la consolidada. CARGOS ya llegaba a nov-26. Encima
cruzaba Cobros por nombre («Fabric», «Volta + Open») y por mes de PAGO, no por bloque:
aun extendida daba otro número que la pestaña que ve el locatario. Nunca falló un
chequeo porque el único era «¿vino con filas?» — y 64 filas viejas son filas.

**Fix:** el radar lee las **pestañas por local** (layout único en
`reglas_locales.PESTANAS`, compartido con `deuda_efectivo.py`) y CARGOS − Cobros para
los que no tienen pestaña. Regla de cobro explícita: bloque del mes M = alquiler de M +
expensas de M−1 (`mes_de_cobro`, verificada leyendo las 5 pestañas; un concepto
desconocido corta en vez de adivinarse). Dos alarmas nuevas: último período con más de
1 mes de atraso → «sin dato» (el brief no muestra el total), y la cadena de SALDO de la
pestaña tiene que dar cargos − pagos (±$1). Al 11/11 las cinco cierran al centavo.
`exportar_ctas_ctes.py` (mismo origen, sin consumidor en la app) quedó dado de baja.
Tests: `execution/tests/test_radar_deudores.py`.

**Lección:** una tabla «que se calcula sola» con filas escritas a mano no se calcula
sola: envejece. Para saber si una fuente está al día se mira su **último período**, no
si tiene filas.

### 2026-11-11 · FAIL ✓ · Bot de Telegram: «solo lectura» por instrucción, no por permiso

**Qué pasó.** La primera versión de `execution/telegram_bot.py` corría `claude -p` con un
`--allowedTools` de lectura y la instrucción «no escribas». La prueba «creá un archivo» pasó, pero
porque el modelo obedeció, no porque no pudiera: el `~/.claude/settings.json` global auto-aprueba
Edit/Write/WebFetch y tiene `defaultMode: auto`. Es la misma trampa del 29/10 (más abajo); la atajó
el `code-reviewer`, no yo. Además, Gmail + WebFetch juntos eran un camino de fuga: un mail con
instrucciones podía hacerle leer un secreto y mandarlo en una URL.

**Fix.** `--tools Read,Glob,Grep` (las demás propias no existen), `--permission-mode dontAsk`,
`--disallowedTools` con todo lo que escribe o manda en los conectores y con `Read(**/.env*)`, sin
web, y Claude corre con un entorno mínimo (no hereda el `.env`). Probado headless pidiéndole que
INTENTE cada cosa prohibida: Write, Bash, WebFetch, el borrador y la etiqueta de Gmail ni existen;
el `.env` da «denied by your permission settings».

**Lección.** La prueba de un permiso es pedirle al agente que lo intente «de verdad, sin negarte de
antemano»; si se niega por instrucción, la prueba no probó nada.

### 2026-11-10 · FAIL ✓ · Paseo: el cuadro operativo contaba el FCI y dos correcciones viejas habían vuelto

**Qué pasó.** La pestaña «Dashboard» del Master Plan (resultado operativo) mostraba octubre con
$73,2M de ingresos y $64,1M de egresos: las 3 suscripciones al FCI ($47M) entraban de los dos lados.
También contaba «Ajuste de caja» como gasto (−$882.814 en el acumulado), cosa que el reporte a
inversores no hace. En la revisión completa aparecieron además el aporte de Richi de $20M con día y
mes invertidos (03/02 en vez de 02/03) y Tubomarket otra vez en $391.325, una corrección del 27/07.

**Causa raíz.** (1) La lista de lo que no es operativo vivía en dos lados: los SUMIFS de la hoja y
`NO_OPERATIVO` de `reporte_inversores.py`. El FCI se agregó sólo al script el 26/10. (2) La hoja es
un espejo de la base de la app: la corrección del 27/07 se hizo sólo en la hoja y un sync posterior
la pisó. La fecha del aporte también estaba mal **en la base**. No hay `updated_at`, así que no se
sabe quién la cambió entre el 21/10 y el 10/11.

**Fix.** Fórmulas del Dashboard alineadas; `verificar_dashboard.py` paso 5 compara el cuadro contra
`NO_OPERATIVO` (probado con el cuadro viejo: marca abr, jun y oct). Fecha y monto corregidos en la
base y en la hoja. `CAMBIO` (Pesos a USD / Cambio de USD) sumado a `NO_OPERATIVO`.

**Lección.** Un dato del Paseo se corrige en Supabase; la hoja sola no alcanza.

### 2026-11-10 · FAIL ✓ · Paseo: efectivo-diario murió "sin red" con la red andando

**Qué pasó.** Mail de falla de `efectivo-diario`: "Sin red después de 15 minutos". La Mac estuvo
cerrada toda la mañana (`pmset -g log`): sólo DarkWakes de mantenimiento de ~45 s a las 07:39, 08:07
y 08:44. `correr.sh` vio red en el primero y largó la tarea; `efectivo_diario.sh` tenía **su propia**
espera de red, que la perdió y consumió sus 30 intentos entre DarkWakes hasta morir a las 08:44.
El mail salió en los 20 s de FullWake. Los datos estaban sanos: a mano, 665 = 665 y $0 a volcar.

**Causa raíz.** Espera de red duplicada: el mismo error que `correr.sh` ya documentaba ("la red se
decide UNA vez", 01/11), sobreviviendo adentro de un script. **Fix:** se sacó el loop de
`efectivo_diario.sh`; la red la decide sólo `correr.sh`. No queda otro `host -W` en el repo.

**Lección.** Una tarea que corre por `correr.sh` no chequea la red por su cuenta.

### 2026-11-04 · FAIL ✓ · Paseo: una rutina podía mandarle el reporte a Richi sola, y las rutinas "en la nube" no eran de la nube

**Qué pasó.** Revisando los agentes que corren con la Mac apagada: `Conciliacion mensual`
(`trig_01PGsAkK6F7Ponc8V7HFaGYC`) tenía orden de mandarle el reporte a inversores a Richi sin OK si sus
controles cerraban, con definiciones anteriores al arreglo de `reporte_inversores.py`. Nunca llegó a mandarlo:
en su única corrida faltaba el extracto. La próxima era el 10/11.

**Causa.** Es una tarea de Cowork atada a la Mac (`bound_device_uuid`): usa carpetas locales y el Chrome de
Facu. Figura en la lista de rutinas igual que las de la nube, y `succeeded` no dice qué hizo.

**Arreglo.** Rutina vieja apagada, sin borrar. La conciliación pasó a `cierre_mensual.sh` (día 16, ya con el
extracto), que no manda nada. Si no cierra o falta el PDF, avisa.

**Lo no obvio.** Una rutina creada por API NO se puede atar a la compu: `bound_device_uuid` se ignora en create y
update, y corre sin carpetas ni Chrome (probado: `trig_01TNYyNLjfyNMjQf9R4i2Ake`, apagada). Para ver si una rutina
trabajó, mirar `get_run_log`, no el estado.

### 2026-10-30 · FAIL ✓ · Pauta: el chequeo de los lunes daba FALLA siempre, y no miraba si se gastaba

**Dónde:** `active/astronomy/pauta/reporte_embudo.py` (`chequeo`, nuevo `gasto_de_ayer`).

**Qué pasó:** desde el 09/10 ningún anuncio activo manda a la web, pero el chequeo exigía visitas
de pauta en 48 h con cualquier anuncio activo: FALLA todos los lunes, o sea ruido. Y al pasar los
videos de José a un público de ~65 mil (30/10) no había nada que avisara si Meta dejaba de gastar.

**Causa raíz:** el chequeo contaba anuncios activos, no anuncios activos *a la web*; y el gasto
real nunca se medía contra el presupuesto.

**Fix:** visitas sólo si hay anuncios activos con UTM web. Nuevo: cada conjunto activo (de más de
2 días) tiene que haber gastado ayer ≥ 40% de su presupuesto, si no FALLA; conjunto de WhatsApp con
3 días de gasto y 0 chats → AVISO. Probado con datos reales (OK) y con gasto 0 simulado (FALLA).
Plist diario `com.facu.chequeo-pauta` (11:00) escrito; la instalación la hace Facu.

### 2026-10-21 · FAIL ✓ · Paseo: una factura pagaba dos débitos, y el extracto sin resumen no se podía leer

**Dónde:** `cierre-mes-nordelta/scripts/extracto_a_movimientos.py` (`resolver_con_facturas`, `texto_pdf`).

**Qué pasó:** con el export de movimientos de septiembre (no había resumen mensual), el match
por importe le dio la factura de Annie ($1.500.000) a dos débitos: el pago real del 15/09 y una
transferencia del 16/09 al CUIT de la propia MAHNI. El segundo iba a entrar como Marketing sin
ningún aviso. Además, el script sólo leía el layout del resumen mensual.

**Causa raíz:** el matcheo nunca marcaba una factura como usada ni miraba el CUIT de la glosa.

**Fix:** cada factura se usa una sola vez y, si la glosa trae CUIT, la factura tiene que ser de
ese CUIT. El export se lee por la coordenada de la columna y se valida contra cada saldo diario,
el final y los totales de la cabecera. Julio y agosto dan idéntico al código viejo.

### 2026-10-19 · FAIL ✓ · Caja del Paseo: lo que Mati no veía, lo volvía a cargar

**Dónde:** app del Paseo, `src/pages/Caja.tsx` (vista Mati) y `src/lib/parseCaja.ts`.

**Qué pasó:** un pago de $600.000 a Daniel quedó cargado 4 veces en octubre ($1.800.000 de
caja de más descontados), y «Recio de Boss $300.000» (typo de Recibí) entró como egreso
Otros (−$600.000 de diferencia). Mati avisó «no me lo toma… descontó la plata» el 14/10.

**Causa raíz:** (1) la vista de Mati escondía las Inversiones pero el saldo las descontaba:
cargaba, no lo veía y recargaba. Daniel caía en Inversiones por regla del parser. (2) el
parser decide ingreso/egreso sólo por el verbo; sin verbo, egreso por default.

**Fix:** c2e5c53 (Mati ve todo lo que carga salvo aportes), f9893ab (Daniel + mantenimiento/
arreglo/rejilla → Mejoras), y sin verbo + nombre de local → cobro. Datos corregidos en base y
Sheet; `reconciliar_hoja.py` 585/585, dif $0, neto oct +$590.965.

**Lección:** una pantalla que esconde un renglón pero cuenta su plata invita a cargarlo dos veces.

### 2026-10-10 · FAIL ✓ · Netlify y Vercel en plan gratis, a una corrida de pausar los sitios

**Dónde:** cuenta Netlify «Astronomy» (Free, 300 créditos/período) que hostea la app del
Paseo (3 sitios) · Vercel team `astronomyofficial` (Hobby, 4 h de Fluid Active CPU).

**Qué pasó:** los mails de 50/75% de Netlify (02 y 05/10) y el «Approaching your limits» de
Vercel (05/10) quedaron sin leer. Ninguno decía qué se rompe: en los dos planes gratis, al
pasar el 100% **se pausan los sitios** hasta el reset.

**Causa raíz:** Netlify cobra 15 créditos por deploy de producción y `deploy.sh` publica 3
sitios por corrida (45). 6 corridas del 13/09 al 05/10 = 18 deploys = 270/300. Nada en el
script miraba el saldo. En Vercel: 3 h 07 m de 4 h en 30 días; la base fija son los crons
de pg_cron `sync-sheet` (cada hora, ~38 min/mes) y `sync-mp` (~cada 20 min, ~25 min/mes).

**Fix:** `deploy.sh` cuenta los deploys del período y frena antes del build si el próximo
deja la cuenta sin margen (`--forzar` para saltearlo). Probado sobre una copia sin publicar:
lee 270/300 y corta. Vercel: queda la recomendación de pasar a Pro (US$20/mes; Hobby
además es sólo para uso no comercial y la web cobra membresías) — lo decide Facu.

### 2026-10-10 · FAIL ✓ · Paseo: un timeout LEYENDO cortaba el volcado de efectivo del día

**Dónde:** `cierre-mes-nordelta/scripts/volcar_cobros.py` (paso 2 de `efectivo_diario.sh`).

**Qué pasó:** el 02/10 y el 09/10 la tarea salió con código 1: `TimeoutError: The read
operation timed out` en un `values().get`. No dejó nada a medias (falló leyendo, antes de
escribir) y el día siguiente lo levantó la ventana de 60 días, pero cada falla es un mail
de alarma y un día sin volcar.

**Causa raíz:** `googleapiclient` sabe reintentar timeouts, pero sólo si se le pasa
`execute(num_retries=N)`; por default es 0. Ninguna lectura lo pasaba.

**Fix:** las 6 lecturas con `num_retries=4` (`LECTURA_REINTENTOS`). Las 2 escrituras NO:
reintentar un insert duplica un pago. Probado con un `http` que tira 2 timeouts: con el fix
sale al tercer intento; sin el fix falla igual que el 09/10.

**Lección:** toda lectura de Sheets en una tarea programada va con `num_retries`; toda
escritura no idempotente, sin.

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

## 28/10/2026 — `claude -p`: las reglas de archivo son Edit(...) y las rutas absolutas llevan //

Armando el agente de reels diarios (`active/astronomy/contenido/reels_diarios/`), los deny de
`--disallowedTools "Write(**/qa.json)"` NO bloqueaban nada: el CLI avisa que «Write(path) is not
matched by file permission checks — only Edit(path) rules are» (Edit cubre Write). Y una ruta
`Edit(/Users/...)` con una sola barra es relativa al repo: para absolutas va `Edit(//Users/...)`, y
`**/x` sin `//` sólo mira adentro del repo. Probado headless con haiku pidiéndole escribir 5
archivos: con `Edit(//**/qa.json)` queda denegado, con `Edit(//<carpeta del día>/**)` permitido.
**Lección:** un permiso de un agente que corre solo se prueba headless pidiéndole que haga lo
prohibido; leer la regla no alcanza.

## 29/10/2026 — el `claude -p` heredaba el modo «auto» de la config global

El agente de reels diarios hizo un `git commit` que no estaba en su `--allowedTools`:
`~/.claude/settings.json` tiene `defaultMode: auto` y el headless lo hereda, así que un
clasificador aprobaba comandos fuera de la lista. Con eso, un comando de shell podía escribir el
registro o un qa.json esquivando los deny de `Edit(...)`. Fix: `--permission-mode dontAsk`
(niega todo lo que no está listado; probado headless). **Lección:** todo agente headless que
toca el mundo va con `--permission-mode dontAsk` explícito; no alcanza con `--allowedTools`.

## 02/11/2026 — tres fallas silenciosas de las tareas programadas, y un script que el cron iba a deshacer

**`correr.sh` decía «sin red 15 minutos» a los 19 segundos.** Preguntaba por la red en el loop y otra
vez después: con la Mac recién despierta la primera dio bien y la segunda mal, y la tarea moría.
Perdió el radar y el efectivo del 01/11 y el reporte de pauta del 02/11. Fix: se decide una sola vez.
`execution/tests/test_correr_red.py` falló contra el código viejo antes del arreglo.

**La carpeta de 10.000 estuvo 62 h sin correr y nadie se enteró.** No pasaba por `correr.sh`, así que
el radar no la miraba. Se pasó a `correr.sh` con horario fijo; la causa exacta de por qué `StartInterval`
dejó de disparar no se confirmó. Al probarla apareció otra: Claude escribió `PAPER_OK` entre backticks,
el `grep "^PAPER_OK"` no lo vio y una corrida buena mandó mail de falla.

**`cursodj-a-silver.mjs` no iba a durar una hora.** `reconcileSubscriptions` corre cada hora, ve el cobro
de octubre como `cursodj` y reescribía `plan_id`. Se arregló antes de aplicar y se corrió el reconcile real
después: quedó Silver. **Lección:** un script de migración con fecha se prueba contra los crons que
escriben esa misma columna, no sólo con su simulación.

## 02/11/2026 — `cargos_del_mes.py` se cortó a la mitad por la cuota de Sheets

La corrida con `--escribir` pasó el tope de 60 lecturas/escrituras por minuto y murió dos veces: una
antes de CARGOS y otra a mitad de Peak One. Las dos se retomaron bien por el dedupe, pero la segunda
destapó otro bug: **un cargo de $0 no se reconocía como existente** (el dedupe ignora las filas en $0 a
propósito), así que cada re-corrida duplicaba «Peak One / Alquiler» (CARGOS 208; ya pasó en oct, 176/187).
Fix: `_con_reintento_429` en `Planillas` (un 429 no aplica nada, reintentar es seguro; probado con 429
que se recupera, 429 agotado y 500) y el dedupe compara $0 contra $0. **El fix del dedupe no se corrió
contra la planilla**: la re-corrida quedó frenada junto con el borrado de la fila 208.

## 02/11/2026 — emisión de facturas desde el Chrome de Facu, sin `emitir.js`

Los 6 comprobantes de noviembre salieron con la extensión, porque Facu no quiere una segunda ventana.
El robot sigue siendo más seguro para tipear, pero exige el puerto 9333. Se perdió tiempo en dos cosas que
los controles frenaron antes de emitir: el concepto quedó vacío en una factura y en `003 Viáticos Exento`
en una nota de débito (el click cayó en otro renglón porque el viewport cambió de alto). **El dato a
controlar es siempre el campo releído antes de emitir, nunca el click.** FC 21 tuvo un rechazo de WSAA que
se resolvió con Solicitar CAE, sin reemitir: el número no se perdió. Detalle en la memoria de Bejerman.

## 02/11/2026 — reels diarios: el agente confundió un comando negado con «Bash bloqueado»

Primera corrida real con `dontAsk` (el fix del 29/10 se probó con comandos sueltos, nunca una corrida
entera): el agente armó un solo comando con `RD=...; PY=...; $PY ...; $PY ...; ls ...`. Esa forma no
matchea ningún `Bash(...)` de la lista y se negó, que es lo correcto. Con esa única negativa concluyó
«Bash está bloqueado», cortó sin reintentar y salió con 0 reels. Detrás había otra falla: `mkdir -p`
sobre la carpeta del día (ruta entre comillas y con espacios) también se negaba, aunque tenía regla.
Fix: el encabezado del prompt fija la forma de llamar a Bash (un comando por llamada, sin variables,
sin mkdir: `Write` crea la carpeta) y dice que una negativa es de ese comando; se sacaron las reglas
de mkdir. Probado headless con los mismos permisos: indexar, leer_trials, Write y armar_reel, 0 negativas.
**Lección:** un permiso de agente headless se prueba también con la forma en que el agente escribe de
verdad los comandos y con una corrida entera, no sólo con el comando ideal.

## 03/11/2026 — Duplicar un anuncio dejó sin DM a los que comentaron «Gold»

**Síntoma:** comentarios «Gold» en los videos de pauta sin mensaje privado (Facu lo notó).
**Causa raíz:** duplicar un anuncio crea un posteo con otro media ID, y el bot sólo respondía en `instagram_cuenta.media_ids`. `fuera_de_lista` no avisaba a nadie: se rompió en silencio 24 días.
**Arreglo:** los 3 IDs a la lista; un comentario que es sólo la palabra se responde en cualquier posteo (`c076180`, probado rompiendo la línea); `reporte_embudo.py` avisa `fuera_de_lista`.
**Lección:** un filtro que descarta a un cliente tiene que avisar. Y la respuesta privada de Instagram vence a los 7 días: pasado eso no hay rescate por API.

**Corrección del mismo día:** el estado `respondido` no prueba la entrega. A @angelitodicheii la API le dio OK y el chat de Instagram dice que la cuenta no acepta solicitudes de mensaje. Lo reporté como entregado leyendo la API y la respuesta pública, sin mirar el chat: la prueba de un DM es el chat. Instagram tampoco avisa por API, así que el bot no lo puede detectar.


## 04/11/2026 — El espejo de Mercado Pago quedó clavado en el 22/10 y se declaraba sano

**Dónde:** `astronomy-members/lib/espejoMp.ts` (`sincronizarEspejo`, `pedirReporte`). Fix: `496c63f`.

**Qué pasó:** Luqui mandó a AA - Cobranzas una captura de `/admin/mp` que terminaba en el 22/10. Hacía 13 días que la pantalla no traía salidas ni saldo real ($783.134,84 contra $2.187.273,46). Lo vio una persona mirando, no un chequeo.

**Causa raíz:** se pedía siempre un reporte desde el 01/07, y MP pasó a rechazar los rangos de 90 días o más (400 `interval_too_long`). El rechazo sólo llegaba a un `console.error`. El cron seguía bajando el último archivo, le cuadraba el saldo y escribía `error: null`: la frescura se medía por la hora de la corrida, no por la del dato. El 400 está probado el 04/11; que arrancó el 22/10 es inferencia, porque ahí termina la lista de reportes.

**Fix:** rango móvil de 30 días desde medianoche AR, con prueba de encaje antes de escribir, y rojo si el reporte tiene más de 24 h (6 h si MP rechaza el pedido). También se dejó de escribir un reporte que no cuadra.

**Trampa nueva:** `date_created` de MP trae la hora UTC con un `-04:00` falso. Leído tal cual, «pedir cada 40 min» era cada casi 5 h y cualquier alerta de antigüedad salta 4 h tarde. La encontró el agente `numeros`.

**Lección:** cuadrar contra un archivo viejo prueba que el archivo es coherente, no que está al día. Un chequeo de frescura tiene que medir la edad del dato, no la de la corrida.

## 05/11/2026 — Dos publicaciones programadas murieron porque launchd no deja a `shasum` leer el Desktop

**Dónde:** `active/astronomy/contenido/publicar_generico_una_vez.sh` y `publicar_pulgar_una_vez.sh`.

**Qué pasó:** `pulgar-v4` (04/11 18:07) y el video genérico (05/11 12:00) no salieron. El log decía «cambió desde el OK» con el hash vacío, aunque el archivo era idéntico. En el pulgar, además, el mail de aviso falló por un corte de red y la memoria siguió diciendo «sale hoy 18:00» sin que nadie lo mirara.

**Causa raíz:** `--ensayo` se probó desde la sesión, que tiene permiso de macOS sobre el Desktop. Bajo launchd, `shasum` da `Operation not permitted`. Probado con un job descartable: `[[ -s ]]` y la escritura de bash andan, `shasum` falla, el Python del venv lee y escribe (tiene su permiso en TCC). El script comparaba el hash vacío sin chequearlo y lo reportaba como «cambió».

**Fix:** el genérico hashea con el Python del venv y distingue «no pude leer» de «cambió». El pulgar no se tocó: su fecha pasó y necesita un OK nuevo de todos modos.

**Lección:** un ensayo desde la sesión no prueba lo que va a pasar bajo launchd. Lo que toca el Desktop en una tarea programada se ensaya con `launchctl submit`.

## 06/11/2026 — El efectivo diario dijo «no coinciden» dos mañanas cuando era la red

**Dónde:** `.claude/skills/cierre-mes-nordelta/scripts/efectivo_diario.sh`, paso 1.

**Qué pasó:** el 05/11 y el 06/11 el job cortó con «la app y la planilla no coinciden». En los dos casos fue un timeout de red al bajar el Master Plan; el 06/11 la corrida duró 1 h 38 min. Corrido a mano a las 09:54: 655 = 655, nada que volcar. No se perdió ningún cobro.

**Fix:** el mensaje ahora dice que el paso 1 se corta por diferencia O por no poder bajar los datos, y manda a mirar el error. Queda sin resolver por qué la red de la Mac falla a esa hora.

**Lección:** el mismo patrón que el `shasum` del 05/11: un chequeo que no pudo leer no tiene que reportar un veredicto.

## 11/11/2026 — Jarvis de escritorio: «no tengo el dato» con el dato en disco, y un pkill que no mataba nada

**Dónde:** `execution/jarvis/servidor.py`.

**Qué pasó (1):** se le preguntó por voz cuántos alumnos activos había. Contestó que no tenía el número, y estaba en `data/jarvis/numeros.json` (19). La instrucción decía «usalo», pero Claude busca con Glob y `data/` está gitignoreada.

**Fix:** los números del día van pegados adentro de cada pregunta, con hora y fecha, y marcados VIEJOS si no son de hoy.

**Qué pasó (2):** el servidor se reiniciaba con `pkill -f "jarvis/servidor.py"`, pero se había arrancado como `python servidor.py`, desde su carpeta. El pkill no matchea nada, el arranque nuevo muere por puerto ocupado y las pruebas «en vivo» le pegan al código viejo. Se detectó porque no aparecían los headers nuevos.

**Fix:** se arranca siempre con path absoluto (`jarvis.sh`), y para matar se busca por puerto (`lsof -tiTCP:7777`).

**Lección:** después de reiniciar un servidor, se verifica que el proceso que escucha es el nuevo: PID y comando, o algo que sólo tiene el código nuevo. Y un dato que el modelo «tiene que ir a buscar» no cuenta como dato: si importa, va en el prompt.

**Revisión (code-reviewer + qa, 60 tests en `execution/tests/test_jarvis.py`):** encontró un doble «Sí» concurrente que podía ejecutar un plan dos veces (pasaba en 1 de cada ~10 corridas) y un plan ya ejecutado que podía revivir. Se arregló con un lock sobre todo leer-modificar-guardar de `estado.json`. Después del fix, 10 corridas seguidas en verde.

**Y una más, la misma noche:** el plist del brief le pasaba a `correr.sh` el comando en dos partes (python | brief.py). `correr.sh` toma solo la primera, así que corría Python sin script: «éxito» en 0 segundos, código 0, sin brief. Se vio porque la hora del brief no cambió. **Fix de raíz:** `correr.sh` ahora corta con código 64, notificación y registro si el comando viene en más de una parte. Se probó con el plist viejo: saltó. Las otras 13 tareas estaban bien.

**v2, misma noche: Jarvis como intermediario completo.** Facu: «que todo lo que le digo te comande a vos». El cerebro pasó de solo lectura a Claude Code completo (`--permission-mode auto`), con tareas en segundo plano (otra sesión, abrible en Terminal o Antigravity). Dos trampas:
- **Retomar la sesión vieja arrastra lo que creía.** Con el prompt nuevo seguía diciendo «estoy en solo lectura»: el historial le ganó al prompt nuevo. Cuando cambian los poderes de un agente, se arranca sesión nueva.
- **La regla 10 iba solo por instrucción.** La revisión lo marcó. Ahora es con llave: `--disallowedTools "Bash(*--send*)"` + envío de Gmail. Probado en vivo: `echo hola --send` bloqueado, `echo hola` corre; un mail pedido por voz vuelve como PLAN. Las pruebas rompen la llave a propósito y fallan.

## 12/11/2026 — «Hey Jarvis»: medición y una trampa de prueba

- **Medición antes de prenderlo** (openWakeWord `hey_jarvis`, umbral 0,5): 0 disparos en 78 min de música
  (playlist del Paseo + producciones de Facu) y 25 min de la voz de Jarvis. Música encima de la palabra
  dicha en inglés: sigue en 1,00. Dicha con acento castellano (voces Diego/Mónica): 0,4–0,5 → si a Facu no
  lo agarra, bajar `JARVIS_UMBRAL_DESPERTAR`, no reentrenar.
- **Trampa:** los Chrome headless de prueba (`--remote-debugging-port`) quedaron vivos tras `ch.kill()`,
  seguían sondeando con token válido y, sin micrófono, apagaban la escucha para todos (el estado es
  compartido). Parecía un bug de carrera del servidor. Al terminar una prueba: `pkill -f remote-debugging-port`.
- Chrome headless con `--use-file-for-fake-audio-capture` entrega silencio: para probar de punta a punta
  se reemplaza `getUserMedia` por un `MediaStreamDestination` que reproduce el wav.
