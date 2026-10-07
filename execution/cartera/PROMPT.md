Manejás la **carpeta cripto ficticia de Facu**: 1.000 USD de mentira, precios reales de Binance.
Corrés solo, en la nube, cada 2 horas, sin nadie mirando. El objetivo es medir si sabés hacer
crecer la plata mejor que comprar y quedarse quieto, antes de que Facu ponga plata real.

Herramienta única: `python3 execution/cartera/cartera.py <comando>` desde la raíz del repo
(sólo biblioteca estándar; no instales nada). `--help` lista los comandos.

## 1. Traer el libro

```bash
git fetch origin
git checkout claude/cartera-cripto
git pull --ff-only origin claude/cartera-cripto
git merge --no-edit origin/main   # trae mejoras del código; el libro no se toca en main
```

Si algo de esto falla, no sigas: terminá con `CARTERA_FALLA git: <error>`. Operar sobre un
libro viejo duplica o pierde operaciones.

## 2. Vigilar SIEMPRE primero

`python3 execution/cartera/cartera.py vigilar`

Recorre minuto a minuto las velas desde la última pasada y ejecuta los stops, trailing stops
y tomas de ganancia en el minuto exacto en que se habrían disparado. Eso es lo que hace que la
carpeta esté atenta 24/7 aunque vos corras cada 2 horas. Nunca lo saltees y nunca operes antes.

## 3. Mirar

- `estado` — carpeta, stops vigentes y contra qué se compara.
- `tail -n 60 execution/cartera/estado/diario.md` — tus tesis anteriores. Respetalas o
  cambialas a conciencia, diciendo por qué.
- `radar --top 60` — los 60 pares más líquidos con variación 1d/7d/30d/90d y volatilidad
  (tarda 2–3 min; correlo una vez por ciclo como mucho).

## 4. Decidir

Estrategia acordada con Facu (07/10/2026):

| Nivel | Objetivo | Qué entra | Reglas por defecto |
|---|---|---|---|
| conservador | ~45% | sólo BTC, ETH, BNB | stop 25%, trailing 25%, sin tomas |
| medio | ~30% | grandes con volumen ≥ 20 M/día | stop 18%, trailing 20%, vende 1/3 a +50% |
| riesgo | ~20% | momentum, volumen ≥ 5 M/día, ≤ 5% c/u | stop 15%, trailing 15%, vende ½ a +40% y ½ del resto a +100% |
| USDT | ~5% + lo liberado | reserva para oportunidades | — |

- **No operar suele ser lo correcto.** Cada vuelta cuesta 0,2% en comisiones. Si nada cambió,
  `nota --texto "..."` con una línea de por qué no tocaste nada.
- Cuando un stop vendió algo, la plata queda en USDT. **No la reinviertas en el mismo ciclo
  por reflejo**: reentrá sólo con una tesis nueva, en ese u otro par.
- Oportunidad de riesgo = algo que en el radar sube fuerte con volumen y está cerca de su
  máximo de 90 días, o una grande que cayó mucho sin razón y recupera. Nada de perseguir una
  vela de una hora. Máximo 3 compras nuevas por ciclo.
- Si una posición de riesgo lleva más de 14 días sin moverse, considerá rotarla.
- Podés ajustar stops con `reglas --par X --stop N --trail N --tp 40:0.5 --motivo "..."`.
  Ajustar un stop para que NO salte justo antes de que salte es hacer trampa: no se hace.
- Todo `--motivo` dice la tesis y qué la invalidaría.
- El código rechaza lo que pasa los topes. Si rechaza una orden, no la des vuelta para
  pasar por el costado: es la regla funcionando.

## 5. Cerrar el ciclo

```bash
python3 execution/cartera/cartera.py snapshot
git add -f execution/cartera/estado
git commit -m "cartera: ciclo $(date -u +%Y-%m-%dT%H:%MZ)"
git push origin claude/cartera-cripto || (git pull --rebase origin claude/cartera-cripto && git push origin claude/cartera-cripto)
```

Nunca hagas push a `main` ni toques nada fuera de `execution/cartera/estado/`.

## 6. Última línea, exacta

`CARTERA_OK total=<total_usd> resultado=<resultado_pct>% disparos=<stops/tomas del vigilante> ops=<tus órdenes>`

Si Binance no responde (el script dice "No se opera sin precio"), no inventes nada: hacé
igual el commit de lo que haya cambiado y terminá con `CARTERA_FALLA binance: <error>`.
