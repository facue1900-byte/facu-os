# Veredicto de las carpetas cripto — 2026-11-27 18:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,87%)**, casi toda en USDT; atrás vienen **DCA BTC (-6,72%)** y **Laboratorio (-7,14%)**. **Agresiva** sigue **abajo de HODL BTC** (-28,87% contra -28,05%, -0,82 pp). **3 niveles** está en -20,69%, +7,55 pp sobre HODL. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% sin operar: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-24,92%). Quedarse quieto en USDT rinde más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 793,10 | -20,69% | +7,55 pp (HODL -28,23%) | -13,18% (HODL -26,02%) | -0,70% (HODL +1,40%) | -21,20% (HODL -34,25%) | 3,39 USD (1,6% de la pérdida) | 108 |
| Agresiva | 711,26 | -28,87% | **-0,82 pp** (HODL -28,05%) | -22,00% (HODL -26,01%) | -4,78% (HODL +1,55%) | -28,87% (HODL -34,07%) | 59,05 USD (20,4% de la pérdida) | 428 |
| Laboratorio | 928,58 | -7,14% | +18,77 pp (HODL -25,91%) | -7,14% (HODL -25,91%) | -1,46% (HODL +1,54%) | -8,55% (HODL -32,09%) | 5,40 USD (7,6% de la pérdida) | 30 |
| DCA BTC | 932,83 | -6,72% | +17,45 pp (HODL -24,16%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -5,29% (HODL -16,61%; base 10/11 18:33) | -6,72% (HODL -24,17%) | 0,50 USD (0,7% de la pérdida) | 5 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +24,92 pp (HODL BTC -24,92%; precio crudo -26,09%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.813,16 | -1,87% | +26,93 pp (HODL -28,80%) | -1,87% (HODL -26,38%) | -0,84% (HODL -1,47%) | -2,05% (HODL -31,58%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último (para la DCA, que es semanal, cae en el del 10/11).
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv`; por eso los HODL difieren según la hora del último snapshot.
- **Frescura (ahora 27/11 18:52 UTC):** 3 niveles 18:06 (46 min) · Agresiva 18:32 (20 min) · Laboratorio 18:16 (36 min) · DCA 23/11 13:04 (4 d 5 h 48 min; límite 8 días) · Torneo `vivo.json` 16:42 (2 h 10 min; límite 8 h) · Original 27/11 15:20 (3 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. La peor es A3: -38,12%, peor caída -39,85%, 35 ops y 24,42 USD de comisiones. Promedio de las 33: -10,42% (antes -9,67%).
- **Original:** 7.496 USD en USDT y ~2.317 USD en posiciones (3 ops). No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,99%, Agresiva -22,16%, Original -1,87%; Laboratorio y DCA (menos de 30 días, desde el inicio) -6,68% y -6,72%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.813 (-1,87%) | 9.816 (-1,84%) | 27/11 15:20 |
| DCA | 9.328 (-6,72%) | 9.329 (-6,71%) | 23/11 13:04 |
| Laboratorio | 9.286 (-7,14%) | 9.269 (-7,31%) | 27/11 18:16 |
| Torneo (promedio) | 8.958 (-10,42%) | 8.958 (-10,42%) | 27/11 16:42 |
| 3 niveles | 7.931 (-20,69%) | 8.635 (-13,65%) | 27/11 18:06 |
| Agresiva | 7.113 (-28,87%) | 7.799 (-22,01%) | 27/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.369 (-26,31%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.340 | -6,60% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 8.968 | -10,32% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.151 | -8,49% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.441 | -15,59% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.188.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles** (796,44 → 793,10): sin operaciones nuevas; sigue con el BTC, ETH y BNB de las 02:06. 108 ops.
- **Agresiva** (716,27 → 711,26): vendió el HYPE a las 15:00 (compra a 64,88, venta a 63,46) y quedó 100% en USDT. 428 ops; el 20,4% de lo perdido es comisión.
- **Laboratorio** (936,27 → 928,58): vendió el NEAR a las 16:16 (compra a 3,048, venta a 3,004) y quedó 100% en USDT. 30 ops.
- **DCA BTC:** sin cambios; compra los lunes, la próxima el 30/11.
- **Original** (9.894,25 → 9.813,16): sin operaciones nuevas; bajó por las posiciones que tiene abiertas.
- **Torneo:** promedio de -9,67% a -10,42%; las líderes siguen sin operar.
- **Régimen:** BTC abajo de la media 200, bajando 30 d (igual que los días anteriores).

## Recomendación

- **3 niveles — seguir.** -20,69%, pero +7,55 pp contra HODL BTC; mide bien.
- **Agresiva — seguir.** -28,87%, **-0,82 pp contra HODL BTC**: le va peor que comprar BTC y no tocar, y en 7 días (-4,78%) también (HODL +1,55%). El 20,4% de la pérdida es comisión (428 ops). El número es malo, pero hasta el 27/01/2027 no se apaga por resultado.
- **Laboratorio — seguir.** -7,14%, +18,77 pp contra HODL, peor caída -8,55%.
- **DCA BTC — seguir.** -6,72%, +17,45 pp contra HODL.
- **Torneo — seguir.** 0 de 33 le ganan a USDT; las que operan más (A3, -38,12%) son las que más pierden.
- **Original — seguir.** -1,87%, la mejor de todas, pero porque estuvo en USDT, no porque operó bien.

Key real: se decide el 27/01/2027

apagar=ninguna
