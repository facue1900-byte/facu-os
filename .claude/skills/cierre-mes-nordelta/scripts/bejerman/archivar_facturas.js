// Baja los PDF de comprobantes de Bejerman usando la sesión del Chrome abierto
// en 9333 y los deja en un directorio, sin renombrar. Verifica que existan
// (404 = no emitido) antes de escribir nada.
//
//   node archivar_facturas.js <destino> "FC A0002-000000013" "ND A0002-000000008" ...
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE = 'https://www.bejermanweb.com.ar/BW20180100/PROWEB/facturas/101838/0073/';
const destino = process.argv[2];
const comps = process.argv.slice(3);
if (!destino || !comps.length) { console.log('uso: archivar_facturas.js <destino> <comp...>'); process.exit(1); }

(async () => {
  const B = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const P = B.contexts()[0].pages().find(x => x.url().includes('bejermanweb'));
  if (!P) { console.log('!! no encuentro ninguna pestaña de Bejerman'); process.exit(1); }
  fs.mkdirSync(destino, { recursive: true });
  let fallos = 0;
  for (const c of comps) {
    const url = BASE + encodeURIComponent(c) + '.pdf';
    const r = await P.evaluate(async (u) => {
      const res = await fetch(u, { credentials: 'include' });
      if (!res.ok) return { status: res.status };
      const b = new Uint8Array(await res.arrayBuffer());
      let s = ''; for (const x of b) s += String.fromCharCode(x);
      return { status: 200, b64: btoa(s) };
    }, url);
    if (r.status !== 200) { console.log(`!! ${c}: HTTP ${r.status}`); fallos++; continue; }
    const buf = Buffer.from(r.b64, 'base64');
    if (buf.slice(0, 4).toString() !== '%PDF') { console.log(`!! ${c}: no es un PDF (${buf.length} bytes)`); fallos++; continue; }
    const f = path.join(destino, c + '.pdf');
    fs.writeFileSync(f, buf);
    console.log(`ok ${c} -> ${f} (${buf.length} bytes)`);
  }
  await B.close().catch(()=>{});
  process.exit(fallos ? 3 : 0);
})();
