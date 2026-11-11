// Routes Mercado Pago "report ready" notifications to studio@ instead of the account owner (Vlado).
// Backs up the previous config first so it can be restored.
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
fs.writeFileSync(backup, JSON.stringify(antes, null, 2));
console.log("backup ->", backup);

const r = await fetch(U, { method: "PUT", headers: H, body: JSON.stringify({ ...antes, notification_email_list: ["studio@astronomyofficial.com"] }) });
console.log("PUT", r.status, (await r.text()).slice(0, 400));

const despues = await (await fetch(U, { headers: H })).json();
console.log("notification_email_list ahora:", JSON.stringify(despues.notification_email_list));
