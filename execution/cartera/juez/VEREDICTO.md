# Veredicto de las carpetas cripto — 2026-11-24 06:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-6,84%)**. **3 niveles** mejora a -19,46% con el LISTA que compró anoche. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-24,64%). **Agresiva queda apenas debajo de HODL BTC (-0,21 pp).** Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 805,38 | -19,46% | +8,07 pp (HODL -27,53%) | -11,83% (HODL -25,30%) | +0,18% (HODL -6,67%) | -20,65% (HODL -34,25%) | 3,14 USD (1,6% de la pérdida) | 100 |
| Agresiva | 724,41 | -27,56% | **-0,21 pp** (HODL -27,35%) | -20,55% (HODL -25,29%) | -8,04% (HODL -6,20%) | -27,56% (HODL -34,07%) | 57,02 USD (20,7% de la pérdida) | 414 |
| Laboratorio | 931,63 | -6,84% | +18,38 pp (HODL -25,22%) | -6,84% (HODL -25,22%) | -2,50% (HODL -6,90%) | -8,25% (HODL -32,09%) | 5,03 USD (7,4% de la pérdida) | 28 |
| DCA BTC | 932,83 | -6,72% | +17,44 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +24,64 pp (HODL BTC -24,64%; precio crudo -25,82%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +23,82 pp (HODL -24,86%) | -1,04% (HODL -22,31%) | +0,00% (HODL -2,32%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 24/11 06:51 UTC):** 3 niveles 06:06 (45 min) · Agresiva 06:32 (19 min) · Laboratorio 06:16 (35 min) · DCA 23/11 13:04 (17 h 47 min; límite 8 días) · Torneo `vivo.json` 04:41 (2 h 10 min; límite 8 h) · Original 23/11 16:09 (14 h 42 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,03%, peor caída -39,85%, 31 ops y 22,00 USD de comisiones. Promedio de las 33: -10,25% (antes -9,94%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -11,89%, Agresiva -21,56%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,84% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo de carpeta. La posición de LISTA de 3 niveles tocó un máximo de 0,115 contra entrada 0,0888 (+29,5% sobre 30 USD).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 23/11 16:09 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.316 (-6,84%) | 9.300 (-7,00%) | 24/11 06:16 |
| Torneo (promedio) | 8.975 (-10,25%) | 8.975 (-10,25%) | 24/11 04:41 |
| 3 niveles | 8.054 (-19,46%) | 8.769 (-12,31%) | 24/11 06:06 |
| Agresiva | 7.244 (-27,56%) | 7.943 (-20,57%) | 24/11 06:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.441 (-25,59%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.382 | -6,18% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.036 | -9,64% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.245 | -7,55% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.524 | -14,76% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.197.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (798,73 → 805,38 en 24 h, +0,83%): el LISTA que compró a las 20:06 por 30 USD subió; el resto sigue en USDT (768,73).
- **Agresiva** (739,34 → 724,41, -2,02%): la pérdida son las ops de SOL, ETH y XRP de ayer a la tarde (compró 3×110 USD a las 14:32, vendió entre 16:47 y 17:31 en 315,38). Desde entonces quieta en USDT.
- **Laboratorio** (942,34 → 931,63, -1,14%): el PEPE de ayer salió por stop. 100% en USDT, sin ops desde el último veredicto.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes; Original publica desde la Mac).
- **Torneo:** el promedio empeoró (-9,94% → -10,25%) con la baja de BTC.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -19,46%, pero +8,07 pp contra HODL BTC; casi todo en USDT y mide bien.
- **Agresiva — seguir.** -27,56%, **-0,21 pp contra HODL BTC** y -8,04% en 7 días (HODL -6,20%). El 20,7% de la pérdida es comisión (414 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,84%, +18,38 pp contra HODL, peor caída -8,25%.
- **DCA BTC — seguir.** -6,72%, +17,44 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
