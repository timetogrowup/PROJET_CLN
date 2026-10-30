from pathlib import Path
import re,json,sys,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from case_journey import FIELDS
names=['index','solutions','pipelines','approche','realisations','diagnostic','contact','merci','mentions-legales','confidentialite']
for name in names:
 s=(ROOT/(name+'.html')).read_text();nav=re.search(r'<nav\b.*?</nav>',s,re.S)[0]
 assert len(re.findall(r'<a\b',nav))==5 and 'solutions.html' not in nav and 'realisations.html' not in nav
 assert 'Et si on étudiait votre cas ?' in nav
 assert 'Faire le point' not in re.sub(r'<script.*?</script>','',s,flags=re.S)
for name in ['solutions','realisations']:assert (ROOT/(name+'.html')).exists()
q=(ROOT/'diagnostic.html').read_text();c=(ROOT/'contact.html').read_text();messages=json.loads((ROOT/'i18n/messages.json').read_text())
for name,label,title,multi,options in FIELDS:
 assert f'name="{name}"' in q
 for code,labels in options:
  assert f'value="{code}"' in q and set(messages['case.choice.'+name+'.'+code])=={'fr','en','pt-BR','es'}
assert 'maxlength="2000"' in q and 'id="case-transfer-fallback"' in q
assert 'name="message"' in c and 'for="message">Votre situation</label>' in c and 'diagnostic.js' not in c
assert 'recommendation-add' not in c and 'need-add' not in c
assert 'case-data.js' in q and 'case-data.js' in c
assert '$message\\r\\n\\r\\nFormulaire' in (ROOT/'contact.php').read_text()
assert "sessionStorage.setItem('clnCaseTransfer'" in (ROOT/'diagnostic.js').read_text()
assert 'localStorage' not in (ROOT/'diagnostic.js').read_text()
# Generation must preserve all ten outputs and both catalogues on a second pass.
files=[ROOT/(n+'.html') for n in names]+[ROOT/'i18n/static.json',ROOT/'i18n/messages.json']
def hashes():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();subprocess.run([sys.executable,str(ROOT/'scripts/build_pedagogy.py')],check=True,stdout=subprocess.DEVNULL);assert hashes()==before
print('PASS V11 static: ten five-link menus, retained pages, seven coded groups and optional free text, localized labels, shared data contract, native message/email contract and idempotent generation.')
