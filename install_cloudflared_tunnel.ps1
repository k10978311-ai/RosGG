# Install and start Cloudflare Tunnel as a Windows service (run PowerShell as Administrator).
# The tunnel complements ros_mock HTTPS; it does NOT replace dns_server.py UDP/53 for Wi‑Fi DNS on the phone.
param(
    [Parameter(Mandatory = $true)]
    [string]$Token,
    [switch]$Uninstall
)

$cf = Join-Path $PSScriptRoot "cloudflared.exe"
if (-not (Test-Path $cf)) {
    throw "Missing $cf — download from https://github.com/cloudflare/cloudflared/releases"
}

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    throw "Run this script in an elevated PowerShell (Administrator)."
}

if ($Uninstall) {
    & $cf service uninstall
    Write-Host "[+] cloudflared service uninstalled."
    exit 0
}

& $cf service install $Token
Write-Host "[+] Service installed. Starting..."
& $cf service start
Get-Service cloudflared -ErrorAction SilentlyContinue | Format-List Name, Status, StartType
Write-Host ""
Write-Host "Also run (Admin): dns_server.py + ros_mock_server.py"
Write-Host "Note10+: setup_device.ps1 then set Wi‑Fi DNS to `$env:ROS_PC_IP (default 192.168.1.18)."