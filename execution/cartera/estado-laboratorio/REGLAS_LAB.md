# Reglas del laboratorio — v1 (27/10/2026)

Las escribe y reescribe el entrenador (`PROMPT_ENTRENADOR.md`). Quien opera las cumple, no las
mejora. v1 sale de lo que mostraron las otras carpetas entre el 07/10 y el 27/10:
la agresiva hizo 203 operaciones y pagó 26,55 USD de comisiones (2,7% de la carpeta) con stops
de 5% que saltaban en el ruido; la de 3 niveles perdió sobre todo en monedas medianas que caían.
v1 apuesta a lo opuesto: **pocas entradas, sólo a favor de la tendencia, stops más anchos.**

## Cada ciclo (cada 2 h)

1. `radar --corto --top 20` (velas de 1 h, últimas 48 h).
2. **Filtro de mercado:** si BTCUSDT tiene `var_24h` < −2 o `var_4h` < −1,5, **no se abre
   nada nuevo**. Sólo se vigila.
3. **Entrada** (todas a la vez, sobre el mismo par):
   - par entre los 20 de mayor volumen del radar;
   - `var_24h` ≥ +3 y `var_4h` > 0 (viene subiendo y sigue);
   - `var_1h` ≤ +2,5 (no está estirada);
   - `vs_max_48h` ≥ −1,5 (está en zona de máximo, no rebotando de abajo);
   - `volumen_4h_vs_promedio` ≥ 1,3.
4. Si entra más de un par, se elige el de mayor `volumen_4h_vs_promedio`. **Una entrada por
   ciclo como mucho y 4 por día** (contalas en `libro.json` → `operaciones` con fecha UTC de hoy).
5. Tamaño: **20% de la carpeta**. Máximo **3 posiciones** abiertas a la vez.

```bash
python3 execution/cartera/cartera.py orden --lado buy --par <PAR> --usd <20% del total> \
  --nivel trading --stop 7 --trail 8 --tp 10:0.5,20:1 --motivo "[v1] <reglas que cumplió> · invalida: <...>"
```

Nivel `trading` si el par no es BTC/ETH/BNB; `conservador` si lo es (mismos stops y tomas).

## Salidas (además de los stops automáticos)

- Si una posición lleva **48 h** sin tocar +10% ni el stop, se vende entera (`[v1] tiempo`).
- Si el par tiene `var_24h` < 0 **y** `var_4h` < −2, se vende entera (`[v1] tendencia rota`).
- Ninguna otra venta discrecional.

## Si no pasa nada

Quedarse en USDT es una decisión válida. Una `nota` corta con la regla que faltó y listo.
