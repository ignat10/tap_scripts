$repo = "ignat10/screen_objects"

$releases = Invoke-RestMethod `
    -Uri "https://api.github.com/repos/$repo/releases"

$latestRelease = $releases |
    Sort-Object published_at -Descending |
    Select-Object -First 1

if (-not $latestRelease) {
    throw "No releases found"
}

$asset = $latestRelease.assets |
    Where-Object { $_.name -like "*.whl" } |
    Select-Object -First 1

if (-not $asset) {
    throw "No wheel found in latest release: $($latestRelease.tag_name)"
}

if (-not $asset.browser_download_url) {
    throw "Asset missing download URL"
}

$tempFile = Join-Path $env:TEMP $asset.name

Invoke-WebRequest `
    -Uri $asset.browser_download_url `
    -OutFile $tempFile

if (-not (Test-Path $tempFile)) {
    throw "Download failed"
}

python -m pip install --upgrade $tempFile