import re

def detect_language(text: str) -> str:
    turkish_keywords = ["merhaba", "analiz", "değer", "yüksek", "düşük", "sonuç", "nedir", "lütfen"]
    if any(word in text.lower() for word in turkish_keywords):
        return "tr"
    return "en"

def build_prompt(user_input: str, analyzed_data: str = "") -> str:
    lang = detect_language(user_input)

    if lang == "tr":
        base_instruction = (
            "Sen bir yapay zeka destekli tıbbi asistansın. "
            "Yalnızca kullanıcının mevcut test sonuçlarına dayalı olarak cevap ver. "
            "Eksik testlere dair uydurma bilgi verme. "
            "Anormal değer varsa kısa açıklama yap ve uygun önerileri sun.\n\n"
        )

        if "analiz et" in user_input.lower():
            return (
                base_instruction +
                "Kullanıcının test analiz sonuçları aşağıdadır:\n\n" +
                analyzed_data +
                "\n\nYukarıdaki bilgilere dayanarak sadece tespit edilen anormal sonuçlar için açıklama ve öneri sun."
            )

        return (
            base_instruction +
            f"Kullanıcının sorusu: {user_input}\n"
            "Cevabını sadece mevcut verilere dayandır. Eksik testlere dair yorum yapma."
        )

    else:
        base_instruction = (
            "You are an AI-powered medical assistant. "
            "Only provide answers based on existing test data. "
            "Do not assume or fabricate missing results. Focus on actual abnormalities and provide short explanations and recommendations.\n\n"
        )

        if "analyze" in user_input.lower():
            return (
                base_instruction +
                "User's test analysis results:\n\n" +
                analyzed_data +
                "\n\nBased on the above, briefly explain the abnormal results and give helpful suggestions."
            )

        return (
            base_instruction +
            f"User question: {user_input}\n"
            "Answer only based on the available data. Avoid speculation or irrelevant detail."
        )
