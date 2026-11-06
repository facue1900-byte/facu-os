# Veredicto de las carpetas cripto — 2026-11-06 06:51 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde es **DCA BTC (-0,38%, pero con precio del lunes 02/11)** y después Original (-1,04%). En el Torneo las 4 de arriba (P0, P8, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 31 le ganan a HODL BTC (-5,22%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie en +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 871,19 | -12,88% | -3,44 pp (HODL -9,44%) | -4,63% (HODL -6,64%) | -2,02% (HODL -3,93%) | -13,44% (HODL -10,89%) | 2,60 USD (2,0% de la pérdida) | 91 |
| Agresiva | 872,58 | -12,74% | -3,66 pp (HODL -9,08%) | -4,30% (HODL -6,51%) | -3,07% (HODL -3,79%) | -12,74% (HODL -11,14%) | 38,42 USD (30,2% de la pérdida) | 286 |
| Laboratorio | 954,01 | -4,60% | +1,94 pp (HODL -6,54%) | -4,60% (HODL -6,54%) | -3,79% (HODL -3,95%) | -6,05% (HODL -7,33%) | 3,15 USD (6,8% de la pérdida) | 17 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | -0,37% (HODL -3,56%) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 31 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +5,22 pp (HODL BTC -5,22%) | falta (arrancó 29/10 00:00) | ≈ desde inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +8,57 pp (HODL -9,61%) | -1,04% (HODL -6,54%) | -1,22% (HODL -7,08%) | -1,22% (HODL -10,67%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento. **7 días** = base en o antes del 30/10 06:51 UTC. Cada carpeta compara contra la columna `hodl_btc` de su propio `historial.csv`, por eso el HODL de referencia cambia entre filas.
- **Frescura (ahora 06:51 UTC):** 3 niveles 06:06, Agresiva 06:32, Laboratorio 06:17, DCA 02/11 13:56 (89 h; límite 8 días), Torneo `vivo.json` 04:41 (última vela 04:00), Original 05/11 23:20 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes, así que su -0,38% no incluye la caída de BTC desde el 02/11. No se estima; se verá el lunes 09/11.
- **Torneo:** la mejor que operó es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). L9 -1,74% (peor caída -8,65%). La peor, A3, -24,74%. Nadie cerca de +20%.
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 05/11 23:20 |
| Torneo (promedio) | 9.712 (-2,88%) | 9.712 (-2,88%) | 06/11 04:41 |
| Agresiva | 8.726 (-12,74%) | 9.568 (-4,32%) | 06/11 06:32 |
| Laboratorio | 9.540 (-4,60%) | 9.523 (-4,77%) | 06/11 06:17 |
| 3 niveles | 8.712 (-12,88%) | 9.485 (-5,15%) | 06/11 06:06 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.299 (-7,01%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.693 | -3,07% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.692 | -3,08% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.667 | -3,33% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.602 | -3,98% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.526.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** BTC siguió bajando: en 24 h HODL BTC -6,03% (medido en 3 niveles). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** -3,22% en 24 h (HODL -6,03%). Sin operaciones nuevas (91); 443,73 en USDT y 4 posiciones. Nuevo mínimo: -12,88%, peor caída -13,44% contra -10,89% de HODL.
- **Agresiva:** -0,40% en 24 h (HODL -6,03%). Sin operaciones desde el último veredicto: sigue **100% en USDT** (872,58).
- **Laboratorio:** sin cambios, 100% en USDT (954,01). -3,43% en 24 h (HODL -6,24%).
- **DCA BTC:** sin cambios desde la cuota del lunes. Próxima el lunes 09/11.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. A3 mejoró de -25,70% a -24,74%.
- **Original:** sin dato nuevo de la Mac desde 05/11 23:20: 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -12,88%, la peor; 3,44 pp abajo de HODL BTC y peor caída -13,44% contra -10,89% de HODL.
- **Agresiva: seguir.** -12,74%; 38,42 USD de comisiones en 286 operaciones (30,2% de la pérdida).
- **Laboratorio: seguir.** -4,60%, pero +1,94 pp sobre HODL BTC y peor caída -6,05% contra -7,33% de HODL.
- **DCA BTC: seguir.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve la caída de esta semana.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +8,57 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
