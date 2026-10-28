<?php
declare(strict_types=1);
require __DIR__.'/../contact_security.php';
$dir=sys_get_temp_dir().'/cln-test-'.bin2hex(random_bytes(8));mkdir($dir,0700);
$key=str_repeat('k',64);$checks=0;
function check(bool $condition,string $label):void{global $checks;if(!$condition)throw new RuntimeException('FAIL '.$label);$checks++;}
function core(string $name):CLNSecurity{global $dir,$key;return new CLNSecurity($dir.'/'.$name.'.json',$key);}
function send(CLNSecurity $s,string $email,int $time,string $ip='192.0.2.1',?array $c=null,?callable $transport=null):array{$c??=$s->challenge($time);return $s->submit($email,$ip,$c['token'],'1',$time,$transport??fn()=>true);}
$t=1000000;$s=core('human');$c=$s->challenge($t);
check(!isset($c['a'])&&!isset($c['b']),'no arithmetic payload');
check($s->submit('test@example.invalid','192.0.2.9',$c['token'],'0',$t,fn()=>throw new Exception('Must not send'))['status']==='human_invalid','unchecked blocks SMTP');
$legacy=['id'=>str_repeat('a',32),'expires'=>$t+600,'sig'=>hash_hmac('sha256',str_repeat('a',32).'|'.($t+600).'|1',$key)];$legacyToken=rtrim(strtr(base64_encode(json_encode($legacy)),'+/','-_'),'=');
check($s->submit('test@example.invalid','192.0.2.8',$legacyToken,'1',$t,fn()=>throw new Exception('Must not send'))['status']==='human_invalid','legacy purpose rejected');
$r=$s->submit('test@example.invalid','192.0.2.1',$c['token'],'99',$t,fn()=>throw new Exception('Must not send'));check($r['status']==='human_invalid','unchecked confirmation');
check(send($s,'test@example.invalid',$t,'192.0.2.1',$c)['status']==='success','invalid does not consume send quota');
check(send($s,'other@example.invalid',$t+61,'192.0.2.2',$c)['status']==='human_used','single use');
$c=$s->challenge($t);check(send($s,'a@example.invalid',$t+600,'192.0.2.3',$c)['status']==='human_invalid','expiry at boundary');
$c=$s->challenge($t);$c['token'].='x';check(send($s,'b@example.invalid',$t,'192.0.2.4',$c)['status']==='human_invalid','forged token');
$s=core('email');check(send($s,'User@Example.invalid',$t)['status']==='success','first');
$r=send($s,' user@example.INVALID ',$t+599,'192.0.2.2');check($r['status']==='rate'&&$r['wait']===1,'normalisation and different IP');
check(send($s,'USER@example.invalid',$t+600,'192.0.2.2')['status']==='success','gap exact');
check(send($s,'user@example.invalid',$t+1200)['status']==='success','third');
$r=send($s,'user@example.invalid',$t+1800);check($r['status']==='rate'&&$r['wait']===1800,'fourth hourly');
check(send($s,'user@example.invalid',$t+3600)['status']==='success','rolling window expiry');
$s=core('aliases');check(send($s,'a.b@example.invalid',$t)['status']==='success','dotted address');check(send($s,'ab@example.invalid',$t+61)['status']==='success','dots not merged');check(send($s,'a+b@example.invalid',$t+122)['status']==='success','plus suffix not merged');
$s=core('smtp');check(send($s,'test@example.invalid',$t,'192.0.2.1',null,fn()=>false)['status']==='error','SMTP failure');check(send($s,'test@example.invalid',$t)['status']==='success','failure does not consume quota');
$s=core('ip');send($s,'one@example.invalid',$t);$r=send($s,'two@example.invalid',$t+1);check($r['status']==='rate'&&$r['wait']===59,'IP rule retained');
$s=core('abuse');for($i=0;$i<30;$i++)$s->submit('a@example.invalid','192.0.2.1','bad','0',$t,fn()=>true);check(send($s,'a@example.invalid',$t)['status']==='rate','attempt throttle');
$raw=file_get_contents($dir.'/email.json');check(!str_contains(strtolower($raw),'example.invalid')&&!str_contains($raw,'192.0.2.'),'no plaintext identifiers');
$s=core('purge');send($s,'expired@example.invalid',$t);send($s,'fresh@example.invalid',$t+4000);$state=json_decode(file_get_contents($dir.'/purge.json'),true);check(count($state['email'])===1&&count($state['used'])===1,'expiry cleanup');
file_put_contents($dir.'/corrupt.json','bad');try{send(core('corrupt'),'a@example.invalid',$t);check(false,'corruption must fail closed');}catch(JsonException $e){check(true,'corruption fails closed');}
if(!function_exists('pcntl_fork'))throw new RuntimeException('Concurrency test requires pcntl');
$s=core('concurrent');$tokens=[$s->challenge($t),$s->challenge($t)];$children=[];
for($i=0;$i<2;$i++){$pid=pcntl_fork();if($pid===0){$r=send($s,'same@example.invalid',$t,'192.0.2.'.($i+1),$tokens[$i],function()use($dir){file_put_contents($dir.'/mails','sent\n',FILE_APPEND|LOCK_EX);usleep(150000);return true;});file_put_contents($dir.'/result'.$i,$r['status']);exit;}if($pid<0)throw new RuntimeException('fork');$children[]=$pid;}
foreach($children as $pid)pcntl_waitpid($pid,$status);
$results=[file_get_contents($dir.'/result0'),file_get_contents($dir.'/result1')];sort($results);check($results===['rate','success'],'concurrent submissions');check(substr_count(file_get_contents($dir.'/mails'),'sent')===1,'only one transport call');
foreach(glob($dir.'/*')as $p)unlink($p);rmdir($dir);echo 'PASS '.$checks." security checks including concurrency; no real email sent.\n";
