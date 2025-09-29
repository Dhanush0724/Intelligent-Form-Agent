
from transformers import pipeline
import re

SUM_MODEL = "facebook/bart-large-cnn"


class FormSummarizer:
    def __init__(self):
        # Load summarization pipeline once
        self.summarizer = pipeline("summarization", model=SUM_MODEL, device=-1)

    def extract_fields(self, text: str) -> dict:
        
        fields = {}

       
        name_match = re.search(r"(?:Name|Applicant|Full\s*Name)\s*:\s*([^\n:]+)", text, re.IGNORECASE)

        fields["name"] = name_match.group(1).strip() if name_match else None

        
        dob_match = re.search(r"(?:DOB|Date\s*of\s*Birth|Birthdate|Date)[:\s]+(\d{2}/\d{2}/\d{4})", text, re.IGNORECASE)
        fields["dob"] = dob_match.group(1).strip() if dob_match else None

       
        address_match = re.search(r"(?:Address|Location|Residence)[:\s]+(.+)", text, re.IGNORECASE)
        fields["address"] = address_match.group(1).strip() if address_match else None

        return fields


    def summarize(self, text: str, max_chunk_chars: int = 4000) -> str:
       
        chunks = [text[i: i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
        summaries = []

        
        for c in chunks:
            s = self.summarizer(c, max_length=130, min_length=30, do_sample=False)
            summaries.append(s[0]["summary_text"].strip())

        
        if len(summaries) == 1:
            return summaries[0]
        combined = "\n".join(summaries)
        final = self.summarizer(combined, max_length=150, min_length=40, do_sample=False)
        return final[0]["summary_text"].strip()

    def summarize_with_fields(self, text: str) -> dict:
        
        fields = self.extract_fields(text)
        summary = self.summarize(text)
        return {
            "extracted_fields": fields,
            "summary": summary
        }
