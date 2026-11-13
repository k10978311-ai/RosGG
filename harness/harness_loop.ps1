# One dual-device harness iteration: env sync, reachability, optional PLAY tap, artifacts.
param(
    [switch]$TapPlay,
    [switch]$LdOnly,
    [int]$WaitSeconds = 40,
    [string]$ReplyVariant = ""
)

$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
. (Join-Path $Root "adb_common.ps1")

if ($ReplyVariant) { $env:REPLY_VARIANT = $ReplyVariant }
$ts = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
$capDir = Join-Path $PSScriptRoot "captures"
New-Item -ItemType Directory -Force -Path $capDir | Out-Null

Write-Host "=== RoS harness iteration $ts ==="

& powershell -ExecutionPolicy Bypass -File (Join-Path $Root "sync_server_list.ps1") | Out-Host
$verify = & powershell -ExecutionPolicy Bypass -File (Join-Path $Root "verify_play_path.ps1") 2>&1 | Out-String

# Capture file stats before PLAY
$gateBefore = if (Test-Path "gate_capture.bin") { (Get-Item "gate_capture.bin").Length } else { 0 }
$tcpBefore = if (Test-Path "tcp_gate_capture.bin") { (Get-Item "tcp_gate_capture.bin").Length } else { 0 }

$deviceResults = @{}

$targets = if ($LdOnly) { @("ldplayer") } else { @("ldplayer", "phone") }
foreach ($target in $targets) {
    try {
        $serial = Resolve-RosSerial -Target $target
    } catch {
        $deviceResults[$target] = @{ status = "absent"; serial = $null }
        continue
    }
    if (-not $serial) {
        $deviceResults[$target] = @{ status = "absent"; serial = $null }
        continue
    }

    Write-Host "`n--- $target ($serial) ---"
    & $RosAdb -s $serial shell "am force-stop $RosPackage" | Out-Null
    & $RosAdb -s $serial logcat -c | Out-Null
    & $RosAdb -s $serial shell "monkey -p $RosPackage -c android.intent.category.LAUNCHER 1" | Out-Null
    Start-Sleep -Seconds 12

    if ($TapPlay) {
        # Approximate PLAY button region (1920x1080 landscape); adjust per device in STATE if needed
        & $RosAdb -s $serial shell "input tap 960 820" | Out-Null
        Start-Sleep -Seconds ($WaitSeconds - 12)
    } else {
        Start-Sleep -Seconds ($WaitSeconds - 12)
    }

    $stamp = "$ts" -replace "[:T]", "-"
    $shot = Join-Path $capDir "${stamp}_${target}.png"
    $tmpCap = Join-Path $env:TEMP "ros_cap_$serial.png"
    & cmd /c "`"$RosAdb`" -s $serial exec-out screencap -p > `"$tmpCap`""
    if (Test-Path $tmpCap) { Move-Item -Force $tmpCap $shot }

    $logPath = Join-Path $capDir "${stamp}_${target}_script.log"
    $patterns = "Mercury|mercury|BigWorld|ServerConnection|ServerConn|logOn|LogOn|logOnBegin|logOnComplete|onLoginReply|LoginHandler|BaseAppLogin|REASON_|Nub::|Bundle::|Failed to connect|25000|neox::bwclient|SCRIPT"
    & $RosAdb -s $serial logcat -d -v time 2>$null |
        Select-String -Pattern $patterns |
        ForEach-Object { $_.Line.Substring(0, [Math]::Min(400, $_.Line.Length)) } |
        Set-Content $logPath

    $mercuryPath = Join-Path $capDir "${stamp}_${target}_mercury.log"
    & $RosAdb -s $serial logcat -d 2>$null |
        Select-String -Pattern "bwclient|BWClient|Mercury|bwserver|ServerConnection" |
        ForEach-Object { $_.Line.Substring(0, [Math]::Min(500, $_.Line.Length)) } |
        Set-Content $mercuryPath

    $pingOk = (& $RosAdb -s $serial shell "ping -c 1 -W 2 $RosPcIp 2>&1") -match "1 received"
    $deviceResults[$target] = @{
        status       = "ok"
        serial       = $serial
        screenshot   = $shot
        script_log   = $logPath
        ping_pc      = [bool]$pingOk
        log_lines    = (Get-Content $logPath -ErrorAction SilentlyContinue | Measure-Object).Count
    }
}

$gateAfter = if (Test-Path "gate_capture.bin") { (Get-Item "gate_capture.bin").Length } else { 0 }
$tcpAfter = if (Test-Path "tcp_gate_capture.bin") { (Get-Item "tcp_gate_capture.bin").Length } else { 0 }

$parseOut = ""
try {
    $parseOut = python (Join-Path $Root "scratch\parse_baseapp.py") 2>&1 | Select-Object -Last 8 | Out-String
} catch {
    $parseOut = $_.Exception.Message
}

$entry = [ordered]@{
    timestamp          = $ts
    ros_pc_ip          = $RosPcIp
    reply_variant      = $env:REPLY_VARIANT
    tap_play           = [bool]$TapPlay
    gate_capture_delta = $gateAfter - $gateBefore
    tcp_capture_delta  = $tcpAfter - $tcpBefore
    devices            = $deviceResults
    parse_tail         = $parseOut.Trim()
    verify_snippet     = ($verify -split "`n" | Select-Object -First 12) -join "`n"
}

$logFile = Join-Path $PSScriptRoot "iteration_log.jsonl"
($entry | ConvertTo-Json -Compress -Depth 6) | Add-Content -Encoding utf8 $logFile

# Refresh STATE last_run
$statePath = Join-Path $PSScriptRoot "STATE.json"
if (Test-Path $statePath) {
    $state = Get-Content $statePath -Raw | ConvertFrom-Json
    $state | Add-Member -NotePropertyName last_run -NotePropertyValue $ts -Force
    $state | Add-Member -NotePropertyName gate_capture_bytes -NotePropertyValue $gateAfter -Force
    $state | ConvertTo-Json -Depth 6 | Set-Content $statePath
}

Write-Host "`n[+] Logged iteration -> harness/iteration_log.jsonl"
Write-Host $parseOut
