# Rules of Survival 2.0 — Offline Boot Harness (LDPlayer)

Documents a local setup that boots **Rules of Survival 2.0** (`com.netease.chiji`,
client `1.610637.617289`) on LDPlayer past the dead-server screens, up to the point
where it tries to join a match.

NetEase shut the game down on **27 June 2022**. The login/update servers partly
still answer but refuse service; the actual **game server is gone**. This harness
replaces the server-side pieces that can be replaced and documents the one that
can't.

## Status

| Stage | Result |
|-------|--------|
| `Retrieving patch lists 0.00%` | ✅ solved — serves the real patch manifest with the version floor lowered |
| Main menu (logo / PLAY / notices) | ✅ loads |
| UniSDK init (`/api/games/config`, `/api/devices/init`) | ✅ passthrough to NetEase (still alive) |
| Guest login + auto-login | ✅ **forged** locally (NetEase refuses with "service stopped" / "user does not exist") |
| EULA, logged in as **Guest**, `af_login` fired | ✅ |
| **Login RSA wall** | ✅ **broken** — key-swapped; client's `LogOnParams` now decryptable with our key (see "Groundwork") |
| **LoginApp login reply** | ✅ **solved** — client reaches `ServerConnection::logOn: status==LOGGED_ON` |
| **BaseApp handshake (entities → hall)** | ⏳ client connects to BaseApp, exchanges `authenticate`/`createBasePlayer`, handshake loops |

## ★ Breakthrough: client reaches `status==LOGGED_ON`

The full LoginApp Mercury login is now emulated end to end. Working reply (loginapp.py `build_reply`
variant 24, flags `0x40`):

```
[flags=0x40 00] [0xFF] [len:u32] [reply_id:u32] [status=0x01] [BF(LoginReplyRecord)] [seq=1 :u32]
```

Solved pieces, in order:
1. **Reply framing** — off-channel packet, `0xFF` reply message, DWORD length (Cimmeria RE).
2. **Reply-id** = the client's request id at **packet offset 5–8** (`data[5:9]`), echoed back → the
   client's `Nub::handleMessage` matches its pending login handler and calls `LoginHandler::onLoginReply`.
3. **LogOnStatus byte** `0x01` (LOGGED_ON), read in clear before the encrypted record.
4. **LoginReplyRecord** `{ip:4, port:2, salt:2, sessionKey:4}` **Blowfish-encrypted** with the client's
   session key. The key is the **4 bytes at LogOnParams-tail offset 1** (the `04` prefix is the length;
   bytes 1–4 are the only per-session-random bytes — confirmed by diffing three sessions).
5. **Cipher** — not plain ECB. NeoX uses a **plaintext-feedback Blowfish** mode
   (`loginapp.custom_bf_{encrypt,decrypt}`): block0 = `BF(P0)`, blockN = `BF(PN ^ P(N-1))`. This yielded
   `onLoginReply: convertAddress ... 192.168.1.18` and `checkScriptBaseAppAddr addr=192.168.1.18:25000`.

Result on the wire:
```
ServerConnection::logOn: status==LOGGED_ON
ServerConnection::logOn: to:   192.168.1.18:25000
```

> **Provenance note:** the BaseApp-channel handler in `ros_mock_server.py` and the custom-Blowfish
> helpers in `loginapp.py` were written across a usage-limit reset (they appeared on disk between turns).
> They are a direct continuation of this work and are what carried the client to LOGGED_ON.

### Remaining: BaseApp entity handshake → 3D hall
After login the client connects to the BaseApp (`:25000`, our gate), sends `authenticate` on the
channel, and the server replies with `resetEntities` + `createBasePlayer`. The client currently **loops**
(re-sending `authenticate`), so the channel ACK / entity-creation sequence isn't fully accepted yet. This
is the BaseApp/CellApp entity protocol (the real "server emulator" part): correct on-channel ACK of the
client's reliable seq, then a valid `createBasePlayer`/`createCellPlayer` + the player entity's `.def`
properties so the hall scene loads.

### The wall

Pressing **PLAY** makes the client connect to the game server:

