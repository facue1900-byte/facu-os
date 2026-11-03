"""Cambia los carteles del render de la plaza: KIOSKO → FABRIC, HELADERIA → SCHOCK BA. Parte de img/plaza.jpg, que no se toca."""
import pathlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
B=pathlib.Path(__file__).parent.parent/'img'
im=Image.open(B/'plaza.jpg').convert('RGB'); a=np.array(im).astype(float)
X0,Y0,K=1178,517,646/1600
def src(x,y): return int(X0+x*K),int(Y0+y*K)
PAN=[((212,112),(494,182)),((888,112),(1332,182))]   # paneles en coordenadas del recorte
for (p0,p1) in PAN:
    x0,y0=src(*p0); x1,y1=src(*p1); r=a[y0:y1,x0:x1]
    lum=r.mean(2); sat=r.max(2)-r.min(2)
    base=np.median(lum)
    m=(lum>base+22)&(sat<48)
    # dilatar la máscara dos píxeles
    for _ in range(2):
        n=m.copy(); n[1:]|=m[:-1]; n[:-1]|=m[1:]; n[:,1:]|=m[:,:-1]; n[:,:-1]|=m[:,1:]; m=n
    print('panel',x0,y0,x1,y1,'base',round(base),'px máscara',int(m.sum()))
    for y in range(r.shape[0]):
        xs=np.where(~m[y])[0]
        if len(xs)<2: continue
        for c in range(3): r[y,:,c]=np.interp(np.arange(r.shape[1]),xs,r[y,xs,c])
    a[y0:y1,x0:x1]=r
out=Image.fromarray(a.astype('uint8'))
S=4; F='/System/Library/Fonts/HelveticaNeue.ttc'
def rotulo(t,cx,cy,alto):
    w,h=out.size; l=Image.new('L',(w*S,h*S),0); d=ImageDraw.Draw(l)
    f=ImageFont.truetype(F,int(alto*S/0.72),index=0)
    b=d.textbbox((0,0),t,font=f); x=cx*S-(b[2]-b[0])/2-b[0]; y=cy*S-(b[3]-b[1])/2-b[1]
    d.text((x,y),t,font=f,fill=255)
    l=l.resize((w,h),Image.LANCZOS).filter(ImageFilter.GaussianBlur(.45))
    out.paste(Image.new('RGB',(w,h),(214,208,197)),(0,0),l)
c=src(330,147); rotulo('FABRIC',c[0],c[1],20)
c=src(1110,147); rotulo('SCHOCK BA',c[0],c[1],20)
out.save(B/'plaza-carteles.jpg',quality=92)
