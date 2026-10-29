# Veredicto de las carpetas cripto — 2026-10-29 18:55 UTC

**En una línea:** 3 niveles (-8,82%) y Agresiva (-8,12%) siguen perdiendo contra USDT (0%) y HODL BTC (~-3,1%). Laboratorio (+0,66%) es la única con historia que le gana a los dos, pero lleva 2 días. La líder del Torneo es un HODL 50/50 (+2,19% en 16 h). Ninguna demuestra todavía que le gane a quedarse quieto.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 911.76 | -8.82% | -5.68 pp (HODL -3.15%) | -0.19% (HODL -0.16%) | -0.74% (HODL -0.40%) | -10.42% (HODL -6.10%) | 2.43 USD (2.8% de la pérdida) | 86 |
| Agresiva | 918.79 | -8.12% | -4.99 pp (HODL -3.13%) | +0.76% (HODL -0.38%) | -1.79% (HODL -0.70%) | -9.70% (HODL -6.27%) | 29.57 USD (36.4% de la pérdida) | 221 |
| Laboratorio | 1006.58 | +0.66% | +0.68 pp (HODL -0.02%) | +0.66% (HODL -0.02%) | falta (arrancó 27/10) | -0.87% (HODL -2.07%) | 1.11 USD (16.9% de la ganancia) | 6 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder P2 HODL 50/50 BTC-ETH | 1021.92 | +2.19% (16 h) | +0.10 pp (P1 HODL BTC +2.09%) | falta (arrancó 29/10 00:00) | falta | -0.41% | 1.00 USD | 2 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37; DCA tiene un solo snapshot, 22:38). El Torneo arrancó después, no entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 22/10 18:06, Agresiva 22/10 18:32).
- **Frescura (ahora 18:50 UTC):** 3 niveles 18:07, Agresiva 18:32, Laboratorio 18:18 (todas < 1 h). DCA 27/10 22:38 (44 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 16:41, última vela 16:00 (límite 8 h). **Todas corren.**
- **Torneo:** 33 estrategias, 16 h de vida. Le ganan a USDT 4 de 33 (P2, P1, P3, P4); a USDT **y** a HODL BTC (P1, +2,09%) sólo 1 de 33 (P2). 29 siguen en 1.000 sin operar. El campo `hodl_btc` de `vivo.json` sigue sin coincidir con P1 (dice +0,53% contra +2,09%); tomé P1 como HODL. Conviene revisarlo.
- **Torneo y la hora:** su foto es de las 16:00; las otras carpetas son de las 18:xx, y en ese rato BTC bajó (el HODL de 3 niveles pasó de 978,98 a 968,54 entre 16:15 y 18:07). No es comparable hora a hora.
- **DCA:** su valor y su HODL son del 27/10 (no tiene snapshots entre cuotas); no refleja lo que se movió BTC desde entonces.
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- Peor caída sobre `total_usd` del `historial.csv` (capital inicial como primer máximo); HODL BTC con su propia columna. Comisiones y ops del `libro.json` (la suma por operación coincide con `comisiones_usd` en las cuatro).
- Historial del Torneo para el récord: armado con las 3 versiones de `vivo.json` en git (08:41, 12:45, 16:41).

## Qué pasó desde ayer

- **3 niveles:** +0,03% en 24 h (911,50 → 911,76), con BTC plano-bajista. Una operación: compra de HYPE por 40 USD (16:15). 276 USD en USDT. -9,4% desde su máximo de 1.006,50.
- **Agresiva:** +0,55% en 24 h (913,77 → 918,79). Diez operaciones: dos salidas de PEPE en pérdida (02:29 -2,55%, 08:32 -3,54%), entradas en BTC y ETH (04:32), HYPE (11:33), BNB (12:39) y ENA (14:48), y toma de ganancia +8% en la mitad de HYPE (15:09). Comisiones 29,57 USD: más de un tercio de lo que pierde. En la ventana común es la que mejor anda de las viejas (+0,76% contra -0,38% de HODL).
- **Laboratorio:** +1,21% en 24 h (994,59 → 1.006,58). Vendió PEPE con -1,2% (10:18), compró HYPE (12:18), UNI (14:37) y ENA (16:24), y tomó +10% en la mitad de HYPE (16:37). Hizo récord de 1.015,43 a las 16:24 y bajó a 1.006,58.
- **DCA BTC:** sin cambios; próxima cuota el lunes 02/11.
- **Torneo:** las cuatro que compraron BTC/ETH de entrada (P1–P4) subieron a récord con la vela de las 16:00; el resto sigue sin operar.
- **Alarmas:** **récord en el Torneo** (P2 1.021,92, también P1, P3 y P4 en su máximo) → mail mandado a facue1900@gmail.com. Laboratorio también tocó récord hoy (16:24) pero ya se había avisado hoy (`alertas.json`), no se repite; y su último snapshot ya no es el máximo. Ninguna carpeta ni estrategia cerca de +20% (la mejor, +2,19%).

## Recomendación

- **3 niveles — apagar.** 21 días (≥14), -8,82% contra 0% de USDT y -3,15% de HODL BTC; en 7 días -0,74%, peor que HODL (-0,40%): no mejoró. Lo decide Facu.
- **Agresiva — apagar.** 21 días, -8,12% contra 0% y -3,13% de HODL. En 7 días -1,79%, peor que HODL (-0,70%). 29,57 USD en comisiones en 221 operaciones: 3 de los 8 puntos que pierde. Lo único a su favor es la ventana común (+0,76%), dos días. Lo decide Facu.
- **Laboratorio — seguir.** +0,66%, arriba de USDT y de HODL BTC (+0,68 pp). Dos días y seis operaciones; no hay con qué juzgarlo.
- **DCA BTC — seguir.** Una cuota; es la referencia barata contra la que se miden las otras.
- **Torneo — seguir.** 16 h de vida; la líder es un HODL, no una estrategia activa.

**¿Key real de Binance?** Hoy, claramente no (la sección formal arranca el 07/11/2026). Las dos carpetas con 21 días pierden contra USDT y contra HODL BTC, y ninguna otra tiene más de dos días.
