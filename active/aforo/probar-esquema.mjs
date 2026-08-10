// ============================================================================
// EL EJE DE AFORO, PROBADO CONTRA UN POSTGRES DE VERDAD
// ============================================================================
//   node probar-esquema.mjs
//
// Corre `ESQUEMA_EJE.sql` sobre Postgres 18 en WASM (PGlite) — sin Docker, sin
// proyecto en la nube, sin gastar un peso. Prueba lo único que no se puede
// arreglar hacia atrás: **que una productora no vea un solo dato de otra**.
//
// ── POR QUÉ SE PRUEBA ACÁ Y NO SÓLO EN SUPABASE ─────────────────────────────
// Las policies de RLS y los triggers son Postgres, no Supabase. Se pueden probar
// enteros antes de pagar los US$25/mes del tercer proyecto. Lo que NO se prueba
// acá y hay que probar en la nube: PostgREST (que la anon key no vea nada) y
// Auth. Eso queda dicho para no confundir "probado" con "probado todo".
//
// PGlite no trae el esquema `auth` de Supabase, así que se crea el mínimo:
// `auth.users` y `auth.uid()` leyendo una variable de sesión. Es exactamente lo
// que hace Supabase por dentro, y sirve para probar las policies tal como están.
import { PGlite } from "@electric-sql/pglite";
import { readFileSync } from "node:fs";

let fallas = 0;
const ok = (cond, txt, dio) => {
  console.log(`  ${cond ? "OK  " : "FALLA"}   ${txt}${dio !== undefined ? ` → ${dio}` : ""}`);
  if (!cond) fallas++;
};

const db = await PGlite.create();

// ── El mínimo de Supabase que el esquema necesita ──────────────────────────
await db.exec(`
  create schema if not exists auth;
  create table auth.users (id uuid primary key, email text);
  -- Igual que en Supabase: el uid sale del JWT, acá de una variable de sesión.
  create or replace function auth.uid() returns uuid language sql stable as $$
    select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
  $$;
  create role anon;
  create role authenticated;
  -- ATENCION: asi arranca un proyecto de Supabase de verdad. Las tablas nuevas
  -- del schema public nacen con GRANT para anon y authenticated. Se replica aca
  -- para que el test parta del mismo lugar, y no de un Postgres mas seguro que
  -- el real. (Sin acentos ni backticks: esto vive dentro de un template de JS.)
  alter default privileges in schema public grant all on tables to anon, authenticated;
`);

console.log("\n[1] El esquema se aplica limpio");
const sql = readFileSync(new URL("./ESQUEMA_EJE.sql", import.meta.url), "utf8");
try {
  await db.exec(sql);
  ok(true, "ESQUEMA_EJE.sql corre sin errores");
} catch (e) {
  ok(false, "ESQUEMA_EJE.sql corre sin errores", e.message.slice(0, 200));
  console.log("\n>>> el esquema no aplica, no tiene sentido seguir");
  process.exit(1);
}

const tablas = await db.query(`
  select tablename, rowsecurity from pg_tables where schemaname = 'public' order by tablename`);
ok(tablas.rows.length === 4, "quedaron las 4 tablas del eje", tablas.rows.map(t => t.tablename).join(", "));
ok(tablas.rows.every(t => t.rowsecurity), "las 4 con RLS PRENDIDA", tablas.rows.filter(t => !t.rowsecurity).map(t => t.tablename).join(",") || "todas");
const forzada = await db.query(`select relname from pg_class where relforcerowsecurity and relnamespace = 'public'::regnamespace`);
ok(forzada.rows.length === 4, "y las 4 con RLS FORZADA: una función security definer mal escrita no la saltea", forzada.rows.length);

console.log("\n[2] Nadie tiene policies para el cliente anónimo");
// Si mañana alguien le agrega una policy a `anon` para "mostrar la fecha", publica
// también `puerta_clave`: la RLS filtra FILAS, no COLUMNAS. Es el bug que dejó 8
// tablas abiertas en la academia.
const pa = await db.query(`
  select tablename, policyname, roles::text from pg_policies
  where schemaname='public' and roles::text like '%anon%'`);
ok(pa.rows.length === 0, "cero policies para anon, a propósito", pa.rows.length);

// Lo encontró este test: en Supabase las tablas nacen con GRANT para anon, así que
// el esquema tiene que revocarlo explícitamente. Dos rejas y no una.
const gr = await db.query(`
  select table_name, privilege_type from information_schema.role_table_grants
  where grantee = 'anon' and table_schema = 'public'`);
