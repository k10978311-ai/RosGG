#!/usr/bin/env bash
# Relaunch RoS, wait for the auto-connect, then dump the client's Mercury ("M" tag) log.
# Usage: bash mcycle.sh [wait_seconds] [tap_play:0|1]
cd /c/Users/Lufy/Desktop/Server
export MSYS_NO_PATHCONV=1
ADB=/c/LDPlayer/LDPlayer9/adb.exe
WAIT=${1:-100}
TAP=${2:-0}
if [ "$TAP" = "1" ]; then
  $ADB logcat -c
  $ADB shell input tap 790 660
else
  $ADB shell am force-stop com.netease.chiji
  $ADB logcat -c
  $ADB shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
fi
sleep "$WAIT"
$ADB logcat -d -v time 2>/dev/null | grep -a " M (" | sed -E 's/^([0-9-]+ [0-9:.]+).*\] M \( *[0-9]+\): /\1 /' | cut -c1-320 > mercury_log.txt
$ADB logcat -d -v time 2>/dev/null | grep -a "<SCRIPT>" | cut -c1-320 > script_log.txt
$ADB exec-out screencap -p > scratch_shot1.png
echo "mercury lines: $(wc -l < mercury_log.txt)  script lines: $(wc -l < script_log.txt)"
