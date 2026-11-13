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
    """The tail of LogOnParams holds the Blowfish session key.
    Structure: [0x04 = key length: 4 bytes] [4-byte BF key] ...
    The client initializes Blowfish with this 4-byte key! (Proven: 69.253.255.76 = 45fdff4c)"""
    import os as _os
    rest = params.get("rest", b"")
    spec = _os.environ.get("BF_SPEC")
    if not spec or spec == "1:16" or spec == "2:16":
        spec = "1:4"
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
        return rest[1:5]


def custom_bf_encrypt(key, data):
    """NeoX Mercury EncryptionFilter custom plaintext-feedback Blowfish mode.
    Block 0: BF_ecb_encrypt(P[0])
    Block i: BF_ecb_encrypt(P[i] ^ P[i-1])
    """
    from Crypto.Cipher import Blowfish
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    out = bytearray()
    prev_plain = None
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        if prev_plain is not None:
            xored = bytes(a ^ b for a, b in zip(block, prev_plain))
        else:
            xored = block
        out.extend(cipher.encrypt(xored))
        prev_plain = block
    return bytes(out)


def custom_bf_decrypt(key, data):
    """NeoX Mercury EncryptionFilter custom plaintext-feedback Blowfish mode decrypt.
    Block 0: BF_ecb_decrypt(C[0])
    Block i: BF_ecb_decrypt(C[i]) ^ P[i-1]
    """
    from Crypto.Cipher import Blowfish
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    out = bytearray()
    prev_plain = None
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        dec = cipher.decrypt(block)
        if prev_plain is not None:
            plain = bytes(a ^ b for a, b in zip(dec, prev_plain))
        else:
            plain = dec
        out.extend(plain)
        prev_plain = plain
    return bytes(out)


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

    # LoginReplyRecord in NeoX ARM64:
    # LoginHandler::onLoginReply reads 20 bytes (0x14) directly:
    #   [0..3]   uint32 IP (network byte order)
    #   [4..5]   uint16 Port (network byte order)
    #   [6..15]  10 bytes address padding / salt
    #   [16..19] uint32 sessionKey
    ip_bytes = socket.inet_aton(local_ip)
    port_be = struct.pack(">H", baseapp_port)
    session_key = struct.pack("<I", 0x11223344)
    record20 = ip_bytes + port_be + b"\x00" * 10 + session_key   # 20 bytes
    record = record20 + b"\x00" * 4                              # 24 bytes (multiple of 8)

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
    elif variant == 24:      # status + blowfish-encrypted 24-byte record
        enc_rec = record
        try:
            if bf:
                enc_rec = custom_bf_encrypt(bytes(bf), record)
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
