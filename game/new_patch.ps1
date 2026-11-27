# Register a newly built, signed APK as the next patch version.
#   .\new_patch.ps1 -Apk ..\tools_dl\vok\signed\out_unsigned-aligned-debugSigned.apk -Name vokdev-fix -From v005 -Changes "what changed"
# Creates patches\vNNN_<date>_<name>\ with game.apk (hard link, no extra disk space), PATCH.md, and an entry in VERSIONS.md.
param(
    [Parameter(Mandatory)][string]$Apk,
    [Parameter(Mandatory)][string]$Name,
    [string]$From = "",
    [string]$Changes = "TODO: describe the change",
    [switch]$Copy            # copy instead of hard link (use when the APK is on another drive)
)
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$src = (Resolve-Path $Apk).Path
$patches = Join-Path $root "patches"

$last = Get-ChildItem $patches -Directory | Where-Object Name -match '^v(\d{3})_' |
    ForEach-Object { [int]$Matches[1] } | Sort-Object | Select-Object -Last 1
$num = "v{0:D3}" -f ([int]$last + 1)
$date = Get-Date -Format "yyyy-MM-dd"
$safe = ($Name -replace '[^A-Za-z0-9-]', '-').ToLower()
$dir = Join-Path $patches "${num}_${date}_${safe}"
New-Item -ItemType Directory $dir | Out-Null

$dst = Join-Path $dir "game.apk"
if ($Copy) { Copy-Item $src $dst } else { New-Item -ItemType HardLink -Path $dst -Value $src | Out-Null }
$md5 = (Get-FileHash $dst -Algorithm MD5).Hash.ToLower()

$dupe = Get-ChildItem $patches -Recurse -Filter game.apk | Where-Object { $_.FullName -ne $dst } |
    Where-Object { (Get-FileHash $_.FullName -Algorithm MD5).Hash.ToLower() -eq $md5 } | Select-Object -First 1
if ($dupe) { Write-Warning "Same APK already registered as $($dupe.Directory.Name)" }

@"
# ${num}_${date}_${safe}

- **Built:** $((Get-Item $src).LastWriteTime.ToString('yyyy-MM-dd HH:mm'))
- **From:** $(if ($From) { $From } else { '-' })
- **Original file:** ``$src``
- **MD5:** ``$md5``
- **Changes:** $Changes
- **Installed on:** -
"@ | Set-Content -Encoding utf8 (Join-Path $dir "PATCH.md")

Add-Content -Encoding utf8 (Join-Path $root "VERSIONS.md") "| $num | $date | $safe | $(if ($From) { $From } else { '-' }) | $Changes | ``$($md5.Substring(0,8))`` |"
Write-Host "Registered $num -> $dir"
Write-Host "Install:  .\install_patch.ps1 -Version $num -Target ldplayer"
