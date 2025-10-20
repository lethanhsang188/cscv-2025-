#!/usr/bin/env python3
import sys

HEX = b"0123456789abcdef"

def is_ascii_hex(bs: bytes) -> bool:
    return all(c in HEX for c in bs)

def find_ascii_hex_32_from_two_blocks(exe: bytes, target: bytes, window=16, radius=512):
    assert len(target) == 32
    t1, t2 = target[:16], target[16:]
    hits = []
    n = len(exe)
    # First half candidates
    first = []
    for i in range(0, n - window + 1):
        k1 = exe[i:i+window]
        cand1 = bytes([a ^ b for a,b in zip(k1, t1)])
        if is_ascii_hex(cand1):
            first.append((i, cand1))
    # For each first half, try nearby for second half
    for i, cand1 in first:
        jmin = max(0, i - radius)
        jmax = min(n - window, i + radius)
        for j in range(jmin, jmax+1):
            k2 = exe[j:j+window]
            cand2 = bytes([a ^ b for a,b in zip(k2, t2)])
            if is_ascii_hex(cand2):
                hits.append((i, j, cand1 + cand2))
    return hits

if __name__ == "__main__":
    print("This module is intended to be imported by extract_flag.py")