```
ServerConnection::logOnBegin connecting to 192.168.1.18:25000 for loginAPP
RetryingRequest(login): Final attempt of 10 failed (REASON_TIMER_EXPIRED)
ServerConnection::logOnComplete: Logon failed (Mercury::REASON_TIMER_EXPIRED)
```

Captured traffic (`mercury_login_handshake.bin`) shows **BigWorld "Mercury"
protocol over UDP** on port 25000:

```
01 00 00 84 | seq(2B, increments) | ..2b | len | <128-byte RSA-encrypted LogOnParams> | 02 00
```

The 128-byte block is `LogOnParams` RSA-encrypted with the key in
`entities/loginapp.pubkey`. Because that key ships *inside the client*, it can be
swapped for one you control — so this is not a dead cryptographic end, but the start
of a BigWorld server-emulator project. See "Reverse-engineering findings" below.

## Reverse-engineering findings (what the engine actually is)

Pulled `libclient.so` (72 MB NeoX engine) and read its symbols/strings. The game is
built on **BigWorld Technology** — the strings are explicit:

- `neox::bwclient::Mercury::{Nub,Bundle,Packet,Channel,EncryptionFilter,CompressionEncryptionFilter}`
- `BigWorld.AvatarFilter()`, `BigWorld.setSendBaseAppLoginHookCallback`, `BaseAppExtInterface`, `baseAppLogin`, `authenticate`
- Login key loaded from the res path **`entities\loginapp.pubkey`**
- `LogOnParams::addToStream publicEncrypt failed` / `readFromStream privateDecrypt failed`

So the architecture is classic BigWorld: **LoginApp → BaseApp → CellApp**, entity-based
(your character is an `Avatar` entity), Mercury transport over UDP.

### This changes the wall from "impossible" to "a defined project"

The RSA block isn't an unbreakable barrier after all. The client encrypts `LogOnParams`
with the public key in **`entities/loginapp.pubkey`**, which ships *inside the client*
(`assets.npk`). The standard BigWorld private-server move is:

1. **Unpack `assets.npk`** — it's NetEase's `NXPK` format (magic `NXPK`, zlib-compressed
   entries, hashed filenames). Tools: `zhouhang95/neox_tools` or similar NXPK extractors.
2. **Replace `entities/loginapp.pubkey`** with *your own* RSA public key, repack (or drop a
   loose-file override if this build reads res before the npk), so the client encrypts the
   login with a key **you** hold the private half of.
3. **Stand up a Mercury LoginApp** that decrypts `LogOnParams` with your private key and
   returns a login-success reply pointing at your BaseApp + a session key. This alone gets
   the client **past** `REASON_TIMER_EXPIRED`.
4. **Implement BaseApp + CellApp + the hall** — the big part. The 3D lobby ("hall") is an
   entity scene: the server must send the Avatar entity, inventory, currency, and run the
   entity method protocol defined by RoS's `.def` files (extracted from `entities.npk` /
   `script.npk`). `KBEngine` is an open-source BigWorld-compatible server that could be the
   base, but the RoS-specific entity definitions and exact protocol version must be matched.

### Honest scope

Steps 1–3 are achievable but non-trivial (NXPK round-trip, a correct Mercury LoginApp for
this protocol version). Step 4 is a **server-emulator project** — reimplementing RoS's
server-authoritative hall (character, inventory, matchmaking are all server data that no
longer exist anywhere). No public RoS emulator exists, so this is original work on the
scale of a community server project, not a config change. That is why this harness stops
at the login handshake: everything client-reachable is done, and the hall is behind a
server that must be rebuilt from scratch.

## Groundwork done — the RSA wall is broken ✅

The server-emulator groundwork is started and the crypto barrier is **solved**:

