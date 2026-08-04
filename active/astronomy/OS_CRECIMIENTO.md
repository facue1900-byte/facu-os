# OS de Crecimiento — Astronomy Academy

`v1 · 04/08/2026` · **Documento vivo.** Se actualiza al cierre de cada sprint, nunca se
reescribe entero: lo viejo queda tachado con la fecha, para poder ver en qué nos
equivocamos.

**Objetivo de 12 meses: pasar de 22 a 44 alumnos activos.**

Cada afirmación va etiquetada. Nunca se mezclan:

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra la base, la planilla de finanzas o la API. Reproducible. |
| **[INFERENCIA]** | Calculado a partir de hechos. La aritmética es sólida; los supuestos se dicen. |
| **[HIPÓTESIS]** | Se puede testear y todavía no lo hicimos. |
| **[OPINIÓN]** | Mi juicio. Discutible por definición. |

---

## 0. La aritmética que gobierna los 12 meses

**[HECHO]** Hoy: 22 alumnos activos, ~3 altas/mes, retención junio→julio 80% (churn 20%).

**[INFERENCIA]** Una base de suscripción tiende siempre a `altas ÷ churn`:

```
hoy:      3 altas ÷ 20% churn  =  15 alumnos   ← hacia donde vamos
meta:    44 alumnos
```

Para llegar a 44 hay exactamente tres caminos, y conviene ver los tres números juntos:

| Camino | Altas/mes necesarias | Churn necesario | ¿Qué implica? |
|---|---|---|---|
| **Sólo adquisición** | **8,8** | 20% (igual) | triplicar las altas · CAC US$170 × 8,8 = **US$1.500/mes de pauta** — el triple del techo actual |
| **Sólo retención** | 3 (igual) | **6,8%** | churn casi nulo. Ninguna academia lo logra |
| **Mixto** | **5,3** | **12%** | +75% de altas y la mitad del churn |

**[OPINIÓN]** El camino mixto es el único realista, y tiene una ventaja que no se ve en la
tabla: **la mitad del trabajo ya está pago**. Bajar el churn se hace con los 22 alumnos que
ya tenés — no cuesta CAC, no cuesta pauta, y el material para empezar son 9 nombres con
teléfono.

**[INFERENCIA]** Por eso el orden de este roadmap es: **retención primero, conversión
segundo, volumen tercero.** No porque adquirir sea menos importante, sino porque con
LTV/CAC entre 0,64x y 1,88x **[HECHO, medido]**, cada alta comprada hoy puede estar
destruyendo valor — y no lo vamos a saber hasta el 31/08.

---

## 1. Tres críticas antes de empezar

Me pediste ser crítico. Estas tres cosas creo que están mal, incluida una mía:

### 1.1 Me equivoqué al priorizar "llenar las horas muertas del estudio"

En el análisis anterior puse "+$680.000/mes por llenar 20 horas muertas con una oferta de
entrada". **[OPINIÓN] Estaba mal priorizado y lo retiro de los primeros sprints.**

**[HECHO]** La ocupación es 26%. **[INFERENCIA]** Pero la capacidad ociosa no genera plata:
**la demanda genera plata**. Nadie compra un curso porque el estudio esté vacío. Crear una
oferta de entrada nueva sin haber arreglado la conversión es mover el mismo problema de
conversión a un producto más barato — y encima canibaliza.

**[HECHO]** Hay 9 alumnos que ya pagan y no vienen, con **20.000 créditos vivos** entre
todos. **[INFERENCIA]** La forma barata de llenar horas muertas es que vengan ellos:
ingreso ya cobrado, cero CAC, y ataca el churn al mismo tiempo.

### 1.2 El objetivo "duplicar alumnos" puede llevarte a la decisión equivocada

**[OPINIÓN]** Si el KPI es "cantidad de alumnos activos", la forma más rápida de moverlo es
bajar el precio o comprar más pauta — y las dos empeoran el negocio si LTV/CAC < 1.

**[OPINIÓN]** El objetivo que yo firmaría es **"44 alumnos activos con LTV/CAC > 3"**. Es el
mismo número con una restricción que impide ganarlo haciendo trampa. Si preferís el objetivo
sin restricción, decímelo y lo cambio — pero quiero que quede escrito que lo discutí.

### 1.3 No construyas un CRM

**[HECHO]** Hoy entran ~232 conversaciones/mes ≈ 8 por día hábil. **[OPINIÓN]** A ese
volumen, un CRM es una excusa para no hacer el trabajo comercial. WhatsApp Business con 4
etiquetas y una planilla aguanta hasta ~50 conversaciones por día. **El día que las etiquetas
se queden cortas, ese día se justifica un CRM — y para entonces vas a saber exactamente qué
campos necesita**, que hoy no sabemos.

