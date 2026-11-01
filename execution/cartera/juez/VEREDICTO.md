# Veredicto de las carpetas cripto — 2026-11-01 12:50 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +2,97 pp arriba de HODL BTC. 3 niveles (-11,53%) y Agresiva (-11,32%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+4,82%). **Sin mails:** P7 y L8 del Torneo marcaron récord, pero al Torneo ya se le avisó hoy.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884.73 | -11.53% | -5.02 pp (HODL -6.51%) | -3.15% (HODL -3.62%) | -2.53% (HODL -2.93%) | -12.94% (HODL -9.63%) | 2.60 USD (2.3% de la pérdida) | 91 |
| Agresiva | 886.84 | -11.32% | -4.83 pp (HODL -6.49%) | -2.74% (HODL -3.84%) | -3.92% (HODL -3.15%) | -11.33% (HODL -9.82%) | 32.32 USD (28.6% de la pérdida) | 241 |
| Laboratorio | 991.57 | -0.84% | +2.97 pp (HODL -3.82%) | -0.84% (HODL -3.82%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (6 de 33 le ganan a USDT y a HODL BTC) | 1048.21 | +4.82% (84 h) | +7.48 pp (P1 HODL BTC -2.66%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último.
- **Frescura (ahora 12:50 UTC):** 3 niveles 12:07, Agresiva 12:32, Laboratorio 12:18 (todas < 1 h). DCA 27/10 22:38 (110 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 12:41, última vela 12:00 (límite 8 h). **Todas corren.**
- **DCA:** la próxima cuota es mañana, lunes 02/11. Si el martes 03/11 no hay snapshot nuevo, es falla.
- **Torneo:** 6 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,66%): A7 (+4,82%), L9 (+3,09%), P7 (+0,65%), L4 (+0,54%), L8 (+0,15%) y D2 (+0,01%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,16% mientras la estrategia P1 HODL BTC dice -2,66%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 19 versiones anteriores de `vivo.json` en la historia de la rama. **P7** 1.006,53 (máx. previo 1.005,92) y **L8** 1.001,521 (máx. previo 1.001,518, prácticamente empatado) están en récord. A7 1.048,21 sigue debajo de su máximo (1.053,02, de las 08:41); L9 1.030,91 (1.035,34); L4 1.005,42 (1.007,15). Como el Torneo ya tuvo su mail de récord hoy (`alertas.json`: 2026-11-01), no se manda otro.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,45% en 24 h, con HODL BTC +0,74%. Sin operaciones nuevas desde la venta de HYPE del 31/10 10:06. Tiene 443,73 en USDT.
- **Agresiva:** -0,48% en 24 h, con HODL BTC +0,28%. Compró TRX por 120 a las 00:32 y hizo una vuelta corta en AVAX (compra 130 a las 07:32, venta 128,00 a las 09:32, -1,5%). En 7 días pierde más que HODL (-3,92% contra -3,15%). Lleva 32,32 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,33%. Sigue 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es mañana, lunes 02/11.
- **Torneo:** A7 subió de 1.044,40 a 1.048,21 desde el veredicto de la mañana, pero sigue debajo del máximo de las 08:41. P7 y L8 marcaron máximo propio. Pasaron de 5 a 6 las estrategias que le ganan a USDT y a HODL BTC (entró D2, por un pelo).
- **Alarmas:** récords de P7 y L8 (Torneo) → sin mail, ya avisado hoy. Nadie en +20%. Las cuatro carpetas con historial están debajo de su capital o de su máximo.

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,53% contra 0% de USDT y -6,51% de HODL BTC, y en 7 días hizo -2,53%: perdió algo menos que HODL (-2,93%) pero siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,32% contra 0% de USDT y -6,49% de HODL, y en 7 días hizo -3,92%, peor que HODL (-3,15%). Pagó 32,32 USD de comisiones en 241 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,97 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 5 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 84 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
