# Oferta 2026 — Astronomy Academy

**Borrador de trabajo.** Dictado por Facu y Mateo el 17/09/2026, segunda pasada.
Lo que sigue abierto está marcado con 🔴. **Nada de acá sale a un alumno hasta el OK de Facu.**

Esta es la **fuente única de verdad** de la oferta. De acá se derivan, en este orden:
la landing, el árbol del bot, los guiones de pauta, `lib/productos.ts` y la tabla `plans`.
Si algo dice un precio distinto al de este archivo, está mal ese otro lado.

---

## La decisión de fondo

**La membresía es el único producto.** Se discontinúan como productos sueltos:

- **Modo Profesional** ($449.999, cohorte oct-2026). Cero ventas en toda su historia, y
  bloquea la franja 17-22 de la cabina las 8 semanas. **No se elimina: se incrusta dentro
  de Platinum**, con el mismo contenido (8 clases), repartido en 2 meses.
- **Curso de DJ mensual** (240 cr que se resetean). Los 14 activos pasan a Silver.

Facu: *"si ya tenemos un producto que funciona, que son las membresías, ¿por qué queremos
crear más cursos que no sabemos si funcionan? No vendimos nada y nos quita tiempo para
ofrecer nuestro producto. Mezclamos a José, a Luqui, las finanzas, el bot."*

Y sobre por qué el curso va adentro y no al lado: *"la idea es potenciar esta venta de
membresías, que no tengamos tantas cosas y que no se entienda."*

**Los créditos se mantienen** como moneda interna.

**Las membresías NO son nivelatorias** (Facu, 17/09). Nadie queda excluido de un plan por
su nivel: el alumno elige según el servicio que quiere. A mayor membresía, más cosas puede
hacer — pero no hay un examen ni un portero.

---

## Los tres niveles

| | **Silver** | **Gold** | **Platinum** |
|---|---|---|---|
| Créditos/mes | **240** | 🔴 **360** (a confirmar) | **540** |
| Clases de DJ | ✅ | ✅ | ✅ |
| Clases de producción | ✅ | ✅ | ✅ |
| Producción online (Valen Frando / Owners Of Time) | — | ✅ | ✅ |
| Alquiler de cabina | — | ✅ | ✅ |
| DJ Delivery | 🔴 add-on pago | ✅ | ✅ |
| Unreleased tracks | — | ✅ | ✅ |
| **Carrera Profesional** (8 clases en 2 meses) | — | — | ✅ |
| Presskit | — | — | ✅ al completar las 8 clases |
| Instalación de Ableton / plugins | — | — | ✅ a pedido, 🔴 cuesta créditos |

Los créditos **acumulan** mientras el alumno siga pagando, y **vencen a 2 meses del último
pago** (regla del 04/08/2026, sin cambios).

### Silver — sólo clases
240 créditos = 4 clases de DJ o de producción. Sin cabina, sin producción online, sin
tracks inéditos. Es el nivel que hoy consume 130% de su plan y tiene 69% de churn.

### Gold — el estudio
Todo lo de Silver **más** producción online con Valen Frando, alquiler de cabina,
DJ Delivery y tracks inéditos. Hoy consume 65% de su plan y casi no se va: es el nivel sano.

### Platinum — el ecosistema
Todo lo de Gold **más** la **Carrera Profesional**, el presskit y la instalación.

---

## La Carrera Profesional, dentro de Platinum

Es el ex Modo Profesional, **mismo contenido**, reempaquetado:

- **8 clases en total**, con temario, a razón de **4 por mes durante 2 meses**.
- **Cada clase vale el doble**: 120 créditos en vez de 60. **El doble crédito aplica sólo a
  las clases de la Carrera** (Facu, 17/09) — una clase normal sigue costando 60.
- **Horario fijo semanal.** Se elige día y hora y se respetan las 4 semanas del mes.
- **Se cobra por adelantado.** Es a propósito: *"la idea es no faltar porque ya se cobra."*
- Si se paga en 2 cuotas, al acreditarse la segunda se agendan las clases restantes en el
  mismo día y horario, o el alumno puede elegir cambiarlo.

**Por qué Platinum tiene 540 y no 480:** la Carrera consume 480 créditos por mes
(4 × 120). Los 60 que sobran son para que el alumno igual pueda pagar un alquiler de
cabina, un mixing & mastering o una clase de producción ese mes.

**El objetivo declarado de este diseño es que el alumno pague Platinum dos veces**, que es
lo que le toma completar la carrera.

---

## ⚠️ El agujero del doble crédito

El doble crédito protege el costo **sólo si el alumno hace la Carrera**.

Un Platinum que **no** la hace gasta sus 540 créditos en **9 clases normales** (540 ÷ 60),
y eso son **$99.000 de profe** — más caro que Gold, que son 6 clases por $66.000. O sea que
el peor caso de Platinum no es el que hace la carrera: es el que no la hace.

| Platinum | Consumo | Clases reales | Costo de profe |
|---|---|---|---|
| Hace la Carrera | 480 + 60 | 4 + 1 | **$55.000** |
| No la hace | 540 en clases sueltas | 9 | **$99.000** |

🔴 **Decisión pendiente: ¿la Carrera es obligatoria al comprar Platinum, o es opcional?**
Si es opcional, el precio tiene que cubrir los $99.000 del peor caso.

---

## Precios — recomendación

Costos medidos: profe **$11.000/clase**, Mercado Pago **7,99% parejo** (monotributo, el IVA
no se recupera), comisión del closer **7%**.

| | Hoy | **Propuesto** | Contribución |
|---|---|---|---|
| Silver | $143.520 | **$175.000** | 60% |
| Gold | $195.600 | **$245.000** | 58% |
| Platinum | $272.000 | **$340.000** | 69% con Carrera · **56% sin ella** |

