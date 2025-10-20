import base64
from Crypto.Cipher import AES

def lagrange_interpolation(shares, prime):
    secret = 0
    k = len(shares)
    for i in range(k):
        xi, yi = shares[i]
        num, den = 1, 1
        for j in range(k):
            if i != j:
                xj, _ = shares[j]
                num = (num * (0 - xj)) % prime
                den = (den * (xi - xj)) % prime
        inv = pow(den, prime - 2, prime)
        secret = (secret + yi * num * inv) % prime
    return secret

# Shares recovered
shares_data = [
    (1, 201522632269176227792529259658745111658),
    (2, 224770860677244800791621415404633393675),
    (3, 135324715440419453670163953081590813641),
    (4, 120473893289346312314482711088749854173),
    (5, 25019457618722413877035949434840599806)
]

prime = 309465533233587653298203953963739275397

secret = lagrange_interpolation(shares_data, prime)
secret_hex = hex(secret)[2:]
if len(secret_hex) % 2:
    secret_hex = '0' + secret_hex

key = bytes.fromhex(secret_hex)
print(f"[+] Reconstructed AES Key: {key.decode('ascii')}")
