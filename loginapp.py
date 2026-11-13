"""Experimental BigWorld/NeoX Mercury LoginApp reply builder.

The client (libclient.so, neox::bwclient) sends a login request to UDP :25000:

    01 00 00 84 | 00 | seq(uint16 LE) | 01 00 00 00 | 2b | 00 00 00 | <128B RSA LogOnParams> | 02 00

We swapped entities/loginapp.pubkey for our own key, so the 128-byte block decrypts
(RSA-OAEP) to LogOnParams: flags, username, password, and a Blowfish session key.

Goal of this module: craft a login *reply* the client's LoginHandler::onLoginReply
accepts, carrying the BaseApp address + a session key (Blowfish-encrypted). This is
iterative — we send a candidate and read the client's Mercury log reaction.
"""
import os, struct, socket

PRIV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server_keys", "loginapp_priv.pem")
LOGON_STATUS_LOGGED_ON = 1


def decrypt_logon(rsa_block):
    """RSA-OAEP decrypt the 128-byte block with our private key -> LogOnParams fields."""
    try:
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_OAEP
        key = RSA.import_key(open(PRIV).read())
        pt = PKCS1_OAEP.new(key).decrypt(rsa_block)
    except Exception as e:
        return {"error": f"decrypt failed: {e}"}
    try:
        i = 0
        flags = pt[i]; i += 1
        ul = pt[i]; i += 1
        username = pt[i:i+ul]; i += ul
        pl = pt[i]; i += 1
        password = pt[i:i+pl]; i += pl
        rest = pt[i:]
        return {"flags": flags, "username": username, "password": password,
                "rest": rest, "raw": pt}
    except Exception as e:
        return {"error": f"parse failed: {e}", "raw": pt}


def extract_blowfish_key(params):
    """The tail of LogOnParams holds the Blowfish session key. The exact slice is set by
    env BF_SPEC="offset:length" into `rest` (confirmed: offset=1, length=16, ECB mode).
    Structure: 04 | <16-byte BF key> | <4-byte per-session nonce>
    The 0x04 prefix is a type tag; the 16-byte key follows immediately at offset 1."""
    import os as _os
    rest = params.get("rest", b"")
    spec = _os.environ.get("BF_SPEC", "1:16")
    if spec == "sweep":
        f = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "bf_off.txt")
        try:
            off = int(open(f).read().strip())
        except Exception:
            off = 0
        try:
            open(f, "w").write(str((off + 1) % 10))
        except Exception:
            pass
        print(f"      [BF sweep] off={off} key={rest[off:off+16].hex()}")
        return rest[off:off+16]
    try:
        off, ln = (int(x) for x in spec.split(":"))
        if ln == 0:
            ln = len(rest) - off
        return rest[off:off+ln]
    except Exception:
        return rest[1:17]


