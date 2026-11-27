#!/usr/bin/env bash
# Relaunch RoS, wait until the main menu fetched notice_pc_hw.txt (server.log), dismiss the Events
# popup, tap PLAY, wait, then print filtered client Mercury + <SCRIPT> logs.
# Usage: bash harness/play_cycle.sh [wait_after_play_s=60]
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
A="/c/LDPlayer/LDPlayer9/adb.exe -s ${ADB_SERIAL:-emulator-5554}"
WAIT=${1:-60}
before=$(grep -c 'notice_pc_hw.txt' server.log)
$A shell am force-stop com.netease.chiji
$A logcat -G 16M 2>/dev/null; $A logcat -c
$A shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
i=0
until [ "$(grep -c 'notice_pc_hw.txt' server.log)" -gt "$before" ] || [ $i -ge 80 ]; do sleep 3; i=$((i+1)); done
echo "[menu after $((i*3))s]"
sleep 25   # the Events popup is drawn well after the notice fetch
$A shell input tap 1538 89
sleep 2
$A shell input tap 790 660
sleep "$WAIT"
$A logcat -d -v time 2>/dev/null | grep -a " M (" | sed -E 's/^([0-9-]+ [0-9:.]+).*\] M \( *[0-9]+\): /\1 /' | cut -c1-330 > mercury_log.txt
$A logcat -d -v time 2>/dev/null | grep -a "<SCRIPT>" | cut -c1-400 > script_log.txt
$A exec-out screencap -p > scratch_shot1.png
echo "=== CLIENT (Mercury, from logOnBegin)"
sed -n '/logOnBegin/,$p' mercury_log.txt | sed -E 's/^[0-9-]+ //' | grep -vE "texture format|PublicKey|recreateListening|convertAddress|checkScriptBase|minUnackPacket|Couldn't find handler|setCustomClassFunctions|Resending|Load sound|Audio::|FMOD|AUIDO|StaticTest invalid" | cut -c1-260 | head -50
echo "=== CLIENT (<SCRIPT>)"
sed -E 's/^.*<SCRIPT> \( *[0-9]+\): //' script_log.txt | grep -vE "fetch_by_domain|http_get|verify_result|should be initialized|CythonOverrides|LINYUAN|trouger|fubingnan|process_result|hardware_inst|settingLang|patch_lang|hotfix|fbn|This is a test|modified|axeso|natproxy|_fetch_http|Volumes/Samsung" | cut -c1-260 | tail -45
