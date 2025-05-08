import json
import os

ADVICE_FILE = "advice_dataset.json"

def load_advice():
    if not os.path.exists(ADVICE_FILE):
        return {}

    with open(ADVICE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_advice_for_test(test_name: str) -> dict:
    data = load_advice()
    for item in data:
        if item["tahlil_adi"].strip().lower() in test_name.strip().lower():
            return item
    return {}
