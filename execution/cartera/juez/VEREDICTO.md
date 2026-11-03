# Veredicto de las carpetas cripto — 2026-11-03 12:55 UTC

**En una línea:** la única que asoma arriba de USDT es el Torneo, con **L9 compra pánico en tendencia alcista** en +0,52% (2 de 33 estrategias en positivo, ambas también arriba de HODL BTC). El resto de las carpetas pierde contra USDT (0%): Laboratorio (-0,84%), DCA (-0,38%) y Original (-1,04%) le ganan a HODL BTC; 3 niveles (-11,99%) y Agresiva (-11,89%) pierden contra los dos. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 880,07 | -11,99% | -4,34 pp (HODL -7,65%) | -3,66% (HODL -4,80%) | -2,49% (HODL -3,23%) | -12,94% (HODL -9,67%) | 2,60 USD (2,2% de la pérdida) | 91 |
| Agresiva | 881,13 | -11,89% | -4,88 pp (HODL -7,01%) | -3,37% (HODL -4,38%) | -3,54% (HODL -3,19%) | -12,34% (HODL -9,82%) | 34,41 USD (29,0% de la pérdida) | 256 |
| Laboratorio | 991,57 | -0,84% | +3,58 pp (HODL -4,42%) | -0,84% (HODL -4,42%) | falta (arrancó 27/10 22:37) | -2,35% (HODL -6,13%) | 1,60 USD (19,0% de la pérdida) | 9 |
| DCA BTC | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | falta (arrancó 27/10) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder L9 compra pánico sólo en tendencia alcista, 14 monedas (2 de 33 le ganan a USDT y a HODL BTC) | 1.005,21 | +0,52% (5 d, desde 29/10) | +4,25 pp (P1 HODL BTC -3,73%) | falta (arrancó 29/10 00:00) | falta | -4,43% | 1,00 USD (19,2% de la ganancia) | 5 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +6,52 pp (HODL -7,56%) | -1,04% (HODL -4,42%) | -1,04% (HODL -3,76%) | -1,22% (HODL -9,44%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento.
- **Frescura (ahora 12:55 UTC):** 3 niveles 12:06, Agresiva 12:32, Laboratorio 12:18, DCA 02/11 13:56 (límite 8 días), Torneo `vivo.json` 12:41 (última vela 12:00), Original 03/11 12:17 (Mac). **Todas corren.**
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- **Torneo:** L9 (+0,52%) y L8 (+0,11%) en positivo; 29 de 33 le ganan a P1 HODL BTC (-3,73%). Ninguna cerca de +20%; la peor, A3, -17,84%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -5,21% y la estrategia P1 HODL BTC dice -3,73%.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.
- Récords: ya no mandan mail. Para anotar: L9 en +0,52% es el máximo del Torneo en esta corrida (ruido, no evento).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 03/11 12:17 |
| Laboratorio | 9.916 (-0,84%) | 9.898 (-1,02%) | 03/11 12:18 |
| Torneo (promedio) | 9.814 (-1,86%) | 9.814 (-1,86%) | 03/11 12:41 |
| Agresiva | 8.811 (-11,89%) | 9.662 (-3,38%) | 03/11 12:32 |
| 3 niveles | 8.801 (-11,99%) | 9.582 (-4,18%) | 03/11 12:06 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.482 (-5,18%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.873 | -1,27% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.803 | -1,97% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.780 | -2,20% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.755 | -2,45% |

Torneo, 33 estrategias: mejor L9 compra pánico sólo en tendencia alcista, 14 monedas 10.052; peor A3 la que más subió en 7 d, rota cada día 8.216.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles:** -0,54% en 24 h, con HODL BTC -1,24%. Sin operaciones. 443,73 en USDT y 4 posiciones (BTC, ETH, BNB, XRP).
- **Agresiva:** -0,23% en 24 h, con HODL BTC -0,59%. 9 operaciones en 24 h; quedan 2 posiciones (XRP, ETH) y 616,94 en USDT. Las comisiones ya son el 29,0% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC -0,96%. Sigue 100% en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes (02/11 13:56). 200 en BTC y 800 en USDT.
- **Torneo:** desde la corrida de las 06:55, L9 pasó de abajo a +0,52% y L8 a +0,11%: por primera vez desde el 02/11 hay estrategias arriba de USDT. Régimen: BTC arriba de la media 200, bajando 30 d.
- **Original:** dato nuevo de la Mac (03/11 12:17), sin cambios: 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -11,99% contra 0% de USDT y -7,65% de HODL BTC; en 7 días -2,49%, mejor que HODL (-3,23%) pero igual pierde.
- **Agresiva: seguir.** -11,89%; en 7 días -3,54%, peor que HODL (-3,19%). 34,41 USD de comisiones en 256 operaciones (29,0% de la pérdida).
- **Laboratorio: seguir.** -0,84%, +3,58 pp sobre HODL BTC, peor caída -2,35% contra -6,13% de HODL.
- **DCA BTC: seguir.** -0,38%, la cuota semanal corre bien.
- **Torneo: revisar.** El líder L9 hace +0,52% en 5 días (muy poco para leer algo), y el `hodl_btc` de `vivo.json` (-5,21%) no coincide con P1 (-3,73%): la vara contra HODL no mide bien.
- **Original: seguir.** -1,04%, +6,52 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Torneo L9 mejor_que_usdt=1 apagar=ninguna avisos=0
