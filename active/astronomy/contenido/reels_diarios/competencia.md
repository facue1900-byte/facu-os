# Competencia — qué suben otras academias y estudios de DJ

El agente diario la mantiene: cuenta → qué formatos les rinden (fecha + números). Se suman
cuentas nuevas cuando aparecen.

## 09/11/2026 — qué datos de otras cuentas se pueden leer (probado)
- `yt-dlp` por reel suelto SÍ trae likes, comentarios y fecha, sin login: Point Blank `DezOZjKFaFZ` 242/24 y `DeuJb8gDmXs` 186/8. Vistas NO.
- `yt-dlp` por perfil NO lista los reels (`Unsupported URL` en `/reels/`, `Unable to extract data` en el perfil).
- API oficial `business_discovery`: con el token de Instagram, campo inexistente; con `META_ACCESS_TOKEN`, error 10 (la app no tiene permiso).
- Rankear contra la mediana de cada cuenta se puede con likes + comentarios, si se consigue la lista de links por otro lado.

## 28/10/2026 — primer intento, SIN datos
- WebSearch «escuela de DJ instagram reels Point Blank / Crossfader»: nada útil (sólo notas genéricas).
- WebFetch de `instagram.com/pointblankmusicschool/`: la página trae links de reels (ej. DezOZjKFaFZ 22/10,
  DeuJb8gDmXs 20/10) pero **sin captions, likes ni vistas**. No se pudo medir qué les rinde.
- Único caso de escuela de DJ con número: Table Tutors (Vancouver), reel de un policía DJ en un colegio, +36.000 vistas
  (dailyhive.com, sin fecha confirmada). Formato: persona inesperada tocando.
- Cuentas a probar mañana: @pointblankmusicschool (reels de arriba, abrir cada uno), @crossfaderdjschool, @adsrmusic, @pyramindtrainingcenter.
