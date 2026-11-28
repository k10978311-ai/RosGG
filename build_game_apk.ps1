# Build custom RoS APK (icon + optional 17-char label + asset overlays) and install via adb.
#
#   .\build_game_apk.ps1 -Icon "game\base\1.610637.617289\icon.png" -Install
#   .\build_game_apk.ps1 -Icon C:\art\my_icon.png -AppLabel "RoS Private Srv" -Install
#   .\build_game_apk.ps1 -Icon .\my.png -Overlay ".\banner.png=assets/res/ui/login_logo.png" -Install
#
# Config (config.cmd / config.local.cmd): ROS_CUSTOM_ICON, ROS_APP_LABEL
param(
    [string]$Icon = "",
    [string]$AppLabel = "",
    [string]$BaseApk = "",
    [string[]]$Overlay = @(),
    [switch]$Install,
    [ValidateSet("phone", "ldplayer", "both")]
    [string]$Target = "phone",
    [switch]$Register,
    [string]$PatchName = "custom-build"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot\adb_common.ps1"

$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

if (-not $Icon) {
    $Icon = $RosConfig.ROS_CUSTOM_ICON
    if (-not $Icon) { $Icon = Join-Path $PSScriptRoot "game\base\1.610637.617289\icon.png" }
}
if (-not $AppLabel) { $AppLabel = $RosConfig.ROS_APP_LABEL }
if (-not $BaseApk) {
    $BaseApk = Join-Path $PSScriptRoot "game\patches\v003_2026-11-18_phone-trustall\game.apk"
}

if (-not (Test-Path $Icon)) { throw "Icon not found: $Icon" }
if (-not (Test-Path $BaseApk)) { throw "Base APK not found: $BaseApk" }

$argsPy = @(
    (Join-Path $PSScriptRoot "tools\build_custom_apk.py"),
    "--base", $BaseApk,
    "--icon", $Icon
)
if ($AppLabel) { $argsPy += @("--label", $AppLabel) }
foreach ($o in $Overlay) { $argsPy += @("--overlay", $o) }

Write-Host "[*] Building custom APK..."
& $py @argsPy
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$signed = Get-ChildItem (Join-Path $PSScriptRoot "scratch\signed_apk") -Filter *.apk |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $signed) { throw "No signed APK in scratch\signed_apk" }

if ($Register) {
    $changes = "Icon=$Icon"
    if ($AppLabel) { $changes += "; label=$AppLabel" }
    if ($Overlay) { $changes += "; overlays=$($Overlay.Count)" }
    & "$PSScriptRoot\game\new_patch.ps1" -Apk $signed.FullName -Name $PatchName -From v003 -Changes $changes
}

$localCfg = Join-Path $PSScriptRoot "config.local.cmd"
if (-not (Test-Path $localCfg)) {
    @"
@echo off
call config.cmd
set ROS_LOCAL_APK=$($signed.FullName)
"@ | Set-Content -Encoding ascii $localCfg
    Write-Host "[+] Wrote config.local.cmd -> ROS_LOCAL_APK"
} else {
    $content = Get-Content $localCfg -Raw
    if ($content -match 'set ROS_LOCAL_APK=') {
        $content = $content -replace 'set ROS_LOCAL_APK=.*', "set ROS_LOCAL_APK=$($signed.FullName)"
    } else {
        $content += "`r`nset ROS_LOCAL_APK=$($signed.FullName)`r`n"
    }
    Set-Content -Path $localCfg -Value $content.TrimEnd() -Encoding ascii
    Write-Host "[+] Updated config.local.cmd ROS_LOCAL_APK"
}

if ($Install) {
    & "$PSScriptRoot\install_apk.ps1" -Apk $signed.FullName -Target $Target -UninstallOnMismatch
} else {
    Write-Host "Install: .\install_apk.ps1 -Apk `"$($signed.FullName)`" -Target phone -UninstallOnMismatch"
}