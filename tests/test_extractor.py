import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor  # import functions

def test_pdf_extraction():
    pdf_path = "data/sample_form.pdf"
    print(f"Looking for PDF at: {os.path.abspath(pdf_path)}")
    if os.path.exists(pdf_path):
        text = extractor.extract_text_from_pdf(pdf_path)
        norm_text = extractor.normalize_text(text)
        fields = extractor.extract_structured_fields(norm_text)
        print("\n--- Extracted PDF Text ---\n")
        print(norm_text)
        print("\n--- Extracted Fields ---\n")
        for k, v in fields.items():
            print(f"{k}: {v}")
    else:
        print("⚠️ No sample PDF found in data/")

def test_image_extraction():
    image_path = "data/sample_form.png"
    print(f"Looking for Image at: {os.path.abspath(image_path)}")
    if os.path.exists(image_path):
        text = extractor.extract_text_from_image(image_path)  # use OCR function
        norm_text = extractor.normalize_text(text)
        fields = extractor.extract_structured_fields(norm_text)
        print("\n--- Extracted Image Text ---\n")
        print(norm_text)
        print("\n--- Extracted Fields ---\n")
        for k, v in fields.items():
            print(f"{k}: {v}")
    else:
        print("⚠️ No sample image found in data/")

if __name__ == "__main__":
    test_pdf_extraction()
    test_image_extraction()
