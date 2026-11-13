import re
data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
for m in re.finditer(rb"-----BEGIN [A-Z ]*PUBLIC KEY-----", data):
    start = m.start()
    end = data.find(b"-----END", start)
    if end != -1:
        end = data.find(b"-----", end + 5) + 5
        block = data[start:end]
        if 60 < len(block) < 1000:
            print("OFFSET", hex(start), "len", len(block))
            print(block.decode("ascii", "replace"))
            print("----")
# also any base64-looking RSA modulus blobs near 'Mercury' login
idx = data.find(b"publicEncrypt failed")
print("publicEncrypt str at", hex(idx) if idx>=0 else "n/a")
