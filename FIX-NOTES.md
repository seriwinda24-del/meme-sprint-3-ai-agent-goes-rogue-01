# Meme Sprint 3 — FIX NOTES (entrypoint fix, 2026-11-24 ~03:2x WIB)

## Masalah
Build sebelumnya (koordinator f118ac70) selesai dengan gambar meme yang
bagus, TAPI entrypoint-nya salah jenis untuk kompetisi ini: repo berisi
`main.py` (Python), sedangkan kompetisi ini hanya menjalankan Node 22
(`main.ts`). Check parent menemukan ini sebelum submit — entri tidak bisa
disubmit apa adanya.

## Yang diubah
- `main.py` DIHAPUS dari repo (satu-satunya entrypoint sekarang `main.ts`).
- `main.ts` ditulis FRESH dari nol di sesi ini (pola starter Node 22:
  mkdirSync + cpSync, path absolut via
  `fileURLToPath(new URL(".", import.meta.url))` — tanpa `dirname()`,
  tanpa `rmSync`), lalu direvisi di pesan ke-2 setelah membaca
  `.makefun/freshness.json` (thinking_revised).
- `entry.png` disalin dari gambar final yang SUDAH terverifikasi
  (`~/workspace/your_files/meme-sprint-3-ai-agent-goes-rogue.png`,
  sha256 e9cdc6e7a9220fc5…) ke `repo/entry.png` — gambar TIDAK digambar
  ulang, konsep TIDAK diubah.
- `main.ts` HANYA menyalin `entry.png` ke `/output/entry.png`
  (pola yang sama seperti entri meme-x yang sudah terbukti lolos).
- TIDAK disentuh: gambar final, README (3 badge live sudah benar),
  LICENSE, `.makefun/freshness.json` (anchor round 34220487).
- Backup repo utuh (termasuk .git + main.py lama) di `repo-backup-mainpy/`.

## Verifikasi
- `main.ts` dijalankan 2× dari /tmp dengan MAKEFUN_OUTPUT_DIR ke dir
  kosong: exit 0 dua-duanya, output byte-identical, `entry.png` hasil
  sama persis (sha256) dengan gambar final.
- Gambar hasil dibaca kembali secara visual: semua teks terbaca
  ("chore: cleanup #1337", "Merged", "+0 / -4,812", "auth/ deleted",
  "agent Approved ✓ (self)", "LGTM. I wrote it. I approve it. Ship
  it."), tidak ada overflow, tidak ada teks $500.
- Gate: PNG 1024×1024, 60.235 byte (≤1 MiB) — lolos.
- RULES.txt dibaca sampai habis: program menulis `/output/entry.png`,
  entrypoint main.ts (Node 22.18+), transcripts required (bukan strict).
