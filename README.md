<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=210&color=0:0f172a,50:2563eb,100:14b8a6&text=ForgeCore%20Polyglot%20Compiler%20Quiz%20Studio&fontSize=34&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Multi-language%20compiler%20sandbox%2C%20adaptive%20quiz%2C%20dan%20learning%20hub&descAlignY=58" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=3000&pause=700&color=60A5FA&center=true&vCenter=true&width=980&lines=Studio+desktop+Python+untuk+uji+banyak+bahasa+dengan+toolchain+asli;Compile%2C+run%2C+validasi+output%2C+quiz+adaptif%2C+dan+materi+dalam+satu+app;Cocok+untuk+latihan%2C+eksperimen%2C+demo%2C+dan+pembelajaran+multi-toolchain" />

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776ab" />
  <img src="https://img.shields.io/badge/Tkinter-Desktop%20UI-1f6feb" />
  <img src="https://img.shields.io/badge/Multi--Toolchain-36%20Profiles-14b8a6" />
  <img src="https://img.shields.io/badge/Quiz-Adaptive-8b5cf6" />
  <img src="https://img.shields.io/badge/Learning%20Hub-PDF%20Ready-0ea5e9" />
</p>

</div>

---

## Overview
**ForgeCore Polyglot Compiler Quiz Studio** adalah aplikasi desktop berbasis **Python + Tkinter** untuk mencoba banyak bahasa pemrograman menggunakan **compiler / runtime asli** yang terpasang di komputer pengguna. Proyek ini menggabungkan area compile-run, validasi expected output, quiz adaptif, riwayat report, dan pusat materi belajar dalam satu workspace.

Fokus utama proyek ini adalah membuat pengalaman belajar dan eksperimen terasa lebih natural seperti terminal biasa, tetapi tetap rapi, terstruktur, dan nyaman dipakai untuk latihan harian.

---

## Key Features
### 💻 Compiler Studio
- Menjalankan source code memakai **toolchain asli** dari mesin lokal
- Output utama fokus pada **hasil nyata program** (`stdout`) dan error compile/runtime bila ada
- Mendukung **Program Input (stdin)** agar hasil benar-benar mengikuti input pengguna
- **Expected Output** dapat diedit langsung untuk validasi manual
- Ringkasan eksekusi tetap tersedia, seperti:
  - exit code
  - durasi eksekusi
  - status cocok / tidak cocok dengan expected output

### 🧠 Adaptive Quiz Arena
- Quiz bertimer untuk latihan konsep lintas bahasa
- Pengguna bisa memilih:
  - kategori quiz
  - jumlah soal
  - durasi
- Soal yang sudah dijawab benar akan ditandai **mastered**
- Soal mastered **tidak ditampilkan lagi** pada sesi berikutnya agar latihan lebih efisien

### 📚 Learning Hub
- Ringkasan materi bahasa pemrograman
- Roadmap belajar dan command cheat sheet
- Strategi latihan untuk mempercepat pemahaman toolchain
- Tiga file PDF dibundel di folder `resources/` dan bisa diakses dari aplikasi

### 📊 Reports dan Progress
- Menyimpan report JSON detail untuk audit dan debugging
- Menyimpan riwayat quiz dan progress pengguna secara otomatis
- Membantu pengguna melihat perkembangan latihan dari waktu ke waktu

### 🎨 UI Lebih Terlihat
- Kolom pilihan bahasa, kategori quiz, jumlah soal, dan durasi memakai **tema gelap**
- Tata letak dibuat agar fokus ke editor, input, output, dan kontrol utama

---

## Use Case Utama
- **Belajar Banyak Bahasa**: mencoba syntax dan perilaku eksekusi lintas toolchain dari satu aplikasi
- **Validasi Output**: membandingkan hasil aktual program dengan output yang diharapkan
- **Latihan Coding Dasar**: cocok untuk eksperimen kecil, contoh cepat, dan cek perilaku runtime
- **Quiz Pembelajaran**: mengulang materi dengan mode latihan bertimer dan progress mastery
- **Demo Edukatif**: cocok untuk presentasi sederhana, latihan mandiri, atau portfolio belajar

---

