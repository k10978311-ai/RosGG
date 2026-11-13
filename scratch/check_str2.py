data = open(r"C:\Users\Lufy\Desktop\Server\extract\libclient.so", "rb").read()
va = 0x2a27b9d
end = data.find(b"\x00", va)
print(f"String at {hex(va)}:", data[va:end])
