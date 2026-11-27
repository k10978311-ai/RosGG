import struct, re

with open("extract/libclient.so", "rb") as f:
    data = f.read()

# Let's search for string "createBasePlayer" or "resetEntities"
for s in [b"createBasePlayer", b"resetEntities", b"bandwidthNotification"]:
    idx = 0
    while True:
        idx = data.find(s, idx)
        if idx == -1: break
        print(f"String '{s.decode()}' at 0x{idx:x}")
        idx += len(s)
