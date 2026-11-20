# Veredicto de las carpetas cripto — 2026-11-20 00:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**. Atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**, que esta noche salió de NEAR por stop. En el Torneo, las líderes (P0, L2 y L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-22,59%). Lo que más rinde sigue siendo quedarse quieto. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 803,54 | -19,65% | +5,94 pp (HODL -25,58%) | -12,04% (HODL -23,29%) | -4,36% (HODL -13,12%) | -20,25% (HODL -27,17%) | 3,08 USD (1,6% de la pérdida) | 98 |
| Agresiva | 762,17 | -23,78% | +1,75 pp (HODL -25,54%) | -16,41% (HODL -23,43%) | -7,65% (HODL -13,01%) | -23,88% (HODL -27,50%) | 53,69 USD (22,6% de la pérdida) | 389 |
| Laboratorio | 942,34 | -5,77% | +17,39 pp (HODL -23,16%) | -5,77% (HODL -23,16%) | -1,38% (HODL -12,95%) | -7,22% (HODL -24,19%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +22,59 pp (HODL BTC -22,59%; precio crudo -23,80%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +24,60 pp (HODL -25,64%) | -1,04% (HODL -23,12%) | +0,00% (HODL -12,93%) | -1,22% (HODL -26,51%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC. Para cada carpeta, la base es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 20/11 00:52 UTC):**
  - 3 niveles: 00:06 (46 min).
  - Agresiva: 00:32 (20 min).
  - Laboratorio: 00:16 (36 min).
  - DCA: 16/11 13:06 (3 d 11 h 46 min; el límite es 8 días).
  - Torneo: `vivo.json` de las 00:41 (11 min; el límite es 8 h).
  - Original: 20/11 00:05 (47 min; corre en la Mac y un dato viejo no es falla).
  - **Todas corren.**
- **Torneo:**
  - Entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11%, con 2 ops. Atrás vienen L7 (-0,24%) y L6 (-0,28%).
  - La peor es A3: -37,21%, con una peor caída de -39,85%, 27 ops y 19,58 USD de comisiones.
  - El promedio de las 33 es -9,50%; en la corrida anterior era -9,12%.
- **Original:** está 100% en USDT y no se movió en 7 días. No publica `libro.json`, así que faltan las comisiones y las ops.
- **+20% en 30 días:**
  - En 30 días: 3 niveles -15,72%, Agresiva -19,95% y Original -1,04%.
  - Laboratorio y DCA tienen menos de 30 días, así que cuentan desde el inicio: -5,77% y -5,11%.
  - Torneo: la mejor estrategia está en 0,00%.
  - Ninguna está cerca.
- **Cómo se mide:** la peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops salen del `libro.json`.
- **Récords (no mandan mail):** ninguno positivo. Al revés: la Agresiva marcó otra vez su **peor caída histórica, -23,88%** (00:32), contra -23,14% de la corrida anterior.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 20/11 00:05 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 20/11 00:16 |
| Torneo (promedio) | 9.050 (-9,50%) | 9.050 (-9,50%) | 20/11 00:41 |
| 3 niveles | 8.035 (-19,65%) | 8.748 (-12,52%) | 20/11 00:06 |
| Agresiva | 7.622 (-23,78%) | 8.357 (-16,43%) | 20/11 00:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.641 (-23,59%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.447 | -5,53% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.159 | -8,41% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.301 | -6,99% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.775 | -12,25% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.279.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo -1,23% en 3 niveles, -1,38% en Agresiva y -1,12% en Laboratorio. BTC tocó 61.428 a las 21 UTC. Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** en 24 h, -0,04%. Sigue con el MEGA del 19/11 (5% de la carpeta, entrada 0,05913, stop 15%). El resto, 763,90, en USDT.
- **Agresiva:** en 24 h, -1,65%. Desde la corrida anterior:
  - 19:32 compró UNI por 120 (rebote en soporte).
  - 20:32 vendió el BTC de las 18:32 porque perdió el soporte: **-1,89%**.
  - 22:32 volvió a comprar BTC por 150 a 62.178,6 y ETH por 120 a 1.759,8.
  - 4 operaciones más, 0,53 USD más de comisiones. Tiene 376,25 en USDT y tres posiciones abiertas.
- **Laboratorio:** en 24 h, -0,64%. A las 21:32 saltó el stop del NEAR (entrada 3,302, salida 3,199): **-3,12%**. Quedó 100% en USDT.
- **DCA BTC:** no hay snapshot nuevo desde la cuota del lunes 16/11. Es lo normal, porque corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT. El promedio empeoró de -9,12% a -9,50%.
- **Original:** publicó a las 00:05 sin cambios. Sigue 100% en USDT, en -1,04%.
- **Alarmas:** nadie llegó a +20%, ni carpeta ni estrategia, y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** Está en -19,65%, +5,94 pp sobre HODL BTC. Su peor caída es -20,25%, contra -27,17% de HODL.
- **Agresiva: seguir.** Es la peor: -23,78%, apenas +1,75 pp sobre HODL BTC, y volvió a tocar su peor caída (-23,88%). Las comisiones (53,69 USD en 389 ops) son el 22,6% de la pérdida.
- **Laboratorio: seguir.** Está en -5,77%, +17,39 pp sobre HODL BTC. Su peor caída es -7,22%, contra -24,19% de HODL.
- **DCA BTC: seguir.** Está en -5,11%, +15,41 pp sobre HODL BTC. La próxima cuota es el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** Está en -1,04%, +24,60 pp sobre HODL BTC. Faltan las comisiones y las ops.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
