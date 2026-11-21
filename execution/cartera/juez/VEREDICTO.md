# Veredicto de las carpetas cripto — 2026-11-21 12:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-27,30%). Todas le ganan a HODL BTC, pero quedarse quieto en USDT sigue rindiendo más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +10,13 pp (HODL -30,26%) | -12,56% (HODL -28,10%) | -2,49% (HODL -13,45%) | -20,64% (HODL -34,25%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 741,04 | -25,90% | +3,79 pp (HODL -29,69%) | -18,73% (HODL -27,70%) | -7,40% (HODL -12,83%) | -25,90% (HODL -34,07%) | 54,60 USD (21,1% de la pérdida) | 396 |
| Laboratorio | 942,34 | -5,77% | +22,15 pp (HODL -27,91%) | -5,77% (HODL -27,91%) | -1,38% (HODL -13,22%) | -7,22% (HODL -32,09%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +27,30 pp (HODL BTC -27,30%; precio crudo -28,44%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +29,10 pp (HODL -30,14%) | -1,04% (HODL -27,77%) | +0,00% (HODL -15,44%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv` (la DCA mide contra su último snapshot, del 16/11, y la Original contra el suyo de las 03:20; por eso sus HODL difieren).
- **Frescura (ahora 21/11 12:52 UTC):** 3 niveles 12:07 (45 min) · Agresiva 12:31 (21 min) · Laboratorio 12:16 (36 min) · DCA 16/11 13:06 (4 d 23 h 46 min; límite 8 días) · Torneo `vivo.json` 12:41 (11 min; límite 8 h) · Original 03:20 (9 h 32 min; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops; atrás L7 (-0,24%) y L6 (-0,28%). La peor es A3: -38,58%, peor caída -39,85%, 27 ops y 19,58 USD de comisiones. Promedio de las 33: -11,13% (antes -11,76%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,86%, Agresiva -20,79%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -5,77% y -5,11%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo. La peor caída de la Agresiva sigue en -25,90%.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 21/11 03:20 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 21/11 12:16 |
| Torneo (promedio) | 8.887 (-11,13%) | 8.887 (-11,13%) | 21/11 12:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 21/11 12:07 |
| Agresiva | 7.410 (-25,90%) | 8.126 (-18,74%) | 21/11 12:31 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.161 (-28,39%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.399 | -6,01% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.084 | -9,16% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.262 | -7,38% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.610 | -13,90% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.142.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo -5,19% en 3 niveles, -5,29% en Agresiva y -5,70% en Laboratorio; desde la corrida de las 06:52 rebotó algo (el HODL de la ventana pasó de -31,39% a -28,39% en escenarios). Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** en 24 h, 0,00%. 100% en USDT (798,73), sin operaciones nuevas desde el stop del MEGA (20/11 03:49).
- **Agresiva:** en 24 h, -2,22% (contra -5,29% de HODL BTC); es el stop de BTC de las 03:55. Sin operaciones nuevas desde entonces: 100% en USDT (741,04).
- **Laboratorio:** en 24 h, 0,00%. 100% en USDT, sin cambios.
- **DCA BTC:** sin snapshot nuevo desde la cuota del lunes 16/11; normal, corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT; el promedio mejoró de -11,76% a -11,13% con el rebote.
- **Original:** último dato 03:20; 100% en USDT, -1,04%.
- **Alarmas:** nadie llegó a +20% y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** -20,13%, +10,13 pp sobre HODL BTC; peor caída -20,64% contra -34,25% de HODL.
- **Agresiva: seguir.** La peor: -25,90%, +3,79 pp sobre HODL BTC; peor caída -25,90%. Las comisiones (54,60 USD en 396 ops) son el 21,1% de la pérdida.
- **Laboratorio: seguir.** -5,77%, +22,15 pp sobre HODL BTC; peor caída -7,22% contra -32,09%.
- **DCA BTC: seguir.** -5,11%, +15,41 pp sobre HODL BTC. Próxima cuota el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +29,10 pp sobre HODL BTC. Faltan comisiones y ops.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
