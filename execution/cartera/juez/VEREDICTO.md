# Veredicto de las carpetas cripto — 2026-11-27 12:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,06%)**, casi toda en USDT; atrás vienen **Laboratorio (-6,37%)** y **DCA BTC (-6,72%)**. **Agresiva** sigue **abajo de HODL BTC** (-28,37% contra -26,03%, -2,34 pp). **3 niveles** está en -20,36%, +5,76 pp sobre HODL. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-22,99%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 796,44 | -20,36% | +5,76 pp (HODL -26,12%) | -12,81% (HODL -23,84%) | -0,29% (HODL -0,22%) | -21,02% (HODL -34,25%) | 3,39 USD (1,7% de la pérdida) | 108 |
| Agresiva | 716,27 | -28,37% | **-2,34 pp** (HODL -26,03%) | -21,45% (HODL -23,94%) | -5,34% (HODL -0,05%) | -28,55% (HODL -34,07%) | 58,91 USD (20,8% de la pérdida) | 427 |
| Laboratorio | 936,27 | -6,37% | +17,38 pp (HODL -23,75%) | -6,37% (HODL -23,75%) | -0,64% (HODL -0,25%) | -8,28% (HODL -32,09%) | 5,22 USD (8,2% de la pérdida) | 29 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +22,99 pp (HODL BTC -22,99%; precio crudo -24,19%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.894,25 | -1,06% | +25,25 pp (HODL -26,30%) | -1,06% (HODL -23,80%) | -0,02% (HODL -0,57%) | -1,25% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 27/11 12:52 UTC):** 3 niveles 12:06 (46 min) · Agresiva 12:32 (20 min) · Laboratorio 12:16 (36 min) · DCA 23/11 13:04 (3 d 23 h 48 min; límite 8 días) · Torneo `vivo.json` 12:41 (11 min; límite 8 h) · Original 27/11 11:52 (1 h; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -36,83%, peor caída -39,85%, 35 ops y 24,42 USD de comisiones. Promedio de las 33: -9,67% (antes -9,76%).
- **Original:** 7.496 USD en USDT y ~2.398 USD en posiciones (3 ops). No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,38%, Agresiva -22,26%, Original -1,06%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,39% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.894 (-1,06%) | 9.897 (-1,03%) | 27/11 11:52 |
| Laboratorio | 9.363 (-6,37%) | 9.346 (-6,54%) | 27/11 12:16 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Torneo (promedio) | 9.033 (-9,67%) | 9.033 (-9,67%) | 27/11 12:41 |
| 3 niveles | 7.964 (-20,36%) | 8.671 (-13,29%) | 27/11 12:06 |
| Agresiva | 7.163 (-28,37%) | 7.854 (-21,46%) | 27/11 12:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.586 (-24,14%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.418 | -5,82% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.022 | -9,78% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.215 | -7,85% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.506 | -14,94% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.317.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (797,06 → 796,44): sin operaciones nuevas desde la compra de BTC, ETH y BNB de las 02:06. 108 ops.
- **Agresiva** (717,16 → 716,27): sigue con el HYPE de las 02:32; sin operaciones nuevas. 427 ops; el 20,8% de lo perdido es comisión.
- **Laboratorio** (936,46 → 936,27): sigue con el NEAR del 25/11; sin operaciones nuevas.
- **DCA BTC:** sin cambios; compra los lunes, la próxima el 30/11.
- **Original** (9.893,30 → 9.894,25): sin operaciones nuevas.
- **Torneo:** promedio de -9,76% a -9,67%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,36%, pero +5,76 pp contra HODL BTC; mide bien.
- **Agresiva — seguir.** -28,37%, **-2,34 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-5,34%) también (HODL -0,05%). El 20,8% de la pérdida es comisión (427 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,37%, +17,38 pp contra HODL, peor caída -8,28%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3, -36,83%) son las que más pierden.
- **Original — seguir.** -1,06%, la mejor de todas, pero porque estuvo en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
