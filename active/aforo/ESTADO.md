# Aforo — estado

Última actualización: 2026-08-10 · **negocio nuevo, nada en producción todavía**

**Qué es.** La ticketera como producto propio, separada de la academia y de la web de
Astronomy. Cualquier productora crea su cuenta, arma su fecha y vende; el que compra tiene
**una sola cuenta** para todas las productoras de Aforo.

**El nombre lo eligió Facu el 10/08/2026: Aforo.** El aforo es cuánta gente entra en un
lugar, que es lo que la ticketera administra. Cinco letras, se dicta por teléfono sin dudas
—importa: alguien lo va a dictar en una puerta a las 3 AM— y sirve para una fiesta, un
teatro o un congreso sin sonar a ninguno de los tres.

**Dominio: LIBRES LOS DOS, verificado el 10/08/2026 contra el registro oficial.** NIC.ar sí
tiene RDAP público —`https://rdap.nic.ar/domain/<dominio>`, 404 = libre— y el endpoint se
comprobó primero contra `mercadolibre.com.ar`, `google.com.ar`, `nic.ar` y `afip.gob.ar`,
que devuelven 200 con datos. Sobre esa base:

| Dominio | Estado | Arancel NIC.ar (registro y renovación, por año) |
|---|---|---|
| `aforo.com.ar` | **libre** | **$8.500** |
| `aforo.ar` | **libre** | **$25.500** |
| `aforo.net.ar` · `elaforo.com.ar` | libres | $8.500 c/u |

**Recomendación: registrar los dos** ($34.000/año), con **`aforo.com.ar` como el principal**
—el que se dicta, se imprime y se manda— y `aforo.ar` redirigiendo. El motivo no es estética:
en Argentina el que escucha "aforo punto a-erre" tipea `aforo.com.ar` por reflejo, y si ese
lo tiene otro, el tráfico se le regala. $8.500 más por año es barato al lado de eso.

Falta confirmar una sola cosa, y sólo NIC.ar la puede contestar al intentar el alta: que
`aforo` no esté en su lista de términos reservados. **El registro lo tiene que hacer Facu**
con su CUIT y clave fiscal de AFIP.

Si algún día tiene que ser `.com`, `elaforo.com` está libre verificado por RDAP de Verisign.
Todos los `.com` de una palabra en español están tomados.

> ⚠️ **Cómo se verifica un dominio, porque me equivoqué el 10/08:** `dig` NO sirve —
> reporté `molinete.com` y `pista.com` como libres y estaban registradas desde 2003 y 2002,
> sin NS delegados. Se usa RDAP, que es el registro oficial:
> `curl -o /dev/null -w "%{http_code}" https://rdap.verisign.com/com/v1/domain/<dominio>`
> → **404 = libre**, 200 = registrado.

---

## Decisiones tomadas (Facu, 10/08/2026)

| | |
|---|---|
| **Base** | Proyecto de Supabase **nuevo**. La base de compradores no tiene nada que ver con la de alumnos. |
| **Astronomy** | **No se muda.** Sigue vendiendo sus fechas en astronomyofficial.com. Aforo es para las demás productoras. |
| **Cuenta del comprador** | **Una sola** para todas las productoras de Aforo. La identidad es de la plataforma: es el activo. |
| **Dominio por productora** | `aforo.ar/<productora>` (path o subdominio). El dominio propio de una productora obliga a hacer SSO y se deja para cuando alguna lo pida y lo pague. |
| **Modelo** | Gratis para la productora. Aforo se queda los contactos. |
| **Comisión** | **5% al que compra la entrada, 0% para Astronomy.** Es **por productora**, no global. Arranca en 0 y se prende con volumen. |
| **La plata de la entrada** | Va **directo a la cuenta de la productora**, por **OAuth de Marketplace de Mercado Pago** — nunca pegando un access token a mano. Aforo retiene el fee como `application_fee`. |
| **Alta de una fecha** | Camino **obligatorio** de 4 pasos: datos → puerta → cobro → publicar. Borrador desde el paso 1. |
| **Clave de puerta** | **La genera el sistema**, por fecha, corta y dictable. |
| **Canje de créditos de Academy** | El alumno **elige la fecha y recibe el QR en el momento**. Sin códigos de descuento. |

