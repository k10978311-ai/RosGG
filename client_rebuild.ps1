# Rebuild / install Rules of Survival from RoS_Client decompiled tree (LDPlayer or phone).
# Read-only source: C:\Users\LUFY\Desktop\RoS_Client\Client\Decompiled\Source\RoS_Decompiled
# Prebuilt (no Java):    C:\Users\LUFY\Desktop\RoS_Client\Android\apk\signed\ros_custom_test-aligned-debugSigned.apk
#
#   .\client_rebuild.ps1 -InstallOnly              # signed debug rebuild
#   .\client_rebuild.ps1 -Rebuild -Install         # needs JDK + apktool.jar
#   .\client_rebuild.ps1 -Install -Target ldplayer -ThenHarness

param(
    [switch]$Rebuild,
    [switch]$Install,
    [switch]$InstallOnly,
    [switch]$ThenHarness,
    [switch]$UseBaselineApk,
    [ValidateSet("ldplayer", "phone", "both")]
    [string]$Target = "ldplayer",
    [string]$RosClientRoot = "C:\Users\LUFY\Desktop\RoS_Client"
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot\adb_common.ps1"

$readOnly = Join-Path $RosClientRoot "Client\Decompiled\Source\RoS_Decompiled"
$workspace = Join-Path $RosClientRoot "Android\apk\RoS_Decompiled"
$apktool = Join-Path $RosClientRoot "Android\tools\apktool.jar"
$signer = Join-Path $RosClientRoot "Android\tools\uber-apk-signer-1.3.0.jar"
$unsignedOut = Join-Path $RosClientRoot "Android\apk\ros_custom_test.apk"
$signedOut = Join-Path $RosClientRoot "Android\apk\signed\ros_custom_test-aligned-debugSigned.apk"
$baselineApk = Join-Path $RosClientRoot "Client\Decompiled\APK\com.netease.chiji.apk"

function Find-Java {
    $candidates = @(
        "$env:JAVA_HOME\bin\java.exe",
        "C:\Program Files\Android\Android Studio\jbr\bin\java.exe",
        "C:\Program Files\Eclipse Adoptium\*\bin\java.exe",
        "C:\Program Files\Java\*\bin\java.exe"
    )
    foreach ($c in $candidates) {
        $hits = Get-Item $c -ErrorAction SilentlyContinue
        if ($hits) { return $hits[0].FullName }
    }
    return $null
}

if ($Rebuild) {
    if (-not (Test-Path $readOnly)) { throw "Missing decompiled tree: $readOnly" }
    if (-not (Test-Path $apktool)) { throw "Missing apktool: $apktool" }
    $java = Find-Java
    if (-not $java) {
        throw "JDK not found. Install Temurin 17 or use -InstallOnly with prebuilt signed APK."
    }
    if (Test-Path $workspace) {
        Write-Host "[*] Removing old workspace..."
        Remove-Item $workspace -Recurse -Force
    }
    Write-Host "[*] Copying decompiled tree to editable workspace (slow, ~2min)..."
    robocopy $readOnly $workspace /MIR /NFL /NDL /NJH /NJS /nc /ns /np | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy failed: $LASTEXITCODE" }

    $patch = Join-Path $RosClientRoot "Android\apk\patch_android.py"
    if (Test-Path $patch) {
        Write-Host "[*] Running patch_android.py (optional NetEase origin -> LAN)..."
        python $patch
    }

    Write-Host "[*] apktool build..."
    & $java -jar $apktool b $workspace -o $unsignedOut
    if (-not (Test-Path $unsignedOut)) { throw "apktool did not produce $unsignedOut" }

    if (Test-Path $signer) {
        Write-Host "[*] Signing..."
        & $java -jar $signer --apks $unsignedOut --out (Split-Path $signedOut)
    }
}

$doInstall = $Install -or $InstallOnly -or $Rebuild
if (-not $doInstall) {
    Write-Host "Nothing to do. Use -InstallOnly, -Rebuild -Install, or -ThenHarness."
    exit 0
}

if ($UseBaselineApk -and (Test-Path $baselineApk)) {
    $apk = $baselineApk
} elseif (Test-Path $signedOut) {
    $apk = $signedOut
} elseif (Test-Path $unsignedOut) {
    $apk = $unsignedOut
} else {
    throw "No APK found (signed, unsigned, or baseline)."
}

$serials = switch ($Target) {
    "phone" { @(Resolve-RosSerial -Target phone) }
    "ldplayer" { @(Resolve-RosSerial -Target ldplayer) }
    "both" { @(Resolve-RosSerial -Target phone), @(Resolve-RosSerial -Target ldplayer) }
}
$serials = $serials | Where-Object { $_ } | Select-Object -Unique
if (-not $serials) { throw "No adb device." }

foreach ($s in $serials) {
    Write-Host "`n=== install $apk -> $s ==="
    $remote = "/data/local/tmp/ros_rebuild.apk"
    & $RosAdb -s $s push $apk $remote | Write-Host
    $out = & $RosAdb -s $s shell pm install -r $remote 2>&1
    Write-Host $out
    if ($out -match "INSTALL_FAILED_UPDATE_INCOMPATIBLE" -and (Test-Path $baselineApk) -and $apk -ne $baselineApk) {
        Write-Warning "Signature mismatch — retrying with baseline APK from Decompiled/APK/"
        & $RosAdb -s $s push $baselineApk $remote | Out-Null
        $out = & $RosAdb -s $s shell pm install -r $remote 2>&1
        Write-Host $out
    } elseif ($out -notmatch "Success") {
        Write-Warning "Debug rebuild needs: adb -s $s uninstall com.netease.chiji then -UseBaselineApk or reinstall signed APK"
    }
    Push-RosLoginPubKey -Serial $s
}

if ($ThenHarness) {
    & "$PSScriptRoot\setup_emulator.ps1"
    & "$PSScriptRoot\sync_server_list.ps1"
    & "$PSScriptRoot\harness\ld_debug.ps1" -TapPlay
}

Write-Host "`nDecompiled layout:"
Write-Host "  Smali/Java shell: $readOnly\smali*"
Write-Host "  Native:           $readOnly\lib\armeabi-v7a\libclient.so (LD uses ARM via Houdini)"
Write-Host "  Mercury login:    native libclient — server fixes stay in RosGG loginapp.py"
Write-Host "  Apktool metadata: $readOnly\apktool.yml (1.610637.617289)"
