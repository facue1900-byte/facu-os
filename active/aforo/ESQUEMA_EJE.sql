-- ============================================================================
-- AFORO — EL EJE: QUIÉN ES DUEÑO DE QUÉ
-- ============================================================================
-- Base nueva, proyecto nuevo. NO se aplica sobre la de la academia: un comprador
-- de entradas y un alumno no tienen nada que ver, y mezclarlos es cómo el panel
-- del comprador termina siendo el del alumno (ya pasó).
--
-- Esto es SÓLO el eje. No están todavía las tandas, las órdenes ni los QR: esas
-- se portan de `astronomy-members`, donde ya funcionan y están probadas. Lo que
-- no existe en ningún lado —y por eso se escribe primero— es **el dueño**: hoy
-- todo el sistema asume una sola productora.
--
-- ── LO QUE NO PUEDE FALLAR ACÁ ──────────────────────────────────────────────
-- Una productora NO puede ver un solo dato de otra. Ni un comprador, ni un
-- teléfono, ni cuánto vendió. Ese aislamiento es el producto: el día que Puzzle
-- vea la base de otra productora, no hay forma de arreglarlo hacia atrás.
--
-- Y se verifica **pegándole con `curl` y contando filas**, no leyendo este
-- archivo. Tres veces cayó lo mismo en la academia: RLS prendida no alcanza
-- (PostgREST publica cada función de `public`, RLS no filtra columnas, y una
-- VISTA ignora la RLS de su tabla). Ver `superficie-directa-supabase`.

-- ════════════════════════════════════════════════════════════════════════════
-- 1. PRODUCTORAS
-- ════════════════════════════════════════════════════════════════════════════
create table if not exists public.productoras (
  id uuid primary key default gen_random_uuid(),
  -- El slug es la URL pública: aforo.ar/puzzle. Inmutable en la práctica: si se
  -- cambia, todos los links repartidos por WhatsApp quedan muertos.
  slug text not null unique check (slug ~ '^[a-z0-9][a-z0-9-]{1,38}$'),
  nombre text not null,
  logo_url text,
  contacto_email text,
  contacto_tel text,
  instagram text,

  -- ── LA COMISIÓN, POR PRODUCTORA Y NO GLOBAL ───────────────────────────────
  -- Facu, 10/08/2026: 5% en Aforo y 0% en Astronomy. Una productora grande podría
  -- negociar 3%, así que vive acá y no en una constante.
  --
  -- ⚠️ ES EL PORCENTAJE QUE SE LE COBRA AL QUE COMPRA, sobre el precio de la
  -- entrada. La plata de la entrada va DIRECTO a la cuenta de la productora
  -- (OAuth de Marketplace de Mercado Pago) y Aforo retiene esto como
  -- `application_fee`. Arranca en 0 y se prende cuando haya volumen.
  fee_pct numeric(5,2) not null default 5 check (fee_pct >= 0 and fee_pct <= 100),

  -- ── MERCADO PAGO DE LA PRODUCTORA ─────────────────────────────────────────
  -- Se conecta por OAuth, NUNCA pegando un access token a mano. Con OAuth, el día
  -- que se quiera cobrar el fee se cambia un número; con tokens pelados hay que
  -- reconectar a todas las productoras una por una, y con cientos eso no se hace
  -- nunca. Es la decisión que hoy sale gratis y mañana es imposible.
  mp_user_id text,
  mp_access_token text,
  mp_refresh_token text,
  mp_expira_en timestamptz,
  -- Sin esto no se puede vender: es lo que el paso 3 del alta tiene que lograr.
  mp_conectado_en timestamptz,

  activa boolean not null default true,
  creada_en timestamptz not null default now()
);

