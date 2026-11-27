# decompile/ — XAPK unpack + API host replacement

Source: `Desktop\RULES+OF+SURVIVAL_1.610637.617289_APKPure.xapk` (4.25 GB).

| Path | What | In git? |
|------|------|---------|
| `xapk/` | `com.netease.chiji.apk` (93 MB), `main.1227927…obb` (2.1 GB), `patch.1227927…obb` (2.0 GB), `manifest.json` | no |
| `apk_unzip/` | raw unzip of the APK (5 dex, `lib/{arm64-v8a,armeabi-v7a}`, assets) | no |
| `patched/` | `ros_patched_unsigned.apk` + `.patchlog.txt` (every replaced offset) | no |
| `tools/scan_urls.py` | finds every URL / host / IPv4 in the tree → `report/urls_raw.json` | yes |
| `tools/patch_hosts.py` | same-length host replacement in dex / .so / assets / arsc, then repack | yes |
| `tools/sign_apk.ps1` | sign (uber-apk-signer) + `adb install` | yes |
| `hosts_map.example.json` | the replacement map | yes |
| `report/hosts_netease.txt` | 82 NetEase hosts and the files that hold them | yes |

## Where the API hosts live

| Layer | Hosts | Patchable here? |
|-------|-------|-----------------|
| Java UniSDK (`classes*.dex`) | `unisdk.update`, `mcount`, `sdk-os.mpsdk`, `who/whoami.nie`, `httpdns.nie`, `*.proxima.nie`, `dns.update`, `dl.nstool`, `www.rulesofsurvivalgame.com` … | ✅ |
| Native (`libclient.so`, `libunisdkdctool.so`, `libstreammgr.so`, `libijkplayer.so`, `libAudioEngine.so`) | `clientdump.x`, `acsdk.gameyw`, `api.vop`, `proxy-state.nie`, `data-detect.nie`, `km`, CC live/voice | ✅ |
| `assets/`, `res/raw/pushconfig.properties`, `resources.arsc` | `notice.easebar.com`, `push.x.netease.com` | ✅ |
| **Game scripts:** `script.npk` (patch OBB) | **`h45na.update.easebar.com`** → `/server_list_ad.txt`, `/pl/h45na_hc`, `/pl/npk_version_na_android.plist`, `/notice_pc_hw.txt`, plus `gph` CDN, sigma/keypoint, voice, pharos, NAT | ✅ loose `.nxs` override (see below) |

## script.npk: decoded

From the importer, read in-game with `frida/payloads/script_importer.py` (`redirect.NpkImporter.load_module`):

```
entry bytes --rotor.decrypt(KEY)--> zlib --decompress--> _reverse_string --> NeoX marshal (Py 2.7 code object)
_reverse_string: XOR first 128 bytes with 0x9A, then reverse the whole buffer
NeoX marshal: every s/t/u string payload (and co_code) is XORed with (len-1-i)
```

- NXPK header: 4386 entries, 28-byte index records, all stored uncompressed. The two CRC
  fields are a NeoX-specific checksum (not CRC32/Adler of any stage), so we **don't rebuild the npk**.
- `KEY` is this build's 313-char rotor key, saved in `tools/neox_rotor_key.txt`. It differs from the
  key published for other NeoX games.
- The encoder reproduces original entries byte-for-byte (zlib level 9).
- Bytecode opcodes may be remapped; that's not needed for string work.

| Tool | Does |
|------|------|
| `tools/rotor.py` | pure-Python port of CPython 2 `rotormodule.c` |
| `tools/npk_decrypt.py script/script.npk script/out` | all entries → `out/<hash>.code` (27 s; 4384/4386, the 2 failures are non-script blobs) |
| `tools/neox_marshal.py script/out script/strings` | parses all 4383 modules → per-module string dump + `_files.json` (hash → `co_filename`) |
| `tools/patch_scripts.py hosts_map.example.json script/script.npk script/patched` | same-length host swap inside marshal strings → `patched/nxs/<module>.nxs` + `changes.txt` |

URL-bearing modules: `ui/UILogin` (server list), `patch/Headcode`, `patch/ResourcePatcher`,
`patch/config`, `patch_first/FirstResourcePatcher`, `patch/patch_utils`, `extconfigs`,
`elkLogging`, `PyDetect/Utility`, `nat/*`, `helpers/pharos_lib/config`, `ui/chat/voiceUtils`.
The last run patched 68 modules and 254 strings.

