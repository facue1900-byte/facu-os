# Veredicto de las carpetas cripto — 2026-10-29 12:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse quieto: 3 niveles (-9,22%) y Agresiva (-9,20%) pierden contra 0% de USDT y ~-4% de HODL BTC; Laboratorio cayó a -0,32% (le gana a HODL, no a USDT). Lo único arriba de USDT es la líder del Torneo (HODL 50/50 BTC-ETH, +0,25% en 12 h), que no es evidencia de nada.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 907.80 | -9.22% | -5.18 pp (HODL -4.04%) | -0.62% (HODL -1.08%) | -1.91% (HODL -2.16%) | -10.42% (HODL -6.10%) | 2.39 USD (2.6% de la pérdida) | 85 |
| Agresiva | 908.01 | -9.20% | -5.48 pp (HODL -3.72%) | -0.42% (HODL -0.99%) | -2.94% (HODL -2.17%) | -9.70% (HODL -6.27%) | 29.34 USD (31.9% de la pérdida) | 219 |
| Laboratorio | 996.80 | -0.32% | +0.54 pp (HODL -0.86%) | -0.32% (HODL -0.86%) | falta (arrancó 27/10) | -0.82% (HODL -2.07%) | 0.60 USD (18.7% de la pérdida) | 3 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder P2 HODL 50/50 BTC-ETH | 1002.46 | +0.25% (12 h) | +0.16 pp (P1 HODL BTC +0.09%) | falta (arrancó 29/10 00:00) | falta | -0.28% | 1.00 USD | 2 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37; DCA tiene un solo snapshot, 22:38). El Torneo arrancó después, no entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 22/10 12:11, Agresiva 22/10 11:32).
- **Frescura (ahora 12:53 UTC):** 3 niveles 12:27, Agresiva 12:39, Laboratorio 12:18 (todas < 1 h). DCA 27/10 22:38 (38 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 12:45, última vela 12:00 (límite 8 h). **Todas corren.**
- **Torneo:** 33 estrategias, 12 h de vida. Le ganan a USDT 3 de 33 (P2, P1, P4); a USDT **y** a HODL BTC (P1, +0,09%) sólo 1 de 33 (P2). 29 siguen en 1.000 sin operar. Ojo: el campo `hodl_btc` de `vivo.json` dice -1,44%, que no coincide con P1 HODL BTC (+0,09%) del mismo período; tomé P1 como HODL, igual que el `RESUMEN.md` del torneo. Conviene revisar ese campo.
- **DCA:** su valor y su HODL son del 27/10 (no tiene snapshots entre cuotas); no refleja la baja de BTC desde entonces.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- Peor caída sobre `total_usd` del `historial.csv` (capital inicial como primer máximo); HODL BTC con su propia columna. Comisiones y ops del `libro.json` (la suma por operación coincide con `comisiones_usd` en las cuatro).

## Qué pasó desde ayer

- **3 niveles:** -0,75% en 24 h (914,66 → 907,80), siguiendo a BTC. Sin operaciones desde el 24/10; 316 USD en USDT. -9,8% desde su máximo de 1.006,50.
- **Agresiva:** -1,45% en 24 h (921,33 → 908,01). Nueve operaciones: tres salidas de PEPE en pérdida (16:46 -3,08%, 02:29 -2,55%, 08:32 -3,54%), entradas en BTC y ETH (04:32), HYPE (11:33) y BNB (12:39). Comisiones 29,34 USD: casi un tercio de lo que pierde.
- **Laboratorio:** de 1.000,20 (28/10 10:17) a 996,80: -0,34%. Tocó récord (1.003,80) a las 00:17 y bajó; a las 10:18 vendió PEPE con -1,2% (tendencia rota) y a las 12:18 compró HYPE (199 USD). Ya no le gana a USDT.
- **DCA BTC:** sin cambios; próxima cuota el lunes 02/11.
- **Torneo:** primer `vivo.json`. Tras 12 h, sólo las tres que compraron BTC/ETH de entrada están arriba; P3 (canasta BTC/ETH/BNB) -0,07%.
- **Alarmas:** ninguna. Ninguna carpeta en récord (todas debajo de su máximo o del capital inicial) y ninguna cerca de +20% (la mejor, +0,25%). Para las estrategias del Torneo no hay historial por estrategia para chequear récord; con +0,25% no hay objetivo. No se mandó mail.

## Recomendación

- **3 niveles — apagar.** 21 días (≥14), -9,22% contra 0% de USDT y -4,04% de HODL BTC; en 7 días -1,91%: pierde menos que HODL (-2,16%) pero sigue perdiendo, no mejoró. Lo decide Facu.
- **Agresiva — apagar.** 21 días, -9,20% contra 0% y -3,72% de HODL. En 7 días -2,94%, peor que HODL (-2,17%). 29,34 USD en comisiones en 219 operaciones: 2,9 de los 9,2 puntos que pierde. Lo decide Facu.
- **Laboratorio — seguir.** -0,32%: debajo de USDT, arriba de HODL BTC por 0,54 pp. Dos días y tres operaciones; no hay con qué juzgarlo.
- **DCA BTC — seguir.** Una cuota; es la referencia barata contra la que se miden las otras.
- **Torneo — seguir.** 12 h de vida; la líder es un HODL, no una estrategia activa.

**¿Key real de Binance?** Hoy, claramente no (la sección formal arranca el 07/11/2026). Las dos carpetas con 21 días pierden contra USDT y contra HODL BTC, y ninguna otra tiene más de dos días.
