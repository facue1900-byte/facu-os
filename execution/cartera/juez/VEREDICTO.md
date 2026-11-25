# Veredicto de las carpetas cripto — 2026-11-25 18:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**, porque está en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-6,84%)**. **Agresiva** volvió a entrar, ahora en ETH (175 USD a las 17:32), y está en -27,79%, apenas +0,57 pp sobre HODL BTC. **3 niveles** sigue con el OPG, en -19,94%. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-27,13%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 800,58 | -19,94% | +8,36 pp (HODL -28,30%) | -12,36% (HODL -26,08%) | -0,41% (HODL -5,22%) | -20,65% (HODL -34,25%) | 3,20 USD (1,6% de la pérdida) | 102 |
| Agresiva | 722,13 | -27,79% | +0,57 pp (HODL -28,35%) | -20,80% (HODL -26,33%) | -7,13% (HODL -6,11%) | -27,94% (HODL -34,07%) | 57,48 USD (20,7% de la pérdida) | 417 |
| Laboratorio | 931,63 | -6,84% | +19,09 pp (HODL -25,93%) | -6,84% (HODL -25,93%) | -1,34% (HODL -5,22%) | -8,25% (HODL -32,09%) | 5,03 USD (7,4% de la pérdida) | 28 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +27,13 pp (HODL BTC -27,13%; precio crudo -28,27%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +29,73 pp (HODL -30,76%) | -1,04% (HODL -28,41%) | +0,00% (HODL -9,21%) | -1,22% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 25/11 18:52 UTC):** 3 niveles 18:06 (46 min) · Agresiva 18:31 (21 min) · Laboratorio 18:16 (36 min) · DCA 23/11 13:04 (2 d 5 h 48 min; límite 8 días) · Torneo `vivo.json` 16:41 (2 h 11 min; límite 8 h) · Original 15:20 (3 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -39,19%, peor caída -39,85%, 31 ops y 22,00 USD de comisiones. Promedio de las 33: -11,17% (antes -11,05%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,00%, Agresiva -21,04%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,84% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo de carpeta.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 25/11 15:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.316 (-6,84%) | 9.300 (-7,00%) | 25/11 18:16 |
| Torneo (promedio) | 8.883 (-11,17%) | 8.883 (-11,17%) | 25/11 16:41 |
| 3 niveles | 8.006 (-19,94%) | 8.716 (-12,84%) | 25/11 18:06 |
| Agresiva | 7.221 (-27,79%) | 7.918 (-20,82%) | 25/11 18:31 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.362 (-26,38%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.355 | -6,45% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.008 | -9,92% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.226 | -7,74% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.484 | -15,16% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.081.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (24 h: ~801 → 800,58): mantiene el OPG que compró hoy a las 06:06 (24 USD); el resto en USDT (777,69). 102 ops.
- **Agresiva:** hoy 11:31 vendió el BTC por tiempo (-2,27%) y a las 17:32 compró ETH por 175 USD (rebote en soporte; stop 5%, salida por tiempo en 24 h). 417 ops; quedan 545,84 en USDT.
- **Laboratorio** (931,63 → 931,63): 100% en USDT; sin ops nuevas.
- **DCA BTC y Original:** sin cambios (DCA compra los lunes, la próxima el 30/11; Original en USDT).
- **Torneo:** el promedio empeoró de -11,05% a -11,17%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -19,94%, pero +8,36 pp contra HODL BTC; mide bien.
- **Agresiva — seguir.** -27,79%, apenas +0,57 pp contra HODL BTC, y en 7 días (-7,13%) le fue peor que a HODL (-6,11%). El 20,7% de la pérdida es comisión (417 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -6,84%, +19,09 pp contra HODL, peor caída -8,25%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3) son las que más pierden.
- **Original — seguir.** -1,04%, la mejor de todas, pero porque está en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
