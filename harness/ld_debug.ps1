# LDPlayer-only debug cycle (emulator-5554).
param([switch]$TapPlay, [switch]$FridaDiag)

$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$env:ROS_PC_IP = if ($env:ROS_PC_IP) { $env:ROS_PC_IP } else { "192.168.100.137" }
$env:REPLY_VARIANT = if ($env:REPLY_VARIANT) { $env:REPLY_VARIANT } else { "24" }
$env:BF_SPEC = if ($env:BF_SPEC) { $env:BF_SPEC } else { "1:4" }
$env:BASEAPP_ACK = "off"
$env:BASEAPP_REPLY_VARIANT = if ($env:BASEAPP_REPLY_VARIANT) { $env:BASEAPP_REPLY_VARIANT } else { "1" }

Write-Host "=== LDPlayer debug ===" -ForegroundColor Cyan
Write-Host "ROS_PC_IP=$env:ROS_PC_IP REPLY_VARIANT=$env:REPLY_VARIANT BASEAPP_REPLY_VARIANT=$env:BASEAPP_REPLY_VARIANT"

& powershell -ExecutionPolicy Bypass -File "$Root\setup_emulator.ps1"
& powershell -ExecutionPolicy Bypass -File "$Root\verify_play_path.ps1"

$harnessArgs = @("-ExecutionPolicy", "Bypass", "-File", "$PSScriptRoot\harness_loop.ps1", "-LdOnly")
if ($TapPlay) { $harnessArgs += "-TapPlay" }
& powershell @harnessArgs

if ($FridaDiag) {
    Write-Host "`n--- Frida diag (emulated realm) ---"
    $job = Start-Job { param($r) Set-Location $r; python run_frida.py diag.js --attach --realm emulated 2>&1 | Select-Object -First 25 } -ArgumentList $Root
    Start-Sleep -Seconds 8
    Receive-Job $job -ErrorAction SilentlyContinue | Write-Host
    Stop-Job $job -ErrorAction SilentlyContinue; Remove-Job $job -ErrorAction SilentlyContinue
}

Write-Host "`nWatch PC console for: [UDP GATE:25000] LOGIN  then  [BASEAPP] SENT REPLY"
Write-Host "Artifacts: harness/captures/*_ldplayer*  gate_capture.bin  server terminal output"
