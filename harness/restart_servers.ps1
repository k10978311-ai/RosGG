# Restart dns + ros_mock with Athlete/lobby env (detached). Existing listeners on 53/443 are stopped first.
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
. (Join-Path $Root "adb_common.ps1")

$pcIp = $RosPcIp
$py = Join-Path $Root ".venv\Scripts\python.exe"

$envLines = @(
    "ROS_PC_IP=$pcIp",
    "REPLY_VARIANT=24",
    "BASEAPP_REPLY_VARIANT=3",
    "CBP_TYPE=41",
    "CBP_PROPS=account",
    "SWITCH_TO=athlete",
    "AVATAR_ENTITY=Avatar",
    "AVATAR_MAP=701",
    "AVATAR_CHAR=30001",
    "AVATAR_CAMP=30",
    "AUTO_TRANSITION_HALL=on",
    "TRANSITION_DELAY=2.5",
    "HALL_DELAY=2.0",
    "ATHLETE_CELL=off",
    "ATHLETE_CAN_CREATE_ROOM=1",
    "ATHLETE_PKG_CAPACITY=64",
    "STUB_8080=on",
    "started=$(Get-Date -Format o)"
)
$envLines | Set-Content (Join-Path $PSScriptRoot "SERVER_ENV.txt") -Encoding utf8

foreach ($port in @(53, 80, 443, 20001, 25000)) {
    $pids = @()
    $pids += Get-NetUDPEndpoint -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    $pids += Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
    foreach ($procId in ($pids | Sort-Object -Unique)) {
        if ($procId -gt 0 -and (Get-Process -Id $procId -ErrorAction SilentlyContinue).ProcessName -eq "python") {
            Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
        }
    }
}
Start-Sleep -Seconds 2

Start-Process -FilePath $py -ArgumentList "-u", "dns_server.py" -WorkingDirectory $Root `
    -RedirectStandardOutput (Join-Path $Root "dns.stdout.log") `
    -RedirectStandardError (Join-Path $Root "dns.stderr.log") -WindowStyle Minimized

$cmd = @"
Set-Location '$Root'
`$env:ROS_PC_IP='$pcIp'
`$env:REPLY_VARIANT='24'
`$env:BASEAPP_REPLY_VARIANT='3'
`$env:CBP_TYPE='41'
`$env:CBP_PROPS='account'
`$env:SWITCH_TO='athlete'
`$env:AVATAR_ENTITY='Avatar'
`$env:AVATAR_MAP='701'
`$env:AVATAR_CHAR='30001'
`$env:AVATAR_CAMP='30'
`$env:AUTO_TRANSITION_HALL='on'
`$env:TRANSITION_DELAY='2.5'
`$env:HALL_DELAY='2.0'
`$env:ATHLETE_CELL='off'
`$env:ATHLETE_CAN_CREATE_ROOM='1'
`$env:ATHLETE_PKG_CAPACITY='64'
`$env:STUB_8080='on'
& '$py' -u ros_mock_server.py *>> '$Root\server.stdout.log' 2>> '$Root\server.stderr.log'
"@
Start-Process powershell -ArgumentList "-NoProfile", "-Command", $cmd -WindowStyle Minimized
Start-Sleep -Seconds 5

foreach ($port in @(53, 80, 443, 25000)) {
    $tcp = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    $udp = Get-NetUDPEndpoint -LocalPort $port -ErrorAction SilentlyContinue
    Write-Host ("Port {0,5}  tcp={1}  udp={2}" -f $port, [bool]$tcp, [bool]$udp)
}
Write-Host "[+] Athlete/lobby env — harness/SERVER_ENV.txt"