// Manda por mail, desde Bejerman, los comprobantes emitidos en una fecha.
//
//   node enviar_mail.js 03/09/2026 "FC A 0002 00000013" "FC A 0002 00000014" ...
//   node enviar_mail.js 03/09/2026 ... --enviar
//
// Sin --enviar es SOLO LECTURA: filtra, lista y muestra qué tildaría. Con
// --enviar tilda exactamente los comprobantes pedidos y dispara el envío.
// Bejerman ya tiene el mail de cada cliente: no hace falta saberlo.
//
// Requiere el Chrome con --remote-debugging-port=9333 logueado y parado en
// Ventas → Facturación → Enviar (URL .../ang/#/sales-send-vouchers-email).
//
// Lo que costó descubrir:
//  - La grilla es Wijmo FlexGrid. El checkbox NO está dentro de la fila: vive
//    en `.wj-rowheaders`, la fila de datos en `.wj-cells`, y el de `.wj-topleft`
//    es el "seleccionar todos" (no se toca). Emparejar por índice falla porque
//    la grilla virtualiza y mete la fila de títulos; por `style.top` falla
//    porque Wijmo posiciona CELDAS, no filas. Lo único confiable es la
//    posición REAL en pantalla: `getBoundingClientRect().top` del checkbox
//    contra el de las celdas de la fila (tolerancia 12px).
//  - "Enviar seleccionados" abre DOS modales: "Datos para envío" (asunto,
//    cuerpo, checkbox "Agrupar por cliente") y después "¿Seguro que desea
//    enviar los Comprobantes?" con Aceptar. Recién ahí manda.
//  - "Agrupar por cliente" = un mail por local con todos sus comprobantes.
//    Sin tildarlo salen 6 mails sueltos.
//  - El resultado es un alert: «Se han enviado N correos con sus
//    correspondientes comprobantes». N = cantidad de clientes si se agrupó.
const { chromium } = require('playwright-core');
const args = process.argv.slice(2);
const ENVIAR = args.includes('--enviar');
const [FECHA, ...ESPERADOS] = args.filter(a => a !== '--enviar');
const ASUNTO = process.env.ASUNTO || 'Paseo Nordelta - Comprobantes';
if (!FECHA || !ESPERADOS.length) { console.log('uso: enviar_mail.js dd/mm/aaaa "FC A 0002 000000NN" ... [--enviar]'); process.exit(1); }

