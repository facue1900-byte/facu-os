// Números de Astronomy Academy para el brief de Jarvis. SÓLO LEE.
// Usa las MISMAS funciones que el admin (lib/ingresos.ts, lib/payments.ts): la definición vive en la
// app, acá no se recalcula nada a mano. Se corre con cwd = astronomy-members (lo hace brief.py):
//
//   cd ~/Desktop/Productoras/Astronomy/Academia/astronomy-members && \
//     node --env-file=.env.local --import ./scripts/_registrar.mjs ~/facu-os/execution/jarvis/astronomy_numeros.mjs
//
// Imprime UN JSON en stdout. Nunca llama a notifyVencidos() ni a nada que mande.
import { createAdminClient } from "@/lib/supabase/admin";
import { resumenIngresos, resumenIngresosRango } from "@/lib/ingresos";
import { vencidosActuales } from "@/lib/payments";
import { labelProducto } from "@/lib/productos";

const admin = createAdminClient();
const ahora = new Date();
const ar = new Date(ahora.getTime() - 3 * 3600000);            // mes argentino, como el admin
const ym = ar.toISOString().slice(0, 7);
const hace7 = new Date(ahora.getTime() - 7 * 86400000).toISOString();

const [mes, semana, vencidos] = await Promise.all([
  resumenIngresos(admin, ym),
  resumenIngresosRango(admin, hace7, ahora.toISOString()),
  vencidosActuales(admin),
]);

// Alumnos activos: misma cuenta que el dashboard (scripts/verificar-reportes.mjs [3]).
const [{ data: subsAct, error: e1 }, { data: proAct, error: e2 }, { data: internosRows, error: e3 }] = await Promise.all([
  admin.from("subscriptions").select("user_id").eq("status", "authorized").neq("plan_id", "djdelivery"),
  admin.from("pro_enrollments").select("user_id").eq("status", "activa"),
  admin.from("profiles").select("id").eq("es_interno", true),
]);
if (e1 || e2 || e3) throw new Error("activos: " + (e1 || e2 || e3).message);
const internos = new Set((internosRows || []).map((p) => p.id));
const activos = new Set([...(subsAct || []), ...(proAct || [])].map((s) => s.user_id).filter((u) => !internos.has(u)));
if (activos.size === 0) throw new Error("activos dio 0: sospechoso (regla 2), no lo informo");

console.log(JSON.stringify({
  mes: ym,
  ingresos_mes: Math.round(mes.total),
  movimientos_mes: mes.movimientos.length,
  por_fuente: mes.porFuente.map((f) => ({ fuente: f.fuente, monto: Math.round(f.monto) })),
  ingresos_7d: Math.round(semana.total),
  movimientos_7d: semana.movimientos.length,
  activos: activos.size,
  vencidos: vencidos.length,
  vencidos_detalle: vencidos.slice(0, 10).map((v) => ({ plan: labelProducto(v.plan_id), vencia: String(v.next_charge_date).slice(0, 10) })),
}));
