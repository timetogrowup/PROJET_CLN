# CLN Static Site — Technical Overview

This document summarises the structure and technical choices of the CLN marketing site.

## 1. Purpose And Scope
- Static showcase site describing the Connecter – Liberer – Normaliser offering.
- Target hosting: GitHub Pages historically, now migrated to Hostinger shared hosting.
- Content: HTML pages, one CSS stylesheet, inline JavaScript for the diagnostic questionnaire.

## 2. Project Layout
```
PROJET_CLN/
├── index.html             # Landing page
├── solutions.html         # Offer details
├── approche.html          # Mission and methodology
├── realisations.html      # Case studies + CTA
├── diagnostic.html        # Interactive questionnaire
├── contact.html           # Contact form (posts to contact.php)
├── merci.html             # Confirmation page
├── contact.php            # PHP handler for the contact form
├── styles.css             # Global styles
├── LOGO_CLN.png           # Main logo
├── *.jpg / *.png          # Visual assets
├── TECHNICAL_OVERVIEW.md  # This document
└── ...                    # Supplementary files (presentations, scripts, docs)
```

## 3. Technologies
- HTML5 for page markup with a repeated header/footer structure.
- CSS3 (single file `styles.css`) using flexbox, grid, and custom properties.
- Vanilla JavaScript embedded in `diagnostic.html` and `contact.html`.
- PHP 8+ minimal script (`contact.php`) used to send email from the form.
- No external JS/CSS dependencies; fonts rely on system fallbacks (Montserrat stack).

## 4. Design System
- Palette: primary `#5a4fcf`, dark accent `#3e36a8`, secondary accent `#00b894`, neutral backgrounds.
- Typography: `Montserrat`, `Segoe UI`, `Helvetica Neue`, `Arial`, sans-serif fallback.
- Reusable components:
  - Sticky header with `.navbar` container and CTA button.
  - `.card` / `.card-grid` for most content sections.
  - `.timeline`, `.projects-grid`, `.contact-grid` for specific layouts.
  - `.cta-button` reused across pages for primary actions.
- Responsiveness handled via CSS grid `auto-fit` patterns and media queries around 720px.

## 5. Pages And Content
1. **index.html** – hero message, key commitments, quote block.
2. **solutions.html** – detailed presentation of the three modules (Connecter, Liberer, Normaliser).
3. **approche.html** – mission/vision cards and four-step timeline.
4. **realisations.html** – three case studies, tags, and calls to action.
5. **diagnostic.html** – multi-step questionnaire producing a recommendation summary (results persisted in `localStorage` for reuse in contact form).
6. **contact.html** – contact information, recommendation preview, and form posting to `contact.php`.
7. **merci.html** – acknowledgement page with link back to the home page.

## 6. Diagnostic Questionnaire
- Form controls:
  - Checkboxes `modules[]` to pick the levers (Connecter/Liberer/Normaliser).
  - Radio groups for organisation size, project timeframe, and engagement mode.
  - Select `priorite` to capture the main priority.
- JavaScript (inline):
  - `buildModuleSummary`, `recommendationFromPriority`, `rendezVousMessage` generate tailored text.
  - Local storage stores the latest recommendation for reuse in `contact.html`.
  - Smooth scroll to the result card when generated.
- Possible extensions: export to PDF, server-side persistence, analytics of module selection.

## 7. Contact Form Flow
- Front-end (`contact.html`):
  - Required fields: `name`, `_replyto`, `message`, `consent`.
  - Status banner shown based on query parameter `status` (`success`, `invalid`, `error`).
  - Prefills the textarea with the recommendation stored in `localStorage` when available.
- Back-end (`contact.php`):
  - Accepts POST only; redirects to `contact.html` otherwise.
  - Trims inputs, guards against header injection, validates email syntax and consent.
  - Sends an email via PHP `mail()` to `patrick.lyonnet@cln-solutions.fr` with `Reply-To` set to the visitor email.
  - Redirects with HTTP 303 to `merci.html?status=success` on success, or back to `contact.html?status=error` on failure.
  - Easy upgrades: swap `mail()` for PHPMailer in SMTP mode, add CAPTCHA, log submissions.

## 8. Deployment On Hostinger
- **Automated pipeline** - workflow .github/workflows/deploy-hostinger.yml triggers on every push to main (and on manual dispatch):
  1. Checkout repository.
  2. Sync web assets to Hostinger via FTPS (SamKirkland/FTP-Deploy-Action) while excluding tooling files; a state file prevents re-uploading unchanged content.
  3. Wait about 10 seconds, then submit a POST request to contact.php to confirm a 303 redirect towards merci.html?status=success.
  4. Expose HTTP status and redirect location via job outputs; any anomaly fails the workflow.
- **Required secrets**: HOSTINGER_FTP_HOST, HOSTINGER_FTP_USER, HOSTINGER_FTP_PASSWORD, optional HOSTINGER_FTP_DIR, HOSTINGER_CONTACT_URL, HOSTINGER_CONTACT_TEST_EMAIL.
- **Manual fallback** (if automation is paused):
  1. Keep this repository as source of truth and ensure assets are current.
  2. Upload the site to public_html via Hostinger File Manager (zip + extract) or hPanel Git deployment.
  3. Verify server layout (public_html/index.html, contact.php, styles.css, assets).
  4. Browse https://cln-solutions.fr and submit the contact form manually (expect success redirect plus email).
  5. Maintain Hostinger nameservers ns1.dns-parking.com / ns2.dns-parking.com and remove legacy GitHub Pages DNS records.
## 9. Testing & Validation
- **Static preview**: `python -m http.server 8000` and open `http://localhost:8000/index.html`.
- **PHP contact form locally**: `php -S localhost:8000` then POST to `http://localhost:8000/contact.php` (set `mail()` to log or use a dummy handler when developing).
- **Questionnaire QA**: verify result generation with zero, single, and multiple modules; check `localStorage` persistence between diagnostic → contact.
- **Accessibility & SEO**:
  - Confirm readable contrasts, focus states, and keyboard navigation.
  - Add page-level meta descriptions and image `alt` text where missing (tracked as future enhancement).
- **Email deliverability**: regular test with the Python script `test_mailbox.py` or manual send/receive checks.

## 10. Evolution Ideas
- Mobile navigation toggle (burger menu) replacing the simple hide/show behaviour.
- Add favicon, web manifest, and Open Graph/Twitter cards.
- Optimise large images (WebP exports, lazy loading).
- Instrument analytics (Plausible, Matomo, GA4) once privacy policy is settled.
- Consider templating or a lightweight static site generator to deduplicate header/footer.
- Internationalisation (duplicate templates with `lang` and translated copy).

## 11. Maintenance Notes
- Keep `styles.css` organised by section; document new component blocks inline.
- Reuse `.cta-button`, `.card`, `.contact-grid` classes to stay consistent.
- Update contact information simultaneously across all pages when changes occur.
- Secure credentials: `.env` stays local (SMTP password never committed).
- Monitor .github/workflows/deploy-hostinger.yml logs; rotate Hostinger credentials and update repository secrets when needed.

## 12. Annexes
- `BUSINESS_OVERVIEW.md`, `CODE_REFERENCE.md` provide complementary documentation.
- `PRESENTATION_PPT/` holds supporting decks plus Python utilities for email and language normalisation.
- Static assets include `LOGO_CLN.png`, Pexels imagery, and diagnostic resources.

---
Last reviewed: migration to Hostinger with PHP mail handler (November 2025). Update this document after every significant architectural or hosting change.
