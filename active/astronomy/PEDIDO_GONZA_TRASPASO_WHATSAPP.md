# Traspaso del WhatsApp de Academy: sacar a Gonza del medio

Armado 02/11/2026. **SIN MANDAR**: lo manda Facu. Reemplaza a `PEDIDO_GONZA_EXPORT_REFERRAL.md`.

## Lo que no sabemos todavía

- En qué plataforma corre el bot y a nombre de quién está el número +54 9 11 2400-5565.
- El token de Meta de facu-os no tiene permisos de WhatsApp: Meta devuelve error #200 al
  preguntar por las cuentas de WhatsApp del business `1973140593055903`.

## Mensaje

> Gonza, ¿cómo va? Decidimos pasar el WhatsApp de Academy a administrarlo nosotros. Para
> hacerlo ordenado, sin cortar la atención, necesito que me pases esto:
>
> **1. Dónde está montado**
> - ¿Qué plataforma usa el bot? ¿Va por la API oficial de WhatsApp o por otra vía?
> - ¿A nombre de quién está la cuenta de WhatsApp Business (WABA) del número y en qué
>   Business Manager? Pasame el ID de la WABA y el Phone Number ID.
> - ¿Quién paga las conversaciones a Meta y con qué medio de pago?
>
> **2. Accesos**
> - Darme como administrador en la plataforma y en la WABA (facue1900@gmail.com).
> - El PIN de verificación en dos pasos del número.
> - ¿Dónde está la línea (el chip)? ¿Quién recibe el SMS o la llamada de verificación?
>
> **3. Todo lo que armaste**
> - Export de todas las conversaciones, desde el 17/09 hasta hoy (hasta el 16/09 ya lo
>   tengo), con estas columnas por chat: teléfono, fecha y hora de cada mensaje, y si
>   entró por un anuncio: `referral.source_id`, `source_url`, `ctwa_clid`.
> - Las instrucciones del bot: prompt, escenarios, base de conocimiento.
> - Las plantillas de mensajes aprobadas y las reglas de los seguimientos automáticos.
> - La URL del webhook actual y cualquier otra integración conectada.
>
> **4. El cambio**
> - Por ahora no cambies ni apagues nada. Coordinamos juntos el día del pase.
> - Si hay algo pendiente de pago, o algún costo que hoy pagues vos, pasámelo.
>
> ¿Me lo mandás esta semana? ¡Gracias!

## Qué define cada respuesta

| Si dice | Qué pasa |
|---|---|
| WABA en nuestro Business Manager | Es lo más simple: se saca su acceso y se conecta la nuestra. |
| WABA en su Business Manager o del proveedor | Hay que migrar el número a nuestra cuenta. Necesita su colaboración y el PIN. |
| No usa la API oficial | No hay nada para migrar: se registra el número en la API y hay riesgo de bloqueo mientras tanto. |

## Antes de cortar

1. El historial no se migra con el número: guardar el export completo antes del pase.
2. Decidir dónde contesta José. Hoy usa WhatsApp Web; con API pura eso puede dejar de
   andar. Confirmar si aplica la coexistencia (app de WhatsApp Business + API) en este número.
3. `active/astronomy/bot/responder.py` es del 29/07 y nunca se conectó al WhatsApp real:
   su catálogo es anterior a la oferta de solo membresías. Actualizarlo y probarlo.
4. No apagar el bot de Gonza hasta tener el reemplazo probado con un número de prueba.
