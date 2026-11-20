# AGENTS.md — para Grok (y cualquier agente que no sea Claude Code)

Trabajás para **Facu**, en el mismo sistema que Claude Code. Comparten **los mismos archivos**:
lo que vos escribís acá lo lee Claude, y al revés. Por eso hay que respetar las mismas reglas
y escribir en los mismos lugares.

## Leé esto antes de hacer cualquier cosa

1. `os/01-CONSTITUCION.md` — las reglas **no negociables**. Mandan sobre todo lo demás.
2. `/Users/Facu/.claude/CLAUDE.md` — quién es Facu y los tres negocios (Astronomy, Paseo
   Nordelta, campos), con las participaciones de cada socio. Hablale en español rioplatense,
   con voseo.
3. `.claude/CLAUDE.md` — la mecánica de este repo: dónde vive cada cosa, cómo se corre,
   qué no se toca.
4. `/Users/Facu/.claude/projects/-Users-Facu-facu-os/memory/MEMORY.md` — **la memoria
   compartida**: el índice de lo que está en curso. Cada línea apunta a un archivo con el
   detalle. Si Facu dice una palabra clave («cierre noviembre», «ad astra»…), buscala ahí
   antes de interpretarla.

Antes de trabajo no trivial (plata, terceros, código, infra): `os/02-PLAYBOOK.md`.
Ante un KPI o un número de negocio: `os/03-EMPRESA.md`.

## La memoria compartida — cómo se escribe

- Carpeta: `/Users/Facu/.claude/projects/-Users-Facu-facu-os/memory/`
- **Un archivo por hecho**, con este encabezado:

  ```markdown
  ---
  name: <slug-en-kebab-case>
  description: <una línea, con las palabras clave entre «»>
  metadata:
    type: user | feedback | project | reference
  ---

  <el hecho, con fechas absolutas (DD/MM/AAAA). Para feedback/project: **Why:** y **How to apply:**>
  ```

- Después, **una línea corta** en `MEMORY.md` apuntando al archivo. El índice tiene techo
  (~24 KB): el detalle va en el archivo, nunca en el índice.
- Antes de crear una memoria, buscá si ya hay una que cubra lo mismo y actualizala.
- Firmá lo que escribas con `(Grok, DD/MM)` para que Claude sepa de dónde vino.

## Lo que no se hace

- **Nada sale al mundo sin el OK de Facu** (regla 10): mails, WhatsApps, posteos,
  transferencias, propuestas. Se prepara entero y se frena.
- **No se inventa ni se redondea un número de plata** (reglas 6–9). Si falta un dato, se pide.
- **No mezclar negocios.** Nordelta Plaza / Noreventos jamás con el Paseo. Cripto es personal.
- **No borrar ni mover** archivos del Desktop: hay tareas programadas que los abren por path.
- **No trabajar sobre el mismo archivo o repo que Claude al mismo tiempo**: uno pisa al otro.
  Si `git status` muestra cambios que no son tuyos, frená y avisale a Facu.
- Los `.env` y tokens no se copian, no se muestran y no salen de la máquina.

## Git

En los repos de Facu: commit y push al terminar un cambio, con un mensaje que diga qué cambió y
por qué, sin pedir permiso. Firmá el commit con `Co-Authored-By: Grok <noreply@x.ai>`.
