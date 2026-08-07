# Robot de facturación — Bejerman Web (Paseo Nordelta / MAHNI MANAGEMENT)

Emite comprobantes en Bejerman Web manejando un Chrome real por CDP. **No guarda
credenciales**: Facu loguea a mano en la ventana que se abre.

## Cómo se levanta

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 \
  --user-data-dir=/tmp/chrome-bejerman --no-first-run --no-default-browser-check \
  "https://www.bejermanweb.com.ar/BW20180100/Home"
```

Facu loguea, entra a **Ventas → Facturación**, y recién ahí corre `emitir.js`.

```bash
node emitir.js '{"buscaCli":"SUSHINOR","pickCli":"000001","espCli":"SUSHINOR",
 "buscaTipo":"FC","pickTipo":"FC - Factura","espTipo":"Factura",
 "buscaConc":"008","pickConc":"008","espConc":"008",
 "desc":"Servicios y Expensas Julio 2026","precio":"992393","total":"1.200.795,53"}'
```

`grabar.js <archivo.log>` registra lo que hace Facu a mano (clicks + campos), para
descubrir pasos que todavía no sabemos automatizar.

## Datos fijos

- Emisor: MAHNI MANAGEMENT S.A. · CUIT 30-71901250-3 · **punto de venta 0002**
  (el 00001 es el portal de ARCA, no se usa desde Bejerman).
- Clientes: `000001` SUSHINOR S.A. (Fabric) · `000002` RODOLFO SRL (Bigg).
- Conceptos: **015** Alquileres (21%) · **008** Servicios y Expensas (21%) ·
  **EXE** para Recupero de gastos (sale como *Exento*).
- Descripciones: `Alquiler <Mes> <Año>`, `Servicios y Expensas <Mes> <Año>`,
  `Recupero de Gastos <Mes> <Año>`.
- El vencimiento **no se carga**: sale igual a la fecha de emisión (Cuenta Corriente a 0 días).
- Los importes salen de las Ctas Ctes, **redondeados al peso entero**.

## Trampas de esta app (costaron horas)

1. **Tipear "FC" y soltar elige sola la Factura de Crédito MiPyME (201)**, no la Factura A.
   Siempre elegir la opción por texto exacto y **releer el campo** para confirmar.
2. **Dos botones distintos comparten el id `sales-crud-add-button`**: el "Agregar" de la
   grilla de ítems y el "Agregar (alt+G)" que guarda. Hay que filtrar por texto.
3. **"Agregar" registra, "Emitir" emite.** Un comprobante en estado *Registrado* no tiene
   CAE y no es una factura válida.
4. El buscador de conceptos **devuelve resultados desfasados una consulta**. Hay que
   reintentar hasta ver la opción buscada; nunca aceptar la primera lista.
5. Los dropdowns dejan **overlays apilados** que tapan los campos siguientes: se enfoca por
   JS y se tipea con teclado real, y las opciones se clickean por evento sintético.
6. **La emisión puede fallar DESPUÉS de confirmar**, dejando un cartel de error y ningún
   comprobante. Nunca dar por emitido sin verificar; el chequeo bueno es bajar el PDF:
   `PROWEB/facturas/101838/0073/<TIPO> A0002-<NRO>.pdf` — 404 significa que no existe.

7. **Las Notas de Débito exigen período, y el campo NO es el que parece.** El modal de
   Datos Adicionales de una ND tiene **dos pares de fechas**:
   - `DatosAdic_Dscv_FECHADESDE` / `...FECHAHASTA` → *Fecha Desde/Hasta **Servicio***
   - `DatosAdic_Dscv_FECHADESDEPERIODO` / `...FECHAHASTAPERIODO` → *Fecha Desde/Hasta **Período***

   ARCA pide el **segundo**. Llenar el primero deja el formulario aparentemente completo y
   la emisión falla igual, con el mensaje *"Debe ingresar la Fecha Desde Período o
   seleccionar un comprobante asociado desde Datos Adicionales"*. Costó tres emisiones
   fallidas y se descubrió grabando a Facu hacerlo a mano. Las Facturas no piden período.

---

# El mes que viene: los 6 comandos

Cada mes se emiten **seis comprobantes**: el **alquiler del mes corriente** y el
**recupero + servicios comunes del mes ANTERIOR**, para Fabric y Bigg.

## Paso 1 — sacar los importes de las Ctas Ctes

Planilla `Ctas Ctes Paseo Nordelta - 2026` (`10BDmKvv2wY2M4lVYYab3NiNT04WLh5JjO-EhWI4tnNs`),
pestañas `Fabric` y `Bigg`. Se toma **el último bloque de cargos** (el que arranca después
del último saldo en 0). Los renglones que se facturan son:

| Renglón de la planilla | Va a |
|---|---|
| `Alquiler` | Factura A, concepto **015** |
| `Servicios comunes` | Factura A, concepto **008** |
| `Recupero de gastos` | Nota de Débito A, concepto **EXE** |
| `IVA Alquiler` / `IVA Servicios Comunes` | **no se cargan**: los calcula Bejerman |
| `Diferencia Alquiler (sin iva)` (sólo Bigg) | **NO se factura** — es la mitad en efectivo |

Los netos se cargan **redondeados al peso entero**. El total esperado es
`round(neto) * 1,21` para los del 21%, y el neto pelado para el recupero.

## Paso 2 — levantar Chrome y loguear

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1 \
  --user-data-dir=/tmp/chrome-bejerman --no-first-run --no-default-browser-check \
  "https://www.bejermanweb.com.ar/BW20180100/Home"
```

