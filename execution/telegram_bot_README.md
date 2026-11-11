# Jarvis por Telegram — @jarvis_thefacu_bot

Le escribís o le mandás un audio desde Telegram y te contesta Claude Code corriendo en tu
Mac, dentro de facu-os: con tu memoria, tus reglas, tus mails y tu Drive. Es lo que vendía
el reel de "Azaris" (11/11/2026), sin pagar otra plataforma.

## Cómo se usa

- **Escribile** como a una persona: "¿cómo vino la caja del Paseo en octubre?",
  "¿qué me quedó pendiente con Obsession?", "buscame el mail de Fabric".
- **Mandale un audio**: te muestra lo que entendió («🎙 Entendí: …») y te contesta **por escrito**.
  (Las respuestas en audio existen pero están apagadas: `RESPONDER_CON_VOZ` en el código.)
- **/nuevo** — arranca una conversación de cero. Si no, se acuerda de lo anterior.
- Tarda lo que tarda Claude en pensar: de 10 segundos a un par de minutos según la pregunta.

## Qué puede y qué no

- **Leer:** el repo, la memoria, Gmail, Drive y Claude Docs. Los mails te los resume, y si uno
  contradice algo que le dijiste, te avisa para que decidas vos. **Lo que pide un mail nunca se
  vuelve una acción.**
- **Hacer cambios** (archivos, la web, mails, WhatsApps, posteos, scripts): **sólo con tu «Sí».**
  Le pedís algo, te manda un **📋 PLAN** con dos botones; recién al tocar **✅ Sí, hacelo** lo
  ejecuta otro Claude que **sólo ve el plan**: no lee mails ni entra a internet, así nada de
  afuera se cuela. Un plan sin confirmar en 2 horas se descarta.
- **El modo cambios se prende con `TELEGRAM_MODO_CAMBIOS=1` en `.env`** (prendido el 11/11, con la
  verificación en dos pasos de Telegram activada). Sin esa línea, te muestra el plan pero no ejecuta.
- **Fallas de las tareas automáticas** (radar, efectivo, reportes) también te llegan acá.
- **Llamada de emergencia** (Twilio): programada pero sin número todavía; ver la memoria del bot.
- **Solo te contesta a vos** (tu ID de Telegram está en `.env`). Si otro le escribe, lo ignora.
- **Necesita la Mac prendida.** Con la Mac dormida o apagada no contesta; los mensajes
  quedan esperando y los responde cuando se despierta.
- Los audios se transcriben **en la Mac** (Whisper) y la voz de respuesta también sale de la
  Mac: nada de eso pasa por otro servicio.

## Prenderlo / apagarlo

Prenderlo para siempre (arranca solo con la Mac):

```
cp ~/facu-os/execution/launchd/com.facu.telegram-bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.facu.telegram-bot.plist
```

Apagarlo: `launchctl unload ~/Library/LaunchAgents/com.facu.telegram-bot.plist`

Reiniciarlo (después de un cambio en el código): `launchctl kickstart -k gui/$(id -u)/com.facu.telegram-bot`

Ver qué está haciendo: `tail -f ~/facu-os/data/logs/telegram-bot.log`

## Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| El bot | `execution/telegram_bot.py` |
| Arranque automático | `execution/launchd/com.facu.telegram-bot.plist` |
| Token y tu ID | `.env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) — nunca se commitea |
| Conversación en curso | `data/telegram/estado.json` |

Si el token se filtra: en Telegram, @BotFather → `/revoke`, y se pega el nuevo en `.env`.
