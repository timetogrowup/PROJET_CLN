"""V9 procedural case diagram. Usage: python scripts/render_protys_media.py fr|en|pt-BR|es [GIF_OUTPUT_DIR]. Requires Pillow, NumPy, ffmpeg, DejaVu Sans."""
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
from pathlib import Path
from functools import lru_cache
import numpy as np, math, json, sys, tempfile, subprocess
ROOT=Path(__file__).resolve().parents[1];LANG=sys.argv[1] if len(sys.argv)>1 else 'fr'
assert LANG in ['fr','en','pt-BR','es']
COPY=json.loads((ROOT/'scripts/protys_translations.json').read_text())
OUT=ROOT/'assets/protys';OUT.mkdir(parents=True,exist_ok=True)
GIFS=Path(sys.argv[2]) if len(sys.argv)>2 else ROOT/'dist/protys-gifs';GIFS.mkdir(parents=True,exist_ok=True)
TEMP=tempfile.TemporaryDirectory();P=Path(TEMP.name);W,H=1320,800
FP='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
@lru_cache(maxsize=None)
def ft(n,b=False):return ImageFont.truetype(FB if b else FP,n)
def tr(s):
 if LANG=='fr' or s in ['CLN PERFORMANCE','PROTYS','PIPELINE CLN']:return s
 if s not in COPY:raise ValueError('Untranslated text: '+s)
 return COPY[s][LANG]
y,x=np.mgrid[:H,:W];g=(x/W*.5+y/H*.5)[...,None];base=Image.fromarray(np.uint8(np.array([12,29,48])*(1-g)+np.array([41,76,103])*g))
WHITE='#f6f8f4';MUTED='#bed0de';CYAN='#79dbf5';GOLD='#ffdb91';LINE='#50728b'
def txt(d,pos,s,n=16,b=False,c=WHITE,anchor=None,maxw=None):
 s=tr(s);f=ft(n,b)
 if maxw:
  while d.textlength(s,font=f)>maxw:f=ft(f.size-1,b)
 d.text(pos,s,font=f,fill=c,anchor=anchor)
def box(d,r,title,sub='',active=False):
 d.rounded_rectangle(r,12,fill='#19364f',outline=CYAN if active else '#496b84',width=6)
 txt(d,(r[0]+15,r[1]+15),title,18,True,maxw=r[2]-r[0]-30)
 if sub:txt(d,(r[0]+15,r[1]+48),sub,14,c=MUTED,maxw=r[2]-r[0]-30)
def pt(path,u):
 lengths=[math.dist(a,b) for a,b in zip(path,path[1:])];v=u*sum(lengths)
 for i,l in enumerate(lengths):
  if v<=l:return tuple(path[i][j]+(path[i+1][j]-path[i][j])*v/l for j in (0,1))
  v-=l
 return path[-1]
