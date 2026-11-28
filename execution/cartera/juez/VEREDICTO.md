# Veredicto de las carpetas cripto — 2026-11-28 00:55 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,74%)**, casi toda en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-7,14%)**. **Agresiva** sigue **abajo de HODL BTC** (-28,87% contra -27,91%, -0,96 pp). **3 niveles** está en -20,68%, +7,42 pp sobre HODL. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-25,16%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 793,23 | -20,68% | +7,42 pp (HODL -28,10%) | -13,16% (HODL -25,88%) | -0,69% (HODL +1,54%) | -21,23% (HODL -34,25%) | 3,39 USD (1,6% de la pérdida) | 108 |
| Agresiva | 711,26 | -28,87% | **-0,96 pp** (HODL -27,91%) | -22,00% (HODL -25,87%) | -4,90% (HODL +1,55%) | -28,87% (HODL -34,07%) | 59,05 USD (20,4% de la pérdida) | 428 |
| Laboratorio | 928,58 | -7,14% | +18,67 pp (HODL -25,81%) | -7,14% (HODL -25,81%) | -1,46% (HODL +1,69%) | -8,55% (HODL -32,09%) | 5,40 USD (7,6% de la pérdida) | 30 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +25,16 pp (HODL BTC -25,16%; precio crudo -26,33%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.825,91 | -1,74% | +26,66 pp (HODL -28,40%) | -1,74% (HODL -25,97%) | -0,71% (HODL +1,27%) | -2,05% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 28/11 00:52 UTC):** 3 niveles 00:05 (47 min) · Agresiva 00:32 (20 min) · Laboratorio 00:16 (36 min) · DCA 23/11 13:04 (4 d 11 h 48 min; límite 8 días) · Torneo `vivo.json` 00:41 (11 min; límite 8 h) · Original 27/11 23:20 (1 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -36,04%, peor caída -39,85%, 35 ops y 24,42 USD de comisiones. Promedio de las 33: -10,33% (antes -10,42%).
- **Original:** 7.496 USD en USDT y el resto en posiciones (3 ops). No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,64%, Agresiva -22,28%, Original -1,71%; Laboratorio y DCA (menos de 30 días, desde el inicio) -7,31% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.826 (-1,74%) | 9.829 (-1,71%) | 27/11 23:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.286 (-7,14%) | 9.269 (-7,31%) | 28/11 00:16 |
| Torneo (promedio) | 8.967 (-10,33%) | 8.967 (-10,33%) | 28/11 00:41 |
| 3 niveles | 7.932 (-20,68%) | 8.636 (-13,64%) | 28/11 00:05 |
| Agresiva | 7.113 (-28,87%) | 7.799 (-22,01%) | 28/11 00:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.383 (-26,17%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.347 | -6,53% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 8.972 | -10,28% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.156 | -8,44% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.444 | -15,56% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.396.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (795,07 → 793,23): sin operaciones nuevas; sigue con BTC, ETH y BNB. 108 ops.
- **Agresiva** (714,60 → 711,26): sigue 100% en USDT desde la venta del HYPE del 27/11 15:00. 428 ops; el 20,4% de lo perdido es comisión.
- **Laboratorio** (931,94 → 928,58): sigue 100% en USDT desde la venta del NEAR del 27/11 16:16. 30 ops.
- **DCA BTC:** sin cambios; compra los lunes, la próxima el 30/11.
- **Original** (9.896,38 → 9.825,91): sin operaciones nuevas; bajó por las posiciones abiertas.
- **Torneo:** promedio de -10,42% a -10,33%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,68%, pero +7,42 pp contra HODL BTC; mide bien.
- **Agresiva — seguir.** -28,87%, **-0,96 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-4,90%) también (HODL +1,55%). El 20,4% de la pérdida es comisión (428 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -7,14%, +18,67 pp contra HODL, peor caída -8,55%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3, -36,04%) son las que más pierden.
- **Original — seguir.** -1,74%, la mejor de todas, pero porque estuvo en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
