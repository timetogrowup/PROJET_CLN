from pathlib import Path
from PIL import Image
import json,subprocess,ast,sys
root=Path(__file__).resolve().parents[1];s=(root/'pipelines.html').read_text()
assert s.count('id="chantier-protys"')==1
assert s.index('</h1>')<s.index('id="chantier-protys"')<s.index('id="exemple"')<s.index('id="capacites"')
assert s.count('id="pipeline-animation"')==1 and 'data-media-base="assets/protys/protys"' in s
assert '<details class="pipeline-other-example">' in s and 'class="pipeline-steps"' in s
assert 'Lire les étapes du suivi de chantier' in s and 'preload="none"' in s
assert 'data-media-base="assets/protys/protys"' not in (root/'solutions.html').read_text()
copy=json.loads((root/'scripts/protys_translations.json').read_text())
assert all(set(v)=={'en','pt-BR','es'} and all(v.values()) for v in copy.values())
# Every literal drawn by txt()/box() is in the translation map or an allowed brand.
allowed={'CLN PERFORMANCE','PROTYS','PIPELINE CLN'}
tree=ast.parse((root/'scripts/render_protys_media.py').read_text())
for n in ast.walk(tree):
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['txt','box']:
  for arg in n.args[2:3] if n.func.id=='txt' else n.args[2:4]:
   if isinstance(arg,ast.Constant) and isinstance(arg.value,str) and arg.value:assert arg.value in copy or arg.value in allowed,arg.value
for lang in ['fr','en','pt-BR','es']:
 for ext in ['webm','mp4','webp']:
  p=root/f'assets/protys/protys-{lang}.{ext}'
  assert 0<p.stat().st_size<2_500_000
  if ext=='webp':assert Image.open(p).size==(1320,800)
  else:
   d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height','-show_entries','format=duration','-of','json',str(p)]))
   assert abs(float(d['format']['duration'])-28)<.1
   assert (d['streams'][0]['width'],d['streams'][0]['height'])==(1320,800)
   assert d['streams'][0]['codec_name']==('vp9' if ext=='webm' else 'h264')
 gifdir=Path(sys.argv[1]) if len(sys.argv)>1 else root/'dist/protys-gifs'
 if gifdir.exists():
  forcheck=gifdir/f'CLN_pipeline_chantier_PROTYS_{lang}.gif';im=Image.open(forcheck);total=0
  assert im.size==(1320,800) and im.info.get('loop')==0
  for k in range(im.n_frames):im.seek(k);total+=im.info['duration']
  assert total==28000 and forcheck.stat().st_size<25_000_000
print(f'PASS V9 placement, preservation of planning example/V8, {len(copy)} translated diagram labels, 12 web assets; 28-second looping GIFs checked when the optional output folder exists.')
