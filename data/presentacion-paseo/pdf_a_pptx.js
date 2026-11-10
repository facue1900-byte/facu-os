// El PowerPoint de la general: una imagen por lámina, sacada del PDF, para que se vea idéntico con la tipografía del Paseo.
// Uso: node pdf_a_pptx.js <carpeta con 01.jpg, 02.jpg...> <salida.pptx>. No es editable: el texto se cambia en deck.template.html.
const pptxgen = require('pptxgenjs'), fs = require('fs'), path = require('path');
const [dir, out] = process.argv.slice(2);
const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';
p.title = 'Paseo Nordelta · Presentación general';
p.author = 'Paseo Nordelta';
fs.readdirSync(dir).filter(f => f.endsWith('.jpg')).sort().forEach((f, i) => {
  const s = p.addSlide();
  s.addImage({ path: path.join(dir, f), x: 0, y: 0, w: 13.333, h: 7.5, objectName: 'Lámina ' + (i + 1), altText: 'Lámina ' + (i + 1) + ' de la presentación de Paseo Nordelta' });
});
p.writeFile({ fileName: out }).then(() => console.log(out));