1. **Res-override discovered.** Tracing `open()` (`trace_pubkey.js`) shows the client looks
   for `entities/loginapp.pubkey` on the **loose filesystem first**, in this order:
   ```
   .../h45na/Documents/cloth_dlc/res/entities/loginapp.pubkey
   .../h45na/Documents/res/entities/loginapp.pubkey
   .../h45na/res/entities/loginapp.pubkey        <-- we use this one
   ```
   Only if all are missing does it fall back to the OBB copy. So a loose file overrides
   NetEase's embedded key. The same override applies to the entity `.def` files and
   `entities.xml` (useful later for the hall).

2. **Key swapped.** Generated an RSA-1024 keypair (`server_keys/loginapp_priv.pem` +
   `loginapp.pubkey`) and pushed the public half to
   `.../h45na/res/entities/loginapp.pubkey`. The client now encrypts its login with **our**
   key (no `publicEncrypt failed`).

3. **Proven by decryption.** Captured a fresh login packet and decrypted the 128-byte RSA
   block with our private key (**RSA-OAEP** padding) → valid BigWorld `LogOnParams`
   (`extract/logonparams_decrypted.bin`):
   ```
   flags = 0x01
   username = "9000000001@ad.netease_global.win.163.com"   (our forged guest uid)
   password = "aec05336cadcad87"
   + session (Blowfish) key material the client wants to use for the channel
   ```
   We can now **read the client's login in full and hold its session key.**

### LoginApp reply — in progress (client now parses our replies)

`loginapp.py` + the UDP gate in `ros_mock_server.py` decrypt the login and send a
candidate Mercury reply back to `:25000`. Progress by the client's own error ladder
(set `REPLY_VARIANT` env var to switch framings):

- **No reply** → `Mercury::REASON_TIMER_EXPIRED` (packet never answered).
- **Reply v0** (mirror header + status + Blowfish record) →
  `Nub::processOrderedPacket: Discarding bundle due to corrupted header for message id 137`.
  The outer **packet framing is accepted** — the client parses it as a bundle and reads
  messages; it only desyncs on the inner message header (hits byte `0x89` in our blob).
- **Reply v3** (`0xFF` reply-id + int32 length + record) →
  `Bundle::iterator::unpack( shortEntityMessage ): Not enough data on stream at 18 for
  payload (13 left, needed ...)`. The client now **recognizes message types** and checks
  payload length — we're one framing detail away.

Request framing is decoded:
`01 00 00 84 | 00 | seq(uint16 LE, increments) | 01 00 00 00 | 2b | 00 00 00 | <128B RSA> | 02 00`
(byte 11 `0x2b` is the login message id; `01 00 00 00` is the candidate reply-id).

**Msgid sweep (loginapp.py `build_reply`, `REPLY_VARIANT=sweep`):** swept the reply
message-id 0x00–0xB3 with an 11-byte header (`01 00 00 84 00 [seq] 01 00 00 00`) and a
`[msgid][len:2][body]` message. The client's `Bundle::iterator::unpack(<name>)` errors
revealed real BigWorld **ClientInterface** message names — `createBasePlayer`,
`shortEntityMessage` — confirming the id space, but no msgid produced a reply reaction
(`handler for reply id` / `onLoginReply`). Past ~msgid 0x14 every packet resolved to the
same `createBasePlayer`, i.e. the client stopped reading our swept byte as the id — so the
msgid is read from a different offset than assumed, and the packet/bundle layout model is
not yet correct.

**Conclusion of the fuzzing pass:** black-box convergence stalled because the exact
bundle framing (where the msgid sits, the reply-message identifier, length/reply-id
encoding, packet footers) can't be pinned from error strings alone. Finishing the reply
needs the **BigWorld 2.x Mercury source** (`packet.hpp`, `bundle.cpp`,
`interface_element.cpp`, `REPLY_MESSAGE_IDENTIFIER`, `Bundle::startReply`) or a
Ghidra/IDA pass on `libclient.so`'s `Bundle::iterator::unpack` and the LoginApp reply
handler — then the reply carries BaseApp `IP:port` + session key (Blowfish-encrypted with
the `LogOnParams` key) and the client proceeds to BaseApp login.

**Reusable from this pass:** `loginapp.py` (reply builder + variants + msgid sweep),
`extract/syms.py` (ELF symbol dumper), `extract/analyze_pkts.py` (packet field diff),
and the confirmed msgid→name observations above.

