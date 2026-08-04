# Astronomy Academy — Auditoría económica y roadmap por ROI

`04/08/2026` · Medido contra la base (`qeakrjnseboiulcojlcw`), la planilla `Finanzas -
Astronomy Academy` y las memorias de pauta. **Tipo de cambio: $1.472/USD**, el implícito de
la planilla en julio 2026. Cada estimación lleva su supuesto escrito; lo que no se puede
estimar con lo que hay dice **"falta el dato"** en vez de inventar un número.

---

## 0. El cuello de botella económico de toda la empresa

No es la conversión, ni el ticket, ni el producto. Es esto:

> **La base de alumnos se está encogiendo, y el negocio está clavado en su punto de
> equilibrio desde hace 26 meses.**

Tres hechos medidos que juntos lo explican todo:

**1. En 26 meses la academia ganó US$1.945 en total.** Ingresos US$53.442, egresos
US$51.497. No es un mal mes: es el patrón completo. Mes a mes oscila entre −US$980 y
+US$1.090 y nunca se despega.

**2. La base de 22 alumnos no es estable: viene cayendo.** En julio se migraron 39 cuentas
de alumnos existentes. Hoy quedan **22 suscripciones activas**. Entran ~3 alumnos nuevos por
mes. Y la matemática de una suscripción es implacable:

```
base estable = altas por mes ÷ churn mensual
3 altas ÷ 20% de churn = 15 alumnos
```

**Al ritmo actual el negocio converge a ~15 alumnos**, que es exactamente su punto de
equilibrio (14,5). No está creciendo despacio: está volviendo a cero, y desde arriba.

**3. Cada alumno nuevo cuesta más de lo que deja.**

| | |
|---|---|
| Contribución por alumno | **$94.047/mes (66% del ticket)** — descontado profe, comisión y Mercado Pago |
| Costos fijos | ~US$928/mes ($1.366.016) — pauta, diseño, suscripciones, Luki, mantenimiento |
| Punto de equilibrio | **14,5 alumnos** |
| CAC actual | **US$170** (US$510 de pauta en julio ÷ 3 primeros pagos) |
| LTV | **US$109 a US$319**, según qué medida de vida se use |
| **LTV / CAC** | **0,64x a 1,88x** |

El rango es enorme porque hay dos medidas de vida útil que no coinciden: los alumnos que se
dieron de baja duraron 44–62 días (LTV US$109 → **destruye valor**), pero la retención
junio→julio fue del 80%, que implica 5 meses de vida (LTV US$319 → flojo pero viable).

**Con los datos que existen hoy no se puede saber cuál de las dos es la verdadera.** Y esa
es la métrica que decide si conviene poner un dólar más de pauta. Se resuelve solo el
**31/08**, cuando se vea cuántos de los 19 que pagaron en julio renovaron.

### Por qué te discuto el orden de prioridades

Vos pusiste: 1) más alumnos · 2) convertir · 3) ticket · 4) retención. Los datos dicen que
**1 va después de 2 y 4**, y no es una sutileza:

- Traer más gente al CAC de hoy (US$170) contra un LTV que puede ser US$109 **acelera la
  pérdida**. Es comprar pesos a peso y medio.
- Subir la conversión de WhatsApp del 1,3% al 5% **divide el CAC por cuatro (US$170 →
  US$44) sin gastar un peso más**, y recién ahí traer gente genera plata.
- Y sin retención, el volumen no acumula: con churn del 59% mensual (el peor escenario),
  aún metiendo 11 alumnos por mes la base se estanca en 20. Es llenar un balde agujereado.

**El orden que sostienen los números: conversión y retención primero, volumen después.**
Mismo destino, distinto orden — y el orden acá es la diferencia entre crecer y financiar la
pérdida con pauta.

### Lo que puede triplicar el negocio

Una sola cosa, y está medida:

```
232 conversaciones de WhatsApp por mes (Meta, julio)
        ↓  1,3%
   3 alumnos nuevos
```

Si esa conversión llega al 5% —1 de cada 20 personas que te escriben por voluntad propia—
son **11,6 altas por mes**. Con churn del 20%, la base estable pasa de 15 a **58 alumnos**:

| | Hoy | Con 5% de conversión |
|---|---|---|
| Altas/mes | 3 | 11,6 |
| Base estable | 15 | **58** |
| Facturación/mes | ~$3.000.000 | **~$8.300.000** |
| Resultado/mes | ~US$0 | **~US$2.600** |
| CAC | US$170 | US$44 |

