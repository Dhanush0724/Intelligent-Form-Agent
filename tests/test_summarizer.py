import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src import extractor
from src.summarizer import FormSummarizer

def test_chunk_summarization():
    pdf_path = "data/sample_form.pdf"
    if not os.path.exists(pdf_path):
        print("⚠️ Sample PDF not found.")
        return

    
    text = extractor.extract_text_from_pdf(pdf_path)
    
    
    summarizer = FormSummarizer()
    
    
    summary = summarizer.summarize(text)
    print("\n--- Chunk-based Form Summary ---\n")
    print(summary)

if __name__ == "__main__":
    test_chunk_summarization()
