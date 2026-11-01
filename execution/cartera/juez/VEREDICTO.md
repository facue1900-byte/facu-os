# Veredicto de las carpetas cripto — 2026-11-01 06:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +2,71 pp arriba de HODL BTC. 3 niveles (-11,59%) y Agresiva (-11,08%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+4,44%). **Un aviso: récord de L8 en el Torneo (1.001,25), mail mandado.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884.14 | -11.59% | -5.03 pp (HODL -6.56%) | -3.21% (HODL -3.67%) | -3.28% (HODL -3.57%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 889.17 | -11.08% | -4.78 pp (HODL -6.30%) | -2.49% (HODL -3.65%) | -3.72% (HODL -3.28%) | -11.21% (HODL -9.82%) | 32.06 USD (28.9% de la pérdida) | 239 |
| Laboratorio | 991.57 | -0.84% | +2.71 pp (HODL -3.55%) | -0.84% (HODL -3.55%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (5 de 33 le ganan a USDT y a HODL BTC) | 1044.40 | +4.44% (76 h) | +7.30 pp (P1 HODL BTC -2.86%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (25/10 04:06 y 06:32).
- **Frescura (ahora 06:51 UTC):** 3 niveles 06:06, Agresiva 06:32, Laboratorio 06:17 (todas < 1 h). DCA 27/10 22:38 (104 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 04:41, última vela 04:00 (2 h; límite 8 h). **Todas corren.**
- **DCA:** la próxima cuota es el lunes 02/11. Si el martes 03/11 no hay snapshot nuevo, es falla.
- **Torneo:** 5 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,86%): A7 (+4,44%), L9 (+2,50%), L4 (+0,60%), L8 (+0,12%) y P7 (+0,08%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,35% mientras la estrategia P1 HODL BTC dice -2,86%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 17 versiones anteriores de `vivo.json` en la historia de la rama. **L8 está en récord:** 1.001,25 contra un máximo previo de 1.000,00 (estaba quieta en USDT; compró ETH). Las demás no: A7 1.044,40 (máx. 1.050,13), L9 1.025,03 (1.028,30), L4 1.006,01 (1.007,15), P7 1.000,82 (1.005,92).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,33% en 24 h, con HODL BTC +0,85%. Sin operaciones nuevas desde la venta de HYPE del 31/10 10:06. Tiene 443,73 en USDT.
- **Agresiva:** -0,22% en 24 h, con HODL BTC +0,91%. Sin operaciones desde la compra de TRX por 120 a las 00:32. En 7 días ahora pierde más que HODL (-3,72% contra -3,28%). Lleva 32,06 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,84%. Sigue 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** A7 sigue debajo de su máximo (1.044,40 vs 1.050,13). L8 compró ETH y marcó máximo propio. Pasaron de 3 a 5 las estrategias que le ganan a USDT y a HODL BTC.
- **Alarmas:** récord de L8 (Torneo) → mail mandado a facue1900@gmail.com. Nadie en +20%. Las cuatro carpetas con historial están debajo de su capital o de su máximo.

## Recomendación

- **3 niveles: apagar.** Lleva 24 días (≥14), está en -11,59% contra 0% de USDT y -6,56% de HODL BTC, y en 7 días hizo -3,28%: perdió algo menos que HODL (-3,57%) pero siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 24 días, está en -11,08% contra 0% de USDT y -6,30% de HODL, y en 7 días hizo -3,72%, peor que HODL (-3,28%). Pagó 32,06 USD de comisiones en 239 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,71 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 4 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 76 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 24 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=1
