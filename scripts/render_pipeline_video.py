"""Render the approved V8 pipeline illustration. Usage: python scripts/render_pipeline_video.py fr|en|pt-BR|es."""
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math, numpy as np
from pathlib import Path
import sys, tempfile, subprocess, json
ROOT=Path(__file__).resolve().parents[1]
LANG=sys.argv[1] if len(sys.argv)>1 else 'fr'
assert LANG in ['fr','en','pt-BR','es']
COPY=json.loads((ROOT/'scripts/pipeline_video_translations.json').read_text())
def tr(s):return COPY.get(s,{}).get(LANG,s)
OUT=ROOT/'assets/pipeline';OUT.mkdir(parents=True,exist_ok=True)
TEMP=tempfile.TemporaryDirectory();P=Path(TEMP.name)
W,H=1100,680
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(bold if b else fontpath,n)
F={n:font(n) for n in [13,14,15,16,18,20,22,30]};B={n:font(n,True) for n in [14,15,16,18,20,22,30]}
y,x=np.mgrid[:H,:W];g=(x/W*.5+y/H*.5)[...,None];bg=np.uint8(np.array([13,31,51])*(1-g)+np.array([43,77,105])*g);base=Image.fromarray(bg)
white='#f6f6ee';muted='#b4c9dc';line='#42617c';cyan='#78d9f4';gold='#ffdb91'
sources=[(40,215,260,305),(40,345,260,435),(40,475,260,565)]
outputs=[(840,215,1060,305),(840,345,1060,435),(840,475,1060,565)]
match=(335,320,520,440);calc=(565,320,750,440)
leftpaths=[[(260,(r[1]+r[3])/2),(289,(r[1]+r[3])/2),(310,380),(335,380)] for r in sources]
rightpaths=[[(750,380),(782,380),(810,(r[1]+r[3])/2),(840,(r[1]+r[3])/2)] for r in outputs]
midpath=[(520,380),(565,380)]
def text(d,xy,s,f,fill=white,anchor=None):
 s=tr(s)
 if xy[0] in [351,581] and f.size==14:
  while d.textlength(s,font=f)>153:f=font(f.size-1,True)
 d.text(xy,s,font=f,fill=fill,anchor=anchor)
def card(d,r,title,sub,active=False,accent=cyan):
 title,sub=tr(title),tr(sub)
 d.rounded_rectangle(r,12,fill='#19364f',outline=accent if active else '#46647c',width=10)
 f=B[18]
 while d.textlength(title,font=f)>r[2]-r[0]-32: f=font(f.size-1,True)
 text(d,(r[0]+16,r[1]+17),title,f)
 sf=F[14]
 while d.textlength(sub,font=sf)>r[2]-r[0]-32:sf=font(sf.size-1)
 text(d,(r[0]+16,r[1]+49),sub,sf,muted)
def point(path,t):
 lens=[math.dist(path[i],path[i+1]) for i in range(len(path)-1)];s=t*sum(lens)
 for i,l in enumerate(lens):
  if s<=l:return tuple(path[i][j]+(path[i+1][j]-path[i][j])*s/l for j in [0,1])
  s-=l
 return path[-1]
def particle(d,path,u,c):
 px,py=point(path,u);d.ellipse((px-5,py-5,px+5,py+5),fill=c)
