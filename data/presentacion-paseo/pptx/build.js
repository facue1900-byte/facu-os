// Los 5 ppt del Paseo: general + café, pizzería, Market y tira. Los números salen de LOCALES; se edita acá y se recompila.
const pptxgen=require('pptxgenjs'), path=require('path'), fs=require('fs');
const {applyTheme}=require(process.env.PPTX_SKILL+'/scripts/apply_theme.js');
const A=f=>path.join(__dirname,'a',f), SAL=process.argv[2];
const THEME={name:'Paseo Nordelta',headFontFace:'Arial',bodyFontFace:'Arial',colors:{dk1:'171614',lt1:'F2ECE1',dk2:'26231F',lt2:'C4BCAE',accent1:'C4622D',accent2:'D97742',accent3:'8A8276',accent4:'3A362F',accent5:'F2ECE1',accent6:'C4BCAE',hlink:'D97742',folHlink:'C4622D'}};
const MES='Noviembre 2026';
const LOCALES={
 cafe:{archivo:'Cafeteria',nombre:'Cafetería',titulo:'La cafetería\ndel paseo',bajada:'130 m² cubiertos sobre el sendero principal, con galería semicubierta y deck.',chip:'DISPONIBLE HOY',foto:'cafe-exterior.jpg',ilu:true,
  stats:[['130','m²','Cubiertos'],['52','m²','Galería semicubierta'],['39','m²','Deck descubierto']],
  tituloLocal:'130 m² cubiertos y 13 m de frente',plano:'plano-cafe.png',planoCap:'Planta preliminar · Arq. Max Elewaut',
  puntos:['Salón de 9,25 × 9,60 m en una sola pieza','Dos ambientes de apoyo sobre el lateral','Galería de 13 × 4 m para mesas afuera','Deck de 13 × 3 m como ampliación posible'],
  ubi:'ubi-cafe.png',tituloUbi:'Entre el salón y la plaza central',textoUbi:'Sobre el sendero principal, el eje que conecta el acceso con la plaza. Es el camino de quienes vienen a entrenar, a jugar al fútbol o a comer.',
  fotos:[['cafe-exterior.jpg','Imagen ilustrativa · el local con su galería y el deck'],['cafe-sendero.jpg','Render del proyecto · el sendero principal']],
  alquiler:'$3.500.000',expensas:'$1.050.000',entrega:'Hoy',entregaNota:'En obra en gris. Libre y entregable de inmediato.'},
 pizzeria:{archivo:'Pizzeria',nombre:'Pizzería',titulo:'La pizzería\nde la galería nueva',bajada:'47,9 m² a estrenar en la galería gastronómica, con cocina prevista en el proyecto.',chip:'DISPONIBLE · ENERO 2027 APROX.',foto:'render-galeria-dia.jpg',ilu:true,
  stats:[['47,9','m²','A estrenar'],['1','','Cocina prevista en el proyecto'],['3','','Locales gastronómicos en la galería']],
  tituloLocal:'47,9 m² con cocina propia',fotoLocal:'galeria-noche.jpg',planoCap:'Imagen ilustrativa · la galería de noche',
  puntos:['Local a estrenar, se entrega en obra en gris','Cocina prevista desde el proyecto','Frente vidriado sobre la galería semicubierta','Al lado de Fabric y la heladería Schock BA'],
  ubi:'ubi-pizzeria.png',tituloUbi:'En la galería gastronómica nueva',textoUbi:'Junto a la cancha y a la plaza del sector deportivo, en un bloque de tres locales gastronómicos con la vereda como parte del salón.',
  alquiler:'$2.500.000',expensas:'$780.000',entrega:'Enero 2027',entregaNota:'Fecha aproximada. Se entrega en obra en gris.'},
 market:{archivo:'Market',nombre:'Market',titulo:'El Market\ndel paseo',bajada:'Unos 119 m² junto al acceso principal, a la cabeza de la tira de locales de servicios.',chip:'EN OBRA · JULIO 2027 APROX.',foto:'acceso.jpg',ilu:true,
  stats:[['~119','m²','Superficie aproximada'],['~13','m','De frente sobre el paseo'],['9','m','De fondo']],
  tituloLocal:'Una planta libre de ~119 m²',esquema:'market',planoCap:'Esquema sobre el plano de etapa 2 · medidas aproximadas',
  puntos:['Equivale a 4 módulos de 29,7 m²','Primer local al entrar desde la avenida','Pegado a 8 locales de servicios','Pensado para minimercado de cercanía'],
  ubi:'ubi-market.png',tituloUbi:'Sobre el acceso principal',textoUbi:'Junto al acceso desde Av. de los Colegios, de paso para quienes van a la cancha, al Wellness Center o a los locales.',
  fotos:[['acceso.jpg','Imagen ilustrativa · el acceso al paseo'],['market-aereo.jpg','Imagen ilustrativa · vista aérea del sector']],
  alquiler:'$4.000.000',expensas:'$800.000',entrega:'Julio 2027',entregaNota:'Fecha aproximada. Se entrega en obra en gris.'},
 tira:{archivo:'Locales de servicios',nombre:'Locales de servicios',titulo:'Ocho locales\nde servicios',bajada:'Locales de 29,7 m² en el paseo, junto al Market, para rubros de todos los días.',chip:'EN OBRA · JULIO 2027 APROX.',foto:'servicios.jpg',ilu:true,
  stats:[['8','','Locales'],['29,7','m²','Cada uno'],['3,30 × 9','m','Frente por fondo']],
  tituloLocal:'Ocho módulos de 29,7 m²',esquema:'tira',planoCap:'Esquema sobre el plano de etapa 2 · medidas aproximadas',
  puntos:['Farmacia, barbería, estética, librería, kiosco','Sin necesidad de cocina ni obra pesada','Frente vidriado hacia el paseo','Al lado del Market'],
  ubi:'ubi-tira.png',tituloUbi:'Sobre el lateral de la avenida',textoUbi:'Miran hacia el paseo y la plaza, entre el Market y el Wellness Center. Es el recorrido de quienes llegan a entrenar todas las semanas.',
  alquiler:'$2.000.000',alqNota:'Por local, por mes, en pesos',expensas:'$780.000',expNota:'Por local. ',entrega:'Julio 2027',entregaNota:'Fecha aproximada. Se entrega en obra en gris.'},
};
function nuevo(titulo){
 const p=new pptxgen(); p.layout='LAYOUT_WIDE'; p.title=titulo; p.author='Paseo Nordelta'; p.company='MAHNI MANAGEMENT S.A.';
 p.theme={headFontFace:THEME.headFontFace,bodyFontFace:THEME.bodyFontFace};
 const C=p.SchemeColor;
 const foot=[{text:{text:'PASEO NORDELTA',options:{x:.6,y:7.02,w:4,h:.3,fontSize:10,color:C.accent3,charSpacing:2,margin:0}}}];
 p.defineSlideMaster({title:'CONTENIDO',background:{color:'171614'},objects:[...foot,
  {placeholder:{options:{name:'title',type:'title',x:.6,y:.45,w:12.1,h:1.05,fontSize:36,color:C.background1,align:'left',valign:'top',margin:0},text:''}}],
  slideNumber:{x:12.1,y:7.0,w:.6,h:.3,fontSize:10,color:C.accent3,align:'right'}});
 p.defineSlideMaster({title:'FOTO',background:{color:'171614'},objects:[
  {placeholder:{options:{name:'title',type:'title',x:.6,y:5.05,w:10.5,h:.8,fontSize:38,color:C.background1,align:'left',valign:'bottom',margin:0},text:''}}]});
 return p;
}
function foto(p,s,img,titulo,texto,ilu=true){const C=p.SchemeColor;
 s.addImage({path:A(img),x:0,y:0,w:13.333,h:7.5,objectName:'Foto',altText:titulo});
 s.addImage({path:A('velo.png'),x:0,y:0,w:13.333,h:7.5,objectName:'Velo',altText:''});
 s.addText(titulo,{placeholder:'title'});
 s.addText(texto,{x:.6,y:5.92,w:9.2,h:.8,fontSize:17,color:C.background1,margin:0,valign:'top',isTextBox:true,objectName:'Texto'});
 if(ilu)s.addText('IMAGEN ILUSTRATIVA',{x:.6,y:6.82,w:5,h:.25,fontSize:10,color:C.background2,charSpacing:2,margin:0,isTextBox:true,objectName:'Aviso'});
}
function card(p,s,x,y,w,h){const C=p.SchemeColor;s.addShape(p.shapes.RECTANGLE,{x,y,w,h,fill:{color:C.text2},line:{color:C.accent4,width:.75},objectName:'Tarjeta'});}
function stat(p,s,x,y,w,h,n,u,l){const C=p.SchemeColor;card(p,s,x,y,w,h);
 s.addText([{text:n,options:{fontSize:n.length>=7?24:(n.length>=4&&u?30:40),color:C.background1}},{text:u?' '+u:'',options:{fontSize:15,color:C.background2}}],{x:x+.22,y:y+.2,w:w-.44,h:.8,margin:0,valign:'middle',isTextBox:true,objectName:'Número'});
 s.addText(l,{x:x+.22,y:y+1.02,w:w-.44,h:h-1.15,fontSize:14,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Detalle'});}
function esquema(p,s,tipo,x,y,w,h){const C=p.SchemeColor;
 const box=(bx,by,bw,bh,t,on)=>s.addText(t,{shape:p.shapes.RECTANGLE,x:bx,y:by,w:bw,h:bh,fill:{color:on?C.accent1:C.text2},line:{color:on?C.accent2:C.accent3,width:1},fontSize:13,color:C.background1,align:'center',valign:'middle',margin:0,objectName:'Módulo'});
 // tira real: 4 bloques Market + 3 locales, separación, 5 locales. Módulo 3,30 m; separación 7,76 m.
 const u=w/(12*3.3+7.76), bh=Math.min(h-1.1,9*u*1.0+.9), y0=y+.55; let cx=x;
 const on=tipo==='market';
 box(cx,y0,13.2*u,bh,'Market\n~119 m²',on); cx+=13.2*u;
 for(let i=0;i<3;i++){box(cx,y0,3.3*u,bh,String(i+1),!on);cx+=3.3*u;}
 s.addText('Paso',{x:cx,y:y0,w:7.76*u,h:bh,fontSize:12,color:C.accent3,align:'center',valign:'middle',margin:0,isTextBox:true,objectName:'Paso'}); cx+=7.76*u;
 for(let i=3;i<8;i++){box(cx,y0,3.3*u,bh,String(i+1),!on);cx+=3.3*u;}
 s.addText('AV. DE LOS COLEGIOS',{x,y:y,w,h:.35,fontSize:11,color:C.accent3,charSpacing:2,align:'center',margin:0,isTextBox:true,objectName:'Avenida'});
 s.addText('EL PASEO · FRENTE DE LOS LOCALES',{x,y:y0+bh+.12,w,h:.35,fontSize:11,color:C.accent2,charSpacing:2,align:'center',margin:0,isTextBox:true,objectName:'Frente'});
}
function contacto(p,s,y){const C=p.SchemeColor;
 const d=[['DIRECCIÓN','Av. de los Colegios 160, Nordelta'],['EMAIL','paseonordelta@gmail.com'],['INSTAGRAM','@paseonordelta'],['WEB','paseonordelta.com']],W=[4.3,3.5,2.3,2];let x=.6;
 d.forEach(([k,v],i)=>{s.addText(k,{x,y,w:W[i],h:.25,fontSize:10,color:C.accent3,charSpacing:2,margin:0,isTextBox:true,objectName:'Contacto'});s.addText(v,{x,y:y+.27,w:W[i],h:.32,fontSize:14,color:C.background1,margin:0,isTextBox:true,objectName:'Contacto'});x+=W[i];});}
async function ficha(k){const L=LOCALES[k],p=nuevo('Paseo Nordelta · '+L.nombre),C=p.SchemeColor;
 // 1 portada
 let s=p.addSlide({masterName:'FOTO'});
 s.addImage({path:A(L.foto),x:0,y:0,w:13.333,h:7.5,objectName:'Foto',altText:L.nombre});
 s.addImage({path:A('velo.png'),x:0,y:0,w:13.333,h:7.5,objectName:'Velo',altText:''});
 s.addImage({path:A('velo-top.png'),x:0,y:0,w:13.333,h:7.5,objectName:'Velo superior',altText:''});
 s.addImage({path:A('logo.png'),x:.6,y:.5,w:2.6,h:2.6*imgRatio('logo.png'),objectName:'Logo',altText:'Paseo Nordelta'});
 s.addText(L.chip,{shape:p.shapes.ROUNDED_RECTANGLE,rectRadius:.15,x:.6,y:4.72,w:Math.max(2.3,.125*L.chip.length+.5),h:.38,fill:{color:C.accent1},color:C.background1,fontSize:11,bold:true,charSpacing:1,align:'center',valign:'middle',margin:0,objectName:'Estado'});
 s.addText(L.titulo.replace('\n',' '),{placeholder:'title',fontSize:40});
 s.addText(L.bajada,{x:.6,y:5.92,w:9.2,h:.8,fontSize:17,color:C.background1,margin:0,valign:'top',isTextBox:true,objectName:'Bajada'});
 s.addText('IMAGEN ILUSTRATIVA',{x:.6,y:6.82,w:5,h:.25,fontSize:10,color:C.background2,charSpacing:2,margin:0,isTextBox:true,objectName:'Aviso'});
 // 2 el local
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText(L.tituloLocal,{placeholder:'title'});
 const sw=1.92; L.stats.forEach((d,i)=>stat(p,s,.6+i*(sw+.12),1.55,sw,1.95,d[0],d[1],d[2]));
 s.addText(L.puntos.map((t,i)=>({text:t,options:{bullet:{code:'25CF',color:'D97742'},breakLine:i<L.puntos.length-1}})),{x:.6,y:3.8,w:6.0,h:2.7,fontSize:16,color:C.background1,paraSpaceAfter:9,margin:0,valign:'top',isTextBox:true,objectName:'Puntos'});
 const rx=6.95,ry=1.55,rw=5.78,rh=4.75;
 if(L.plano){const r=imgRatio(L.plano),ih=Math.min(rh,rw*r),iw=ih/r; s.addImage({path:A(L.plano),x:rx+(rw-iw)/2,y:ry+(rh-ih)/2,w:iw,h:ih,objectName:'Plano',altText:L.planoCap});}
 else if(L.fotoLocal){const iw=rw,ih=rw*9/16;s.addImage({path:A(L.fotoLocal),x:rx,y:ry+.5,w:iw,h:ih,objectName:'Foto',altText:L.planoCap});}
 else {card(p,s,rx,ry,rw,rh);esquema(p,s,L.esquema,rx+.2,ry+.5,rw-.4,rh-.8);}
 s.addText(L.planoCap,{x:rx,y:L.fotoLocal?ry+.5+rw*9/16+.1:6.38,w:rw,h:.3,fontSize:11,color:C.background2,margin:0,isTextBox:true,objectName:'Pie'});
 // 3 dónde
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText(L.tituloUbi,{placeholder:'title'});
 s.addImage({path:A(L.ubi),x:.6,y:1.45,w:5.4,h:5.4,objectName:'Ubicación',altText:'Plano del paseo con '+L.nombre+' marcado'});
 s.addText('ACÁ ESTÁ',{x:6.45,y:1.55,w:6,h:.3,fontSize:12,color:C.accent2,charSpacing:3,margin:0,isTextBox:true,objectName:'Etiqueta'});
 s.addText(L.nombre,{x:6.45,y:1.9,w:6.2,h:.7,fontSize:28,color:C.background1,margin:0,isTextBox:true,objectName:'Local'});
 s.addText(L.textoUbi,{x:6.45,y:2.7,w:6.2,h:1.5,fontSize:17,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Texto'});
 s.addText('A su alrededor',{x:6.45,y:4.35,w:6.2,h:.35,fontSize:15,bold:true,color:C.background1,margin:0,isTextBox:true,objectName:'Subtítulo'});
 s.addText(['Cancha de fútbol y escuelas','BIGG, centro de entrenamiento','Wellness Center de 750 m², en obra','Plaza central y gastronomía'].map((t,i)=>({text:t,options:{bullet:{code:'25CF',color:'D97742'},breakLine:i<3}})),{x:6.45,y:4.75,w:6.2,h:1.9,fontSize:15,color:C.background2,paraSpaceAfter:6,margin:0,valign:'top',isTextBox:true,objectName:'Entorno'});
 // 4 imágenes
 if(L.fotos){s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Cómo se imagina el sector',{placeholder:'title'});
  L.fotos.forEach(([f,c],i)=>{const x=.6+i*6.17,w=5.95,h=w*9/16;s.addImage({path:A(f),x,y:1.6,w,h,objectName:'Foto',altText:c});s.addText(c,{x,y:1.6+h+.12,w,h:.5,fontSize:12,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Pie'});});}
 // 5 condiciones
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Las condiciones',{placeholder:'title'});
 const cs=[['ALQUILER',L.alquiler,L.alqNota||'Por mes, en pesos','Ajusta por IPC, trimestralmente.'],['EXPENSAS',L.expensas+' aprox.',(L.expNota||'')+'Por mes, en pesos','Se liquidan según el gasto real del predio.'],['ENTREGA',L.entrega+(L.entrega==='Hoy'?'':' aprox.'),'Obra en gris',L.entregaNota]];
 const w3=3.9; cs.forEach(([k,v,a,b],i)=>{const x=.6+i*(w3+.2);card(p,s,x,1.55,w3,3.05);
  s.addText(k,{x:x+.28,y:1.8,w:w3-.56,h:.3,fontSize:12,color:C.accent2,charSpacing:3,margin:0,isTextBox:true,objectName:'Concepto'});
  s.addText(v,{x:x+.28,y:2.18,w:w3-.56,h:.85,fontSize:v.length>16?24:29,color:C.background1,margin:0,valign:'middle',isTextBox:true,objectName:'Valor'});
  s.addText(a,{x:x+.28,y:3.08,w:w3-.56,h:.35,fontSize:14,bold:true,color:C.background1,margin:0,isTextBox:true,objectName:'Nota'});
  s.addText(b,{x:x+.28,y:3.45,w:w3-.56,h:.95,fontSize:14,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Detalle'});});
 s.addText('Valores de '+MES.toLowerCase()+'. Medidas y plazos aproximados, se verifican en obra. El local se entrega en gris: la terminación la define el locatario.',{x:.6,y:4.85,w:12.1,h:.6,fontSize:14,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Aclaración'});
 contacto(p,s,5.75);
 const f=path.join(SAL,'Paseo Nordelta - '+L.archivo+'.pptx'); await p.writeFile({fileName:f}); await applyTheme(f,THEME); console.log(f);
}
const sharpless=require('child_process');
function imgRatio(f){const b=fs.readFileSync(A(f));if(f.endsWith('.png'))return b.readUInt32BE(20)/b.readUInt32BE(16);let i=2;while(i<b.length){const m=b[i+1],l=b.readUInt16BE(i+2);if(m>=0xC0&&m<=0xC3)return b.readUInt16BE(i+5)/b.readUInt16BE(i+7);i+=2+l;}throw new Error('sin tamaño '+f);}
async function general(){const p=nuevo('Paseo Nordelta · Presentación general'),C=p.SchemeColor;let s;
 s=p.addSlide({masterName:'FOTO'}); s.addImage({path:A('acceso.jpg'),x:0,y:0,w:13.333,h:7.5,objectName:'Foto',altText:'Acceso a Paseo Nordelta'}); s.addImage({path:A('velo.png'),x:0,y:0,w:13.333,h:7.5,objectName:'Velo',altText:''});
 s.addImage({path:A('velo-top.png'),x:0,y:0,w:13.333,h:7.5,objectName:'Velo superior',altText:''});
 s.addImage({path:A('logo.png'),x:.6,y:.5,w:3,h:3*imgRatio('logo.png'),objectName:'Logo',altText:'Paseo Nordelta'});
 s.addText('Un plan en sí mismo',{placeholder:'title',fontSize:44}); s.addText('Av. de los Colegios 160, Nordelta · Gastronomía, deporte, wellness y eventos',{x:.6,y:5.92,w:11,h:.45,fontSize:17,color:C.background1,margin:0,isTextBox:true,objectName:'Bajada'});
 s.addText('PRESENTACIÓN PARA MARCAS · '+MES.toUpperCase()+' · IMÁGENES ILUSTRATIVAS',{x:.6,y:6.82,w:10,h:.25,fontSize:10,color:C.background2,charSpacing:2,margin:0,isTextBox:true,objectName:'Aviso'});
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Un paseo al aire libre que ya está funcionando',{placeholder:'title'});
 s.addText('Paseo Nordelta no abre: se transforma. Sobre un predio que ya recibe gente todos los días, con la cancha, las escuelas de fútbol, el gimnasio y la gastronomía en marcha, estamos construyendo el paseo comercial que le faltaba a esa circulación. Una marca no tiene que esperar a que el lugar se llene.',{x:.6,y:1.45,w:11.6,h:1.65,fontSize:19,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Texto'});
 [['9.800','m²','Superficie del predio'],['1','','Cancha de fútbol propia'],['3','','Locales gastronómicos nuevos, en obra'],['8','','Locales de servicios, en obra'],['1','','Market, en obra']].forEach((d,i)=>stat(p,s,.6+i*2.44,3.45,2.34,2.0,d[0],d[1],d[2]));
 s=p.addSlide({masterName:'FOTO'}); foto(p,s,'plaza.jpg','La Plaza Central','Gastronomía y heladería alrededor de la escultura de acero Corten. Acá se cruzan los que vienen a entrenar, los que traen a los chicos y los que vienen a comer.');
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Lo que ya está funcionando',{placeholder:'title'});
 [['Fabric','Gastronomía','Sushi, ~350 m² sobre la galería principal',1],['BIGG','Entrenamiento','Centro de entrenamiento sobre la plaza',1],['BOSS','Hamburguesería','Gastronomía rápida',1],['La Jaula','Fútbol','Torneos y alquiler de la cancha',1],['Escuelas de fútbol','Deporte infantil','Dos escuelitas durante la semana',1],['Peak One','Wellness','En obra: 750 m² de entrenamiento y recuperación',0],['Volta + Open 25','Heladería y kiosko','~115 m², se renueva con el proyecto',1],['Pole Position','Lavadero','Lavadero de autos dentro del predio',1],['Salón de eventos','Eventos','Eventos sociales, activaciones y música',1]].forEach((d,i)=>{const x=.6+(i%3)*4.07,y=1.35+Math.floor(i/3)*1.78;card(p,s,x,y,3.95,1.66);
  s.addShape(p.shapes.OVAL,{x:x+.22,y:y+.3,w:.13,h:.13,fill:{color:d[3]?C.accent2:C.text2},line:{color:C.accent2,width:1},objectName:'Estado'});
  s.addText(d[0],{x:x+.45,y:y+.17,w:3.3,h:.38,fontSize:17,bold:true,color:C.background1,margin:0,isTextBox:true,objectName:'Local'});
  s.addText(d[1],{x:x+.22,y:y+.57,w:3.5,h:.28,fontSize:12,color:C.accent2,margin:0,isTextBox:true,objectName:'Rubro'});
  s.addText(d[2],{x:x+.22,y:y+.86,w:3.55,h:.68,fontSize:14,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Detalle'});});
 s.addText('● Operativo, '+MES.toLowerCase()+'    ○ En obra',{x:6.5,y:7.0,w:5.4,h:.3,fontSize:11,color:C.background2,align:'right',margin:0,isTextBox:true,objectName:'Referencias'});
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Todo al aire libre',{placeholder:'title'});
 [['jaula.jpg','El sector deportivo: la gente llega por acá y se queda'],['senderos.jpg','Senderos, no pasillos: de un local al otro entre jacarandás'],['galeria.jpg','La galería gastronómica, con la vereda como parte del salón']].forEach(([f,c],i)=>{const x=.6+i*4.1,w=3.95,h=w*.75;s.addImage({path:A(f),x,y:1.55,w,h,objectName:'Foto',altText:c});s.addText(c,{x,y:1.55+h+.15,w,h:.9,fontSize:15,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Pie'});});
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Qué hay en cada sector',{placeholder:'title'});
 const sz=JSON.parse(fs.readFileSync(A('sizes.json'))).aerea,iw=6.3,ih=iw*sz[1]/sz[0],ix=.6,iy=1.75;
 s.addImage({path:A('aerea.jpg'),x:ix,y:iy,w:iw,h:ih,objectName:'Vista aérea',altText:'Vista aérea numerada del paseo'});
 const pins=[[47,17],[43,30],[78,19],[67,42],[47,41],[20,32],[86,65,1],[22,73],[36,55,1],[9,23,1],[57,92],[89,37,1]];
 pins.forEach(([a,b,l],i)=>s.addText(String(i+1),{shape:p.shapes.OVAL,x:ix+iw*a/100-.17,y:iy+ih*b/100-.17,w:.34,h:.34,fill:{color:l?C.background1:C.accent1},color:l?C.text1:C.background1,fontSize:10,bold:true,align:'center',valign:'middle',margin:0,objectName:'Pin '+(i+1)}));
 s.addText('Blanco: con espacio disponible',{x:ix,y:iy+ih+.12,w:iw,h:.3,fontSize:12,color:C.background2,margin:0,isTextBox:true,objectName:'Referencias'});
 const li=[['Cancha de fútbol','La Jaula y escuelas de fútbol'],['Patio deportivo','Deck, mesas y contenedores'],['Wellness Center','Peak One, 750 m². En obra'],['Plaza Central','La escultura de acero Corten'],['Fabric (próximamente restaurante Pata Negra)','Gastronomía'],['BIGG','Entrenamiento, sobre la plaza'],['Market','En obra. Buscando operador'],['Salón Multiespacios','Hoy funciona como salón de eventos'],['Café de especialidad','Disponible hoy'],['Los tres locales nuevos','En obra. Pizzería disponible'],['Acceso','Av. de los Colegios 160'],['8 locales de servicios','En obra. Por asignar']];
 li.forEach(([a,b],i)=>{const x=7.15+(i%2)*2.85,y=1.45+Math.floor(i/2)*.87;s.addText(String(i+1),{x,y:y+.02,w:.3,h:.26,fontSize:11,bold:true,color:C.accent2,margin:0,isTextBox:true,objectName:'Número'});
  s.addText([{text:a,options:{bold:true,color:C.background1,breakLine:true,fontSize:13}},{text:b,options:{color:C.background2,fontSize:12}}],{x:x+.3,y,w:2.45,h:.82,margin:0,valign:'top',isTextBox:true,objectName:'Sector'});});
 s=p.addSlide({masterName:'FOTO'}); foto(p,s,'cafe-exterior.jpg','La cafetería, disponible hoy','130 m² cubiertos, 52 m² de galería semicubierta y 39 m² de deck, sobre el sendero principal.');
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Lo que se viene',{placeholder:'title'});
 [['HOY','Cafetería','Disponible, en obra en gris y con entrega inmediata'],['EN OBRA','Wellness Center','Peak One: 750 m² y patio propio para entrenar al aire libre'],['ENERO 2027 APROX.','La galería nueva','Tres locales gastronómicos: Fabric, Schock BA y la pizzería, disponible'],['JULIO 2027 APROX.','Market','Junto al acceso principal, buscando operador'],['JULIO 2027 APROX.','8 locales de servicios','Para rubros que no necesitan cocina ni obra pesada']].forEach((d,i)=>{const y=1.5+i*1.04;card(p,s,.6,y,12.1,.92);
  s.addText(d[0],{x:.85,y,w:2.4,h:.92,fontSize:12,bold:true,color:C.accent2,margin:0,valign:'middle',isTextBox:true,objectName:'Fecha'});
  s.addText(d[1],{x:3.3,y,w:3,h:.92,fontSize:18,color:C.background1,margin:0,valign:'middle',isTextBox:true,objectName:'Qué'});
  s.addText(d[2],{x:6.4,y,w:6.1,h:.92,fontSize:14,color:C.background2,margin:0,valign:'middle',isTextBox:true,objectName:'Detalle'});});
 s=p.addSlide({masterName:'FOTO'}); foto(p,s,'peak-sendero.jpg','El Wellness Center','750 m² cerrados y un patio de entrenamiento al aire libre. Otro motivo para venir al paseo todas las semanas.');
 s=p.addSlide({masterName:'FOTO'}); foto(p,s,'render-galeria-dia.jpg','La galería nueva','Tres locales gastronómicos de 48, 88 y 124 m². Fabric y Schock BA ya están; la pizzería de 48 m² sigue disponible.');
 s=p.addSlide({masterName:'FOTO'}); foto(p,s,'servicios.jpg','Ocho locales de servicios y un Market','En obra, de 30 m² cada local: farmacia, barbería, estética, librería, kiosco. Todavía por asignar.');
 s=p.addSlide({masterName:'CONTENIDO'}); s.addText('Por qué estar acá',{placeholder:'title'});
 [['Público que ya circula','La cancha, las escuelas y el gimnasio traen gente todos los días, no sólo el fin de semana.'],['Un flujo, no una vidriera','Quien viene por una cosa se cruza con todas las demás.'],['Más que un alquiler','Local, presencia de marca y activaciones en los eventos del paseo.'],['Entrar mientras crece','Las mejores ubicaciones se definen ahora.']].forEach(([a,b],i)=>{const x=.6+i*3.05;card(p,s,x,1.5,2.95,3.2);s.addText(a,{x:x+.22,y:1.72,w:2.5,h:.85,fontSize:18,bold:true,color:C.background1,margin:0,valign:'top',isTextBox:true,objectName:'Argumento'});s.addText(b,{x:x+.22,y:2.62,w:2.5,h:1.95,fontSize:15,color:C.background2,margin:0,valign:'top',isTextBox:true,objectName:'Detalle'});});
 contacto(p,s,5.2); s.addText('Renders e imágenes ilustrativas. Medidas y plazos aproximados, sujetos a verificación en obra.',{x:.6,y:6.2,w:12,h:.3,fontSize:12,color:C.background2,margin:0,isTextBox:true,objectName:'Aclaración'});
 const f=path.join(SAL,'Paseo Nordelta - General.pptx'); await p.writeFile({fileName:f}); await applyTheme(f,THEME); console.log(f);
}
(async()=>{await general();for(const k of Object.keys(LOCALES))await ficha(k);})().catch(e=>{console.error(e);process.exit(1)});
