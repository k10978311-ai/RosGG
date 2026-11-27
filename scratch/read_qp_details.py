import struct
with open('scratch/classes.dex', 'rb') as f:
    d = f.read()

string_ids_size, string_ids_off = struct.unpack_from('<II', d, 0x38)

def get_str(idx):
    if idx >= string_ids_size: return None
    off = struct.unpack_from('<I', d, string_ids_off + idx*4)[0]
    l = 0; shift = 0; p = off
    while True:
        b = d[p]; p += 1
        l |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return d[p:p+l].decode('utf-8', errors='replace')

p = 0x3e24e0
while p < 0x3e2600:
    op = d[p]
    if op == 0x1a:
        reg = d[p+1]
        s_id = struct.unpack_from('<H', d, p+2)[0]
        s = get_str(s_id)
        print("%s: const-string v%d, %r" % (hex(p), reg, s))
        p += 4
    elif op == 0x1b:
        reg = d[p+1]
        s_id = struct.unpack_from('<I', d, p+2)[0]
        s = get_str(s_id)
        print("%s: const-string/jumbo v%d, %r" % (hex(p), reg, s))
        p += 6
    else:
        p += 2
