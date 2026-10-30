"""V10 home acceptance and approved animation scenario, without browser dependencies."""
from pathlib import Path
from html import unescape
import sys,re,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import roi_animation as a
home=unescape((ROOT/'index.html').read_text())
order=['class="hero"','id="capital"','id="productivite"','id="investissement"','id="pipelines"']
positions=[home.index(s) for s in order];assert positions==sorted(positions)
assert home.count('id="brand-animation"')==1 and home.count('id="pipeline-animation"')==1
assert 'data-media-base="assets/roi/roi"' in home and 'data-kind="roi"' in home
assert 'Une petite structure.' in home and 'chirurgicale' in home
assert 'un remplacement peut rester nécessaire' in home and 'n’est pas automatiquement une économie financière' in home
assert 'Scénario illustratif' in home and 'Lire la comparaison et ses étapes' in home
assert 'href="diagnostic.html"' in home and 'href="contact.html"' in home and 'href="pipelines.html"' in home
assert '<source' not in home[home.index('class="pipeline-demo'):], 'ROI media must remain lazy'
assert '.gif' not in home and 'preload="none"' in home
assert a.N/a.FPS==36 and a.month(13)==9 and a.month(34)==36
for s in a.D.values():assert len(s['a'])==3 and len(s['b'])==9
assert a.value(3,0)>a.value(3,1), 'CLN initial investment must be smaller'
assert a.value(9,0)>0 and a.value(9,1)<0
assert a.value(36,0)>a.value(9,0) and a.value(36,1)<0
# Common graph dimensions and value() mapping; no separately scaled curves.
source=(ROOT/'scripts/roi_animation.py').read_text()
assert 'for side,x in enumerate([40,620])' in source and 'gw=465;gy=805;sc=78' in source
from PIL import Image
for lang in a.D:
 for ext in ['mp4','webm','webp']:
  path=ROOT/f'assets/roi/roi-{lang}.{ext}';assert path.exists()
  if ext=='webp':
   assert path.stat().st_size<200_000
   assert Image.open(path).size==(1200,1100)
  else:
   assert path.stat().st_size<2_500_000
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=codec_name,width,height,codec_type','-of','json',str(path)]))
   assert abs(float(probe['format']['duration'])-36)<.1
   assert len(probe['streams'])==1 and probe['streams'][0]['codec_type']=='video'
   s=probe['streams'][0];assert (s['width'],s['height'])==(1200,1100)
   assert s['codec_name']==('h264' if ext=='mp4' else 'vp9')
# Home generation must remain deterministic even after previous V10 output.
files=list(ROOT.glob('*.html'))+[ROOT/'i18n/static.json',ROOT/'i18n/messages.json']
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run([sys.executable,str(ROOT/'scripts/build_pedagogy.py')],check=True,stdout=subprocess.DEVNULL)
assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'Generation changed outputs on a second pass'
print('PASS V10: home order, preserved arrow, accessible/lazy ROI, illustrative copy, 4 languages, 3/9 steps, 9/36 months, identical scales, 12 media and idempotent generation.')
