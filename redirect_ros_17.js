/**
 * Frida 17.26.2 Network Redirector + URL Sniffer for Rules of Survival (LDPlayer)
 * File: redirect_ros_17.js
 *
 * Usage:  frida -U -f com.netease.chiji -l redirect_ros_17.js
 */

const LOCAL_IP = "192.168.1.18";   // Windows PC LAN IPv4 (must match ros_mock_server.py)
const LOCAL_HTTP_PORT = 80;
const LOCAL_GATE_PORT = 20001;

// Strstr is called constantly by the engine; disable if the game stutters/ANRs.
const ENABLE_STRSTR_URL_LOG = true;
// Redirect TCP connects to *any* non-local IP:port>1024 (catches hard-coded gate IPs).
// Set false if it breaks unrelated traffic (Google Play services, LDPlayer, etc.).
const REDIRECT_ALL_HIGH_PORTS = true;

const DOMAIN_MATCHES = ["netease", "163.com", "126.net", "easebar", "chiji", "g83", "nie."];

function inet_addr(ipStr) {
    const p = ipStr.split('.').map(Number);
    return ((p[3] << 24) | (p[2] << 16) | (p[1] << 8) | p[0]) >>> 0;
}
function intToIPv4(num) {
    return [num & 0xff, (num >>> 8) & 0xff, (num >>> 16) & 0xff, (num >>> 24) & 0xff].join('.');
}
function swap16(v) {
    return ((v & 0xff) << 8) | ((v >> 8) & 0xff);
}

const localIpInt = inet_addr(LOCAL_IP);
const libc = Process.findModuleByName("libc.so");

console.log(`[*] Frida 17 Redirector Active -> Routing NetEase traffic to ${LOCAL_IP}`);

if (!libc) {
    console.log("[!] libc.so not found — nothing hooked");
} else {
    // 1. Log HTTP/HTTPS URL strings passed through strstr
    const strstrPtr = libc.findExportByName("strstr");
    if (ENABLE_STRSTR_URL_LOG && strstrPtr) {
        const seen = new Set();
        Interceptor.attach(strstrPtr, {
            onEnter(args) {
                if (args[0].isNull()) return;
                try {
                    const s = args[0].readUtf8String(300);
                    if (s && (s.startsWith("http://") || s.startsWith("https://")) && !seen.has(s)) {
                        seen.add(s);
                        console.log(`[URL] ${s}`);
                    }
                } catch (e) {}
            }
        });
    }

    // 2. getaddrinfo: resolve NetEase domains to the PC
    const getaddrinfoPtr = libc.findExportByName("getaddrinfo");
    if (getaddrinfoPtr) {
        Interceptor.attach(getaddrinfoPtr, {
            onEnter(args) {
                if (args[0].isNull()) return;
                let host;
                try { host = args[0].readUtf8String(); } catch (e) { return; }
                if (host && DOMAIN_MATCHES.some(d => host.includes(d))) {
                    console.log(`[DNS] Redirecting ${host} -> ${LOCAL_IP}`);
                    this.buf = Memory.allocUtf8String(LOCAL_IP); // keep reference alive for the call
                    args[0] = this.buf;
                }
            }
        });
    }

    // 3. connect: force HTTP(S) and gate TCP to the PC
    const connectPtr = libc.findExportByName("connect");
    if (connectPtr) {
        Interceptor.attach(connectPtr, {
            onEnter(args) {
                const sa = args[1];
                if (sa.isNull()) return;
                const family = sa.readU16();
                if (family === 10) { // AF_INET6 — not rewritten, just reported
                    console.log(`[IPv6] connect() seen (not redirected) port ${swap16(sa.add(2).readU16())}`);
                    return;
                }
                if (family !== 2) return; // AF_INET only

                const port = swap16(sa.add(2).readU16());
                const ipStr = intToIPv4(sa.add(4).readU32());
                if (ipStr.startsWith("127.") || port === 53 || port === 27042) return;

                if (port === 80) {
                    if (ipStr !== LOCAL_IP) console.log(`[HTTP] ${ipStr}:80 -> ${LOCAL_IP}:${LOCAL_HTTP_PORT}`);
                    sa.add(2).writeU16(swap16(LOCAL_HTTP_PORT));
                    sa.add(4).writeU32(localIpInt);
                } else if (port === 443) {
                    // NOTE: a TLS ClientHello sent to a plain-HTTP server will fail. Kept on 443 so it
                    // fails visibly; needs a TLS listener on the PC (and likely a cert-pinning bypass).
                    console.log(`[HTTPS] ${ipStr}:443 -> ${LOCAL_IP}:443  (needs TLS listener!)`);
                    sa.add(4).writeU32(localIpInt);
                } else if (port > 1024 && port !== LOCAL_GATE_PORT &&
                           (ipStr === LOCAL_IP || REDIRECT_ALL_HIGH_PORTS)) {
                    console.log(`[GATE TCP] ${ipStr}:${port} -> ${LOCAL_IP}:${LOCAL_GATE_PORT}`);
                    sa.add(2).writeU16(swap16(LOCAL_GATE_PORT));
                    sa.add(4).writeU32(localIpInt);
                }
            }
        });
    }
}
