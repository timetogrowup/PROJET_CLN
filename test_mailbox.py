#!/usr/bin/env python3
"""
Utility to send a test email through a mailbox and optionally confirm its reception.

Example:
    $ python test_mailbox.py \\
        --smtp-host smtp.hostinger.com --smtp-port 465 --smtp-ssl \\
        --imap-host imap.hostinger.com --imap-port 993 \\
        --user patrick.lyonnet@cln-solutions.fr --password '***' \\
        --recipient patrick.lyonnet@cln-solutions.fr

Environment variables can provide any option (prefix TEST_MAILBOX_*).
For instance export TEST_MAILBOX_USER, TEST_MAILBOX_PASSWORD, etc.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
import ssl
from dataclasses import dataclass
from email import message_from_bytes
from email.message import EmailMessage
from imaplib import IMAP4, IMAP4_SSL
from smtplib import SMTP, SMTP_SSL
from typing import Optional


ENV_PREFIX = "TEST_MAILBOX_"


def env_default(name: str, fallback: Optional[str] = None) -> Optional[str]:
    """Read a default value from the environment."""
    return os.getenv(f"{ENV_PREFIX}{name}", fallback)


@dataclass
class MailboxConfig:
    user: str
    password: str
    smtp_host: str
    smtp_port: int
    smtp_ssl: bool
    smtp_starttls: bool
    imap_host: Optional[str]
    imap_port: Optional[int]
    recipient: str
    wait_seconds: int
    subject_prefix: str
    debug: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send a test email and verify reception.")
    parser.add_argument("--user", default=env_default("USER"), help="Mailbox username / email.")
    parser.add_argument(
        "--password",
        default=env_default("PASSWORD"),
        help="Mailbox password (or app-specific password).",
    )
    parser.add_argument(
        "--recipient",
        default=env_default("RECIPIENT"),
        help="Recipient email address. Defaults to the mailbox user.",
    )
    parser.add_argument(
        "--smtp-host",
        default=env_default("SMTP_HOST", "smtp.hostinger.com"),
        help="SMTP server hostname.",
    )
    parser.add_argument(
        "--smtp-port",
        type=int,
        default=int(env_default("SMTP_PORT", "465")),
        help="SMTP server port.",
    )
    parser.add_argument(
        "--smtp-ssl",
        action="store_true",
        default=env_default("SMTP_SSL", "true").lower() in {"1", "true", "yes"},
        help="Use SMTP over SSL (default: true).",
    )
    parser.add_argument(
        "--smtp-starttls",
        action="store_true",
        default=env_default("SMTP_STARTTLS", "false").lower() in {"1", "true", "yes"},
        help="Upgrade SMTP connection with STARTTLS (default: false).",
    )
    parser.add_argument(
        "--imap-host",
        default=env_default("IMAP_HOST", "imap.hostinger.com"),
        help="IMAP server hostname (skip to disable reception check).",
    )
    parser.add_argument(
        "--imap-port",
        type=int,
        default=int(env_default("IMAP_PORT", "993")),
        help="IMAP server port.",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=int(env_default("WAIT_SECONDS", "30")),
        help="Seconds to wait for the message on IMAP (default: 30).",
    )
    parser.add_argument(
        "--subject-prefix",
        default=env_default("SUBJECT_PREFIX", "[CLN mailbox test]"),
        help="Prefix to use in the test email subject.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=env_default("DEBUG", "false").lower() in {"1", "true", "yes"},
        help="Enable verbose SMTP/IMAP debug output.",
    )

    return parser


def validate_args(args: argparse.Namespace) -> MailboxConfig:
    if not args.user:
        raise SystemExit("Missing --user (or TEST_MAILBOX_USER).")
    if not args.password:
        raise SystemExit("Missing --password (or TEST_MAILBOX_PASSWORD).")

    recipient = args.recipient or args.user

    return MailboxConfig(
        user=args.user,
        password=args.password,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        smtp_ssl=args.smtp_ssl,
        smtp_starttls=args.smtp_starttls,
        imap_host=args.imap_host,
        imap_port=args.imap_port,
        recipient=recipient,
        wait_seconds=max(0, args.wait),
        subject_prefix=args.subject_prefix,
        debug=args.debug,
    )


def send_email(cfg: MailboxConfig, token: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = f"{cfg.subject_prefix} {token}"
    message["From"] = cfg.user
    message["To"] = cfg.recipient
    message.set_content(
        f"""Bonjour,

Ce message automatique vérifie l'envoi depuis {cfg.user}.
Identifiant: {token}

Cordialement.
"""
    )

    if cfg.smtp_ssl:
        smtp_client: SMTP = SMTP_SSL(cfg.smtp_host, cfg.smtp_port, timeout=30)
    else:
        smtp_client = SMTP(cfg.smtp_host, cfg.smtp_port, timeout=30)

    with smtp_client as server:
        if cfg.debug:
            server.set_debuglevel(1)
        server.ehlo()
        if cfg.smtp_starttls and not cfg.smtp_ssl:
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.ehlo()
        server.login(cfg.user, cfg.password)
        server.send_message(message)

    return message


def find_message(cfg: MailboxConfig, token: str) -> bool:
    if not cfg.imap_host or not cfg.imap_port:
        return False

    deadline = time.time() + cfg.wait_seconds

    while time.time() <= deadline:
        with IMAP4_SSL(cfg.imap_host, cfg.imap_port) as client:  # type: ignore[arg-type]
            if cfg.debug:
                client.debug = 4
            client.login(cfg.user, cfg.password)
            client.select("INBOX")
            typ, data = client.search(None, "UNSEEN")
            if typ != "OK":
                time.sleep(2)
                continue

            message_ids = data[0].split()
            for msg_id in message_ids:
                typ, msg_data = client.fetch(msg_id, "(RFC822)")
                if typ != "OK" or not msg_data:
                    continue
                raw = msg_data[0][1]
                if not raw:
                    continue
                message = message_from_bytes(raw)
                subject = message.get("Subject", "")
                if token in subject:
                    return True
        time.sleep(2)

    return False


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = validate_args(args)

    token = str(int(time.time()))
    print(f"Sending test email with token {token} to {cfg.recipient}...", flush=True)
    try:
        send_email(cfg, token)
    except Exception as exc:
        print(f"[ERROR] SMTP send failed: {exc}", file=sys.stderr)
        return 2
    print("SMTP send succeeded.")

    if cfg.imap_host and cfg.imap_port and cfg.wait_seconds:
        print(f"Checking IMAP for token {token} during {cfg.wait_seconds} seconds...")
        try:
            if find_message(cfg, token):
                print("IMAP check succeeded: message found.")
                return 0
            print("Message not found on IMAP (check manually).")
            return 1
        except Exception as exc:
            print(f"[WARNING] IMAP check failed: {exc}", file=sys.stderr)
            return 1

    print("IMAP check skipped (no host/port configured).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