## Static RE pass (Ghidra/IDA-style, done with capstone)

No Ghidra/IDA, so this used a custom capstone + ELF toolchain on `extract/libclient.so`.
Results:

### Engine + why dynamic hooking is hard
`libclient.so` is **BigWorld Technology** (symbols `neox::bwclient::Mercury::*`,
`BigWorld.AvatarFilter`). **The app is arm64 running on an x86_64 emulator via a native
bridge** (`libnb.so` / Houdini). Frida enumerates only the x86_64 modules — `libclient.so`
is translated and **not directly hookable** (`findModuleByName("libclient.so") == NULL`).
→ For dynamic instrumentation of the engine, use an **arm64** Android device/emulator; on
this x86_64 setup, static analysis is the practical route. `libc` hooks (fopen/strstr)
still work because libc is native.

### Message framing (decoded from the registration code)
Messages register via a call at `libclient.so+0x98f654` taking `(iface, name, lengthStyle,
lengthParam)`; ids are assigned sequentially per interface. `extract/regseq.py` dumps the
whole table → `extract/message_map.txt` (124 entries across 3 interfaces):
- **LoginInterface**: `login`(VARIABLE,2), `probe`
- **BaseAppExtInterface**: `baseAppLogin`(VARIABLE,2), `authenticate`(FIXED,4),
  `avatarUpdate*`, `enableEntities`(FIXED,8), `disconnectClient`(FIXED,1), …
- **ClientInterface**: `bandwidthNotification`, `setGameTime`(FIXED,4),
  `resetEntities`(FIXED,1), `createBasePlayer`(VARIABLE,2), `createCellPlayer`,
  `createEntity`, `shortEntityMessage`(VARIABLE,1), `longEntityMessage`(VARIABLE,2), …

Length styles: **FIXED** = `[id][payload(param bytes)]`; **VARIABLE** =
`[id][len:param bytes LE][payload]`. On the wire the login request used msg id `0x2b`.

### Still unresolved (the two concrete blockers)
1. **Packet header size / msgid offset.** The sweep showed the client reading the wire id
   from a fixed position that our swept byte didn't occupy, so the 11-byte-header model is
   not exactly right. The `login` request's 2-byte length field also doesn't line up with a
   128-byte RSA payload at the assumed offset — so the login packet uses special
   once-off/LoginApp framing, not plain bundle framing. Resolve by disassembling the packet
   receive/parse path (around `Nub::processOrderedPacket` / `Bundle::iterator::unpack`) in
   `libclient.so`.
2. **Login reply + reply-id.** How the LoginApp reply is framed and matched
   (`LoginHandler::onLoginReply`, `Couldn't find handler for reply id`). Best read straight
   from the BigWorld 2.x source (`Bundle::startReply`, `LoginInterface`) now that the
   message map and length styles are known.

New tools from this pass: `extract/elf.py`, `extract/msgmap.py`, `extract/xref2.py`,
`extract/disas_fn.py`, `extract/regseq.py`, and `extract/message_map.txt` (the full map).
- **BaseApp + CellApp + hall entity** — the large part: implement the `Avatar`/hall entity
  protocol from the `.def` files (now loose-readable under `res/entities/defs/`), send the
  player entity + inventory so the 3D hall renders.

### Groundwork artifacts

- `trace_pubkey.js` — Frida tracer for the key-load path.
- `server_keys/` — our RSA keypair (`loginapp_priv.pem` is the one the LoginApp decrypts with).
- `extract/decrypt_login.py` — decrypts a captured login block; `extract/logonparams_decrypted.bin`
  is the proven plaintext.
- Loose key installed on device at `res/entities/loginapp.pubkey`.

### Artifacts for whoever continues

- `extract/libclient.so` — the BigWorld/NeoX engine (analyze in IDA/Ghidra for the exact
  Mercury login message IDs and the LoginApp reply format).
