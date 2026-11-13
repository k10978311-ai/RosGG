# Prepares the LDPlayer test emulator to talk to the local RoS mock servers.
#  - turns off Private DNS (DNS-over-TLS hides/bypasses DNS redirection)
#  - installs certs\<hash>.0 (local test CA) into the system trust store
#  - DNATs all emulator DNS (udp/53) to the PC's dns_server.py
# Run: powershell -ExecutionPolicy Bypass -File setup_emulator.ps1   (add -Undo to revert)
param([switch]$Undo)

$adb = "C:\LDPlayer\LDPlayer9\adb.exe"
$PC_IP = "192.168.1.18"
$caFile = Get-ChildItem "$PSScriptRoot\certs\*.0" | Select-Object -First 1

& $adb root | Out-Null
Start-Sleep 1

if ($Undo) {
    & $adb shell "iptables -t nat -D OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53 2>/dev/null; umount /system/etc/security/cacerts 2>/dev/null; settings put global private_dns_mode opportunistic"
    "Reverted."
    exit
}

& $adb shell "settings put global private_dns_mode off"
& $adb push $caFile.FullName "/data/local/tmp/$($caFile.Name)" | Out-Null
# /system is read-only (system-as-root), so overlay the cacerts dir with a tmpfs copy (lost on emulator reboot).
$n = $caFile.Name
& $adb shell "D=/system/etc/security/cacerts; if [ ! -f `$D/$n ]; then mkdir -p /data/local/tmp/cacerts_bak; cp `$D/* /data/local/tmp/cacerts_bak/; mount -t tmpfs tmpfs `$D; cp /data/local/tmp/cacerts_bak/* `$D/; cp /data/local/tmp/$n `$D/; chmod 644 `$D/*; chcon u:object_r:system_file:s0 `$D/*; fi; ls -l `$D/$n"
& $adb shell "iptables -t nat -C OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53 2>/dev/null || iptables -t nat -A OUTPUT -p udp --dport 53 -j DNAT --to-destination ${PC_IP}:53; iptables -t nat -L OUTPUT -n | grep 53"
"Emulator configured."
