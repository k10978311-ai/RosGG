# RoS_Client decompile bridge (RosGG harness)

Paths on this PC (sibling repo):

| Path | Role |
|------|------|
| `RoS_Client\Client\Decompiled\Source\RoS_Decompiled` | Apktool 3.0.3 tree (**read-only**) — smali, res, `lib/*/libclient.so` |
| `RoS_Client\Client\Decompiled\APK\com.netease.chiji.apk` | **NetEase-signed baseline** (1.610637.617289) — use for LD reinstall |
| `RoS_Client\Android\apk\signed\*.apk` | Debug-signed rebuild — requires **uninstall** before install |
| `RoS_Client\Android\tools\apktool.jar` | Rebuild tool (needs JDK 17+) |

## What the APK can vs cannot fix

- **Smali/res**: UniSDK HTTP, cleartext/user CA (`network_security_config.xml` already allows user certs).
- **Mercury LoginApp / lobby**: **`libclient.so` + OBB`**, not Java — keep changing **`loginapp.py`** / `ros_mock_server.py` in RosGG.
- Do **not** patch native code here to skip server auth (charter).

## Install on LDPlayer

```powershell
cd C:\Users\LUFY\Desktop\RosGG
.\client_rebuild.ps1 -UseBaselineApk -Target ldplayer
# or after JDK install:
.\client_rebuild.ps1 -Rebuild -Install -Target ldplayer
# uninstall first if switching to debug rebuild:
# adb -s emulator-5554 uninstall com.netease.chiji
```

Then: `.\setup_emulator.ps1`, `.\sync_server_list.ps1`, `.\harness\ld_debug.ps1 -TapPlay`

## Rebuild prerequisites

```powershell
winget install EclipseAdoptium.Temurin.17.JDK
```

Editable copy is built under `RoS_Client\Android\apk\RoS_Decompiled` (copied from read-only source by `client_rebuild.ps1 -Rebuild`).
