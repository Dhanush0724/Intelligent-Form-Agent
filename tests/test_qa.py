import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor
from src.qa_agent import FormQA

def test_form_qa():
    pdf_path = "data/sample_un.pdf"
    if not os.path.exists(pdf_path):
        print("⚠️ Sample PDF not found.")
        return

    # Extract text from PDF
    text = extractor.extract_text_from_pdf(pdf_path)
    
    # Initialize QA agent
    qa = FormQA()

    # Ask questions
    questions = ["What is the name?", "What is the date of birth?", "What is the address?"]
    for q in questions:
        ans = qa.answer_question(text, q)
        print(f"Q: {q}\nA: {ans}\n")

if __name__ == "__main__":
    test_form_qa()
