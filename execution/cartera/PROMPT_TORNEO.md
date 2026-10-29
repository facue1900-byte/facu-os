Manejás el **torneo cripto de Facu**: ~33 estrategias ficticias, todas con 1.000 USD desde el
29/10/2026, mismas velas de Binance y mismo costo. Las estrategias están escritas en código
(`execution/cartera/torneo.py`) y son deterministas: **vos no operás ni elegís nada**. Tu
trabajo es (1) leer las noticias una vez por día y anotar el sesgo, y (2) recalcular la tabla.
Plata ficticia: no hay keys, no mandás nada a nadie.

## 1. Traer la rama

```bash
git fetch origin
git checkout claude/cartera-torneo 2>/dev/null || git checkout -b claude/cartera-torneo
git pull --ff-only origin claude/cartera-torneo 2>/dev/null || true
git merge --no-edit origin/main
export TORNEO_DIR=execution/cartera/estado-torneo
mkdir -p $TORNEO_DIR
```

Si algo de git falla, no sigas: `TORNEO_FALLA git: <error>`.

## 2. Noticias — UNA vez por día (si ya hay una línea con la fecha UTC de hoy en `noticias.jsonl`, saltá al paso 3)

Buscá con WebSearch lo que mueve cripto **hoy**: Fed y tasas, datos de EE.UU. (inflación, empleo),
flujos de los ETF de BTC y ETH, regulación (SEC, EE.UU., Europa), hackeos o quiebras de exchanges,
liquidaciones grandes, noticias de BTC/ETH/SOL. Mínimo 3 búsquedas, fuentes con fecha de las
últimas 48 h. No inventes: si no encontrás nada con fecha, el sesgo es `neutral`.

Elegí UNO:
- `riesgo_fuera` — hay un golpe concreto y fechado que todavía no terminó (hackeo/quiebra grande,
  suba de tasas sorpresa, salida fuerte y sostenida de los ETF, prohibición). Es lo único que hace
  que las estrategias "+ freno de noticias" vendan todo: usalo sólo con un hecho, no con un clima.
- `riesgo_dentro` — un viento a favor concreto y fechado (baja de tasas, entradas fuertes a los ETF,
  aprobación regulatoria).
- `neutral` — todo lo demás. Es lo normal.

Agregá UNA línea (append, nunca reescribas las anteriores) a `$TORNEO_DIR/noticias.jsonl`:

```bash
python3 - <<'EOF'
import json, datetime, os
d = {"fecha": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"),
     "sesgo": "neutral",            # riesgo_dentro | neutral | riesgo_fuera
     "motivo": "<una o dos frases con el hecho concreto>",
     "fuentes": ["<url con fecha>", "<url>"]}
open(os.environ["TORNEO_DIR"] + "/noticias.jsonl", "a").write(json.dumps(d, ensure_ascii=False) + "\n")
EOF
```

## 3. Recalcular

```bash
python3 execution/cartera/torneo.py bajar --desde 2026-01-01
python3 execution/cartera/torneo.py vivo --desde 2026-10-29
```

Esto reescribe `$TORNEO_DIR/RESUMEN.md` y `vivo.json`. No los edites a mano. Si Binance no responde
(403, timeout), no inventes la tabla: `TORNEO_FALLA binance: <error>` (con commit de las noticias si las
escribiste).

## 4. Cerrar

```bash
git add -f $TORNEO_DIR/RESUMEN.md $TORNEO_DIR/vivo.json $TORNEO_DIR/noticias.jsonl
git commit -m "torneo: ciclo $(date -u +%Y-%m-%dT%H:%MZ)"
git push origin claude/cartera-torneo || (git pull --rebase origin claude/cartera-torneo && git push origin claude/cartera-torneo)
```

Nunca push a `main` ni a otra rama; nunca toques nada fuera de `execution/cartera/estado-torneo/`
(la caché `torneo-cache/` no se commitea) y nunca edites `torneo.py` ni `HISTORIA.md`.

## 5. Última línea, exacta

La que imprime `vivo` (`TORNEO_OK hasta=... lider="..." ...`) seguida de ` sesgo=<el de hoy>`.
