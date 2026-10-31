# Veredicto de las carpetas cripto — 2026-10-31 18:55 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,39% al precio de hoy). El Laboratorio (-0,84%) va +2,98 pp arriba de HODL BTC. 3 niveles (-11,73%) y Agresiva (-10,78%) pierden contra USDT y contra HODL BTC. En el Torneo A7 marca **récord** (1.043,91, +4,39% en 64 h), pero el aviso de récord del Torneo ya salió hoy: **no se mandó mail.**

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 882.74 | -11.73% | -4.88 pp (HODL -6.85%) | -3.37% (HODL -3.97%) | -2.58% (HODL -3.18%) | -12.94% (HODL -9.63%) | 2.60 USD (2.2% de la pérdida) | 91 |
| Agresiva | 892.16 | -10.78% | -4.18 pp (HODL -6.61%) | -2.16% (HODL -3.96%) | -3.34% (HODL -3.28%) | -10.93% (HODL -9.82%) | 31.64 USD (29.3% de la pérdida) | 235 |
| Laboratorio | 991.57 | -0.84% | +2.98 pp (HODL -3.82%) | -0.84% (HODL -3.82%) | falta (arrancó 27/10) | -2.35% (HODL -5.66%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | falta (un solo snapshot, 22:38) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder A7 top 5 por 90 d (3 de 33 le ganan a USDT y a HODL BTC) | 1043.91 | +4.39% (64 h) | +7.48 pp (P1 HODL BTC -3.09%) | falta (arrancó 29/10 00:00) | falta | -3.60% | 0.98 USD | 5 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). La DCA tiene un solo snapshot (22:38) y el Torneo arrancó después, así que ninguno de los dos entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (24/10 18:06 y 18:31).
- **Frescura (ahora 18:55 UTC):** 3 niveles 18:07, Agresiva 18:32, Laboratorio 18:17 (todas < 1 h). DCA 27/10 22:38 (92 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 16:41 con última vela 16:00 (< 3 h; límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** el BTC que implica el HODL del Laboratorio a las 18:17 es 77.753 (80.841,96 × 0,96179). A ese precio su cuota de 0,0012356 BTC vale 96,07 y el total da **996,07 (-0,39%)**, contra -3,82% de HODL BTC. Cálculo propio, no snapshot oficial; la tabla deja el oficial.
- **Torneo:** 3 de 33 están arriba de 1.000 y del HODL BTC de P1 (-3,09%): A7 (+4,39%), L9 (+2,11%) y L4 (+0,72%). Ninguna llega a +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,58% mientras la estrategia P1 HODL BTC dice -3,09%. Hay que revisarlo en el torneo, no acá.
- **Récords del Torneo:** el máximo previo sale de las 14 versiones anteriores de `vivo.json` en la historia de la rama. Las tres superan su máximo: A7 1.043,91 (máx. previo 1.035,77), L9 1.021,07 (1.018,79), L4 1.007,15 (1.004,79). `alertas.json` ya tiene el récord del Torneo avisado el 31/10: no se repite el mail hoy.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- La peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo; la de HODL BTC, de su propia columna. Comisiones y ops salen del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.

## Qué pasó desde ayer

- **3 niveles:** +0,24% en 24 h (880,65 → 882,74), con HODL BTC +0,80%. Una operación nueva: a las 10:06 vendió HYPE (36,07 USD) por tesis invalidada. Tiene 443,73 en USDT y está -12,3% abajo de su máximo de 1.006,50.
- **Agresiva:** +0,08% en 24 h (891,43 → 892,16), con HODL BTC +1,11%. Volvió a entrar: a las 16:32 compró NEAR por 110 USD (momentum 24 h). Antes, a las 02:32, había vendido ETH. Comisiones: 31,64 USD, el 29% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h (991,57), con HODL BTC +0,95%. 100% en USDT desde el stop de HYPE del 29/10 23:43: no perdió, pero tampoco agarró el rebote.
- **DCA BTC:** sin cambios; la próxima cuota es el lunes 02/11.
- **Torneo:** sube desde el juez de las 12:55: A7 1.031,84 → 1.043,91, L9 1.017,41 → 1.021,07, L4 1.004,77 → 1.007,15. Las tres en máximo.
- **Alarmas:** récord en el Torneo (A7, L9, L4), ya avisado hoy → sin mail. Nadie llegó a +20%. Las demás carpetas están debajo de su capital: no hay récord posible.

## Recomendación

- **3 niveles: apagar.** Lleva 24 días (≥14), está en -11,73% contra 0% de USDT y -6,85% de HODL BTC, y en 7 días hizo -2,58%: perdió algo menos que HODL (-3,18%) pero no mejoró, siguió cayendo. Lo decide Facu.
- **Agresiva: apagar.** Lleva 24 días, está en -10,78% contra 0% de USDT y -6,61% de HODL, y en 7 días hizo -3,34% (HODL -3,28%): sigue cayendo, peor que HODL. Pagó 31,64 USD de comisiones en 235 operaciones. Lo decide Facu.
- **Laboratorio: seguir.** -0,84%, abajo de USDT pero +2,98 pp arriba de HODL BTC, con peor caída (-2,35%) menor a la mitad de la de HODL (-5,66%). Lleva 4 días: todavía no se puede juzgar.
- **DCA BTC: seguir.** Una sola cuota; es la referencia barata contra la que se miden las demás.
- **Torneo: revisar.** A7 lidera y está en récord, pero son 64 h de datos y el `hodl_btc` de `vivo.json` no coincide con P1: falta mucho para creerle al ranking.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta con historia le gana a USDT, y las dos que llevan 24 días pierden más de 10%.

JUEZ_OK lider=Torneo A7 mejor_que_usdt=1 apagar=3 niveles,Agresiva avisos=0