ok(gr.rows.length === 0, "anon no tiene NI UN permiso sobre las tablas del eje", gr.rows.length);
const ga = await db.query(`
  select count(*)::int n from information_schema.role_table_grants
  where grantee = 'authenticated' and table_schema = 'public' and privilege_type = 'SELECT'`);
ok(ga.rows[0].n === 4, "y authenticated sí puede leer las 4 (la RLS decide qué filas)", ga.rows[0].n);

console.log("\n[3] Dos productoras, y ninguna ve a la otra");
// El caso real: Puzzle y otra productora en la misma base.
const [U1, U2] = ["11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222"];
await db.exec(`
  insert into auth.users (id, email) values ('${U1}','duenio@puzzle.com'), ('${U2}','otra@productora.com');
  insert into public.productoras (id, slug, nombre, mp_conectado_en) values
    ('aaaaaaaa-0000-0000-0000-000000000001','puzzle','Puzzle', now()),
    ('aaaaaaaa-0000-0000-0000-000000000002','otra','Otra Productora', now());
  insert into public.productora_miembros (productora_id, user_id, rol) values
    ('aaaaaaaa-0000-0000-0000-000000000001','${U1}','dueño'),
    ('aaaaaaaa-0000-0000-0000-000000000002','${U2}','dueño');
  insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave, estado) values
    ('aaaaaaaa-0000-0000-0000-000000000001','aniversario','Puzzle Aniversario','2026-09-12 23:00+00','PZL-0001','AAA111','publicado'),
    ('aaaaaaaa-0000-0000-0000-000000000002','aniversario','Otra Aniversario','2026-09-20 23:00+00','OTR-0001','BBB222','publicado');
`);
ok(true, "cargadas 2 productoras con 1 fecha cada una");

// Se entra COMO el dueño de Puzzle: rol `authenticated` y su uid, igual que Supabase.
// Devuelve `{rows}` o `{error}`: un rechazo de permisos es un RESULTADO esperado
// en varios de estos chequeos, no una excepción que corta el script.
// Cada intento va en su SAVEPOINT: en Postgres, una sentencia que falla aborta la
// transacción entera y todo lo que sigue devuelve "current transaction is aborted".
// Sin esto, el primer rechazo —que es justo lo que se está probando— se lleva
// puestos los chequeos de abajo y parecen fallar todos.
let n = 0;
const como = async (uid, q) => {
  const sp = `sp${++n}`;
  try {
    await db.exec(`savepoint ${sp}; set local role authenticated; set local "request.jwt.claim.sub" = '${uid}';`);
    const r = await db.query(q);
    await db.exec(`reset role; reset "request.jwt.claim.sub"; release savepoint ${sp};`);
    return { rows: r.rows };
  } catch (e) {
    try { await db.exec(`rollback to savepoint ${sp}; reset role; reset "request.jwt.claim.sub";`); } catch {}
    return { rows: [], error: String(e.message || e).slice(0, 90) };
  }
};

await db.exec("begin");
const misFechas = await como(U1, "select nombre from public.eventos");
ok(misFechas.rows.length === 1, "el dueño de Puzzle ve 1 fecha, no 2", misFechas.rows.map(r => r.nombre).join(","));
ok(misFechas.rows[0]?.nombre === "Puzzle Aniversario", "y es la suya", misFechas.rows[0]?.nombre);

const misProds = await como(U1, "select nombre from public.productoras");
ok(misProds.rows.length === 1 && misProds.rows[0].nombre === "Puzzle", "y ve una sola productora: la suya", misProds.rows.map(r => r.nombre).join(","));

// ⚠️ LO QUE NO SE PUEDE ARREGLAR HACIA ATRÁS: pedir la clave de puerta de otro.
const claveAjena = await como(U1, `select puerta_clave from public.eventos where puerta_id = 'OTR-0001'`);
ok(claveAjena.rows.length === 0, "⚠️  NO puede leer la clave de puerta de la otra productora", claveAjena.rows.length);

// Y tampoco escribirle encima.
await como(U1, `update public.eventos set nombre = 'HACKEADA' where puerta_id = 'OTR-0001'`);
const tras = await db.query(`select nombre from public.eventos where puerta_id='OTR-0001'`);
const escribio = tras.rows[0].nombre === "HACKEADA";
ok(!escribio, "⚠️  NO puede editar la fecha de la otra productora");

// Ni crear una fecha a nombre de otra.
const intento = await como(U1, `insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave)
    values ('aaaaaaaa-0000-0000-0000-000000000002','colada','Colada','2026-10-01 23:00+00','X-1','Z1')`);