src=[(25,235,235,320),(25,365,235,450),(25,495,235,580)]
outs=[(1060,235,1295,320),(1060,365,1295,450),(1060,495,1295,580)]
inpaths=[[(235,(r[1]+r[3])/2),(251,(r[1]+r[3])/2),(265,407),(275,407)] for r in src]
taskpath=[(755,410),(805,410)];backpath=[(905,535),(905,614),(520,614),(520,590)]
outpaths=[[(755,250),(1035,250),(1035,(r[1]+r[3])/2),(1060,(r[1]+r[3])/2)] for r in outs]
rng=np.random.default_rng(57);stars=[(rng.uniform(285,745),rng.uniform(215,580),rng.uniform(0,3)) for _ in range(38)]
TA=Image.new('L',(W,H));ImageDraw.Draw(TA).text((300,217),'PIPELINE CLN',font=ft(20,True),fill=255);TA=np.array(TA)/255
captions=[('1. Collecter les informations','Déclarations, réponses, plans et données internes arrivent de plusieurs sources.'),('2. Rattacher au bon chantier','Le pipeline harmonise les données et ajoute la localisation et l’équipe concernée.'),('3. Enrichir et construire le bilan','Il identifie les exploitants attendus, les réponses reçues, les pièces et les délais.'),('4. Préparer les actions utiles','Le bilan devient une liste de tâches : relancer, récupérer les documents, déposer en GED.'),('5. Exécuter et récupérer les résultats','Le robot exécute les tâches. Les succès et les actions à reprendre reviennent dans le suivi.'),('6. Restituer une situation actualisée','Les documents disponibles et le bilan rejoignent les outils utilisés par les équipes.'),('Des informations dispersées. Un dossier enrichi. Des actions suivies.','Une réponse attendue et un dépôt à reprendre restent visibles : le suivi continue.')]
def render(k):
 t=k/8;s=min(6,int(t/4));im=base.copy();d=ImageDraw.Draw(im)
 txt(d,(25,22),'CLN PERFORMANCE',16,True,CYAN)
 txt(d,(25,56),'Déclarations de chantier : des données enrichies pour agir',32,True,maxw=1270)
 txt(d,(25,108),'« Construire sans détruire » : déclarer les travaux et recueillir les informations des exploitants de réseaux.',18,c=MUTED,maxw=1270)
 txt(d,(25,166),'SOURCES',15,True,MUTED);txt(d,(805,268),'EXÉCUTION',15,True,MUTED);txt(d,(1060,198),'OUTILS DES ÉQUIPES',15,True,MUTED,maxw=235)
 d.rounded_rectangle((275,200,755,590),18,fill='#102a41',outline=CYAN,width=6)
 for path in inpaths+[taskpath,backpath]+outpaths:d.line(path,fill=LINE,width=3)
 box(d,src[0],'PROTYS','Déclarations',s==0 or s==6);box(d,src[1],'PROTYS','Réponses et plans',s==0 or s==6);box(d,src[2],'Référentiels internes','Localisation · équipe',s==0 or s==6)
 txt(d,(300,217),'PIPELINE CLN',20,True,CYAN);txt(d,(300,251),'Contrôles et historique',13,c=MUTED)
 d.rounded_rectangle((295,281,735,563),12,fill='#19364f',outline='#62839b',width=3)
 txt(d,(315,297),'CHANTIER A',20,True);txt(d,(315,331),'Déclaration rattachée' if s>=1 else 'Déclaration reçue',16,c=CYAN)
 rows=[('Localisation : secteur Nord',s>=1),('Équipe : exploitation',s>=1),('Exploitants attendus : 3',s>=2),('Réponses reçues : 2 sur 3',s>=2),('Plans disponibles : 2',s>=2),('Délais et historique associés',s>=2)]
 for j,(label,shown) in enumerate(rows):
  if shown:txt(d,(315,365+j*25),label,16,c=MUTED if j<2 else WHITE,maxw=395)
 if s>=3:txt(d,(300,565),'Suivi : 1 réponse attendue · 1 dépôt à reprendre' if s>=5 else 'À faire : relancer · récupérer · déposer',14,True,GOLD,maxw=430)
 box(d,(805,310,1005,535),'ROBOT','Tâches préparées' if s>=3 else 'En attente',s==4)
 if s>=3:
  for j,label in enumerate(['Relancer','Récupérer les plans','Déposer en GED']):txt(d,(822,393+j*34),label,15,c=MUTED,maxw=165)
 if s>=4:
  txt(d,(822,495),'Résultats enregistrés',13,True,CYAN,maxw=165)
  txt(d,(710,642),'Relance envoyée · 1 dépôt réussi · 1 dépôt à reprendre',15,True,GOLD,anchor='mm',maxw=1000)
 else:txt(d,(710,642),'Les résultats du robot complètent le bilan du chantier',14,c=MUTED,anchor='mm',maxw=1000)
 txt(d,(780,388),'Tâches',12,c=GOLD,anchor='mm',maxw=46);txt(d,(898,231),'Documents et bilan',13,c=MUTED,anchor='mm',maxw=265)
 box(d,outs[0],'Gestion documentaire','1 plan classé' if s>=5 else 'Plans à classer',s>=5)
 box(d,outs[1],'Suivi des dossiers','1 réponse attendue' if s>=5 else 'Bilan à actualiser',s>=5)
 box(d,outs[2],'Équipes opérationnelles','Dossier consultable' if s>=5 else 'Informations à consolider',s>=5)
 if s>=5:txt(d,(1060,602),'1 dépôt reste à reprendre',14,True,GOLD,maxw=235)
 glow=Image.new('RGB',(W,H));gd=ImageDraw.Draw(glow)
 paths=inpaths if s==0 else [taskpath] if s==3 else [backpath] if s==4 else outpaths if s==5 else []
 for j,path in enumerate(paths):
  for offset in [0,.48]:
   u=(t*.65+j*.1+offset)%1
   for trail in range(4):
    v=u-trail*.025
    if v>=0:
     px,py=pt(path,v);col=tuple(int(c*(1-trail/5)) for c in ((255,219,145) if s in [3,4] else (121,219,245)));gd.ellipse((px-4,py-4,px+4,py+4),fill=col)
 for sx,sy,off in stars:
  q=max(0,math.sin((t/3+off)*math.pi*2))**10;r=6*q;c=tuple(int(v*q) for v in (210,243,255))
  if q>.05:gd.line((sx-r,sy,sx+r,sy),fill=c);gd.line((sx,sy-r,sx,sy+r),fill=c)
 im=ImageChops.screen(im,ImageChops.add(glow,glow.filter(ImageFilter.GaussianBlur(4))))
 a=np.asarray(im).astype(np.float32);phase=(t%7)/7;dist=x-.27*(y-H/2)-(-450+2200*phase)
 wave=(.26*np.exp(-(dist/210)**2)+.18*np.exp(-(dist/65)**2))*math.sin(math.pi*phase)**.7
 shine=np.clip(wave+TA*(.35+.45*np.exp(-((x-(280+(t%3)/3*500))/40)**2)),0,.95)
 a=255-(255-a)*(1-shine[...,None]*np.array([.45,.68,.85]));im=Image.fromarray(np.uint8(a));d=ImageDraw.Draw(im)
 title,sub=captions[s];txt(d,(W/2,701),title,26 if s<6 else 23,True,anchor='mm',maxw=1250);txt(d,(W/2,741),sub,17,c=MUTED,anchor='mm',maxw=1260)
 for j in range(7):xx=559+j*30;d.rounded_rectangle((xx,767,xx+20,771),2,fill=CYAN if j==s else '#496b84')
 txt(d,(1295,780),'Exemple fictif · Ne vaut pas autorisation de travaux',12,c=MUTED,anchor='ra',maxw=570)
 return im
palette=Image.fromarray(np.vstack([np.array(render(k))[::5,::5] for k in [0,70,134,174,214]])).quantize(colors=256)
frames=[]
for k in range(224):
 im=render(k);im.save(P/f'{k:03d}.png')
 if k==208:im.save(OUT/f'protys-{LANG}.webp',quality=90)
 frames.append(im.quantize(palette=palette,dither=Image.Dither.NONE))
frames[0].save(GIFS/f'CLN_pipeline_chantier_PROTYS_{LANG}.gif',save_all=True,append_images=frames[1:],duration=[120,130]*112,loop=0,optimize=True)
for ext,args in [('mp4',['-c:v','libx264','-crf','24','-movflags','+faststart']),('webm',['-c:v','libvpx-vp9','-b:v','0','-crf','36'])]:
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','8','-i',str(P/'%03d.png'),'-vf','format=yuv420p','-an','-threads','2',*args,str(OUT/f'protys-{LANG}.{ext}')],check=True)
TEMP.cleanup();print('Rendered',LANG,flush=True)
