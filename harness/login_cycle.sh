#!/usr/bin/env bash
# Full login cycle on LDPlayer: relaunch RoS, dismiss Events popup, tap PLAY, then print the
# client's Mercury log (from logOnBegin), filtered <SCRIPT> output, and server-side BaseApp notes.
# Usage: bash harness/login_cycle.sh [wait_after_play_s=35]
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
A=/c/LDPlayer/LDPlayer9/adb.exe
WAIT=${1:-35}
$A shell am force-stop com.netease.chiji
$A logcat -c
$A shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
# wait until the main menu is up (client logs ui/ui_enter_game_new), max ~240s
for i in $(seq 1 48); do
  sleep 5
  if $A logcat -d 2>/dev/null | grep -aq "ui_enter_game_new"; then echo "[menu after $((i*5))s]"; break; fi
done
sleep 4
$A shell input tap 1538 89     # close Events popup (if shown)
sleep 2
$A shell input tap 795 556     # Confirm on a dialog (if shown)
sleep 3
$A shell input tap 790 660     # PLAY
sleep "$WAIT"
$A logcat -d -v time 2>/dev/null | grep -a " M (" | sed -E 's/^([0-9-]+ [0-9:.]+).*\] M \( *[0-9]+\): /\1 /' | cut -c1-330 > mercury_log.txt
$A logcat -d -v time 2>/dev/null | grep -a "<SCRIPT>" | cut -c1-400 > script_log.txt
$A exec-out screencap -p > scratch_shot1.png
echo "=== CLIENT (Mercury)"
sed -n '/logOnBegin/,$p' mercury_log.txt | sed -E 's/^[0-9-]+ //' | grep -v "texture format" | cut -c1-300 | head -60
echo "=== CLIENT (<SCRIPT>)"
sed -E 's/^.*<SCRIPT> \( *[0-9]+\): //' script_log.txt | grep -vE "fetch_by_domain|http_get|verify_result|should be initialized|CythonOverrides|LINYUAN|trouger|fubingnan|process_result|hardware_inst|settingLang|patch_lang" | cut -c1-300 | tail -40
echo "=== SERVER"
grep -E "fragment|Athlete|handshake|client msgs: \[\(1, '44332211'\), \((1[0-9][0-9]|2[0-9][0-9])" server.log | cut -c1-200 | tail -20
