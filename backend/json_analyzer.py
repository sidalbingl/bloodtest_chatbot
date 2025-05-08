import json
import os
import re
import unicodedata

PARSED_FILE = "parsed/latest.json"

def normalize(text):
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = text.replace("\n", " ")
    text = text.replace("(", "").replace(")", "")
    text = text.replace("serum/plazma", "")
    text = re.sub(r"\b00\b", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def analyze_latest_json():
    if not os.path.exists(PARSED_FILE):
        return "Henüz analiz yapılacak veri bulunamadı."

    with open(PARSED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    index = 1

    for test, info in data.items():
        try:
            value_raw = str(info.get("value", "")).replace(",", ".").strip()
            value = float(re.findall(r"[-+]?[0-9]*\.?[0-9]+", value_raw)[0])

            ref = info.get("ref", "").strip()
            unit = info.get("unit", "")

            match = re.match(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", ref)
            if not match:
                continue

            ref_low = float(match.group(1))
            ref_high = float(match.group(2))

            if value < ref_low:
                durum = "Düşük"
                emoji = "🔻"
            elif value > ref_high:
                durum = "Yüksek"
                emoji = "🔺"
            else:
                continue

            lines.append(f"{index}. {emoji} {test.strip()} - Değer: {value} {unit} - Referans: {ref}")
            index += 1

        except Exception:
            continue

    return "🚨 Anormal Test Sonuçları:\n\n" + "\n".join(lines) if lines else "Tüm test sonuçları referans aralığında."