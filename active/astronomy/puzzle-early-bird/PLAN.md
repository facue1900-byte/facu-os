# OBSESSION (31/10/2026) — mail de early birds a la base de Puzzle

Estado 24/09/2026: **mail armado, nada enviado** (regla 10).

## El evento (leído de Planout el 24/09)

- OBSESSION · Palacio Alsina · sábado 31/10/2026 23:59 · flyer: **+27**
- Link: `https://planout.ar/eventos/es/comprarEvento?idEvento=1300&affId=FC`
- Early bird **$20.000 + $3.000** de gastos de gestión. VIP mujer +25 $50.000 + $7.500 ·
  VIP hombre +27 $70.000 + $10.500. Precio de la tanda siguiente: no publicado.

## El mail

- Template: `mail.html` + `obsession-banner.jpg` (va embebido en el mail, no linkeado).
- **Asunto:** `OBSESSION: ya se fue la mitad de los early birds`
- **Preheader:** `31/10 en Palacio Alsina. LA fiesta de Halloween. No lo dejes para el final.`
- Variables: `{{nombre}}` `{{link}}` `{{banner}}`.
- 🔴 "la mitad de los early birds" tiene que ser **cierto el día que sale**: se chequea en
  el panel de Planout antes de cada tanda.

## 🚨 La base de Puzzle y el +27

Base: `~/Desktop/Productoras/Puzzle/base_contactos_unificada PUZZLE.xlsx` (1.367 mails).

| Edad (col. "Edad aprox.") | Personas |
|---|---|
| Cumplen (mujer 25+, hombre 27+) | 128 (92 mujeres, 36 hombres) |
| Con edad y NO cumplen | 702 — de ellos **78 son menores de 18** |
| Sin edad | 537 |

La base de Puzzle es de 19 a 24 años; OBSESSION es +27. Pendiente de Facu: a quién se manda.

## Cómo se manda

1. Un mail por persona, nunca CCO masivo.
2. Script con `--send` apagado: sin el flag manda uno solo a Facu de prueba. Log por destinatario.
3. Menores de 18: **nunca**, decida lo que decida con el resto.
4. Las respuestas "baja" van a una lista de exclusión.
