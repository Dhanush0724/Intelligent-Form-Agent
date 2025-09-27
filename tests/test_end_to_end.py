import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor
from src.qa_agent import FormQA
from src.summarizer import FormSummarizer
import json

def test_end_to_end():
    pdf_path = "data/sample_form.pdf"

    if not os.path.exists(pdf_path):
        print("⚠️ Sample PDF not found.")
        return

    # Step 1: Extract text from PDF
    print("\n--- Extracting Text ---")
    text = extractor.extract_text_from_pdf(pdf_path)
    print(text)

    # Step 2: QA
    print("\n--- Question Answering ---")
    qa_agent = FormQA()
    questions = [
        "What is the name?",
        "What is the date of birth?",
        "What is the address?"
    ]
    for q in questions:
        answer = qa_agent.answer_question(text, q)
        print(f"Q: {q}\nA: {answer}\n")

    # Step 3: Summarization with structured fields
    print("\n--- Summarization with Structured Fields ---")
    summarizer = FormSummarizer()
    result = summarizer.summarize_with_fields(text)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    test_end_to_end()
