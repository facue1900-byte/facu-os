# Astronomy Academy — Roadmap de crecimiento, 90 días

`04/08/2026` · Todos los números salen de la base (`qeakrjnseboiulcojlcw`) y de las memorias
de pauta, medidos el 04/08/2026. **Lo que es estimación está marcado como tal, con el
supuesto escrito.** Lo que necesita un dato que hoy no existe, también.

---

## 1. Dónde está parado el negocio

| Métrica | Valor | Cómo se midió |
|---|---|---|
| Facturación julio | **$3.026.640** (20 pagos) + $184.800 cargados a mano | `sales`, `manual_payments` |
| Alumnos que pagan hoy | **22** (15 Curso de DJ · 4 Silver · 3 Gold) + 2 DJ Delivery | `subscriptions` status `authorized`, sin internos |
| Ticket promedio | **~$150.000** · Curso de DJ es el 70% del volumen | `sales` |
| Retención jun → jul | **80%** (16 de 20 volvieron a pagar) | cohorte sobre `sales` |
| Vida media del alumno | **44 días** (Curso DJ) · 62 (Silver) · 52 (Gold) | `subscriptions` canceladas vs primer pago |
| LTV estimado | **$215.000 – $290.000** | vida media × ticket |
| Ocupación del estudio | **26%** (cabina 44% · estudio de producción **7%**) | `slot_bookings` julio vs `studio_hours` |
| Créditos entregados y no usados | **22.840 de 38.570 (59%)**, y 4.080 ya vencieron sin usarse | `credit_lots` |
| Pauta | **US$590/mes** → 232 conversaciones de WhatsApp → **3 primeros pagos** | memorias de pauta + `sales` |
| Conversión conversación → alumno | **1,3%** · CAC ~US$170 | ídem |
| Bajas pedidas por el alumno | **0 de 29.** Todas administrativas ("dejó de pagar") | `cancellations` |

### Las tres cosas que dicen los datos

**1. El negocio no tiene un problema de producto: tiene un problema de embudo.**
Retención del 80% mes a mes y 190 clases dadas en julio son números de un producto que
funciona. Pero en 3 semanas entraron **12 cuentas nuevas** y pagaron **3**. El motor de
adquisición está apagado, no roto: la plata de pauta se gasta, las conversaciones llegan,
y se caen antes de la cuenta.

**2. El agujero está en WhatsApp, y no tiene fondo medido.**
232 conversaciones en julio → 3 primeros pagos. **De cada 100 personas que escriben, 98,7
no compran, y no existe un solo registro de qué les pasó.** No hay tiempo de respuesta, no
hay etiquetas, no hay seguimiento. Todo lo demás de este documento vale menos que esto.

**3. Se está entregando la mitad de lo que se cobra.**
59% de los créditos comprados no se usaron. El estudio está vacío el 74% del tiempo. Un
alumno que paga $143.520 y no viene, no renueva — y como nadie cancela formalmente, el
negocio se entera un mes tarde, cuando José lo da de baja "por dejar de pagar".

---

## 2. Auditoría por etapa

### Llegada (pauta → WhatsApp)
- **Bien:** US$1,94 por conversación es barato. El histórico de la cuenta tiene creativos a
  US$0,67 (`Curso DJ 2`, 228 conversaciones) — hay techo probado para mejorar.
- **Mal:** el 100% del presupuesto activo apunta al producto más barato del catálogo. Tres
  anuncios comparten exactamente el mismo copy y compiten entre sí.
- **Falta medir:** de qué anuncio viene cada conversación. Hoy todas caen al mismo WhatsApp
  sin distinción.
