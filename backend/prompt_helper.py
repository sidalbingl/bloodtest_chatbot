import re

# Dahili bilgi tabanı (veri seti)
advice_entries = [
    {
        "tahlil": "albumin",
        "durum": "yüksek",
        "cevap": "Yüksek albümin seviyesi genellikle vücudun susuz kaldığını (dehidrasyon) gösterir. Ayrıca bazı böbrek veya karaciğer problemleriyle de ilişkili olabilir. Günlük su tüketiminizi artırın ve yeterli sıvı aldığınızdan emin olun. Durumun altında yatan başka bir neden olup olmadığını belirlemek için mutlaka doktorunuza danışın."
    },
    {
        "tahlil": "laktat dehidrogenaz",
        "durum": "düşük",
        "cevap": "Düşük laktat dehidrogenaz (LDH) nadir görülür ve çoğunlukla klinik olarak belirgin bir anlam taşımaz. Ancak bazı genetik enzim eksiklikleri veya laboratuvar hataları bu sonuca yol açabilir. Testin tekrarlanması ve uzman görüşü alınması önemlidir. Kesin değerlendirme için doktorunuza başvurun."
    },
    {
        "tahlil": "ldl kolesterol",
        "durum": "düşük",
        "cevap": "Düşük LDL kolesterol düzeyleri bazı durumlarda olumlu görülse de, aşırı düşüklük hormonal bozukluklar (örneğin tiroit sorunları), yetersiz yağ alımı, emilim bozuklukları veya bazı genetik durumlara bağlı olabilir. Beslenme düzeniniz gözden geçirilmeli ve gerekli görülürse yağ dengesi sağlanmalıdır. Detaylı değerlendirme ve uygun yönlendirme için doktorunuza danışın."
    },
    {
        "tahlil": "hidroksi vitamin d",
        "durum": "düşük",
        "cevap": "Düşük D vitamini seviyesi bağışıklık sistemini zayıflatabilir, kemik sağlığını olumsuz etkileyebilir ve yorgunluk, kas ağrıları gibi semptomlara neden olabilir. Günde 10-15 dakika güneş ışığına maruz kalmak, D vitamini içeren besinler (örneğin yağlı balık, yumurta) tüketmek ve D3 vitamini takviyesi almak faydalı olabilir. Doz ve uygulama süresi kişisel faktörlere göre değişir; bu nedenle mutlaka doktorunuza danışarak hareket edin."
    },
    {
        "tahlil": "pdw",
        "durum": "yüksek",
        "cevap": "Yüksek PDW (Platelet Distribution Width) değeri, trombosit boyutlarında artmış çeşitlilik olduğunu ve olası inflamasyon, enfeksiyon veya bazı hematolojik durumları işaret edebileceğini gösterir. Ancak tek başına tanı koymak için yeterli değildir. Diğer parametrelerle (trombosit sayısı, MPV, CRP, ESR gibi) birlikte değerlendirilmelidir. Net sonuçlar ve doğru yönlendirme için doktor kontrolü şarttır"
    },
    {
        "tahlil": "mcv",
        "durum": "düşük",
        "cevap": "Düşük MCV (Mean Corpuscular Volume), yani kırmızı kan hücrelerinin ortalama hacminin düşük olması genellikle demir eksikliği anemisini gösterir. Bu durumda halsizlik, baş dönmesi, çarpıntı gibi belirtiler görülebilir. Demir içeriği yüksek besinler (örneğin kırmızı et, yeşil yapraklı sebzeler) tüketilmeli ve gerekirse demir takviyesi alınmalıdır. Tedaviye başlamadan önce mutlaka doktorunuza danışın."
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
            return analyzed_data  

        matched = find_response_in_prompt_dataset(user_input)
        if matched:
            return matched  # sadece verilen cevabı gönderiyoruz

        return (
            f"Kullanıcının sorusu: {user_input}\n"
            "Sen bir sağlık chatbotusun.Türkçe ve anlaşılır bir şekilde cevap ver. Cevaplarını mümkün olduğunca basit ve net tut. "
            "Eğer analiz edilmiş veri varsa ona dayanarak kısa ve anlaşılır cevap ver. "
            "Genelleme yapma, test dışı tahminde bulunma. Eğer değer düşükse neden düşük olabileceğini ve önerileri belirt."
            "Hiçbir ekleme, çıkarma, açıklama, öneri, yorum veya yorumlama yapma. Sadece metni döndür:\n\n{matched}"
            "Eğer değer yüksekse neden yüksek olabileceğini ve yapılması gerekenleri belirt."
        )

    else:
        if "analyze" in user_input.lower():
            return analyzed_data

        return (
            f"User question: {user_input}\n"
            "You are a health chatbot. Answer in Turkish and understandable. Keep your answers as simple and clear as possible."
            "Answer briefly and clearly based on available analyzed data. Avoid assumptions."
            "Answer clearly based on analyzed blood test results if available. "
            "Explain why values might be high or low and suggest actionable steps."
        )
