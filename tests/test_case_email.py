"""Exercise the unchanged PHP endpoint with a local mailer double; no SMTP connection."""
import json,subprocess,tempfile,pathlib,urllib.request,urllib.error,urllib.parse,time,shutil,os,socket,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='cln-case-mail-') as tmp:
 base=pathlib.Path(tmp);www=base/'www';www.mkdir();private=base/'.cln-secrets';private.mkdir();mailer=base/'.cln-mailer/7.1.1';mailer.mkdir(parents=True)
 shutil.copy(ROOT/'contact.php',www/'contact.php');shutil.copy(ROOT/'contact_security.php',private/'contact_security.php')
 (private/'mail.json').write_text(json.dumps({'password':'fixture-only','security_key':'a'*64}))
 capture=base/'captured.json';fixtures=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else base/'fixtures.json'
 if len(sys.argv)==1:subprocess.run(['node','tests/case-journey.mjs',str(fixtures)],cwd=ROOT,check=True)
 (mailer/'autoload.php').write_text('''<?php
 namespace PHPMailer\\PHPMailer;
 #[\\AllowDynamicProperties]
 class PHPMailer {
  const ENCRYPTION_SMTPS='ssl';
  function __construct($throws=true){}
  function isSMTP(){}
  function setFrom($address,$name){}
  function addAddress($address){}
  function addReplyTo($address,$name){}
  function send(){file_put_contents(getenv('CLN_TEST_CAPTURE'),json_encode(['body'=>$this->Body,'subject'=>$this->Subject],JSON_UNESCAPED_UNICODE));return true;}
 }
 ''')
 class Stop(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args,**kwargs):return None
 opener=urllib.request.build_opener(Stop)
 with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
 env=dict(os.environ,CLN_TEST_CAPTURE=str(capture));server=subprocess.Popen(['php','-S',f'127.0.0.1:{port}','-t',str(www)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 def request(query='',data=None):
  req=urllib.request.Request(f'http://127.0.0.1:{port}/contact.php'+query,headers={'Origin':'https://cln-performance.com'},data=None if data is None else urllib.parse.urlencode(data).encode())
  try:return opener.open(req,timeout=5)
  except urllib.error.HTTPError as error:return error
 try:
  for attempt in range(40):
   try:request();break
   except OSError:time.sleep(.05)
  rows=json.loads(fixtures.read_text())
  for row in rows:
   # Independent test cases, each with its own security fixture state.
   (private/'contact-state.json').unlink(missing_ok=True)
   r=request('?op=human');assert r.code==200;token=json.loads(r.read())['token']
   payload={'name':'Test local','_replyto':'fixture@example.invalid','company':'Entreprise fictive','message':row['message'],'lang':row['lang'],'consent':'on','human_token':token,'human_confirmed':'1'}
   r=request(data=payload);assert r.code==303 and 'status=success' in r.headers['Location'],(r.code,r.headers,r.read())
   mail=json.loads(capture.read_text());assert row['message'].strip() in mail['body'];assert 'Correction personnelle : éèà <script>texte seulement</script>.' in mail['body'];assert mail['subject']=='Demande de contact CLN Performance'
  print('PASS V11 PHP email: actual endpoint and security, four edited/localized situations included verbatim in captured mail bodies. Local mailer double only; no SMTP/email.')
 finally:server.terminate();server.wait(timeout=5)
