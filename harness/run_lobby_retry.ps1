# Retry lobby path: LoginApp A/B then TAP PLAY (LD only).
param(
    [int]$Variant = 24,
    [string]$BaseAppVariant = "3",
    [switch]$KeepSession
)

$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
$env:ROS_PC_IP = if ($env:ROS_PC_IP) { $env:ROS_PC_IP } else { "192.168.100.137" }
$env:BF_SPEC = "1:4"
$env:BASEAPP_REPLY_VARIANT = $BaseAppVariant
$env:STUB_8080 = "on"
$env:SESSION_U32 = if ($env:SESSION_U32) { $env:SESSION_U32 } else { "0x11223344" }
$env:REPLY_VARIANT = "$Variant"

. "$Root\adb_common.ps1"
$adb = $RosAdb
$serial = Resolve-RosSerial -Target ldplayer
# logcat cleared inside harness_loop before launch

Write-Host "`n========== REPLY_VARIANT=$Variant ==========" -ForegroundColor Cyan
Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object { $_.CommandLine -match 'ros_mock_server' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep 1
$py = "C:\Users\LUFY\AppData\Local\Programs\Python\Python312\python.exe"
Start-Process -FilePath $py -ArgumentList "-u", "ros_mock_server.py" -WorkingDirectory $Root -WindowStyle Normal | Out-Null
Start-Sleep 2
$ldSplat = @{ TapPlay = $true }
if ($KeepSession) { $ldSplat.KeepSession = $true }
& "$PSScriptRoot\ld_debug.ps1" @ldSplat

if ($serial) {
    $hits = & $adb -s $serial logcat -d 2>&1 | Select-String -Pattern "onLoginReply|convertAddress|logOnComplete|LOGGED_ON|createBasePlayer|Unable to connect to BaseApp"
    $log = Get-ChildItem "$PSScriptRoot\captures\*_ldplayer_script.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($log) {
        $hits = Get-Content $log.FullName -ErrorAction SilentlyContinue | Select-String -Pattern "onLoginReply|convertAddress|logOnComplete"
    }
    if ($hits) { $hits | Select-Object -Last 10 | ForEach-Object { Write-Host $_ } }
    else { Write-Host "(no Mercury lines in logcat — check screenshot)" -ForegroundColor Yellow }
}

Write-Host "`nScreenshot: harness/captures/ (latest *_ldplayer.png)"
