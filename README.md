# 🧩 Shamir’s Secret Sharing – CSCV 2025

[![Crypto](https://img.shields.io/badge/Category-Crypto-blue)]()
[![Difficulty](https://img.shields.io/badge/Difficulty-Medium-lightgreen)]()
[![CTF](https://img.shields.io/badge/Event-CSCV2025-red)]()

---

## 📖 Challenge Overview

Reconstruct an AES key split into 5 shares using **Shamir’s Secret Sharing** and decrypt the final vault.

---

## 🧩 Shares Extracted

| File        | Method                                           | (x, y) |
|-------------|--------------------------------------------------|--------|
| share1.txt  | Plain                                            | (1, 201522632269176227792529259658745111658) |
| share2.png  | QR + Caesar(+5)                                  | (2, 224770860677244800791621415404633393675) |
| share3.bin  | RSA decrypt                                      | (3, 135324715440419453670163953081590813641) |
| share4.zip  | Unzip (pass: `ctf_2025`)                         | (4, 120473893289346312314482711088749854173) |
| share5.pdf  | Metadata → UTF-16 hex → Vigenère(key=`ctf_2025`) → Base64 | (5, 25019457618722413877035949434840599806) |

Prime modulus:
```
p = 309465533233587653298203953963739275397
```

---

## ⚙️ Step 1 – Reconstruct the AES Key

```bash
cd scripts
python3 reconstruct_key.py
```

Expected output:
```
[+] Reconstructed AES Key: thresh0ld_k3y_05
```

---

## 🔐 Step 2 – Decrypt the Vault

```bash
python3 decrypt_vault.py
```

Expected output:
```
[+] Flag: CSCV2025{Thresh0ld_c1pher_2025@?}
```

---

## 🧠 Key Concepts

- **Shamir’s Secret Sharing:** splits secret S into n shares; need k to recover.
- **Lagrange interpolation mod p:** reconstructs S = f(0).
- **AES-128-CBC:** used for final vault decryption.

---

## 🧰 Tools

- `Python 3`, `pycryptodome`
- `CyberChef`, `zbarimg`, `qpdf`
- `OpenSSL`, `base64`

---

## 🧭 Repository Layout

```
shamirs-secret-sharing/
├── shares/
│   ├── share1.txt
│   ├── share2_info.txt
│   ├── share3_info.txt
│   ├── share4_info.txt
│   └── share5_info.txt
├── scripts/
│   ├── reconstruct_key.py
│   └── decrypt_vault.py
├── vault/
│   └── vault.enc
└── README.md
```

---

## 🧠 Author
**Lê Thanh Sang (sanglt)** – Reverse & Crypto @ CSCV2025
