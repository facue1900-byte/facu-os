# Veredicto de las carpetas cripto — 2026-11-26 12:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**, porque está en USDT; atrás vienen **Laboratorio (-6,70%)** y **DCA BTC (-6,72%)**, casi empatadas. **Agresiva** sigue **abajo de HODL BTC** (-27,67% contra -27,16%, -0,52 pp) y cerró ZEC por stop. **3 niveles** quieta en 100% USDT, en -20,49%. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-24,18%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 795,07 | -20,49% | +6,60 pp (HODL -27,09%) | -12,96% (HODL -24,84%) | -1,10% (HODL -4,73%) | -21,01% (HODL -34,25%) | 3,27 USD (1,6% de la pérdida) | 105 |
| Agresiva | 723,26 | -27,67% | **-0,52 pp** (HODL -27,16%) | -20,68% (HODL -25,09%) | -7,22% (HODL -4,98%) | -27,99% (HODL -34,07%) | 57,90 USD (20,9% de la pérdida) | 420 |
| Laboratorio | 932,98 | -6,70% | +18,24 pp (HODL -24,94%) | -6,70% (HODL -24,94%) | -2,19% (HODL -4,96%) | -8,28% (HODL -32,09%) | 5,22 USD (7,8% de la pérdida) | 29 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +24,18 pp (HODL BTC -24,18%; precio crudo -25,36%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +26,74 pp (HODL -27,78%) | -1,04% (HODL -25,32%) | +0,00% (HODL -3,54%) | -1,22% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 26/11 12:52 UTC):** 3 niveles 12:06 (46 min) · Agresiva 12:32 (20 min) · Laboratorio 12:16 (36 min) · DCA 23/11 13:04 (2 d 23 h 48 min; límite 8 días) · Torneo `vivo.json` 12:41 (11 min; límite 8 h) · Original 25/11 23:20 (13 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,12%, peor caída -39,85%, 33 ops y 23,20 USD de comisiones. Promedio de las 33: -10,16% (antes -10,13%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -11,91%, Agresiva -20,82%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,70% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 25/11 23:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.330 (-6,70%) | 9.313 (-6,87%) | 26/11 12:16 |
| Torneo (promedio) | 8.984 (-10,16%) | 8.984 (-10,16%) | 26/11 12:41 |
| 3 niveles | 7.951 (-20,49%) | 8.656 (-13,44%) | 26/11 12:06 |
| Agresiva | 7.233 (-27,67%) | 7.931 (-20,69%) | 26/11 12:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.486 (-25,14%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.390 | -6,10% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.019 | -9,81% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.212 | -7,88% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.523 | -14,77% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.188.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (795,07 → 795,07): sin operaciones desde el stop de MMT de las 04:21. 100% en USDT. 105 ops.
- **Agresiva** (724,10 → 723,26): saltó el stop de ZEC a las 06:47 (-1,90%, 137,20 USD). Quedan ETH y NEAR abiertas y 402,90 en USDT. 420 ops; el 20,9% de lo perdido es comisión.
- **Laboratorio** (932,36 → 932,98): sigue con el NEAR de las 22:17 del 25/11; sin operaciones nuevas.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes, la próxima el 30/11; Original en USDT).
- **Torneo:** el promedio empeoró apenas de -10,13% a -10,16%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,49%, pero +6,60 pp contra HODL BTC; mide bien. Las entradas chicas de momentum (OPG, MMT) vienen saltando por stop.
- **Agresiva — seguir.** -27,67%, **-0,52 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-7,22%) también (HODL -4,98%). El 20,9% de la pérdida es comisión (420 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,70%, +18,24 pp contra HODL, peor caída -8,28%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
