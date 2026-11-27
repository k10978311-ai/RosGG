# Launch harness\start_servers.cmd outside the calling process tree (WMI Win32_Process.Create).
$root = Split-Path $PSScriptRoot -Parent
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'ros_mock_server|dns_server' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep 1
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = "cmd.exe /c `"$root\harness\start_servers.cmd`""; CurrentDirectory = $root }
"Win32_Process.Create rc=$($r.ReturnValue) pid=$($r.ProcessId)"
Start-Sleep 5
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'ros_mock_server|dns_server' } | ForEach-Object { "$($_.ProcessId) $($_.CommandLine)" }
