# Reconstruct first half from Java logic
key = [66, 51, 122, 33, 86]
enc = [122,86,27,22,53,35,80,77,24,98,122,7,72,21,98,114]
dec = [(enc[i] ^ key[i % len(key)]) for i in range(16)]
print(''.join(f'{b:02x}' for b in dec))  # 8ea7cac794842440
