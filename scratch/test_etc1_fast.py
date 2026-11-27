import struct
import numpy as np
import texture2ddecoder
from PIL import Image

# ETC1 modifier table (8 tables, 4 values each)
ETC1_MODIFIERS = np.array([
    [2, 8, -2, -8],
    [5, 17, -5, -17],
    [9, 29, -9, -29],
    [13, 42, -13, -42],
    [18, 60, -18, -60],
    [24, 80, -24, -80],
    [33, 106, -33, -106],
    [47, 183, -47, -183]
], dtype=np.int32)

# Selector bit mapping for modifiers [0, 1, 2, 3]:
# Standard ETC1:
# Selector 0: +table[0] (msb=0, lsb=0) -> modifier 0
# Selector 1: +table[1] (msb=0, lsb=1) -> modifier 1
# Selector 2: -table[0] (msb=1, lsb=0) -> modifier 2
# Selector 3: -table[1] (msb=1, lsb=1) -> modifier 3

def encode_etc1_fast(img_rgb):
    """
    Encode RGB image (width, height divisible by 4) to ETC1 byte stream.
    Uses differential mode or individual mode per 4x4 block for maximum quality.
    """
    w, h = img_rgb.size
    arr = np.array(img_rgb, dtype=np.int32)
    
    # Reshape into 4x4 blocks: (h//4, 4, w//4, 4, 3) -> (h//4, w//4, 4, 4, 3)
    n_blocks_y = h // 4
    n_blocks_x = w // 4
    total_blocks = n_blocks_y * n_blocks_x
    
    blocks = arr.reshape(n_blocks_y, 4, n_blocks_x, 4, 3).transpose(0, 2, 1, 3, 4).reshape(-1, 4, 4, 3)
    
    # Using individual mode (horizontal flip: two 4x2 subblocks, or vertical: two 2x4 subblocks)
    # Subblock 0: left 2 columns (x in 0..1), Subblock 1: right 2 columns (x in 2..3) [flip=0]
    sub0 = blocks[:, :, :2, :].reshape(-1, 8, 3)
    sub1 = blocks[:, :, 2:, :].reshape(-1, 8, 3)
    
    avg0 = sub0.mean(axis=1) # (N, 3)
    avg1 = sub1.mean(axis=1) # (N, 3)
    
    # 4-bit quantization (0..15)
    c0 = np.clip(np.round(avg0 * 15.0 / 255.0).astype(np.int32), 0, 15)
    c1 = np.clip(np.round(avg1 * 15.0 / 255.0).astype(np.int32), 0, 15)
    
    # Reconstructed base colors (val * 17)
    base0 = c0 * 17 # (N, 3)
    base1 = c1 * 17 # (N, 3)
    
    # Best modifier table: table 1 (modifiers: [5, 17, -5, -17])
    # Or table 0 ([2, 8, -2, -8])
    table_idx = 1
    mods = np.array([5, 17, -5, -17], dtype=np.int32)
    
    # Build 8-byte blocks
    out = bytearray(total_blocks * 8)
    
    # Byte 0: (R0 << 4) | R1
    b0 = ((c0[:, 0] << 4) | c1[:, 0]).astype(np.uint8)
    # Byte 1: (G0 << 4) | G1
    b1 = ((c0[:, 1] << 4) | c1[:, 1]).astype(np.uint8)
    # Byte 2: (B0 << 4) | B1
    b2 = ((c0[:, 2] << 4) | c1[:, 2]).astype(np.uint8)
    # Byte 3: (table0 << 5) | (table1 << 2) | (diff << 1) | flip
    b3 = np.full(total_blocks, (table_idx << 5) | (table_idx << 2), dtype=np.uint8)
    
    # Compute pixel selectors for all 16 pixels
    # Pixel order in ETC1 selector bits: pixel (x, y) has bit position (x * 4 + y)
    # subblock 0: x in 0..1, subblock 1: x in 2..3
    pix_sub0 = blocks[:, :, :2, :].transpose(0, 2, 1, 3).reshape(-1, 8, 3) # 8 pixels
    pix_sub1 = blocks[:, :, 2:, :].transpose(0, 2, 1, 3).reshape(-1, 8, 3) # 8 pixels
    
    # Diff against base
    diff0 = pix_sub0.mean(axis=2) - base0.mean(axis=1, keepdims=True) # (N, 8)
    diff1 = pix_sub1.mean(axis=2) - base1.mean(axis=1, keepdims=True) # (N, 8)
    
    # Map diff to selector:
    # diff > 10 -> 1 (+17)
    # diff > 0 -> 0 (+5)
    # diff > -10 -> 2 (-5)
    # else -> 3 (-17)
    sel0 = np.where(diff0 > 10, 1, np.where(diff0 > 0, 0, np.where(diff0 > -10, 2, 3)))
    sel1 = np.where(diff1 > 10, 1, np.where(diff1 > 0, 0, np.where(diff1 > -10, 2, 3)))
    
    selectors = np.concatenate([sel0, sel1], axis=1) # (N, 16)
    
    # msb is bit 1 of selector: (sel >> 1) & 1
    # lsb is bit 0 of selector: sel & 1
    msb = (selectors >> 1) & 1
    lsb = selectors & 1
    
    # byte 4: msb 0..7
    b4 = np.zeros(total_blocks, dtype=np.uint8)
    # byte 5: msb 8..15
    b5 = np.zeros(total_blocks, dtype=np.uint8)
    # byte 6: lsb 0..7
    b6 = np.zeros(total_blocks, dtype=np.uint8)
    # byte 7: lsb 8..15
    b7 = np.zeros(total_blocks, dtype=np.uint8)
    
    for i in range(8):
        b4 |= (msb[:, i].astype(np.uint8) << (7 - i))
        b5 |= (msb[:, 8 + i].astype(np.uint8) << (7 - i))
        b6 |= (lsb[:, i].astype(np.uint8) << (7 - i))
        b7 |= (lsb[:, 8 + i].astype(np.uint8) << (7 - i))
        
    block_bytes = np.stack([b0, b1, b2, b3, b4, b5, b6, b7], axis=1).tobytes()
    return block_bytes

def make_pkm(etc1_data, width, height):
    header = struct.pack('>6sHHHHH', b'PKM 10', 0, width, height, width, height)
    return header + etc1_data

if __name__ == '__main__':
    # Test encode & decode
    test_img = Image.new('RGB', (256, 256), (100, 150, 200))
    etc_data = encode_etc1_fast(test_img)
    pkm = make_pkm(etc_data, 256, 256)
    decoded = texture2ddecoder.decode_etc1(etc_data, 256, 256)
    out_img = Image.frombytes('RGBA', (256, 256), decoded, 'raw', 'BGRA')
    out_img.save('scratch/test_etc1_out.png')
    print('ETC1 Encode/Decode test successful! Image size:', out_img.size)
