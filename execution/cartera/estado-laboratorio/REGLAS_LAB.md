# Reglas del laboratorio — v3 (28/11/2026)

Las escribe y reescribe el entrenador (`PROMPT_ENTRENADOR.md`). Quien opera las cumple, no las
mejora. **Cambio de v2 a v3: una sola cosa — espera de 7 días para volver a entrar a un par que
cerró su última vuelta en pérdida** (regla 3, último punto). Todo lo demás queda igual que v2.
Por qué: las 4 veces que el lab volvió a entrar a un par a menos de 7 días de cerrarlo en pérdida
perdió las 4 (UNI 04/11, NEAR 17/11 12 h, NEAR 17/11 22 h, NEAR 25/11; −22,08 USD en total, el 30%
de lo que perdió el lab). En la historia (velas de 4 h desde 2021, ventanas de 30 d) la espera
de 7 d mejora la mediana y la peor caída en el total y en el mercado de hoy; en 2025-2026 la
mediana empeora un poco (−0,34% → −0,47%). Ver `ENTRENADOR.md` 28/11.

v2 (06/11): máximo 1 posición abierta a la vez (antes 3), porque las 5 entradas de v1 abiertas
con otra posición ya abierta perdieron las 5.

v1 (27/10) salió de lo que mostraron las otras carpetas entre el 07/10 y el 27/10:
la agresiva hizo 203 operaciones y pagó 26,55 USD de comisiones (2,7% de la carpeta) con stops
de 5% que saltaban en el ruido; la de 3 niveles perdió sobre todo en monedas medianas que caían.
La idea sigue siendo la opuesta: **pocas entradas, sólo a favor de la tendencia, stops más anchos.**

## Cada ciclo (cada 2 h)

1. `radar --corto --top 20` (velas de 1 h, últimas 48 h).
2. **Filtro de mercado:** si BTCUSDT tiene `var_24h` < −2 o `var_4h` < −1,5, **no se abre
   nada nuevo**. Sólo se vigila.
3. **Entrada** (todas a la vez, sobre el mismo par):
   - par entre los 20 de mayor volumen del radar;
   - `var_24h` ≥ +3 y `var_4h` > 0 (viene subiendo y sigue);
   - `var_1h` ≤ +2,5 (no está estirada);
   - `vs_max_48h` ≥ −1,5 (está en zona de máximo, no rebotando de abajo);
   - `volumen_4h_vs_promedio` ≥ 1,3;
   - **(v3) el par no está en espera:** en `libro.json` → `operaciones`, buscá la última venta
     de ese par. Si fue hace **menos de 168 h** y la vuelta que cerró dio pérdida (sumado: lo
     que se cobró en las ventas de esa vuelta < lo que se pagó en su compra), el par no entra
     (anotalo en la `nota`: "PAR en espera hasta <fecha>"). Si el par nunca se operó, si la
     última vuelta dio ganancia o si pasaron 168 h, no hay espera.
4. Si entra más de un par, se elige el de mayor `volumen_4h_vs_promedio`. **Una entrada por
   ciclo como mucho y 4 por día** (contalas en `libro.json` → `operaciones` con fecha UTC de hoy).
5. Tamaño: **20% de la carpeta**. Máximo **1 posición** abierta a la vez: si ya hay una
   posición abierta, **no se abre nada nuevo** aunque otro par cumpla todo (se anota en la
   `nota` qué par cumplía). Se vuelve a poder entrar recién cuando esa posición se cerró entera.

```bash
python3 execution/cartera/cartera.py orden --lado buy --par <PAR> --usd <20% del total> \
  --nivel trading --stop 7 --trail 8 --tp 10:0.5,20:1 --motivo "[v3] <reglas que cumplió> · invalida: <...>"
```

Nivel `trading` si el par no es BTC/ETH/BNB; `conservador` si lo es (mismos stops y tomas).

## Salidas (además de los stops automáticos)

- Si una posición lleva **48 h** sin tocar +10% ni el stop, se vende entera (`[v3] tiempo`).
- Si el par tiene `var_24h` < 0 **y** `var_4h` < −2, se vende entera (`[v3] tendencia rota`).
- Ninguna otra venta discrecional.

## Si no pasa nada

Quedarse en USDT es una decisión válida. Una `nota` corta con la regla que faltó y listo.
