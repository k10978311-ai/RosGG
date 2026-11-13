# Shared ADB helpers for LDPlayer + physical device testing.
$script:RosAdb = @(
    "E:\LDPlayer\LDPlayer9\adb.exe",
    "C:\LDPlayer\LDPlayer9\adb.exe",
    "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $script:RosAdb) {
    throw "adb.exe not found. Install LDPlayer adb or Android platform-tools."
}

# PC LAN IP used by dns_server / ros_mock_server (override with $env:ROS_PC_IP).
$script:RosPcIp = if ($env:ROS_PC_IP) { $env:ROS_PC_IP } else { "192.168.100.137" }

$script:RosPackage = "com.netease.chiji"
$script:RosPubKey = Join-Path $PSScriptRoot "server_keys\loginapp.pubkey"
$script:RosKeyRemote = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/entities/loginapp.pubkey"

function Get-RosDevices {
    $lines = & $script:RosAdb devices | Select-Object -Skip 1
    foreach ($line in $lines) {
        if ($line -match "^(?<id>\S+)\s+device") {
            [PSCustomObject]@{ Serial = $Matches.id; Line = $line }
        }
    }
}

function Resolve-RosSerial {
    param(
        [ValidateSet("auto", "phone", "ldplayer", "emulator")]
        [string]$Target = "auto",
        [string]$Serial = ""
    )
    if ($Serial) { return $Serial }
    $devs = Get-RosDevices
  if ($Target -eq "phone") {
        return ($devs | Where-Object { $_.Serial -notmatch "^emulator-" } | Select-Object -First 1).Serial
    }
    if ($Target -in @("ldplayer", "emulator")) {
        return ($devs | Where-Object { $_.Serial -match "^emulator-" } | Select-Object -First 1).Serial
    }
    # auto: prefer phone if present, else emulator
    $phone = $devs | Where-Object { $_.Serial -notmatch "^emulator-" } | Select-Object -First 1
    if ($phone) { return $phone.Serial }
    return ($devs | Select-Object -First 1).Serial
}

function Push-RosLoginPubKey {
    param([string]$Serial)
    if (-not (Test-Path $script:RosPubKey)) {
        Write-Warning "Missing $script:RosPubKey"
        return
    }
    # Single-quoted shell arg: PowerShell treats /emulated/0/ as division in double quotes.
    & $script:RosAdb -s $Serial shell "mkdir -p '/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/res/entities'" | Out-Null
    & $script:RosAdb -s $Serial push $script:RosPubKey $script:RosKeyRemote | Out-Null
    Write-Host "[+] loginapp.pubkey -> $Serial"
}
