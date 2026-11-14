# Inbound allow rules for the RoS private harness (run as Administrator).
#Requires -RunAsAdministrator
param([switch]$Remove)

$portsTcp = @(80, 443, 20001, 25000)
$portsUdp = @(53, 20001, 25000)
$name = "RoS Private Harness"

if ($Remove) {
    Get-NetFirewallRule -DisplayName $name -ErrorAction SilentlyContinue | Remove-NetFirewallRule
    Write-Host "Removed firewall rule '$name'."
    exit
}

$existing = Get-NetFirewallRule -DisplayName $name -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Rule '$name' already exists."
    exit
}

New-NetFirewallRule -DisplayName $name -Direction Inbound -Action Allow -Profile Private -Protocol TCP -LocalPort $portsTcp | Out-Null
New-NetFirewallRule -DisplayName $name -Direction Inbound -Action Allow -Profile Private -Protocol UDP -LocalPort $portsUdp | Out-Null
Write-Host "[+] Allowed inbound TCP $($portsTcp -join ',') and UDP $($portsUdp -join ',') on Private networks."
