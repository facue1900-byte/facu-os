# OS de Crecimiento — Astronomy Academy

`v2 · 04/08/2026` · **Documento vivo.** Se actualiza al cierre de cada sprint. Lo que se
retira queda escrito abajo con la fecha y el motivo — para poder ver en qué nos equivocamos.

**Objetivo (12 meses):** 44 alumnos activos, **LTV/CAC > 3**, sin deteriorar la experiencia
y con procesos que escalen.

**Restricción vigente: está prohibido escribir código.** Se levanta sólo si (a) el proceso
manual funcionó 2 semanas, (b) el cuello pasó a ser operativo y (c) automatizar rinde más
que seguir a mano.

| Etiqueta | Qué significa |
|---|---|
| **[HECHO]** | Medido contra la base, la planilla o la API. Reproducible. |
| **[INFERENCIA]** | Calculado desde hechos. La aritmética es sólida; los supuestos van escritos. |
| **[HIPÓTESIS]** | Testeable, todavía no probada. |
| **[OPINIÓN]** | Mi juicio. Discutible. |

---

## 1. El criterio que pediste, aplicado — y por qué solo no alcanza

Ordenado por **retorno esperado por hora invertida**. Cada tasa de éxito es un supuesto y
está escrita al lado: si el Sprint 1 la desmiente, la fila se recalcula.

| Iniciativa | $/mes esperado | Horas | **$/hora** | Supuesto |
|---|---|---|---|---|
| Decidir Toninelli + Pacino | $195.600 | 0,25 | **$782.400** | sigue 1 de los 2 |
| Escribir a los 9 que pagan y no vienen | $488.544 | 1,0 | **$488.544** | vuelve el 35% |
| Escribir a los 10 con créditos venciendo | $344.448 | 0,75 | **$459.264** | agenda el 40% |
| Escribir a los 5 que se fueron | $86.112 | 0,5 | $172.224 | vuelve 1 de 5 |
| Ofrecer Gold a los 4 Silver | $52.080 | 0,33 | $157.818 | suben 2 de 4 |
| Escribir a los 12 que no pagaron | $48.797 | 0,75 | $65.062 | cierran 2 de 12 |
| `wa.me` con código por anuncio | $0 | 0,33 | **$0** | habilita atribuir |
| **Etiquetar WhatsApp 2 semanas** | **$0** | **10,0** | **$0** | **no genera plata: genera el dato** |

**[INFERENCIA] Todo el bloque manual: 14 horas de trabajo humano → $1.215.581/mes esperado.
Es +41% sobre la facturación actual, sin gastar un peso ni escribir una línea.**

### 🔴 La crítica: el criterio que me diste pone en último lugar lo más importante

**[HECHO]** Etiquetar el WhatsApp puntúa **$0/hora**: no genera un peso por sí solo.
**[HECHO]** Y es la única acción del plan que puede llevar el negocio de 3 a 9 altas por mes
—de 15 a 45 alumnos de base estable— porque es la que revela por qué se pierde el 98,7% de
las conversaciones.

**[OPINIÓN]** Ordenar todo por ROI/hora te lleva sistemáticamente a **cosechar y nunca
sembrar**. Es el criterio correcto para elegir qué hacer *dentro* de una semana, y el
criterio equivocado para elegir en qué apostar los 90 días.

**La corrección que propongo** —y si no te convence, discutámosla, porque cambia todo el
plan—: separar las acciones en dos categorías que se priorizan distinto.

| | **Cosecha** | **Siembra** |
|---|---|---|
| Qué es | Convierte plata que ya está en la mesa | Compra información que habilita una decisión grande |
| Cómo se prioriza | **ROI por hora** | **Valor de la decisión que desbloquea** |
| Ejemplos | los 9 inactivos, los créditos venciendo, el upgrade de Silver | etiquetar WhatsApp, preguntar por qué se fueron |
| Límite | **se agota**: hay 22 alumnos, no 200 | es lo único que hace crecer la empresa |

