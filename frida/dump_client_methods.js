/**
 * READ-ONLY RE hook: when the client resolves a server->client entity method
 * (libclient+0x9d46f8, MethodDescriptions::exposedFromMsgID-like), dump the exposed method
 * table of that entity type: exposed[i] -> methods[exposed[i]].name. Observes only.
 *
 * LDPlayer: python run_frida.py frida/dump_client_methods.js --attach --realm emulated
 */
const lib = Process.findModuleByName("libclient.so");
const seen = new Set();

function readStdString(p) {
    // libc++ std::string (24 bytes): short if (byte0 & 1) == 0 -> len = byte0 >> 1, data at +1
    try {
        const b0 = p.readU8();
        if ((b0 & 1) === 0) {
            const n = b0 >> 1;
            return n > 0 && n < 23 ? p.add(1).readUtf8String(n) : null;
        }
        const n = p.add(8).readU64().toNumber();
        if (n <= 0 || n > 200) return null;
        return p.add(16).readPointer().readUtf8String(n);
    } catch (e) { return null; }
}

function methodName(m) {
    for (const off of [8, 0, 16, 24, 32]) {
        const s = readStdString(m.add(off));
        if (s && /^[A-Za-z_][A-Za-z0-9_]{2,}$/.test(s)) return s + "@" + off;
    }
    return "?";
}

if (!lib) {
    console.log("[-] libclient.so not found (use --realm emulated)");
} else {
    Interceptor.attach(lib.base.add(0x9d46f8), {
        onEnter(args) {
            const c = args[0];
            const key = c.toString();
            const msgid = args[1].toInt32() & 0xff;
            console.log("[method lookup] container=" + c + " msgIndex=" + msgid);
            if (seen.has(key)) return;
            seen.add(key);
            const vb = c.add(0x1d0).readPointer(), ve = c.add(0x1d8).readPointer();
            const base = c.add(0x1b8).readPointer();
            const n = ve.sub(vb).toInt32() / 4;
            console.log("[exposed] count=" + n);
            for (let i = 0; i < n; i++) {
                const ix = vb.add(i * 4).readS32();
                console.log("   exposed[" + i + "] -> methods[" + ix + "] " + methodName(base.add(ix * 0x68)));
            }
        }
    });
    console.log("[+] hooked method lookup @ " + lib.base.add(0x9d46f8));
}
