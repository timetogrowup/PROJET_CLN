import json,subprocess,tempfile,pathlib,urllib.request,urllib.error,urllib.parse,time,shutil,os
root=pathlib.Path(__file__).resolve().parents[1];private=root.parent/'.cln-secrets'
if private.exists():raise RuntimeError('Test fixture path already exists; refusing to overwrite')
private.mkdir(mode=0o700);(private/'mail.json').write_text(json.dumps({'password':'test-only-not-a-real-password','security_key':'a'*64}));shutil.copy(root/'contact_security.php',private/'contact_security.php')
class Stop(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*a,**k):return None
opener=urllib.request.build_opener(Stop)
server=subprocess.Popen(['php','-S','127.0.0.1:8080','-t',str(root)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def request(path='',data=None,origin='https://cln-performance.com'):
 h={} if origin is None else {'Origin':origin}
 req=urllib.request.Request('http://127.0.0.1:8080/contact.php'+path,data=None if data is None else urllib.parse.urlencode(data).encode(),headers=h)
 try:r=opener.open(req,timeout=5)
 except urllib.error.HTTPError as e:r=e
 return r.code,r.headers,r.read().decode()
try:
 for _ in range(30):
  try:request();break
  except OSError:time.sleep(.1)
 code,h,b=request();assert code==405 and h.get('Allow')=='POST'
 code,h,b=request('?op=challenge');c=json.loads(b);assert code==200 and h['Access-Control-Allow-Origin']=='https://cln-performance.com' and c['a']+c['b']<=18
 assert 'password' not in b and 'security_key' not in b
 assert request('?op=challenge',origin='https://evil.invalid')[0]==403
 base={'name':'Test','_replyto':'contact@cln-performance.com','company':'','message':'Test without sending','consent':'on','lang':'es'}
 code,h,b=request(data=base);assert code==303 and 'status=captcha_required' in h['Location'] and 'lang=es' in h['Location']
 code,h,b=request(data=dict(base,captcha_token=c['token'],captcha_answer='99'));assert 'status=captcha_invalid' in h['Location']
 code,h,b=request(data=dict(base,lang='https://evil.invalid'));assert 'lang=fr' in h['Location'] and 'evil' not in h['Location']
 code,h,b=request(data=base,origin='https://evil.invalid');assert 'status=forbidden' in h['Location']
 code,h,b=request(data={'name[]':'array','lang':'en'});assert 'status=invalid' in h['Location']
 code,h,b=request(data={'message':'a'*21000});assert 'status=too_large' in h['Location']
 print('PASS HTTP: CORS, challenge, field types, payload limit, localised redirects and missing/invalid CAPTCHA. No mail sent.')
finally:
 server.terminate();server.wait(timeout=5);shutil.rmtree(private)
