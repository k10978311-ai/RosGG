# A/B LoginApp reply variants without editing code (restart ros_mock_server between runs).
param(
    [int[]]$Variants = @(22, 24),
    [switch]$TapPlay
)

$Root = Split-Path $PSScriptRoot -Parent
Write-Host "Run each variant with a FRESH ros_mock_server.py process."
foreach ($v in $Variants) {
    Write-Host "`n========== REPLY_VARIANT=$v =========="
    $env:REPLY_VARIANT = "$v"
    $env:BF_SPEC = "1:16"
    $env:BASEAPP_ACK = "off"
    $env:BASEAPP_REPLY_VARIANT = "1"
    Write-Host "Set in server terminal: `$env:REPLY_VARIANT='$v' then restart python ros_mock_server.py"
    $null = Read-Host "Press Enter when server restarted and game at PLAY"
    & "$PSScriptRoot\harness_loop.ps1" @(
        if ($TapPlay) { "-TapPlay" }
    )
}
