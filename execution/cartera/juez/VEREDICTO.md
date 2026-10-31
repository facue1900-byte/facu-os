# Veredicto de las carpetas cripto — 2026-10-31 12:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,41% al precio de hoy). El Laboratorio (-0,84%) va +3,17 pp arriba de HODL BTC. 3 niveles (-11,82%) y Agresiva (-10,89%) pierden contra USDT y contra HODL BTC. En el Torneo sigue liderando A7 (1.031,84, +3,18% en 60 h). No hubo récord ni +20% en ninguna: **no se mandó mail.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 881.76 | -11.82% | -4.85 pp (HODL -6.97%) | -3.47% (HODL -4.10%) | -3.22% (HODL -3.70%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 891.10 | -10.89% | -4.14 pp (HODL -6.75%) | -2.27% (HODL -4.11%) | -3.83% (HODL -3.94%) | -10.93% (HODL -9.82%) | 31.53 USD (29.0% de la pérdida) | 234 |
| Laboratorio | 991.57 | -0.84% | +3.17 pp (HODL -4.01%) | -0.84% (HODL -4.01%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1031.84 | +3.18% (60 h) | +6.27 pp (P1 HODL BTC -3.09%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (24/10 12:06 y 12:32).
- **Frescura (ahora 12:55 UTC):** 3 niveles 12:09, Agresiva 12:32, Laboratorio 12:21 (todas < 1 h). DCA 27/10 22:38 (86 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 12:41 con última vela 12:00 (< 1 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 12:21 es 77.599 (80.841,96 × 0,95989). A ese precio su cuota de 0,0012356 BTC vale 95,88 y el total da **995,88 (-0,41%)**, contra -4,01% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,09%): A7 (+3,18%), L9 (+1,74%) y L4 (+0,48%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,58% mientras la estrategia P1 HODL BTC dice -3,09%. Hay que revisarlo en el torneo, no acá.
- **Récord del Torneo:** el máximo se sacó de todas las versiones de `vivo.json` en la historia de la rama. Ninguna estrategia supera su máximo: A7 1.031,84 (máx. 1.035,77), L9 1.017,41 (máx. 1.018,79), L4 1.004,77 (máx. 1.004,79).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -0,07% en 24 h (882,38 → 881,76), con HODL BTC +0,17%. Una operación nueva: a las 10:06 vendió HYPE (36,07 USD, -9,74%) por tesis invalidada, antes de que saltara el stop. Tiene 443,73 en USDT y está -12,4% abajo de su máximo de 1.006,50.
- **Agresiva:** -0,97% en 24 h (899,83 → 891,10), con HODL BTC -0,23%. Sin operaciones nuevas desde la venta de ETH de las 02:32; sigue 100% en USDT. Comisiones: 31,53 USD, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h (991,57), con HODL BTC +0,26%. 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** retrocede un poco desde el juez de las 06:55: A7 1.034,85 → 1.031,84, L9 1.018,79 → 1.017,41, L4 1.004,07 → 1.004,77.
- **Alarmas:** ningún récord (ninguna carpeta está arriba de su capital salvo el Torneo, y ahí ninguna estrategia superó su máximo) y nadie llegó a +20%. **No se mandó nada.**

## Recomendación

- **3 niveles: apagar.** Lleva 23 días (≥14), está en -11,82% contra 0% de USDT y -6,97% de HODL BTC, y en 7 días hizo -3,22%: perdió algo menos que HODL (-3,70%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 23 días, está en -10,89% contra 0% de USDT y -6,75% de HODL, y en 7 días hizo -3,83% (HODL -3,94%): sigue cayendo. Pagó 31,53 USD de comisiones en 234 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,17 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,66%). Lleva 4 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 60 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 23 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
