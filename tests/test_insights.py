# tests/test_insights.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extractor import extract_text_from_pdf, extract_structured_fields
from src.summarizer import FormSummarizer
from src.insights import MultiFormInsights

# Sample PDF files
pdf_files = [
    "data/sample_form1.pdf",
    "data/sample_form2.pdf",
    "data/sample_form3.pdf"
]

def test_multi_form_insights():
    summarizer = FormSummarizer()
    multi_insights = MultiFormInsights()

    extracted_fields_list = []

    for pdf_path in pdf_files:
        print(f"\n=== Processing: {pdf_path} ===\n")
        text = extract_text_from_pdf(pdf_path)
        fields = extract_structured_fields(text)
        summary = summarizer.summarize(text)
        extracted_fields_list.append(fields)
        print("Extracted Fields:", fields)
        print("Summary:", summary, "\n")

    # Generate multi-form insights
    insights = multi_insights.process_forms(extracted_fields_list)
    print("\n=== Multi-Form Insights ===")
    print("Total Forms Processed:", insights["total_forms"])
    print("Most Common City:", insights["most_common_city"])
    print("DOB Range:", insights["dob_range"])
    print("Average Year of Birth:", insights["average_year"])
    print("All Names:", insights["all_names"])
    print("All Addresses:", insights["all_addresses"])
    print("\nHolistic Summary:\n", insights["holistic_summary"])

if __name__ == "__main__":
    test_multi_form_insights()
