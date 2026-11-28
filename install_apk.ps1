# Install a changed / patched RoS APK (not the XAPK flow — use install_ros.ps1 for stock XAPK).
#
#   .\install_apk.ps1 -Apk C:\path\to\signed.apk -Target phone
#   .\install_apk.ps1 -Patch v005 -Target phone
#   .\install_apk.ps1 -Target phone                    # uses config: ROS_LOCAL_APK or ROS_PATCH_VERSION
#
# Register a new build first:
#   .\game\new_patch.ps1 -Apk C:\path\to\signed.apk -Name my-fix -Changes "..."
param(
    [string]$Apk = "",
    [string]$Patch = "",
    [ValidateSet("phone", "ldplayer", "both")]
    [string]$Target = "phone",
    [string]$Serial = "",
    [switch]$UninstallOnMismatch,
    [switch]$SkipPubKey
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot\adb_common.ps1"

function Resolve-RosApk {
    param([string]$ApkPath, [string]$PatchVer)

    if ($ApkPath) {
        $ApkPath = (Resolve-Path $ApkPath).Path
        if (-not (Test-Path $ApkPath)) { throw "APK not found: $ApkPath" }
        return $ApkPath
    }

    if (-not $PatchVer -and $RosConfig.ROS_LOCAL_APK) {
        $ApkPath = $RosConfig.ROS_LOCAL_APK
        if (Test-Path $ApkPath) { return (Resolve-Path $ApkPath).Path }
        Write-Warning "config ROS_LOCAL_APK missing on disk: $ApkPath"
    }

    if (-not $PatchVer) { $PatchVer = $RosConfig.ROS_PATCH_VERSION }
    if (-not $PatchVer) { $PatchVer = "v005" }

    $dir = Get-ChildItem (Join-Path $PSScriptRoot "game\patches") -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like "$PatchVer*" } | Select-Object -First 1
    if (-not $dir) { throw "No patch folder for $PatchVer under game\patches\" }

    $candidate = Join-Path $dir.FullName "game.apk"
    if (-not (Test-Path $candidate)) {
        throw "Missing $candidate — register with .\game\new_patch.ps1 -Apk <signed.apk> -Name <label>"
    }
    return $candidate
}

function Install-RosApkOne {
    param([string]$s, [string]$localApk)

    $md5 = (Get-FileHash $localApk -Algorithm MD5).Hash.ToLower()
    $sizeMb = [math]::Round((Get-Item $localApk).Length / 1MB, 1)
    Write-Host "`n=== $s ==="
    Write-Host "APK: $localApk"
    Write-Host "MD5: $md5  (${sizeMb} MB)"

    $remote = "/data/local/tmp/ros_custom_install.apk"
    & $RosAdb -s $s shell am force-stop $RosPackage 2>&1 | Out-Null
    & $RosAdb -s $s push $localApk $remote 2>&1 | ForEach-Object { Write-Host $_ }

    $tryInstall = {
        param([string]$Method)
        if ($Method -eq "adb") {
            return (& $RosAdb -s $s install -r $localApk 2>&1 | Out-String).Trim()
        }
        return (& $RosAdb -s $s shell "pm install -r -d '$remote'" 2>&1 | Out-String).Trim()
    }

    $out = & $tryInstall "shell"
    Write-Host $out

    if ($out -notmatch "Success") {
        if ($out -match "INSTALL_FAILED_UPDATE_INCOMPATIBLE|SIGNATURE") {
            Write-Warning "Signature mismatch vs installed package."
            if ($UninstallOnMismatch) {
                Write-Host "[*] Uninstalling $RosPackage (OBB on /sdcard is kept)..."
                & $RosAdb -s $s uninstall $RosPackage 2>&1 | Write-Host
                $out = & $tryInstall "adb"
                Write-Host $out
            } else {
                Write-Host "    Retry: .\install_apk.ps1 -Apk '$localApk' -Target phone -UninstallOnMismatch"
            }
        } elseif ($out -match "INSTALL_FAILED_CONFLICTING_PROVIDER.*roslegacy") {
            Write-Host "    adb -s $s uninstall net.roslegacy.prod"
        } else {
            $out2 = & $tryInstall "adb"
            if ($out2 -ne $out) { Write-Host "(adb install) $out2" }
            $out = $out2
        }
    }

    if ($out -match "Success") {
        $ver = (& $RosAdb -s $s shell dumpsys package $RosPackage 2>&1 | Select-String "versionName=").ToString().Trim()
        Write-Host "[+] Installed — $ver"
        if (-not $SkipPubKey) { Push-RosLoginPubKey -Serial $s }
        return $true
    }

    $paths = (& $RosAdb -s $s shell pm path $RosPackage 2>&1)
    if ($paths -match "package:") {
        Write-Warning "pm install reported failure but package still present: $paths"
        if (-not $SkipPubKey) { Push-RosLoginPubKey -Serial $s }
        return $true
    }
  return $false
}

$resolved = Resolve-RosApk -ApkPath $Apk -PatchVer $Patch

$serials = @()
switch ($Target) {
    "phone" { $serials += Resolve-RosSerial -Target phone -Serial $Serial }
    "ldplayer" { $serials += Resolve-RosSerial -Target ldplayer -Serial $Serial }
    "both" {
        $serials += Resolve-RosSerial -Target phone -Serial $Serial
        $serials += Resolve-RosSerial -Target ldplayer -Serial $Serial
    }
}
$serials = $serials | Where-Object { $_ } | Select-Object -Unique
if (-not $serials) { throw "No adb device for $Target" }

$ok = $true
foreach ($s in $serials) {
    if (-not (Install-RosApkOne -s $s -localApk $resolved)) { $ok = $false }
}

if (-not $ok) { exit 1 }
Write-Host "`nPhone: TrustAll builds use patch v003+; stock NetEase sig use install_ros.ps1 from XAPK."
Write-Host "Harness: .\apply_config.ps1 -> .\setup_device.ps1"