(async () => {
  const B = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const P = B.contexts()[0].pages().find(x => x.url().includes('PocAngular'));
  if (!P) { console.log('!! no encuentro la pestaña de Bejerman'); process.exit(1); }
  const F = () => P.frames().find(x => x.url().includes('/ang/'));
  if (!F().url().includes('sales-send-vouchers-email')) { console.log('!! no estás en Ventas → Facturación → Enviar. URL: ' + F().url()); await B.close(); process.exit(1); }
  const M = () => F().evaluate(() => { const m = document.querySelector('ngb-modal-window, .modal.show'); return m ? (m.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 300) : null; });

  // filtro: fecha de ingreso desde/hasta
  for (const name of ['entryDateFrom', 'entryDateTo']) {
    await F().evaluate((n) => { const e = document.querySelector(`input[name=${n}]`); e.focus(); e.setSelectionRange(0, e.value.length); }, name);
    await P.keyboard.press('Backspace'); await P.keyboard.type(FECHA, { delay: 60 }); await P.keyboard.press('Tab');
    await P.waitForTimeout(500);
  }
  await F().locator('#send-vouchers-email-btn-apply').click();
  await P.waitForTimeout(6000);

  const mapear = () => F().evaluate(() => {
    const vis = e => e.offsetParent !== null, y = e => Math.round(e.getBoundingClientRect().top);
    const porY = {};
    for (const c of [...document.querySelectorAll('.wj-cells .wj-cell')].filter(vis)) { const k = y(c); (porY[k] = porY[k] || []).push((c.innerText || '').trim()); }
    const datos = Object.entries(porY).map(([k, cells]) => ({ y: +k, t: cells.join(' ').replace(/\s+/g, ' ').trim() })).filter(d => d.t);
    return [...document.querySelectorAll('.wj-rowheaders input[type=checkbox]')].filter(vis).map((cb, i) => {
      const fila = datos.find(d => Math.abs(d.y - y(cb)) <= 12);
      return { i, checked: cb.checked, fila: fila ? fila.t : '' };
    });
  });
  let mapa = await mapear();
  const conDato = mapa.filter(m => /^(FC|ND|NC) A \d{4}/.test(m.fila));
  conDato.forEach(m => console.log(`  ${m.checked ? '☑' : '☐'} ${m.fila.slice(0, 80)}`));
  const ids = conDato.map(m => m.fila.slice(0, 19).trim());
  const fuera = ids.filter(x => !ESPERADOS.includes(x)), faltan = ESPERADOS.filter(x => !ids.includes(x));
  if (fuera.length) console.log(`  (listados pero NO pedidos, no se tildan: ${fuera.join(', ')})`);
  if (faltan.length) { console.log(`!! FRENO: faltan en la grilla: ${faltan.join(', ')}`); await B.close(); process.exit(2); }
  const aTildar = conDato.filter(m => ESPERADOS.includes(m.fila.slice(0, 19).trim()));
  if (!ENVIAR) { console.log(`\n[sin --enviar] tildaría ${aTildar.length}. No toqué nada.`); await B.close(); return; }

  for (const m of aTildar) { if (!m.checked) { await F().evaluate((i) => { [...document.querySelectorAll('.wj-rowheaders input[type=checkbox]')].filter(e => e.offsetParent !== null)[i].click(); }, m.i); await P.waitForTimeout(400); } }
  mapa = await mapear();
  const marcados = mapa.filter(m => m.checked && /^(FC|ND|NC) A \d{4}/.test(m.fila)).map(m => m.fila.slice(0, 19).trim());
  if (marcados.length !== ESPERADOS.length || marcados.some(x => !ESPERADOS.includes(x))) { console.log(`!! FRENO: tildados ${marcados}`); await B.close(); process.exit(3); }
  console.log(`\nseleccionados ${marcados.length}: ${marcados.join(', ')}`);

  await F().locator('#send-vouchers-email-btn-send-selected').click();
  await P.waitForTimeout(3000);
  if (!/Datos para env/i.test((await M()) || '')) { console.log('!! no abrió "Datos para envío": ' + await M()); await B.close(); process.exit(4); }
  await F().evaluate(() => { const e = document.getElementById('sendMailSubject'); e.focus(); e.setSelectionRange(0, e.value.length); });
  await P.keyboard.press('Backspace'); await P.keyboard.type(ASUNTO, { delay: 40 });
  await F().evaluate(() => { const m = document.querySelector('ngb-modal-window, .modal.show'); const cb = m.querySelector('input[type=checkbox]'); if (cb && !cb.checked) cb.click(); });
  await P.waitForTimeout(600);
  const est = await F().evaluate(() => ({ asunto: document.getElementById('sendMailSubject').value, agrupar: document.querySelector('ngb-modal-window, .modal.show').querySelector('input[type=checkbox]').checked }));
  console.log('modal:', JSON.stringify(est));
  if (est.asunto !== ASUNTO || !est.agrupar) { console.log('!! FRENO: el modal no quedó como esperaba'); await B.close(); process.exit(5); }
  await F().evaluate(() => { const m = document.querySelector('ngb-modal-window, .modal.show'); [...m.querySelectorAll('button')].find(x => /^enviar$/i.test((x.innerText || '').trim())).click(); });
  await P.waitForTimeout(3000);
  if (!/Seguro que desea enviar/i.test((await M()) || '')) { console.log('!! no apareció la confirmación: ' + await M()); await B.close(); process.exit(6); }
  await F().evaluate(() => { const m = document.querySelector('ngb-modal-window, .modal.show'); [...m.querySelectorAll('button')].find(x => /^aceptar$/i.test((x.innerText || '').trim())).click(); });

  let res = { alertas: [] };
  for (let t = 0; t < 20 && !res.alertas.length; t++) {
    await P.waitForTimeout(2000);
    res = await F().evaluate(() => ({ alertas: [...document.querySelectorAll('.alert,[role=alert],.toast,.bui-alert,ngb-toast,.notification,.bento-alert,.bento-toast')].filter(e => e.offsetParent !== null).map(e => (e.innerText || '').replace(/\s+/g, ' ').trim()).filter(Boolean) }));
  }
  console.log('\nRESULTADO:', res.alertas.join(' || ') || '(sin mensaje en 40s — verificar a mano)');
  if (!res.alertas.some(a => /se han enviado/i.test(a))) { await B.close(); process.exit(7); }
  await B.close();
})().catch(e => { console.log('ERROR: ' + e.message.slice(0, 200)); process.exit(1); });
