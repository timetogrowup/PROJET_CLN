# CLN

This repository stores the static CLN website.

## GitHub Pages deployment

1. Push the repository to https://github.com/timetogrowup/PROJET_CLN.
2. In GitHub settings (Settings > Pages), choose branch `main` and folder `/`.
3. The `Deploy static site` workflow uploads the artifact and publishes the site.

Open `index.html` locally in a browser to preview the site.

## Contact email configuration

The public contact address is `patrick.lyonnet@cln-solutions.fr`.  
Update the `.env` file with your Hostinger SMTP credentials before running any email automation:

```env
SMTP_HOST=smtp.hostinger.com
SMTP_PORT=465
SMTP_SENDER=patrick.lyonnet@cln-solutions.fr
SMTP_USERNAME=patrick.lyonnet@cln-solutions.fr
SMTP_PASSWORD=CHANGE_ME
SMTP_USE_SSL=1
SMTP_USE_TLS=0
CLN_NOTIFICATION_EMAIL=patrick.lyonnet@cln-solutions.fr
```

Never commit the real password—replace `CHANGE_ME` locally with the mailbox password or an app password.

## Automation script

The PowerShell script `publish.ps1` automates the full workflow (commit, GitHub repository creation, push, and GitHub Pages configuration).  
Before running it, create a GitHub personal access token (scopes `repo` and `pages:write`) and set it in your VS Code terminal:

```powershell
$env:GITHUB_TOKEN = "ghp_xxxxx"
```

Then run:

```powershell
.\publish.ps1 -CommitMessage "Site update"
```

The script pushes the `main` branch, enables GitHub Pages on the repository root, and prints the final site URL.
