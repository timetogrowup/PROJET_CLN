"""Rebuild the 12 V10 web assets. Usage: python scripts/render_roi_media.py [fr|en|pt-BR|es].
Requires Pillow, DejaVu Sans and ffmpeg. Optional --gif-dir reuses approved GIFs.
Without it, all animation frames are rendered from roi_animation.py in a temporary folder.
"""
from pathlib import Path
import argparse,subprocess,tempfile
import roi_animation as a
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('lang',nargs='?',choices=list(a.D));p.add_argument('--gif-dir',type=Path);args=p.parse_args()
out=ROOT/'assets/roi';out.mkdir(parents=True,exist_ok=True)
for lang in ([args.lang] if args.lang else a.D):
 with tempfile.TemporaryDirectory() as tmp:
  if args.gif_dir:
   source=['-i',str(args.gif_dir/f'CLN_ROI_existant_{lang}.gif')]
  else:
   for k in range(a.N):a.frame(k,lang).save(Path(tmp)/f'{k:04}.png')
   source=['-framerate',str(a.FPS),'-i',str(Path(tmp)/'%04d.png')]
  common=['ffmpeg','-hide_banner','-loglevel','error','-y',*source,'-an','-r',str(a.FPS),'-t','36']
  subprocess.run(common+['-c:v','libvpx-vp9','-crf','35','-b:v','0','-deadline','good','-cpu-used','4',str(out/f'roi-{lang}.webm')],check=True)
  subprocess.run(common+['-c:v','libx264','-crf','24','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(out/f'roi-{lang}.mp4')],check=True)
  a.frame(204,lang).save(out/f'roi-{lang}.webp',quality=90,method=6)
  print('Rendered',lang,flush=True)
