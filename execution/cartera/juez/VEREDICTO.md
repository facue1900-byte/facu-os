# Veredicto de las carpetas cripto — 2026-11-05 18:51 UTC

**En una línea:** BTC se cayó fuerte en las últimas horas (HODL BTC -5,5% en 6 h según 3 niveles) y **ninguna carpeta le gana a USDT**: la que menos pierde es **DCA BTC (-0,38%, pero con precio del lunes 02/11)** y después Original (-1,04%). En el Torneo las 4 de arriba (P0, P8, L2, L5) están en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 30 le ganan a HODL BTC (-5,07%). Quedarse quieto sigue siendo lo mejor. **Sin mail:** nadie en +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 873,67 | -12,63% | -3,44 pp (HODL -9,19%) | -4,36% (HODL -6,39%) | -4,18% (HODL -6,24%) | -13,20% (HODL -10,70%) | 2,60 USD (2,1% de la pérdida) | 91 |
| Agresiva | 874,80 | -12,52% | -3,97 pp (HODL -8,55%) | -4,06% (HODL -5,96%) | -4,79% (HODL -5,60%) | -12,64% (HODL -10,35%) | 37,90 USD (30,3% de la pérdida) | 283 |
| Laboratorio | 954,01 | -4,60% | +1,40 pp (HODL -6,00%) | -4,60% (HODL -6,00%) | -5,22% (HODL -5,98%) | -6,05% (HODL -6,81%) | 3,15 USD (6,8% de la pérdida) | 17 |
| DCA BTC (dato del 02/11) | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | -0,37% (HODL -3,56%) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder empatado: P0 USDT quieto, P8, L2, L5, todas sin operar (0 de 33 le ganan a USDT; 30 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +5,07 pp (HODL BTC -5,07%) | falta (arrancó 29/10 00:00) | ≈ desde inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +6,39 pp (HODL -7,43%) | -1,04% (HODL -4,28%) | -1,22% (HODL -4,83%) | -1,22% (HODL -9,44%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento. **7 días** = base en o antes del 29/10 18:51 UTC. Cada carpeta compara contra la columna `hodl_btc` de su propio `historial.csv`, por eso el HODL de referencia cambia un poco entre filas (distintas horas de medición).
- **Frescura (ahora 18:51 UTC):** 3 niveles 18:06, Agresiva 18:32, Laboratorio 18:16, DCA 02/11 13:56 (77 h; límite 8 días), Torneo `vivo.json` 16:41 (última vela 16:00), Original 05/11 15:20 (Mac). **Todas corren.**
- **Ojo con la DCA:** sólo mide los lunes, así que su -0,38% no incluye la caída de BTC desde el 02/11. Con el BTC de hoy perdería más; no se estima, se verá el lunes 09/11.
- **Torneo:** la mejor que operó es L4 cruce 20/50 en las 14 (-0,11%, 2 ops). L9, que lideraba al mediodía con +4,83%, bajó a -1,96% (peor caída -7,87%). La peor, A3, -25,22%. Nadie cerca de +20%.
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords (no mandan mail): ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 05/11 15:20 |
| Torneo (promedio) | 9.708 (-2,92%) | 9.708 (-2,92%) | 05/11 16:41 |
| Agresiva | 8.748 (-12,52%) | 9.592 (-4,08%) | 05/11 18:32 |
| Laboratorio | 9.540 (-4,60%) | 9.523 (-4,77%) | 05/11 18:16 |
| 3 niveles | 8.737 (-12,63%) | 9.512 (-4,88%) | 05/11 18:06 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.325 (-6,75%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.692 | -3,08% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.700 | -3,00% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.677 | -3,23% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.613 | -3,87% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 7.478.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** caída fuerte de BTC hoy a la tarde (HODL -6,1% en 24 h en el historial de 3 niveles; en el Torneo HODL BTC pasó de +0,36% a -5,07% desde el 29/10). Régimen: BTC arriba de la media 200, bajando 30 d.
- **3 niveles:** -3,16% en 24 h (HODL -6,09%). Sin operaciones nuevas (91); sigue con 443,73 en USDT y 4 posiciones (BTC, ETH, BNB, XRP). Su peor caída (-13,20%) ya es peor que la de HODL (-10,70%).
- **Agresiva:** -0,73% en 24 h (HODL -5,56%): la salvó haber quedado 100% en USDT a las 12:32. A las 18:32 volvió a comprar BTC por 175 USD («rebote en soporte»). Las comisiones siguen siendo el 30,3% de lo que pierde.
- **Laboratorio:** -3,78% en 24 h (HODL -5,77%). Le saltaron los stops de SUI y ETH y vendió BTC por «tendencia rota»; quedó **100% en USDT** (954,01). Le gana a HODL BTC por 1,40 pp.
- **DCA BTC:** sin cambios desde la cuota del lunes. Próxima cuota el lunes 09/11.
- **Torneo:** se dio vuelta. 6 h antes 15 de 33 le ganaban a USDT; ahora ninguna. Las que nunca entraron quedaron arriba.
- **Original:** dato nuevo de la Mac (15:20), sin cambios: 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -12,63%, la peor; 3,44 pp abajo de HODL BTC y peor caída -13,20% contra -10,70% de HODL.
- **Agresiva: seguir.** -12,52%; 37,90 USD de comisiones en 283 operaciones (30,3% de la pérdida).
- **Laboratorio: seguir.** -4,60%, pero +1,40 pp sobre HODL BTC y peor caída -6,05% contra -6,81% de HODL.
- **DCA BTC: seguir.** -0,38% al 02/11, +3,17 pp sobre HODL; el número no ve la caída de esta semana.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** -1,04%, +6,39 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=ninguna avisos=0
