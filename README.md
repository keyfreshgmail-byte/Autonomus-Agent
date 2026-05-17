<h1 align="center">🧠 Universal AI Agent Architecture</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Architecture-Modular-black?style=for-the-badge&logo=databricks&logoColor=white" alt="Architecture">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

<p align="center">
  <em>Sistem agen AI tingkat lanjut yang mendukung banyak penyedia LLM (OpenRouter, Groq, OpenAI, Gemini, Anthropic, Ollama) dengan kemampuan Fallback dan Memori Persisten.</em>
</p>

---

## 🚀 Fitur Utama
- **Multi-Provider Support:** Bebas beralih antar AI provider ternama di dunia.
- **Auto-Fallback System:** Jika API utama mati/limit, otomatis pindah ke API cadangan.
- **Smart Retry Logic:** Otomatis mengulang pengiriman (retry) jika server gagal (timeout/500 Error).
- **Persistent Key-Value Memory:** AI bisa mengingat informasi antar sesi obrolan.
- **Environment Secrets (.env):** Sangat aman, tanpa hardcode kredensial.

## ⚙️ Instalasi (Windows / Linux / Termux)
1. Clone repo ini.
```bash
git clone https://github.com/username/ai-agent.git
cd ai-agent
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