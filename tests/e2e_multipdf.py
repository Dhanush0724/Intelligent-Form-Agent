import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor
from src.qa_agent import FormQA
from src.summarizer import FormSummarizer


def run_pipeline(pdf_path: str):
    print(f"\n=== Processing: {pdf_path} ===")
    if not os.path.exists(pdf_path):
        print("⚠️ File not found.")
        return

    # Step 1: Extract text
    text = extractor.extract_text_from_pdf(pdf_path)
    print("\n--- Extracted Text ---")
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


def test_multiple_forms():
    data_dir = "data"
    sample_files = ["sample_form1.pdf", "sample_form2.pdf", "sample_form3.pdf"]
    for fname in sample_files:
        run_pipeline(os.path.join(data_dir, fname))


if __name__ == "__main__":
    test_multiple_forms()
