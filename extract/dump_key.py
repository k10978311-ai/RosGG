data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
needle = b"-----BEGIN PUBLIC KEY-----"
i = 0
while True:
    i = data.find(needle, i)
    if i < 0:
        break
    print("=== BEGIN marker at", hex(i))
    print(repr(data[i:i+420]))
    i += 1
# Also search for the common BigWorld filename strings
for s in [b"loginapp.pubkey", b"pubkey", b".pubkey", b"server/", b"loginApp", b"login_app", b"baseApp", b"BaseApp", b"login key", b"encryptionKey"]:
    j = data.find(s)
    if j >= 0:
        print(s, "->", hex(j), repr(data[j-20:j+40]))