Facu loguea a mano (Bejerman cierra sesión todos los meses) y entra a
**Ventas → Facturación**. Recién ahí se corre el robot.

## Paso 3 — las 6 corridas

Cada una tarda ~100 s; conviene lanzarlas de a una y **verificar antes de la siguiente**.
Reemplazar mes, año e importes. `desde`/`hasta` **sólo** en las Notas de Débito.

```bash
B=.claude/skills/cierre-mes-nordelta/scripts/bejerman

# 1. Fabric — alquiler del mes corriente
node $B/emitir.js '{"buscaCli":"SUSHINOR","pickCli":"000001","espCli":"SUSHINOR",
 "buscaTipo":"FC","pickTipo":"FC - Factura","espTipo":"Factura",
 "buscaConc":"alq","pickConc":"015","espConc":"015",
 "desc":"Alquiler Septiembre 2026","precio":"<neto>","total":"<total>"}'

# 2. Fabric — servicios comunes del mes anterior
node $B/emitir.js '{"buscaCli":"SUSHINOR","pickCli":"000001","espCli":"SUSHINOR",
 "buscaTipo":"FC","pickTipo":"FC - Factura","espTipo":"Factura",
 "buscaConc":"008","pickConc":"008","espConc":"008",
 "desc":"Servicios y Expensas Agosto 2026","precio":"<neto>","total":"<total>"}'

# 3. Fabric — recupero del mes anterior (ND: LLEVA período)
node $B/emitir.js '{"buscaCli":"SUSHINOR","pickCli":"000001","espCli":"SUSHINOR",
 "buscaTipo":"ND","pickTipo":"ND - Nota de","espTipo":"Nota de d",
 "buscaConc":"exe","pickConc":"EXE","espConc":"EXE",
 "desc":"Recupero de Gastos Agosto 2026","precio":"<neto>","total":"<neto>",
 "desde":"01/08/2026","hasta":"31/08/2026"}'

# 4, 5 y 6 — igual, con "buscaCli":"RODOLFO","pickCli":"000002","espCli":"RODOLFO"
```

## Paso 4 — verificar (NO saltear)

**La emisión puede fallar después de confirmar.** No alcanza con que el robot diga
`CONFIRMADO`. Se baja cada PDF con la sesión del navegador y se chequea que tenga CAE:

```
https://www.bejermanweb.com.ar/BW20180100/PROWEB/facturas/101838/0073/FC%20A0002-000000NN.pdf
```

404 = no existe. Y antes de reintentar una emisión fallida, chequear que el número
siguiente dé 404 confirma que no se duplicó nada.

## Paso 5 — archivar

Los PDF van a `~/Desktop/Paseo Nordelta/Principio de mes/Facturas de Venta/2026/<Mes> <Año>/`
con los nombres que usa Facu: `Alquiler <mes> <año> FABRIC.pdf`,
`Servicios comunes <mes> <año> BIGG.pdf`, `Recupero de gastos <mes> <año> FABRIC.pdf`.
**Sólo copiar un PDF después de verificar que tiene CAE y que el total esperado figura adentro.**

## Si algo se comporta distinto a lo documentado

Correr `node grabar.js /tmp/registro.log`, pedirle a Facu que haga **un** comprobante a
mano, y leer el log. Registra cada click con el id del elemento y cada campo con su valor,
en todos los frames y todas las pestañas. Es lo que destrabó el bug de las Notas de Débito
después de tres emisiones fallidas.
