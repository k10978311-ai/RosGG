/**
 * READ-ONLY RE trace: log each property as EntityDescription::readStream parses it.
 *   0x9d4fdc  per-property visitor(this{+8 stream,+0x10 dict}, DataDescription* desc)
 *   0x9a5008  DataDescription name getter -> libc++ std::string*
 * Prints "name remaining_before" in parse order, so the server can build streams in exactly the
 * client's order. Observes only (calls the name getter and the stream's size() virtual).
 */
const lib = Process.findModuleByName("libclient.so");
const getName = new NativeFunction(lib.base.add(0x9a5008), "pointer", ["pointer"]);
function readStdString(p) {
    const b0 = p.readU8();
    if ((b0 & 1) === 0) return p.add(1).readUtf8String(b0 >> 1);
    const n = p.add(8).readU64().toNumber();
    return p.add(16).readPointer().readUtf8String(n);
}
let n = 0;
Interceptor.attach(lib.base.add(0x9d4fdc), {
    onEnter(args) {
        try {
            const name = readStdString(getName(args[1]));
            const stream = args[0].add(8).readPointer();
            const size = new NativeFunction(stream.readPointer().add(0x18).readPointer(), "int", ["pointer"])(stream);
            console.log("PROP " + (n++) + " " + name + " " + size);
        } catch (e) { console.log("PROP err " + e); }
    }
});
console.log("[+] prop-order hook ready");
