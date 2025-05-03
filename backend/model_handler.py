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
PARSED_FILE = "parsed/latest.json"

class ModelHandler:
    def __init__(self):
        self.chat_history = []

    def process_text(self, text: str) -> str:
        try:
            logger.info(f"Gelen metin: {text}")

            # Eğer analiz et komutu varsa JSON'dan analizleri al
            json_analysis = ""
            if "analiz et" in text.lower() or "analyze" in text.lower():
                json_analysis = analyze_latest_json()

            # Prompt oluştur
            prompt = build_prompt(text, analyzed_data=json_analysis)

            # Ollama'ya istek gönder
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            })

            if response.status_code == 200:
                output = response.json()["response"]
                logger.info(f"Oluşturulan yanıt: {output}")

                self.chat_history.append({"role": "user", "content": text})
                self.chat_history.append({"role": "assistant", "content": output})

                return output.strip()
            else:
                logger.error(f"API hatası: {response.status_code} - {response.text}")
                return "Modelden yanıt alınamadı."

        except Exception as e:
            logger.error(f"Metin işleme hatası: {str(e)}")
            return f"Hata oluştu: {str(e)}"

model_handler = ModelHandler()
