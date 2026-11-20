# Veredicto de las carpetas cripto — 2026-11-20 06:53 UTC

**En una línea:** **ninguna carpeta le gana a USDT.** La que menos pierde sigue siendo **Original (-1,04%)**. Atrás vienen **DCA BTC (-5,11%)** y **Laboratorio (-5,77%)**. A las 03:49 a **3 niveles** le saltó el stop del MEGA (-12,8%) y quedó 100% en USDT. En el Torneo, las líderes (P0, L2 y L5) siguen en 0,00% porque nunca operaron: **0 de 33 le ganan a USDT** y 29 le ganan a HODL BTC (-22,38%). Lo que más rinde sigue siendo quedarse quieto. **Sin mail:** nadie llegó a +20% y todas las carpetas corren.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 798,73 | -20,13% | +5,74 pp (HODL -25,87%) | -12,56% (HODL -23,58%) | -3,00% (HODL -9,36%) | -20,64% (HODL -27,42%) | 3,11 USD (1,5% de la pérdida) | 99 |
| Agresiva | 757,66 | -24,23% | +1,40 pp (HODL -25,63%) | -16,91% (HODL -23,53%) | -7,83% (HODL -10,17%) | -24,31% (HODL -27,50%) | 54,05 USD (22,3% de la pérdida) | 392 |
| Laboratorio | 942,34 | -5,77% | +17,69 pp (HODL -23,45%) | -5,77% (HODL -23,45%) | -1,38% (HODL -10,33%) | -7,22% (HODL -24,50%) | 4,67 USD (8,1% de la pérdida) | 26 |
| DCA BTC | 948,91 | -5,11% | +15,41 pp (HODL -20,52%) | falta (el primer snapshot es del 27/10 22:38, 1 min después del corte) | -4,75% (HODL -17,60%; base 02/11 13:56) | -5,11% (HODL -20,53%) | 0,40 USD (0,8% de la pérdida) | 4 |
| Torneo: líder empatado entre P0 USDT quieto, L2 y L5, que no operaron nunca (0 de 33 le ganan a USDT; 29 le ganan a HODL BTC) | 1.000,00 | +0,00% (desde 29/10) | +22,38 pp (HODL BTC -22,38%; precio crudo -23,59%) | falta (arrancó el 29/10 00:00) | ≈ igual que desde el inicio (+0,00%) | 0,00% | 0,00 USD | 0 |
| Original 10.000 (Mac) | 9.896,38 | -1,04% | +24,60 pp (HODL -25,64%) | -1,04% (HODL -23,12%) | +0,00% (HODL -12,93%) | -1,22% (HODL -26,51%) | falta | falta |

Notas de medición:
- **Ventana común:** arranca el 27/10 22:37 UTC. Para cada carpeta, la base es su último snapshot en o antes de ese momento.
- **7 días:** la base es el último snapshot en o antes de 7 días antes del último.
- **HODL BTC:** cada carpeta se compara contra la columna `hodl_btc` de su propio `historial.csv`.
- **Frescura (ahora 20/11 06:53 UTC):**
  - 3 niveles: 06:07 (46 min).
  - Agresiva: 06:32 (21 min).
  - Laboratorio: 06:16 (37 min).
  - DCA: 16/11 13:06 (3 d 17 h 47 min; el límite es 8 días).
  - Torneo: `vivo.json` de las 04:41 (2 h 12 min; el límite es 8 h).
  - Original: 20/11 00:05 (6 h 48 min; corre en la Mac y un dato viejo no es falla).
  - **Todas corren.**
- **Torneo:**
  - Entre las que operaron, la mejor sigue siendo L4 (cruce 20/50 en las 14): -0,11%, con 2 ops. Atrás vienen L7 (-0,24%) y L6 (-0,28%).
  - La peor es A3: -37,37%, con una peor caída de -39,85%, 27 ops y 19,58 USD de comisiones.
  - El promedio de las 33 es -9,61%; en la corrida anterior era -9,50%.
- **Original:** está 100% en USDT y no se movió en 7 días. No publica `libro.json`, así que faltan las comisiones y las ops.
- **+20% en 30 días:**
  - En 30 días: 3 niveles -15,93%, Agresiva -19,06% y Original -1,04%.
  - Laboratorio y DCA tienen menos de 30 días, así que cuentan desde el inicio: -5,77% y -5,11%.
  - Torneo: la mejor estrategia está en 0,00%.
  - Ninguna está cerca.
- **Cómo se mide:** la peor caída sale del `total_usd` del `historial.csv`, con el capital inicial como primer máximo. Comisiones y ops salen del `libro.json`.
- **Récords (no mandan mail):** ninguno positivo. Al revés: **3 niveles** marcó su peor caída histórica, **-20,64%** (antes -20,25%), y la **Agresiva** también, **-24,31%** (antes -23,88%).

## Si fueran 10.000

Todo llevado a 10.000 USD. La ventana común arranca el 29/10/2026 (largada del Torneo).

