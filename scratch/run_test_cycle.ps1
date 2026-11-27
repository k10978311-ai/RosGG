. .\adb_common.ps1
$serial = "emulator-5554"

Write-Host "[1/7] Stopping app on $serial..."
& $script:RosAdb -s $serial shell "am force-stop com.netease.chiji"
& $script:RosAdb -s $serial logcat -c

Write-Host "[2/7] Launching RoS..."
& $script:RosAdb -s $serial shell "monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1"

Write-Host "[3/7] Waiting 26s for title screen..."
Start-Sleep -Seconds 26

Write-Host "[4/7] Closing notice popup if present (1535, 100)..."
& $script:RosAdb -s $serial shell "input tap 1535 100"
Start-Sleep -Seconds 2
& $script:RosAdb -s $serial shell "input tap 1535 100"
Start-Sleep -Seconds 1

Write-Host "[5/7] Tapping PLAY (800, 680)..."
& $script:RosAdb -s $serial shell "input tap 800 680"

Write-Host "[6/7] Waiting for Avatar -> Athlete -> Hall transition (monitoring every 10s up to 60s)..."
for ($i = 1; $i -le 6; $i++) {
    Start-Sleep -Seconds 10
    $elapsed = $i * 10
    Write-Host "   [$elapsed s] Capturing intermediate screenshot..."
    & $script:RosAdb -s $serial shell "screencap -p /sdcard/screen.png"
    & $script:RosAdb -s $serial pull /sdcard/screen.png "scratch/screen_${elapsed}s.png"
}

Write-Host "[7/7] Saving final screenshot..."
Copy-Item "scratch/screen_60s.png" "scratch/screen_latest.png" -Force
Write-Host "Test cycle complete!"
