# Local agent wake loop — run in background; pair with Cursor /loop skill on AGENT_LOOP_TICK_ROS.
param(
    [int]$IntervalMinutes = 15,
    [switch]$TapPlay
)

$Root = Split-Path $PSScriptRoot -Parent
$prompt = "RoS harness tick: run harness/harness_loop.ps1"
if ($TapPlay) { $prompt += " -TapPlay" }
$prompt += "; read harness/iteration_log.jsonl tail; update harness/last_report.md; one minimal fix in loginapp or ros_mock_server if evidence supports it. Read AGENTS.md."

$seconds = $IntervalMinutes * 60
Write-Host "RoS loop every ${IntervalMinutes}m. Sentinel: AGENT_LOOP_TICK_ROS"
Write-Host "First tick after sleep; run harness once now if desired."

$loopArgs = @("-ExecutionPolicy", "Bypass", "-File", (Join-Path $PSScriptRoot "harness_loop.ps1"))
if ($TapPlay) { $loopArgs += "-TapPlay" }
& powershell @loopArgs | Out-Host

while ($true) {
    Start-Sleep -Seconds $seconds
    $payload = @{ prompt = $prompt } | ConvertTo-Json -Compress
    Write-Output "AGENT_LOOP_TICK_ROS $payload"
}
