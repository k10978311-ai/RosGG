# Sign + install the host-patched APK.
#   .\decompile\tools\sign_apk.ps1                       # sign only
#   .\decompile\tools\sign_apk.ps1 -Install -Target ldplayer
# Needs a JDK (winget install EclipseAdoptium.Temurin.17.JDK) and
# decompile\tools\uber-apk-signer.jar (github.com/patrickfav/uber-apk-signer releases, v1.3.0).
# The NetEase signature is lost: uninstall the store build first (adb uninstall com.netease.chiji).
# OBB files stay valid: they live in /sdcard/Android/obb/com.netease.chiji and are not signature-bound.
param(
    [string]$Unsigned = "$PSScriptRoot\..\patched\ros_patched_unsigned.apk",
    [switch]$Install,
    [ValidateSet("ldplayer", "phone", "both")] [string]$Target = "ldplayer"
)
$ErrorActionPreference = "Stop"

function Find-Java {
    foreach ($c in @("$PSScriptRoot\jdk\bin\java.exe",
                     "$env:JAVA_HOME\bin\java.exe",
                     "C:\Program Files\Eclipse Adoptium\*\bin\java.exe",
                     "C:\Program Files\Java\*\bin\java.exe",
                     "C:\Program Files\Android\Android Studio\jbr\bin\java.exe")) {
        $hit = Get-Item $c -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($hit) { return $hit.FullName }
    }
    $cmd = Get-Command java -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}

$java = Find-Java
if (-not $java) { throw "No JDK. Run: winget install EclipseAdoptium.Temurin.17.JDK" }
$signer = Join-Path $PSScriptRoot "uber-apk-signer.jar"
if (-not (Test-Path $signer)) { throw "Missing $signer (download uber-apk-signer-1.3.0.jar and rename)." }

$outDir = Join-Path $PSScriptRoot "..\patched\signed"
New-Item -ItemType Directory -Force $outDir | Out-Null
& $java -jar $signer --apks $Unsigned --out $outDir --allowResign
$signed = Get-ChildItem $outDir -Filter *.apk | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Write-Host "[+] signed: $($signed.FullName)"

if ($Install) {
    . "$PSScriptRoot\..\..\adb_common.ps1"
    $serials = switch ($Target) {
        "phone"    { @(Resolve-RosSerial -Target phone) }
        "ldplayer" { @(Resolve-RosSerial -Target ldplayer) }
        "both"     { @(Resolve-RosSerial -Target phone), @(Resolve-RosSerial -Target ldplayer) }
    }
    foreach ($s in ($serials | Where-Object { $_ } | Select-Object -Unique)) {
        Write-Host "[*] $s : uninstall store build (keeps OBB), install patched"
        & $script:RosAdb -s $s uninstall -k com.netease.chiji 2>$null
        & $script:RosAdb -s $s install -r $signed.FullName
    }
}
