# Playbook Operativo

`PLAYBOOK-v2` · 08/08/2026

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
| ☐ | **¿El chequeo nuevo falla cuando tiene que fallar?** | Se rompe el código a propósito y se mira si lo agarra. Ver abajo. |
| ☐ | **¿Falla ruidoso?** | Si se rompe a las 3 AM, ¿alguien se entera? Si no, no está listo. |
| ☐ | **¿Está documentado?** | `SKILL.md`, `ESTADO.md` o memoria actualizados. |
| ☐ | **¿Es escalable / se puede automatizar?** | ¿Sirve para los tres negocios o quedó clavado a uno? |
| ☐ | **¿Genera valor o reduce costo?** | Decir cuál de los dos, con número si se puede. |
| ☐ | **¿Algo sale al mundo?** | Entonces está frenado esperando el OK. |

### Un chequeo nuevo se rompe a propósito antes de confiar en él

La Constitución dice que un chequeo que nunca falló es sospechoso (regla 3). El método
para saberlo el mismo día que se escribe: **romper el código a propósito, una cosa por
vez, y mirar si el chequeo lo agarra.** Se restaura y listo. Cuesta dos minutos.

Y el caso que engaña, del 08/08/2026: un chequeo de *"esto tiene que pasar derecho"*
—que algo NO se toque, NO se guarde, NO se intercepte— **puede dar verde porque ninguna
regla lo agarró, no porque la protección funcione.** Se saca la protección y el chequeo
sigue en verde. La única forma de que valga es apuntarle al camino que se lo comería:
la petición con la forma exacta que caería en la rama peligrosa.

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

## 7. Análisis 360° — una función nueva nunca vive sola

`v1 · 03/08/2026`. Regla de Facu, textual: **"nunca implementes únicamente lo
solicitado"**. Cada vez que se crea, cambia o borra una funcionalidad, se revisa el
ecosistema entero ANTES de darla por terminada. Nunca asumir que el cambio afecta sólo
al lugar donde se pidió.

El disparador es siempre el mismo: **buscar cómo se llama lo que ya existe y aparecer en
todos los lugares donde aparece**. En la práctica, un `grep` del hermano mayor de la
función nueva (¿dónde se enumera `cursodj`?) da el mapa completo en un minuto.

| # | Frente | Qué se pregunta |
|---|---|---|
| 1 | **Interfaces** | Alumno, admin, back office, profe, moderador, soporte. ¿Cada rol ve lo que le corresponde? |
| 2 | **Navegación** | Menús, breadcrumbs, links, accesos rápidos, botones. ¿Se puede *llegar* sin que te pasen el link? |
| 3 | **Formularios** | Campos, validaciones, errores, mensajes de éxito, placeholders, defaults. |
| 4 | **Panel admin** | Crear, editar, borrar, activar, desactivar, ordenar, archivar, buscar, filtrar, exportar. **Nunca mostrar un dato que el admin no pueda gestionar.** |
| 5 | **Filtros** | Filtros, orden, búsqueda, categorías, etiquetas, estados, fechas. Pensado para miles de registros. |
| 6 | **Estados** | Activo, inactivo, borrador, publicado, archivado, eliminado — y qué acción tiene cada uno. |
| 7 | **Permisos** | Quién ve, edita, borra, administra. **Nunca de más.** |
| 8 | **Base de datos** | Tablas, relaciones, índices, restricciones, integridad, migración. **Una sola fuente de verdad por dato.** |
| 9 | **Automatizaciones** | Qué paso manual se puede evitar. Mails, notificaciones, registros, logs, procesos encadenados. |
| 10 | **Integraciones** | Pagos, mail, WhatsApp, APIs, calendario, analítica, almacenamiento. |
| 11 | **UX** | Clics, claridad, accesibilidad, consistencia, feedback. Nadie debería preguntarse qué hacer. |
| 12 | **UI** | Tamaños, márgenes, alineación, color, tipografía, iconos, responsive, oscuro. Respeta el sistema de diseño. |
| 13 | **Scroll** | Vertical, horizontal, paginado, sticky, comportamiento en móvil. |
| 14 | **Responsive** | Desktop, notebook, tablet, celular. Nunca sólo desktop. |
| 15 | **Rendimiento** | Consultas de más, caché, escala con miles de usuarios. |
| 16 | **Seguridad** | Validación, permisos, sanitización, autenticación, exposición de datos. |
| 17 | **Casos límite** | Sin datos, con un millón, sin internet, usuario que abandona, alguien que quiere romperlo. |
| 18 | **Calidad** | Completo, intuitivo, consistente, mantenible, escalable, documentado. |

**Regla de oro:** implementar además todo lo necesario para que quede integrado con el
resto de la plataforma —coherente visual, funcional y técnicamente— y pueda crecer sin
deuda. Lo que falte y no se haga, se dice explícitamente y queda anotado.
