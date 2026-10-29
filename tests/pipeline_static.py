from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parents[1]
s=(root/'solutions.html').read_text()
assert s.count('id="bout-en-bout"')==1
assert s.index('</h1>')<s.index('id="bout-en-bout"')<s.index('id="ressaisies"')
assert s.count('id="pipeline-animation"')==1
assert 'preload="none"' in s and '<source' not in s
assert 'id="pipeline-dialog"' in s and 'Lire les étapes du schéma' in s
for lang in ['fr','en','pt-BR','es']:
 for ext in ['mp4','webm','webp']:
  path=root/f'assets/pipeline/pipeline-{lang}.{ext}'
  assert 0<path.stat().st_size<1_000_000,(path,path.stat().st_size)
  if ext!='webp':
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-show_entries','stream=codec_name,width,height','-of','json',str(path)]))
   assert abs(float(probe['format']['duration'])-15)<.1,probe
   stream=probe['streams'][0];assert (stream['width'],stream['height'])==(1100,680)
   assert stream['codec_name']==('h264' if ext=='mp4' else 'vp9')
catalog=json.loads((root/'scripts/pipeline_video_translations.json').read_text())
assert len(catalog)==37
assert all(set(v)=={'fr','en','pt-BR','es'} and all(v.values()) for v in catalog.values())
print('PASS V8: placement, single instance, lazy markup, accessible transcript, 12 localized assets, 8 video codecs/durations and 37 translated labels.')
