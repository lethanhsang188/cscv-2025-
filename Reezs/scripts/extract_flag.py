#!/usr/bin/env python3
"""
Reverse-style extractor for CSCV2025 – ReezS
- Reads reez.exe (default: data/reez.exe)
- Uses known 32-byte target from memcpy to data_140029000
- Scans the binary for two 16-byte blocks that, when XORed with target halves,
  produce ASCII-hex → yields the 32-char flag-core
- Also supports the trivial case key == 0xAA * 32
"""
import sys, os, argparse, hashlib, binascii
from pathlib import Path
from scan_two_blocks import find_ascii_hex_32_from_two_blocks

TARGET_HEX = "9acbcf9e98c9c89dc998999b9ccf9f93cfcfcf9dcf989a999b9a98cb9d9d9d9f"

def file_hashes(p: Path):
    h_md5 = hashlib.md5()
    h_sha1 = hashlib.sha1()
    h_sha256 = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            chunk = f.read(1<<20)
            if not chunk: break
            h_md5.update(chunk)
            h_sha1.update(chunk)
            h_sha256.update(chunk)
    return h_md5.hexdigest(), h_sha1.hexdigest(), h_sha256.hexdigest()

def main():
    ap = argparse.ArgumentParser(description="Extract CSCV2025 – ReezS flag (reverse-style)")
    ap.add_argument("exe", nargs="?", default=str(Path(__file__).resolve().parents[1] / "data" / "reez.exe"),
                    help="Path to reez.exe (default: data/reez.exe)")
    ap.add_argument("--try-key-aa", action="store_true",
                    help="Also try the trivial key 0xAA*32 and print the result")
    args = ap.parse_args()

    exe_path = Path(args.exe)
    if not exe_path.exists():
        print("[-] File not found:", exe_path)
        sys.exit(1)

    md5, sha1, sha256 = file_hashes(exe_path)
    print(f"[i] reez.exe md5={{md5}} sha1={{sha1}} sha256={{sha256}}")

    target = bytes.fromhex(TARGET_HEX)
    exe = exe_path.read_bytes()

    print("[i] Scanning for two 16B blocks that yield ASCII-hex when XORed with target halves...")
    hits = find_ascii_hex_32_from_two_blocks(exe, target, window=16, radius=1024)
    if hits:
        i1, i2, cand32 = hits[0]
        flag_core = cand32.decode("ascii")
        print(f"[+] Found candidate at offsets {{i1}} & {{i2}}")
        print(f"[+] flag_core = {{flag_core}}")
        print(f"[+] FLAG = CSCV2025{{{{{flag_core}}}}}")
        key32 = bytes([a ^ b for a,b in zip(cand32, target)])
        print(f"[i] Derived key32 (hex) = {{key32.hex()}}")
    else:
        print("[-] No two-block ASCII-hex candidate found nearby.")

    if args.try_key_aa:
        print("[i] Trying key = 0xAA * 32 ...")
        key = bytes([0xAA]*32)
        flag_core_aa = bytes([t ^ k for t,k in zip(target, key)]).hex()
        print(f"[+] flag_core(AA) = {{flag_core_aa}}")
        print(f"[+] FLAG(AA) = CSCV2025{{{{{flag_core_aa}}}}}")

if __name__ == "__main__":
    main()
