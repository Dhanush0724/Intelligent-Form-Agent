"""
Chunk-based summarization using transformers pipeline.
"""
from transformers import pipeline

SUM_MODEL = "facebook/bart-large-cnn"


class FormSummarizer:
    def __init__(self):
        # Load summarization pipeline once
        self.summarizer = pipeline("summarization", model=SUM_MODEL, device=-1)

    def summarize(self, text: str, max_chunk_chars: int = 4000) -> str:
        """
        Summarizes the given text using a chunk-based approach.

        Args:
            text (str): The text to summarize.
            max_chunk_chars (int): Maximum number of characters per chunk.

        Returns:
            str: The summarized text.
        """
        # Split text into chunks
        chunks = [text[i: i + max_chunk_chars] for i in range(0, len(text), max_chunk_chars)]
        summaries = []

        # Summarize each chunk
        for c in chunks:
            s = self.summarizer(c, max_length=130, min_length=30, do_sample=False)
            summaries.append(s[0]["summary_text"].strip())

        # Combine summaries and summarize again if multiple chunks
        if len(summaries) == 1:
            return summaries[0]
        combined = "\n".join(summaries)
        final = self.summarizer(combined, max_length=150, min_length=40, do_sample=False)
        return final[0]["summary_text"].strip()
