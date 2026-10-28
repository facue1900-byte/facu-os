# Veredicto de las carpetas cripto — 2026-10-28 06:52 UTC

**En una línea:** ninguna carpeta le gana a quedarse quieto. 3 niveles (-8,53%) y Agresiva (-7,92%) pierden en 20 días contra -3,03% / -2,77% de HODL BTC y 0% de USDT. Laboratorio (-0,82%) y DCA (-0,01%) tienen horas de vida: todavía no dicen nada.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 914.74 | -8.53% | -5.50 pp (HODL -3.03%) | +0.14% (HODL -0.04%) | -3.72% (HODL -2.27%) | -10.42% (HODL -6.10%) | 2.39 USD (2.8% de la pérdida) | 85 |
| Agresiva | 920.84 | -7.92% | -5.15 pp (HODL -2.77%) | +0.99% (HODL -0.02%) | -1.62% (HODL -2.30%) | -9.08% (HODL -6.27%) | 27.36 USD (34.6% de la pérdida) | 208 |
| Laboratorio | 991.79 | -0.82% | -1.02 pp (HODL +0.20%) | -0.82% (HODL +0.20%) | falta (arrancó 27/10) | -0.82% (HODL -0.15%) | 0.20 USD (2.4% de la pérdida) | 1 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | 0.00% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC (arranque de Laboratorio y DCA). Base: el último snapshot de cada carpeta en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). Lleva ~8 h: sirve recién en unos días.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 21/10 04:07, Agresiva 21/10 06:32).
- **Frescura:** 3 niveles 06:06, Agresiva 06:32, Laboratorio 06:20 UTC (todas < 1 h). DCA 27/10 22:38 (8,2 h; corre los lunes, límite 8 días). Todas corren.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- Peor caída sobre `total_usd` del `historial.csv`; HODL BTC con su propia columna en el mismo historial. Comisiones y ops del `libro.json` (la suma por operación coincide con `comisiones_usd` en las cuatro).

## Qué pasó desde ayer

- **3 niveles:** +1,06% en 24 h (905,16 → 914,74), siguiendo a BTC. Sin operaciones desde el 24/10; 316 USD en USDT. Sigue -9,1% desde su máximo de 1.006,50.
- **Agresiva:** +0,80% en 24 h (913,49 → 920,84). Seis operaciones: compró ZEC, NEAR y PEPE (200 USD cada una); vendió NEAR (197,72, -2,28) y PEPE en dos tomas (107,89 + 103,80 = 211,69, +11,69 bruto). Queda con ZEC y 722 USD en USDT. Le ganó a HODL en la ventana común y en 7 días, pero nunca superó los 1.000 USD iniciales y las comisiones ya son el 35% de su pérdida.
- **Laboratorio:** primera operación: compró PEPE por 200 USD (02:16 UTC), hoy -0,82% contra +0,20% de HODL. 800 USD en USDT.
- **DCA BTC:** sin cambios; próxima cuota el lunes.
- **Alarmas:** ninguna. Ninguna carpeta está por encima de su capital inicial (no hay récord) ni cerca de +20%. No se mandó mail.

## Recomendación

- **3 niveles — apagar.** 20 días (≥14), -8,53% contra 0% de USDT y -3,03% de HODL BTC; 7 días -3,72% contra -2,27% de HODL, tampoco mejoró. Lo decide Facu.
- **Agresiva — apagar.** 20 días, -7,92% contra 0% y -2,77% de HODL; 7 días -1,62% (perdió menos que HODL, -2,30%, pero sigue perdiendo: no mejoró). 27,36 USD en comisiones en 208 operaciones: casi 3 puntos de los 8 que pierde. Lo decide Facu.
- **Laboratorio — seguir.** Horas de vida, una operación. Se juzga con historia.
- **DCA BTC — seguir.** Horas de vida; es la referencia barata contra la que se miden las otras.

**¿Key real de Binance?** Hoy, claramente no (la sección formal arranca el 07/11/2026). Ninguna carpeta le gana ni a USDT desde su inicio.
