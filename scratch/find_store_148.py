import struct, capstone

so_path = r"C:\Users\Lufy\Desktop\Server\extract\libclient.so"
with open(so_path, "rb") as f:
    data = f.read()

# Search for STR X..., [X..., #0x148]
# STR (immediate, 64-bit):
# [31:22] = 1111100101 (0x3e5) -> 0xF9400000 | (imm12 << 10) | (Rn << 5) | Rt
# imm12 for offset 0x148: 0x148 / 8 = 0x29 = 41
target_imm = 0x29
cs = capstone.Cs(capstone.CS_ARCH_ARM64, capstone.CS_MODE_ARM)

for pc in range(0, 0x2a00000, 4):
    insn = struct.unpack_from("<I", data, pc)[0]
    if (insn & 0xFFC00000) == 0xF9000000:
        imm12 = (insn >> 10) & 0xFFF
        if imm12 == target_imm:
            # disasm this instruction
            for i in cs.disasm(data[pc:pc+4], pc):
                print(f"0x{pc:x}: {i.mnemonic} {i.op_str}")
