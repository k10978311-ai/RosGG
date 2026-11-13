const mods = Process.enumerateModules().filter(m => /client|neox|messiah/i.test(m.name));
console.log("[*] modules matching client/neox:");
mods.forEach(m => console.log(`    ${m.name}  base=${m.base}  size=${m.size}  path=${m.path}`));
const lc = Process.findModuleByName("libclient.so");
console.log("[*] findModuleByName(libclient.so) = " + (lc ? lc.base : "NULL"));
if (!lc) {
    console.log("[!] libclient.so missing — on LDPlayer attach with: frida -U --realm=emulated");
    console.log("    or: python run_frida.py diag.js --attach --realm emulated");
}
function check_libclient() {
    const m = Process.findModuleByName("libclient.so");
    return m ? { name: m.name, base: m.base.toString(), size: m.size } : null;
}
rpc.exports = { check_libclient };
