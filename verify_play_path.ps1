# Pre-flight checks before pressing PLAY (IP in server list, PC listeners, firewall, device reachability).
. "$PSScriptRoot\adb_common.ps1"

$ip = $RosPcIp
$listFile = Join-Path $PSScriptRoot "real\server_list_ad.local.txt"
$listLine = (Get-Content $listFile -First 1).Trim()
Write-Host "PC harness IP (ROS_PC_IP): $ip"
Write-Host "server_list_ad.local.txt:  $listLine"

if ($listLine -match '127\.0\.0\.1|0\.0\.0\.0') {
    Write-Warning "server list still points at loopback — run sync_server_list.ps1"
}
if ($listLine -notmatch [regex]::Escape($ip)) {
    Write-Warning "server list IP does not match ROS_PC_IP — run sync_server_list.ps1"
}

$ports = @(53, 80, 443, 20001, 25000)
Write-Host "`nPC listeners (must be LISTENING while servers run):"
foreach ($port in $ports) {
    $c = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    $cu = Get-NetUDPEndpoint -LocalPort $port -ErrorAction SilentlyContinue
    $tcp = if ($c) { "TCP ok" } else { "TCP --" }
    $udp = if ($cu) { "UDP ok" } else { "UDP --" }
    Write-Host ("  {0,5}  {1}  {2}" -f $port, $tcp, $udp)
}

Write-Host "`nNote: Fast Private-Server uses the three :25000 entries (BigWorld Mercury UDP+TCP)."
Write-Host "      Port 20001 is legacy JSON / Frida redirect — not in server_list_ad.local.txt."

foreach ($d in (Get-RosDevices)) {
    $s = $d.Serial
    Write-Host "`n--- Device $s ---"
    $ping = (& $RosAdb -s $s shell "ping -c 1 -W 2 $ip 2>&1") -join " "
    if ($ping -match "1 received") { Write-Host "[+] ping $ip" } else { Write-Warning "ping failed: $ping" }
    foreach ($port in @(25000, 20001)) {
        $r = & $RosAdb -s $s shell "sh -c '(echo >/dev/tcp/$ip/$port) 2>/dev/null && echo open || echo closed'" 2>&1
        Write-Host "  TCP $port -> $($r.Trim())"
    }
}

Write-Host "`nIf TCP is closed: start ros_mock_server.py + dns_server.py (Admin) and run setup_firewall.ps1 (Admin)."
Write-Host "If TCP opens but PLAY fails: watch for [UDP GATE:25000] LOGIN in server console (Mercury login, not TCP gate handshake)."
