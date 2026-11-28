# Install a patch version on LDPlayer or the phone and record it in CURRENT.md.
#   .\install_patch.ps1 -Version v005 -Target ldplayer
#   .\install_patch.ps1 -Version v004 -Target phone
# Uses adb install -r (keeps game data + OBB). Signature change -> uninstall first (loses data; OBB stays in /sdcard/Android/obb).
param(
    [Parameter(Mandatory)][string]$Version,
    [ValidateSet("ldplayer", "phone", "auto")][string]$Target = "ldplayer",
    [string]$Serial = ""
)
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "..\adb_common.ps1")

$dir = Get-ChildItem (Join-Path $PSScriptRoot "patches") -Directory | Where-Object Name -like "$Version*" | Select-Object -First 1
if (-not $dir) { throw "No patch folder matching $Version" }
$apk = Join-Path $dir.FullName "game.apk"
$serial = Resolve-RosSerial -Target $Target -Serial $Serial
if (-not $serial) { throw "No device for target $Target" }

Write-Host "Installing $($dir.Name) on $serial ..."
& $RosAdb -s $serial shell am force-stop $RosPackage | Out-Null
$out = & $RosAdb -s $serial install -r $apk 2>&1 | Out-String
Write-Host $out.Trim()
if ($out -notmatch "Success") { throw "Install failed (INSTALL_FAILED_UPDATE_INCOMPATIBLE = different signature: uninstall $RosPackage first)" }

$md5 = (Get-FileHash $apk -Algorithm MD5).Hash.ToLower()
$cur = Join-Path $PSScriptRoot "CURRENT.md"
$line = "| $serial | $($dir.Name) | ``$($md5.Substring(0,8))`` | $(Get-Date -Format 'yyyy-MM-dd HH:mm') |"
$rows = if (Test-Path $cur) { Get-Content $cur | Where-Object { $_ -notmatch "^\| $([regex]::Escape($serial)) \|" } } else { @() }
if (-not ($rows -match '^\| Device')) { $rows = @("# Installed patch per device", "", "| Device | Version | MD5 | Installed |", "|---|---|---|---|") }
($rows + $line) | Set-Content -Encoding utf8 $cur
Write-Host "Recorded in CURRENT.md"
