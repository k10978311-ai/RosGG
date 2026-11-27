$RosAdb = "C:\LDPlayer\LDPlayer9\adb.exe"
$serial = "emulator-5554"

Write-Host "=== Starting Full Lobby Test on $serial ===" -ForegroundColor Cyan

# 1. Force stop and clear logcat
Write-Host "[1/6] Stopping app and clearing logcat..."
& $RosAdb -s $serial shell "am force-stop com.netease.chiji"
& $RosAdb -s $serial logcat -c
Start-Sleep -Seconds 2

# 2. Launch RoS
Write-Host "[2/6] Launching RoS..."
& $RosAdb -s $serial shell "monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1"

# 3. Wait for title screen and notice
Write-Host "[3/6] Waiting 28s for title screen..."
Start-Sleep -Seconds 28

# 4. Dismiss notice popup (tap close button at 1535, 100)
Write-Host "[4/6] Dismissing notice popup..."
& $RosAdb -s $serial shell "input tap 1535 100"
Start-Sleep -Seconds 2
& $RosAdb -s $serial shell "input tap 1535 100"
Start-Sleep -Seconds 2

# Capture menu screen
& $RosAdb -s $serial shell "screencap -p /sdcard/screen.png"
& $RosAdb -s $serial pull /sdcard/screen.png "scratch/screen_menu_test.png"

# 5. Tap PLAY (800, 730)
Write-Host "[5/6] Tapping PLAY (800, 730)..."
& $RosAdb -s $serial shell "input tap 800 730"

# 6. Wait and monitor transition
Write-Host "[6/6] Monitoring transition (taking screenshots every 10s up to 60s)..."
for ($i = 1; $i -le 6; $i++) {
    Start-Sleep -Seconds 10
    $elapsed = $i * 10
    Write-Host "   [$elapsed s] Capturing screenshot..."
    & $RosAdb -s $serial shell "screencap -p /sdcard/screen.png"
    & $RosAdb -s $serial pull /sdcard/screen.png "scratch/screen_test_${elapsed}s.png"
}

Copy-Item "scratch/screen_test_60s.png" "scratch/screen_lobby_success.png" -Force
Write-Host "=== Test Complete ===" -ForegroundColor Green
