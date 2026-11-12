# Jarvis de escritorio

Es tu intermediario con Claude Code: la pantalla que se prende cuando te sentás en la Mac. Lo que le
decís, lo hace Claude con todas sus herramientas, tu memoria y la Constitución. Para Jarvis es lo
mismo que si lo escribieras en la terminal.
- **v1 (11/11/2026):** salió del reel de @cindiezhu. Estaba en solo lectura y contestaba «no tengo el dato».
- **v2 (el mismo día):** pedido de Facu, «que todo lo que le digo te comande a vos».

## Cómo se usa

- **Abrirlo:** **Jarvis** en `~/Applications` (arrastralo al Dock). Si el servidor no está prendido, lo levanta.
- **Despertarlo:** tocá la pantalla o una tecla. Te lee el resumen del día con la voz de **Diego** (Argentina).
- **Hablarle:** mantené apretada la **barra espaciadora** (o el botón del micrófono o el núcleo).
  Hablá cuando diga «te escucho» y soltá. Whisper transcribe en la Mac.
- **Escribirle:** en la barra de abajo, más Enter.
- **Pedirle cosas:** pregunta un dato y lo busca (base, planillas, mails, código); pedile que
  corrija algo y lo corrige, lo verifica y commitea.
- **Tareas largas:** si algo lleva más de unos minutos, Jarvis lo **lanza en otra sesión de Claude Code**
  y sigue charlando. Aparece en **Operaciones**. Cuando termina, te avisa y te lee el reporte.
- **Abrir una sesión:** cada tarea tiene botones **Terminal** y **Antigravity** para entrar a esa sesión
  y seguir hablando ahí con Claude. Los botones de abajo abren la conversación de Jarvis.
  En Antigravity te deja el comando `claude --resume …` copiado para pegarlo en su terminal.
  También se lo podés pedir de palabra («abrime la tarea en la terminal»).
- **Lo que sale al mundo** (mails, WhatsApps, posteos, transferencias): vuelve como **PLAN** y se
  ejecuta sólo con **Aprobar** (regla 10, mismo interruptor `TELEGRAM_MODO_CAMBIOS`).
- **Nueva:** arranca la conversación de cero. **Actualizar:** recalcula los números (~1 min).

> El bot de **Telegram NO cambió**: sigue en solo lectura. Un teléfono se pierde; esta Mac no sale de casa.

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

Apagar el servidor: `lsof -tiTCP:7777 -sTCP:LISTEN | xargs kill`. Log: `data/logs/jarvis.log`.

## Seguridad

- El servidor escucha **solo en 127.0.0.1:7777**: nadie de afuera de la Mac lo ve.
- Cada `/api` exige un token que cambia cada vez que arranca el servidor y se chequea el `Host`.
  Así una página web abierta en el mismo Chrome no le puede mandar órdenes.
- El Claude que contesta tiene **el mismo alcance que tu terminal** (`--permission-mode auto`). El
  contenido de mails y webs es dato, nunca instrucciones. Lo que sale al mundo pasa por el botón.

## Lo que muestra el reel y acá no está, a propósito

- **Contestar mails de clientes solo.** Va contra la regla 10: nada sale sin tu OK. Un borrador sí
  se puede pedir como plan.
- **Publicar en todas las redes con un comando.** Mismo motivo; además, el agente de reels está pausado.
- **Voz británica / ElevenLabs.** No querés más suscripciones.
- **Palabra de activación ("Hey Jarvis").** Necesita el micrófono escuchando todo el tiempo.
  Hoy se usa la barra espaciadora.
- **Voz:** Diego (español de Argentina, gratis de Apple). Se elige solo en `telegram_bot._elegir_voz()`.
