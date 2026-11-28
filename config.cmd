@echo off
rem RoS private-server harness — edit ROS_PC_IP here (or override in config.local.cmd).
rem Powershell: .\apply_config.ps1  |  CMD servers: harness\start_servers.cmd

set ROS_PC_IP=192.168.1.21

rem Phone install (MTP: copy RosGG folder to Internal storage)
set ROS_PHONE_SERIAL=R3CM90BCXGJ
set ROS_XAPK_NAME=RULES+OF+SURVIVAL_1.610637.617289_APKPure.xapk
set ROS_PHONE_XAPK_DIR=/sdcard/RosGG

rem Patched APK (install_apk.ps1) — set ROS_LOCAL_APK to your new signed file, or pick a registered patch
set ROS_LOCAL_APK=
set ROS_PATCH_VERSION=v005
rem Custom build (build_game_apk.ps1): icon path + launcher label (exactly 17 UTF-8 chars)
set ROS_CUSTOM_ICON=
set ROS_APP_LABEL=
rem Run setup_device_permissions.ps1 with setup_device (1=on)
set ROS_DEVICE_FULL_PERMISSIONS=1
rem Note10+ with harness CA: v003 (phone-trustall) or newer; stock official sig: use install_ros.ps1 + XAPK

rem Mock server / LoginApp experiment knobs (harness may override via server_env_override.cmd)
set REPLY_VARIANT=24
set BASEAPP_REPLY_VARIANT=3
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