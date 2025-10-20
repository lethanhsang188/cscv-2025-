import base64
from Crypto.Cipher import AES
from pathlib import Path

key = b'thresh0ld_k3y_05'

vault_path = Path(__file__).resolve().parent.parent / "vault" / "vault.enc"
with open(vault_path, 'r') as f:
    data = base64.b64decode(f.read().strip())

iv = data[:16]
ciphertext = data[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext).rstrip(b'\x00').decode('ascii')

print(f"[+] Flag: {plaintext}")