---

## 2. Sprints

Seis sprints de 2 semanas. **Un objetivo por sprint, máximo 5 tareas.** Si una tarea no
entra, no entra: se corre al siguiente.

---

### SPRINT 1 · 04–17 de agosto
## 🎯 Objetivo único: **que los 9 alumnos que pagan y no vienen, vuelvan**

**[HECHO]** 9 de 22 alumnos activos (41%) no toman clase hace más de 30 días. Representan
**$1.395.840/mes** de facturación recurrente — el 46% del total.

**Hipótesis:** un alumno que pagó y no viene no está enojado, está sin fecha en el
calendario. Si alguien le ofrece dos horarios concretos y le agenda el turno, vuelve.

**Por qué creemos que funciona:** **[HECHO]** ninguna de las 29 bajas históricas fue pedida
por el alumno — todas son "dejó de pagar". **[INFERENCIA]** Eso describe abandono por
inercia, no rechazo del producto. La inercia se rompe con un empujón; el rechazo, no.

| # | Tarea | Responsable | Tiempo |
|---|---|---|---|
| 1 | Escribirles a los **9 de la Lista 1** ofreciendo dos horarios concretos y agendando vos el turno | José | 1 h |
| 2 | Escribirles a los **10 con créditos venciendo** antes del 22/08 | José | 45 min |
| 3 | Decidir qué hacer con **Toninelli y Pacino** (ver trade-off en las listas) | **Facu** | 15 min |
| 4 | Anotar cada contacto en la planilla: a quién · qué se dijo · qué contestó · qué pasó | José | incluido |
| 5 | Prender las **4 etiquetas de WhatsApp** (`Nuevo`/`Contestado`/`Cotizado`/`Cerrado`) y empezar a usarlas desde el día 1 | José | 30 min |

**Costo:** 3 horas de José. Cero pesos. Cero código.
**Riesgo:** bajo. El único real es que alguno conteste "quiero la devolución" — con Toninelli
(22 meses pagando sin venir) es posible. **[OPINIÓN]** Ese riesgo ya existe hoy y crece
$195.600 por mes; la conversación es más barata ahora.

**KPI:** clases agendadas por esos 9 alumnos dentro de los 14 días.
**Criterio de éxito:** **5 de 9 agendan.** (**[OPINIÓN]** 55% es exigente para una
reactivación en frío, pero estos no son leads fríos: son clientes que pagaron este mes.)
**Cuándo lo descartamos:** si agendan 2 o menos, la hipótesis "es inercia" es falsa y el
problema es el producto o el horario. Ahí el sprint 2 cambia por completo: pasa a ser
entrevistas, no reactivación.

---

### SPRINT 2 · 18–31 de agosto
## 🎯 Objetivo único: **saber por qué el 98,7% de los WhatsApp no compra**

**[HECHO]** 232 conversaciones/mes → 3 primeros pagos (1,3%). **[HECHO]** No existe ni un
registro de qué pasa con las otras 229.

**Hipótesis:** la mayor pérdida no es de precio ni de interés — es de **tiempo de respuesta y
de falta de seguimiento**. Nadie vuelve a escribir al que no contestó.

**Por qué creemos que funciona:** **[INFERENCIA]** de 232 conversaciones sólo ~12 llegan a
crear cuenta (medido: 12 cuentas nuevas en 3 semanas). La caída ocurre *antes* de la web, o
sea dentro de la conversación. **[HIPÓTESIS]** el cuello es operativo, no comercial.

| # | Tarea | Responsable | Tiempo |
|---|---|---|---|
| 1 | Dos semanas completas de etiquetado, sin excepción | José | 2 min/conv |
| 2 | Medir **tiempo de primera respuesta** de cada conversación | José | incluido |
| 3 | Escribirles a las **12 personas que crearon cuenta y no pagaron** (Lista 3) preguntando qué pasó | José | 45 min |
| 4 | Escribirles a los **5 que se fueron** (Lista 4) — **sin oferta**, sólo la pregunta | José | 30 min |
| 5 | `wa.me` con código por anuncio (`#DJ2`, `#REEL`, `#PRO`) | Facu | 20 min |

**Costo:** ~4 horas. Cero pesos.
**Riesgo:** medio — **[OPINIÓN]** el único riesgo real de todo el plan es que el etiquetado
no se sostenga. Si José no lo hace 14 días seguidos, no tenemos el dato y el sprint 3 no se
puede planificar.

