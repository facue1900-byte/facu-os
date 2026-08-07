const { chromium } = require('playwright-core');
const fs = require('fs');
const OUT = process.argv[2];

const INJECT = `
if (!window.__rec) {
  window.__rec = [];
  const d = e => {
    if (!e || !e.tagName) return '?';
    const txt = (e.innerText || e.value || e.getAttribute && e.getAttribute('title') || '').toString().trim().replace(/\\s+/g,' ').slice(0,55);
    const cls = (typeof e.className === 'string' && e.className) ? '.' + e.className.split(' ').filter(Boolean).slice(0,2).join('.') : '';
    return e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + cls + (txt ? ' "' + txt + '"' : '');
  };
  document.addEventListener('click', ev => {
    const p = ev.composedPath ? ev.composedPath().filter(x => x && x.tagName).slice(0,3).map(d).join('  <  ') : d(ev.target);
    window.__rec.push({ k: 'CLICK', v: p });
  }, true);
  document.addEventListener('change', ev => {
    const t = ev.target; if (!t || !/INPUT|SELECT|TEXTAREA/.test(t.tagName)) return;
    window.__rec.push({ k: 'CAMPO', v: (t.id || t.name || '(sin id)') + ' = "' + String(t.value || '').slice(0,70) + '"' });
  }, true);
  document.addEventListener('focusout', ev => {
    const t = ev.target; if (!t || !/INPUT|SELECT|TEXTAREA/.test(t.tagName)) return;
    const val = String(t.value || ''); if (!val) return;
    window.__rec.push({ k: 'SALE', v: (t.id || t.name || '(sin id)') + ' = "' + val.slice(0,70) + '"' });
  }, true);
}
'installed';
`;

const hhmm = () => new Date().toTimeString().slice(0,8);

(async () => {
  const b = await chromium.connectOverCDP('http://127.0.0.1:9333');
  const ctx = b.contexts()[0];
  fs.appendFileSync(OUT, `\n===== grabación iniciada ${hhmm()} =====\n`);
  const vistos = new Set();
  let ultimoEstado = '';
  while (true) {
    const paginas = ctx.pages();
    if (!paginas.length) { await new Promise(r => setTimeout(r, 1500)); continue; }
    const p = paginas.find(x => x.url().includes('PocAngular')) || paginas[paginas.length - 1];
    const todosLosFrames = [];
    for (const pg of paginas) for (const f of pg.frames()) todosLosFrames.push(f);
    for (const f of todosLosFrames) {
      if (f.url().includes('LiveChat') || f.url() === 'about:blank') continue;
      try {
        await f.evaluate(INJECT);
        const ev = await f.evaluate(() => (window.__rec && window.__rec.length) ? window.__rec.splice(0) : []);
        const etiqueta = f.url().includes('DatoAdicional') ? '[modal]' : f.url().includes('/ang/') ? '[app]' : '[shell]';
        for (const e of ev) {
          const linea = `${hhmm()} ${etiqueta} ${e.k}: ${e.v}`;
          const clave = e.k + e.v;
          if (e.k === 'SALE' && vistos.has(clave)) continue;
          if (e.k === 'SALE') vistos.add(clave);
          fs.appendFileSync(OUT, linea + '\n');
        }
      } catch (_) {}
    }
    // registrar cambios de pantalla
    try {
      const F = p.frames().find(x => x.url().includes('/ang/'));
      if (F) {
        const st = await F.evaluate(() => {
          const filas = [...document.querySelectorAll('[role=row]')].filter(e => e.offsetParent).slice(1,3).map(e => (e.innerText||'').replace(/\s+/g,' ').slice(0,85));
          const modal = document.querySelector('ngb-modal-window,.modal.show');
          return (location.hash.includes('/crud') ? 'FORM' : 'GRILLA') + '|' + filas.join(' // ') + '|' + (modal ? 'MODAL:' + (modal.innerText||'').replace(/\s+/g,' ').slice(0,90) : '');
        });
        if (st !== ultimoEstado) { fs.appendFileSync(OUT, `${hhmm()} [estado] ${st}\n`); ultimoEstado = st; }
      }
    } catch (_) {}
    await new Promise(r => setTimeout(r, 1200));
  }
})().catch(e => { fs.appendFileSync(OUT, 'ERROR ' + e.message + '\n'); process.exit(1); });