title_mask=Image.new('L',(W,H));ImageDraw.Draw(title_mask).text((342,239),'PIPELINE CLN',font=B[18],fill=255)
title_alpha=np.asarray(title_mask)/255
panel_mask=Image.new('L',(W,H));ImageDraw.Draw(panel_mask).rounded_rectangle((310,275,775,473),18,fill=255)
panel_alpha=np.asarray(panel_mask)/255
rng=np.random.default_rng(62)
stars=[(float(rng.uniform(320,765)),float(rng.uniform(285,463)),float(rng.uniform(0,3)),float(rng.uniform(3,7))) for _ in range(55)]
stars += [(float(rng.uniform(344,475)),float(rng.uniform(242,258)),float(rng.uniform(0,3)),float(rng.uniform(3,6))) for _ in range(12)]
frames=[]
for k in range(180):
 t=k/12;stage=min(4,int(t/3));im=base.copy();d=ImageDraw.Draw(im)
 text(d,(40,28),'CLN PERFORMANCE',B[16],cyan)
 text(d,(40,63),'Vos données circulent. Leur valeur grandit.',B[30])
 text(d,(40,108),'Un exemple : traiter une demande en utilisant vos applications existantes.',F[18],muted)
 for px in range(40,1080,28):d.ellipse((px,161,px+1,162),fill='#486780')
 text(d,(40,181),'APPLICATIONS SOURCES',B[14],muted)
 text(d,(342,239),'PIPELINE CLN',B[18],cyan)
 text(d,(840,181),'APPLICATIONS DESTINATAIRES',F[13],muted)
 d.rounded_rectangle((310,275,775,473),18,fill='#102a41',outline='#375d7c',width=5)
 for path in leftpaths+rightpaths+[midpath]:d.line(path,fill=line,width=3)
 card(d,sources[0],'Gestion des demandes','Demande #1042',stage==0 or stage==4)
 card(d,sources[1],'Référentiel clients','Client · contrat · localisation',stage==0 or stage==4)
 card(d,sources[2],'Planning','Disponibilités des équipes',stage==0 or stage==4)
 card(d,match,'Rapprocher','Demande + client',stage==1 or stage==4)
 card(d,calc,'Enrichir / calculer','Règles métier',stage==2 or stage==4,gold)
 text(d,(match[0]+16,match[1]+83),'Dossier #1042',B[14],cyan if stage>=1 else muted)
 text(d,(calc[0]+16,calc[1]+83),'Priorité : HAUTE' if stage>=2 else 'Priorité à calculer',B[14],gold if stage>=2 else muted)
 card(d,outputs[0],'Planning enrichi','Priorité haute · délai 24 h' if stage>=3 else 'Priorité et délai à recevoir',stage>=3)
 card(d,outputs[1],'Dossier complété','Contexte client intégré' if stage>=3 else 'Contexte client à recevoir',stage>=3)
 card(d,outputs[2],'Tableau de bord','Indicateurs actualisés' if stage>=3 else 'Résultats à recevoir',stage>=3)
 # Branching data routes with trailing light.
 glow=Image.new('RGB',(W,H));gd=ImageDraw.Draw(glow)
 paths=leftpaths if stage==0 else [midpath] if stage in [1,2] else rightpaths if stage==3 else leftpaths+[midpath]+rightpaths
 if stage!=4:
  for j,path in enumerate(paths):
   for offset in [0,.43]:
    u=((t%3)/1.4+offset+j*.12)%1
    for trail in range(5):
     v=u-trail*.025
     if v>=0:particle(gd,path,v,tuple(int(z*(1-trail/6)) for z in ((255,219,145) if stage==2 else (120,217,244))))
  from PIL import ImageChops
  im=ImageChops.screen(im,ImageChops.add(glow,glow.filter(ImageFilter.GaussianBlur(6))));d=ImageDraw.Draw(im)
 if stage in [1,2]:
  r=match if stage==1 else calc
  progress=(t%3)/3
  d.rounded_rectangle((r[0]+16,r[3]-12,r[0]+16+int((r[2]-r[0]-32)*progress),r[3]-8),2,fill=cyan if stage==1 else gold)
 captions=[('1. Collecter','Les données utiles quittent plusieurs applications.'),('2. Rapprocher','Le pipeline relie la demande aux informations du client.'),('3. Enrichir et calculer','Il applique les règles et calcule la priorité et le délai.'),('4. Redistribuer','Les résultats enrichis rejoignent plusieurs outils métier.'),('Des applications reliées. Des résultats utiles.','Vos outils existants bénéficient de données enrichies.')]
 title,subtitle=captions[stage]
 text(d,(550,592),title,B[22],white,'mm');text(d,(550,624),subtitle,F[16],muted,'mm')
 for j in range(5):
  xx=480+j*30;d.rounded_rectangle((xx,649,xx+20,653),2,fill=cyan if j==stage else '#47637a')
 text(d,(1060,659),'Scénario illustratif',F[13],muted,'ra')

 # Wide diagonal blue-grey light wave, three passes per 15-second loop.
 phase=(t%5)/5
 center=-480+2100*phase
 distance=x-.28*(y-H/2)+20*np.sin(y/160)-center
 envelope=math.sin(math.pi*phase)**.65
 wave=(.30*np.exp(-(distance/210)**2)+.23*np.exp(-(distance/65)**2))*envelope
 pixels=np.asarray(im).astype(np.float32)
 tint=np.array([115,174,217],dtype=np.float32)
 # Screen blending adds light while preserving white type and bright particles.
 pixels=255-(255-pixels)*(1-wave[...,None]*tint/255)
 im=Image.fromarray(np.uint8(np.clip(pixels,0,255)))
 # Continuous glints cover the complete CLN panel and the title glyphs.
 pixels=np.asarray(im).astype(np.float32)
 sheen=(.07+.10*(.5+.5*np.sin(x/34+y/42-t*3))) * panel_alpha
 stripe=np.exp(-((x-(280+(t%3)/3*550))/36)**2)
 title_shine=title_alpha*(.35+.65*stripe)
 shine=np.clip(sheen+title_shine,0,.95)
 pixels=255-(255-pixels)*(1-shine[...,None]*np.array([.62,.85,1.]))
 im=Image.fromarray(np.uint8(np.clip(pixels,0,255)))
 glints=Image.new('RGB',(W,H));gd=ImageDraw.Draw(glints)
 pulse=.5+.5*math.sin(t*2*math.pi/3)
 gd.rounded_rectangle((310,275,775,473),18,outline=tuple(int(v*(.30+.35*pulse)) for v in (135,216,255)),width=10)
 for sx,sy,offset,radius in stars:
  q=max(0,math.sin(2*math.pi*(t/3+offset)))**10
  if q>.025:
   r=radius*q;colour=tuple(int(v*q) for v in (222,247,255))
   gd.line((sx-r,sy,sx+r,sy),fill=colour,width=1)
   gd.line((sx,sy-r,sx,sy+r),fill=colour,width=1)
   gd.ellipse((sx-q*1.6,sy-q*1.6,sx+q*1.6,sy+q*1.6),fill=colour)
 from PIL import ImageChops
 im=ImageChops.screen(im,ImageChops.add(glints,glints.filter(ImageFilter.GaussianBlur(4))))
 if k==96:im.save(P/'pipeline_contours_x5_preview.png')
 im.save(P/f'{k:03d}.png')
 if k==166:im.save(OUT/f'pipeline-{LANG}.webp',quality=90)

for ext,args in [('mp4',['-c:v','libx264','-crf','23','-movflags','+faststart']),('webm',['-c:v','libvpx-vp9','-b:v','0','-crf','35'])]:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','12','-i',str(P/'%03d.png'),'-vf','format=yuv420p','-an',*args,str(OUT/f'pipeline-{LANG}.{ext}')],check=True)
TEMP.cleanup()
print('Rendered',LANG,flush=True)
