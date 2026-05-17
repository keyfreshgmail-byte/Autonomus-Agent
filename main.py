import os
import json
import time
import logging
from config import Config

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory", "memory.json")

SYSTEM_PROMPT = """You are a highly capable, autonomous AI assistant.
Your primary goal is to provide accurate, professional, and structured answers.
Always consider the user's permanent memory context below before replying.
"""

# ==========================================
# MANAJEMEN MEMORI
# ==========================================
def read_memory() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading memory: {e}")
        return {}

def save_memory(key: str, value: str):
    memories = read_memory()
    memories[key] = value
    try:
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memories, f, indent=4)
        logging.info(f"Memory saved: {key}")
    except Exception as e:
        logging.error(f"Error saving memory: {e}")

def forget_memory(key: str):
    memories = read_memory()
    if key in memories:
        del memories[key]
        try:
            with open(MEMORY_FILE, 'w') as f:
                json.dump(memories, f, indent=4)
            logging.info(f"Memory erased: {key}")
        except Exception as e:
            logging.error(f"Error erasing memory: {e}")

# ==========================================
# ROUTER PROVIDER
# ==========================================
def route_provider(provider: str, model: str, prompt: str, system_context: str) -> str:
    prov = provider.lower()
    if prov == "openrouter":
        from providers.openrouter_provider import generate
        return generate(prompt, system_context, model, Config.OPENROUTER_API_KEY, Config.TIMEOUT)
    elif prov == "openai":
        from providers.openai_provider import generate
        return generate(prompt, system_context, model, Config.OPENAI_API_KEY, Config.TIMEOUT)
    elif prov == "groq":
        from providers.groq_provider import generate
        return generate(prompt, system_context, model, Config.GROQ_API_KEY, Config.TIMEOUT)
    elif prov == "gemini":
        from providers.gemini_provider import generate
        return generate(prompt, system_context, model, Config.GEMINI_API_KEY, Config.TIMEOUT)
    elif prov == "anthropic":
        from providers.anthropic_provider import generate
        return generate(prompt, system_context, model, Config.ANTHROPIC_API_KEY, Config.TIMEOUT)
    elif prov == "ollama":
        from providers.ollama_provider import generate
        return generate(prompt, system_context, model, Config.OLLAMA_BASE_URL, Config.TIMEOUT)
    else:
        raise ValueError(f"Provider {prov} tidak dikenali.")

# ==========================================
# FUNGSI UTAMA AI DENGAN RETRY & FALLBACK
# ==========================================
def ask_ai(prompt: str) -> str:
    memories = read_memory()
    dynamic_system_prompt = SYSTEM_PROMPT
    if memories:
        dynamic_system_prompt += f"\n\n[USER MEMORY DATA]:\n{json.dumps(memories, indent=2)}"

    def attempt_request(provider, model):
        retries = 2
        for i in range(retries):
            try:
                logging.info(f"Mengirim request ke {provider} (Model: {model}) - Attempt {i+1}")
                response = route_provider(provider, model, prompt, dynamic_system_prompt)
                return response
            except Exception as e:
                logging.error(f"Gagal request {provider}: {e}")
                if i < retries - 1:
                    time.sleep(2) # Delay sebelum retry
        return None

    # 1. Coba Provider Utama
    response = attempt_request(Config.DEFAULT_PROVIDER, Config.DEFAULT_MODEL)
    if response: return response

    # 2. Jika Gagal, Auto-Fallback
    logging.warning(f"Provider utama tumbang. Beralih ke fallback: {Config.FALLBACK_PROVIDER}")
    response = attempt_request(Config.FALLBACK_PROVIDER, Config.FALLBACK_MODEL)
    if response: return response

    return "Maaf, sistem AI sedang mengalami gangguan pada semua provider jaringan."

# ==========================================
# TESTING AREA
# ==========================================
if __name__ == "__main__":
    print("==== MENJALANKAN SYSTEM AI ====")
    # Contoh Memory Test
    save_memory("name", "Komandan Cyber")
    save_memory("role", "Software Engineer")
    
    # Contoh AI Request
    pertanyaan = "Siapa nama saya dan apa pekerjaan saya berdasarkan ingatanmu?"
    jawaban = ask_ai(pertanyaan)
    print(f"\n[AI]: {jawaban}")