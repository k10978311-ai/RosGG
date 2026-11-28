@echo off
rem Start dns_server.py + ros_mock_server.py (lobby config) detached. Launched via WMI
rem (harness\start_servers.ps1) so they live outside the agent's tool job and survive cleanup.
cd /d %~dp0..
call config.cmd
if exist config.local.cmd call config.local.cmd
start "ros_dns" /min cmd /c ".venv\Scripts\python.exe -u dns_server.py > dns.log 2> dns_err.log"
rem Per-run overrides (written by the harness), applied last.
if exist harness\server_env_override.cmd call harness\server_env_override.cmd
start "ros_server" /min cmd /c ".venv\Scripts\python.exe -u ros_mock_server.py > server.log 2> server_err.log"
