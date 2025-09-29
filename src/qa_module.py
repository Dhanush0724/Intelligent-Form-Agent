
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i: i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks


class Retriever:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.embeddings = None
        self.docs = []

    def build(self, docs: List[str]):
        self.docs = docs
        embs = self.model.encode(docs, show_progress_bar=True, convert_to_numpy=True)
        self.embeddings = embs.astype("float32")
        d = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(d)
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

    def query(self, q: str, top_k: int = 3) -> List[Tuple[int, float]]:
        q_emb = self.model.encode([q], convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, top_k)
        return [(int(i), float(D[0][idx])) for idx, i in enumerate(I[0]) if i != -1]


def answer_with_retrieval(question: str, text: str) -> Dict[str, Any]:
    chunks = chunk_text(text)
    r = Retriever()
    r.build(chunks)
    hits = r.query(question, top_k=3)
    contexts = [chunks[idx] for idx, _ in hits]
    return {"question": question, "answers": contexts, "hits": hits}
