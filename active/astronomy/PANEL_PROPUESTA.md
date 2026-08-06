# Panel de Astronomy OS — propuesta antes de implementar

`06/08/2026` · Los 8 cambios pedidos, contrastados contra el código actual.
Pantalla: `/admin/herramientas`. **Todavía sin implementar.**

---

## Lo primero: tres de los ocho ya existen o chocan con algo que existe

No los cambio por mi cuenta. Los pongo arriba porque cambian el alcance.

### Cambio 6 (⌘K) — **ya está construido**

`components/AccionesRapidas.tsx`, montado en el header (`components/Nav.tsx`, el "+").

| Lo que pediste | Estado |
|---|---|
| ⌘K en Mac / Ctrl+K en Windows | Hecho — y además `/` |
| Filtrar mientras se escribe | Hecho |
| Abrir directamente una sección | Hecho (Enter va al primer resultado) |
| Buscar herramientas | **Falta.** Hoy busca **alumnos** y 6 acciones sueltas, no las ~20 herramientas |

**No hay que construir un buscador: hay que darle el catálogo.** Y ahí está la decisión
técnica que sostiene todo lo demás — ver "Un solo catálogo" abajo.

### Cambio 3 ("HOY") — el nombre choca con `/admin`

`/admin` **ya es** la pantalla que contesta *"¿qué tengo que hacer hoy?"*: cola por
persona, una sola tarea activa, el resto en espera. Si Herramientas abre con una sección
titulada **HOY**, hay dos pantallas contestando la misma pregunta y ninguna es la buena.

Pero lo que pedís **sí sirve**, y es otra cosa: de estas veinte puertas, cuatro son las que
abrís siempre. Eso son **atajos**, no trabajo.

> **Recomiendo:** hacerlo, con el título **"LO QUE MÁS ABRÍS"** y no "HOY". Mismo
> contenido, misma personalización por rol, sin competirle a `/admin`.

### Cambio 5 ("BANDEJA / PENDIENTES") — ya hay dos bandejas

Los pendientes de verdad ya viven en dos lugares: **`/admin`** (la cola) y
**`/admin/problemas`** (Centro de Operaciones, 18 detectores). Una tercera bandeja sería
la tercera respuesta a la misma pregunta.

Y lo que hoy está abajo en Herramientas **no son pendientes**: Avisos (3), Postulaciones
(3), Bajas (30 registros históricos) y Equipo con acceso (6) son **listados y registros**.
Ponerles el título "BANDEJA" promete una bandeja de entrada y entrega un archivo. El único
que sí requiere acción es "Pagos que no arrancaron".

> **Recomiendo:** la división que pedís, con dos nombres honestos —**HERRAMIENTAS** arriba
> y **REGISTROS** abajo—, y que "Pagos que no arrancaron" suba con el resto o linkee a
> `/admin/problemas`. La bandeja no se duplica.

---

## La decisión técnica que ordena todo: un solo catálogo

Hoy la lista de herramientas está escrita **dos veces**: en
`app/admin/herramientas/page.tsx` y, parcialmente, en `components/AccionesRapidas.tsx`
(6 acciones a mano). Si agrego el buscador de herramientas sin tocar eso, quedan **tres**
listas y la primera que alguien edite deja mintiendo a las otras dos.

**Propongo `lib/herramientas.ts`: una sola declaración, tres consumidores.**

```ts
export type Herramienta = {
  href: string;
  label: string;          // el nombre, ya con la regla verbo/sustantivo aplicada
  grupo: GrupoId;         // alumnos | estudio | plata | correcciones | demos | ...
  unidad: UnidadId;       // academy | label | domine | empresa
  permiso: string | null; // EXACTAMENTE el que ya tiene hoy
  soloMaestro?: boolean;
  badge?: BadgeId;        // qué contador le corresponde, si tiene
  atajo?: Dueno[];        // para quién es un atajo de "lo que más abrís"
};
```

De ahí salen: la pantalla, el buscador y los contadores. **Es lo único que evita que los
ocho cambios se conviertan en tres listas desincronizadas.**

---

## 1 · PROPUESTA VISUAL

```
  Herramientas
  Las pantallas que se abren cuando hacen falta.  24 alumnos · 54 cuentas

  LO QUE MÁS ABRÍS                                    ← Cambio 3, renombrado
  [ Cobros del mes 3 ] [ Alumnos ] [ Calendario ] [ Cargar un pago ]

┌──────────────┬────────────────────────────────────────────────────────┐
│ EN ESTA      │  HERRAMIENTAS                          ← Cambio 5      │
│ PANTALLA     │                                                        │
│              │  ▾ ASTRONOMY                              (3)          │
│ ● Astronomy  │    ├ Academy · alumnos, cobros y estudio   (3)          │
│   Dominé     │    │   ALUMNOS │ ESTUDIO │ PLATA │ CORRECCIONES        │
│   Empresa    │    │   …       │ …       │ …     │ …     ← Cambio 4    │
│ ──────────   │    └ Label · demos y catálogo                          │
│   Registros  │                                                        │
│              │  ▸ DOMINÉ · eventos                                    │
│              │                                                        │
│              │  ▸ EMPRESA · auditoría y números                       │
│              │                                                        │
│              │  REGISTROS                             ← Cambio 5      │
│              │  ▸ Avisos (3)  ▸ Postulaciones (3)  ▸ Bajas (30)       │
└──────────────┴────────────────────────────────────────────────────────┘
```

**Cambio 1 — la marca vive en el encabezado.** `ASTRONOMY` como grupo, y adentro
**Academy** y **Label** a secas. Se va la repetición.

