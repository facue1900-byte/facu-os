// Tandas diarias de WhatsApp desde el número de Facu, con una sesión vinculada PROPIA
// (como un WhatsApp Web más: no usa su Chrome ni le roba la pantalla).
//
// Cada campaña vive en campanas.json: un CSV (fuente única del estado de cada contacto),
// el texto aprobado por Facu, cuántos por día y cada cuánto.
//
//   node tanda.mjs --setup                      vincular la sesión (QR en data/wa_tanda/qr.png)
//   node tanda.mjs --campana habanna-earlys     simulacro: dice a quién le mandaría, no conecta
//   node tanda.mjs --campana habanna-earlys --send     manda de verdad (lo corre launchd)
//   --forzar   ignora horario y tope del día (para probar a mano)
//   --limite N pisa el tope diario de la campaña
//   WA_TANDA_DATOS=<dir> pisa la carpeta de sesión/estado (para pruebas aisladas)
//
// Protecciones, cada una por un modo de falla concreto:
// - El CSV se RELEE antes de cada marca y se toca sólo la fila de ese teléfono: si Facu u
//   otro script lo editó durante la tanda (~45 min), no se pisa.
// - Se marca «ENVIANDO» ANTES de mandar: si el envío sale y algo falla después, esa fila ya
//   no es elegible y nadie recibe dos veces.
// - BAJA: se mira el historial del chat. Una sesión vinculada nueva puede no tener el
//   historial sincronizado; si no aparece NINGÚN mensaje nuestro (y el CSV dice que le
//   mandamos), el chequeo de BAJA no chequea nada → no se manda, se marca REVISAR.
// - Un contacto que tira error se marca ERROR y se sigue; 3 errores seguidos cortan con exit 1.
// - El horario se revisa antes de cada envío, no sólo al arrancar.
// Salidas: 0 ok o nada que hacer · 1 error · 2 sesión vencida (hay que correr --setup).
// Lo corre execution/launchd/com.facu.wa-tanda.plist vía correr.sh, que avisa si falla.

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify/sync';
import QRCode from 'qrcode';
import wweb from 'whatsapp-web.js';

const { Client, LocalAuth } = wweb;
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const DATOS = process.env.WA_TANDA_DATOS || '/Users/Facu/facu-os/data/wa_tanda';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const BAJA = /\b(baja|stop|no (me )?(escrib|mand)|sacame|borrame)/i;

const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const valor = (f) => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : undefined; };

const hoyISO = () => new Date().toLocaleDateString('sv-SE', { timeZone: 'America/Argentina/Buenos_Aires' });
const hoyCorto = () => { const [, m, d] = hoyISO().split('-'); return `${d}/${m}`; };
const horaAR = () => Number(new Date().toLocaleString('en-US', { hour: 'numeric', hourCycle: 'h23', timeZone: 'America/Argentina/Buenos_Aires' }));
const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
const log = (...a) => console.log(new Date().toTimeString().slice(0, 8), ...a);
const digitos = (t) => (t || '').replace(/\D/g, '');

function notificar(texto) {
  log(`[aviso] ${texto}`);
  try { execFileSync('osascript', ['-e', `display notification ${JSON.stringify(texto)} with title "WhatsApp tanda"`]); } catch {}
}

function leerCSV(c) {
  const filas = parse(fs.readFileSync(c.csv, 'utf8'), { columns: true, skip_empty_lines: true, bom: true });
  if (!filas.length) throw new Error(`El CSV ${c.csv} está vacío: no lo doy por "campaña terminada"`);
  const columnas = Object.keys(filas[0]);
  for (const col of [c.col_nombre, c.col_telefono, c.col_estado]) {
    if (!columnas.includes(col)) throw new Error(`Falta la columna "${col}" en ${c.csv} (hay: ${columnas.join(', ')})`);
  }
  return { filas, columnas };
}

// Relee el CSV y agrega el sufijo sólo a la fila de ese teléfono (o reemplaza uno previo).
function marcar(c, telefono, sufijo, reemplaza) {
  const { filas, columnas } = leerCSV(c);
  const f = filas.find((x) => digitos(x[c.col_telefono]) === digitos(telefono));
  if (!f) throw new Error(`No encuentro ${telefono} en el CSV al marcar "${sufijo}"`);
  const actual = f[c.col_estado] || '';
  f[c.col_estado] = reemplaza && actual.endsWith(` + ${reemplaza}`)
    ? actual.slice(0, -reemplaza.length) + sufijo
    : `${actual} + ${sufijo}`;
  const tmp = c.csv + '.tmp';
  fs.writeFileSync(tmp, stringify(filas, { header: true, columns: columnas }));
  fs.renameSync(tmp, c.csv);
}

