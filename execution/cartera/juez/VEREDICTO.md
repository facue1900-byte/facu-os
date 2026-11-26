# Veredicto de las carpetas cripto — 2026-11-26 06:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**, porque está en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-6,76%)**. **Agresiva** sigue **abajo de HODL BTC** (-27,59% contra -27,14%, -0,45 pp). **3 niveles** perdió otra entrada chica (MMT, stop -13,22%) y vuelve a estar 100% en USDT, en -20,49%. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-24,09%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 795,07 | -20,49% | +6,82 pp (HODL -27,31%) | -12,96% (HODL -25,07%) | -1,10% (HODL -4,52%) | -21,01% (HODL -34,25%) | 3,27 USD (1,6% de la pérdida) | 105 |
| Agresiva | 724,10 | -27,59% | **-0,45 pp** (HODL -27,14%) | -20,59% (HODL -25,08%) | -7,01% (HODL -4,38%) | -27,99% (HODL -34,07%) | 57,76 USD (20,9% de la pérdida) | 419 |
| Laboratorio | 932,36 | -6,76% | +18,38 pp (HODL -25,15%) | -6,76% (HODL -25,15%) | -2,30% (HODL -4,69%) | -8,28% (HODL -32,09%) | 5,22 USD (7,7% de la pérdida) | 29 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +24,09 pp (HODL BTC -24,09%; precio crudo -25,28%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +26,74 pp (HODL -27,78%) | -1,04% (HODL -25,32%) | +0,00% (HODL -3,54%) | -1,22% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 26/11 06:52 UTC):** 3 niveles 06:06 (46 min) · Agresiva 06:31 (21 min) · Laboratorio 06:16 (36 min) · DCA 23/11 13:04 (2 d 17 h 48 min; límite 8 días) · Torneo `vivo.json` 04:41 (2 h 11 min; límite 8 h) · Original 25/11 23:20 (7 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,33%, peor caída -39,85%, 33 ops y 23,20 USD de comisiones. Promedio de las 33: -10,13% (antes -10,29%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,16%, Agresiva -20,73%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,76% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 25/11 23:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.324 (-6,76%) | 9.307 (-6,93%) | 26/11 06:16 |
| Torneo (promedio) | 8.987 (-10,13%) | 8.987 (-10,13%) | 26/11 04:41 |
| 3 niveles | 7.951 (-20,49%) | 8.656 (-13,44%) | 26/11 06:06 |
| Agresiva | 7.241 (-27,59%) | 7.940 (-20,60%) | 26/11 06:31 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.464 (-25,36%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.389 | -6,11% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.020 | -9,80% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.212 | -7,88% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.527 | -14,73% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.167.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (798,28 → 795,07): compró MMT a las 02:06 (24 USD, momentum) y saltó el stop a las 04:21 (-13,22%). De nuevo 100% en USDT. 105 ops.
- **Agresiva** (728,36 → 724,10): sin operaciones nuevas; sigue con ETH, ZEC y NEAR abiertas y 265,84 en USDT. El 20,9% de lo perdido es comisión.
- **Laboratorio** (934,01 → 932,36): sigue con el NEAR de las 22:17 del 25/11; sin operaciones nuevas.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes, la próxima el 30/11; Original en USDT).
- **Torneo:** el promedio mejoró de -10,29% a -10,13%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,49%, pero +6,82 pp contra HODL BTC; mide bien. Las entradas chicas de momentum (OPG, MMT) vienen saltando por stop.
- **Agresiva — seguir.** -27,59%, **-0,45 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-7,01%) también (HODL -4,38%). El 20,9% de la pérdida es comisión (419 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,76%, +18,38 pp contra HODL, peor caída -8,28%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
