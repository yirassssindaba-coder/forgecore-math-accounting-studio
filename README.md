<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=210&color=0:111827,50:1d4ed8,100:14b8a6&text=ForgeCore%20Math%20%26%20Accounting%20Studio&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Nuansa%20menghitung%20dengan%20kalkulator%2C%20quiz%2C%20materi%2C%20dan%20focus%20music&descAlignY=58" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=700&color=60A5FA&center=true&vCenter=true&width=980&lines=Desktop+app+Python+untuk+belajar+matematika+dan+akuntansi+dalam+satu+workspace;Super+Calculator+dengan+rumus+inti+dan+hasil+yang+terstruktur;Quiz+Arena+1000+soal+plus+Learning+Hub+dan+playlist+fokus+berbasis+URL" />

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776ab" />
  <img src="https://img.shields.io/badge/Tkinter-Desktop%20UI-1f6feb" />
  <img src="https://img.shields.io/badge/Quiz-1000%20Soal-14b8a6" />
  <img src="https://img.shields.io/badge/Calculator-Math%20%26%20Accounting-0ea5e9" />
  <img src="https://img.shields.io/badge/PDF-Learning%20Hub-f59e0b" />
  <img src="https://img.shields.io/badge/Focus%20Music-Playlist%20URL-8b5cf6" />
  <img src="https://img.shields.io/badge/Windows-Ready-22c55e" />
</p>

</div>

---

## Overview
**ForgeCore Math & Accounting Studio** adalah aplikasi desktop berbasis **Python + Tkinter** yang dirancang untuk membangun **nuansa menghitung** dalam satu workspace modern. Proyek ini menggabungkan:
- **Super Calculator** untuk rumus matematika dan akuntansi,
- **Quiz Arena 1000 soal** dengan progres belajar,
- **Learning Hub** untuk membuka dan menyalin PDF materi,
- **Music & Focus** agar sesi belajar terasa lebih fokus dan hidup.

Tujuan utama proyek ini adalah membuat pengalaman belajar menjadi **praktis, interaktif, dan terarah** tanpa harus berpindah antara banyak aplikasi.

---

## Key Features
### 🧠 Super Calculator
- Kalkulator multi-kategori untuk kebutuhan belajar dan latihan hitung
- Mendukung rumus inti seperti:
  - kalkulus dasar
  - statistik
  - probabilitas
  - linear algebra
  - time value of money
  - cost-volume-profit
  - rasio keuangan
  - audit risk
- Form input dinamis mengikuti formula yang dipilih
- Menampilkan **hasil utama** dan **langkah ringkas** agar mudah diverifikasi

### 🎯 Quiz Arena 1000 Soal
- Bank soal **1000 soal** untuk topik **Matematika** dan **Akuntansi**
- Pilihan mode:
  - Matematika
  - Akuntansi
  - Campur
- Pengaturan sesi belajar:
  - jumlah soal
  - durasi menit
- Fitur **Hide Mastered** untuk menyembunyikan soal yang sudah dijawab benar
- Cocok untuk review bertahap, latihan cepat, dan simulasi belajar mandiri

### 📚 Learning Hub
- Menyediakan PDF materi bawaan langsung dari aplikasi
- Mendukung aksi:
  - **Open** untuk membuka file PDF
  - **Export Copy** untuk menyimpan salinan ke folder pilihan
- Membantu pengguna tetap terhubung ke materi inti saat belajar atau mengulang konsep

### 🎵 Music & Focus
- Menyediakan playlist URL untuk link seperti YouTube, Spotify, atau audio lainnya
- Tombol play membuka URL melalui player default yang tersedia di sistem
- Dilengkapi metronome BPM sederhana untuk membangun ritme fokus saat menghitung

### ✅ Learning Progress Friendly
- Soal yang sudah dikuasai bisa tidak dimunculkan lagi
- State belajar tersimpan agar latihan terasa lebih efisien
- Desain ini cocok untuk belajar bertahap tanpa mengulang soal yang sama terus-menerus

---

