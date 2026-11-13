# Rewrite game-server IPs in real/server_list_ad.local.txt to match $env:ROS_PC_IP (or adb_common default).
. "$PSScriptRoot\adb_common.ps1"

$path = Join-Path $PSScriptRoot "real\server_list_ad.local.txt"
if (-not (Test-Path $path)) { throw "Missing $path" }

$ip = $RosPcIp
$line = Get-Content $path -Raw
$updated = [regex]::Replace(
    $line,
    '\d{1,3}(?:\.\d{1,3}){3}:(\d+)',
    { param($m) "$ip`:$($m.Groups[1].Value)" }
)
if ($line -ne $updated) {
    Set-Content -Path $path -Value $updated.TrimEnd() -NoNewline
    Write-Host "[+] Updated server_list_ad.local.txt -> $ip (ports preserved)"
} else {
    Write-Host "[=] server_list_ad.local.txt already uses $ip"
}
Write-Host (Get-Content $path -First 1)
