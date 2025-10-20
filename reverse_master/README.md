# CSCV 2025 – Reverse Engineering (Android • Java + JNI + NEON)

[![Category](https://img.shields.io/badge/Category-Mobile%20RE-blue)](#)
[![Platform](https://img.shields.io/badge/Platform-Android%20ARM64-green)](#)
[![Lang](https://img.shields.io/badge/Code-Python%20%26%20Java-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](#license)

> **Goal:** Phân tích APK, vượt anti-debug/anti-frida, khôi phục flag dạng  
> `CSCV2025{<32 hex>}` = **16 hex đầu** (Java) + **16 hex sau** (JNI/NEON).

---

## Table of Contents

- [Bối cảnh & Mục tiêu](#bối-cảnh--mục-tiêu)
- [Anti-RE & Cách bypass nhanh](#anti-re--cách-bypass-nhanh)
- [Luồng kiểm tra ở Java (First Half)](#luồng-kiểm-tra-ở-java-first-half)
- [Luồng kiểm tra ở Native (Second Half)](#luồng-kiểm-tra-ở-native-second-half)
- [Giải thuật `sub_1AD68` (NEON mixer)](#giải-thuật-sub_1ad68-neon-mixer)
- [Script tái tạo kết quả](#script-tái-tạo-kết-quả)
- [Kết quả cuối & Verify](#kết-quả-cuối--verify)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Ảnh minh hoạ (tuỳ chọn)](#ảnh-minh-hoạ-tuỳ-chọn)
- [Tooling & Tips](#tooling--tips)
- [License](#license)

---

## Bối cảnh & Mục tiêu

Challenge kiểm tra flag trong Activity Android. Flag phải có format `CSCV2025{...}`. App chia chuỗi giữa dấu ngoặc nhọn thành 2 nửa:
- **Nửa 1 (16 ký tự hex)** xử lý/đối chiếu ở **Java**.
- **Nửa 2 (16 ký tự hex)** kiểm tra trong **native** (`libnative-lib.so`) qua JNI.

---

## Anti-RE & Cách bypass nhanh

App chặn màn hình chính nếu phát hiện:
- **Debuggable** (build debug),
- **Root/SU** (nhiều path + `Runtime.exec("su")`),
- **Frida** (scan process strings `frida`, `gum-js-loop`, `gmain`; thăm dò port `127.0.0.1:27042–27052`).

**Bypass nhanh**:
- Cài release build sạch hoặc **patch điều kiện hiển thị** (smali).
- Disable kiểm tra bằng frida/patch tạm ở native.
- Chạy trên thiết bị/AVD “sạch”, tắt tooling khi nhập flag.

---

## Luồng kiểm tra ở Java (First Half)

Trong `MainActivity`, khi bấm **Check**:
- Xác thực pattern `CSCV2025{...}` và dấu `}`.
- Lấy phần giữa, tách **firstHalf** = 16 ký tự đầu.
- **firstHalf** được so khớp bằng **XOR** với mảng `enc[16]` và **key** lặp chu kỳ 5 byte.

Pseudo (rút gọn):
```java
byte[] enc = {122,86,27,22,53,35,80,77,24,98,122,7,72,21,98,114};
byte[] key = {66,51,122,33,86}; // "B3z!V"
for (int i = 0; i < 16; i++) out[i] = (byte)(enc[i] ^ key[i % 5]);
String firstHalf = new String(out, StandardCharsets.UTF_8); // 8ea7cac794842440
