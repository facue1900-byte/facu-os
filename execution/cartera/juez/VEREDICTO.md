# Veredicto de las carpetas cripto — 2026-10-30 12:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,43% al precio de hoy). El Laboratorio (-0,84%) está +3,33 pp arriba de HODL BTC. 3 niveles (-11,76%) y Agresiva (-10,80%) pierden contra USDT y contra HODL BTC. En el Torneo la líder sigue siendo A7 (+2,69% en 32 h), nuevo máximo, pero el récord de A7 ya se avisó hoy: no se repite el mail.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 882.38 | -11.76% | -4.63 pp (HODL -7.14%) | -3.41% (HODL -4.27%) | -4.62% (HODL -5.04%) | -12.94% (HODL -9.63%) | 2.56 USD (2.2% de la pérdida) | 90 |
| Agresiva | 892.04 | -10.80% | -3.78 pp (HODL -7.02%) | -2.17% (HODL -4.38%) | -5.91% (HODL -5.34%) | -10.80% (HODL -9.33%) | 31.23 USD (28.9% de la pérdida) | 232 |
| Laboratorio | 991.57 | -0.84% | +3.33 pp (HODL -4.18%) | -0.84% (HODL -4.18%) | falta (arrancó 27/10) | -2.35% (HODL -5.40%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (4 de 33 le ganan a USDT y a HODL BTC) | 1026.90 | +2.69% (32 h) | +5.1 pp (P1 HODL BTC -2.39%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento. La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (23/10 a la misma hora).
- **Frescura (ahora 12:52 UTC):** 3 niveles 12:07, Agresiva 12:47, Laboratorio 12:25 (todas < 1 h). DCA 27/10 22:38 (62 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 08:41 con última vela 08:00 (4,2 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 12:25 es 77.464 (80.841,96 × 0,95822, el mismo BTC de inicio que la DCA). A ese precio su cuota de 0,0012356 BTC vale 95,72 y el total da **995,72 (-0,43%)**, contra -4,18% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 4 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,39%): A7, L9, L4 y P7 (P7 con +0,004%, casi empate). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -3,88% mientras la estrategia P1 HODL BTC dice -2,39%. Hay que revisarlo en el torneo, no acá.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -2,81% en 24 h (907,85 → 882,38), con HODL BTC -3,34%. Sin operaciones desde el stop de LTC de las 00:18. Tiene 407,70 en USDT y está -12,3% abajo de su máximo de 1.006,50.
- **Agresiva:** -1,76% en 24 h (908,01 → 892,04), con HODL BTC -3,42%. Desde el último juez compró TRX a las 10:32 (150 USD, rebote en soporte) y vendió HYPE a las 12:47 (-0,52%, se invalidó la tesis de momentum). Las comisiones ya suman 31,23 USD: el 29% de lo que pierde.
- **Laboratorio:** -0,52% en 24 h (996,80 → 991,57), con HODL BTC -3,34%. Sin operaciones desde el stop de HYPE de las 23:43; 100% en USDT. Quedarse afuera le ahorró la caída de hoy.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** A7 subió de 1.020,74 a 1.026,90; L9 a 1.013,03 y L4 a 1.003,24. Las HODL (P1 a P3) van entre -2,4% y -3,3%.
- **Alarmas:** A7 marcó un nuevo máximo (1.026,90, el más alto de los `vivo.json` commiteados y arriba de 1.000), pero el récord del Torneo ya se avisó hoy (30/10) en el juez de las 06:55: **no se manda otro mail**. Nadie llegó a +20%. Ninguna de las otras cuatro está en su máximo y arriba de 1.000.

## Recomendación

- **3 niveles: apagar.** Lleva 23 días (≥14), está en -11,76% contra 0% de USDT y -7,14% de HODL BTC, y en 7 días hizo -4,62%: perdió algo menos que HODL (-5,04%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 23 días, está en -10,80% contra 0% de USDT y -7,02% de HODL, y en 7 días hizo -5,91%, peor que HODL (-5,34%). Pagó 31,23 USD de comisiones en 232 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,33 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,40%). Lleva 2,6 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero el `hodl_btc` de `vivo.json` no coincide con P1 y son 32 h de datos: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 23 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
