# Veredicto de las carpetas cripto — 2026-11-21 18:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-25,14%). Todas le ganan a HODL BTC, pero quedarse quieto en USDT sigue rindiendo más que todas. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +7,81 pp (HODL -27,93%) | -12,56% (HODL -25,71%) | -1,70% (HODL -8,72%) | -20,64% (HODL -34,25%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 740,85 | -25,92% | +1,82 pp (HODL -27,73%) | -18,75% (HODL -25,69%) | -6,90% (HODL -8,77%) | -26,03% (HODL -34,07%) | 54,89 USD (21,2% de la pérdida) | 398 |
| Laboratorio | 942,34 | -5,77% | +19,83 pp (HODL -25,59%) | -5,77% (HODL -25,59%) | -1,38% (HODL -8,62%) | -7,22% (HODL -32,09%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +25,14 pp (HODL BTC -25,14%; precio crudo -26,31%) | falta (arrancó el 29/10 00:00) | falta (vivo.json no trae serie) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +27,19 pp (HODL -28,23%) | -1,04% (HODL -25,79%) | +0,00% (HODL -9,01%) | -1,22% (HODL -31,36%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC; la base de cada carpeta es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta contra la columna `hodl_btc` de su propio `historial.csv` (la DCA mide contra su último snapshot, del 16/11, y la Original contra el suyo de las 15:52; por eso sus HODL difieren).
- **Frescura (ahora 21/11 18:52 UTC):** 3 niveles 18:06 (46 min) · Agresiva 18:32 (20 min) · Laboratorio 18:16 (36 min) · DCA 16/11 13:06 (5 d 5 h 46 min; límite 8 días) · Torneo `vivo.json` 16:41 (2 h 11 min; límite 8 h) · Original 15:52 (3 h; corre en la Mac, no es falla). **Todas corren.**
- **Torneo:** entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops; atrás L7 (-0,24%). La peor es A3: -38,29%, peor caída -39,85%, 27 ops y 19,58 USD de comisiones. Promedio de las 33: -10,53% (antes -11,13%).
- **Original:** 100% en USDT, sin movimiento en 7 días. No publica `libro.json`: faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,04%, Agresiva -20,81%, Original -1,04%; Laboratorio y DCA (menos de 30 días, desde el inicio) -5,77% y -5,11%; Torneo, la mejor en 0,00%. Ninguna cerca.
- **Cómo se mide:** peor caída sobre `total_usd` del `historial.csv`, con el capital inicial como primer máximo; comisiones y ops del `libro.json`.
- **Récords (no mandan mail):** la peor caída de la Agresiva pasó de -25,90% a **-26,03%** (snapshot de 17:32, después de comprar TAO y UNI).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 21/11 15:52 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 21/11 18:16 |
| Torneo (promedio) | 8.947 (-10,53%) | 8.947 (-10,53%) | 21/11 16:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 21/11 18:06 |
| Agresiva | 7.408 (-25,91%) | 8.123 (-18,77%) | 21/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.400 (-26,00%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.416 | -5,84% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.094 | -9,06% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.262 | -7,38% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.627 | -13,73% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.171.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo +1,82% en 3 niveles, +2,00% en Agresiva y +1,98% en Laboratorio: sigue el rebote (el HODL de la ventana en escenarios pasó de -28,39% a -26,00% desde la corrida de las 12:52). Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** en 24 h, 0,00%. 100% en USDT (798,73), sin operaciones nuevas desde el stop del MEGA (20/11 03:49).
- **Agresiva:** en 24 h, -0,82% (contra +2,00% de HODL BTC). Volvió a entrar: compró TAO (148 USD, 15:32) y UNI (148 USD, 16:31) por momentum 24 h; quedan 445,04 USD en USDT. Ops 396 → 398, comisiones 54,60 → 54,89 USD.
- **Laboratorio:** en 24 h, 0,00%. 100% en USDT, sin cambios.
- **DCA BTC:** sin snapshot nuevo desde la cuota del lunes 16/11; normal, corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT; el promedio mejoró de -11,13% a -10,53% con el rebote.
- **Original:** último dato 15:52; 100% en USDT, -1,04%.
- **Alarmas:** nadie llegó a +20% y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** -20,13%, +7,81 pp sobre HODL BTC; peor caída -20,64% contra -34,25% de HODL.
- **Agresiva: seguir.** La peor: -25,92%, apenas +1,82 pp sobre HODL BTC; peor caída nueva -26,03%. Las comisiones (54,89 USD en 398 ops) son el 21,2% de la pérdida.
- **Laboratorio: seguir.** -5,77%, +19,83 pp sobre HODL BTC; peor caída -7,22% contra -32,09%.
- **DCA BTC: seguir.** -5,11%, +15,41 pp sobre HODL BTC. Próxima cuota el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +27,19 pp sobre HODL BTC. Faltan comisiones y ops.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
