# Jarvis de escritorio

La pantalla que se prende cuando te sentás en la Mac. Te saluda en voz alta y canta los números del día.
Además le podés hablar o escribir.
Se armó el 11/11/2026 a partir del reel de @cindiezhu ("How to build your own JARVIS"). El cerebro
es el mismo que el de Jarvis por Telegram (`execution/telegram_bot.py`). Esto le agrega la escena:
pantalla, voz y brief diario.

## Cómo se usa

- **Abrirlo:** doble click en **Jarvis** (en `~/Applications`; arrastralo al Dock), o
  `~/facu-os/execution/jarvis/jarvis.sh`. Si el servidor no estaba prendido, lo levanta.
- **Despertarlo:** tocá la pantalla o apretá cualquier tecla. Jarvis lee el brief del día.
- **Hablarle:** **mantené apretada la barra espaciadora** (o el orbe del medio), hablá y soltá.
  El audio se transcribe en la Mac con Whisper: no sale a ningún servicio.
- **Escribirle:** en la barra de abajo, + Enter.
- **Pedirle un cambio:** te muestra un **PLAN** con botones. Recién con **Sí, hacelo** lo
  ejecuta otro Claude que solo ve el plan. Es el mismo candado que en Telegram, y depende del
  mismo interruptor: `TELEGRAM_MODO_CAMBIOS=1` en `.env`.
- **Actualizar:** recalcula los números y el brief al momento (tarda ~1 min).
- **Nueva charla:** arranca la conversación de cero.

## El brief de la mañana

`brief.py` corre todos los días a las **07:50** (`launchd/com.facu.jarvis-brief.plist`) y deja
todo listo en `data/jarvis/`:

| Panel | De dónde sale | Nota |
|---|---|---|
| Astronomy Academy | `astronomy_numeros.mjs` → `lib/ingresos.ts` y `lib/payments.ts` de la app | Son las mismas funciones que usa el admin. Activos = la cuenta del dashboard. |
| Pauta · Meta Ads | `active/astronomy/pauta/leer_meta.py` | En USD y sin convertir. Techo US$500/mes (`os/03-EMPRESA.md`). |
| Paseo Nordelta | `radar_deudores.clasificar()` sobre Ctas Ctes, que se baja fresca cada vez | Ctas Ctes se carga **a mano**: si está atrasada, la deuda también. |
| Bandeja y sistema | Gmail (`messagesUnread` de INBOX) + `recolectar.chequeo_tareas()` | Cuentas facu, paseo y studio. |

Los números los calcula el código; Claude solo los cuenta. Una fuente que falla aparece en
**"Sin dato"**, nunca en cero. El texto hablado puede sumar pendientes del doc **Radar Facu**.

## Prenderlo / apagarlo

Brief automático (una vez, desde la Terminal):

```
cp ~/facu-os/execution/launchd/com.facu.jarvis-brief.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.facu.jarvis-brief.plist
```

Apagar el servidor: `pkill -f jarvis/servidor.py`. Log: `data/logs/jarvis.log`.

## Seguridad

- El servidor escucha **solo en 127.0.0.1:7777**: nadie de afuera de la Mac lo ve.
- Cada `/api` exige un token que cambia cada vez que arranca el servidor y se chequea el `Host`.
  Así una página web abierta en el mismo Chrome no le puede mandar órdenes.
- El Claude que contesta está en **solo lectura y sin internet** (los mismos permisos que el bot).

## Lo que muestra el reel y acá no está, a propósito

- **Contestar mails de clientes solo.** Va contra la regla 10: nada sale sin tu OK. Un borrador sí
  se puede pedir como plan.
- **Publicar en todas las redes con un comando.** Mismo motivo; además, el agente de reels está pausado.
- **Voz británica / ElevenLabs.** No querés más suscripciones. Se usa la voz de la Mac, grave.
  Si aparece una argentina instalable, se cambia `VOZ` en `telegram_bot.py`.
- **Palabra de activación ("Hey Jarvis").** Necesita el micrófono escuchando todo el tiempo.
  Hoy se usa la barra espaciadora.
