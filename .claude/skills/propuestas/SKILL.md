---
name: propuestas
description: Genera una propuesta comercial prolija en HTML y PDF — para inversores del Paseo, candidatos a locatario, venues o productoras de Astronomy, o cualquier tercero. Usar cuando Facu pida "armame una propuesta", "un quote", "algo para mandarle a", "una carpeta para el inversor/locatario/venue". El documento se genera y SE FRENA: no se manda nada.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Propuestas

Porta el `create-proposal` del curso, sin PandaDoc: acá el documento se arma local
(HTML → PDF con Chrome headless, sin abrir ventanas) y **no se manda** — se le
entrega el archivo a Facu y él decide.

El reparto de trabajo es el de siempre: **yo escribo el contenido** (problemas,
beneficios, propuesta de valor — eso es criterio), **el script arma el documento**
(template, estilos, PDF — eso es código).

## Los destinatarios se configuran, no se hardcodean

`destinatarios.json`, al lado de este archivo, define cada tipo de destinatario:
tono, qué secciones lleva, y qué NO decir. Hoy están: `inversor-paseo`,
`locatario-paseo`, `venue-astronomy`, `productora-astronomy`, `generico`.
Si aparece un tipo nuevo (un frigorífico, un sponsor), se agrega ahí.

## Flujo

**1. Juntar la información.** De lo que diga Facu, de una grabación (usar
`grabacion-a-tareas` si hay audio) o de los archivos del negocio. Lo que falte y
sea crítico, **se pregunta** — especialmente montos. Los números de plata salen
de la fuente (sheet, contrato, factura), nunca de una estimación mía.

**2. Escribir el contenido** en un JSON (ver `ejemplo_contenido.json` el formato):
título, para/de, intro, secciones (problema → propuesta → beneficios), inversión
como lista de ítems con monto y moneda, y cierre. Guardarlo en
`.tmp/propuestas/<slug>.json`. Seguir el tono del destinatario según
`destinatarios.json`.

**3. Armar el documento:**

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/propuestas/scripts/armar_propuesta.py" \
  --contenido /Users/Facu/facu-os/.tmp/propuestas/<slug>.json \
  --salida "/Users/Facu/facu-os/data/propuestas/<slug>" \
  --pdf
```

Genera `<slug>.html` y (con `--pdf`) `<slug>.pdf`. Sin Chrome instalado, `--pdf`
falla con mensaje claro y queda el HTML.

**4. Frenar.** Mostrarle a Facu el path del PDF y un resumen de qué dice. **No se
manda por ningún canal.** Si Facu pide cambios, se edita el JSON y se regenera.

## Reglas

- **Montos**: el script NO suma ni calcula. Si el JSON trae `total`, el script
  verifica que coincida con la suma de los ítems de la misma moneda y **corta si
  no coincide** — un total que no cierra no sale en un PDF con el nombre de Facu.
- Si un dato de plata no está confirmado, va marcado "(a confirmar)" en el
  documento, no inventado.
- Monedas: ARS y USD no se mezclan en un mismo total. Si la propuesta cruza
  monedas, decir con qué tipo de cambio y de cuándo.
- El PDF se genera con Chrome **headless** — nunca abrir una ventana.

## Lecciones cargadas

- El skill original del curso mandaba la propuesta directo por la API de PandaDoc.
  Acá eso se cortó a propósito: nada sale al mundo sin el OK de Facu.