-- ── QUIÉN ADMINISTRA CADA PRODUCTORA ────────────────────────────────────────
-- Una productora son varias personas (el dueño, el que carga las fechas, el que
-- mira la plata). Y una persona puede estar en dos productoras: el mismo pibe
-- produce con Puzzle y con otra. Por eso es una tabla y no una columna.
create table if not exists public.productora_miembros (
  productora_id uuid not null references public.productoras(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  -- `dueño` toca la plata y el MP. `staff` carga fechas y ve las bases. El de
  -- puerta NO entra por acá: valida con el ID y la clave de la fecha, sin cuenta.
  rol text not null default 'staff' check (rol in ('dueño', 'staff')),
  creado_en timestamptz not null default now(),
  primary key (productora_id, user_id)
);
create index if not exists prod_miembros_user_idx on public.productora_miembros (user_id);

-- ════════════════════════════════════════════════════════════════════════════
-- 2. FECHAS
-- ════════════════════════════════════════════════════════════════════════════
create table if not exists public.eventos (
  id uuid primary key default gen_random_uuid(),
  productora_id uuid not null references public.productoras(id) on delete restrict,
  -- `restrict` y no `cascade`: borrar una productora con fechas vendidas se
  -- llevaría órdenes pagas y QR que están en el celular de alguien. Se desactiva,
  -- no se borra.

  -- Único POR PRODUCTORA, no global: dos productoras pueden tener su "aniversario".
  -- La URL es aforo.ar/<productora>/<evento>.
  slug text not null check (slug ~ '^[a-z0-9][a-z0-9-]{1,58}$'),
  nombre text not null,
  descripcion text,
  flyer_url text,
  -- El plano del salón, para numerar las mesas mirando una sola pantalla. Pedido
  -- por Facu el 10/08/2026: es del EVENTO porque el venue cambia por fecha.
  plano_url text,

  empieza_en timestamptz not null,
  termina_en timestamptz,
  puertas_en timestamptz,
  venue_nombre text,
  venue_direccion text,
  venue_maps_url text,
  edad_min int,

  capacidad int check (capacidad is null or capacidad >= 0),

  -- ── LA PUERTA DE ESTA FECHA ───────────────────────────────────────────────
  -- Facu, 10/08/2026: los genera el sistema, no la productora. Si los elige una
  -- persona termina siendo el nombre del boliche o 1234, y esa clave abre el
  -- escaneo de una fecha con plata adentro. Son POR FECHA: el de puerta de ayer
  -- no valida la de mañana.
  puerta_id text not null unique,
  puerta_clave text not null,

  -- `borrador` mientras se completa el alta de 4 pasos. No se puede pasar a
  -- `publicado` sin Mercado Pago conectado: sin eso la gente compra y la plata no
  -- va a ninguna cuenta. Lo garantiza un trigger, más abajo.
  estado text not null default 'borrador' check (estado in ('borrador', 'publicado', 'cancelado')),
  -- `oculto` = existe y vende, pero no aparece en la lista pública. Es para
  -- preventas y links privados.
  visibilidad text not null default 'publico' check (visibilidad in ('publico', 'oculto')),

  publicado_en timestamptz,
  creado_en timestamptz not null default now(),
  unique (productora_id, slug)
);
create index if not exists eventos_prod_idx on public.eventos (productora_id, empieza_en desc);

-- ── NO SE PUBLICA UNA FECHA QUE NO PUEDE COBRAR ─────────────────────────────
-- La regla vive en la base y no sólo en la pantalla: una server action se puede
-- llamar desde afuera, y "no se puede publicar sin cobro" es la clase de garantía
-- que no puede depender de que el formulario esté bien hecho.
create or replace function public.exigir_cobro_para_publicar()
returns trigger language plpgsql as $$
declare conectado timestamptz;
begin
  if new.estado = 'publicado' then
    select mp_conectado_en into conectado from public.productoras where id = new.productora_id;
    if conectado is null then
      raise exception 'La productora todavía no conectó Mercado Pago: si se publica, la gente compra y la plata no va a ninguna cuenta.';
    end if;
    if new.publicado_en is null then new.publicado_en := now(); end if;
  end if;
  return new;
end $$;

drop trigger if exists eventos_exigir_cobro on public.eventos;
create trigger eventos_exigir_cobro
  before insert or update of estado on public.eventos
  for each row execute function public.exigir_cobro_para_publicar();

-- ════════════════════════════════════════════════════════════════════════════
-- 3. EL QUE COMPRA
-- ════════════════════════════════════════════════════════════════════════════
-- UNA cuenta para todas las productoras de Aforo (Facu, 10/08: "no quiero que se
-- tengan que crear una cuenta en un link nuevo y después otra"). La identidad es
-- de la plataforma, no de la productora: es el activo.
create table if not exists public.compradores (
  id uuid primary key references auth.users(id) on delete cascade,
  nombre text,
  telefono text,
  dni text,
  creado_en timestamptz not null default now()
);

-- ── QUÉ VE UNA PRODUCTORA DE ESTA GENTE ─────────────────────────────────────
-- ⚠️ Facu: el activo son los contactos. Pero la productora necesita la base de
-- SU fecha para trabajar. La regla, que hay que escribir también en los términos:
-- una productora ve el contacto de quien compró **a sus fechas**, y nada más.
-- Nunca el padrón completo. Se implementa con RLS, abajo.

-- ════════════════════════════════════════════════════════════════════════════
-- 4. LA REJA
-- ════════════════════════════════════════════════════════════════════════════
-- Todo prendido y sin policies para el cliente anónimo. Lo público (ver una fecha
-- para comprar) sale por funciones controladas, no abriendo tablas.
alter table public.productoras          enable row level security;
alter table public.productora_miembros  enable row level security;
alter table public.eventos              enable row level security;
alter table public.compradores          enable row level security;

-- Fuerza la RLS también para el dueño de la tabla: sin esto, una función
-- `security definer` mal escrita la saltea sin avisar.
alter table public.productoras          force row level security;
alter table public.productora_miembros  force row level security;
alter table public.eventos              force row level security;
alter table public.compradores          force row level security;

-- ── LOS PERMISOS, EXPLÍCITOS Y NO HEREDADOS ────────────────────────────────
-- ⚠️ En Supabase, una tabla nueva en `public` **nace con GRANT para `anon` y
-- `authenticated`** por los default privileges del proyecto. O sea: nace
-- publicada en PostgREST, y lo único que la tapa es la RLS. Eso es exactamente
-- lo que dejó 8 tablas abiertas en la academia.
--
-- Acá se escribe al revés: se revoca todo y se da sólo lo que hace falta.
-- `anon` no recibe NADA — ninguna de estas tablas se lee sin sesión. Así, el día
-- que alguien agregue una policy sin pensar, el GRANT tampoco está: dos rejas y
-- no una. Lo descubrió el test del esquema, que corría sin permisos.
revoke all on all tables in schema public from anon, authenticated;
grant select, insert, update, delete on public.eventos             to authenticated;
grant select                        on public.productoras          to authenticated;
grant select                        on public.productora_miembros  to authenticated;
grant select, insert, update        on public.compradores          to authenticated;
-- Que se cree una tabla mañana y herede permisos por olvido, no.
alter default privileges in schema public revoke all on tables from anon, authenticated;

-- ── Quién soy: las dos funciones que usan todas las policies ────────────────
create or replace function public.mis_productoras()
returns setof uuid language sql stable security definer set search_path = public as $$
  select productora_id from public.productora_miembros where user_id = auth.uid()
$$;
revoke all on function public.mis_productoras() from anon, authenticated;

-- ── Compradores: cada uno el suyo, y nadie más ─────────────────────────────
create policy "el comprador ve y edita lo suyo" on public.compradores
  for all to authenticated using (id = auth.uid()) with check (id = auth.uid());

-- ── Productoras y fechas: sólo las mías ────────────────────────────────────
create policy "miembro ve su productora" on public.productoras
  for select to authenticated using (id in (select public.mis_productoras()));
create policy "miembro ve sus fechas" on public.eventos
  for select to authenticated using (productora_id in (select public.mis_productoras()));
create policy "miembro edita sus fechas" on public.eventos
  for all to authenticated
  using (productora_id in (select public.mis_productoras()))
  with check (productora_id in (select public.mis_productoras()));
create policy "miembro se ve a si mismo" on public.productora_miembros
  for select to authenticated using (user_id = auth.uid());

-- ⚠️ NINGUNA policy para `anon`, a propósito. La página pública de una fecha NO
-- lee estas tablas con la anon key: lo hace el servidor. Abrir `eventos` a `anon`
-- para "mostrar la fecha" publica también `puerta_clave` — RLS filtra FILAS, no
-- COLUMNAS, y eso es exactamente lo que dejó abiertas 8 tablas en la academia.
--
-- Y ojo con las vistas: una VISTA ignora la RLS de su tabla. Si mañana se crea
-- `eventos_publicos` como vista, nace abierta. Ver `superficie-directa-supabase`.

-- ════════════════════════════════════════════════════════════════════════════
-- 5. LO QUE SIGUE (no está acá a propósito)
-- ════════════════════════════════════════════════════════════════════════════
-- Se porta de `astronomy-members`, donde ya funciona y está probado:
--   niveles y tandas · órdenes · entradas y QR · escaneos de puerta ·
--   mesas con sectores · comisiones escalonadas de RRPP · cortesías masivas
-- Todo eso gana una columna `productora_id` o cuelga de `eventos`, y hereda el
-- mismo aislamiento. Se hace cuando el eje esté verificado con `curl`, no antes:
-- portar sobre un eje sin probar es portar el bug a dos lugares.
