# Reels diarios — lo que aprendimos

El agente diario lee esto ANTES de elegir las ideas del día y lo actualiza AL FINAL con lo
nuevo. Corto, con fecha y con número. Si algo deja de ser cierto, se borra.

## Gusto de Facu (manda sobre las métricas)

- 27/10: **nada animado, caricatura, 3D con personajes, pixel art ni historieta**: «muy falso, muy animado, de mala calidad».
  Sí le gustó el del cerebro (dato real, corto, estética neón premium, drop a los 6,5 s).
- 27/10: material real **con voz en off encima** (voz Charon, acento argentino), no sólo texto.
- La estética de la cuenta: negro, monocromo, mayúsculas, sin emojis en las piezas, sin violeta de la app.
- Las piezas no llevan precio en pesos.

- 29/10: los 10 del 28/10 «están mal hechos»: **terminaban con el audio mudo** (bug del armador:
  el audio se cortaba al terminar la voz; arreglado, y el QA ahora mide el audio) y **la voz no
  coincidía con los subtítulos** (los carteles los ponía el agente a ojo; ahora los subtítulos salen
  solos de la voz). La web de IG no deja archivar (sólo borrar): se le pidió a Facu archivarlos desde la app. Pasamos a **5 por día, menos pero mejores**.
- 29/10: la estética de las portadas «está bien, funcionan». Las ideas y la ejecución «están flojas».

## Lo que midieron los números

- 28/10 (31 h, todavía en prueba): los 10 reels «ciencia» 3D + la bala. Rango 98 → 1.395 vistas.
  Arriba: copa (1.395), túnel a la Tierra (1.350), espacio (1.305 y 5 guardados), papel (1.231), Newton (959).
  Abajo: sol (98), dominó (135), bala (135), agujero negro (172).
  O sea: el hook de «dato físico raro» funciona en vistas aunque a Facu no le guste lo 3D →
  probar el MISMO tipo de hook (pregunta/dato que intriga en el primer segundo) con material real.
- Vistas no son alumnos: en octubre la pauta trajo clics sin intención (0 clientes). Lo que vale
  es que el reel lo vea gente de zona norte y que escriban al WhatsApp.

## Proceso (28/10)
- 28/10: los guiones se generaron con un script; **regenerar guiones ya armados cambia su huella y `publicar.py` corta** → rearmar con `armar_reel.py` (voz cacheada, sin gasto de cuota) y no tocar guiones armados.
- 28/10: texto blanco sobre tomas claras del estudio (sala con la pared blanca) no se lee → `efecto: oscuro` + `pos: abajo`.
- 28/10: IG no entrega likes/vistas de otras cuentas por WebFetch; la competencia no se puede medir así.
- 28/10: se publicaron 10 reels nuevos de formatos distintos (swipe falso, loading, POV, process, etc.). Leer sus números el 31/10 para ver qué formato gana.

## 29/10
- 29/10: set completo de GUEVA = mina de tomas (manos en CDJ ~150, 540, 930, 1170, 1230, 1560 s; cara 600, 990, 1380 s; humo 180, 510, 1110 s; cuidado: 780 y 2010 tapa la cabeza). Los segundos de la hoja de contacto pueden correrse ±1 s: siempre mirar `revision.jpg`.
- 29/10: armador: `efecto: slam` + `antes_del_drop: seco` clipea el audio (pico 0 dB); `space-miami` con drop 7 dio «mudo en 0.0». Usar `go-back` + `filtro`.
- 29/10: los `textos` NO interpretan `<br>` (sale literal); sólo la portada. Un cartel no puede pisar la voz.
- 29/10: publicados 5 de formatos y largos distintos (9–22 s, drops 5–14). Medir el 01/11: promesa «3 segundos», timelapse, dato, POV, pregunta.
