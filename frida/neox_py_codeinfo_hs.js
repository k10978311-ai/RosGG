/**
 * READ-ONLY NeoX Python code introspection for RE (AGENTS.md rule 1: discovery only).
 * Reads names/constants of loaded code objects; never calls game methods, never changes state.
 *
 * LDPlayer: python run_frida.py frida/neox_py_codeinfo.js --attach --realm emulated
 * Output:   /storage/emulated/0/Android/data/com.netease.chiji/files/py_codeinfo.log
 *
 * Env-free tuning: edit NEEDLES below.
 */
const NEEDLES = ["onHandshake", "reconnectMapID"];

const libclient = Process.findModuleByName("libclient.so");
if (!libclient) {
    console.log("[-] libclient.so not found — on LDPlayer use --realm emulated");
} else {
    // Python is statically linked and stripped in build 1.610637.617289. Offsets found statically:
    //   PyGILState_Ensure       0x1dc9d6c  (refs "Couldn't create thread-state for new thread")
    //   PyGILState_Release      0x1dc9df0  (refs "auto-releasing thread-state, but no thread-state...")
    //   PyRun_SimpleStringFlags 0x1ddc20c  (AddModule("__main__") + PyRun_StringFlags(.., 257, ..))
    const ens = libclient.findExportByName("PyGILState_Ensure") || libclient.base.add(0x1dc9d6c);
    const rel = libclient.findExportByName("PyGILState_Release") || libclient.base.add(0x1dc9df0);
    const run = libclient.findExportByName("PyRun_SimpleStringFlags") || libclient.base.add(0x1ddc20c);
    console.log("[*] Ensure=" + ens + " Release=" + rel + " RunSimpleStringFlags=" + run);
    {
        const gilEnsure = new NativeFunction(ens, "int", []);
        const gilRelease = new NativeFunction(rel, "void", ["int"]);
        const pyRunFlags = new NativeFunction(run, "int", ["pointer", "pointer"]);
        const pyRun = (p) => pyRunFlags(p, NULL);
        const py = [
            "import sys, types, traceback",
            "OUT = '/storage/emulated/0/Android/data/com.netease.chiji/files/py_codeinfo.log'",
            "NEEDLES = " + JSON.stringify(NEEDLES),
            "f = open(OUT, 'w')",
            "def w(s):",
            "    f.write(s + '\\n')",
            "def walk(co, path, depth=0):",
            "    if depth > 6: return",
            "    names = set(co.co_names) | set(c for c in co.co_consts if isinstance(c, str))",
            "    hit = [n for n in NEEDLES if n in names]",
            "    if hit:",
            "        w('HIT %s %s' % (path, hit))",
            "        w('   names=%r' % (list(co.co_names)[:80],))",
            "        w('   strs=%r' % ([c for c in co.co_consts if isinstance(c, str)][:60],))",
            "    for c in co.co_consts:",
            "        if isinstance(c, types.CodeType):",
            "            walk(c, path + '.' + c.co_name, depth + 1)",
            "def scan_obj(obj, path, seen, depth=0):",
            "    if id(obj) in seen or depth > 3: return",
            "    seen.add(id(obj))",
            "    if isinstance(obj, types.FunctionType):",
            "        walk(obj.func_code, path)",
            "    elif isinstance(obj, types.MethodType) and obj.im_func:",
            "        walk(obj.im_func.func_code, path)",
            "    elif isinstance(obj, (type, types.ClassType)):",
            "        for k, v in list(obj.__dict__.items()):",
            "            scan_obj(v, path + '.' + k, seen, depth + 1)",
            "try:",
            "    w('=== py_codeinfo (read-only) ===')",
            "    try:",
            "        import BigWorld",
            "        p = BigWorld.player()",
            "        w('player=%r class=%r module=%r' % (p, p.__class__.__name__ if p else None, p.__class__.__module__ if p else None))",
            "        if p:",
            "            w('player MRO=%r' % ([c.__name__ + '@' + c.__module__ for c in p.__class__.__mro__],))",
            "    except Exception:",
            "        w('player: ' + traceback.format_exc())",
            "    seen = set()",
            "    for mname, mod in sorted(sys.modules.items()):",
            "        if mod is None: continue",
            "        try:",
            "            for k, v in list(vars(mod).items()):",
            "                if getattr(v, '__module__', mname) == mname:",
            "                    scan_obj(v, mname + ':' + k, seen)",
            "        except Exception:",
            "            pass",
            "    w('modules=%d' % len(sys.modules))",
            "    w('login-ish modules: %r' % ([m for m in sys.modules if any(x in m.lower() for x in ('login','proxy','connect','hall','lobby'))],))",
            "except Exception:",
            "    w(traceback.format_exc())",
            "f.close()",
        ].join("\n") + "\n";
        const st = gilEnsure();
        const r = pyRun(Memory.allocUtf8String(py));
        gilRelease(st);
        console.log("[+] py_codeinfo done rc=" + r + " -> files/py_codeinfo.log");
    }
}
