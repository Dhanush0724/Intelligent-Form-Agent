"""
Tiny CLI demonstrating extract / summarize / qa flows.
"""
import argparse
from pathlib import Path

from src import extractor, qa_module, summarizer


def cmd_extract(path: str):
    txt = extractor.extract_text_from_pdf(path)
    norm = extractor.normalize_text(txt)
    fields = extractor.extract_structured_fields(norm)
    print("--- Extracted fields ---")
    for k, v in fields.items():
        print(f"{k}: {v}")
    out = Path(path).with_suffix(".txt")
    out.write_text(norm)
    print(f"Full normalized text saved to: {out}")


def cmd_summarize(path: str):
    txt = Path(path).read_text()
    s = summarizer.summarize_text(txt)
    print("--- Summary ---")
    print(s)


def cmd_qa(path: str, question: str):
    txt = Path(path).read_text()
    ans = qa_module.answer_with_retrieval(question, txt)
    print("--- QA Results (retrieved contexts) ---")
    for i, c in enumerate(ans["answers"], 1):
        print(f"[{i}] ({ans['hits'][i-1][1]:.3f})\n{c}\n---\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["extract", "summarize", "qa"], required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--question", default=None)
    args = parser.parse_args()

    if args.mode == "extract":
        cmd_extract(args.file)
    elif args.mode == "summarize":
        cmd_summarize(args.file)
    elif args.mode == "qa":
        if not args.question:
            raise SystemExit("--question is required for qa mode")
        cmd_qa(args.file, args.question)


if __name__ == "__main__":
    main()
