# One-command harness env + reminder to restart mock server.
. "$PSScriptRoot\..\adb_common.ps1"

$env:ROS_PC_IP = $RosPcIp
$env:REPLY_VARIANT = if ($env:REPLY_VARIANT) { $env:REPLY_VARIANT } else { "24" }
$env:BF_SPEC = "1:16"
$env:BASEAPP_ACK = "off"
$env:BASEAPP_REPLY_VARIANT = if ($env:BASEAPP_REPLY_VARIANT) { $env:BASEAPP_REPLY_VARIANT } else { "1" }

Write-Host "ROS_PC_IP=$env:ROS_PC_IP REPLY_VARIANT=$env:REPLY_VARIANT BASEAPP_REPLY_VARIANT=$env:BASEAPP_REPLY_VARIANT"
Write-Host "Restart ros_mock_server.py in another window if code changed, then press Enter..."
$null = Read-Host

& "$PSScriptRoot\harness_loop.ps1" @args
