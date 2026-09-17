# Oferta 2026 — Astronomy Academy

**Borrador de trabajo.** Dictado por Facu y Mateo el 17/09/2026. Todavía tiene decisiones
abiertas, marcadas con 🔴. **Nada de acá sale a un alumno hasta que Facu lo apruebe.**

Esta es la **fuente única de verdad** de la oferta. De acá se derivan, en este orden:
la landing, el árbol del bot, los guiones de pauta, `lib/productos.ts` y la tabla `plans`.
Si algo dice un precio distinto al de este archivo, está mal ese otro lado.

---

## La decisión de fondo

**La membresía es el único producto.** Se discontinúan como productos sueltos:

- **Modo Profesional** ($449.999, cohorte oct-2026). Cero ventas en toda su historia, y
  bloquea la franja 17-22 de la cabina las 8 semanas. Se absorbe dentro de Platinum, en
  formato más chico (4 clases, no 8).
- **Curso de DJ mensual** (240 cr que se resetean). Los 14 activos pasan a Silver.

Motivo, en palabras de Facu: *"si ya tenemos un producto que funciona, que son las
membresías, ¿por qué queremos crear más cursos que no sabemos si funcionan? No vendimos
nada y nos quita tiempo para ofrecer nuestro producto. Mezclamos a José, a Luqui, las
finanzas, el bot."*

**Los créditos se mantienen.** Facu: *"podemos jugar con la inflación, tenemos nuestra
propia economía interna."* Ver la sección *La economía del crédito* más abajo: esa palanca
tiene un costo que hay que decidir a ojos abiertos.

---

## Los tres niveles

| | **Silver** | **Gold** | **Platinum** |
|---|---|---|---|
| Créditos/mes | **240** | 🔴 360 (a confirmar) | 🔴 720 (a confirmar) |
| Clases de DJ | ✅ nivel inicial | ✅ | ✅ |
| Clases de producción | ✅ nivel inicial | ✅ | ✅ |
| Producción online (Valen Frando / Owners Of Time) | — | ✅ | ✅ |
| Alquiler de cabina | — | ✅ | ✅ |
| DJ Delivery | — | ✅ | ✅ |
| Unreleased tracks | — | ✅ | ✅ |
| **Curso Profesional** (4 clases, temario, horario fijo) | — | — | ✅ |
| Presskit (si no tiene) | — | — | ✅ |
| Instalación de Ableton / plugins | — | — | ✅ |

Los créditos **acumulan** mientras el alumno siga pagando, y **vencen a 2 meses del último
pago** (regla dictada el 04/08/2026, sin cambios).

### Silver — la puerta de entrada
240 créditos, canjeables **sólo por clases** de DJ o de producción, **nivel inicial**.
Sin cabina, sin DJ Delivery, sin producción online. Es el nivel que hoy consume 130% de su
plan y tiene 69% de churn: la apuesta es que un Silver más definido empuje a subir a Gold
en vez de irse.

### Gold — el estudio
Todo lo de Silver **más**: producción online con Valen Frando, alquiler de cabina,
DJ Delivery y tracks inéditos. Es el nivel que hoy consume 65% de su plan y casi no se va.

### Platinum — el ecosistema
Todo lo de Gold **más**:

- **Curso Profesional.** 4 clases que valen **el doble de créditos** que una normal
  (120 cr cada una, 480 en total). Con temario. **Horario fijo semanal**: se elige un día y
  una hora y se respetan las 4 semanas. **Se cobra por adelantado** — la idea es
  justamente que no se falte, porque ya está pago. Si se paga en 2 cuotas, al acreditarse
  la segunda se agendan las clases restantes en el mismo día y horario, o el alumno puede
  elegir cambiarlo.
- **Presskit**, para el que no tiene.
- **Instalación de Ableton, plugins y demás**, para productores.
- **Mínimo 2 meses de permanencia.** 🔴 Ver pregunta 5.

---

## La economía del crédito

Hoy: **1 clase = 60 créditos**. De ahí sale todo lo demás.

| Plan | Créditos | Clases equivalentes | Costo de profe al tope ($11.000/clase) |
|---|---|---|---|
| Silver | 240 | 4 | $44.000 |
| Gold | 360 | 6 | $66.000 |
| Platinum | 720 | 4 del Curso Profesional + 4 normales = **8 reales** | $88.000 |

⚠️ **Por qué Platinum necesita 720 y no 480.** El Curso Profesional consume 480 créditos
él solo (4 × 120). Si Platinum queda en los 480 de hoy, el curso **se come el mes entero**
y al alumno no le queda un crédito para una clase suelta ni para la cabina. 720 le deja el
curso más 4 clases normales.

### Lo de la "inflación" — la palanca y su costo

