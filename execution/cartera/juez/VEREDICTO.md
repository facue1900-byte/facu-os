# Veredicto de las carpetas cripto — 2026-11-03 18:55 UTC

**En una línea:** la única que le gana a USDT sigue siendo el Torneo, con **L9 compra pánico en tendencia alcista** en +1,34% (4 de 33 estrategias en positivo, todas también arriba de HODL BTC). El resto pierde contra USDT (0%): Laboratorio (-0,84%), DCA (-0,38%) y Original (-1,04%) le ganan a HODL BTC; 3 niveles (-11,55%) y Agresiva (-11,75%) pierden contra los dos. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884,51 | -11,55% | -4,72 pp (HODL -6,83%) | -3,17% (HODL -3,96%) | -2,93% (HODL -3,51%) | -12,94% (HODL -9,67%) | 2,60 USD (2,3% de la pérdida) | 91 |
| Agresiva | 882,45 | -11,75% | -5,24 pp (HODL -6,52%) | -3,22% (HODL -3,87%) | -3,03% (HODL -3,46%) | -12,34% (HODL -9,82%) | 34,54 USD (29,4% de la pérdida) | 257 |
| Laboratorio | 991,57 | -0,84% | +3,06 pp (HODL -3,90%) | -0,84% (HODL -3,90%) | falta (arrancó 27/10 22:37) | -2,35% (HODL -6,13%) | 1,60 USD (19,0% de la pérdida) | 9 |
| DCA BTC | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | falta (arrancó 27/10) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder L9 compra pánico sólo en tendencia alcista, 14 monedas (4 de 33 le ganan a USDT y a HODL BTC) | 1.013,45 | +1,34% (5 d, desde 29/10) | +4,35 pp (P1 HODL BTC -3,01%) | falta (arrancó 29/10 00:00) | falta | -4,43% | 1,00 USD (7,4% de la ganancia) | 5 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +6,35 pp (HODL -7,39%) | -1,04% (HODL -4,24%) | -1,04% (HODL -3,99%) | -1,22% (HODL -9,44%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento.
- **Frescura (ahora 18:51 UTC):** 3 niveles 18:07, Agresiva 18:33, Laboratorio 18:17, DCA 02/11 13:56 (límite 8 días), Torneo `vivo.json` 16:41 (última vela 16:00), Original 03/11 15:20 (Mac). **Todas corren.**
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- **Torneo:** L9 (+1,34%), L8 (+0,58%), P7 (+0,39%) y D2 (+0,05%) en positivo; ninguna cerca de +20%; la peor, A3, -17,77%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,49% y la estrategia P1 HODL BTC dice -3,01%.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.
- Récords: ya no mandan mail. Para anotar: L9 en +1,34% es el máximo del Torneo hasta ahora (ruido, no evento).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 03/11 15:20 |
| Laboratorio | 9.916 (-0,84%) | 9.898 (-1,02%) | 03/11 18:17 |
| Torneo (promedio) | 9.846 (-1,54%) | 9.846 (-1,54%) | 03/11 16:41 |
| Agresiva | 8.824 (-11,75%) | 9.676 (-3,24%) | 03/11 18:33 |
| 3 niveles | 8.845 (-11,55%) | 9.630 (-3,70%) | 03/11 18:07 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.566 (-4,34%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.883 | -1,17% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.819 | -1,81% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.796 | -2,04% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.771 | -2,29% |

Torneo, 33 estrategias: mejor L9 compra pánico sólo en tendencia alcista, 14 monedas 10.134; peor A3 la que más subió en 7 d, rota cada día 8.223.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles:** +0,41% en 24 h, con HODL BTC +0,55%. Sin operaciones. 443,73 en USDT y 4 posiciones (BTC, ETH, BNB, XRP).
- **Agresiva:** +0,65% en 24 h, con HODL BTC +1,02%. 5 operaciones en 24 h (compra XRP, compra y venta de BTC, compra ETH, compra ZEC 18:32); quedan 3 posiciones (XRP, ETH, ZEC) y 486,94 en USDT. Las comisiones ya son el 29,4% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +0,53%. Sigue 100% en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes (02/11 13:56). 200 en BTC y 800 en USDT.
- **Torneo:** desde la corrida de las 12:55, L9 pasó de +0,52% a +1,34%; las que le ganan a USDT pasaron de 2 a 4 (se sumaron P7 y D2). Régimen: BTC arriba de la media 200, bajando 30 d.
- **Original:** dato nuevo de la Mac (03/11 15:20), sin cambios: 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -11,55% contra 0% de USDT y -6,83% de HODL BTC; en 7 días -2,93%, apenas mejor que HODL (-3,51%) pero igual pierde.
- **Agresiva: seguir.** -11,75%; en 7 días -3,03% (HODL -3,46%). 34,54 USD de comisiones en 257 operaciones (29,4% de la pérdida).
- **Laboratorio: seguir.** -0,84%, +3,06 pp sobre HODL BTC, peor caída -2,35% contra -6,13% de HODL.
- **DCA BTC: seguir.** -0,38%, la cuota semanal corre bien.
- **Torneo: revisar.** El líder L9 hace +1,34% en 5 días (muy poco para leer algo), y el `hodl_btc` de `vivo.json` (-4,49%) no coincide con P1 (-3,01%): la vara contra HODL no mide bien.
- **Original: seguir.** -1,04%, +6,35 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Torneo L9 mejor_que_usdt=1 apagar=ninguna avisos=0