**Por qué el OAuth no es un detalle:** que la plata vaya directo a la productora y que Aforo
cobre un % **no son excluyentes**. Con OAuth de Marketplace se tienen las dos y el fee es un
número que se cambia. Con access tokens pegados a mano, el día que se quiera cobrar hay que
**reconectar a todas las productoras una por una** — con cientos, eso no se hace nunca.

---

## ✅ El eje está escrito Y PROBADO (10/08/2026)

`probar-esquema.mjs` corre `ESQUEMA_EJE.sql` sobre **Postgres 18 real** (PGlite, en WASM) sin
Docker y sin gastar un peso: **26 chequeos en verde**. Se corre con
`cd active/aforo && node probar-esquema.mjs`.

Lo que quedó demostrado, no opinado:

- **El dueño de Puzzle ve 1 fecha, no 2.** No puede leer la clave de puerta de otra
  productora, ni editarle una fecha, ni crear una a su nombre. Las tres cosas probadas
  entrando como él, con su uid, igual que hace Supabase.
- **Una fecha no se publica sin Mercado Pago conectado** (lo garantiza un trigger, no el
  formulario) y el error lo dice en castellano. Pero **sí se guarda como borrador**: no se
  pierde lo cargado. Conectando MP, se publica y se sella la fecha sola.
- Un slug con mayúsculas se rechaza, un fee del 120% se rechaza, dos productoras no comparten
  slug **pero sí pueden tener cada una su «aniversario»**, y dos fechas no comparten ID de
  puerta. Una productora con fechas **no se borra de un tirón**.

🔎 **Lo que el test encontró y yo no había visto:** en Supabase, una tabla nueva de `public`
**nace con GRANT para `anon`** por los default privileges del proyecto — o sea, nace publicada
en PostgREST y lo único que la tapa es la RLS. El esquema ahora **revoca todo y da sólo lo que
hace falta**, y revoca los default privileges para las tablas que se creen mañana. Dos rejas y
no una. Es la tercera cara del mismo bug que ya cayó tres veces en la academia.

⚠️ **Lo que esto NO prueba, y hay que probar en la nube:** PostgREST con la anon key de verdad
(pegándole con `curl` y contando filas) y Auth. Probado ≠ probado todo.

## Dónde se prueba la app entera (decidido el 10/08/2026)

**Supabase local con Docker.** Es gratis, se resetea a cero en segundos —y el plan es correr
el test de punta a punta N veces— y sobre todo **da lo único que PGlite no dio: PostgREST con
la anon key de verdad y Auth**, que es exactamente lo que quedó sin probar del eje.

Las otras dos se descartaron por motivos, no por precio:

- **La base de Astronomy con un esquema aparte, NO.** Ya está decidido que la base de
  compradores no comparte nada con la de alumnos, y el riesgo no es teórico: hay dos refs de
  Supabase parecidos y un `ref` equivocado escribe en el negocio equivocado sin avisar. Meterle
  tablas nuevas a la base que hoy cobra membresías, para probar, es la peor combinación.
- **US$25/mes ahora, tampoco:** se pagaría por algo que todavía no existe. Ese gasto arranca el
  día que Aforo salga a producción — y ahí **sí o sí**, porque el free tier no tiene backups y
  una base con órdenes pagas y QR emitidos no puede vivir sin backup diario.

**Lo único que no se puede probar 100% local** es el OAuth de Mercado Pago y sus webhooks:
necesitan una URL pública para el callback. Se resuelve con un túnel a localhost
(`cloudflared tunnel --url http://localhost:3000`), gratis y sin cuenta.

Docker Desktop es **gratis** para empresas de menos de 250 empleados y menos de US$10M de
facturación. La Mac es **Apple Silicon (M1)**: va el build `arm64`.

## Lo que falta antes de aplicar la primera tabla

