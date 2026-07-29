# Creativos nuevos y campañas por producto

Fecha: 2026-07-28 · Cuenta `CP - Astronomy Academy`

> **Al 29/07/2026 hay que volver a subirlas.** Las 75 placas se rehicieron (una foto
> distinta por tarjeta y el gancho al frente — ver `LAB_NOTES.md`) y el
> `META_ACCESS_TOKEN` del `.env` está vencido: Facebook lo invalidó por cambio de
> contraseña. Con un token nuevo: `subir_creativos.py --send` y después
> `crear_carrusel.py --producto modo-profesional --variante dolor --send`.

Las placas se suben por API con `scripts/subir_creativos.py`; los hashes quedan en
`data/pauta/creativos.json`. No hace falta arrastrar archivos en el Administrador.

| Formato | Medida | Para qué |
|---|---|---|
| `feed` | 1080 × 1350 | Anuncio simple en feed |
| `square` | 1080 × 1080 | **Tarjetas de carrusel** |
| `story` | 1080 × 1920 | Stories y Reels |

Cinco productos × cinco ángulos: `que-es · beneficios · como-funciona · profe · contacto`.

---

## Qué está bloqueado y qué no

La app `astronomy-ads` está en modo Desarrollo. Eso bloquea **crear anuncios** por API —
Meta los marca `WITH_ISSUES` y no entregan. No bloquea subir imágenes, leer métricas,
pausar, reactivar ni mover presupuesto.

Se destraba cuando `astronomyofficial.com/privacidad` esté online y la app pase a "Activo".
Todo lo de abajo está armado para ejecutarse en ese momento, o a mano en el Administrador
por quien quiera hacerlo antes.

---

## La restricción que ordena todo el plan

Presupuesto actual: **US$19,56/día ≈ US$587/mes**, todo en un solo conjunto.

Meta necesita ~50 conversiones por semana y por conjunto para salir de aprendizaje. A
US$2 la conversación, US$587/mes son ~290 conversaciones al mes, o **67 por semana**.

**Eso alcanza para un conjunto bien alimentado. No para cinco.** Lanzar los cinco
productos juntos deja a cada uno con 13 conversaciones semanales: ninguno sale de
aprendizaje, todos entregan mal, y a fin de mes no sabés nada de ninguno.

Por eso: **se construyen los cinco, se enciende uno por vez.**

---

# Movimiento 1 — El carrusel, sin esperar nada

Lo más barato y de mayor valor que se puede hacer hoy: **meter un carrusel como sexto
anuncio dentro del conjunto que ya está corriendo.**

Sin campaña nueva, sin conjunto nuevo, sin partir el presupuesto y sin reiniciar el
aprendizaje. Meta reparte la entrega entre los anuncios existentes y el carrusel, y en
dos semanas se ve solo cuál gana.

Es relevante porque **la cuenta nunca pautó un carrusel**: en 35 meses y 186 anuncios,
todos fueron imagen simple o video. Es una variable entera sin explorar.

### Estructura del carrusel — Curso de DJ

Cinco tarjetas en formato `square`, en orden narrativo:

| # | Placa | Titular de la tarjeta |
|---|---|---|
| 1 | `curso-dj/que-es__square` | Aprendé a mezclar en cabina real |
| 2 | `curso-dj/beneficios__square` | Cuatro clases por mes, uno a uno |
| 3 | `curso-dj/como-funciona__square` | Elegís día y horario desde tu cuenta |
| 4 | `curso-dj/profe__square` | Con DJs que tocan de verdad |
| 5 | `curso-dj/contacto__square` | Escribinos y arrancás esta semana |

**Texto principal:**

> Cabina profesional en Nordelta Plaza, clases uno a uno y profes que están tocando hoy.
> No es un curso grabado: venís, te sentás en los platos y aprendés con alguien al lado.
> Escribinos y te contamos cómo arrancar.

**Descripción:** Astronomy Academy · Nordelta Plaza
**Botón:** Enviar mensaje por WhatsApp

---

# Movimiento 2 — Las campañas por producto

Todas con la misma estructura, que es la única que la cuenta demostró que funciona:

```
Campaña   academy | <producto> | mensajes | <mes-año>
          objetivo Interacción · optimización CONVERSACIONES · destino WHATSAPP
└── Conjunto  <producto> | <geo> | 18-65 | advantage+
    ├── Carrusel  5 tarjetas square
    ├── Simple    feed  · ángulo que-es
    └── Simple    story · ángulo contacto
```

Número de WhatsApp: `5491124005565` · Página: `271070669425605`

## El orden, y por qué

### 1. Producción online — el primero, y es un cambio de prioridad

**Va primero por la geografía.** El hallazgo más fuerte de toda la cuenta es que los
conjuntos de alcance país rinden 387–680 impresiones por conversación y los atados a un
radio chico, 1.067–1.564. Dos a tres veces mejor.

