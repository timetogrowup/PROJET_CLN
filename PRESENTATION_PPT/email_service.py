from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, Optional


class EmailConfigurationError(RuntimeError):
    """Raised when the SMTP configuration is incomplete."""


_ENV_LOADED = False


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_env_file() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = Path(__file__).parent / ".env"
    env_entries: dict[str, str] = {}

    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            env_entries[key] = value
            os.environ.setdefault(key, value)

    changed = _ensure_smtp_defaults(env_entries)
    changed = _apply_mailjet_defaults(env_entries) or changed

    if changed or not env_path.exists():
        _write_env_file(env_path, env_entries)

    _ENV_LOADED = True


def _ensure_smtp_defaults(env_entries: dict[str, str]) -> bool:
    defaults = {
        "SMTP_PORT": "587",
        "SMTP_USE_SSL": "0",
        "SMTP_USE_TLS": "1",
    }
    changed = False

    for key, default in defaults.items():
        current_env = os.environ.get(key)
        if current_env in {None, ""}:
            os.environ[key] = default
            changed = True
        if key not in env_entries:
            env_entries[key] = default
            changed = True

    return changed


def _apply_mailjet_defaults(env_entries: dict[str, str]) -> bool:
    changed = False
    api_key = os.getenv("MAILJET_API_KEY") or env_entries.get("MAILJET_API_KEY")
    secret_key = os.getenv("MAILJET_SECRET_KEY") or env_entries.get("MAILJET_SECRET_KEY")

    # Map Mailjet credentials to SMTP defaults when available
    if api_key and not os.getenv("SMTP_USERNAME"):
        os.environ["SMTP_USERNAME"] = api_key
        if env_entries.get("SMTP_USERNAME") != api_key:
            env_entries["SMTP_USERNAME"] = api_key
            changed = True

    if secret_key and not os.getenv("SMTP_PASSWORD"):
        os.environ["SMTP_PASSWORD"] = secret_key
        if env_entries.get("SMTP_PASSWORD") != secret_key:
            env_entries["SMTP_PASSWORD"] = secret_key
            changed = True

    if api_key and secret_key:
        if not os.getenv("SMTP_HOST"):
            os.environ["SMTP_HOST"] = "in-v3.mailjet.com"
            if env_entries.get("SMTP_HOST") != "in-v3.mailjet.com":
                env_entries["SMTP_HOST"] = "in-v3.mailjet.com"
                changed = True
        if "SMTP_PORT" not in env_entries:
            env_entries["SMTP_PORT"] = os.environ.get("SMTP_PORT", "587")
            changed = True

    return changed or False


def _write_env_file(path: Path, entries: dict[str, str]) -> None:
    lines = [f"{key}={value}" for key, value in sorted(entries.items())]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


@dataclass(frozen=True)
class SMTPSettings:
    host: str
    port: int
    sender: str
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False

    @classmethod
    def from_env(cls) -> "SMTPSettings":
        _load_env_file()

        host = os.getenv("SMTP_HOST")
        sender = os.getenv("SMTP_SENDER")
        if not host:
            raise EmailConfigurationError(
                "SMTP_HOST must be defined to enable email confirmation."
            )
        if not sender:
            raise EmailConfigurationError(
                "SMTP_SENDER must be defined to enable email confirmation."
            )

        port_raw = os.getenv("SMTP_PORT", "587")
        try:
            port = int(port_raw)
        except ValueError as exc:
            raise EmailConfigurationError(
                f"SMTP_PORT must be an integer (current: {port_raw!r})."
            ) from exc

        username = os.getenv("SMTP_USERNAME")
        password = os.getenv("SMTP_PASSWORD")

        use_ssl = _get_bool_env("SMTP_USE_SSL", False)
        use_tls = _get_bool_env("SMTP_USE_TLS", not use_ssl)

        if not username or not password:
            raise EmailConfigurationError(
                "SMTP_USERNAME and SMTP_PASSWORD must be provided via environment variables or .env file."
            )

        return cls(
            host=host,
            port=port,
            sender=sender,
            username=username,
            password=password,
            use_tls=use_tls,
            use_ssl=use_ssl,
        )


def _build_message(
    sender: str, recipient: str, subject: str, body: str
) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body)
    return message


def _format_summary_block(summary: Optional[str]) -> str:
    if not summary:
        return ""
    lines = [line.strip() for line in summary.splitlines() if line.strip()]
    if not lines:
        return ""
    bullet_lines = "\n".join(f"- {line}" for line in lines)
    return f"\nSynthèse de votre diagnostic :\n{bullet_lines}\n"


def _format_section(title: str, lines: Iterable[str]) -> str:
    content = "\n".join(line for line in lines if line)
    return f"{title}\n{content}\n" if content else ""


def send_lead_confirmation_email(
    settings: SMTPSettings,
    name: str,
    email: str,
    *,
    summary: Optional[str] = None,
    rendezvous_hint: Optional[str] = None,
) -> None:
    subject = "Merci pour votre prise de contact avec CLN"
    body_parts = [
        f"Bonjour {name},",
        "",
        "Merci d'avoir complété notre pré-diagnostic. Votre demande a bien été enregistrée.",
    ]

    summary_block = _format_summary_block(summary)
    if summary_block:
        body_parts.append(summary_block.strip())

    if rendezvous_hint:
        body_parts.append(rendezvous_hint.strip())

    body_parts.extend(
        [
            "",
            "Nous revenons vers vous sous 48 heures pour convenir de la suite (ateliers, rendez-vous ou plan d'action).",
            "",
            "Bien cordialement,",
            "L'équipe CLN",
        ]
    )

    message = _build_message(settings.sender, email, subject, "\n".join(body_parts))
    _send(settings, message)


def send_internal_notification_email(
    settings: SMTPSettings,
    recipient: Optional[str] = None,
    *,
    lead_name: str,
    lead_email: str,
    organisation: Optional[str] = None,
    message_text: Optional[str] = None,
    summary: Optional[str] = None,
) -> None:
    _load_env_file()
    resolved_recipient = recipient or os.getenv("CLN_NOTIFICATION_EMAIL")
    if not resolved_recipient:
        resolved_recipient = settings.sender

    subject = f"[CLN] Nouveau pré-diagnostic — {lead_name}"

    contact_lines = [
        f"Nom : {lead_name}",
        f"Email : {lead_email}",
    ]
    if organisation:
        contact_lines.append(f"Organisation : {organisation}")

    body_parts = [
        "Un visiteur vient de finaliser le pré-diagnostic sur le site CLN.",
        "",
        _format_section("Coordonnées :", contact_lines).strip(),
    ]

    if message_text:
        body_parts.append(
            _format_section("Message :", [message_text.strip()]).strip()
        )

    summary_block = _format_summary_block(summary)
    if summary_block:
        body_parts.append(summary_block.strip())

    body_parts.append("")
    body_parts.append("Pensez à répondre sous 48 heures pour tenir la promesse commerciale.")

    message = _build_message(
        settings.sender,
        resolved_recipient,
        subject,
        "\n".join(part for part in body_parts if part),
    )
    _send(settings, message)


def _send(settings: SMTPSettings, message: EmailMessage) -> None:
    if settings.use_ssl:
        smtp: smtplib.SMTP = smtplib.SMTP_SSL(
            settings.host, settings.port, timeout=30
        )
    else:
        smtp = smtplib.SMTP(settings.host, settings.port, timeout=30)

    with smtp as server:
        server.ehlo()
        if settings.use_tls and not settings.use_ssl:
            server.starttls()
            server.ehlo()
        if settings.username:
            server.login(settings.username, settings.password or "")
        server.send_message(message)
