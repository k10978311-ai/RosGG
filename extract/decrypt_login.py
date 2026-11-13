import subprocess, os
base = r"C:\Users\Lufy\Desktop\Server"
pkt = open(base + r"\gate_capture.bin", "rb").read()[:145]
print("packet len", len(pkt), "hex head", pkt[:16].hex())
# RSA-1024 ciphertext is the 128 bytes before the 2-byte trailer
block = pkt[-130:-2]
print("rsa block len", len(block))
open(base + r"\extract\block.bin", "wb").write(block)

priv = base + r"\server_keys\loginapp_priv.pem"
for pad in ("pkcs1", "oaep", "none"):
    try:
        out = subprocess.run(
            ["openssl", "pkeyutl", "-decrypt", "-inkey", priv,
             "-in", base + r"\extract\block.bin", "-pkeyopt", f"rsa_padding_mode:{pad}"],
            capture_output=True)
        if out.returncode == 0:
            data = out.stdout
            print(f"\n=== padding={pad} OK, {len(data)} bytes ===")
            print("hex:", data.hex())
            print("repr:", data)
        else:
            print(f"padding={pad} FAIL: {out.stderr.decode(errors='replace').strip()[:120]}")
    except FileNotFoundError:
        print("openssl not found on PATH")
        break
