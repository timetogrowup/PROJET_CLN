<?php
declare(strict_types=1);
const SITE='https://cln-performance.com';
const CONTACT='contact@cln-performance.com';
header('Cache-Control: no-store');header('X-Content-Type-Options: nosniff');
function value(string $key,array $from=[]): string { $v=($from?:$_POST)[$key]??'';return is_string($v)?trim($v):''; }
$lang=value('lang',$_POST?:$_GET);if(!in_array($lang,['fr','en','pt-BR','es'],true))$lang='fr';
function finish(string $status,int $wait=0): never {
    global $lang;
    $page=$status==='success'?'/merci.html':'/contact.html';
    $args=['status'=>$status,'lang'=>$lang];if($wait>0){$args['wait']=min(3600,$wait);header('Retry-After: '.min(3600,$wait));}
    header('Location: '.SITE.$page.'?'.http_build_query($args),true,303);exit;
}
$origin=$_SERVER['HTTP_ORIGIN']??'';
$allowed=in_array($origin,[SITE,'https://www.cln-performance.com'],true);
$challenge=($_SERVER['REQUEST_METHOD']??'')==='GET'&&value('op',$_GET)==='challenge';
if($challenge){
    header('Content-Type: application/json; charset=utf-8');header('Vary: Origin');
    if(!$allowed){http_response_code(403);exit(json_encode(['error'=>'forbidden']));}
    header('Access-Control-Allow-Origin: '.$origin);
} elseif(($_SERVER['REQUEST_METHOD']??'')!=='POST') {header('Allow: POST');http_response_code(405);exit;}
if(!$allowed)finish('forbidden');
if((int)($_SERVER['CONTENT_LENGTH']??0)>20000)finish('too_large');
try {
    $root=dirname(__DIR__).'/.cln-secrets';
    // The optional path is accepted only in CLI tests, never from an HTTP parameter.
    if(PHP_SAPI==='cli'&&getenv('CLN_TEST_PRIVATE_ROOT'))$root=getenv('CLN_TEST_PRIVATE_ROOT');
    $config=json_decode(file_get_contents($root.'/mail.json'),true,8,JSON_THROW_ON_ERROR);
    if(!is_array($config)||!is_string($config['security_key']??null)||!is_string($config['password']??null))throw new RuntimeException('Configuration unavailable');
    require_once $root.'/contact_security.php';
    $security=new CLNSecurity($root.'/contact-state.json',$config['security_key']);
    if($challenge)exit(json_encode($security->challenge(time()),JSON_THROW_ON_ERROR));
    $name=value('name');$email=value('_replyto');$company=value('company');$message=value('message');
    if(value('website')!=='')finish('invalid');
    if($name===''||strlen($name)>800||strlen($company)>1200||strlen($message)>40000||$message===''||strlen($email)>254||!filter_var($email,FILTER_VALIDATE_EMAIL)||preg_match('/[\r\n\x00]/',$name.$email.$company)||value('consent')!=='on')finish('invalid');
    // Character limits match maxlength while the overall request retains its 20 kB cap.
    if(mb_strlen($name,'UTF-8')>200||mb_strlen($company,'UTF-8')>300||mb_strlen($message,'UTF-8')>10000)finish('invalid');
    $token=value('captcha_token');$answer=value('captcha_answer');if($token===''||$answer==='')finish('captcha_required');
    $result=$security->submit($email,$_SERVER['REMOTE_ADDR']??'unknown',$token,$answer,time(),function()use($config,$name,$email,$company,$message,$lang){
        require_once dirname(__DIR__).'/.cln-mailer/7.1.1/autoload.php';
        $mail=new \PHPMailer\PHPMailer\PHPMailer(true);$mail->isSMTP();$mail->Host='ssl0.ovh.net';$mail->Port=465;$mail->SMTPSecure=\PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS;$mail->SMTPAuth=true;$mail->Username=CONTACT;$mail->Password=$config['password'];$mail->SMTPDebug=0;$mail->Timeout=15;$mail->Timelimit=20;$mail->CharSet='UTF-8';$mail->Encoding='base64';$mail->setFrom(CONTACT,'CLN Performance');$mail->Sender=CONTACT;$mail->addAddress(CONTACT);$mail->addReplyTo($email,$name);$mail->Subject='Demande de contact CLN Performance';
        $names=['fr'=>'Français','en'=>'English','pt-BR'=>'Português (Brasil)','es'=>'Español'];
        $mail->Body="Langue souhaitée : ".$names[$lang]."\r\nNom : $name\r\nEmail : $email\r\nOrganisation : $company\r\nInformation confidentialité : lue\r\n\r\n$message\r\n\r\nFormulaire cln-performance.com";
        return $mail->send();
    });
    finish($result['status'],(int)($result['wait']??0));
} catch(Throwable $error){
    error_log('CLN contact: secure processing failed');
    if($challenge){http_response_code(503);exit(json_encode(['error'=>'unavailable']));}
    finish('error');
}
