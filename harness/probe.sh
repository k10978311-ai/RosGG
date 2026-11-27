#!/usr/bin/env bash
# Run a read-only Python payload in the game via Frida (emulated realm) and print its output.
# Usage: bash probe.sh frida/payloads/<payload>.py [outfile]
cd /c/Users/Lufy/Desktop/Server
export MSYS_NO_PATHCONV=1
A="/c/LDPlayer/LDPlayer9/adb.exe -s ${ADB_SERIAL:-emulator-5554}"
F=/storage/emulated/0/Android/data/com.netease.chiji/files
OUTF=${2:-py_out_probe.log}
$A shell "rm -f $F/py_out.log"
$A push "$1" $F/py_payload.py >/dev/null
timeout 60 .venv/Scripts/python.exe -u run_frida.py frida/neox_py_eval.js --attach --realm emulated 2>&1 | grep -E "payload|rror|Process not found"
$A shell "cat $F/py_out.log" > "$OUTF"
cut -c1-900 "$OUTF"
