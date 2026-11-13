/**
 * Frida 17+ Compatible URL Sniffer for NetEase NeoX (Rules of Survival)
 */

const seenUrls = new Set();

function logUrl(source, url) {
    if (!url || seenUrls.has(url)) return;
    seenUrls.add(url);
    console.log(`\n[+] [${source}] URL: ${url}`);
}

console.log("[*] Starting NetEase NeoX URL Sniffer (Frida 17+)...");

// 1. Hook Java URL / OkHttp
if (Java.available) {
    Java.perform(function () {
        try {
            const URL = Java.use("java.net.URL");
            URL.$init.overload("java.lang.String").implementation = function (urlStr) {
                logUrl("Java.URL", urlStr);
                return this.$init(urlStr);
            };
        } catch (e) {}
    });
}

// 2. Hook libc.so :: strstr & send (Frida 17 API)
const libc = Process.findModuleByName("libc.so");
if (libc) {
    const strstrPtr = libc.findExportByName("strstr");
    if (strstrPtr) {
        Interceptor.attach(strstrPtr, {
            onEnter: function (args) {
                if (!args[0].isNull()) {
                    try {
                        const str = args[0].readUtf8String();
                        if (str && (str.startsWith("http://") || str.startsWith("https://")) && str.length < 300) {
                            logUrl("Native.strstr", str);
                        }
                    } catch (e) {}
                }
            }
        });
    }

    const sendPtr = libc.findExportByName("send");
    if (sendPtr) {
        Interceptor.attach(sendPtr, {
            onEnter: function (args) {
                const len = args[2].toInt32();
                if (len > 4 && len < 4096) {
                    try {
                        const buf = args[1].readUtf8String(Math.min(len, 512));
                        if (buf && (buf.startsWith("GET ") || buf.startsWith("POST ") || buf.startsWith("HEAD "))) {
                            console.log(`\n[TCP send Request]\n${buf.trim()}`);
                        }
                    } catch (e) {}
                }
            }
        });
    }
}

// 3. Hook SSL_write across loaded modules
const sslMod = Process.findModuleByName("libssl.so");
if (sslMod) {
    const sslWrite = sslMod.findExportByName("SSL_write");
    if (sslWrite) {
        Interceptor.attach(sslWrite, {
            onEnter: function (args) {
                const len = args[2].toInt32();
                if (len > 4 && len < 4096) {
                    try {
                        const buf = args[1].readUtf8String(Math.min(len, 512));
                        if (buf && (buf.startsWith("GET ") || buf.startsWith("POST ") || buf.startsWith("HEAD "))) {
                            console.log(`\n[SSL_write Request]\n${buf.trim()}`);
                        }
                    } catch (e) {}
                }
            }
        });
    }
}