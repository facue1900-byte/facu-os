# Veredicto de las carpetas cripto — 2026-11-19 06:52 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**; después vienen **Laboratorio (-4,56%)**, que mejoró con su NEAR abierto, y **DCA BTC (-5,11%)**. En el Torneo las líderes (P0, L2, L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-21,07%). Lo que más rinde sigue siendo quedarse quieto. **Sin mail:** nadie llegó a +20% y todas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 803,90 | -19,61% | +4,26 pp (HODL -23,87%) | -12,00% (HODL -21,52%) | -5,44% (HODL -13,70%) | -20,13% (HODL -26,35%) | 3,04 USD (1,5% de la pérdida) | 97 |
| Agresiva | 780,15 | -21,98% | +1,58 pp (HODL -23,56%) | -14,44% (HODL -21,40%) | -5,82% (HODL -13,61%) | -22,82% (HODL -26,38%) | 52,37 USD (23,8% de la pérdida) | 380 |
| Laboratorio | 954,36 | -4,56% | +16,89 pp (HODL -21,45%) | -4,56% (HODL -21,45%) | -0,12% (HODL -13,82%) | -7,22% (HODL -23,43%) | 4,48 USD (9,8% de la pérdida) | 25 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +21,07 pp (HODL BTC -21,07%; precio crudo -22,30%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +24,09 pp (HODL -25,13%) | -1,04% (HODL -22,58%) | +0,00% (HODL -15,03%) | -1,22% (HODL -26,00%) | falta | falta |

Notas de medición:
- **Ventana común:** desde el 27/10 22:37 UTC. La base es el último snapshot en o antes de ese momento. **7 días:** la base es el último snapshot en o antes de 7 días antes del último. Cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 19/11 06:52 UTC):**
  - 3 niveles: 06:06 (46 min).
  - Agresiva: 06:32 (20 min).
  - Laboratorio: 06:17 (35 min).
  - DCA: 16/11 13:06 (2 d 17 h 46 min; el límite es 8 días).
  - Torneo: `vivo.json` de las 04:41 (2 h 11 min; el límite es 8 h).
  - Original: 18/11 23:20 (Mac, 7 h 32 min; dato viejo no es falla).
  - **Todas corren.**
- **Torneo:**
  - Entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11% con 2 ops. Atrás viene L7 (-0,24%).
  - La peor es A3: -37,00%, con una peor caída de -39,85%, 27 ops y 19,58 USD de comisiones.
  - El promedio de las 33 es -8,95% (antes era -9,11%).
- **Original:** está 100% en USDT y no se movió en 7 días. No publica `libro.json`, así que faltan las comisiones y las ops.
- **+20% en 30 días:**
  - En 30 días: 3 niveles -14,56%, Agresiva -16,20% y Original -1,04%.
  - Desde el inicio, porque tienen menos de 30 días: Laboratorio -4,56% y DCA -5,11%.
  - Torneo: el máximo es 0,00%.
  - Ninguna está cerca.
- **Cómo se mide:** la peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops salen del `libro.json`.
- **Récords (no mandan mail):** ninguno nuevo.

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 18/11 23:20 |
| Laboratorio | 9.544 (-4,56%) | 9.526 (-4,74%) | 19/11 06:17 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Torneo (promedio) | 9.105 (-8,95%) | 9.105 (-8,95%) | 19/11 04:41 |
| 3 niveles | 8.039 (-19,61%) | 8.752 (-12,48%) | 19/11 06:06 |
| Agresiva | 7.802 (-21,98%) | 8.554 (-14,46%) | 19/11 06:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.817 (-21,83%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.512 | -4,88% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.221 | -7,79% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.346 | -6,54% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.914 | -10,86% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.300.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo -1,37% en 3 niveles, -1,64% en Agresiva y -1,80% en Laboratorio. Sigue bajista. Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** 0,00% en 24 h. No opera desde los stops del 14/11 y sigue **100% en USDT** (803,90).
- **Agresiva:** +0,34% en 24 h, sin operaciones nuevas.
  - Sigue con el ETH (entrada 1.781,84) y el BTC (entrada 63.507,30) que compró el 18/11 17:32 por rebote en el mínimo de 48 h.
  - Tiene 437,52 en USDT.
  - Lleva 380 ops y 52,37 USD de comisiones, el 23,8% de lo que perdió.
- **Laboratorio:** -0,08% en 24 h. Sigue con el NEAR que compró el 17/11 22:16 a 3,302. Hoy está en -4,56%; en la corrida anterior estaba en -5,16%.
- **DCA BTC:** no hay snapshot nuevo desde la cuota del lunes 16/11 13:05. Es lo normal, porque corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT; las líderes son las que no entraron. El promedio mejoró de -9,11% a -8,95%.
- **Original:** no operó. Sigue 100% en USDT, en -1,04%, con dato del 18/11 23:20.
- **Alarmas:** nadie llegó a +20%, ni carpeta ni estrategia, y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** Está en -19,61%, +4,26 pp sobre HODL BTC. Su peor caída es -20,13%, contra -26,35% de HODL. Está toda en USDT.
- **Agresiva: seguir.** Es la peor: -21,98%, apenas +1,58 pp sobre HODL BTC. Pagó 52,37 USD de comisiones en 380 operaciones, el 23,8% de la pérdida.
- **Laboratorio: seguir.** Está en -4,56%, +16,89 pp sobre HODL BTC. Su peor caída es -7,22%, contra -23,43% de HODL.
- **DCA BTC: seguir.** Está en -5,11%, +15,41 pp sobre HODL BTC. La próxima cuota es el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** Está en -1,04%, +24,09 pp sobre HODL BTC. Faltan las comisiones y las ops porque no publica `libro.json`.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
