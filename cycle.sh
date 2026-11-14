#!/usr/bin/env bash
# Relaunch the game, wait, then dump NeoX <SCRIPT> logs + screenshot.  Usage: bash cycle.sh [wait_seconds]
cd "$(dirname "$0")"
if [ -f "/e/LDPlayer/LDPlayer9/adb.exe" ]; then
    ADB=/e/LDPlayer/LDPlayer9/adb.exe
else
    ADB=/c/LDPlayer/LDPlayer9/adb.exe
fi
WAIT=${1:-45}
$ADB shell am force-stop com.netease.chiji
$ADB logcat -c
$ADB shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
sleep "$WAIT"
PID=$($ADB shell pidof com.netease.chiji | tr -d '\r')
echo "pid=$PID"
$ADB logcat -d -v time 2>/dev/null | grep -E "<SCRIPT>|AndroidRuntime|FATAL" | cut -c1-400 > script_log.txt
$ADB exec-out screencap -p > shot.png
wc -l < script_log.txt
