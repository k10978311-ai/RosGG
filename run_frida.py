"""Spawn or attach Rules of Survival under Frida and load a JS script.

Usage:
  python run_frida.py                          # spawn + redirect_ros_17.js (native realm)
  python run_frida.py diag.js --attach
  python run_frida.py diag.js --attach --realm emulated   # LDPlayer ARM (libclient.so visible)

On x86_64 emulators with a Houdini/native-bridge ARM translation layer, the game logic
lives in the *emulated* realm. libc hooks (trace_pubkey.js) work in native; engine hooks
need --realm emulated.
"""
import argparse
import os
import sys
import time

import frida

PACKAGE = "com.netease.chiji"
PROCESS_NAMES = {PACKAGE, "Rules of Survival"}


def log(msg):
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def on_message(message, data):
    if message["type"] == "send":
        log(f"[send] {message['payload']}")
    elif message["type"] == "error":
        log(f"[script error] {message.get('stack') or message.get('description')}")
    else:
        log(str(message))


def resolve_process(device, realm):
    procs = device.enumerate_processes()
    for p in procs:
        if p.name in PROCESS_NAMES:
            return p
    names = ", ".join(sorted({p.name for p in procs[:8]}))
    raise SystemExit(
        f"Process not found ({', '.join(PROCESS_NAMES)}). "
        f"Open the game first. Sample running names: {names}..."
    )


def attach_kw(realm):
    if realm and realm != "native":
        return {"realm": realm}
    return {}


def main():
    ap = argparse.ArgumentParser(description="Frida loader for Rules of Survival")
    ap.add_argument("script", nargs="?", default="redirect_ros_17.js", help="Frida .js to inject")
    ap.add_argument("--attach", action="store_true", help="Attach to running game instead of spawn")
    ap.add_argument(
        "--realm",
        choices=("native", "emulated"),
        default=os.environ.get("FRIDA_REALM", "native"),
        help="Frida realm (use emulated on LDPlayer for libclient.so)",
    )
    args = ap.parse_args()

    script_path = args.script
    if not os.path.isfile(script_path):
        raise SystemExit(f"Script not found: {script_path}")

    device = frida.get_usb_device(timeout=15)
    log(f"Device: {device.name} ({device.id})  realm={args.realm}")

    kw = attach_kw(args.realm)
    if args.attach:
        proc = resolve_process(device, args.realm)
        session = device.attach(proc.pid, **kw)
        pid = proc.pid
        log(f"Attached to pid {pid} ({proc.name})")
    else:
        pid = device.spawn([PACKAGE])
        session = device.attach(pid, **kw)
        log(f"Spawned pid {pid}")

    session.on("detached", lambda reason, crash: log(f"[detached] {reason} {crash or ''}"))

    with open(script_path, encoding="utf-8") as f:
        script = session.create_script(f.read())
    script.on("message", on_message)
    script.set_log_handler(lambda level, text: log(text))
    script.load()
    log(f"Loaded {script_path}")

    if not args.attach:
        device.resume(pid)
        log("Resumed")

    if args.realm == "emulated" and os.path.basename(script_path) == "diag.js":
        try:
            info = script.exports_sync.check_libclient()
            log(f"[diag] libclient.so = {info}")
        except Exception as e:
            log(f"[diag] libclient check skipped: {e}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Exiting")


if __name__ == "__main__":
    main()
