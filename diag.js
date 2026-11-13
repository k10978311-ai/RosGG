const mods = Process.enumerateModules().filter(m => /client|neox|messiah/i.test(m.name));
console.log("[*] modules matching client/neox:");
mods.forEach(m => console.log(`    ${m.name}  base=${m.base}  size=${m.size}  path=${m.path}`));
const lc = Process.findModuleByName("libclient.so");
console.log("[*] findModuleByName(libclient.so) = " + (lc ? lc.base : "NULL"));
