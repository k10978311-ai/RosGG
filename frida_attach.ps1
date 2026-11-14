# Attach Frida to Rules of Survival (LDPlayer: use -Realm emulated).
param(
    [string]$Script = "diag.js",
    [ValidateSet("native", "emulated")]
    [string]$Realm = "emulated",
    [switch]$Spawn
)

$py = Join-Path $PSScriptRoot "run_frida.py"
$args = @($Script, "--realm", $Realm)
if (-not $Spawn) { $args += "--attach" }
& python $py @args
