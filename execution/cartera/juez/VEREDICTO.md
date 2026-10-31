# Veredicto de las carpetas cripto — 2026-10-31 00:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,43% al precio de hoy). El Laboratorio (-0,84%) va +3,40 pp arriba de HODL BTC. 3 niveles (-11,78%) y Agresiva (-10,87%) pierden contra USDT y contra HODL BTC. En el Torneo, A7 hizo **récord: 1.035,77 (+3,58% en 48 h)**, y L9 también (1.018,66). **Se mandó un mail.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 882.16 | -11.78% | -4.46 pp (HODL -7.32%) | -3.43% (HODL -4.46%) | -3.84% (HODL -4.67%) | -12.94% (HODL -9.63%) | 2.56 USD (2.2% de la pérdida) | 90 |
| Agresiva | 891.28 | -10.87% | -3.72 pp (HODL -7.15%) | -2.25% (HODL -4.52%) | -4.29% (HODL -4.32%) | -10.93% (HODL -9.82%) | 31.37 USD (28.9% de la pérdida) | 233 |
| Laboratorio | 991.57 | -0.84% | +3.40 pp (HODL -4.24%) | -0.84% (HODL -4.24%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1035.77 | +3.58% (48 h) | +6.98 pp (P1 HODL BTC -3.40%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento. La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último.
- **Frescura (ahora 00:55 UTC):** 3 niveles 00:07, Agresiva 00:32, Laboratorio 00:16 (todas < 1 h). DCA 27/10 22:38 (74 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 00:41 con última vela 00:00 (< 1 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 00:16 es 77.412 (80.841,96 × 0,95757). A ese precio su cuota de 0,0012356 BTC vale 95,65 y el total da **995,65 (-0,43%)**, contra -4,24% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,40%): A7 (+3,58%), L9 (+1,87%) y L4 (+0,40%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,89% mientras la estrategia P1 HODL BTC dice -3,40%. Hay que revisarlo en el torneo, no acá.
- **Récord del Torneo:** el máximo se sacó de todas las versiones de `vivo.json` en la historia de la rama (A7: 1.026,90 a las 08:00 del 30/10; L9: 1.013,03 a la misma hora).
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** -0,31% en 24 h (884,94 → 882,16), con HODL BTC -1,17%. Sin operaciones desde el stop de LTC del 30/10 00:18. Tiene 407,70 en USDT y está -12,4% abajo de su máximo de 1.006,50.
- **Agresiva:** -0,47% en 24 h (895,48 → 891,28), con HODL BTC +0,48%. Una operación nueva: salió de TRX a las 22:32 (-3,19%) porque el soporte no sostuvo. Comisiones: 31,37 USD, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h (991,57), con HODL BTC -0,46%. 100% en USDT desde el stop de HYPE del 29/10 23:43.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** A7 subió de 1.021,22 (último juez) a 1.035,77 y L9 de 1.002,34 a 1.018,66; L4 bajó un poco a 1.003,96. Las HODL (P1 a P3) van entre -3,2% y -3,8%.
- **Alarmas:** récord en el Torneo (A7 1.035,77, máximo histórico y arriba de 1.000). **Mail mandado a facue1900@gmail.com** (uno solo por el Torneo). Nadie llegó a +20%.

## Recomendación

- **3 niveles: apagar.** Lleva 23 días (≥14), está en -11,78% contra 0% de USDT y -7,32% de HODL BTC, y en 7 días hizo -3,84%: perdió algo menos que HODL (-4,67%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 23 días, está en -10,87% contra 0% de USDT y -7,15% de HODL, y en 7 días hizo -4,29% (HODL -4,32%): sigue cayendo. Pagó 31,37 USD de comisiones en 233 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +3,40 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,66%). Lleva 3 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera y hizo récord, pero son 48 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 23 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=1
