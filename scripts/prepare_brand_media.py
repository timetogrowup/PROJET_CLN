"""Convert the approved x20 GIF to web assets. Usage: python scripts/prepare_brand_media.py /path/to/approved.gif"""
from pathlib import Path
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parents[1] / 'assets/brand'
out.mkdir(parents=True, exist_ok=True)
for extension, codec in [('mp4', ['-c:v', 'libx264', '-crf', '23', '-movflags', '+faststart']),
                         ('webm', ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '35'])]:
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                    '-vf', 'crop=520:220:80:205,format=yuv420p', '-an', *codec,
                    str(out / ('cln-signature.' + extension))], check=True)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(out / 'cln-signature.mp4'),
                '-frames:v', '1', str(out / 'cln-signature-poster.webp')], check=True)
