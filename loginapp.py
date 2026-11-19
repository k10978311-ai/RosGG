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

# Blowfish key slice inside decrypted LogOnParams.rest (confirmed on build 1.610637.617289)
os.environ["BF_SPEC"] = "1:4"


def _seq_footer(data):
    """u32 footer when Mercury reply uses flags HAS_SEQUENCE (0x40)."""
    mode = os.environ.get("SEQ_FOOTER", "off7")
    if mode == "off5":
        return data[5:9]
    if mode == "seq16":
        return struct.pack("<I", struct.unpack("<H", data[5:7])[0])
    # Client login requests keep bytes [7:11] == 01 00 00 00 while seq at [5:7] increments.
    return data[7:11]


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
    The client initializes Blowfish with this 4-byte key (BF_SPEC=1:4 on this build)."""
    import os as _os
    rest = params.get("rest", b"")
    spec = _os.environ.get("BF_SPEC")
    if not spec or spec in ("1:16", "2:16"):
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
        print(f"      [BF sweep] off={off} key={rest[off:off+4].hex()}")
        return rest[off:off+4]
    try:
        off, ln = (int(x) for x in spec.split(":"))
        if ln == 0:
            ln = len(rest) - off
        return rest[off:off+ln]
    except Exception:
        return rest[1:5]


def _build_record20(local_ip, baseapp_port, session_key):
    """20-byte LoginReplyRecord (layout selectable via RECORD_LAYOUT)."""
    ip_bytes = socket.inet_aton(local_ip)
    port_mode = os.environ.get("MERCURY_PORT_ENDIAN", "be").lower()
    if port_mode == "le":
        port_bytes = struct.pack("<H", baseapp_port)
    else:
        port_bytes = struct.pack(">H", baseapp_port)
    layout = os.environ.get("RECORD_LAYOUT", "compact").lower()
    if layout == "legacy":
        return ip_bytes + port_bytes + b"\x00" * 10 + session_key
    if layout == "compact":
        # Mercury::Address (8) + sessionKey (4) + pad (8) — matches scratch/port_check.py
        return ip_bytes + port_bytes + b"\x00\x00" + session_key + b"\x00" * 8
    if layout == "session_first":
        return session_key + ip_bytes + port_bytes + b"\x00" * 10
    if layout == "port_tail":
        # Client convertAddress reads port from last u16 (bytes 18-19); ip @ 0-3, session @ 8-11
        return ip_bytes + b"\x00" * 4 + session_key + b"\x00" * 4 + port_bytes
    if layout == "port_both":
        return ip_bytes + port_bytes + b"\x00\x00" + session_key + b"\x00" * 6 + port_bytes
    return ip_bytes + port_bytes + b"\x00\x00" + session_key + b"\x00" * 8


def extract_session_u32(params):
    """u32 for LoginReplyRecord.sessionKey — default fixed; override for RE sweeps."""
    hex_override = os.environ.get("SESSION_U32_HEX", "").strip()
    if hex_override:
        h = hex_override.replace("0x", "")
        if len(h) == 8:
            return bytes.fromhex(h)
    spec = os.environ.get("SESSION_U32_SPEC", "")
    rest = params.get("rest", b"")
    if spec and rest:
        try:
            off, ln = (int(x) for x in spec.split(":"))
            if ln == 4 and len(rest) >= off + 4:
                return rest[off : off + 4]
        except ValueError:
            pass
    return struct.pack("<I", int(os.environ.get("SESSION_U32", "0x11223344"), 0))


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
    rsa_block = data[15:143]
    params = decrypt_logon(rsa_block)
    bf = extract_blowfish_key(params)
    seq_footer = _seq_footer(data)

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

    session_key = extract_session_u32(params)
    record20 = _build_record20(local_ip, baseapp_port, session_key)
    record = record20 + b"\x00" * 4                              # 24 bytes (BF block alignment)

    # Variant selects the reply-data shape / encryption while we converge on the client's reaction.
    if variant == 10:        # LoginReplyRecord only (20B), no leading status byte
        rdata = record20
    elif variant == 11:      # status byte + record (exactly 20B LoginReplyRecord)
        rdata = bytes([LOGON_STATUS_LOGGED_ON]) + record20
    elif variant == 12:      # Cimmeria connect-reply shape: ticket_len=20 + 20-byte ticket
        ip_b = socket.inet_aton(local_ip)
        port_b = struct.pack(">H", baseapp_port)
        rdata = bytes([20]) + (session_key + ip_b + port_b + b"\x00" * 10)[:20]
    elif variant == 13:      # record blowfish-encrypted with the LogOnParams key
        rdata = record
        try:
            from Crypto.Cipher import Blowfish
            if bf:
                padded = record + b"\x00" * ((-len(record)) % 8)
                rdata = Blowfish.new(bytes(bf), Blowfish.MODE_ECB).encrypt(padded)
        except Exception:
            pass
    elif variant == 23:      # status(LOGGED_ON) + plaintext 20-byte LoginReplyRecord
        rdata = bytes([LOGON_STATUS_LOGGED_ON]) + record20
    elif variant == 24:      # status + NeoX custom_bf encrypted 24-byte record (20B + alignment pad)
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
    if variant in (11, 12, 13):
        flags = struct.pack("<H", 0x0000)         # plain off-channel packet
        pkt = flags + reply_msg
    elif variant in (10, 20, 22, 23, 24):
        flags = struct.pack("<H", 0x0040)         # HAS_SEQUENCE only + seq footer
        pkt = flags + reply_msg + seq_footer
    elif variant == 21:
        flags = struct.pack("<H", 0x0001)         # HAS_REQUESTS (mirror request) + firstReqOffset footer
        pkt = flags + reply_msg + struct.pack("<H", 2)
    else:
        flags = struct.pack("<H", 0x0058)
        pkt = flags + reply_msg + seq_footer
    if bf:
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "latest_bf_key.bin"), "wb") as f:
                f.write(bytes(bf))
        except Exception:
            pass
    return pkt, params, bf


def parse_baseapp_login_probe(data: bytes):
    """Post-login UDP probe `01 00 00 0b` (baseAppLogin channel setup)."""
    if len(data) < 12 or data[:4] != b"\x01\x00\x00\x0b":
        return None
    reply_id = data[7:11]
    if reply_id in (b"\x00\x00\x00\x00", b"\x00\x00\x00\x01"):
        # Some builds register the probe reply handler on data[5:9] instead.
        alt = data[5:9]
        if alt != b"\x00\x00\x00\x00":
            reply_id = alt
    return {
        "reply_id": reply_id,
        "req_field_5_9": data[5:9],
        "client_sess": data[11:15] if len(data) >= 15 else None,
        "seq_footer": _seq_footer(data),
    }


def build_baseapp_probe_reply_encrypted(data: bytes, bf_key: bytes, session_key: bytes):
    """Exactly one 0xFF reply for a baseAppLogin probe — no duplicate reply IDs."""
    probe = parse_baseapp_login_probe(data)
    if not probe or not bf_key:
        return None
    reply_id = probe["reply_id"]
    sess = session_key or probe.get("client_sess") or struct.pack("<I", 0x11223344)
    reply_msg = b"\xff" + struct.pack("<I", 8) + reply_id + sess
    pkt = struct.pack("<H", 0x0040) + reply_msg + probe["seq_footer"]
    pad_len = 8 - (len(pkt) % 8) or 8
    padded = pkt + b"\x00" * (pad_len - 1) + bytes([pad_len])
    return custom_bf_encrypt(bytes(bf_key), padded)


def parse_mercury_probe(data):
    """Best-effort parse of post-login UDP probes (magic 01 00 00 0b… from gate_capture)."""
    if len(data) < 16 or data[:3] != b"\x01\x00\x00":
        return None
    return {
        "magic": data[3],
        "seq": struct.unpack("<H", data[5:7])[0] if len(data) >= 7 else None,
        "field_7_11": data[7:11].hex() if len(data) >= 11 else None,
        "field_5_9": data[5:9].hex() if len(data) >= 9 else None,
        "len": len(data),
    }


def _bundle_body(pkt: bytes) -> bytes:
    """Mercury packet body after flags, without seq footer when HAS_SEQUENCE."""
    if len(pkt) < 2:
        return b""
    flags = struct.unpack("<H", pkt[:2])[0]
    body = pkt[2:]
    if flags & 0x0040 and len(body) >= 4:
        body = body[:-4]
    return body


def extract_identify_version_point(pkt: bytes):
    """Parse BaseAppExtInterface message 12 (0x0c identifyVersionPoint) from a bundle."""
    body = _bundle_body(pkt)
    i = 0
    while i + 3 <= len(body):
        msg_id = body[i]
        i += 1
        ln = struct.unpack_from("<H", body, i)[0]
        i += 2
        if i + ln > len(body):
            break
        payload = body[i : i + ln]
        i += ln
        if msg_id == 0x0C:
            return payload
    return None


def build_summarise_version_point(identify_payload: bytes) -> bytes:
    """BaseAppExtInterface message 13 (0x0d summariseVersionPoint), VARIABLE 2-byte len."""
    payload = identify_payload or (b"\x14\x00\x0a" + b"This docum")
    return bytes([0x0D]) + struct.pack("<H", len(payload)) + payload


def build_probe_ack(data):
    """Minimal off-channel Mercury reply to keep the channel handshake observable (experimental)."""
    if len(data) < 11 or data[:4] != b"\x01\x00\x00\x0b":
        return None
    # Mirror login-reply shape: HAS_SEQUENCE + 0xFF + request_id@5:9 + empty body.
    request_id = data[5:9]
    rdata = b""
    reply_msg = b"\xff" + struct.pack("<I", len(request_id) + len(rdata)) + request_id + rdata
    flags = struct.pack("<H", 0x0040)
    return flags + reply_msg + _seq_footer(data)


def build_baseapp_reply(data, variant=1, bf_key=None):
    """Reply to post-login baseAppLogin probes (magic 01 00 00 0b, ~24B).
    Encrypted with Blowfish CBC using the channel key and PKCS#7 padding."""
    if len(data) < 15 or data[:4] != b"\x01\x00\x00\x0b":
        return None
    req_id_7 = data[7:11]
    req_id_5 = data[5:9]
    sess_key = data[11:15] if len(data) >= 15 else b"\x44\x33\x22\x11"

    # In BaseAppLoginRequest::handleMessage (libclient.so+0x93d914):
    # stream.read(4) -> loads session key / entity ID -> schedules onBaseAppReply(this, key).
    # So reply payload for a request is: request_id (4B) + session_key (4B) = 8 bytes.
    rdata = sess_key

    seq_footer = _seq_footer(data)

    if bf_key is None:
        try:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "latest_bf_key.bin"), "rb") as f:
                bf_key = f.read().strip()
        except Exception:
            bf_key = None

    if variant == 1:
        # Match request_id at data[7:11]
        reply_payload = req_id_7 + rdata
        reply_msg = b"\xff" + struct.pack("<I", len(reply_payload)) + reply_payload
        flags = struct.pack("<H", 0x0040)
        raw = flags + reply_msg + seq_footer
    elif variant == 2:
        # Match request_id at data[5:9]
        reply_payload = req_id_5 + rdata
        reply_msg = b"\xff" + struct.pack("<I", len(reply_payload)) + reply_payload
        flags = struct.pack("<H", 0x0040)
        raw = flags + reply_msg + seq_footer
    elif variant == 3:
        # Both candidate reply IDs bundled together + createBasePlayer (msgid 4)
        msg1 = b"\xff" + struct.pack("<I", 8) + req_id_7 + rdata
        msg2 = b"\xff" + struct.pack("<I", 8) + req_id_5 + rdata
        flags = struct.pack("<H", 0x0040)
        raw = flags + msg1 + msg2 + seq_footer
    elif variant == 5:
        # Reply to baseAppLogin + createBasePlayer (entity ID 10001, Avatar entity type 1)
        reply_payload = req_id_7 + rdata
        reply_msg = b"\xff" + struct.pack("<I", len(reply_payload)) + reply_payload
        cbp_msg = b"\x04\x06\x00" + struct.pack("<I", 10001) + struct.pack("<H", 1)
        flags = struct.pack("<H", 0x0040)
        raw = flags + reply_msg + cbp_msg + seq_footer
    elif variant == 4:
        # Off-channel flags 0x0000
        reply_payload = req_id_7 + rdata
        reply_msg = b"\xff" + struct.pack("<I", len(reply_payload)) + reply_payload
        flags = struct.pack("<H", 0x0000)
        raw = flags + reply_msg
    else:
        reply_payload = req_id_7 + rdata
        reply_msg = b"\xff" + struct.pack("<I", len(reply_payload)) + reply_payload
        flags = struct.pack("<H", 0x0040)
        raw = flags + reply_msg + seq_footer

    # Apply PKCS#7 padding and Blowfish-CBC encryption
    if bf_key:
        try:
            from Crypto.Cipher import Blowfish
            pad_len = 8 - (len(raw) % 8)
            padded = raw + bytes([pad_len]) * pad_len
            cipher = Blowfish.new(bytes(bf_key), Blowfish.MODE_CBC, b"\x00" * 8)
            return cipher.encrypt(padded)
        except Exception as e:
            print(f"      [BASEAPP BF enc err] {e}")

    return raw
