# 🤖 Autonomous Termux Agent

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-black?logo=terminal&logoColor=white)
![AI](https://img.shields.io/badge/AI-Gemini%20%7C%20Ollama%20%7C%20OpenRouter-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Autonomous Termux Agent** adalah bot Telegram cerdas yang berjalan di lingkungan Termux (Android) atau PC. Bot ini tidak hanya sekadar membalas chat, tetapi juga dapat berpikir secara otonom untuk mengeksekusi perintah terminal, membaca isi website, mengirim file, dan mengontrol WhatsApp secara mandiri.

---

## ✨ Fitur Utama

- **🧠 Multi-Provider AI**: Mendukung **Google Gemini** (Cloud), **Ollama** (Local Offline AI), dan **OpenRouter** (Claude, Llama, dll).
- **💻 Eksekusi Perintah Terminal**: AI dapat memberikan dan mengeksekusi perintah shell (bash/cmd) secara langsung melalui persetujuan di Telegram.
- **📱 Integrasi WhatsApp (Mudslide)**: AI dapat mengirim pesan dan gambar ke WhatsApp pengguna lain secara otomatis.
- **🌐 Web Scraper & Downloader**: Mampu membaca isi artikel/website langsung dari URL dan mendownload gambar/file dari internet ke penyimpanan lokal.
- **💾 Memori Jangka Panjang**: Bot dapat mengingat fakta-fakta penting tentang Anda ke dalam file `memory.json`.
- **🔄 Auto-Sync GitHub**: Dilengkapi fitur bawaan untuk melakukan *Pull* dan *Push* ke GitHub langsung dari UI Terminal, tanpa harus mengetik perintah git manual.
- **🛡️ Resilien & Auto-Restart**: Sistem *error handling* yang kuat dengan *auto-restart* jika koneksi terputus.

---

## ⚙️ Persyaratan Sistem

- **Python 3.8+**
- **Git** (Untuk sinkronisasi & instalasi)
- **Node.js** (Opsional, khusus untuk fitur WhatsApp CLI / Mudslide)
- **Termux:API** (Opsional, jika dijalankan di Termux Android untuk cek baterai/hardware)

---

## 🚀 Cara Instalasi

Ikuti langkah-langkah berikut untuk menjalankan bot ini di terminal/Termux Anda:

### 1. Clone Repository
```bash
git clone https://github.com/keyfreshgmail-byte/Autonomus-Agent.git
cd Autonomus-Agent
```

### 2. Jalankan Program
Program ini dirancang untuk melakukan **Auto-Install** semua *library* Python yang dibutuhkan (`pyTelegramBotAPI`, `requests`, `beautifulsoup4`) saat pertama kali dijalankan.

```bash
python bot.py
```

### 3. Setup Melalui Dashboard Interaktif
Setelah program berjalan, Anda akan disambut oleh **Menu Dashboard Utama**. Lakukan langkah berikut:
1. Pilih menu **Setup Provider AI** (Pilih Gemini, Ollama, atau OpenRouter).
2. Masukkan **API Key** (Gemini/OpenRouter) dan **Telegram Bot Token** dari @BotFather.
3. Kembali ke menu utama dan pilih **Jalankan Bot**.

Bot sekarang sudah aktif dan siap menerima perintah dari Telegram! 🎉

---

## 📂 Struktur Direktori

```text
📁 Autonomus-Agent/
├── bot.py          # Core logic dan integrasi Telegram Bot
├── ui.py           # Konfigurasi antarmuka (Splash Screen & ASCII Art)
├── .gitignore      # Mengecualikan file sensitif (konfigurasi & log) dari GitHub
├── config.json     # (Auto-generated) Menyimpan API Key & Token
├── memory.json     # (Auto-generated) Menyimpan ingatan jangka panjang AI
└── error.log       # (Auto-generated) Menyimpan log jika terjadi error
```

---

## 🔒 Keamanan

**JANGAN PERNAH** membagikan file `config.json` dan `memory.json` Anda. File `.gitignore` pada repositori ini telah diatur sedemikian rupa agar file konfigurasi yang berisi API Key dan Token Anda tidak akan ikut ter-upload ke GitHub meskipun Anda melakukan *Auto-Sync*.

---

## 📝 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan otomatisasi pribadi. Anda bebas memodifikasi dan mengembangkan kode ini sesuai kebutuhan.

*Created with ❤️ by Muzaqi Dev | Copyright 2026*