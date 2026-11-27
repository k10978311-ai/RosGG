# game/ — RoS client files and patch versions

```
game/
  base/1.610637.617289/     original client: com.netease.chiji.apk + main/patch OBB (never edit)
  patches/vNNN_<date>_<name>/
      game.apk              signed, ready-to-install APK of that version
      PATCH.md              built from, what changed, MD5, where installed
      (extra files)         patch logs / scripts used for that build
  VERSIONS.md               one line per version
  CURRENT.md                which version is installed on which device
  new_patch.ps1             register a new build as the next version
  install_patch.ps1         install a version on LDPlayer / phone and record it
```

Files are **hard links** to the build outputs (decompile/, tools_dl/, scratch/), so they take no
extra disk space. Deleting one copy does not delete the other. Never edit a `game.apk` in place:
build a new APK and register it as a new version.

## New patch

1. Build + sign as usual (apktool → `uber-apk-signer`), e.g. output in `tools_dl\<work>\signed\`.
2. Register it:
   ```powershell
   .\new_patch.ps1 -Apk ..\tools_dl\vok\signed\out_unsigned-aligned-debugSigned.apk -Name my-change -From v005 -Changes "what changed"
   ```
3. Install and record:
   ```powershell
   .\install_patch.ps1 -Version v006 -Target ldplayer
   ```

The OBB files (~4 GB) never change between patches; they stay on the device in
`/sdcard/Android/obb/com.netease.chiji/`. `install -r` keeps game data; a signature change
needs an uninstall first.
