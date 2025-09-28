"""
Simple extractor: tries text extraction with pdfplumber and falls back to OCR via pdf2image + pytesseract.
Also provides a tiny `extract_structured_fields` using regexes for common fields (name, email, phone, dob).
"""
import re
from typing import Dict, Optional
import pdfplumber


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


def extract_structured_fields(text: str) -> dict:
    """Enhanced regex-based extraction for common fields."""
    fields = {"name": None, "email": None, "phone": None, "dob": None, "address": None}

    # Email
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if m:
        fields["email"] = m.group(0)

    # Phone (simple international/local)
    m = re.search(r"(\+?\d[\d\-\s]{7,}\d)", text)
    if m:
        fields["phone"] = m.group(0)

    # DOB (common patterns)
    m = re.search(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", text)
    if m:
        fields["dob"] = m.group(0)

    # Name: lines starting with Name:, Applicant:, Full Name:
    m = re.search(r"(?:Name|Applicant|Full Name)[:\s]+([A-Z][A-Za-z ,.'-]{2,100})", text)
    if m:
        fields["name"] = m.group(1).strip()

    # Address: lines starting with Address:, Location:, Residence:
    m = re.search(r"(?:Address|Location|Residence)[:\s]+(.{3,200})", text)
    if m:
        fields["address"] = m.group(1).strip()

    return fields

