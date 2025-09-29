import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor  # import functions

def test_pdf_extraction():
    pdf_path = "data/sample_un.pdf"
    print(f"Looking for PDF at: {os.path.abspath(pdf_path)}")
    if os.path.exists(pdf_path):
        text = extractor.extract_text_from_pdf(pdf_path)
        norm_text = extractor.normalize_text(text)
        fields = extractor.extract_fields(norm_text)  # ✅ updated here
        print("\n--- Extracted PDF Text ---\n")
        print(norm_text)
        print("\n--- Extracted Fields ---\n")
        for k, v in fields.items():
            print(f"{k}: {v}")
    else:
        print("⚠️ No sample PDF found in data/")


if __name__ == "__main__":
    test_pdf_extraction()
