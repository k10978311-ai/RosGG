# RoS Harness — Iteration 2

**When:** 2026-11-13 23:06  
**Command:** `harness_loop.ps1 -TapPlay` (`REPLY_VARIANT=24`, default `SESSION_U32` → `0x11223344`)

## Coherence check (LoginApp ↔ BaseApp)

| Piece | Behavior |
|-------|----------|
| `loginapp.build_reply` | `LoginReplyRecord.session_key` from `extract_session_u32(params)` (default **11223344**; override `SESSION_U32_HEX` or `SESSION_U32_SPEC=off:4` on `LogOnParams.rest`) |
| `loginapp.build_baseapp_reply` | `rdata` = probe bytes **[11:15]**; reply payload **req_id@[7:11] + sess_key** (variant 1); flags `0x0040` + seq footer `1` |
| `ros_mock_server` BaseApp handler | Parses `req_id@5:9`, `sess@11:15`, attempt; sends `build_baseapp_reply` when `BASEAPP_ACK≠on` |

**Wire-level:** BaseApp handler mirrors `build_baseapp_reply` (same offsets, same 8-byte inner payload). **Semantic gap:** latest probe `sess=968f892b` still ≠ login record `session_key=11223344` — client likely not applying `onLoginReply` yet; probes use client-local nonce.

## Harness results

| Device | Ping PC | Logcat lines | Mercury / ServerConnection / logOn |
|--------|---------|--------------|-------------------------------------|
| LDPlayer | OK | 602 | **No hits** (widened patterns); UniSDK **8080 ConnectException** only |
| Note10+ | **FAIL** | 112 | Same — phone off LAN |

**Captures:** LOGIN **57** (+1), PROBE **50** (+5); `gate_capture_delta=0` (server process not restarted this tap — counts from existing `gate_capture.bin` tail).

## Code (iteration 2)

- `extract_session_u32()` in `loginapp.py` (`SESSION_U32_SPEC`, `SESSION_U32_HEX`, default `0x11223344`)
- Wider logcat patterns in `harness_loop.ps1` (Mercury, ServerConnection, logOn, LoginHandler, …)
- Removed unreachable tail in `build_baseapp_reply`

## Next

```powershell
$env:ROS_PC_IP = "192.168.100.137"
$env:REPLY_VARIANT = "24"
$env:BASEAPP_REPLY_VARIANT = "1"
# A/B once login accepted: $env:SESSION_U32_HEX = "968f892b"
# Restart mock server so UDP handler picks up loginapp changes:
python -u ros_mock_server.py
.\harness\harness_loop.ps1 -TapPlay
```

**Follow-up (parent):** BaseApp replies now use `_seq_footer(probe)`; server logs `session_u32=` per login; harness saves `*_mercury.log`; A/B via `.\harness\ab_login_reply.ps1 -TapPlay`.
