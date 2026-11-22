# Panduan Master Database — Pusat Komando 10.0 (Tahap 1 Foundation)

Dibuat 22 Nov 2026 (perintah Cipta: "Iya" — mulai Tahap 1).
Sumber rancangan: Blueprint Pusat Komando 10.0 + Audit 40 Agent (ChatGPT).
File: `agents/master_database.py` — database: `data/master_database.db` (SQLite).

## 1. Apa itu Master Database

Satu sumber data untuk semua agent. Sebelum ini informasi tersebar di
`data/agents.json`, `data/crm.json`, `data/progres.json`, `data/handoff.json`,
`data/koordinasi.json`, dan memori bersama. Sekarang 12 tabel dalam satu
database SQLite — semua agent membaca dan menulis di sini.

**File database TIDAK di-commit ke Git** (seperti `memori_bersama.db`).
Bangun ulang kapan saja:

```bash
cd <repo pusat-komando>
python agents/master_database.py
```

Perintah itu menghapus database lama dan membangun ulang dari sumber
(`data/agents.json` + `data/crm.json` + seed terverifikasi di dalam modul).
Verifikasi jalan otomatis: 40 agent, status tugas valid, semua tugas
punya proyek.

## 2. 12 tabel

| Tabel | Isi | Jumlah awal |
|---|---|---|
| AGENTS | Identitas 40 agent (kode, jabatan, divisi, jobdesk, skill) | 40 |
| DIVISIONS | 6 divisi + 1 kelompok Pendukung | 7 |
| TASKS | Daftar pekerjaan (lihat §3) | 8 |
| PROJECTS | Daftar proyek | 3 |
| WORKFLOWS | Alur otomatisasi / cron | 9 |
| INTELLIGENCE | 15 sistem Intelligence (I01–I15) | 15 |
| PRODUCTS | Produk yang dibuat / dijual | 10 |
| CUSTOMERS | Prospek dan pelanggan (dari CRM) | 48 |
| FINANCE | Pemasukan dan pengeluaran | 0 (belum ada transaksi) |
| APPROVALS | Riwayat persetujuan Cipta | 7 |
| PERFORMANCE | KPI per agent | 40 (nilai NULL = belum diukur) |
| AUDIT_LOGS | Riwayat aktivitas | 1 |

## 3. ID dan status tugas

- ID tugas: `TASK-0001`, `TASK-0002`, … (tambah berurutan).
- ID proyek: `PROJECT-001`, `PROJECT-002`, …
- Status tugas — 9 nilai, WAJIB seragam (dipaksa CHECK constraint):

| Status | Arti |
|---|---|
| BACKLOG | Belum dimulai |
| READY | Siap dikerjakan |
| IN_PROGRESS | Sedang dikerjakan |
| REVIEW | Menunggu pemeriksaan QC |
| REVISION | Perlu diperbaiki |
| PENDING_APPROVAL | Menunggu persetujuan Cipta |
| APPROVED | Sudah disetujui |
| PUBLISHED | Sudah diterbitkan |
| FAILED | Gagal dan perlu ditangani |

**Aturan keras:** agent TIDAK BOLEH mengubah status jadi APPROVED atau
PUBLISHED sendiri. Persetujuan hanya dari Cipta (`approved_by`).

## 4. Cara pakai (contoh query)

```bash
sqlite3 data/master_database.db
```

```sql
-- Tugas terbuka per agent
SELECT task_id, task_name, status FROM TASKS WHERE status NOT IN ('APPROVED','PUBLISHED','FAILED');

-- Produk yang sudah live
SELECT name, marketplace, price_usd FROM PRODUCTS WHERE status='PUBLISHED';

-- Saldo keuangan (saat ini 0 — belum ada transaksi)
SELECT type, SUM(amount) FROM FINANCE GROUP BY type;

-- Persetujuan Cipta
SELECT id, item, decided_at FROM APPROVALS ORDER BY decided_at;
```

Dari Python:

```python
from agents.master_database import build, verify
counts = build()      # bangun ulang + seed
print(verify())       # {'counts': {...}, 'problems': []}
```

## 5. SOP komunikasi antar-agent (ringkas)

Satu standar pesan (format JSON) untuk handoff antar-agent:

```json
{
  "message_id": "MSG-0001",
  "from": "A06", "to": "A08",
  "type": "TASK_HANDOFF",
  "project_id": "PROJECT-001", "task_id": "TASK-0001",
  "payload": {"topic": "Peluang produk digital", "finding": "Kebutuhan template bisnis"},
  "status": "READY", "requires_approval": false
}
```

Setiap pesan wajib punya: ID pesan, pengirim, penerima, ID proyek dan
tugas, isi pekerjaan, status, dan apakah butuh persetujuan.

**Alur konten (dari Audit, diadopsi 22 Nov 2026)** — supaya A11/A19/A33/A36
tidak tabrakan pada satu proyek:
A33 (strategi & peluang konten) → A19 (konsep & paket konten) →
A11 (produksi video) → A36 (copywriting) → A38 (QA akhir).

**Alur koordinasi (11 langkah):** 1) Muse terima target dari Cipta;
2) A03 pecah jadi tugas; 3) I01 tentukan pembagian kerja; 4) agent
kerjakan tugasnya; 5) hasil masuk database; 6) A04 + I08 evaluasi;
7) yang lolos diteruskan; 8) bila butuh tindakan eksternal, masuk
Approval Center; 9) Cipta putuskan; 10) agent pelaksana jalankan yang
disetujui; 11) I07 + I11 ukur hasilnya.

**Bila gagal:** catat pesan error, simpan hasil sementara, coba ulang
maksimal 3x untuk error yang aman diulang, lalu lapor ke Muse. Untuk
upload, pembayaran, dan email keluar: JANGAN coba ulang otomatis tanpa
cek status — cegah transaksi/publikasi ganda.

## 6. Yang sudah ada vs yang masih rencana

Sudah jalan di sistem (bukan klaim kosong): memori bersama SQLite
(I09 Memory), Qdrant, dashboard 5 tab, cron pemicu jadwal, aturan
persetujuan, papan handoff/koordinasi, modul akuntansi, CRM 48 kontak.

Masih RENCANA (status di tabel INTELLIGENCE): I01–I15 sebagai sistem
terpisah. Sebagian fungsinya sudah dijalankan agent yang ada
(mis. I08 Quality = A04 + A38; I11 Revenue = A29 + A05) — Tahap 2 yang
memformalkan mereka jadi sistem.

## 7. Langkah berikut (Tahap 1 lanjutan)

1. Tab dashboard "Master Database" di `app.py` (baca langsung dari
   database ini) — supaya Cipta bisa melihat tugas/produk/keuangan
   tanpa membuka file.
2. Isi PERFORMANCE dengan KPI nyata per agent (pengukuran dimulai
   dari laporan harian yang sudah ada).
3. Salinan Google Sheets (opsional, bila Cipta mau melihat dari HP
   tanpa membuka dashboard) — bukan pengganti database ini.

## 8. Aturan keamanan

- Tidak ada password/kredensial di database ini.
- Akses minimum yang diperlukan; catat siapa mengubah data
  (AUDIT_LOGS).
- Pisahkan draf dan tindakan nyata; simpan bukti persetujuan
  (APPROVALS).
- Backup `data/` secara berkala (lihat `agents/backup.py`).
