"""V7 shared identity. Called by build_pedagogy.py after page generation."""
import re

LABELS = {
 'brand.pause': ('Mettre l’animation en pause', 'Pause animation', 'Pausar animação', 'Pausar animación'),
 'brand.play': ('Lire l’animation', 'Play animation', 'Reproduzir animação', 'Reproducir animación'),
}


def apply(root, messages):
    for key, values in LABELS.items():
        messages[key] = dict(zip(['fr', 'en', 'pt-BR', 'es'], values))
    for name in ['index', 'solutions', 'pipelines', 'approche', 'realisations',
                 'diagnostic', 'contact', 'merci', 'mentions-legales', 'confidentialite']:
        path = root / (name + '.html')
        text = path.read_text()
        text = re.sub(r'<img[^>]+src="(?:LOGO_CLN.png|assets/brand/cln-signature-poster.webp)"[^>]*>',
                      '<img src="assets/brand/cln-signature-poster.webp" alt="" width="112" height="48"/>', text, count=1)
        if name == 'index' and 'class="brand-signature"' not in text:
            example = re.search(r'<div class="before-after">.*?</div>', text, flags=re.S)
            if not example:
                raise ValueError('Home example block missing')
            example_html = example.group().replace('<div ', '<section ', 1)
            example_html = example_html[:-6] + '</section>'
            signature = '''<figure class="brand-signature">
<div class="brand-media">
<img class="brand-poster" src="assets/brand/cln-signature-poster.webp" alt="" width="520" height="220"/>
<video id="brand-animation" muted loop playsinline preload="none" poster="assets/brand/cln-signature-poster.webp" width="520" height="220" aria-hidden="true" tabindex="-1">
<source data-src="assets/brand/cln-signature.webm" type="video/webm"/>
<source data-src="assets/brand/cln-signature.mp4" type="video/mp4"/>
</video>
</div>
<figcaption>CLN Performance</figcaption>
<button class="brand-motion-toggle" type="button" aria-controls="brand-animation" data-msg="brand.play" hidden>Lire l’animation</button>
</figure>'''
            text = text[:example.start()] + signature + text[example.end():]
            hero_start = text.index('<section class="hero">')
            hero_end = text.index('</section>', hero_start) + len('</section>')
            text = text[:hero_end] + '\n' + example_html + text[hero_end:]
        text = re.sub(r'\?v=20261029-v[4567]', '?v=20261029-v7', text)
        path.write_text(text)
