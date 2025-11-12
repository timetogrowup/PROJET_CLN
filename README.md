# CLN Website

Static marketing site for CLN (Connecter – Libérer – Normaliser).

## Deployment Overview

- **Source control**: GitHub repository `timetogrowup/PROJET_CLN` (`main` branch).
- **Production hosting**: Hostinger shared hosting serving `cln-solutions.fr` (files placed in `public_html`).
- **Continuous delivery**: GitHub Actions workflow `.github/workflows/deploy-hostinger.yml` pushes the site on every `main` commit and performs a smoke test of the contact form.

### GitHub Actions pipeline

The `Deploy to Hostinger` workflow executes the following steps:

1. Checkout the repository.
2. Upload the web assets to Hostinger via FTPS, excluding local tooling files.
3. Wait briefly, then submit an automated request to `contact.php` to confirm the form returns a `303` redirect to `merci.html?status=success`.

#### Required secrets

Configure these repository secrets in GitHub before enabling the workflow:

| Secret | Description |
| --- | --- |
| `HOSTINGER_FTP_HOST` | Hostname of the Hostinger FTP/FTPS server (e.g. `ftp.cln-solutions.fr`). |
| `HOSTINGER_FTP_USER` | FTP username. |
| `HOSTINGER_FTP_PASSWORD` | FTP password. |
| `HOSTINGER_FTP_DIR` | *(Optional)* target directory (defaults to `/public_html/`). |
| `HOSTINGER_CONTACT_URL` | *(Optional)* full URL to `contact.php` (defaults to `https://cln-solutions.fr/contact.php`). |
| `HOSTINGER_CONTACT_TEST_EMAIL` | *(Optional)* destination email for the smoke test (defaults to `patrick.lyonnet@cln-solutions.fr`). |

The workflow runs automatically on pushes to `main`, and can be triggered manually from the Actions tab (workflow_dispatch).

### Manual deployment fallback

If you prefer a manual upload:

1. Ensure local changes are committed and pushed to GitHub.
2. Create an archive: `Compress-Archive -Path * -DestinationPath site.zip`.
3. Upload the archive via Hostinger hPanel > File Manager > `public_html`, then extract it and delete the archive.
4. Browse `https://cln-solutions.fr` and submit a form test manually to confirm delivery.

## Contact Email Configuration

- Official inbox: `patrick.lyonnet@cln-solutions.fr` (Hostinger).
- `.env` keeps SMTP credentials for local scripts (file is ignored by Git):

```env
SMTP_HOST=smtp.hostinger.com
SMTP_PORT=465
SMTP_SENDER=patrick.lyonnet@cln-solutions.fr
SMTP_USERNAME=patrick.lyonnet@cln-solutions.fr
SMTP_PASSWORD=CHANGE_ME   # replace locally; never commit the real secret
SMTP_USE_SSL=1
SMTP_USE_TLS=0
CLN_NOTIFICATION_EMAIL=patrick.lyonnet@cln-solutions.fr
```

Update `SMTP_PASSWORD` locally before launching any automation that sends emails (e.g., `test_mailbox.py`).

## Contact Form Back-End

- `contact.php` processes POST submissions, validates the required fields, sends a message via PHP `mail()` (reply-to set to the sender), then redirects with status flags.
- `contact.html` displays a status banner based on the `status` query parameter (`success`, `invalid`, `error`).
- Local test command: `php -S localhost:8000` and submit `http://localhost:8000/contact.php`.  
  The GitHub Actions smoke test described above performs the same call against production.

## Tooling & Useful Commands

- `test_mailbox.py` — CLI helper to exercise SMTP/IMAP for the Hostinger mailbox.
- `publish.ps1` — legacy automation for GitHub Pages (kept for archival purposes).
- Quick previews:

```powershell
# Static preview
python -m http.server 8000

# PHP preview (contact form)
php -S localhost:8000

# Create archive for Hostinger File Manager
Compress-Archive -Path * -DestinationPath site.zip
```

Keep documentation and deployment notes up to date whenever the hosting strategy or form handling changes.
