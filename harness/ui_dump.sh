#!/usr/bin/env bash
# Dump the phone's current UI (text/desc/bounds/clickable). Usage: bash harness/ui_dump.sh [serial]
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
P="/c/LDPlayer/LDPlayer9/adb.exe -s ${1:-${ADB_SERIAL:-R3CM90BCXGJ}}"
$P shell uiautomator dump /sdcard/ui.xml >/dev/null; $P shell cat /sdcard/ui.xml > scratch_ui.xml
.venv/Scripts/python.exe -c "
import re
x=open('scratch_ui.xml',encoding='utf-8').read()
for m in re.finditer(r'<node [^>]*>', x):
    n=m.group(0); g=lambda k: re.search(k+r'=\"([^\"]*)\"',n).group(1)
    t,d,b,r=g('text'),g('content-desc'),g('bounds'),g('resource-id').split('/')[-1]
    if t or d or 'EditText' in n: print(repr(t)[:42], repr(d)[:30], r[:28], b, 'C' if 'clickable=\"true\"' in n else '')
"
