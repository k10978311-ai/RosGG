#!/usr/bin/env bash
# Relaunch RoS, attach the read-only property-order trace, PLAY, then compare the client's
# per-property parse (name + bytes consumed) with extract/bwdefs.py's Avatar streams.
# Usage: bash harness/traced_play.sh [entity=Avatar]
cd "$(dirname "$0")/.."
export MSYS_NO_PATHCONV=1
A="/c/LDPlayer/LDPlayer9/adb.exe -s ${ADB_SERIAL:-emulator-5554}"
ENT=${1:-Avatar}
before=$(grep -c 'notice_pc_hw.txt' server.log)
$A shell am force-stop com.netease.chiji
$A logcat -c
$A shell monkey -p com.netease.chiji -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1
i=0; until [ "$(grep -c 'notice_pc_hw.txt' server.log)" -gt "$before" ] || [ $i -ge 80 ]; do sleep 3; i=$((i+1)); done
echo "[menu after $((i*3))s]"
.venv/Scripts/python.exe -u run_frida.py frida/trace_prop_order.js --attach --realm emulated > frida_prop_order.log 2>&1 &
FPID=$!
i=0; until grep -q "prop-order hook ready" frida_prop_order.log || [ $i -ge 40 ]; do sleep 1; i=$((i+1)); done
sleep 20
$A shell input tap 1538 89; sleep 2; $A shell input tap 790 660
sleep 45
kill $FPID 2>/dev/null
grep -oE "PROP [0-9]+ \S+ -?[0-9]+" frida_prop_order.log | awk '{print $3, $4}' > scratch_client_props.txt
echo "client props parsed: $(wc -l < scratch_client_props.txt)"
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe - "$ENT" <<'EOF'
import sys; sys.path.insert(0, 'extract')
import bwdefs
ent = sys.argv[1]
D = bwdefs.Defs()
cl = [l.split() for l in open('scratch_client_props.txt')]
base = [p[0] for p in D.base_client_props(ent)]
start = 7  # Account's 7 props come first
print('base order matches:', [c[0] for c in cl[start:start + len(base)]] == base)
cell = cl[start + len(base):]
mine = D.cell_own_client_props(ent)
OV = {'mapID': 4}
for k in range(len(cell) - 1):
    p = mine[k] if k < len(mine) else None
    csz = int(cell[k][1]) - int(cell[k + 1][1])
    msz = OV.get(p[0], len(bwdefs.encode_default(D.resolve(p[1]), D.defaults.get(p[0])))) if p else None
    if not p or p[0] != cell[k][0] or csz != msz:
        print('first mismatch k=%d client=%s(%d) mine=%s(%s) type=%s' % (k, cell[k][0], csz, p and p[0], msz, p and ' '.join(p[1].split())[:80]))
        break
else:
    print('cell: all %d parsed props match (mine has %d)' % (len(cell), len(mine)))
EOF
