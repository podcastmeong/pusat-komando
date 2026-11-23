# Skill: Perburuan Kubernetes & Docker — Permukaan Infrastruktur Terekspos

> **BELUM DIUJI — dibangun dari riset, bukan pengalaman teruji.** Seluruh isi di bawah ini adalah metodologi dari riset (referensi: `~/workspace/catatan/riset-tambahan-skill-bounty-2026-11-24.md` Bagian 4 kandidat 52, Claude-BugHunter `hunt-k8s`, 13 laporan terungkap), bukan pengalaman teruji sampai ada temuan yang lolos triase dan dicatat di log. Label ini berlaku untuk semua bagian.

## Pemicu (kapan dipakai)

- Program bounty in-scope secara EKSPLISIT mencantumkan aset infrastruktur (cluster Kubernetes, host Docker, IP range infrastruktur) — **tanpa pencantuman eksplisit, skill ini TIDAK dipakai.**
- Ditemukan port khas terekspos saat recon: 6443 (API server), 10250 (kubelet), 2379 (etcd), 10255 (kubelet read-only), 2375/2376 (Docker daemon), 8080/8443 (dashboard).
- Ditemukan dashboard Kubernetes dengan opsi skip-login atau service account token yang bocor.

## Pemilik + penanggung jawab

| Peran | Agent | Tugas |
|---|---|---|
| Pengerjaan | **A62** | Menjalankan fingerprinting + pengujian akses anonim infrastruktur |
| Audit | **A60 Security Auditor** | Memeriksa apakah bukti tiap temuan memenuhi gerbang validasi |
| Pemimpin | **Muse** | Memutuskan temuan mana yang maju ke triase |

## Sudah tercakup (jangan diduplikat)

- Enumerasi aset cloud (bucket S3/GCS/Azure terbuka) → skill `enumerasi-aset-cloud`. Skill ini soal cluster/container runtime, bukan bucket penyimpanan.
- Pemindaian port & layanan non-standar → skill `pemindaian-port-layanan`. Skill ini memakai hasil pemindaian itu sebagai input, lalu menguji permukaan K8s/Docker spesifik.
- Rantai pasok CI/CD → skill `recon-rantai-pasok-cicd`. Skill ini tidak membahas pipeline CI/CD, hanya runtime cluster/container yang terekspos.

## Aturan keras

1. **Hanya program bounty resmi in-scope DAN aset infrastruktur tercantum eksplisit.** Bila program hanya mencantumkan aplikasi web, JANGAN sentuh port infrastruktur — itu di luar scope.
2. **Hanya akun sendiri + canary palsu.** Gunakan hanya data uji milik sendiri; jangan membaca secret/token milik workload lain.
3. **Tanpa data orang lain.** Secret, token service account, dan data etcd milik workload lain TIDAK BOLEH dibaca, disalin, atau dilampirkan — cukup buktikan akses anonim ke endpoint-nya (mis. respons 200 pada `/api/v1/namespaces` tanpa auth) lalu STOP.
4. **Tanpa uji korban (victim-agent fraud tests DIBLOKIR — jangan dicoba).**
5. **Tanpa DoS / resource exhaustion** — dilarang membuat pod/container, menghapus workload, atau menghabiskan resource cluster.
6. **Tanpa payload di permukaan publik.**
7. **Validasi human-in-the-loop (AI bantu, manusia putuskan dan validasi).**
8. **Tanpa laporan tanpa persetujuan Cipta.**
9. **Patuhi larangan otomasi program (huntr "Humans only"; Gray Swan dilewati total — jangan buat skill untuknya).**
10. **Larang aksi destruktif (DROP, DELETE, hapus/ubah data)** — pembuktian harus aman dan read-only. **DILARANG KERAS:** membuat/menghapus pod, menjalankan perintah di container (`exec`), membaca secret, atau escape ke host via docker.sock. Pembuktian berhenti di: endpoint merespons tanpa autentikasi + daftar resource yang TERLIHAT (nama saja, tanpa isi secret).
11. **Jangan menjalankan exploit escape host.** Bukti "docker.sock terekspos" cukup berupa: socket merespons API Docker tanpa auth (mis. `GET /version` mengembalikan versi). JANGAN membuat container dengan mount host.

## Langkah + gerbang

### Gerbang 1 — Fingerprinting permukaan (pasif + satu request per endpoint)

Petakan apa yang terekspos sebelum menguji. Standar lulus: tiap port/endpoint tercatat "terbuka + respons" atau "tertutup" dengan bukti.

| Port / endpoint | Yang diperiksa |
|---|---|
| 6443 Kubernetes API | `GET /version`, `GET /api/v1/namespaces` tanpa auth — 401/403 = aman; 200 = kandidat |
| 10250 kubelet | `GET /pods`, `GET /runningpods` tanpa auth |
| 2379 etcd | `GET /version`, `GET /v2/keys/` tanpa auth |
| 2375/2376 Docker daemon | `GET /version` tanpa TLS/auth |
| Dashboard (8080/8443) | Opsi skip-login tersedia? Login anonim masuk? |
| 10255 kubelet read-only | `GET /pods` (read-only, tetap sensitif) |