**Esto no requiere gastar un dólar más de pauta, ni una línea de código.** Requiere que
alguien conteste bien 232 conversaciones por mes. Es la única palanca del negocio que puede
triplicar la facturación, y es donde iría toda la energía.

---

## 1. Los 26 frentes, con lo que encontré en cada uno

Ordenados por plata esperada. **"Falta el dato"** significa que no hay forma de estimarlo
con lo que existe hoy, y digo cómo conseguirlo barato.

### 🔴 Frentes con plata grande y evidencia dura

#### 1. WhatsApp — **el agujero principal: hasta $5.300.000/mes**
- **Evidencia:** 232 conversaciones en julio (Meta), 3 primeros pagos en `sales`. 1,3%.
- **Por qué:** una persona que escribe por voluntad propia es el lead más caliente que hay.
  Un 5% de cierre es un piso bajo para ese tipo de contacto, no un techo optimista.
- **Falta el dato — y es el más importante de la empresa:** cuánto tarda José en contestar,
  cuántas quedan sin respuesta, y qué contesta. **Cero registro.**
- **Experimento mínimo:** 4 etiquetas en WhatsApp Business (`Nuevo`/`Contestado`/`Cotizado`/
  `Cerrado`) + una fila por conversación en una planilla, 14 días. 30 min de setup.
- **Impacto** hasta +$5,3M/mes · **Esfuerzo** 30 min + 2 min/conversación · **Riesgo** nulo,
  salvo que no se sostenga · **Dependencia** José · **Medir:** conversaciones → cuentas →
  pagos por semana, y tiempo de primera respuesta.

#### 2. Retención / churn — **decide si el negocio escala o se apaga**
- **Evidencia:** 39 cuentas migradas en julio → 22 activas. Vida media de los que se fueron:
  44 días (Curso DJ), 62 (Silver). **Las 29 bajas son administrativas: ni una la pidió el
  alumno.** Nadie preguntó nunca por qué se fue.
- **Por qué:** con LTV/CAC entre 0,64 y 1,88, cada punto de retención cambia si la pauta es
  inversión o gasto.
- **Falta el dato:** el motivo de baja. Y el churn real de agosto (se sabe el 31/08).
- **Experimento mínimo:** escribirle a los 16 ex-alumnos (facturaron $1.041.680) con **una**
  pregunta abierta. 1 hora.
- **Impacto:** bajar el churn del 20% al 12% lleva la base estable de 15 a 25 alumnos =
  **+$1.435.200/mes** · **Esfuerzo** 1 h · **Riesgo** nulo · **Medir:** % que renueva mes a mes.

#### 3. Uso de créditos — **$861.120/mes de recurrencia en riesgo, ahora**
- **Evidencia:** **59% de los créditos vendidos nunca se usaron** (22.840 de 38.570). Ya
  vencieron 4.080. Y hay **6 alumnos con 240 créditos venciendo entre el 13 y el 22 de
  agosto, sin una sola clase agendada** — cada uno pagó $143.520 por esos créditos.
- **Por qué:** un alumno que deja vencer 4 clases pagadas no renueva. Es la señal de churn
  más temprana y más accionable que tiene el negocio.
- **Falta el dato:** confirmar la relación entre "dejó vencer" y "no renovó". La muestra
  está: son esos 6.
- **Experimento mínimo:** escribirles a mano esta semana. 30 min. Si agendan, se automatiza.
- **Impacto** +$861.120/mes de recurrencia protegida · **Esfuerzo** 30 min · **Riesgo** nulo.

#### 4. Horarios muertos del estudio — **+$680.000/mes con costo marginal casi cero**
- **Evidencia:** ocupación del **26%** (88 h usadas de 344 disponibles en julio). El estudio
  de producción está al **7%**: 12 horas en todo el mes.
- **Por qué:** el alquiler ya está pagado. Una clase deja 69% de margen bruto ($35.880 de
  ingreso, $11.000 de profe); un alquiler de cabina, 77%.
- **Falta el dato:** si una oferta de entrada canibaliza la membresía. **Es la decisión que
  no puedo tomar por vos.**
- **Experimento mínimo:** clase suelta de prueba en franjas muertas, cupo limitado, 1 mes.
- **Impacto:** llenar 20 h/mes = **+$680.000** bruto · **Riesgo** medio (canibalización).

