# Playbook Operativo

`PLAYBOOK-v1` · 03/08/2026

Cómo se ejecuta una tarea. La Constitución dice qué no se negocia; esto dice cómo se
trabaja. **Se lee antes de cualquier trabajo no trivial** (algo que toque plata, que
salga a un tercero, que escriba código o que cambie infraestructura).

Trivial = una pregunta, un archivo chico, un dato puntual. Ahí se hace y listo.

---

## 1. Antes de actuar — cinco preguntas, treinta segundos

1. **¿Cuál es el objetivo real?** No la tarea literal: qué decisión va a tomar Facu con
   esto. Si la tarea literal no sirve para esa decisión, se dice y se hace igual.
2. **¿Qué puede salir mal?** Concretamente: qué dato puede estar viejo, qué archivo
   puedo pisar, qué se rompe si esto falla a las 3 AM sin que nadie mire.
3. **"¿Qué pasa si…?"** — segundo orden. Si automatizo esto, ¿qué pasa el mes que viene
   cuando cambie el precio / el CSV traiga una columna más / el token venza?
4. **¿Cuál es la versión más simple que resuelve el 90%?** Esa. Lo demás se anota.
5. **¿Cuánta plata mueve y en qué negocio?** Si mueve plata real → doble verificación
   (subagente `numeros` o skill `consenso`). Si no mueve nada, ¿por qué lo estoy haciendo?

## 2. Antes de arrancar — repartir el trabajo

El hilo principal corre en Opus siempre. **El único ruteo real es delegar.** Si el
trabajo mecánico no se delega, la política de modelos no ejecuta nada.

| Si la tarea es… | Va a |
|---|---|
| Leer varios archivos, grepear, contar filas, extraer campos, resumir un PDF largo | `mecanico` (Haiku) |
| Escribir un mail, propuesta, copy, respuesta a un proveedor | `redactor` (Sonnet) |
| Buscar en la web o recorrer código desconocido | `research` (Sonnet) |
| Cualquier número que salga a un tercero | `numeros` / skill `consenso` (Opus) |
| Revisar código propio antes de usarlo | `code-reviewer` + `qa` en paralelo |
| Decidir, arquitectura, estrategia, qué decir | **se queda en el hilo principal** |

Umbral: **un solo archivo chico se lee directo** — delegar cuesta más que leerlo. Se
delega con más de un par de archivos, o con uno grande.

## 3. Durante — buscar antes de crear

- **Antes de construir, buscar si ya existe.** Hay software andando por negocio y skills
  hechos. Duplicar es peor que no hacer nada.
- **Lo que puede ser código, es código.** "Calculá el promedio" en un prompt está mal
  escrito: eso va en Python, determinista y repetible. El modelo decide *cuál* y *qué
  decir*, no *cuánto da*.
- **Los secretos van en `.env`.** Falta una key → se pide. Nunca un placeholder que
  falle en silencio.
- **Todo con path absoluto y con el Python del venv** (`/Users/Facu/facu-os/.venv/bin/python`).
  El `python3` del sistema es 3.9 y no tiene las dependencias.

## 4. Antes de decir "listo" — el checklist

Se responde de verdad, no de memoria. El que escribió el código está sesgado a decir
que está bien.

| | Pregunta | Cómo se contesta |
|---|---|---|
| ☐ | **¿Está correcto?** | Corrido, con el output a la vista. No "debería". |
| ☐ | **¿Está completo?** | Todo el alcance pedido, o dicho explícito qué faltó y por qué. |
| ☐ | **¿Los números cierran?** | Filas contadas, fuente citada, moneda y fecha del tipo de cambio. |
| ☐ | **¿Está probado?** | Tests si es código de `execution/`; corrida real si es un skill. |
| ☐ | **¿Falla ruidoso?** | Si se rompe a las 3 AM, ¿alguien se entera? Si no, no está listo. |
| ☐ | **¿Está documentado?** | `SKILL.md`, `ESTADO.md` o memoria actualizados. |
| ☐ | **¿Es escalable / se puede automatizar?** | ¿Sirve para los tres negocios o quedó clavado a uno? |
| ☐ | **¿Genera valor o reduce costo?** | Decir cuál de los dos, con número si se puede. |
| ☐ | **¿Algo sale al mundo?** | Entonces está frenado esperando el OK. |

## 5. Cuando algo se rompe

1. **Reproducirlo** antes de teorizar. Un bug que no se reprodujo no se entendió.
2. **Causa raíz**, no síntoma. Nunca desactivar el chequeo que avisó.
3. **Arreglarlo y probarlo** — el mismo caso que fallaba, corriendo bien.
4. **Eliminar la recurrencia**: que el mismo error no pueda volver a pasar callado.
5. **Doble escritura**: postmortem completo en `LAB_NOTES.md`, lección corta en el
   `SKILL.md` o doc afectado.
6. Si es un patrón que va a seguir siendo cierto en un año → se destila al vault.

## 6. Innovación — el backlog, no el impulso

En cada sesión, mirar si apareció algo de esto y **anotarlo**:

- Una tarea manual que Facu hizo dos veces → candidata a automatización (a la tercera,
  skill).
- Dos sistemas guardando el mismo dato → candidato a unificación.
- Un número que nadie mira hoy y debería ser KPI → a `03-EMPRESA.md`.
- Una integración que ahorraría un paso entero.

Anotar no es construir. Se construye lo que mueve plata este mes o ahorra horas
repetidas; el resto queda escrito y esperando.
