# One-shot phone prep: ADB file push + open Wi-Fi / cert UI + verify DNS.
# Static Wi-Fi DNS must be set on the phone (Samsung cannot do this via non-root ADB).
. "$PSScriptRoot\..\adb_common.ps1"

$serial = Resolve-RosSerial -Target phone
if (-not $serial) { throw "Connect Note10+ with USB debugging." }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "..\setup_device.ps1") -Serial $serial | Out-Host

Write-Host "`nOpening Wi-Fi settings on the phone..." -ForegroundColor Yellow
& $RosAdb -s $serial shell "am start -a android.settings.WIFI_SETTINGS" | Out-Null

Write-Host ">>> On phone: no_internet5g -> Manage -> Advanced -> IP Static" -ForegroundColor Cyan
Write-Host "    IP 192.168.1.168 | Gateway 192.168.1.1 | DNS1 $RosPcIp | DNS2 empty`n"

$view = & $RosAdb -s $serial shell "am start -a android.intent.action.VIEW -d file:///sdcard/Download/ros_harness_ca.crt -t application/x-x509-ca-cert 2>&1"
if ($view -match "Error") {
    Write-Host ">>> Install CA manually: My Files -> Download -> ros_harness_ca.crt" -ForegroundColor Cyan
} else {
    Write-Host ">>> Approve CA install on phone (name: RoS Harness)" -ForegroundColor Cyan
}

Read-Host "Press Enter after Wi-Fi DNS + CA are done"
& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "fix_mobile_connect.ps1") | Out-Host

$dns = (& $RosAdb -s $serial shell "ping -c 1 -W 2 h45na.update.easebar.com 2>&1" | Out-String)
if ($dns -match $RosPcIp) {
    Write-Host "`n[+] DNS OK — launching game..." -ForegroundColor Green
    & $RosAdb -s $serial shell "am force-stop $RosPackage" | Out-Null
    & $RosAdb -s $serial shell "monkey -p $RosPackage -c android.intent.category.LAUNCHER 1" | Out-Null
} else {
    Write-Host "`n[!] DNS still wrong. Checklist:" -ForegroundColor Red
    Write-Host "  1) Admin PC: .\setup_firewall.ps1  (UDP 53 must reach the phone)"
    Write-Host "  2) Phone Static Wi-Fi: DNS1=$RosPcIp and DNS2 EMPTY (remove 117.120.24.1)"
    Write-Host "  3) .\harness\fix_mobile_connect.ps1 until Harness DNS redirect working: YES"
}