"""
Chunk-based summarization using transformers pipeline.
"""
from transformers import pipeline

SUM_MODEL = "facebook/bart-large-cnn"


def summarize_text(text: str, max_chunk_chars: int = 4000) -> str:
    summarizer = pipeline("summarization", model=SUM_MODEL, device=-1)
    # naive chunk by characters
    chunks = [text[i: i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
    summaries = []
    for c in chunks:
        s = summarizer(c, max_length=130, min_length=30, do_sample=False)
        summaries.append(s[0]["summary_text"].strip())

    # combine summaries and summarize again if multiple
    if len(summaries) == 1:
        return summaries[0]
    combined = "\n".join(summaries)
    final = summarizer(combined, max_length=150, min_length=40, do_sample=False)
    return final[0]["summary_text"].strip()
