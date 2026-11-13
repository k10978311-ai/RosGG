# RoS Harness — Iteration 3 (LD debug)

**When:** 2026-11-13 23:44  
**Branch:** `harness/baseapp-bf-key` (PR #1)  
**Command:** `harness\ld_debug.ps1 -TapPlay` (`REPLY_VARIANT=24`, `BF_SPEC=1:4`)

## Results

| Check | Outcome |
|-------|---------|
| LDPlayer ping PC | OK |
| Phone (Note10+) ping PC | FAIL (different LAN — unchanged) |
| Mercury LOGIN on wire | Yes — seq `5c67`, bf=`20b0ed72` (4-byte key) |
| BaseApp probes | Yes — `0100000b` probes; capture totals **LOGIN 45 / PROBE 115** (+64 B delta this tap) |
| Logcat | UniSDK **:8080 ConnectException** (aux); EntityDef init noise; **no** clear LoginHandler success string |
| Mock server | Restarted with branch code + `BF_SPEC=1:4` |

**Latest variant-24 reply (40B):**  
`4000ff1d0000005c670100019a48af099cf8587d9a48af099cf8587d68ee1e8b47a8663301000000`

## Harness tweak

- `ld_debug.ps1` now defaults `BF_SPEC=1:4` (was `1:16`).

## Frida discovery (blocked this run)

`run_frida.py` attached to **phone** (`R3CM90BCXGJ`) — Frida server not running there. For LD-only discovery: unplug phone **or** add device selection; then:

```powershell
$env:ANDROID_SERIAL='emulator-5554'  # if supported
python run_frida.py frida/neox_py_discover.js --attach --realm emulated
E:\LDPlayer\LDPlayer9\adb.exe -s emulator-5554 shell cat /sdcard/neox_py_discover.log
```

## Next hypothesis

1. Align `SESSION_U32` with probe `field` bytes once client accepts login record (try `SESSION_U32_SPEC` / `SESSION_U32_HEX` from latest probe `d361245d` region).
2. Watch **new** mock-server window for `[BASEAPP LOGIN REPLY]` + `createBasePlayer` after this restart (older `server.log` is stale).
3. Optional stub **:8080** in mock server if UniSDK blocks UI thread before Mercury retry.

```powershell
$env:ROS_PC_IP = "192.168.100.137"
$env:REPLY_VARIANT = "24"
$env:BF_SPEC = "1:4"
.\harness\ld_debug.ps1 -TapPlay
```
