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
// Credentials and mailer live outside the public web root.
try {
    $privateRoot = dirname(__DIR__);
    $configPath = $privateRoot . '/.cln-secrets/mail.json';
    $autoload = $privateRoot . '/.cln-mailer/7.1.1/autoload.php';
    if (!is_readable($configPath) || !is_readable($autoload)) {
        throw new RuntimeException('SMTP configuration unavailable');
    }
    $config = json_decode(file_get_contents($configPath), true, 8, JSON_THROW_ON_ERROR);
    if (!is_array($config) || !is_string($config['password'] ?? null) || $config['password'] === '') {
        throw new RuntimeException('SMTP credential unavailable');
    }
    require_once $autoload;
    $mail = new \PHPMailer\PHPMailer\PHPMailer(true);
    $mail->isSMTP();
    $mail->Host = 'ssl0.ovh.net';
    $mail->Port = 465;
    $mail->SMTPSecure = \PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS;
    $mail->SMTPAuth = true;
    $mail->Username = CONTACT;
    $mail->Password = $config['password'];
    $mail->SMTPDebug = 0;
    $mail->Timeout = 20;
    $mail->CharSet = 'UTF-8';
    $mail->Encoding = 'base64';
    $mail->setFrom(CONTACT, 'CLN Performance');
    $mail->Sender = CONTACT;
    $mail->addAddress(CONTACT);
    $mail->addReplyTo($email, $name);
    $mail->Subject = 'Demande de contact CLN Performance';
    $mail->Body = $body;
    $mail->send();
} catch (\Throwable $error) {
    // Never expose SMTP diagnostics, credentials or visitor content.
    error_log('CLN contact: authenticated SMTP send failed');
    finish('error');
}
// SMTP acceptance still requires an independent mailbox delivery check.
finish('success');