Platinum a $340.000 **aguanta los dos casos** del agujero de arriba, así que no hace falta
decidir si la Carrera es obligatoria para poner el precio — sólo para prometerla bien.

**Estos números son derivaciones sobre el consumo promedio medido el 04/08/2026, no sobre
el consumo real alumno por alumno.** Antes de que salgan a un socio o entren al Libro, hay
que correrlos contra la base.

### El número que hay que mirar de frente

**Completar la Carrera ahora cuesta 2 × $340.000 = $680.000**, contra los $449.999 de Modo
Profesional. Es 51% más caro.

El contraargumento, y es fuerte: **Modo Profesional a $449.999 vendió cero.** No hay ninguna
evidencia de que ese precio fuera vendible — lo único probado es que las membresías venden.
Además el que paga $680.000 no se lleva sólo 8 clases: se lleva dos meses de estudio
completo, cabina, producción online, DJ Delivery, tracks inéditos y presskit, y **queda
adentro como member el mes 3**, que es donde está el negocio de verdad.

Aun así, es el número que más fácil puede frenar una venta. 🔴 Facu decide.

### Referencia de mercado
120 BPM cobra **$121.000/mes** por 1 clase semanal de 1h20 durante 5 meses, sin cabina y con
fecha de fin (bpmescuela.com, 17/09/2026). Es la única de las cinco competidoras que publica
tarifario completo. Silver a $175.000 está 45% arriba, por algo que ellos no dan.

---

## Los Silver de hoy: la quita y el incentivo

Los 9 Silver activos hoy tienen DJ Delivery y pueden canjear créditos por cabina. En el
diseño nuevo pierden las dos cosas. Facu: *"avisarles con anticipación, pero habría que
buscar un incentivo para que se transformen de Silver a Gold, o que paguen el DJ Delivery
aparte."*

**Recomendación: DJ Delivery como add-on pago para Silver, a $35.000/mes.**

Convierte la quita en una decisión del alumno en vez de un castigo, y hace la aritmética
obvia:

| | Total | Qué se lleva |
|---|---|---|
| Silver + DJ Delivery | $210.000 | 4 clases + DJ Delivery |
| **Gold** | **$245.000** | 6 clases + DJ Delivery + cabina + producción online + tracks |

**Por $35.000 más se lleva 2 clases, la cabina, producción online y los tracks.** El que
hace la cuenta sube. El que no la hace, igual paga $35.000 que hoy no paga.

🔴 A confirmar: el precio del add-on y si se les mantiene el precio viejo de Silver
($143.520) a los 9 activos mientras sigan pagando.

---

## El diferencial

**Ninguna de las cinco competidoras vende una membresía mensual con acceso al estudio.**
Las cinco venden cursos con fecha de fin. Lo más parecido del mercado es alquiler de cabina
por hora (La Juanita, Sónica): pago por uso, sin acumulación, sin empaquetar con las clases.

Y las cinco comunican **formación**, ninguna comunica el después:
*"14 años formando"* (Arjaus) · *"Más de 20 años formando artistas"* (Sónica) ·
*"#APRENDECOMOLOSMEJORES"* (120 BPM) · *"La casa de los DJs y Productores"* (La Juanita).

> **Titular propuesto: todos te venden un curso. Nosotros te damos un estudio y una escena.**

El único parado en ese territorio es **Tekgen** (*"Primera Academia Underground Argentina"*,
academia + sello + productora) — sin web, sin precios públicos, 13K de Instagram. Es al que
hay que ganarle de mano.

Detalle completo en `COMPETENCIA_2026.md`.

---

## 🔴 Lo que falta definir

1. **Créditos de Gold.** Propuesta: 360 (6 clases). Silver 240 y Platinum 540 ya están.
2. **¿La Carrera Profesional es obligatoria al comprar Platinum o es opcional?**
3. **Cuántos créditos cuesta la instalación de Ableton/plugins.** Propuesta: 60 (una clase).
4. **Los tres precios**, y si Platinum a $340.000 (Carrera completa = $680.000) va o no.
5. **Precio del add-on de DJ Delivery para Silver.** Propuesta: $35.000/mes.
6. **A los 22 activos: ¿se les mantiene el precio viejo mientras sigan pagando?**
   Recomendación: sí. Con 69% de churn en Silver, un aumento en el mismo mail que les cambia
   la modalidad es la forma más rápida de perder la base — que ya viene cayendo hacia el
   equilibrio de 14,5 alumnos.
7. **Techo de Carreras simultáneas.** La cabina es UNA: 25 celdas en la franja 17-22, y cada
   Carrera bloquea un horario fijo durante 8 semanas. Hay que fijar el número antes de
   venderlas, no después.
8. **Fecha de inicio.** Propuesta: **1 de noviembre de 2026**, avisando esta semana. Cae el
   1° de un mes (si no, José y Luqui prorratean a mano) y deja octubre para construir.
9. **Qué pasa con la cohorte `oct-2026`**, que arranca el 05/10 y termina el 30/11, a caballo
   del cambio. Recomendación: no abrirla.

---

## Lo que viene después de cerrar esto

1. Mail y WhatsApp a los alumnos activos. **Se prepara entero y se frena hasta el OK.**
2. Landing, sobre `/academy/preview`, que ya está armada.
3. Guiones de pauta.
4. Árbol del bot, leyendo los precios del mismo lugar que la web (hoy el bot cotiza
   $440.000 y $495.000 para el mismo producto, y la landing $449.999).
5. `lib/productos.ts` y la tabla `plans`.
