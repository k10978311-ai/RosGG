#!/usr/bin/env bash
# Restart frida-server on LDPlayer (it wedges with TransportError timeouts after heavy payloads).
export MSYS_NO_PATHCONV=1
A="/c/LDPlayer/LDPlayer9/adb.exe -s ${ADB_SERIAL:-emulator-5554}"
$A shell "for p in \$(pidof frida-server); do kill -9 \$p; done" 2>/dev/null
$A shell "/data/local/tmp/frida-server -D >/dev/null 2>&1 &"
i=0; until $A shell pidof frida-server >/dev/null || [ $i -ge 10 ]; do sleep 1; i=$((i+1)); done
sleep 2
