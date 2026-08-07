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

## PENDIENTE

Las **Notas de Débito** exigen período: *"Debe ingresar la Fecha Desde Período o
seleccionar un comprobante asociado desde Datos Adicionales"*. Cargar las fechas en el
modal de Datos Adicionales y aceptar **no alcanza** — sigue rechazando. Falta descubrir
qué hace Facu a mano que el robot no reproduce. Las Facturas no tienen este problema.