Gunakan `curl -k --max-time 5` satu request per endpoint; jangan memindai agresif (lihat `pacing-request-aman`).

### Gerbang 2 — Pengujian akses anonim (read-only, tanpa isi secret)

Untuk tiap endpoint yang merespons 200 tanpa auth, buktikan SATU hal: endpoint itu mengembalikan data tanpa autentikasi. Ambil bukti minimal:

- **API server anonim:** daftar namespace/pod (NAMA saja). JANGAN ambil isi secret/configmap.
- **Kubelet anonim:** daftar pod yang berjalan di node (nama + namespace). JANGAN pakai endpoint `/exec` atau `/run` — itu eksekusi perintah, DILARANG.
- **etcd anonim:** tunjukkan `GET /v2/keys/` merespons (bukti akses). JANGAN membaca nilai key yang berisi kredensial.
- **Docker daemon anonim:** `GET /version` + `GET /containers/json` (daftar container). JANGAN membuat/menghapus container.
- **Dashboard skip-login:** masuk sebagai anonim, tangkap screenshot daftar workload. JANGAN mengubah apa pun.

### Gerbang 3 — Penilaian RBAC & service account (tanpa penyalahgunaan)

Bila ditemukan token service account yang bocor di tempat PUBLIK (mis. di repo publik, di respons API in-scope — bukan dari membaca secret cluster):

1. Periksa scope token itu terhadap API server in-scope dengan SATU request baca (`GET /api/v1/namespaces`).
2. Catat peran yang melekat (read-only vs cluster-admin) dari respons error/sukses — JANGAN memakai token itu untuk menulis/menghapus.
3. Bila token itu berasal dari membaca secret cluster = pelanggaran Aturan keras 3 — HAPUS dari log dan laporkan pelanggaran ke Muse, jangan jadikan temuan.

### Gerbang 4 — Gerbang validasi laporan

1. **Dampak keamanan nyata:** Valid = endpoint infrastruktur merespons tanpa auth + data yang terlihat (daftar workload/namespace) terbukti. **TOLAK** = sekadar "port terbuka" tanpa respons bermakna (lihat `gerbang-sinyal-dampak`).
2. **Reproduksibilitas:** ulangi request minimal 2×; simpan respons mentah (dengan isi secret disensor/dihapus).
3. **Higienitas bukti:** sensor SEMUA token, secret, dan nama workload internal yang tidak relevan sebelum dilampirkan (`[REDACTED]`).

Hanya temuan yang lolos keempat gerbang yang diteruskan ke `penilaian-cvss` → `artikulasi-dampak-bisnis` → `triase-duplikat` → `laporan-poc-otomatis` → audit A60 → tinjau manusia 2–3 menit → persetujuan Cipta → kirim.

## Alat

| Alat | Cara pakai |
|---|---|
| `curl -k --max-time 5` | Satu request per endpoint; baca respons tanpa auth |
| `kubectl --insecure-skip-tls-verify` (read-only) | HANYA `get` (namespace/pod) bila API anonim merespons; JANGAN `exec`/`delete`/`apply` |
| `nmap` / `pemindaian-port-layanan` | Pemetaan port awal (sudah tercakup — pakai hasilnya) |
| `~/workspace/catatan/log-bug-bounty.md` | Log endpoint yang diperiksa + keputusan gerbang |

## Format output

Tulis ke `~/workspace/catatan/log-bug-bounty.md` (bagian per tanggal) dengan format:

```
Target: [program + aset infrastruktur in-scope]
Permukaan: [port/endpoint + respons tanpa auth]
Pembuktian: [apa yang terlihat (nama saja) + bukti respons]
Keputusan gerbang: [lolos / ditolak + alasan]
Status: [dipetakan / diuji / terbukti / dilaporkan / ditolak]
```

Format judul laporan (bila maju): `[Aset Infrastruktur] - [Komponen: API Server / kubelet / etcd / Docker] tanpa autentikasi menyebabkan [Dampak Spesifik]`.

## Batasan yang diketahui

- Metodologi ini dari riset (Claude-BugHunter `hunt-k8s`, 13 laporan), bukan pengalaman teruji — tiap komponen butuh satu kasus nyata yang lolos triase sebelum label BELUM DIUJI dicabut.
- **Skill ini HANYA dipakai bila program in-scope secara eksplisit mencakup aset infrastruktur.** Program web biasa yang tidak mencantumkan infrastruktur = JANGAN dipakai, sekalipun port-nya terlihat terbuka dari internet.
- Pembuktian sengaja dibatasi read-only: dampak penuh (RCE via kubelet exec, escape via docker.sock) TIDAK dibuktikan live — jelaskan sebagai dampak potensial di laporan dengan merujuk dokumentasi publik, bukan dengan eksekusi.
- Cluster yang terekspos sering honeypot — verifikasi bahwa aset itu benar milik program in-scope (cocokkan IP/domain dengan scope) sebelum menguji.
