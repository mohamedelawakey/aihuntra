from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
from .config import Config
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class Model:
    @staticmethod
    def ollama_model():

        model = OllamaLLM(
            model = Config.OLLAMA_MODEL,
            base_url = Config.OLLAMA_URL,
            temperature=Config.OLLAMA_TEMPERATURE
        )

        return model

    @staticmethod
    def openai_model():

        model = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            base_url=Config.OPENAI_URL,
            temperature=Config.OPENAI_TEMPERATURE
        )

        return model
