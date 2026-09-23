# Aviso del 1/10 — los cambios que rigen el 1/11/2026

**Borradores. No sale nada sin OK de Facu (regla 10).** Armado el 23/09/2026 con la base
de ese día. Antes de mandar, volver a contar: la gente cambia de plan.

## A quién le cambia algo el 1/11 (medido 23/09, sin cuentas internas)

| Grupo | Cuántos | Qué pierde el 1/11 | ¿Lo usan hoy? (últimos 60 días) |
|---|---|---|---|
| Curso de DJ → pasa a Silver | 12 (+1 pendiente) | DJ Delivery y producción online | nada de eso |
| Silver de antes del 22/09 | 9 | alquiler de cabina/estudio, producción online, grupales, DJ Delivery, y bajan de 250 a 240 créditos | **sí: 8 alquileres y 5 clases online** |
| Gold de antes del 22/09 | 2 | clases grupales (pasan a ser de Platinum) | no |
| DJ Delivery suelto | 3 | pasa de $16.499 a $25.000 | — |

Los 9 Silver son los que más pierden y los que más usan lo que pierden: son el grupo al
que hay que ofrecerle Gold uno por uno.

Lo técnico ya está hecho y corre solo el 1/11: los límites por plan
(`lib/beneficios.ts`) y que cada cobro del curso se acredite como Silver
(`planQueSeAcredita`, `lib/payments.ts`). El 1/11 falta correr
`scripts/cursodj-a-silver.mjs --aplicar` (sólo cambia la etiqueta) y subir el plan
`djdelivery` a $25.000 **en Mercado Pago** (la base sola no cambia lo que cobra MP).

---

## 1. Curso de DJ (12)

> Hola {nombre}! Te escribo de Astronomy Academy con una novedad buena. Desde el 1 de
> noviembre el Curso de DJ pasa a ser la membresía **Silver**: pagás lo mismo
> ($143.520), seguís con tus 240 créditos por mes (4 clases), y ahora **los créditos que
> no uses se acumulan** mientras sigas siendo member, en vez de vencerse a fin de mes.
> No tenés que hacer nada: el cambio es automático.
> Si querés sumar la cabina para practicar solo y producción online, está **Gold**:
> astronomyofficial.com/academy. Cualquier duda, acá estamos.

## 2. Silver de antes (9)

> Hola {nombre}! Te escribo de Astronomy Academy para contarte con tiempo un cambio en
> las membresías que arranca el **1 de noviembre**.
> Silver pasa a ser la membresía de **clases**: 240 créditos por mes (4 clases de DJ o
> de producción). El **alquiler de cabina y estudio**, la **producción online** y
> **DJ Delivery** pasan a ser parte de **Gold**.
> Como vos venís usando {la cabina / producción online}, te conviene mirar Gold:
> $195.600, 6 clases por mes, la cabina y el estudio para practicar, producción online
> con Valen y DJ Delivery. Son $52.080 más que hoy y te llevás dos clases más y todo lo
> demás. Si preferís quedarte en Silver y sumar sólo DJ Delivery, son $25.000 aparte.
> Hasta el 31/10 seguís con todo como hasta ahora. ¿Te paso el link para cambiarte?

*(Personalizar el `{…}` con lo que usa cada uno: sale de sus reservas en `slot_bookings`.)*

## 3. Gold de antes (2)

> Hola {nombre}! Un aviso corto de Astronomy Academy: desde el **1 de noviembre** las
> **clases grupales** pasan a ser parte de Platinum. Todo lo demás de tu Gold sigue igual
> (tus clases, la cabina, el estudio, producción online y DJ Delivery). Cualquier duda,
> escribinos.

*(Ninguno de los dos hizo una grupal en los últimos 60 días: se puede no mandar.)*

## 4. DJ Delivery suelto (3)

> Hola {nombre}! Te escribo de Astronomy Academy: desde el **1 de noviembre** DJ Delivery
> pasa a **$25.000 por mes**. Si querés, con **Gold** ($195.600) viene incluido junto con
> clases, la cabina y el estudio: astronomyofficial.com/academy.

---

## 🔴 Pendiente de Facu
- OK a los textos y a quién se le manda.
- Precio de DJ Delivery en Mercado Pago el 1/11 (el preapproval_plan `d57dbc6a…`).
