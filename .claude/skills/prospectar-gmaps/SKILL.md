---
name: prospectar-gmaps
description: Arma listas de negocios reales desde Google Maps (nombre, dirección, teléfono, web, rating) en un CSV para abrir en Sheets. Usar cuando Facu pida buscar candidatos a locatario para un local vacío del Paseo, venues o productoras para un evento, o proveedores/frigoríficos/transportistas de una zona.
allowed-tools: Bash, Read, Write
---

# Prospectar en Google Maps

Una búsqueda de Google Maps convertida en planilla. Sirve para armar la lista de
a quién llamar, no para mandarle nada a nadie.

## Estado

**Falta la key para que corra.** Necesita `APIFY_API_TOKEN` en el `.env`
(apify.com → Settings → API & Integrations). El parseo y el manejo de errores
están probados; el scrape real todavía no se corrió nunca.

Apify cobra por uso: **~USD 0,015 por listado**, o sea ~USD 1,50 cada 100. Tiene
free tier mensual. No lo corras en loop y decile a Facu cuánto va a salir antes
de pedir un límite alto.

## Para qué se usa acá

| Frente | Búsqueda tipo |
|---|---|
| Local vacío del Paseo | `gastronomía en Nordelta, Tigre` · `heladerías en zona norte GBA` — candidatos a locatario, con teléfono para llamar |
| Astronomy eventos | `salones de eventos en Tigre` · `productoras de eventos en CABA` — venues y socios nuevos |
| Campos / Chaco | `frigoríficos en Resistencia, Chaco` · `transporte de hacienda en Chaco` — proveedores y compradores |

## Cómo se corre

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/prospectar-gmaps/scripts/scrape_gmaps.py" \
  --buscar "gastronomía en Nordelta, Tigre" \
  --limite 30 \
  --salida "/Users/Facu/facu-os/data/prospectos/gastro-nordelta.csv"
```

| Flag | Qué hace |
|---|---|
| `--buscar` | Qué y **dónde**. La zona va adentro de la búsqueda. |
| `--limite` | Máximo de listados. Cada uno cuesta plata. Default 20. |
| `--salida` | CSV. Va a `data/prospectos/` (gitignoreado). |
| `--json` | Opcional, guarda la respuesta cruda por si falta un campo. |

## Reglas

- **La zona va en la búsqueda.** `"heladerías"` solo devuelve cualquier cosa;
  `"heladerías en Nordelta, Tigre"` devuelve lo que sirve. Si vuelven cero
  resultados, el script corta: es la query, no el mercado.
- **Esto no contacta a nadie.** Sale un CSV y ahí termina. Cualquier mail o
  WhatsApp a esta lista se prepara aparte y se frena hasta que Facu diga que sí.
- **Los datos de Google Maps envejecen.** Teléfonos viejos, locales cerrados,
  webs caídas. Antes de pasarle la lista a un tercero, verificá una muestra.
- **Nada de enriquecer con LLM.** La versión de la que salió esto le pedía a un
  modelo que sacara "el email del dueño" scrapeando la web. Eso inventa datos.
  Acá sale lo que Google Maps publica y nada más.
