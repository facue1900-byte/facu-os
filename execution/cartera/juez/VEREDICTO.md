# Veredicto de las carpetas cripto — 2026-11-04 06:55 UTC

**En una línea:** ninguna carpeta le gana a quedarse quieto. El Torneo lo "lidera" **P0 USDT quieto** con 0,00%: ninguna de las 33 estrategias está en positivo (L9, que iba +0,50%, cayó a -1,10%). Laboratorio (-0,84%), DCA (-0,38%) y Original (-1,04%) pierden contra USDT pero le ganan a HODL BTC; 3 niveles (-11,52%) y Agresiva (-12,04%) pierden contra los dos. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884,83 | -11,52% | -4,89 pp (HODL -6,63%) | -3,14% (HODL -3,75%) | -3,27% (HODL -3,71%) | -12,94% (HODL -9,67%) | 2,60 USD (2,3% de la pérdida) | 91 |
| Agresiva | 879,60 | -12,04% | -5,78 pp (HODL -6,26%) | -3,53% (HODL -3,60%) | -4,48% (HODL -3,59%) | -12,64% (HODL -9,99%) | 35,50 USD (29,5% de la pérdida) | 264 |
| Laboratorio | 991,57 | -0,84% | +2,92 pp (HODL -3,76%) | -0,84% (HODL -3,76%) | -0,02% (HODL -3,95%) | -2,35% (HODL -6,13%) | 1,60 USD (19,0% de la pérdida) | 9 |
| DCA BTC | 996,25 | -0,38% | +3,17 pp (HODL -3,55%) | falta (primer snapshot 27/10 22:38, 1 min después del corte) | -0,37% (HODL -3,56%) | -0,38% (HODL -3,56%) | 0,20 USD (5,3% de la pérdida) | 2 |
| Torneo — líder P0 USDT quieto (0 de 33 le ganan a USDT; 30 le ganan a HODL BTC) | 1.000,00 | 0,00% (6 d, desde 29/10) | +4,49 pp (P1 HODL BTC -4,49%) | falta (arrancó 29/10 00:00) | falta (6 días) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +5,74 pp (HODL -6,78%) | -1,04% (HODL -3,62%) | -1,04% (HODL -3,62%) | -1,22% (HODL -9,44%) | falta | falta |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC; base = último snapshot en o antes de ese momento. **7 días** = base en o antes del 28/10 06:55 UTC.
- **Frescura (ahora 06:55 UTC):** 3 niveles 06:06, Agresiva 06:32, Laboratorio 06:16, DCA 02/11 13:56 (41 h; límite 8 días), Torneo `vivo.json` 04:42 (última vela 04:00), Original 03/11 23:39 (Mac, no cuenta como falla). **Todas corren.**
- **Torneo:** las 4 en 0,00% (P0, P8, L2, L5) no operaron. La mejor que operó es D2 DCA 50/50 (-0,13%); L9 -1,10%, L8 -0,66%. La peor, A3, -18,99%. **Sigue la inconsistencia:** la columna `hodl_btc` de `vivo.json` dice -5,96% y la estrategia P1 HODL BTC dice -4,49%.
- **Original:** 100% en USDT con 2 operaciones. Sin `libro.json`: comisiones y ops faltan.
- Peor caída: del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops: del `libro.json`.
- Récords: no mandan mail. Sin récord nuevo esta corrida.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| DCA | 9.962 (-0,38%) | 9.963 (-0,37%) | 02/11 13:56 |
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 03/11 23:39 |
| Laboratorio | 9.916 (-0,84%) | 9.898 (-1,02%) | 04/11 06:16 |
| Torneo (promedio) | 9.764 (-2,36%) | 9.764 (-2,36%) | 04/11 04:42 |
| Agresiva | 8.796 (-12,04%) | 9.645 (-3,55%) | 04/11 06:32 |
| 3 niveles | 8.848 (-11,52%) | 9.634 (-3,66%) | 04/11 06:06 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 9.587 (-4,13%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.858 | -1,42% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.801 | -1,99% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.794 | -2,06% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 9.731 | -2,69% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 8.100.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **3 niveles:** +0,85% en 24 h, con HODL BTC +1,71%. Sin operaciones nuevas (91). 443,73 en USDT y 4 posiciones.
- **Agresiva:** +0,25% en 24 h (HODL +1,62%). Desde el veredicto anterior, 6 operaciones (258 → 264), casi todas compras: bajó de 619,94 a 308,91 en USDT y quedó con 4 posiciones. Las comisiones ya son el 29,5% de lo que pierde.
- **Laboratorio:** 0,00% en 24 h, con HODL BTC +1,62%. Sigue 100% en USDT.
- **DCA BTC:** sin cambios desde la cuota del lunes (02/11 13:56). Próxima cuota el lunes 09/11.
- **Torneo:** desde la corrida de las 00:55, L9 pasó de +0,50% a -1,10% y L8 de +0,22% a -0,66%: las que le ganan a USDT bajaron de 2 a 0. Régimen: BTC arriba de la media 200, bajando 30 d.
- **Original:** sin dato nuevo de la Mac (03/11 23:39): 100% en USDT, -1,04%.
- **Alarmas:** nadie en +20%, ninguna carpeta parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga nada por resultado; los números van sin suavizar.

- **3 niveles: seguir.** -11,52% contra 0% de USDT y -6,63% de HODL BTC; peor caída -12,94%, peor que la de HODL (-9,67%).
- **Agresiva: seguir.** -12,04%, la peor; 35,50 USD de comisiones en 264 operaciones (29,5% de la pérdida), y en 7 días -4,48% contra -3,59% de HODL.
- **Laboratorio: seguir.** -0,84%, +2,92 pp sobre HODL BTC, peor caída -2,35% contra -6,13% de HODL.
- **DCA BTC: seguir.** -0,38%, la cuota semanal corre bien.
- **Torneo: revisar.** Ninguna de las 33 en positivo; el líder es no hacer nada (P0, 0,00%). Y el `hodl_btc` de `vivo.json` (-5,96%) no coincide con P1 (-4,49%): la vara contra HODL no mide bien.
- **Original: seguir.** -1,04%, +5,74 pp sobre HODL BTC; faltan comisiones y ops (no publica `libro.json`).

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Torneo P0 mejor_que_usdt=0 apagar=ninguna avisos=0
