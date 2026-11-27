/**
 * READ-ONLY RE trace: how server->client method ids are decoded (observes only).
 *   0x9644a4 dispatcher (w2 = msg idx)            -> retval (1 = dispatched)
 *   0x9a4600 id->description decoder (w1 = idx)   -> path vector out (x3)
 *   0x9d4644 method-by-index lookup (w1 = index)
 */
const lib = Process.findModuleByName("libclient.so");
const B = (o) => lib.base.add(o);
function hook(off, name, enter, leave) {
    try {
        Interceptor.attach(B(off), { onEnter(a) { this.a = a; if (enter) enter.call(this, a); }, onLeave(r) { if (leave) leave.call(this, r); } });
        console.log("[+] hooked " + name);
    } catch (e) { console.log("[-] " + name + " " + e); }
}
hook(0x9644a4, "dispatch", function (a) { this.idx = a[2].toInt32(); }, function (r) { console.log("[dispatch] idx=" + this.idx + " ret=" + r.toInt32()); });
hook(0x9a4600, "decode", function (a) {
    this.idx = a[1].toInt32(); this.out = a[3];
    try { const o = a[0]; const cnt = new NativeFunction(o.readPointer().add(0x18).readPointer(), 'int', ['pointer'])(o); this.cnt = cnt; } catch (e) { this.cnt = "?" + e; }
}, function (r) {
    let path = [];
    try {
        const b0 = this.out.readU8();
        if ((b0 & 1) === 0) { const n = b0 >> 1; for (let i = 0; i < n; i++) path.push(this.out.add(4 + 4 * i).readS32()); }
        else { const n = this.out.add(8).readU64().toNumber(); const p = this.out.add(16).readPointer(); for (let i = 0; i < n && i < 8; i++) path.push(p.add(4 * i).readS32()); }
    } catch (e) { path = ["err " + e]; }
    console.log("[decode] idx=" + this.idx + " count=" + this.cnt + " ret=" + r + " path=" + JSON.stringify(path));
});
hook(0x9d4644, "lookup", function (a) { console.log("[lookup] index=" + a[1].toInt32()); });
console.log("method-decode trace ready");
