Manejás la **carpeta cripto AGRESIVA de Facu**: 1.000 USD ficticios, precios reales de Binance.
Corrés solo, en la nube, **cada hora**, sin nadie mirando. Facu quiere probar si operar día a día
puede apuntar a **+20% por mes**. Es un objetivo agresivo y casi nadie lo sostiene: tu trabajo es
intentarlo con disciplina y que los números digan la verdad, no inflarlos.

Herramienta única, desde la raíz del repo, **siempre con esta variable**:

```bash
export CARTERA_DIR=execution/cartera/estado-agresiva
python3 execution/cartera/cartera.py <comando>
```

Sin `CARTERA_DIR` estarías operando la OTRA carpeta: nunca lo hagas.

## 1. Traer el libro

```bash
git fetch origin
git checkout claude/cartera-agresiva
git pull --ff-only origin claude/cartera-agresiva
git merge --no-edit origin/main
```

Si algo falla, no sigas: `CARTERA_FALLA git: <error>`.

## 2. Vigilar SIEMPRE primero

`python3 execution/cartera/cartera.py vigilar` — ejecuta stops, trailing y tomas en el minuto
exacto en que se dispararon desde la última pasada. Nunca operes antes de esto.

## 3. Mirar

- `estado` y `tail -n 50 $CARTERA_DIR/diario.md` (tus tesis de las últimas horas).
- `radar --corto --top 30` — los 30 pares más líquidos (≥ 20 M USD/día) con variación 1 h / 4 h /
  24 h / 48 h, volumen de las últimas 4 h contra su promedio, y distancia al máximo y mínimo de 48 h.

## 4. Decidir

Todo se opera con `--nivel trading`. Reglas por defecto: **stop 5%, trailing 5%, vende la mitad a
+8% y el resto a +15%**. El código pone el tope: ninguna posición pasa el 25% de la carpeta.

Qué buscar (elegí UNA tesis clara por entrada y escribila):
- **Ruptura con volumen:** rompe el máximo de 48 h con `volumen_4h_vs_promedio` ≥ 1,5.
- **Rebote en soporte:** grande y líquida que cae al mínimo de 48 h y deja de caer (la última
  hora ya no hace mínimo nuevo).
- **Momentum de 24 h:** +5% en 24 h, sigue subiendo en 4 h y no está estirada (+1 h no > +4%).

Disciplina:
- 2 a 5 posiciones a la vez. Plata parada en USDT cuando no hay nada claro está bien.
- Máximo 3 entradas por hora. Cada vuelta cuesta 0,2%: una entrada sin tesis es pérdida segura.
- Si una posición lleva 24 h sin llegar a +8% ni al stop, sacala y rotá.
- Si BTC cae más de 3% en 4 h, no abras nada nuevo esa hora.
- Podés ajustar con `reglas --par X --stop N --trail N --tp 8:0.5,15:1 --motivo "..."`.
  Nunca alejes un stop para que no salte: eso es trampa.
- Cada `--motivo`: la tesis, y el precio o señal que la invalida.
- Si el código rechaza una orden, es la regla funcionando: no busques el costado.

## 5. Cerrar

```bash
python3 execution/cartera/cartera.py snapshot
git add -f execution/cartera/estado-agresiva
git commit -m "agresiva: ciclo $(date -u +%Y-%m-%dT%H:%MZ)"
git push origin claude/cartera-agresiva || (git pull --rebase origin claude/cartera-agresiva && git push origin claude/cartera-agresiva)
```

Nunca push a `main` ni a otra rama; nunca toques fuera de `execution/cartera/estado-agresiva/`.

## 6. Última línea, exacta

`CARTERA_OK total=<total_usd> resultado=<resultado_pct>% disparos=<n> ops=<n>`

Si Binance no responde: commit de lo que haya cambiado y `CARTERA_FALLA binance: <error>`.
