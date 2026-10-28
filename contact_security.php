<?php
declare(strict_types=1);
/** Shared production/test security core. Never stores an email or IP in clear text. */
final class CLNSecurity {
    public function __construct(private string $path, private string $key) {
        if (strlen($key) < 32) throw new RuntimeException('Missing security key');
    }
    private static function encode(string $s): string { return rtrim(strtr(base64_encode($s), '+/', '-_'), '='); }
    public function challenge(int $now): array {
        $a=random_int(1,9); $b=random_int(1,9); $id=bin2hex(random_bytes(16)); $expires=$now+600;
        $sig=hash_hmac('sha256', $id.'|'.$expires.'|'.($a+$b), $this->key);
        return ['a'=>$a,'b'=>$b,'expires'=>$expires,'token'=>self::encode(json_encode(['id'=>$id,'expires'=>$expires,'sig'=>$sig],JSON_THROW_ON_ERROR))];
    }
    private function verify(string $token,string $answer,int $now): ?array {
        if(strlen($token)>512||!preg_match('/^[A-Za-z0-9_-]+$/D',$token)||!preg_match('/^\d{1,2}$/D',$answer)) return null;
        $raw=base64_decode(strtr($token,'-_','+/'),true);if($raw===false)return null;
        $data=json_decode($raw,true);
        if(!is_array($data)||!is_string($data['id']??null)||!preg_match('/^[a-f0-9]{32}$/D',$data['id'])||!is_int($data['expires']??null)||!is_string($data['sig']??null))return null;
        if($data['expires']<=$now||$data['expires']>$now+600)return null;
        $sig=hash_hmac('sha256',$data['id'].'|'.$data['expires'].'|'.((int)$answer),$this->key);
        return hash_equals($sig,$data['sig'])?$data:null;
    }
    private function fingerprint(string $kind,string $value): string {return hash_hmac('sha256',$kind.'|'.$value,$this->key);}
    private function save($file,array $state): void {
        $json=json_encode($state,JSON_THROW_ON_ERROR);rewind($file);
        if(!ftruncate($file,0)||fwrite($file,$json)!==strlen($json)||!fflush($file))throw new RuntimeException('State write failed');
    }
    private function purge(array &$state,int $now): void {
        foreach(['email','ip','attempts'] as $kind){
            foreach($state[$kind] as $id=>$times){$times=array_values(array_filter($times,fn($t)=>is_int($t)&&$t>$now-3600));if($times)$state[$kind][$id]=$times;else unset($state[$kind][$id]);}
        }
        foreach($state['used'] as $id=>$expires)if(!is_int($expires)||$expires<=$now)unset($state['used'][$id]);
    }
    private function delay(array $times,int $now,int $gap,int $limit): int {
        sort($times);$wait=$times?max(0,max($times)+$gap-$now):0;
        if(count($times)>=$limit)$wait=max($wait,$times[count($times)-$limit]+3600-$now);
        return $wait;
    }
    /** The short SMTP transaction is protected by the same inter-process lock. */
    public function submit(string $email,string $ip,string $token,string $answer,int $now,callable $send): array {
        $file=@fopen($this->path,'c+');if(!$file)throw new RuntimeException('State unavailable');
        @chmod($this->path,0600);
        try {
            if(!flock($file,LOCK_EX))throw new RuntimeException('Lock unavailable');
            $raw=stream_get_contents($file);
            $state=$raw===''?['email'=>[],'ip'=>[],'used'=>[],'attempts'=>[]]:json_decode($raw,true,512,JSON_THROW_ON_ERROR);
            foreach(['email','ip','used','attempts'] as $kind)if(!isset($state[$kind])||!is_array($state[$kind]))throw new RuntimeException('Invalid state');
            $this->purge($state,$now);
            $mail=$this->fingerprint('email',strtolower(trim($email)));$address=$this->fingerprint('ip',$ip);
            $attempts=$state['attempts'][$address]??[];
            if(count($attempts)>=30){$this->save($file,$state);return ['status'=>'rate','wait'=>max(1,min($attempts)+3600-$now)];}
            $state['attempts'][$address][]=$now;
            $challenge=$this->verify($token,$answer,$now);
            if(!$challenge){$this->save($file,$state);return ['status'=>'captcha_invalid'];}
            if(isset($state['used'][$challenge['id']])){$this->save($file,$state);return ['status'=>'captcha_used'];}
            $state['used'][$challenge['id']]=$challenge['expires'];
            $wait=max($this->delay($state['email'][$mail]??[],$now,600,3),$this->delay($state['ip'][$address]??[],$now,60,5));
            // Persist consumption before SMTP so a crash cannot replay the challenge.
            $this->save($file,$state);
            if($wait>0)return ['status'=>'rate','wait'=>$wait];
            try {$accepted=$send();} catch(Throwable $error) {$accepted=false;}
            if(!$accepted)return ['status'=>'error'];
            $state['email'][$mail][]=$now;$state['ip'][$address][]=$now;
            $this->save($file,$state);
            return ['status'=>'success'];
        } finally {flock($file,LOCK_UN);fclose($file);}
    }
}
