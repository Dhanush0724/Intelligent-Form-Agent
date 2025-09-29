

import re
import pdfplumber
from typing import Dict

def extract_text_from_pdf(path: str) -> str:
    """Try digital text extraction first; if empty, fall back to OCR pages."""
    text_parts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
    except Exception as e:
        raise

    text = "\n\n".join(p for p in text_parts if p)
    if text.strip():
        return text

    # fallback: OCR using pdf2image + pytesseract
    try:
        from pdf2image import convert_from_path
        import pytesseract

        images = convert_from_path(path, dpi=200)
        ocr_text = []
        for im in images:
            ocr_text.append(pytesseract.image_to_string(im))
        return "\n\n".join(ocr_text)
    except Exception as e:
        raise RuntimeError("Failed to extract text (pdfplumber + OCR fallback failed): " + str(e))


def normalize_text(text: str) -> str:
    """Basic cleanup"""
    return re.sub(r"\s+", " ", text).strip()


def extract_fields(text: str) -> Dict[str, str]:
    fields = {
        "name": None, "email": None, "phone": None, "dob": None, "address": None,
        "current_role": None, "reason_for_applying": None, "comments": None
    }

    # Structured field patterns (same as before)...
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if m: fields["email"] = m.group(0)

    m = re.search(r"(\+?\d[\d\-\s]{7,}\d)", text)
    if m: fields["phone"] = m.group(0)

    m = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", text)
    if m: fields["dob"] = m.group(0)

    m = re.search(r"(?:Name|Applicant|Full Name)[:\s]+([A-Z][A-Za-z ,.'-]{2,100})", text)
    if m: fields["name"] = m.group(1).strip()

    m = re.search(r"(?:Address|Location|Residence)[:\s]+(.{3,200})", text)
    if m: fields["address"] = m.group(1).strip()

    # 🔹 Unstructured fallback patterns
    m = re.search(r"I[, ]+\s*([A-Z][A-Za-z ]+)\s*,\s*born", text, re.IGNORECASE)
    if m: fields["name"] = m.group(1).strip()

    m = re.search(r"born on\s+(\d{1,2}\s+[A-Za-z]+\s+\d{4})", text, re.IGNORECASE)
    if m: fields["dob"] = m.group(1).strip()

    m = re.search(r"(?:reside|living) at\s+([A-Za-z ,]+)", text, re.IGNORECASE)
    if m: fields["address"] = m.group(1).strip()

    # Unstructured extras (optional, if text has them)
    patterns = {
        "current_role": r"(?:currently working as|my role is)\s+([A-Za-z ]+)",
        "reason_for_applying": r"(?:because|reason.*apply is)\s+([^.]+)",
        "comments": r"(?:note|comment|remark)[:\s]+(.+)",
    }
    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m: fields[key] = m.group(1).strip()

    return fields



if __name__ == "__main__":
    pdf_path = "form.pdf"  # Replace with your file
    raw_text = extract_text_from_pdf(pdf_path)
    clean_text = normalize_text(raw_text)

    fields = extract_fields(clean_text)
    print("Extracted fields:", fields)

