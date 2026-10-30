# Veredicto de las carpetas cripto — 2026-10-30 18:52 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,48% al precio de hoy). El Laboratorio (-0,84%) está +3,88 pp arriba de HODL BTC. 3 niveles (-11,94%) y Agresiva (-10,86%) pierden contra USDT y contra HODL BTC. En el Torneo la líder sigue siendo A7 (+2,12% en 40 h), que bajó desde su máximo de 1.026,90: no hay récord ni +20%, no se manda mail.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 880.65 | -11.94% | -4.34 pp (HODL -7.59%) | -3.60% (HODL -4.74%) | -4.81% (HODL -5.49%) | -12.94% (HODL -9.63%) | 2.56 USD (2.1% de la pérdida) | 90 |
| Agresiva | 891.43 | -10.86% | -3.22 pp (HODL -7.64%) | -2.24% (HODL -5.02%) | -5.08% (HODL -5.67%) | -10.86% (HODL -9.47%) | 31.23 USD (28.8% de la pérdida) | 232 |
| Laboratorio | 991.57 | -0.84% | +3.88 pp (HODL -4.73%) | -0.84% (HODL -4.73%) | falta (arrancó 27/10) | -2.35% (HODL -5.56%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1021.22 | +2.12% (40 h) | +5.2 pp (P1 HODL BTC -3.09%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento. La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (23/10 a la misma hora).
- **Frescura (ahora 18:52 UTC):** 3 niveles 18:06, Agresiva 18:32, Laboratorio 18:17 (todas < 1 h). DCA 27/10 22:38 (68 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 16:48 con última vela 16:00 (2 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 18:17 es 77.021 (80.841,96 × 0,95274, el mismo BTC de inicio que la DCA). A ese precio su cuota de 0,0012356 BTC vale 95,17 y el total da **995,17 (-0,48%)**, contra -4,73% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,09%): A7 (+2,12%), L4 (+0,45%) y L9 (+0,23%). P7 bajó a -0,7%. Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,58% mientras la estrategia P1 HODL BTC dice -3,09%. Hay que revisarlo en el torneo, no acá.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -4,26% en 24 h (919,85 → 880,65), con HODL BTC -5,61%. Sin operaciones desde el stop de LTC de las 00:18. Tiene 407,70 en USDT y está -12,5% abajo de su máximo de 1.006,50.
- **Agresiva:** -2,98% en 24 h (918,79 → 891,43), con HODL BTC -4,65%. Sin operaciones nuevas desde el último juez (la última fue la venta de HYPE de las 12:47, -0,52%). Las comisiones ya suman 31,23 USD: el 29% de lo que pierde.
- **Laboratorio:** -1,54% en 24 h (1.007,05 → 991,57), con HODL BTC -4,74%. Sin operaciones desde el stop de HYPE de las 23:43; 100% en USDT. Quedarse afuera le ahorró la caída de hoy.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** A7 bajó de 1.026,90 a 1.021,22; L4 subió a 1.004,47 y L9 bajó a 1.002,34. Las HODL (P1 a P3) van entre -3,1% y -3,9%.
- **Alarmas:** ninguna. Nadie está en su máximo histórico por encima de 1.000 (A7 está abajo de su 1.026,90, y además el récord del Torneo ya se avisó hoy) y nadie llegó a +20%. **No se mandó mail.**

## Recomendación

- **3 niveles: apagar.** Lleva 23 días (≥14), está en -11,94% contra 0% de USDT y -7,59% de HODL BTC, y en 7 días hizo -4,81%: perdió algo menos que HODL (-5,49%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 23 días, está en -10,86% contra 0% de USDT y -7,64% de HODL, y en 7 días hizo -5,08% (HODL -5,67%): sigue cayendo. Pagó 31,23 USD de comisiones en 232 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,88 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,56%). Lleva 2,8 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero el `hodl_btc` de `vivo.json` no coincide con P1 y son 40 h de datos: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 23 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
