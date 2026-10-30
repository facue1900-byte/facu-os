# Veredicto de las carpetas cripto — 2026-10-30 00:55 UTC

**En una línea:** ninguna carpeta le gana a quedarse en USDT (0%). La que menos pierde es la DCA BTC (-0,01% en su foto del 27/10; -0,39% al precio de hoy), seguida por el Laboratorio (-0,84%, pero +2,96 pp arriba de HODL BTC). 3 niveles (-11,51%) y Agresiva (-10,45%) siguen perdiendo contra USDT y contra HODL BTC. En el Torneo la "líder" es no hacer nada: 27 de 33 estrategias siguen en 1.000 sin operar y ninguna le gana a USDT.

| Carpeta | Total | Desde inicio | vs HODL BTC | Ventana común | 7 días | Peor caída | Comisiones | Ops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 niveles | 884.94 | -11.51% | -5.28 pp (HODL -6.23%) | -3.13% (HODL -3.33%) | -3.88% (HODL -3.78%) | -12.08% (HODL -7.73%) | 2.54 USD (2.2% de la pérdida) | 89 |
| Agresiva | 895.48 | -10.45% | -2.86 pp (HODL -7.59%) | -1.79% (HODL -4.98%) | -4.20% (HODL -5.44%) | -10.45% (HODL -9.33%) | 30.63 USD (29.3% de la pérdida) | 228 |
| Laboratorio | 991.57 | -0.84% | +2.96 pp (HODL -3.80%) | -0.84% (HODL -3.80%) | falta (arrancó 27/10) | -2.35% (HODL -4.61%) | 1.60 USD (19.0% de la pérdida) | 9 |
| DCA BTC | 999.90 | -0.01% | -0.02 pp (HODL +0.01%, al 27/10) | 0.00% (un solo snapshot) | falta (arrancó 27/10) | -0.01% (un solo snapshot) | 0.10 USD (toda la pérdida) | 1 |
| Torneo — líder P0 USDT quieto (empatada con 26 más en 1.000) | 1000.00 | 0.00% (24 h) | +2.6 pp (P1 HODL BTC -2.6%) | falta (arrancó 29/10 00:00) | falta | 0.00% | 0.00 USD | 0 |
| 10.000 USD (Mac) | — | — | — | — | — | — | — | — |

Notas de medición:
- **Ventana común** = desde el 27/10 22:37 UTC. Base: último snapshot en o antes de ese momento (3 niveles 22:07, Agresiva 22:32, Laboratorio 22:37). DCA tiene un solo snapshot (22:38). El Torneo arrancó después, no entra.
- **7 días** = contra el último snapshot en o antes de 7 días antes del último (3 niveles 23/10 00:06, Agresiva 23/10 00:32).
- **Frescura (ahora 00:51 UTC):** 3 niveles 00:06, Agresiva 00:32, Laboratorio 00:16 (todas < 1 h). DCA 27/10 22:38 (50 h; corre los lunes, límite 8 días). Torneo: `vivo.json` generado 00:42, última vela 00:00 (límite 8 h). **Todas corren.**
- **DCA a precio de hoy:** su foto es del 27/10 y no refleja que BTC bajó. Con el precio de BTC que implica el HODL del Laboratorio a las 00:16 (77.768, mismo BTC de inicio que la DCA), su cuota de 0,0012356 BTC vale 96,09 → total **996,09 (-0,39%)** contra HODL BTC -3,79%. Es cálculo, no el snapshot oficial; la tabla deja el oficial.
- **Torneo:** 33 estrategias, 24 h de vida. Le ganan a USDT **0 de 33**; a HODL BTC (P1, -2,6%) 30 de 33 — pero 27 de esas 30 es porque no operaron. Las únicas que operaron y le ganan a HODL: P4 60/40 (-1,6%) y L1/L1N (-1,4%). Mercado según el torneo: "BTC arriba de la media 200, bajando 30 d".
- **La carpeta de 10.000 USD** vive en la Mac de Facu: desde la nube no se ve y no se juzga.
- Peor caída sobre `total_usd` del `historial.csv` (capital inicial como primer máximo); HODL BTC con su propia columna. Comisiones y ops del `libro.json` (la suma por operación coincide con `comisiones_usd` en las cuatro).

## Qué pasó desde ayer

- **3 niveles:** -3,67% en 24 h (918,62 → 884,94), con HODL BTC -3,76%. Tres stops automáticos a la noche: TAO -16,9% (20:42), LINK -18,0% y SOL -18,0% (20:47). Antes compró HYPE por 40 USD (16:15). 387 USD en USDT, -12,1% desde su máximo de 1.006,50.
- **Agresiva:** -2,15% en 24 h (915,15 → 895,48), con HODL BTC -5,29%. Dieciséis operaciones: entró y salió de PEPE, BTC, ETH, BNB, ENA y HYPE dos veces; ganó en HYPE (+8,0% y +7,8%) y perdió en casi todo lo demás (PEPE -2,6% y -3,5%, BNB -2,5%, ETH -2,2%, BTC -1,1%, HYPE -4,75% en el último stop de 23:08). Quedó 100% en USDT. Las comisiones ya son 30,63 USD: casi un tercio de lo que pierde.
- **Laboratorio:** -1,02% en 24 h (1.001,80 → 991,57), con HODL BTC -4,28%. Vendió PEPE (-1,2%), compró HYPE, UNI y ENA; tomó +10% en la mitad de HYPE (16:37), salió de ENA (-4,4%) y UNI (-3,4%) a las 20:18 y el resto de HYPE por stop con +1,4% (23:43). Quedó 100% en USDT. Ayer hizo récord de 1.015,43; hoy está 2,35% abajo de ese máximo.
- **DCA BTC:** sin cambios; próxima cuota el lunes 02/11.
- **Torneo:** BTC y ETH bajaron y arrastraron a las cuatro que compraron de entrada (P1–P4, ayer en récord) a entre -1,6% y -3,4%. L1/L1N operaron dos veces y van -1,4%. El resto sigue sin operar.
- **Alarmas:** ninguna. Ninguna carpeta ni estrategia está en su máximo **y** arriba del capital inicial, y la mejor está en 0%, lejos de +20%. No se mandó mail.

## Recomendación

- **3 niveles — apagar.** 22 días (≥14), -11,51% contra 0% de USDT y -6,23% de HODL BTC; en 7 días -3,88%, peor que HODL (-3,78%): no mejoró. Lo decide Facu.
- **Agresiva — apagar.** 22 días, -10,45% contra 0% y -7,59% de HODL. En 7 días perdió 4,20% más (le ganó a HODL, -5,44%, pero sigue perdiendo plata): no mejoró. 30,63 USD en comisiones en 228 operaciones. Lo decide Facu.
- **Laboratorio — seguir.** -0,84%, abajo de USDT pero +2,96 pp arriba de HODL BTC, con una caída máxima (-2,35%) que es la mitad de la de HODL (-4,61%). Dos días y nueve operaciones; no hay con qué juzgarlo.
- **DCA BTC — seguir.** Una cuota; es la referencia barata contra la que se miden las otras.
- **Torneo — seguir.** 24 h de vida; la que va primera es no operar.

**¿Key real de Binance?** No (la sección formal arranca el 07/11/2026). Ninguna carpeta le gana a USDT, y las dos con 22 días pierden más de 10%.

JUEZ_OK lider=DCA BTC mejor_que_usdt=0 apagar=3 niveles,Agresiva avisos=0
