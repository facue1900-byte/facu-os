# Puzzle — mail de early birds a la base

Estado 24/09/2026: **mail y plan armados, nada enviado** (regla 10). Faltan los datos de
la fecha para completar el mail.

## Base

`~/Desktop/Productoras/Puzzle/base_contactos_unificada PUZZLE.xlsx`, hoja `Unificada`
(armada el 01/09 a partir de las fechas de abril 490638 y junio 514816 de Passline).

| | |
|---|---|
| Personas | 1.367 |
| Mail válido y único | 1.367 |
| Con nombre usable para el saludo | 1.254 (el resto: "Hola," a secas) |
| Compraron 2+ entradas | 384 — los que traen grupo |
| Con teléfono | 852 |

## El mail

- Template: `mail.html` (HTML de tablas con estilos inline, anda en Gmail/iPhone/Outlook).
- **Asunto:** `Puzzle vuelve: early birds antes que nadie`
- **Preheader:** `Antes que nadie y al mejor precio. Hasta el {{fecha_corte}} o hasta que se agoten.`
- Variables: `{{nombre}}` `{{fecha}}` `{{lugar}}` `{{precio_eb}}` `{{precio_general}}`
  `{{cupo}}` `{{fecha_corte}}` `{{link}}`.

## Cómo se manda

1. **Un mail por persona, nunca CCO masivo.** CCO con 1.367 va directo a spam.
2. **Tandas de 450 por día, 3 días.** Gmail corta a los ~500/día en una cuenta común y
   un pico de golpe quema la reputación del remitente.
3. **Orden por intención:** día 1 los de 2+ entradas (384) + los primeros de 1 entrada;
   días 2 y 3 el resto. El que trae grupo es el que más vende.
4. Script con `--send` apagado por defecto: sin el flag, arma los mails y se manda
   **uno solo a Facu** de prueba. Log de a quién salió cada uno, para no repetir si se corta.
5. Las respuestas "baja" se anotan en una lista de exclusión antes de cualquier envío futuro.

## FOMO sin inventar

- El cupo y la fecha de corte del mail tienen que ser **reales**.
- Recordatorio a los 4-5 días **sólo a los que no compraron** (se cruza con el export de
  Passline / la ticketera): "quedan X early birds", con X leído del panel ese día.

## Lo que falta para ejecutar

- Fecha y lugar · precio early bird y precio siguiente · cantidad de early birds ·
  fecha de corte · link de compra (Passline o la ticketera propia).
- Desde qué cuenta sale (ver recomendación en el chat).
