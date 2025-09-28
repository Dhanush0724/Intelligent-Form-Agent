# Intelligent Form Agent – Read, Extract, and Explain

## Overview
The **Intelligent Form Agent** is a Python-based tool that automatically processes and understands forms. It can:  
- Extract structured fields (e.g., name, date of birth, address) from forms.  
- Answer questions related to individual forms using a QA pipeline.  
- Generate concise summaries of forms.  
- Provide holistic insights across multiple forms.

---

## Setup

### 1. Clone the repository
```bash
git clone <repository_url>
cd Agent
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate
```
## 3. Install dependencies
``` bash
pip install -r requirements.txt
```
### Usage
## 1. Extract and Summarize a Single Form
python tests/test_extractor.py
python tests/test_summarizer.py

## 2. Run Question Answering (QA) on a Form
python tests/test_qa.py

## 3. Multi-Form Insights
python tests/test_insights.py

Example Queries & Outputs
Example 1 – Single Form QA

Question: What is the applicant's name?
Answer: Dhanush V

Example 2 – Summarization with Structured Fields

Input: Full form text
Output:

{
  "extracted_fields": {
    "name": "Dhanush V",
    "dob": "27/09/2025",
    "address": "Bangalore"
  },
  "summary": "Name: Dhanush V. Date: 27/09/2025 Address: Bangalore Generated with https://kome.ai"
}


Screenshot / log placeholder:


Example 3 – Multi-Form Insights

### Insight Summary:

Total forms processed: 3
Most common city: Bangalore
DOB range: 1990–2025
Average year of birth: 2004
Names: Dhanush V, Kiran R, John Doe
Addresses: Bangalore
Holistic Summary:
The most common city is Bangalore. The birth years range from 1990 to 2025, with an average year of birth around 2004. Across 3 forms, the applicants include: Dhanush V, Kiran R, John Doe.

Screenshot / log placeholder:


Optional Design Notes

Pipeline Overview:
Extraction: pdfplumber for digital text extraction with OCR fallback using pytesseract.
Structured Fields: Regex-based extraction of key fields (name, DOB, address, email, phone).
QA: Hugging Face transformers (distilbert-base-uncased-distilled-squad) for answering questions.
Summarization: Chunk-based summarization using facebook/bart-large-cnn.
Multi-Form Insights: Aggregates multiple forms and generates holistic statistics and summaries.
Architecture diagram placeholder:


Notes

Ensure all sample PDFs are placed in the /data directory.
Logs and outputs can be found in /tests when running test scripts.
Creative extensions such as UI or advanced reasoning modules can be added in /src/extensions with proper documentation.
