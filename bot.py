import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import time
import shutil
import re
import logging
from ui import *

# ==========================================
# SETUP LOGGING
# ==========================================
logging.basicConfig(filename='error.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ==========================================
# 1. FITUR AUTO-INSTALL LIBRARY PYTHON
# ==========================================
def install_libraries():
    print(f"{CYAN}--- Pengecekan Sistem & Library ---{RESET}")
    required_libs = {
        'telebot': 'pyTelegramBotAPI',
        'requests': 'requests',
        'bs4': 'beautifulsoup4'
    }
    
    for lib, pkg in required_libs.items():
        try:
            __import__(lib)
            print(f"Library {pkg:<25} [{GREEN}✓{RESET}]")
        except ImportError:
            print(f"Library {pkg:<25} [{YELLOW}Menginstall...{RESET}]", end="\r")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", pkg, "--quiet"])
                print(f"Library {pkg:<25} [{GREEN}✓{RESET}]          ")
            except Exception as e:
                print(f"Library {pkg:<25} [{RED}✗{RESET}]")
                print(f"{RED}[Fatal Error]{RESET} Gagal menginstall {pkg}: {e}")
                logging.error(f"Gagal menginstall library {pkg}: {e}")
                sys.exit(1)

install_libraries()

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup

# ==========================================
# 2. FITUR AUTO-CHECK (TERMUX:API & WA CLI)
# ==========================================
def check_dependencies():
    if shutil.which("termux-battery-status"):
        print(f"Package Termux:API            [{GREEN}✓{RESET}]")
    else:
        print(f"Package Termux:API            [{YELLOW}Menginstall...{RESET}]", end="\r")
        subprocess.run("pkg install termux-api -y", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Package Termux:API            [{GREEN}✓{RESET}]          ")

    try:
        res = subprocess.run("termux-battery-status", shell=True, capture_output=True, text=True, timeout=3)
        if res.returncode == 0 and len(res.stdout.strip()) > 5:
            print(f"Koneksi APK Termux:API        [{GREEN}✓{RESET}]")
        else:
             print(f"Koneksi APK Termux:API        [{RED}✗{RESET}] (Pastikan APK terinstall)")
    except Exception:
        print(f"Koneksi APK Termux:API        [{RED}?{RESET}]")

    if shutil.which("node") and shutil.which("npx"):
        print(f"Node.js & NPX (Untuk WA)      [{GREEN}✓{RESET}]")
    else:
        print(f"Node.js & NPX (Untuk WA)      [{YELLOW}Menginstall...{RESET}]", end="\r")
        subprocess.run("pkg install nodejs -y", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Node.js & NPX (Untuk WA)      [{GREEN}✓{RESET}]          ")

    try:
        res = subprocess.run("yes | npx mudslide me", shell=True, capture_output=True, text=True, timeout=10)
        if "id" in res.stdout.lower() or res.returncode == 0:
            print(f"Status Login WhatsApp         [{GREEN}Terhubung{RESET}]")
        else:
            print(f"Status Login WhatsApp         [{RED}Belum Scan QR{RESET}]")
    except Exception:
        pass

# ==========================================
# 3. CORE BOT AUTONOMOUS
# ==========================================
CONFIG_FILE = "config.json"
MEMORY_FILE = "memory.json"

# Defaults
DEFAULT_PROVIDER = "gemini"
DEFAULT_MODEL = "gemini-1.5-flash"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder:7b"
DEFAULT_OPENROUTER_MODEL = "google/gemma-4-26b-a4b-it:free"
MAX_HISTORY_LENGTH = 15

AVAILABLE_GEMINI_MODELS = {
    "1": "gemini-1.5-flash",
    "2": "gemini-1.5-pro",
    "3": "gemini-2.5-flash",
    "4": "gemini-2.5-pro"
}

user_histories = {}
pending_commands = {}

def load_config():
    default_config = {
        "provider": DEFAULT_PROVIDER, 
        "model": DEFAULT_MODEL, 
        "ollama_url": DEFAULT_OLLAMA_URL, 
        "ollama_model": DEFAULT_OLLAMA_MODEL,
        "openrouter_api_key": "",
        "openrouter_model": DEFAULT_OPENROUTER_MODEL
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                for k, v in default_config.items():
                    if k not in config: config[k] = v
                return config
        except Exception as e: 
            logging.error(f"Gagal load_config: {e}")
            return default_config
    return default_config

def save_config(config_data):
    try:
        with open(CONFIG_FILE, "w") as f: json.dump(config_data, f, indent=4)
        return True
    except Exception as e: 
        logging.error(f"Gagal save_config: {e}")
        return False

def load_memories():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f: return json.load(f)
        except Exception as e: 
            logging.error(f"Gagal load_memories: {e}")
            return []
    return []

def save_memories(memories_list):
    try:
        with open(MEMORY_FILE, "w") as f: json.dump(memories_list, f, indent=4)
    except Exception as e: 
        logging.error(f"Gagal save_memories: {e}")

def extract_json_robust(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(text)
    except Exception as e:
        logging.error(f"Gagal extract_json_robust: {e} | Teks: {text[:100]}...")
        return {"reply": text, "command": "", "save_memory": "", "send_file": "", "read_url": "", "download": {}}

def setup_provider():
    config = load_config()
    print(f"\n{CYAN}--- Setup Provider AI ---{RESET}")
    print(f"Provider saat ini: {YELLOW}{config['provider'].upper()}{RESET}")
    print("1. Google Gemini (Cloud / API Key)")
    print("2. Ollama (Local AI / Tanpa Internet)")
    print("3. OpenRouter (Gemma 4, Claude, dll)")
    
    pilihan = input(f"\n{GREEN}Pilih provider (1/2/3):{RESET} ").strip()
    if pilihan == '1':
        config["provider"] = "gemini"
        save_config(config)
        print(f"{BLUE}[Berhasil]{RESET} Provider diubah ke Gemini.")
        setup_gemini_credentials(config)
    elif pilihan == '2':
        config["provider"] = "ollama"
        save_config(config)
        print(f"{BLUE}[Berhasil]{RESET} Provider diubah ke Ollama.")
        setup_ollama_config(config)
    elif pilihan == '3':
        config["provider"] = "openrouter"
        save_config(config)
        print(f"{BLUE}[Berhasil]{RESET} Provider diubah ke OpenRouter.")
        setup_openrouter_credentials(config)
    else:
        print(f"{RED}[Error]{RESET} Pilihan tidak valid.")

def setup_gemini_credentials(config=None):
    if not config: config = load_config()
    print(f"\n{CYAN}--- Setup Gemini & Telegram ---{RESET}")
    if config.get("api_key"): print(f"{YELLOW}Gemini API Key sudah tersimpan.{RESET}")
    key = input(f"{GREEN}Masukkan Gemini API Key (kosongkan jika tidak ganti):{RESET} ").strip()
    if key: config["api_key"] = key
            
    if config.get("telegram_token"): print(f"{YELLOW}Telegram Bot Token sudah tersimpan.{RESET}")
    token = input(f"{GREEN}Masukkan Telegram Bot Token (kosongkan jika tidak ganti):{RESET} ").strip()
    if token: config["telegram_token"] = token
    save_config(config)
    print(f"{BLUE}[Selesai]{RESET} Konfigurasi Gemini disimpan!\n")

def setup_openrouter_credentials(config=None):
    if not config: config = load_config()
    print(f"\n{CYAN}--- Setup OpenRouter & Telegram ---{RESET}")
    if config.get("openrouter_api_key"): print(f"{YELLOW}OpenRouter API Key sudah tersimpan.{RESET}")
    key = input(f"{GREEN}Masukkan OpenRouter API Key (kosongkan jika tidak ganti):{RESET} ").strip()
    if key: config["openrouter_api_key"] = key
    
    curr_model = config.get("openrouter_model", DEFAULT_OPENROUTER_MODEL)
    print(f"\n{YELLOW}Model OpenRouter saat ini: {curr_model}{RESET}")
    model = input(f"{GREEN}Masukkan Model (kosongkan untuk tetap {curr_model}):{RESET} ").strip()
    if model: config["openrouter_model"] = model
            
    if config.get("telegram_token"): print(f"\n{YELLOW}Telegram Bot Token sudah tersimpan.{RESET}")
    token = input(f"{GREEN}Masukkan Telegram Bot Token (kosongkan jika tidak ganti):{RESET} ").strip()
    if token: config["telegram_token"] = token
    
    save_config(config)
    print(f"{BLUE}[Selesai]{RESET} Konfigurasi OpenRouter disimpan!\n")

def setup_ollama_config(config=None):
    if not config: config = load_config()
    print(f"\n{CYAN}--- Setup Ollama & Telegram ---{RESET}")
    
    curr_url = config.get("ollama_url", DEFAULT_OLLAMA_URL)
    print(f"{YELLOW}URL Ollama saat ini: {curr_url}{RESET}")
    url = input(f"{GREEN}Masukkan URL Ollama (kosongkan jika tidak ganti):{RESET} ").strip()
    if url: config["ollama_url"] = url
    
    curr_model = config.get("ollama_model", DEFAULT_OLLAMA_MODEL)
    print(f"\n{YELLOW}Model Ollama saat ini: {curr_model}{RESET}")
    model = input(f"{GREEN}Masukkan Nama Model:{RESET} ").strip()
    if model: config["ollama_model"] = model
    
    if config.get("telegram_token"): print(f"\n{YELLOW}Telegram Bot Token sudah tersimpan.{RESET}")
    token = input(f"{GREEN}Masukkan Telegram Bot Token (kosongkan jika tidak ganti):{RESET} ").strip()
    if token: config["telegram_token"] = token
            
    save_config(config)
    print(f"{BLUE}[Selesai]{RESET} Konfigurasi Ollama disimpan!\n")

def setup_model():
    config = load_config()
    if config["provider"] == "gemini":
        print(f"\n{CYAN}--- Pilih Model Gemini ---{RESET}")
        for key, name in AVAILABLE_GEMINI_MODELS.items(): print(f"{key}. {name}")
        pilihan = input(f"\n{GREEN}Pilih nomor model:{RESET} ").strip()
        if pilihan in AVAILABLE_GEMINI_MODELS:
            config["model"] = AVAILABLE_GEMINI_MODELS[pilihan]
            save_config(config)
            print(f"{BLUE}[Berhasil]{RESET} Model diubah menjadi {AVAILABLE_GEMINI_MODELS[pilihan]}\n")
    elif config["provider"] == "openrouter":
        setup_openrouter_credentials(config)
    else:
        setup_ollama_config(config)

def send_ai_request(history, retries=3):
    config = load_config()
    provider = config.get("provider", "gemini")
    
    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]

    memories = load_memories()
    memory_text = "\n".join([f"- {m}" for m in memories]) if memories else "Belum ada memori."
    
    system_instruction = (
        f"Anda adalah Autonomous AI Agent. "
        "Lingkungan: Termux Android. Interaksi via Telegram Bot.\n\n"
        f"🧠 [INGATAN PERMANEN ANDA]:\n{memory_text}\n\n"
        "KEMAMPUAN SUPER ANDA:\n"
        "1. FILE: Kirim file lokal ke Telegram (isikan path di 'send_file').\n"
        "2. INTERNET: Isikan URL pada 'read_url' untuk membacanya.\n"
        "3. WHATSAPP (MUDSLIDE):\n"
        "   - Kirim Teks: `npx mudslide send 628xxx \"Isi Pesan\"`\n"
        "   - Kirim Gambar: `npx mudslide send-image 628xxx path_gambar.jpg` (TANPA CAPTION)\n"
        "   - MENGIRIM GAMBAR + TEKS: `npx mudslide send-image 628xxx path.jpg && sleep 5 && npx mudslide send 628xxx \"Ini fotonya\"`\n"
        "   - ATURAN WAJIB NOMOR: Jika user memberi nomor '089512346025', perhatikan setiap angkanya! Ubah '08' menjadi '628', SISANYA HARUS PERSIS SAMA (jadi 6289512346025). JANGAN MENGHILANGKAN ANGKA!\n"
        "   - ATURAN WAJIB UPLOAD: Anda HARUS menyisipkan `&& sleep 5` setiap kali menggunakan perintah send-image agar file selesai diupload sebelum program tertutup.\n"
        "     Contoh benar: `npx mudslide send-image 6281234567890 gambar.jpg && sleep 5`\n"
        "4. DOWNLOAD INTERNET: Jika user meminta gambar, isikan JSON 'download' dengan url dan filename.\n"
        "   - TRIK GAMBAR: Gunakan URL `https://image.pollinations.ai/prompt/deskripsi_inggris` untuk generate gambar.\n\n"
        "PENTING: Output Anda HARUS berupa JSON valid tanpa teks tambahan dengan struktur:\n"
        "{\n"
        "  \"reply\": \"Pesan Anda ke pengguna\",\n"
        "  \"command\": \"perintah_shell_jika_ada_atau_kosong\",\n"
        "  \"save_memory\": \"fakta_baru_atau_kosong\",\n"
        "  \"send_file\": \"path_file_atau_kosong\",\n"
        "  \"read_url\": \"url_yg_mau_dibaca_atau_kosong\",\n"
        "  \"download\": {\"url\": \"\", \"filename\": \"\"}\n"
        "}"
    )

    if provider == "gemini":
        return send_gemini_request(config, history, system_instruction, retries)
    elif provider == "openrouter":
        return send_openrouter_request(config, history, system_instruction, retries)
    else:
        return send_ollama_request(config, history, system_instruction)

def send_openrouter_request(config, history, system_instruction, retries):
    api_key = config.get("openrouter_api_key", "").strip()
    model_name = config.get("openrouter_model", DEFAULT_OPENROUTER_MODEL)
    
    or_messages = [{"role": "system", "content": system_instruction}]
    for msg in history:
        role = "assistant" if msg["role"] == "model" else "user"
        content = msg["parts"][0]["text"]
        or_messages.append({"role": role, "content": content})

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/termux-agent", 
        "X-Title": "Autonomous Termux Agent"
    }
    
    payload = {
        "model": model_name,
        "messages": or_messages,
        "temperature": 0.7,
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 429:
                wait_time = (attempt + 1) * 3
                print(f"\n{YELLOW}[OpenRouter 429]{RESET} Rate limit tercapai. Mencoba ulang dalam {wait_time} detik...")
                time.sleep(wait_time)
                continue
                
            if response.status_code != 200:
                print(f"\n{RED}[OpenRouter Error Detail]{RESET}")
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")
                
            response.raise_for_status()
            data = response.json()
            
            if 'usage' in data:
                reasoning = data['usage'].get('reasoningTokens', 0)
                if reasoning > 0:
                    print(f"{YELLOW}[OpenRouter]{RESET} Reasoning Tokens: {reasoning}")
                    
            content = data['choices'][0]['message']['content']
            return extract_json_robust(content)
            
        except requests.exceptions.HTTPError as e:
            if attempt == retries - 1:
                try:
                    err_json = response.json()
                    err_msg = err_json.get("error", {}).get("message", str(e))
                except:
                    err_msg = str(e)
                logging.error(f"OpenRouter HTTP Error: {err_msg}")
                return {"reply": f"Terjadi kesalahan API OpenRouter: {err_msg}", "command": "", "save_memory": "", "send_file": "", "read_url": ""}
        except Exception as e:
            if attempt == retries - 1:
                logging.error(f"OpenRouter Fatal Error: {e}")
                return {"reply": f"Error OpenRouter: {str(e)}", "command": "", "save_memory": "", "send_file": "", "read_url": ""}
            
    return {"reply": f"Gagal merespons setelah {retries} percobaan karena server penuh (429 Rate Limit). Coba model lain.", "command": "", "save_memory": "", "send_file": "", "read_url": ""}

def send_gemini_request(config, history, system_instruction, retries):
    api_key = config.get("api_key", "").strip()
    model_name = config.get("model", DEFAULT_MODEL)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    data = {
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "contents": history,
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7}
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                return json.loads(text_response)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep((attempt + 1) * 3)
                continue
            logging.error(f"Gemini HTTPError: {e.code} - {e.reason}")
            return {"reply": f"Terjadi kesalahan API Gemini: {e.code} - {e.reason}", "command": "", "save_memory": "", "send_file": "", "read_url": ""}
        except Exception as e:
            logging.error(f"Gemini Exception: {e}")
            return {"reply": f"Terjadi kesalahan Gemini: {str(e)}", "command": "", "save_memory": "", "send_file": "", "read_url": ""}
    return {"reply": "Error: Terlalu banyak request (429).", "command": "", "save_memory": "", "send_file": "", "read_url": ""}

def send_ollama_request(config, history, system_instruction):
    ollama_url = config.get("ollama_url", DEFAULT_OLLAMA_URL).rstrip("/")
    model_name = config.get("ollama_model", DEFAULT_OLLAMA_MODEL)
    
    ollama_messages = [{"role": "system", "content": system_instruction}]
    for msg in history:
        role = "assistant" if msg["role"] == "model" else "user"
        content = msg["parts"][0]["text"]
        ollama_messages.append({"role": role, "content": content})
        
    payload = {
        "model": model_name,
        "messages": ollama_messages,
        "format": "json",       
        "stream": False,
        "options": {"temperature": 0.7}
    }
    
    try:
        response = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        content = data.get("message", {}).get("content", "")
        return extract_json_robust(content)
    except Exception as e:
         logging.error(f"Ollama Error: {e}")
         return {"reply": f"Error Ollama: {str(e)}", "command": "", "save_memory": "", "send_file": "", "read_url": ""}

def fetch_url_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.extract()
            
        text = soup.get_text(separator='\n')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text[:15000] + "\n\n...[Teks dipotong]"
    except Exception as e:
        logging.error(f"Fetch URL Error ({url}): {e}")
        return f"Gagal membaca URL: {str(e)}"

def start_telegram_bot():
    config = load_config()
    telegram_token = config.get("telegram_token")

    if not telegram_token:
        print(f"{RED}[Error]{RESET} Telegram Token belum disetup!")
        return

    bot = telebot.TeleBot(telegram_token)
    
    # Cetak UI Dashboard saat bot mulai
    term_width = get_terminal_width()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Header Frame
    print(f"{CYAN}╔" + "═" * (term_width - 2) + f"╗{RESET}")
    for line in ASCII_ART.strip('\n').split('\n'):
        print(f"{CYAN}║{MAGENTA}{line.center(term_width - 2)}{CYAN}║{RESET}")
    print(f"{CYAN}╠" + "═" * (term_width - 2) + f"╣{RESET}")
    
    print(f"{CYAN}║{YELLOW}{'🤖 AUTONOMOUS AGENT AKTIF 🚀'.center(term_width - 2)}{CYAN}║{RESET}")
    print(f"{CYAN}╚" + "═" * (term_width - 2) + f"╝{RESET}")
    
    if config['provider'] == 'gemini': active_model = config['model']
    elif config['provider'] == 'openrouter': active_model = config['openrouter_model']
    else: active_model = config['ollama_model']
    
    print(f"\n{WHITE}➤ Provider : {YELLOW}{config['provider'].upper()}{RESET}")
    print(f"{WHITE}➤ Model    : {YELLOW}{active_model}{RESET}")
    print(f"{WHITE}➤ Status   : {GREEN}Standby & Menunggu instruksi...{RESET}\n")

    @bot.message_handler(commands=['start', 'clear'])
    def handle_commands(message):
        user_histories[message.chat.id] = []
        bot.reply_to(message, "Riwayat dibersihkan. Agent siap!")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        chat_id = message.chat.id
        user_input = message.text

        if chat_id not in user_histories: user_histories[chat_id] = []

        bot.send_chat_action(chat_id, 'typing')
        user_histories[chat_id].append({"role": "user", "parts": [{"text": user_input}]})
        print(f"{BLUE}[Pesan]{RESET} {message.from_user.first_name}: {user_input}")

        response_json = send_ai_request(user_histories[chat_id])
        user_histories[chat_id].append({"role": "model", "parts": [{"text": json.dumps(response_json)}]})

        reply = response_json.get("reply", "")
        command = response_json.get("command", "")
        new_memory = response_json.get("save_memory", "")
        send_file_path = response_json.get("send_file", "")
        read_url = response_json.get("read_url", "")
        download_req = response_json.get("download", {})

        if new_memory:
            mems = load_memories()
            mems.append(new_memory)
            save_memories(mems)
            print(f"{YELLOW}🧠 [Memori]: {new_memory}{RESET}")

        if reply: bot.send_message(chat_id, reply)

        if isinstance(download_req, dict) and download_req.get("url"):
            dl_url = download_req["url"]
            dl_name = download_req.get("filename", "downloaded_file.jpg")
            print(f"{GREEN}[Download]{RESET} Mengunduh: {dl_url}")
            bot.send_message(chat_id, f"📥 Sedang mendownload gambar dari server ke sistem...")
            try:
                r = requests.get(dl_url, stream=True, timeout=30)
                r.raise_for_status()
                with open(dl_name, 'wb') as f:
                    for chunk in r.iter_content(1024): 
                        if chunk: f.write(chunk)
                
                sys_feedback = f"[SYSTEM FEEDBACK] Gambar berhasil didownload: {dl_name}. Lanjutkan mengirim gambar sesuai instruksi prompt utama (jangan lupa tambahkan && sleep 5)."
                user_histories[chat_id].append({"role": "user", "parts": [{"text": sys_feedback}]})
                
                bot.send_chat_action(chat_id, 'typing')
                next_resp = send_ai_request(user_histories[chat_id])
                user_histories[chat_id].append({"role": "model", "parts": [{"text": json.dumps(next_resp)}]})
                
                if next_resp.get("reply"): bot.send_message(chat_id, next_resp["reply"])
                if next_resp.get("command"):
                    command = next_resp["command"] 
                    
            except Exception as e:
                bot.send_message(chat_id, f"❌ Gagal mendownload gambar: {e}")
                sys_feedback = f"[SYSTEM FEEDBACK] Gagal download file: {e}. Beritahu pengguna."
                user_histories[chat_id].append({"role": "user", "parts": [{"text": sys_feedback}]})

        if read_url:
            print(f"{GREEN}[Web Reader]{RESET} Membaca URL: {read_url}")
            bot.send_chat_action(chat_id, 'typing') 
            
            url_content = fetch_url_content(read_url)
            sys_feedback = f"[SYSTEM FEEDBACK]\nKonten web:\n{url_content}\nSilakan jawab/rangkum."
            user_histories[chat_id].append({"role": "user", "parts": [{"text": sys_feedback}]})
            
            bot.send_chat_action(chat_id, 'typing')
            resp_json_url = send_ai_request(user_histories[chat_id])
            user_histories[chat_id].append({"role": "model", "parts": [{"text": json.dumps(resp_json_url)}]})
            if resp_json_url.get("reply"): bot.send_message(chat_id, f"📄 *Analisis Web:*\n{resp_json_url['reply']}", parse_mode="Markdown")

        if send_file_path:
            send_file_path = os.path.expanduser(send_file_path)
            if os.path.exists(send_file_path):
                bot.send_chat_action(chat_id, 'upload_document')
                with open(send_file_path, 'rb') as f: bot.send_document(chat_id, f)

        if command:
            pending_commands[chat_id] = command
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ Izinkan Eksekusi", callback_data="exec_y"), InlineKeyboardButton("❌ Batal", callback_data="exec_n"))
            bot.send_message(chat_id, f"💻 *Perintah Sistem:*\n`{command}`", reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if chat_id not in pending_commands: return
        command = pending_commands[chat_id]
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None) 

        if call.data == "exec_y":
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=45)
                output = result.stdout.strip()
                if result.stderr: output += "\n" + result.stderr.strip()
                if not output: output = "Perintah berhasil dijalankan tanpa output teks."
                if len(output) > 2000: output = output[:2000] + "\n...[Output dipotong]"

                bot.send_message(chat_id, f"✅ Selesai.\nOutput (sebagian):\n`{output[:300]}...`", parse_mode="Markdown")

                sys_feedback = f"[SYSTEM FEEDBACK] Hasil command:\n{output}\nInfo ini hanya untuk catatan Anda. Jawab 'Oke' saja."
                user_histories[chat_id].append({"role": "user", "parts": [{"text": sys_feedback}]})
                
                send_ai_request(user_histories[chat_id])

            except subprocess.TimeoutExpired:
                 bot.send_message(chat_id, f"✅ Perintah masih berjalan di latar belakang (Timeout menunggu, tapi proses tetap lanjut).")
            except Exception as e:
                logging.error(f"Command Eksekusi Error: {e}")
                bot.send_message(chat_id, f"❌ Gagal: {e}")
            del pending_commands[chat_id]
        elif call.data == "exec_n":
            bot.send_message(chat_id, "🛑 Eksekusi Dibatalkan.")
            del pending_commands[chat_id]

    while True:
        try: 
            bot.polling(none_stop=True)
            break # Berhenti jika bot di-stop secara normal
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Bot dihentikan oleh pengguna (Ctrl+C).{RESET}")
            break
        except Exception as e: 
            logging.error(f"Telegram Bot Polling Terputus: {e}")
            print(f"\n{RED}[Error]{RESET} Koneksi Terputus: {e}")
            print(f"{YELLOW}Mencoba menghubungkan kembali dalam 5 detik (Auto-Restart)...{RESET}")
            time.sleep(5)

def sync_with_github():
    print(f"\n{CYAN}--- Sinkronisasi Otomatis GitHub ---{RESET}")
    if not shutil.which("git"):
        print(f"{RED}❌ Git belum terinstall! Install dengan: pkg install git{RESET}\n")
        return
        
    if not os.path.exists(".git"):
        print(f"{YELLOW}⚠️ Folder ini belum menjadi repository Git.{RESET}")
        print(f"{WHITE}Silakan ikuti instruksi inisialisasi di terminal terlebih dahulu.{RESET}\n")
        return
        
    try:
        print(f"{WHITE}📥 Menarik perubahan terbaru (git pull)...{RESET}")
        subprocess.run("git pull origin main", shell=True)
        
        print(f"{WHITE}➕ Menambahkan file (git add .)...{RESET}")
        subprocess.run("git add .", shell=True)
        
        print(f"{WHITE}📝 Membuat commit...{RESET}")
        commit_msg = f"Auto-sync: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(f'git commit -m "{commit_msg}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"{WHITE}🚀 Mengirim ke GitHub (git push)...{RESET}")
        res = subprocess.run("git push origin main", shell=True)
        
        if res.returncode == 0: print(f"{GREEN}✅ Sinkronisasi ke GitHub berhasil!{RESET}\n")
        else: print(f"{RED}❌ Gagal Push. Pastikan koneksi & Autentikasi GitHub sudah benar.{RESET}\n")
    except Exception as e: 
        logging.error(f"GitHub Sync Error: {e}")
        print(f"{RED}❌ Terjadi kesalahan saat sinkronisasi: {e}{RESET}\n")

# Variabel global untuk memastikan splash screen hanya dipanggil sekali
has_run_splash = False

def main():
    global has_run_splash
    if not has_run_splash:
        show_splash_screen()
        check_dependencies()
        print(f"\n{CYAN}--------------------------------------------------------------{RESET}\n")
        has_run_splash = True
        
    while True:
        config = load_config()
        prov = config.get("provider", "gemini").upper()
        
        # UI Menu Utama 
        term_width = get_terminal_width()
        print(f"{CYAN}┌" + "─" * (term_width - 2) + f"┐{RESET}")
        print(f"{CYAN}│{YELLOW}{'MENU DASHBOARD UTAMA'.center(term_width - 2)}{CYAN}│{RESET}")
        print(f"{CYAN}└" + "─" * (term_width - 2) + f"┘{RESET}")
        print(f" {WHITE}1.{RESET} Jalankan Bot {GREEN}[Aktif: {prov}]{RESET}")
        print(f" {WHITE}2.{RESET} Setup Provider AI (Gemini / Ollama / OpenRouter)")
        print(f" {WHITE}3.{RESET} Ganti Model Spesifik")
        print(f" {WHITE}4.{RESET} Sinkronisasi ke GitHub (Auto Pull & Push)")
        print(f" {WHITE}5.{RESET} Keluar")
        
        try:
            pilihan = input(f"\n{GREEN}➤ Pilih menu (1-5):{RESET} ")
            if pilihan == '1': start_telegram_bot()
            elif pilihan == '2': setup_provider()
            elif pilihan == '3': setup_model()
            elif pilihan == '4': sync_with_github()
            elif pilihan == '5': sys.exit(0)
        except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__":
    main()