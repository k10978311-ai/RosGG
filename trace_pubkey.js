/**
 * Trace how the NeoX client loads entities/loginapp.pubkey.
 * Hooks fopen/open and the OpenSSL PEM reader to dump the key bytes + lookup path.
 */
const libc = Process.getModuleByName("libc.so");

function hookOpen(name) {
    const p = libc.findExportByName(name);
    if (!p) return;
    Interceptor.attach(p, {
        onEnter(args) {
            try {
                const path = args[0].readUtf8String();
                if (path && /pubkey|loginapp|entities/i.test(path)) {
                    console.log(`[${name}] ${path}`);
                }
            } catch (e) {}
        }
    });
}
["fopen", "open", "open64", "fopen64"].forEach(hookOpen);

// Dump the PEM buffer handed to the public-key parser (BIO_new_mem_buf or d2i)
function hookPemReader(mod) {
    const names = ["PEM_read_bio_PUBKEY", "PEM_read_bio_RSA_PUBKEY", "BIO_new_mem_buf"];
    for (const n of names) {
        const p = mod.findExportByName(n);
        if (!p) continue;
        Interceptor.attach(p, {
            onEnter(args) {
                if (n === "BIO_new_mem_buf") {
                    try {
                        const len = args[1].toInt32();
                        const buf = args[0];
                        if (len > 50 && len < 4000) {
                            const s = buf.readUtf8String(Math.min(len, 2000));
                            if (s && s.indexOf("KEY") >= 0) {
                                console.log(`[BIO_new_mem_buf ${len}]\n${s}`);
                            }
                        }
                    } catch (e) {}
                } else {
                    console.log(`[${n}] called`);
                }
            }
        });
    }
}

const client = Process.findModuleByName("libclient.so");
if (client) {
    try { hookPemReader(client); } catch (e) { console.log("pem hook err " + e); }
}
console.log("[*] pubkey tracer armed");
