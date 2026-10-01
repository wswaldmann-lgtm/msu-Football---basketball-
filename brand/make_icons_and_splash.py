import random
from PIL import Image, ImageDraw, ImageFilter
R='/home/user/msu-football---basketball-/icons/'
G=(11,93,59)
logo=Image.open('logo/option-B.png').convert('RGB')
# icons (full-bleed; phones round the corners)
for size,name in [(192,'icon-192.png'),(512,'icon-512.png'),(180,'apple-touch-icon.png')]:
    logo.resize((size,size),Image.LANCZOS).save(R+name,optimize=True)
m=Image.new('RGB',(512,512),G); small=logo.resize((400,400),Image.LANCZOS); m.paste(small,(56,56)); m.save(R+'icon-maskable-512.png',optimize=True)

# white-on-transparent logo mask for the splash
L=logo.convert('L').point(lambda v: 255 if v>200 else (0 if v<120 else int((v-120)*255/80)))

W,H=1080,1500
random.seed(7)
im=Image.new('RGB',(W,H))
d=ImageDraw.Draw(im)
for y in range(H):  # night-sky to deep green
    t=y/H
    c=(int(4+8*t),int(18+45*t),int(13+28*t))
    d.line([(0,y),(W,y)],fill=c)
# field at the bottom
fy=int(H*0.80)
for y in range(fy,H):
    t=(y-fy)/(H-fy)
    d.line([(0,y),(W,y)],fill=(int(16+10*t),int(78+30*t),int(46+14*t)))
for i in range(-6,7):  # perspective yard lines
    x0=W/2+i*60; x1=W/2+i*260
    d.line([(x0,fy),(x1,H)],fill=(60,130,90),width=3)
d.line([(0,fy),(W,fy)],fill=(150,220,180),width=4)
# stadium light banks: soft halo + beams toward the field
glow=Image.new('L',(W,H),0); gd=ImageDraw.Draw(glow)
for cx in (130,W-130):
    gd.ellipse([cx-150,140-150,cx+150,140+150],fill=120)
    tx=W/2+(-1 if cx<W/2 else 1)*80
    gd.polygon([(cx-60,140),(cx+60,140),(tx+(1 if cx<W/2 else -1)*260,fy),(tx-(1 if cx<W/2 else -1)*120,fy)],fill=38)
glow=glow.filter(ImageFilter.GaussianBlur(55))
im=Image.composite(Image.new('RGB',(W,H),(205,255,225)),im,glow)
lamps=Image.new('L',(W,H),0); ld=ImageDraw.Draw(lamps)
for cx in (130,W-130):
    for r in range(3):
        for k in range(5):
            x=cx-100+k*50; y=95+r*45
            ld.ellipse([x-11,y-11,x+11,y+11],fill=255)
im.paste((255,255,250),(0,0),lamps)
# crowd sparkle
sp=ImageDraw.Draw(im)
for _ in range(500):
    x=random.randint(0,W); y=random.randint(int(H*0.45),fy-10)
    b=random.randint(90,200); sp.point((x,y),fill=(b,min(255,b+40),b))
# logo with soft glow, centered
S=620; lm=L.resize((S,S),Image.LANCZOS)
pos=((W-S)//2,int(H*0.24))
halo=Image.new('L',(W,H),0); halo.paste(lm,pos); halo=halo.filter(ImageFilter.GaussianBlur(26))
im=Image.composite(Image.new('RGB',(W,H),(120,220,160)),im,halo.point(lambda v:int(v*0.7)))
im.paste((255,255,255),pos,lm)
im.save(R+'splash.jpg',quality=84,optimize=True,progressive=True)
print('done')
