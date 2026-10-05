# ManyChat — «Comentá SILVER / GOLD / PLATINUM»

Armado 05/10/2026, del plan de octubre (`~/Desktop/Productoras/Astronomy/Academia/Pauta/Pauta Academy - plan de octubre.pdf`, §3).
**Textos SIN OK de Facu** — le llegan a terceros (regla 10). Nada se activa hasta el OK.

Precios y clases verificados el 05/10 contra `plans` (base `qeakrjnseboiulcojlcw`) y contra
`astronomyofficial.com/academy` en vivo: Silver $143.520 · 4 clases · Gold $195.600 · 6 · Platinum $272.000 · 8.

## Dónde se dispara

| Palabra | Disparador en ManyChat | Video (anuncio pausado) |
|---|---|---|
| SILVER | Comentario en Instagram, cualquier posteo o reel, palabra clave `SILVER` | `120249372348700448` · instagram.com/p/Dd9oIEXgObq |
| GOLD | ídem, `GOLD` | `120249372356490448` · instagram.com/p/Dd9oQA6A7iQ |
| PLATINUM | ídem, `PLATINUM` | `120249372367740448` · instagram.com/p/Dd9oWxSAeMV |

«Cualquier posteo» a propósito: el mismo video va en orgánico y como anuncio; así cubre los dos.
Palabra clave sin distinguir mayúsculas («silver», «Silver»).

## El flujo (igual para los tres, cambia el bloque del plan)

**1. Respuesta pública al comentario** (rotan, para que Instagram no lo marque como spam):
- «Te mandé un mensaje 📩»
- «¡Listo! Fijate en tus mensajes»
- «Te escribí por privado»

**2. DM de apertura + pregunta con dos botones**
> ¡Hola! Te paso lo de [PLAN] 🎧
> Antes, una pregunta: ¿arrancás de cero o ya mezclás o producís?
>
> [Arranco de cero] [Ya mezclo o produzco]

**3. Según el botón, una línea** (después sigue igual):
- De cero: «Perfecto: las clases arrancan de tu nivel, con equipo real desde la primera.»
- Ya mezcla: «Buenísimo: el profe arma las clases sobre lo que ya sabés.»

**4. El plan, en tres líneas + precio**

SILVER
> • 4 clases por mes, de DJ o de producción, en el estudio de Nordelta
> • Elegís profe, día y hora desde la web
> • Lo que no usás se acumula
> **$143.520 por mes**

GOLD
> • 6 clases por mes, de DJ o de producción
> • La cabina y el estudio de producción para practicar solo
> • Producción online con Valen Frando, DJ Delivery y tracks unreleased
> **$195.600 por mes**

PLATINUM
> • 8 clases por mes, o la Carrera Profesional: 8 clases con temario en 2 meses
> • Tu presskit al terminarla
> • Todo lo de Gold, más grabación con cámaras y mixing y mastering
> **$272.000 por mes**

**5. Botón «Reservar mi primera clase»** (abre la web, con el plan ya elegido):
- Silver: `https://astronomyofficial.com/registro?plan=silver&utm_source=instagram&utm_medium=manychat&utm_campaign=comenta-plan&utm_content=silver-video`
- Gold: `…?plan=gold&…&utm_content=gold-video`
- Platinum: `…?plan=platinum&…&utm_content=platinum-video`

(Los tres responden 200, verificado 05/10. `utm_content` es lo que lee `/admin/leads/pauta`.)

Debajo, segundo botón: **«Prefiero hablar por WhatsApp»** → `https://wa.me/5491124005565?text=Hola!%20Vengo%20de%20Instagram%2C%20quiero%20[PLAN]%20%5BIG-[PLAN]%5D`
— el código `[IG-SILVER]` / `[IG-GOLD]` / `[IG-PLATINUM]` es para saber en el bot que vino de acá.

**6. Recordatorio único, 23 h después, sólo si no tocó ningún botón**
> ¿Pudiste mirarlo? Si querés, te reservo un lugar esta semana 👇
> [Reservar mi primera clase]

(23 h y no 24: después de 24 h Instagram no deja escribir sin que la persona responda.)

## Después de armarlo

1. Probar con una cuenta propia comentando en uno de los videos: que llegue el DM, que los dos botones anden y que el link abra el registro con el plan.
2. Con el OK de Facu: activar las 3 automatizaciones y prender los 3 anuncios
   (`POST {ad_id} status=ACTIVE`). Releer de Meta que quedaron ACTIVE.
3. Mirar el 16/10 en `/admin/leads/pauta`: cuentas y compras con `utm_medium=manychat`.