- `extract/assets.npk` — the NXPK archive containing `entities/loginapp.pubkey`.
- `mercury_login_handshake.bin` — the client's real login UDP packets to `:25000`.
- `script_log.txt` — NeoX Python traceback showing `GameEntry.py → app.py → Globals.py →
  NATProxy.py` call flow.

## Current state (resume here)

- **Working now:** game patches, loads the menu, auto-logs-in as Guest, reaches PLAY.
  Fails only at the game-server handshake (expected — no server emulator yet).
- **To run:** `dns_server.py` + `ros_mock_server.py` on the PC (admin), then
  `setup_emulator.ps1` once per emulator boot, then launch the game. See "How to run".
- **Login reply experiments are OFF by default** (`REPLY_VARIANT=off`); set it to `sweep`
  or a number to re-enable the `loginapp.py` reply attempts.
- **Biggest unknowns to continue:** packet-header/msgid offset and the login-reply framing
  (see "Static RE pass" → "Still unresolved"). Best next step: BigWorld 2.x Mercury source,
  or an arm64 environment so `libclient.so` can be hooked with Frida.

### File index
| File | Purpose |
|------|---------|
| `ros_mock_server.py` | HTTP/HTTPS + TCP/UDP gate; serves patch/version/server-list, forges login, proxies live SDK hosts |
| `dns_server.py` | DNS redirect (NetEase hosts → PC, else 8.8.8.8) |
| `setup_emulator.ps1` | Private-DNS off, install local CA (tmpfs), iptables DNS redirect (`-Undo` reverts) |
| `loginapp.py` | Experimental Mercury login-reply builder (decrypts LogOnParams, reply variants, msgid sweep) |
| `cycle.sh` | Relaunch game + dump NeoX `<SCRIPT>` logs + screenshot |
| `trace_pubkey.js` | Frida: trace the `loginapp.pubkey` load path (libc hooks) |
| `run_frida.py` | Spawn/attach the game under Frida |
| `redirect_ros_17.js`, `dump_urls.js` | Original Frida redirector / URL sniffer (not needed for the DNS flow) |
| `dump_msgmap.js`, `diag.js` | Frida msgid-map dumper + module diag (blocked by native bridge here) |
| `certs/` | Local test CA + leaf cert (SANs for NetEase hosts) |
| `real/` | Real patch files from NetEase CDN (+ the `.patched.plist` version fix) + server list |
| `server_keys/` | Our RSA-1024 keypair; `loginapp_priv.pem` decrypts the client login |
| `extract/` | Static-RE toolchain (`elf.py`, `regseq.py`, `xref2.py`, …), `libclient.so`, `assets.npk`, `message_map.txt`, decrypted login proof |
| `mercury_login_handshake.bin` | Captured client login UDP packets |

## Architecture

```
          LDPlayer (emulator-5554, root, Android 9, arm64 via libnb bridge)
          com.netease.chiji
                │  DNS (udp/53) ── iptables DNAT ──►  PC dns_server.py
                │                                       (NetEase hosts → PC IP, else → 8.8.8.8)
                │  HTTPS/HTTP (443/80) ─────────────►  PC ros_mock_server.py
                │     trusts certs/834a6af3.0 (local CA, tmpfs-overlaid into system store)
                │  game server (udp/25000) ─────────►  PC ros_mock_server.py (UDP gate) ✗ can't answer
                ▼
          PC = 192.168.1.18 (LAN; NOT the Tailscale 100.x address)
```

Redirection is done with **DNS + a trusted CA**, not the Frida script. `redirect_ros_17.js`
(Frida) still exists as an alternative/diagnostic path but is not needed for the
DNS-based flow.

## Files

### Servers (run on the PC)
- **`ros_mock_server.py`** — main server. Listens HTTP:80, HTTPS:443 (local CA cert),
  TCP+UDP gate on 20001 and 25000. Serves the real patch/version/server-list files
  from `real/`, passes `who/whoami/mpsdk` through to NetEase, and **forges** the
  `/api/users/login/*` responses. Logs every request.
- **`dns_server.py`** — answers NetEase domains with the PC IP, forwards everything
  else to 8.8.8.8. Needed because the game uses raw DNS (once Private DNS is off).

