import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openrouter")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-4o")
    FALLBACK_PROVIDER = os.getenv("FALLBACK_PROVIDER", "groq")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "llama-3.3-70b-versatile")
    
    TIMEOUT = 30 # Detik