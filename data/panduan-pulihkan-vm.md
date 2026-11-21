# Panduan Pulihkan VM — Pusat Komando

**Dibuat:** 21 Nov 2026 (perintah Cipta "1234 eksekusi", item 2: server
selalu nyala / auto-recovery)
**Skrip:** `~/workspace/bin/pulihkan-vm.sh` (di luar repo — alat infra VM)

## Kenapa perlu

VM ini **ephemeral**: tiap restart / penggantian VM, hilang:
user sistem (kuma, valkey, grafana), unit systemd, plugin Grafana,
override ProtectHome, tunnel SSH, dan semua isi `/tmp`.
Yang **aman** (tinggal di `~/workspace`, persisten): kode + data
Pusat Komando, Uptime Kuma (kuma.db), Valkey (dump.rdb), Qdrant
(storage/), file .deb Grafana, ssh-proxy.py.

Yang **TIDAK pulih otomatis**: data Grafana (`/var/lib/grafana`
lenyap) — sandi admin kembali default `admin/admin`, datasource
"Memori Bersama" + dasbor "Bintang Command Center" harus dibuat ulang
(lihat § Setelah skrip).

## Pakai

```bash
sudo ~/workspace/bin/pulihkan-vm.sh --dry-run   # lihat rencana, tanpa ubah apa pun
sudo ~/workspace/bin/pulihkan-vm.sh             # pulihkan sungguhan
```

Semua langkah **idempotent**: aman dijalankan berulang kali; yang
sudah benar dilewati. Skrip berhenti dengan exit 1 bila ada langkah
GAGAL (lihat baris GAGAL di output). `--dry-run` selalu exit 0 bila
sintaks benar (tidak mengubah apa pun).

## Yang dipulihkan skrip (berurutan)

| # | Langkah | Cara cek sudah benar |
|---|---|---|
| 1 | User sistem `kuma` + `valkey` | `id kuma`, `id valkey` |
| 2 | Akses layanan (bukan kepemilikan): user layanan bisa baca+tulis yang dibutuhkannya | `sudo -u kuma test -w ~/workspace/uptime-kuma` |
| 3 | Izin traversal `/home/hatch` (711) bila user grafana tidak bisa baca DB memori | `sudo -u grafana test -r .../data/memori_bersama.db` |
| 4 | Grafana dari `.deb` (`~/workspace/tmp/grafana_13.3.1_amd64.deb`) | `command -v grafana-server` |
| 5 | Plugin SQLite `frser-sqlite-datasource` (dari `/usr/share/grafana`) | `[ -d /var/lib/grafana/plugins/frser-sqlite-datasource ]` |
| 6 | Override `ProtectHome=read-only` (Grafana bisa baca DB di home) | isi `/etc/systemd/system/grafana-server.service.d/allow-home-read.conf` |
| 7 | Unit systemd `uptime-kuma.service` + `valkey.service` (isi persis seperti yang sedang jalan) | bandingkan isi file |
| 8 | `daemon-reload` bila ada unit berubah; `enable` + `restart` hanya layanan yang berubah/belum aktif | `systemctl is-active grafana-server uptime-kuma valkey` |
| 9 | Qdrant via `~/workspace/qdrant/start-qdrant.sh` (sudah idempotent) | `curl http://127.0.0.1:6333/healthz` |
| 10 | Salin `~/workspace/bin/ssh-proxy.py` → `/tmp/ssh-proxy.py` | `cmp` kedua file |
| 11 | Verifikasi: Grafana 3000 (200), Kuma 3001 (302), Valkey PONG, Qdrant healthz | output skrip |

## Catatan penting

- **chown sering gagal di VM ini** ("Operation not permitted" walau
  root — workspace di mount terbatas). Skrip TIDAK memaksa chown:
  yang diuji adalah **akses** user layanan. Bila akses OK, chown
  dilewati. Bila akses gagal dan chown gagal, skrip hanya memberi
  PERINGATAN dan lanjut — layanan tetap bisa jalan bila direktorinya
  777 (seperti `uptime-kuma` saat ini).
- **Tunnel Pinggy TIDAK dibuat otomatis** oleh skrip (sengaja): VM
  baru butuh konfirmasi host key `yes` + URL baru tiap ~60 menit
  (batas tunnel gratis). Skrip mencetak langkah manualnya di akhir.
  Pola yang terbukti (21 Nov 2026): SSH **tanpa -N** (URL tercetak
  di output sesi), ProxyCommand `python3 /tmp/ssh-proxy.py %h %p`
  lewat egress proxy VM; Grafana forward port lokal 3000, Uptime
  Kuma port 3001. Perintah SSH persis mengikuti sesi terakhir yang
  berhasil — catat perintahnya dari sesi itu saat membuat tunnel baru.
- **Bila file .deb hilang** dari `~/workspace/tmp/`: unduh ulang
  `grafana_13.3.1_amd64.deb` sebelum menjalankan skrip (skrip akan
  GAGAL di langkah Grafana + plugin, tapi tetap memulihkan yang lain).

## Setelah skrip (manual, tidak bisa otomatis)

1. **Grafana:** login `admin` / `admin` (default setelah instal ulang)
   → ganti sandi admin lewat kartu aman (nilai tidak pernah ditulis).
   Buat ulang datasource "Memori Bersama" (SQLite, path
   `.../pusat-komando/data/memori_bersama.db`, `_pragma=query_only(1)`).
   Buat ulang dasbor "Bintang Command Center" (7 panel — spesifikasi
   di MEMORY.md).
2. **Tunnel Pinggy:** buat tunnel Grafana (3000) + Kuma (3001) manual,
   jawab `yes` saat host key ditanya, catat URL baru, verifikasi
   `curl` (Grafana 200, Kuma 302), beri URL ke tugas browser yang
   menunggu.
3. **Qdrant:** tidak auto-start saat VM restart — skrip ini yang
   menyalakannya. Bila butuh auto-start permanen, putuskan dulu
   (butuh unit systemd Qdrant — belum dibuat).

## Uji yang dilakukan (21 Nov 2026)

- `--dry-run`: semua langkah terdeteksi sudah benar (kecuali chown
  uptime-kuma — kemudian diubah jadi uji akses, lihat catatan di atas).
- Run sungguhan (VM sedang jalan): semua langkah LEWATI (idempotent),
  verifikasi lolos semua (Grafana 200, Kuma 302, Valkey PONG, Qdrant
  healthz OK), exit 0. **Tidak ada restart VM sungguhan dalam uji ini**
  — pemulihan pasca-restart sesungguhnya belum teruji sampai VM
  benar-benar restart; skrip dirancang untuk saat itu terjadi.
