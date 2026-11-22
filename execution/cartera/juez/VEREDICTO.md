# Veredicto de las carpetas cripto — 2026-11-22 18:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-23,95%). Todas le ganan a HODL BTC, pero quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +7,05 pp (HODL -27,18%) | -12,56% (HODL -24,93%) | -0,64% (HODL -6,00%) | -20,64% (HODL -34,25%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 741,06 | -25,89% | +1,18 pp (HODL -27,08%) | -18,73% (HODL -25,01%) | -6,34% (HODL -6,02%) | -26,38% (HODL -34,07%) | 56,22 USD (21,7% de la pérdida) | 407 |
| Laboratorio | 942,34 | -5,77% | +19,04 pp (HODL -24,81%) | -5,77% (HODL -24,81%) | -1,38% (HODL -6,15%) | -7,22% (HODL -32,09%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +23,95 pp (HODL BTC -23,95%; precio crudo -25,14%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +25,68 pp (HODL -26,72%) | -1,04% (HODL -24,23%) | +0,00% (HODL -6,38%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv` (la DCA mide contra su último snapshot, del 16/11; por eso su HODL difiere).
- **Frescura (ahora 22/11 18:51 UTC):** 3 niveles 18:07 (44 min) · Agresiva 18:32 (19 min) · Laboratorio 18:16 (35 min) · DCA 16/11 13:06 (6 d 5 h 45 min; límite 8 días, le toca el lunes 23/11) · Torneo `vivo.json` 16:41 (2 h 10 min; límite 8 h) · Original 22/11 12:12 (6 h 39 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,86%, peor caída -39,85%, 29 ops y 20,79 USD de comisiones. Promedio de las 33: -10,16% (antes -10,15%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,66%, Agresiva -21,09%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -5,77% y -5,11%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo en esta corrida.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 22/11 12:12 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 22/11 18:16 |
| Torneo (promedio) | 8.984 (-10,16%) | 8.984 (-10,16%) | 22/11 16:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 22/11 18:07 |
| Agresiva | 7.411 (-25,89%) | 8.126 (-18,74%) | 22/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.477 (-25,23%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.428 | -5,72% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.100 | -9,00% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.262 | -7,38% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.639 | -13,61% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.114.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **BTC volvió a bajar un poco** desde la corrida de las 12:51: el HODL BTC de cada carpeta empeoró ~0,2–0,5 pp (en el Torneo, de -23,74% a -23,95%).
- **Agresiva:** de -25,96% a **-25,89%**. Una op más: vendió HYPE a las 18:32 (148,16 USD) por invalidación del momentum. Queda sólo con NEAR (~148 USD, ~20% invertido). Comisiones: 56,22 USD, el 21,7% de lo que perdió.
- **3 niveles, Laboratorio, DCA y Original** quietos (100% USDT; la DCA, con su BTC): mismo total.
- **Torneo:** casi igual (promedio -10,15% → -10,16%); los líderes siguen siendo los que no operaron.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,13%, pero +7,05 pp contra HODL BTC; está 100% en USDT y mide bien.
- **Agresiva — seguir.** -25,89%, apenas +1,18 pp contra HODL; el 21,7% de la pérdida es comisión y en 7 días perdió más que HODL (-6,34% vs -6,02%). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -5,77%, +19,04 pp contra HODL, peor caída -7,22%.
- **DCA BTC — seguir.** -5,11%, +15,41 pp contra HODL; le toca la compra del lunes 23/11.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
