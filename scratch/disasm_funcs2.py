import capstone, struct

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Let's check functions: 0x985c10, 0x98d948, 0x98e73c, 0x985f54
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

funcs = [0x985c10, 0x98d948, 0x98e73c, 0x985f54, 0x985df8, 0x985cfc]
for fn in funcs:
    print(f"\n--- Disasm 0x{fn:x} ---")
    code = data[fn : fn + 48]
    for insn in cs.disasm(code, fn):
        print(f"0x{insn.address:x}: {insn.mnemonic:10s} {insn.op_str}")
