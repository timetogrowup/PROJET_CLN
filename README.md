# CLN Website

Static marketing site for CLN (Connecter – Libérer – Normaliser).

## Deployment Overview

- **Source control**: GitHub repository `timetogrowup/PROJET_CLN` (`main` branch).
- **Production hosting**: Hostinger shared hosting serving `cln-solutions.fr` (files placed in `public_html`).
- **Legacy preview**: GitHub Pages workflow `.github/workflows/deploy-pages.yml` still builds the site for preview at `https://timetogrowup.github.io/PROJET_CLN/`.

### Deploying to Hostinger (recommended)

1. Ensure local changes are committed and pushed to GitHub.
2. Deliver the files to Hostinger:
   - **File Manager route** – `Compress-Archive -Path * -DestinationPath site.zip`, upload the archive in hPanel > File Manager, extract inside `public_html`, then delete the archive.
   - **Git deployment route** – hPanel > Git > Add repository, set the repository URL `https://github.com/timetogrowup/PROJET_CLN.git`, choose `public_html` as the deployment directory, click Deploy.
3. Check that `index.html`, `contact.php`, `styles.css` and assets are present in `public_html`.
4. Visit `https://cln-solutions.fr`, navigate across pages, submit a form test and confirm the email is received by `patrick.lyonnet@cln-solutions.fr`.
5. DNS: keep Hostinger nameservers (`ns1.dns-parking.com`, `ns2.dns-parking.com`) and remove any legacy GitHub Pages A/CNAME records if they still exist.

### GitHub Pages workflow (optional preview)

1. Push to `origin/main`.
2. Monitor the **Deploy static site** action; it publishes to `https://timetogrowup.github.io/PROJET_CLN/`.
3. Disable the workflow once Hostinger hosting becomes the only delivery path.

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