#### 5. Meta Ads — **no tocar el presupuesto todavía**
- **Evidencia:** US$590/mes, un solo conjunto, radio de 35 km sobre Nordelta, sin intereses.
  **Tres anuncios de Curso de DJ comparten exactamente el mismo copy** y compiten entre sí.
  El 100% del presupuesto va al producto más barato del catálogo. El mejor creativo de la
  historia de la cuenta (`Curso DJ 2`) hizo 228 conversaciones a US$0,67 y **nadie miró
  nunca por qué funcionaba**.
- **Por qué NO subirlo:** con LTV/CAC posiblemente < 1, cada dólar extra puede destruir
  valor. Primero el frente 1.
- **Experimento mínimo (gratis):** un `wa.me` distinto por anuncio con código en el mensaje
  prellenado (`#DJ2`, `#REEL`, `#PRO`). 20 minutos, permite atribuir sin ningún sistema.
- **Impacto:** no genera solo; **habilita decidir** dónde van los US$590.

### 🟡 Frentes con plata mediana

#### 6. Pricing y upselling — Silver está roto
- **Evidencia:** Silver consume **130% de sus créditos** (se queda corto todos los meses) y
  tiene **69% de churn** (9 bajas de 13). Gold consume 65% y casi no cae.
- **Lectura:** el Silver se frustra y se va en lugar de subir a Gold.
- **Experimento mínimo:** a los 4 Silver activos, ofrecerles Gold a mano cuando se quedan
  sin créditos (+$52.080/mes cada uno).
- **Impacto** +$104.160/mes si suben 2 · **Esfuerzo** 20 min.

#### 7. Registro y checkout — 9 personas en la caja
- **Evidencia:** **24 cuentas sin ningún pago** (9 en las últimas 3 semanas), 6 suscripciones
  en `pending`. La cuenta se crea *dentro* del flujo de compra: llegaron a la caja y se fueron.
- **Experimento mínimo:** escribirles a los 9. 30 min.
- **Impacto** +$287.040 si cierran 2, más su recurrencia.

#### 8. Referidos — la palanca más barata que está sin usar
- **Evidencia:** la plomería existe (`shared_accesses`, invitaciones grupales) con **2 y 3
  registros en toda la historia**. Con contribución de $94.047/mes por alumno, pagar 1–2
  clases en créditos por un referido que paga se recupera el primer mes — y esos créditos
  se consumen en horas que hoy están vacías.
- **Experimento mínimo:** pedírselo a mano a los 15 alumnos de Curso de DJ. Si nadie refiere
  pedido a mano, un botón tampoco lo va a lograr.
- **Impacto** +$430.560/mes si 3 traen 1 · **Esfuerzo** 1 h.

#### 9. Email — el canal existe y está apagado
- **Evidencia:** el sistema manda **un solo** mail automático de negocio: el recordatorio 34hs
  antes de una clase **ya agendada**. No hay bienvenida, ni aviso de vencimiento, ni
  recuperación de checkout, ni reactivación. La plomería (Resend + plantilla de marca + cron
  diario) **ya está construida**.
- **Impacto:** es el vehículo de los frentes 3, 7 y 10 · **Esfuerzo** 1 día cada uno.

#### 10. Primeras clases / activación
- **Evidencia:** 18 de 25 pagadores agendaron en la web. No hay mail de bienvenida que diga
  "tu próximo paso es agendar".
- **Falta el dato:** cuánto tarda hoy un alumno nuevo en agendar la primera clase.
- **Experimento mínimo:** medirlo con una query antes de construir nada.

#### 11. Agenda de profesores
- **Evidencia:** Mateo Pastrana da 106 clases, Mateo Guini 43, Owners of Time 16. Pastrana
  concentra el 64%. Costo por clase: $11.000 (Pastrana/Guini), $15.000 (Owners).
- **Riesgo de negocio:** dependencia de una persona. Si Pastrana se va, se cae el 64% de la
  entrega.
- **Falta el dato:** disponibilidad real declarada vs vendida.

### 🟢 Frentes sin datos suficientes — cómo conseguirlos barato

