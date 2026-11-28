# Configure a physical Android device (e.g. Note10+) for the local RoS harness.
# Non-root: no iptables — set Wi-Fi DNS to the PC IP manually (see below).
# Run: powershell -ExecutionPolicy Bypass -File setup_device.ps1
param(
    [string]$Serial = "",
    [string]$PcIp = "",
    [switch]$FullPermissions
)

. "$PSScriptRoot\adb_common.ps1"
if ($PcIp) { $script:RosPcIp = $PcIp }

$Serial = Resolve-RosSerial -Target phone -Serial $Serial
if (-not $Serial) { throw "No phone on adb (USB debugging on?)" }

Write-Host "Target device: $Serial"
Write-Host "PC harness IP: $RosPcIp"
& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "harness\fix_mobile_connect.ps1") | Out-Host

& $RosAdb -s $Serial shell "settings put global private_dns_mode off"
Write-Host "[+] Private DNS off"

if ($FullPermissions -or $RosDeviceFullPermissions) {
    & powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "setup_device_permissions.ps1") -Serial $Serial | Out-Host
}

Push-RosLoginPubKey -Serial $Serial

$caCrt = Join-Path $PSScriptRoot "certs\ca.crt"
$remoteCa = "/sdcard/Download/ros_harness_ca.crt"
if (Test-Path $caCrt) {
    & $RosAdb -s $Serial push $caCrt $remoteCa | Out-Null
    Write-Host "[+] CA pushed to $remoteCa"
}

@"
=== Manual steps on the phone (required, once) ===

1. Wi-Fi (same LAN as PC) -> Manage network -> Advanced:
   IP settings **Static** (Samsung usually ignores DNS on DHCP — this is why patch stays at 0%).
   IP = phone's current address, gateway = router, DNS 1 = $RosPcIp, DNS 2 blank.
   Verify: .\harness\fix_mobile_connect.ps1 must show h45na.update.easebar.com -> $RosPcIp.

2. Install the test CA: Settings -> Biometrics and security -> Other security
   -> Install from device storage -> Download -> ros_harness_ca.crt
   (name it "RoS Harness" and use it for Wi-Fi / user certs as prompted).

3. On PC (Administrator): dns_server.py + ros_mock_server.py
   Firewall must allow UDP 53, 25000, TCP 443/80 on $RosPcIp.

4. Frida on a real arm64 device: use native realm (no --realm emulated):
   python run_frida.py diag.js --attach --realm native

LDPlayer still uses setup_emulator.ps1 (root + iptables).
"@ | Write-Host

Write-Host "[+] Device-side file prep done."
