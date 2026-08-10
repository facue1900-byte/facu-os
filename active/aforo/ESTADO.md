# Aforo — estado

Última actualización: 2026-08-10 · **negocio nuevo, nada en producción todavía**

**Qué es.** La ticketera como producto propio, separada de la academia y de la web de
Astronomy. Cualquier productora crea su cuenta, arma su fecha y vende; el que compra tiene
**una sola cuenta** para todas las productoras de Aforo.

**El nombre lo eligió Facu el 10/08/2026: Aforo.** El aforo es cuánta gente entra en un
lugar, que es lo que la ticketera administra. Cinco letras, se dicta por teléfono sin dudas
—importa: alguien lo va a dictar en una puerta a las 3 AM— y sirve para una fiesta, un
teatro o un congreso sin sonar a ninguno de los tres.

**Dominio: pendiente de registrar.** `aforo.ar` (8 caracteres) es la primera opción y
`aforo.com.ar` la segunda; las dos aparecen sin delegar pero **NIC.ar no tiene registro
público, hay que confirmarlo ahí**. Si tiene que ser `.com`, `elaforo.com` está **libre
verificado por RDAP**. Todos los `.com` de una palabra en español están tomados.

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

## Lo que falta antes de aplicar la primera tabla

1. 🔴 **En qué organización de Supabase va el proyecto.** Hoy hay dos orgs, una por negocio
   (`Astronomy` y `Paseo Nordelta`), con un proyecto cada una. El free tier permite 2
   proyectos activos **por organización**, así que probablemente sea gratis — **pero el
   endpoint de facturación no existe en la API pública y no pude confirmarlo**. No se crea
   sin OK de Facu: puede facturar (Constitución, regla 6).
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
