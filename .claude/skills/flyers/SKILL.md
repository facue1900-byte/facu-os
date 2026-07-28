---
name: flyers
description: Genera tandas de flyers en PNG listos para Instagram (feed, story y cuadrado) para los productos de Astronomy Academy — Curso de DJ, producción presencial, producción online, membresías y Modo Profesional. Usar cuando Facu pida "flyers", "placas", "creativos para pauta", "algo para postear del curso/las membresías", o cuando cambie un precio y haya que rehacer las piezas.
---

# flyers

Un producto × N ángulos de venta × M formatos, generados de una. El copy vive en
`contenido/academy.json`, los precios salen de la base de la app, y la estética
usa los mismos tokens de color que `astronomyofficial.com`.

## Correr

Siempre en dos pasos, y en este orden:

```bash
# 1. Refrescar precios contra la fuente de verdad (tabla `plans` de Supabase)
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/flyers/scripts/sync_precios.py"

# 2. Generar
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/flyers/scripts/generar_flyers.py"
```

Sale todo a `~/Desktop/Productoras/Astronomy/Flyers Academy/<estilo>/<producto>/<angulo>__<formato>.png`,
más una `_hoja-de-contacto.jpg` por estilo para revisar las piezas de un vistazo.

Filtros útiles cuando cambia una sola cosa:

```bash
--estilo foto|plano                 # default: foto
--productos membresias,curso-dj     # solo esos productos
--angulos precio                    # solo el ángulo de precio
--formatos story                    # solo 1080x1920
```

## Los dos estilos

| Estilo | Qué es | Cuándo |
|---|---|---|
| `foto` (default) | Foto del estudio a sangre + velo + firma cursiva. | **Instagram (@astronomy.academy).** Es la estética propia de Academy: estudio oscuro, luz violeta, el neón con la firma. |
| `plano` | Degradado violeta sobre negro + isotipo estrella. | La app y el sitio (astronomyofficial.com), donde manda el sistema de diseño del producto. |

El velo del estilo `foto` va en tres tramos (oscuro arriba y abajo, transparente en
el medio) y el tinte violeta va en **`soft-light`, nunca `screen`**: con `screen` se
levantan los negros y la foto queda como una sopa violeta plana. Las fotos del
estudio ya tienen luz violeta sobre negros profundos; el tinte solo unifica
temperaturas entre tomas.

Las fotos viven en `assets/fotos/` y se asignan por producto en `academy.json`
(campo `foto`). Vinieron de `~/Desktop/Productoras/Astronomy/Astronomy Academy/Material para contenido/`,
reescaladas a 1800px de lado largo.

## Qué hay adentro

| Archivo | Qué es |
|---|---|
| `contenido/academy.json` | Productos, ángulos y copy. **Es lo único que se edita para cambiar textos.** |
| `contenido/precios.json` | Snapshot de la tabla `plans`, con fecha. Lo escribe `sync_precios.py`. |
| `templates/flyer.html` | La estética. Tokens copiados de `app/globals.css` de astronomy-members. |
| `assets/marca/` | Isotipo, logotipo y **firma cursiva** (`academy-blanco.png`, la del neón del estudio). |
| `assets/fotos/` | Fotos del estudio para el estilo `foto`. |
| `assets/fonts/` | Montserrat variable. |

**Productos** (5): `curso-dj`, `produccion`, `produccion-online`, `membresias`,
`modo-profesional`.
**Ángulos** (5 por producto): `precio`, `beneficios`, `profe`, `como-funciona`, `cta`.
**Formatos** (3): `feed` 1080×1350 · `story` 1080×1920 · `square` 1080×1080.

Total por tanda completa: **75 piezas**.

## Los precios no se escriben a mano

`precio_ars` en `academy.json` lo pisa `sync_precios.py` leyendo la tabla `plans`
de Supabase — la misma que lee el checkout. Un flyer con precio viejo se publica,
alguien lo compara con Mercado Pago y no coincide.

Si un producto no tiene precio propio en la base (`produccion`, `produccion-online`),
va `precio_ars: null` y su ángulo de precio muestra el costo en **créditos**, que sí
está verificado. El script revienta si un ángulo de tipo `precio` se encuentra con un
`precio_ars` nulo: prefiere no generar antes que generar con el precio en blanco.

`modo-profesional` es la excepción: su precio está hardcodeado en
`app/actions/buyCursoPro.ts` (`PRECIO_UNICO`, `PRECIO_CUOTA`), no en la base. Si allá
cambia, hay que actualizarlo a mano acá.

## Verificación

Ninguna pieza se da por buena porque Chrome no tiró error. De cada PNG se chequea:

- que las dimensiones sean exactamente las del formato;
- que pese más de 40 KB (menos que eso es una placa vacía: el render se colgó antes
  de pintar el texto);
- que el texto **no haya desbordado**. El template mide el alto real y achica la
  tipografía hasta que entra; deja el veredicto en el `<title>` y el script lo lee
  del DOM en la misma corrida de Chrome. Si ni al 62% entra, la pieza se reprueba y
  el script sale con error.

Una tanda con aunque sea una pieza mala termina en exit 1. No exporta 74 buenas y
una rota en silencio.

## Lecciones

- **`--user-data-dir` cuelga al Chrome de macOS.** Con un perfil nuevo en `/tmp` el
  proceso se queda esperando para siempre, sin escribir el PNG ni tirar error — ni
  agregando `--no-first-run --no-default-browser-check --disable-sync`. Sin el flag
  anda, y cinco corridas en paralelo dan PNGs byte a byte idénticos. No volver a
  agregarlo "por prolijidad".
- **`timeout` no existe en macOS**, así que no sirve para acotar un render colgado.
  El corte va en el `subprocess.run(timeout=...)` de Python.
- El auto-ajuste del template es la razón por la que se puede escribir copy sin
  contar caracteres. Si una pieza sale con la tipografía notoriamente más chica que
  sus hermanas, el copy es demasiado largo — acortarlo en vez de subir el piso
  del 62%.
