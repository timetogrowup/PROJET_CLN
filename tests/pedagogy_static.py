"""Link/anchor, metadata and complete translation checks for shipped HTML."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(convert_charrefs=True);self.ids=set();self.links=[];self.stack=[];self.text=[];self.h1=0;self.title=False;self.meta=False;self.feed(path.read_text())
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs);self.stack.append((tag,attrs)) if tag not in ['meta','link','img','input','br','hr'] else None
  if 'id' in attrs:assert attrs['id'] not in self.ids,attrs['id'];self.ids.add(attrs['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='meta' and attrs.get('name')=='description':self.meta=True;self.text.append(attrs.get('content',''))
  for a in ['alt','placeholder','aria-label']:
   if attrs.get(a):self.text.append(attrs[a])
  if tag in ['a','link','script','img']:
   url=attrs.get('href',attrs.get('src',''));self.links.append(url)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,s):
  if any(t in ['script','style','noscript'] or 'data-dynamic' in a or 'data-msg' in a for t,a in self.stack):return
  s=re.sub(r'\s+',' ',s).strip()
  if s:self.text.append(s)
root=Path(__file__).resolve().parents[1];names=['index','solutions','pipelines','approche','realisations','diagnostic','contact','merci','mentions-legales','confidentialite'];pages={n+'.html':Page(root/(n+'.html')) for n in names};catalog=json.loads((root/'i18n/static.json').read_text())
for required in ['recommendation-add','need-context','need-add','human-dialog','contact-form']:
 assert required in pages['contact.html'].ids,required
for name,page in pages.items():
 scripts=[urlsplit(u).path for u in page.links if urlsplit(u).path.endswith('.js')]
 assert len(scripts)==len(set(scripts)),(name,'duplicate scripts')
links=0;missing=set()
for name,page in pages.items():
 assert page.h1==1,(name,'h1',page.h1)
 assert page.title and page.meta,(name,'metadata')
 assert 'main-content' in page.ids,(name,'skip link target')
 for url in page.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  target=unquote(u.path) or name
  assert (root/target).exists(),(name,url)
  if u.fragment and target in pages:assert u.fragment in pages[target].ids,(name,url,'anchor')
  links+=1
 for text in page.text:
  if text in catalog or not re.search(r'[A-Za-zÀ-ÿ]',text) or text.startswith(('+33','contact@')) or text in ['Email :','Téléphone :','.']:continue
  missing.add((name,text))
assert not missing,'Missing translations: '+repr(sorted(missing))
for key in ['ressaisies','repetitif','chiffres','suivi']:assert key in pages['solutions.html'].ids
for name in ['index','solutions','pipelines','approche','realisations','contact']:
 text=(root/(name+'.html')).read_text();assert 'chirurgicale' not in text and '40 %' not in text and '60 %' not in text
print('PASS',len(pages),'pages,',links,'local references/anchors, metadata, skip links and complete visible translation coverage.')

# V5 structural invariants for the explanatory page and shared menu.
pipeline=(root/'pipelines.html').read_text()
assert pipeline.count('class="pipeline-case"')==4
assert 'class="pipeline-steps"' in pipeline and 'id="exemple"' in pipeline
for anchor in ['capacites','situations','equipes','benefices']:
 assert anchor in pages['pipelines.html'].ids,anchor
assert 'bout-en-bout' in pages['solutions.html'].ids
assert 'pipeline' in pages['approche.html'].ids
assert 'pipelines' in pages['index.html'].ids
for name in pages:
 text=(root/name).read_text()
 nav=re.search(r'<nav\b.*?</nav>',text,re.S).group(0)
 assert len(re.findall(r'<a\b',nav))==7,(name,'seven navigation links')
 assert 'pipelines.html' in nav,(name,'pipeline navigation')
import xml.etree.ElementTree as ET
urls={node.text for node in ET.parse(root/'sitemap.xml').iter() if node.tag.endswith('}loc')}
assert 'https://cln-performance.com/pipelines.html' in urls
print('PASS V5 pipeline structure, seven-link shared navigation and sitemap.')
