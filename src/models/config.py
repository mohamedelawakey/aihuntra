from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_URL = os.getenv("OPENAI_URL")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0"))