| Frente | Qué sé | Cómo medirlo barato |
|---|---|---|
| **Instagram** | Sin acceso a métricas desde acá | Exportar el resumen de 30 días desde la app: alcance, visitas al perfil, clicks al link. 10 min |
| **Contenido** | Nada medido | Igual que arriba: qué posteo trajo visitas al perfil |
| **SEO** | El sitio tiene sitemap y metadata; falta pedir indexación en Search Console | Search Console → Rendimiento. 5 min. **Bloqueado** hasta que Google indexe |
| **Landing pages** | `/academy` prerenderiza y el pixel está desde el 31/07 | Sin analytics de visitas no se puede calcular conversión de landing. Falta el dato |
| **Comunidad** | No existe como producto | — |
| **Cross-selling con eventos** | La ticketera está construida y **vacía**: 1 evento, 0 órdenes, 0 tickets | Cruzar alumnos con asistentes a fechas de Astronomy. Hoy no hay dato del lado de eventos |
| **Productos nuevos** | Modo Profesional ($440.000) lleva **0 ventas** | Hablar con 10 personas antes de invertir un peso más ahí |
| **IA** | Sin caso de uso con ROI hoy | Recién cuando el proceso de WhatsApp esté medido y sea repetible |

---

## 2. Roadmap por dinero esperado

### Los próximos 14 días — todo esto es sin código

| # | Acción | Plata/mes | Esfuerzo | Riesgo |
|---|---|---|---|---|
| 1 | **Etiquetar y cronometrar el WhatsApp**, 14 días | hasta **+$5.300.000** | 30 min + 2 min/conv | nulo |
| 2 | `wa.me` con código por anuncio | habilita decidir US$590 | 20 min | nulo |
| 3 | Escribirles a los **6 con créditos venciendo** | **+$861.120** protegidos | 30 min | nulo |
| 4 | Escribirles a los **9 que no pagaron** | +$287.040 | 30 min | nulo |
| 5 | Preguntarles a los **16 que se fueron** por qué | +$430.560 si vuelven 3 | 1 h | bajo |
| 6 | Ofrecer Gold a los 4 Silver | +$104.160 | 20 min | nulo |
| 7 | Pedir referidos a mano a los 15 de Curso DJ | +$430.560 | 1 h | nulo |

**Total del bloque: menos de 5 horas de trabajo humano, sin una línea de código.**

### Días 15–45 — automatizar lo que ya funcionó

Sólo se construye lo que en el bloque anterior demostró que funciona a mano:

1. **Aviso automático de créditos por vencer** (cron + mail, 1 día) — si el frente 3 funcionó.
2. **Guardar `utm_source` y `referrer` al crear la cuenta** (2 h) — sin esto, escalar pauta
   es apostar, y hay techo de US$500/mes justamente por eso.
3. **Mail de bienvenida con un solo botón: agendá tu primera clase** (1 día).
4. **Recuperación automática de checkout abandonado** (1 día) — si el frente 4 funcionó.

### Días 45–90 — recién acá, volumen

**Con una condición dura:** sólo si al 31/08 el churn de agosto confirma LTV/CAC > 2. Si no,
no se sube un peso de pauta.

1. Escalar pauta al techo de US$500 con el creativo que el código de WhatsApp haya validado.
2. Oferta de entrada para llenar las 256 horas muertas.
3. Programa de referidos formal.

---

## 3. Lo que NO haría, y por qué

- **No subir el presupuesto de pauta hoy.** LTV/CAC puede ser 0,64. Es comprar pesos a peso
  y medio y llamarlo crecimiento.
- **No empujar Modo Profesional.** $440.000 de ticket, cero ventas. Con cero ventas no hay
  nada que optimizar: hay que preguntar.
- **No construir un dashboard nuevo.** Ya hay `/admin/growth` y `/admin/conciliacion`. El
  dato que falta (WhatsApp) no está en ninguna base: está en el teléfono de José.
- **Nada nuevo sobre pagos.** Congelado.

---

## 4. La pregunta que ordena los próximos 90 días

**¿Cuántos de los 19 que pagaron en julio renuevan en agosto?**

Ese número —que llega solo el 31/08, sin trabajo— define si el negocio es una máquina que
escala o un balde agujereado:

- **Si renuevan 15 o más** (churn ≤ 20%): LTV/CAC ~1,9 y con el WhatsApp arreglado se va a
  3–7x. Ahí se escala pauta con todo.
- **Si renuevan menos de 12**: la retención es el problema y **cada peso de pauta hasta
  arreglarla es plata tirada**.

Mientras tanto, las 5 horas del primer bloque se hacen igual: son gratis y no dependen de
esa respuesta.
