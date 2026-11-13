# Where login / lobby logic actually lives for RoS 1.610637.617289.
# The Apktool tree has NO unpacked game .py — NeoX scripts are embedded in libclient.so + OBB.
param(
    [string]$DecompiledRoot = "C:\Users\LUFY\Desktop\RoS_Client\Client\Decompiled\Source\RoS_Decompiled",
    [string]$LibClient = "C:\Users\LUFY\Desktop\RosGG\extract\libclient.so"
)

Write-Host "=== .py under Decompiled (expect 0 game scripts) ===" -ForegroundColor Cyan
$py = Get-ChildItem $DecompiledRoot -Recurse -Filter "*.py" -ErrorAction SilentlyContinue
Write-Host "count: $($py.Count)"

Write-Host "`n=== Apktool layout ===" -ForegroundColor Cyan
@("smali", "smali_classes2", "lib\armeabi-v7a\libclient.so", "assets", "res") | ForEach-Object {
    $p = Join-Path $DecompiledRoot $_
    Write-Host ("  {0,-40} {1}" -f $_, ($(if (Test-Path $p) { "ok" } else { "missing" })))
}

if (-not (Test-Path $LibClient)) {
    $LibClient = Join-Path $DecompiledRoot "lib\arm64-v8a\libclient.so"
}

Write-Host "`n=== libclient.so string hits (C++ Mercury / LoginHandler) ===" -ForegroundColor Cyan
if (Test-Path $LibClient) {
    python -c @"
import pathlib, re, sys
p = pathlib.Path(r'$LibClient')
d = p.read_bytes()
needles = [
    'LoginHandler', 'onLoginReply', 'LogOnParams', 'createBasePlayer',
    'baseAppLogin', 'ServerConnection', 'Failed to connect',
    'PlayerAvatar', 'world.scene', 'Mercury', 'identifyVersionPoint',
]
for n in needles:
    b = n.encode()
    i = d.find(b)
    print(f'{n:24} file_offset={hex(i) if i >= 0 else \"NOT_FOUND\"}')
"@ 
} else {
    Write-Warning "libclient.so not found"
}

Write-Host "`n=== RosGG server-side RE (packet matching) ===" -ForegroundColor Cyan
Write-Host "  extract\message_map.txt, extract\msgmap.py, loginapp.py, HANDOFF_NOTES.md"
Write-Host "  python scratch\parse_baseapp.py"
Write-Host "  python extract\syms.py onLoginReply LogOnParams createBasePlayer"
