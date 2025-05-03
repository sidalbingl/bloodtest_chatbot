import re

def detect_language(text: str) -> str:
    """
    Kullanıcının girdiği metnin dilini belirler (basit kontrol).
    """
    turkish_keywords = ["merhaba", "analiz", "değer", "yüksek", "düşük", "sonuç", "nedir", "lütfen"]
    if any(word in text.lower() for word in turkish_keywords):
        return "tr"
    return "en"

def build_prompt(user_input: str, analyzed_data: str = "") -> str:
    lang = detect_language(user_input)

    if lang == "tr":
        base_instruction = (
            "Sen bir yapay zeka destekli tıbbi asistanısın. "
            "Kullanıcının son kan tahliline göre sadece mevcut test sonuçlarını değerlendir. "
            "Veri bulunmayan testler hakkında yorum yapma ve uydurma bilgi verme. "
            "Eğer önemli eksik test varsa, yalnızca testin yapılmasını öner.\n\n"
        )
        if "analiz et" in user_input.lower():
            return (
                base_instruction +
                "Kullanıcının kan tahlil sonuçları aşağıda yer almaktadır:\n" +
                analyzed_data +
                "\n\nLütfen sadece yüksek ya da düşük sonuçlara odaklan. "
                "Her anormal sonuç için kısa ve halkın anlayacağı şekilde açıklama yap. "
                "Referans aralıklarına göre değerlendir. "
                "Test sonucu eksikse yorum yapma."
            )
        return (
            base_instruction +
            f"Kullanıcının sorusu: {user_input}\n"
            "Soru kan tahliliyle ilgiliyse mevcut verileri kullanarak yorum yap. "
            "Eğer test sonucu eksikse belirt ama yorum yapma. "
            "Soru farklı bir konudaysa sadece genel sağlık bilgisiyle cevapla."
        )
    
    else:  # English prompt
        base_instruction = (
            "You are a medical assistant powered by AI. "
            "Evaluate only the available test results from the user's latest blood test. "
            "Do not invent or assume values. "
            "If an important test is missing, only recommend doing the test.\n\n"
        )
        if "analyze" in user_input.lower():
            return (
                base_instruction +
                "User's blood test results:\n" +
                analyzed_data +
                "\n\nPlease focus only on abnormal (high or low) values. "
                "Explain briefly in simple language for each abnormal result."
            )
        return (
            base_instruction +
            f"User question: {user_input}\n"
            "If the question is about lab results, use the data provided. "
            "If it's about general health, give a helpful medical response accordingly."
        )
