import json
import os
import re

PARSED_FILE = "parsed/latest.json"

def analyze_latest_json():
    if not os.path.exists(PARSED_FILE):
        return "Henüz analiz yapılacak veri bulunamadı."

    with open(PARSED_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    index = 1

    for test, info in data.items():
        try:
            value = float(info["value"])
            ref = info["ref"]
            unit = info.get("unit", "")

            match = re.match(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", ref)
            if match:
                ref_low = float(match.group(1))
                ref_high = float(match.group(2))
                if value < ref_low:
                    status = "🔻 DÜŞÜK"
                elif value > ref_high:
                    status = "🔺 YÜKSEK"
                else:
                    continue  # normalse ekleme

                lines.append(f"{index}. {status} {test}\n   - Değer: {value} {unit}\n   - Referans: {ref}\n   - Durum: {status.split()[1]}")
                index += 1

        except Exception as e:
            continue  # sorunlu satırları atla

    if not lines:
        return "Tüm test sonuçları referans aralığında."

    return "🚨 Anormal Test Sonuçları:<br><br>" + "<br><br>".join(lines)

