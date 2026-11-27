#!/usr/bin/env bash
# Relaunch RoS, attach the read-only entity-message tracer, tap PLAY, wait, then run a probe payload.
# Usage: bash harness/traced_cycle.sh [wait_s=45] [probe_payload]
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
A="/c/LDPlayer/LDPlayer9/adb.exe -s ${ADB_SERIAL:-emulator-5554}"
WAIT=${1:-45}
before=$(grep -c 'notice_pc_hw.txt' server.log)
$A shell am force-stop com.netease.chiji; $A logcat -G 16M 2>/dev/null; $A logcat -c
$A shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
i=0; until [ "$(grep -c 'notice_pc_hw.txt' server.log)" -gt "$before" ] || [ $i -ge 80 ]; do sleep 3; i=$((i+1)); done
echo "[menu after $((i*3))s]"
.venv/Scripts/python.exe -u run_frida.py ${TRACER:-frida/trace_entity_msgs.js} --attach --realm emulated > scratch/trace_em.log 2>&1 &
FPID=$!
sleep 25
$A shell input tap 1538 89; sleep 2; $A shell input tap 790 660
sleep "$WAIT"
kill $FPID 2>/dev/null; sleep 2
$A logcat -d -v time 2>/dev/null | grep -a " M (" | sed -E 's/^([0-9-]+ [0-9:.]+).*\] M \( *[0-9]+\): /\1 /' | cut -c1-330 > mercury_log.txt
$A logcat -d -v time 2>/dev/null | grep -a "<SCRIPT>" | cut -c1-400 > script_log.txt
$A exec-out screencap -p > scratch_shot1.png
[ -n "$2" ] && bash harness/probe.sh "$2" scratch/probe_out.txt >/dev/null 2>&1
echo done
