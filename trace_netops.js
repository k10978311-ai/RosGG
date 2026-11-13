/**
 * Frida script: trace Mercury login reply handling and BaseApp connect.
 * Hooks:
 *   1. sendto() - to see what UDP packets the client sends (BaseApp probes)
 *   2. recvfrom() - to confirm it receives our login reply
 *   3. connect() - to see if it tries a socket connect to BaseApp
 *   4. onLoginReply handler area - trace the callback result
 */

const libc = Process.getModuleByName("libc.so");

// Hook sendto
const sendto_p = libc.findExportByName("sendto");
if (sendto_p) {
    Interceptor.attach(sendto_p, {
        onEnter(args) {
            try {
                const fd  = args[0].toInt32();
                const buf = args[1];
                const len = args[2].toInt32();
                const flags = args[3].toInt32();
                const addr_ptr = args[4];
                if (addr_ptr.isNull()) return;
                // Parse sockaddr_in: family(2) + port(2 BE) + ip(4)
                const family = addr_ptr.readU16();
                if (family !== 2) return; // AF_INET only
                const port = (addr_ptr.add(2).readU8() << 8) | addr_ptr.add(3).readU8();
                const ip_b = [addr_ptr.add(4).readU8(), addr_ptr.add(5).readU8(),
                              addr_ptr.add(6).readU8(), addr_ptr.add(7).readU8()];
                const ip_str = ip_b.join('.');
                const payload = buf.readByteArray(Math.min(len, 32));
                const hex = Array.from(new Uint8Array(payload))
                    .map(b => b.toString(16).padStart(2,'0')).join('');
                console.log(`[sendto] fd=${fd} -> ${ip_str}:${port} len=${len} data=${hex}`);
            } catch(e) {}
        }
    });
    console.log("[*] sendto hooked");
}

// Hook recvfrom
const recvfrom_p = libc.findExportByName("recvfrom");
if (recvfrom_p) {
    Interceptor.attach(recvfrom_p, {
        onLeave(retval) {
            try {
                const len = retval.toInt32();
                if (len <= 0) return;
                const buf = this.context.x1 || this.context.r1;  // ARM/ARM64
                const addr_ptr = this.context.x4 || this.context.r4;
                if (!buf || buf.isNull()) return;
                const payload = buf.readByteArray(Math.min(len, 48));
                const hex = Array.from(new Uint8Array(payload))
                    .map(b => b.toString(16).padStart(2,'0')).join('');
                // Try to get source addr
                let src = '';
                try {
                    if (!addr_ptr.isNull()) {
                        const family = addr_ptr.readU16();
                        if (family === 2) {
                            const port = (addr_ptr.add(2).readU8() << 8) | addr_ptr.add(3).readU8();
                            const ip_b = [addr_ptr.add(4).readU8(), addr_ptr.add(5).readU8(),
                                          addr_ptr.add(6).readU8(), addr_ptr.add(7).readU8()];
                            src = ` from=${ip_b.join('.')}:${port}`;
                        }
                    }
                } catch(e) {}
                console.log(`[recvfrom] len=${len}${src} data=${hex}`);
            } catch(e) {}
        },
        onEnter(args) {
            this.buf_arg  = args[1];
            this.addr_arg = args[4];
        }
    });
    console.log("[*] recvfrom hooked");
}

// Hook connect (TCP/UDP)
const connect_p = libc.findExportByName("connect");
if (connect_p) {
    Interceptor.attach(connect_p, {
        onEnter(args) {
            try {
                const fd = args[0].toInt32();
                const addr_ptr = args[1];
                const family = addr_ptr.readU16();
                if (family !== 2) return;
                const port = (addr_ptr.add(2).readU8() << 8) | addr_ptr.add(3).readU8();
                const ip_b = [addr_ptr.add(4).readU8(), addr_ptr.add(5).readU8(),
                              addr_ptr.add(6).readU8(), addr_ptr.add(7).readU8()];
                console.log(`[connect] fd=${fd} -> ${ip_b.join('.')}:${port}`);
            } catch(e) {}
        }
    });
    console.log("[*] connect hooked");
}

console.log("[*] Mercury network tracer armed - trigger PLAY now");