**[INFERENCIA]** Toda la cosecha disponible hoy son ~$1,2M/mes y **se agota en dos semanas**
— son 36 personas en total y no hay más. La siembra es lo que decide si dentro de 12 meses
hay 15 alumnos o 45. **Por eso el Sprint 1 hace las dos cosas al mismo tiempo**: la cosecha
paga el sprint, la siembra paga el año.

---

## 2. Qué dejamos de hacer HOY

Esto es lo que mato, y empiezo por cosas que propuse yo:

| Lo que se mata | Por qué | Quién lo propuso |
|---|---|---|
| **El ensayo de pago real de Modo Profesional** (bajar el precio a $616, pagar, restaurar) | **[HECHO]** cero ventas en la historia del producto. Gastar 30 min y tocar un precio público para validar el cobro de algo que nadie compró es la definición de optimizar lo irrelevante | **yo, hace dos días** |
| **Pedir indexación en Search Console / SEO** | **[OPINIÓN]** no mueve un peso en 90 días. Es real, es gratis, y no es ahora | yo |
| **Cualquier dashboard nuevo** | el dato que falta (WhatsApp) no está en ninguna base: está en el teléfono de José | — |
| **Mirar `/admin/growth` y `/admin/conciliacion` a diario** | **[OPINIÓN]** ya cumplieron su función. Si no cambian una decisión esta semana, no se abren | yo |
| **El resto de las verificaciones manuales del módulo de pagos** | congelado | yo |
| **Modo Profesional como producto activo** | **[HECHO]** $440.000 de ticket, 0 ventas. **[OPINIÓN]** no se mata todavía, se congela: se decide en el Sprint 4 con 10 conversaciones, no con desarrollo | — |

**Se salva una sola cosa del bloque técnico:** confirmar los dos precios que se editaron con
el token de prueba (Bronze $71.760 y el link viejo del Curso de DJ $143.520). **[OPINIÓN]**
5 minutos, y un precio mal en producción es plata real todos los días.

---

## 3. Los 6 sprints

### SPRINT 1 · 4–17 ago
## 🎯 **Que la plata que ya cobramos se convierta en clases dadas**

**Problema económico:** **[HECHO]** 9 de 22 alumnos activos (41%) no toman clase hace +30
días; son $1.395.840/mes, el 46% de la facturación. **[HECHO]** 10 alumnos tienen créditos
venciendo antes del 22/08.

**Evidencia:** **[HECHO]** ninguna de las 29 bajas históricas fue pedida por el alumno: todas
son "dejó de pagar". **[HECHO]** Federico Toninelli lleva 22 meses pagando Gold sin tomar una
clase.

**Hipótesis:** el alumno que pagó y no viene no está enojado — está sin fecha en el
calendario. Un empujón con dos horarios concretos lo trae de vuelta.

**Experimento manual más barato:** 19 mensajes de WhatsApp escritos por José. 3 horas.

**Qué lo descarta:** si agendan 2 de 9 o menos. Ahí la causa no es inercia: es el producto,
el horario o el profe, y el Sprint 2 se convierte en entrevistas en profundidad.

**Costo de oportunidad:** ninguno. Es la mayor concentración de plata por hora del plan y se
agota si no se hace esta semana (los créditos vencen el 13/08).

| # | Tarea | Responsable | Tiempo |
|---|---|---|---|
| 1 | Escribir a los **9 inactivos** con dos horarios concretos y agendar vos el turno | José | 1 h |
| 2 | Escribir a los **10 con créditos venciendo** antes del 22/08 | José | 45 min |
| 3 | Decidir **Toninelli y Pacino** (trade-off escrito en las listas) | **Facu** | 15 min |
| 4 | Prender las **4 etiquetas de WhatsApp** y usarlas desde el día 1 | José | 30 min |
| 5 | Anotar cada contacto: a quién · qué se dijo · qué contestó · qué pasó | José | incluido |

