const { chromium } = require('playwright-core');
const s = JSON.parse(process.argv[2]);
const log = m => process.stdout.write(m + '\n');
const wd = setTimeout(() => { log('!! WATCHDOG 300s'); process.exit(9); }, 300000);
let B, P;
const die = async (m, c) => { log('!! ' + m); clearTimeout(wd); if (B) await B.close().catch(()=>{}); process.exit(c); };

(async () => {
  B = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const ctx = B.contexts()[0];
  P = ctx.pages().find(x => x.url().includes('PocAngular'));
  if (!P) await die('no encuentro la pestaña de Bejerman', 1);
  const F = () => P.frames().find(x => x.url().includes('/ang/'));
  const opciones = () => F().evaluate(() => {
    const o = []; document.querySelectorAll('[role=option]').forEach(e => {
      if (e.offsetParent === null) return;
      const t = (e.innerText||'').trim().replace(/\s+/g,' '); if (t) o.push({ id: e.id, t: t.slice(0,95) }); });
    return o;
  });
  const neutro = async () => {
    await F().evaluate(() => {
      const t = document.querySelector('.main-sales-crud') || document.body;
      t.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      document.activeElement && document.activeElement.blur && document.activeElement.blur();
    }).catch(()=>{});
    await P.keyboard.press('Escape').catch(()=>{});
    await P.waitForTimeout(1200);
  };
  const enfocarYTipear = async (sel, texto) => {
    await F().evaluate(([q, t]) => {
      const e = document.querySelector(q);
      if (!e) return;
      e.focus();
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(e, '');
      e.dispatchEvent(new Event('input', { bubbles: true }));
    }, [sel, texto]);
    await P.waitForTimeout(500);
    await P.keyboard.type(texto, { delay: 130 });
  };
  const combo = async (sel, texto, pick, esperado) => {
    let ops = [];
    const tiene = a => a.some(o => o.t.startsWith(pick));
    for (let i = 1; i <= 6 && !tiene(ops); i++) {
      await enfocarYTipear(sel, texto);
      for (let k = 0; k < 18 && !tiene(ops); k++) { await P.waitForTimeout(400); ops = await opciones(); }
      if (!tiene(ops)) log(`   (${sel}: todavía no aparece "${pick}" (${ops.length} opciones), reintento ${i})`);
    }
    const idx = ops.findIndex(o => o.t.startsWith(pick));
    if (idx < 0) await die(`${sel}: no hay opción "${pick}". Hay: ${ops.map(o=>o.t).join(' | ').slice(0,320)}`, 2);
    const clicOk = await F().evaluate((id) => {
      const e = document.getElementById(id);
      if (!e) return false;
      e.scrollIntoView({ block: 'nearest' });
      for (const t of ['mousedown', 'mouseup', 'click']) {
        e.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window }));
      }
      return true;
    }, ops[idx].id);
    if (!clicOk) await die(`no pude clickear la opción ${ops[idx].t}`, 11);
    await P.waitForTimeout(3000);
    const q = await F().locator(sel).first().inputValue();
    if (esperado && !q.includes(esperado)) await die(`${sel} quedó "${q}", esperaba "${esperado}"`, 3);
    log(`   ${sel} = ${q}`);
  };

  // asegurar grilla
  for (let i = 0; i < 3 && F().url().includes('/crud'); i++) {
    await F().evaluate(() => { const c=[...document.querySelectorAll('button')].find(e=>e.offsetParent&&/^(Cancelar|Cerrar)/.test((e.innerText||'').trim())); if(c)c.click(); });
    await P.waitForTimeout(4000);
    await F().evaluate(() => { const d=document.querySelector('ngb-modal-window,.modal.show'); if(d){const y=[...d.querySelectorAll('button')].find(e=>/^s[ií]$/i.test((e.innerText||'').trim())); if(y)y.click();} }).catch(()=>{});
    await P.waitForTimeout(4000);
  }
  if (F().url().includes('/crud')) await die('no pude volver a la grilla', 4);

  // EMITIR -> abre form
  await F().evaluate(() => { const e=[...document.querySelectorAll('button,a')].find(x=>x.offsetParent&&(x.innerText||'').trim()==='Emitir'); if(e)e.click(); });
  await P.waitForTimeout(9000);
  if (!F().url().includes('/crud')) await die('no abrió el formulario de emisión', 5);
  const hayEmitir = await F().evaluate(() => !!document.getElementById('sales-crud-emit-button'));
  if (!hayEmitir) await die('el form abierto NO es el de Emitir (falta sales-crud-emit-button)', 6);
  log('formulario de EMISION abierto');

  await combo('#contact', s.buscaCli, s.pickCli, s.espCli);
  await combo('#voucherType', s.buscaTipo, s.pickTipo, s.espTipo);
  await combo('#salePoint-combo', '0002', '0002', '0002');
  const nro = await F().evaluate(() => { const e = document.getElementById('number'); return e ? e.value : '(lo asigna ARCA al emitir)'; });
  log(`   número: ${nro}`);

  // renglón
  let hay = false;
  for (let i = 0; i < 3 && !hay; i++) {
    await F().evaluate(() => { const a=[...document.querySelectorAll('button')].find(e=>e.offsetParent&&(e.innerText||'').trim()==='Agregar'); if(a)a.click(); });
    await P.waitForTimeout(5000);
    hay = await F().evaluate(() => !!document.getElementById('itemsConcepts'));
  }
  if (!hay) await die('no pude agregar el renglón', 7);
  await combo('#itemsConcepts', s.buscaConc, s.pickConc, s.espConc);

  const celda = async (n, valor) => {
    await F().evaluate((i) => {
      const v = [...document.querySelectorAll('input')].filter(e => e.offsetParent && !e.id);
      const e = v[i]; if (!e) return;
      e.focus();
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(e, ''); e.dispatchEvent(new Event('input', { bubbles: true }));
    }, n);
    await P.waitForTimeout(600);
    await P.keyboard.type(String(valor), { delay: 70 });
    await P.keyboard.press('Tab');
    await P.waitForTimeout(2500);
  };
  await celda(0, s.desc);
  await celda(2, s.precio);
  await P.waitForTimeout(3500);

  // período (obligatorio en Notas de Débito)
  if (s.desde && s.hasta) {
    await F().evaluate(() => { const b2=[...document.querySelectorAll('button')].find(e=>e.offsetParent&&(e.innerText||'').trim()==='Datos adicionales'); if(b2)b2.click(); });
    await P.waitForTimeout(8000);
    const M = () => P.frames().find(x => x.url().includes('DatoAdicionalComprobante'));
    if (!M()) await die('no abrió Datos adicionales (la ND lo necesita)', 12);
    for (const [id, val] of [['DatosAdic_Dscv_FECHADESDE', s.desde], ['DatosAdic_Dscv_FECHAHASTA', s.hasta]]) {
      const el = M().locator('#' + id);
      await el.click({ timeout: 12000 }); await el.fill(''); await el.type(val, { delay: 90 });
      await P.waitForTimeout(700);
    }
    const per = await M().evaluate(() => ({ d: document.getElementById('DatosAdic_Dscv_FECHADESDE').value, h: document.getElementById('DatosAdic_Dscv_FECHAHASTA').value }));
    if (per.d !== s.desde || per.h !== s.hasta) await die(`período quedó ${per.d}-${per.h}, pedí ${s.desde}-${s.hasta}`, 13);
    log(`   período ${per.d} a ${per.h}`);
    await M().locator('#DatosAdic_aceptar').click({ timeout: 12000 });
    await P.waitForTimeout(7000);
  }

  const est = await F().evaluate(() => {
    const v=[]; document.querySelectorAll('input').forEach(e=>{ if(e.offsetParent&&!e.id) v.push(String(e.value||'')); });
    const t=document.body.innerText.replace(/\s+/g,' ');
    const m=t.match(/Total \$\s*([\d\.,]+)/) || t.match(/Perc\.\/Ret\.\s*Total\s*\$?\s*([\d\.,]+)/);
    return { desc: v[0], precio: v[2], neto: v[v.length-4], iva: v[v.length-3], total: m?m[1]:null };
  });
  log(`   descripción: "${est.desc}"   precio: ${est.precio}`);
  log(`   neto ${est.neto} + IVA ${est.iva}`);
  log(`   TOTAL: ${est.total}   (esperado ${s.total})`);
  if (est.desc !== s.desc) await die(`la descripción quedó "${est.desc}"`, 8);
  if (est.total !== s.total) await die(`TOTAL NO COINCIDE: ${est.total} vs ${s.total}. NO EMITO.`, 9);
  log('   verificado, emito');

  await F().locator('#sales-crud-emit-button').first().click({ timeout: 20000, noWaitAfter: true }).catch(e => log('   warn ' + e.message.slice(0,60)));
  await P.waitForTimeout(4000);
  const c = await F().evaluate(() => {
    const m=document.querySelector('ngb-modal-window,.modal.show'); if(!m) return 'sin modal';
    const txt=(m.innerText||'').replace(/\s+/g,' ');
    if(!/emisi/i.test(txt)) return 'modal inesperado: '+txt.slice(0,120);
    const y=[...m.querySelectorAll('button')].find(e=>/^s[ií]$/i.test((e.innerText||'').trim()));
    if(!y) return 'sin Sí';
    y.click(); return 'CONFIRMADO';
  });
  log('   ' + c);
  if (c !== 'CONFIRMADO') await die('no confirmé la emisión', 10);
  await P.waitForTimeout(9000);
  const alerta = await F().evaluate(() => {
    const a = [...document.querySelectorAll('.alert,.bento-alert,[role=alert],.bui-alert')].filter(e => e.offsetParent)
      .map(e => (e.innerText||'').replace(/\s+/g,' ').trim()).filter(Boolean);
    return a.join(' || ').slice(0, 300);
  }).catch(() => '');
  if (alerta && !/exitos/i.test(alerta)) await die('LA EMISION FALLO: ' + alerta, 14);
  if (alerta) log('   mensaje: ' + alerta);
  for (let i=0;i<20;i++){ await P.waitForTimeout(3000); const f=F(); if(f && !f.url().includes('/crud')) break; }
  await P.waitForTimeout(3000);
  const fila = await F().evaluate(() => { const r=[...document.querySelectorAll('[role=row]')].filter(e=>e.offsetParent)[1]; return r?(r.innerText||'').replace(/\s+/g,' ').slice(0,100):'(sin filas)'; }).catch(()=>'(no leí)');
  log('   >> primera fila de la grilla: ' + fila);
  clearTimeout(wd); await B.close(); process.exit(0);
})().catch(async e => { log('ERROR: ' + e.message.slice(0,160)); if (B) await B.close().catch(()=>{}); process.exit(1); });
