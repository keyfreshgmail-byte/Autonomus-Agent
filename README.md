<h1 align="center"> Autonomous AI Agent</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Windows%20%7C%20Linux-black?style=for-the-badge&logo=terminal&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/AI-Multi%20Provider-orange?style=for-the-badge" alt="AI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <em>Asisten AI otonom tingkat lanjut berbasis Telegram dengan fitur Web Scraper, Auto-Updater, kontrol perangkat, dan integrasi WhatsApp.</em>
</p>

---

## ✨ Fitur Unggulan

* **🧠 Multi-Provider AI**: Mendukung **OpenAI**, **Groq**, **Gemini**, **OpenRouter**, dan **Ollama** (Offline).
* **💻 Command Execution**: Bot dapat mengeksekusi perintah shell/terminal di perangkat Anda (dengan persetujuan).
* **🌐 Web & Downloader**: Mengekstrak teks dari URL dan mendownload file gambar otomatis.
* **💾 Memori Cerdas**: Mengingat identitas dan preferensi Anda antar sesi obrolan.
* **🔄 Lifetime Auto-Update**: Bot mengecek update GitHub di latar belakang dan merestart dirinya sendiri jika ada pembaruan kode.

---

## 🚀 Panduan Instalasi

<details>
<summary><b>👉 Klik disini untuk melihat cara instalasi langkah demi langkah</b></summary>

<br>

### Langkah 1: Clone Repository
Unduh kode sumber ke perangkat Anda.
```bash
git clone https://github.com/keyfreshgmail-byte/Autonomus-Agent.git
cd Autonomus-Agent
```

### Langkah 2: Jalankan Autopilot
Sistem dilengkapi dengan fitur **Auto-Installer**. Anda tidak perlu repot menginstal library secara manual, cukup jalankan:
```bash
python bot.py
```
*(Sistem akan otomatis menginstal library `pyTelegramBotAPI`, `requests`, `beautifulsoup4`, dll).*

### Langkah 3: Setup Melalui Dashboard
Saat pertama kali berjalan, layar terminal akan menampilkan **Menu Dashboard Utama**.
1. Ketik `2` untuk masuk ke menu **Setup Provider AI**.
2. Pilih AI yang ingin digunakan (misal: Gemini, Groq, atau OpenAI) dan masukkan **API Key** serta **Telegram Bot Token**.
3. Ketik `0` untuk kembali ke menu awal.
4. Ketik `1` untuk menyalakan Bot. Selesai! 🎉

</details>

---

## 📂 Struktur Proyek

Proyek ini diatur agar tetap rapi, bersih, dan modular.
```text
📁 Autonomus-Agent/
├── 📄 bot.py          # Entry point utama & manajemen Telegram Bot
├── 📄 ui.py           # Engine antarmuka CLI (Animasi, Warna, & Splash Screen)
├── 📄 .gitignore      # Aturan keamanan untuk memblokir file rahasia/sampah
├── 🔒 config.json     # (Lokal) Konfigurasi kredensial & API Key pengguna
├── 🔒 memory.json     # (Lokal) Database ingatan jangka panjang AI
└── 🔒 error.log       # (Lokal) Catatan error sistem (Auto-generated)
```

---

## 🔒 Keamanan

**JANGAN PERNAH** membagikan file `config.json` dan `memory.json` Anda. File `.gitignore` pada repositori ini telah diatur sedemikian rupa agar file konfigurasi yang berisi API Key dan Token Anda tidak akan ikut ter-upload ke GitHub meskipun Anda melakukan *Auto-Sync*.

---

## 📝 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan otomatisasi pribadi. Anda bebas memodifikasi dan mengembangkan kode ini sesuai kebutuhan.

*Created with ❤️ by Muzaqi Dev | Copyright 2026*