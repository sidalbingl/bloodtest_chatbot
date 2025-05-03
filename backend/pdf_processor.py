import os
import fitz  # PyMuPDF
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        os.makedirs("parsed", exist_ok=True)

    def parse_blood_test_results(self, text: str) -> dict:
        try:
            results = {}

            # Normal test formatı (adı, değer, birim, referans aralığı varsa)
            pattern_normal = r'([A-ZÇĞİÖŞÜa-zçğıöşüA-Z()/%\s\d]+?)\s+([\d.,]+)\s+([a-zA-Zµ/%]+)?\s*([\d.,\-<> ]*)'
            # Basit pozitif/negatif testler
            pattern_simple = r'([A-ZÇĞİÖŞÜa-zçğıöşüA-Z()/%\s\d]+?)\s+([\d.,]+)\s+(Negatif|Pozitif)'

            matches = re.findall(pattern_normal, text)
            for match in matches:
                test_name, value, unit, ref = match
                try:
                    test_name = test_name.strip()
                    value = float(value.replace(',', '.'))
                    results[test_name] = {
                        "value": value,
                        "unit": unit.strip() if unit else "",
                        "ref": ref.strip() if ref else ""
                    }
                except ValueError:
                    continue

            if not results:
                matches = re.findall(pattern_simple, text)
                for match in matches:
                    test_name, value, result_status = match
                    try:
                        results[test_name.strip()] = {
                            "value": float(value.replace(',', '.')),
                            "unit": result_status,
                            "ref": ""
                        }
                    except ValueError:
                        continue

            return results
        except Exception as e:
            logger.error(f"Sonuç ayrıştırma hatası: {str(e)}")
            return {}

    def process_pdf(self, file_path: str):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()

            print("\U0001F4C4 PDF metni:\n", text)

            results = self.parse_blood_test_results(text)

            if results:
                summary = f"Toplam {len(results)} test değeri başarıyla ayrıştırıldı."
            else:
                summary = "Hiçbir test değeri ayrıştırılamadı."

            # Dosya adını kaydetme
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            save_path = os.path.join("parsed", f"{base_filename}.json")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            return results, summary

        except Exception as e:
            logger.error(f"PDF işleme hatası: {str(e)}")
            return {}, "PDF işlenemedi."

# Örnek kullanım
if __name__ == "__main__":
    processor = PDFProcessor()
    results, summary = processor.process_pdf("path_to_pdf.pdf")
    print(summary)