## Use Case Utama
- **Belajar Mandiri**: mengulang konsep, mencoba rumus, dan mengerjakan quiz dalam satu aplikasi
- **Persiapan Ujian**: latihan cepat untuk topik hitung, statistik, dan akuntansi dasar sampai lanjutan
- **Review Materi**: membuka PDF referensi sambil langsung mencoba formula terkait
- **Fokus Belajar**: memadukan kalkulasi, quiz, dan musik latar agar sesi belajar terasa lebih konsisten

---

## Modul Formula
| Kategori | Contoh Formula | Kegunaan |
|---|---|---|
| **Calculus** | turunan dasar, integral sederhana | memahami perubahan nilai dan akumulasi |
| **Statistics** | mean, variance, standard deviation, z-score | analisis data dan distribusi |
| **Probability** | kombinasi, permutasi, binomial, poisson, Bayes | peluang dan prediksi |
| **Linear Algebra** | determinan 2x2, invers 2x2 | operasi matriks dasar |
| **Finance & TVM** | NPV, present value, future value | valuasi arus kas dan investasi |
| **Cost Accounting** | COGS, contribution margin, BEP | analisis biaya dan profitabilitas |
| **Financial Ratios** | current ratio, debt ratio, gross margin | membaca kesehatan keuangan |
| **Audit & Risk** | audit risk model | latihan audit dan evaluasi risiko |

---

## Learning Assets
### PDF Bawaan
- `materi-matematika-akuntansi-dan-1000-soal.pdf`
- `panduan-matematika-sains-data-lengkap.pdf`
- `panduan-akuntansi-s1-s3-lengkap.pdf`

### Data Belajar
- `data/quiz_math_accounting_1000.json` sebagai bank soal utama
- Penyimpanan progres untuk mendukung mekanisme mastered question

---

## Tech Stack
### Core Application
- **Python 3.x**
- **Tkinter** untuk desktop interface
- **JSON** untuk bank soal, metadata, dan state belajar
- **Windows shell integration** untuk membuka PDF dan URL dengan aplikasi default

### Functional Areas
- Engine quiz untuk seleksi soal dan evaluasi jawaban
- Engine kalkulator untuk formula terstruktur
- Resource manager untuk PDF Learning Hub
- Playlist utility untuk focus music berbasis URL

---

## Struktur Proyek
```text
forgecore-math-accounting-studio/
├─ app.py
├─ core.py
├─ smoke_test.py
├─ run.ps1
├─ run.bat
├─ README.md
├─ SMOKE_TEST_RESULTS.json
├─ VALIDATION_RESULTS.md
├─ LANGUAGE_RECOMMENDATIONS.md
├─ data/
│  └─ quiz_math_accounting_1000.json
├─ resources/
│  ├─ materi-matematika-akuntansi-dan-1000-soal.pdf
│  ├─ panduan-akuntansi-s1-s3-lengkap.pdf
│  └─ panduan-matematika-sains-data-lengkap.pdf
└─ __pycache__/
```

---

## Cara Menjalankan
### Jalankan Langsung
```powershell
cd .\forgecore-math-accounting-studio
python .\app.py
```

### Jalankan via Shortcut Script
```powershell
.\run.ps1
```

### Smoke Test
```powershell
python .\smoke_test.py
```

---

## Highlight Tampilan dan Alur Belajar
1. Pilih mode belajar atau formula yang ingin digunakan
2. Atur jumlah soal dan durasi quiz sesuai target sesi
3. Kerjakan soal dan lihat feedback langsung
4. Gunakan kalkulator untuk memeriksa hasil hitung atau memahami rumus
5. Buka PDF dari Learning Hub saat butuh teori tambahan
6. Putar playlist fokus untuk menjaga ritme belajar tetap nyaman

---

## Future Improvements
- Embedded audio player langsung di dalam aplikasi
- Formula library yang lebih luas untuk topik akuntansi lanjutan
- Grafik progres belajar dan statistik performa
- Mode review khusus untuk soal yang pernah salah
- Tema UI yang lebih dinamis dengan visual belajar yang lebih interaktif

---

## License
Proyek ini dibuat untuk **pembelajaran, latihan, eksplorasi rumus, dan pengembangan aplikasi edukasi desktop**.
