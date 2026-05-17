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

### 🔥 Cara Paling Cepat (1-Click Install untuk Termux)
Salin satu baris perintah di bawah ini, lalu tempelkan (paste) ke dalam aplikasi Termux Anda dan tekan Enter:

```bash
curl -sL https://raw.githubusercontent.com/keyfreshgmail-byte/Autonomus-Agent/main/install.sh | bash
```
*(Perintah di atas akan otomatis mengunduh sistem, memasang Python, Node.js, dan menjalankan bot tanpa Anda perlu mengetik apa pun lagi).*

<br>

<details>
<summary><b>👉 Klik disini untuk melihat cara instalasi manual (Langkah demi langkah)</b></summary>

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

## ☁️ Panduan Deploy ke VPS (24/7 Standby)

Agar bot menyala nonstop tanpa memakan kuota/baterai HP, Anda bisa menjalankannya di VPS Linux (Ubuntu/Debian).

### 1. Install Dependensi Dasar VPS
Buka terminal/SSH VPS Anda, lalu jalankan:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git tmux nodejs npm -y
```

### 2. Clone & Install
```bash
git clone https://github.com/keyfreshgmail-byte/Autonomus-Agent.git
cd Autonomus-Agent
pip3 install -r requirements.txt
```

### 3. Jalankan di Latar Belakang (Background)
Gunakan `tmux` agar program tidak terhenti saat Anda menutup koneksi SSH VPS:
```bash
tmux new -s agent
python3 bot.py
```
* **Detach (Keluar terminal tanpa mematikan bot):** Tekan `Ctrl + B`, lalu lepaskan, dan tekan `D`.
* **Attach (Melihat log bot kembali):** Ketik `tmux attach -t agent`.

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