function nuevoCliente() {
  return new Client({
    authStrategy: new LocalAuth({ clientId: 'facu', dataPath: path.join(DATOS, 'sesion') }),
    puppeteer: { executablePath: CHROME, headless: true, args: ['--no-first-run'] },
  });
}

function conectar(cliente, { setup }) {
  return new Promise((resolve, reject) => {
    const corte = setTimeout(() => reject(new Error('WhatsApp no conectó en 3 minutos')), setup ? 600000 : 180000);
    cliente.on('qr', async (qr) => {
      if (!setup) { clearTimeout(corte); const e = new Error('Sesión vencida: hay que volver a vincular con --setup'); e.codigo = 2; reject(e); return; }
      const png = path.join(DATOS, 'qr.png');
      await QRCode.toFile(png, qr, { width: 420 });
      log(`QR listo en ${png} — escanealo desde el celu: WhatsApp > Dispositivos vinculados > Vincular dispositivo`);
    });
    cliente.on('auth_failure', (m) => { clearTimeout(corte); reject(new Error('Falló la autenticación: ' + m)); });
    cliente.on('ready', () => { clearTimeout(corte); resolve(); });
    cliente.initialize().catch((e) => { clearTimeout(corte); reject(e); });
  });
}

async function setup() {
  fs.mkdirSync(DATOS, { recursive: true });
  const cliente = nuevoCliente();
  try {
    await conectar(cliente, { setup: true });
    log(`Vinculado como ${cliente.info.wid.user}. La sesión queda en ${DATOS}/sesion.`);
    try { fs.unlinkSync(path.join(DATOS, 'qr.png')); } catch {}
    await dormir(8000); // que termine de guardar la sesión antes de cerrar
  } finally {
    await cliente.destroy().catch(() => {});
  }
}

