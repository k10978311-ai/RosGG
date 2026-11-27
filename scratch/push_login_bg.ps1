. "$PSScriptRoot\..\adb_common.ps1"

$serial = "emulator-5554"
$remoteBase = "/storage/emulated/0/Android/data/com.netease.chiji/files/netease/h45na"

$dirs = @(
    "$remoteBase/res/ui/out_game/ui_login/loginpanel",
    "$remoteBase/res/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/res/out_game/ui_login/loginpanel",
    "$remoteBase/res/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/ui/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/out_game/ui_login/LoginPanel",
    "$remoteBase/res/_international/en/ui/out_game/ui_login/loginpanel",
    "$remoteBase/res/_international/en/ui/out_game/ui_login/LoginPanel",
    "$remoteBase/Documents/res/_international/en/ui/out_game/ui_login/loginpanel",
    "$remoteBase/Documents/res/_international/en/ui/out_game/ui_login/LoginPanel"
)

foreach ($d in $dirs) {
    & $script:RosAdb -s $serial shell "mkdir -p $d"
    & $script:RosAdb -s $serial push "$PSScriptRoot\patch_res\login6.png" "$d/login6.png"
    & $script:RosAdb -s $serial push "$PSScriptRoot\patch_res\login6.pkm" "$d/login6.pkm"
    & $script:RosAdb -s $serial push "$PSScriptRoot\patch_res\login6.alpha.pkm" "$d/login6.alpha.pkm"
    & $script:RosAdb -s $serial push "$PSScriptRoot\patch_res\login6.plist" "$d/login6.plist"
    Write-Host "Pushed to $d"
}

Write-Host "All files pushed successfully!"