**KPI:** clases agendadas por esos 19 alumnos dentro de 14 días.
**Éxito:** ≥ 9 agendan. **Fracaso:** ≤ 4 agendan.
**Aprendizaje esperado:** si el abandono es inercia (se arregla con un empujón) o rechazo
(hay que cambiar el producto). **Es la pregunta más importante del negocio después del
WhatsApp.**
**Decisión que habilita:** si es inercia → el Sprint 4 automatiza el empujón. Si es rechazo →
se frena toda la adquisición hasta arreglar el producto, porque traer gente a un producto que
la gente abandona es tirar el CAC.

---

### SPRINT 2 · 18–31 ago
## 🎯 **Saber por qué el 98,7% de los WhatsApp no compra**

**Problema económico:** **[HECHO]** 232 conversaciones/mes → 3 primeros pagos. **[INFERENCIA]**
llevar eso al 5% son 11,6 altas/mes y una base estable de 58 alumnos.

**Evidencia:** **[HECHO]** 12 cuentas nuevas en 3 semanas contra ~170 conversaciones en el
mismo período. La caída ocurre *antes* de la web, dentro de la conversación. **[HECHO]** cero
registro de qué pasa ahí.

**Hipótesis:** el cuello es operativo (tiempo de respuesta y falta de seguimiento), no
comercial (precio o interés).

**Experimento manual más barato:** 14 días de etiquetado + 17 mensajes a los que se fueron y
a los que no pagaron. ~4 horas repartidas.

**Qué lo descarta:** si el tiempo de respuesta resulta < 15 min y el 80% recibe seguimiento,
la hipótesis operativa cae y el cuello es la oferta o el precio.

**Costo de oportunidad:** dos semanas sin generar plata directa. **[OPINIÓN]** Es el precio de
dejar de adivinar, y es barato: 4 horas.

| # | Tarea | Responsable | Tiempo |
|---|---|---|---|
| 1 | Etiquetado completo, 14 días sin excepción | José | 2 min/conv |
| 2 | Registrar **tiempo de primera respuesta** de cada conversación | José | incluido |
| 3 | Escribir a los **12 que crearon cuenta y no pagaron** | José | 45 min |
| 4 | Escribir a los **5 que se fueron** — sin oferta, sólo la pregunta | José | 30 min |
| 5 | `wa.me` con código por anuncio (`#DJ2`, `#REEL`, `#PRO`) | Facu | 20 min |

**KPI:** % de conversaciones etiquetadas (>90%) y tiempo mediano de primera respuesta.
**Éxito:** al día 14 sabemos cuántos escriben, en cuánto se responde, cuántos cotizan y
cuántos cierran. **Fracaso:** < 50% etiquetado → se simplifica a UNA etiqueta.
**Decisión que habilita:** dónde atacar el embudo, y si el techo de US$500 de pauta se sube o
se baja.

---

### SPRINT 3 · 1–14 sep
## 🎯 **Arreglar el cuello que el Sprint 2 encontró**

**[OPINIÓN] No lo puedo planificar hoy sin mentir.** Un roadmap que detalla el Sprint 3 antes
de tener el dato del 2 es decoración.

| Si el dato dice… | El sprint es… |
|---|---|
| Se responde tarde (> 1 h) | guardias de respuesta + mensajes guardados. Sin código |
| Se responde rápido y no cierra | dos guiones distintos, 50 conversaciones cada uno |
| Cierra bien pero llegan pocos | recién ahí el cuello es pauta y se escala presupuesto |

**Además llega solo el dato más valioso del trimestre:** **[HECHO]** el 31/08 se sabe cuántos
de los 19 que pagaron en julio renovaron. Eso cierra el rango LTV/CAC 0,64x–1,88x.
**Decisión que habilita:** si se escala adquisición o se corta pauta.

---

### SPRINT 4 · 15–28 sep
## 🎯 **Automatizar únicamente lo que ya funcionó a mano**