**Cambio 2 — acordeones.** Encabezado con nombre, una línea de qué hay adentro, y el
contador. Detalle que hay que decidir y no está en el pedido: **"abrir sólo los que tienen
pendientes" y "recordar cómo lo dejó cada uno" se contradicen el día 2.** Regla que
propongo: *la preferencia guardada manda; si esa persona nunca tocó nada, se abre lo que
tiene pendientes.* Se guarda en `localStorage`, no en la base — sin tabla nueva, sin
migración.

**Los contadores, sin contar dos veces.** Hoy los badges salen de cinco números que ya se
calculan en la página. Se reparten así, y ninguno aparece en dos grupos:

| Grupo | Cuenta |
|---|---|
| Academy | cobros vencidos + pagos de MP sin dueño + nombres del Libro sin dueño |
| Label | demos sin abrir + lanzamientos sin publicar |
| Empresa | ventas sin closer |

> El badge de `/admin/problemas` hoy suma `sinAtribuir + pagosPendientes + ventasSinCloser`
> — o sea que **si lo dejo tal cual, Academy y Empresa cuentan lo mismo dos veces**. Por eso
> Empresa se queda sólo con lo que no está en ningún otro grupo.

**Cambio 4 — Correcciones.** Cuarta columna de Academy, separando lo excepcional:
`Cargar un pago` · `Agendar una clase` · `Créditos dados a mano` · `Pagos de MP sin dueño` ·
`Nombres del Libro sin dueño` · `Auditoría de créditos`.

Deja Academy en cuatro columnas parejas: Alumnos (3) · Estudio (5) · Plata (2) ·
Correcciones (6).

> Una salvedad sobre **"Cargar un pago"**: lo pusiste en Correcciones, pero es la acción
> número uno del ⌘K y se usa para cobrar efectivo y transferencias, que es operación
> normal, no una excepción. Lo dejo donde pediste y lo mantengo en los atajos, así está a
> un tecla igual. Si preferís que vuelva a Plata, es una línea.

**Cambio 7 — nombres.** Sustantivo para pantallas, verbo para acciones:

| Hoy | Queda |
|---|---|
| Base de alumnos | **Alumnos** |
| Leads calientes | **Leads** |
| Calendario general | **Calendario** |
| Agendar a mano | **Agendar una clase** |
| Cargar un pago a mano | **Cargar un pago** |
| Libro (entró y salió) | **Libro** |
| Accesos compartidos (DJ Delivery) | **Accesos compartidos** |
| Eventos y entradas | **Eventos** |
| Problemas (y cómo resolverlos) | **Problemas** |

**Cambio 8 — el índice.** Ya es sticky. Le falta saber dónde estás: un
`IntersectionObserver` marca la sección visible, y al abrir un acordeón el índice lo
refleja. Se apaga con «Reducir movimiento» — el scroll suave del salto, no el resaltado.

---

## 2 · COMPONENTES AFECTADOS

| Archivo | Qué pasa | Riesgo |
|---|---|---|
| **`lib/herramientas.ts`** | **Nuevo.** El catálogo único | Ninguno: sólo datos |
| `app/admin/herramientas/page.tsx` | Deja de declarar la lista; la lee del catálogo y arma unidades y contadores | Bajo. Es la pantalla que ya rehicimos hoy |
| **`components/admin/GrupoAcordeon.tsx`** | **Nuevo (cliente).** Acordeón + `localStorage` | Bajo |
| **`components/admin/IndiceLateral.tsx`** | **Nuevo (cliente).** Scroll-spy del índice | Bajo |
| `components/AccionesRapidas.tsx` | Sus 6 acciones a mano salen del catálogo, y se le suman las herramientas | **Medio: es el ⌘K que se usa todos los días.** Va con verificación aparte |
| `app/ui.css` | Estilos de acordeón y atajos, aditivos | Bajo |
| `components/Nav.tsx` | Sin cambios | — |

**No se toca:** ninguna ruta, ningún permiso, ninguna consulta a la base, ninguna server
action, ni `lib/workflows.ts`, ni `/admin`, ni `/admin/problemas`.

---

## 3 · CAMBIOS NECESARIOS

1. `lib/herramientas.ts` con las ~20 herramientas, cada una con **el mismo permiso que
   tiene hoy** (se copian del archivo actual, uno por uno, sin criterio).
2. Reescribir el armado de la página leyendo el catálogo.
3. El acordeón cliente, con la regla de apertura y `localStorage`.
4. El scroll-spy del índice.
5. Sumarle el catálogo al ⌘K.
6. Aplicar los renombres de la tabla de arriba.

**Migraciones: ninguna. Tablas nuevas: ninguna. Permisos tocados: ninguno.**

### Cómo se verifica antes de decir que está

- **La reja no se movió:** un script que compara, herramienta por herramienta, el permiso
  del catálogo nuevo contra el que tenía la página vieja. Si difiere uno solo, falla.
- **Nadie ve de más:** abrir la pantalla con la vista previa de cada perfil y contar
  cuántas herramientas ve, contra las que veía antes.
- **Los contadores no se cuentan dos veces:** que la suma de los badges de los grupos sea
  igual a la suma de los cinco números de origen.
- **La vista:** captura en escritorio y en teléfono, y medir que no haya scroll horizontal
  ni columnas desalineadas, como hicimos hoy.

---

## Lo que necesito que decidas

1. **"LO QUE MÁS ABRÍS" en vez de "HOY"** — para no competirle a `/admin`. ¿Va?
2. **"REGISTROS" en vez de "BANDEJA"** — porque abajo hay listados, no pendientes, y la
   bandeja real ya existe dos veces. ¿Va?
3. **"Cargar un pago"**: ¿queda en Correcciones como pediste, o vuelve a Plata?

Con eso arranco. Los otros cinco cambios los tengo cerrados y no necesitan nada tuyo.
