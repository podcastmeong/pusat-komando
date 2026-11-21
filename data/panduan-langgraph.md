# Panduan LangGraph Orchestrator — Pusat Komando 4.0

Dibuat 21 Nov 2026 (perintah Cipta: "Pasang aja biar bisa mikir
sendiri... bisa initiative"). LangGraph 1.2.24 + langchain-core 1.8.4
di venv-pk (`~/workspace/tmp/venv-pk`).

## Apa ini

Graf pikir–aksi (ReAct) per agen: LLM memutuskan langkah berikutnya
berdasarkan tugas + hasil sejauh ini, lalu menjalankan SATU alat,
lalu menilai lagi — sampai tugas selesai atau batas langkah tercapai.
Modul: `agents/langgraph_orchestrator.py`.

Node graf:

| Node | Kerja |
|---|---|
| `pikir` | Tanya LLM lewat `llm_router` (kelas "berat" = Gemini free tier). Jawaban WAJIB JSON: `{"aksi": ..., "argumen": {...}, "alasan": ...}` atau `{"selesai": true, "hasil": ...}`. Bila LLM gagal / bukan JSON (2 percobaan) → graf GAGAL TERSTRUKTUR, bukan mengarang. |
| `aksi` | Jalankan SATU alat HANYA lewat Tool Registry. Pra-cek kata terlarang + alat tidak dikenal (lapis 1); registry cek izin fail-closed (lapis 2). |
| `cek` | Routing: selesai / batas langkah → END, lanjut → `pikir`. |

## Pagar pengaman (jangan dilanggar)

- **DRAF-only.** Semua output untuk persetujuan Cipta. Graf TIDAK
  BISA kirim/bayar/publikasi/submit/upload/hapus — alat seperti itu
  tidak ada di registry dan ditolak dua lapis.
- **Batas langkah: maks 10 per tugas** (anti loop tak berujung).
- **Semua langkah tercatat** ke memori bersama (`riwayat_tugas` +
  `langgraph_hasil`).
- **LLM hanya boleh pakai alat yang diizinkan** untuk agen itu
  (registry `cek_izin`); `panggil_llm` dan `catat_tugas` tidak
  ditawarkan ke LLM (dipakai orchestrator sendiri).

## Cara menjalankan (satu agen, satu tugas)

```bash
cd ~/workspace/your_files/oyen-podcast/pusat-komando
# Bukti A09 (riset 3 harga kompetitor, baca + catat saja):
PK_NO_LOG=1 ~/workspace/tmp/venv-pk/bin/python \
  -m agents.langgraph_orchestrator --contoh-a09

# Tugas bebas untuk satu agen:
PK_NO_LOG=1 ~/workspace/tmp/venv-pk/bin/python \
  -m agents.langgraph_orchestrator --agen A09 \
  --tugas "riset 3 harga kompetitor jasa video promo" \
  --maks-langkah 10
```

Dari Python:

```python
import sys
sys.path.insert(0, "agents")
from langgraph_orchestrator import jalankan_tugas_agen
hasil = jalankan_tugas_agen("A09", "riset 3 harga kompetitor jasa video promo")
# hasil: {"ok": True/False, "status": "selesai"/"gagal"/"batas_langkah",
#         "langkah": [...], "hasil_akhir": ..., "error": ...}
```

Catatan lingkungan (terbukti 21 Nov 2026):
- **Probe/import modul: env bersih tanpa proxy**
  (`env -i PATH="$PATH" HOME="$HOME"`).
- **Jalankan graf (panggilan LLM live): pakai env shell biasa
  (dengan proxy)** — dengan `env -i`, jalur Gemini gagal total
  (secure storage helper butuh env runtime). Ini temuan, bukan
  alasan berhenti — lihat "Masalah yang ditemukan".
- Semua probe memakai `PK_NO_LOG=1`; run nyata TIDAK BOLEH pakai
  `PK_NO_LOG=1`.

## Cara menambah agen lain nanti

1. Pastikan agen itu punya handler/izin alat di `tool_registry.py`
   (jangan ubah DAFTAR_TERLARANG).
2. Panggil `jalankan_tugas_agen("Axx", "<tugas baca-saja dulu>")`.
3. Uji dulu dengan tugas baca + catat (seperti bukti A09). Agen
   dengan alat tulis (`tulis_file`/`tulis_json`/`simpan_crm`) baru
   dipakai setelah bukti baca-saja lolos.
4. Urutan saran: A06 (riset pasar) → A10 (validasi produk) →
   A07 (tren) → A25 (baca CRM saja) → lainnya. A28/A25 dengan
   aksi kirim TETAP DRAF-only.

## Hasil tes sandbox (21 Nov 2026)

9/9 lulus: import OK (1); end-to-end A09 selesai sendiri 2 langkah
dengan data nyata (1); tugas terlarang tidak mengirim apa pun,
berhenti sendiri 4 langkah (1); penolakan alat terlarang
(kirim_email, hapus_data, bayar, publikasi_video) + alat tidak
dikenal (5); hasil tercatat di memori_bersama (1).

## Masalah yang ditemukan (untuk ditangani belakangan)

1. **LLM kadang tidak mengembalikan JSON** (teks penjelasan) —
   diatasi sementara dengan retry 1x + penegasan "balas HANYA JSON".
   Bila sering kambuh: perketat prompt / pakai mode JSON bila
   gateway mendukung.
2. **Jalur Gemini gagal total di env bersih (`env -i`)** — secure
   storage helper butuh env runtime. Run live harus pakai env
   shell biasa (dengan proxy). Perlu diputuskan: aturan env mana
   yang berlaku untuk run LangGraph.
3. **LLM tidak tahu nilai kategori persis** di database harga
   kompetitor (`jasa_video_promo_desain`, bukan "video promo") —
   diatasi dengan daftar kategori dinamis di prompt. Pola yang
   sama mungkin dibutuhkan untuk alat lain yang memakai filter
   nilai persis.
4. **LLM mengulang baca yang sama** (tugas terlarang: 4x `baca_crm`
   identik sebelum menyerah) — boros panggilan. Perlu aturan
   "jangan ulangi alat + argumen yang sama" di prompt / node cek.
5. **Rekaman contoh (`contoh:video-promo-15dtk`, "Studio Contoh")
   di memori ikut dibaca sebagai harga nyata** — sebaiknya ditandai
   contoh atau dihapus dari data riset.
6. **Versi LangGraph** tidak ada di `langgraph.__version__` (1.x) —
   dipakai `importlib.metadata` sebagai gantinya.
