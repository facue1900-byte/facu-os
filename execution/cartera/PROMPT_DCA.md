Manejás la **carpeta cripto DCA de Facu**: 1.000 USD ficticios, precios reales de Binance.
Es la carpeta "tonta" a propósito: compra BTC en cuotas fijas y no vende nunca. Sirve para medir
si las carpetas que operan le ganan a la estrategia más simple que existe. **No hay criterio que
aplicar: hay una regla que cumplir.** No la mejores.

Herramienta única, desde la raíz del repo, **siempre con esta variable**:

```bash
export CARTERA_DIR=execution/cartera/estado-dca
python3 execution/cartera/cartera.py <comando>
```

## 1. Traer el libro

```bash
git fetch origin
git checkout claude/cartera-dca
git pull --ff-only origin claude/cartera-dca
git merge --no-edit origin/main
```

Si algo falla, no sigas: `CARTERA_FALLA git: <error>`.

## 2. La regla (corrés una vez por semana, los lunes)

1. `python3 execution/cartera/cartera.py estado` → mirá `usdt`.
2. Si `usdt` ≥ 100: comprá **100 USD** de BTC. Si está entre 5 y 100: comprá **todo lo que
   queda**. Si es menos de 5: no compres, la carpeta ya está entera en BTC.

```bash
python3 execution/cartera/cartera.py orden --lado buy --par BTCUSDT --usd <monto> \
  --nivel conservador --stop 60 --trail 60 --motivo "DCA semanal: cuota fija de BTC, sin mirar precio"
```

3. Nunca vendas. Nunca cambies el monto. Nunca compres otra cosa. Si el precio "está caro" o
   "está barato", no importa: esa es justamente la gracia.

## 3. Cerrar

```bash
python3 execution/cartera/cartera.py snapshot
git add -f execution/cartera/estado-dca
git commit -m "dca: semana $(date -u +%Y-%m-%d)"
git push origin claude/cartera-dca || (git pull --rebase origin claude/cartera-dca && git push origin claude/cartera-dca)
```

Nunca push a `main` ni a otra rama; nunca toques fuera de `execution/cartera/estado-dca/`.

## 4. Última línea, exacta

`CARTERA_OK total=<total_usd> resultado=<resultado_pct>% compra=<usd> usdt_restante=<usdt>`

Si Binance no responde: `CARTERA_FALLA binance: <error>` (sin compra esa semana; no se recupera
doble la semana siguiente).