**Primer sprint donde se permite código, y sólo si se cumplen las tres condiciones.**
Candidatos en orden de plata: aviso de créditos por vencer · aviso de "no viniste en 30
días" · mail de bienvenida con un botón para agendar · guardar `utm_source` · recuperación de
checkout.

**Criterio de entrada, sin excepción:** si la versión manual no movió su KPI, **no se
automatiza**. **[OPINIÓN]** Automatizar algo que no funciona sólo hace que falle más rápido y
en silencio.

**Acá también se decide Modo Profesional**, con 10 conversaciones hechas, no con desarrollo.

---

### SPRINT 5 · 29 sep–12 oct
## 🎯 **Subir el ticket de los alumnos que ya están**

**[HECHO]** Silver consume 130% de sus créditos y tiene 69% de churn (9 bajas de 13); Gold
consume 65% y casi no cae. **Hipótesis:** el Silver se queda corto, se frustra y se va en vez
de subir a Gold (+$52.080/mes).
**KPI:** upgrades/mes y churn de Silver. **Éxito:** 2 de 4 suben.

---

### SPRINT 6 · 13–26 oct
## 🎯 **Volumen — sólo si los números lo habilitan**

**Condición dura de entrada: LTV/CAC > 3 confirmado** con el churn real de agosto y
septiembre. **[OPINIÓN]** Si no se cumple, este sprint no existe y se repite retención.
Escalar con LTV/CAC < 3 es comprar crecimiento con pérdida.

---

## 4. Las 5 métricas diarias

| # | Métrica | Hoy |
|---|---|---|
| 1 | Conversaciones nuevas de WhatsApp | ~8/día hábil **[INFERENCIA]** |
| 2 | Tiempo de primera respuesta | **falta el dato** |
| 3 | Clases agendadas para los próximos 7 días | 4 alumnos **[HECHO]** |
| 4 | Alumnos activos sin venir hace 30 días | **9 de 22** **[HECHO]** |
| 5 | Altas del mes (primeros pagos) | 3/mes **[HECHO]** |

**[OPINIÓN]** La 3 y la 4 predicen la facturación del mes que viene; la 5 la confirma cuando
ya es tarde. Ninguna se construye como pantalla hasta tener 2 semanas de datos a mano.

---

## 5. El mayor riesgo de que el plan fracase

**No es el churn, ni la pauta, ni el producto. Es que el plan no se ejecute.**

**[HECHO]** Las 14 horas del bloque manual dependen de una sola persona (José), que hoy
además hace administración y cobranzas. **[HECHO]** El 64% de las clases las da un solo profe
(Mateo Pastrana).

**[OPINIÓN]** El plan tiene un único punto de falla y es humano, no técnico. Si José no
declara el seguimiento comercial como su prioridad #1 —y alguien le saca otra cosa de encima
para que entre—, este documento no se ejecuta y dentro de 90 días vamos a tener otro
diagnóstico igual de prolijo y cero alumnos nuevos.

**Señal temprana:** una semana sin contactos anotados en la planilla. **Qué hacemos:** se
achica el plan a lo que una persona pueda sostener de verdad, o se suma alguien.

---

## Registro de cambios

| Fecha | Qué cambió | Por qué |
|---|---|---|
| 04/08 | v1 | — |
| 04/08 | **Retirado** "llenar horas muertas con oferta de entrada" de los primeros sprints | la capacidad ociosa no genera demanda; primero la llenan los que ya pagan |
| 04/08 | **v2 — reordenado por ROI/hora**, y agregada la distinción cosecha/siembra | el criterio ROI/hora puro puntúa en $0 lo único que puede triplicar el negocio |
| 04/08 | **Matado** el ensayo de pago real de Modo Profesional | cero ventas: validar el cobro de algo que nadie compra es optimizar lo irrelevante |
| 04/08 | **Matado** SEO / Search Console por 90 días | no mueve un peso en el plazo del plan |
| 04/08 | Sprint 1 pasa a hacer cosecha **y** siembra a la vez | la cosecha se agota en 2 semanas; la siembra paga el año |
