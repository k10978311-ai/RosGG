# Prepares the LDPlayer test emulator to talk to the local RoS mock servers.
#  - turns off Private DNS (DNS-over-TLS hides/bypasses DNS redirection)
#  - installs certs\<hash>.0 (local test CA) into the system trust store
#  - DNATs all emulator DNS (udp/53) to the PC's dns_server.py
# Run: powershell -ExecutionPolicy Bypass -File setup_emulator.ps1   (add -Undo to revert)
param([switch]$Undo)

. "$PSScriptRoot\adb_common.ps1"
$adb = $script:RosAdb
$PC_IP = $script:RosPcIp
$serial = Resolve-RosSerial -Target ldplayer
if (-not $serial) { throw "LDPlayer not found (emulator-5554). Start LDPlayer first." }
$adbArgs = @("-s", $serial)
$caFile = Get-ChildItem "$PSScriptRoot\certs\*.0" | Select-Object -First 1

& $adb @adbArgs root | Out-Null
& $adb @adbArgs wait-for-device
Write-Host "Emulator serial: $serial"
Start-Sleep 2

if ($Undo) {
    & $adb @adbArgs shell "iptables -t nat -D OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53 2>/dev/null; umount /system/etc/security/cacerts 2>/dev/null; settings put global private_dns_mode opportunistic"
    "Reverted."
    exit
}

& $adb @adbArgs shell "settings put global private_dns_mode off"
& $adb @adbArgs push $caFile.FullName "/data/local/tmp/$($caFile.Name)" | Out-Null
# /system is read-only (system-as-root), so overlay the cacerts dir with a tmpfs copy (lost on emulator reboot).
$n = $caFile.Name
& $adb @adbArgs shell "D=/system/etc/security/cacerts; if [ ! -f `$D/$n ]; then mkdir -p /data/local/tmp/cacerts_bak; cp `$D/* /data/local/tmp/cacerts_bak/; mount -t tmpfs tmpfs `$D; cp /data/local/tmp/cacerts_bak/* `$D/; cp /data/local/tmp/$n `$D/; chmod 644 `$D/*; chcon u:object_r:system_file:s0 `$D/*; fi; ls -l `$D/$n"
& $adb @adbArgs shell "iptables -t nat -C OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53 2>/dev/null || iptables -t nat -A OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53; iptables -t nat -L OUTPUT -n | grep 53"

# Install custom loginapp.pubkey so client encrypts login with our key
$pubKey = "$PSScriptRoot\server_keys\loginapp.pubkey"
if (Test-Path $pubKey) {
    Push-RosLoginPubKey -Serial $serial
}
"Emulator configured."