def build_reply(data, local_ip, baseapp_port, variant=0):
    """Build a candidate reply for a captured login request `data`."""
    if len(data) < 145 or data[:4] != b"\x01\x00\x00\x84":
        return None
    seq = data[5:7]                      # echo the request sequence
    rsa_block = data[15:143]
    params = decrypt_logon(rsa_block)
    bf = extract_blowfish_key(params)

    # LoginReplyRecord: Mercury::Address(serverAddr) + sessionKey(uint32)
    ip_bytes = socket.inet_aton(local_ip)                 # 4 bytes, network order
    port_be = struct.pack(">H", baseapp_port)             # BigWorld stores port in network order
    salt = b"\x00\x00"
    session_key = struct.pack("<I", 0x11223344)
    record = ip_bytes + port_be + salt + session_key      # 12 bytes

    # Blowfish-encrypt the record (ECB, pad to 8) if we have a key
    enc = record
    try:
        from Crypto.Cipher import Blowfish
        if bf:
            padlen = (-len(record)) % 8
            padded = record + b"\x00" * padlen
            enc = Blowfish.new(bytes(bf), Blowfish.MODE_ECB).encrypt(padded)
    except Exception:
        pass

    # BigWorld Mercury wire format (from Cimmeria RE):
    #   header: flags (2 bytes LE) at offset 0
    #   body:   messages. A REPLY message = [0xFF][len:u32 LE][request_id:u32][reply data]
    #   footer: sequence id (u32) present when flag 0x40 set, at the packet tail
    # REPLY_FLAGS = 0x58 = ON_CHANNEL(0x08)|RELIABLE(0x10)|HAS_SEQUENCE(0x40)
    REPLY_FLAGS = 0x58
    # request/reply id: must match the client's pending login request. Sweep it via
    # sweep_msgid.txt when variant == 20 (framing is confirmed correct: flags 0x40 + seq).
    import os as _os
    if variant == 20:
        _f = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "sweep_msgid.txt")
        try:
            rid = int(open(_f).read().strip())
        except Exception:
            rid = 0
        try:
            open(_f, "w").write(str(rid + 1))   # advance sweep each reply
        except Exception:
            pass
        request_id = struct.pack("<I", rid)
    elif variant == 22:
        request_id = data[11:15]     # the constant 2b 00 00 00 field (= 43) — reply-id candidate
    elif variant in (23, 24):
        request_id = data[5:9]       # Cimmeria: request_id at body[3..7] = packet offset 5..9
    else:
        request_id = data[7:11]

    # reply data — try the BigWorld LoginReplyRecord: serverAddr(ip4+port2+salt2) + sessionKey(4)
    ip_bytes = socket.inet_aton(local_ip)
    port_be = struct.pack(">H", baseapp_port)
    salt = b"\x00\x00"
    session_key = struct.pack("<I", 0x11223344)
    record = ip_bytes + port_be + salt + session_key     # 12 bytes

    # Variant selects the reply-data shape / encryption while we converge on the client's reaction.
    if variant == 10:        # LoginReplyRecord, plaintext
        rdata = record
    elif variant == 11:      # status byte + record
        rdata = bytes([LOGON_STATUS_LOGGED_ON]) + record
    elif variant == 12:      # Cimmeria connect-reply shape: ticket_len=20 + 20-byte ticket
        rdata = bytes([20]) + (session_key + ip_bytes + port_be + b"\x00"*10)[:20]
    elif variant == 13:      # record blowfish-encrypted with the LogOnParams key
        rdata = record
        try:
            from Crypto.Cipher import Blowfish
            if bf:
                padded = record + b"\x00" * ((-len(record)) % 8)
                rdata = Blowfish.new(bytes(bf), Blowfish.MODE_ECB).encrypt(padded)
        except Exception:
            pass
    elif variant == 23:      # status(LOGGED_ON) + plaintext record
        rdata = bytes([LOGON_STATUS_LOGGED_ON]) + record
    elif variant == 24:      # status + blowfish-encrypted record
        import os as _os
        mode = _os.environ.get("BF_MODE", "ecb")
        enc_rec = record
        try:
            from Crypto.Cipher import Blowfish
            if bf:
                padded = record + b"\x00" * ((-len(record)) % 8)
                if mode == "cbc":
                    c = Blowfish.new(bytes(bf), Blowfish.MODE_CBC, b"\x00" * 8)
                elif mode == "cfb":
                    c = Blowfish.new(bytes(bf), Blowfish.MODE_CFB, b"\x00" * 8)
                else:
                    c = Blowfish.new(bytes(bf), Blowfish.MODE_ECB)
                enc_rec = c.encrypt(padded)
        except Exception as _e:
            print(f"      [BF enc err] {_e}")
        rdata = bytes([LOGON_STATUS_LOGGED_ON]) + enc_rec
    else:                    # default: plaintext record
        rdata = record

    reply_msg = b"\xff" + struct.pack("<I", len(request_id) + len(rdata)) + request_id + rdata

    # The login reply is OFF-channel (no channel exists yet), so ON_CHANNEL(0x08) must be
    # cleared or the client drops it: "absence of local channel". Try off-channel flags.
    if variant in (10, 11, 12, 13):
        flags = struct.pack("<H", 0x0000)         # plain off-channel packet
        pkt = flags + reply_msg
    elif variant in (20, 22, 23, 24):
        flags = struct.pack("<H", 0x0040)         # HAS_SEQUENCE only + seq footer
        pkt = flags + reply_msg + struct.pack("<I", 1)
    elif variant == 21:
        flags = struct.pack("<H", 0x0001)         # HAS_REQUESTS (mirror request) + firstReqOffset footer
        pkt = flags + reply_msg + struct.pack("<H", 2)
    else:
        flags = struct.pack("<H", 0x0058)
        pkt = flags + reply_msg + struct.pack("<I", 1)
    return pkt, params, bf
