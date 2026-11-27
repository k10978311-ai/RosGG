with open("extract/libclient.so", "rb") as f:
    f.seek(0x2a28900)
    data = f.read(512)

# split by null bytes
parts = data.split(b"\x00")
for p in parts:
    if p:
        print(p.decode("latin1", "replace"))
