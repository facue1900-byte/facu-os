# Pedido a Gonza — export del bot con el referral del anuncio

Armado 05/10/2026. **SIN MANDAR** — lo manda Facu.

## Por qué

El export del 16/09 (`data/whatsapp-bot-academy-2026-09-16/`, 999 CSV) trae solo
`Fecha,Hora,De,Mensaje`. Sin el referral no se puede saber qué anuncio trajo cada lead,
y la atribución hoy se hace por el texto autocompletado del anuncio, que se
pierde si el lead lo borra.

El reporte de Meta de septiembre ya está bajado por API:
`data/meta-ads-2026-09/ads_manager_sep_2026.csv` (5 anuncios, US$444,46, 289
conversaciones; cierra contra el total de la cuenta).

## Mensaje

> Gonza, ¿cómo va? Necesito un export nuevo de las conversaciones del bot de Academy,
> desde el 01/09 hasta hoy, y esta vez con el dato del anuncio que trajo a cada persona.
>
> Cuando alguien escribe desde un anuncio de Meta (click-to-WhatsApp), el primer mensaje
> llega con un objeto `referral` en el webhook. Necesito, por chat:
>
> - teléfono
> - fecha y hora del primer mensaje
> - `referral.source_id` (el ID del anuncio)
> - `referral.source_type` y `referral.source_url`
> - `referral.ctwa_clid` (el click ID)
> - `referral.headline` si viene
>
> Si la plataforma no guarda el `referral`, avisame cuál es la plataforma y si se puede
> activar para que se guarde de acá en adelante. Con que esté en una columna más del
> export me alcanza.
>
> ¡Gracias!
