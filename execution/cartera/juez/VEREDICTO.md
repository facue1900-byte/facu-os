# Veredicto de las carpetas cripto — 2026-10-30 06:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,28% al precio de hoy). Le sigue el Laboratorio (-0,84%, pero +1,85 pp arriba de HODL BTC). 3 niveles (-11,09%) y Agresiva (-9,98%) siguen perdiendo contra USDT y contra HODL BTC. En el Torneo la líder es A7 (+2,07% en 28 h): es **récord**, se avisó por mail.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 889.11 | -11.09% | -5.35 pp (HODL -5.73%) | -2.67% (HODL -2.83%) | -4.24% (HODL -3.96%) | -12.94% (HODL -9.63%) | 2.56 USD (2.3% de la pérdida) | 90 |
| Agresiva | 900.20 | -9.98% | -4.47 pp (HODL -5.51%) | -1.28% (HODL -2.83%) | -4.02% (HODL -3.98%) | -10.47% (HODL -9.33%) | 30.93 USD (31.0% de la pérdida) | 230 |
| Laboratorio | 991.57 | -0.84% | +1.85 pp (HODL -2.69%) | -0.84% (HODL -2.69%) | falta (arrancó 27/10) | -2.35% (HODL -5.40%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (14 de 33 le ganan a USDT y a HODL BTC) | 1020.74 | +2.07% (28 h) | +4.4 pp (P1 HODL BTC -2.3%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento. La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (los dos del 23/10 a la misma hora).
- **Frescura (ahora 06:54 UTC):** 3 niveles 06:11, Agresiva 06:32, Laboratorio 06:18 (todas < 1 h). DCA 27/10 22:38 (56 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 04:41 con última vela 04:00 (2,2 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 06:18 es 78.664 (inicio 80.841,96 × 0,97306, el mismo BTC de inicio que la DCA). A ese precio, su cuota de 0,0012356 BTC vale 97,20 y el total da **997,20 (-0,28%)**, contra -2,69% de HODL BTC. Es cálculo propio, no el snapshot oficial; la tabla deja el oficial.
- **Torneo:** 14 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,3%). Ojo: D1, D3 y D4 entran en esa cuenta con +0,001%, así que de verdad son 11. Hay 6 que no operaron. **Inconsistencia:** el ciclo de las 00:42 mostraba casi todas en 1.000 y P1 en -2,6%; el de las 04:41 (una sola vela de 4 h después) muestra caídas máximas de -2% a -7% en estrategias que antes estaban quietas, y la columna `hodl_btc` dice -3,82% mientras P1 dice -2,3%. Parece que el torneo recalculó el camino desde el 29/10 y no sumó sólo una vela. Hay que revisarlo en el torneo, no acá.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC sale de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -2,21% en 24 h (909,17 → 889,11), con HODL BTC -2,00%. Stop de LTC a las 00:18 (-18,0%). Tiene 407,70 en USDT y está -12,9% abajo de su máximo de 1.006,50.
- **Agresiva:** -0,85% en 24 h (907,89 → 900,20), con HODL BTC -1,86%. Desde el último juez compró ETH a las 02:32 (150 USD, rebote en soporte) y HYPE a las 03:32 (150 USD, re-entrada por momentum); las dos van alrededor de +1,7%. Las comisiones ya suman 30,93 USD: el 31% de lo que pierde.
- **Laboratorio:** -1,10% en 24 h (1.002,60 → 991,57), con HODL BTC -1,80%. Sin operaciones desde el stop de HYPE de las 23:43 y 100% en USDT.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** en el ciclo de las 04:41 pasaron al frente A7 (+2,07%, canasta NEAR/SOL/LINK/AVAX/LTC), L9 (+1,03%) y P7 (+0,59%). Las HODL (P1 a P3) van entre -2,3% y -2,9%. Ver la inconsistencia en las notas.
- **Alarmas:** **récord en el Torneo** (A7, 1.020,74: el máximo de los `vivo.json` commiteados y arriba de 1.000). Mail mandado a facue1900@gmail.com. Nadie llegó a +20%. Ninguna de las otras cuatro está en su máximo y arriba de 1.000.

## Recomendación

- **3 niveles: apagar.** Lleva 22 días (≥14), está en -11,09% contra 0% de USDT y -5,73% de HODL BTC, y en 7 días hizo -4,24%, peor que HODL (-3,96%): no mejoró. Lo decide Facu.
- **Agresiva: apagar.** Lleva 22 días, está en -9,98% contra 0% de USDT y -5,51% de HODL, y en 7 días hizo -4,02%, peor que HODL (-3,98%): no mejoró. Pagó 30,93 USD de comisiones en 230 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** Está en -0,84%, abajo de USDT pero +1,85 pp arriba de HODL BTC, y su peor caída (-2,35%) es menos de la mitad de la de HODL (-5,40%). Lleva 2,3 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Tiene una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** El récord de A7 vale, pero antes de creerle al ranking hay que ver por qué el ciclo de las 04:41 reescribió el camino del 29/10.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 22 días pierden alrededor de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=1
