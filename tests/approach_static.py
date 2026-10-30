from pathlib import Path
import json,re,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'approche.html').read_text()
assert s.count('<h1>')==1 and 'class="method-page"' in s
ids=['diagnostic','intervention','pipeline','intelligence-artificielle','remuneration','questions-pratiques']
positions=[s.index('id="'+x+'"') for x in ids];assert positions==sorted(positions)
hero=s[s.index('id="diagnostic"'):s.index('id="intervention"')]
for text in ['Un premier diagnostic en quelques jours','Sur un périmètre défini','interlocuteurs et les informations nécessaires disponibles','Ce que vous obtenez','budget','calendrier','mesurer']:assert text in hero,text
assert len(re.findall(r'<a class="cta-button" href="diagnostic.html">',s))==2
steps=re.search(r'<ol class="method-steps">(.*?)</ol>',s,re.S)[1];assert steps.count('<li>')==4
assert s.count('<details>')==4 and '<details open' not in s
for text in ['chirurgicale','perturbations minimisées','retour arrière','intensivement l’IA','revus, testés et validés','confidentialité','peut intégrer de l’IA','autonomie','accord commercial','temps libéré']:assert text in s,text
assert 'quelles que soient les technologies' not in s and '<video' not in s and '.gif' not in s
nav=re.search(r'<nav\b.*?</nav>',s,re.S)[0];assert nav.count('<a ')==5
files=list(ROOT.glob('*.html'))+[ROOT/'i18n/static.json',ROOT/'i18n/messages.json']
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();subprocess.run([sys.executable,str(ROOT/'scripts/build_pedagogy.py')],check=True,stdout=subprocess.DEVNULL);assert hashes()==before
print('PASS V12: diagnostic/conditions/deliverables visible, section order, four steps, two CTA, four native disclosures, IA uses, preserved anchors/menu and idempotent generation.')
