"""Imágenes de los ppt del Paseo: fotos 16:9, velos y ubicadores sobre el plano etapa2 (plano vigente)."""
import fitz,json,pathlib
from PIL import Image,ImageDraw,ImageOps
B=pathlib.Path(__file__).parent; A=B/'a'; P=B.parent/'img'; F=B.parent.parent/'fichas-locales'/'img'
PLANOS="/Users/Facu/Desktop/Paseo Nordelta/Documentación/Obra /PLANOS/"
GROUND=(23,22,20); COR=(217,119,66)
def cover(src,name,w=1600,h=900,focus=.5):
    im=Image.open(src).convert('RGB'); r=w/h; W,H=im.size
    if W/H>r: nw=int(H*r); x=int((W-nw)*focus); im=im.crop((x,0,x+nw,H))
    else: nh=int(W/r); y=int((H-nh)*focus); im=im.crop((0,y,W,y+nh))
    im.resize((w,h),Image.LANCZOS).save(A/f'{name}.jpg',quality=86)
cover(P/'plaza-carteles.jpg','plaza')
for n in ['acceso','cafe-exterior','peak-sendero','render-galeria-dia','servicios']: cover(P/f'{n}.jpg',n)
for n in ['jaula','senderos','galeria']: cover(P/f'{n}.jpg',n,900,675)
cover(F/'render-galeria-noche.jpg','galeria-noche'); cover(F/'cafe-sendero.jpg','cafe-sendero')
a=Image.open(P/'aerea-wellness.jpg').convert('RGB'); a.thumbnail((1600,1600)); a.save(A/'aerea.jpg',quality=86)
W,H=a.size; a.crop((int(W*.55),int(H*.5),W,int(H*.5+W*.45*9/16))).resize((1600,900),Image.LANCZOS).save(A/'market-aereo.jpg',quality=86)
Image.open(P/'logo.png').save(A/'logo.png')
# velo: transparente arriba, negro cálido abajo
v=Image.new('RGBA',(16,450))
for y in range(450):
    t=max(0,(y-140)/310); al=int(245*min(1,t**1.15))
    for x in range(16): v.putpixel((x,y),(*GROUND,al))
v.save(A/'velo.png')
t=Image.new('RGBA',(16,450))
for y in range(450):
    al=int(170*max(0,1-y/130))
    for x in range(16): t.putpixel((x,y),(*GROUND,al))
t.save(A/'velo-top.png')
# plano etapa2 en oscuro
d=fitz.open(PLANOS+'Paseo Nordelta - etapa2.pdf'); S=3
z=S*1900/842
px=d[0].get_pixmap(matrix=fitz.Matrix(z,z),alpha=False)
im=Image.frombytes('RGB',(px.width,px.height),px.samples).convert('L')
im=ImageOps.invert(im).point(lambda v:int(235*(v/255)**.55))
im=ImageOps.colorize(im,GROUND,(242,236,225)).convert('RGBA')
LOC={'market':[[(133,664),(214,664),(214,808),(133,808)]],
 'tira':[[(133,808),(214,808),(214,915),(133,915)],[(133,949),(214,949),(214,1127),(133,1127)]],
 'pizzeria':[[(838,948),(872,948),(945,1025),(838,1025)]],
 'cafe':[[(433,658),(605,658),(605,790),(433,790)]]}
for k,pols in LOC.items():
    o=im.copy(); l=Image.new('RGBA',o.size,(0,0,0,0)); dr=ImageDraw.Draw(l)
    for pol in pols:
        q=[(x*S,y*S) for x,y in pol]; dr.polygon(q,fill=(*COR,150)); dr.line(q+[q[0]],fill=(*COR,255),width=8)
    o=Image.alpha_composite(o,l).convert('RGB')
    cx0,cy0,cx1,cy1=10*S,480*S,1150*S,1620*S
    o.crop((cx0,cy0,cx1,cy1)).resize((1400,1400),Image.LANCZOS).save(A/f'ubi-{k}.png',optimize=True)
# planta del café (Max) en oscuro
d=fitz.open("/Users/Facu/Desktop/Paseo Nordelta/Documentación/Obra /Paseo Nordelta Cafe.pdf")
px=d[0].get_pixmap(matrix=fitz.Matrix(2.2,2.2),alpha=False)
c=Image.frombytes('RGB',(px.width,px.height),px.samples).convert('L')
c=ImageOps.invert(c).point(lambda v:min(255,int(v*1.0))); c=ImageOps.colorize(c,GROUND,(242,236,225)); W2,H2=c.size; c.crop((int(W2*.2),int(H2*.02),int(W2*.82),int(H2*.9))).save(A/'plano-cafe.png')
print(json.dumps({'aerea':a.size})); json.dump({'aerea':a.size},open(A/'sizes.json','w'))
