# Veredicto de las carpetas cripto — 2026-11-01 18:50 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +2,71 pp arriba de HODL BTC. 3 niveles (-11,59%) y Agresiva (-11,20%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+4,05%, bajó desde +4,82%). **Sin mails:** P7 del Torneo marcó récord, pero al Torneo ya se le avisó hoy.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884.14 | -11.59% | -5.05 pp (HODL -6.54%) | -3.21% (HODL -3.65%) | -3.14% (HODL -3.48%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 888.01 | -11.20% | -4.87 pp (HODL -6.33%) | -2.61% (HODL -3.67%) | -4.19% (HODL -3.38%) | -11.33% (HODL -9.82%) | 32.32 USD (28.9% de la pérdida) | 241 |
| Laboratorio | 991.57 | -0.84% | +2.71 pp (HODL -3.55%) | -0.84% (HODL -3.55%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (6 de 33 le ganan a USDT y a HODL BTC) | 1040.54 | +4.05% (88 h) | +6.69 pp (P1 HODL BTC -2.63%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último.
- **Frescura (ahora 18:50 UTC):** 3 niveles 18:06, Agresiva 18:32, Laboratorio 18:16 (todas < 1 h). DCA 27/10 22:38 (116 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 16:41, última vela 16:00 (límite 8 h). **Todas corren.**
- **DCA:** la próxima cuota es mañana, lunes 02/11. Si el martes 03/11 no hay snapshot nuevo, es falla.
- **Torneo:** 6 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,63%): A7 (+4,05%), L9 (+2,66%), P7 (+0,68%), L4 (+0,46%), L8 (+0,10%) y D2 (+0,0004%, literalmente 0,004 USD). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,13% mientras la estrategia P1 HODL BTC dice -2,63%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 20 versiones anteriores de `vivo.json` en la historia de la rama. **P7** 1.006,75 (máx. previo 1.006,53, de las 12:41) está en récord. A7 1.040,54 sigue debajo de su máximo (1.053,02, de las 08:41); L9 1.026,57 (1.035,34); L4 1.004,56 (1.007,15); L8 1.001,03 (1.001,52). Como el Torneo ya tuvo su mail de récord hoy (`alertas.json`: 2026-11-01), no se manda otro.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,23% en 24 h, con HODL BTC +0,45%. Sin operaciones nuevas desde la venta de HYPE del 31/10 10:06. Tiene 443,73 en USDT.
- **Agresiva:** -0,47% en 24 h, con HODL BTC +0,30%. Tres vueltas perdedoras en 24 h: NEAR (-1,0%), LINK (-1,7%) y AVAX (-1,4%); además compró TRX por 120 a las 00:32 y lo tiene. En 7 días pierde más que HODL (-4,19% contra -3,38%). Lleva 32,32 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,28%. Sigue 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es mañana, lunes 02/11.
- **Torneo:** A7 bajó de 1.048,21 (veredicto de las 12:50) a 1.040,54; L9 de 1.030,91 a 1.026,57. P7 marcó máximo propio. Siguen 6 las que le ganan a USDT y a HODL BTC.
- **Alarmas:** récord de P7 (Torneo) → sin mail, ya avisado hoy. Nadie en +20%. Las cuatro carpetas con historial están debajo de su capital o de su máximo.

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,59% contra 0% de USDT y -6,54% de HODL BTC, y en 7 días hizo -3,14%: algo menos malo que HODL (-3,48%) pero siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,20% contra 0% de USDT y -6,33% de HODL, y en 7 días hizo -4,19%, peor que HODL (-3,38%). Pagó 32,32 USD de comisiones en 241 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,71 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 5 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 88 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
