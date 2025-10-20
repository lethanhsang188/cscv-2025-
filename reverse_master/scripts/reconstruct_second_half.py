# Reconstruct second half according to sub_1AD68 NEON-like logic

def u8(x): return x & 0xFF

# Constants from sub_1AD68
v24 = 99     # 'c'
v25 = 125    # '}'
v26 = -30    # -> 226
v27 = 20
v28 = -72    # -> 184

# v22 (5 bytes): *(DWORD*)v22 = -1206590851; *(v22+4) = 99
val = (-1206590851) & 0xFFFFFFFF
v41 = (val     ) & 0xFF
v40 = (val >> 8) & 0xFF
v42 = (val >>16) & 0xFF
v43 = (val >>24) & 0xFF
v44 = 99

v35 = u8(v26)          # 226
v36 = u8(v27 | 1)      # 21

# v37[0..7]
v37 = [0]*8
v37[0] = u8(v25 ^ 4)
v37[1] = u8(v26 | 5)
v37[2] = u8(v27 ^ 6)
v38_32 = ((v24 ^ 3) ^ 0x77777777) - 19
v38 = u8(v38_32)
v37[3] = u8(v28 | 7)
v37[4] = u8(v24 | 8)
v37[5] = u8(v25 ^ 9)
v37[6] = u8(v26 ^ 0xA)
v37[7] = u8(v27 | 0xB)

v39 = u8(v24 ^ 0xD)

# v23 (16 bytes) table
v23 = [0]*16
v23[0] = v41; v23[1] = v40; v23[2] = v42; v23[3] = v43; v23[4] = v44
v23[8] = v41; v23[9] = v40; v23[10] = v42; v23[11] = v43; v23[12] = v44

def add_s8(a,b):
    def i8(t): return t if t < 128 else t - 256
    return [u8(i8(x)+i8(y)) for x,y in zip(a,b)]

def eor_s8(a,b): return [x ^ y for x,y in zip(a,b)]

def vqtbl1_s8(table16, idx8):
    return [table16[i] if i < 16 else 0 for i in idx8]

def imm64_le(x):
    x &= 0xFFFFFFFFFFFFFFFF
    return [(x>>(8*i)) & 0xFF for i in range(8)]

# immediates
C1  = 6046115782741346120
C2  = (-3037436198342301718) & 0xFFFFFFFFFFFFFFFF
C3  = 867798387104613893
IDX = 144396680282898688

c1  = imm64_le(C1)
c2  = imm64_le(C2)
c3  = imm64_le(C3)
idx = imm64_le(IDX)

t1  = eor_s8(v37, c1)
t2  = add_s8(t1, c2)
t3  = eor_s8(t2, c3)
tbl = vqtbl1_s8(v23, idx)
t4  = eor_s8(t3, tbl)

v4 = [0]*16
v4[0]  = u8(((v25 ^ 0x2F) - 7) ^ v41)
v4[1]  = u8(((v35 ^ 0x6C) - 10) ^ v40)
v4[2]  = u8(((v36 ^ 0x95) - 13) ^ v42 ^ 2)
v4[3]  = u8((((u8(v28) | 2) ^ 0x21) - 16) ^ v43)
v4[4]  = u8(v38 ^ v44 ^ 4)
for i in range(8): v4[5+i] = t4[i]
v4[13] = u8(((u8(v28) ^ 8) - 46) ^ v43 ^ 0xD)
v4[14] = u8(((v39 ^ 0x57) - 49) ^ v44 ^ 0xE)
v4[15] = u8(((v25 ^ 7) - 52) ^ v41 ^ 0xF)

as_ascii = ''.join(chr(b) for b in v4)
print(as_ascii)  # 6fe3ccc3cf2197e4