Hasta ahora ese dato no se podía aprovechar, porque los productos son presenciales en
Nordelta y una conversación desde Salta no sirve. **Producción online es el único producto
que se vende legítimamente a todo el país** — es el que puede usar el inventario barato sin
traer gente que no puede venir.

- **Geo:** Argentina entera, **excluyendo** 35 km alrededor de Nordelta (si no, compite
  contra el conjunto presencial y encarece a los dos).
- **Ángulos:** carrusel completo + `que-es` feed + `profe` story.

**Texto principal:**

> Producí música desde tu casa, con un profe que corrige lo que hacés. Clases uno a uno
> por videollamada, en Ableton, adaptadas a tu nivel y a lo que querés hacer. Estés donde
> estés. Escribinos y te contamos cómo empezar.

### 2. Membresías — la palanca de LTV

El problema más caro del negocio es que **el 46% de los alumnos paga una sola vez**. Una
membresía es recurrente por diseño: es el producto que ataca el problema, no el síntoma.

- **Geo:** 35 km alrededor de Nordelta (mismo que el conjunto actual).
- **Ángulos:** carrusel completo + `beneficios` feed + `como-funciona` story.

**Texto principal:**

> Una membresía, todos los créditos que quieras usar. Clases de DJ, producción en Ableton,
> alquiler de cabina y de estudio: elegís vos en qué los gastás, mes a mes, y lo que no
> usás se acumula. Escribinos y te armamos el plan que te sirve.

### 3. Modo Profesional — con los videos

Los videos humanos ya están filmados. El video es el formato que la cuenta menos exploró
y el que mejor funciona para este público.

- **Geo:** 35 km alrededor de Nordelta.
- **Creativos:** los videos como principal, y las placas de `modo-profesional` como banco
  de rotación cuando el video se gaste.

**Texto principal:**

> Ya sabés lo básico y querés dar el salto. Modo Profesional es para el que quiere vivir
> de esto: producción, identidad sonora y salida real a tocar. Escribinos y charlamos si
> es para vos.

### 4. Producción presencial — última, y por una razón

Compite contra Curso de DJ por el mismo público, en la misma zona y con el mismo
presupuesto. Encenderla mientras el Curso de DJ corre es hacer que dos conjuntos tuyos
pujen por las mismas impresiones y se encarezcan mutuamente.

**Entra solo si el Curso de DJ se apaga, o si el presupuesto sube lo suficiente como para
alimentar a los dos.**

---

## Nomenclatura

Hoy hay campañas llamadas `Int`, `Interaccion` y `Tráfico`, y dos conjuntos con el mismo
nombre. Así no se puede leer la cuenta a tres meses vista.

```
Campaña   academy | <producto> | mensajes | <mes-año>
Conjunto  <producto> | <geo> | <edad>
Anuncio   <producto> | <angulo|carrusel> | <formato> | <variante> | v<n> | <mes-año>
```

Ejemplo: `academy | produccion-online | mensajes | ago-26` → `produccion-online | arg-sin-nordelta | 18-65`
→ `produccion-online | carrusel | square | base | v2 | ago-26`.

**La versión y el mes no son decoración, y no se escriben a mano.** El 29/07/2026 se
creó un carrusel que quedó con el nombre **idéntico** al viejo que venía a reemplazar,
porque el nombre salía de producto+formato+variante y la variante no había cambiado.
En el Administrador se distinguían solo por el estado: un click de distancia de pausar
el equivocado. Ahora `nombrar()` en `crear_carrusel.py` lee los anuncios del conjunto,
busca el `v<n>` más alto de esa misma combinación y usa el siguiente. Arranca en `v2`
porque `v1` es el nombre viejo, el que no llevaba versión explícita.

---

## Reglas de operación

**No tocar 7 días.** Un conjunto nuevo no se edita durante su primera semana: cada cambio
reinicia el aprendizaje y tira lo aprendido. Es el error más caro y el más común.

**Rotación.** Si un creativo pasa 4 días seguidos con el costo por conversación 50% arriba
del promedio de su conjunto, se apaga y entra otro del banco. Cuatro días, no dos: con este
volumen, dos días malos son ruido.

**Nunca apagar por menos de 20 conversiones.** Con muestras de 3 a 5 se decide por azar.

---

## Lo que este plan no puede resolver

Todo esto mejora el **costo por conversación**. Ninguna parte mejora la conversión de
conversación a alumno que paga.

Entran ~100 conversaciones por mes y el negocio suma 7,8 alumnos nuevos. Si esa tasa es
mala, cinco campañas nuevas ejecutadas perfecto le multiplican el trabajo a José y no la
facturación.

**El carrusel y la rotación de creativos valen igual** —bajan el costo del lead sin subir
el gasto— pero encender productos nuevos y subir presupuesto sigue esperando la tasa de
cierre.
