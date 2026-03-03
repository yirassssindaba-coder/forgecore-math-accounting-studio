# ForgeCore Math & Accounting Studio

Desktop app (Python + Tkinter) untuk **nuansa menghitung**:  
✅ **Super Calculator** (rumus matematika + akuntansi)  
✅ **Quiz Arena** (1000 soal dari PDF yang kamu lampirkan, lengkap dengan kunci)  
✅ **Learning Hub** (3 PDF bawaan bisa dibuka & di-export)  
✅ **Music & Focus** (playlist URL + metronome BPM untuk fokus)

---

## Fitur Utama

- **Quiz 1000 Soal (Matematika + Akuntansi)**
  - Pilih subject: Matematika / Akuntansi / Campur
  - Pilih jumlah soal & menit
  - Opsi **Hide mastered** (soal yang sudah benar tidak dimunculkan lagi)
  - Feedback langsung + hint dari kunci jawaban

- **Super Calculator**
  - Formula library (kategori: Calculus, Statistik, Probabilitas, Linear Algebra, CVP, Ratios, NPV, Audit Risk, dll)
  - Input dinamis per formula
  - Output + steps

- **Learning Hub (PDF bawaan)**
  - `materi-matematika-akuntansi-dan-1000-soal.pdf`
  - `panduan-matematika-sains-data-lengkap.pdf`
  - `panduan-akuntansi-s1-s3-lengkap.pdf`
  - Bisa **Open** atau **Export copy** ke folder pilihanmu

- **Music & Focus**
  - Playlist URL (YouTube/Spotify/MP3 link)
  - Tombol play membuka URL dengan player default (paling stabil tanpa dependency tambahan)
  - Metronome BPM (Windows: beep)

---

## Cara Menjalankan (Windows PowerShell)

```powershell
cd .\forgecore-math-accounting-studio
python .\app.py
```

Atau:

```powershell
.\run.ps1
```

---

## Struktur Folder

- `app.py` — UI utama
- `core.py` — engine (quiz + kalkulator + state + playlist)
- `data/quiz_math_accounting_1000.json` — bank soal 1000
- `resources/*.pdf` — PDF bawaan untuk Learning Hub
- `run.ps1` / `run.bat` — shortcut run

---
