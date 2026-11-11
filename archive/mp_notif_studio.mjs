// Routes Mercado Pago "report ready" notifications to studio@ instead of the account owner (Vlado).
// Backs up the previous config first so it can be restored.
// v2 (11/11/2026): v1 resent the whole GET body and MP answered 500 internal_error.
// Now it sends only the fields MP documents for PUT /config, with frequency.value as a number.
import fs from "node:fs";
const APP = "/Users/Facu/Desktop/Productoras/Astronomy/Academia/astronomy-members";
const env = Object.fromEntries(
  fs.readFileSync(`${APP}/.env.local`, "utf8").split("\n")
    .filter((l) => l.includes("=") && !l.startsWith("#"))
    .map((l) => { const i = l.indexOf("="); return [l.slice(0, i).trim(), l.slice(i + 1).trim().replace(/^"|"$/g, "")]; }),
);
const H = { Authorization: `Bearer ${env.MP_ACCESS_TOKEN}`, "Content-Type": "application/json" };
const U = "https://api.mercadopago.com/v1/account/release_report/config";

const antes = await (await fetch(U, { headers: H })).json();
const backup = "/Users/Facu/facu-os/archive/mp-release-config-antes-2026-11-11.json";
if (!fs.existsSync(backup)) fs.writeFileSync(backup, JSON.stringify(antes, null, 2));
console.log("backup ->", backup);

const body = {
  file_name_prefix: antes.file_name_prefix,
  include_withdrawal_at_end: antes.include_withdrawal_at_end,
  scheduled: antes.scheduled,
  execute_after_withdrawal: antes.execute_after_withdrawal,
  separator: antes.separator,
  display_timezone: antes.display_timezone,
  report_language: antes.report_language,
  columns: antes.columns.map((c) => ({ key: c.key })),
  notification_email_list: ["studio@astronomyofficial.com"],
};
// v3: value 0 → 400 invalid_frequency; value "" (as GET returns it) → 500. Try the remaining
// shapes in order and stop at the first one MP accepts. A rejected PUT changes nothing.
const hour = antes.frequency?.hour ?? 0;
const intentos = [
  { hour, type: "daily" },
  { hour, type: "daily", value: "" },
  { hour, type: "daily", value: 1 },
  undefined,
];
for (const frequency of intentos) {
  const b = frequency ? { ...body, frequency } : body;
  const r = await fetch(U, { method: "PUT", headers: H, body: JSON.stringify(b) });
  console.log("PUT", JSON.stringify(frequency ?? "sin frequency"), "→", r.status, (await r.text()).slice(0, 200));
  if (r.ok) break;
}

const despues = await (await fetch(U, { headers: H })).json();
console.log("notification_email_list ahora:", JSON.stringify(despues.notification_email_list));
