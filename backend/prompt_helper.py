import re

# Dahili bilgi tabanı (veri seti)
advice_entries = [
    {
        "tahlil": "albumin",
        "durum": "yüksek",
        "cevap": "Yüksek albümin genellikle vücudun susuz kaldığını gösterir. Su tüketiminizi artırın."
    },
    {
        "tahlil": "laktat dehidrogenaz",
        "durum": "düşük",
        "cevap": "Düşük laktat dehidrogenaz nadirdir, test tekrarı veya genetik durumlar için doktor kontrolü önerilir."
    },
    {
        "tahlil": "ldl kolesterol",
        "durum": "düşük",
        "cevap": "Düşük LDL kolesterol hormonal veya beslenmeye bağlı olabilir. Doktorla değerlendirin."
    },
    {
        "tahlil": "hidroksi vitamin d",
        "durum": "düşük",
        "cevap": "Düşük D vitamini bağışıklık ve kemik sağlığını etkiler. Güneşlenin, takviye alın."
    },
    {
        "tahlil": "pdw",
        "durum": "yüksek",
        "cevap": "Yüksek PDW inflamasyon göstergesi olabilir. Tam kan sayımı ile birlikte değerlendirilmelidir."
    },
    {
        "tahlil": "mcv",
        "durum": "düşük",
        "cevap": "Düşük MCV değeri genellikle demir eksikliği anemisine işaret eder. Demir takviyesi önerilir."
    }
]

def detect_language(text: str) -> str:
    turkish_keywords = ["merhaba", "analiz", "değer", "yüksek", "düşük", "sonuç", "nedir", "lütfen"]
    if any(word in text.lower() for word in turkish_keywords):
        return "tr"
    return "en"

def find_response_in_prompt_dataset(text: str) -> str:
    text = text.lower()
    for item in advice_entries:
        if item["tahlil"] in text and item["durum"] in text:
            return item["cevap"]
    return ""

def build_prompt(user_input: str, analyzed_data: str = "") -> str:
    lang = detect_language(user_input)

    if lang == "tr":
        if "analiz et" in user_input.lower():
            return analyzed_data  # bu kısmı aynen koruduk ❤️

        matched = find_response_in_prompt_dataset(user_input)
        if matched:
            return matched  # sadece verilen cevabı gönderiyoruz

        return (
            f"Kullanıcının sorusu: {user_input}\n"
            "Eğer analiz edilmiş veri varsa ona dayanarak kısa ve anlaşılır cevap ver. "
            "Varsa advice_dataset içeriğini kullan. Eksik testler hakkında yorum yapma."
            "Hiçbir ekleme, çıkarma, açıklama, öneri, yorum veya yorumlama yapma. Sadece metni döndür:\n\n{matched}"
        )

    else:
        if "analyze" in user_input.lower():
            return analyzed_data

        return (
            f"User question: {user_input}\n"
            "Answer briefly and clearly based on available analyzed data. Avoid assumptions."
        )
