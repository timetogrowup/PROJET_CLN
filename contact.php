<?php
declare(strict_types=1);
// Deploy this file to OVHcloud's www directory. GitHub Pages cannot execute PHP.
const SITE = 'https://cln-performance.com';
const CONTACT = 'contact@cln-performance.com';
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
function finish(string $status): never {
    $page = $status === 'success' ? '/merci.html' : '/contact.html';
    header('Location: ' . SITE . $page . '?status=' . $status, true, 303);
    exit;
}
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    http_response_code(405);
    exit('Utilisez le formulaire de contact.');
}
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 20000) {
    http_response_code(413);
    exit('Demande trop volumineuse.');
}
// Browser submissions must originate from our site; this is not a bot-proof credential.
if (!in_array($_SERVER['HTTP_ORIGIN'] ?? '', [SITE, 'https://www.cln-performance.com'], true)) {
    http_response_code(403);
    exit('Origine non autorisée.');
}
function value(string $key): string {
    $v = $_POST[$key] ?? '';
    return is_string($v) ? trim($v) : '';
}
$name = value('name');
$email = value('_replyto');
$company = value('company');
$message = value('message');
if (value('website') !== '') {
    http_response_code(400);
    exit('Demande non acceptée.');
}
if ($name === '' || strlen($name) > 200 || strlen($company) > 300 ||
    !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 254 ||
    preg_match('/[\r\n\x00]/', $name . $email . $company) ||
    $message === '' || strlen($message) > 10000 || value('consent') !== 'on') {
    finish('invalid');
}
// Private, locked rolling-window counters outside the web root. Never trust X-Forwarded-For.
$dir = sys_get_temp_dir() . '/cln-contact-' . substr(hash('sha256', __DIR__), 0, 16);
if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) finish('error');
$path = $dir . '/' . hash('sha256', $_SERVER['REMOTE_ADDR'] ?? 'unknown') . '.json';
$handle = @fopen($path, 'c+');
if (!$handle || !flock($handle, LOCK_EX)) finish('error');
$now = time();
$times = json_decode(stream_get_contents($handle), true);
$times = is_array($times) ? array_values(array_filter($times, fn($t) => is_int($t) && $t > $now - 3600)) : [];
if (count($times) >= 5 || ($times && max($times) > $now - 60)) {
    flock($handle, LOCK_UN); fclose($handle);
    header('Retry-After: 60'); http_response_code(429);
    exit('Trop de demandes. Réessayez plus tard ou contactez-nous par email.');
}
$times[] = $now;
ftruncate($handle, 0); rewind($handle); fwrite($handle, json_encode($times));
flock($handle, LOCK_UN); fclose($handle);
$body = "Nom : $name\r\nEmail : $email\r\nOrganisation : $company\r\nConsentement : oui\r\n\r\n$message\r\n\r\nFormulaire cln-performance.com";
$headers = ['From: CLN Performance <' . CONTACT . '>', 'Reply-To: ' . $email,
    'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8'];
// mail() acceptance is not proof of mailbox delivery. Verify receipt before enabling the form.
$sent = @mail(CONTACT, 'Demande de contact CLN Performance', $body, implode("\r\n", $headers));
if (!$sent) error_log('CLN contact: mail transport failed');
finish($sent ? 'success' : 'error');