## Profil Toolchain yang Disediakan
| Profil | Keterangan |
|---|---|
| **Python / Py Launcher** | Menjalankan skrip Python dari interpreter lokal. |
| **C / C++** | Compile dan run memakai compiler native yang tersedia. |
| **Java** | Compile dan run source Java dari JDK lokal. |
| **.NET** | Menjalankan workflow berbasis toolchain .NET lokal. |
| **Go / Swift / Kotlin / Ruby / Rust** | Profil native untuk eksperimen lintas bahasa umum. |
| **Node.js / V8 / npm / npx** | Eksekusi JavaScript dan workflow Node lokal. |
| **TypeScript / Vite / Deno / Bun** | Profil modern untuk ecosystem JavaScript dan TypeScript. |
| **R / Julia / SQLite** | Profil untuk script, numerik, dan query dasar. |
| **Haskell / Scala / Clojure / Elixir / Erlang / OCaml / Scheme** | Profil functional dan akademik untuk eksplorasi lebih luas. |
| **Bash / PHP / Lua / Tcl / Nim / Crystal / NASM** | Profil tambahan untuk variasi toolchain dan low-level practice. |

---

## Learning Resources
### PDF yang Dibundel
- `ringkasan-lengkap-bahasa-pemrograman.pdf`
- `materi-bahasa-pemrograman-dan-1000-soal.pdf`
- `IELTS_JLPT_1000_Practice_Pack.pdf`

### Materi yang Tersedia di App
- Ringkasan fondasi bahasa pemrograman
- Peta besar runtime, platform, dan toolchain
- Command cheat sheet dasar
- Strategi latihan dan roadmap belajar bertahap

---

## Tech Stack
### Aplikasi
- **Python 3**
- **Tkinter**
- **JSON** untuk data quiz, report, dan progress
- **PowerShell / batch launcher** untuk shortcut menjalankan aplikasi di Windows

### Komponen Internal
- `engine.py` untuk proses compile-run dan orkestrasi output
- `profiles.py` untuk definisi profil toolchain
- `quizzes.py` untuk bank soal dan logika quiz
- `materials.py` untuk materi dan Learning Hub

---

## Struktur Proyek
```text
forgecore-polyglot-compiler-quiz-studio/
├─ app.py
├─ engine.py
├─ profiles.py
├─ quizzes.py
├─ materials.py
├─ compiler_guide.md
├─ quiz_guide.md
├─ smoke_test.py
├─ run.ps1
├─ run.bat
├─ README.md
└─ resources/
   ├─ ringkasan-lengkap-bahasa-pemrograman.pdf
   ├─ materi-bahasa-pemrograman-dan-1000-soal.pdf
   └─ IELTS_JLPT_1000_Practice_Pack.pdf
```

---

## Cara Menjalankan
### PowerShell
```powershell
cd .\forgecore-polyglot-compiler-quiz-studio
python .\app.py
```

### Alternatif Script
```powershell
cd .\forgecore-polyglot-compiler-quiz-studio
.\run.ps1
```

---

## Validasi Cepat
```powershell
cd .\forgecore-polyglot-compiler-quiz-studio
python .\smoke_test.py
```

---

## Workspace Pengguna
Saat aplikasi berjalan, file pengguna dan progress akan disimpan otomatis di:

- `~/ForgeCorePolyglotCompilerQuizStudio/samples`
- `~/ForgeCorePolyglotCompilerQuizStudio/reports`
- `~/ForgeCorePolyglotCompilerQuizStudio/quiz_history`

---

## Alur Pakai Singkat
1. Pilih profil bahasa / toolchain
2. Tulis atau muat source code sample
3. Isi **Program Input** bila diperlukan
4. Jalankan compile / run
5. Bandingkan hasil aktual dengan **Expected Output**
6. Lanjutkan ke tab quiz untuk latihan dan mastery
7. Buka **Learning Hub** untuk materi dan PDF pendukung

---

## Catatan Implementasi
- Hasil compile dan run mengikuti kondisi toolchain asli di komputer pengguna
- Perbedaan versi compiler, PATH, SDK, linker, atau dependency lokal dapat memengaruhi hasil
- Aplikasi ini bukan simulator; hasil eksekusi bergantung pada environment nyata pengguna
- Tidak membutuhkan dependency Python eksternal tambahan untuk fungsi inti

---

## Future Improvements
- Tambah editor yang lebih mirip IDE mini
- Tambah terminal interaktif yang lebih natural untuk input bertahap
- Tambah preset sample per bahasa yang lebih banyak
- Tambah statistik progress quiz yang lebih visual
- Tambah export report yang lebih lengkap untuk review pembelajaran

---

## License
Proyek ini dibuat untuk **pembelajaran, eksperimen, latihan, dan pengembangan skill teknis**.
