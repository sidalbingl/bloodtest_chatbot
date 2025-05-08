from prompt_helper import build_prompt
import os
import logging
import requests
import json
from dotenv import load_dotenv
from json_analyzer import analyze_latest_json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

class ModelHandler:
    def __init__(self):
        self.chat_history = []

    def process_text(self, text: str) -> str:
        try:
            logger.info(f"Gelen metin: {text}")

            # Analiz et komutu gelirse model kullanmadan direkt sonucu ver
            if "analiz et" in text.lower():
                return analyze_latest_json()

            # Normal prompt işle
            prompt = build_prompt(text)
            print("📤 Modele giden prompt:", prompt)

            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0  # model susturulur
                }
            })

            if response.status_code == 200:
                output = response.json()["response"]
                self.chat_history.append({"role": "user", "content": text})
                self.chat_history.append({"role": "assistant", "content": output})
                return output.strip()
            else:
                return f"Modelden yanıt alınamadı: {response.status_code}"

        except Exception as e:
            return f"Hata oluştu: {str(e)}"

model_handler = ModelHandler()
