# RoS Harness — LDPlayer lobby test (2026-11-16 08:11–08:17)

**Env:** `SWITCH_TO=off SWITCH_TO_ATHLETE=on ATHLETE_ENTER_HALL=on ATHLETE_CELL=on` — see `harness/SERVER_ENV.txt`  
**Run:** `harness/restart_servers.ps1` + `ld_debug.ps1 -RestartServers -TapPlay`

## Changes this session
- **`harness/restart_servers.ps1`** — restart DNS + mock with Athlete/lobby env
- **`ld_debug.ps1`** — `-RestartServers`, `-MenuWaitSeconds` (default 50), `-WaitSeconds` (default 90)
- **`harness_loop.ps1`** — `-MenuWaitSeconds` so PLAY is not tapped during patch loading

## Iteration results
| Run | Screenshot | Outcome |
|-----|------------|---------|
| 08:11 (55s, tap @12s) | Still on RoS loading bar | TAP too early |
| 08:15 (50s menu wait) | **Slow connection** login modal | Mock **443 was down** mid-run; UniSDK never forged |

Mercury: LOGIN/PROBE counts increment; no logcat `enterHall` / `onBecomePlayer` in captured window.

## Next
1. Keep one server process: `.\harness\restart_servers.ps1` (verify 443/25000 listening).
2. `.\harness\ld_debug.ps1 -TapPlay` (no `-RestartServers` unless code changed).
3. Server console: `[FORGE games/config]`, `[FORGE user/info]`, `[BASEAPP] -> Athlete`.
4. If Slow connection persists with 443 up: grep logcat for `mpsdk` / `channelLoginFail`.