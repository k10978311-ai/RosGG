"""Split the captured gate stream into 145-byte login packets and diff their fields."""
d = open(r"C:\Users\Lufy\Desktop\Server\gate_capture.bin", "rb").read()
SZ = 145
pkts = [d[i:i+SZ] for i in range(0, len(d)-SZ+1, SZ) if len(d[i:i+SZ]) == SZ]
# keep only packets that look like login (start 01 00 00 84)
pkts = [p for p in pkts if p[:4] == b"\x01\x00\x00\x84"]
print(f"{len(pkts)} login packets")
if not pkts:
    raise SystemExit
# header = first 15 bytes, then 128 RSA, then 2 trailer
for idx, p in enumerate(pkts[:12]):
    print(f"pkt{idx}: hdr={p[:15].hex()} trailer={p[-2:].hex()}")
print("\n--- per-byte: constant across packets? ---")
for off in range(15):
    vals = {p[off] for p in pkts}
    tag = "CONST" if len(vals) == 1 else "VARY "
    print(f"byte[{off:2}] {tag} {' '.join('%02x'%p[off] for p in pkts[:10])}")
print("trailer bytes:")
for off in (SZ-2, SZ-1):
    vals = {p[off] for p in pkts}
    print(f"byte[{off}] {'CONST' if len(vals)==1 else 'VARY'} {' '.join('%02x'%p[off] for p in pkts[:10])}")
