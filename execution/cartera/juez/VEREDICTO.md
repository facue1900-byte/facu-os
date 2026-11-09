# Veredicto de las carpetas cripto — 2026-11-09 12:53 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **DCA BTC (-0,38%, con el precio del lunes 02/11; la cuota de hoy lunes todavía no corrió)**, después Original (-1,04%). En el Torneo las líderes (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-7,14%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie llegó a +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 862,28 | -13,77% | -3,05 pp (HODL -10,72%) | -5,61% (HODL -7,97%) | -2,51% (HODL -4,42%) | -14,69% (HODL -12,91%) | 2,62 USD (1,9% de la pérdida) | 92 |
| Agresiva | 855,22 | -14,48% | -4,47 pp (HODL -10,01%) | -6,21% (HODL -7,46%) | -3,29% (HODL -3,88%) | -14,77% (HODL -12,70%) | 40,89 USD (28,2% de la pérdida) | 302 |
| Laboratorio | 953,44 | -4,66% | +3,00 pp (HODL -7,65%) | -4,66% (HODL -7,65%) | -3,85% (HODL -4,24%) | -6,55% (HODL -9,09%) | 3,34 USD (7,2% de la pérdida) | 18 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -0,37% (HODL -3,56%) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +7,14 pp (HODL BTC -7,14%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +9,32 pp (HODL -10,36%) | -1,04% (HODL -7,32%) | +0,00% (HODL -2,94%) | -1,22% (HODL -12,16%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; la base es el último snapshot en o antes de ese momento. **7 días** = base en o antes de 7 días atrás. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 2026-11-09 12:53 UTC):** 3 niveles 12:09, Agresiva 12:32, Laboratorio 12:24, DCA 02/11 13:56 (167 h; el límite es 8 días = 192 h, vence el 10/11 13:56), Torneo `vivo.json` 12:41 (última vela 12:00), Original 09/11 12:40 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes; su -0,38% no ve lo que bajó BTC desde el 02/11 (HODL BTC de las otras carpetas -4% en la semana). No se estima: la cuota de hoy la actualiza. Si mañana 10/11 a las 14 UTC sigue sin snapshot, pasa a `parada`.
- **Torneo:** la mejor de las que operaron es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). La peor es A3, con -25,56% (peor caída -26,63%, 10,26 USD de comisiones). Promedio de las 33: -3,96%. Nadie cerca de +20%.
- **Original:** 100% en USDT; sin movimiento en 7 días. No publica `libro.json`, así que faltan comisiones y ops.
- **+20% en 30 días:** 3 niveles -11,91%, Agresiva -13,74% y Original -1,04% en 30 días; Laboratorio y DCA se miden desde el inicio (≤ 0%). Torneo: máximo 0,00%. Nadie cerca.
- Peor caída: sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): ninguno positivo. Al revés: **3 niveles y Agresiva marcaron nueva peor caída** entre corridas (-14,69% y -14,77%), aunque ahora rebotaron un poco.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 09/11 12:40 |
| Torneo (promedio) | 9.604 (-3,96%) | 9.604 (-3,96%) | 09/11 12:41 |
| Laboratorio | 9.534 (-4,66%) | 9.517 (-4,83%) | 09/11 12:24 |
| 3 niveles | 8.623 (-13,77%) | 9.388 (-6,12%) | 09/11 12:09 |
| Agresiva | 8.552 (-14,48%) | 9.378 (-6,22%) | 09/11 12:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.167 (-8,33%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.658 | -3,42% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.625 | -3,75% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.617 | -3,83% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.473 | -5,27% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.444.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC bajó en 24 h (HODL BTC -1,97% medido en 3 niveles, -1,45% en Agresiva, -1,70% en Laboratorio). Régimen: BTC arriba de la media 200, bajando 30 d. HODL BTC del Torneo -7,14% (vela de las 12:00).
- **3 niveles:** -1,28% en 24 h (HODL -1,97%). Sin operaciones en 24 h. Quedan 468,28 en USDT y 3 posiciones (BTC, ETH, BNB).
- **Agresiva:** -0,94% en 24 h (HODL -1,45%). Desde el último veredicto compró XRP (150, 08:36, rebote en soporte), HYPE (150, 11:32, rebote) y ARB (150, 12:32, momentum). Ahora tiene 4 posiciones y quedan 233,88 en USDT. Comisiones: 40,89 USD en 302 ops, 28,2% de lo que perdió.
- **Laboratorio:** -0,06% en 24 h (HODL -1,70%). Sigue con el PEPE; quedan 763,21 en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes 02/11. La de hoy todavía no aparece.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. Le ganan a HODL BTC 29.
- **Original:** sin operar; sigue 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20% (ni carpeta ni estrategia), ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -13,77%, 3,05 pp abajo de HODL BTC, y peor caída de -14,69% contra -12,91% de HODL.
- **Agresiva: seguir.** -14,48%, la peor; 40,89 USD de comisiones en 302 operaciones (28,2% de la pérdida), y acaba de cargar 450 USD en tres monedas.
- **Laboratorio: seguir.** -4,66%, pero +3,00 pp sobre HODL BTC y peor caída de -6,55% contra -9,09% de HODL.
- **DCA BTC: seguir.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve el precio de esta semana. Si la cuota de hoy no aparece antes del 10/11 13:56, queda parada.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +9,32 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
