---
name: email-verification-status
description: Menghasilkan status akhir — mengembalikan status verifikasi terstruktur.
---

# email-verification-status

Menghasilkan status akhir — mengembalikan status verifikasi terstruktur.

Menghasilkan status akhir verifikasi email dalam bentuk terstruktur.

Cara pakai: kembalikan objek status: email, email_valid, otp_sent, otp_received, otp_verified, dan status akhir. Status akhir hanya salah satu dari: VERIFIED, PENDING, INVALID, EXPIRED, atau FAILED.

Verifikasi: isi tiap field sesuai fakta yang sudah diperiksa (jangan isi true untuk langkah yang belum terkonfirmasi).

---
Bagian dari EMAIL OTP VERIFICATION PRO (Cipta, 25 Nov 2026).
