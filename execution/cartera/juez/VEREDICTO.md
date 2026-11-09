# Veredicto de las carpetas cripto — 2026-11-09 18:55 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **DCA BTC (-0,38%, con el precio del lunes 02/11; la cuota de hoy lunes todavía no corrió)**, después Original (-1,04%). En el Torneo las líderes (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-5,69%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie llegó a +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 864,04 | -13,60% | -3,26 pp (HODL -10,34%) | -5,41% (HODL -7,57%) | -1,92% (HODL -3,23%) | -14,69% (HODL -12,91%) | 2,62 USD (1,9% de la pérdida) | 92 |
| Agresiva | 845,95 | -15,40% | -5,07 pp (HODL -10,34%) | -7,23% (HODL -7,80%) | -3,51% (HODL -3,10%) | -15,40% (HODL -12,70%) | 41,63 USD (27,0% de la pérdida) | 307 |
| Laboratorio | 958,33 | -4,17% | +3,41 pp (HODL -7,57%) | -4,17% (HODL -7,57%) | -3,35% (HODL -3,31%) | -6,55% (HODL -9,09%) | 3,34 USD (8,0% de la pérdida) | 18 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | falta (no hay snapshot nuevo desde el 02/11) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +5,69 pp (HODL BTC -5,69%; precio crudo -7,14%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +8,87 pp (HODL -9,91%) | -1,04% (HODL -6,85%) | +0,00% (HODL -3,36%) | -1,22% (HODL -12,16%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; la base es el último snapshot en o antes de ese momento. **7 días** = base en o antes de 7 días atrás. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 2026-11-09 18:52 UTC):** 3 niveles 18:06, Agresiva 18:32, Laboratorio 18:16, DCA 02/11 13:56 (173 h; el límite es 8 días = 192 h, vence el 10/11 13:56), Torneo `vivo.json` 16:41 (última vela 16:00), Original 09/11 15:20 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes; su -0,38% no ve lo que bajó BTC desde el 02/11 (HODL BTC de las otras carpetas -3% en la semana). No se estima. Si mañana 10/11 a las 13:56 UTC sigue sin snapshot, pasa a `parada` y manda mail.
- **Torneo:** la mejor de las que operaron es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). La peor es A3, con -25,58% (peor caída -26,63%, 10,26 USD de comisiones). Promedio de las 33: -3,24%. HODL BTC del Torneo: -5,69% con la entrada en la vela siguiente (precio crudo desde el 29/10 00:00: -7,14%).
- **Original:** 100% en USDT; sin movimiento en 7 días. No publica `libro.json`, así que faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,43%, Agresiva -14,66% y Original -1,04% en 30 días; Laboratorio y DCA se miden desde el inicio (≤ 0%). Torneo: máximo 0,00%. Nadie cerca.
- Peor caída: sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): ninguno positivo. Al revés: **Agresiva marcó nueva peor caída, -15,40%, en el último snapshot** (antes -14,77%).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 09/11 15:20 |
| Torneo (promedio) | 9.676 (-3,24%) | 9.676 (-3,24%) | 09/11 16:41 |
| Laboratorio | 9.583 (-4,17%) | 9.566 (-4,34%) | 09/11 18:16 |
| 3 niveles | 8.640 (-13,60%) | 9.407 (-5,93%) | 09/11 18:06 |
| Agresiva | 8.460 (-15,40%) | 9.276 (-7,24%) | 09/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.206 (-7,94%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.699 | -3,01% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.631 | -3,69% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.623 | -3,77% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.454 | -5,46% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.442.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC bajó en 24 h (HODL BTC -1,33% medido en 3 niveles, -1,77% en Agresiva, -1,58% en Laboratorio). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** -0,95% en 24 h (HODL -1,33%). Sin operaciones en 24 h. Quedan 468,28 en USDT y 3 posiciones (BTC, ETH, BNB).
- **Agresiva:** -2,00% en 24 h (HODL -1,77%). Desde el veredicto de las 12:53 hizo 5 operaciones y perdió en las tres que cerró: compró AVAX (15:32) y lo vendió a las 17:32 (-2,90%); vendió ARB (16:32, -0,82%); compró PEPE (16:32) y lo vendió a las 18:32 (-2,08%). Quedan BTC, XRP y HYPE, y 374,30 en USDT. Comisiones: 41,63 USD en 307 ops, 27,0% de lo que perdió.
- **Laboratorio:** +0,45% en 24 h (HODL -1,58%), la única que subió. Sigue con el PEPE; quedan 763,21 en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes 02/11. La de hoy todavía no aparece.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. Le ganan a HODL BTC 29.
- **Original:** sin operar; sigue 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20% (ni carpeta ni estrategia), ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -13,60%, 3,26 pp abajo de HODL BTC, y peor caída de -14,69% contra -12,91% de HODL.
- **Agresiva: seguir.** -15,40%, la peor y en su mínimo; 5,07 pp abajo de HODL BTC, 41,63 USD de comisiones en 307 operaciones (27,0% de la pérdida). Entra y sale en horas y pierde en casi todas.
- **Laboratorio: seguir.** -4,17%, pero +3,41 pp sobre HODL BTC y peor caída de -6,55% contra -9,09% de HODL.
- **DCA BTC: seguir.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve el precio de esta semana. Si la cuota de hoy no aparece antes del 10/11 13:56, queda parada.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +8,87 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
