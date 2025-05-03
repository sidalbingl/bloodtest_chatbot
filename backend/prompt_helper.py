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
            "Lütfen yalnızca açık, kısa ve öz cümlelerle cevap ver. "
            "Gereksiz tekrar yapma. Anlatım halk diliyle sade olsun. "
            "Tıbbi analizde sadece mevcut değerlere göre konuş. "
            "Eksik testler hakkında yorum yapma, sadece 'test sonucu yok' de.\n\n"
        )
        if "analiz et" in user_input.lower():
            return (
                base_instruction +
                "Kullanıcının kan tahlili sonuçları:\n" +
                analyzed_data +
                "\n\nYalnızca yüksek veya düşük değerlere kısa açıklama yap. "
                "Her madde tek satır olmalı. Örneğin: 'Glukoz: Yüksek Normal aralık bu olmalı ancak sizin değeriniz şu kadar'"
            )
        return (
            base_instruction +
            f"Soru: {user_input}\n"
            "Soruda geçen test değerleri sadece varsa analiz et. Her açıklama kısa, net ve anlaşılır olmalı. "
            "Genel yorum yapma, sadece ilgili veriye cevap ver."
        )
    
    else:
        base_instruction = (
            "You are an AI-powered medical assistant. "
            "Please reply only with short, clear, and direct sentences. "
            "Avoid unnecessary elaboration. Use plain English. "
            "Only discuss existing values. Do not speculate about missing ones.\n\n"
        )
        if "analyze" in user_input.lower():
            return (
                base_instruction +
                "User's blood test results:\n" +
                analyzed_data +
                "\n\nFocus only on abnormal values. Respond with brief explanations like: "
                "'1. Glucose: High – Possible reason: insulin resistance.'"
            )
        return (
            base_instruction +
            f"User question: {user_input}\n"
            "Answer only based on available test data. Keep your response short and simple. "
            "Do not provide general or unrelated information."
        )
