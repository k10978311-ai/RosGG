# After the PC joins the SAME Wi-Fi as the phone (e.g. Ruijie-2 / 192.168.8.x), set ROS_PC_IP and sync server list.
. "$PSScriptRoot\..\adb_common.ps1"

$phone = Resolve-RosSerial -Target phone
$phoneIp = (& $RosAdb -s $phone shell "ip -4 addr show wlan0" 2>$null | Select-String "inet (\d+\.\d+\.\d+\.\d+)")
if ($phoneIp -match "inet (\d+\.\d+\.\d+)\.\d+") {
    $wantPrefix = $Matches[1]
    Write-Host "Phone on $wantPrefix.x (wlan0)"
} else {
    throw "Phone wlan0 has no IPv4 — connect phone to Wi-Fi."
}

$pcIp = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -like "$wantPrefix.*" -and $_.PrefixOrigin -ne "WellKnown" } |
    Select-Object -First 1 -ExpandProperty IPAddress

if (-not $pcIp) {
    Write-Host @"
PC is not on $wantPrefix.x yet.

On this PC: connect Wi-Fi to the same network as the phone (SSID from fix_mobile_connect.ps1),
then run this script again.
"@
    & "$PSScriptRoot\fix_mobile_connect.ps1"
    exit 1
}

$env:ROS_PC_IP = $pcIp
Write-Host "[+] ROS_PC_IP = $pcIp"

& "$PSScriptRoot\..\sync_server_list.ps1"
& "$PSScriptRoot\..\setup_device.ps1"

$ping = (& $RosAdb -s $phone shell "ping -c 2 -W 2 $pcIp 2>&1") -match "1 received|2 received"
if ($ping) {
    Write-Host "[+] Phone pings PC — set phone Wi-Fi DNS 1 = $pcIp , install ros_harness_ca.crt , restart dns_server + ros_mock_server"
} else {
    Write-Host "[-] Ping still failing — check Windows Firewall (setup_firewall.ps1)"
}
