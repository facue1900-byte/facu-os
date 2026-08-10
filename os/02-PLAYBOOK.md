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

### Una prueba NUNCA escribe sobre datos reales

**09/08/2026, y costó datos de Facu.** Dos verificadores de pantalla creaban, cobraban
y **borraban** sobre la Previa de Maceo Plex —una fecha real, con plata real— porque era
la que estaba a mano cuando se escribieron. Facu estaba en esa misma pantalla cargando
escalones de comisión: el `limpiar()` del script le borró la categoría por debajo, el
escalón siguiente reventó con un error de foreign key y desde su lado parecía un bug.

No fue una carrera desafortunada: **era inevitable.** Un script que borra por
`event_id` y una persona trabajando en ese `event_id` no pueden convivir.

El método, para cualquier verificador que ESCRIBA:

- **Se crea su propio objeto descartable** —una fecha, un alumno, un local— con un
  nombre que se reconozca (`zz-prueba-<lo-que-prueba>`), lo usa y lo borra entero.
- **Nace apagado.** Si algo falla y queda colgado, un evento en `draft` o un alumno
  inactivo no se ve en la web ni le llega a nadie.
- **Ningún id de producción escrito en un script.** Si hay un uuid real hardcodeado en
  `scripts/`, eso ya es el bug esperando.
- Un verificador que sólo LEE puede mirar datos reales: el problema es escribir.

### Lo que se da por protegido: preguntar por su superficie DIRECTA

Del 08/08/2026, auditando Astronomy. La reja estaba bien escrita y la pared de al lado no
llegaba al techo. **La pregunta no es "¿quién llama a esto?" sino "¿qué pasa si le pegan
sin pasar por acá?"**

Supabase publica cosas que el código no menciona. Antes de decir que algo está protegido:

- **Las funciones de la base son endpoints.** PostgREST publica cada función de `public`
  como `/rest/v1/rpc/<nombre>` y Postgres les da `EXECUTE` a PUBLIC por default. Si además
  son `SECURITY DEFINER`, corren **por encima de RLS**. Toda función nueva nace con
  `revoke execute ... from public, anon, authenticated` — a `public` también, o entran por
  herencia.
- **RLS filtra filas, NO columnas.** Una política `USING (auth.uid() = id)` correcta más un
  `GRANT` de UPDATE sobre toda la tabla deja que el usuario se escriba las columnas de
  control. Hay que leer el `GRANT`, no sólo la política.
- **Un permiso que se verifica tiene que poder otorgarse.** Si no está en el catálogo, nadie
  lo tiene, y la salida bajo presión va a ser dar el rol máximo.
- **La falta de configuración tiene que CERRAR, no abrir.** Nada de `if (secret) { validar }`
  ni `|| ""` como último recurso: sin secreto se corta. Sin excepción por entorno.

Y el método que las encontró: **atacar de verdad con `curl`**, con la clave pública y sin
sesión. Las tres estaban en código que ya había leído entero. Leer muestra las puertas;
sólo pegarle muestra las paredes que faltan.

### Contar filas no es contar hechos

Del mismo día. Una tabla de log guarda **un golpe por reintento**, no un hecho por fila.
Leer `webhook_hits` como si cada fila fuera un pago dio "7 pagos fallidos" donde había **un
pago de prueba reintentado 7 veces**, y "13 rechazados" donde había **4** — y salió reportado
antes de verificarlo.

Es la regla 2 de la Constitución al revés: un resultado **grande** también es un error hasta
que se demuestre lo contrario, cuando la unidad de la fila no es la unidad del hecho. Antes
de reportar un número que sale de un log: `count(distinct <la cosa real>)`, no `count(*)`.

### Un dato válido puede pisar a otro dato válido

10/08/2026, la escalera de comisiones. El formulario validaba cada escalón contra sí mismo
—que el «hasta» fuera mayor que el «desde», que el % estuviera entre 0 y 100— y **nunca
contra los que ya estaban**. Entraron «3 a 5 al 12%» y «4 a 99999 al 20%»: los dos rangos
bien formados, y con 4 mesas vendidas la comisión la decidía el orden del `sort`.

Ninguna validación local ve un solape. Cuando un campo nuevo entra en una **colección** que
ya tiene reglas entre sus miembros (rangos, fechas, tramos, cupos, porcentajes que suman
100), el chequeo se hace contra el conjunto: se leen los que ya están antes de guardar.

Y la mejor validación es la que no hace falta: **si el valor correcto se puede calcular, no
se pregunta.** Acá el «desde» pasó a ser el número siguiente al último cargado, mostrado
fijo y no editable. Un campo que no se puede escribir mal no se escribe mal — y el servidor
lo verifica igual, porque un `<input>` se edita con las herramientas del navegador.

Lo que ya está cargado mal **no se borra solo**: si es plata, se marca en la pantalla y lo
decide Facu.

### Si apretar un botón mueve la pantalla, el problema es el canal de vuelta

Mismo día, dos pedidos de Facu sobre el scroll que salta al guardar. El arreglo anterior
—agregarle un `#ancla` al `redirect()`— era el síntoma: el ancla igual reposiciona.

**La causa era usar la URL para comunicar el resultado.** Un `&ok=…` en la query obliga a
redirigir, redirigir navega, y navegar mueve el scroll. Un formulario que se aprieta varias
veces seguidas (una fila por persona, un escalón tras otro) devuelve su resultado en vez de
navegar, y la pantalla se queda donde está. Se navega cuando **cambia qué se está mirando**,
no para avisar que algo se guardó.

Corolario para las pruebas: cambiar ese contrato **cambia el protocolo del formulario**, y
un arnés que conoce un solo protocolo empieza a reportar "no se guardó" con la pantalla
andando bien. Ver el Lab Note del 10/08/2026.

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
