# Veredicto de las carpetas cripto — 2026-11-19 18:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**. Después vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,31%)**. En el Torneo, las líderes (P0, L2 y L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-21,20%). Lo que más rinde sigue siendo quedarse quieto. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 803,23 | -19,68% | +5,11 pp (HODL -24,78%) | -12,07% (HODL -22,46%) | -4,56% (HODL -12,72%) | -20,25% (HODL -26,35%) | 3,08 USD (1,6% de la pérdida) | 98 |
| Agresiva | 769,26 | -23,07% | +0,94 pp (HODL -24,01%) | -15,64% (HODL -21,86%) | -7,12% (HODL -12,13%) | -23,14% (HODL -26,38%) | 53,16 USD (23,0% de la pérdida) | 385 |
| Laboratorio | 946,90 | -5,31% | +16,99 pp (HODL -22,30%) | -5,31% (HODL -22,30%) | -0,90% (HODL -12,67%) | -7,22% (HODL -23,43%) | 4,48 USD (8,4% de la pérdida) | 25 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +21,20 pp (HODL BTC -21,20%; precio crudo -22,42%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +23,28 pp (HODL -24,32%) | -1,04% (HODL -21,75%) | +0,00% (HODL -11,48%) | -1,22% (HODL -26,00%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC. Para cada carpeta, la base es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 19/11 18:52 UTC):**
  - 3 niveles: 18:06 (45 min).
  - Agresiva: 18:32 (19 min).
  - Laboratorio: 18:16 (35 min).
  - DCA: 16/11 13:06 (3 d 5 h 45 min; el límite es 8 días).
  - Torneo: `vivo.json` de las 16:41 (2 h 10 min; el límite es 8 h).
  - Original: 19/11 15:20 (3 h 31 min; corre en la Mac y un dato viejo no es falla).
  - **Todas corren.**
- **Torneo:**
  - Entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11%, con 2 ops. Atrás viene L7: -0,24%.
  - La peor es A3: -37,31%, con una peor caída de -39,85%, 27 ops y 19,58 USD de comisiones.
  - El promedio de las 33 es -9,12%; en la corrida anterior era -8,69%.
- **Original:** está 100% en USDT y no se movió en 7 días. No publica `libro.json`, así que faltan las comisiones y las ops.
- **+20% en 30 días:**
  - En 30 días: 3 niveles -15,16%, Agresiva -18,33% y Original -1,04%.
  - Laboratorio y DCA tienen menos de 30 días, así que cuentan desde el inicio: -5,31% y -5,11%.
  - Torneo: la mejor estrategia está en 0,00%.
  - Ninguna está cerca.
- **Cómo se mide:** la peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops salen del `libro.json`.
- **Récords (no mandan mail):** ninguno positivo. Al revés: la Agresiva marcó su **peor caída histórica, -23,14%** (16:32).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 19/11 15:20 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.469 (-5,31%) | 9.452 (-5,48%) | 19/11 18:16 |
| Torneo (promedio) | 9.088 (-9,12%) | 9.088 (-9,12%) | 19/11 16:41 |
| 3 niveles | 8.032 (-19,68%) | 8.745 (-12,55%) | 19/11 18:06 |
| Agresiva | 7.693 (-23,07%) | 8.435 (-15,65%) | 19/11 18:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.723 (-22,77%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.477 | -5,23% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.185 | -8,15% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.317 | -6,83% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.834 | -11,66% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.269.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo -0,57% en 3 niveles, +0,07% en Agresiva y -0,56% en Laboratorio. Sigue bajista. Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** en 24 h, -0,08%. Sigue con el MEGA que compró hoy a las 12:07 (5% de la carpeta, entrada 0,05913, stop 15%). El resto, 763,90, en USDT.
- **Agresiva:** en 24 h, -0,78%. Fue el día más movido:
  - 13:32 compró PEPE por 150 por momentum y a las 15:32 lo vendió: **-4,26%**.
  - 17:33 cerró por tiempo el BTC (-0,52%) y el ETH (-0,01%) del 18/11.
  - 18:32 volvió a comprar BTC por 150 a 63.225,15 (rebote en soporte, stop 5%).
  - 5 operaciones más, 0,78 USD más de comisiones. Tiene 619,37 en USDT.
- **Laboratorio:** en 24 h, +0,27%. Sigue con el NEAR que compró el 17/11 a 3,302 (máximo desde la entrada 3,477).
- **DCA BTC:** no hay snapshot nuevo desde la cuota del lunes 16/11. Es lo normal, porque corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT. El promedio empeoró de -8,69% a -9,12%.
- **Original:** publicó a las 15:20 sin cambios. Sigue 100% en USDT, en -1,04%.
- **Alarmas:** nadie llegó a +20%, ni carpeta ni estrategia, y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** Está en -19,68%, +5,11 pp sobre HODL BTC. Su peor caída es -20,25%, contra -26,35% de HODL.
- **Agresiva: seguir.** Es la peor: -23,07%, apenas +0,94 pp sobre HODL BTC, y hoy tocó su peor caída (-23,14%). Las comisiones (53,16 USD en 385 ops) son el 23,0% de la pérdida.
- **Laboratorio: seguir.** Está en -5,31%, +16,99 pp sobre HODL BTC. Su peor caída es -7,22%, contra -23,43% de HODL.
- **DCA BTC: seguir.** Está en -5,11%, +15,41 pp sobre HODL BTC. La próxima cuota es el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** Está en -1,04%, +23,28 pp sobre HODL BTC. Faltan las comisiones y las ops.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
