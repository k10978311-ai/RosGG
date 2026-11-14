# Install Rules of Survival from the XAPK on the phone (or a local copy).
# Extracts only the base APK for a fast reinstall; use -WithObb for first-time / missing-OBB installs (~4GB).
#
#   .\install_ros.ps1 -Target phone              # APK only (already has OBB)
#   .\install_ros.ps1 -Target phone -WithObb     # APK + both OBB blobs from XAPK
#   .\install_ros.ps1 -Target ldplayer -WithObb
param(
    [ValidateSet("phone", "ldplayer", "both")]
    [string]$Target = "phone",
    [switch]$WithObb,
    [string]$XapkName = "RULES+OF+SURVIVAL_1.610637.617289_APKPure.xapk",
    [string]$PhoneXapkDir = "/sdcard/RosGG"
)

. "$PSScriptRoot\adb_common.ps1"

$obbRemote = "/sdcard/Android/obb/com.netease.chiji"
$stage = "/data/local/tmp/ros_install"
$apkName = "com.netease.chiji.apk"

function Install-One {
    param([string]$Serial)
    Write-Host "`n=== $Serial ==="
    $abi = (& $RosAdb -s $Serial shell getprop ro.product.cpu.abi).Trim()
    Write-Host "ABI: $abi"

    $xapkOnPhone = "$PhoneXapkDir/$XapkName"
    $hasXapk = (& $RosAdb -s $Serial shell "test -f '$xapkOnPhone' && echo yes").Trim() -eq "yes"
    if (-not $hasXapk) {
        Write-Warning "XAPK not on device at $xapkOnPhone — copy RosGG folder to Internal storage first."
        return
    }

    & $RosAdb -s $Serial shell "mkdir -p $stage" | Out-Null

    Write-Host "[*] Extracting base APK from XAPK..."
    & $RosAdb -s $Serial shell "unzip -oj '$xapkOnPhone' $apkName -d $stage" 2>&1 | Out-Null

    Write-Host "[*] Installing APK..."
    $out = & $RosAdb -s $Serial shell "pm install -r $stage/$apkName" 2>&1
    Write-Host $out
    if ($out -match "INSTALL_FAILED_CONFLICTING_PROVIDER" -and $out -match "roslegacy") {
        Write-Warning "Uninstall net.roslegacy.prod (conflicts with official package), then rerun."
        Write-Host "    adb -s $Serial uninstall net.roslegacy.prod"
    } elseif ($out -match "Success") {
        Write-Host "[+] APK installed"
    } elseif (& $RosAdb -s $Serial shell "pm path $RosPackage" 2>&1 | Select-String "package:") {
        Write-Host "[+] $RosPackage already installed (APK refresh optional)"
    }

    if ($WithObb) {
        Write-Host "[*] Extracting OBB (~4GB, several minutes)..."
        & $RosAdb -s $Serial shell "mkdir -p $obbRemote" | Out-Null
        $work = "/data/local/tmp/ros_obb"
        & $RosAdb -s $Serial shell "rm -rf $work; mkdir -p $work/Android/obb/com.netease.chiji" | Out-Null
        & $RosAdb -s $Serial shell "cd $work && unzip -o '$xapkOnPhone' 'Android/obb/com.netease.chiji/*'" 2>&1
        & $RosAdb -s $Serial shell "cp -f $work/Android/obb/com.netease.chiji/*.obb $obbRemote/ && chmod 644 $obbRemote/*.obb && ls -la $obbRemote"
    } else {
        $obbList = (& $RosAdb -s $Serial shell "ls $obbRemote 2>/dev/null").Trim()
        if (-not $obbList) {
            Write-Warning "No OBB in $obbRemote — rerun with -WithObb for a full asset install."
        } else {
            Write-Host "[+] OBB present: $obbList"
        }
    }

    Push-RosLoginPubKey -Serial $Serial
}

$serials = @()
switch ($Target) {
    "phone" { $serials += @(Resolve-RosSerial -Target phone) }
    "ldplayer" { $serials += @(Resolve-RosSerial -Target ldplayer) }
    "both" {
        $serials += @(Resolve-RosSerial -Target phone)
        $serials += @(Resolve-RosSerial -Target ldplayer)
    }
}
$serials = $serials | Where-Object { $_ } | Select-Object -Unique
if (-not $serials) { throw "No adb device found. Enable USB debugging or start LDPlayer." }

foreach ($s in $serials) { Install-One -Serial $s }
Write-Host "`nDone. Start mock servers on PC ($RosPcIp) then run setup_device.ps1 or setup_emulator.ps1."