**KPI:** % de conversaciones etiquetadas (meta: >90%) y tiempo mediano de primera respuesta.
**Criterio de éxito:** al día 14 podemos contestar: cuántos escriben, en cuánto se les
responde, cuántos cotizan y cuántos cierran.
**Cuándo lo descartamos:** no se descarta. Si al día 7 el etiquetado no llega al 50%, se
simplifica a **una sola** etiqueta (`Contestado`) — el dato mínimo es mejor que ninguno.

---

### SPRINT 3 · 1–14 de septiembre
## 🎯 Objetivo único: **atacar el cuello que el sprint 2 encontró**

**No lo puedo planificar hoy** y sería deshonesto fingir que sí. **[OPINIÓN]** Un roadmap que
detalla el sprint 3 antes de tener el dato del sprint 2 es un roadmap decorativo.

Los tres escenarios probables y qué haríamos en cada uno:

| Si el dato dice… | El sprint 3 es… |
|---|---|
| Se responde tarde (> 1 h) | Guardias de respuesta + respuestas rápidas guardadas. **Sin código.** |
| Se responde rápido pero no se cierra | El problema es el guion o el precio. Se prueban 2 guiones distintos, 50 conversaciones cada uno |
| Se cierra bien pero llegan pocos | Recién ahí el cuello es la pauta, y se escala presupuesto |

**Además, en este sprint llega solo el dato que más vale:** **[HECHO]** el 31/08 se sabe
cuántos de los 19 que pagaron en julio renovaron en agosto. Eso define el churn real y
resuelve el rango LTV/CAC 0,64x–1,88x.

---

### SPRINT 4 · 15–28 de septiembre
## 🎯 Objetivo único: **automatizar lo que ya funcionó a mano**

**Sólo entra acá lo que en los sprints 1 y 2 demostró funcionar manualmente.** Candidatos, en
orden de plata:

1. **Aviso de créditos por vencer** (cron + mail, 1 día) — si el sprint 1 mostró que agendar
   funciona.
2. **Aviso de "no viniste en 30 días"** (1 día) — mismo criterio.
3. **Mail de bienvenida con un botón: agendá tu primera clase** (1 día). **[HECHO]** hoy
   Ivon y Roberto pagaron y nunca agendaron: el problema existe.
4. **Guardar `utm_source` y `referrer`** al crear la cuenta (2 h).
5. **Recuperación de checkout abandonado** (1 día) — si el sprint 2 mostró que responden.

**Criterio de entrada, sin excepción:** si una acción manual no movió su KPI, **no se
automatiza**. Automatizar algo que no funciona sólo hace que falle más rápido y en silencio.

---

### SPRINT 5 · 29 de septiembre – 12 de octubre
## 🎯 Objetivo único: **subir el ticket con los alumnos que ya tenés**

**[HECHO]** Silver consume 130% de sus créditos y tiene 69% de churn (9 bajas de 13). Gold
consume 65% y casi no cae.

**Hipótesis:** el Silver se queda corto todos los meses, se frustra y se va — en vez de subir
a Gold (+$52.080/mes).

**[OPINIÓN]** Esta es la palanca de ticket con mejor evidencia. Las demás (subir precios,
productos nuevos) son apuestas; ésta tiene un patrón medido detrás.

**KPI:** upgrades/mes · churn de Silver.
**Criterio de éxito:** 2 de los 4 Silver activos suben a Gold = **+$104.160/mes**.

---

### SPRINT 6 · 13–26 de octubre
## 🎯 Objetivo único: **volumen — pero sólo si los números lo habilitan**

**Condición de entrada, dura:** LTV/CAC > 2 confirmado con el churn real de agosto y
septiembre. **[OPINIÓN] Si no se cumple, este sprint no se hace** y se repite el ciclo de
retención. Escalar pauta con LTV/CAC < 2 es financiar la pérdida con más velocidad.

Si se habilita: escalar al techo de US$500/mes con el creativo que el código de WhatsApp
haya validado, y recién ahí evaluar la oferta de entrada para las horas muertas.

---

## 3. Las 5 métricas de todos los días

Cinco, en un renglón cada una. **[OPINIÓN]** Si mirás más de cinco, no mirás ninguna.

