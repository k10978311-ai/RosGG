@echo off
rem Start dns_server.py + ros_mock_server.py (lobby config) detached. Launched via WMI
rem (harness\start_servers.ps1) so they live outside the agent's tool job and survive cleanup.
cd /d %~dp0..
set ROS_PC_IP=192.168.1.18
start "ros_dns" /min cmd /c ".venv\Scripts\python.exe -u dns_server.py > dns.log 2> dns_err.log"
set REPLY_VARIANT=24
set CBP_TYPE=41
set CBP_PROPS=account
set SEND_CELL_PLAYER=off
set SWITCH_TO=avatar
set SWITCH_TO_ATHLETE=off
set AVATAR_ENTITY=BattleGroundAvatar
set AUTO_TRANSITION_HALL=on
if "%TRANSITION_DELAY%"=="" set TRANSITION_DELAY=12
set ATHLETE_CELL=on
if "%TEST_ACCOUNT_NAME%"=="" set TEST_ACCOUNT_NAME=TestPlayer
if "%HALL_DELAY%"=="" set HALL_DELAY=3
rem Per-run overrides (written by the harness), applied last.
if exist harness\server_env_override.cmd call harness\server_env_override.cmd
start "ros_server" /min cmd /c ".venv\Scripts\python.exe -u ros_mock_server.py > server.log 2> server_err.log"
