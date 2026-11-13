import re, struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Let's search for calls to EncryptionFilter constructor or setKey
# Typeinfo for EncryptionFilter was at 0x38c5f90
# Let's search for ADRP/references to 0x38c5f90 or "EncryptionFilter" strings
matches = []
for m in re.finditer(b"EncryptionFilter", data):
    matches.append(m.start())
print("EncryptionFilter string matches:", [hex(x) for x in matches])
for pos in matches:
    end = data.find(b"\x00", pos)
    print(" ", data[pos:end])
