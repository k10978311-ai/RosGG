# Rules of Survival (NeoX / BigWorld) Backend Emulation Handoff Notes

## 1. Executive Summary & Architecture Overview
This project emulates the backend services for *Rules of Survival* (NetEase NeoX / BigWorld 2.0 engine, Android package `com.netease.chiji`, running in LDPlayer 9 on `emulator-5554` at `192.168.1.18`).
The goal is to bypass the title screen PLAY button network checks and transition into the 3D lobby/hangar scene.

All mock services are unified into `ros_mock_server.py`:
* **HTTP (:80) / HTTPS (:443)**: Spoofs patch checks, server list (`Fast North-America` -> `192.168.1.18:25000`), UniSDK authentication (`mpsdk.easebar.com`).
* **UDP (:25000)**: Serves both `LoginApp` and `BaseApp` Mercury channels.
* **TCP (:20001)**: Legacy gate port listener.

---

## 2. Fully Solved & Reverse-Engineered Milestones

### A. Patch / UniSDK Bypass (100% Complete)
* Bypassed "Retrieving patch lists" by returning empty filelists with matching versions.
* Spoofed UniSDK guest login (`/users/login/` on `mpsdk.easebar.com`) returning forged user `uid: 9000000001`, `token: localguesttoken0001`, `login_channel: guest`.
* The client displays `Guest` account and `Fast North-America` server in green.

### B. LoginApp Handshake (100% Complete)
* **Client Request**: 145-byte UDP packet `01 00 00 84 ...` with RSA-1024 encrypted `LogOnParams`.
* **Server Logic** (`loginapp.py`):
  * Private key `server_priv.pem` decrypts `LogOnParams`.
  * Extracts 4-byte session key `CURRENT_BF_KEY` (e.g. `0b6afd8e`).
  * Assembles `LoginReplyRecord` (`flags=0x0040`, `msg_id=0xFF`, `seq=1`) redirecting the client to BaseApp at `192.168.1.18:25000`.

### C. BaseApp Handshake & Encryption Filter (100% Complete)
* **Client Request**: Unencrypted `baseAppLogin` (`flags=0x0001`, `msg_id=0`, `req_id=data[5:9]`).
* **Encryption Mode**: Blowfish ECB with custom plaintext-feedback mode:
  $$C_0 = E_K(P_0), \quad C_i = E_K(P_i \oplus P_{i-1})$$
  $$P_0 = D_K(C_0), \quad P_i = D_K(C_i) \oplus P_{i-1}$$
  * Padding: Wastage byte at the end of block (`pad_len = 8 - (len % 8)`). Receiver subtracts `wastage` from length.
  * Implemented in `loginapp.custom_bf_encrypt()` and `loginapp.custom_bf_decrypt()`.
* **BaseApp Reply**: 19 bytes cleartext (`flags=0x0040`, `0xFF`, `req_id + session_key 0x11223344`, `seq=1`) padded to 24 bytes and Blowfish-encrypted.
* **Result**: Client transitions to `ServerConnection::logOn: status==LOGGED_ON`.

### D. Mercury Wire Format & Endianness (100% Complete)
* NetEase compiled BigWorld for ARM64 with **Little-Endian (`<I`)** for wire sequence numbers and footers.
* `FLAG_HAS_CUMULATIVE_ACK (0x0400)` is **forbidden** by this client (`cmp w9, #0x400; b.lo`).
* Channel flags: `0x005c` = `ON_CHANNEL (0x08) | RELIABLE (0x10) | HAS_ACKS (0x04) | HAS_SEQUENCE (0x40)`.
* Footers (LIFO order): `[server_seq: 4B LE] [ack_seq: 4B LE] [nAcks: 1B = 0x01]`.

---

## 3. Discovered Interface Definitions in `libclient.so`

### `BaseAppExtInterface` (Client -> BaseApp):
* `0`: `baseAppLogin`
* `1`: `authenticate` (Fixed 4B: `sessionKey`)
* `2`: `avatarUpdateImplicit`
* `3`: `avatarUpdateExplicit`
* `4`: `avatarUpdateWardImplicit`
* `5`: `avatarUpdateWardExplicit`
* `6`: `switchInterface`
* `7`: `requestEntityUpdate`
* `8`: `enableEntities`
* `9`: `setSpaceViewportAck`
* `10`: `setVehicleAck`
* `11`: `restoreClientAck`
* `12`: `identifyVersionPoint` (Variable: interface digest verification)
* `13`: `summariseVersionPoint`
* `14`: `commenceResourceDownload`
* `15`: `disconnectClient`
* `16`: `resourceVersionTag`
* `17`: `entityMessage`

### `ClientInterface` (BaseApp -> Client):
* `0`: `bandwidthNotification` (4B)
* `1`: `updateFrequencyNotification` (1B)
* `2`: `setGameTime` (4B)
* `3`: `resetEntities` (1B: `keepPlayerOnBase`)
* `4`: `createBasePlayer` (Variable 2B len: `uint32 entityID`, `uint16 entityType`, properties stream)
* `5`: `createCellPlayer` (Variable 2B len)
* `6`: `spaceData`
* `7`: `spaceViewportInfo`
* `8`: `updateEntity`

---

## 4. Current State & Immediate Next Steps for the Next Agent

### A. Current Client Packet Cycle:
Once `LOGGED_ON`, the client repeatedly sends an on-channel bundle (`flags=0x0008`):
```hex
08 00 01 44 33 22 11 0c 0d 00 14 00 0a 54 68 69 73 20 64 6f 63 75 6d
```
* `08 00`: `FLAG_ON_CHANNEL` (unsequenced)
* `01`: `BaseAppExtInterface::authenticate` with session key `0x11223344`
* `0c`: `BaseAppExtInterface::identifyVersionPoint` (13 bytes containing interface digest prefix `"This docum..."`)

### B. Next Steps to Reach 3D Lobby:
1. **Handle `identifyVersionPoint`**:
   * Inspect the interface synchronization response expected by `libclient.so`.
2. **Send Player Entity Creation Bundle**:
   * Format `ClientInterface::resetEntities` (`0x03 0x00`) followed by `ClientInterface::createBasePlayer` (`0x04 ...`).
   * Provide the minimal entity properties (Avatar position, model, name) so `ClientApp::onBasePlayerCreate` initializes the local avatar.
3. **Frida / Script Injection Alternative**:
   * The Python VM inside `libclient.so` can be invoked directly:
     ```python
     import game_mgr
     game_mgr.enter_hall() # or login_mgr.on_login_success()
     ```
   * Hook `0x032c4000` base in PID `26076` via `run_frida.py`.
