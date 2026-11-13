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

Write-Host "`nPing $RosPcIp from phone: $(if ($pingOk) { 'OK' } else { 'FAIL' })"
if (-not $pingOk) { Write-Host $ping }

$pubkey = (& $RosAdb -s $serial shell "test -f '/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/entities/loginapp.pubkey' && echo ok").Trim()

Write-Host "`nloginapp.pubkey on device: $pubkey"
Write-Host "CA in Download: $(if ((& $RosAdb -s $serial shell 'test -f /sdcard/Download/ros_harness_ca.crt && echo yes').Trim() -eq 'yes') {'yes'} else {'missing'})"

if ($phonePrefix -ne $pcPrefix -and -not $pingOk) {
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
} elseif ($pingOk) {
    Write-Host "`n[+] L3 OK — if PLAY still fails: install CA, set Wi-Fi DNS to $RosPcIp, run servers + setup_firewall.ps1"
}
