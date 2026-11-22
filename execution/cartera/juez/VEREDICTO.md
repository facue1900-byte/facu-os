# Veredicto de las carpetas cripto — 2026-11-22 06:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-25,86%). Todas le ganan a HODL BTC, pero quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +9,06 pp (HODL -29,18%) | -12,56% (HODL -27,00%) | -0,64% (HODL -8,07%) | -20,64% (HODL -34,25%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 736,22 | -26,38% | +2,70 pp (HODL -29,07%) | -19,26% (HODL -27,06%) | -6,93% (HODL -8,49%) | -26,38% (HODL -34,07%) | 55,63 USD (21,1% de la pérdida) | 403 |
| Laboratorio | 942,34 | -5,77% | +21,10 pp (HODL -26,86%) | -5,77% (HODL -26,86%) | -1,38% (HODL -8,15%) | -7,22% (HODL -32,09%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +25,86 pp (HODL BTC -25,86%; precio crudo -27,03%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +27,91 pp (HODL -28,94%) | -1,04% (HODL -26,53%) | +0,00% (HODL -8,53%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv` (la DCA mide contra su último snapshot, del 16/11; por eso su HODL difiere).
- **Frescura (ahora 22/11 06:51 UTC):** 3 niveles 06:06 (45 min) · Agresiva 06:32 (19 min) · Laboratorio 06:16 (35 min) · DCA 16/11 13:06 (5 d 17 h 45 min; límite 8 días, le toca el lunes 23/11) · Torneo `vivo.json` 04:41 (2 h 10 min; límite 8 h) · Original 22/11 03:59 (2 h 52 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops; atrás L7 (-0,24%). La peor es A3: -39,23%, peor caída -39,85%, 29 ops y 20,79 USD de comisiones. Promedio de las 33: -10,80% (antes -10,45%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,87%, Agresiva -21,50%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -5,77% y -5,11%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** la peor caída de la Agresiva pasó de -26,28% a **-26,38%** (último snapshot, 06:32).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 22/11 03:59 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 22/11 06:16 |
| Torneo (promedio) | 8.920 (-10,80%) | 8.920 (-10,80%) | 22/11 04:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 22/11 06:06 |
| Agresiva | 7.362 (-26,38%) | 8.073 (-19,27%) | 22/11 06:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.271 (-27,29%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.408 | -5,92% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.081 | -9,19% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.257 | -7,43% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.594 | -14,06% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.077.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Agresiva** sigue perdiendo de a poco: de -26,28% a **-26,38%** (2 ops más: vendió UNI a la 01:32 y volvió a comprar ZEC a las 06:32, con ~20% invertido). En 7 días hizo -6,93% contra -8,49% de HODL BTC. Las comisiones ya son 55,63 USD, el 21,1% de lo que perdió.
- **3 niveles, Laboratorio, DCA y Original** quietos en USDT (la DCA, con su BTC): mismo total que la corrida anterior.
- **Torneo:** el promedio empeoró (-10,45% → -10,80%) porque BTC volvió a bajar; los líderes siguen siendo los que no operaron.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,13%, pero +9,06 pp contra HODL BTC; está 100% en USDT y mide bien.
- **Agresiva — seguir.** -26,38%, apenas +2,70 pp contra HODL; el 21% de la pérdida es comisión. El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -5,77%, +21,10 pp contra HODL, peor caída -7,22%.
- **DCA BTC — seguir.** -5,11%, +15,41 pp contra HODL; le toca la compra del lunes 23/11.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
