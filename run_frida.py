"""Spawn Rules of Survival with redirect_ros_17.js and stream script output to stdout.

Usage: python run_frida.py [script.js] [--attach]
"""
import sys
import time
import frida

PACKAGE = "com.netease.chiji"
script_path = next((a for a in sys.argv[1:] if a.endswith(".js")), "redirect_ros_17.js")
attach_mode = "--attach" in sys.argv


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def on_message(message, data):
    if message["type"] == "send":
        log(f"[send] {message['payload']}")
    elif message["type"] == "error":
        log(f"[script error] {message.get('stack') or message.get('description')}")
    else:
        log(str(message))


device = frida.get_usb_device(timeout=10)
log(f"Device: {device.name} ({device.id})")

if attach_mode:
    proc = next(p for p in device.enumerate_processes() if p.name in (PACKAGE, "Rules of Survival"))
    session = device.attach(proc.pid)
    pid = proc.pid
else:
    pid = device.spawn([PACKAGE])
    session = device.attach(pid)
log(f"Attached to pid {pid}")

session.on("detached", lambda reason, crash: log(f"[detached] {reason} {crash or ''}"))

with open(script_path, encoding="utf-8") as f:
    script = session.create_script(f.read())
script.on("message", on_message)
script.set_log_handler(lambda level, text: log(text))
script.load()

if not attach_mode:
    device.resume(pid)
    log("Resumed")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
