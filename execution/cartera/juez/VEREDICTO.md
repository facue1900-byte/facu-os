# Veredicto de las carpetas cripto — 2026-11-24 18:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**, porque está en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-6,84%)**. **Agresiva** tiene BTC desde las 11:32 y sube a +0,31 pp sobre HODL BTC (-27,52% vs -27,83%). **3 niveles** quieta en USDT (-19,83%). En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-25,41%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 801,69 | -19,83% | +8,01 pp (HODL -27,84%) | -12,24% (HODL -25,61%) | -0,27% (HODL -5,67%) | -20,65% (HODL -34,25%) | 3,18 USD (1,6% de la pérdida) | 101 |
| Agresiva | 724,80 | -27,52% | +0,31 pp (HODL -27,83%) | -20,51% (HODL -25,79%) | -6,95% (HODL -5,93%) | -27,64% (HODL -34,07%) | 57,16 USD (20,8% de la pérdida) | 415 |
| Laboratorio | 931,63 | -6,84% | +18,79 pp (HODL -25,63%) | -6,84% (HODL -25,63%) | -1,79% (HODL -5,63%) | -8,25% (HODL -32,09%) | 5,03 USD (7,4% de la pérdida) | 28 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +25,41 pp (HODL BTC -25,41%; precio crudo -26,58%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +27,37 pp (HODL -28,41%) | -1,04% (HODL -25,97%) | +0,00% (HODL -7,95%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 24/11 18:51 UTC):** 3 niveles 18:06 (45 min) · Agresiva 18:32 (19 min) · Laboratorio 18:16 (35 min) · DCA 23/11 13:04 (1 d 5 h 47 min; límite 8 días) · Torneo `vivo.json` 16:41 (2 h 10 min; límite 8 h) · Original 24/11 15:20 (3 h 31 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,44%, peor caída -39,85%, 31 ops y 22,00 USD de comisiones. Promedio de las 33: -10,63% (antes -10,24%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,17%, Agresiva -21,80%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,84% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo de carpeta.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 24/11 15:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.316 (-6,84%) | 9.300 (-7,00%) | 24/11 18:16 |
| Torneo (promedio) | 8.937 (-10,63%) | 8.937 (-10,63%) | 24/11 16:41 |
| 3 niveles | 8.017 (-19,83%) | 8.728 (-12,72%) | 24/11 18:06 |
| Agresiva | 7.248 (-27,52%) | 7.947 (-20,53%) | 24/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.409 (-25,91%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.371 | -6,29% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.024 | -9,76% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.233 | -7,67% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.515 | -14,85% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.156.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (798,73 → 801,69 en 24 h, +0,37%): la venta del LISTA de hoy 06:31 (+10%) es lo único. 100% en USDT, sin ops desde entonces.
- **Agresiva** (724,41 → 724,80, +0,05%): tiene BTC (comprado 11:32 a 59.836) y USDT 579,41; sin ops nuevas (415). Sigue -6,95% en 7 días contra -5,93% de HODL.
- **Laboratorio** (933,43 → 931,63, -0,19%): el PEPE salió por stop; 100% en USDT, sin ops nuevas.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes; Original en USDT).
- **Torneo:** el promedio bajó de -10,24% a -10,63% con BTC más abajo (HODL -25,41%).
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -19,83%, pero +8,01 pp contra HODL BTC; todo en USDT y mide bien.
- **Agresiva — seguir.** -27,52%, apenas +0,31 pp contra HODL BTC y -6,95% en 7 días (HODL -5,93%). El 20,8% de la pérdida es comisión (415 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,84%, +18,79 pp contra HODL, peor caída -8,25%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
