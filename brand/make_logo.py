from PIL import Image, ImageDraw, ImageFont
F='node_modules/@fontsource/'
GRAD=F+'graduate/files/graduate-latin-400-normal.woff'
ANTON=F+'anton/files/anton-latin-400-normal.woff'
OSW=F+'oswald/files/oswald-latin-700-normal.woff'
G=(11,93,59); GD=(6,58,37); W=(255,255,255)
N=1024

def centered(d, xy, text, font, **kw):
    d.text(xy, text, font=font, anchor='mm', **kw)

def opt_a():  # varsity monogram: S centered, T stem runs through it with a green gap
    im=Image.new('RGB',(N,N),G); d=ImageDraw.Draw(im)
    fS=ImageFont.truetype(GRAD,640); fT=ImageFont.truetype(GRAD,700)
    centered(d,(N/2,N*0.55),'S',fS,fill=W)
    centered(d,(N/2,N*0.47),'T',fT,fill=W,stroke_width=24,stroke_fill=G)
    return im

def opt_b():  # athletic italic wordmark in a ring, with a tracker pulse
    im=Image.new('RGB',(N,N),G); d=ImageDraw.Draw(im)
    d.ellipse([110,110,N-110,N-110],outline=W,width=30)
    f=ImageFont.truetype(ANTON,470)
    # fake italic via shear
    t=Image.new('L',(N,N),0); td=ImageDraw.Draw(t)
    centered(td,(N/2+20,N*0.47),'ST',f,fill=255)
    t=t.transform((N,N),Image.AFFINE,(1,0.18,-90,0,1,0),resample=Image.BICUBIC)
    im.paste(W,(0,0),t)
    y=N*0.74; pts=[(300,y),(420,y),(460,y-55),(510,y+45),(555,y-25),(590,y),(724,y)]
    d.line(pts,fill=W,width=22,joint='curve')
    return im

def opt_c():  # shield badge
    im=Image.new('RGB',(N,N),G); d=ImageDraw.Draw(im)
    top,bot,l,r=150,900,190,834
    shield=[(l,top),(r,top),(r,560),(N/2,bot),(l,560)]
    d.polygon(shield,fill=W)
    inset=[(l+40,top+40),(r-40,top+40),(r-40,548),(N/2,bot-58),(l+40,548)]
    d.polygon(inset,fill=GD)
    f=ImageFont.truetype(OSW,380)
    centered(d,(N/2,500),'ST',f,fill=W)
    return im

opts={'A':opt_a(),'B':opt_b(),'C':opt_c()}
for k,im in opts.items(): im.save(f'logo/option-{k}.png')
# preview sheet: each option as a rounded app icon with label
S=360; sheet=Image.new('RGB',(S*3+80,S+90),(244,244,240)); sd=ImageDraw.Draw(sheet)
lab=ImageFont.truetype(OSW,40)
for i,(k,im) in enumerate(opts.items()):
    ic=im.resize((S,S),Image.LANCZOS)
    m=Image.new('L',(S,S),0); ImageDraw.Draw(m).rounded_rectangle([0,0,S-1,S-1],radius=80,fill=255)
    x=20+i*(S+20); sheet.paste(ic,(x,20),m)
    sd.text((x+S/2,S+55),'Option '+k,font=lab,fill=(30,30,30),anchor='mm')
sheet.save('logo/options.png')
