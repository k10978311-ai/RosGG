# Phone DNS: remove ISP DNS #2, ensure PC UDP/53 is open, verify redirect.
#Requires -RunAsAdministrator
. "$PSScriptRoot\..\adb_common.ps1"

$serial = Resolve-RosSerial -Target phone
if (-not $serial) { throw "Connect phone with USB debugging." }

$fw = Get-NetFirewallRule -DisplayName "RoS Private Harness" -ErrorAction SilentlyContinue
if (-not $fw) {
    & (Join-Path $PSScriptRoot "..\setup_firewall.ps1")
} else {
    Write-Host "[=] RoS Private Harness firewall rule already present."
}

Write-Host "`nPhone must use ONLY DNS 1 = $RosPcIp on Static Wi-Fi (delete DNS 2 / ISP 117.x)." -ForegroundColor Yellow
Write-Host "Wi-Fi settings opening on device..."
& $RosAdb -s $serial shell "am start -a android.settings.WIFI_SETTINGS" | Out-Null

Read-Host "After saving Wi-Fi with DNS1=$RosPcIp and empty DNS2, press Enter"

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "fix_mobile_connect.ps1") | Out-Host