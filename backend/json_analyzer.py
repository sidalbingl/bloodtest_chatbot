import json
import os
import re

PARSED_FILE = "parsed/latest.json"
ADVICE_FILE = "backend/advice_dataset.json"

def analyze_latest_json():
    if not os.path.exists(PARSED_FILE):
        return "Henüz analiz yapılacak veri bulunamadı."

    with open(PARSED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    advice_data = []
    if os.path.exists(ADVICE_FILE):
        with open(ADVICE_FILE, "r", encoding="utf-8") as af:
            advice_data = json.load(af)

    lines = []
    index = 1

    for test, info in data.items():
        try:
            value = float(info["value"])
            ref = info.get("ref", "")
            unit = info.get("unit", "")

            match = re.match(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", ref)
            if match:
                ref_low = float(match.group(1))
                ref_high = float(match.group(2))
                durum = None

                if value < ref_low:
                    durum = "Düşük"
                    durum_emoji = "🔻"
                elif value > ref_high:
                    durum = "Yüksek"
                    durum_emoji = "🔺"
                else:
                    continue

                # Öneri veri setinden eşleşen açıklama ve öneri bul
                matched_advice = next(
                    (item for item in advice_data if item["tahlil_adi"].strip().lower() == test.strip().lower()
                     and item["durum"].lower() == durum.lower()), None
                )

                explanation = matched_advice["aciklama"] if matched_advice else "Açıklama bulunamadı."
                recommendation = matched_advice["oneri"] if matched_advice else "Öneri bulunamadı."

                lines.append(
                    f"{index}. {durum_emoji} {test} - Değer: {value} {unit} - Referans: {ref}\n"
                    f"   Açıklama: {explanation}\n"
                    f"   Öneri: {recommendation}"
                )
                index += 1

        except Exception as e:
            continue

    if not lines:
        return "Tüm test sonuçları referans aralığında."

    return "🚨 Anormal Test Sonuçları:\n\n" + "\n\n".join(lines)
