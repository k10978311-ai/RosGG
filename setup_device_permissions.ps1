# Grant RoS + ADB-friendly settings on a physical phone (non-root). Run after USB connect.
#   .\setup_device_permissions.ps1
#   .\setup_device_permissions.ps1 -OpenSettings   # also opens battery / unknown-sources UIs
param(
    [string]$Serial = "",
    [switch]$OpenSettings,
    [switch]$Silent
)

. "$PSScriptRoot\adb_common.ps1"
$Serial = Resolve-RosSerial -Target phone -Serial $Serial
if (-not $Serial) { throw "No phone on adb" }

function Invoke-AdbShell {
    param([string]$Cmd)
    & $RosAdb -s $Serial shell $Cmd 2>&1 | Out-String
}

function Write-Step {
    param([string]$Msg)
    if (-not $Silent) { Write-Host $Msg }
}

Write-Step "=== Device permissions ($Serial) ==="

# Developer / USB stability
Invoke-AdbShell "settings put global private_dns_mode off" | Out-Null
Invoke-AdbShell "settings put global adb_enabled 1" | Out-Null
Invoke-AdbShell "settings put global stay_on_while_plugged_in 3" | Out-Null
Invoke-AdbShell "settings put global verifier_verify_adb_installs 0" | Out-Null
Invoke-AdbShell "settings put global package_verifier_enable 0" | Out-Null
Write-Step "[+] USB stay-awake, private DNS off, relaxed ADB package verify (where supported)"

$perms = @(
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.CAMERA",
    "android.permission.RECORD_AUDIO",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.BLUETOOTH_SCAN",
    "android.permission.BLUETOOTH_CONNECT",
    "android.permission.BLUETOOTH_ADVERTISE",
    "android.permission.POST_NOTIFICATIONS"
)

foreach ($p in $perms) {
    $out = & $RosAdb -s $Serial shell pm grant $RosPackage $p 2>&1 | Out-String
    if ($out -match "Unknown permission|not a changeable permission") { continue }
    if ($out -match "SecurityException|Exception") {
        Write-Step "[~] pm grant skipped $p"
    } else {
        Write-Step "[+] granted $p"
    }
}

$appops = @(
    @{ Op = "READ_EXTERNAL_STORAGE"; Mode = "allow" },
    @{ Op = "WRITE_EXTERNAL_STORAGE"; Mode = "allow" },
    @{ Op = "RUN_IN_BACKGROUND"; Mode = "allow" },
    @{ Op = "RUN_ANY_IN_BACKGROUND"; Mode = "allow" },
    @{ Op = "WAKE_LOCK"; Mode = "allow" },
    @{ Op = "START_FOREGROUND"; Mode = "allow" },
    @{ Op = "SYSTEM_ALERT_WINDOW"; Mode = "allow" }
)
foreach ($a in $appops) {
    Invoke-AdbShell "cmd appops set $RosPackage $($a.Op) $($a.Mode)" | Out-Null
}
Write-Step "[+] appops: storage, background, overlay (where supported)"

# Android 12+ ignore battery optimizations (may show a system dialog on phone)
Invoke-AdbShell "am start -a android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS -d package:$RosPackage" | Out-Null

if ($OpenSettings) {
    Write-Step "[*] Opening Samsung / Android permission screens on phone..."
    Invoke-AdbShell "am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:$RosPackage" | Out-Null
    Start-Sleep -Seconds 2
    Invoke-AdbShell "am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:com.android.shell" | Out-Null
}

$dump = Invoke-AdbShell "dumpsys package $RosPackage"
$denied = @($dump | Select-String "granted=false")
if ($denied.Count -eq 0) {
    Write-Step "[+] All listed runtime permissions granted"
} else {
    Write-Step "[~] Still denied ($($denied.Count)) — tap Allow on phone if a dialog appeared:"
    $denied | ForEach-Object { Write-Step "    $_" }
}

Write-Step ""
Write-Step "Still manual (non-root): Wi-Fi static DNS, user CA install, Samsung install-unknown-apps for sideload."
Write-Step "Run: .\setup_device.ps1  and  .\harness\setup_phone_now.ps1"