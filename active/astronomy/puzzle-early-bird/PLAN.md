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

## Edad (decisión de Facu, 24/09)

El flyer y el mail dicen **+27** a propósito, para frenar a los más chicos. El corte real en
puerta es **+23 mujeres / +24 hombres** y se controla ahí. **No se aclara en ningún lado.**
Se manda a toda la base salvo **menores de 18 (78), que no reciben nunca**.
Tampoco se aclaran los $3.000 de gastos de gestión: el mail dice $20.000.

## Cómo se manda — `enviar.py`

- `--contar`: a cuántos le sale y quién queda afuera. Hoy: **1.289** (1.367 − 78 menores).
- Sin flags: una prueba a Facu. `--send`: tanda real de 450 (Gmail personal corta ~500/día)
  → **3 días**. Ordenado por cantidad de entradas compradas (el que trae grupo, primero).
- Sale de `facue1900@gmail.com` como "OBSESSION": la cuenta `studio` tiene el token roto.
- `enviados.csv` (gitignoreado) anota cada envío al instante: si se corta, se re-corre y sigue.
- Las respuestas "baja" se pegan en `bajas.txt`, una por línea.
- Saludo por nombre sólo si hay apellido (los usuarios de Instagram vienen sin): 1.175 con nombre.
