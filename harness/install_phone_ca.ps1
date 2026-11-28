# Push harness CA in several names/formats and open Samsung cert-install settings.
. "$PSScriptRoot\..\adb_common.ps1"
$serial = Resolve-RosSerial -Target phone
if (-not $serial) { throw "Connect phone with USB debugging" }

$src = Join-Path $PSScriptRoot "..\certs\ca.crt"
if (-not (Test-Path $src)) { throw "Missing $src" }

$pem = Get-Content $src -Raw
$derPath = Join-Path $env:TEMP "ros_harness_ca.der"
$b64 = ($pem -replace '-----BEGIN CERTIFICATE-----', '' -replace '-----END CERTIFICATE-----', '' -replace '\s', '')
[IO.File]::WriteAllBytes($derPath, [Convert]::FromBase64String($b64))

$targets = @(
    "/sdcard/Download/ros_harness_ca.crt",
    "/sdcard/Download/ros_harness_ca.cer",
    "/sdcard/Download/ros_harness_ca.pem",
    "/sdcard/Documents/ros_harness_ca.crt"
)
& $RosAdb -s $serial shell "mkdir -p /sdcard/Documents" | Out-Null
foreach ($t in $targets) {
    & $RosAdb -s $serial push $src $t 2>&1 | Out-Null
}
& $RosAdb -s $serial push $derPath "/sdcard/Download/ros_harness_ca.der" 2>&1 | Out-Null

Write-Host "[+] Pushed CA to Download (crt/cer/pem/der) + Documents"

# Samsung / AOSP install entry points (one may work)
$intents = @(
    "am start -a android.settings.SECURITY_SETTINGS",
    "am start -a android.settings.DEVICE_CREDENTIAL_INSTALL",
    "am start -a android.credentials.INSTALL",
    "am start -a android.intent.action.VIEW -d file:///sdcard/Download/ros_harness_ca.crt -t application/x-x509-ca-cert",
    "am start -a android.intent.action.VIEW -d file:///sdcard/Download/ros_harness_ca.cer -t application/x-x509-ca-cert",
    "am start -a android.intent.action.VIEW -d file:///sdcard/Download/ros_harness_ca.der -t application/x-x509-ca-cert"
)
foreach ($i in $intents) {
    $out = & $RosAdb -s $serial shell $i 2>&1 | Out-String
    if ($out -notmatch "Error: Activity not started|Unable to resolve") {
        Write-Host "[+] Started: $i"
        break
    }
}

$lock = (& $RosAdb -s $serial shell "settings get secure lockscreen.password_type" 2>&1).Trim()
Write-Host ""
Write-Host "=== Samsung Note10+ (Android 12) — if install fails ==="
Write-Host "1. Set a screen lock PIN first (required for user CA):"
Write-Host "   Settings -> Biometrics and security -> Screen lock type -> PIN"
Write-Host "2. Then:"
Write-Host "   Settings -> Biometrics and security -> Other security settings"
Write-Host "   -> Install from device storage -> select Download -> ros_harness_ca.crt"
Write-Host "   Name: RoS Harness | Used for: VPN and apps (or Wi-Fi)"
Write-Host ""
Write-Host "Wi-Fi static (do NOT use PC IP as phone IP):"
Write-Host "   Phone IP = 192.168.1.168 (example) | DNS 1 = $RosPcIp | DNS 2 = empty"
if ($lock -eq "0" -or $lock -eq "65536") {
    Write-Host ""
    Write-Host "*** Likely blocker: NO PIN set (lock type $lock). Samsung refuses CA install without PIN."
}