# afiagent

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Bahasa Indonesia](./README.md)

> 源于开源，回馈开源

AfiAgent adalah kerangka kerja otomatisasi AI berbasis komunitas yang dibangun di atas karya luar biasa dari komunitas sumber terbuka. Tujuan kami adalah mengintegrasikan model bahasa dengan alat profesional seperti pencarian web, perayap, dan eksekusi kode Python, sambil memberikan kontribusi kembali kepada komunitas yang memungkinkan semua ini.

## Video Demo

> **Tugas**: Hitung indeks pengaruh DeepSeek R1 di HuggingFace. Indeks ini dapat dirancang dengan mempertimbangkan jumlah tertimbang dari faktor-faktor seperti pengikut, unduhan, dan suka.

[![Demo](./assets/demo.gif)](./assets/demo.mp4)

- [Tonton di YouTube](https://youtu.be/sZCHqrQBUGk)
- [Unduh Video](https://github.com/afiagent/afiagent/blob/main/assets/demo.mp4)

## Daftar Isi
- [afiagent](#afiagent)
  - [Video Demo](#video-demo)
  - [Daftar Isi](#daftar-isi)
  - [Mulai Cepat](#mulai-cepat)
  - [Arsitektur](#arsitektur)
  - [Fitur](#fitur)
    - [Kemampuan Inti](#kemampuan-inti)
    - [Alat dan Integrasi](#alat-dan-integrasi)
    - [Fitur Pengembangan](#fitur-pengembangan)
    - [Manajemen Alur Kerja](#manajemen-alur-kerja)
  - [Mengapa Memilih AfiAgent?](#mengapa-memilih-afiagent)
  - [Instalasi dan Pengaturan](#instalasi-dan-pengaturan)
    - [Prasyarat](#prasyarat)
    - [Langkah-langkah Instalasi](#langkah-langkah-instalasi)
    - [Konfigurasi](#konfigurasi)
    - [Mengkonfigurasi Git Hooks Pre-commit](#mengkonfigurasi-git-hooks-pre-commit)
  - [Penggunaan](#penggunaan)
    - [Eksekusi Dasar](#eksekusi-dasar)
    - [Server API](#server-api)
    - [Konfigurasi Lanjut](#konfigurasi-lanjut)
    - [Sistem Prompt Agen](#sistem-prompt-agen)
      - [Peran Agen Inti](#peran-agen-inti)
      - [Arsitektur Sistem Prompt](#arsitektur-sistem-prompt)
  - [Antarmuka Web](#antarmuka-web)
  - [Pengembangan](#pengembangan)
    - [Pengujian](#pengujian)
    - [Kualitas Kode](#kualitas-kode)
  - [Kontribusi](#kontribusi)
  - [Lisensi](#lisensi)
  - [Ucapan Terima Kasih](#ucapan-terima-kasih)
  - [Integrasi Code Server](#integrasi-code-server)
    - [Cara Kerja Integrasi](#cara-kerja-integrasi)
    - [Meluncurkan Code Server](#meluncurkan-code-server)
    - [Ketergantungan Baru](#ketergantungan-baru)
    - [Alur Kerja yang Diperbarui](#alur-kerja-yang-diperbarui)

## Mulai Cepat

```bash
# Kloning repositori
git clone https://github.com/afiagent/afiagent.git
cd afiagent

# Buat dan aktifkan virtual environment dengan uv
uv python install 3.12
uv venv --python 3.12

source .venv/bin/activate  # Untuk Windows: .venv\Scripts\activate

# Instal dependensi
uv sync

# Konfigurasi lingkungan
cp .env.example .env
# Edit file .env dan masukkan kunci API Anda

# Jalankan proyek
uv run main.py
```

## Arsitektur

AfiAgent mengimplementasikan sistem multi-agen berlapis, di mana agen Supervisor mengoordinasikan agen-agen khusus untuk menyelesaikan tugas-tugas kompleks:

![Arsitektur AfiAgent](./assets/architecture.png)

Sistem ini bekerja sama dengan agen-agen berikut:

1. **Koordinator (Coordinator)**: Titik masuk alur kerja, menangani interaksi awal dan merutekan tugas.
2. **Perencana (Planner)**: Menganalisis tugas dan mengembangkan strategi eksekusi.
3. **Supervisor**: Mengawasi dan mengelola eksekusi agen lain.
4. **Peneliti (Researcher)**: Mengumpulkan dan menganalisis informasi.
5. **Programmer (Coder)**: Bertanggung jawab untuk pembuatan dan modifikasi kode.
6. **Peramban (Browser)**: Melakukan penjelajahan web dan pengambilan informasi.
7. **Pelapor (Reporter)**: Menghasilkan laporan dan ringkasan hasil alur kerja.

## Fitur

### Kemampuan Inti
- 🤖 **Integrasi LLM**
    - Mendukung Google Gemini API (gemini-2.0-flash)
    - Fallback otomatis ke Gemini (jika API berbahasa Mandarin terdeteksi)
    - Antarmuka API yang kompatibel dengan OpenAI
    - Sistem LLM multi-tingkat untuk beradaptasi dengan kompleksitas tugas yang berbeda

### Alat dan Integrasi
- 🔍 **Pencarian dan Pengambilan**
    - Pencarian web melalui Tavily API
    - Ekstraksi konten tingkat lanjut

### Fitur Pengembangan
- 🐍 **Integrasi Python**
    - Python REPL bawaan
    - Lingkungan eksekusi kode
    - Menggunakan uv untuk manajemen paket

### Manajemen Alur Kerja
- 📊 **Visualisasi dan Kontrol**
    - Visualisasi diagram alur kerja
    - Orkes multi-agen
    - Penugasan dan pemantauan tugas

## Mengapa Memilih AfiAgent?

Kami percaya pada kekuatan kolaborasi sumber terbuka. Implementasi proyek ini tidak akan mungkin terjadi tanpa dukungan dari proyek-proyek luar biasa berikut:
- [Google Gemini API](https://ai.google.dev/): Menyediakan model bahasa yang kuat
- [Tavily](https://tavily.com/): Menyediakan kemampuan pencarian
- Dan banyak kontributor sumber terbuka lainnya

Kami berkomitmen untuk memberikan kontribusi kembali kepada komunitas, dan kami menyambut semua bentuk kontribusi - baik itu perbaikan kesalahan ketik, peningkatan dokumentasi, laporan masalah, atau saran fitur. Silakan lihat [Panduan Kontribusi](CONTRIBUTING.md) kami untuk memulai.

## Instalasi dan Pengaturan

### Prasyarat

- Manajer paket [uv](https://github.com/astral-sh/uv)

### Langkah-langkah Instalasi

AfiAgent menggunakan [uv](https://github.com/astral-sh/uv) sebagai manajer paket untuk menyederhanakan manajemen dependensi.
Ikuti langkah-langkah di bawah ini untuk menyiapkan virtual environment dan menginstal dependensi yang diperlukan:

```bash
# Langkah 1: Buat dan aktifkan virtual environment dengan uv
uv python install 3.12
uv venv --python 3.12

# Untuk sistem Unix/macOS:
source .venv/bin/activate

# Untuk sistem Windows:
.venv\Scripts\activate

# Langkah 2: Instal dependensi proyek
uv sync
```

### Konfigurasi

AfiAgent menggunakan sistem LLM tiga lapis untuk penalaran, tugas dasar, dan tugas bahasa visual. Buat file `.env` di direktori root proyek dan konfigurasikan variabel lingkungan berikut:

```ini
# Konfigurasi LLM Penalaran (untuk tugas penalaran kompleks)
REASONING_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your_gemini_api_key

# Konfigurasi LLM Dasar (untuk tugas sederhana)
BASIC_MODEL=your_basic_model # Contoh: gpt-4o
BASIC_API_KEY=your_basic_api_key

# Konfigurasi LLM Bahasa Visual (untuk tugas yang melibatkan gambar)
VL_MODEL=your_vl_model # Contoh: gpt-4o
VL_API_KEY=your_vl_api_key

# Kunci API Alat
TAVILY_API_KEY=your_tavily_api_key

# Konfigurasi Peramban
CHROME_INSTANCE_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome  # Opsional, jalur ke executable Chrome
```

> **Catatan:**
>
> - Sistem menggunakan model yang berbeda untuk jenis tugas yang berbeda:
>     - LLM Penalaran untuk keputusan dan analisis kompleks (sekarang default ke Gemini)
>     - LLM Dasar untuk tugas teks sederhana
>     - LLM Bahasa Visual untuk tugas yang melibatkan pemahaman gambar
> - Jika model penalaran menggunakan API berbahasa Mandarin, itu akan secara otomatis mendeteksi dan kembali ke Gemini.
> - Jika model dasar dan bahasa visual bukan Gemini, URL dasar mereka dapat disesuaikan secara independen.
> - Setiap LLM dapat menggunakan kunci API yang berbeda.
> - Pencarian Tavily secara default dikonfigurasi untuk mengembalikan hingga 5 hasil (Anda bisa mendapatkan kunci ini di [app.tavily.com](https://app.tavily.com/))

Anda dapat menyalin file `.env.example` sebagai template untuk memulai:

```bash
cp .env.example .env
```

### Mengkonfigurasi Git Hooks Pre-commit
AfiAgent menyertakan hook pre-commit yang menjalankan pemeriksaan kode dan pemformatan sebelum setiap commit. Ikuti langkah-langkah ini untuk mengaturnya:

1. Jadikan skrip pre-commit dapat dieksekusi:
```bash
chmod +x pre-commit
```

2. Instal hook pre-commit:
```bash
ln -s ../../pre-commit .git/hooks/pre-commit
```

Hook pre-commit akan secara otomatis:
- Menjalankan pemeriksaan kode (`make lint`)
- Memformat kode (`make format`)
- Menambahkan kembali file yang diformat ulang ke area staging
- Mencegah commit jika ada kesalahan pemeriksaan kode atau pemformatan

## Penggunaan

### Eksekusi Dasar

Jalankan AfiAgent dengan pengaturan default:

```bash
uv run main.py
```

### Server API

AfiAgent menyediakan server API berbasis FastAPI yang mendukung respons streaming:

```bash
# Mulai server API
make serve

# Atau jalankan langsung
uv run server.py
```

Server API menyediakan endpoint berikut:

- `POST /api/chat/stream`: Endpoint obrolan untuk panggilan LangGraph, respons streaming
    - Body Permintaan:
    ```json
    {
      "messages": [
        {"role": "user", "content": "Masukkan kueri Anda di sini"}
      ],
      "debug": false
    }
    ```
    - Mengembalikan aliran Server-Sent Events (SSE) yang berisi respons agen


### Konfigurasi Lanjut

AfiAgent dapat disesuaikan melalui berbagai file konfigurasi di direktori `src/config`:
- `env.py`: Mengkonfigurasi model LLM, kunci API, dan URL dasar
- `tools.py`: Menyesuaikan pengaturan khusus alat (misalnya, batas hasil pencarian Tavily)
- `agents.py`: Memodifikasi komposisi tim dan prompt sistem agen

### Sistem Prompt Agen

AfiAgent menggunakan sistem prompt yang canggih di direktori `src/prompts` untuk menentukan perilaku dan tanggung jawab agen:

#### Peran Agen Inti

- **Supervisor ([`src/prompts/supervisor.md`](src/prompts/supervisor.md))**: Mengoordinasikan tim dan menetapkan tugas dengan menganalisis permintaan dan menentukan ahli mana yang akan menanganinya. Bertanggung jawab untuk memutuskan penyelesaian tugas dan transisi alur kerja.

- **Peneliti ([`src/prompts/researcher.md`](src/prompts/researcher.md))**: Mengkhususkan diri dalam mengumpulkan informasi melalui pencarian web dan pengumpulan data. Menggunakan pencarian Tavily dan fungsionalitas perayapan web, menghindari perhitungan matematika atau operasi file.

- **Programmer ([`src/prompts/coder.md`](src/prompts/coder.md))**: Peran insinyur perangkat lunak profesional yang berfokus pada skrip Python dan bash. Menangani:
    - Eksekusi dan analisis kode Python
    - Eksekusi perintah Shell
    - Pemecahan masalah teknis dan implementasi

- **Manajer File ([`src/prompts/file_manager.md`](src/prompts/file_manager.md))**: Menangani semua operasi sistem file, dengan fokus pada pemformatan dan penyimpanan konten dalam format markdown yang benar.

- **Peramban ([`src/prompts/browser.md`](src/prompts/browser.md))**: Pakar interaksi web, menangani:
    - Navigasi situs web
    - Interaksi halaman (klik, input, gulir)
    - Ekstraksi konten dari halaman web

#### Arsitektur Sistem Prompt

Sistem prompt menggunakan mesin template ([`src/prompts/template.py`](src/prompts/template.py)) untuk:
- Memuat template markdown khusus peran
- Menangani penggantian variabel (misalnya, waktu saat ini, informasi anggota tim)
- Memformat prompt sistem untuk setiap agen

Setiap prompt agen didefinisikan dalam file markdown terpisah, memungkinkan modifikasi perilaku dan tanggung jawab yang mudah tanpa mengubah kode dasar.

## Antarmuka Web

AfiAgent menyediakan antarmuka web default.

Silakan lihat proyek [afiagent/afiagent-web](https://github.com/afiagent/afiagent-web) untuk informasi lebih lanjut.

## Pengembangan

### Pengujian

Jalankan suite pengujian:

```bash
# Jalankan semua pengujian
make test

# Jalankan file pengujian tertentu
pytest tests/integration/test_workflow.py

# Jalankan pengujian cakupan
make coverage
```

### Kualitas Kode

```bash
# Jalankan pemeriksaan kode
make lint

# Format kode
make format
```

## Kontribusi

Kami menyambut semua bentuk kontribusi! Baik itu memperbaiki kesalahan ketik, meningkatkan dokumentasi, atau menambahkan fitur baru, bantuan Anda akan sangat dihargai. Silakan lihat [Panduan Kontribusi](CONTRIBUTING.md) kami untuk memulai.

## Lisensi

Proyek ini adalah sumber terbuka, berdasarkan [Lisensi MIT](LICENSE).

## Ucapan Terima Kasih

Terima kasih khusus kepada semua proyek sumber terbuka dan kontributor yang memungkinkan AfiAgent. Kami berdiri di atas bahu para raksasa.

## Integrasi Code Server

AfiAgent sekarang mendukung eksekusi kode otomatis menggunakan Code Server setiap kali pengguna meminta pembuatan kode. Ini memungkinkan agen untuk menjalankan dan menguji kode yang dihasilkan dalam lingkungan yang terisolasi dan interaktif.

### Cara Kerja Integrasi

Ketika agen menerima permintaan yang melibatkan pembuatan atau eksekusi kode, agen akan:
1. Meluncurkan Code Server di lingkungan sandbox.
2. Mengirim kode yang dihasilkan ke Code Server untuk eksekusi.
3. Menangkap output dan hasil eksekusi dari Code Server.
4. Menggunakan hasil ini untuk melanjutkan tugas atau memberikan umpan balik kepada pengguna.

### Meluncurkan Code Server

Code Server dapat diluncurkan secara manual menggunakan perintah berikut:

```bash
PASSWORD=4f9c26af9e42b1b8 /usr/bin/code-server \
  --bind-addr 0.0.0.0:8329 \
  --auth password \
  --disable-workspace-trust \
  /home/ubuntu/AfiAgent
```

- `PASSWORD=4f9c26af9e42b1b8`: Menetapkan kata sandi untuk akses Code Server. Kata sandi ini harus dijaga kerahasiaannya.
- `--bind-addr 0.0.0.0:8329`: Mengikat Code Server ke semua antarmuka jaringan yang tersedia pada port 8329. Ini memungkinkan akses dari luar sandbox.
- `--auth password`: Mengaktifkan otentikasi berbasis kata sandi.
- `--disable-workspace-trust`: Menonaktifkan fitur kepercayaan ruang kerja, yang berguna untuk lingkungan pengembangan yang cepat.
- `/home/ubuntu/AfiAgent`: Menentukan direktori ruang kerja untuk Code Server. Ini adalah direktori root proyek AfiAgent.

Setelah diluncurkan, Code Server akan tersedia melalui URL yang diekspos oleh Manus (misalnya, `https://8329-ixwutjurcmch5eqtvwerp-fb845e4a.manus.computer`). Anda dapat mengaksesnya di browser Anda menggunakan kata sandi yang ditentukan.

### Ketergantungan Baru

Integrasi Code Server memperkenalkan ketergantungan baru:
- **Code Server**: Aplikasi Code Server itu sendiri, yang sudah diinstal di lingkungan sandbox.

Tidak ada dependensi Python tambahan yang diperlukan untuk integrasi ini, karena Code Server beroperasi secara independen dan berkomunikasi dengan agen melalui antarmuka baris perintah atau API.

### Alur Kerja yang Diperbarui

Alur kerja agen telah diperbarui untuk secara otomatis memicu Code Server ketika tugas-tugas tertentu yang melibatkan eksekusi kode terdeteksi. Ini memastikan bahwa agen memiliki lingkungan yang kuat untuk menguji dan memvalidasi kode yang dihasilkan, meningkatkan keandalan dan akurasi respons agen.