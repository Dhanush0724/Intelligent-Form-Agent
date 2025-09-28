"""
Chunk-based summarization using transformers pipeline with structured field extraction.
"""
from transformers import pipeline
import re

SUM_MODEL = "facebook/bart-large-cnn"


class FormSummarizer:
    def __init__(self):
        # Load summarization pipeline once
        self.summarizer = pipeline("summarization", model=SUM_MODEL, device=-1)

    def extract_fields(self, text: str) -> dict:
        """
        Extracts structured fields like name, date of birth, and address from the text.
        Handles multiple common label variations.
        """
        fields = {}

        # --- Name: can be "Name", "Applicant", "Full Name"
        name_match = re.search(r"(?:Name|Applicant|Full\s*Name)\s*:\s*([^\n:]+)", text, re.IGNORECASE)

        fields["name"] = name_match.group(1).strip() if name_match else None

        # --- DOB: can be "DOB", "Date of Birth", "Birthdate", "Date"
        dob_match = re.search(r"(?:DOB|Date\s*of\s*Birth|Birthdate|Date)[:\s]+(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
        fields["dob"] = dob_match.group(1).strip() if dob_match else None

        # --- Address: can be "Address", "Location", "Residence"
        address_match = re.search(r"(?:Address|Location|Residence)[:\s]+(.+)", text, re.IGNORECASE)
        fields["address"] = address_match.group(1).strip() if address_match else None

        return fields


    def summarize(self, text: str, max_chunk_chars: int = 4000) -> str:
        """
        Summarizes the given text using a chunk-based approach.
        """
        # Split text into chunks
        chunks = [text[i: i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
        summaries = []

        # Summarize each chunk
        for c in chunks:
            s = self.summarizer(c, max_length=130, min_length=30, do_sample=False)
            summaries.append(s[0]["summary_text"].strip())

        # Combine summaries if multiple chunks
        if len(summaries) == 1:
            return summaries[0]
        combined = "\n".join(summaries)
        final = self.summarizer(combined, max_length=150, min_length=40, do_sample=False)
        return final[0]["summary_text"].strip()

    def summarize_with_fields(self, text: str) -> dict:
        """
        Returns both structured fields and the summary in JSON format.
        """
        fields = self.extract_fields(text)
        summary = self.summarize(text)
        return {
            "extracted_fields": fields,
            "summary": summary
        }
