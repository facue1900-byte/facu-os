# Veredicto de las carpetas cripto — 2026-10-31 06:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,45% al precio de hoy). El Laboratorio (-0,84%) va +3,52 pp arriba de HODL BTC. 3 niveles (-11,88%) y Agresiva (-10,89%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (1.034,85, +3,49% en 54 h) y L9 marcó récord (1.018,79), pero el Torneo ya tuvo su aviso de récord hoy: **no se mandó mail.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 881.21 | -11.88% | -4.54 pp (HODL -7.34%) | -3.53% (HODL -4.48%) | -3.61% (HODL -4.20%) | -12.94% (HODL -9.63%) | 2.56 USD (2.2% de la pérdida) | 90 |
| Agresiva | 891.10 | -10.89% | -3.75 pp (HODL -7.14%) | -2.27% (HODL -4.51%) | -4.32% (HODL -4.28%) | -10.93% (HODL -9.82%) | 31.53 USD (29.0% de la pérdida) | 234 |
| Laboratorio | 991.57 | -0.84% | +3.52 pp (HODL -4.36%) | -0.84% (HODL -4.36%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1034.85 | +3.49% (54 h) | +7.14 pp (P1 HODL BTC -3.65%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (24/10 06:06 y 05:32).
- **Frescura (ahora 06:55 UTC):** 3 niveles 06:06, Agresiva 06:32, Laboratorio 06:16 (todas < 1 h). DCA 27/10 22:38 (80 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 04:41 con última vela 04:00 (2,2 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 06:16 es 77.317 (80.841,96 × 0,95639). A ese precio su cuota de 0,0012356 BTC vale 95,53 y el total da **995,53 (-0,45%)**, contra -4,36% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,65%): A7 (+3,49%), L9 (+1,88%) y L4 (+0,41%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -5,13% mientras la estrategia P1 HODL BTC dice -3,65%. Hay que revisarlo en el torneo, no acá.
- **Récord del Torneo:** el máximo se sacó de todas las versiones de `vivo.json` en la historia de la rama. L9 (1.018,79) supera su máximo previo (1.018,66). A7 (1.034,85) quedó apenas abajo del suyo (1.035,77).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -0,41% en 24 h (884,83 → 881,21), con HODL BTC -0,79%. Sin operaciones desde el stop de LTC del 30/10 00:18. Tiene 407,70 en USDT y está -12,4% abajo de su máximo de 1.006,50.
- **Agresiva:** -1,01% en 24 h (900,20 → 891,10), con HODL BTC -1,73%. Una operación nueva desde el último juez: vendió ETH a las 02:32 por la regla de 24 h (+1,39%). Quedó 100% en USDT. Comisiones: 31,53 USD, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h (991,57), con HODL BTC -1,07%. 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** casi quieto desde el juez anterior: A7 1.035,77 → 1.034,85, L9 1.018,66 → 1.018,79 (récord), L4 1.003,96 → 1.004,07.
- **Alarmas:** récord de L9 en el Torneo, pero `alertas.json` ya tiene el récord del Torneo avisado hoy (31/10): máximo un mail por carpeta, evento y día, así que **no se mandó nada**. Nadie llegó a +20%. Ninguna de las otras carpetas está arriba de su capital inicial.

## Recomendación

- **3 niveles: apagar.** Lleva 23 días (≥14), está en -11,88% contra 0% de USDT y -7,34% de HODL BTC, y en 7 días hizo -3,61%: perdió algo menos que HODL (-4,20%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 23 días, está en -10,89% contra 0% de USDT y -7,14% de HODL, y en 7 días hizo -4,32% (HODL -4,28%): sigue cayendo. Pagó 31,53 USD de comisiones en 234 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,52 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,66%). Lleva 3 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 54 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 23 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
