# Diagnose why the phone cannot reach the PC harness (most common: wrong Wi-Fi / subnet).
. "$PSScriptRoot\..\adb_common.ps1"

$serial = Resolve-RosSerial -Target phone
if (-not $serial) { throw "No phone on USB (enable USB debugging)." }

Write-Host "PC harness IP (ROS_PC_IP): $RosPcIp"
$pcPrefix = ($RosPcIp -split '\.')[0..2] -join '.'

$wlan = (& $RosAdb -s $serial shell "ip -4 addr show wlan0 2>/dev/null" | Out-String).Trim()
$ssid = (& $RosAdb -s $serial shell "dumpsys wifi | grep 'SSID:' | head -1" 2>$null) -replace '.*SSID: "', '' -replace '".*', ''

Write-Host "`nPhone Wi-Fi:"
Write-Host $wlan
Write-Host "SSID: $ssid"

$phoneIp = if ($wlan -match 'inet (\d+\.\d+\.\d+\.\d+)') { $Matches[1] } else { "" }
$phonePrefix = if ($phoneIp) { ($phoneIp -split '\.')[0..2] -join '.' } else { "?" }

$ping = (& $RosAdb -s $serial shell "ping -c 2 -W 2 $RosPcIp 2>&1") -join "`n"
$pingOk = $ping -match "1 received|2 received"

Write-Host "`nPing $RosPcIp from phone: $(if ($pingOk) { 'OK' } else { 'FAIL (ICMP often blocked on Windows — not fatal)' })"
if (-not $pingOk) { Write-Host $ping }

$tcpBytes = (& $RosAdb -s $serial shell "echo | toybox timeout 3 toybox nc $RosPcIp 443 | wc -c").Trim()
$tcpOk = ($tcpBytes -match '^\d+$') -and ([int]$tcpBytes -gt 0)
Write-Host "TCP 443 mock server from phone: $(if ($tcpOk) { 'OK' } else { 'FAIL — run setup_firewall.ps1 as Administrator on the PC' })"

$patchProbe = (& $RosAdb -s $serial shell "ping -c 1 -W 2 h45na.update.easebar.com 2>&1" | Out-String)
$patchIp = if ($patchProbe -match '\((\d+\.\d+\.\d+\.\d+)\)') { $Matches[1] } elseif ($patchProbe -match 'from (\d+\.\d+\.\d+\.\d+)') { $Matches[1] } else { "" }
$dnsOk = $patchIp -eq $RosPcIp
Write-Host "Patch host h45na.update.easebar.com resolves to: $(if ($patchIp) { $patchIp } else { 'unknown' })"
Write-Host "Harness DNS redirect working: $(if ($dnsOk) { 'YES' } else { 'NO — phone is NOT using PC DNS (stuck at patch 0% until fixed)' })"

$wifiDns = (& $RosAdb -s $serial shell "dumpsys wifi 2>/dev/null" | Select-String -Pattern "Static configuration:.*DNS servers" | Select-Object -Last 1).Line
if ($wifiDns) { Write-Host "Wi-Fi DNS config: $($wifiDns.Trim())" }
if ($wifiDns -match '192\.168\.1\.18' -and $wifiDns -match '117\.') {
    Write-Host "WARNING: DNS2 (ISP) still set — Android may fall back when UDP/53 to PC fails. Clear DNS 2 entirely."
}

$pubkey = (& $RosAdb -s $serial shell "test -f '/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/entities/loginapp.pubkey' && echo ok").Trim()

Write-Host "`nloginapp.pubkey on device: $pubkey"
Write-Host "CA in Download: $(if ((& $RosAdb -s $serial shell 'test -f /sdcard/Download/ros_harness_ca.crt && echo yes').Trim() -eq 'yes') {'yes'} else {'missing'})"

if (-not $dnsOk) {
    Write-Host @"

*** BLOCKER: Game patch server still points at the REAL internet ($patchIp), not $RosPcIp.
Samsung often ignores DNS on DHCP — use Static IP on Wi‑Fi '$ssid':

  Settings -> Connections -> Wi‑Fi -> (your network) -> Manage -> Advanced
  IP settings: Static
    IP: $phoneIp (or keep current)
    Gateway: router (usually ${pcPrefix}.1)
    Prefix length: 24
    DNS 1: $RosPcIp
    DNS 2: (leave blank)

  Settings -> Connections -> More connection settings -> Private DNS -> Off
  Re-run this script until 'Harness DNS redirect working: YES'
  Then force-stop Rules of Survival and open again.
"@
} elseif ($phonePrefix -ne $pcPrefix -and -not $pingOk) {
    Write-Host @"

*** BLOCKER: Phone is on $phonePrefix.x but the harness PC is $pcPrefix.x — different networks.

Fix (pick one):
  A) Connect the phone to the SAME Wi-Fi as the PC (the LAN where $RosPcIp lives).
  B) Connect the PC to '$ssid' ($phonePrefix.x), run 'ipconfig', set:
       `$env:ROS_PC_IP = '<PC's new .8.x address>'
     then .\sync_server_list.ps1 and restart dns_server + ros_mock_server.

Then on the phone Wi-Fi settings -> Advanced -> DNS 1 = your ROS_PC_IP (not 8.8.8.8).
Install ros_harness_ca.crt from Downloads (user certificate).
Run .\setup_device.ps1 again.
"@
} elseif ($tcpOk) {
    Write-Host @"

[+] Phone can reach the mock HTTPS port on $RosPcIp.

Still required on the phone (once per Wi‑Fi network):
  Wi‑Fi -> Advanced -> DNS 1 = $RosPcIp  (not 8.8.8.8 / router only)
  Private DNS = Off (already OK if settings show off)

On PC: dns_server.py + ros_mock_server.py (Admin). Avoid 'pm clear' on the game (UniSDK channelLoginFail 10).
"@
} elseif (-not $tcpOk) {
    Write-Host "`n*** Run as Administrator on the PC: .\setup_firewall.ps1 then retest."
}
