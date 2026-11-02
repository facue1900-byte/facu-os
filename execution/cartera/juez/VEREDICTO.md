# Veredicto de las carpetas cripto — 2026-11-02 12:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La única en positivo es el Torneo con A7 (+1,61%), que en 8 h cayó desde +3,57%. El Laboratorio (-0,84%) va +2,73 pp arriba de HODL BTC. 3 niveles (-11,55%) y Agresiva (-11,57%) pierden contra USDT y contra HODL BTC. **Sin mail:** no hubo récord ni +20% en ninguna carpeta ni estrategia.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884.47 | -11.55% | -4.96 pp (HODL -6.60%) | -3.18% (HODL -3.71%) | -2.74% (HODL -3.14%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 884.33 | -11.57% | -5.19 pp (HODL -6.38%) | -3.02% (HODL -3.73%) | -3.78% (HODL -2.99%) | -11.69% (HODL -9.82%) | 33.17 USD (28.7% de la pérdida) | 247 |
| Laboratorio | 991.57 | -0.84% | +2.73 pp (HODL -3.57%) | -0.84% (HODL -3.57%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 27/10 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (6 de 33 le ganan a USDT y a HODL BTC) | 1016.12 | +1.61% (108 h) | +4.36 pp (P1 HODL BTC -2.75%) | falta (arrancó 29/10 00:00) | falta | -3.96% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después: ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 26/10 10:10, Agresiva 26/10 11:32).
- **Frescura (ahora 12:55 UTC):** 3 niveles 12:07, Agresiva 12:34, Laboratorio 12:33 (todas < 1 h). DCA 27/10 22:38 (134 h; límite 8 días). Torneo: `vivo.json` generado 12:48, última vela 12:00 (< 1 h; límite 8 h). **Todas corren.**
- **DCA:** la cuota de hoy (lunes 02/11) todavía no está en la rama a las 12:55 UTC. Si no aparece, el 04/11 22:38 pasa los 8 días y es falla.
- **Torneo:** 6 de 33 están arriba de 1.000 y del HODL BTC de P1 (-2,75%): A7 +1,61%, L9 +1,59%, P7 +0,45%, L8 +0,39%, L4 +0,10%, D2 +0,04%. Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,24% mientras la estrategia P1 HODL BTC dice -2,75%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** máximo previo sacado de las 25 versiones anteriores de `vivo.json`. Ninguna en récord: A7 1.016,12 (máx. 1.053,02), L9 1.015,93 (1.035,34), P7 1.004,47 (1.015,44), L8 1.003,90 (1.007,21).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -0,03% en 24 h, con HODL BTC -0,09%. Sin operaciones nuevas. Tiene 443,73 en USDT.
- **Agresiva:** -0,28% en 24 h, con HODL BTC +0,12%. 6 operaciones: SOL compra y venta (-0,85%), venta de TRX (+1,82%), compra de ETH (200), SOL (140) y XRP (130, 08:37). Quedan 416,30 en USDT. En 7 días pierde más que HODL (-3,78% contra -2,99%). Lleva 33,17 USD de comisiones, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,26%. Sigue 100% en USDT desde el stop de HYPE.
- **DCA BTC:** sin cambios; la cuota de hoy lunes todavía no corrió.
- **Torneo:** bajón de mercado desde las 04:00: A7 de 1.035,73 a 1.016,12; L9 de 1.027,21 a 1.015,93; P7 de 1.015,44 a 1.004,47. Las que le ganan a USDT y a HODL BTC bajaron de 13 a 6 (L3, P5, P6, P5N y D1/D3/D4 volvieron abajo de 1.000).
- **Alarmas:** ningún récord y nadie en +20%. **No se mandó mail.**

## Recomendación

- **3 niveles: apagar.** Lleva 25 días (≥14), está en -11,55% contra 0% de USDT y -6,60% de HODL BTC, y en 7 días no mejoró: -2,74% (algo menos malo que HODL, -3,14%, pero igual pierde). Lo decide Facu.
- **Agresiva: apagar.** Lleva 25 días, está en -11,57% contra 0% de USDT y -6,38% de HODL, y en 7 días hizo -3,78%, peor que HODL (-2,99%). Pagó 33,17 USD de comisiones en 247 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,73 pp arriba de HODL BTC, con peor caída (-2,35%) menos de la mitad que la de HODL (-5,66%). Lleva 5 días: todavía no se puede juzgar.
- **DCA BTC: revisar.** Una sola cuota; la de hoy lunes no está en la rama. Si mañana sigue sin aparecer, se arregla.
- **Torneo: revisar.** A7 lidera con +1,61%, pero son 108 h de datos, está 3,5% abajo de su máximo y el `hodl_btc` de `vivo.json` no coincide con P1.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 25 días pierden más de 11%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
