"""V10 approved illustrative animation; shared source for all four languages.
No financial scale or guarantee. Values are arbitrary illustrative net balances.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,json
O=Path(__file__).parent;W,H=1200,1100;FPS=6;N=216
F='/usr/share/fonts/truetype/dejavu/DejaVuSans';BG='#0b1728';FG='#ecf5ff';MUT='#9eb2c9';CYAN='#72dff6';GOLD='#ebbc83'
D={
'fr':dict(title='Investir moins. Produire des gains plus tôt.',left='Valoriser l’existant avec CLN',right='Remplacer les applications',sub='Même capital de départ : applications, données et savoir-faire',a=['Cibler et connecter','Automatiser et mettre en service','Étendre et stabiliser'],b=['Cadrer le programme','Choisir la solution','Concevoir la cible','Paramétrer','Développer les interfaces','Migrer les données','Tester','Former les équipes','Déployer'],month='MOIS',steps='3 étapes • 9 mois',long='9 étapes • 36 mois',running='En service : les gains s’accumulent',building='Transformation en cours',final='Déploiement : les gains démarrent',capital='Investissement limité • Mise en œuvre rapide',cost='Investissement et adaptation sur la durée',chart='Gains cumulés moins coûts cumulés',scale='Mêmes échelles de temps et de montant • courbes illustratives',paid='Investissement amorti',gain='Gains déjà engagés',end='Votre existant est un capital. Faites-le fructifier.',note='Scénario illustratif. Calendrier, coûts et retour à évaluer pour chaque projet.'),
'en':dict(title='Invest less. Generate benefits sooner.',left='Build on existing tools with CLN',right='Replace the applications',sub='The same starting capital: applications, data and expertise',a=['Focus and connect','Automate and go live','Expand and stabilise'],b=['Define the programme','Select the solution','Design the target','Configure','Develop the interfaces','Migrate the data','Test','Train the teams','Deploy'],month='MONTH',steps='3 stages • 9 months',long='9 stages • 36 months',running='Live: benefits keep accumulating',building='Transformation in progress',final='Deployment: benefits begin',capital='Limited investment • Fast implementation',cost='Investment and adaptation over time',chart='Cumulative benefits minus cumulative costs',scale='Identical time and value scales • illustrative curves',paid='Investment recovered',gain='Benefits already underway',end='Your existing assets are capital. Make them grow.',note='Illustrative scenario. Timeline, costs and returns must be assessed for each project.'),
'pt-BR':dict(title='Investir menos. Gerar benefícios mais cedo.',left='Valorizar o que já existe com a CLN',right='Substituir os aplicativos',sub='O mesmo capital inicial: aplicativos, dados e conhecimento',a=['Definir o foco e conectar','Automatizar e colocar em operação','Ampliar e estabilizar'],b=['Definir o programa','Escolher a solução','Projetar o modelo futuro','Configurar','Desenvolver as interfaces','Migrar os dados','Testar','Treinar as equipes','Implantar'],month='MÊS',steps='3 etapas • 9 meses',long='9 etapas • 36 meses',running='Em operação: os ganhos se acumulam',building='Transformação em andamento',final='Implantação: os ganhos começam',capital='Investimento limitado • Implantação rápida',cost='Investimento e adaptação ao longo do tempo',chart='Benefícios acumulados menos custos acumulados',scale='Mesmas escalas de tempo e valor • curvas ilustrativas',paid='Investimento recuperado',gain='Benefícios já em andamento',end='O que você já tem é um capital. Valorize-o.',note='Cenário ilustrativo. Prazos, custos e retorno devem ser avaliados para cada projeto.'),
'es':dict(title='Invertir menos. Generar beneficios antes.',left='Potenciar lo existente con CLN',right='Sustituir las aplicaciones',sub='El mismo capital inicial: aplicaciones, datos y conocimiento',a=['Definir el foco y conectar','Automatizar y poner en servicio','Ampliar y estabilizar'],b=['Definir el programa','Elegir la solución','Diseñar el modelo futuro','Configurar','Desarrollar las interfaces','Migrar los datos','Probar','Formar a los equipos','Desplegar'],month='MES',steps='3 etapas • 9 meses',long='9 etapas • 36 meses',running='En servicio: los beneficios se acumulan',building='Transformación en curso',final='Despliegue: comienzan los beneficios',capital='Inversión limitada • Implantación rápida',cost='Inversión y adaptación a lo largo del tiempo',chart='Beneficios acumulados menos costes acumulados',scale='Mismas escalas de tiempo y valor • curvas ilustrativas',paid='Inversión recuperada',gain='Beneficios ya en marcha',end='Lo que ya tiene es un capital. Hágalo crecer.',note='Escenario ilustrativo. Plazos, costes y retorno deben evaluarse para cada proyecto.')}
def ft(n,b=False):return ImageFont.truetype(F+('-Bold' if b else '')+'.ttf',n)
def text(d,x,y,s,n=20,c=FG,b=False,w=None):
 while w and d.textlength(s,font=ft(n,b))>w:n-=1
 d.text((x,y),s,font=ft(n,b),fill=c)
def month(t):
 if t<3:return 0
 if t<11:return (t-3)*9/8
 if t<15:return 9
 if t<31:return 9+(t-15)*27/16
 return 36
def value(m,side):
 # Illustrative net cumulative value, common arbitrary units, no numeric financial claims.
 pts=[(0,0),(3,-.15),(6,.03),(9,.30),(36,1.25)] if side==0 else [(0,0),(4,-.30),(8,-.40),(12,-.50),(16,-.60),(20,-.69),(24,-.77),(28,-.85),(32,-.91),(34,-.94),(36,-.85)]
 for (a,v),(b,u) in zip(pts,pts[1:]):
  if m<=b:return v+(u-v)*(m-a)/(b-a)
 return pts[-1][1]
def frame(k,l):
 s=D[l];t=k/FPS;m=month(t);im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
 text(d,40,22,'CLN PERFORMANCE',18,CYAN,True)
 text(d,40,58,s['title'],35,b=True,w=1120);text(d,40,110,s['sub'],21,MUT,w=1120)
 # shared chronological progress with months 0,9,18,27,36
 x0,x1=65,1135;y=170
 d.line((x0,y,x1,y),fill='#354a63',width=5);xx=x0+(x1-x0)*m/36
 d.line((x0,y,xx,y),fill=CYAN,width=5)
 for mm in [0,9,18,27,36]:
  x=x0+(x1-x0)*mm/36;d.ellipse((x-4,y-4,x+4,y+4),fill=FG);text(d,x-12,y+14,str(mm),16,MUT)
 d.ellipse((xx-8,y-8,xx+8,y+8),fill=CYAN)
 text(d,930,132,s['month']+' '+f'{m:02.0f}'+' / 36',19,CYAN,True,w=220)
 for side,x in enumerate([40,620]):
  c=CYAN if side==0 else GOLD; entries=s['a'] if side==0 else s['b'];dur=3 if side==0 else 4
  d.rounded_rectangle((x,222,x+540,630),18,fill='#122339',outline=c,width=4)
  text(d,x+21,240,s['left' if side==0 else 'right'],24,c,True,w=498)
  text(d,x+21,280,s['steps' if side==0 else 'long'],20,MUT)
  for j,label in enumerate(entries):
   start=j*dur;end=(j+1)*dur; yy=322+j*29 if side else 335+j*59
   visible=m>=start and t>=3
   if not visible:continue
   done=m>=end;active=start<=m<end
   if active:d.rounded_rectangle((x+15,yy-4,x+525,yy+26),6,fill='#29435b')
   text(d,x+24,yy,'✓' if done else '›',21,c,True)
   text(d,x+52,yy,f'{j+1}. '+label,19,FG if active or done else MUT,w=380)
   text(d,x+452,yy,f'{end} '+('m'),17,MUT,w=65)
  if side==0:
   # familiar applications remain present after all three stages
   for j in range(3):
    ax=x+24+j*170;d.rounded_rectangle((ax,535,ax+150,575),7,fill='#223c53',outline=CYAN,width=2);text(d,ax+39,545,'APP '+str(j+1),16,FG,True)
   if m>=3:
    d.line((x+45,590,x+494,590),fill=CYAN,width=3)
    cx=x+45+((t*.16)%1)*449;d.ellipse((cx-5,585,cx+5,595),fill='white')
  status=s['running'] if side==0 and m>=9 else s['building'] if side==1 and m<36 else s['final'] if side==1 else s['steps']
  text(d,x+21,600,status,19,c,True,w=498)
  text(d,x+5,648,s['capital' if side==0 else 'cost'],20,c,True,w=530)
  # independent identical chart, y range +1.35 .. -1.05, x 0..36
  gx=x+44;gw=465;gy=805;sc=78
  text(d,x+5,686,s['chart'],18,FG,True,w=530)
  d.line((gx,707,gx,904),fill='#5a6c83',width=2);d.line((gx,gy,gx+gw,gy),fill='#7c8da3',width=2)
  text(d,gx-24,gy-11,'0',15,MUT)
  for mm in [0,9,18,27,36]:
   px=gx+gw*mm/36;d.line((px,900,px,906),fill=MUT);text(d,px-10,911,str(mm),15,MUT)
  text(d,gx+gw-45,935,s['month'],13,MUT)
  if t>=3:
   pts=[(gx+gw*min(m,i/8)/36,gy-value(min(m,i/8),side)*sc) for i in range(int(m*8)+2)]
   if len(pts)>1:d.line(pts,fill=c,width=5,joint='curve')
   px,py=pts[-1];d.line((px,713,px,900),fill='#344a60',width=1);d.ellipse((px-6,py-6,px+6,py+6),fill=c)
   if side==0 and m>=6:text(d,gx+95,845,s['paid'],15,c,True,w=330)
   if side==0 and 9<=m<=9.001:text(d,gx+85,733,s['gain'],18,c,True,w=350)
 # subtle CLN-only wave and glints
 if t>=3:
  ov=Image.new('RGBA',(W,H));od=ImageDraw.Draw(ov);cx=60+(t*.13%1)*630
  for j in range(-65,66,3):od.line((cx+j,315,cx+j-65,588),fill=(190,225,248,int(18*(1-abs(j)/66))),width=4)
  ov.paste((0,0,0,0),(580,0,W,H));ov.paste((0,0,0,0),(0,0,40,H));im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB');d=ImageDraw.Draw(im)
  for j in range(12):
   a=max(0,math.sin(t*2+j*2.4))**12
   if a>.4:
    px=61+(j*89)%490;py=225+(j*53)%395;r=3
    d.line((px-r,py,px+r,py),fill='#d7f8ff');d.line((px,py-r,px,py+r),fill='#d7f8ff')
 text(d,40,973,s['scale'],17,MUT,w=1120)
 text(d,40,1007,s['end'],29,CYAN,True,w=1120)
 text(d,40,1064,s['note'],16,MUT,w=1120)
 return im