### Loose override (no npk/OBB rebuild)

`C_file.find_file('ui/UILogin.nxs', ...)` resolves names relative to the script root and also checks two
loose dirs (found with marker files): `.../files/netease/h45na/script/` and
`.../h45na/Documents/script/`. The patcher writes into `Documents`, so use the first:

```bash
adb -s emulator-5554 push decompile/script/patched/nxs/. /storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/script/
# undo: adb shell rm -r /storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na/script
```

`anticheat_record/hosts_guard` only inspects the Windows hosts file, so it is irrelevant on Android.

## Replacement rule: same length, TLD swap

Dex string data and native C strings have fixed sizes, so replacement must be byte-for-byte
the same length. In dex, `string_ids` must also stay sorted (the ART verifier rejects the
APK otherwise). A different name such as `rosserv.lan` breaks the sort order in 3 of 5 dex files.
**Swapping only the TLD keeps the order**:

```
easebar.com             -> easebar.lan
netease.com             -> netease.lan
www.rulesofsurvivalgame.com -> www.rulesofsurvivalgame.lan
```

`.lan` resolves only through your own `dns_server.py` (suffixes added), and the leaf cert in
`certs/` now carries `*.easebar.lan` / `*.netease.lan` SANs (old cert in `certs/*.bak`).
The patcher checks length and dex order and refuses or skips the change if either breaks.

## Run

```powershell
python -I decompile\tools\scan_urls.py decompile\apk_unzip decompile\report\urls_raw.json
python -I decompile\tools\patch_hosts.py decompile\hosts_map.example.json decompile\xapk\com.netease.chiji.apk decompile\patched\ros_patched_unsigned.apk
.\decompile\tools\sign_apk.ps1 -Install -Target ldplayer     # needs JDK + uber-apk-signer.jar
```

### LDPlayer without restarting dns_server.py

`report/hosts.emulator` maps every `.lan` host in `report/lan_hosts.txt` to the PC IP.
Bind-mount it (root, no system-disk write, gone after emulator reboot). In Git Bash set
`MSYS_NO_PATHCONV=1` or device paths get rewritten:

```bash
adb -s emulator-5554 push decompile/report/hosts.emulator /data/local/tmp/hosts.ros
adb -s emulator-5554 shell "su -c 'chmod 644 /data/local/tmp/hosts.ros; chcon u:object_r:system_file:s0 /data/local/tmp/hosts.ros; mount -o bind /data/local/tmp/hosts.ros /system/etc/hosts'"
# undo: adb -s emulator-5554 shell "su -c 'umount /system/etc/hosts'"
```

### Smoke test 2026-11-15 #2 (patched APK + patched scripts)

- No import or marshal errors. Every script `http_get` now goes to `h45na.update.easebar.lan`
  (server_list_ad, h45na_hc, npk_version_na_android.plist, notice_pc_hw), served by
  `ros_mock_server.py`; the login screen and notice board load (`report/smoke_scripts.png`).
- Only `sdk-os.mpsdk.easebar.com` is still `.com` (UniSDK mpay config, a passthrough host).
- The cert was reissued again with 35 `.lan` wildcards (adds gph, voice, gmsdk, fp.ps ...). Restart
  `ros_mock_server.py` to load it.

### Smoke test 2026-11-15 #1 (LDPlayer, debug-signed patched APK)

- Boots and runs, with no signature or verifier errors.
- These `.lan` hosts reached `ros_mock_server.py`: drpf-h45na.proxima.nie, unisdk.proxima.nie,
  unisdk.update, data-detect.nie, dl.nstool, who.nie, mcount, dns.update, appdump.nie,
  www.rulesofsurvivalgame.
- Still `.com` (built at runtime, outside the APK strings): `h45na.update.easebar.com`
  (game scripts), `sdk-os.mpsdk`, `whoami.nie`, `sigma-keypoint-h45na.proxima.nie`,
  part of `unisdk.update`.
- The first cert was missing `*.matrix.netease.lan`. It was reissued with wildcards built from every
  host in `lan_hosts.txt`. Restart `ros_mock_server.py` to load it.

Last run: 173 replacements (dex 105, .so 50, arsc/assets/raw 18). Zip test OK, all stored
entries aligned (.so on 4096 bytes).
