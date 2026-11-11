# Jarvis por Telegram — @jarvis_thefacu_bot

Le escribís o le mandás un audio desde Telegram y te contesta Claude Code corriendo en tu
Mac, dentro de facu-os: con tu memoria, tus reglas, tus mails y tu Drive. Es lo que vendía
el reel de "Azaris" (11/11/2026), sin pagar otra plataforma.

## Cómo se usa

- **Escribile** como a una persona: "¿cómo vino la caja del Paseo en octubre?",
  "¿qué me quedó pendiente con Obsession?", "buscame el mail de Fabric".
- **Mandale un audio**: te muestra lo que entendió («🎙 Entendí: …») y después contesta.
- **/nuevo** — arranca una conversación de cero. Si no, se acuerda de lo anterior.
- Tarda lo que tarda Claude en pensar: de 10 segundos a un par de minutos según la pregunta.

## Qué puede y qué no

- **Solo lectura.** Lee el repo, la memoria, Gmail, Drive, Claude Docs y la web.
  **No manda, no escribe, no borra nada** (regla 10). Si le pedís algo así, te dice qué
  haría y que lo hagas desde Claude Code en la Mac.
- **Solo te contesta a vos** (tu ID de Telegram está en `.env`). Si otro le escribe, lo ignora.
- **Necesita la Mac prendida.** Con la Mac dormida o apagada no contesta; los mensajes
  quedan esperando y los responde cuando se despierta.
- Los audios se transcriben **en la Mac** (Whisper), no salen a ningún servicio.

## Prenderlo / apagarlo

Prenderlo para siempre (arranca solo con la Mac):

```
cp ~/facu-os/execution/launchd/com.facu.telegram-bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.facu.telegram-bot.plist
```

Apagarlo: `launchctl unload ~/Library/LaunchAgents/com.facu.telegram-bot.plist`

Ver qué está haciendo: `tail -f ~/facu-os/data/logs/telegram-bot.log`

## Dónde vive cada cosa

| Qué | Dónde |
|---|---|
| El bot | `execution/telegram_bot.py` |
| Arranque automático | `execution/launchd/com.facu.telegram-bot.plist` |
| Token y tu ID | `.env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) — nunca se commitea |
| Conversación en curso | `data/telegram/estado.json` |

Si el token se filtra: en Telegram, @BotFather → `/revoke`, y se pega el nuevo en `.env`.
