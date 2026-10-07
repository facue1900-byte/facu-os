---
name: triage-inbox
description: Ordena el inbox de Gmail clasificando cada mail en Plata / Acción / Esperando / Referencia y asignándole un ámbito configurable. Usar cuando Facu pida "ordename el mail", "qué tengo pendiente", "triage del inbox", "qué me están pidiendo", "revisá los mails", o pregunte si se le pasó algo por mail.
allowed-tools: Bash, Read, Write, Task
---

# Triage de inbox

Baja los mails, los clasifica con subagentes en paralelo, y devuelve **un reporte
para leer** antes de tocar nada. Aplicar las etiquetas en Gmail es un paso
aparte y opcional.

Lo que sale es la lista de qué hay que hacer, agrupada por plata primero y por
ámbito. El objetivo no es tener el inbox lindo: es que no se pierda un
vencimiento.

## Los ámbitos se configuran, no se hardcodean

Viven en **`contextos.json`**, al lado de este archivo. Ahí se declara cada
ámbito con las señales para reconocerlo, y opcionalmente un `no_confundir` para
los que se parecen entre sí.

Hoy están los cuatro negocios de Facu, pero el skill no sabe nada de ellos: si
cambiás ese JSON, cambia el triage. `Personal` y `—` valen siempre y no hace
falta declararlos.

El merge **valida** que cada ámbito devuelto esté declarado ahí. Un ámbito
inventado corta la corrida: un mail archivado en un grupo que no existe se
pierde igual que uno sin clasificar.

## Antes de correrlo

- El OAuth de Google tiene que estar hecho: `.venv/bin/python execution/google_auth.py --setup --cuenta facu`
- Los scripts van con path absoluto y con el Python del venv.
- Para el paso 5 (aplicar etiquetas) hacen falta scopes que hoy **no** están.
  Ver "Aplicar etiquetas" abajo.

## Flujo

Todo va a `.tmp/triage/`, que es descartable.

### 1. Bajar

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/triage-inbox/scripts/fetch_emails.py" \
  --query "in:inbox is:unread" --limit 200 \
  --output /Users/Facu/facu-os/.tmp/triage/emails.json
```

Queries útiles: `in:inbox is:unread` (lo de siempre), `in:inbox newer_than:7d`
(la semana), `in:inbox` (todo, para la primera pasada).

### 2. Partir

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/triage-inbox/scripts/split_chunks.py" \
  --input /Users/Facu/facu-os/.tmp/triage/emails.json \
  --chunks 8 --output-dir /Users/Facu/facu-os/.tmp/triage/chunks
```

Imprime `CHUNKS=N` al final: ese N es cuántos subagentes lanzar. Con menos de 40
mails usá `--chunks 4`; partir de más no acelera nada.

### 3. Clasificar en paralelo

Lanzá **N subagentes `clasificador-mails` en un solo mensaje** (si van en
mensajes separados corren en serie y se pierde todo el beneficio). A cada uno:

```
subagent_type: "clasificador-mails"
prompt: "Leé /Users/Facu/facu-os/.tmp/triage/chunks/chunk_N.json, clasificá cada
mail, y escribí el resultado en
/Users/Facu/facu-os/.tmp/triage/chunks/clasificado_N.json"
```

**No leas la salida de los subagentes.** Escriben archivos; con 200 mails, leer
sus respuestas te llena el contexto al pedo. Esperá a que existan los archivos:

```bash
cd /Users/Facu/facu-os/.tmp/triage/chunks && \
for i in $(seq 0 $((N-1))); do
  while [ ! -f "clasificado_$i.json" ]; do sleep 2; done
done && echo "listos los $N"
```

### 4. Juntar y leer

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/triage-inbox/scripts/merge_labels.py" \
  --emails /Users/Facu/facu-os/.tmp/triage/emails.json \
  --input-dir /Users/Facu/facu-os/.tmp/triage/chunks \
  --output /Users/Facu/facu-os/.tmp/triage/labels.json \
  --report /Users/Facu/facu-os/.tmp/triage/reporte.md
```

Si un mail quedó sin clasificar, **el script corta acá**. No lo esquives: volvé
al paso 3 con los chunks que faltaron. Un triage que se come mails en silencio
es peor que no tener triage.

Leé `reporte.md` y contale a Facu lo de **Plata** y **Acción** primero, con el
ámbito de cada uno. `Esperando` y `Referencia` van en una línea de resumen.

### 5. Aplicar etiquetas en Gmail (opcional, y no por default)

Esto le toca el inbox de verdad, así que lleva `--send` apagado por default.
Primero mostrale el plan:

```bash
/Users/Facu/facu-os/.venv/bin/python \
  "/Users/Facu/facu-os/.claude/skills/triage-inbox/scripts/apply_labels.py" \
  --input /Users/Facu/facu-os/.tmp/triage/labels.json
```

Y recién con su OK explícito, lo mismo con `--send`. Las etiquetas se crean bajo
`Triage/` (`Triage/Plata`, `Triage/Acción`, …) para que se puedan borrar todas
juntas si no sirve.

**Hoy este paso falla**, y está bien que falle: `execution/google_auth.py` pide
`gmail.readonly` y `gmail.send`, no `gmail.modify` ni `gmail.labels`. Es una
decisión de seguridad escrita en ese archivo — si un script se vuelve loco, que
no pueda borrar nada. Para habilitarlo hay que agregar los dos scopes, borrar
`token-facu.json` y rehacer el login con `--setup --cuenta facu`. **Eso lo decide
Facu, no vos.**

Los pasos 1 a 4 andan sin tocar nada de eso: bajar y clasificar es solo lectura.

## Las etiquetas

| Etiqueta | Qué es |
|---|---|
| **Plata** | Toca dinero: vencimientos, facturas, impuestos, extractos, transferencias, liquidaciones. |
| **Acción** | Te piden algo y no es plata: trámites, firmas, respuestas, permisos. |
| **Esperando** | Mandaste algo y esperás a un tercero. |
| **Referencia** | Newsletters, notificaciones, informativo. |

Son excluyentes y en ese orden de precedencia. Estas cuatro sí son fijas: valen
para cualquier inbox. Lo que cambia por contexto son los **ámbitos**, y esos van
en `contextos.json`.

Las reglas finas de clasificación viven en `.claude/agents/clasificador-mails.md`
— si el triage etiqueta mal algo, se arregla ahí, no acá.

## Lecciones

- **Contar antes de confiar.** El merge compara los IDs clasificados contra el
  `emails.json` original y corta si falta uno. La versión de la que salió esto
  no chequeaba nada: un subagente que moría dejaba mails sin etiquetar y el
  resumen igual decía "listo".
- **Ante la duda, `—`.** Dos ámbitos que se parecen son la trampa clásica (Paseo
  Nordelta vs Nordelta Plaza: comparten el nombre y son negocios distintos). Por
  eso `contextos.json` tiene el campo `no_confundir`, y por eso la instrucción es
  marcar `—` en vez de adivinar. Un `—` se revisa a mano; un ámbito equivocado se
  pierde.
