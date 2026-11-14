/**
 * Read-only NeoX embedded Python module discovery (no scene load, no UI bypass).
 *
 * LDPlayer (ARM via Houdini): python run_frida.py frida/neox_py_discover.js --attach --realm emulated
 * Real phone (arm64):         python run_frida.py frida/neox_py_discover.js --attach --realm native
 */
const libclient = Process.findModuleByName("libclient.so");
if (!libclient) {
    console.log("[-] libclient.so not found — on LDPlayer use --realm emulated");
} else {
    console.log("[+] libclient.so @ " + libclient.base);

    const PyGILState_Ensure = libclient.findExportByName("PyGILState_Ensure");
    const PyGILState_Release = libclient.findExportByName("PyGILState_Release");
    const PyRun_SimpleString = libclient.findExportByName("PyRun_SimpleString");

    if (!(PyRun_SimpleString && PyGILState_Ensure && PyGILState_Release)) {
        const pyExports = libclient.enumerateExports().filter((e) => e.name.startsWith("Py"));
        console.log("[-] Named Py* exports missing. Sample:", JSON.stringify(pyExports.slice(0, 12)));
    } else {
        const gilEnsure = new NativeFunction(PyGILState_Ensure, "int", []);
        const gilRelease = new NativeFunction(PyGILState_Release, "void", ["int"]);
        const pyRun = new NativeFunction(PyRun_SimpleString, "int", ["pointer"]);

        function execPy(code) {
            const state = gilEnsure();
            const codePtr = Memory.allocUtf8String(code);
            const res = pyRun(codePtr);
            gilRelease(state);
            return res;
        }

        globalThis.execPy = execPy;

        const payload =
            "import sys, traceback\n" +
            "p = '/sdcard/neox_py_discover.log'\n" +
            "f = open(p, 'w')\n" +
            "try:\n" +
            "    f.write('=== NeoX module discovery (read-only) ===\\n')\n" +
            "    keys = sorted(sys.modules.keys())\n" +
            "    hit = [k for k in keys if any(w in k.lower() for w in " +
            "('world','scene','lobby','login','avatar','hall','ui','stage','client','logic'))]\n" +
            "    f.write('modules: ' + ', '.join(hit) + '\\n')\n" +
            "    for name in ['world','game3d','logic','client']:\n" +
            "        if name in sys.modules:\n" +
            "            f.write(name + ' -> ' + str(dir(sys.modules[name])[:40]) + '\\n')\n" +
            "except Exception:\n" +
            "    f.write(traceback.format_exc())\n" +
            "f.close()\n";

        execPy(payload);
        console.log("[+] Wrote /sdcard/neox_py_discover.log — adb pull or: adb shell cat ...");
    }
}
