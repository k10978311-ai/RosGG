/**
 * READ-ONLY RE trace of the server->client entity message path (observes only).
 *   0x94c10c ServerConnection::createBasePlayer   (control: must fire)
 *   0x94bbf0 EntityMessageHandler::handleMessage  (msg id, selected entity, handler)
 *   handler vtable+0x40 (entity method) / +0x48 (property)  (attached dynamically)
 *   0x964918 SimpleClientEntity::methodEvent, 0x9d46f8 exposed-method lookup
 * LDPlayer: python run_frida.py frida/trace_entity_msgs.js --attach --realm emulated
 */
const lib = Process.findModuleByName("libclient.so");
const B = (o) => lib.base.add(o);
const rel = (p) => "+0x" + p.sub(lib.base).toString(16);
const attached = new Set();

function hook(addr, name, cb) {
    try {
        Interceptor.attach(addr, { onEnter(args) { cb ? cb.call(this, args) : console.log("[" + name + "]"); } });
        console.log("[+] hooked " + name + " @ " + rel(addr));
    } catch (e) { console.log("[-] hook " + name + " failed: " + e); }
}

if (!lib) {
    console.log("[-] libclient.so not found (use --realm emulated)");
} else {
    hook(B(0x94c10c), "ServerConnection::createBasePlayer");
    hook(B(0x9260d0), "Entity::onMethod", (a) => console.log("[Entity::onMethod] idx=" + a[1].toInt32()));
    hook(B(0x964918), "SimpleClientEntity::methodEvent", (a) => console.log("[methodEvent] idx=" + a[2].toInt32()));
    const dumped = new Set();
    hook(B(0x9d46f8), "exposedLookup", (a) => {
        const c = a[0];
        console.log("[exposedLookup] idx=" + (a[1].toInt32() & 0xff) + " container=" + c);
        if (dumped.has(c.toString())) return;
        dumped.add(c.toString());
        try {
            const vb = c.add(0x1d0).readPointer(), ve = c.add(0x1d8).readPointer();
            const base = c.add(0x1b8).readPointer();
            const n = ve.sub(vb).toInt32() / 4;
            for (let i = 0; i < n; i++) {
                const ix = vb.add(i * 4).readS32();
                const m = base.add(ix * 0x68);
                let name = "?";
                for (const off of [8, 0, 16, 24, 32]) {
                    try {
                        const p = m.add(off), b0 = p.readU8();
                        let s = null;
                        if ((b0 & 1) === 0) { const k = b0 >> 1; if (k > 2 && k < 23) s = p.add(1).readUtf8String(k); }
                        else { const k = p.add(8).readU64().toNumber(); if (k > 2 && k < 100) s = p.add(16).readPointer().readUtf8String(k); }
                        if (s && /^[A-Za-z_]\w+$/.test(s)) { name = s + "@" + off; break; }
                    } catch (e) {}
                }
                console.log("   exposed[" + i + "] -> methods[" + ix + "] " + name);
            }
        } catch (e) { console.log("   dump err " + e); }
    });
    hook(B(0x94bbf0), "EntityMessageHandler::handleMessage", (a) => {
        try {
            const hdr = a[2];
            const msgid = hdr.readU8();
            const sc = hdr.add(0x10).readPointer().add(0x4458).readPointer();
            const sel = sc.add(0xe10).readU32();
            const handler = sc.add(0x110).readPointer();
            const queued = sc.add(0x140).readPointer();
            console.log("[EntityMsg] id=0x" + msgid.toString(16) + " selected=" + sel + " handler=" + handler + " sc+0x140=" + queued);
            if (!handler.isNull()) {
                const vt = handler.readPointer();
                for (const [off, nm] of [[0x40, "handler.method"], [0x48, "handler.property"]]) {
                    const fn = vt.add(off).readPointer();
                    if (!attached.has(fn.toString())) {
                        attached.add(fn.toString());
                        console.log("    " + nm + " -> " + rel(fn));
                        hook(fn, nm, (b) => console.log("[" + nm + "] id=" + b[1].toInt32() + " idx=" + b[2].toInt32()));
                    }
                }
            }
        } catch (e) { console.log("[EntityMsg] read err " + e); }
    });
}
