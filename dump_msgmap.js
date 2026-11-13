/**
 * Dump the BigWorld message map by hooking the InterfaceElement registration
 * function at libclient.so + 0x98f654 (and the 3-arg sibling 0x98f5dc).
 *
 * Observed call shape (ARM64):
 *   x0 = interface object (this)
 *   x1 = const char* name
 *   w2 = lengthStyle   (0 = FIXED, 1 = VARIABLE, 2 = CALLBACK)
 *   w3 = lengthParam   (fixed: byte length; variable: #bytes of length field)
 *   -> returns the assigned message id (x0)
 */
const STYLE = { 0: "FIXED", 1: "VARIABLE", 2: "CALLBACK", 3: "VARIABLE4?" };
let installed = false;

function hookReg(off, label) {
    const addr = base.add(off);
    Interceptor.attach(addr, {
        onEnter(args) {
            this.iface = args[0];
            try { this.name = args[1].readUtf8String(); } catch (e) { this.name = "?"; }
            this.w2 = args[2].toInt32() & 0xffffffff;
            this.w3 = args[3].toInt32() & 0xffffffff;
        },
        onLeave(ret) {
            const id = ret.toInt32() & 0xff;
            console.log(`[${label}] id=0x${id.toString(16).padStart(2,"0")} (${id})  ` +
                        `style=${this.w2}(${STYLE[this.w2]||this.w2}) param=${this.w3}  name=${this.name}`);
        }
    });
    console.log("[*] hooked " + label + " @ " + addr);
}

function install() {
    if (installed) return true;
    const mod = Process.findModuleByName("libclient.so");
    if (!mod) return false;
    globalThis.base = mod.base;
    console.log("[*] libclient.so base = " + mod.base);
    hookReg.base = mod.base;
    hookReg(0x98f654, "REG4");
    hookReg(0x98f5dc, "REG3");
    installed = true;
    console.log("[*] message-map dumper armed");
    return true;
}
// patch hookReg to use the resolved base
const _hookReg = hookReg;
// try immediately, then poll until the module shows up
if (!install()) {
    const iv = setInterval(() => { if (install()) clearInterval(iv); }, 20);
}
