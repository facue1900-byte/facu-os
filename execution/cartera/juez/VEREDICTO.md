# Veredicto de las carpetas cripto — 2026-11-02 18:50 UTC

**En una línea:** ninguna carpeta con historia le gana a quedarse en USDT (0%). La única en positivo es el Torneo, ahora con L9 al frente (+1,03%; A7 bajó a +0,61%). Laboratorio (-0,84%), DCA (-0,38%) y Original (-1,04%) le ganan a HODL BTC pero pierden contra USDT. 3 niveles (-11,91%) y Agresiva (-12,33%) pierden contra los dos. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 880,93 | -11,91% | -4,56 pp (HODL -7,34%) | -3,56% (HODL -4,48%) | -3,16% (HODL -3,78%) | -12,94% (HODL -9,63%) | 2,60 USD (2,2% de la pérdida) | 91 |
| Agresiva | 876,74 | -12,33% | -4,86 pp (HODL -7,47%) | -3,85% (HODL -4,85%) | -4,13% (HODL -4,07%) | -12,33% (HODL -9,82%) | 33,89 USD (27,5% de la pérdida) | 252 |
| Laboratorio | 991,57 | -0,84% | +3,57 pp (HODL -4,41%) | -0,84% (HODL -4,41%) | falta (arrancó 27/10) | -2,35% (HODL -5,66%) | 1,60 USD (19,0% de la pérdida) | 9 |
| DCA BTC | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | falta (arrancó 27/10) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder L9 compra pánico en tendencia alcista (3 de 33 le ganan a USDT y a HODL BTC) | 1.010,26 | +1,03% (112 h) | +4,25 pp (P1 HODL BTC -3,22%) | falta (arrancó 29/10 00:00) | falta | -3,26% | 1,00 USD | 5 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +5,75 pp (HODL -6,78%) | -1,04% (HODL -3,62%) | -1,04% (HODL -2,46%) | -1,22% (HODL -8,72%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento.
- **Frescura (ahora 18:50 UTC):** 3 niveles 18:07, Agresiva 18:32, Laboratorio 18:17, DCA 02/11 13:56 (cuota del lunes ya cargada), Torneo `vivo.json` 17:20 (última vela 16:00), Original 15:20 (Mac). **Todas corren.**
- **Original:** entre el 30/10 23:09 y el 02/11 13:43 no hay snapshots (Mac apagada); está 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- **Torneo:** las 3 que le ganan a USDT y a P1 HODL BTC (-3,22%): L9 +1,03%, A7 +0,61%, L8 +0,20%. Ninguna cerca de +20%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -4,70% y la estrategia P1 HODL BTC dice -3,22%.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`; la suma por operación coincide con `comisiones_usd` en las cuatro.
- Récords: ya no mandan mail y no se rastrean acá.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 02/11 15:20 |
| Laboratorio | 9.916 (-0,84%) | 9.898 (-1,02%) | 02/11 18:17 |
| Torneo (promedio) | 9.833 (-1,67%) | 9.833 (-1,67%) | 02/11 17:20 |
| Agresiva | 8.767 (-12,33%) | 9.613 (-3,87%) | 02/11 18:32 |
| 3 niveles | 8.809 (-11,91%) | 9.591 (-4,09%) | 02/11 18:07 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.514 (-4,86%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.879 | -1,21% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.800 | -2,00% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.778 | -2,22% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.736 | -2,64% |

Torneo, 33 estrategias: mejor L9 compra pánico sólo en tendencia alcista, 14 monedas 10.103; peor A3 la que más subió en 7 d, rota cada día 8.284.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles:** -0,36% en 24 h, con HODL BTC -0,86%. Sin operaciones. 443,73 en USDT.
- **Agresiva:** -1,27% en 24 h, con HODL BTC -1,22%. 11 operaciones en 24 h (SOL, TRX, ETH, XRP, HYPE): compró y vendió casi todo el mismo día y quedó **100% en USDT** (876,74). Las comisiones ya son el 27,5% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC -0,89%. Sigue 100% en USDT.
- **DCA BTC:** entró la cuota del lunes (100 USD a BTC, 13:56). Lleva 200 en BTC y 800 en USDT.
- **Torneo:** el mercado siguió bajando. L9 pasó al frente (1.010,26); A7 cayó a 1.006,10 (desde 1.016,12 al mediodía). Las que le ganan a USDT y a HODL BTC bajaron de 6 a 3. Régimen: BTC arriba de la media 200, bajando 30 d.
- **Original:** sin cambios desde que la Mac volvió a publicar (100% en USDT).
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -11,91% contra 0% de USDT y -7,34% de HODL BTC; en 7 días -3,16%, algo mejor que HODL (-3,78%) pero igual pierde.
- **Agresiva: seguir.** -12,33%, la peor; en 7 días -4,13%, peor que HODL (-4,07%). 33,89 USD de comisiones en 252 operaciones.
- **Laboratorio: seguir.** -0,84%, +3,57 pp sobre HODL BTC, peor caída -2,35% contra -5,66% de HODL.
- **DCA BTC: seguir.** -0,38%, la cuota semanal corre bien.
- **Torneo: revisar.** L9 lidera con +1,03% en 112 h, pero el `hodl_btc` de `vivo.json` (-4,70%) no coincide con P1 (-3,22%): la vara contra HODL no mide bien.
- **Original: seguir.** -1,04%, +5,75 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Torneo L9 mejor_que_usdt=1 apagar=ninguna avisos=0
