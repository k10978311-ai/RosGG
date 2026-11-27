/**
 * Generic READ-ONLY NeoX Python introspection runner for RE (AGENTS.md rule 1: discovery only).
 * Executes files/py_payload.py inside the client and lets it write files/py_out.log.
 * Payloads must only READ state (names, consts, dicts) — never call game methods or alter UI/scenes.
 *
 *   adb push payload.py /storage/emulated/0/Android/data/com.netease.chiji/files/py_payload.py
 *   python run_frida.py frida/neox_py_eval.js --attach --realm emulated
 *   adb shell cat /storage/emulated/0/Android/data/com.netease.chiji/files/py_out.log
 */
const FILES = "/storage/emulated/0/Android/data/com.netease.chiji/files/";
const libclient = Process.findModuleByName("libclient.so");
if (!libclient) {
    console.log("[-] libclient.so not found — on LDPlayer use --realm emulated");
} else {
    // Static offsets (stripped CPython 2.7 in build 1.610637.617289); see neox_py_codeinfo.js
    const gilEnsure = new NativeFunction(libclient.base.add(0x1dc9d6c), "int", []);
    const gilRelease = new NativeFunction(libclient.base.add(0x1dc9df0), "void", ["int"]);
    const pyRunFlags = new NativeFunction(libclient.base.add(0x1ddc20c), "int", ["pointer", "pointer"]);
    const code =
        "import traceback\n" +
        "try:\n" +
        "    execfile('" + FILES + "py_payload.py', {'__name__': '__ro_payload__', 'OUT': '" + FILES + "py_out.log'})\n" +
        "except Exception:\n" +
        "    open('" + FILES + "py_out.log', 'a').write(traceback.format_exc())\n";
    const st = gilEnsure();
    const rc = pyRunFlags(Memory.allocUtf8String(code), NULL);
    gilRelease(st);
    console.log("[+] payload rc=" + rc + " -> " + FILES + "py_out.log");
}
