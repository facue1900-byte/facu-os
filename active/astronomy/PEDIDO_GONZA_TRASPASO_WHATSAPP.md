# Traspaso del WhatsApp de Academy: sacar a Gonza del medio

Actualizado 02/11/2026. **SIN MANDAR**: lo manda Facu. Reemplaza a `PEDIDO_GONZA_EXPORT_REFERRAL.md`.

## Lo que sabemos

Gonza dijo el 16/09 que el bot corre en **Evolution API**. Es un puente de código abierto que
puede conectarse por una sesión tipo WhatsApp Web, vinculada con QR (no oficial), o por la API
oficial de Meta. Falta confirmar cuál usa. Si es QR, no hay cuenta de Meta para migrar: el
número vive en el teléfono o chip, y el servidor de Gonza es un dispositivo vinculado.

## Mensaje

> Gonza, vamos a pasar el bot de Academy a administrarlo nosotros. Por ahora no apagues
> ni cambies nada, coordinamos el día juntos. Necesito:
>
> 1. ¿Evolution está conectado por QR (Baileys) o por la API oficial de Meta?
> 2. ¿Dónde corre el servidor, a nombre de quién está y cuánto cuesta por mes?
> 3. ¿Qué más hay conectado además de Evolution (n8n, Typebot, Chatwoot, otro)? ¿Me das
>    acceso o me exportás esos flujos?
> 4. El prompt del bot, sus escenarios y la base de conocimiento, tal como están hoy.
> 5. Las reglas de los seguimientos automáticos: textos, cuándo salen y a quién.
> 6. Export de las conversaciones desde el 17/09 hasta hoy, en el mismo formato que la vez
>    pasada. Si los mensajes que entran por anuncio guardan el dato del anuncio
>    (`externalAdReply`, `ctwaClid`, `sourceId`), que venga en una columna más.
> 7. Si hay alguna cuenta de IA o servicio pago a tu nombre, o algo pendiente de pago, pasámelo.
>
> ¿Me lo mandás esta semana? ¡Gracias!

## Qué define cada respuesta

| Si dice | Qué pasa |
|---|---|
| QR / Baileys | Nada que migrar en Meta. Se corta desvinculando el dispositivo desde el teléfono. Hay riesgo de bloqueo por ser no oficial: conviene pasar a la API oficial. |
| API oficial de Meta | Pedir ID de la WABA, Phone Number ID, PIN de dos pasos, y en qué Business Manager está. |

## Antes de cortar

1. El teléfono lo tenemos nosotros (Facu, 02/11). Mirar en Dispositivos vinculados si figura el bot.
2. Guardar el export completo: es la única copia del historial.
3. Decidir dónde contesta José.
4. `active/astronomy/bot/responder.py` es del 29/07 y nunca se conectó al WhatsApp real: su
   catálogo es anterior a la oferta de solo membresías. Actualizarlo y probarlo.
5. No desvincular el bot de Gonza hasta tener el reemplazo probado con un número de prueba.