const colada = await db.query(`select count(*)::int n from public.eventos where slug='colada'`);
const creo = !intento.error && colada.rows[0].n > 0;
ok(!creo, "⚠️  NO puede crear una fecha a nombre de la otra productora");
await db.exec("rollback");

console.log("\n[4] No se publica una fecha que no puede cobrar");
// La regla vive en la base y no sólo en la pantalla: una server action se llama
// desde afuera, y "no se publica sin cobro" no puede depender del formulario.
await db.exec(`insert into public.productoras (id, slug, nombre) values
  ('aaaaaaaa-0000-0000-0000-000000000003','sinmp','Sin Mercado Pago')`);
let publico = true, motivo = "";
try {
  await db.exec(`insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave, estado)
    values ('aaaaaaaa-0000-0000-0000-000000000003','fecha','Fecha','2026-11-01 23:00+00','SIN-1','C1','publicado')`);
} catch (e) { publico = false; motivo = e.message; }
ok(!publico, "una fecha NO se publica si la productora no conectó Mercado Pago");
ok(motivo.includes("la plata no va a ninguna cuenta"), "y el error lo dice en castellano, no en jerga", motivo.slice(0, 72));

// En borrador sí entra: la fecha existe desde el paso 1 y se completa después.
await db.exec(`insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave)
  values ('aaaaaaaa-0000-0000-0000-000000000003','borrador','En Borrador','2026-11-01 23:00+00','SIN-2','C2')`);
const bo = await db.query(`select estado, publicado_en from public.eventos where puerta_id='SIN-2'`);
ok(bo.rows[0].estado === "borrador", "pero SÍ se guarda como borrador: no se pierde lo cargado", bo.rows[0].estado);
ok(bo.rows[0].publicado_en === null, "y no se marca como publicada");

// Y al conectar MP, la misma fecha se puede publicar.
await db.exec(`update public.productoras set mp_conectado_en = now() where slug='sinmp'`);
await db.exec(`update public.eventos set estado='publicado' where puerta_id='SIN-2'`);
const ya = await db.query(`select estado, publicado_en from public.eventos where puerta_id='SIN-2'`);
ok(ya.rows[0].estado === "publicado" && ya.rows[0].publicado_en !== null,
   "conectando Mercado Pago sí se publica, y se sella la fecha sola");

console.log("\n[5] Los datos que no pueden entrar mal");
const rechaza = async (q, txt) => {
  let entro = true;
  try { await db.exec(q); } catch { entro = false; }
  ok(!entro, txt);
};
await rechaza(`insert into public.productoras (slug, nombre) values ('Puzzle Oficial','X')`,
  "un slug con mayúsculas y espacios se rechaza: va en la URL");
await rechaza(`insert into public.productoras (slug, nombre, fee_pct) values ('pepe','X', 120)`,
  "un fee del 120% se rechaza");
await rechaza(`insert into public.productoras (slug, nombre) values ('puzzle','Duplicada')`,
  "dos productoras con el mismo slug se rechazan: la URL es una sola");
// Dos productoras SÍ pueden tener su "aniversario": el slug es único por productora.
let dosAniv = true;
try {
  await db.exec(`insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave)
    values ('aaaaaaaa-0000-0000-0000-000000000003','aniversario','Tercera Aniversario','2026-12-01 23:00+00','TER-1','D1')`);
} catch { dosAniv = false; }
ok(dosAniv, "pero dos productoras SÍ pueden tener cada una su «aniversario»");
await rechaza(`insert into public.eventos (productora_id, slug, nombre, empieza_en, puerta_id, puerta_clave)
  values ('aaaaaaaa-0000-0000-0000-000000000001','otra-fecha','X','2026-12-01 23:00+00','PZL-0001','E1')`,
  "dos fechas con el mismo ID de puerta se rechazan: la clave abre una sola");

console.log("\n[6] Una productora con plata vendida no se borra de un tirón");
let borro = true;
try { await db.exec(`delete from public.productoras where slug='puzzle'`); } catch { borro = false; }
ok(!borro, "borrar una productora con fechas se rechaza: se lleva QR que están en celulares ajenos");

console.log(fallas === 0
  ? "\n>>> TODO OK — el eje aísla, no publica sin cobro y no acepta datos mal\n    (falta probar en la nube: PostgREST con la anon key, y Auth)"
  : `\n>>> ${fallas} FALLA(S)`);
process.exit(fallas === 0 ? 0 : 1);
