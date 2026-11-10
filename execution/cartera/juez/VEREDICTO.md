# Veredicto de las carpetas cripto — 2026-11-10 12:53 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **DCA BTC (-0,38%, con el precio del lunes 02/11; la cuota del lunes 09/11 sigue sin aparecer y la carpeta vence hoy a las 13:56 UTC)**, después Original (-1,04%). En el Torneo las líderes (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-7,08%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie llegó a +20% y todas corren todavía.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 861,00 | -13,90% | -2,99 pp (HODL -10,91%) | -5,75% (HODL -8,16%) | -2,17% (HODL -3,53%) | -14,69% (HODL -12,91%) | 2,62 USD (1,9% de la pérdida) | 92 |
| Agresiva | 835,50 | -16,45% | -5,59 pp (HODL -10,86%) | -8,37% (HODL -8,33%) | -5,18% (HODL -4,14%) | **-16,45%** (HODL -12,70%) | 43,60 USD (26,5% de la pérdida) | 320 |
| Laboratorio | 962,47 | -3,75% | +4,28 pp (HODL -8,03%) | -3,75% (HODL -8,03%) | -2,93% (HODL -3,78%) | -6,55% (HODL -9,09%) | 3,34 USD (8,9% de la pérdida) | 18 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | falta (no hay snapshot nuevo desde el 02/11) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +7,08 pp (HODL BTC -7,08%; precio crudo -8,51%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +9,99 pp (HODL -11,02%) | -1,04% (HODL -8,00%) | +0,00% (HODL -3,75%) | -1,22% (HODL -12,16%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; la base es el último snapshot en o antes de ese momento. **7 días** = base en o antes de 7 días atrás. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 2026-11-10 12:53 UTC):** 3 niveles 12:08, Agresiva 12:32, Laboratorio 12:21, DCA 02/11 13:56 (190,9 h; el límite es 8 días = 192 h, **vence hoy 10/11 13:56**, en una hora), Torneo `vivo.json` 12:42 (última vela 12:00), Original 10/11 09:14 (Mac). **Todas corren.**
- **Ojo con la DCA:** la rama no tiene commits desde el 02/11 13:56: la cuota del lunes 09/11 no corrió. Su -0,38% no ve lo que bajó BTC desde el 02/11. No se estima. Si a las 13:56 UTC de hoy sigue sin snapshot, la próxima corrida del juez la marca `parada` y manda mail.
- **Torneo:** la mejor de las que operaron es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). La peor es A3, con -28,71% (peor caída -29,05%, 11,72 USD de comisiones, 15 ops). Promedio de las 33: -4,13% (antes -3,90%).
- **Original:** 100% en USDT; sin movimiento en 7 días. No publica `libro.json`, así que faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -13,06%, Agresiva -14,83% y Original -1,04% en 30 días; Laboratorio y DCA se miden desde el inicio (≤ 0%). Torneo: máximo 0,00%. Nadie cerca.
- Peor caída: sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- **Récords (no mandan mail):** Agresiva marcó un **nuevo mínimo**: 835,50 USD, peor caída -16,45% (antes -15,94%).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 10/11 09:14 |
| Laboratorio | 9.625 (-3,75%) | 9.607 (-3,93%) | 10/11 12:21 |
| Torneo (promedio) | 9.587 (-4,13%) | 9.587 (-4,13%) | 10/11 12:42 |
| 3 niveles | 8.610 (-13,90%) | 9.374 (-6,26%) | 10/11 12:08 |
| Agresiva | 8.355 (-16,45%) | 9.161 (-8,39%) | 10/11 12:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.147 (-8,53%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.689 | -3,11% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.599 | -4,01% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.610 | -3,90% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.378 | -6,22% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.129.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC algo abajo en 24 h (HODL BTC -0,21% medido en 3 niveles, -0,94% en Agresiva, -0,41% en Laboratorio). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** -0,15% en 24 h (HODL -0,21%). Sin operaciones nuevas (92). Quedan 468,28 en USDT y 3 posiciones (BTC, ETH, BNB).
- **Agresiva:** -2,31% en 24 h (HODL -0,94%): otra vez la que más perdió, y quedó en su mínimo. 5 operaciones más desde el veredicto anterior (315 → 320): **vendió todo y quedó 100% en USDT** (835,50). Comisiones: 43,60 USD, 26,5% de lo que perdió.
- **Laboratorio:** +0,95% en 24 h (HODL -0,41%). Sigue con el PEPE; quedan 763,21 en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes 02/11. La del lunes 09/11 no apareció; vence hoy 13:56 UTC.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. Le ganan a HODL BTC 29. El promedio empeoró a -4,13%; A3 cayó a -28,71%.
- **Original:** sin operar; sigue 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20% (ni carpeta ni estrategia), ninguna carpeta parada todavía. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -13,90%, 2,99 pp abajo de HODL BTC, y peor caída de -14,69% contra -12,91% de HODL.
- **Agresiva: seguir.** -16,45%, la peor; 5,59 pp abajo de HODL BTC, peor caída -16,45% (nuevo mínimo) contra -12,70% de HODL, 43,60 USD de comisiones en 320 operaciones (26,5% de la pérdida).
- **Laboratorio: seguir.** -3,75%, +4,28 pp sobre HODL BTC y peor caída de -6,55% contra -9,09% de HODL.
- **DCA BTC: revisar (técnico).** -0,38% al 02/11, +3,17 pp sobre HODL; pero la cuota del 09/11 no corrió y el número no ve el precio de esta semana. Vence hoy 10/11 13:56 UTC.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +9,99 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
