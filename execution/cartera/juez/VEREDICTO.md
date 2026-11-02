# Veredicto de las carpetas cripto — 2026-11-02 00:51 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +2,53 pp arriba de HODL BTC. 3 niveles (-11,41%) y Agresiva (-11,37%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+3,23%, bajó desde +4,05%). **Un mail:** récord de P7 en el Torneo (1.008,50).

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 885.87 | -11.41% | -5.27 pp (HODL -6.15%) | -3.02% (HODL -3.25%) | -2.46% (HODL -2.24%) | -12.94% (HODL -9.63%) | 2.60 USD (2.3% de la pérdida) | 91 |
| Agresiva | 886.30 | -11.37% | -5.27 pp (HODL -6.10%) | -2.80% (HODL -3.44%) | -3.90% (HODL -2.32%) | -11.37% (HODL -9.82%) | 32.70 USD (28.8% de la pérdida) | 244 |
| Laboratorio | 991.57 | -0.84% | +2.53 pp (HODL -3.37%) | -0.84% (HODL -3.37%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (13 de 33 le ganan a USDT y a HODL BTC) | 1032.27 | +3.23% (96 h) | +5.41 pp (P1 HODL BTC -2.18%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 26/10 00:06, Agresiva 25/10 23:31).
- **Frescura (ahora 00:51 UTC):** 3 niveles 00:08, Agresiva 00:31, Laboratorio 00:17 (todas < 1 h). DCA 27/10 22:38 (122 h; límite 8 días). Torneo: `vivo.json` generado 00:42, última vela 00:00. **Todas corren.**
- **DCA:** la cuota de hoy (lunes 02/11) todavía no está en la rama. Si el martes 03/11 no hay snapshot nuevo, es falla (se pasaría de 8 días el 04/11 22:38).
- **Torneo:** 13 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,18%), pero de esas 13 sólo A7 (+3,23%), L9 (+2,20%) y P7 (+0,85%) sacan más de +0,4%; el resto (L4, L8, L3, P5, P6, P5N, D1–D4) está entre +0,01% y +0,38%. Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -3,68% mientras la estrategia P1 HODL BTC dice -2,18%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 22 versiones anteriores de `vivo.json`. En récord: **P7** 1.008,50 (máx. previo 1.006,75), L8 1.002,25 (1.001,52), L3/P5/P6/P5N 1.001,6 (1.000,11) y las DCA D1–D4 (+0,01% a +0,04%). A7 1.032,27 sigue debajo de su máximo (1.053,02); L9 1.022,05 (1.035,34); L4 1.003,82 (1.007,15).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,46% en 24 h, con HODL BTC +0,99%. Sin operaciones nuevas. Tiene 443,73 en USDT.
- **Agresiva:** -0,17% en 24 h, con HODL BTC +0,78%. Cinco operaciones: AVAX (-1,44%), SOL (-0,85%) y TRX (+1,82%, salió a las 00:31 por la regla de 24 h). Quedó 100% en USDT. En 7 días pierde más que HODL (-3,90% contra -2,32%). Lleva 32,70 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,75%. Sigue 100% en USDT desde el stop de HYPE del 29/10.
- **DCA BTC:** sin cambios; la cuota de hoy lunes todavía no corrió.
- **Torneo:** A7 bajó de 1.040,54 a 1.032,27; L9 de 1.026,57 a 1.022,05. P7 subió a 1.008,50 (récord). Pasaron de 6 a 13 las que le ganan a USDT y a HODL BTC, casi todas por centavos.
- **Alarmas:** récord del Torneo (P7, más L8 y otras) → **mail mandado** a facue1900@gmail.com (nuevo día UTC; el aviso anterior fue el 01/11). Nadie en +20%. Las cuatro carpetas con historial están debajo de su capital o de su máximo.

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,41% contra 0% de USDT y -6,15% de HODL BTC, y en 7 días hizo -2,46%, peor que HODL (-2,24%). Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,37% contra 0% de USDT y -6,10% de HODL, y en 7 días hizo -3,90%, peor que HODL (-2,32%). Pagó 32,70 USD de comisiones en 244 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,53 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 5 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás. Ojo con la cuota de hoy.
- **Torneo: revisar.** A7 lidera, pero son 96 h de datos, A7 viene bajando desde su máximo y el `hodl_btc` de `vivo.json` no coincide con P1.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=1