async function tanda(id) {
  const campanas = JSON.parse(fs.readFileSync(path.join(AQUI, 'campanas.json'), 'utf8'));
  const c = campanas[id];
  if (!c) throw new Error(`No existe la campaña "${id}". Hay: ${Object.keys(campanas).join(', ')}`);
  const enviar = flag('--send');
  const forzar = flag('--forzar');
  const limite = Number(valor('--limite') ?? c.limite_diario);
  if (!Number.isInteger(limite) || limite <= 0) throw new Error(`Límite inválido: ${valor('--limite') ?? c.limite_diario}`);
  const enHorario = () => forzar || (horaAR() >= c.horario[0] && horaAR() < c.horario[1]);

  if (hoyISO() > c.hasta) { log(`La campaña venció el ${c.hasta}: no hago nada.`); return; }
  if (enviar && !enHorario()) { log(`Fuera de horario (${horaAR()} hs, se manda de ${c.horario[0]} a ${c.horario[1]}).`); return; }

  const re = new RegExp(c.elegibles);
  const elegibles = (filas) => filas.filter((f) => re.test((f[c.col_estado] || '').trim()));

  if (!enviar) {
    const pend = elegibles(leerCSV(c).filas);
    log(`${id}: ${pend.length} pendientes, cupo ${limite}.`);
    pend.slice(0, limite).forEach((f, i) => log(`  ${i + 1}. ${f[c.col_nombre]} (${f[c.col_telefono]})`));
    log(pend.length ? 'Simulacro: no mandé nada. Para mandar: --send' : 'No queda nadie: campaña terminada.');
    return;
  }

  fs.mkdirSync(DATOS, { recursive: true });
  const lock = path.join(DATOS, `${id}.lock`);
  if (fs.existsSync(lock) && Date.now() - fs.statSync(lock).mtimeMs > 3 * 3600e3) fs.unlinkSync(lock); // lock viejo de una corrida muerta
  try { fs.writeFileSync(lock, String(process.pid), { flag: 'wx' }); }
  catch { log('Ya hay una tanda corriendo (lock): salgo.'); return; }

  let cliente;
  try {
    const archivoEstado = path.join(DATOS, `${id}.json`);
    const estado = fs.existsSync(archivoEstado) ? JSON.parse(fs.readFileSync(archivoEstado, 'utf8')) : {};
    const hechosHoy = estado.fecha === hoyISO() ? estado.enviados : 0;
    const cupo = forzar ? limite : limite - hechosHoy;
    if (cupo <= 0) { log(`Hoy ya salieron ${hechosHoy}: tope del día cumplido.`); return; }

    const pendientes = elegibles(leerCSV(c).filas);
    log(`${id}: ${pendientes.length} pendientes, cupo de hoy ${cupo}.`);
    if (!pendientes.length) { notificar(`${id}: terminada, no queda nadie.`); return; }

    cliente = nuevoCliente();
    await conectar(cliente, { setup: false });
    log(`Conectado como ${cliente.info.wid.user}.`);
    await dormir(10000); // recién conectado, getNumberId puede dar null en falso

    let enviados = 0, salteados = 0, erroresSeguidos = 0;
    const vistos = new Set();
    for (const f of pendientes) {
      if (enviados >= cupo) break;
      if (!enHorario()) { log('Se pasó el horario: freno y sigo mañana.'); break; }
      const nombre = f[c.col_nombre], tel = f[c.col_telefono], num = digitos(tel);
      if (!num || vistos.has(num)) { marcar(c, tel, `SALTEADO ${hoyCorto()} (sin número o repetido)`); salteados++; continue; }
      vistos.add(num);
      try {
        const wid = await cliente.getNumberId(num);
        if (!wid) { marcar(c, tel, `SIN WHATSAPP? ${hoyCorto()}`); salteados++; log(`  - ${nombre}: sin WhatsApp`); erroresSeguidos = 0; continue; }
        const chat = await cliente.getChatById(wid._serialized);
        const msgs = await chat.fetchMessages({ limit: 300 });
        const nuestros = msgs.filter((m) => m.fromMe);
        log(`  · ${nombre}: ${msgs.length} mensajes en el historial (${nuestros.length} nuestros)`);
        if (msgs.some((m) => !m.fromMe && BAJA.test(m.body || ''))) { marcar(c, tel, `respondio BAJA (visto ${hoyCorto()})`); salteados++; log(`  - ${nombre}: dijo BAJA, salteado`); erroresSeguidos = 0; continue; }
        if (nuestros.some((m) => (m.body || '').includes(c.huella))) { marcar(c, tel, `${c.marca.replace('{fecha}', hoyCorto())} (ya lo tenía)`); salteados++; erroresSeguidos = 0; continue; }
        if (!nuestros.length) { marcar(c, tel, `REVISAR ${hoyCorto()} (historial sin cargar, no sé si dijo BAJA)`); salteados++; log(`  - ${nombre}: historial vacío, NO mando`); erroresSeguidos = 0; continue; }

        if (enviados > 0) await dormir((c.espera_seg[0] + Math.random() * (c.espera_seg[1] - c.espera_seg[0])) * 1000);
        if (!enHorario()) { log('Se pasó el horario: freno y sigo mañana.'); break; }
        const enviando = `ENVIANDO ${hoyCorto()}`;
        marcar(c, tel, enviando);
        enviados++; // cuenta desde que se intenta: un envío dudoso igual consume cupo
        fs.writeFileSync(archivoEstado, JSON.stringify({ fecha: hoyISO(), enviados: hechosHoy + enviados }));
        const m = await cliente.sendMessage(wid._serialized, c.texto, { linkPreview: true });
        if (!m?.id?.id) throw new Error('el envío no devolvió id de mensaje (puede haber salido: queda ENVIANDO)');
        marcar(c, tel, c.marca.replace('{fecha}', hoyCorto()), enviando);
        erroresSeguidos = 0;
        log(`  ✓ ${nombre} (${enviados}/${cupo})`);
      } catch (e) {
        erroresSeguidos++;
        log(`  ✗ ${nombre}: ${e.message}`);
        try { if (!/ENVIANDO/.test(e.message)) marcar(c, tel, `ERROR ${hoyCorto()}`); } catch {}
        if (erroresSeguidos >= 3) throw new Error(`3 errores seguidos, freno la tanda. Último: ${e.message}`);
      }
    }
    const quedan = elegibles(leerCSV(c).filas).length;
    notificar(`${id}: ${enviados} enviados, ${salteados} salteados, quedan ${quedan}.`);
  } finally {
    if (cliente) { await dormir(4000); await cliente.destroy().catch(() => {}); }
    try { fs.unlinkSync(lock); } catch {}
  }
}

try {
  if (flag('--setup')) await setup();
  else if (valor('--campana')) await tanda(valor('--campana'));
  else { console.error('Uso: node tanda.mjs --setup | --campana <id> [--send] [--forzar] [--limite N]'); process.exit(64); }
  process.exit(0);
} catch (e) {
  console.error('ERROR:', e.message);
  process.exit(e.codigo || 1);
}
