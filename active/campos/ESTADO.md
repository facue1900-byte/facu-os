# Campos — Chaco y Pergamino

Última actualización: 2026-08-14

## Qué es

Campos de la familia. Hoy el trabajo es casi todo **Chaco**, en la parte operativa:
papeleo de SENASA para traslado de jaulas, venta de vacas y novillos a frigoríficos,
autorizaciones de venta y pases de provincia.

**Objetivo real: eficientizar el tiempo del viejo de Facu.**

## Restricción del contexto (define toda solución)

Chaco es una zona muy pobre. Conectividad mala, poca tecnología en el campo, y gente que
no va a usar una app complicada. **WhatsApp, papel y planillas simples** antes que
cualquier sistema que requiera entrenamiento. Una solución que necesita capacitación ya
falló.

## Dónde está todo

`~/Desktop/Chaco/`. **Ordenado el 14/08/2026** — los 650 PDFs estaban sueltos en una
sola carpeta y ahora están separados por tipo:

| Carpeta | Qué hay |
|---|---|
| `Guias de traslado/<año>/` | **540 guías** de SENASA, por año |
| `Reportes historicos/` | **108** reportes de stock e históricos por campo — no son movimientos |
| `Otros/` | 2 PDFs que no son del campo (`Comunicado IMPORTANTE`, `Crew Passport`) |
| raíz | `stock_ganadero.xlsx` y `RENSPA ESTEVEZ por campo.xlsx` |

Nomenclatura de los PDFs: `<cantidad y categoría> <Origen> - <Destino> (DD:MM:AAAA).pdf`
(ej. `100 vacas Fortin Cocherek - El Colmena (16:03:2025).pdf`).

**Guías por año:** 2022 (61) · 2023 (152) · 2024 (104) · 2025 (124) · 2026 (99).

De las 540, **474 traían la fecha en el nombre y 66 no**: esas se dataron por fecha de
modificación del archivo, que se verificó contra las 504 que sí la tienen y coincide en
**502 (99,6%)**. Casi todas las sin fecha son de 2022, cuando todavía no existía la
convención de nombres. **Un parser nuevo tiene que recorrer recursivo**, no `Chaco/*.pdf`.

**Los 646 nombres ya están parseados** (27/07/2026). El conocimiento permanente quedó en
`~/Obsidian/facu-vault/wiki/campo/` — seis notas. Lo esencial:

- **Once campos propios**, todos con RENSPA `05.023.x`. **El Galicia y El Colmena son
  campos, no compradores** (aparecen como destino igual que un frigorífico).
- **Stock: 10.114 cabezas** (`stock_ganadero.xlsx`): 5.053 vacas · 2.212 novillitos ·
  1.810 vaquillonas · 399 novillos.
- **La jaula son 32 cabezas**: 189 de 358 salidas son exactamente 32; el 85% cae entre 30
  y 36. Vender es una decisión discreta — la pregunta es "¿está la jaula completa?".
- **Dos canales**: novillo sale por **La Camila** (158 guías), vaca por **El Sábalo** (104).
  La Rural y Frinea compran solo vaca; Talabera solo macho.
- **La Brava concentra el riesgo**: 159 guías y 5.097 cabezas, más de la mitad de todo.
  El segundo (Agua Viva) tiene 35. Frigorífico en Corrientes, CUIT 30-70781069-2.

~~Ojo: `Lista 22 de Julio AUTOGESTIONADOS.xlsx` está traspapelado en `~/Desktop/Chaco/`~~
→ **movido el 14/08/2026** a `~/Desktop/Productoras/Astronomy/Eventos/Barra/`. Es la
lista de precios de whisky de la barra de eventos. **Falta confirmar si es de Astronomy
o de Puzzle**; quedó en Astronomy por descarte.

## IVA de Sucesores de Ricardo Estevez — 11/08/2026

Link para cargar facturas A por foto y que el IVA se anote solo en una planilla,
separando neto de IVA, para netear compras contra ventas y saber cuánto pagar.
Vive en `~/Desktop/Chaco/App IVA Estevez/` (repo git propio, ver su `README.md`).

**Arranca de cero: no hay ninguna factura cargada todavía.** Empieza en agosto 2026.

| | |
|---|---|
| Planilla | `1YD0-ujMDjmcM9cJ6Omf3L_ZWlEdLB69mP3fXcF4Tcz4` (creada, con Config, Resumen IVA y la hoja 2026-08) |
| Backend | Apps Script dentro de la planilla — **falta desplegarlo** |
| Pantalla | `web/` verificada, y `apps-script/Pantalla.html` como alternativa sin hosting |
| Sitio Netlify | `iva-estevez-chaco` creado, **sin deployar** |

**Bloqueante: falta el CUIT de la empresa.** Sin ese dato el sistema no puede saber
si un comprobante es compra o venta —lo deduce del CUIT, no se marca a mano— ni si
la factura es de la empresa. Frena todo lo que llega. Va en la hoja `Config`.

Decisiones que ya están tomadas y probadas: el modelo transcribe y el código
calcula; nada entra al cálculo del IVA sin que una persona lo confirme; las
percepciones van aparte porque no son crédito fiscal; sólo las facturas A pasan.

## Automatizaciones que quiere Facu

1. Conteos y negociaciones.
2. Precio de la carne del día: cuándo vender, a cuánto el kilo, qué % de desbaste, y qué
   conviene según todo eso junto.
3. Cuándo conviene vender una jaula de 32 novillos o 32 vacas.

## Oportunidad ya cuantificada

Esas 540 guías son **cuatro años de movimientos de hacienda ya registrados** y nadie los
lee. Un parser de nombres de archivo (sin abrir un solo PDF) daría el histórico de qué
salió de qué campo, cuándo y cuánto — la base para los tres puntos de arriba. Es el
próximo candidato a skill después de que `cierre-mes-nordelta` esté rodando.

## Pendiente de dato

- ~~Volumen de hacienda y con qué frigoríficos se opera~~ → **resuelto 27/07/2026**, arriba.
- **SENASA: no está documentado el paso a paso del DT-e.** Facu preguntó si se puede operar
  ARCA/SENASA desde acá: **no se puede** — no hay browser automation instalada, ni
  certificado digital, ni credenciales en el `.env`, y ARCA pide Clave Fiscal con 2FA.
  Pendiente: investigar el trámite contra la fuente oficial y dejar checklist verificado, y
  averiguar si existe web service de ARCA/SENASA para DT-e.
- Kilos, precio por kilo, desbaste y criterio de cuándo vender: **no están en ningún
  archivo**. Las guías son sanitarias, no comerciales. Ver `wiki/campo/que-falta-saber-del-campo`.
- De dónde sale el precio de referencia del kilo (frigorífico directo, Rosgan, WhatsApp
  de un consignatario). Sin esto no hay skill de precios.
- Situación de Pergamino, que hoy casi no se toca.
