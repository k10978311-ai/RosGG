# Load config.cmd (+ config.local.cmd), set ROS_PC_IP, sync server list, print device DNS hint.
. "$PSScriptRoot\adb_common.ps1"

$env:ROS_PC_IP = $RosPcIp
& "$PSScriptRoot\sync_server_list.ps1"

Write-Host ""
Write-Host "Active harness IP: $RosPcIp"
if ($RosPhoneSerial) { Write-Host "Phone serial:      $RosPhoneSerial" }
Write-Host "Note10+ Wi-Fi DNS: set Static -> DNS 1 = $RosPcIp (Private DNS Off)"
Write-Host "Then: .\setup_device.ps1   and   .\harness\fix_mobile_connect.ps1"