# Veredicto de las carpetas cripto — 2026-11-07 12:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **DCA BTC (-0,38%, con el precio del lunes 02/11)**, y después viene Original (-1,04%). En el Torneo las líderes (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 31 le ganan a HODL BTC (-5,13%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie llegó a +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 873,28 | -12,67% | -3,74 pp (HODL -8,93%) | -4,40% (HODL -6,12%) | -0,96% (HODL -2,10%) | -13,44% (HODL -10,89%) | 2,62 USD (2,1% de la pérdida) | 92 |
| Agresiva | 863,36 | -13,66% | -4,99 pp (HODL -8,67%) | -5,32% (HODL -6,08%) | -3,11% (HODL -2,05%) | -13,66% (HODL -11,14%) | 39,46 USD (28,9% de la pérdida) | 292 |
| Laboratorio | 954,01 | -4,60% | +1,38 pp (HODL -5,98%) | -4,60% (HODL -5,98%) | -3,79% (HODL -2,05%) | -6,05% (HODL -7,40%) | 3,15 USD (6,8% de la pérdida) | 17 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -0,37% (HODL -3,56%) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 31 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +5,13 pp (HODL BTC -5,13%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +7,77 pp (HODL -8,81%) | -1,04% (HODL -5,71%) | +0,00% (HODL -1,27%) | -1,22% (HODL -10,67%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; la base es el último snapshot en o antes de ese momento. **7 días** = base en o antes del 31/10 12:52 UTC. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 12:52 UTC):** 3 niveles 12:06, Agresiva 12:31, Laboratorio 12:16, DCA 02/11 13:56 (119 h; el límite es 8 días), Torneo `vivo.json` 12:41 (última vela 12:00), Original 07/11 09:12 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes; su -0,38% no incluye lo que se movió BTC desde el 02/11. No se estima: se va a ver el lunes 09/11.
- **Torneo:** la mejor de las que operaron es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). La peor es A3, con -24,68% (peor caída -26,63%). Nadie cerca de +20%.
- **Original:** 100% en USDT con 2 operaciones; sin movimiento en 7 días. No publica `libro.json`, así que faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -10,45% y Agresiva -12,59% en 30 días; el resto se mide desde el inicio (todas ≤ 0%). Torneo: máximo 0,00%. Nadie cerca.
- Peor caída: sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): la Agresiva marcó una nueva peor caída (-13,66%, que es su valor actual de las 12:31).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 07/11 09:12 |
| Torneo (promedio) | 9.716 (-2,84%) | 9.716 (-2,84%) | 07/11 12:41 |
| Laboratorio | 9.540 (-4,60%) | 9.523 (-4,77%) | 07/11 12:16 |
| 3 niveles | 8.733 (-12,67%) | 9.508 (-4,92%) | 07/11 12:06 |
| Agresiva | 8.634 (-13,66%) | 9.467 (-5,33%) | 07/11 12:31 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.351 (-6,49%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.694 | -3,06% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.679 | -3,21% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.663 | -3,37% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.553 | -4,47% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.532.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC algo abajo en 24 h (HODL BTC -0,28% medido en 3 niveles, -0,36% en Agresiva, -0,18% en Laboratorio). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** -0,20% en 24 h (HODL -0,28%). Sin operaciones nuevas (92); 468,28 en USDT y 3 posiciones.
- **Agresiva:** -1,06% en 24 h (HODL -0,36%). Una operación más (292) y ahora está 100% en USDT (863,36). Comisiones: 39,46 USD, casi un tercio de lo que perdió.
- **Laboratorio:** sin operaciones, 100% en USDT (954,01). 0,00% en 24 h.
- **DCA BTC:** sin cambios desde la cuota del lunes. La próxima es el lunes 09/11.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. HODL BTC del torneo pasó de -5,24% a -5,13%.
- **Original:** dato nuevo de la Mac a las 09:12: sigue 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20% (ni carpeta ni estrategia), ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -12,67%, 3,74 pp abajo de HODL BTC, y peor caída de -13,44% contra -10,89% de HODL.
- **Agresiva: seguir.** -13,66%, la peor y en su mínimo; 39,46 USD de comisiones en 292 operaciones (28,9% de la pérdida).
- **Laboratorio: seguir.** -4,60%, pero +1,38 pp sobre HODL BTC y peor caída de -6,05% contra -7,40% de HODL.
- **DCA BTC: seguir.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve el precio de esta semana.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +7,77 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
