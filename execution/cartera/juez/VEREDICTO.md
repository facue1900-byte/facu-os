# Veredicto de las carpetas cripto — 2026-10-29 06:55 UTC

**En una línea:** va ganando Laboratorio (+0,26%, 1 día y una sola operación), la única arriba de USDT y de HODL BTC (-0,91%). 3 niveles (-9,08%) y Agresiva (-9,21%) llevan 21 días perdiendo contra 0% de USDT y ~-3,8% de HODL BTC. Nada con historia le gana a quedarse quieto.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 909.17 | -9.08% | -5.27 pp (HODL -3.81%) | -0.47% (HODL -0.84%) | -2.78% (HODL -3.15%) | -10.42% (HODL -6.10%) | 2.39 USD (2.6% de la pérdida) | 85 |
| Agresiva | 907.89 | -9.21% | -5.50 pp (HODL -3.72%) | -0.43% (HODL -0.99%) | -2.95% (HODL -2.95%) | -9.21% (HODL -6.27%) | 28.89 USD (31.4% de la pérdida) | 216 |
| Laboratorio | 1002.60 | +0.26% | +1.17 pp (HODL -0.91%) | +0.26% (HODL -0.91%) | falta (arrancó 27/10) | -0.82% (HODL -2.07%) | 0.20 USD (7.7% de la ganancia) | 1 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo | — | falta (no arrancó) | — | — | — | — | — | — |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37; DCA tiene un solo snapshot, 22:38).
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 22/10 06:07, Agresiva 22/10 06:32).
- **Frescura:** 3 niveles 06:08, Agresiva 06:32, Laboratorio 06:17 UTC (todas < 1 h). DCA 27/10 22:38 (32 h; corre los lunes, límite 8 días). Torneo: último ciclo 04:41 UTC (2,2 h, límite 8 h). Todas corren.
- **DCA:** su valor y su HODL son del 27/10 (no tiene snapshots entre cuotas); no refleja la baja de BTC desde entonces.
- **Torneo:** arrancó el 29/10 pero todavía no cerró ninguna vela de 4 h desde el inicio (última 00:00 UTC), así que no hay `vivo.json`: no hay líder ni conteo contra USDT/HODL que dar. No es falla: corre y espera la vela.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- Peor caída sobre `total_usd` del `historial.csv` (capital inicial como primer máximo); HODL BTC con su propia columna. Comisiones y ops del `libro.json` (la suma por operación coincide con `comisiones_usd` en las cuatro).

## Qué pasó desde ayer

- **3 niveles:** -0,61% en 24 h (914,74 → 909,17), siguiendo a BTC. Sin operaciones desde el 24/10; 316 USD en USDT. Sigue -9,7% desde su máximo de 1.006,50.
- **Agresiva:** -1,41% en 24 h (920,84 → 907,89). Ocho operaciones: dos stops de PEPE (16:46 -3,08% y 02:29 -2,55%) y una salida de ZEC (-0,89%); a las 04:32 entró en BTC y ETH (200 USD cada uno) y a las 05:32 volvió a PEPE (150 USD). Comisiones ya en 28,89 USD: casi un tercio de lo que pierde.
- **Laboratorio:** de 996,20 (28/10 04:16) a 1.002,60: +0,64%. Tocó récord (1.003,80) a las 00:17 y bajó. Sigue con su única operación (PEPE 200 USD a 4,99e-06). Ahora le gana a HODL BTC del mismo período por 1,17 pp.
- **DCA BTC:** sin cambios; próxima cuota el lunes 02/11.
- **Torneo:** sin resultados todavía (ver nota).
- **Alarmas:** ninguna. Ningún récord en el último snapshot (Laboratorio está debajo de su máximo de 1.003,80) y ninguna carpeta cerca de +20%. No se mandó mail.

## Recomendación

- **3 niveles — apagar.** 21 días (≥14), -9,08% contra 0% de USDT y -3,81% de HODL BTC; en 7 días -2,78%: pierde menos que HODL (-3,15%) pero sigue perdiendo, no mejoró. Lo decide Facu.
- **Agresiva — apagar.** 21 días, -9,21% contra 0% y -3,72% de HODL. En 7 días -2,95%, igual que HODL: no mejoró. 28,89 USD en comisiones en 216 operaciones: 2,9 de los 9,2 puntos que pierde. Lo decide Facu.
- **Laboratorio — seguir.** +0,26% le gana a USDT y a HODL BTC, pero con 1 día y una operación es suerte de PEPE, no evidencia. Se juzga con historia.
- **DCA BTC — seguir.** Una cuota; es la referencia barata contra la que se miden las otras.
- **Torneo — seguir.** Todavía no empezó a medir.

**¿Key real de Binance?** Hoy, claramente no (la sección formal arranca el 07/11/2026). Las dos carpetas con 21 días pierden contra USDT y contra HODL BTC; la única positiva tiene un día.
