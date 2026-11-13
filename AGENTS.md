# RoS Private Server — Agent Charter

Agents working in this repo emulate **Rules of Survival 1.610637.617289** (dead NetEase title) for preservation / research. Stack: **BigWorld Mercury** (UDP `:25000`), `loginapp.py`, `ros_mock_server.py`, LDPlayer + physical arm64 phone.

## Roles

| Role | Responsibility |
|------|----------------|
| **Harness Agent** | Run `harness/harness_loop.ps1`, read `harness/iteration_log.jsonl`, fix connectivity + LoginApp reply + BaseApp stubs |
| **RE Agent** | Static analysis on `extract/libclient.so` (`disas_fn.py`, `message_map.txt`), no client cheating |
| **Device Agent** | `setup_emulator.ps1` / `setup_device.ps1`, `install_ros.ps1`, Frida `native` (phone) vs `emulated` (LD) |

## Hard rules

1. **Never** inject NeoX Python to skip server auth (force-lobby, fake `PlayerAvatar`, dismiss connection UI, load `.scn` without LoginApp). **OK:** read-only module discovery via `frida/neox_py_discover.js` for RE.
2. **One IP everywhere:** `$env:ROS_PC_IP` = `adb_common.ps1` = `real/server_list_ad.local.txt` = `dns_server.py` / `ros_mock_server.py`.
3. **PLAY path:** server list → **`IP:25000`** Mercury (UDP primary). Port `20001` is auxiliary.
4. **Dual test:** every iteration logs results for **LDPlayer** (`emulator-5554`) and **phone** when connected.
5. **Minimal diffs** in `loginapp.py` / `ros_mock_server.py`; capture evidence in `harness/captures/` and `harness/iteration_log.jsonl`.

## Iteration loop (each cycle)

1. `.\sync_server_list.ps1`
2. `.\verify_play_path.ps1` (servers must be running for listener checks)
3. `.\harness\harness_loop.ps1 [-TapPlay]` (screenshot + logcat + capture stats)
4. Parse: `scratch/parse_baseapp.py`, `server.log` tail, new bytes in `gate_capture.bin` / `tcp_gate_capture.bin`
5. Apply **one** hypothesis (e.g. `REPLY_VARIANT`, `SEQ_FOOTER`, `build_probe_ack`)
6. Append `harness/iteration_log.jsonl` and update `harness/last_report.md`

## Spawn a Harness Agent (Cursor Task)

```
Task: "RoS harness iteration N"
Prompt: Read AGENTS.md, run harness_loop.ps1, analyze captures, propose ≤2 code changes, append iteration_log.jsonl.
subagent_type: generalPurpose
model: composer-2.5-fast (or claude-sonnet-5-5-high for deep RE)
```

## Key files

- `loginapp.py` — Mercury login reply variants (`REPLY_VARIANT`, `BF_SPEC`, `SEQ_FOOTER`)
- `ros_mock_server.py` — HTTP/DNS targets + UDP/TCP gates
- `harness/STATE.json` — current variant matrix and last known client error
- `README.md` — architecture and blockers
