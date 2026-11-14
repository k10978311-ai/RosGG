# Harness test loop

## Quick start

```powershell
cd C:\Users\LUFY\Desktop\RosGG
# Terminal 1 (Admin): dns_server.py
# Terminal 2 (Admin): ros_mock_server.py  (restart after loginapp edits)

.\harness\run_iteration.ps1 -TapPlay   # sets REPLY_VARIANT / BASEAPP_* env, then harness_loop
```

LoginApp session key experiments: `$env:SESSION_U32_HEX="8c1b3e2f"` or `$env:SESSION_U32_SPEC="21:4"` on `LogOnParams.rest`.

## Continuous local loop (wake Cursor agent every N minutes)

```powershell
.\harness\loop_ros.ps1 -IntervalMinutes 15
```

Emits `AGENT_LOOP_TICK_ROS` on stdout; pair with Cursor loop skill or run agents manually after each tick.

## Outputs

| File | Content |
|------|---------|
| `iteration_log.jsonl` | One JSON object per iteration |
| `last_report.md` | Human summary (sub-agent maintained) |
| `STATE.json` | `REPLY_VARIANT`, device status, blockers |
| `captures/` | Screenshots + logcat snippets per device |