Subir el precio en créditos de la clase (de 60 a 80, por ejemplo) sube el precio real sin
tocar el número que dice el plan. **Pero hay 22.840 créditos comprados y sin usar dando
vueltas** (59% de todo lo vendido; Toninelli solo tiene 7.680 acumulados). Devaluar el
crédito le licúa el saldo a los que ahorraron, exactamente como una devaluación de verdad,
y son justo los que menos vienen y más fácil se van.

**Recomendación: no tocar el valor de la clase en este cambio.** La palanca de precio son
los créditos del plan y el precio en pesos, que son limpios y no le sacan nada a nadie. La
inflación del crédito queda guardada para más adelante, avisada y con fecha.

---

## Precios

🔴 **Sin definir.** La derivación, apuntando al 60% de contribución que hoy da Gold —el
único nivel que no se va— y con los costos medidos (profe $11.000/clase, Mercado Pago
7,99% parejo, comisión del closer 7%):

| | Hoy | Derivado |
|---|---|---|
| Silver | $143.520 | ~$176.000 |
| Gold | $195.600 | ~$264.000 |
| Platinum | $272.000 | ~$355.000 |

**Son proyecciones sobre el consumo promedio medido el 04/08/2026, no sobre el consumo real
alumno por alumno, y el costo de profe está al tope (todos usan todas sus clases).** Antes
de que estos números salgan a un socio o entren al Libro, hay que correrlos contra la base.

Referencia de mercado (relevamiento 17/09/2026, ver `COMPETENCIA_2026.md`): 120 BPM cobra
**$121.000/mes** por 1 clase semanal de 1h20 durante 5 meses, sin cabina y con fecha de fin.
Es el único competidor de los cinco que publica tarifario completo.

---

## El diferencial

**Ninguna de las cinco competidoras vende una membresía mensual con acceso al estudio.**
Las cinco venden cursos con fecha de fin. Lo más parecido del mercado es alquiler de cabina
por hora (La Juanita, Sónica): pago por uso, sin acumulación, sin empaquetar con las clases.

Y las cinco comunican **formación**, ninguna comunica el después:
*"14 años formando"* (Arjaus) · *"Más de 20 años formando artistas"* (Sónica) ·
*"#APRENDECOMOLOSMEJORES"* (120 BPM) · *"La casa de los DJs y Productores"* (La Juanita).

> **Titular propuesto: todos te venden un curso. Nosotros te damos un estudio y una escena.**

El único que ya está parado en ese territorio es **Tekgen** (*"Primera Academia Underground
Argentina"*, academia + sello + productora) — pero sin web, sin precios públicos y con 13K
de Instagram. Es el que hay que ganarle de mano.

---

## 🔴 Decisiones abiertas

1. **Créditos de Gold y Platinum.** Facu definió 240 para Silver. Propuesta: Gold 360,
   Platinum 720 (ver arriba por qué 720).
2. **"Nivel inicial" en Silver: ¿qué es?** ¿Es el contenido de la clase, o es que sólo un
   principiante puede comprar Silver? Y si es lo segundo: quién decide que alguien dejó de
   ser principiante, y qué le pasa cuando lo decide.
3. **La quita a los Silver de hoy.** Los 9 Silver activos hoy tienen DJ Delivery y pueden
   canjear créditos por cabina. Con el diseño nuevo pierden las dos cosas. ¿Se las
   mantenemos mientras sigan pagando, o se las sacamos en la fecha de cambio?
4. **Quién hace el presskit y la instalación de Ableton.** Son horas de alguien. Si no
   tienen dueño con nombre, el beneficio se promete y no se cumple.
5. **El mínimo de 2 meses de Platinum:** ¿es permanencia (se cobran 2 meses juntos) o es
   que el presskit y la instalación se entregan recién con el segundo pago acreditado?
   La segunda opción no necesita desarrollo nuevo y no se cae si el alumno cancela en MP.
6. **Cabina.** El Curso Profesional de Platinum sigue bloqueando horario fijo en la cabina,
   igual que Modo Profesional. La cabina es UNA: 25 celdas en la franja 17-22. Hay que fijar
   cuántos Platinum se pueden vender antes de que la promesa se rompa.
7. **Fecha de inicio.** Propuesta: **1 de noviembre de 2026**, avisando esta semana. Cae el
   1° de un mes (si no, José y Luqui prorratean a mano) y deja octubre para construir.
8. **Precio de los tres niveles.**
9. **El punto 3 de Facu quedó sin dictar.**

---

## Lo que viene después de cerrar esto

1. Mail y WhatsApp a los alumnos activos. **Se prepara entero y se frena hasta el OK.**
2. Landing, sobre `/academy/preview`, que ya está armada.
3. Guiones de pauta.
4. Árbol del bot, leyendo los precios del mismo lugar que la web (hoy el bot cotiza
   $440.000 y $495.000 para el mismo producto, y la landing $449.999).
5. `lib/productos.ts` y la tabla `plans`.
