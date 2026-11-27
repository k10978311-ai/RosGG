$adb = "C:\LDPlayer\LDPlayer9\adb.exe"
$serial = "emulator-5554"
$remoteBase = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"

$dirs = @(
    "$remoteBase/res/out_game/ui_login/loginpanel",
    "$remoteBase/res/out_game/ui_login/LoginPanel",
    "$remoteBase/res/ui/out_game/ui_login/loginpanel",
    "$remoteBase/res/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/res/_international/en/ui/out_game/ui_login/loginpanel",
    "$remoteBase/res/_international/en/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/ui/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/_international/en/ui/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/_international/en/ui/out_game/ui_login/LoginPanel"
)

foreach ($d in $dirs) {
    & $adb -s $serial shell "mkdir -p $d"
    & $adb -s $serial push "scratch/patch_res/login.png" "$d/login.png"
    & $adb -s $serial push "scratch/patch_res/login.pkm" "$d/login.pkm"
    & $adb -s $serial push "scratch/patch_res/login.alpha.pkm" "$d/login.alpha.pkm"
    & $adb -s $serial push "scratch/patch_res/login.plist" "$d/login.plist"
    
    & $adb -s $serial push "scratch/patch_res/login6.png" "$d/login6.png"
    & $adb -s $serial push "scratch/patch_res/login6.pkm" "$d/login6.pkm"
    & $adb -s $serial push "scratch/patch_res/login6.alpha.pkm" "$d/login6.alpha.pkm"
    & $adb -s $serial push "scratch/patch_res/login6.plist" "$d/login6.plist"
    Write-Host "Pushed login & login6 to $d" -ForegroundColor Green
}
Write-Host "All title banner assets pushed successfully!" -ForegroundColor Cyan
