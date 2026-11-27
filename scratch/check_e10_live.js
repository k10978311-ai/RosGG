const libclient = Process.findModuleByName("libclient.so");
if (!libclient) {
    console.log("[-] libclient.so not found");
} else {
    // Intercept 0x94bca4 in EntityMessageHandler
    const hookAddr = libclient.base.add(0x94bca4);
    Interceptor.attach(hookAddr, {
        onEnter: function(args) {
            const x23 = this.context.x23;
            const val = x23.add(0xe10).readU32();
            console.log("[*] EntityMessageHandler at 0x94bca4: x23=" + x23 + " [x23+0xe10]=" + val);
        }
    });
    console.log("[+] Hooked 0x94bca4");
}
