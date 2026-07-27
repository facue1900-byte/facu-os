---
name: consenso
description: Manda varios auditores independientes a verificar el mismo cálculo, reporte o análisis sin que se vean entre sí, y compara lo que encontró cada uno. Usar antes de que un número salga hacia un tercero, antes de una decisión que cuesta plata o es difícil de revertir, o cuando Facu pida "verificá esto bien", "estás seguro?", "que lo revise otro".
allowed-tools: Bash, Read, Write, Task
---

# Consenso

Un solo verificador tiene un problema: si se equivoca, nadie lo agarra. Este skill
manda **N auditores que no se ven entre sí** al mismo trabajo y después compara.

Lo que varios encuentran por separado es sólido. Lo que vio uno solo puede ser
que haya sido más fino o que se haya equivocado — y eso se marca como tal en vez
de mezclarlo con el resto.

Sirve para cualquier cosa verificable contra una fuente: una conciliación, un
reparto de ganancias, una proyección, un análisis, una conclusión de un informe.
El caso duro es plata, pero no es el único.

## Cuándo vale la pena

Cuesta N veces más que una verificación sola. Se justifica cuando:

- El número **sale hacia un tercero** (un socio, un frigorífico, un inversionista).
- La decisión es **cara de revertir**.
- Ya hubo un error antes en ese mismo cálculo.

Para un chequeo de rutina, alcanza con un solo agente `numeros`. No uses esto
para todo: si se vuelve el default, deja de significar algo.

## Flujo

Todo va a `.tmp/consenso/` (crearlo si no existe: es descartable y no está en git).

### 1. Preparar qué se audita

Necesitás tener a mano, con paths absolutos:
- **Qué** se audita: el reporte, el cálculo o el archivo con la conclusión.
- **Contra qué**: las fuentes (xlsx, PDF del extracto, CSV, el script que lo generó).

Si no tenés las fuentes, paralo acá. Tres auditores sin fuente producen tres
opiniones, no un consenso.

### 2. Lanzar los auditores en paralelo

**Tres es el default.** Lanzalos **en un solo mensaje**, si no corren en serie.

```
subagent_type: "auditor-consenso"
prompt: "Audite <qué>. Las fuentes son <paths>. Escribí tu JSON en
/Users/Facu/facu-os/.tmp/consenso/auditor_N.json"
```

Con N = 1, 2, 3. Cada uno escribe **su propio archivo**.

**No les cuentes qué encontraron los otros, ni les pases un resumen previo.** El
valor entero de esto es que lleguen a la misma conclusión sin haberse visto. Un
auditor contaminado es peor que no tenerlo: agrega una confirmación falsa.

Esperá a que existan los tres archivos:

```bash
mkdir -p /Users/Facu/facu-os/.tmp/consenso && \
cd /Users/Facu/facu-os/.tmp/consenso && \
for i in 1 2 3; do while [ ! -f "auditor_$i.json" ]; do sleep 2; done; done && \
echo "listos"
```

### 3. Comparar

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/consenso/scripts/comparar_auditorias.py" \
  --input-dir /Users/Facu/facu-os/.tmp/consenso \
  --output /Users/Facu/facu-os/.tmp/consenso/consenso.md
```

Sale con código 0 **solo** si el veredicto es CIERRA y fue unánime. Cualquier
otra cosa da 1: eso es algo para mirar, no un fallo del script.

### 4. Contarle a Facu

En este orden:

1. **El veredicto y si fue unánime.** Si no fue unánime, decilo primero — es la
   señal más informativa del reporte.
2. **Los confirmados por varios**, con el monto exacto.
3. **Los que vio uno solo**, marcados como tales. No los presentes como
   equivalentes a los confirmados.
4. **Lo que quedó sin verificar.** Esta sección no se saltea aunque el veredicto
   diga CIERRA.

## Cómo se cruzan los hallazgos

Por `valor_diferencia` **exacto**. Es el único campo que se puede comparar entre
auditores sin adivinar: dos que reportan la misma diferencia al centavo están
viendo lo mismo, aunque lo describan distinto.

Los hallazgos sin valor numérico **no se cruzan** — se listan como vistos por uno
solo. Es a propósito: fingir un cruce semántico entre textos distintos daría
falsos "confirmado por 2" que es justo lo que este skill existe para evitar.

Por eso el agente tiene instrucción explícita de no redondear ese campo. Un
auditor que escribe `152340` donde otro escribe `152340.50` figura como que
nadie más lo vio.

## El veredicto es el más conservador

Si un auditor de tres dice NO CIERRA, el consenso es NO CIERRA. No hay votación
por mayoría: en algo que toca plata, la duda de uno alcanza para frenar y mirar.

## Lecciones

- **Un consenso de uno no es un consenso.** El script se niega a correr con menos
  de dos auditorías (`--minimo`, default 2).
- **Que ninguno declare huecos es sospechoso**, no tranquilizador. El reporte lo
  marca explícitamente cuando la sección "sin verificar" sale vacía.
- **Los auditores no se ven entre sí y eso no es una limitación, es el punto.**
  Cualquier atajo que les pase contexto de los otros invalida el ejercicio
  entero.
