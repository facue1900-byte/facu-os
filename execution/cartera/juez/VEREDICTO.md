# Veredicto de las carpetas cripto — 2026-11-26 18:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**, porque está en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-6,74%)**, casi empatadas. **Agresiva** se aleja **abajo de HODL BTC** (-28,40% contra -27,13%, -1,28 pp) tras dos stops y dos salidas anticipadas en el día. **3 niveles** quieta en 100% USDT, en -20,49%. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-24,29%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 795,07 | -20,49% | +6,95 pp (HODL -27,45%) | -12,96% (HODL -25,21%) | -1,02% (HODL -3,54%) | -21,01% (HODL -34,25%) | 3,27 USD (1,6% de la pérdida) | 105 |
| Agresiva | 715,96 | -28,40% | **-1,28 pp** (HODL -27,13%) | -21,48% (HODL -25,07%) | -6,93% (HODL -4,10%) | -28,50% (HODL -34,07%) | 58,63 USD (20,6% de la pérdida) | 425 |
| Laboratorio | 932,61 | -6,74% | +18,44 pp (HODL -25,18%) | -6,74% (HODL -25,18%) | -1,51% (HODL -3,71%) | -8,28% (HODL -32,09%) | 5,22 USD (7,7% de la pérdida) | 29 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +24,29 pp (HODL BTC -24,29%; precio crudo -25,48%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +26,71 pp (HODL -27,75%) | -1,04% (HODL -25,30%) | +0,00% (HODL -4,54%) | -1,22% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 26/11 18:52 UTC):** 3 niveles 18:06 (46 min) · Agresiva 18:32 (20 min) · Laboratorio 18:16 (36 min) · DCA 23/11 13:04 (3 d 5 h 48 min; límite 8 días) · Torneo `vivo.json` 16:42 (2 h 10 min; límite 8 h) · Original 26/11 15:20 (3 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,39%, peor caída -39,85%, 33 ops y 23,20 USD de comisiones. Promedio de las 33: -10,26% (antes -10,16%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,71%, Agresiva -21,32%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,74% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 26/11 15:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.326 (-6,74%) | 9.309 (-6,91%) | 26/11 18:16 |
| Torneo (promedio) | 8.974 (-10,26%) | 8.974 (-10,26%) | 26/11 16:42 |
| 3 niveles | 7.951 (-20,49%) | 8.656 (-13,44%) | 26/11 18:06 |
| Agresiva | 7.160 (-28,40%) | 7.851 (-21,49%) | 26/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.450 (-25,50%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.386 | -6,14% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.003 | -9,97% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.204 | -7,96% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.479 | -15,21% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.161.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (795,07 → 795,07): sin operaciones desde el stop de MMT de las 04:21. 100% en USDT. 105 ops.
- **Agresiva** (723,26 → 715,96, -1,01% desde el veredicto de las 12:52): compró SOL a las 14:32; saltó el stop de NEAR a las 15:07; a las 17:31 salió de ETH por tiempo (24 h sin llegar a +8%) y de SOL por invalidación de la tesis; a las 18:32 volvió a comprar NEAR (140 USD a 3,098, más caro que el stop de 2,981). 425 ops; el 20,6% de lo perdido es comisión.
- **Laboratorio** (932,98 → 932,61): sigue con el NEAR del 25/11 22:17; sin operaciones nuevas.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes, la próxima el 30/11; Original en USDT).
- **Torneo:** el promedio empeoró de -10,16% a -10,26%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,49%, pero +6,95 pp contra HODL BTC; mide bien. Las entradas chicas de momentum (LISTA, OPG, MMT) vienen saltando por stop.
- **Agresiva — seguir.** -28,40%, **-1,28 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-6,93%) también (HODL -4,10%). El 20,6% de la pérdida es comisión (425 ops) y hoy vendió NEAR por stop para recomprarlo 3,9% más caro tres horas después. El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,74%, +18,44 pp contra HODL, peor caída -8,28%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
