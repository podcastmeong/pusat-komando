---
name: validate-email
description: Mengecek format dan domain email — validasi sintaks dan MX record.
---

# validate-email

Mengecek format dan domain email — validasi sintaks dan MX record.

Memvalidasi alamat email sebelum dipakai.

Cara pakai: periksa sintaks (format user@domain), lalu periksa domain dan MX record bila tersedia (lewat terminal: dig MX / nslookup). Tolak format yang tidak valid.

Verifikasi: email dinyatakan valid hanya bila format benar dan domainnya punya MX record (atau domain dikenal). Jangan lanjut kirim OTP ke alamat yang tidak valid.

---
Bagian dari EMAIL OTP VERIFICATION PRO (Cipta, 25 Nov 2026).
