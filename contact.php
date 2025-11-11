<?php

declare(strict_types=1);

$contactAddress = 'patrick.lyonnet@cln-solutions.fr';
$fallbackRedirect = 'contact.html';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: ' . $fallbackRedirect, true, 303);
    exit;
}

function field_value(string $key): string
{
    return trim(str_replace(["\r", "\n"], '', (string)($_POST[$key] ?? '')));
}

$name = field_value('name');
$email = field_value('_replyto');
$company = field_value('company');
$message = trim((string)($_POST['message'] ?? ''));
$consent = isset($_POST['consent']);

if ($message !== '') {
    $message = preg_replace("/\r\n|\r|\n/", "\r\n", $message);
}

$isEmailValid = filter_var($email, FILTER_VALIDATE_EMAIL);

if ($name === '' || !$isEmailValid || $message === '' || !$consent) {
    header('Location: contact.html?status=invalid', true, 303);
    exit;
}

$subject = 'Demande de contact CLN - ' . $name;

if (function_exists('mb_encode_mimeheader')) {
    $subject = mb_encode_mimeheader($subject, 'UTF-8');
}

$bodyLines = [
    "Nom et prénom : {$name}",
    "Email : {$email}",
    $company !== '' ? "Organisation : {$company}" : 'Organisation : (non renseignée)',
    "Consentement : oui",
    '',
    'Message :',
    $message,
    '',
    '—',
    'Message envoyé depuis le formulaire CLN (cln-solutions.fr).'
];

$body = implode("\r\n", $bodyLines);

$headers = [
    'From: CLN <' . $contactAddress . '>',
    'Reply-To: ' . $email,
    'X-Mailer: PHP/' . PHP_VERSION,
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit'
];

$sent = mail($contactAddress, $subject, $body, implode("\r\n", $headers));

if ($sent) {
    header('Location: merci.html?status=success', true, 303);
    exit;
}

header('Location: contact.html?status=error', true, 303);
exit;
