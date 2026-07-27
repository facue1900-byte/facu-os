# Campos — Chaco y Pergamino

Última actualización: 2026-07-27

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

`~/Desktop/Chaco/` — **650 archivos** (646 PDFs de guías de traslado + 4 xlsx).
Nomenclatura de los PDFs: `<cantidad y categoría> <Origen> - <Destino> (DD:MM:AAAA).pdf`
(ej. `100 vacas Fortin Cocherek - El Colmena (16:03:2025).pdf`).

Por año: 2022 (2) · 2023 (158) · 2024 (121) · 2025 (115) · 2026 (92 hasta julio).

Campos que aparecen como origen o destino: **La Brava** (178), **La Camila** (162),
**El Sabalo** (123), Cañada Rica, El Colmena, Agua Viva, Fortín Cocherek, La Magdalena,
Patroncito, Talabera, La Horquilla, La Victorina, El Galicia.

## Automatizaciones que quiere Facu

1. Conteos y negociaciones.
2. Precio de la carne del día: cuándo vender, a cuánto el kilo, qué % de desbaste, y qué
   conviene según todo eso junto.
3. Cuándo conviene vender una jaula de 32 novillos o 32 vacas.

## Oportunidad ya cuantificada

Esos 650 PDFs son **cuatro años de movimientos de hacienda ya registrados** y nadie los
lee. Un parser de nombres de archivo (sin abrir un solo PDF) daría el histórico de qué
salió de qué campo, cuándo y cuánto — la base para los tres puntos de arriba. Es el
próximo candidato a skill después de que `cierre-mes-nordelta` esté rodando.

## Pendiente de dato

- Volumen de hacienda y con qué frigoríficos se opera.
- De dónde sale el precio de referencia del kilo (frigorífico directo, Rosgan, WhatsApp
  de un consignatario). Sin esto no hay skill de precios.
- Situación de Pergamino, que hoy casi no se toca.