1. 🔴 **US$25/mes: el tercer proyecto de Supabase no entra en el free tier.** El límite es de
   **2 proyectos free por CUENTA** (no por organización, como suponía) y Facu ya tiene los dos
   en producción: Astronomy Oficial y Paseo Nordelta. La API lo dijo así al intentar crearlo.
   La org **`Aforo` ya está creada y vacía** (`sgsaxobnhldomziaklpm`), sin costo. Para poner el
   proyecto adentro hay que pasar esa org a **Pro: US$25/mes**.

   Y un motivo extra para pagarlo recién al salir a producción, pero pagarlo: **el free tier
   no tiene backups**. Una base con órdenes pagas y QR emitidos sin backup diario no puede ir
   a producción.
2. 🟡 **Repo nuevo o el mismo.** Facu quiere Aforo *"que no tenga nada que ver con la web de
   astronomy"*, y hay un argumento fuerte para **repo y deploy separados**: él pidió *"que
   nunca se caiga la página"*, y con un solo deploy un bug de Aforo tira abajo
   astronomyofficial.com, que hoy cobra membresías. El costo de separar es la **duplicación**
   del validador, el design engine y el QR. Recomendación: **repo nuevo**, copiando
   deliberadamente esas piezas, y extraerlas a un paquete compartido recién cuando duela.
   El acoplamiento se paga siempre; la duplicación se paga cuando aparece.
3. 🟡 **La fecha de Puzzle.** Facu: *"después la vemos, primero quiero hacer 500 pruebas"*.

---

## Los cinco criterios de Facu, traducidos a algo verificable

Textual (10/08/2026): *"primero quiero hacer 500 pruebas de que esto funciona de principio a
fin"*, y después los cinco criterios de abajo. Tal como los dijo no se pueden verificar —
"la mejor estética" no falla nunca. Así quedan medibles:

| Lo que pidió | Cómo se verifica |
|---|---|
| **Que el productor vea todas sus finanzas de todos sus eventos** | Un panel que suma **N fechas**, no una. El chequeo: cargar 3 fechas con plata distinta y que el total del panel dé **igual a la suma calculada aparte en Python**, contra la base. Es el skill `consenso` aplicado a una pantalla. |
| **Que su base de datos esté perfecta** | Exportar la base de una fecha y que la cantidad de filas **coincida con las órdenes pagas**. Y el aislamiento: la productora A pidiendo la base de la B tiene que dar **0 filas, pegándole con `curl`**. |
| **Que el que compra tenga la mejor experiencia** | Se mide, no se opina: **cuántos clicks y cuántos segundos** de la página de la fecha al QR en el mail. Se cronometra en cada corrida y no puede subir. |
| **Que las cortesías lleguen sin problema** | Emitir 30 de una lista pegada y verificar que **las 30 tienen QR válido y distinto**, y que **los 30 mails salieron** (hoy en Astronomy los mails NO se mandan solos — en Aforo eso tiene que estar). |
| **Que nunca se caiga** | Lo que tira una ticketera es la fecha con 500 personas comprando a la vez. El chequeo: **N compras concurrentes de la última entrada** y que se venda **exactamente una** — nunca 2, nunca 0. Es la prueba de sobreventa y hoy no existe. |
| **La mejor estética** | Medir en el navegador, no mirar la captura: contraste ≥ 4,5:1 en todo texto, tamaños parejos, y **imprimir el `<h1>`** para saber qué se capturó. Ver `medir-en-pantalla-chrome-headless`. |

**El test que resume todo, y que hay que poder correr N veces:** crear productora → crear
fecha → conectar MP (sandbox) → publicar → comprar de verdad → recibir el QR → escanearlo en
la puerta → ver esa plata en el panel de la productora. Si eso corre solo y en verde, el
producto funciona de punta a punta. **Que sea scriptable de entrada condiciona la
arquitectura**, y por eso se decide ahora y no después.

---

## Lo que se porta de `astronomy-members` (no se reescribe — Ley 8)

Ya funciona y está probado apretando los botones: carrito, design engine que saca la piel
del flyer, QR, validador `/puerta` con modo offline y service worker, mesas con sectores,
comisiones escalonadas por RRPP, cortesías masivas pegando dos columnas del Excel, panel de
RRPP por link privado, y las fechas que se apagan solas. Todo eso hoy asume **una sola
productora**: lo único que falta es el eje de dueño, que está en `ESQUEMA_EJE.sql`.
