# Veredicto de las carpetas cripto — 2026-11-02 06:51 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +2,39 pp arriba de HODL BTC. 3 niveles (-11,34%) y Agresiva (-11,57%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+3,57%). **Sin mail:** P7 y otras del Torneo hicieron récord, pero el récord del Torneo ya se avisó hoy.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 886.62 | -11.34% | -5.28 pp (HODL -6.06%) | -2.94% (HODL -3.16%) | -2.27% (HODL -2.17%) | -12.94% (HODL -9.63%) | 2.60 USD (2.3% de la pérdida) | 91 |
| Agresiva | 884.29 | -11.57% | -5.55 pp (HODL -6.02%) | -3.02% (HODL -3.36%) | -4.11% (HODL -2.30%) | -11.57% (HODL -9.82%) | 33.04 USD (28.6% de la pérdida) | 246 |
| Laboratorio | 991.57 | -0.84% | +2.39 pp (HODL -3.23%) | -0.84% (HODL -3.23%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 27/10 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (13 de 33 le ganan a USDT y a HODL BTC) | 1035.73 | +3.57% (100 h) | +5.40 pp (P1 HODL BTC -1.83%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles y Agresiva: 26/10 06:07 y 06:32).
- **Frescura (ahora 06:51 UTC):** 3 niveles 06:07, Agresiva 06:32, Laboratorio 06:23 (todas < 1 h). DCA 27/10 22:38 (128 h; límite 8 días). Torneo: `vivo.json` generado 04:41, última vela 04:00 (2 h; límite 8 h). **Todas corren.**
- **DCA:** la cuota de hoy (lunes 02/11) todavía no está en la rama. Si mañana no hay snapshot nuevo, es falla (se pasa de 8 días el 04/11 22:38).
- **Torneo:** 13 de 33 están arriba de 1.000 y del HODL BTC de P1 (-1,83%): A7 +3,57%, L9 +2,72%, P7 +1,54%, L8 +0,72%, y L3/P5/P6/P5N (+0,52%), L4 y D1–D4 por centavos. Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -3,33% mientras la estrategia P1 HODL BTC dice -1,83%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 23 versiones anteriores de `vivo.json`. En récord: **P7** 1.015,44 (máx. previo 1.008,50), L8 1.007,21 (1.002,25), L3/P5/P6/P5N ~1.005,2 (1.001,6) y D1–D4. A7 1.035,73 sigue debajo de su máximo (1.053,02); L9 1.027,21 (1.035,34).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,28% en 24 h, con HODL BTC +0,53%. Sin operaciones nuevas. Tiene 443,73 en USDT.
- **Agresiva:** -0,55% en 24 h, con HODL BTC +0,30%. Volvió a entrar a las 01:33: compró ETH (200 USD) y SOL (140 USD); quedan 546,30 en USDT. En 7 días pierde más que HODL (-4,11% contra -2,30%). Lleva 33,04 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,34%. Sigue 100% en USDT desde el stop de HYPE.
- **DCA BTC:** sin cambios; la cuota de hoy lunes todavía no corrió.
- **Torneo:** A7 subió de 1.032,27 a 1.035,73; L9 de 1.022,05 a 1.027,21; P7 a 1.015,44 (récord). Siguen 13 las que le ganan a USDT y a HODL BTC.
- **Alarmas:** récord en el Torneo (P7, L8 y otras) → **sin mail**: ya se avisó el récord del Torneo hoy (02/11). Nadie en +20%. Las cuatro carpetas con historial están debajo de su capital.

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,34% contra 0% de USDT y -6,06% de HODL BTC, y en 7 días hizo -2,27%, peor que HODL (-2,17%). Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,57% contra 0% de USDT y -6,02% de HODL, y en 7 días hizo -4,11%, peor que HODL (-2,30%). Pagó 33,04 USD de comisiones en 246 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,39 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 5 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás. Ojo con la cuota de hoy.
- **Torneo: revisar.** A7 lidera, pero son 100 h de datos, A7 está 1,6% abajo de su máximo y el `hodl_btc` de `vivo.json` no coincide con P1.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
