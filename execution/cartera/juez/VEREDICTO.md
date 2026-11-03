# Veredicto de las carpetas cripto — 2026-11-03 00:51 UTC

**En una línea:** ninguna carpeta le gana a quedarse en USDT (0%). En el Torneo la líder pasó a ser **P0 USDT quieto** (empatada con 3 que no operaron): ninguna de las 33 está en positivo. Laboratorio (-0,84%), DCA (-0,38%) y Original (-1,04%) le ganan a HODL BTC pero pierden contra USDT. 3 niveles (-12,17%) y Agresiva (-12,25%) pierden contra los dos. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 878,33 | -12,17% | -4,14 pp (HODL -8,02%) | -3,85% (HODL -5,19%) | -3,30% (HODL -4,30%) | -12,94% (HODL -9,63%) | 2,60 USD (2,1% de la pérdida) | 91 |
| Agresiva | 877,53 | -12,25% | -4,92 pp (HODL -7,33%) | -3,76% (HODL -4,70%) | -4,05% (HODL -3,94%) | -12,34% (HODL -9,82%) | 34,28 USD (28,0% de la pérdida) | 255 |
| Laboratorio | 991,57 | -0,84% | +4,04 pp (HODL -4,88%) | -0,84% (HODL -4,88%) | falta (arrancó 27/10 22:37) | -2,35% (HODL -5,68%) | 1,60 USD (19,0% de la pérdida) | 9 |
| DCA BTC | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | falta (arrancó 27/10) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder P0 USDT quieto (0 de 33 le ganan a USDT y a HODL BTC; la mejor que operó: L8, -0,10%) | 1.000,00 | 0,00% (120 h) | +4,09 pp (P1 HODL BTC -4,09%) | falta (arrancó 29/10 00:00) | falta | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +6,94 pp (HODL -7,97%) | -1,04% (HODL -4,85%) | -1,04% (HODL -4,02%) | -1,22% (HODL -9,17%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento.
- **Frescura (ahora 00:51 UTC):** 3 niveles 00:06, Agresiva 00:32, Laboratorio 00:16, DCA 02/11 13:56 (cuota del lunes cargada; límite 8 días), Torneo `vivo.json` 00:41 (última vela 00:00), Original 02/11 23:20 (Mac). **Todas corren.**
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- **Torneo:** 0 estrategias en positivo; 29 de 33 le ganan a P1 HODL BTC (-4,09%), pero ninguna a USDT. Máximo del torneo: 0,00%. Ninguna cerca de +20%; la peor, A3, -17,96%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -5,57% y la estrategia P1 HODL BTC dice -4,09%.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.
- Récords: ya no mandan mail y no se rastrean acá. Hoy no hay ninguno que anotar.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 02/11 23:20 |
| Laboratorio | 9.916 (-0,84%) | 9.898 (-1,02%) | 03/11 00:16 |
| Torneo (promedio) | 9.793 (-2,07%) | 9.793 (-2,07%) | 03/11 00:41 |
| Agresiva | 8.775 (-12,25%) | 9.622 (-3,78%) | 03/11 00:32 |
| 3 niveles | 8.783 (-12,17%) | 9.563 (-4,37%) | 03/11 00:06 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.444 (-5,56%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.867 | -1,33% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.790 | -2,10% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.770 | -2,30% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.729 | -2,71% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 8.204.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles:** -0,53% en 24 h, con HODL BTC -1,37%. Sin operaciones. 443,73 en USDT.
- **Agresiva:** -0,99% en 24 h, con HODL BTC -1,30%. 11 operaciones en 24 h: volvió a entrar en XRP (130 USD) y BTC (130 USD); BTC lo vendió a las 00:32 por invalidación. Queda 1 posición (XRP) y 746,94 en USDT. Las comisiones ya son el 28,0% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC -1,13%. Sigue 100% en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes (13:56). 200 en BTC y 800 en USDT.
- **Torneo:** el mercado siguió bajando y se borraron las ganancias: L9 pasó de +1,03% a -0,14% (peor caída -4,4%), A7 de +0,61% a -1,21%. Ahora ninguna de las 33 está arriba de USDT; la tabla la encabezan las 4 que no operaron. Régimen: BTC arriba de la media 200, bajando 30 d.
- **Original:** sin cambios (100% en USDT).
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -12,17% contra 0% de USDT y -8,02% de HODL BTC; en 7 días -3,30%, mejor que HODL (-4,30%) pero igual pierde.
- **Agresiva: seguir.** -12,25%, la peor; en 7 días -4,05%, peor que HODL (-3,94%). 34,28 USD de comisiones en 255 operaciones (28,0% de la pérdida).
- **Laboratorio: seguir.** -0,84%, +4,04 pp sobre HODL BTC, peor caída -2,35% contra -5,68% de HODL.
- **DCA BTC: seguir.** -0,38%, la cuota semanal corre bien.
- **Torneo: revisar.** Ninguna de las 33 le gana a USDT (máximo 0,00%), y el `hodl_btc` de `vivo.json` (-5,57%) no coincide con P1 (-4,09%): la vara contra HODL no mide bien.
- **Original: seguir.** -1,04%, +6,94 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Torneo P0 USDT quieto mejor_que_usdt=0 apagar=ninguna avisos=0