- **Automatizar:** un `wa.me` distinto por anuncio, con texto prellenado ("Hola, vengo por
  el Curso de DJ — #DJ2"). Cero código, se cambia en el administrador de anuncios.

### Landing (`/academy`, `/curso-profesional-dj`)
- **Bien:** carga prerenderizada, precios en vivo desde la base, pixel instalado el 31/07.
- **Mal:** la pauta no manda a la web, manda a WhatsApp. El pixel mide un tráfico que casi
  no existe.
- **Falta medir:** visitantes. No hay analytics de visitas propio ni en el panel.
- **Construir (chico):** guardar `utm_source` y `referrer` al crear la cuenta. Son ~15
  líneas y es la única forma de saber qué campaña trae a los que **pagan**, no a los que
  hacen click.

### Registro
- **Bien:** la cuenta se crea dentro del flujo de compra — no hay fricción de "registrate
  primero" separada del pago.
- **Mal:** eso hace que "creó cuenta y no compró" sea el peor momento posible para
  perderlo: la persona ya puso mail y nombre, estaba en la caja.
- **Dato:** **24 cuentas sin ningún pago**, 9 de ellas en las últimas 3 semanas.
- **Automatizar:** mail + WhatsApp a las 2 horas de abandonar. Hoy no se hace nada.

### Checkout
- **Bien:** módulo cerrado, atómico, con plan B. No es el cuello de botella.
- **Dato:** 6 suscripciones quedaron en `pending` (arrancó el checkout de Mercado Pago y no
  autorizó).
- **Falta medir:** en qué paso se cae. Con 6 casos, se resuelve preguntándoles, no
  instrumentando.

### Primer acceso / primera clase
- **Bien:** 18 de 25 pagadores agendaron en la web; casi todos dieron clase alguna vez.
- **Mal:** no hay ningún mail de bienvenida que diga "tu próximo paso es agendar". El único
  mail automático del sistema es el recordatorio 34hs antes de una clase **ya agendada**.
- **Automatizar:** mail de bienvenida a las 2 horas del pago, con un solo botón: agendar la
  primera clase.

### Primer mes
- **Mal, y es lo más caro:** el Curso de DJ da 240 créditos (4 clases) que **vencen al mes**.
  Hoy hay al menos **6 alumnos con 240 créditos venciendo entre el 13 y el 22 de agosto y
  ninguna clase agendada**. Cada uno pagó $143.520 por esos créditos.
- **Falta medir:** nada. El dato está, no lo mira nadie.
- **Automatizar:** aviso a los 10 y a los 3 días del vencimiento, con el link de agendar.

### Renovación
- **Bien:** 80% de retención mes a mes. Mercado Pago cobra solo.
- **Mal:** Silver tiene **69% de churn** (9 bajas de 13) y es el único plan donde el alumno
  consume **130% de sus créditos** — se queda corto todos los meses y en vez de subir a
  Gold, se va.
- **Construir (chico):** cuando un Silver llega al 100% de sus créditos antes de fin de mes,
  ofrecerle Gold (+$52.080/mes) en la pantalla y por mail.

### Recomendaciones
- **Mal:** existe la plomería (`shared_accesses`, invitaciones grupales) y está sin uso: 2 y
  3 registros en toda la historia.
- **Dato que la habilita:** con un LTV de ~$215.000 se puede pagar muy bien un referido.
- **Proceso, no código:** pedirlo a mano a los 15 alumnos activos del Curso de DJ. Si
  funciona, después se automatiza.

### Reactivación
- **Mal:** 16 ex-alumnos que ya facturaron **$1.041.680** y a los que nunca nadie les
  escribió. Ninguno se dio de baja: dejaron de pagar y los bajó José.
- **Falta medir:** **por qué se fueron. No existe un solo dato.** Es la pregunta más barata
  y más valiosa del negocio.

---

## 3. Roadmap ordenado por ROI

Cada estimación de plata dice su supuesto. Donde no hay base para estimar, dice
**"requiere dato nuevo"** en vez de inventar un número.

### QUICK WINS — menos de un día

#### QW1 · Etiquetar y cronometrar el WhatsApp *(cero código)*
- **Qué:** 4 etiquetas en WhatsApp Business (`Nuevo` · `Contestado` · `Cotizado` · `Cerrado`)
  y una fila por conversación en una planilla: fecha, de qué anuncio vino, si contestó, si
  cerró. Dos semanas.
- **Por qué está primero:** es el 98,7% de la pérdida y **hoy no se puede decidir nada sobre
  pauta sin este dato**. Todo lo demás del roadmap compite por migajas al lado de esto.
- **Plata:** *requiere dato nuevo para estimar el piso*. Techo si la conversión pasa de 1,3%
  a 5% (1 de cada 20, estándar bajo para un lead que escribió por voluntad propia):
  **+8 alumnos/mes = +$1.148.160/mes**, sin gastar un dólar más de pauta.
- **Métrica:** conversaciones → cuentas → pagos, por semana. Y tiempo de primera respuesta.
- **Dificultad:** baja · **Tiempo:** 30 min de setup + 2 min por conversación · **Riesgo:**
  nulo. Depende de que José lo sostenga: si no se sostiene 2 semanas, no sirve.
- **Cómo validar:** al día 14 tenés el número real. Si el tiempo de respuesta es > 1 hora,
  ahí está la fuga y se ataca con QW2.

#### QW2 · Un `wa.me` distinto por anuncio *(cero código)*
- **Qué:** cambiar el link de cada anuncio para que el mensaje prellenado traiga un código
  (`#DJ2`, `#REEL`, `#PRO`). Se hace en el administrador de anuncios.
- **Plata:** no genera sola; **habilita** decidir dónde poner los US$590/mes. Hoy se reparten
  a ciegas entre 3 anuncios con el mismo copy.
- **Métrica:** conversaciones y cierres por código.
- **Dificultad:** baja · **Tiempo:** 20 min · **Riesgo:** nulo.

#### QW3 · Escribirles a los 6 que tienen créditos venciendo *(a mano, esta semana)*
- **Qué:** los 6 alumnos con 240 créditos que vencen entre el 13 y el 22/08 sin clase
  agendada. Un mensaje personal: "te quedan 4 clases y vencen el 13, ¿qué día venís?".
- **Plata:** **$861.120/mes de recurrencia en riesgo** (6 × $143.520). Supuesto: un alumno
  que deja vencer 4 clases pagadas no renueva. Es la hipótesis más razonable con vida media
  de 44 días, pero **no está probada** — QW3 la prueba.
- **Métrica:** cuántos de los 6 agendan en 7 días, y cuántos renuevan.
- **Dificultad:** baja · **Tiempo:** 30 min · **Riesgo:** nulo.

#### QW4 · Preguntarles a los 16 que se fueron por qué se fueron
- **Qué:** un mensaje corto a los 16 ex-alumnos ($1.041.680 facturados históricamente).
  Una sola pregunta abierta. Sin oferta todavía — primero entender.
- **Plata:** *requiere dato nuevo*. Si 3 de 16 vuelven: **+$430.560/mes**.
- **Métrica:** respuestas por motivo. Con 5 respuestas ya sabés más de lo que sabés hoy.
- **Dificultad:** baja · **Tiempo:** 1 hora · **Riesgo:** bajo (alguno puede contestar feo;
  es información igual).

#### QW5 · Escribirles a los 9 que crearon cuenta y no pagaron
- **Qué:** los 9 de las últimas 3 semanas. Llegaron a la caja y se fueron.
- **Plata:** si cierra 2: **+$287.040** de una, más su recurrencia.
- **Métrica:** cuántos responden y cuántos pagan en 7 días.
- **Dificultad:** baja · **Tiempo:** 30 min · **Riesgo:** nulo.

---

### ALTO IMPACTO — 1 a 3 días

#### AI1 · Aviso automático de créditos por vencer *(cron + mail)*
- **Qué:** a los 10 y a los 3 días del vencimiento, mail con las clases que le quedan y un
  botón para agendar. La plomería existe (Resend, `brandEmail`, cron diario de Vercel).
- **Por qué acá:** convierte QW3 —que es manual y no escala— en un proceso que corre solo
  todos los meses.
- **Plata:** hoy vencen 4.080 créditos sin usar (10,6% de lo entregado). Recuperar la mitad
  son **~1.100 créditos/mes de consumo** = clases dadas = renovaciones que no se caen.
  Impacto real sobre recurrencia: **estimado $400.000–$860.000/mes**, según cuántos de los
  que dejan vencer efectivamente renuevan. *El rango se cierra con el resultado de QW3.*
- **Métrica:** % de créditos que vencen sin usar (hoy 10,6%), y clases agendadas dentro de
  los 7 días del aviso.
- **Dificultad:** media · **Tiempo:** 1 día · **Riesgo:** bajo. **Cuidado:** que no se
  convierta en spam — dos avisos por ciclo, no más.

#### AI2 · Mail de bienvenida con un solo botón: agendá tu primera clase
- **Qué:** a las 2 horas del primer pago. Hoy no existe ningún mail de bienvenida.
- **Plata:** *requiere dato nuevo* (no está medido cuánto tarda hoy un alumno nuevo en
  agendar). El supuesto de la industria —cuanto antes usa el producto, más retiene— es
  fuerte, pero acá no está verificado.
- **Métrica:** días entre el primer pago y la primera clase agendada, antes y después.
- **Dificultad:** media · **Tiempo:** 1 día · **Riesgo:** bajo.

#### AI3 · Guardar de dónde vino cada cuenta *(`utm_source` + `referrer`)*
- **Qué:** ~15 líneas al crear la cuenta, más una columna en `profiles`.
- **Por qué:** sin esto, **escalar pauta es apostar**. Y hay un techo de US$500/mes que
  sólo se puede levantar con un número medido (regla ya escrita en la memoria de pauta).
- **Plata:** no genera directo. Es lo que permite decidir si el próximo dólar de pauta vale.
- **Métrica:** % de pagos con origen conocido.
- **Dificultad:** baja · **Tiempo:** 2 horas · **Riesgo:** bajo.

#### AI4 · Recuperación automática de checkout abandonado
- **Qué:** si creó cuenta y no pagó en 2 horas → mail; a las 24hs → aviso a José para que
  escriba por WhatsApp.
- **Plata:** al ritmo actual (9 abandonos cada 3 semanas), recuperar 1 de cada 3 son
  **+$430.560/mes**. Supuesto de tasa de recuperación: 33%, que es alto para un mail solo y
  razonable con el WhatsApp de José atrás. *Se valida con QW5 antes de construirlo.*
- **Métrica:** abandonos recuperados / abandonos totales.
- **Dificultad:** media · **Tiempo:** 1 día · **Riesgo:** bajo.

---

### PROYECTOS — hasta una semana

#### P1 · Llenar la capacidad ociosa con una oferta de entrada
- **El dato:** el estudio está vacío el **74% del tiempo**; el estudio de producción, el
  **93%** (12 horas en todo julio). El costo del local ya está pagado: cada hora vendida ahí
  es margen casi puro menos el profe.
- **Qué:** una clase suelta de prueba a precio de entrada, en las franjas muertas, como
  primer escalón hacia la membresía. Y usar esas horas como incentivo de referido.
- **Plata:** llenar 20 horas/mes de las 256 vacías a ~$34.000 la clase = **+$680.000/mes**
  bruto. Supuesto: precio equivalente al de una clase dentro de la membresía (60 créditos ×
  $574). **Requiere decisión de Facu sobre precio y sobre si canibaliza la membresía** — es
  la parte que no puedo decidir con datos.
- **Métrica:** ocupación semanal (hoy 26%) y cuántos de prueba pasan a membresía.
- **Dificultad:** media (proceso comercial + una pantalla) · **Tiempo:** 3–5 días ·
  **Riesgo:** medio — canibalización. Se prueba 1 mes con cupo limitado.

#### P2 · Upgrade Silver → Gold cuando se queda sin créditos
- **El dato:** Silver consume **130%** de su plan y tiene **69% de churn**. Se quedan cortos
  todos los meses y se van en vez de subir.
- **Qué:** cuando un Silver llega al 100% de sus créditos, mostrarle el upgrade en `/member`
  y mandarle un mail con el diferencial exacto ($52.080/mes por 110 créditos más).
- **Plata:** si 2 de los 4 Silver activos suben: **+$104.160/mes recurrente**. El upside
  real está en dejar de perder Silvers: cada uno que no se va vale $143.520/mes.
- **Métrica:** upgrades/mes y churn de Silver (hoy 69%).
- **Dificultad:** media · **Tiempo:** 2–3 días · **Riesgo:** bajo.

#### P3 · Programa de referidos con premio en créditos
- **El dato:** LTV ~$215.000 y la plomería de invitaciones ya existe sin uso.
- **Qué:** el alumno que trae a alguien que paga, recibe créditos (equivalente a 1–2 clases).
  Se paga solo con una fracción del primer mes.
- **Plata:** si 3 de los 22 activos traen 1 cada uno: **+$430.560/mes** con un costo de
  ~$103.000 en créditos (que además llenan horas ociosas, o sea costo marginal bajo).
- **Métrica:** referidos que pagan / alumnos activos.
- **Dificultad:** media · **Tiempo:** 3–4 días · **Riesgo:** bajo. **Antes de construirlo:
  pedirlo a mano a 15 alumnos** (QW). Si nadie refiere pedido a mano, tampoco lo va a hacer
  con un botón.

---

## 4. Lo que NO haría

- **Modo Profesional ($440.000): 0 ventas.** Es el producto más caro y no vendió una sola
  unidad. **No le pondría más pauta ni más desarrollo hasta entender por qué**: puede ser
  precio, puede ser que el público de Nordelta no esté para eso, puede ser el creativo. Con
  cero ventas no hay nada que optimizar — hay que preguntarle a 10 personas.
- **Subir el presupuesto de pauta.** Con 1,3% de conversión, cada dólar extra compra más
  conversaciones que se pierden igual. Primero QW1.
- **Cualquier cosa nueva sobre pagos.** Congelado.

---

## 5. Los 14 días que vienen, en orden

1. **Día 1:** QW1 (etiquetas de WhatsApp) + QW2 (`wa.me` por anuncio). 1 hora en total.
2. **Día 1:** QW3 (los 6 con créditos venciendo) y QW5 (los 9 que no pagaron). 1 hora.
3. **Día 2:** QW4 (los 16 que se fueron).
4. **Días 3–5:** AI3 (origen de la cuenta) y AI1 (aviso de vencimiento).
5. **Día 14:** leer el resultado de QW1 y **recién ahí** decidir si el problema es volumen
   de conversaciones, tiempo de respuesta, o la oferta.

**La regla que ordena todo esto:** el negocio hoy no sabe por qué pierde al 98,7% de la
gente que le escribe. Hasta que ese número tenga cara, cualquier cosa que construyamos es
una apuesta con nuestra plata.