| # | Métrica | De dónde sale | Hoy |
|---|---|---|---|
| 1 | **Conversaciones nuevas de WhatsApp** | etiqueta `Nuevo` | ~8/día hábil **[INFERENCIA]** |
| 2 | **Tiempo de primera respuesta** | WhatsApp | **falta el dato** |
| 3 | **Clases agendadas para los próximos 7 días** | `slot_bookings` | 4 alumnos **[HECHO]** |
| 4 | **Alumnos activos que no vienen hace 30 días** | base | **9 de 22** **[HECHO]** |
| 5 | **Altas del mes** (primeros pagos) | `sales` | 3/mes **[HECHO]** |

**[OPINIÓN]** La 3 y la 4 son las que predicen la facturación del mes que viene. La 5 la
confirma cuando ya es tarde para hacer algo.

**Las tres primeras no están en ningún dashboard y no las voy a construir todavía**: la 1 y
la 2 viven en el teléfono de José, y hasta que no haya dos semanas de datos no sé qué corte
sirve. Construir la pantalla antes es adivinar.

---

## 4. Las 5 decisiones que vas a tener que tomar

Son tuyas. Escribo el trade-off, no la respuesta.

**1. Toninelli y Pacino** (esta semana). Activarlos = recuperás $391.200/mes de clientes
reales, pero liberás 246 clases acumuladas contra la capacidad. No tocarlos = seguís cobrando
hasta que se den cuenta. *Riesgo reputacional creciente contra ingreso presente.*

**2. Objetivo con o sin restricción de LTV/CAC** (esta semana). "44 alumnos" es fácil de
mover con precio y pauta; "44 alumnos con LTV/CAC > 3" te obliga a que el negocio cierre.
*Velocidad contra sanidad.*

**3. Si el churn de agosto sale mal** (31/08). Con LTV/CAC < 1 hay dos salidas: **subir
precios** (mejora el LTV, baja la conversión) o **cortar pauta** hasta arreglar la retención
(salva plata, frena el crecimiento). *No hay tercera.*

**4. Modo Profesional** (septiembre). **[HECHO]** $440.000 de ticket, **cero ventas**.
Matarlo libera foco; sostenerlo requiere hablar con 10 personas antes de gastar un peso más.
*Foco contra opcionalidad.*

**5. Dedicación de José** (permanente). **[OPINIÓN]** Todo este plan depende de una persona
que hoy además hace administración y cobranzas. Si el seguimiento comercial no es su
prioridad #1 declarada, el plan no ocurre. *O se le libera tiempo de otra cosa, o se suma
alguien, o el plan se achica a lo que una persona pueda sostener.*

---

## 5. Riesgos que pueden hacer fracasar todo

| # | Riesgo | Probabilidad | Señal temprana | Qué hacemos |
|---|---|---|---|---|
| 1 | **El etiquetado de WhatsApp no se sostiene** | **alta** — es trabajo repetitivo sin recompensa inmediata | < 50% etiquetado al día 7 | bajar a UNA etiqueta |
| 2 | **La retención real es mucho peor que 80%** | media | renuevan < 12 de 19 en agosto | cortar pauta, todo a retención |
| 3 | **Dependencia de una persona** — José ejecuta todo el plan; Pastrana da el 64% de las clases **[HECHO]** | media | una semana sin contactos anotados | repartir o achicar |
| 4 | **Los datos de julio están inflados por la migración** | **[HECHO], ya pasó** | — | ninguna decisión se toma con junio/julio solos |
| 5 | **Volvemos a construir software en vez de vender** | **alta** — es lo que sabemos hacer y es más cómodo | un sprint que termina con código y sin conversaciones | los sprints 1, 2 y 3 tienen prohibido el código |

**[OPINIÓN]** El riesgo 5 es el más peligroso de todos, y por eso lo escribo último para que
quede último en la memoria: **este equipo tiene una habilidad enorme para construir sistemas
y ninguna práctica de seguimiento comercial**. La tentación de resolver un problema de
ventas con una pantalla nueva va a aparecer en cada sprint.

---

## 6. Cómo se cierra un ciclo

Al final de cada sprint, cuatro preguntas y nada más:

1. **¿Qué funcionó?** — con el número, no con la sensación.
2. **¿Qué no?** — y si la hipótesis quedó refutada, se tacha acá arriba con fecha.
3. **¿Qué aprendimos que no sabíamos?**
4. **¿Qué cambia del roadmap?** — si no cambia nada, es sospechoso: significa que no
   aprendimos nada.

**Regla de honestidad:** una hipótesis refutada es un buen resultado del sprint. Un sprint
donde "todo salió como esperábamos" normalmente significa que no medimos.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08/2026 | v1 | — |
| 04/08/2026 | **Retirado** "llenar horas muertas con oferta de entrada" de los primeros sprints | La capacidad ociosa no genera demanda. Primero la llenan los que ya pagan |
