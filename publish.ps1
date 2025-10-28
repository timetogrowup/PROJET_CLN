param(
    [string]$RepoName = "PROJET_CLN",
    [string]$GithubUser = "timetogrowup",
    [string]$GithubEmail = "timetogrowup@outlook.fr",
    [string]$Branch = "main",
    [string]$CommitMessage = "Configure GitHub Pages deployment"
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Args
    )

    $result = & git @Args
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $exitCode"
    }

    return $result
}

function Get-GitConfigValue {
    param([string]$Key)

    $value = & git config --get $Key 2>$null
    if ($LASTEXITCODE -ne 0) {
        return $null
    }

    return $value.Trim()
}

function Ensure-GitRepository {
    if (-not (Test-Path ".git")) {
        Write-Host "Initializing new Git repository..."
        Invoke-Git init
    }
}

function Ensure-GitIdentity {
    param(
        [string]$UserName,
        [string]$UserEmail
    )

    if (-not (Get-GitConfigValue "user.name")) {
        Write-Host "Configuring git user.name to $UserName"
        Invoke-Git config user.name $UserName
    }

    if (-not (Get-GitConfigValue "user.email")) {
        Write-Host "Configuring git user.email to $UserEmail"
        Invoke-Git config user.email $UserEmail
    }
}

function Ensure-Branch {
    param([string]$TargetBranch)

    $currentBranch = (& git branch --show-current 2>$null).Trim()
    if (-not $currentBranch) {
        $currentBranch = "HEAD"
    }

    if ($currentBranch -ne $TargetBranch) {
        Write-Host "Switching to branch $TargetBranch"
        Invoke-Git checkout '-B' $TargetBranch
    }
}

function Ensure-Remote {
    param(
        [string]$RemoteName,
        [string]$RemoteUrl
    )

    $existingUrl = & git remote get-url $RemoteName 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Adding remote $RemoteName -> $RemoteUrl"
        Invoke-Git remote add $RemoteName $RemoteUrl
    }
    elseif ($existingUrl.Trim() -ne $RemoteUrl) {
        Write-Host "Updating remote $RemoteName to $RemoteUrl"
        Invoke-Git remote set-url $RemoteName $RemoteUrl
    }
}

function Ensure-GitHubRepository {
    param(
        [string]$Token,
        [string]$Repo,
        [bool]$Private = $false
    )

    $headers = @{
        Authorization = "Bearer $Token"
        "User-Agent" = "publish-script"
        Accept       = "application/vnd.github+json"
    }

    $body = @{
        name    = $Repo
        private = $Private
    } | ConvertTo-Json

    try {
        Write-Host "Creating GitHub repository $Repo (if it does not exist)..."
        Invoke-RestMethod -Method Post -Headers $headers -Uri "https://api.github.com/user/repos" -Body $body
        Write-Host "Repository $Repo created or already available."
    }
    catch {
        $response = $_.Exception.Response
        if ($response -and $response.StatusCode.Value__ -eq 422) {
            Write-Host "Repository $Repo already exists on GitHub."
        }
        elseif ($response -and $response.StatusCode.Value__ -eq 401) {
            throw "GitHub authentication failed. Verify the GITHUB_TOKEN environment variable."
        }
        else {
            throw $_
        }
    }
}

function Set-GitHubPages {
    param(
        [string]$Token,
        [string]$Owner,
        [string]$Repo,
        [string]$SourceBranch,
        [string]$SourcePath = "/"
    )

    $headers = @{
        Authorization = "Bearer $Token"
        "User-Agent" = "publish-script"
        Accept       = "application/vnd.github+json"
    }

    $body = @{
        source = @{
            branch = $SourceBranch
            path   = $SourcePath
        }
    } | ConvertTo-Json

    $pagesEndpoint = "https://api.github.com/repos/$Owner/$Repo/pages"

    try {
        Write-Host "Configuring GitHub Pages..."
        Invoke-RestMethod -Method Post -Headers $headers -Uri $pagesEndpoint -Body $body | Out-Null
    }
    catch {
        $response = $_.Exception.Response
        if ($response) {
            $statusCode = $response.StatusCode.Value__
            if ($statusCode -eq 409) {
                Write-Host "GitHub Pages already configured, updating settings..."
                Invoke-RestMethod -Method Put -Headers $headers -Uri $pagesEndpoint -Body $body | Out-Null
            }
            elseif ($statusCode -eq 422) {
                Write-Host "Pages configuration still pending; will fetch current status."
            }
            else {
                throw $_
            }
        }
        else {
            throw $_
        }
    }

    Start-Sleep -Seconds 2
    try {
        $status = Invoke-RestMethod -Method Get -Headers $headers -Uri $pagesEndpoint
        if ($status.html_url) {
            Write-Host "GitHub Pages site url: $($status.html_url)"
        }
        else {
            Write-Host "GitHub Pages configured. It may take a minute before the site url becomes available."
        }
    }
    catch {
        Write-Host "Unable to retrieve Pages status immediately. Check the repository settings later."
    }
}

Ensure-GitRepository
Ensure-GitIdentity -UserName $GithubUser -UserEmail $GithubEmail
Ensure-Branch -TargetBranch $Branch

Invoke-Git add '-A'
$pendingChanges = Invoke-Git status '--porcelain'
if ($pendingChanges) {
    Write-Host "Committing local changes..."
    Invoke-Git commit '-m' $CommitMessage
}
else {
    Write-Host "No local changes to commit."
}

$remoteUrl = "https://github.com/$GithubUser/$RepoName.git"
Ensure-Remote -RemoteName "origin" -RemoteUrl $remoteUrl

$token = $env:GITHUB_TOKEN
if (-not $token) {
    throw "Set the GITHUB_TOKEN environment variable with a personal access token (scope: repo, pages:write)."
}

Ensure-GitHubRepository -Token $token -Repo $RepoName

$pushUrl = "https://${GithubUser}:${token}@github.com/$GithubUser/$RepoName.git"
Write-Host "Pushing branch $Branch to GitHub..."
Invoke-Git push '-u' $pushUrl $Branch

Set-GitHubPages -Token $token -Owner $GithubUser -Repo $RepoName -SourceBranch $Branch

Write-Host "Done. Monitor the GitHub Actions tab for the 'Deploy static site' workflow."
