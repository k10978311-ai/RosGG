$RosAdb = "C:\LDPlayer\LDPlayer9\adb.exe"
$serial = "emulator-5554"

Write-Host "Tapping PLAY (800, 730)..." -ForegroundColor Cyan
& $RosAdb -s $serial shell "input tap 800 730"

$timestamps = @(5, 15, 25, 35, 45, 55, 65)
foreach ($t in $timestamps) {
    Start-Sleep -Seconds 10
    Write-Host "[$t s] Capturing screenshot..."
    & $RosAdb -s $serial shell "screencap -p /sdcard/screen.png"
    & $RosAdb -s $serial pull /sdcard/screen.png "scratch/screen_stage_${t}s.png"
}

Copy-Item "scratch/screen_stage_65s.png" "scratch/screen_final.png" -Force
Write-Host "Play and monitor cycle complete!" -ForegroundColor Green