| Caja | Desde su inicio | Desde la ventana | Dato al |
|---|---:|---:|---|
| Original | 9.896 (-1,04%) | 9.899 (-1,01%) | 20/11 00:05 |
| DCA | 9.489 (-5,11%) | 9.490 (-5,10%) | 16/11 13:06 |
| Laboratorio | 9.423 (-5,77%) | 9.406 (-5,94%) | 20/11 06:16 |
| Torneo (promedio) | 9.039 (-9,61%) | 9.039 (-9,61%) | 20/11 04:41 |
| 3 niveles | 7.987 (-20,13%) | 8.696 (-13,04%) | 20/11 06:07 |
| Agresiva | 7.577 (-24,23%) | 8.308 (-16,92%) | 20/11 06:32 |
| *Quedarse en USDT* | — | 10.000 (+0,00%) | — |
| *HODL BTC* | — | 7.612 (-23,88%) | — |

| Reparto de 10.000 | Pesos | Hoy | Resultado |
|---|---|---:|---:|
| Sin 3 niveles ni Agresiva | 40% Laboratorio, 30% Torneo (promedio), 30% Original | 9.444 | -5,56% |
| Parejo | 17% Original, 17% 3 niveles, 17% Agresiva, 17% Laboratorio, 17% DCA, 17% Torneo (promedio) | 9.140 | -8,60% |
| Prudente | 40% Original, 30% 3 niveles, 20% Laboratorio, 10% Agresiva | 9.281 | -7,19% |
| Agresivo | 50% Agresiva, 30% Torneo (promedio), 20% Laboratorio | 8.747 | -12,53% |

Torneo, 33 estrategias: mejor P0 USDT quieto 10.000; peor A3 la que más subió en 7 d, rota cada día 6.263.

Regla de tres sobre resultados reales: con 10.000 reales las órdenes mueven más el precio. El Torneo entra en la vela siguiente a la largada (04:00 del 29/10), así que su número no incluye esas primeras 4 horas. La DCA invierte de a 1.000 por semana: el resto sigue en USDT.

## Qué pasó desde ayer

- **Mercado:** en 24 h, HODL BTC hizo -2,62% en 3 niveles, -2,71% en Agresiva y -2,54% en Laboratorio. Régimen: **BTC abajo de la media 200, bajando 30 d**.
- **3 niveles:** en 24 h, -0,64%. A las 03:49 saltó el stop del MEGA que había comprado el 19/11 (entrada 0,05913, salida 0,051595): **-12,8%**, 5,13 USD sobre los 40 puestos. Quedó 100% en USDT (798,73).
- **Agresiva:** en 24 h, -2,88%, peor que HODL BTC en ese plazo (-2,71%). Desde la corrida anterior:
  - 01:54 saltó el stop del UNI (entrada 5,031, salida 4,808): **-4,5%**.
  - 02:31 vendió el ETH de las 22:32 porque se invalidó el rebote (entrada 1.759,8, salida 1.733,05): **-1,6%**.
  - 06:32 volvió a comprar ETH por 120 a 1.743,69 (otro rebote en soporte).
  - 3 operaciones más, 0,36 USD más de comisiones. Tiene 488,64 en USDT, BTC (entrada 62.178,6) y ETH abiertos.
- **Laboratorio:** en 24 h, -1,25% (el stop del NEAR de anoche). Sigue 100% en USDT, sin cambios desde la corrida anterior.
- **DCA BTC:** no hay snapshot nuevo desde la cuota del lunes 16/11. Es lo normal, porque corre los lunes. Le quedan 600 USD en USDT.
- **Torneo:** 0 de 33 le ganan a USDT. El promedio empeoró de -9,50% a -9,61%.
- **Original:** sin publicación nueva desde las 00:05. Sigue 100% en USDT, en -1,04%.
- **Alarmas:** nadie llegó a +20%, ni carpeta ni estrategia, y ninguna carpeta está parada. **No se mandó mail.**

## Recomendación

Hasta el 27/01/2027 no se apaga ninguna carpeta por resultado. Los números van sin suavizar.

- **3 niveles: seguir.** Está en -20,13%, +5,74 pp sobre HODL BTC. Su peor caída es -20,64%, contra -27,42% de HODL.
- **Agresiva: seguir.** Es la peor: -24,23%, apenas +1,40 pp sobre HODL BTC, y volvió a tocar su peor caída (-24,31%). Las comisiones (54,05 USD en 392 ops) son el 22,3% de la pérdida.
- **Laboratorio: seguir.** Está en -5,77%, +17,69 pp sobre HODL BTC. Su peor caída es -7,22%, contra -24,50% de HODL.
- **DCA BTC: seguir.** Está en -5,11%, +15,41 pp sobre HODL BTC. La próxima cuota es el lunes 23/11.
- **Torneo: seguir.** 0 de 33 le ganan a USDT; las líderes son las que no hicieron nada.
- **Original: seguir.** Está en -1,04%, +24,60 pp sobre HODL BTC. Faltan las comisiones y las ops.

Key real: se decide el 27/01/2027.

JUEZ_OK lider=Original mejor_que_usdt=0 apagar=ninguna avisos=0
