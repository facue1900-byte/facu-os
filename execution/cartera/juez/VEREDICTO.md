# Veredicto de las carpetas cripto — 2026-11-23 18:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **Laboratorio (-6,66%)** y **DCA BTC (-6,72%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-21,45%). **Agresiva ahora pierde contra HODL BTC (-1,45 pp):** compró XRP, ETH y SOL a las 14:32 y salió de las tres con pérdida. Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +6,06 pp (HODL -26,19%) | -12,56% (HODL -23,91%) | -0,64% (HODL -5,19%) | -20,64% (HODL -34,25%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 724,41 | -27,56% | **-1,45 pp** (HODL -26,11%) | -20,55% (HODL -24,01%) | -8,32% (HODL -5,19%) | -27,56% (HODL -34,07%) | 57,02 USD (20,7% de la pérdida) | 414 |
| Laboratorio | 933,43 | -6,66% | +17,29 pp (HODL -23,95%) | -6,66% (HODL -23,95%) | -2,31% (HODL -4,78%) | -8,08% (HODL -32,09%) | 4,86 USD (7,3% de la pérdida) | 27 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +21,45 pp (HODL BTC -21,45%; precio crudo -22,68%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +23,83 pp (HODL -24,86%) | -1,04% (HODL -22,31%) | +0,00% (HODL -2,32%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 23/11 18:51 UTC):** 3 niveles 18:06 (45 min) · Agresiva 18:32 (19 min) · Laboratorio 18:16 (35 min) · DCA 23/11 13:04 (5 h 48 min; límite 8 días; **apareció la compra semanal de hoy**) · Torneo `vivo.json` 16:41 (2 h 10 min; límite 8 h) · Original 23/11 16:09 (2 h 42 min; corre en la Mac). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -37,81%, peor caída -39,85%, 31 ops y 22,00 USD de comisiones. Promedio de las 33: -9,18% (antes -9,95%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -11,85%, Agresiva -21,52%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,66% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo. Agresiva marca su peor caída nueva (-27,56%).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 23/11 16:09 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.334 (-6,66%) | 9.318 (-6,82%) | 23/11 18:16 |
| Torneo (promedio) | 9.082 (-9,18%) | 9.082 (-9,18%) | 23/11 16:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 23/11 18:06 |
| Agresiva | 7.244 (-27,56%) | 7.943 (-20,57%) | 23/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.579 (-24,21%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.421 | -5,79% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.045 | -9,55% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.226 | -7,74% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.560 | -14,40% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.219.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Agresiva** (741,06 → 724,41 en 24 h, -2,25%): a las 14:32 compró XRP, ETH y SOL por momentum; BTC dio vuelta, saltó el stop de SOL (16:47) y a las 17:31 sacó XRP y ETH antes del stop. Quedó 100% en USDT, ahora por debajo de HODL BTC.
- **Laboratorio** (942,34 → 933,43, -0,95%): compró PEPE a las 14:16 (188,46 USD) y va -4,63%.
- **DCA BTC:** hizo la compra semanal de hoy (100 USD); 948,91 → 932,83 por la baja de BTC.
- **3 niveles y Original:** sin cambios, en USDT.
- **Torneo:** el promedio mejoró apenas (-9,95% → -9,18%) porque BTC bajó menos medido a las 16:00.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,13%, pero +6,06 pp contra HODL BTC; está 100% en USDT y mide bien.
- **Agresiva — seguir.** -27,56%, **-1,45 pp contra HODL BTC** y -8,32% en 7 días (HODL -5,19%). El 20,7% de la pérdida es comisión (414 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,66%, +17,29 pp contra HODL, peor caída -8,08%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL; la compra de los lunes llegó en fecha.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
