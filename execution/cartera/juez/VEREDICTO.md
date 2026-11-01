# Veredicto de las carpetas cripto — 2026-11-01 00:50 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01%, foto del 27/10). El Laboratorio (-0,84%) va +3,25 pp arriba de HODL BTC. 3 niveles (-11,82%) y Agresiva (-11,19%) pierden contra USDT y contra HODL BTC. En el Torneo lidera A7 (+4,43%), pero hoy no está en récord. **Sin avisos: no se mandó mail.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 881.80 | -11.82% | -4.75 pp (HODL -7.07%) | -3.47% (HODL -4.20%) | -3.41% (HODL -4.05%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 888.15 | -11.19% | -4.51 pp (HODL -6.67%) | -2.60% (HODL -4.03%) | -3.88% (HODL -3.98%) | -11.21% (HODL -9.82%) | 32.06 USD (28.7% de la pérdida) | 239 |
| Laboratorio | 991.57 | -0.84% | +3.25 pp (HODL -4.10%) | -0.84% (HODL -4.10%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1044.27 | +4.43% (72 h) | +7.57 pp (P1 HODL BTC -3.14%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (25/10 00:06 y 00:32).
- **Frescura (ahora 00:50 UTC):** 3 niveles 00:06, Agresiva 00:32, Laboratorio 00:16 (todas < 1 h). DCA 27/10 22:38 (98 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 00:41 con última vela 00:00 (< 1 h; límite 8 h). **Todas corren.**
- **DCA:** la próxima cuota es el lunes 02/11. Si el martes 03/11 no hay snapshot nuevo, es falla.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,14%): A7 (+4,43%), L9 (+2,28%) y L4 (+0,64%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,62% mientras la estrategia P1 HODL BTC dice -3,14%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 16 versiones anteriores de `vivo.json` en la historia de la rama. Ninguna supera su máximo: A7 1.044,27 (máx. 1.050,13), L9 1.022,82 (1.028,30), L4 1.006,40 (1.007,15). Sin récord, sin mail.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,28% en 24 h (879,38 → 881,80), con HODL BTC +0,86%. Sin operaciones nuevas desde la venta de HYPE del 31/10 10:06. Tiene 443,73 en USDT.
- **Agresiva:** -0,35% en 24 h (891,28 → 888,15), con HODL BTC +0,51%. Siguió rotando: vendió NEAR y compró LINK a las 19:32, vendió LINK a las 23:32 (98,19 por 100 invertidos) y compró TRX por 120 a las 00:32. Lleva 32,06 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h (991,57), con HODL BTC +0,15%. Sigue 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** A7 bajó de su máximo de 1.050,13 a 1.044,27; L9 de 1.028,30 a 1.022,82. El ranking de arriba no cambió.
- **Alarmas:** ninguna. Ninguna carpeta en récord (las cuatro con historial están debajo de su capital o de su máximo) y nadie en +20%.

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,82% contra 0% de USDT y -7,07% de HODL BTC, y en 7 días hizo -3,41%: perdió algo menos que HODL (-4,05%) pero siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,19% contra 0% de USDT y -6,67% de HODL, y en 7 días hizo -3,88% (HODL -3,98%): sigue cayendo. Pagó 32,06 USD de comisiones en 239 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,25 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 4 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera, pero son 72 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
