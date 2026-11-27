$adb = "C:\LDPlayer\LDPlayer9\adb.exe"
$serial = "emulator-5554"
$remoteBase = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"

Write-Host "=== PUSHING ALL UI & LOADING ASSETS TO LDPLAYER ===" -ForegroundColor Cyan

# 1. Push ui_login_en (New Title Banner & Start Game PLAY Button)
$loginEnDirs = @(
    "$remoteBase/res/_international/en/ui/out_game/ui_login",
    "$remoteBase/res/ui/out_game/ui_login",
    "$remoteBase/Documents/res/_international/en/ui/out_game/ui_login",
    "$remoteBase/Documents/res/ui/out_game/ui_login"
)
foreach ($d in $loginEnDirs) {
    & $adb -s $serial shell "mkdir -p $d"
    & $adb -s $serial push "scratch/patch_res/ui_login_en.png" "$d/ui_login_en.png"
    & $adb -s $serial push "scratch/patch_res/ui_login_en.pkm" "$d/ui_login_en.pkm"
    & $adb -s $serial push "scratch/patch_res/ui_login_en.alpha.pkm" "$d/ui_login_en.alpha.pkm"
    & $adb -s $serial push "scratch/patch_res/ui_login_en.plist" "$d/ui_login_en.plist"
    Write-Host "Pushed ui_login_en to $d" -ForegroundColor Green
}

# 2. Push login6 (New Battle Royale Background) & login7 (Blanked monkey king animations)
$loginPanelDirs = @(
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
foreach ($d in $loginPanelDirs) {
    & $adb -s $serial shell "mkdir -p $d"
    & $adb -s $serial push "scratch/patch_res/login6.png" "$d/login6.png"
    & $adb -s $serial push "scratch/patch_res/login6.pkm" "$d/login6.pkm"
    & $adb -s $serial push "scratch/patch_res/login6.alpha.pkm" "$d/login6.alpha.pkm"
    & $adb -s $serial push "scratch/patch_res/login6.plist" "$d/login6.plist"
    
    & $adb -s $serial push "scratch/patch_res/login7.png" "$d/login7.png"
    & $adb -s $serial push "scratch/patch_res/login7.pkm" "$d/login7.pkm"
    & $adb -s $serial push "scratch/patch_res/login7.alpha.pkm" "$d/login7.alpha.pkm"
    & $adb -s $serial push "scratch/patch_res/login7.plist" "$d/login7.plist"
    Write-Host "Pushed login6 and login7 to $d" -ForegroundColor Green
}

# 3. Push loading screens (bg_loading_01..08, bg_loading_dts, loading_0..13, etc.)
$loadingDirs = @(
    "$remoteBase/res/images/loading",
    "$remoteBase/res/ui/images/loading",
    "$remoteBase/Documents/res/images/loading",
    "$remoteBase/Documents/res/ui/images/loading"
)
foreach ($d in $loadingDirs) {
    & $adb -s $serial shell "mkdir -p $d"
    & $adb -s $serial push "scratch/patch_res/loading/." "$d/"
    Write-Host "Pushed loading screens to $d" -ForegroundColor Green
}

Write-Host "=== ALL ASSETS PUSHED SUCCESSFULLY ===" -ForegroundColor Cyan