### Emulator setup
- **`setup_emulator.ps1`** — turns off Private DNS, installs `certs/*.0` into the
  system trust store via a tmpfs overlay (system partition is read-only), and adds
  the `iptables` DNS redirect. `-Undo` reverts. **Lost on emulator reboot — re-run after reboot.**
- **`cycle.sh`** — force-stop + relaunch the game, wait, dump NeoX `<SCRIPT>` logs to
  `script_log.txt` and a screenshot to `shot.png`. Used for each test iteration.

### Certs (`certs/`)
- `ca.crt` / `ca.key` — local test CA. `834a6af3.0` is the same CA hashed for the
  Android store. `server.crt` / `server.key` — leaf cert; SANs cover
  `*.easebar.com`, `*.update/nie/proxima/gph/nstool/mpsdk.easebar.com`,
  `*.netease.com`, `*.163.com`, `*.rulesofsurvivalgame.com`, `IP:192.168.1.18`.
  `server_chain.crt` — leaf+CA, loaded by the HTTPS server.

### Captured game data (`real/`)
- `npk_version_na_android.plist` — real patch manifest from NetEase CDN
  (`52.221.3.167`). **`.patched.plist`** = same file with
  `min_patch_client_version` dropped `619421` → `617289` (this is what breaks the
  "version too low, force Patch" loop).
- `h45na_hc` — anti-hijack headcode blob. `server_list_ad.txt` — real region list;
  **`.local.txt`** = IPs rewritten to `192.168.1.18:25000`. `notice_pc_hw.txt` —
  shutdown notice. `games_config.json` — SDK config.

### Frida (optional, not used by the DNS flow)
- `redirect_ros_17.js` — connect()/getaddrinfo redirector + URL sniffer.
- `dump_urls.js` — URL sniffer only. `run_frida.py` — spawns the game under Frida
  and streams script output.

### Capture
- `mercury_login_handshake.bin` — the 10 UDP login packets the client sends to
  `:25000` (the RSA key-exchange described above).
- `gate_capture.bin` — scratch capture from the running server.

## How to run (fresh boot)

Assumes LDPlayer running with the game installed, `frida-server` not required for
this flow, PC IP `192.168.1.18`. ADB is at `C:\LDPlayer\LDPlayer9\adb.exe` (not on PATH).

1. Start the servers (two terminals, from `C:\Users\Lufy\Desktop\Server`):
   ```bash
   .\.venv\Scripts\python.exe -u dns_server.py
   ```
   ```bash
   .\.venv\Scripts\python.exe -u ros_mock_server.py
   ```
   The HTTPS server needs to bind :443 and :80 — run that terminal **as Administrator**,
   and allow `python.exe` through the Windows firewall on **Private** networks
   (first run prompts; UDP 25000/20001/53 must be allowed too).

2. Configure the emulator (once per emulator boot):
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup_emulator.ps1
   ```

3. Launch the game. It will patch, load the menu, auto-login as Guest, and — on
   PLAY — fail at the game-server handshake (expected).

To revert the emulator: `setup_emulator.ps1 -Undo`.

## If the PC IP changes

It is hard-coded in: `ros_mock_server.py` (`LOCAL_SERVER_IP`), `dns_server.py`
(`LOCAL_IP`), `setup_emulator.ps1` (`$PC_IP`), `real/server_list_ad.local.txt`, and
the cert SAN (`certs/leaf.ext` → regenerate `server.crt`). Use the **LAN** address,
never the Tailscale `100.x` one.

## Notes / gotchas

- System cert store is read-only (system-as-root); the CA is injected via a tmpfs
  mount over `/system/etc/security/cacerts`, so it **does not survive an emulator reboot**.
- Private DNS (DoT) must be **off** or all lookups bypass the local DNS server.
- The patch files are HTTPS with an anti-hijack check — plain HTTP mocking is not
  enough; the trusted CA is required.
- `who`/`whoami`/`mpsdk` are proxied live because the client validates server
  signatures on those; they can't be mocked, only forwarded.
