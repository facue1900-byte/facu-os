# Veredicto de las carpetas cripto — 2026-11-10 00:55 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **DCA BTC (-0,38%, con el precio del lunes 02/11; la cuota de ayer lunes 09/11 todavía no apareció)**, después Original (-1,04%). En el Torneo las líderes (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-5,90%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie llegó a +20% y todas corren (la DCA vence hoy 10/11 a las 13:56 UTC).

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 866,63 | -13,34% | -3,66 pp (HODL -9,67%) | -5,13% (HODL -6,88%) | -1,33% (HODL -1,79%) | -14,69% (HODL -12,91%) | 2,62 USD (2,0% de la pérdida) | 92 |
| Agresiva | 846,56 | -15,34% | -5,57 pp (HODL -9,78%) | -7,16% (HODL -7,22%) | -3,53% (HODL -2,64%) | -15,40% (HODL -12,70%) | 42,40 USD (27,6% de la pérdida) | 312 |
| Laboratorio | 956,83 | -4,32% | +2,57 pp (HODL -6,89%) | -4,32% (HODL -6,89%) | -3,50% (HODL -2,12%) | -6,55% (HODL -9,09%) | 3,34 USD (7,7% de la pérdida) | 18 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | falta (no hay snapshot nuevo desde el 02/11) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +5,90 pp (HODL BTC -5,90%; precio crudo -7,35%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +8,74 pp (HODL -9,77%) | -1,04% (HODL -6,71%) | +0,00% (HODL -1,96%) | -1,22% (HODL -12,16%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; la base es el último snapshot en o antes de ese momento. **7 días** = base en o antes de 7 días atrás. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 2026-11-10 00:52 UTC):** 3 niveles 00:06, Agresiva 00:32, Laboratorio 00:16, DCA 02/11 13:56 (179 h; el límite es 8 días = 192 h, vence hoy 10/11 13:56), Torneo `vivo.json` 00:41 (última vela 00:00), Original 09/11 23:54 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes y la cuota del lunes 09/11 no apareció en todo el día. Su -0,38% no ve lo que bajó BTC desde el 02/11. No se estima. Si hoy 10/11 a las 13:56 UTC sigue sin snapshot, pasa a `parada` y manda mail.
- **Torneo:** la mejor de las que operaron es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). La peor es A3, con -25,58% (peor caída -26,63%, 10,26 USD de comisiones). Promedio de las 33: -3,51%. HODL BTC del Torneo: -5,90% con la entrada en la vela siguiente (precio crudo desde el 29/10 00:00: -7,35%).
- **Original:** 100% en USDT; sin movimiento en 7 días. No publica `libro.json`, así que faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -12,27%, Agresiva -14,08% y Original -1,04% en 30 días; Laboratorio y DCA se miden desde el inicio (≤ 0%). Torneo: máximo 0,00%. Nadie cerca.
- Peor caída: sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): ninguno. Agresiva quedó apenas arriba de su peor caída (-15,34% contra el mínimo de -15,40%).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 09/11 23:54 |
| Torneo (promedio) | 9.649 (-3,51%) | 9.649 (-3,51%) | 10/11 00:41 |
| Laboratorio | 9.568 (-4,32%) | 9.551 (-4,49%) | 10/11 00:16 |
| 3 niveles | 8.666 (-13,34%) | 9.435 (-5,65%) | 10/11 00:06 |
| Agresiva | 8.466 (-15,34%) | 9.283 (-7,17%) | 10/11 00:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.275 (-7,25%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.685 | -3,15% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.630 | -3,70% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.629 | -3,71% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.446 | -5,54% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.442.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC subió apenas en 24 h (HODL BTC +1,05% medido en 3 niveles, +0,04% en Agresiva, +0,12% en Laboratorio). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** +0,44% en 24 h (HODL +1,05%). Sin operaciones nuevas. Quedan 468,28 en USDT y 3 posiciones (BTC, ETH, BNB).
- **Agresiva:** -1,13% en 24 h (HODL +0,04%): la única que bajó. Desde el veredicto anterior hizo 5 operaciones más (307 → 312): a las 22:32 vendió BTC por la regla de 24 h (+0,91%) y UNI por tesis invalidada (-0,87%), y volvió a comprar AVAX; a las 00:32 compró ZEC. Quedan XRP, HYPE, AVAX y ZEC, y 243,89 en USDT. Comisiones: 42,40 USD en 312 ops, 27,6% de lo que perdió.
- **Laboratorio:** +0,36% en 24 h (HODL +0,12%). Sigue con el PEPE; quedan 763,21 en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes 02/11. La del lunes 09/11 no apareció.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. Le ganan a HODL BTC 29. El promedio empeoró a -3,51% (antes -3,24%).
- **Original:** sin operar; sigue 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20% (ni carpeta ni estrategia), ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -13,34%, 3,66 pp abajo de HODL BTC, y peor caída de -14,69% contra -12,91% de HODL.
- **Agresiva: seguir.** -15,34%, la peor; 5,57 pp abajo de HODL BTC, 42,40 USD de comisiones en 312 operaciones (27,6% de la pérdida). Bajó en un día en que BTC subió.
- **Laboratorio: seguir.** -4,32%, pero +2,57 pp sobre HODL BTC y peor caída de -6,55% contra -9,09% de HODL.
- **DCA BTC: seguir, con ojo técnico.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve el precio de esta semana y la cuota del 09/11 no corrió. Si no aparece antes de hoy 10/11 13:56 UTC, queda parada y pasa a `revisar`.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +8,74 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
